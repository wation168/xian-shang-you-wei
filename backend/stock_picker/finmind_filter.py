"""
finmind_filter.py — 數值篩選層
輸入：股票代號列表（從新聞萃取）
輸出：通過篩選的個股，依加分排序，上限 30 支（SEO 熱門股曝光用）

保留門檻：
  - 最低均量 1000 張
  - 最低股價 $10

加分規則：
  +2  有題材新聞
  +2  法人連續買超 ≥ 3 日
  +1  法人近日有買超（< 3 日）

本檔另含「深度選股」流程（run_deep_scan），供 main.py 每交易日 17:00 排程使用，
與上述精選股流程各自獨立，互不影響。
"""

from crawler import fetch_price_history, fetch_institutional
from kbar_indicators import detect_kbar_pattern, calc_breakout_signals
import time
import numpy as np


CFG = {
    "min_avg_volume": 1000,   # 最低均量（張）
    "min_price":      10.0,   # 最低股價
}

MAX_RESULTS = 30


def _score(result: dict) -> int:
    s = 0
    if result["news"]:
        s += 2
    if result["consecutive_buy_days"] >= 3:
        s += 2
    elif result["consecutive_buy_days"] >= 1:
        s += 1
    return s


def analyze_stock(stock_id: str, news_list: list[dict]) -> dict | None:
    """
    對單一股票做量化分析，回傳指標 dict 或 None（不符合基本門檻）
    """
    related_news = [
        {"title": n["title"], "link": n["link"], "keywords": n["keywords"]}
        for n in news_list
        if stock_id in n["codes"] and n["title"]
    ]

    prices = fetch_price_history(stock_id, days=30)
    if len(prices) < 10:
        return None

    price = prices[-1]["close"]
    if price < CFG["min_price"]:
        return None

    vols = [p["volume"] for p in prices if p["volume"] > 0]
    avg_vol_20 = sum(vols) / len(vols) if vols else 0
    if avg_vol_20 < CFG["min_avg_volume"]:
        return None

    avg_vol_5 = sum(p["volume"] for p in prices[-5:]) / 5

    inst = fetch_institutional(stock_id, days=20)
    if not inst:
        consecutive_buy_days = 0
        inst_5d_total  = 0
        inst_20d_total = 0
    else:
        consecutive_buy_days = 0
        for row in reversed(inst):
            if row["total"] > 0:
                consecutive_buy_days += 1
            else:
                break
        inst_5d_total  = sum(r["total"] for r in inst[-5:])
        inst_20d_total = sum(r["total"] for r in inst)

    kws = list({kw for n in related_news for kw in n["keywords"]})
    score_factors = [
        f"題材新聞 {len(related_news)} 則，關鍵字：{', '.join(kws[:5]) if kws else '無'}",
        f"法人連續買超 {consecutive_buy_days} 天，近5日 {inst_5d_total:+,} 張，近20日 {inst_20d_total:+,} 張",
        f"近5日均量 {round(avg_vol_5):,} 張，近20日均量 {round(avg_vol_20):,} 張",
        f"現價 {price}",
    ]

    result = {
        "stock_id":             stock_id,
        "price":                price,
        "consecutive_buy_days": consecutive_buy_days,
        "inst_5d_total":        inst_5d_total,
        "inst_20d_total":       inst_20d_total,
        "avg_vol_5":            round(avg_vol_5),
        "avg_vol_20":           round(avg_vol_20),
        "news":                 related_news[:5],
        "score_factors":        score_factors,
    }
    result["score"] = _score(result)
    return result


def run_filter(candidate_ids: list[str], news_list: list[dict],
               max_results: int = MAX_RESULTS, delay: float = 1.0) -> list[dict]:
    """
    對候選代號列表逐一篩選，依加分排序後回傳前 max_results 支
    """
    passed = []
    total = len(candidate_ids)
    print(f"[filter] 開始篩選 {total} 檔候選股票...")

    for i, sid in enumerate(candidate_ids, 1):
        print(f"[filter] ({i}/{total}) {sid} ...", end=" ", flush=True)
        result = analyze_stock(sid, news_list)
        if result:
            print(f"✓ 通過（分數 {result['score']}，"
                  f"法人連買 {result['consecutive_buy_days']}日，"
                  f"新聞 {len(result['news'])} 則）")
            passed.append(result)
        else:
            print("✗ 未通過")
        if i < total:
            time.sleep(delay)

    passed.sort(key=lambda x: x["score"], reverse=True)
    print(f"[filter] 篩選完畢，通過 {len(passed)}/{total} 檔，取前 {max_results} 支")
    return passed[:max_results]


