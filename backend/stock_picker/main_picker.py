"""
main_picker.py — 一鍵執行：爬取 → 篩選 → 分析 → 輸出

用法：
  python main_picker.py

環境變數：
  FINMIND_TOKEN      必填
  ANTHROPIC_API_KEY  必填
"""

import os
import sys
from crawler import fetch_cnyes_news, fetch_stock_name
from finmind_filter import run_filter
from generator import run as generate_html


def main():
    # 環境變數檢查
    if not os.environ.get("FINMIND_TOKEN"):
        print("❌ 請設定 FINMIND_TOKEN")
        sys.exit(1)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ 請設定 ANTHROPIC_API_KEY")
        sys.exit(1)

    print("=" * 50)
    print("🔍 低基期選股生成器 啟動")
    print("=" * 50)

    # ── Step 1：抓鉅亨新聞，萃取候選代號 ──
    print("\n[Step 1] 爬取鉅亨 RSS 新聞...")
    news_list = fetch_cnyes_news(max_items=100)

    # 從新聞萃取所有出現過的股票代號
    all_codes = []
    for n in news_list:
        for c in n["codes"]:
            if c not in all_codes:
                all_codes.append(c)

    print(f"  → 共萃取到 {len(all_codes)} 個候選代號：{all_codes[:10]}{'...' if len(all_codes)>10 else ''}")

    if not all_codes:
        print("⚠️ 沒有從新聞中找到任何股票代號，流程結束")
        sys.exit(0)

    # ── Step 2：數值篩選 ──
    print(f"\n[Step 2] 數值篩選（回檔/法人/量能）...")
    filtered = run_filter(all_codes, news_list, max_results=20, delay=1.2)

    if not filtered:
        print("⚠️ 沒有股票通過篩選條件，流程結束")
        sys.exit(0)

    # 補上股票名稱
    print("\n[Step 2.5] 補充股票名稱...")
    for stock in filtered:
        stock["name"] = fetch_stock_name(stock["stock_id"])

    # ── Step 3：Claude 評分 + 輸出 HTML ──
    print(f"\n[Step 3] Claude API 分析 + 產出 HTML（共 {len(filtered)} 檔）...")
    output_path = generate_html(filtered, api_delay=2.0)

    print("\n" + "=" * 50)
    print(f"✅ 完成！輸出檔案：{output_path}")
    print(f"   同時更新：{output_path.replace(output_path.split('/')[-1], 'latest.html')}")
    print("=" * 50)


def run_full_scan():
    """全台股掃描：逐一分析均線/趨勢/K線型態，輸出 scan_result.html"""
    import time as _time
    from crawler import get_all_tw_stocks, fetch_price_history, fetch_stock_name
    from finmind_filter import detect_kline_patterns
    from generator import generate_scan_result

    print("[scan] 取得全台股票列表...")
    all_stocks = get_all_tw_stocks()
    if not all_stocks:
        print("[scan] ❌ 無法取得股票列表，請確認 FINMIND_TOKEN")
        return None

    batch = all_stocks[:500]
    print(f"[scan] 開始掃描 {len(batch)} 檔（每檔間隔 0.4s）...")

    results = []
    for i, sid in enumerate(batch, 1):
        try:
            prices = fetch_price_history(sid, days=70)
            if len(prices) < 20:
                continue

            closes  = [p["close"]  for p in prices]
            opens   = [p["open"]   for p in prices]
            highs   = [p["high"]   for p in prices]
            lows    = [p["low"]    for p in prices]
            volumes = [p["volume"] for p in prices]

            price = closes[-1]
            if price < 10:
                continue

            n60  = min(60, len(closes))
            ma5  = sum(closes[-5:]) / 5
            ma20 = sum(closes[-20:]) / 20
            ma60 = sum(closes[-n60:]) / n60

            support    = min(lows[-20:])
            resistance = max(highs[-20:])

            if ma5 > ma20 > ma60:
                trend = "多頭"
            elif ma5 < ma20 < ma60:
                trend = "空頭"
            else:
                trend = "整理"

            if trend == "多頭" and price > ma60:
                risk_level = "low"
            elif trend == "空頭" or price < ma60 * 0.95:
                risk_level = "high"
            else:
                risk_level = "medium"

            kline_pattern, win_rate = detect_kline_patterns(closes, opens, highs, lows, volumes)

            risk     = max(price - support, 0.01)
            reward   = max(resistance - price, 0)
            rr_ratio = round(reward / risk, 2)

            results.append({
                "stock_id":      sid,
                "name":          "",
                "price":         price,
                "ma5":           round(ma5, 2),
                "ma20":          round(ma20, 2),
                "ma60":          round(ma60, 2),
                "support":       round(support, 2),
                "resistance":    round(resistance, 2),
                "trend":         trend,
                "risk_level":    risk_level,
                "kline_pattern": kline_pattern,
                "win_rate":      win_rate,
                "rr_ratio":      rr_ratio,
            })
        except Exception:
            pass

        if i % 50 == 0:
            print(f"[scan] 已處理 {i}/{len(batch)}，通過 {len(results)} 檔")
            _time.sleep(2)
        else:
            _time.sleep(0.4)

    print(f"[scan] 掃描完畢：{len(results)} 檔通過（共 {len(batch)} 檔）")
    if not results:
        print("[scan] ⚠️ 無結果，跳過輸出")
        return None

    for s in results:
        try:
            s["name"] = fetch_stock_name(s["stock_id"])
        except Exception:
            pass

    return generate_scan_result(results)


