"""
finmind_filter.py — 數值篩選層
輸入：股票代號列表（從新聞萃取）
輸出：通過篩選的個股，附帶量化指標

選股三要素：
  1. 鉅亨有題材新聞（有故事）← 必要條件
  2. 法人近 N 日連續買超（籌碼回流）
  3. 成交量從低量開始放大（量先價行）

型態偵測（v2）：
  - is_breakout_signal：均線糾結轉強  →「🚀 突破轉強」
  - is_golden_cross：轉多頭金叉      →「✅ 強勢金叉」/「✅ 金叉轉多」
  - is_death_cross：轉空頭死叉       →「⚠️ 強勢死叉」/「⚠️ 死叉轉空」（風險警示）
"""

from crawler import fetch_price_history, fetch_institutional
import time


# ──────────────────────────────────────────
# 篩選參數（可調整）
# ──────────────────────────────────────────
CFG = {
    # 【必要條件】鉅亨需有題材新聞才納入
    "require_news": True,

    # 法人連續買超天數門檻（純型態訊號可放寬）
    "min_consecutive_buy_days": 3,

    # 量能放大：近 5 日均量 / 近 20 日均量
    "min_vol_ratio": 1.2,

    # 最低成交量（張）：太冷門的過濾掉
    "min_avg_volume": 300,

    # 現價下限（過濾雞蛋水餃股）
    "min_price": 10.0,
}


# ──────────────────────────────────────────
# 型態偵測函數
# ──────────────────────────────────────────

def is_breakout_signal(prices: list[dict]) -> dict:
    """
    均線糾結轉強（同時滿足）：
    - MA5、MA20、MA60 差距皆 < 3%（糾結）
    - 當日成交量 ≥ 前5日均量的 1.5 倍
    - 收盤價 > 開盤價（收紅K）
    - 收盤價 > MA5、MA20、MA60
    - 收盤價 > 前10日最高價（突破近期高點）
    """
    if len(prices) < 62:
        return {"triggered": False, "label": ""}

    closes = [p["close"] for p in prices]
    ma5  = sum(closes[-5:])  / 5
    ma20 = sum(closes[-20:]) / 20
    ma60 = sum(closes[-60:]) / 60

    # MA 差距 < 3%（糾結判斷）
    ma_max = max(ma5, ma20, ma60)
    ma_min = min(ma5, ma20, ma60)
    if ma_min <= 0 or (ma_max - ma_min) / ma_min >= 0.03:
        return {"triggered": False, "label": ""}

    last  = prices[-1]
    close = last["close"]
    open_ = last["open"]
    vol   = last["volume"]

    # 收紅K
    if close <= open_:
        return {"triggered": False, "label": ""}

    # 收盤 > 三條均線
    if not (close > ma5 and close > ma20 and close > ma60):
        return {"triggered": False, "label": ""}

    # 成交量 ≥ 前5日均量 × 1.5
    prev5_avg = sum(p["volume"] for p in prices[-6:-1]) / 5
    if prev5_avg <= 0 or vol < prev5_avg * 1.5:
        return {"triggered": False, "label": ""}

    # 收盤 > 前10日最高價（不含今日）
    recent_high = max(p["high"] for p in prices[-11:-1])
    if close <= recent_high:
        return {"triggered": False, "label": ""}

    return {"triggered": True, "label": "🚀 突破轉強"}


