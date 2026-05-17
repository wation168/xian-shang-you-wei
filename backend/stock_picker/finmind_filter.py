"""
finmind_filter.py — 數值篩選層（v3）

篩選邏輯：
  第一層（必要，任一成立）：金叉型態
    - MA5  上穿 MA20（前日 MA5 <= MA20，今日 MA5 > MA20）
    - MA20 上穿 MA60（前日 MA20 <= MA60，今日 MA20 > MA60）
    - KD 金叉（前日 K <= D，今日 K > D，且 K < 80 非超買）
  第二層（必要）：量能放大
    - 近5日均量 >= 近20日均量 * 1.5
  第三層（必要）：MACD DIF 在 0 軸以上或剛上穿
    - DIF > 0（含由負轉正）
    - 若無股票通過，放寬為 DIF > -0.5
  第四層（加分，影響排序）：
    - 有鉅亨個股新聞：+2
    - 法人連買 >= 3 日：+2
    - 法人連買 >= 2 日：+1
    - KD 金叉：+1
    - MA 均線金叉：+1
  輸出：依總分排序，取前 20 名
"""

from crawler import fetch_price_history, fetch_institutional
import time


CFG = {
    "min_avg_volume":      300,
    "min_price":           10.0,
    "vol_ratio_threshold": 1.5,
}


# ──────────────────────────────────────────
# 技術指標計算
# ──────────────────────────────────────────

def calc_kd(prices: list[dict], n: int = 9) -> tuple[float, float, float, float]:
    """
    計算隨機指標 KD（n 日 RSV，預設 9 日）
    回傳 (K今, D今, K昨, D昨)；資料不足時回傳 (50, 50, 50, 50)
    """
    if len(prices) < n + 1:
        return 50.0, 50.0, 50.0, 50.0

    K, D = 67.0, 67.0
    K_prev, D_prev = 67.0, 67.0

    for i in range(n - 1, len(prices)):
        window = prices[i - n + 1: i + 1]
        high9  = max(p["high"] for p in window)
        low9   = min(p["low"]  for p in window)
        close  = prices[i]["close"]
        rsv    = (close - low9) / (high9 - low9) * 100 if high9 != low9 else 50.0
        K_prev, D_prev = K, D
        K = K * 2 / 3 + rsv / 3
        D = D * 2 / 3 + K   / 3

    return K, D, K_prev, D_prev


def calc_macd(closes: list[float]) -> tuple[float, float]:
    """
    計算 MACD DIF（EMA12 - EMA26）
    回傳 (DIF今, DIF昨)；資料不足時回傳 (0.0, 0.0)
    """
    if len(closes) < 27:
        return 0.0, 0.0

    def _ema_series(data: list[float], period: int) -> list[float]:
        k    = 2 / (period + 1)
        seed = sum(data[:period]) / period
        out  = [seed]
        for p in data[period:]:
            seed = p * k + seed * (1 - k)
            out.append(seed)
        return out

    ema12 = _ema_series(closes, 12)
    ema26 = _ema_series(closes, 26)
    # ema12 比 ema26 長；兩者皆以最新日收尾，從尾端對齊
    dif = [a - b for a, b in zip(ema12[-len(ema26):], ema26)]

    if len(dif) < 2:
        return dif[-1] if dif else 0.0, 0.0
    return dif[-1], dif[-2]


# ──────────────────────────────────────────
# K 線型態偵測
# ──────────────────────────────────────────

def detect_kline_patterns(closes, opens, highs, lows, volumes):
    """偵測最新 K 線型態，回傳 (型態標籤, 勝率)"""
    n = len(closes)
    if n < 3:
        return "常態 K 線（無觸發極端型態）", 0.50
    c0, o0, h0, l0, v0 = closes[-1], opens[-1], highs[-1], lows[-1], volumes[-1]
    body_size0    = abs(c0 - o0)
    upper_shadow0 = h0 - max(c0, o0)
    lower_shadow0 = min(c0, o0) - l0
    range0        = max(h0 - l0, 0.001)
    avg_vol       = sum(volumes[-6:-1]) / 5 if n >= 6 else (sum(volumes[:-1]) / max(len(volumes) - 1, 1))
    vol_surge     = v0 > avg_vol * 1.3
    is_downtrend  = closes[-1] < closes[-5] if n >= 5 else False
    is_uptrend    = closes[-1] > closes[-5] if n >= 5 else False
    if vol_surge and (body_size0 >= range0 * 0.5) and (c0 > o0):
        return "量增大紅棒（突破確認）", 0.62
    if vol_surge and (body_size0 >= range0 * 0.5) and (c0 < o0):
        return "量增大黑棒（跌破確認）", 0.62
    if (is_downtrend and (lower_shadow0 >= range0 * 0.4)
            and (lower_shadow0 >= body_size0 * 1.5)
            and (upper_shadow0 <= range0 * 0.2)):
        return "低檔錘子線（底部承接力道強）", 0.53
    if (is_uptrend and (upper_shadow0 >= range0 * 0.4)
            and (upper_shadow0 >= body_size0 * 1.5)
            and (lower_shadow0 <= range0 * 0.2)):
        return "高檔流星線（多頭上攻力竭）", 0.53
    return "常態 K 線（無觸發極端型態）", 0.50


