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


if __name__ == "__main__":
    from crawler import fetch_cnyes_news
    news = fetch_cnyes_news(30)
    result = analyze_stock("2330", news)
    if result:
        print("通過：", result)
    else:
        print("未通過篩選條件")
