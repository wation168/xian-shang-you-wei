"""
crawler.py — 資料爬取層
1. 鉅亨 RSS：抓近一週財經新聞，萃取出現的股票代號與題材關鍵字（不打 FinMind）
2. TWSE STOCK_DAY_ALL：取上市股成交量前100（不打 FinMind）
3. FinMind：僅用於最終候選股的技術分析（≤50 支）
"""

import os
import re
import ssl as _ssl
import json
import time
import urllib.request
import urllib.error
from datetime import date, datetime, timedelta, timezone
from xml.etree import ElementTree as ET


FINMIND_TOKEN = os.environ.get("FINMIND_TOKEN", "")

# 證交所／櫃買中心網站憑證在部分主機環境驗證會失敗，比照 main.py 的處理方式關閉驗證。
# 只用於讀取兩個交易所公開的盤後統計資料，不涉及任何帳密或個資傳輸。
_TWSE_SSL_CTX = _ssl.create_default_context()
_TWSE_SSL_CTX.check_hostname = False
_TWSE_SSL_CTX.verify_mode = _ssl.CERT_NONE

# ──────────────────────────────────────────
# 鉅亨 RSS feeds
# ──────────────────────────────────────────
CNYES_FEEDS = [
    "https://feeds.feedburner.com/cnyes",                   # 頭條
    "https://news.cnyes.com/rss/category/tw_stock",         # 台股
    "https://news.cnyes.com/rss/category/fund",             # 產業基金
    "https://news.cnyes.com/rss/category/tw_stock_news",    # 個股新聞
    "https://news.cnyes.com/rss/category/industry",         # 產業
]

# 股票代號正則（4~6碼數字，後接中文公司名 or 括號）
_CODE_RE = re.compile(r"[（(](\d{4,6})[)）]|(?<!\d)(\d{4,6})(?=[^\d]|$)")

# 過濾掉太常見、無意義的數字（年份、百分比等）
_SKIP_NUMS = {"2024", "2025", "2026", "1000", "5000", "10000",
              "100", "200", "500", "300", "400", "600", "700", "800", "900"}