# ──────────────────────────────────────────
# 主篩選函數
# ──────────────────────────────────────────

def analyze_stock(stock_id: str, news_list: list[dict]) -> dict | None:
    """
    對單一股票計算技術指標並標記各層通過狀態。
    回傳 dict（含 pass_l1/l2/l3/pass_l3_relaxed/score），或 None（資料不足）。
    """
    # ── 股價資料（拉 90 日曆天 ≈ 60~65 交易日，支援 MA60+KD+MACD）──
    prices = fetch_price_history(stock_id, days=90)
    if len(prices) < 26:
        return None

    price = prices[-1]["close"]
    if price < CFG["min_price"]:
        return None

    closes = [p["close"] for p in prices]
    m      = len(closes)

    if m < 21:
        return None

    # ── MA 計算 ──
    ma5_t  = sum(closes[-5:])    / 5
    ma5_y  = sum(closes[-6:-1])  / 5
    ma20_t = sum(closes[-20:])   / 20
    ma20_y = sum(closes[-21:-1]) / 20

    if m >= 61:
        ma60_t = sum(closes[-60:])   / 60
        ma60_y = sum(closes[-61:-1]) / 60
    else:
        ma60_t = ma60_y = None

    # 均線金叉
    ma5_20_cross  = (ma5_t > ma20_t) and (ma5_y <= ma20_y)
    ma20_60_cross = (ma60_t is not None
                     and ma20_t > ma60_t and ma20_y <= ma60_y)
    ma_cross      = ma5_20_cross or ma20_60_cross

    # ── KD ──
    K_t, D_t, K_y, D_y = calc_kd(prices)
    kd_cross = (K_t > D_t) and (K_y <= D_y) and (K_t < 80)

    # ── MACD ──
    dif_t, dif_y      = calc_macd(closes)
    macd_cross_zero   = (dif_y < 0) and (dif_t > 0)   # 由負轉正
    macd_pass         = dif_t > 0                       # 含上穿0軸
    macd_pass_relaxed = dif_t > -0.5

    # ── 量能 ──
    vols       = [p["volume"] for p in prices if p["volume"] > 0]
    avg_vol_20 = sum(vols[-20:]) / min(20, len(vols)) if vols else 0
    avg_vol_5  = sum(p["volume"] for p in prices[-5:]) / 5
    vol_ratio  = round(avg_vol_5 / avg_vol_20, 2) if avg_vol_20 > 0 else 0

    if avg_vol_20 < CFG["min_avg_volume"]:
        return None

    # ── 篩選層旗標 ──
    pass_l1         = ma_cross or kd_cross
    pass_l2         = avg_vol_5 >= avg_vol_20 * CFG["vol_ratio_threshold"]
    pass_l3         = macd_pass
    pass_l3_relaxed = macd_pass_relaxed

    # ── 新聞（加分用，不作為必要條件）──
    related_news = []
    for n in news_list:
        if stock_id in n["codes"] and n["title"]:
            related_news.append({
                "title":    n["title"],
                "link":     n["link"],
                "keywords": n["keywords"],
            })
    has_news = bool(related_news)

    # ── 法人（L1+L2 皆通過才呼叫 API，節省配額）──
    consecutive_buy_days = 0
    inst_5d_total        = 0
    inst_20d_total       = 0
    if pass_l1 and pass_l2:
        inst = fetch_institutional(stock_id, days=20)
        if inst:
            for row in reversed(inst):
                if row["total"] > 0:
                    consecutive_buy_days += 1
                else:
                    break
            inst_5d_total  = sum(r["total"] for r in inst[-5:])
            inst_20d_total = sum(r["total"] for r in inst)

    # ── 第四層評分 ──
    score = 0
    if has_news:                    score += 2
    if consecutive_buy_days >= 3:   score += 2
    elif consecutive_buy_days >= 2: score += 1
    if kd_cross:                    score += 1
    if ma_cross:                    score += 1

    # ── 信號標籤 ──
    if ma5_20_cross and ma20_60_cross:
        signal_label = "✅ 雙均線金叉"
    elif ma5_20_cross:
        signal_label = "✅ MA5穿MA20金叉"
    elif ma20_60_cross:
        signal_label = "✅ MA20穿MA60金叉"
    elif kd_cross:
        signal_label = f"✅ KD金叉（K={K_t:.1f}）"
    else:
        signal_label = ""

    # ── K 線型態 ──
    kline_pattern, win_rate = detect_kline_patterns(
        closes,
        [p["open"]   for p in prices],
        [p["high"]   for p in prices],
        [p["low"]    for p in prices],
        [p["volume"] for p in prices],
    )

    kws = list({kw for n in related_news for kw in n["keywords"]})
    macd_desc = "上穿0軸" if macd_cross_zero else ("0軸以上" if dif_t > 0 else "0軸以下")
    score_factors = [
        f"鉅亨題材新聞 {len(related_news)} 則" + (f"，關鍵字：{', '.join(kws[:5])}" if kws else ""),
        f"量能：近5日均量是20日均量的 {vol_ratio}x（門檻 {CFG['vol_ratio_threshold']}x）",
        f"MACD DIF={dif_t:.3f}（{macd_desc}）",
        f"KD: K={K_t:.1f} D={D_t:.1f}（{'金叉' if kd_cross else '未金叉'}）",
        f"法人連買 {consecutive_buy_days} 日，近5日 {inst_5d_total:+,} 張，近20日 {inst_20d_total:+,} 張",
        f"現價 {price}，近5日均量 {round(avg_vol_5):,} 張",
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
        # 篩選層旗標（供 run_filter 判斷，不傳給 generator）
        "pass_l1":              pass_l1,
        "pass_l2":              pass_l2,
        "pass_l3":              pass_l3,
        "pass_l3_relaxed":      pass_l3_relaxed,
        "score":                score,
    }