# ══════════════════════════════════════════════════════════════════════
# 深度選股（雙路徑入選＋加分）— 2026/07/27 補回，2026/08/07 改MACD為加分項，
#                                2026/08/20 加入路徑B（剛突破）
#
# 這一段是給 main.py 的 _run_deep_analysis_job() 用的，入口是 run_deep_scan()。
# 上面的 analyze_stock / run_filter 是「精選股」用的舊流程，兩者互不影響，
# 舊功能完全沒有更動。
#
# 【2026/08/20背景】帥哥鴻反映「深度選股選出來的個股都是已經漲一段才出現」。
# 根因：原本唯一的入選條件是月季線金叉，這是落後指標——MA20要翻到MA60上方，
# 代表過去20天均價已經回升超過過去60天均價，這件事發生時股價通常早就漲一段了。
# 這不是bug，是「趨勢確認型」策略天生的特性，但使用者體感就是「怎麼都追高」。
# 解法：不是拿掉舊機制，而是新增一條時間點更早的入選路徑，兩條路徑並存，
# 各自標註清楚是哪一種訊號，讓使用者自己判斷要不要進場，而不是統一包裝成
# 「深度選股」讓人誤以為每一檔都是同一種訊號：
#
#   路徑A（趨勢確認）：月季線金叉＋站上月線，金叉後未再翻回空頭。
#     訊號穩定可信，但入選時通常已經上漲一段，操作建議是「等拉回再上」，
#     不建議現價追價。
#
#   路徑B（剛突破，2026/08/20新增）：近期（breakout_recent_days內）放量突破
#     盤整區間高點（用 kbar_indicators.calc_breakout_signals，跟main.py個股
#     解析同一套函式），且現價還守在突破價之上沒有被打回假突破。
#     訊號比路徑A早，是這次新增的目的，但相對沒有經過時間驗證、波動風險較高，
#     操作建議是「停損嚴設在突破當天低點，跌破視為假突破要立刻出場」。
#
# 每檔股票只會落在其中一條路徑（路徑A優先判斷，不成立才看路徑B），不會同時算兩次。
#
# MACD金叉（DIF 由下往上穿越 DEA，且發生在 3 個交易日內）2026/08/07 改為加分項，
# 不再是強制門檻——太多波段初升段的股票會因為 MACD 還沒黃金交叉而被誤刪，
# 改成「有金叉多加分，沒有金叉不淘汰」，兩條路徑共用這個加分項。
#
# 通過入選後再依「MACD金叉、股價位置/突破強度、量能、法人籌碼」加分，分數愈高訊號愈強。
# 回傳欄位與 generator.render_deep_card() 及前端 showDeepAnalysisPage()
# 所需欄位完全一致，新增的 entry_path/entry_path_label/entry_path_note 欄位
# 是額外補充，沒有的話前端會拿不到值但不會壞。
# ══════════════════════════════════════════════════════════════════════

DEEP_CFG = {
    "min_price":        10.0,   # 最低股價
    "min_avg_volume":   500,    # 最低20日均量（張）
    "ma_cross_lookback": 20,    # 月季線金叉往回找幾個交易日
    "macd_cross_days":   3,     # MACD金叉必須發生在幾個交易日內
    "min_score":          3,    # 2026/08/22新增：入選門檻，score<3（＝信心等級「一般」，
                                 # 沒有MACD金叉/量能/法人籌碼任何一項加分確認）不列入結果。
                                 # 原本只要符合路徑A/B條件、不論分數高低一律入選，帥哥鴻反映
                                 # 「一次選出22檔太多」，改成只留至少有一項加分確認的中信心⭐
                                 # 以上訊號，數量會隨市況自然浮動，不是卡死的筆數上限。
    "max_results":       30,    # 最多回傳幾檔（安全上限，通常不會卡到這個數字）
    "api_delay":         0.35,  # 每檔之間的間隔秒數（避免打爆 FinMind）
    "breakout_recent_days": 10, # 路徑B：突破必須發生在幾個交易日內才算「剛」突破
    "breakout_hold_pct":  0.97, # 路徑B：現價不能跌破突破當天收盤價的這個比例（防假突破被打回還入選）
}


