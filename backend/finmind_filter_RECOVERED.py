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


# ──────────────────────────────────────────
# 深度選股分析（每日17:00）
# 篩選條件：KD金叉 + MACD動能軸上增強 + 量能≥1.5倍
# ──────────────────────────────────────────

def _calc_kd(prices: list[dict], n: int = 9) -> tuple[float, float, str]:
    """計算 KD 值，回傳 (K, D, signal)"""
    if len(prices) < n + 1:
        return 50.0, 50.0, "neutral"
    closes = [p["close"] for p in prices]
    highs  = [p["high"]  for p in prices]
    lows   = [p["low"]   for p in prices]

    K, D = 50.0, 50.0
    for i in range(n - 1, len(prices)):
        period_high = max(highs[i - n + 1:i + 1])
        period_low  = min(lows[i  - n + 1:i + 1])
        rsv = (closes[i] - period_low) / (period_high - period_low) * 100 if period_high != period_low else 50
        K = K * 2 / 3 + rsv / 3
        D = D * 2 / 3 + K / 3

    # 前一根的 K D
    K_prev, D_prev = 50.0, 50.0
    if len(prices) >= n + 2:
        for i in range(n - 1, len(prices) - 1):
            period_high = max(highs[i - n + 1:i + 1])
            period_low  = min(lows[i  - n + 1:i + 1])
            rsv = (closes[i] - period_low) / (period_high - period_low) * 100 if period_high != period_low else 50
            K_prev = K_prev * 2 / 3 + rsv / 3
            D_prev = D_prev * 2 / 3 + K_prev / 3

    # 金叉：K 由下往上穿越 D
    if K > D and K_prev <= D_prev:
        signal = "golden_cross"
    elif K > D:
        signal = "bullish"
    elif K < D:
        signal = "bearish"
    else:
        signal = "neutral"

    return round(K, 2), round(D, 2), signal


def _calc_macd(prices: list[dict]) -> tuple[float, float, float, str]:
    """計算 MACD，回傳 (DIF, DEA, hist, signal)"""
    closes = [p["close"] for p in prices]
    if len(closes) < 35:
        return 0.0, 0.0, 0.0, "neutral"

    def ema(data, period):
        k = 2 / (period + 1)
        result = [data[0]]
        for v in data[1:]:
            result.append(v * k + result[-1] * (1 - k))
        return result

    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    dif = [e12 - e26 for e12, e26 in zip(ema12, ema26)]
    dea = ema(dif, 9)
    hist = [(d - e) * 2 for d, e in zip(dif, dea)]

    cur_dif  = round(dif[-1],  3)
    cur_dea  = round(dea[-1],  3)
    cur_hist = round(hist[-1], 3)
    prev_hist = hist[-2] if len(hist) > 1 else 0

    if cur_dif > 0 and cur_dif > cur_dea and cur_hist > prev_hist:
        signal = "strong_bullish"   # 軸上且動能增強
    elif cur_dif > 0 and cur_dif > cur_dea:
        signal = "bullish"
    elif cur_dif > -0.5:
        signal = "weak"
    else:
        signal = "bearish"

    return cur_dif, cur_dea, cur_hist, signal


def _calc_ma_trend(prices: list[dict]) -> str:
    """回傳均線排列：bullish / bearish / mixed"""
    closes = [p["close"] for p in prices]
    if len(closes) < 60:
        return "mixed"
    ma5  = sum(closes[-5:])  / 5
    ma20 = sum(closes[-20:]) / 20
    ma60 = sum(closes[-60:]) / 60
    if ma5 > ma20 > ma60:
        return "bullish"
    elif ma5 < ma20 < ma60:
        return "bearish"
    return "mixed"


def _calc_vol_ratio(prices: list[dict]) -> float:
    """近5日均量 / 近20日均量"""
    vols = [p["volume"] for p in prices if p["volume"] > 0]
    if len(vols) < 20:
        return 0.0
    avg5  = sum(vols[-5:]) / 5
    avg20 = sum(vols[-20:]) / 20
    return round(avg5 / avg20, 2) if avg20 > 0 else 0.0