def fetch_cnyes_news(max_items: int = 300, days: int = 7) -> list[dict]:
    """
    從鉅亨 RSS 抓近 days 天的財經新聞
    每筆: {title, link, pub_date, codes: [股票代號...], keywords: [關鍵字...]}
    """
    from email.utils import parsedate_to_datetime
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    items = []
    seen_titles = set()

    for feed_url in CNYES_FEEDS:
        try:
            req = urllib.request.Request(feed_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw_xml = resp.read()
            root = ET.fromstring(raw_xml)
            channel = root.find("channel")
            if channel is None:
                continue
            for item in channel.findall("item"):
                title = (item.findtext("title") or "").strip()
                if not title or title in seen_titles:
                    continue
                # 日期過濾
                pub_str = item.findtext("pubDate") or ""
                try:
                    pub_dt = parsedate_to_datetime(pub_str)
                    if pub_dt < cutoff:
                        continue
                except Exception:
                    pass
                seen_titles.add(title)
                link    = item.findtext("link") or ""
                codes   = _extract_codes(title)
                keywords = _extract_keywords(title)
                items.append({
                    "title":    title,
                    "link":     link,
                    "pub_date": pub_str,
                    "codes":    codes,
                    "keywords": keywords,
                })
                if len(items) >= max_items:
                    break
        except Exception as e:
            print(f"[crawler] 鉅亨 RSS 抓取失敗 {feed_url}：{e}")
        if len(items) >= max_items:
            break

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

def _fetch_volume_top_from_twse(n: int) -> tuple[list[str], dict[str, str]]:
    """
    方法一：直接讀證交所盤後全市場統計 STOCK_DAY_ALL（CSV 格式）

    2026/07/27 改用這條路的原因：
      FinMind 的 TaiwanStockPrice「不指定個股、抓全市場」查詢已限制為贊助會員，
      免費(register)等級呼叫會回 400「Your level is register」，導致整個深度選股
      拿不到候選名單。證交所這條是公開資料、不需要金鑰、沒有額度限制。

    注意不要加 ?response=json —— 那個參數在海外IP會被擋403，
    改讀 CSV 是 main.py v8.12 已經驗證過可行的作法（開盤熱門股一直用這條）。

    CSV 欄位順序：
      日期(0) 代號(1) 名稱(2) 成交股數(3) 成交金額(4)
      開盤(5) 最高(6) 最低(7) 收盤(8) 漲跌(9) 成交筆數(10)

    附帶好處：這裡拿得到真正的中文股名，FinMind 那條路只能用代號填充。
    已知差異：STOCK_DAY_ALL 只涵蓋「上市」個股，不含上櫃(OTC)。
    """
    import csv as _csv, io as _io

    url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY_ALL"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer":    "https://www.twse.com.tw/",
    })
    with urllib.request.urlopen(req, timeout=20, context=_TWSE_SSL_CTX) as resp:
        raw_text = resp.read().decode("utf-8-sig", errors="replace")

    name_dict: dict[str, str] = {}
    volume_stocks: list[tuple[str, int]] = []

    for row in _csv.reader(_io.StringIO(raw_text)):
        try:
            if len(row) < 10:
                continue
            code = str(row[1]).strip().strip('="')
            name = str(row[2]).strip().strip('="')
            if not re.match(r"^\d{4}$", code):
                continue
            vol_str = str(row[3]).strip().strip('="').replace(",", "")
            if not vol_str or vol_str in ("--", "X", ""):
                continue
            vol = int(float(vol_str)) // 1000     # 股 → 張
            if vol <= 0:
                continue
            name_dict[code] = name or code
            volume_stocks.append((code, vol))
        except Exception:
            continue

    if not volume_stocks:
        raise ValueError("TWSE CSV 解析後沒有任何有效資料")

    volume_stocks.sort(key=lambda x: x[1], reverse=True)
    top_ids = [c for c, _v in volume_stocks[:n]]
    return top_ids, name_dict


def _fetch_volume_top_from_tpex(n: int) -> tuple[list[str], dict[str, str]]:
    """
    上櫃(OTC)成交量排行 —— 櫃買中心 OpenAPI（公開資料、免金鑰、無額度限制）

    2026/07/27 新增。原本整套只抓上市股，上櫃完全沒被納入候選池。

    端點：/openapi/v1/tpex_mainboard_daily_close_quotes
    回傳為 JSON 陣列，每筆是一檔上櫃有價證券的當日收盤資訊。
    已實際核對過的欄位（不是猜的）：
      SecuritiesCompanyCode 代號（含ETF/債券ETF/權證，需自行過濾）
      CompanyName           中文名稱
      TradingShares         成交股數（單位：股，要 //1000 換成張，與上市一致）
      Date                  民國年日期，例 "1150727"

    注意：全部約 10,000 筆裡只有約 850 檔是 4 碼純數字的普通股，
    其餘是 ETF（006201）、債券ETF（00679B）、權證等，一律過濾掉。
    """
    url = "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept":     "application/json",
    })
    with urllib.request.urlopen(req, timeout=25, context=_TWSE_SSL_CTX) as resp:
        rows = json.loads(resp.read().decode("utf-8-sig", errors="replace"))

    if not isinstance(rows, list) or not rows:
        raise ValueError("櫃買中心回傳格式非預期或為空")

    name_dict: dict[str, str] = {}
    volume_stocks: list[tuple[str, int]] = []

    for row in rows:
        try:
            code = str(row.get("SecuritiesCompanyCode", "")).strip()
            if not re.match(r"^\d{4}$", code):
                continue          # 排除 ETF / 債券ETF / 權證等非普通股
            name = str(row.get("CompanyName", "")).strip()
            vol_str = str(row.get("TradingShares", "")).strip().replace(",", "")
            if not vol_str or vol_str in ("--", "X", ""):
                continue
            vol = int(float(vol_str)) // 1000      # 股 → 張
            if vol <= 0:
                continue
            name_dict[code] = name or code
            volume_stocks.append((code, vol))
        except Exception:
            continue

    if not volume_stocks:
        raise ValueError("櫃買中心資料解析後沒有任何有效個股")

    volume_stocks.sort(key=lambda x: x[1], reverse=True)
    return [c for c, _v in volume_stocks[:n]], name_dict