def _ma(values: list[float], period: int) -> list[float | None]:
    """簡單移動平均，長度與輸入相同，不足期數的位置為 None"""
    out: list[float | None] = []
    run = 0.0
    for i, v in enumerate(values):
        run += v
        if i >= period:
            run -= values[i - period]
        out.append(round(run / period, 2) if i >= period - 1 else None)
    return out


def _ema(values: list[float], period: int) -> list[float]:
    """指數移動平均（第一個值直接當種子）"""
    if not values:
        return []
    k = 2 / (period + 1)
    out = [values[0]]
    for v in values[1:]:
        out.append(v * k + out[-1] * (1 - k))
    return out


def _macd(closes: list[float]) -> tuple[list[float], list[float], list[float]]:
    """回傳 (DIF, DEA, HIST)；HIST 用台股慣用的 (DIF-DEA)*2"""
    if len(closes) < 26:
        return [], [], []
    ema12 = _ema(closes, 12)
    ema26 = _ema(closes, 26)
    dif = [a - b for a, b in zip(ema12, ema26)]
    dea = _ema(dif, 9)
    hist = [(d - s) * 2 for d, s in zip(dif, dea)]
    return dif, dea, hist


def _find_ma_golden_cross_index(ma20: list, ma60: list, lookback: int) -> int | None:
    """
    找出月季線金叉發生在第幾天（索引）。
    條件：往回 lookback 個交易日內，MA20 曾由下往上穿越 MA60，
    且從金叉那天到現在，MA20 一直保持在 MA60 之上（沒有翻回空頭）。
    找不到符合條件的金叉則回傳 None。

    這個索引同時用在兩個地方：① 判斷是否入選（月季線金叉條件）
    ② 計算停損時的「起漲低點」——金叉那天就是這波漲勢的起點，
    起漲低點＝金叉當天到現在這段期間的最低價。
    """
    n = len(ma20)
    if n < 2 or ma20[-1] is None or ma60[-1] is None:
        return None
    if ma20[-1] <= ma60[-1]:
        return None  # 現在不是多頭排列，直接淘汰
    start = max(1, n - lookback)
    cross_idx = None
    for i in range(start, n):
        if ma20[i] is None or ma60[i] is None or ma20[i - 1] is None or ma60[i - 1] is None:
            continue
        if ma20[i - 1] <= ma60[i - 1] and ma20[i] > ma60[i]:
            cross_idx = i
    if cross_idx is None:
        return None
    # 金叉後不可再翻回空頭
    for i in range(cross_idx, n):
        if ma20[i] is None or ma60[i] is None:
            continue
        if ma20[i] <= ma60[i]:
            return None
    return cross_idx


def _check_ma_golden_cross(ma20: list, ma60: list, lookback: int) -> bool:
    """月季線金叉是否成立（不含起漲低點索引，供選股條件判斷用）"""
    return _find_ma_golden_cross_index(ma20, ma60, lookback) is not None


def _find_macd_golden_cross_index(dif: list, dea: list, within_days: int) -> int | None:
    """
    找出 MACD 金叉發生在第幾天（索引）：DIF 由下往上穿越 DEA，
    且發生在最近 within_days 個交易日內。取範圍內「最近一次」的金叉。
    找不到則回傳 None。
    """
    n = len(dif)
    if n < 2:
        return None
    start = max(1, n - within_days)
    cross_idx = None
    for i in range(start, n):
        if dif[i - 1] <= dea[i - 1] and dif[i] > dea[i]:
            cross_idx = i
    return cross_idx