def _fetch_fundamentals(stock_id: str, token: str = "") -> dict:
    """
    抓取個股基本面資料：本益比、殖利率、近四季EPS
    失敗回傳空值，不影響主流程
    """
    import requests
    from datetime import datetime, timedelta

    BASE = "https://api.finmindtrade.com/api/v4/data"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    today = datetime.now().strftime("%Y-%m-%d")
    one_year_ago = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")
    two_year_ago = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")

    result = {
        "per": None,          # 本益比
        "pbr": None,          # 股價淨值比
        "dividend_yield": None,  # 殖利率 %
        "eps_ttm": None,      # 近四季累計EPS
        "eps_yoy": None,      # EPS YoY 成長率 %
    }

    try:
        # ① 本益比、殖利率、PBR — 全部從 TaiwanStockPER 拿
        r = requests.get(BASE, headers=headers, params={
            "dataset": "TaiwanStockPER",
            "data_id": stock_id,
            "start_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "token": token,
        }, timeout=8)
        data = r.json().get("data", [])
        if data:
            latest = data[-1]
            result["per"] = round(float(latest.get("PER", 0) or 0), 1) or None
            result["pbr"] = round(float(latest.get("PBR", 0) or 0), 2) or None
            result["dividend_yield"] = round(float(latest.get("dividend_yield", 0) or 0), 2) or None
    except Exception:
        pass

    try:
        # ② 近四季 EPS
        r = requests.get(BASE, headers=headers, params={
            "dataset": "TaiwanStockFinancialStatements",
            "data_id": stock_id,
            "start_date": two_year_ago,
            "token": token,
        }, timeout=8)
        rows = r.json().get("data", [])
        # 找 EPS 欄位
        eps_rows = [row for row in rows if row.get("type") == "EPS" or
                    "每股" in str(row.get("type", "")) and "盈餘" in str(row.get("type", ""))]
        if not eps_rows:
            # 嘗試另一個欄位名
            eps_rows = [row for row in rows
                        if str(row.get("origin_name", "")).startswith("基本每股盈餘")]
        if len(eps_rows) >= 4:
            eps_vals = [float(row.get("value", 0) or 0) for row in eps_rows[-8:]]
            # 近四季
            ttm = round(sum(eps_vals[-4:]), 2)
            # 前四季
            if len(eps_vals) >= 8:
                prev_ttm = sum(eps_vals[-8:-4])
                yoy = round((ttm - prev_ttm) / abs(prev_ttm) * 100, 1) if prev_ttm else None
            else:
                yoy = None
            result["eps_ttm"] = ttm
            result["eps_yoy"] = yoy
    except Exception:
        pass

    return result