def is_golden_cross(prices: list[dict]) -> dict:
    """
    轉多頭金叉：
    長線（主要）：MA20 上穿 MA60 + MA60 斜率向上 + 收盤 > MA60 + 量 ≥ 前5日均量 1.2x
    短線（輔助）：MA5 上穿 MA20 → 標籤升級為「強勢金叉」
    """
    if len(prices) < 62:
        return {"triggered": False, "label": ""}

    closes = [p["close"] for p in prices]

    # 今日 / 昨日 MA20、MA60
    ma20_t = sum(closes[-20:])   / 20
    ma20_y = sum(closes[-21:-1]) / 20
    ma60_t = sum(closes[-60:])   / 60
    ma60_y = sum(closes[-61:-1]) / 60

    # MA60 斜率（與 5 日前比較）
    ma60_5ago = sum(closes[-65:-5]) / 60 if len(closes) >= 65 else None

    last  = prices[-1]
    close = last["close"]
    vol   = last["volume"]
    prev5 = sum(p["volume"] for p in prices[-6:-1]) / 5

    # 長線金叉條件
    long_ok = (
        ma20_t > ma60_t and          # 今日 MA20 > MA60
        ma20_y <= ma60_y and         # 昨日 MA20 <= MA60（剛上穿）
        (ma60_5ago is None or ma60_t > ma60_5ago) and  # MA60 斜率向上
        close > ma60_t and           # 收盤 > MA60
        prev5 > 0 and vol >= prev5 * 1.2              # 量能確認
    )
    if not long_ok:
        return {"triggered": False, "label": ""}

    # 短線金叉（輔助）
    ma5_t = sum(closes[-5:])   / 5
    ma5_y = sum(closes[-6:-1]) / 5
    short_ok = (ma5_t > ma20_t and ma5_y <= ma20_y)

    label = "✅ 強勢金叉" if short_ok else "✅ 金叉轉多"
    return {"triggered": True, "label": label}


def is_death_cross(prices: list[dict]) -> dict:
    """
    轉空頭死叉：
    長線（主要）：MA20 下穿 MA60 + MA60 斜率向下 + 收盤 < MA60 + 量 ≥ 前5日均量 1.2x
    短線（輔助）：MA5 下穿 MA20 → 標籤升級為「強勢死叉」
    """
    if len(prices) < 62:
        return {"triggered": False, "label": ""}

    closes = [p["close"] for p in prices]

    ma20_t = sum(closes[-20:])   / 20
    ma20_y = sum(closes[-21:-1]) / 20
    ma60_t = sum(closes[-60:])   / 60
    ma60_y = sum(closes[-61:-1]) / 60

    ma60_5ago = sum(closes[-65:-5]) / 60 if len(closes) >= 65 else None

    last  = prices[-1]
    close = last["close"]
    vol   = last["volume"]
    prev5 = sum(p["volume"] for p in prices[-6:-1]) / 5

    # 長線死叉條件
    long_ok = (
        ma20_t < ma60_t and          # 今日 MA20 < MA60
        ma20_y >= ma60_y and         # 昨日 MA20 >= MA60（剛下穿）
        (ma60_5ago is None or ma60_t < ma60_5ago) and  # MA60 斜率向下
        close < ma60_t and           # 收盤 < MA60
        prev5 > 0 and vol >= prev5 * 1.2              # 量能確認
    )
    if not long_ok:
        return {"triggered": False, "label": ""}

    # 短線死叉（輔助）
    ma5_t = sum(closes[-5:])   / 5
    ma5_y = sum(closes[-6:-1]) / 5
    short_ok = (ma5_t < ma20_t and ma5_y >= ma20_y)

    label = "⚠️ 強勢死叉" if short_ok else "⚠️ 死叉轉空"
    return {"triggered": True, "label": label}


def detect_kline_patterns(closes, opens, highs, lows, volumes):
    """偵測最新 K 線型態，回傳 (型態標籤, 勝率)"""
    n = len(closes)
    if n < 3:
        return "常態 K 線（無觸發極端型態）", 0.50
    c0, o0, h0, l0, v0 = closes[-1], opens[-1], highs[-1], lows[-1], volumes[-1]
    body_size0    = abs(c0 - o0)
    upper_shadow0 = h0 - max(c0, o0)
    lower_shadow0 = min(c0, o0) - l0
    range0        = (h0 - l0) or 0.001
    avg_vol    = sum(volumes[-6:-1]) / 5 if n >= 6 else (sum(volumes[:-1]) / max(len(volumes) - 1, 1))
    vol_surge  = v0 > avg_vol * 1.5
    is_downtrend = closes[-1] < closes[-5] if n >= 5 else False
    is_uptrend   = closes[-1] > closes[-5] if n >= 5 else False
    if vol_surge and (body_size0 >= range0 * 0.6) and (c0 > o0):
        return "量增大紅棒（突破確認）", 0.62
    if vol_surge and (body_size0 >= range0 * 0.6) and (c0 < o0):
        return "量增大黑棒（跌破確認）", 0.62
    if is_downtrend and (lower_shadow0 >= body_size0 * 2) and (upper_shadow0 <= body_size0 * 0.5) and (c0 > o0):
        return "低檔錘子線（底部承接力道強）", 0.53
    if is_uptrend and (upper_shadow0 >= body_size0 * 2) and (lower_shadow0 <= body_size0 * 0.5) and (c0 < o0):
        return "高檔流星線（多頭上攻力竭）", 0.53
    return "常態 K 線（無觸發極端型態）", 0.50