def _check_macd_golden_cross(dif: list, dea: list, within_days: int) -> bool:
    """MACD金叉是否成立（不含索引，供選股條件判斷用）"""
    return _find_macd_golden_cross_index(dif, dea, within_days) is not None


def _classify_position(closes: list[float], ma20_now: float,
                       vol_ratio: float) -> tuple[list[str], int]:
    """
    依股價在近期區間的位置分類型態並加分。
    回傳 (matched_conditions, 位置加分)
    代號必須與 generator._deep_condition_label() 的對照表一致。
    """
    conds: list[str] = []
    bonus = 0
    price = closes[-1]

    win = closes[-60:] if len(closes) >= 60 else closes
    hi, lo = max(win), min(win)
    span = hi - lo
    pos = (price - lo) / span if span > 0 else 0.5   # 0=區間最低 1=區間最高

    if pos <= 0.35:
        # 低檔起漲：位置低、剛轉強，風報比最好
        conds.append("cond1_低檔起漲")
        bonus += 3
    elif pos <= 0.70:
        # 高點拉回起漲（買1）：從高點回落整理後再度轉強
        conds.append("cond2_高點拉回起漲(買1)")
        bonus += 2
    else:
        # 均線突破（買2）：已在相對高檔，靠突破續強，需量能確認
        if vol_ratio >= 1.3:
            conds.append("cond3_均線突破(買2)")
            bonus += 1
        else:
            conds.append("cond3_均線突破(買2)_量能未確認")
            bonus += 0
    return conds, bonus


def _calc_stop_loss(closes: list[float], lows: list[float], ma20_now: float,
                    key_low: float | None = None,
                    key_low_label: str = "起漲低點") -> tuple[float, float, str]:
    """
    停損價：分別算出「路徑關鍵低點 / 月線 / 前一根低點」三個候選，
    取其中「在現價之下且離現價最近」的一個（＝下檔風險最小的那個）。
    回傳 (停損價, 距現價百分比, 依據名稱)

    2026/07/27 修正：原本用「近20日低點／近10日低點」不是正確依據，
    改成：
      路徑關鍵低點：由呼叫端傳入，抓不到時為 None。
               路徑A（趨勢確認）傳「起漲低點」＝月季線金叉那天到現在這段期間的最低價；
               路徑B（剛突破，2026/08/20新增）傳「突破量能低點」＝放量突破當天的最低價，
               跌破代表突破失敗，是路徑B該用的停損依據，不是路徑A的起漲低點。
      月線　　：MA20 現值
      前一根低點：昨天那根K棒的最低價（單日，不是近N日區間低點）
    """
    price = closes[-1]
    candidates: list[tuple[float, str]] = []

    if key_low:
        candidates.append((key_low, key_low_label))
    if ma20_now:
        candidates.append((ma20_now, "月線"))
    if len(lows) >= 2:
        candidates.append((lows[-2], "前一根低點"))

    valid = [(v, name) for v, name in candidates if v and v < price]
    if not valid:
        # 極端情況（現價已跌破所有候選）：用現價 8% 當保底停損
        sl = round(price * 0.92, 2)
        return sl, 8.0, "現價8%保底"

    sl, basis = max(valid, key=lambda x: x[0])   # 離現價最近＝數值最大
    sl = round(sl, 2)
    pct = round((price - sl) / price * 100, 2)
    return sl, pct, basis


def _risk_level(stop_loss_pct: float) -> str:
    """低：5%以內 / 中：5~10% / 高：10%以上"""
    if stop_loss_pct <= 5:
        return "低"
    if stop_loss_pct <= 10:
        return "中"
    return "高"


def _confidence(score: int) -> str:
    """5分以上高信心 / 3~4分中信心 / 其餘一般"""
    if score >= 5:
        return "高信心🔥"
    if score >= 3:
        return "中信心⭐"
    return "一般"