def deep_analyze_stock(stock_id: str, stock_name: str = "", finmind_token: str = "") -> dict | None:
    """
    深度分析單一股票
    篩選條件：KD金叉 + MACD軸上動能增強 + 量能≥1.5倍
    回傳完整分析 dict 或 None（不符合條件）
    """
    from crawler import fetch_twse_institutional, fetch_twse_broker_top

    prices = fetch_price_history(stock_id, days=90)
    if len(prices) < 30:
        return None

    price = prices[-1]["close"]
    if price < 10:
        return None

    # ① 技術指標
    K, D, kd_signal    = _calc_kd(prices)
    dif, dea, hist, macd_signal = _calc_macd(prices)
    ma_trend            = _calc_ma_trend(prices)
    vol_ratio           = _calc_vol_ratio(prices)

    # 篩選條件
    kd_ok   = kd_signal == "golden_cross"
    macd_ok = macd_signal in ("strong_bullish", "bullish")
    vol_ok  = vol_ratio >= 1.5

    if not (kd_ok and macd_ok and vol_ok):
        return None

    # ② 法人籌碼（TWSE T86）
    inst = fetch_twse_institutional(stock_id, days=3)
    time.sleep(0.5)

    # ③ 券商分點（TWSE TWT84U）
    broker = fetch_twse_broker_top(stock_id, top_n=15)
    time.sleep(0.5)

    # ④ 均線數值
    closes = [p["close"] for p in prices]
    ma5  = round(sum(closes[-5:])  / 5,  2)
    ma20 = round(sum(closes[-20:]) / 20, 2)
    ma60 = round(sum(closes[-60:]) / 60, 2) if len(closes) >= 60 else None

    # ⑤ 支撐壓力（近60日高低點，排除最後一根避免壓力=現價）
    _ref = prices[-60:-1] if len(prices) >= 61 else prices[:-1]
    if not _ref:
        _ref = prices
    recent_high = max(p["high"] for p in _ref)
    recent_low  = min(p["low"]  for p in _ref)
    resistance  = round(recent_high, 2)
    support     = round(recent_low,  2)
    rr_ratio    = round((resistance - price) / (price - support), 2) if price > support and resistance > price else 0

    vols = [p["volume"] for p in prices if p["volume"] > 0]
    avg_vol_5  = round(sum(vols[-5:])  / 5)
    avg_vol_20 = round(sum(vols[-20:]) / 20)

    prev_close = prices[-2]["close"] if len(prices) >= 2 else price
    change     = round(price - prev_close, 2)
    change_pct = round(change / prev_close * 100, 2) if prev_close else 0.0

    # ⑥ 基本面（本益比、殖利率、近四季EPS）
    fund = _fetch_fundamentals(stock_id, token=finmind_token)

    return {
        "stock_id":   stock_id,
        "stock_name": stock_name or stock_id,
        "price":      price,
        "prev_close": prev_close,
        "change":     change,
        "change_pct": change_pct,
        "date":       prices[-1]["date"],
        # 技術面
        "K": K, "D": D, "kd_signal": kd_signal,
        "dif": dif, "dea": dea, "hist": hist, "macd_signal": macd_signal,
        "ma_trend": ma_trend,
        "ma5": ma5, "ma20": ma20, "ma60": ma60,
        "vol_ratio":  vol_ratio,
        "avg_vol_5":  avg_vol_5,
        "avg_vol_20": avg_vol_20,
        # 支撐壓力
        "support":    support,
        "resistance": resistance,
        "rr_ratio":   rr_ratio,
        # 法人
        "inst": inst,
        # 券商分點
        "broker": broker,
        # 基本面
        "per":            fund.get("per"),
        "pbr":            fund.get("pbr"),
        "dividend_yield": fund.get("dividend_yield"),
        "eps_ttm":        fund.get("eps_ttm"),
        "eps_yoy":        fund.get("eps_yoy"),
    }


def run_deep_scan(candidate_ids: list[str], name_dict: dict = None,
                  delay: float = 1.2, finmind_token: str = "") -> list[dict]:
    """
    批次執行深度選股，回傳通過篩選的股票列表
    """
    name_dict = name_dict or {}
    results = []
    total = len(candidate_ids)
    print(f"[deep_scan] 開始深度掃描 {total} 檔...")

    for i, sid in enumerate(candidate_ids, 1):
        print(f"[deep_scan] ({i}/{total}) {sid} ...", end=" ", flush=True)
        try:
            r = deep_analyze_stock(sid, name_dict.get(sid, ""), finmind_token=finmind_token)
            if r:
                results.append(r)
                print(f"✓ 通過（KD金叉 K={r['K']} D={r['D']}，量比={r['vol_ratio']}）")
            else:
                print("✗ 未通過")
        except Exception as e:
            print(f"✗ 錯誤：{e}")
        if i < total:
            time.sleep(delay)

    print(f"[deep_scan] 完成，通過 {len(results)}/{total} 檔")
    return results


if __name__ == "__main__":
    from crawler import fetch_cnyes_news
    news = fetch_cnyes_news(30)
    result = analyze_stock("2330", news)
    if result:
        print("通過：", result)
    else:
        print("未通過篩選條件")