def run_unified_scan():
    """統合選股：全台掃描 + 新聞選股 → 同時輸出 scan_result.html + latest.html"""
    import time as _time
    from crawler import (get_all_tw_stocks, fetch_price_history, fetch_stock_name,
                         fetch_cnyes_news, fetch_institutional)
    from finmind_filter import detect_kline_patterns, run_filter
    from generator import generate_picks_html, generate_scan_result

    print("[unified] === 統合選股開始 ===")

    # ── Step 1：全台股掃描 ──
    print("[unified] 取得全台股票列表...")
    all_stocks = get_all_tw_stocks()
    if not all_stocks:
        print("[unified] ❌ 無法取得股票列表")
        return

    batch = all_stocks[:500]
    print(f"[unified] 開始掃描 {len(batch)} 檔...")
    scan_results = []
    for i, sid in enumerate(batch, 1):
        try:
            prices = fetch_price_history(sid, days=70)
            if len(prices) < 20:
                continue
            closes  = [p["close"]  for p in prices]
            opens   = [p["open"]   for p in prices]
            highs   = [p["high"]   for p in prices]
            lows    = [p["low"]    for p in prices]
            volumes = [p["volume"] for p in prices]
            price = closes[-1]
            if price < 10:
                continue
            n60  = min(60, len(closes))
            ma5  = sum(closes[-5:]) / 5
            ma20 = sum(closes[-20:]) / 20
            ma60 = sum(closes[-n60:]) / n60
            support    = min(lows[-20:])
            resistance = max(highs[-20:])
            if ma5 > ma20 > ma60:
                trend = "多頭"
            elif ma5 < ma20 < ma60:
                trend = "空頭"
            else:
                trend = "整理"
            if trend == "多頭" and price > ma60:
                risk_level = "low"
            elif trend == "空頭" or price < ma60 * 0.95:
                risk_level = "high"
            else:
                risk_level = "medium"
            kline_pattern, win_rate = detect_kline_patterns(closes, opens, highs, lows, volumes)
            risk   = max(price - support, 0.01)
            reward = max(resistance - price, 0)
            scan_results.append({
                "stock_id":      sid,
                "name":          "",
                "price":         price,
                "ma5":           round(ma5, 2),
                "ma20":          round(ma20, 2),
                "ma60":          round(ma60, 2),
                "support":       round(support, 2),
                "resistance":    round(resistance, 2),
                "trend":         trend,
                "risk_level":    risk_level,
                "kline_pattern": kline_pattern,
                "win_rate":      win_rate,
                "rr_ratio":      round(reward / risk, 2),
            })
        except Exception:
            pass
        if i % 50 == 0:
            print(f"[unified] 掃描進度 {i}/{len(batch)}，通過 {len(scan_results)} 檔")
            _time.sleep(2)
        else:
            _time.sleep(0.4)

    print(f"[unified] 全台掃描完畢：{len(scan_results)} 檔")
    if scan_results:
        for s in scan_results:
            try:
                s["name"] = fetch_stock_name(s["stock_id"])
            except Exception:
                pass
        generate_scan_result(scan_results)

    # ── Step 2：新聞選股 ──
    print("[unified] 爬取鉅亨新聞...")
    news_list = fetch_cnyes_news(max_items=100)
    all_codes = []
    for n in news_list:
        for c in n["codes"]:
            if c not in all_codes:
                all_codes.append(c)
    print(f"[unified] 新聞候選代號：{len(all_codes)} 個")

    if not all_codes:
        print("[unified] ⚠️ 無新聞候選代號，跳過選股")
        return

    filtered = run_filter(all_codes, news_list, max_results=20, delay=1.2)
    if not filtered:
        print("[unified] ⚠️ 無股票通過篩選")
        return

    for stock in filtered:
        stock["name"] = fetch_stock_name(stock["stock_id"])

    output_path = generate_picks_html(filtered)
    print(f"[unified] === 統合選股完成：{output_path} ===")


if __name__ == "__main__":
    if "--schedule" in sys.argv:
        from scheduler import main as schedule_main
        schedule_main()
    elif "--unified" in sys.argv:
        run_unified_scan()
    else:
        main()