def deep_analyze_stock(stock_id: str, stock_name: str = "") -> dict | None:
    """
    對單一股票做雙重確認＋加分的深度分析。
    通過回傳完整結果 dict，未通過回傳 None。
    """
    prices = fetch_price_history(stock_id, days=150)
    if len(prices) < 65:
        return None   # 資料不足以算 MA60

    closes = [p["close"] for p in prices if p["close"] > 0]
    opens  = [p["open"]   for p in prices if p["close"] > 0]
    lows   = [p["low"]    for p in prices if p["close"] > 0]
    highs  = [p["high"]   for p in prices if p["close"] > 0]
    vols   = [p["volume"] for p in prices if p["close"] > 0]
    dates  = [p["date"]   for p in prices if p["close"] > 0]
    if len(closes) < 65:
        return None

    price = closes[-1]
    if price < DEEP_CFG["min_price"]:
        return None

    ma5_l  = _ma(closes, 5)
    ma20_l = _ma(closes, 20)
    ma60_l = _ma(closes, 60)
    ma5, ma20, ma60 = ma5_l[-1], ma20_l[-1], ma60_l[-1]
    if ma20 is None or ma60 is None:
        return None

    # 量能（張）
    vol20 = sum(vols[-20:]) / 20 if len(vols) >= 20 else 0
    vol5  = sum(vols[-5:]) / 5 if len(vols) >= 5 else 0
    if vol20 < DEEP_CFG["min_avg_volume"]:
        return None
    vol_ratio = round(vol5 / vol20, 2) if vol20 > 0 else 0

    # ── 突破訊號（兩條路徑共用，先算好，路徑B的入選判斷跟後面的K棒敘事都要用）──
    # 跟main.py個股解析同一套函式，support/resistance參數這支函式內部沒有實際使用
    # （改用逐根K棒的滾動局部高低點），這裡先傳0，後面算出真正的support/resistance
    # 純供敘事段落顯示用，不影響這裡的判斷。
    _breakout_idx, _breakdown_idx, _breakout_stale, _ = calc_breakout_signals(
        np.array(closes), np.array(highs), np.array(lows), np.array(vols), 0, 0)

    # ── 入選路徑判斷（路徑A優先，不成立才看路徑B，每檔只會落在一條路徑）───
    entry_path = None
    lift_off_low = None
    ma_cross_days_ago = None
    ma_cross_date = None
    breakout_days_ago = None

    # 路徑A（趨勢確認）：月季線金叉＋站上月線，金叉後未再翻回空頭
    cross_idx = _find_ma_golden_cross_index(ma20_l, ma60_l, DEEP_CFG["ma_cross_lookback"])
    if cross_idx is not None and price > ma20:
        entry_path = "A"
        lift_off_low = min(lows[cross_idx:])   # 金叉那天到現在這段期間的最低價＝起漲低點
        ma_cross_days_ago = (len(closes) - 1) - cross_idx   # 幾個交易日前發生金叉，0＝就是今天
        ma_cross_date = dates[cross_idx]   # 金叉當天的實際日期，供 main.py 選股紀錄表去重用

    # 路徑B（剛突破，2026/08/20新增）：路徑A不成立時才檢查。近期放量突破盤整區間高點，
    # 且現價還守在突破價的breakout_hold_pct之上（沒有跌破突破價太多，不是假突破被打回）
    if entry_path is None and _breakout_idx is not None and not _breakout_stale:
        _days_ago = (len(closes) - 1) - _breakout_idx
        _breakout_close = closes[_breakout_idx]
        _still_holds = _breakout_close > 0 and price >= _breakout_close * DEEP_CFG["breakout_hold_pct"]
        if _days_ago <= DEEP_CFG["breakout_recent_days"] and _still_holds and ma5:
            entry_path = "B"
            breakout_days_ago = _days_ago

    if entry_path is None:
        return None

    # MACD金叉：不再是強制門檻，只作為下面的加分項（發生在 macd_cross_days 天內才給分），
    # 兩條路徑共用同一套加分邏輯。
    dif, dea, hist = _macd(closes)
    macd_cross_idx = _find_macd_golden_cross_index(dif, dea, DEEP_CFG["macd_cross_days"]) if dif else None
    macd_cross_days_ago = (len(dif) - 1) - macd_cross_idx if macd_cross_idx is not None else None

    # ── 通過入選，開始加分（依路徑給不同的起始matched/score與操作提醒）──────
    if entry_path == "A":
        matched, score = _classify_position(closes, ma20, vol_ratio)
        entry_path_label = "趨勢確認"
        entry_path_note = (
            "此訊號來自月季線金叉，屬於「趨勢已確認」的穩定型訊號，但代表股價通常已經"
            "上漲一段時間，不是起漲點。不建議現價追價，建議等拉回至防守位附近再進場，"
            "拉回不破再上車，勝率比追高好。"
        )
    else:
        matched, score = ["cond4_剛突破"], 2
        entry_path_label = "剛突破"
        entry_path_note = (
            f"此訊號來自 {breakout_days_ago} 個交易日前放量突破盤整區間，屬於較早期的訊號，"
            "進場時間點比趨勢確認型早，但還沒經過時間驗證，波動風險較高。"
            "停損務必嚴設在突破當天的低點，跌破視為假突破，應立即出場、不要留戀。"
        )

    # MACD金叉加分（原本是強制門檻，2026/08/07 改成加分項：有金叉代表動能已確認，額外加分）
    if macd_cross_idx is not None:
        matched.append("MACD金叉")
        score += 2

    # 量能加分
    if vol_ratio >= 1.5:
        score += 2
    elif vol_ratio >= 1.2:
        score += 1

    # MACD 動能仍在加速（柱狀體連續放大）
    if len(hist) >= 3 and hist[-1] > hist[-2] > hist[-3] and hist[-1] > 0:
        matched.append("MACD動能加速中")
        score += 1

    # 法人籌碼
    inst = fetch_institutional(stock_id, days=20)
    consecutive_buy_days = 0
    inst_5d_total = 0
    if inst:
        for row in reversed(inst):
            if row["total"] > 0:
                consecutive_buy_days += 1
            else:
                break
        inst_5d_total = sum(r["total"] for r in inst[-5:])
    if consecutive_buy_days >= 3:
        score += 2
    elif consecutive_buy_days >= 1:
        score += 1

    # ── 停損 / 支撐壓力 / 風險 ──────────────────────
    # 路徑A用「起漲低點」（lift_off_low）當關鍵停損依據，路徑B改用「突破量能低點」
    # （突破當天的低點，跌破代表突破失敗），見_calc_stop_loss()說明。
    if entry_path == "A":
        _key_low, _key_low_label = lift_off_low, "起漲低點"
    else:
        _key_low, _key_low_label = lows[_breakout_idx], "突破量能低點"
    stop_loss, stop_loss_pct, stop_loss_basis = _calc_stop_loss(
        closes, lows, ma20, _key_low, _key_low_label)
    risk_level = _risk_level(stop_loss_pct)

    support    = round(min(lows[-20:]), 2) if len(lows) >= 20 else round(min(lows), 2)
    resist_win = highs[-60:] if len(highs) >= 60 else highs
    resistance = round(max(resist_win), 2)
    if resistance <= price:   # 已創新高，用近期波動幅度推估上檔空間
        resistance = round(price * 1.08, 2)

    downside = price - stop_loss
    rr_ratio = round((resistance - price) / downside, 2) if downside > 0 else 0

    # ── K棒型態（2026/08/13新增）─────────────────────
    # 用main.py個股解析同一套函式（見kbar_indicators.py），純供敘事用，
    # 刻意不接進score/risk_level/matched_conditions，不改變任何選股結果。
    # _breakout_idx/_breakdown_idx已經在上面「入選路徑判斷」前算過了，這裡直接沿用，
    # 不重算一次（那次呼叫的support/resistance參數函式內部本來就沒用到，提早算不影響結果）。
    kbar_pattern, _kbar_warning, kbar_dir, _kbar_win_rate = detect_kbar_pattern(
        opens, highs, lows, closes, vols)

    # 突破隔日拉回敘事：跟main.py個股解析同一套判斷——「孕線」型態＋前一天已出現突破/跌破，
    # 代表今天的孕線其實是正常拉回整理，不是單純方向不明的整理
    breakout_pullback_note = ""
    _n_bars = len(closes)
    if kbar_pattern and "孕線" in kbar_pattern:
        if _breakout_idx is not None and _breakout_idx == _n_bars - 2:
            _bo_price = round(float(closes[_breakout_idx]), 2)
            breakout_pullback_note = (
                f"昨日已放量突破，今日縮量拉回整理，屬正常拉回而非反轉，"
                f"若不跌破昨日突破價 {_bo_price} 可續抱"
            )
        elif _breakdown_idx is not None and _breakdown_idx == _n_bars - 2:
            _bd_price = round(float(closes[_breakdown_idx]), 2)
            breakout_pullback_note = (
                f"昨日已放量跌破，今日縮量反彈整理，屬弱勢反彈非止跌，"
                f"若無法站回昨日跌破價 {_bd_price} 應持續觀望"
            )

    # ── 漲跌 ──────────────────────────────────────
    prev_close = closes[-2] if len(closes) >= 2 else price
    change     = round(price - prev_close, 2)
    change_pct = round(change / prev_close * 100, 2) if prev_close else 0

    # ── 警示 ──────────────────────────────────────
    warnings: list[str] = []
    if vol_ratio < 1.0:
        warnings.append(f"近5日均量低於20日均量（量比 {vol_ratio}x），突破量能不足")
    if stop_loss_pct > 10:
        warnings.append(f"防守位距現價 {stop_loss_pct}%，下檔風險較大，部位請控管")
    if rr_ratio and rr_ratio < 1:
        warnings.append(f"損益比僅 {rr_ratio}x，上檔空間小於下檔風險")
    if change_pct >= 7:
        warnings.append(f"今日已大漲 {change_pct}%，追高風險提高，建議等拉回")
    if inst and inst_5d_total < 0:
        warnings.append(f"近5日法人合計賣超 {abs(inst_5d_total):,} 張，籌碼面偏弱")

    # 站上月線的幅度（②的具體證據，方便UI顯示「現價高於月線多少%」）
    above_ma20_pct = round((price - ma20) / ma20 * 100, 2) if ma20 else None

    return {
        "stock_id":             stock_id,
        "stock_name":           stock_name or stock_id,
        "price":                round(price, 2),
        "change":               change,
        "change_pct":           change_pct,
        "price_date":           dates[-1] if dates else None,  # 現價對應的實際交易日（動態取自價格資料，非寫死）
        "ma5":                  ma5,
        "ma20":                 ma20,
        "ma60":                 ma60,
        "vol_ratio":            vol_ratio,
        "avg_vol_5":            round(vol5),
        "avg_vol_20":           round(vol20),
        "macd_dif":             round(dif[-1], 3),
        "macd_dea":             round(dea[-1], 3),
        "macd_hist":            round(hist[-1], 3),
        "matched_conditions":   matched,
        "score":                score,
        "confidence":           _confidence(score),
        "risk_level":           risk_level,
        "support":              support,
        "resistance":           resistance,
        "stop_loss":            stop_loss,
        "stop_loss_pct":        stop_loss_pct,
        "stop_loss_basis":      stop_loss_basis,
        # 入選路徑＋加分項的具體證據，讓前端能明確列出「為什麼入選」，不用只憑信任
        # 2026/08/20新增：entry_path區分這檔是路徑A（趨勢確認）還是路徑B（剛突破），
        # 兩種訊號的時間點跟風險特性不同，前端/報告一律要用entry_path_label+entry_path_note
        # 明確標示，不能把兩種訊號混著呈現成同一種「深度選股入選」。
        "entry_path":           entry_path,           # "A"（趨勢確認）或 "B"（剛突破）
        "entry_path_label":     entry_path_label,     # "趨勢確認" 或 "剛突破"
        "entry_path_note":      entry_path_note,      # 對應路徑的操作提醒文字（等拉回／嚴設停損）
        "ma_cross_days_ago":    ma_cross_days_ago,    # 路徑A：月季線金叉發生在幾個交易日前，路徑B為None
        "ma_cross_date":        ma_cross_date,        # 路徑A：月季線金叉發生的實際日期（YYYY-MM-DD），路徑B為None
        "breakout_days_ago":    breakout_days_ago,    # 路徑B：放量突破發生在幾個交易日前，路徑A為None
        "above_ma20_pct":       above_ma20_pct,       # 現價高於月線的百分比
        "macd_cross_days_ago":  macd_cross_days_ago,  # MACD金叉發生在幾個交易日前
        "rr_ratio":             rr_ratio,
        "consecutive_buy_days": consecutive_buy_days,
        "inst_5d_total":        inst_5d_total,
        "warnings":             warnings,
        # 基本面欄位目前沒有資料來源，統一給 None，
        # generator 端會自動略過不顯示（不是漏寫，是刻意留空）
        "per":                  None,
        "dividend_yield":       None,
        "eps_ttm":              None,
        "eps_yoy":              None,
        # K棒型態敘事欄位（2026/08/13新增，與main.py個股解析同一套函式算出，
        # 純供白話結論敘事用，不影響score/risk_level/matched_conditions）
        "kbar_pattern":           kbar_pattern,          # 今日K棒型態名稱，可能為None
        "kbar_dir":               kbar_dir,              # bullish / bearish / neutral
        "breakout_pullback_note": breakout_pullback_note,  # 突破隔日拉回敘事，無則為空字串
    }


