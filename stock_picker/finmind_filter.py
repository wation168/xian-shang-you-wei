"""
finmind_filter.py — 數值篩選層
輸入：股票代號列表（從新聞萃取）
輸出：通過篩選的個股，附帶量化指標

選股三要素：
  1. 鉅亨有題材新聞（有故事）← 必要條件
  2. 法人近 N 日連續買超（籌碼回流）
  3. 成交量從低量開始放大（量先價行）
"""

from crawler import fetch_price_history, fetch_institutional
import time


# ──────────────────────────────────────────
# 篩選參數（可調整）
# ──────────────────────────────────────────
CFG = {
    # 【必要條件】鉅亨需有題材新聞才納入
    "require_news": True,

    # 法人連續買超天數門檻
    "min_consecutive_buy_days": 3,

    # 量能放大：近 5 日均量 / 近 20 日均量，超過才算「量增起步」
    "min_vol_ratio": 1.2,

    # 最低成交量（張）：太冷門的過濾掉
    "min_avg_volume": 300,

    # 現價下限（過濾雞蛋水餃股）
    "min_price": 10.0,
}


def analyze_stock(stock_id: str, news_list: list[dict]) -> dict | None:
    """
    對單一股票做量化分析，回傳指標 dict 或 None（不符合條件）

    回傳結構：
    {
      stock_id,
      price, vol_ratio, avg_vol_5, avg_vol_20,
      consecutive_buy_days, inst_5d_total, inst_20d_total,
      news: [{title, link, keywords}],
      score_factors: [...]   ← 給 Claude 看的評分依據
    }
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

    # ── 股價資料 ──
    prices = fetch_price_history(stock_id, days=30)
    if len(prices) < 10:
        return None

    price = prices[-1]["close"]
    if price < CFG["min_price"]:
        return None

    # ── 量能：量先價行判斷 ──
    vols = [p["volume"] for p in prices if p["volume"] > 0]
    avg_vol_20 = sum(vols) / len(vols) if vols else 0
    if avg_vol_20 < CFG["min_avg_volume"]:
        return None

    avg_vol_5 = sum(p["volume"] for p in prices[-5:]) / 5
    vol_ratio = round(avg_vol_5 / avg_vol_20, 2) if avg_vol_20 > 0 else 0
    if vol_ratio < CFG["min_vol_ratio"]:
        return None

    # ── 法人買賣超 ──
    inst = fetch_institutional(stock_id, days=20)
    if not inst:
        consecutive_buy_days = 0
        inst_5d_total = 0
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

    if consecutive_buy_days < CFG["min_consecutive_buy_days"]:
        return None

    # ── 組合評分依據（給 Claude 閱讀）──
    kws = list({kw for n in related_news for kw in n["keywords"]})
    score_factors = [
        f"鉅亨題材新聞 {len(related_news)} 則，關鍵字：{', '.join(kws[:5]) if kws else '無特定題材標籤'}",
        f"法人連續買超 {consecutive_buy_days} 天，近5日合計 {inst_5d_total:+,} 張，近20日 {inst_20d_total:+,} 張",
        f"量能放大：近5日均量是20日均量的 {vol_ratio}x（量先價行跡象{'明顯' if vol_ratio >= 1.5 else '初現'}）",
        f"現價 {price}，近5日均量約 {round(avg_vol_5):,} 張",
    ]

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
    }


def run_filter(candidate_ids: list[str], news_list: list[dict],
               max_results: int = 20, delay: float = 1.0) -> list[dict]:
    """
    對候選代號列表逐一篩選，回傳通過的個股清單
    delay：每檔之間的間隔秒數，避免 FinMind rate limit
    """
    passed = []
    total = len(candidate_ids)
    print(f"[filter] 開始篩選 {total} 檔候選股票...")

    for i, sid in enumerate(candidate_ids, 1):
        print(f"[filter] ({i}/{total}) {sid} ...", end=" ", flush=True)
        result = analyze_stock(sid, news_list)
        if result:
            print(f"✓ 通過（量能 {result['vol_ratio']}x，"
                  f"法人連買 {result['consecutive_buy_days']}日，"
                  f"新聞 {len(result['news'])} 則）")
            passed.append(result)
        else:
            print("✗ 未通過")
        if i < total:
            time.sleep(delay)

    print(f"[filter] 篩選完畢，通過 {len(passed)}/{total} 檔")
    return passed[:max_results]


if __name__ == "__main__":
    from crawler import fetch_cnyes_news
    news = fetch_cnyes_news(30)
    result = analyze_stock("2330", news)
    if result:
        print("通過：", result)
    else:
        print("未通過篩選條件")
