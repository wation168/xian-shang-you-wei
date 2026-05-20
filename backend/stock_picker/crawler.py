"""
crawler.py — 資料爬取層
1. 鉅亨 RSS：抓近一週財經新聞，萃取出現的股票代號與題材關鍵字（不打 FinMind）
2. TWSE STOCK_DAY_ALL：取上市股成交量前100（不打 FinMind）
3. FinMind：僅用於最終候選股的技術分析（≤50 支）
"""

import os
import re
import json
import ssl
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from xml.etree import ElementTree as ET


FINMIND_TOKEN = os.environ.get("FINMIND_TOKEN", "")

# SSL context 供 TWSE 使用（TWSE 憑證缺少 Subject Key Identifier，無法通過預設驗證）
_TWSE_SSL_CTX = ssl.create_default_context()
_TWSE_SSL_CTX.check_hostname = False
_TWSE_SSL_CTX.verify_mode = ssl.CERT_NONE

# ──────────────────────────────────────────
# 財經新聞 RSS feeds
# ──────────────────────────────────────────
CNYES_FEEDS = [
    "https://feeds.feedburner.com/cnyes",                   # 鉅亨頭條
    "https://tw.stock.yahoo.com/rss",                       # Yahoo 台股
    "https://money.udn.com/rssfeed/news/1001/5590",         # 經濟日報個股
]

# 股票代號正則（4~6碼數字，後接中文公司名 or 括號）
_CODE_RE = re.compile(r"[（(](\d{4,6})[)）]|(?<!\d)(\d{4,6})(?=[^\d]|$)")

# 過濾掉太常見、無意義的數字（年份、百分比等）
_SKIP_NUMS = {"2024", "2025", "2026", "1000", "5000", "10000",
              "100", "200", "500", "300", "400", "600", "700", "800", "900"}


def fetch_cnyes_news(max_items: int = 300, days: int = 7) -> list[dict]:
    """
    爬取鉅亨 RSS，回傳近 days 天的新聞列表（預設近7天）
    每筆: {title, link, pub_date, codes: [股票代號...], keywords: [關鍵字...]}
    """
    from email.utils import parsedate_to_datetime

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
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
                # 日期篩選：超過 days 天的略過
                if pub:
                    try:
                        dt = parsedate_to_datetime(pub)
                        if dt < cutoff:
                            continue
                    except Exception:
                        pass
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

    print(f"[crawler] 鉅亨 RSS 共取得 {len(items)} 則新聞（近{days}天）")
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
# TWSE 成交量排行（不打 FinMind）
# ──────────────────────────────────────────

def fetch_twse_volume_top(n: int = 30) -> tuple[list[str], dict[str, str]]:
    """
    從 TWSE STOCK_DAY_ALL 取最近交易日成交量前 n 支上市股
    回傳 (top_n_stock_ids, name_dict)  — 單次 HTTP 呼叫，不打 FinMind
    """
    today = date.today().strftime("%Y%m%d")
    url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=json&date={today}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12, context=_TWSE_SSL_CTX) as resp:
            data = json.loads(resp.read())

        if data.get("stat") not in ("OK", "ok"):
            print(f"[crawler] TWSE STOCK_DAY_ALL stat={data.get('stat')}，嘗試不帶日期")
            # fallback：不帶 date 參數
            url2 = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=json"
            req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req2, timeout=12, context=_TWSE_SSL_CTX) as resp2:
                data = json.loads(resp2.read())

        rows = data.get("data", [])
        name_dict: dict[str, str] = {}
        volume_stocks: list[tuple[str, int]] = []

        for row in rows:
            if len(row) < 3:
                continue
            code = str(row[0]).strip()
            name = str(row[1]).strip()
            # 只取純 4 碼數字（上市普通股 + ETF，排除權證/特別股等）
            if not re.match(r"^\d{4}$", code):
                continue
            try:
                vol = int(str(row[2]).replace(",", ""))
            except Exception:
                continue
            if vol <= 0:
                continue
            name_dict[code] = name
            volume_stocks.append((code, vol))

        volume_stocks.sort(key=lambda x: x[1], reverse=True)
        top_ids = [s[0] for s in volume_stocks[:n]]
        print(f"[crawler] TWSE 成交量排行：前{n}支（共{len(volume_stocks)}支上市股）")
        return top_ids, name_dict

    except Exception as e:
        print(f"[crawler] fetch_twse_volume_top 失敗：{e}")
        return [], {}


def build_candidates(
    news_codes: list[str],
    volume_ids: list[str],
    max_candidates: int = 50,
) -> list[str]:
    """
    智慧合併新聞候選 + TWSE成交量排行，交集優先，聯集填滿，上限 max_candidates
    優先順序：
      1. 同時出現在新聞和成交量排行 → 最熱門
      2. 只出現在新聞（按首次出現順序）
      3. 只出現在成交量排行（按成交量排序）
    """
    volume_set = set(volume_ids)
    news_set   = set(news_codes)
    seen: set[str] = set()
    result: list[str] = []

    # Priority 1: 交集
    for c in news_codes:
        if c in volume_set and c not in seen:
            seen.add(c)
            result.append(c)

    # Priority 2: 新聞專屬
    for c in news_codes:
        if c not in seen:
            seen.add(c)
            result.append(c)
            if len(result) >= max_candidates:
                break

    # Priority 3: 成交量排行補位
    if len(result) < max_candidates:
        for c in volume_ids:
            if c not in seen:
                seen.add(c)
                result.append(c)
                if len(result) >= max_candidates:
                    break

    result = result[:max_candidates]
    inter = sum(1 for c in result if c in volume_set and c in news_set)
    print(f"[crawler] 候選清單：{len(result)} 支（交集{inter}，新聞{len(news_set)}，排行{len(volume_ids)}）")
    return result


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
            # FinMind 回傳單位為股，除以 1000 換算成張
            net  = (int(r.get("buy", 0) or 0) - int(r.get("sell", 0) or 0)) // 1000
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


def get_all_tw_stocks() -> list[str]:
    """取得全台上市（TWSE）及上櫃（OTC）股票代號列表"""
    url = f"https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockInfo&token={FINMIND_TOKEN}"
    try:
        data = _finmind_request(url)
        if data.get("status") != 200:
            return []
        return [
            str(item["stock_id"])
            for item in data.get("data", [])
            if item.get("type", "").lower() in ("twse", "otc")
            and item.get("stock_id")
        ]
    except Exception as e:
        print(f"[crawler] get_all_tw_stocks 失敗：{e}")
        return []


if __name__ == "__main__":
    # 快速測試
    news = fetch_cnyes_news(20)
    print(f"新聞數：{len(news)}")
    for n in news[:3]:
        print(f"  標題：{n['title'][:40]}")
        print(f"  代號：{n['codes']}  關鍵字：{n['keywords']}")