# ──────────────────────────────────────────
# 主篩選函數
# ──────────────────────────────────────────

def analyze_stock(stock_id: str, news_list: list[dict]) -> dict | None:
    """
    對單一股票做量化分析，回傳指標 dict 或 None（不符合條件）

    回傳結構（新增欄位）：
      signal_label: str  ← 觸發的型態標籤（空字串表示無型態）
      is_risk: bool      ← True 表示死叉風險警示
    """
    # ── 先確認有無題材新聞（必要條件，省去不必要的 API 呼叫）──
    related_news = []
    for n in news_list:
        if stock_id in n["codes"] and n["title"]:
            related_news.append({
                "title":    n["title"],
                "link":     n["link"],
                "keywords": n["keywords"],
            })

    if CFG["require_news"] and not related_news:
        return None

    # ── 股價資料（拉 90 日以支援 MA60 計算）──
    prices = fetch_price_history(stock_id, days=90)
    if len(prices) < 10:
        return None

    price = prices[-1]["close"]
    if price < CFG["min_price"]:
        return None

    # ── 基本量能計算 ──
    vols       = [p["volume"] for p in prices if p["volume"] > 0]
    avg_vol_20 = sum(vols) / len(vols) if vols else 0
    avg_vol_5  = sum(p["volume"] for p in prices[-5:]) / 5
    vol_ratio  = round(avg_vol_5 / avg_vol_20, 2) if avg_vol_20 > 0 else 0

    # ── K 線型態偵測 ──
    _closes  = [p["close"]  for p in prices]
    _opens   = [p["open"]   for p in prices]
    _highs   = [p["high"]   for p in prices]
    _lows    = [p["low"]    for p in prices]
    _volumes = [p["volume"] for p in prices]
    kline_pattern, win_rate = detect_kline_patterns(_closes, _opens, _highs, _lows, _volumes)

    # ── 型態偵測（在拉法人之前先跑，死叉可跳過法人條件）──
    breakout = is_breakout_signal(prices)
    golden   = is_golden_cross(prices)
    death    = is_death_cross(prices)

    kws = list({kw for n in related_news for kw in n["keywords"]})

    # ── 死叉路徑：不需法人連買，直接標記為風險警示 ──
    if death["triggered"]:
        score_factors = [
            f"鉅亨題材新聞 {len(related_news)} 則，關鍵字：{', '.join(kws[:5]) if kws else '無特定題材標籤'}",
            f"量能：近5日均量是20日均量的 {vol_ratio}x，現價 {price}",
            f"型態警示：{death['label']}（MA20 下穿 MA60，注意下跌風險）",
        ]
        return {
            "stock_id":             stock_id,
            "price":                price,
            "consecutive_buy_days": 0,
            "inst_5d_total":        0,
            "inst_20d_total":       0,
            "vol_ratio":            vol_ratio,
            "avg_vol_5":            round(avg_vol_5),
            "avg_vol_20":           round(avg_vol_20),
            "news":                 related_news[:5],
            "score_factors":        score_factors,
            "signal_label":         death["label"],
            "is_risk":              True,
            "kline_pattern":        kline_pattern,
            "win_rate":             win_rate,
        }

    # ── 正常路徑：量能基本門檻 ──
    if avg_vol_20 < CFG["min_avg_volume"]:
        return None

    # 型態訊號自帶量能條件，可放寬整體量比門檻
    if vol_ratio < CFG["min_vol_ratio"] and not breakout["triggered"] and not golden["triggered"]:
        return None

    # ── 法人買賣超 ──
    inst = fetch_institutional(stock_id, days=20)
    if not inst:
        consecutive_buy_days = 0
        inst_5d_total        = 0
        inst_20d_total       = 0
    else:
        consecutive_buy_days = 0
        for row in reversed(inst):
            if row["total"] > 0:
                consecutive_buy_days += 1
            else:
                break
        inst_5d_total  = sum(r["total"] for r in inst[-5:])
        inst_20d_total = sum(r["total"] for r in inst)

    # 型態訊號可放寬法人連買門檻
    if (consecutive_buy_days < CFG["min_consecutive_buy_days"]
            and not breakout["triggered"] and not golden["triggered"]):
        return None

    # ── 決定信號標籤 ──
    if breakout["triggered"]:
        signal_label = breakout["label"]
    elif golden["triggered"]:
        signal_label = golden["label"]
    else:
        signal_label = ""

    # ── 評分依據（給 Claude 閱讀）──
    score_factors = [
        f"鉅亨題材新聞 {len(related_news)} 則，關鍵字：{', '.join(kws[:5]) if kws else '無特定題材標籤'}",
        f"法人連續買超 {consecutive_buy_days} 天，近5日合計 {inst_5d_total:+,} 張，近20日 {inst_20d_total:+,} 張",
        f"量能放大：近5日均量是20日均量的 {vol_ratio}x（量先價行跡象{'明顯' if vol_ratio >= 1.5 else '初現'}）",
        f"現價 {price}，近5日均量約 {round(avg_vol_5):,} 張",
    ]
    if signal_label:
        score_factors.append(f"型態：{signal_label}")

    return {
        "stock_id":             stock_id,
        "price":                price,
        "consecutive_buy_days": consecutive_buy_days,
        "inst_5d_total":        inst_5d_total,
        "inst_20d_total":       inst_20d_total,
        "vol_ratio":            vol_ratio,
        "avg_vol_5":            round(avg_vol_5),
        "avg_vol_20":           round(avg_vol_20),
        "news":                 related_news[:5],
        "score_factors":        score_factors,
        "signal_label":         signal_label,
        "is_risk":              False,
        "kline_pattern":        kline_pattern,
        "win_rate":             win_rate,
    }


