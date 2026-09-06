"""
backtest_stop_rr.py — 分析引擎第三批回測：防守位隨乖離動態調整 + 損益比參數化(趨勢調節)

背景：
  main.py 的個股分析引擎（_do_analyze，約行 3717-3753）目前的「防守位」與「損益比」算法是：
    防守位：以支撐/軌道下緣為錨，夾在現價 -2%~-10% 之間的固定帶狀範圍，沒有考慮乖離率
    損益比：reward = 壓力 - 現價；risk = 現價 - 防守位；目標固定用壓力價，不因趨勢強弱調整

  這支腳本用真實歷史K線資料回測兩個候選改法，跟現有(baseline)算法比較，
  用實際"金叉+站上月線"訊號當進場點（跟深度選股用的同一套雙重確認邏輯一致，
  是這個codebase裡唯一已經在production使用、有明確定義的進場訊號，方便公平比較），
  往後模擬20個交易日，看「先碰到防守位出場」還是「先碰到目標出場」，統計勝率/期望值。

  候選A：防守位隨乖離率(現價偏離月線MA20的幅度)動態調整
    乖離 >=10%（過熱）→ 停損收緊到 -3%
    乖離 5%~10%（正常偏熱）→ 停損 -5%
    乖離 <5%（貼近月線，剛起漲）→ 停損放寬到 -8%
    （其餘沿用baseline的0.90~0.98外層防呆夾範圍）

  候選B：損益比參數化＋趨勢調節
    若MA20仍在上升（近5日MA20走高，代表多頭動能未鈍化）→ 目標價 = 壓力價 × 1.03（給多一點延伸空間）
    否則 → 目標價維持等於壓力價（不變）

  候選AB：A+B同時套用

⚠️ 重要說明（誠實揭露方法論限制，不是要假裝完美複製main.py）：
  1. 支撐/壓力用簡化版算法（近20日低點/近60日高點），不是main.py完整的軌道回歸算法，
     因為main.py不是設計成可以被外部腳本import的模組（有模組層級的DB初始化/token檢查等副作用）。
     這個簡化版跟finmind_filter.py深度選股用的support/resistance算法一致，這套已經在production跑。
  2. 進場價用訊號當天收盤價（隔天才能真正下單，這是常見回測簡化，不是要假裝當天就能成交）。
  3. 同一天內防守位跟目標價都被觸及時，保守認定「先觸及防守位」（不是要製造對baseline不利的假象，
     三個方案的模擬規則完全一致，這條規則對baseline/A/B/AB一視同仁）。
  4. 股票池是60檔常見的台股權值/中大型股，不是全市場，回測結果代表"這個樣本"的表現，
     不是"全市場保證"。

用法：
  1. 確保環境變數 FINMIND_TOKEN 已設定（跟main.py用同一個）
     Windows PowerShell：$env:FINMIND_TOKEN="你的token"
  2. python backtest_stop_rr.py
  3. 跑完後，把終端機印出的「=== 回測結果總表 ===」那段文字，還有產生的
     backtest_trades.csv 一起傳給Claude
  4. 全部60檔跑完視API速度大約10-20分鐘（每檔間隔0.35秒避免打爆FinMind）
"""

import json
import csv
import os
import sys
import time
import urllib.request
from datetime import date, timedelta

FINMIND_TOKEN = os.environ.get("FINMIND_TOKEN", "")
if not FINMIND_TOKEN:
    print("❌ 請先設定環境變數 FINMIND_TOKEN（跟 main.py 用同一個）")
    sys.exit(1)

# ── 股票池：60檔常見台股權值/中大型股，涵蓋電子/金融/傳產/航運/生技等產業 ──
UNIVERSE = [
    "2330", "2317", "2454", "2308", "2382", "2891", "2882", "2881", "2886", "2884",
    "2892", "2880", "1301", "1303", "1326", "2002", "2603", "2609", "2615", "3008",
    "2379", "3034", "2408", "2412", "3045", "4904", "2801", "2809", "5880", "2887",
    "1216", "1101", "1102", "2105", "9910", "2354", "2357", "2377", "2385", "2395",
    "3231", "2301", "2324", "3711", "6505", "2207", "9904", "2201", "2618", "2610",
    "5871", "2823", "2049", "6415", "3653", "3661", "6669", "2360", "2059", "2474",
]

START_DATE = "2022-06-01"
END_DATE = date.today().strftime("%Y-%m-%d")
FORWARD_DAYS = 20        # 模擬進場後往後看幾個交易日（跟deep_pick_log既有的20日追蹤慣例一致）
MA_CROSS_LOOKBACK_NONE = True  # 只抓「當天就是金叉那天」的訊號，不含lookback內較早的金叉（避免同一次金叉重複計入多筆訊號）


