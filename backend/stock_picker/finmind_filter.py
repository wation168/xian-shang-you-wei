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
import time


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
# 深度選股（雙重確認＋MACD加分）— 2026/07/27 補回，2026/08/07 改MACD為加分項
#
# 這一段是給 main.py 的 _run_deep_analysis_job() 用的，入口是 run_deep_scan()。
# 上面的 analyze_stock / run_filter 是「精選股」用的舊流程，兩者互不影響，
# 舊功能完全沒有更動。
#
# 雙重確認（兩個條件必須同時成立才有資格入選）：
#   ① 月季線金叉：MA20 由下往上穿越 MA60，且金叉後未再翻回空頭
#   ② 站上月線　：現價站在 MA20 之上
#
# MACD金叉（DIF 由下往上穿越 DEA，且發生在 3 個交易日內）2026/08/07 改為加分項，
# 不再是強制門檻——太多波段初升段的股票會因為 MACD 還沒黃金交叉而被誤刪，
# 改成「有金叉多加分，沒有金叉不淘汰」。
#
# 通過雙重確認後再依「MACD金叉、股價位置、量能、法人籌碼」加分，分數愈高訊號愈強。
# 回傳欄位與 generator.render_deep_card() 及前端 showDeepAnalysisPage()
# 所需欄位完全一致。
# ══════════════════════════════════════════════════════════════════════

DEEP_CFG = {
    "min_price":        10.0,   # 最低股價
    "min_avg_volume":   500,    # 最低20日均量（張）
    "ma_cross_lookback": 20,    # 月季線金叉往回找幾個交易日
    "macd_cross_days":   3,     # MACD金叉必須發生在幾個交易日內
    "max_results":       30,    # 最多回傳幾檔
    "api_delay":         0.35,  # 每檔之間的間隔秒數（避免打爆 FinMind）
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


def _calc_stop_loss(closes: list[float], lows: list[float],
                    ma20_now: float, lift_off_low: float | None) -> tuple[float, float, str]:
    """
    停損價：分別算出「起漲低點 / 月線 / 前一根低點」三個候選，
    取其中「在現價之下且離現價最近」的一個（＝下檔風險最小的那個）。
    回傳 (停損價, 距現價百分比, 依據名稱)

    2026/07/27 修正：原本用「近20日低點／近10日低點」不是正確依據，
    改成：
      起漲低點：月季線金叉那天到現在這段期間的最低價（這波漲勢真正的起點，
               lift_off_low 由呼叫端傳入，抓不到金叉日期時為 None）
      月線　　：MA20 現值
      前一根低點：昨天那根K棒的最低價（單日，不是近N日區間低點）
    """
    price = closes[-1]
    candidates: list[tuple[float, str]] = []

    if lift_off_low:
        candidates.append((lift_off_low, "起漲低點"))
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

    # ── 雙重確認（硬條件）──────────────────────────
    # ① 月季線金叉（同時取得金叉索引，等下算「起漲低點」停損依據要用）
    cross_idx = _find_ma_golden_cross_index(ma20_l, ma60_l, DEEP_CFG["ma_cross_lookback"])
    if cross_idx is None:
        return None
    lift_off_low = min(lows[cross_idx:])   # 金叉那天到現在這段期間的最低價＝起漲低點
    ma_cross_days_ago = (len(closes) - 1) - cross_idx   # 幾個交易日前發生金叉，0＝就是今天
    ma_cross_date = dates[cross_idx]   # 金叉當天的實際日期，供 main.py 選股紀錄表去重用
    # ② 站上月線
    if price <= ma20:
        return None
    # ③ MACD金叉：不再是硬條件，只作為下面的加分項（發生在 macd_cross_days 天內才給分）
    dif, dea, hist = _macd(closes)
    macd_cross_idx = _find_macd_golden_cross_index(dif, dea, DEEP_CFG["macd_cross_days"]) if dif else None
    macd_cross_days_ago = (len(dif) - 1) - macd_cross_idx if macd_cross_idx is not None else None

    # ── 通過雙重確認，開始加分 ──────────────────────
    matched, score = _classify_position(closes, ma20, vol_ratio)

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
    stop_loss, stop_loss_pct, stop_loss_basis = _calc_stop_loss(closes, lows, ma20, lift_off_low)
    risk_level = _risk_level(stop_loss_pct)

    support    = round(min(lows[-20:]), 2) if len(lows) >= 20 else round(min(lows), 2)
    resist_win = highs[-60:] if len(highs) >= 60 else highs
    resistance = round(max(resist_win), 2)
    if resistance <= price:   # 已創新高，用近期波動幅度推估上檔空間
        resistance = round(price * 1.08, 2)

    downside = price - stop_loss
    rr_ratio = round((resistance - price) / downside, 2) if downside > 0 else 0

    # ── 漲跌 ──────────────────────────────────────
    prev_close = closes[-2] if len(closes) >= 2 else price
    change     = round(price - prev_close, 2)
    change_pct = round(change / prev_close * 100, 2) if prev_close else 0

    # ── 警示 ──────────────────────────────────────
    warnings: list[str] = []
    if vol_ratio < 1.0:
        warnings.append(f"近5日均量低於20日均量（量比 {vol_ratio}x），突破量能不足")
    if stop_loss_pct > 10:
        warnings.append(f"停損距現價 {stop_loss_pct}%，下檔風險較大，部位請控管")
    if rr_ratio and rr_ratio < 1:
        warnings.append(f"風報比僅 {rr_ratio}x，上檔空間小於下檔風險")
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
        # 雙重確認＋加分項的具體證據，讓前端能明確列出「為什麼入選」，不用只憑信任
        "ma_cross_days_ago":    ma_cross_days_ago,   # ①月季線金叉發生在幾個交易日前
        "ma_cross_date":        ma_cross_date,       # ①月季線金叉發生的實際日期（YYYY-MM-DD）
        "above_ma20_pct":       above_ma20_pct,      # ②現價高於月線的百分比
        "macd_cross_days_ago":  macd_cross_days_ago, # ③MACD金叉發生在幾個交易日前
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
    print(f"[deep_scan] 掃描完畢，{len(passed)}/{total} 檔通過雙重確認，取前 {max_results} 檔")
    return passed[:max_results]


if __name__ == "__main__":
    from crawler import fetch_cnyes_news
    news = fetch_cnyes_news(30)
    result = analyze_stock("2330", news)
    if result:
        print("通過：", result)
    else:
        print("未通過篩選條件")
