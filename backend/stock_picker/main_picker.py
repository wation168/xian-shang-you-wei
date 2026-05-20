"""
main_picker.py — 一鍵執行：爬取 → 分析 → 輸出

選股流程（SEO 熱門股模式）：
  Step 1  TWSE STOCK_DAY_ALL 成交量前 30（不打 FinMind）
  Step 2  對全部 30 支打 FinMind 做技術分析（MA/KD/MACD/法人）
  Step 3  依 20 日均量降序輸出（確保主流大量股排前面）

環境變數：
  FINMIND_TOKEN  必填
"""

import os
import sys


def main():
    if not os.environ.get("FINMIND_TOKEN"):
        print("❌ 請設定 FINMIND_TOKEN")
        sys.exit(1)

    from crawler import fetch_twse_volume_top, fetch_stock_name
    from finmind_filter import run_filter
    from generator import run as generate_html

    print("=" * 55)
    print("🔍 選股生成器 啟動（SEO 熱門股模式）")
    print("=" * 55)

    # ── Step 1：TWSE 成交量前 30 ──
    print("\n[Step 1] 抓取 TWSE 成交量排行前 30...")
    volume_ids, name_dict = fetch_twse_volume_top(30)
    if not volume_ids:
        print("⚠️ TWSE 資料取得失敗，流程結束")
        sys.exit(0)
    print(f"  → {volume_ids[:8]}{'...' if len(volume_ids)>8 else ''}")

    # ── Step 2：FinMind 技術分析（30 支）──
    print(f"\n[Step 2] FinMind 技術分析（{len(volume_ids)} 支）...")
    filtered = run_filter(volume_ids, max_results=30, delay=1.0)

    if not filtered:
        print("⚠️ 無股票通過資料門檻，流程結束")
        sys.exit(0)

    # 補名稱
    print("\n[Step 2.5] 補充股票名稱...")
    for stock in filtered:
        sid = stock["stock_id"]
        stock["name"] = name_dict.get(sid) or fetch_stock_name(sid)

    # ── Step 3：輸出 HTML ──
    print(f"\n[Step 3] 產出 HTML（共 {len(filtered)} 檔）...")
    output_path = generate_html(filtered, api_delay=2.0)

    print("\n" + "=" * 55)
    print(f"✅ 完成！輸出：{output_path}")
    print("=" * 55)


def run_unified_scan(delay: float = 1.0) -> list[dict]:
    """
    統合選股主流程（SEO 熱門股模式）：被 scheduler / admin API 呼叫
    直接取 TWSE 成交量前 30，全部做 FinMind 技術分析，依均量降序輸出。
    回傳 picks_list = [{"stock_id","stock_name","score","signals"}, ...]
    """
    from crawler import fetch_twse_volume_top, fetch_stock_name
    from finmind_filter import run_filter
    from generator import generate_picks_html

    print("[unified] === 統合選股開始（SEO 熱門股模式）===")

    # Step 1: TWSE 成交量前 30
    print("[unified] Step 1: TWSE 成交量排行前 30...")
    volume_ids, name_dict = fetch_twse_volume_top(30)
    if not volume_ids:
        print("[unified] ⚠️ TWSE 資料取得失敗，流程結束")
        return []
    print(f"[unified]   → {len(volume_ids)} 支：{volume_ids[:6]}...")

    # Step 2: FinMind 技術分析（全部 30 支）
    print(f"[unified] Step 2: FinMind 技術分析（{len(volume_ids)} 支，delay={delay}s）...")
    filtered = run_filter(volume_ids, max_results=30, delay=delay)
    if not filtered:
        print("[unified] ⚠️ 無股票通過資料門檻，流程結束")
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


if __name__ == "__main__":
    if "--schedule" in sys.argv:
        from scheduler import main as schedule_main
        schedule_main()
    else:
        main()
