"""
main_picker.py — 一鍵執行：爬取 → 篩選 → 分析 → 輸出

選股流程（低 FinMind 用量版）：
  Step 1  鉅亨 RSS 近一週新聞 → 萃取股票代號（不打 FinMind）
  Step 2  TWSE STOCK_DAY_ALL 成交量前 100（不打 FinMind）
  Step 3  兩者交集優先合併，縮小到 ≤50 支候選
  Step 4  只對 ≤50 支打 FinMind 做技術分析（MA/KD/MACD）
目標：每次選股 FinMind 用量從 500 次降到 50 次以內

環境變數：
  FINMIND_TOKEN      必填（僅用於技術分析，不用於候選篩選）
  ANTHROPIC_API_KEY  選填（generator 若有 AI 評分則需要）
"""

import os
import sys


def main():
    if not os.environ.get("FINMIND_TOKEN"):
        print("❌ 請設定 FINMIND_TOKEN")
        sys.exit(1)

    from crawler import (fetch_cnyes_news, fetch_twse_volume_top,
                          build_candidates, fetch_stock_name)
    from finmind_filter import run_filter
    from generator import run as generate_html

    print("=" * 55)
    print("🔍 低基期選股生成器 啟動（低用量版）")
    print("=" * 55)

    # ── Step 1：鉅亨近一週新聞 ──
    print("\n[Step 1] 爬取鉅亨 RSS 新聞（近7天）...")
    news_list  = fetch_cnyes_news(max_items=300, days=7)
    news_codes = _dedup_codes(news_list)
    print(f"  → 新聞萃取 {len(news_codes)} 個候選代號")

    # ── Step 2：TWSE 成交量排行前 100 ──
    print("\n[Step 2] 抓取 TWSE 成交量排行前 100（不打 FinMind）...")
    volume_ids, name_dict = fetch_twse_volume_top(100)

    # ── Step 3：合併候選清單（≤50）──
    print("\n[Step 3] 合併候選清單...")
    candidates = build_candidates(news_codes, volume_ids, max_candidates=50)
    if not candidates:
        print("⚠️ 無候選股票，流程結束")
        sys.exit(0)
    print(f"  → 最終候選 {len(candidates)} 支：{candidates[:8]}{'...' if len(candidates)>8 else ''}")

    # ── Step 4：FinMind 技術分析（≤50 支）──
    print(f"\n[Step 4] FinMind 技術分析（{len(candidates)} 支，預估用量 ≤{len(candidates)*2} 次）...")
    filtered = run_filter(candidates, news_list, max_results=20, delay=1.0)

    if not filtered:
        print("⚠️ 無股票通過篩選條件，流程結束")
        sys.exit(0)

    # 補名稱（優先 TWSE name_dict，減少 FinMind 呼叫）
    print("\n[Step 4.5] 補充股票名稱...")
    for stock in filtered:
        sid = stock["stock_id"]
        stock["name"] = name_dict.get(sid) or fetch_stock_name(sid)

    # ── Step 5：輸出 HTML ──
    print(f"\n[Step 5] 產出 HTML（共 {len(filtered)} 檔）...")
    output_path = generate_html(filtered, api_delay=2.0)

    print("\n" + "=" * 55)
    print(f"✅ 完成！輸出：{output_path}")
    print("=" * 55)


def run_unified_scan(delay: float = 1.0) -> list[dict]:
    """
    統合選股主流程（低 FinMind 用量版）：被 scheduler / admin API 呼叫
    delay: FinMind 兩次呼叫間隔秒數（排程用 1.0，admin 手動觸發用 0.3）
    回傳 picks_list = [{"stock_id","stock_name","score","signals"}, ...]
    """
    from crawler import (fetch_cnyes_news, fetch_twse_volume_top,
                          build_candidates, fetch_stock_name)
    from finmind_filter import run_filter
    from generator import generate_picks_html

    print("[unified] === 統合選股開始（低用量版）===")

    # Step 1: 鉅亨近一週新聞
    print("[unified] Step 1: 爬取鉅亨 RSS（近7天，≤300則）...")
    news_list  = fetch_cnyes_news(max_items=300, days=7)
    news_codes = _dedup_codes(news_list)
    print(f"[unified]   → 新聞代號 {len(news_codes)} 個")

    # Step 2: TWSE 成交量排行前 100
    print("[unified] Step 2: TWSE 成交量排行（不打 FinMind）...")
    volume_ids, name_dict = fetch_twse_volume_top(100)

    # Step 3: 合併候選（≤50）
    print("[unified] Step 3: 合併候選清單（≤50）...")
    candidates = build_candidates(news_codes, volume_ids, max_candidates=50)
    if not candidates:
        print("[unified] ⚠️ 無候選股票，流程結束")
        return []

    # Step 4: FinMind 技術分析
    print(f"[unified] Step 4: FinMind 技術分析（{len(candidates)} 支，delay={delay}s）...")
    filtered = run_filter(candidates, news_list, max_results=20, delay=delay)
    if not filtered:
        print("[unified] ⚠️ 無股票通過篩選，流程結束")
        return []

    # 補名稱
    for stock in filtered:
        sid = stock["stock_id"]
        stock["name"] = name_dict.get(sid) or fetch_stock_name(sid)

    output_path, picks_list = generate_picks_html(filtered)
    print(f"[unified] === 統合選股完成：{output_path}，{len(picks_list)} 支入選 ===")
    return picks_list


# ──────────────────────────────────────────
# 舊版全台掃描（保留但不主動呼叫，FinMind 用量大）
# ──────────────────────────────────────────

def run_full_scan():
    """全台股掃描（已停用，改用 run_unified_scan）"""
    print("[scan] ⚠️ run_full_scan 已停用，請改用 run_unified_scan（低用量版）")


# ──────────────────────────────────────────
# 工具函式
# ──────────────────────────────────────────

def _dedup_codes(news_list: list[dict]) -> list[str]:
    """從新聞列表萃取不重複的股票代號（依首次出現順序）"""
    seen: set[str] = set()
    result: list[str] = []
    for n in news_list:
        for c in n.get("codes", []):
            if c not in seen:
                seen.add(c)
                result.append(c)
    return result


if __name__ == "__main__":
    if "--schedule" in sys.argv:
        from scheduler import main as schedule_main
        schedule_main()
    else:
        main()