def run_filter(candidate_ids: list[str], news_list: list[dict],
               max_results: int = 20, delay: float = 1.0) -> list[dict]:
    """
    對候選代號逐一分析，三層篩選後依分數排序，回傳前 max_results 檔。
    若無股票通過第三層，自動放寬 DIF 門檻（> -0.5）再篩一次。
    """
    all_analyzed = []
    total = len(candidate_ids)
    print(f"[filter] 開始篩選 {total} 檔候選股票...")

    for i, sid in enumerate(candidate_ids, 1):
        print(f"[filter] ({i}/{total}) {sid} ...", end=" ", flush=True)
        r = analyze_stock(sid, news_list)
        if r:
            all_analyzed.append(r)
            print(
                f"L1={'✓' if r['pass_l1'] else '✗'} "
                f"L2={'✓' if r['pass_l2'] else '✗'} "
                f"L3={'✓' if r['pass_l3'] else '✗'} "
                f"分={r['score']}"
            )
        else:
            print("✗ 資料不足")
        if i < total:
            time.sleep(delay)

    # 正常篩選：L1 + L2 + L3
    passed = [r for r in all_analyzed
              if r["pass_l1"] and r["pass_l2"] and r["pass_l3"]]

    # 備援：放寬 L3（DIF > -0.5）
    if not passed:
        print("[filter] ⚠️ 無股票通過三層篩選，放寬第三層（DIF > -0.5）")
        passed = [r for r in all_analyzed
                  if r["pass_l1"] and r["pass_l2"] and r["pass_l3_relaxed"]]

    passed.sort(key=lambda x: x["score"], reverse=True)
    result = passed[:max_results]
    print(f"[filter] 篩選完畢：{len(result)} 檔通過（共 {total} 檔候選）")
    return result


if __name__ == "__main__":
    from crawler import fetch_cnyes_news
    news = fetch_cnyes_news(30)
    result = analyze_stock("2330", news)
    if result:
        print("通過：", result)
    else:
        print("未通過篩選條件")