def run_filter(candidate_ids: list[str], news_list: list[dict],
               max_results: int = 20, max_risk: int = 10,
               delay: float = 1.0) -> list[dict]:
    """
    對候選代號列表逐一篩選，回傳通過的個股清單
    - 做多候選（is_risk=False）最多 max_results 檔
    - 風險警示（is_risk=True）最多 max_risk 檔
    - delay：每檔之間的間隔秒數，避免 FinMind rate limit
    """
    long_list = []
    risk_list = []
    total = len(candidate_ids)
    print(f"[filter] 開始篩選 {total} 檔候選股票...")

    for i, sid in enumerate(candidate_ids, 1):
        print(f"[filter] ({i}/{total}) {sid} ...", end=" ", flush=True)
        result = analyze_stock(sid, news_list)
        if result:
            label = result.get("signal_label", "")
            if result.get("is_risk"):
                print(f"⚠️ 風險警示（{label}，量能 {result['vol_ratio']}x，"
                      f"新聞 {len(result['news'])} 則）")
                risk_list.append(result)
            else:
                tag = f"，型態：{label}" if label else ""
                print(f"✓ 通過（量能 {result['vol_ratio']}x，"
                      f"法人連買 {result['consecutive_buy_days']}日，"
                      f"新聞 {len(result['news'])} 則{tag}）")
                long_list.append(result)
        else:
            print("✗ 未通過")
        if i < total:
            time.sleep(delay)

    print(f"[filter] 篩選完畢：做多候選 {len(long_list)} 檔，"
          f"風險警示 {len(risk_list)} 檔（共 {total} 檔候選）")
    return long_list[:max_results] + risk_list[:max_risk]


if __name__ == "__main__":
    from crawler import fetch_cnyes_news
    news = fetch_cnyes_news(30)
    result = analyze_stock("2330", news)
    if result:
        print("通過：", result)
    else:
        print("未通過篩選條件")