def fetch_prices(stock_id):
    url = (f"https://api.finmindtrade.com/api/v4/data"
           f"?dataset=TaiwanStockPrice&data_id={stock_id}"
           f"&start_date={START_DATE}&end_date={END_DATE}&token={FINMIND_TOKEN}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = json.loads(resp.read())
    except Exception as e:
        print(f"  [{stock_id}] 抓取失敗：{e}")
        return []
    if raw.get("status") != 200 or not raw.get("data"):
        return []
    rows = []
    for d in raw["data"]:
        try:
            o, h, l, c, v = float(d["open"]), float(d["max"]), float(d["min"]), float(d["close"]), float(d["Trading_Volume"])
        except (KeyError, TypeError, ValueError):
            continue
        if o <= 0 or h <= 0 or l <= 0 or c <= 0:
            continue
        rows.append({"date": d["date"], "open": o, "high": h, "low": l, "close": c, "volume": v})
    rows.sort(key=lambda r: r["date"])
    return rows


def sma(values, period):
    out = [None] * len(values)
    run = 0.0
    for i, v in enumerate(values):
        run += v
        if i >= period:
            run -= values[i - period]
        if i >= period - 1:
            out[i] = run / period
    return out


def find_signals(rows):
    """回傳訊號索引清單：MA20當天由下往上穿越MA60、且當天收盤價站上MA20"""
    closes = [r["close"] for r in rows]
    if len(closes) < 65:
        return []
    ma20 = sma(closes, 20)
    ma60 = sma(closes, 60)
    signals = []
    for i in range(1, len(closes)):
        if ma20[i] is None or ma60[i] is None or ma20[i - 1] is None or ma60[i - 1] is None:
            continue
        crossed = ma20[i - 1] <= ma60[i - 1] and ma20[i] > ma60[i]
        above_ma20 = closes[i] > ma20[i]
        if crossed and above_ma20:
            signals.append(i)
    return signals, ma20, ma60


def calc_baseline_stop_target(price, support, resistance):
    sup_dist_pct = (price - support) / price * 100
    if sup_dist_pct > 5:
        raw_stop = price * 0.95
    else:
        raw_stop = support * 0.985
    stop_nearest = price * 0.98
    stop_farthest = price * 0.90
    stop_loss = max(stop_farthest, min(raw_stop, stop_nearest))
    target1 = resistance if resistance > price else price * 1.08
    return round(stop_loss, 2), round(target1, 2)


def calc_candidate_a_stop(price, ma20_now):
    deviation_pct = (price - ma20_now) / ma20_now * 100
    if deviation_pct >= 10:
        stop_pct = 0.03
    elif deviation_pct >= 5:
        stop_pct = 0.05
    else:
        stop_pct = 0.08
    raw_stop = price * (1 - stop_pct)
    stop_loss = max(price * 0.90, min(raw_stop, price * 0.98))
    return round(stop_loss, 2)


def calc_candidate_b_target(price, resistance, ma20_now, ma20_5ago):
    target1 = resistance if resistance > price else price * 1.08
    trend_up = ma20_5ago is not None and ma20_now > ma20_5ago
    if trend_up:
        target1 = target1 * 1.03
    return round(target1, 2)


def simulate(rows, entry_idx, entry_price, stop_loss, target1):
    """往後最多FORWARD_DAYS個交易日，判斷先中停損還是先中目標；同天都中算停損（保守）"""
    end_idx = min(entry_idx + FORWARD_DAYS, len(rows) - 1)
    if end_idx <= entry_idx:
        return None  # 資料不足，排除
    outcome = "neither"
    exit_price = rows[end_idx]["close"]
    exit_days = end_idx - entry_idx
    for j in range(entry_idx + 1, end_idx + 1):
        low_j = rows[j]["low"]
        high_j = rows[j]["high"]
        if low_j <= stop_loss:
            outcome = "stopped"
            exit_price = stop_loss
            exit_days = j - entry_idx
            break
        if high_j >= target1:
            outcome = "target"
            exit_price = target1
            exit_days = j - entry_idx
            break
    ret_pct = round((exit_price - entry_price) / entry_price * 100, 2)
    return {"outcome": outcome, "exit_price": exit_price, "exit_days": exit_days, "ret_pct": ret_pct}


def summarize(label, trades):
    n = len(trades)
    if n == 0:
        print(f"{label}: 無有效交易")
        return
    wins = [t for t in trades if t["outcome"] == "target"]
    stops = [t for t in trades if t["outcome"] == "stopped"]
    neithers = [t for t in trades if t["outcome"] == "neither"]
    avg_ret = sum(t["ret_pct"] for t in trades) / n
    avg_days = sum(t["exit_days"] for t in trades) / n
    win_rate = len(wins) / n * 100
    stop_rate = len(stops) / n * 100
    print(f"{label:12s} | 樣本數 {n:4d} | 勝率(達標) {win_rate:5.1f}% | 停損率 {stop_rate:5.1f}% | "
          f"未到期 {len(neithers):4d} | 平均報酬 {avg_ret:+6.2f}% | 平均持有 {avg_days:4.1f}天")


def main():
    print(f"回測期間：{START_DATE} ~ {END_DATE}，股票池 {len(UNIVERSE)} 檔，往後追蹤 {FORWARD_DAYS} 個交易日")
    all_trades_baseline = []
    all_trades_a = []
    all_trades_b = []
    all_trades_ab = []
    csv_rows = []
    excluded_insufficient_data = 0

    for n, stock_id in enumerate(UNIVERSE, 1):
        print(f"[{n}/{len(UNIVERSE)}] {stock_id} ...", end=" ", flush=True)
        rows = fetch_prices(stock_id)
        if len(rows) < 80:
            print("資料不足，跳過")
            time.sleep(0.35)
            continue

        result = find_signals(rows)
        if not result:
            print("無金叉訊號")
            time.sleep(0.35)
            continue
        signals, ma20, ma60 = result

        closes = [r["close"] for r in rows]
        lows = [r["low"] for r in rows]
        highs = [r["high"] for r in rows]
        sig_count = 0

        for i in signals:
            if i < 60 or i + FORWARD_DAYS >= len(rows):
                excluded_insufficient_data += 1
                continue
            price = closes[i]
            support = min(lows[i - 19:i + 1])
            resistance = max(highs[i - 59:i + 1])
            ma20_now = ma20[i]
            ma20_5ago = ma20[i - 5] if i - 5 >= 0 else None

            stop_base, target_base = calc_baseline_stop_target(price, support, resistance)
            stop_a = calc_candidate_a_stop(price, ma20_now)
            target_b = calc_candidate_b_target(price, resistance, ma20_now, ma20_5ago)

            risk_base = price - stop_base
            risk_a = price - stop_a
            if risk_base <= 0 or risk_a <= 0:
                continue

            t_base = simulate(rows, i, price, stop_base, target_base)
            t_a = simulate(rows, i, price, stop_a, target_base)
            t_b = simulate(rows, i, price, stop_base, target_b)
            t_ab = simulate(rows, i, price, stop_a, target_b)
            if not (t_base and t_a and t_b and t_ab):
                continue

            all_trades_baseline.append(t_base)
            all_trades_a.append(t_a)
            all_trades_b.append(t_b)
            all_trades_ab.append(t_ab)
            sig_count += 1

            csv_rows.append({
                "stock_id": stock_id, "signal_date": rows[i]["date"], "entry_price": price,
                "support": round(support, 2), "resistance": round(resistance, 2),
                "ma20": round(ma20_now, 2), "deviation_pct": round((price - ma20_now) / ma20_now * 100, 2),
                "stop_baseline": stop_base, "stop_a": stop_a,
                "target_baseline": target_base, "target_b": target_b,
                "baseline_outcome": t_base["outcome"], "baseline_ret_pct": t_base["ret_pct"],
                "a_outcome": t_a["outcome"], "a_ret_pct": t_a["ret_pct"],
                "b_outcome": t_b["outcome"], "b_ret_pct": t_b["ret_pct"],
                "ab_outcome": t_ab["outcome"], "ab_ret_pct": t_ab["ret_pct"],
            })

        print(f"{sig_count} 筆有效訊號")
        time.sleep(0.35)

    print("\n=== 回測結果總表 ===")
    print(f"（排除資料不足以模擬滿{FORWARD_DAYS}日的訊號共 {excluded_insufficient_data} 筆）\n")
    summarize("Baseline(現行)", all_trades_baseline)
    summarize("候選A(動態防守位)", all_trades_a)
    summarize("候選B(參數化損益比)", all_trades_b)
    summarize("候選AB(A+B)", all_trades_ab)

    if csv_rows:
        with open("backtest_trades.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(csv_rows)
        print(f"\n明細已寫入 backtest_trades.csv（共 {len(csv_rows)} 筆訊號），跟終端機這段總表一起傳給Claude")
    else:
        print("\n⚠️ 沒有產生任何有效訊號，可能是股票池或期間設定問題")


if __name__ == "__main__":
    main()