def _fetch_volume_top_from_finmind(n: int) -> tuple[list[str], dict[str, str]]:
    """
    方法二（備援）：FinMind TaiwanStockPrice 全市場查詢。

    ⚠️ 此查詢目前需要 FinMind 贊助會員等級，免費帳號會收到
       400 "Your level is register"。保留這條路是為了兩種情況：
       ① 證交所網站暫時掛掉時還有替代來源
       ② 之後若升級 FinMind 方案，這條會自動重新可用（還多涵蓋上櫃股）
    """
    if not FINMIND_TOKEN:
        raise ValueError("FINMIND_TOKEN 未設定")

    for days_back in range(0, 6):
        d = date.today() - timedelta(days=days_back)
        if d.weekday() >= 5:
            continue
        target_date = d.strftime("%Y-%m-%d")
        url = (
            f"https://api.finmindtrade.com/api/v4/data"
            f"?dataset=TaiwanStockPrice&start_date={target_date}&end_date={target_date}"
            f"&token={FINMIND_TOKEN}"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = json.loads(resp.read())
        except urllib.error.HTTPError as he:
            # 把 FinMind 回傳的錯誤內容印出來，不要只留 "HTTP Error 400"，
            # 之前就是因為錯誤訊息被吞掉，查了很久才知道是帳號等級問題。
            try:
                detail = he.read().decode("utf-8", errors="replace")[:300]
            except Exception:
                detail = ""
            print(f"[crawler] FinMind 全市場查詢失敗（{target_date}）：{he} {detail}")
            continue
        except Exception as e:
            print(f"[crawler] FinMind 全市場查詢異常（{target_date}）：{e}")
            continue

        if raw.get("status") != 200:
            print(f"[crawler] FinMind 回應非200（{target_date}）：{str(raw)[:200]}")
            continue

        rows = raw.get("data", [])
        if not rows:
            continue

        name_dict: dict[str, str] = {}
        volume_stocks: list[tuple[str, int]] = []
        for row in rows:
            code = str(row.get("stock_id", "")).strip()
            if not re.match(r"^\d{4}$", code):
                continue
            try:
                vol = int(row.get("Trading_Volume", 0))
            except Exception:
                continue
            if vol <= 0:
                continue
            name_dict[code] = code   # 此資料集無股名，用代號填充
            volume_stocks.append((code, vol))

        if not volume_stocks:
            continue

        volume_stocks.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in volume_stocks[:n]], name_dict

    raise ValueError("FinMind 往前 5 個交易日都取不到資料")


