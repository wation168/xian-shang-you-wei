"""
crawler.py — 資料爬取層
1. 鉅亨 RSS：抓最新財經新聞，萃取出現的股票代號與題材關鍵字
2. FinMind：拉近 60 日股價（算回檔幅度）＋近 20 日法人買賣超
"""

import os
import re
import json
import time
import urllib.request
from datetime import date, timedelta
from xml.etree import ElementTree as ET


FINMIND_TOKEN = os.environ.get("FINMIND_TOKEN", "")

# ──────────────────────────────────────────
# 鉅亨 RSS feeds
# ──────────────────────────────────────────
CNYES_FEEDS = [
    "https://feeds.feedburner.com/cnyes",               # 頭條
    "https://news.cnyes.com/rss/category/tw_stock",     # 台股
    "https://news.cnyes.com/rss/category/fund",         # 產業
]

# 股票代號正則（4~6碼數字，後接中文公司名 or 括號）
_CODE_RE = re.compile(r"[（(](\d{4,6})[)）]|(?<!\d)(\d{4,6})(?=[^\d]|$)")

# 過濾掉太常見、無意義的數字（年份、百分比等）
_SKIP_NUMS = {"2024", "2025", "2026", "1000", "5000", "10000",
              "100", "200", "500", "300", "400", "600", "700", "800", "900"}


def fetch_cnyes_news(max_items: int = 80) -> list[dict]:
    """
    爬取鉅亨 RSS，回傳新聞列表
    每筆: {title, link, pub_date, codes: [股票代號...], keywords: [關鍵字...]}
    """
    items = []
    seen_links = set()

    for feed_url in CNYES_FEEDS:
        try:
            req = urllib.request.Request(
                feed_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                xml = resp.read()
            root = ET.fromstring(xml)
            channel = root.find("channel")
            if channel is None:
                continue
            for item in channel.findall("item"):
                title = (item.findtext("title") or "").strip()
                link  = (item.findtext("link")  or "").strip()
                pub   = (item.findtext("pubDate") or "").strip()
                desc  = (item.findtext("description") or "").strip()
                if not title or link in seen_links:
                    continue
                seen_links.add(link)
                full_text = title + " " + desc
                codes = _extract_codes(full_text)
                keywords = _extract_keywords(title)
                items.append({
                    "title":    title,
                    "link":     link,
                    "pub_date": pub,
                    "codes":    codes,
                    "keywords": keywords,
                })
                if len(items) >= max_items:
                    break
        except Exception as e:
            print(f"[crawler] RSS {feed_url} 失敗：{e}")

    print(f"[crawler] 鉅亨 RSS 共取得 {len(items)} 則新聞")
    return items


def _extract_codes(text: str) -> list[str]:
    codes = []
    for m in _CODE_RE.finditer(text):
        c = m.group(1) or m.group(2)
        if c and c not in _SKIP_NUMS and len(c) in (4, 5, 6):
            if c not in codes:
                codes.append(c)
    return codes


# 題材關鍵字列表（可視需求擴充）
_KEYWORDS = [
    "AI", "人工智慧", "半導體", "CoWoS", "HBM", "伺服器", "資料中心",
    "車用", "電動車", "儲能", "太陽能", "綠能", "5G", "光通訊",
    "航太", "國防", "機器人", "軟板", "PCB", "散熱", "銅箔基板",
    "記憶體", "DRAM", "NAND", "封測", "先進封裝", "玻璃基板",
    "訂單", "拉貨", "出貨", "轉單", "接單", "滿載", "擴產", "擴廠",
    "法說", "獲利", "EPS", "營收創高", "連續買超", "外資買",
]

def _extract_keywords(title: str) -> list[str]:
    return [kw for kw in _KEYWORDS if kw in title]


# ──────────────────────────────────────────
# FinMind 工具函式
# ──────────────────────────────────────────
def _finmind_request(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=12) as resp:
        return json.loads(resp.read())


def fetch_price_history(stock_id: str, days: int = 65) -> list[dict]:
    """
    拉近 N 天日 K 資料（用 FinMind TaiwanStockPrice）
    回傳 [{date, open, high, low, close, volume}, ...]
    """
    start = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    end   = date.today().strftime("%Y-%m-%d")
    url = (f"https://api.finmindtrade.com/api/v4/data"
           f"?dataset=TaiwanStockPrice&data_id={stock_id}"
           f"&start_date={start}&end_date={end}&token={FINMIND_TOKEN}")
    try:
        data = _finmind_request(url)
        if data.get("status") != 200:
            return []
        rows = data.get("data", [])
        return [
            {
                "date":   r.get("date", "")[:10],
                "open":   float(r.get("open", 0) or 0),
                "high":   float(r.get("max",  0) or r.get("high", 0) or 0),
                "low":    float(r.get("min",  0) or r.get("low",  0) or 0),
                "close":  float(r.get("close", 0) or 0),
                "volume": int(r.get("Trading_Volume", 0) or 0),
            }
            for r in rows
        ]
    except Exception as e:
        print(f"[crawler] fetch_price {stock_id} 失敗：{e}")
        return []


def fetch_institutional(stock_id: str, days: int = 25) -> list[dict]:
    """
    拉近 N 天三大法人買賣超（FinMind TaiwanStockInstitutionalInvestorsBuySell）
    回傳 [{date, foreign, invest, dealer, total}, ...]
    """
    start = (date.today() - timedelta(days=days + 5)).strftime("%Y-%m-%d")
    end   = date.today().strftime("%Y-%m-%d")
    url = (f"https://api.finmindtrade.com/api/v4/data"
           f"?dataset=TaiwanStockInstitutionalInvestorsBuySell&data_id={stock_id}"
           f"&start_date={start}&end_date={end}&token={FINMIND_TOKEN}")
    try:
        data = _finmind_request(url)
        if data.get("status") != 200:
            return []
        daily: dict = {}
        for r in data.get("data", []):
            d    = r.get("date", "")[:10]
            name = r.get("name", "")
            net  = int(r.get("buy", 0) or 0) - int(r.get("sell", 0) or 0)
            if d not in daily:
                daily[d] = {"foreign": 0, "invest": 0, "dealer": 0}
            if "外資" in name or "Foreign" in name:
                daily[d]["foreign"] += net
            elif "投信" in name or "Investment" in name:
                daily[d]["invest"] += net
            elif "自營" in name or "Dealer" in name:
                daily[d]["dealer"] += net
        result = []
        for d in sorted(daily.keys())[-days:]:
            v = daily[d]
            total = v["foreign"] + v["invest"] + v["dealer"]
            result.append({"date": d, **v, "total": total})
        return result
    except Exception as e:
        print(f"[crawler] fetch_institutional {stock_id} 失敗：{e}")
        return []


def fetch_stock_name(stock_id: str) -> str:
    """從 FinMind TaiwanStockInfo 取得股票名稱"""
    url = (f"https://api.finmindtrade.com/api/v4/data"
           f"?dataset=TaiwanStockInfo&token={FINMIND_TOKEN}")
    try:
        data = _finmind_request(url)
        for item in data.get("data", []):
            if str(item.get("stock_id", "")) == stock_id:
                return item.get("stock_name", stock_id)
    except Exception:
        pass
    return stock_id


if __name__ == "__main__":
    # 快速測試
    news = fetch_cnyes_news(20)
    print(f"新聞數：{len(news)}")
    for n in news[:3]:
        print(f"  標題：{n['title'][:40]}")
        print(f"  代號：{n['codes']}  關鍵字：{n['keywords']}")
