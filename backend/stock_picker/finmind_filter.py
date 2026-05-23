"""
finmind_filter.py — 數值分析層（SEO 熱門股模式）

輸入：TWSE 成交量前 30 支（已為主流股，無需交集篩選）
基本門檻（排除資料不足）：
  - FinMind 至少 26 筆日 K
  - 最低股價 $10
  - 均量 >= 1000 張

輸出：對全部通過門檻的股票做技術分析，依 20 日均量降序排列
"""

from crawler import fetch_price_history, fetch_institutional
import time


CFG = {
    "min_avg_volume": 1000,
    "min_price":      10.0,
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


def calc_macd(closes: list[float]) -> tuple[float, float, float]:
    """
    計算 MACD DIF（EMA12-EMA26）與 DEA（EMA9 of DIF）
    回傳 (DIF今, DIF昨, DEA今)；資料不足時回傳 (0.0, 0.0, 0.0)
    """
    if len(closes) < 27:
        return 0.0, 0.0, 0.0

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
    dif   = [a - b for a, b in zip(ema12[-len(ema26):], ema26)]

    if len(dif) < 2:
        v = dif[-1] if dif else 0.0
        return v, 0.0, v
    dea_t = _ema_series(dif, 9)[-1] if len(dif) >= 9 else dif[-1]
    return dif[-1], dif[-2], round(dea_t, 3)


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

def analyze_stock(stock_id: str, news_list: list[dict] = []) -> dict | None:
    """
    對單一股票計算技術指標，回傳 dict 或 None（資料不足/未達門檻）。
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
    dif_t, dif_y, dea_t = calc_macd(closes)
    macd_cross_zero   = (dif_y < 0) and (dif_t > 0)   # 由負轉正
    macd_pass         = dif_t > 0                       # 含上穿0軸
    macd_pass_relaxed = dif_t > -0.5

    # ── 量能 ──
    vols       = [p["volume"] for p in prices if p["volume"] > 0]
    avg_vol_20 = sum(vols[-20:]) / min(20, len(vols)) if vols else 0
    avg_vol_5  = sum(p["volume"] for p in prices[-5:]) / 5
    vol_ratio  = round(avg_vol_5 / avg_vol_20, 2) if avg_vol_20 > 0 else 0

    if avg_vol_20 / 1000 < CFG["min_avg_volume"]:
        return None

    # ── 均線趨勢 ──
    if ma60_t is not None:
        if ma5_t > ma20_t > ma60_t:
            trend = "上升"
        elif ma5_t < ma20_t < ma60_t:
            trend = "下降"
        else:
            trend = "盤整"
    else:
        trend = "上升" if ma5_t > ma20_t else ("下降" if ma5_t < ma20_t else "盤整")

    # ── 新聞（加分用）──
    related_news = []
    for n in news_list:
        if stock_id in n["codes"] and n["title"]:
            related_news.append({
                "title":    n["title"],
                "link":     n["link"],
                "keywords": n["keywords"],
            })
    has_news = bool(related_news)

    # ── K棒連K方向 ──
    kbar_streak = 0
    for _p in reversed(prices):
        _c, _o = _p["close"], _p["open"]
        if kbar_streak == 0:
            kbar_streak = 1 if _c >= _o else -1
        elif kbar_streak > 0 and _c >= _o:
            kbar_streak += 1
        elif kbar_streak < 0 and _c < _o:
            kbar_streak -= 1
        else:
            break

    # ── 支撐壓力（近20日）──
    recent20 = prices[-20:]
    resistance = round(max(p["high"] for p in recent20), 2)
    lows_20    = [p["low"] for p in recent20]
    s_candidates = [ma20_t, min(lows_20)]
    if ma60_t:
        s_candidates.append(ma60_t)
    below = [x for x in s_candidates if x < price]
    support = round(max(below) if below else min(s_candidates), 2)

    # ── 損益比 ──
    if support and resistance and price > 0 and resistance > price:
        risk   = price - support
        reward = resistance - price
        if risk > 0:
            rr = round(reward / risk, 2)
            if   rr >= 3:   rr_label = '極佳'
            elif rr >= 2:   rr_label = '良好'
            elif rr >= 1.5: rr_label = '尚可'
            else:           rr_label = '偏低'
        else:
            rr, rr_label = 0, '無法計算'
    else:
        rr, rr_label = 0, '無法計算'

    # ── 法人買賣超 ──
    consecutive_buy_days = 0
    inst_5d_total        = 0
    inst_20d_total       = 0
    inst_foreign_5d      = 0
    inst_invest_5d       = 0
    inst_dealer_5d       = 0
    inst = fetch_institutional(stock_id, days=20)
    if inst:
        for row in reversed(inst):
            if row["total"] > 0:
                consecutive_buy_days += 1
            else:
                break
        inst_5d        = inst[-5:]
        inst_5d_total  = sum(r["total"]              for r in inst_5d)
        inst_20d_total = sum(r["total"]              for r in inst)
        inst_foreign_5d = sum(r.get("foreign", 0)   for r in inst_5d)
        inst_invest_5d  = sum(r.get("invest",  0)   for r in inst_5d)
        inst_dealer_5d  = sum(r.get("dealer",  0)   for r in inst_5d)

    # ── 評分 ──
    score = 0
    if has_news:                    score += 2
    if consecutive_buy_days >= 3:   score += 2
    elif consecutive_buy_days >= 1: score += 1
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
        f"量能：近5日均量是20日均量的 {vol_ratio}x",
        f"MACD DIF={dif_t:.3f}（{macd_desc}）",
        f"KD: K={K_t:.1f} D={D_t:.1f}（{'金叉' if kd_cross else '未金叉'}）",
        f"法人連買 {consecutive_buy_days} 日，近5日 {inst_5d_total:+,} 張，近20日 {inst_20d_total:+,} 張",
        f"現價 {price}，近5日均量 {round(avg_vol_5 / 1000):,} 張",
    ]
    if signal_label:
        score_factors.append(f"型態：{signal_label}")

    return {
        "stock_id":             stock_id,
        "price":                price,
        "ma5":                  round(ma5_t, 2),
        "ma20":                 round(ma20_t, 2),
        "ma60":                 round(ma60_t, 2) if ma60_t else None,
        "kd_k":                 round(K_t, 1),
        "kd_d":                 round(D_t, 1),
        "kd_cross":             kd_cross,
        "consecutive_buy_days": consecutive_buy_days,
        "inst_5d_total":        inst_5d_total,
        "inst_20d_total":       inst_20d_total,
        "inst_foreign_5d":      inst_foreign_5d,
        "inst_invest_5d":       inst_invest_5d,
        "inst_dealer_5d":       inst_dealer_5d,
        "vol_ratio":            vol_ratio,
        "avg_vol_5":            round(avg_vol_5 / 1000),
        "avg_vol_20":           round(avg_vol_20 / 1000),
        "news":                 related_news[:5],
        "score_factors":        score_factors,
        "signal_label":         signal_label,
        "is_risk":              False,
        "kline_pattern":        kline_pattern,
        "win_rate":             win_rate,
        "trend":                trend,
        "macd_dif":             round(dif_t, 3),
        "macd_dea":             round(dea_t, 3),
        "kbar_streak":          kbar_streak,
        "support":              support,
        "resistance":           resistance,
        "target_price":         round(resistance + (resistance - support), 2),
        "support_too_close":    bool((price - support) / price < 0.02) if price > 0 else False,
        "rr":                   rr,
        "rr_label":             rr_label,
        "macd_desc":            macd_desc,
        "score":                score,
    }


def run_filter(candidate_ids: list[str], news_list: list[dict] = [],
               max_results: int = 30, delay: float = 1.0) -> list[dict]:
    """
    對候選代號逐一做 FinMind 技術分析，通過基本門檻（價格/均量/資料量）後
    依 20 日均量降序排列（SEO 熱門股模式：保留主流大量股的自然排序）。
    """
    passed = []
    total = len(candidate_ids)
    print(f"[filter] 開始分析 {total} 檔（SEO 熱門股模式，依成交量排序）...")

    for i, sid in enumerate(candidate_ids, 1):
        print(f"[filter] ({i}/{total}) {sid} ...", end=" ", flush=True)
        r = analyze_stock(sid, news_list)
        if r:
            passed.append(r)
            print(f"✓（均量={r['avg_vol_20']:,}張，法人連買 {r['consecutive_buy_days']}日）")
        else:
            print("✗ 資料不足或未達門檻")
        if i < total:
            time.sleep(delay)

    passed.sort(key=lambda x: x["avg_vol_20"], reverse=True)
    result = passed[:max_results]
    print(f"[filter] 分析完畢：{len(result)} 支（共 {total} 檔候選）")
    return result


if __name__ == "__main__":
    from crawler import fetch_cnyes_news
    news = fetch_cnyes_news(30)
    result = analyze_stock("2330", news)
    if result:
        print("通過：", result)
    else:
        print("未通過篩選條件")