def fetch_twse_volume_top(n: int = 100) -> tuple[list[str], dict[str, str]]:
    """
    取最近交易日成交量前 n 支個股（上市＋上櫃合併排行），
    回傳 (top_n_stock_ids, name_dict)。

    2026/07/27 改版重點：
      ① 主要來源改為兩個交易所的公開資料（免金鑰、無額度限制、有中文股名）：
           上市 → 證交所 STOCK_DAY_ALL CSV
           上櫃 → 櫃買中心 OpenAPI tpex_mainboard_daily_close_quotes
         兩邊成交量單位都是「股」，統一 //1000 換成「張」後再合併排序，
         所以上市上櫃是放在同一個基準上比較，不是各取一半硬湊。
      ② FinMind 全市場查詢降為最後備援 —— 該查詢已限定贊助會員，
         免費(register)等級呼叫會回 400，這是 2026/07/27 深度選股整個
         跑不動的真正原因。

    容錯設計：上市、上櫃任一邊失敗，另一邊的結果照樣回傳（降級但仍可用），
    只有兩邊都失敗才會退到 FinMind；全部失敗才回空值，
    呼叫端（main.py）會印訊息並跳過本次執行，不會讓排程整段崩潰。

    函式名稱保留 fetch_twse_volume_top 是為了不動到既有呼叫端，
    實際涵蓋範圍已包含上櫃。
    """
    merged: list[tuple[str, int]] = []      # 這裡不保留量，只用來記順序
    name_dict: dict[str, str] = {}
    twse_ok = tpex_ok = False

    # 為了正確合併排序，需要各自的「代號→張數」，所以兩個內部函式各回傳
    # 前 n 名即可（合併後再取前 n），單一市場最多也就貢獻 n 檔。
    twse_ids: list[str] = []
    tpex_ids: list[str] = []

    try:
        twse_ids, twse_names = _fetch_volume_top_from_twse(n)
        name_dict.update(twse_names)
        twse_ok = True
        print(f"[crawler] 上市(證交所CSV)成交量排行取得 {len(twse_ids)} 檔")
    except Exception as e:
        print(f"[crawler] 上市(證交所CSV)取得失敗：{e}")

    try:
        tpex_ids, tpex_names = _fetch_volume_top_from_tpex(n)
        name_dict.update(tpex_names)
        tpex_ok = True
        print(f"[crawler] 上櫃(櫃買中心)成交量排行取得 {len(tpex_ids)} 檔")
    except Exception as e:
        print(f"[crawler] 上櫃(櫃買中心)取得失敗：{e}")

    if twse_ok or tpex_ok:
        # 兩邊各自已依成交量排序，用交叉合併保留各自的相對名次，
        # 避免只取單一市場的頭部而讓另一個市場完全落榜。
        combined: list[str] = []
        seen: set[str] = set()
        for i in range(max(len(twse_ids), len(tpex_ids))):
            for lst in (twse_ids, tpex_ids):
                if i < len(lst) and lst[i] not in seen:
                    seen.add(lst[i])
                    combined.append(lst[i])
        top_ids = combined[:n]
        _mk = "上市＋上櫃" if (twse_ok and tpex_ok) else ("僅上市" if twse_ok else "僅上櫃")
        print(f"[crawler] 合併後取前 {len(top_ids)} 檔（{_mk}）")
        return top_ids, name_dict

    # 兩個交易所都失敗，退回 FinMind
    try:
        top_ids, fm_names = _fetch_volume_top_from_finmind(n)
        print(f"[crawler] FinMind 備援成交量排行：前{n}支")
        return top_ids, fm_names
    except Exception as e:
        print(f"[crawler] FinMind 備援也失敗：{e}")

    print("[crawler] fetch_twse_volume_top 所有來源失敗")
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


# ──────────────────────────────────────────
# TWSE 三大法人買賣超（T86）— 免費，不需 token
# ──────────────────────────────────────────

def fetch_twse_institutional(stock_id: str, days: int = 3) -> dict:
    """
    從 TWSE T86 抓近 days 個交易日的三大法人買賣超
    回傳 {
        foreign_3d: int,   # 外資近3日合計（張）
        invest_3d:  int,   # 投信近3日合計（張）
        dealer_3d:  int,   # 自營近3日合計（張）
        total_3d:   int,   # 合計
        rows: [...]        # 原始每日明細
    }
    """
    results = {"foreign_3d": 0, "invest_3d": 0, "dealer_3d": 0, "total_3d": 0, "rows": []}
    today = date.today()
    days_checked = 0
    days_collected = 0

    while days_checked < 10 and days_collected < days:
        d = today - timedelta(days=days_checked)
        days_checked += 1
        # 跳過週末
        if d.weekday() >= 5:
            continue
        date_str = d.strftime("%Y%m%d")
        url = f"https://www.twse.com.tw/fund/T86?response=json&date={date_str}&selectType=ALLBUT0999"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read())
            if data.get("stat") not in ("OK", "ok"):
                continue
            rows = data.get("data", [])
            for row in rows:
                if not row or str(row[0]).strip() != stock_id:
                    continue
                # 欄位：證券代號,證券名稱,外資買進,外資賣出,外資買賣超,投信買進,投信賣出,投信買賣超,自營買進,自營賣出,自營買賣超,...
                try:
                    def _parse(v):
                        return int(str(v).replace(",", "").replace("+", "") or 0)
                    foreign = _parse(row[4]) if len(row) > 4 else 0
                    invest  = _parse(row[7]) if len(row) > 7 else 0
                    dealer  = _parse(row[10]) if len(row) > 10 else 0
                    results["foreign_3d"] += foreign
                    results["invest_3d"]  += invest
                    results["dealer_3d"]  += dealer
                    results["total_3d"]   += foreign + invest + dealer
                    results["rows"].append({
                        "date": d.strftime("%Y-%m-%d"),
                        "foreign": foreign,
                        "invest": invest,
                        "dealer": dealer,
                    })
                    days_collected += 1
                except Exception:
                    pass
                break
            time.sleep(0.5)
        except Exception as e:
            print(f"[crawler] TWSE T86 {date_str} 失敗：{e}")
            time.sleep(1)

    return results