def run_deep_scan(candidate_ids: list[str],
                  name_dict: dict[str, str] | None = None,
                  finmind_token: str | None = None,
                  max_results: int = None,
                  delay: float = None) -> list[dict]:
    """
    深度選股主入口（main.py 的 _run_deep_analysis_job 呼叫這支）。

    參數：
      candidate_ids : 候選股代號列表（通常是成交量前150）
      name_dict     : {代號: 股名}，沒有的話用代號當股名
      finmind_token : FinMind API token，會覆寫 crawler 的模組層設定
      max_results   : 最多回傳幾檔，預設 DEEP_CFG["max_results"]
      delay         : 每檔之間的間隔秒數，預設 DEEP_CFG["api_delay"]

    回傳：通過雙重確認的個股清單，依分數由高到低排序
    """
    if max_results is None:
        max_results = DEEP_CFG["max_results"]
    if delay is None:
        delay = DEEP_CFG["api_delay"]

    # main.py 是從環境變數拿 token 再傳進來，這裡同步給 crawler 用
    if finmind_token:
        import crawler as _crawler_mod
        _crawler_mod.FINMIND_TOKEN = finmind_token

    name_dict = name_dict or {}
    passed: list[dict] = []
    total = len(candidate_ids)
    print(f"[deep_scan] 開始雙重確認掃描 {total} 檔候選股...")

    for i, sid in enumerate(candidate_ids, 1):
        try:
            result = deep_analyze_stock(sid, name_dict.get(sid, sid))
        except Exception as e:
            print(f"[deep_scan] ({i}/{total}) {sid} 分析失敗：{e}")
            result = None

        if result:
            print(f"[deep_scan] ({i}/{total}) {sid} ✓ 入選"
                  f"（分數 {result['score']}／{result['confidence']}／風險{result['risk_level']}）")
            passed.append(result)

        if i < total and delay:
            time.sleep(delay)

    passed.sort(key=lambda x: x["score"], reverse=True)

    # 2026/08/22新增：入選門檻，只留score>=min_score（中信心⭐以上）的訊號，
    # 濾掉沒有任何加分確認、純粹踩到路徑A/B最低條件的「一般」信心訊號，
    # 避免每天入選檔數太多、訊號強弱參差不齊。
    _min_score = DEEP_CFG["min_score"]
    _before_threshold = len(passed)
    passed = [p for p in passed if p["score"] >= _min_score]
    print(f"[deep_scan] 入選門檻(score>={_min_score})：{_before_threshold}檔通過雙重確認中，"
          f"{_before_threshold - len(passed)}檔信心等級「一般」被濾掉，剩{len(passed)}檔")

    print(f"[deep_scan] 掃描完畢，{len(passed)}/{total} 檔通過雙重確認+入選門檻，取前 {max_results} 檔")
    return passed[:max_results]


if __name__ == "__main__":
    from crawler import fetch_cnyes_news
    news = fetch_cnyes_news(30)
    result = analyze_stock("2330", news)
    if result:
        print("通過：", result)
    else:
        print("未通過篩選條件")