# ──────────────────────────────────────────
# TWSE 個股券商分點進出（TWT84U）— 免費，不需 token
# ──────────────────────────────────────────

def fetch_twse_broker_top(stock_id: str, top_n: int = 15) -> dict:
    """
    從 TWSE TWT84U 抓最近交易日個股券商分點買賣明細
    回傳 {
        date: str,
        buyers:  [{broker, buy_vol}, ...],   # 買方前N大（張）
        sellers: [{broker, sell_vol}, ...],  # 賣方前N大（張）
    }
    """
    empty = {"date": "", "buyers": [], "sellers": []}
    today = date.today()

    # 往前找最多7個交易日，直到拿到有效資料
    for i in range(7):
        d = today - timedelta(days=i)
        if d.weekday() >= 5:  # 跳過週末
            continue
        date_str = d.strftime("%Y%m%d")
        url = f"https://www.twse.com.tw/fund/TWT84U?response=json&date={date_str}&stockNo={stock_id}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read())

            if data.get("stat") not in ("OK", "ok"):
                time.sleep(0.3)
                continue

            rows = data.get("data", [])
            if not rows:
                time.sleep(0.3)
                continue

            buyers, sellers = [], []
            for row in rows:
                if len(row) < 6:
                    continue
                try:
                    def _vol(v):
                        v = str(v).replace(",", "").replace("+", "").strip()
                        return int(v) if v else 0
                    # TWT84U 欄位：買方代號, 買方名稱, 買進股數, 賣方代號, 賣方名稱, 賣出股數
                    # 股數 → 張數（÷1000）
                    broker_buy  = str(row[1]).strip()
                    buy_vol     = _vol(row[2]) // 1000
                    broker_sell = str(row[4]).strip()
                    sell_vol    = _vol(row[5]) // 1000
                    if broker_buy and buy_vol > 0:
                        buyers.append({"broker": broker_buy, "buy_vol": buy_vol})
                    if broker_sell and sell_vol > 0:
                        sellers.append({"broker": broker_sell, "sell_vol": sell_vol})
                except Exception:
                    continue

            buyers.sort(key=lambda x: x["buy_vol"], reverse=True)
            sellers.sort(key=lambda x: x["sell_vol"], reverse=True)

            return {
                "date":    d.strftime("%Y-%m-%d"),
                "buyers":  buyers[:top_n],
                "sellers": sellers[:top_n],
            }
        except Exception as e:
            print(f"[crawler] TWSE TWT84U {date_str} 失敗：{e}")
            time.sleep(0.5)

    return empty


if __name__ == "__main__":
    # 快速測試
    news = fetch_cnyes_news(20)
    print(f"新聞數：{len(news)}")
    for n in news[:3]:
        print(f"  標題：{n['title'][:40]}")
        print(f"  代號：{n['codes']}  關鍵字：{n['keywords']}")
