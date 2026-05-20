"""
線上有位 — 台股技術分析 API v2.0
啟動（本機）：uvicorn main:app --reload --port 8000
啟動（上線）：uvicorn main:app --host 0.0.0.0 --port 8000
"""

import sys, io
# Windows cmd 預設 ASCII，強制改為 UTF-8 避免中文 print 錯誤
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import sqlite3, hashlib, hmac, secrets, time as _time_mod
import json as _json_mod
from datetime import datetime, timedelta, date as _date_cls
import re as _re


# ══════════════════════════════════════════════════════════
# 環境設定（上線用環境變數，本機用 fallback）
# ══════════════════════════════════════════════════════════
FINMIND_TOKEN = os.environ.get("FINMIND_TOKEN", "")
if not FINMIND_TOKEN:
    raise RuntimeError("❌ 請設定環境變數 FINMIND_TOKEN")

# JWT 密鑰（請在 Zeabur 設定環境變數 JWT_SECRET）
JWT_SECRET = os.environ.get("JWT_SECRET", "change-me-in-production-please")
JWT_EXPIRE_DAYS = 30   # token 有效期

# 綠界 Webhook 驗證用
ECPAY_MERCHANT_ID = os.environ.get("ECPAY_MERCHANT_ID", "3443173")
ECPAY_HASH_KEY = os.environ.get("ECPAY_HASH_KEY", "")
ECPAY_HASH_IV  = os.environ.get("ECPAY_HASH_IV", "")
FRONTEND_URL   = os.environ.get("FRONTEND_URL", "https://softglow-ai.com")
BACKEND_URL    = os.environ.get("BACKEND_URL",  "https://stock-navigator-api.zeabur.app")

# 寄信設定
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", SMTP_USER)

# SQLite 資料庫路徑（Zeabur 持久化硬碟）
DB_PATH = os.environ.get("DB_PATH", "/data/members.db")

# Web Push VAPID 金鑰（請在 Zeabur 設定環境變數，或用 py-vapid 產生一次）
VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY", "")
VAPID_PUBLIC_KEY  = os.environ.get("VAPID_PUBLIC_KEY",  "")
VAPID_SUBJECT     = os.environ.get("VAPID_SUBJECT", f"mailto:{os.environ.get('SMTP_FROM','admin@example.com')}")

# pywebpush（選裝）
try:
    from pywebpush import webpush as _webpush_fn, WebPushException as _WebPushException
    _WEBPUSH_AVAILABLE = True
except ImportError:
    _WEBPUSH_AVAILABLE = False

# 免費用戶每日查詢次數
FREE_DAILY_LIMIT = 3   # 免費會員每日查詢次數
GUEST_DAILY_LIMIT = 10  # 遊客（未登入）每日查詢次數

# CORS：允許的前端來源
# 本機開發時設 ALLOWED_ORIGINS=* 或留空
# 上線後設為實際前端網址，例如 https://xian-shang-you-wei.zeabur.app
_origins_env = os.environ.get("ALLOWED_ORIGINS", "")
if _origins_env and _origins_env != "*":
    ALLOWED_ORIGINS = [o.strip() for o in _origins_env.split(",") if o.strip()]
else:
    # 開發環境：允許 localhost 各 port
    ALLOWED_ORIGINS = [
        "http://localhost:8080",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        "http://192.168.2.107:8080",
    ]

IS_PROD = os.environ.get("ZEABUR_SERVICE_ID") is not None  # Zeabur 會自動注入此變數

# In-memory SEO cache
SEO_CACHE: dict = {
    "sitemap":  {"data": None, "expires": 0},
    "rankings": {"data": None, "expires": 0},
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    env = "生產環境 🚀" if IS_PROD else "開發環境 💻"
    print(f"✅ 線上有位 API 啟動中（{env}）")
    print(f"   CORS 允許來源：{ALLOWED_ORIGINS}")

    # 初始化 SQLite 資料庫
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    except Exception:
        pass
    _db_init()
    print(f"   ✅ 會員資料庫初始化完成（{DB_PATH}）")

    # 啟動時主動載入 FinMind 全台股名稱快取，避免查詢時才抓造成延遲或亂碼
    try:
        import urllib.request as _ureq, json as _json
        url = (f"https://api.finmindtrade.com/api/v4/data"
               f"?dataset=TaiwanStockInfo&token={FINMIND_TOKEN}")
        req = _ureq.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with _ureq.urlopen(req, timeout=10) as resp:
            data = _json.loads(resp.read())
        if data.get("status") == 200:
            count = 0
            for item in data.get("data", []):
                sid = str(item.get("stock_id", ""))
                sname = str(item.get("stock_name", ""))
                stype = str(item.get("type", "")).lower()   # "twse" / "otc" / "rotc"
                if sid and sname and sid not in _name_cache:
                    _name_cache[sid] = sname
                    _name_to_code[sname] = sid
                    count += 1
                if sid and stype:
                    _market_cache[sid] = stype
            print(f"   ✅ 股名快取載入完成，共 {count} 筆")
        else:
            print(f"   ⚠️ FinMind 回應異常：{data.get('msg','')}")
    except Exception as e:
        print(f"   ⚠️ 股名快取載入失敗（{e}），將在查詢時重試")

    # 啟動 APScheduler 排程
    _bg_scheduler = None
    _picker_running  = False
    _expire_running  = False
    _scan_running    = False
    _alert_running   = False
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        import sys as _sys
        _picker_path = os.path.join(os.path.dirname(__file__), "stock_picker")

        def _run_unified_scan_job():
            nonlocal _scan_running
            if _scan_running:
                print("   ⚠️ 統合選股排程已在執行中，跳過本次")
                return
            _scan_running = True
            try:
                if _picker_path not in _sys.path:
                    _sys.path.insert(0, _picker_path)
                from main_picker import run_unified_scan
                run_unified_scan()
            except Exception as _e:
                print(f"   ❌ 統合選股排程執行失敗：{_e}")
            finally:
                _scan_running = False

        def _run_expire_notice_job():
            nonlocal _expire_running
            if _expire_running:
                print("   ⚠️ 到期提醒排程已在執行中，跳過本次")
                return
            _expire_running = True
            try:
                from zoneinfo import ZoneInfo
                today_str = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d")
                conn = _db_conn()
                members = conn.execute(
                    "SELECT email, expire_at, last_expire_notice_date FROM members "
                    "WHERE plan != 'free' AND expire_at IS NOT NULL AND expire_at >= ?",
                    (today_str,)
                ).fetchall()
                conn.close()
                for m in members:
                    if m["last_expire_notice_date"] == today_str:
                        continue
                    try:
                        delta = (datetime.fromisoformat(m["expire_at"]) - datetime.fromisoformat(today_str)).days
                    except Exception:
                        continue
                    if delta == 3:
                        _send_email(m["email"], "【線上有位】訂閱即將到期",
                            f'<p>您的訂閱將於 <b>{m["expire_at"]}</b> 到期（剩 3 天）。</p>'
                            f'<p><a href="{FRONTEND_URL}/landing.html#pricing">立即續訂</a></p>')
                        _update_notice_date(m["email"], today_str)
                    elif delta == 0:
                        _send_email(m["email"], "【線上有位】訂閱已到期",
                            f'<p>您的訂閱已於今日（{today_str}）到期。</p>'
                            f'<p><a href="{FRONTEND_URL}/landing.html#pricing">立即續訂</a></p>')
                        _update_notice_date(m["email"], today_str)
            except Exception as _e:
                print(f"   ❌ 到期提醒排程執行失敗：{_e}")
            finally:
                _expire_running = False


        def _run_price_alert_job():
            nonlocal _alert_running
            if _alert_running:
                return
            _alert_running = True
            try:
                import urllib.request as _ureq2, json as _json2
                from datetime import date as _date2, timedelta as _td2
                conn = _db_conn()
                alerts = conn.execute(
                    "SELECT * FROM price_alerts WHERE triggered=0"
                ).fetchall()
                conn.close()
                if not alerts:
                    return
                # 每股只查一次最新收盤價
                stock_prices: dict = {}
                for _a in alerts:
                    sid = _a["stock_id"]
                    if sid in stock_prices:
                        continue
                    try:
                        _start = (_date2.today() - _td2(days=5)).strftime("%Y-%m-%d")
                        _end   = _date2.today().strftime("%Y-%m-%d")
                        _url   = (f"https://api.finmindtrade.com/api/v4/data"
                                  f"?dataset=TaiwanStockPrice&data_id={sid}"
                                  f"&start_date={_start}&end_date={_end}&token={FINMIND_TOKEN}")
                        _req = _ureq2.Request(_url, headers={"User-Agent": "Mozilla/5.0"})
                        with _ureq2.urlopen(_req, timeout=8) as _resp:
                            _d = _json2.loads(_resp.read())
                        _rows = _d.get("data", [])
                        stock_prices[sid] = float(_rows[-1]["close"]) if _rows else None
                    except Exception:
                        stock_prices[sid] = None
                conn = _db_conn()
                for _a in alerts:
                    _price = stock_prices.get(_a["stock_id"])
                    if _price is None:
                        continue
                    _triggered = (
                        (_a["direction"] == "above" and _price >= _a["target_price"]) or
                        (_a["direction"] == "below" and _price <= _a["target_price"])
                    )
                    if not _triggered:
                        continue
                    conn.execute(
                        "UPDATE price_alerts SET triggered=1, triggered_at=? WHERE id=?",
                        (_taipei_now_str(), _a["id"])
                    )
                    _dir_text = "漲至" if _a["direction"] == "above" else "跌至"
                    _title = f"到價提醒：{_a['stock_id']}"
                    _body  = f"{_a['stock_id']} 已{_dir_text} {_price}，目標 {_a['target_price']}"
                    # Web Push
                    _subs = conn.execute(
                        "SELECT * FROM push_subscriptions WHERE user_email=?",
                        (_a["user_email"],)
                    ).fetchall()
                    for _sub in _subs:
                        send_web_push(dict(_sub), _title, _body, "/")
                    # Email
                    _send_email(_a["user_email"], f"【線上有位】{_title}",
                        f'<p>{_body}</p><p><a href="{FRONTEND_URL}">立即查看</a></p>')
                conn.commit()
                conn.close()
            except Exception as _e:
                print(f"   ❌ 到價提醒排程執行失敗：{_e}")
            finally:
                _alert_running = False

        _bg_scheduler = BackgroundScheduler(timezone="Asia/Taipei")
        _bg_scheduler.add_job(_run_unified_scan_job,  "cron", hour=15, minute=30, day_of_week="mon-fri")
        _bg_scheduler.add_job(_run_expire_notice_job, "cron", hour=9,  minute=0)
        _bg_scheduler.add_job(_run_price_alert_job,   "cron", hour=15, minute=35, day_of_week="mon-fri")
        _bg_scheduler.start()
        print("   ✅ APScheduler 排程已啟動（統合選股 15:30、到價提醒 15:35、到期通知 09:00）")
    except ImportError:
        print("   ⚠️ apscheduler 未安裝，選股排程請以 scheduler.py 獨立執行")
    except Exception as _sch_err:
        print(f"   ⚠️ 排程啟動失敗：{_sch_err}")

    yield

    if _bg_scheduler and _bg_scheduler.running:
        _bg_scheduler.shutdown(wait=False)
    print("🛑 線上有位 API 關閉")

# 上線時關閉 /docs 和 /redoc，避免 API 被掃描濫用
# 付款暫存資料已改為 SQLite pending_orders 表，見 _db_init()

app = FastAPI(
    title="線上有位 API",
    version="2.0.0",
    lifespan=lifespan,
    docs_url=None if IS_PROD else "/docs",
    redoc_url=None if IS_PROD else "/redoc",
    openapi_url=None if IS_PROD else "/openapi.json",
)
# CORS：明確列出允許來源，支援帶 Authorization header 的請求
_cors_origins = ALLOWED_ORIGINS if ALLOWED_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*", "Authorization", "Content-Type"],
    allow_credentials=False,
    expose_headers=["*"],
)


# ══════════════════════════════════════════════════════════
# 工具函式
# ══════════════════════════════════════════════════════════
def resolve_symbol(stock_id: str) -> str:
    """根據 FinMind market 資訊智慧選 .TW / .TWO 後綴"""
    stock_id = stock_id.strip().upper()
    if stock_id.endswith((".TW", ".TWO")):
        return stock_id
    code = stock_id
    mtype = _market_cache.get(code, "")
    if mtype in ("otc", "rotc"):
        return code + ".TWO"
    # twse 或未知 → 先試 .TW（try_fetch 會做 .TWO fallback）
    return code + ".TW"


def safe_float(v):
    if v is None:
        return None
    try:
        f = float(v)
        return None if (np.isnan(f) or np.isinf(f)) else round(f, 2)
    except Exception:
        return None


def calc_ma(closes: np.ndarray, period: int) -> np.ndarray:
    ma = np.full(len(closes), np.nan)
    for i in range(period - 1, len(closes)):
        ma[i] = closes[i - period + 1: i + 1].mean()
    return ma



def fetch_df_finmind(stock_id: str, period: str, interval: str):
    """
    FinMind 主力抓取台股 K 線資料（TaiwanStockPrice）
    盤中若今日資料尚未收錄，自動用 tick_snapshot 補一筆今日 K 棒
    週線/月線由日線重採樣
    """
    import urllib.request as _ur, json as _j
    from datetime import date, timedelta, datetime, time as _dtime
    from zoneinfo import ZoneInfo

    code = stock_id.strip().upper().replace(".TW", "").replace(".TWO", "")

    period_days = {"5d": 7, "1mo": 35, "3mo": 95, "6mo": 185,
                   "1y": 370, "2y": 740, "3y": 1100, "5y": 1830, "10y": 3660}
    days = period_days.get(period, 1100)
    start     = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    today_str = date.today().strftime("%Y-%m-%d")

    try:
        url = (f"https://api.finmindtrade.com/api/v4/data"
               f"?dataset=TaiwanStockPrice&data_id={code}"
               f"&start_date={start}&end_date={today_str}&token={FINMIND_TOKEN}")
        req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with _ur.urlopen(req, timeout=15) as resp:
            raw = _j.loads(resp.read())
        if raw.get("status") != 200 or not raw.get("data"):
            return pd.DataFrame()
        df = pd.DataFrame(raw["data"])
        df = df.rename(columns={
            "date": "Date", "open": "Open", "max": "High",
            "min": "Low", "close": "Close", "Trading_Volume": "Volume"
        })
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date").sort_index()
        df = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)

        # ── 盤中補今日 K 棒（FinMind tick_snapshot）──
        tz = ZoneInfo("Asia/Taipei")
        now_tw = datetime.now(tz)
        is_weekday = now_tw.weekday() < 5
        in_or_just_after = is_weekday and _dtime(9, 0) <= now_tw.time() <= _dtime(14, 30)
        today_ts = pd.Timestamp(today_str)

        if in_or_just_after:
            try:
                snap_url = (f"https://api.finmindtrade.com/api/v4/taiwan_stock_tick_snapshot"
                            f"?data_id={code}&token={FINMIND_TOKEN}")
                snap_req = _ur.Request(snap_url, headers={"User-Agent": "Mozilla/5.0"})
                with _ur.urlopen(snap_req, timeout=6) as sr:
                    snap = _j.loads(sr.read())
                snap_rows = snap.get("data", [])
                if snap_rows:
                    r = snap_rows[0]
                    cp  = float(r.get("close") or r.get("price") or 0)
                    op  = float(r.get("open") or cp)
                    hi  = float(r.get("high") or cp)
                    lo  = float(r.get("low") or cp)
                    vol = float(r.get("total_volume") or r.get("volume") or 0)
                    if cp > 0:
                        today_bar = pd.DataFrame(
                            [[op, hi, lo, cp, vol]],
                            index=[today_ts],
                            columns=["Open", "High", "Low", "Close", "Volume"]
                        )
                        df = df[df.index != today_ts]
                        df = pd.concat([df, today_bar])
                        print(f"   tick_snapshot 補今日 K 棒：{code} close={cp}")
            except Exception as _e:
                if not (hasattr(_e, 'code') and _e.code == 400):
                    print(f"   tick_snapshot 補棒失敗 {code}：{_e}")

        # ── TWSE/TPEX 月報補今日 K 棒（上述來源均無資料時的最終 fallback）──
        if today_ts not in df.index:
            today_obj = date.today()
            roc_year  = today_obj.year - 1911
            roc_date  = f"{roc_year}/{today_obj.month:02d}/{today_obj.day:02d}"
            yyyymmdd  = today_obj.strftime("%Y%m%d")
            mm        = today_obj.strftime("%m")

            def _parse_tw_num(s):
                return float(str(s).replace(",", "")) if str(s).strip() not in ("--", "", "X") else 0.0

            filled = False
            _is_otc = _market_cache.get(code, "") in ("otc", "rotc")
            if not _is_otc:
                # 上市：TWSE STOCK_DAY
                try:
                    twse_url = (f"https://www.twse.com.tw/exchangeReport/STOCK_DAY"
                                f"?response=json&date={yyyymmdd}&stockNo={code}")
                    twse_req = _ur.Request(twse_url, headers={"User-Agent": "Mozilla/5.0"})
                    with _ur.urlopen(twse_req, timeout=8) as tr:
                        twse_raw = _j.loads(tr.read())
                    for row in twse_raw.get("data", []):
                        if str(row[0]).strip() == roc_date:
                            op  = _parse_tw_num(row[3])
                            hi  = _parse_tw_num(row[4])
                            lo  = _parse_tw_num(row[5])
                            cp  = _parse_tw_num(row[6])
                            vol = _parse_tw_num(row[1])
                            if cp > 0:
                                today_bar = pd.DataFrame(
                                    [[op, hi, lo, cp, vol]],
                                    index=[today_ts],
                                    columns=["Open", "High", "Low", "Close", "Volume"]
                                )
                                df = pd.concat([df, today_bar])
                                print(f"   TWSE 月報補今日 K 棒：{code} close={cp}")
                                filled = True
                            break
                except Exception as _e:
                    print(f"   TWSE 月報補棒失敗 {code}：{_e}")
            else:
                # 上櫃：TPEX st43
                try:
                    tpex_d   = f"{roc_year}/{mm}"
                    tpex_url = (f"https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info"
                                f"/st43_result.php?l=zh-tw&d={tpex_d}&stkno={code}")
                    tpex_req = _ur.Request(tpex_url, headers={"User-Agent": "Mozilla/5.0"})
                    with _ur.urlopen(tpex_req, timeout=8) as pr:
                        tpex_raw = _j.loads(pr.read())
                    for row in tpex_raw.get("aaData", []):
                        if str(row[0]).strip() == roc_date:
                            op  = _parse_tw_num(row[3])
                            hi  = _parse_tw_num(row[4])
                            lo  = _parse_tw_num(row[5])
                            cp  = _parse_tw_num(row[6])
                            vol = _parse_tw_num(row[1])
                            if cp > 0:
                                today_bar = pd.DataFrame(
                                    [[op, hi, lo, cp, vol]],
                                    index=[today_ts],
                                    columns=["Open", "High", "Low", "Close", "Volume"]
                                )
                                df = pd.concat([df, today_bar])
                                print(f"   TPEX 月報補今日 K 棒：{code} close={cp}")
                                filled = True
                            break
                except Exception as _e:
                    print(f"   TPEX 月報補棒失敗 {code}：{_e}")

        # 週線/月線重採樣
        if interval == "1wk":
            df = df.resample("W").agg({
                "Open": "first", "High": "max",
                "Low": "min", "Close": "last", "Volume": "sum"
            }).dropna()
        elif interval == "1mo":
            df = df.resample("ME").agg({
                "Open": "first", "High": "max",
                "Low": "min", "Close": "last", "Volume": "sum"
            }).dropna()

        return df
    except Exception as e:
        print(f"   FinMind 抓取失敗 {code}：{e}")
        return pd.DataFrame()


def try_fetch(stock_id, period, interval):
    """FinMind 抓取台股 K 線資料（唯一來源）"""
    code = stock_id.strip().upper().replace(".TW", "").replace(".TWO", "")
    df = fetch_df_finmind(code, period, interval)
    return resolve_symbol(stock_id), df


# 股名快取（避免重複查詢）
_name_cache: dict[str, str] = {}          # {stock_id: stock_name}
_name_to_code: dict[str, str] = {}        # {stock_name: stock_id}，供名稱查詢轉代號
# 市場別快取：{stock_id: "twse"(上市) | "otc"(上櫃) | "rotc"(興櫃)}
_market_cache: dict[str, str] = {}

# 台股中文名稱對照表（常用股票，優先查表）
STOCK_NAMES = {
    "2330": "台積電", "2317": "鴻海", "2454": "聯發科", "2308": "台達電",
    "2412": "中華電", "6505": "台塑化", "2882": "國泰金", "2881": "富邦金",
    "2886": "兆豐金", "2891": "中信金", "2884": "玉山金", "2892": "第一金",
    "2883": "開發金", "2885": "元大金", "2887": "台新金", "2888": "新光金",
    "2890": "永豐金", "5880": "合庫金", "2801": "彰銀",
    "2002": "中鋼", "1301": "台塑", "1303": "南亞", "1326": "台化",
    "2303": "聯電", "2357": "華碩", "2382": "廣達", "2395": "研華",
    "2402": "毅嘉", "2408": "南亞科", "2409": "友達", "2449": "京元電子",
    "2474": "可成", "2476": "巨祥",
    "2376": "技嘉", "2379": "瑞昱", "2385": "群光", "2392": "正崴",
    "3711": "日月光投控", "2301": "光寶科", "2325": "矽品",
    "3034": "聯詠", "3037": "欣興", "3045": "台灣大", "3702": "大聯大",
    "4904": "遠傳", "4938": "和碩", "5871": "中租KY", "6415": "矽力KY",
    "6669": "緯穎", "2610": "華航", "2618": "長榮航", "2615": "萬海",
    "2603": "長榮", "2609": "陽明", "2607": "榮運",
    "1216": "統一", "2912": "統一超", "2207": "和泰車", "2105": "正新",
    "1402": "遠東新", "1101": "台泥", "1102": "亞泥",
    "2823": "中壽", "3008": "大立光", "2352": "佳世達", "2344": "華邦電",
    "2337": "旺宏", "2360": "致茂", "3354": "律勝", "3443": "創意",
    "6488": "環球晶", "6510": "精測", "6770": "力積電", "3661": "世芯KY",
    "6533": "晶心科", "6278": "台表科", "6121": "新普", "5274": "信驊",
    "3529": "力旺", "3532": "台勝科", "5483": "中美晶", "4989": "榮科",
}

def get_stock_name(symbol: str) -> str:
    """取得台股中文名稱：靜態表 → 快取 → FinMind → 回傳代號"""
    code = symbol.replace(".TWO", "").replace(".TW", "").strip()

    # 1. 靜態對照表（最快）
    if code in STOCK_NAMES:
        return STOCK_NAMES[code]

    # 2. 快取（啟動時已預載全台股，通常直接命中）
    if code in _name_cache:
        return _name_cache[code]

    # 3. 快取沒命中，嘗試即時查 FinMind（可能是新上市股票）
    try:
        import urllib.request as _ureq, json as _json
        url = (f"https://api.finmindtrade.com/api/v4/data"
               f"?dataset=TaiwanStockInfo&token={FINMIND_TOKEN}")
        req = _ureq.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with _ureq.urlopen(req, timeout=5) as resp:
            data = _json.loads(resp.read())
        if data.get("status") == 200:
            for item in data.get("data", []):
                sid = str(item.get("stock_id", ""))
                sname = str(item.get("stock_name", ""))
                stype = str(item.get("type", "")).lower()
                if sid and sname:
                    _name_cache[sid] = sname
                    _name_to_code[sname] = sid
                if sid and stype:
                    _market_cache[sid] = stype
        if code in _name_cache:
            return _name_cache[code]
    except Exception:
        pass

    # 4. 都找不到，直接回傳代號（不走 yfinance 避免亂碼）
    return code


def calc_rsi(closes: np.ndarray, period: int = 14) -> np.ndarray:
    n = len(closes)
    rsi = np.full(n, np.nan)
    if n < period + 1: return rsi
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    for i in range(period, n - 1):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rs = avg_gain / avg_loss if avg_loss > 0 else 100
        rsi[i + 1] = 100 - 100 / (1 + rs)
    return rsi


def calc_macd(closes: np.ndarray, fast=12, slow=26, signal=9):
    n = len(closes)
    ema_fast = np.full(n, np.nan)
    ema_slow = np.full(n, np.nan)
    # EMA
    for arr, p in [(ema_fast, fast), (ema_slow, slow)]:
        k = 2 / (p + 1)
        start = p - 1
        if start >= n: continue
        arr[start] = np.mean(closes[:p])
        for i in range(start + 1, n):
            arr[i] = closes[i] * k + arr[i-1] * (1 - k)
    macd_line = ema_fast - ema_slow
    # Signal line (EMA of MACD)
    sig = np.full(n, np.nan)
    valid = np.where(~np.isnan(macd_line))[0]
    if len(valid) >= signal:
        s0 = valid[signal - 1]
        sig[s0] = np.mean(macd_line[valid[:signal]])
        k = 2 / (signal + 1)
        for i in range(s0 + 1, n):
            if not np.isnan(macd_line[i]):
                sig[i] = macd_line[i] * k + sig[i-1] * (1 - k)
    hist = macd_line - sig
    return macd_line, sig, hist


def calc_kd(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period=9, smooth=3):
    n = len(closes)
    k_arr = np.full(n, np.nan)
    d_arr = np.full(n, np.nan)
    rsv   = np.full(n, np.nan)
    for i in range(period - 1, n):
        lo = lows[i-period+1:i+1].min()
        hi = highs[i-period+1:i+1].max()
        rsv[i] = (closes[i] - lo) / (hi - lo) * 100 if hi > lo else 50
    # Smooth K and D
    k_arr[period-1] = 50
    d_arr[period-1] = 50
    w = 1 / smooth
    for i in range(period, n):
        if np.isnan(rsv[i]): continue
        k_arr[i] = rsv[i] * w + k_arr[i-1] * (1 - w)
        d_arr[i] = k_arr[i] * w + d_arr[i-1] * (1 - w)
    return k_arr, d_arr


def calc_bollinger(closes: np.ndarray, period=20, std_dev=2):
    n = len(closes)
    mid = np.full(n, np.nan)
    upper = np.full(n, np.nan)
    lower = np.full(n, np.nan)
    for i in range(period - 1, n):
        seg = closes[i-period+1:i+1]
        m = seg.mean()
        s = seg.std(ddof=1)
        mid[i]   = round(float(m), 2)
        upper[i] = round(float(m + std_dev * s), 2)
        lower[i] = round(float(m - std_dev * s), 2)
    return mid, upper, lower


def calc_obv(closes: np.ndarray, volumes: np.ndarray):
    n = len(closes)
    obv = np.zeros(n)
    for i in range(1, n):
        if closes[i] > closes[i-1]:
            obv[i] = obv[i-1] + volumes[i]
        elif closes[i] < closes[i-1]:
            obv[i] = obv[i-1] - volumes[i]
        else:
            obv[i] = obv[i-1]
    return obv


def serialize_indicator(arr: np.ndarray, decimals=2) -> list:
    """Convert numpy array to JSON-serializable list, NaN → None"""
    return [None if np.isnan(v) else round(float(v), decimals) for v in arr]


def find_support_resistance(highs, lows, closes, volumes, price, channel_support=None):
    n = len(closes)
    candidates = []

    order = max(3, min(10, n // 40))
    lo_idx = argrelextrema(lows, np.less_equal, order=order)[0]
    hi_idx = argrelextrema(highs, np.greater_equal, order=order)[0]

    # 均量（20日）
    vol_ma20 = np.full(n, np.nan)
    for i in range(19, n):
        vol_ma20[i] = volumes[i - 19: i + 1].mean()

    # ── 1. 最近20根密集不破（多次測試守住的強支撐）──
    # 邏輯：掃描最近20根的低點，找 ±1% 內聚集 ≥ 3 根的價位帶
    recent_20 = list(range(max(0, n - 20), n))
    recent_20_lows = [(i, lows[i]) for i in recent_20 if lows[i] < price * 0.999]
    if len(recent_20_lows) >= 3:
        best_cluster_price = None
        best_cluster_count = 0
        best_cluster_vol_bonus = 0
        for anchor_i, anchor_p in recent_20_lows:
            band_lo, band_hi = anchor_p * 0.99, anchor_p * 1.01
            cluster = [(i, lows[i]) for i, p in recent_20_lows if band_lo <= p <= band_hi]
            if len(cluster) >= 3:
                # 量能加分：量縮（健康測試）或爆量守住（力道測試）
                vol_bonus = 0
                for ci, _ in cluster:
                    if not np.isnan(vol_ma20[ci]):
                        if volumes[ci] < vol_ma20[ci] * 0.6:    # 量縮測試
                            vol_bonus += 2
                        elif volumes[ci] > vol_ma20[ci] * 1.5:  # 爆量守住
                            vol_bonus += 1
                total_score = len(cluster) * 3 + vol_bonus
                if total_score > best_cluster_count * 3 + best_cluster_vol_bonus:
                    best_cluster_count = len(cluster)
                    best_cluster_vol_bonus = vol_bonus
                    best_cluster_price = float(np.mean([p for _, p in cluster]))
        if best_cluster_price and best_cluster_price < price * 0.999:
            vol_note = "含量能確認" if best_cluster_vol_bonus > 0 else ""
            candidates.append((round(best_cluster_price, 2), "dense_20",
                                f"近20根密集不破（{best_cluster_count}次測試守住{'，' + vol_note if vol_note else ''}）"))

    # ── 2. 回測低點（每個「漲→跌→漲」的轉折低點，取最近3個）──
    # 只取在現價以下的轉折低點，最近3個，並依量能加權
    valid_lo = [i for i in lo_idx if lows[i] < price * 0.999]
    # 只取最近的（最多往前看200根），取最近3個
    recent_lo = [i for i in valid_lo if i >= n - 200][-3:] if valid_lo else []
    for lo_i in reversed(recent_lo):
        ago = n - lo_i
        vol_note = ""
        weight = "pullback_low"
        if not np.isnan(vol_ma20[lo_i]):
            if volumes[lo_i] < vol_ma20[lo_i] * 0.6:
                vol_note = "，量縮守住"
                weight = "pullback_low_shrink"
            elif volumes[lo_i] > vol_ma20[lo_i] * 1.5:
                vol_note = "，爆量守住"
                weight = "pullback_low_surge"
        candidates.append((round(float(lows[lo_i]), 2), weight,
                            f"轉折低點（{ago}根前{vol_note}）"))

    # ── 3. 回測後低點（突破壓力後拉回不破，最具支撐意義）──
    for hi in reversed(hi_idx):
        resist_price = highs[hi]
        if resist_price >= price * 1.001:
            continue
        breakout_i = None
        for i in range(hi + 1, n):
            if closes[i] > resist_price * 1.005:
                breakout_i = i
                break
        if breakout_i is None:
            continue
        pullback_lows = [i for i in lo_idx
                         if i > breakout_i
                         and lows[i] >= resist_price * 0.95
                         and lows[i] < price * 0.999]
        if pullback_lows:
            best_pb = max(pullback_lows)
            ago = n - best_pb
            candidates.append((round(float(lows[best_pb]), 2), "pullback_confirmed",
                                f"突破回測低點（{ago}根前，突破{resist_price:.0f}後撐住）"))
            break

    # ── 4. 整理平台低點 ──
    plat_start = 0
    best_plat = None
    best_plat_recent = -1
    for i in range(1, n):
        seg_hi = max(highs[plat_start:i + 1])
        seg_lo = min(lows[plat_start:i + 1])
        if seg_lo > 0 and (seg_hi - seg_lo) / seg_lo * 100 > 2.0:
            length = i - plat_start
            if length >= 3:
                plo = min(lows[plat_start:i])
                if plo < price * 0.999 and i > best_plat_recent:
                    best_plat = (plo, plat_start, i - 1)
                    best_plat_recent = i
            plat_start = i
    if n - plat_start >= 3:
        seg_hi = max(highs[plat_start:n])
        seg_lo = min(lows[plat_start:n])
        if seg_lo > 0 and (seg_hi - seg_lo) / seg_lo * 100 <= 2.0:
            plo = min(lows[plat_start:n])
            if plo < price * 0.999:
                best_plat = (plo, plat_start, n - 1)
                best_plat_recent = n - 1
    if best_plat:
        plo, ps, pe = best_plat
        length = pe - ps + 1
        ago = n - pe
        candidates.append((round(float(plo), 2), "platform_low",
                            f"整理平台低點（{length}根平台，{ago}根前結束）"))

    # ── 5. 爆量支撐 ──
    boom_idx = [i for i in range(20, n)
                if not np.isnan(vol_ma20[i])
                and volumes[i] > vol_ma20[i] * 1.5
                and lows[i] < price * 0.999]
    if boom_idx:
        recent = boom_idx[-3:]
        best = min(recent, key=lambda i: price - lows[i] if lows[i] < price else float('inf'))
        if lows[best] < price:
            ratio = volumes[best] / vol_ma20[best]
            candidates.append((round(float(lows[best]), 2), "volume_surge",
                               f"爆量支撐（{n - best}根前，{ratio:.1f}倍均量）"))

    # ── 6. 凹洞量支撐 ──
    hollow_idx = [i for i in range(20, n)
                  if not np.isnan(vol_ma20[i])
                  and volumes[i] < vol_ma20[i] * 0.5
                  and lows[i] < price * 0.999]
    if hollow_idx:
        recent = hollow_idx[-5:]
        best = min(recent, key=lambda i: price - lows[i] if lows[i] < price else float('inf'))
        if lows[best] < price:
            ratio = volumes[best] / vol_ma20[best]
            candidates.append((round(float(lows[best]), 2), "hollow_volume",
                               f"凹洞量支撐（{n - best}根前，量僅{ratio:.1f}倍均量）"))

    # ── 7. 均線動態支撐 ──
    for period, name in [(20, "MA20"), (60, "MA60")]:
        ma = calc_ma(closes, period)
        v = ma[-1]
        if not np.isnan(v) and v < price * 0.999:
            candidates.append((round(float(v), 2), f"ma{period}", f"{name} 動態支撐"))

    # ── 8. 軌道下緣（距現價 ≤8% 才納入競爭；>8% 不影響支撐選擇）──
    if channel_support and channel_support < price * 0.999:
        ch_dist_pct = (price - channel_support) / price * 100
        if ch_dist_pct <= 8:
            candidates.append((round(float(channel_support), 2), "channel_low",
                                f"軌道下緣（距現價 -{ch_dist_pct:.1f}%）"))

    # ── 最終選擇：優先順序加權 ──
    SOURCE_WEIGHT = {
        "dense_20":           8,   # 最近20根密集不破（最強）
        "pullback_confirmed": 7,   # 突破回測後守住
        "pullback_low_shrink":6,   # 轉折低點+量縮
        "pullback_low_surge": 6,   # 轉折低點+爆量
        "pullback_low":       5,   # 普通轉折低點
        "cluster_low":        5,
        "platform_low":       4,
        "channel_low":        4,   # 軌道下緣動態支撐
        "volume_surge":       3,
        "hollow_volume":      2,
        "ma20": 1, "ma60": 1,
    }
    below = [(p, src, desc) for p, src, desc in candidates if p < price]

    if below:
        prices_only = [p for p, _, _ in below]
        price_range = (price - min(prices_only)) or 1
        def score(item):
            p, src, _ = item
            w = SOURCE_WEIGHT.get(src, 1)
            # proximity 只做次要排序，權重極小（0~0.1），不會蓋過來源強度差異
            proximity = (p - min(prices_only)) / price_range * 0.1
            return w + proximity
        best_item = max(below, key=score)
        support, support_source, support_desc = best_item
    else:
        support = round(float(lows[-20:].min()), 2)
        support_source = "recent_low"
        support_desc = "近20日最低點（備援）"

    # ── 壓力：轉折高點優先，再看近期最高 ──
    # 壓力選擇：現價以上最近的轉折高點，若多個則取最近且最低的（最容易被測試）
    valid_hi_idx = [i for i in hi_idx if highs[i] > price * 1.001]
    if valid_hi_idx:
        # 取最近30根內的轉折高點，沒有就取最近的一個
        recent_hi = [i for i in valid_hi_idx if i >= n - 60]
        pool = recent_hi if recent_hi else valid_hi_idx
        # 最近且最低的（最近壓力）
        nearest_hi = min(pool, key=lambda i: (highs[i], -(i)))
        resistance = round(float(highs[nearest_hi]), 2)
        resistance_desc = f"轉折高點（{n - nearest_hi}根前）"
    else:
        # 排除今天（最後一根），避免今日創高時壓力 = 現價
        hist_highs = highs[:-1] if len(highs) > 20 else highs
        resistance = round(float(hist_highs[-20:].max()), 2)
        resistance_desc = "近20日最高點（備援）"

    scored = sorted(below, key=score, reverse=True) if below else []
    detail = {
        "support_source": support_source,
        "support_desc": support_desc,
        "resistance_desc": resistance_desc,
        "all_candidates": [
            {"price": p, "source": src, "desc": desc,
             "score": round(score((p, src, desc)), 3)}
            for p, src, desc in scored
        ],
    }
    return support, resistance, detail


# ══════════════════════════════════════════════════════════
# 風險評估與條列摘要
# ══════════════════════════════════════════════════════════
def calc_risk_level(price, support, resistance, rr_ratio, near_top, near_bot, pattern):
    """回傳風險等級與條列摘要"""
    sup_dist = (price - support) / price * 100
    res_dist = (resistance - price) / price * 100

    # 風險等級判斷
    if near_top or res_dist < 2:
        risk_level = "high"
        risk_label = "高風險"
        risk_color = "red"
    elif pattern in ["跌破型態"] or (near_bot and rr_ratio < 1):
        risk_level = "high"
        risk_label = "高風險"
        risk_color = "red"
    elif res_dist < 5 or rr_ratio < 1:
        risk_level = "medium"
        risk_label = "留意"
        risk_color = "amber"
    elif (near_bot or sup_dist < 3) and pattern not in [
        "大黑棒（強勢賣壓）", "黑棒", "跌破型態", "吞噬（空頭）",
        "射擊之星", "烏雲蓋頂", "下降趨勢"
    ]:
        risk_level = "low"
        risk_label = "相對安全"
        risk_color = "green"
    elif (near_bot or sup_dist < 3):
        # 靠近支撐但出現空頭K棒，升為留意
        risk_level = "medium"
        risk_label = "留意"
        risk_color = "amber"
    else:
        risk_level = "watch"
        risk_label = "觀望"
        risk_color = "gray"

    return risk_level, risk_label, risk_color


def build_summary(price, support, support_desc, resistance, resistance_desc,
                  trend, pattern, rr_ratio, risk_level, risk_label,
                  near_top, near_bot, stop_loss, target1, rr_basis="防守位",
                  kline_pattern="常態 K 線（無觸發極端型態）", win_rate=0.50):
    """條列式分析摘要"""
    sup_dist = (price - support) / price * 100
    res_dist = (resistance - price) / price * 100
    stop_dist = (price - stop_loss) / price * 100

    lines = []

    # 趨勢（加細節）
    trend_map = {
        "上升趨勢": "均線多頭排列，趨勢偏多，短均在長均之上，回測支撐是買點",
        "下降趨勢": "均線空頭排列，趨勢偏空，短均在長均之下，反彈壓力是賣點",
        "盤整":     "均線糾結，多空拉鋸，方向未明，等待突破方向再跟進",
    }
    lines.append(f"趨勢：{trend_map.get(trend, trend)}")

    # 現價位置
    lines.append(f"現價 {price}，距支撐 -{sup_dist:.1f}%，距壓力 +{res_dist:.1f}%")

    # 支撐說明
    lines.append(f"支撐 {support}（{support_desc}）")

    # 壓力說明
    lines.append(f"壓力 {resistance}（{resistance_desc}）")

    # 型態
    pattern_detail = {
        "突破型態": f"股價突破壓力 {resistance}，若縮量拉回不破壓力，壓力轉支撐，為強勢回測買點",
        "跌破型態": f"股價跌破支撐 {support}，前支撐轉壓力，應等穩定再重新評估，停損優先",
        "支撐整理": f"現價靠近支撐 {support}（-{sup_dist:.1f}%），為相對低風險觀察位，守住偏多，跌破停損",
        "壓力整理": f"現價靠近壓力 {resistance}（+{res_dist:.1f}%），追價風險高，等回測支撐 {support} 或放量突破再跟",
        "整理中":   f"現價位於支撐 {support} 與壓力 {resistance} 之間，等待方向訊號，不宜追高殺低",
    }
    lines.append(f"型態：{pattern_detail.get(pattern, pattern)}")

    # 風險（防守位）
    lines.append(f"防守位置 {stop_loss}（跌破停損，距現價 -{stop_dist:.1f}%）")

    # 損益比（說明計算基礎）
    if rr_ratio >= 2:
        rr_comment = "損益比良好，值得評估"
    elif rr_ratio >= 1.5:
        rr_comment = "損益比尚可"
    elif rr_ratio >= 1:
        rr_comment = "損益比偏低，需謹慎"
    else:
        rr_comment = "損益比不佳，風險大於報酬"
    lines.append(f"風險報酬 {rr_ratio}（以{rr_basis}為停損基準，{rr_comment}）")

    lines.append(f"最新 K 線型態：{kline_pattern}")
    lines.append(f"型態大數據勝率：{win_rate*100:.0f}%")
    if win_rate > 0.50:
        lines.append("需伴隨成交量倍增與隔日收盤站穩確認")

    return lines


def detect_kline_patterns(closes, opens, highs, lows, volumes):
    """根據最新K棒判斷型態與大數據勝率"""
    n = len(closes)
    if n < 3:
        return "常態 K 線（無觸發極端型態）", 0.50
    c0, o0, h0, l0, v0 = closes[-1], opens[-1], highs[-1], lows[-1], volumes[-1]
    body_size0    = abs(c0 - o0)
    upper_shadow0 = h0 - max(c0, o0)
    lower_shadow0 = min(c0, o0) - l0
    range0        = max(h0 - l0, 0.001)
    avg_vol       = sum(volumes[-6:-1]) / 5 if n >= 6 else (sum(volumes[:-1]) / max(len(volumes)-1, 1))
    vol_surge     = v0 > avg_vol * 1.3
    is_downtrend  = closes[-1] < closes[-5] if n >= 5 else False
    is_uptrend    = closes[-1] > closes[-5] if n >= 5 else False
    if vol_surge and (body_size0 >= range0 * 0.5) and (c0 > o0):
        return "量增大紅棒（突破確認）", 0.62
    if vol_surge and (body_size0 >= range0 * 0.5) and (c0 < o0):
        return "量增大黑棒（跌破確認）", 0.62
    # 錘子線：下影線夠長（>=40%全幅）、下影線>=實體1.5倍、上影線短（<=20%全幅）
    if (is_downtrend and (lower_shadow0 >= range0 * 0.4)
            and (lower_shadow0 >= body_size0 * 1.5)
            and (upper_shadow0 <= range0 * 0.2)):
        return "低檔錘子線（底部承接力道強）", 0.53
    # 流星線：上影線夠長（>=40%全幅）、上影線>=實體1.5倍、下影線短（<=20%全幅）
    if (is_uptrend and (upper_shadow0 >= range0 * 0.4)
            and (upper_shadow0 >= body_size0 * 1.5)
            and (lower_shadow0 <= range0 * 0.2)):
        return "高檔流星線（多頭上攻力竭）", 0.53
    return "常態 K 線（無觸發極端型態）", 0.50


# ══════════════════════════════════════════════════════════
# 型態判斷
# ══════════════════════════════════════════════════════════
def detect_pattern(price, support, resistance, ch_lo, ch_hi):
    thr = 0.03
    if price > resistance * (1 + thr):
        return "突破型態", "現價突破壓力區"
    if price < support * (1 - thr):
        return "跌破型態", "現價跌破支撐區"
    if abs(price - support) / support < thr:
        return "支撐整理", "靠近支撐，觀察守住"
    if abs(price - resistance) / resistance < thr:
        return "壓力整理", "靠近壓力，注意量能"
    return "整理中", "位於區間中段"


# ══════════════════════════════════════════════════════════
# 葛蘭碧
# ══════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════
# 趨勢軌道計算
# ══════════════════════════════════════════════════════════
def calc_trend_line_y(x1, y1, x2, y2, x):
    if x2 == x1: return y1
    return y1 + (y2 - y1) / (x2 - x1) * (x - x1)


def find_trend_channel(highs, lows, closes):
    """
    用線性迴歸斜率找最佳軌道起點（R²最高）
    上升軌道：從最佳低點起，平行線複製到最高點
    下降軌道：從最佳高點起，平行線複製到最低點
    另外偵測水平支撐（橫盤區間下緣）
    """
    n_full = len(closes)
    if n_full < 30: return None
    price = closes[-1]

    # 只看最近 120 根，避免歷史走勢干擾近期軌道（用局部變數）
    LOOKBACK = min(n_full, 120)
    _offset  = n_full - LOOKBACK
    _highs   = highs[-LOOKBACK:]
    _lows    = lows[-LOOKBACK:]
    _closes  = closes[-LOOKBACK:]
    n        = LOOKBACK

    # ── 用 R² 找最佳上升軌道起點 ──────────────────────
    from scipy.stats import linregress
    order = max(3, min(8, n // 25))
    lo_idx = argrelextrema(_lows, np.less_equal, order=order)[0]
    hi_idx = argrelextrema(_highs, np.greater_equal, order=order)[0]

    best_up_r2    = 0.0
    best_up_start = None
    best_up_slope = 0.0
    best_up_intercept = 0.0

    # 從最近往回掃低點，找 R² 最高的上升軌道
    for start_lo in lo_idx:
        seg_idx = lo_idx[lo_idx >= start_lo]
        if len(seg_idx) < 2: continue
        x = seg_idx.astype(float)
        y = _lows[seg_idx]
        slope, intercept, r, _, _ = linregress(x, y)
        r2 = r ** 2
        if slope > 0 and r2 > best_up_r2:
            best_up_r2        = r2
            best_up_start     = start_lo
            best_up_slope     = slope
            best_up_intercept = intercept

    # ── 用 R² 找最佳下降軌道起點 ──────────────────────
    best_dn_r2    = 0.0
    best_dn_start = None
    best_dn_slope = 0.0
    best_dn_intercept = 0.0

    for start_hi in hi_idx:
        seg_idx = hi_idx[hi_idx >= start_hi]
        if len(seg_idx) < 2: continue
        x = seg_idx.astype(float)
        y = _highs[seg_idx]
        slope, intercept, r, _, _ = linregress(x, y)
        r2 = r ** 2
        if slope < 0 and r2 > best_dn_r2:
            best_dn_r2        = r2
            best_dn_start     = start_hi
            best_dn_slope     = slope
            best_dn_intercept = intercept

    curr = n - 1
    ext  = curr + 20

    # ── 決定主軌道類型 ──────────────────────────────────
    use_up = best_up_r2 >= 0.35
    use_dn = best_dn_r2 >= 0.35

    # 即使兩者都不足門檻，也選最佳的一個（避免沒有軌道線）
    if not use_up and not use_dn:
        if best_up_r2 > 0 or best_dn_r2 > 0:
            if best_up_r2 >= best_dn_r2:
                use_up = True
            else:
                use_dn = True

    def to_global(x_local):
        """將局部索引轉回全域索引（對應完整 bars 陣列）"""
        return int(x_local) + _offset

    if use_up and (not use_dn or best_up_r2 >= best_dn_r2):
        ctype, cdesc = "up", "上升軌道"
        s0 = int(best_up_start)
        lo_slope     = best_up_slope
        lo_intercept = best_up_intercept

        s_y_start = lo_intercept + lo_slope * s0
        s_y_curr  = lo_intercept + lo_slope * curr
        s_y_ext   = lo_intercept + lo_slope * ext
        s_line = {"x1": to_global(s0),   "y1": round(s_y_start, 2),
                  "x2": to_global(curr), "y2": round(s_y_curr,  2),
                  "x_ext": to_global(ext), "y_ext": round(s_y_ext, 2)}

        peak_idx = int(np.argmax(_highs[s0:])) + s0
        peak_y   = float(_highs[peak_idx])
        sup_at_peak = lo_intercept + lo_slope * peak_idx
        offset_y    = peak_y - sup_at_peak

        r_y_start = s_y_start + offset_y
        r_y_curr  = s_y_curr  + offset_y
        r_y_ext   = s_y_ext   + offset_y
        r_line = {"x1": to_global(s0),   "y1": round(r_y_start, 2),
                  "x2": to_global(curr), "y2": round(r_y_curr,  2),
                  "x_ext": to_global(ext), "y_ext": round(r_y_ext, 2)}

        support_now   = round(s_y_curr, 2)
        resist_now    = round(r_y_curr, 2)
        channel_width = abs(offset_y)

    elif use_dn:
        ctype, cdesc = "down", "下降軌道"
        s0 = int(best_dn_start)
        hi_slope     = best_dn_slope
        hi_intercept = best_dn_intercept

        r_y_start = hi_intercept + hi_slope * s0
        r_y_curr  = hi_intercept + hi_slope * curr
        r_y_ext   = hi_intercept + hi_slope * ext
        r_line = {"x1": to_global(s0),   "y1": round(r_y_start, 2),
                  "x2": to_global(curr), "y2": round(r_y_curr,  2),
                  "x_ext": to_global(ext), "y_ext": round(r_y_ext, 2)}

        trough_idx = int(np.argmin(_lows[s0:])) + s0
        trough_y   = float(_lows[trough_idx])
        res_at_trough = hi_intercept + hi_slope * trough_idx
        offset_y      = trough_y - res_at_trough

        s_y_start = r_y_start + offset_y
        s_y_curr  = r_y_curr  + offset_y
        s_y_ext   = r_y_ext   + offset_y
        s_line = {"x1": to_global(s0),   "y1": round(s_y_start, 2),
                  "x2": to_global(curr), "y2": round(s_y_curr,  2),
                  "x_ext": to_global(ext), "y_ext": round(s_y_ext, 2)}

        resist_now    = round(r_y_curr, 2)
        support_now   = round(s_y_curr, 2)
        channel_width = abs(offset_y)

    else:
        ctype, cdesc = "horizontal", "水平箱型整理"
        rec_lo = lo_idx[-2:] if len(lo_idx) >= 2 else lo_idx
        rec_hi = hi_idx[-2:] if len(hi_idx) >= 2 else hi_idx
        lo1, lo2 = int(rec_lo[-2]), int(rec_lo[-1])
        hi1, hi2 = int(rec_hi[-2]), int(rec_hi[-1])
        support_now = round(float(_lows[[lo1,lo2]].min()), 2)
        resist_now  = round(float(_highs[[hi1,hi2]].max()), 2)
        channel_width = abs(resist_now - support_now)
        s_line = {"x1":to_global(lo1),"y1":support_now,"x2":to_global(lo2),"y2":support_now,"x_ext":to_global(ext),"y_ext":support_now}
        r_line = {"x1":to_global(hi1),"y1":resist_now, "x2":to_global(hi2),"y2":resist_now, "x_ext":to_global(ext),"y_ext":resist_now}

    # ── 位置判斷 ────────────────────────────────────────
    dist_sup = (price - support_now) / support_now * 100 if support_now > 0 else 999
    dist_res = (resist_now - price)  / price * 100 if price > 0 else 999
    thr = 0.02

    if   price > resist_now * (1+thr):  pos,pdesc="breakout_up",  f"已突破上軌 {resist_now}，等幅目標 {round(resist_now+channel_width,2)}"
    elif price < support_now * (1-thr): pos,pdesc="breakout_dn",  f"已跌破下軌 {support_now}，注意下方空間"
    elif dist_res < 3:                  pos,pdesc="near_resist",  f"靠近上軌壓力 {resist_now}（+{dist_res:.1f}%），注意拉回設好防守"
    elif dist_sup < 3:                  pos,pdesc="near_support", f"靠近下軌支撐 {support_now}（-{dist_sup:.1f}%），相對低風險觀察位"
    else:                               pos,pdesc="middle",       f"位於軌道中段，距支撐 -{dist_sup:.1f}%，距壓力 +{dist_res:.1f}%"

    return {
        "type": ctype, "desc": cdesc,
        "r2": round(max(best_up_r2, best_dn_r2), 3),
        "position": pos, "position_desc": pdesc,
        "support_line": s_line, "resist_line": r_line,
        "support_now": support_now, "resist_now": resist_now,
        "channel_width": round(float(channel_width), 2),
        "target1": round(resist_now + channel_width, 2),
        "target2": round(resist_now + channel_width * 2, 2),
    }


def detect_triangle_channel(highs, lows, closes):
    """偵測三角形收斂/擴散型態"""
    from scipy.stats import linregress
    n_full = len(closes)
    if n_full < 20: return None
    LOOKBACK = min(n_full, 120)
    _offset  = n_full - LOOKBACK
    _highs   = highs[-LOOKBACK:]
    _lows    = lows[-LOOKBACK:]
    n        = LOOKBACK
    price    = closes[-1]
    order = max(3, min(8, n // 25))
    lo_idx = argrelextrema(_lows,  np.less_equal,    order=order)[0]
    hi_idx = argrelextrema(_highs, np.greater_equal, order=order)[0]
    if len(lo_idx) < 2 or len(hi_idx) < 2: return None
    def to_global(x): return int(x) + _offset
    xh = hi_idx.astype(float); yh = _highs[hi_idx]
    sh, ih, rh, _, _ = linregress(xh, yh)
    xl = lo_idx.astype(float); yl = _lows[lo_idx]
    sl, il, rl, _, _ = linregress(xl, yl)
    curr = n - 1; ext = curr + 20
    def line_y(s, i, x): return s * x + i
    converging = sh < -0.005 and sl > 0.005
    expanding  = sh > 0.005  and sl < -0.005
    mean_price = float(np.mean(closes[-LOOKBACK:]))
    asc_tri    = abs(sh) < 0.015 * mean_price / max(n, 1) and sl > 0.005
    desc_tri   = sh < -0.005 and abs(sl) < 0.015 * mean_price / max(n, 1)
    r2h = rh**2; r2l = rl**2
    if max(r2h, r2l) < 0.35: return None
    hi_curr = line_y(sh, ih, curr); lo_curr = line_y(sl, il, curr)
    hi_ext  = line_y(sh, ih, ext);  lo_ext  = line_y(sl, il, ext)
    hi_s0   = line_y(sh, ih, hi_idx[0]); lo_s0 = line_y(sl, il, lo_idx[0])
    channel_width = abs(hi_curr - lo_curr)
    s_line = {"x1": to_global(lo_idx[0]), "y1": round(lo_s0, 2),
              "x2": to_global(curr),       "y2": round(lo_curr, 2),
              "x_ext": to_global(ext),     "y_ext": round(lo_ext, 2)}
    r_line = {"x1": to_global(hi_idx[0]), "y1": round(hi_s0, 2),
              "x2": to_global(curr),       "y2": round(hi_curr, 2),
              "x_ext": to_global(ext),     "y_ext": round(hi_ext, 2)}
    support_now = round(lo_curr, 2); resist_now = round(hi_curr, 2)
    if converging:
        ctype, cdesc = "converging", "收斂三角形"
        target_up = round(resist_now + channel_width, 2)
        target_dn = round(support_now - channel_width, 2)
        pdesc = f"收斂三角整理，上破 {resist_now:.1f} 目標 {target_up}，下破 {support_now:.1f} 目標 {target_dn}"
    elif expanding:
        ctype, cdesc = "expanding", "擴散三角形（波動加大）"
        pdesc = f"擴散三角，上緣 {resist_now:.1f} / 下緣 {support_now:.1f}，操作難度高"
    elif asc_tri:
        ctype, cdesc = "ascending_tri", "上升三角形（偏多）"
        target = round(resist_now + channel_width, 2)
        pdesc = f"上升三角，壓力 {resist_now:.1f} 反覆測試，突破後目標 {target}"
    elif desc_tri:
        ctype, cdesc = "descending_tri", "下降三角形（偏空）"
        target = round(support_now - channel_width, 2)
        pdesc = f"下降三角，支撐 {support_now:.1f} 反覆測試，跌破後目標 {target}"
    else:
        return None
    dist_sup = (price - support_now) / support_now * 100 if support_now > 0 else 999
    dist_res = (resist_now - price)  / price * 100 if price > 0 else 999
    if   price > resist_now * 1.02:  pos = "breakout_up"
    elif price < support_now * 0.98: pos = "breakout_dn"
    elif dist_res < 3:               pos = "near_resist"
    elif dist_sup < 3:               pos = "near_support"
    else:                            pos = "middle"
    return {
        "type": ctype, "desc": cdesc, "r2": round((r2h+r2l)/2, 3),
        "position": pos, "position_desc": pdesc,
        "support_line": s_line, "resist_line": r_line,
        "support_now": support_now, "resist_now": resist_now,
        "channel_width": round(float(channel_width), 2),
        "target1": round(resist_now + channel_width, 2),
        "target2": round(resist_now + channel_width * 2, 2),
    }


def detect_reversal_pattern(highs, lows, closes):
    """偵測反轉型態：W底、M頭、頭肩底、頭肩頂"""
    LOOKBACK = min(len(closes), 120)
    _offset  = len(closes) - LOOKBACK
    _h = highs[-LOOKBACK:]; _l = lows[-LOOKBACK:]
    n  = LOOKBACK; price = closes[-1]
    order = max(3, min(8, n // 20))
    lo_idx = argrelextrema(_l, np.less_equal,    order=order)[0].tolist()
    hi_idx = argrelextrema(_h, np.greater_equal, order=order)[0].tolist()
    def to_global(x): return int(x) + _offset

    # W底
    if len(lo_idx) >= 2:
        for i in range(len(lo_idx)-1, 0, -1):
            l2, l1 = lo_idx[i], lo_idx[i-1]
            if l2 - l1 < 5: continue
            v1, v2 = _l[l1], _l[l2]
            if abs(v1-v2)/max(v1, 0.001) > 0.04: continue
            neck = float(_h[l1:l2].max())
            if price >= neck * 0.98:
                target = round(neck + (neck - min(v1, v2)), 2)
                broken = bool(price >= neck * 1.005)
                return {
                    "type": "double_bottom", "desc": "W底（雙底）",
                    "neckline": round(neck, 2), "target": float(target), "broken": broken,
                    "position_desc": f"{'已突破頸線' if broken else '接近頸線'} {neck:.1f}，目標 {target}",
                    "support_now": round(min(v1, v2)*0.99, 2), "resist_now": round(neck, 2),
                    "support_line": None, "resist_line": None,
                    "channel_width": round(neck-min(v1, v2), 2),
                    "target1": target, "target2": round(target+(target-neck), 2),
                }
            break

    # M頭
    if len(hi_idx) >= 2:
        for i in range(len(hi_idx)-1, 0, -1):
            h2, h1 = hi_idx[i], hi_idx[i-1]
            if h2 - h1 < 5: continue
            v1, v2 = _h[h1], _h[h2]
            if abs(v1-v2)/max(v1, 0.001) > 0.04: continue
            neck = float(_l[h1:h2].min())
            if price <= neck * 1.02:
                target = round(neck - (max(v1, v2) - neck), 2)
                broken = bool(price <= neck * 0.995)
                return {
                    "type": "double_top", "desc": "M頭（雙頭）",
                    "neckline": round(neck, 2), "target": float(target), "broken": broken,
                    "position_desc": f"{'已跌破頸線' if broken else '接近頸線'} {neck:.1f}，下行目標 {target}",
                    "support_now": round(neck, 2), "resist_now": round(max(v1, v2), 2),
                    "support_line": None, "resist_line": None,
                    "channel_width": round(max(v1, v2)-neck, 2),
                    "target1": target, "target2": round(target-(neck-target), 2),
                }
            break

    # 頭肩頂
    if len(hi_idx) >= 3:
        for i in range(len(hi_idx)-1, 1, -1):
            rs, head, ls = hi_idx[i], hi_idx[i-1], hi_idx[i-2]
            if rs - ls < 10: continue
            ls_h, head_h, rs_h = _h[ls], _h[head], _h[rs]
            if not (head_h > ls_h*1.02 and head_h > rs_h*1.02): continue
            if abs(ls_h-rs_h)/max(ls_h, 0.001) > 0.06: continue
            neck = (float(_l[ls:head].min()) + float(_l[head:rs].min())) / 2
            if price <= neck * 1.02:
                target = round(neck - (head_h - neck), 2)
                broken = bool(price <= neck * 0.995)
                return {
                    "type": "head_shoulders_top", "desc": "頭肩頂",
                    "neckline": round(neck, 2), "target": float(target), "broken": broken,
                    "position_desc": f"頭肩頂，{'已跌破頸線' if broken else '頸線'} {neck:.1f}，下行目標 {target}",
                    "support_now": round(neck, 2), "resist_now": round(head_h, 2),
                    "support_line": None, "resist_line": None,
                    "channel_width": round(head_h-neck, 2),
                    "target1": target, "target2": round(target-(neck-target), 2),
                }
            break

    # 頭肩底
    if len(lo_idx) >= 3:
        for i in range(len(lo_idx)-1, 1, -1):
            rs, head, ls = lo_idx[i], lo_idx[i-1], lo_idx[i-2]
            if rs - ls < 10: continue
            ls_l, head_l, rs_l = _l[ls], _l[head], _l[rs]
            if not (head_l < ls_l*0.98 and head_l < rs_l*0.98): continue
            if abs(ls_l-rs_l)/max(ls_l, 0.001) > 0.06: continue
            neck = (float(_h[ls:head].max()) + float(_h[head:rs].max())) / 2
            if price >= neck * 0.98:
                target = round(neck + (neck - head_l), 2)
                broken = bool(price >= neck * 1.005)
                return {
                    "type": "head_shoulders_bottom", "desc": "頭肩底",
                    "neckline": round(neck, 2), "target": float(target), "broken": broken,
                    "position_desc": f"頭肩底，{'已突破頸線' if broken else '頸線'} {neck:.1f}，上行目標 {target}",
                    "support_now": round(head_l, 2), "resist_now": round(neck, 2),
                    "support_line": None, "resist_line": None,
                    "channel_width": round(neck-head_l, 2),
                    "target1": target, "target2": round(target+(target-neck), 2),
                }
            break

    return None


def gann_signals(closes, ma20):
    buys, sells = [], []
    for i in range(1, len(closes)):
        if np.isnan(ma20[i]) or np.isnan(ma20[i - 1]):
            continue
        if closes[i - 1] < ma20[i - 1] and closes[i] > ma20[i]:
            buys.append(i)
        elif closes[i - 1] > ma20[i - 1] and closes[i] < ma20[i]:
            sells.append(i)
    return buys[-3:], sells[-3:]


def calc_gann_filtered(closes, highs, lows, volumes, ma_period=20):
    """葛蘭碧 + 量能過濾 + 防守點"""
    n = len(closes)
    ma = np.full(n, np.nan)
    for i in range(ma_period-1, n):
        ma[i] = closes[i-ma_period+1:i+1].mean()
    vol_ma = np.full(n, np.nan)
    for i in range(19, n):
        vol_ma[i] = volumes[i-19:i+1].mean()
    buys, sells, stops = [], [], []
    for i in range(ma_period+1, n):
        if any(np.isnan(x) for x in [ma[i], ma[i-1], ma[i-2], vol_ma[i]]): continue
        ma_up   = ma[i] > ma[i-2]
        ma_dn   = ma[i] < ma[i-2]
        vol_big = volumes[i] > vol_ma[i] * 1.2
        if closes[i-1] < ma[i-1] and closes[i] > ma[i] and ma_up and vol_big:
            buys.append(i)
            stops.append(round(min(float(lows[i]), float(ma[i])), 2))
        elif closes[i-1] > ma[i-1] and closes[i] < ma[i] and ma_dn and vol_big:
            sells.append(i)
    return buys[-3:], sells[-3:], stops[-3:]


def detect_gann_recross(closes, highs, lows, volumes, ma_period=20, lookback=5):
    """
    葛蘭碧站回訊號：
    條件：前N根內曾跌破均線，最新收盤站回均線之上
    回傳：(訊號是否成立, 均線值, 均線名稱, 防守建議)
    """
    n = len(closes)
    if n < ma_period + lookback + 1:
        return False, None, None, None

    ma = np.full(n, np.nan)
    for i in range(ma_period - 1, n):
        ma[i] = closes[i - ma_period + 1: i + 1].mean()

    curr_close = closes[-1]
    curr_ma    = ma[-1]
    if np.isnan(curr_ma):
        return False, None, None, None

    # 現在要站上均線
    if curr_close <= curr_ma:
        return False, None, None, None

    # 往前 lookback 根內，至少有一根收在均線下方（曾跌破）
    had_below = any(
        not np.isnan(ma[-(lookback + 1 + j)]) and closes[-(lookback + 1 + j)] < ma[-(lookback + 1 + j)]
        for j in range(lookback)
    )
    if not had_below:
        return False, None, None, None

    # 均線方向：水平或向上才算有效站回（下降趨勢中的反彈不算）
    ma_slope_ok = ma[-1] >= ma[-(min(5, n))]  # 近5根均線不往下

    name = f"MA{ma_period}"
    stop = round(float(curr_ma) * 0.985, 2)   # 防守位：均線下 1.5%
    return True, round(float(curr_ma), 2), name, stop


def calc_breakout_signals(closes, highs, lows, volumes, support, resistance):
    """
    突破壓力 / 跌破支撐訊號
    量能條件：爆量（>均量1.5倍）或凹洞量（<均量0.5倍，健康型突破）

    ⚠️ Bug fix：改用「滾動局部高低點」作為每根K棒當時的壓力/支撐參考，
       而非用分析當下的 support/resistance 去掃整段歷史（那樣會造成語義偏移）。
    策略：
      - 只在最近 LOOKBACK 根內尋找訊號，避免顯示太舊的標記
      - 每根K棒的「當時壓力」= 前 40 根的局部最高收盤；「當時支撐」= 前 40 根局部最低收盤
      - 最後一次訊號若距今 > 30 根，標記 stale=True，前端可選擇淡化或不顯示
    回傳：
      breakout_idx:  最近一次突破索引（全域），None = 無
      breakdown_idx: 最近一次跌破索引（全域），None = 無
      breakout_stale:  bool，訊號是否過舊
      breakdown_stale: bool，訊號是否過舊
    """
    n = len(closes)
    LOOKBACK = min(n, 120)   # 只掃最近 120 根
    WINDOW   = 40            # 每根K棒「往前看」幾根來決定當時的局部支撐/壓力
    STALE    = 30            # 超過幾根視為過舊

    vol_ma = np.full(n, np.nan)
    for i in range(19, n):
        vol_ma[i] = volumes[i - 19: i + 1].mean()

    breakout_idx  = None
    breakdown_idx = None

    scan_start = max(WINDOW + 1, n - LOOKBACK)

    for i in range(scan_start, n):
        if np.isnan(vol_ma[i]):
            continue
        vol_ok = (volumes[i] > vol_ma[i] * 1.5) or (volumes[i] < vol_ma[i] * 0.5)
        if not vol_ok:
            continue

        # 當時的局部壓力/支撐：往前 WINDOW 根的收盤高/低（不含當根）
        local_resist = closes[i - WINDOW: i].max()
        local_support = closes[i - WINDOW: i].min()

        # 突破：前一根收在局部壓力以下，這一根放量站上局部壓力 × 1.005
        if (closes[i - 1] < local_resist * 1.005
                and closes[i] >= local_resist * 1.005):
            breakout_idx = i

        # 跌破：前一根收在局部支撐以上，這一根放量跌破局部支撐 × 0.995
        if (closes[i - 1] > local_support * 0.995
                and closes[i] <= local_support * 0.995):
            breakdown_idx = i

    # 若訊號距今超過 STALE 根，標記為過舊
    breakout_stale  = (breakout_idx  is not None and (n - 1 - breakout_idx)  > STALE)
    breakdown_stale = (breakdown_idx is not None and (n - 1 - breakdown_idx) > STALE)

    return breakout_idx, breakdown_idx, breakout_stale, breakdown_stale


# ══════════════════════════════════════════════════════════
# API 快取（同股票+時間框架，5分鐘內不重複抓取）
# ══════════════════════════════════════════════════════════
import time as _time
_analyze_cache: dict = {}   # key: "{stock_id}_{tf}_{YYYYMMDD}" → {"ts": float, "data": dict}

_ANALYZE_CACHE_TTL = 86400  # key 含日期，當天只打一次 FinMind，隔天 key 不同自動失效

def _cache_get(key: str):
    entry = _analyze_cache.get(key)
    if entry and (_time.time() - entry["ts"]) < _ANALYZE_CACHE_TTL:
        return entry["data"]
    return None

def _cache_set(key: str, data: dict):
    _analyze_cache[key] = {"ts": _time.time(), "data": data}
    if len(_analyze_cache) > 200:
        cutoff = _time.time() - _ANALYZE_CACHE_TTL
        expired = [k for k, v in _analyze_cache.items() if v["ts"] < cutoff]
        for k in expired:
            _analyze_cache.pop(k, None)


# ══════════════════════════════════════════════════════════
# 端點
# ══════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════
# 會員系統核心函式（需在端點前定義）
# ══════════════════════════════════════════════════════════
import base64 as _base64_mod

def _db_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def _db_init():
    conn = _db_conn()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS members (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            email       TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            plan        TEXT DEFAULT 'free',
            expire_at   TEXT DEFAULT NULL,
            created_at  TEXT DEFAULT (datetime('now','+8 hours')),
            last_login  TEXT DEFAULT NULL,
            token_ver   INTEGER DEFAULT 0,
            session_id  TEXT DEFAULT NULL
        );
        CREATE TABLE IF NOT EXISTS query_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id  INTEGER NOT NULL,
            date       TEXT NOT NULL,
            count      INTEGER DEFAULT 0,
            ip         TEXT    NOT NULL DEFAULT "",
        UNIQUE(member_id, date, ip)
        );
        CREATE TABLE IF NOT EXISTS visits (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            ip    TEXT NOT NULL,
            date  TEXT NOT NULL,
            UNIQUE(ip, date)
        );
        CREATE TABLE IF NOT EXISTS pending_orders (
            merchant_trade_no TEXT PRIMARY KEY,
            email             TEXT NOT NULL,
            hashed_password   TEXT NOT NULL,
            plan              TEXT NOT NULL,
            created_at        TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS processed_orders (
            merchant_trade_no TEXT PRIMARY KEY,
            processed_at      TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS contact_messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            email      TEXT NOT NULL,
            message    TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS blocked_users (
            email      TEXT PRIMARY KEY,
            block_type TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS contact_replies (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            reply      TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            token      TEXT PRIMARY KEY,
            email      TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            used       INTEGER DEFAULT 0,
            ip         TEXT    DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS price_alerts (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email   TEXT    NOT NULL,
            stock_id     TEXT    NOT NULL,
            target_price REAL    NOT NULL,
            direction    TEXT    NOT NULL,
            created_at   TEXT    NOT NULL,
            triggered    INTEGER DEFAULT 0,
            triggered_at TEXT    DEFAULT NULL
        );
        CREATE TABLE IF NOT EXISTS push_subscriptions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email  TEXT    NOT NULL,
            endpoint    TEXT    NOT NULL UNIQUE,
            p256dh      TEXT    NOT NULL,
            auth        TEXT    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS stock_reports (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id    TEXT NOT NULL,
            report_date TEXT NOT NULL,
            stock_name  TEXT NOT NULL DEFAULT '',
            report_html TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now','+8 hours')),
            UNIQUE(stock_id, report_date)
        );
        CREATE TABLE IF NOT EXISTS referral_codes (
            user_email  TEXT PRIMARY KEY,
            code        TEXT UNIQUE NOT NULL,
            created_at  TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS referral_logs (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            inviter_email TEXT NOT NULL,
            invitee_email TEXT NOT NULL,
            invitee_ip    TEXT NOT NULL DEFAULT '',
            status        TEXT DEFAULT 'pending',
            created_at    TEXT DEFAULT (datetime('now','+8 hours'))
        );
    """)
    conn.commit()

    # 自動補上新欄位（舊資料庫升級用）
    new_columns = [
        ("members", "session_id", "TEXT DEFAULT NULL"),
        ("members", "token_ver",  "INTEGER DEFAULT 0"),
        ("members", "expire_at",  "TEXT DEFAULT NULL"),
        ("members", "last_login", "TEXT DEFAULT NULL"),
        ("query_log", "ip",                   "TEXT NOT NULL DEFAULT ''"),
        ("members",   "password_changed_at",  "TEXT DEFAULT NULL"),
        ("members",   "last_expire_notice_date", "TEXT DEFAULT NULL"),
        ("members",   "referral_unlocked",       "INTEGER DEFAULT 0"),
        ("members",   "referral_expire_date",    "TEXT DEFAULT NULL"),
        ("query_log", "report_count",             "INTEGER DEFAULT 0"),
    ]
    for table, col, coldef in new_columns:
        try:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {coldef}")
            conn.commit()
            print(f"   ✅ 資料庫補欄位：{table}.{col}")
        except Exception:
            pass  # 欄位已存在，忽略

    # 自動建立管理員帳號（已存在則不覆蓋）
    ADMIN_EMAIL = "watione@yahoo.com.tw"
    ADMIN_PWD   = "630428"
    ADMIN_EXPIRE = "2099-12-31"
    existing = conn.execute("SELECT id FROM members WHERE email=?", (ADMIN_EMAIL,)).fetchone()
    if not existing:
        conn.execute(
            "INSERT INTO members (email, password, plan, expire_at) VALUES (?, ?, ?, ?)",
            (ADMIN_EMAIL, _hash_pw(ADMIN_PWD), "yearly", ADMIN_EXPIRE)
        )
        conn.commit()
        print(f"   ✅ 管理員帳號已建立：{ADMIN_EMAIL}")
    else:
        print(f"   ✅ 管理員帳號已存在：{ADMIN_EMAIL}")
    # 確保管理員維持 yearly 方案（舊帳號若為 free 則自動升級）
    conn.execute(
        "UPDATE members SET plan='yearly', expire_at=? WHERE email=? AND plan='free'",
        (ADMIN_EXPIRE, ADMIN_EMAIL)
    )
    conn.commit()

    conn.close()

def _b64url_encode(data: bytes) -> str:
    return _base64_mod.urlsafe_b64encode(data).rstrip(b"=").decode()

def _b64url_decode(s: str) -> bytes:
    pad = 4 - len(s) % 4
    if pad != 4:
        s += "=" * pad
    return _base64_mod.urlsafe_b64decode(s)

def _jwt_create(payload: dict) -> str:
    header = _b64url_encode(_json_mod.dumps({"alg":"HS256","typ":"JWT"}).encode())
    body   = _b64url_encode(_json_mod.dumps(payload).encode())
    sig_input = f"{header}.{body}".encode()
    sig = hmac.new(JWT_SECRET.encode(), sig_input, hashlib.sha256).digest()
    return f"{header}.{body}.{_b64url_encode(sig)}"

def _jwt_verify(token: str) -> dict | None:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header, body, sig = parts
        sig_input = f"{header}.{body}".encode()
        expected = hmac.new(JWT_SECRET.encode(), sig_input, hashlib.sha256).digest()
        if not hmac.compare_digest(_b64url_decode(sig), expected):
            return None
        payload = _json_mod.loads(_b64url_decode(body))
        if payload.get("exp", 0) < _time_mod.time():
            return None
        return payload
    except Exception:
        return None

def _hash_pw(password: str) -> str:
    salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return f"{salt}:{h.hex()}"

def _verify_pw(password: str, stored: str) -> bool:
    try:
        salt, h = stored.split(":", 1)
        expected = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
        return hmac.compare_digest(expected.hex(), h)
    except Exception:
        return False

def get_current_user(authorization: str | None = Header(default=None)) -> dict | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization[7:]
    payload = _jwt_verify(token)
    if not payload:
        return None
    conn = _db_conn()
    row = conn.execute("SELECT * FROM members WHERE id=?", (payload["sub"],)).fetchone()
    conn.close()
    if not row or row["token_ver"] != payload.get("ver", 0):
        return None
    # 帳號共享防護：session_id 不符代表已在其他裝置登入
    if row["session_id"] and payload.get("sid") and row["session_id"] != payload.get("sid"):
        return None
    return dict(row)

def require_user(user: dict | None = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="請先登入")
    return user

def require_paid_user(user: dict | None = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="請先登入")
    if _is_referral_active(user):
        return user
    today = _date_cls.today().isoformat()
    if user["plan"] == "free":
        raise HTTPException(status_code=403, detail="此功能需付費方案")
    if user.get("expire_at") and user["expire_at"] < today:
        raise HTTPException(status_code=403, detail="訂閱已到期，請續費後使用")
    return user

def _taipei_today() -> str:
    """台北時間今日日期（YYYY-MM-DD），用於每日查詢次數重置"""
    from zoneinfo import ZoneInfo
    return datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d")

def _taipei_now_str(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """台北時間現在（預設 YYYY-MM-DD HH:MM:SS），全後端存 DB 一律用這個"""
    from zoneinfo import ZoneInfo
    return datetime.now(ZoneInfo("Asia/Taipei")).strftime(fmt)

def _is_referral_active(user: dict) -> bool:
    """邀請制解鎖是否有效（已解鎖 且 未過期）"""
    if not user.get("referral_unlocked", 0):
        return False
    exp = user.get("referral_expire_date")
    if not exp:
        return True  # 舊資料無過期日，向下相容視為有效
    return exp >= _date_cls.today().isoformat()

def _check_query_limit(member_id: int, plan: str) -> tuple[bool, int, int]:
    """回傳 (允許查詢, 今日已用次數, 上限)"""
    if plan != "free":
        return True, 0, 999
    today = _taipei_today()
    conn = _db_conn()
    row = conn.execute(
        "SELECT count FROM query_log WHERE member_id=? AND date=?",
        (member_id, today)
    ).fetchone()
    used = row["count"] if row else 0
    conn.close()
    return used < FREE_DAILY_LIMIT, used, FREE_DAILY_LIMIT

def _inc_query_count(member_id: int):
    today = _taipei_today()
    conn = _db_conn()
    row = conn.execute(
        "SELECT id, count FROM query_log WHERE member_id=? AND date=? AND ip=''",
        (member_id, today)
    ).fetchone()
    if row:
        conn.execute(
            "UPDATE query_log SET count=count+1 WHERE id=?",
            (row["id"],)
        )
    else:
        conn.execute(
            "INSERT INTO query_log (member_id, date, ip, count) VALUES (?, ?, '', 1)",
            (member_id, today)
        )
    conn.commit()
    conn.close()

def _check_report_limit(member_id: int) -> tuple[bool, int]:
    """回傳 (允許產出報告, 今日已產出次數)"""
    today = _taipei_today()
    conn = _db_conn()
    row = conn.execute(
        "SELECT report_count FROM query_log WHERE member_id=? AND date=? AND ip=''",
        (member_id, today)
    ).fetchone()
    used = row["report_count"] if row else 0
    conn.close()
    return used < FREE_DAILY_LIMIT, used

def _inc_report_count(member_id: int):
    today = _taipei_today()
    conn = _db_conn()
    conn.execute(
        "INSERT INTO query_log (member_id, date, ip, count, report_count) VALUES (?,?,'',0,1) "
        "ON CONFLICT(member_id, date, ip) DO UPDATE SET report_count=report_count+1",
        (member_id, today)
    )
    conn.commit()
    conn.close()

PERIOD_MAP = {"D": ("3y", "1d"), "W": ("5y", "1wk"), "M": ("10y", "1mo")}


@app.get("/api/debug/{stock_id}")
def debug_stock(stock_id: str):
    """
    診斷用：查詢股票的市場別判斷 + yfinance 是否能抓到資料
    範例：/api/debug/2377
    """
    code = stock_id.strip().upper()
    mtype = _market_cache.get(code, "未知（未在 FinMind 快取中）")
    symbol_tw  = code + ".TW"
    symbol_two = code + ".TWO"

    results = {}
    for sym in [symbol_tw, symbol_two]:
        try:
            _, df = try_fetch(sym, "5d", "1d")
            results[sym] = {
                "empty": df.empty,
                "rows": len(df),
                "last_close": safe_float(df["Close"].iloc[-1]) if not df.empty else None,
            }
        except Exception as e:
            results[sym] = {"error": str(e)}

    return {
        "stock_id": code,
        "market_cache": mtype,
        "resolved_symbol": resolve_symbol(code),
        "yfinance_results": results,
    }


@app.get("/api/kline/{stock_id}")
def get_kline(stock_id: str, tf: str = "D", user: dict = Depends(require_user)):
    period, interval = PERIOD_MAP.get(tf.upper(), ("3y", "1d"))
    try:
        symbol, df = try_fetch(stock_id, period, interval)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下載失敗：{e}")
    if df.empty:
        mtype = _market_cache.get(stock_id.strip().upper(), "未知")
        raise HTTPException(
            status_code=404,
            detail=f"找不到股票：{stock_id}（嘗試代碼：{symbol}，市場別：{mtype}）"
        )
    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    records = []
    for idx, row in df.iterrows():
        date_str = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)[:10]
        records.append({
            "date": date_str,
            "open": safe_float(row["Open"]), "high": safe_float(row["High"]),
            "low": safe_float(row["Low"]),   "close": safe_float(row["Close"]),
            "volume": int(row["Volume"]) if not np.isnan(row["Volume"]) else 0,
        })
    return {"symbol": symbol, "tf": tf, "count": len(records), "bars": records}


def _do_analyze(stock_id: str, tf: str = "D",
                ma1: int = 5, ma2: int = 10, ma3: int = 20, ma4: int = 60, ma5: int = 120,
                user: dict | None = None):
    """核心分析邏輯（不含驗證），供 analyze() 和 batch_analyze() 共用"""
    # 快取：同股票+時間框架+當天，盤中 15 分鐘更新，收盤後固定到隔天
    _cache_key = f"{stock_id.strip().upper()}_{tf.upper()}_{_taipei_today().replace('-', '')}"
    cached = _cache_get(_cache_key)
    if cached:
        return cached

    period, interval = PERIOD_MAP.get(tf.upper(), ("3y", "1d"))
    try:
        symbol, df = try_fetch(stock_id, period, interval)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if df.empty:
        mtype = _market_cache.get(stock_id.strip().upper(), "未知")
        raise HTTPException(
            status_code=404,
            detail=f"找不到股票：{stock_id}（嘗試代碼：{symbol}，市場別：{mtype}）。"
                   f"可能是 Yahoo Finance 暫時無資料，請稍後再試。"
        )

    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    opens      = df["Open"].values.astype(float)
    closes     = df["Close"].values.astype(float)
    closes_full= closes.copy()   # 保留完整序列供 MA 計算
    highs      = df["High"].values.astype(float)
    lows       = df["Low"].values.astype(float)
    volumes    = df["Volume"].values.astype(float)
    price      = round(float(closes[-1]), 2)

    # 股名
    stock_name = get_stock_name(symbol)

    # 均線
    ma_periods = [p for p in [ma1, ma2, ma3, ma4, ma5] if p and p > 0]
    ma_values = {f"ma{p}": safe_float(calc_ma(closes, p)[-1]) for p in ma_periods}

    # 趨勢
    avail = [(p, calc_ma(closes, p)[-1]) for p in sorted(ma_periods)
             if not np.isnan(calc_ma(closes, p)[-1])]
    trend = "觀察中"
    if len(avail) >= 2:
        s, l = avail[0][1], avail[-1][1]
        trend = "上升趨勢" if s > l * 1.005 else "下降趨勢" if s < l * 0.995 else "盤整"

    # 趨勢軌道（先算，軌道下緣納入支撐候選競爭）
    channel = find_trend_channel(highs, lows, closes)

    # 若直線軌道 R² 不高，嘗試三角形型態
    if not channel or channel.get("r2", 0) < 0.6:
        tri = detect_triangle_channel(highs, lows, closes)
        if tri and tri.get("r2", 0) > (channel.get("r2", 0) if channel else 0):
            channel = tri

    # 支撐壓力（把軌道下緣一起傳入，納入候選競爭）
    _ch_support = channel.get("support_now") if channel else None
    support, resistance, supp_detail = find_support_resistance(
        highs, lows, closes, volumes, price, channel_support=_ch_support)

    # 近期高低點（用於 near_top / near_bot 判斷）
    # 排除今天（最後一根），避免今日創高時 near_top 誤判
    ch_hi    = round(float(highs[:-1][-20:].max()), 2) if len(highs) > 1 else round(float(highs.max()), 2)
    ch_lo    = round(float(lows[-20:].min()), 2)
    near_top = price > ch_hi * 0.97
    near_bot = price < ch_lo * 1.03

    # 反轉型態（W底/M頭/頭肩）— 優先級最高，若找到則覆蓋軌道
    reversal = detect_reversal_pattern(highs, lows, closes)
    if reversal:
        # 反轉型態找到時，整合進 channel 但保留軌道線顯示
        reversal_desc = reversal["desc"]
        reversal_pos  = reversal["position_desc"]
        # 反轉型態的支撐壓力比軌道更重要
        if reversal.get("support_now") and reversal["support_now"] < price:
            support    = reversal["support_now"]
            supp_detail["support_desc"]   = f"{reversal['desc']} 支撐"
            supp_detail["support_source"] = reversal["type"]
        if reversal.get("resist_now") and reversal["resist_now"] > price:
            resistance = reversal["resist_now"]
            supp_detail["resistance_desc"] = f"{reversal['desc']} 頸線/壓力"
    else:
        reversal_desc = None
        reversal_pos  = None

    # 支撐距現價 >12% 時降級，改用 MA20 或 MA60 補位（閾值從8%放寬到12%，保留真實支撐）
    sup_dist_pct = (price - support) / price * 100
    if sup_dist_pct > 12:
        ma20_val = safe_float(calc_ma(closes_full, 20)[-1])
        ma60_val = safe_float(calc_ma(closes_full, 60)[-1])
        for ma_v, ma_name in [(ma20_val, "MA20"), (ma60_val, "MA60")]:
            if ma_v is not None and ma_v < price * 0.999:
                new_dist = (price - ma_v) / price * 100
                if new_dist < sup_dist_pct:
                    support = round(float(ma_v), 2)
                    supp_detail["support_source"] = "ma_fallback"
                    supp_detail["support_desc"] = f"{ma_name} 動態支撐（原支撐過遠已降級）"
                    sup_dist_pct = new_dist
                    break

    # 軌道上緣：若在現價以上且比現有壓力更近，則取代
    if channel:
        ch_res = channel.get("resist_now", 0)
        if ch_res > 0 and ch_res > price * 1.001:
            if ch_res < resistance:
                resistance = round(ch_res, 2)
                supp_detail["resistance_desc"] = f"軌道上緣（{channel['desc']}）"
        # 軌道下緣 >8% 時不納入支撐競爭，但在說明補充提示
        ch_sup = channel.get("support_now", 0)
        if ch_sup and ch_sup < price * 0.999:
            ch_sup_dist = (price - ch_sup) / price * 100
            if ch_sup_dist > 8:
                supp_detail["support_desc"] += f"，軌道下緣 {round(ch_sup,1)}（-{ch_sup_dist:.1f}%，長線參考）"

    # ── 今日突破快速判斷：現價超過前19根最高點 ──
    # 避免今天創高時，近20日最高點 = 現價，導致壓力 = 現價、損益比 = 0
    prev_high = round(float(highs[:-1][-19:].max()), 2) if len(highs) > 1 else resistance
    today_breakout = float(closes[-1]) > prev_high * 1.001

    # 突破當日不顯示「靠近壓力」警告
    if today_breakout:
        near_top = False

    # ── 壓力最小距離過濾：壓力距現價 < 3% 時往上找下一個有效壓力 ──
    MIN_RES_DIST = 0.03
    res_dist_pct = (resistance - price) / price
    if res_dist_pct < MIN_RES_DIST:
        alt_res = None
        alt_res_desc = ""
        from scipy.signal import argrelextrema as _argrelextrema
        # 排除今天（index -1）避免今日高點被選為壓力
        hi_idx_all = _argrelextrema(highs[:-1], np.greater, order=5)[0]
        candidates = [(highs[i], i) for i in hi_idx_all
                      if highs[i] > price * (1 + MIN_RES_DIST)]
        if candidates:
            alt_val, alt_i = min(candidates, key=lambda x: x[0])
            alt_res = round(float(alt_val), 2)
            alt_res_desc = f"轉折高點（{len(highs) - 1 - alt_i}根前）"
        else:
            # fallback：軌道上緣估算或歷史高點
            if channel and channel.get("target1") and channel["target1"] > price * (1 + MIN_RES_DIST):
                alt_res = round(float(channel["target1"]), 2)
                alt_res_desc = "軌道目標價"
            else:
                alt_res = round(float(highs[:-1].max()), 2)
                alt_res_desc = "歷史高點（備援）"

        if alt_res and alt_res != resistance:
            resistance = alt_res
            supp_detail["resistance_desc"] = alt_res_desc + ("（突破後下一壓力）" if today_breakout else "（原壓力過近已調整）")

    # 型態
    # today_breakout 優先：今日收盤突破前高，直接判斷為突破型態，不進 detect_pattern
    if today_breakout:
        pattern, pattern_sub = "突破型態", "今日突破"
    else:
        pattern, pattern_sub = detect_pattern(price, support, resistance, ch_lo, ch_hi)

    # K棒型態辨識
    kbar_pattern, kbar_warning, kbar_dir = detect_kbar_pattern(opens, highs, lows, closes)

    # 葛蘭碧（加量能過濾）
    ma20_arr = calc_ma(closes, 20)
    buy_idx, sell_idx, buy_stops = calc_gann_filtered(closes, highs, lows, volumes, 20)

    # 葛蘭碧站回偵測（跌破後站回 MA20 / MA60）
    gann_ma20_signal, gann_ma20_val, gann_ma20_name, gann_ma20_stop = detect_gann_recross(closes, highs, lows, volumes, 20)
    gann_ma60_signal, gann_ma60_val, gann_ma60_name, gann_ma60_stop = detect_gann_recross(closes, highs, lows, volumes, 60)
    # 優先用 MA60 站回（較強訊號），其次 MA20
    gann_recross = None
    if gann_ma60_signal:
        gann_recross = {"ma": gann_ma60_name, "val": gann_ma60_val, "stop": gann_ma60_stop}
    elif gann_ma20_signal:
        gann_recross = {"ma": gann_ma20_name, "val": gann_ma20_val, "stop": gann_ma20_stop}

    # 突破壓力 / 跌破支撐訊號
    breakout_idx, breakdown_idx, breakout_stale, breakdown_stale = calc_breakout_signals(
        closes, highs, lows, volumes, support, resistance)

    # 防守位：優先順序
    # 1. 若軌道下緣距現價 ≤8%，用軌道下緣下 1.5% 作防守位
    # 2. 若支撐距現價超過 5%，改用現價下方 5%（避免防守位過遠失去意義）
    # 3. 否則用支撐下 1.5%
    # 4. 最小距現價 2%，最大不超過現價 10%
    ch_sup_now = channel.get("support_now") if channel else None
    sup_dist_pct = (price - support) / price * 100
    if ch_sup_now and ch_sup_now < price * 0.999:
        ch_sup_dist_pct = (price - ch_sup_now) / price * 100
        if ch_sup_dist_pct <= 8:
            raw_stop = round(ch_sup_now * 0.985, 2)
        elif sup_dist_pct > 5:
            raw_stop = round(price * 0.95, 2)
        else:
            raw_stop = round(support * 0.985, 2)
    elif sup_dist_pct > 5:
        raw_stop = round(price * 0.95, 2)
    else:
        raw_stop = round(support * 0.985, 2)
    min_stop  = round(price * 0.98, 2)   # 最近不能超過現價 2%
    max_stop  = round(price * 0.90, 2)   # 最遠不超過現價 10%
    stop_loss = min(min_stop, max(raw_stop, max_stop))

    # 目標價
    target1 = resistance
    if channel and channel.get("target1"):
        target2 = channel["target1"]
    else:
        target2 = round(resistance * 1.10, 2)

    # 風險報酬：改用「現價-防守位」當風險，防守位已有最小2%保護
    # 避免支撐太近時（如 -0.7%）導致 RR 爆大失真
    risk   = price - stop_loss          # 以防守位為停損基準
    reward = target1 - price
    rr_ratio = round(reward / risk, 2) if risk > 0 else 0
    rr_basis  = "防守位"               # 說明計算基礎，供前端顯示

    # 風險等級
    risk_level, risk_label, risk_color = calc_risk_level(
        price, support, resistance, rr_ratio, near_top, near_bot, pattern)

    # K 線型態大數據勝率
    k_pattern, h_win_rate = detect_kline_patterns(
        closes.tolist(), opens.tolist(), highs.tolist(), lows.tolist(), volumes.tolist()
    )

    # 條列摘要
    summary_lines = build_summary(
        price, support, supp_detail["support_desc"],
        resistance, supp_detail["resistance_desc"],
        trend, pattern, rr_ratio, risk_level, risk_label,
        near_top, near_bot, stop_loss, target1, rr_basis,
        kline_pattern=k_pattern, win_rate=h_win_rate)

    # K棒型態加進摘要
    if kbar_pattern:
        summary_lines.append(f"K棒型態：{kbar_pattern}")
    if kbar_warning:
        summary_lines.append(f"⚠ {kbar_warning}")

    # ── 最終結論整合器 ──

    # 軌道與均線趨勢是否矛盾（需在使用 conflict_note 之前計算）
    channel_type = channel.get("type", "") if channel else ""
    trend_channel_conflict = (
        (trend == "上升趨勢" and channel_type == "down") or
        (trend == "下降趨勢" and channel_type == "up")
    )
    conflict_note = ""
    if trend_channel_conflict:
        if trend == "上升趨勢" and channel_type == "down":
            conflict_note = f"⚠ 注意：均線多頭但股價在下降軌道內，短線結構偏弱，均線支撐可能失守，建議觀望或輕倉"
        elif trend == "下降趨勢" and channel_type == "up":
            conflict_note = f"⚠ 注意：均線空頭但股價在上升軌道內，反彈動能存在但趨勢仍弱，等均線轉向確認再追"

    # 軌道趨勢矛盾警告（插在最前面，醒目位置）
    if conflict_note:
        summary_lines.insert(0, conflict_note)

    # 反轉/三角型態加進摘要
    if reversal:
        summary_lines.insert(0, f"圖形型態：{reversal['desc']}，{reversal['position_desc']}")

    # K棒方向判斷（含操作建議）
    kbar_bullish = any(k in kbar_pattern for k in ["錘頭","多頭吞噬","早晨之星","三紅兵","穿刺線","大紅棒"]) if kbar_pattern else False
    kbar_bearish = any(k in kbar_pattern for k in ["射擊之星","空頭吞噬","黃昏之星","三烏鴉","烏雲蓋頂","大黑棒"]) if kbar_pattern else False
    kbar_neutral = not kbar_bullish and not kbar_bearish

    # K棒操作說明對照（具體化）
    KBAR_ACTION = {
        "錘頭線":       f"明天收紅且量縮可試多，防守位設 {stop_loss}",
        "射擊之星":     f"頂部反轉訊號，建議先出場觀望，等回測支撐 {support} 守住再重新評估進場時機",
        "十字星":       f"方向未定，等明天收盤確認，不宜追高也不宜殺低",
        "大紅棒":       f"今日強攻，明天若縮量整理不跌破今日收盤 {round(float(closes[-1]),2)}，多頭延續可持有",
        "大黑棒":       f"今日強殺，建議出場觀望，等股價回到支撐 {support} 附近且出現止跌訊號再重新評估",
        "多頭吞噬":     f"底部反轉訊號，明天收紅確認後可設防守位 {stop_loss} 試多",
        "空頭吞噬":     f"頂部反轉訊號，明天收黑確認後建議減碼出場，等回測支撐 {support} 守住再重新布局",
        "孕線":         f"整理型態，等突破今日高低點再進場，不宜在盤中追價",
        "穿刺線":       f"底部潛在反轉，明天若繼續收紅可加碼，防守位設 {stop_loss}",
        "烏雲蓋頂":     f"頂部潛在反轉，明天若收黑確認建議出場，等拉回至支撐 {support} 附近再重新評估",
        "早晨之星":     f"底部強力反轉，確認訊號，可設防守位 {stop_loss} 進場，目標看 {resistance}",
        "黃昏之星":     f"頂部強力反轉，建議出場觀望，待股價拉回至支撐 {support} 附近出現止跌K棒再重新布局",
        "三紅兵":       f"多頭強勢，可持有，但連漲三天後注意追高風險，不宜此時首次進場",
        "三烏鴉":       f"空頭強勢，建議全數出場觀望，等跌勢止穩、支撐 {support} 守住後再重新評估進場",
    }

    # 找對應的操作說明
    kbar_action = ""
    for key, action in KBAR_ACTION.items():
        if kbar_pattern and key in kbar_pattern:
            kbar_action = action
            break

    near_sup = pattern in ("支撐整理",) or (price - support) / price < 0.04
    near_res = pattern in ("壓力整理",) or (resistance - price) / price < 0.04

    # 軌道下緣靠近判斷（距現價 ≤3%）
    ch_near_sup = False
    ch_sup_desc = ""
    if channel and channel.get("position") == "near_support":
        ch_near_sup = True
        ch_sup_val = channel.get("support_now", support)
        ch_sup_desc = f"靠近軌道下緣支撐 {ch_sup_val}"

    if near_sup:
        if rr_ratio >= 1.5 and kbar_bullish:
            conclusion = f"靠近支撐 {support}，出現多頭K棒（{kbar_pattern}），損益比 {rr_ratio} 佳。操作：{kbar_action or f'可設防守位 {stop_loss} 試多，目標壓力 {resistance}'}"
        elif rr_ratio >= 1.5 and kbar_neutral:
            conclusion = f"靠近支撐 {support}，K棒方向未定（{kbar_pattern or '無明確型態'}）。操作：等明天收盤確認方向再進場，防守位 {stop_loss}"
        elif rr_ratio >= 1.5 and kbar_bearish:
            conclusion = f"靠近支撐 {support}，但出現空頭K棒（{kbar_pattern}），支撐恐失守。操作：{kbar_action or f'先觀望，跌破 {support} 出場'}"
        else:
            conclusion = f"靠近支撐 {support}，但損益比 {rr_ratio} 偏低（壓力 {resistance} 太遠或太近）。操作：等支撐確認守住再評估，防守位 {stop_loss}"
    elif ch_near_sup and not near_res:
        # 軌道下緣靠近，優先給出低風險試多建議
        ch_sup_val = channel.get("support_now", support)
        if kbar_bullish:
            conclusion = f"{ch_sup_desc}，出現多頭K棒（{kbar_pattern}），相對低風險位置。操作：{kbar_action or f'可設防守位 {stop_loss} 試多，目標壓力 {resistance}'}"
        elif kbar_bearish:
            conclusion = f"{ch_sup_desc}，但出現空頭K棒（{kbar_pattern}），軌道支撐恐失守。操作：{kbar_action or f'觀望，若跌破軌道下緣 {ch_sup_val} 出場'}"
        else:
            conclusion = f"{ch_sup_desc}，相對低風險觀察位。操作：等明天出現止跌K棒確認守住後可設防守位 {stop_loss} 試多，目標壓力 {resistance}"
    elif gann_recross:
        # 葛蘭碧站回訊號
        ma_name = gann_recross["ma"]
        ma_val  = gann_recross["val"]
        g_stop  = gann_recross["stop"]
        if kbar_bullish:
            conclusion = f"跌破後站回 {ma_name}（{ma_val}），出現多頭K棒（{kbar_pattern}）。葛蘭碧買點確認，操作：可設防守位 {g_stop}（{ma_name} 下方）試多，目標壓力 {resistance}"
        elif kbar_bearish:
            conclusion = f"跌破後站回 {ma_name}（{ma_val}），但出現空頭K棒（{kbar_pattern}），站回力道存疑。操作：等明天確認站穩 {ma_name} 再進場，防守位 {g_stop}"
        else:
            conclusion = f"跌破後站回 {ma_name}（{ma_val}），葛蘭碧潛在買點。操作：明天若確認站穩 {ma_name} 可設防守位 {g_stop} 試多，目標壓力 {resistance}"
    elif near_res:
        if kbar_bullish:
            conclusion = f"靠近壓力 {resistance}，出現多頭K棒（{kbar_pattern}）。操作：{kbar_action or f'等放量突破 {resistance} 再追，未突破先觀望，停損 {stop_loss}'}"
        elif kbar_bearish:
            conclusion = f"靠近壓力 {resistance}，出現空頭K棒（{kbar_pattern}），拉回風險高。操作：{kbar_action or f'建議先出場或減碼觀望，等拉回至支撐 {support} 附近守住再重新評估進場'}"
        else:
            conclusion = f"靠近壓力 {resistance}，追價風險高。操作：等放量突破確認後再跟，或等回測支撐 {support} 後進場，停損 {stop_loss}"
    elif pattern == "突破型態":
        if today_breakout:
            if kbar_bearish:
                conclusion = f"今日突破前高 {prev_high}，但出現空頭K棒（{kbar_pattern}），留意假突破。操作：等明天確認守住 {prev_high} 再進場，防守位 {stop_loss}"
            else:
                conclusion = f"今日放量突破前高 {prev_high}，突破型態確立。操作：可持有，明天若縮量回測不破 {prev_high} 可加碼，防守位 {stop_loss}，下一壓力參考 {resistance}"
        else:
            conclusion = f"股價突破壓力 {prev_high}。操作：{'縮量回測不破可加碼，防守位 ' + str(stop_loss) if not kbar_bearish else f'出現{kbar_pattern}，留意假突破，防守位 {stop_loss}'}"
    elif pattern == "跌破型態":
        conclusion = f"股價跌破支撐 {support}，前支撐轉壓力。操作：{'建議出場觀望，等止跌企穩、支撐 ' + str(support) + ' 重新守住後再重新評估進場' if not kbar_bullish else f'出現{kbar_pattern}，觀察是否為假跌破，守住 {support} 才考慮反彈操作'}"
    else:
        if kbar_bullish:
            conclusion = f"位於軌道中段，出現多頭K棒（{kbar_pattern}）。操作：{kbar_action or f'可小量試多，等突破壓力 {resistance} 確認再加碼，停損 {stop_loss}'}"
        elif kbar_bearish:
            conclusion = f"位於軌道中段，出現空頭K棒（{kbar_pattern}）。操作：{kbar_action or f'建議減碼觀望，等拉回至支撐 {support} 附近止跌後再重新評估進場時機'}"
        else:
            conclusion = f"位於軌道中段，方向未明。操作：觀望為主，等突破 {resistance} 或跌破 {support} 再跟進，防守位 {stop_loss}"

    # 移除舊的 warning，改用整合結論
    warning = conclusion

    # 技術指標
    rsi_arr  = calc_rsi(closes)
    macd_line, macd_sig, macd_hist = calc_macd(closes)
    k_arr, d_arr = calc_kd(highs, lows, closes)
    bb_mid, bb_upper, bb_lower = calc_bollinger(closes)
    obv_arr  = calc_obv(closes, volumes)

    indicators = {
        "rsi":       serialize_indicator(rsi_arr, 1),
        "macd":      serialize_indicator(macd_line, 3),
        "macd_sig":  serialize_indicator(macd_sig, 3),
        "macd_hist": serialize_indicator(macd_hist, 3),
        "k":         serialize_indicator(k_arr, 1),
        "d":         serialize_indicator(d_arr, 1),
        "bb_mid":    serialize_indicator(bb_mid, 2),
        "bb_upper":  serialize_indicator(bb_upper, 2),
        "bb_lower":  serialize_indicator(bb_lower, 2),
        "obv":       serialize_indicator(obv_arr, 0),
    }

    # K 線資料
    bars = []
    for i in range(len(df)):
        d = df.index[i]
        date_str = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)[:10]
        bars.append({
            "date": date_str,
            "open":   safe_float(df["Open"].iloc[i]),
            "high":   safe_float(df["High"].iloc[i]),
            "low":    safe_float(df["Low"].iloc[i]),
            "close":  safe_float(df["Close"].iloc[i]),
            "volume": int(df["Volume"].iloc[i]) if not np.isnan(df["Volume"].iloc[i]) else 0,
        })

    result = {
        "symbol": symbol, "stock_id": stock_id, "stock_name": stock_name, "tf": tf,
        "price": price,
        "support": support, "support_desc": supp_detail["support_desc"],
        "support_source": supp_detail["support_source"],
        "support_candidates": supp_detail["all_candidates"],
        "resistance": resistance, "resistance_desc": supp_detail["resistance_desc"],
        "upper_channel": ch_hi, "lower_channel": ch_lo,
        "trend": trend, "pattern": pattern, "pattern_sub": pattern_sub,
        "stop_loss": stop_loss, "target1": target1, "target2": target2,
        "risk_reward": rr_ratio, "rr_basis": rr_basis,
        "risk_level": risk_level, "risk_label": risk_label, "risk_color": risk_color,
        "summary": summary_lines,
        "warning": warning,
        "conflict_note": conflict_note,
        "kbar_pattern": kbar_pattern, "kbar_warning": kbar_warning,
        "kbar_dir": kbar_dir, "kbar_action": kbar_action,
        "gann_recross": gann_recross,
        "today_breakout": today_breakout, "prev_high": prev_high,
        "near_top": near_top, "near_bot": near_bot,
        "ma_values": ma_values, "buy_signals": buy_idx, "sell_signals": sell_idx,
        "buy_stops": buy_stops, "channel": channel,
        "breakout_idx": breakout_idx,
        "breakdown_idx": breakdown_idx,
        "breakout_stale": breakout_stale,
        "breakdown_stale": breakdown_stale,
        "reversal_pattern": reversal,
        "indicators": indicators,
        "bars": bars,
        "kline_pattern": k_pattern,
        "win_rate": h_win_rate,
    }
    _cache_set(_cache_key, result)

    # 計入查詢次數（免費用戶）
    if user and user["plan"] == "free":
        _inc_query_count(user["id"])

    return result


@app.get("/api/analyze/{stock_id}")
def analyze(stock_id: str, tf: str = "D",
            ma1: int = 5, ma2: int = 10, ma3: int = 20, ma4: int = 60, ma5: int = 120,
            request: Request = None,
            user: dict | None = Depends(get_current_user)):
    """API 端點：遊客可查 1 次，免費會員 3 次，付費無限"""
    # 股名轉代號：非純數字視為股票名稱，在對照表搜尋
    sid_clean = stock_id.strip()
    if not sid_clean.replace(".", "").isdigit():
        resolved = _name_to_code.get(sid_clean)
        if not resolved:
            # 模糊搜尋：包含輸入文字的第一筆
            resolved = next((code for name, code in _name_to_code.items() if sid_clean in name), None)
        if resolved:
            stock_id = resolved
        else:
            raise HTTPException(status_code=404, detail=f"找不到股票：{sid_clean}")
    today = _taipei_today()

    if user:
        plan = user["plan"]
        is_referral_unlocked = _is_referral_active(user)
        # 付費狀態驗證
        if plan != "free" and user["expire_at"] and user["expire_at"] < today:
            raise HTTPException(status_code=403, detail="訂閱已到期，請續費後繼續使用")
        # 免費用戶次數限制（邀請解鎖視為付費）
        if plan == "free" and not is_referral_unlocked:
            allowed, used, limit = _check_query_limit(user["id"], plan)
            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail=f"today_limit|今日免費查詢次數已用完（{limit} 次），升級付費方案即可無限查詢"
                )
    else:
        # 遊客：用 IP 追蹤次數
        client_ip = request.client.host if request else "unknown"
        conn = _db_conn()
        row = conn.execute(
            "SELECT count FROM query_log WHERE member_id=0 AND date=? AND ip=?",
            (today, client_ip)
        ).fetchone()
        used = row["count"] if row else 0
        if used >= GUEST_DAILY_LIMIT:
            raise HTTPException(
                status_code=429,
                detail=f"guest_limit|免費試用已達上限（{GUEST_DAILY_LIMIT} 次），登入後每日可查 {FREE_DAILY_LIMIT} 次"
            )
        # 記錄遊客查詢
        conn.execute(
            "INSERT INTO query_log (member_id, date, ip, count) VALUES (0, ?, ?, 1) "
            "ON CONFLICT(member_id, date) DO UPDATE SET count=count+1",
            (today, client_ip)
        )
        conn.commit()
        conn.close()

    # 記錄獨立訪客
    client_ip = request.client.host if request else "unknown"
    _record_visit(client_ip)

    # 完成邀請制（首次查詢觸發）
    if user:
        try:
            _complete_referral_if_pending(user["email"])
        except Exception as _ref_e:
            print(f"[REFERRAL] complete_referral_if_pending 失敗 {user['email']}：{_ref_e}")

    return _do_analyze(stock_id, tf, ma1, ma2, ma3, ma4, ma5, user=user)


@app.get("/api/top_gainers")
def get_top_gainers(limit: int = 10):
    """
    當日（或最近交易日）漲幅前幾名
    用 FinMind TaiwanStockPrice 抓最新一日全市場資料
    """
    import urllib.request, json as _json
    from datetime import date, timedelta

    # 往回找最近 5 個交易日，避免假日
    token = FINMIND_TOKEN
    for days_back in range(1, 6):
        target = (date.today() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        try:
            url = (f"https://api.finmindtrade.com/api/v4/data"
                   f"?dataset=TaiwanStockPrice&start_date={target}&end_date={target}"
                   f"&token={token}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = _json.loads(resp.read())
            rows = data.get("data", [])
            # 過濾：只留4碼純數字、有成交量、股本不太小
            rows = [r for r in rows
                    if str(r.get("stock_id","")).isdigit()
                    and len(str(r.get("stock_id",""))) == 4
                    and r.get("Trading_Volume", 0) > 500000
                    and r.get("open", 0) > 0]
            if not rows:
                continue
            # 計算漲幅
            for r in rows:
                try:
                    r["change_pct"] = round(
                        (r["close"] - r["open"]) / r["open"] * 100, 2)
                except Exception:
                    r["change_pct"] = 0
            # 排序取前 limit 名
            top = sorted(rows, key=lambda r: r["change_pct"], reverse=True)[:limit]
            # 補上股名
            all_info = get_all_stock_info()
            name_map = {s["stock_id"]: s.get("stock_name","") for s in all_info}
            result = [{
                "stock_id": r["stock_id"],
                "stock_name": name_map.get(r["stock_id"], ""),
                "close": r["close"],
                "change_pct": r["change_pct"],
            } for r in top]
            return {"date": target, "gainers": result}
        except Exception as e:
            print(f"top_gainers 嘗試 {target} 失敗：{e}")
            continue

    # 全部失敗，回傳預設清單
    fallback = [
        {"stock_id":"2330","stock_name":"台積電","close":0,"change_pct":0},
        {"stock_id":"2317","stock_name":"鴻海","close":0,"change_pct":0},
        {"stock_id":"2454","stock_name":"聯發科","close":0,"change_pct":0},
        {"stock_id":"2308","stock_name":"台達電","close":0,"change_pct":0},
        {"stock_id":"2412","stock_name":"中華電","close":0,"change_pct":0},
        {"stock_id":"2882","stock_name":"國泰金","close":0,"change_pct":0},
        {"stock_id":"3008","stock_name":"大立光","close":0,"change_pct":0},
    ]
    return {"date": "", "gainers": fallback}


@app.get("/api/quote/{stock_id}")
def get_quote(stock_id: str, user: dict | None = Depends(get_current_user)):
    """
    即時報價（公開 endpoint，不需登入）
    盤中：tick_snapshot > Yahoo chart > TWSE z > FinMind 今日收盤
    盤後：FinMind 今日收盤 > TWSE z > STOCK_DAY > TWSE y（昨收）
    """
    import urllib.request, json as _json
    from datetime import datetime, time as dtime, date as _date
    from zoneinfo import ZoneInfo

    code = stock_id.strip().replace(".TW", "").replace(".TWO", "")

    tz = ZoneInfo("Asia/Taipei")
    now = datetime.now(tz)
    is_weekday = now.weekday() < 5
    in_session       = is_weekday and dtime(9, 0)  <= now.time() <= dtime(13, 30)
    just_after_close = is_weekday and dtime(13, 30) < now.time() <= dtime(14, 0)

    def _twse_fetch(ex: str):
        url = (f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
               f"?ex_ch={ex}_{code}.tw&json=1&delay=0")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            return _json.loads(resp.read())

    # ── 1. tick_snapshot（盤中 or 剛收盤 13:30–14:00）──
    snap_price = snap_open = snap_high = snap_low = snap_vol = None
    if in_session or just_after_close:
        try:
            snap_url = (f"https://api.finmindtrade.com/api/v4/taiwan_stock_tick_snapshot"
                        f"?data_id={code}&token={FINMIND_TOKEN}")
            snap_req = urllib.request.Request(snap_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(snap_req, timeout=6) as sr:
                snap = _json.loads(sr.read())
            snap_rows = snap.get("data", [])
            if snap_rows:
                r = snap_rows[0]
                cp = float(r.get("close") or r.get("price") or 0)
                if cp > 0:
                    snap_price = cp
                    snap_open  = float(r.get("open")  or cp) or None
                    snap_high  = float(r.get("high")  or cp) or None
                    snap_low   = float(r.get("low")   or cp) or None
                    snap_vol   = float(r.get("total_volume") or r.get("volume") or 0) or None
        except Exception as _e:
            if not (hasattr(_e, 'code') and _e.code == 400):
                print(f"[QUOTE] tick_snapshot 失敗 {code}：{_e}")

    # ── 1.5 Yahoo Finance chart API（snap 失敗時備援）──
    yf_price = yf_open = yf_high = yf_low = None
    if snap_price is None and (in_session or just_after_close):
        try:
            _sym = resolve_symbol(code)
            _yf_url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{_sym}"
                       f"?interval=1d&range=2d")
            _yf_req = urllib.request.Request(_yf_url, headers={
                "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/121.0.0.0 Safari/537.36"),
                "Accept": "application/json",
            })
            with urllib.request.urlopen(_yf_req, timeout=8) as _yr:
                _yd = _json.loads(_yr.read())
            _ym = _yd.get("chart", {}).get("result", [{}])[0].get("meta", {})
            _lp = float(_ym.get("regularMarketPrice") or 0)
            if _lp > 0:
                yf_price = _lp
                yf_open  = float(_ym.get("regularMarketOpen")    or _lp) or None
                yf_high  = float(_ym.get("regularMarketDayHigh") or _lp) or None
                yf_low   = float(_ym.get("regularMarketDayLow")  or _lp) or None
                print(f"[QUOTE] {code} Yahoo chart: price={yf_price} h={yf_high} l={yf_low}")
        except Exception as _ye:
            print(f"[QUOTE] Yahoo chart 失敗 {code}：{_ye}")

    # ── 2. TWSE MIS（z 現價、y 昨收、OHLV 備用）──
    twse_data = None
    for ex in ("tse", "otc"):
        try:
            resp = _twse_fetch(ex)
            arr = resp.get("msgArray", [])
            if arr:
                z_raw = str(arr[0].get("z", "-")).strip()
                if z_raw not in ("-", ""):
                    twse_data = arr[0]
                    break
                if not twse_data:
                    twse_data = arr[0]
        except Exception:
            continue

    def _val(k):
        v = str(twse_data.get(k, "-")).strip() if twse_data else "-"
        return None if v in ("-", "") else v

    z         = _val("z")
    y         = _val("y")
    open_twse = _val("o")
    high_twse = _val("h")
    low_twse  = _val("l")
    vol_twse  = _val("v")
    tick_time = _val("t") or ""

    # debug: 印出 TWSE raw 欄位（輔助排查 z 欄位是否為空）
    if code == "2330":
        print(f"[QUOTE-DEBUG 2330] is_weekday={is_weekday} in_session={in_session} "
              f"just_after={just_after_close} | twse z_raw={str(twse_data.get('z','-') if twse_data else 'N/A')} "
              f"y={str(twse_data.get('y','-') if twse_data else 'N/A')} | snap_price={snap_price}")

    # ── 3. FinMind 今日收盤（snap 失敗 or 盤後 fallback）──
    finmind_close = None
    if snap_price is None:
        try:
            today_str = _date.today().strftime("%Y-%m-%d")
            fm_url = (f"https://api.finmindtrade.com/api/v4/data"
                      f"?dataset=TaiwanStockPrice&data_id={code}"
                      f"&start_date={today_str}&end_date={today_str}&token={FINMIND_TOKEN}")
            fm_req = urllib.request.Request(fm_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(fm_req, timeout=8) as fr:
                fm_raw = _json.loads(fr.read())
            fm_rows = fm_raw.get("data", [])
            if fm_rows:
                finmind_close = float(fm_rows[-1].get("close") or 0) or None
        except Exception as _e:
            print(f"[QUOTE] FinMind 今日收盤失敗 {code}：{_e}")

    # ── 4. TWSE / TPEX STOCK_DAY（盤後補今日收盤，前三者均無效時）──
    stock_day_close = None
    _today_obj = _date.today()
    _is_after_close = is_weekday and now.time() >= dtime(13, 35)
    if snap_price is None and finmind_close is None and not z and _is_after_close:
        _roc_y    = _today_obj.year - 1911
        _roc_date = f"{_roc_y}/{_today_obj.month:02d}/{_today_obj.day:02d}"
        _yyyymmdd = _today_obj.strftime("%Y%m%d")
        _is_otc   = _market_cache.get(code, "") in ("otc", "rotc")
        if not _is_otc:
            # 上市：TWSE STOCK_DAY
            try:
                _sd_url = (f"https://www.twse.com.tw/exchangeReport/STOCK_DAY"
                           f"?response=json&date={_yyyymmdd}&stockNo={code}")
                _sd_req = urllib.request.Request(_sd_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(_sd_req, timeout=8) as _sd:
                    _sd_raw = _json.loads(_sd.read())
                for _row in _sd_raw.get("data", []):
                    if str(_row[0]).strip() == _roc_date:
                        _cp = str(_row[6]).replace(",", "").strip()
                        if _cp not in ("--", "", "X"):
                            stock_day_close = float(_cp)
                        break
            except Exception:
                pass
        else:
            # 上櫃：TPEX st43
            try:
                _tpex_d = f"{_roc_y}/{_today_obj.month:02d}"
                _tpex_url = (f"https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info"
                             f"/st43_result.php?l=zh-tw&d={_tpex_d}&stkno={code}")
                _tpex_req = urllib.request.Request(_tpex_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(_tpex_req, timeout=8) as _pr:
                    _tpex_raw = _json.loads(_pr.read())
                for _row in _tpex_raw.get("aaData", []):
                    if str(_row[0]).strip() == _roc_date:
                        _cp = str(_row[6]).replace(",", "").strip()
                        if _cp not in ("--", "", "X"):
                            stock_day_close = float(_cp)
                        break
            except Exception:
                pass
        if stock_day_close:
            print(f"[QUOTE] {code} STOCK_DAY 補今日收盤：{stock_day_close}")

    # ── 決定現價與來源 ──
    if in_session or just_after_close:
        if snap_price:  # FinMind tick_snapshot（最優先）
            price_val    = snap_price
            price_source = "tick_snapshot"
            open_val = snap_open  or safe_float(open_twse)
            high_val = snap_high  or safe_float(high_twse)
            low_val  = snap_low   or safe_float(low_twse)
            vol_val  = int(snap_vol) if snap_vol else (int(float(vol_twse) * 1000) if vol_twse else None)
        elif yf_price:  # Yahoo Finance chart API（備援）
            price_val    = yf_price
            price_source = "yahoo_chart"
            open_val = yf_open or safe_float(open_twse)
            high_val = yf_high or safe_float(high_twse)
            low_val  = yf_low  or safe_float(low_twse)
            vol_val  = int(float(vol_twse) * 1000) if vol_twse else None
        elif z:  # TWSE MIS z（有時為 "-"，第三選擇）
            price_val    = safe_float(z)
            price_source = "twse_z"
            open_val = safe_float(open_twse)
            high_val = safe_float(high_twse)
            low_val  = safe_float(low_twse)
            vol_val  = int(float(vol_twse) * 1000) if vol_twse else None
        elif finmind_close:
            price_val    = finmind_close
            price_source = "finmind_close"
            open_val = safe_float(open_twse)
            high_val = safe_float(high_twse)
            low_val  = safe_float(low_twse)
            vol_val  = int(float(vol_twse) * 1000) if vol_twse else None
        elif y:
            price_val    = safe_float(y)
            price_source = "twse_y"
            open_val = safe_float(open_twse)
            high_val = safe_float(high_twse)
            low_val  = safe_float(low_twse)
            vol_val  = int(float(vol_twse) * 1000) if vol_twse else None
        else:
            price_val    = None
            price_source = "none"
            open_val = high_val = low_val = vol_val = None
    else:  # 盤後：finmind_close > twse_z > stock_day > twse_y（昨收）
        if finmind_close:
            price_val    = finmind_close
            price_source = "finmind_close"
        elif z:  # TWSE MIS z 剛收盤後仍有效（約收盤後 30 分鐘內）
            price_val    = safe_float(z)
            price_source = "twse_z"
        elif stock_day_close:  # TWSE/TPEX STOCK_DAY 月報 → 最可靠的盤後收盤
            price_val    = stock_day_close
            price_source = "stock_day"
        elif y:
            price_val    = safe_float(y)
            price_source = "twse_y"
        else:
            price_val    = None
            price_source = "none"
        open_val = safe_float(open_twse)
        high_val = safe_float(high_twse)
        low_val  = safe_float(low_twse)
        vol_val  = int(float(vol_twse) * 1000) if vol_twse else None

    # ── 漲跌幅（以昨收 y 為基準）──
    change = change_pct = None
    ref = safe_float(y)
    if price_val and ref:
        try:
            change     = round(price_val - ref, 2)
            change_pct = round(change / ref * 100, 2)
        except Exception:
            pass

    print(f"[QUOTE] {code} | {now.strftime('%Y-%m-%d %H:%M:%S %a')} "
          f"| in_session={in_session} just_after={just_after_close} "
          f"| snap={snap_price} z={z} y={y} fm_close={finmind_close} "
          f"| price={price_val} source={price_source}")

    return {
        "stock_id":     code,
        "price":        price_val,
        "change":       change,
        "change_pct":   change_pct,
        "open":         open_val,
        "high":         high_val,
        "low":          low_val,
        "volume":       vol_val,
        "time":         tick_time,
        "is_trading":   bool((snap_price or yf_price or z) and in_session),
        "in_session":   in_session,
        "price_source": price_source,
        "price_note":   "以昨收價計算" if price_source == "twse_y" else None,
    }






# ══════════════════════════════════════════════════════════
# 管理者端點
# ══════════════════════════════════════════════════════════

def _check_admin(key: str):
    """驗證管理者 key = JWT_SECRET 前 16 碼"""
    if key != JWT_SECRET[:16]:
        raise HTTPException(status_code=403, detail="無權限")

@app.get("/admin/backup-db")
def backup_db(key: str = ""):
    """下載 members.db 備份，key = JWT_SECRET 前16碼"""
    from fastapi.responses import FileResponse
    _check_admin(key)
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=404, detail="資料庫不存在")
    from datetime import date
    filename = f"members_backup_{date.today().isoformat()}.db"
    return FileResponse(DB_PATH, media_type="application/octet-stream", filename=filename)


@app.get("/admin/members")
def admin_list_members(key: str = ""):
    """列出所有會員"""
    _check_admin(key)
    conn = _db_conn()
    rows = conn.execute(
        "SELECT id, email, plan, expire_at, created_at, last_login FROM members ORDER BY id DESC"
    ).fetchall()
    conn.close()
    today = _date_cls.today().isoformat()
    members = []
    for r in rows:
        d = dict(r)
        if d["plan"] == "free":
            d["is_active"] = True
        elif d["expire_at"]:
            d["is_active"] = d["expire_at"] >= today
        else:
            d["is_active"] = False
        members.append(d)
    return {"total": len(members), "members": members}


@app.post("/admin/grant")
def admin_grant(key: str = "", email: str = "", plan: str = "monthly", days: int = 30):
    """
    手動開通或延長會員
    plan: free / monthly / quarterly / yearly
    使用方式：POST /admin/grant?key=xxx&email=xxx&plan=monthly&days=30
    """
    _check_admin(key)
    email = email.strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="請填 email")

    from datetime import date, timedelta, datetime
    new_expire = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")

    conn = _db_conn()
    row = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()
    if row:
        conn.execute(
            "UPDATE members SET plan=?, expire_at=?, token_ver=token_ver+1 WHERE email=?",
            (plan, new_expire, email)
        )
        conn.commit()
        conn.close()
        return {"ok": True, "action": "updated", "email": email, "plan": plan, "expire_at": new_expire}
    else:
        # 新帳號，自動產生密碼
        password = secrets.token_urlsafe(8)
        conn.execute(
            "INSERT INTO members (email, password, plan, expire_at) VALUES (?, ?, ?, ?)",
            (email, _hash_pw(password), plan, new_expire)
        )
        conn.commit()
        conn.close()
        return {"ok": True, "action": "created", "email": email, "password": password, "plan": plan, "expire_at": new_expire}


@app.post("/admin/reset-password")
def admin_reset_password(key: str = "", email: str = ""):
    """重設某用戶密碼，回傳新密碼"""
    _check_admin(key)
    email = email.strip().lower()
    conn = _db_conn()
    row = conn.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="找不到此用戶")
    new_pw = secrets.token_urlsafe(8)
    conn.execute(
        "UPDATE members SET password=?, token_ver=token_ver+1 WHERE email=?",
        (_hash_pw(new_pw), email)
    )
    conn.commit()
    conn.close()
    try:
        _send_email(email, "線上有位 — 密碼已重設",
            f"""<div style="font-family:-apple-system,sans-serif;max-width:480px;margin:0 auto;padding:24px">
              <h2 style="color:#1D9E75">密碼已重設</h2>
              <p>您的帳號密碼已由管理員重設。</p>
              <p>新密碼：<strong style="font-size:18px;letter-spacing:2px">{new_pw}</strong></p>
              <p>請儘快登入後自行修改密碼。</p>
              <p style="font-size:12px;color:#888">若您未申請重設，請聯絡客服。</p>
            </div>"""
        )
    except Exception as _e:
        print(f"[admin_reset] 寄信失敗: {_e}")
    return {"ok": True, "email": email, "new_password": new_pw}


class _DeleteMemberReq(BaseModel):
    email: str = ""

@app.post("/admin/delete-member")
def admin_delete_member(req: _DeleteMemberReq, key: str = ""):
    """刪除會員帳號"""
    _check_admin(key)
    email = req.email.strip().lower()
    conn = _db_conn()
    conn.execute("DELETE FROM members WHERE email=?", (email,))
    conn.commit()
    conn.close()
    return {"ok": True, "deleted": email}

@app.post("/admin/run-scan")
def admin_run_scan(key: str = ""):
    """手動觸發統合選股排程（後台執行，不等結果）"""
    _check_admin(key)
    import threading, sys as _sys
    _picker_path = os.path.join(os.path.dirname(__file__), "stock_picker")
    def _do():
        try:
            if _picker_path not in _sys.path:
                _sys.path.insert(0, _picker_path)
            from main_picker import run_unified_scan
            run_unified_scan()
            print("   ✅ 手動選股排程完成")
        except Exception as e:
            print(f"   ❌ 手動選股排程失敗：{e}")
    threading.Thread(target=_do, daemon=True).start()
    return {"ok": True, "message": "選股排程已觸發，後台執行中，約 5~10 分鐘完成"}


class _BatchUpgradeReq(BaseModel):
    emails: list
    plan: str = "monthly"
    days: int = 30


@app.post("/admin/batch-upgrade")
def admin_batch_upgrade(req: _BatchUpgradeReq, key: str = ""):
    """批次升級免費會員（升級+寄通知信）"""
    _check_admin(key)
    from datetime import datetime, timedelta
    plan_label = {"monthly": "月費方案", "quarterly": "季費方案", "yearly": "年費方案"}.get(req.plan, req.plan)
    results = []
    for raw_email in req.emails:
        email = raw_email.strip().lower()
        if not email:
            continue
        new_expire = (datetime.today() + timedelta(days=req.days)).strftime("%Y-%m-%d")
        conn = _db_conn()
        try:
            row = conn.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()
            if not row:
                conn.close()
                results.append({"email": email, "ok": False, "reason": "帳號不存在"})
                continue
            conn.execute(
                "UPDATE members SET plan=?, expire_at=?, token_ver=token_ver+1 WHERE email=?",
                (req.plan, new_expire, email)
            )
            conn.commit()
        except Exception as e:
            conn.close()
            results.append({"email": email, "ok": False, "reason": str(e)})
            continue
        conn.close()
        email_sent = False
        try:
            _send_email(email, "【線上有位】🎁 早鳥優惠！您的帳號已免費升級",
                f"""<div style="font-family:-apple-system,sans-serif;max-width:560px;margin:0 auto;padding:24px">
                  <div style="text-align:center;margin-bottom:24px">
                    <h1 style="font-size:24px;color:#1D9E75;margin:0">線上<span style="color:#333">有位</span></h1>
                    <p style="color:#666;font-size:13px;margin:4px 0 0">台股技術分析輔助系統</p>
                  </div>
                  <div style="background:#f0fdf4;border-radius:12px;padding:24px;margin-bottom:20px;border:1px solid #86efac">
                    <h2 style="margin:0 0 16px;font-size:18px;color:#166534">🎁 恭喜！您已獲得早鳥免費升級</h2>
                    <p style="color:#555;margin:0 0 16px">感謝您支持線上有位！作為早期用戶，我們為您免費升級了付費方案，讓您體驗完整功能。</p>
                    <table style="width:100%;border-collapse:collapse">
                      <tr><td style="padding:8px 0;color:#888;font-size:13px;width:80px">方案</td><td style="padding:8px 0;font-weight:700;color:#333">{plan_label}</td></tr>
                      <tr><td style="padding:8px 0;color:#888;font-size:13px">到期日</td><td style="padding:8px 0;font-weight:700;color:#333">{new_expire}</td></tr>
                      <tr><td style="padding:8px 0;color:#888;font-size:13px">帳號</td><td style="padding:8px 0;font-weight:700;color:#333">{email}</td></tr>
                    </table>
                  </div>
                  <div style="text-align:center;margin-bottom:20px">
                    <a href="https://softglow-ai.com" style="background:#1D9E75;color:#fff;padding:12px 32px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px">立即登入使用</a>
                  </div>
                  <div style="border-top:1px solid #e5e7eb;padding-top:16px;text-align:center;color:#9ca3af;font-size:12px">
                    <p style="margin:0">如有問題請聯繫：<a href="mailto:watione@yahoo.com.tw" style="color:#1D9E75">watione@yahoo.com.tw</a></p>
                    <p style="margin:4px 0 0">線上有位 © 2026</p>
                  </div>
                </div>"""
            )
            email_sent = True
        except Exception:
            pass
        results.append({"email": email, "ok": True, "expire_at": new_expire, "email_sent": email_sent})
    return {"ok": True, "total": len(req.emails), "success": sum(1 for r in results if r.get("ok")), "results": results}


_HOT_STOCKS = [
    "2330","2317","2454","2308","2412","6505","2882","2881","2886","2891",
    "2884","2892","2883","2885","2887","2888","2890","5880","2801","2002",
    "1301","1303","1326","2303","2357","2382","2395","3034","3037","3045",
    "4904","4938","5871","6415","6669","2610","2618","2615","2603","2609",
    "1216","2912","2207","1101","1102","3008","6488","6770","3661",
]


@app.post("/admin/prebuild-reports")
def admin_prebuild_reports(key: str = ""):
    """批次預建熱門股報告頁（後台執行，SEO 用）"""
    _check_admin(key)
    import threading
    def _do():
        report_date = _taipei_today()
        ok_cnt, fail_cnt = 0, 0
        for sid in _HOT_STOCKS:
            try:
                conn = _db_conn()
                cached = conn.execute(
                    "SELECT id FROM stock_reports WHERE stock_id=? AND report_date=?",
                    (sid, report_date)
                ).fetchone()
                conn.close()
                if cached:
                    ok_cnt += 1
                    continue
                d = _do_analyze(sid, "D", user=None)
                stock_name = d.get("stock_name", sid)
                news_items = _fetch_stock_news(sid)
                html = _build_report_html(sid, stock_name, report_date, d, news_items)
                conn = _db_conn()
                conn.execute(
                    "INSERT OR REPLACE INTO stock_reports (stock_id, report_date, stock_name, report_html) VALUES (?,?,?,?)",
                    (sid, report_date, stock_name, html)
                )
                conn.commit()
                conn.close()
                ok_cnt += 1
                print(f"   ✅ 預建報告：{sid}")
            except Exception as e:
                fail_cnt += 1
                print(f"   ❌ 預建報告失敗 {sid}：{e}")
        print(f"   ✅ 熱門報告預建完成，成功 {ok_cnt}，失敗 {fail_cnt}")
    threading.Thread(target=_do, daemon=True).start()
    return {"ok": True, "total": len(_HOT_STOCKS), "message": f"已啟動預建 {len(_HOT_STOCKS)} 支熱門股報告，後台處理中..."}


def _record_visit(ip: str):
    today = _date_cls.today().isoformat()
    conn = _db_conn()
    conn.execute("INSERT OR IGNORE INTO visits (ip, date) VALUES (?, ?)", (ip, today))
    conn.commit()
    conn.close()

@app.get("/api/stats")
def api_stats():
    conn = _db_conn()
    visit_count = conn.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
    query_count = conn.execute("SELECT COALESCE(SUM(count), 0) FROM query_log").fetchone()[0]
    conn.close()
    return {"visit_count": int(visit_count), "query_count": int(query_count)}

@app.get("/")
def root():
    return {"status": "ok", "app": "線上有位 API", "version": "1.3.0"}


# ── 批次分析端點（關注頁用）──
from pydantic import BaseModel as _BaseModel
from typing import List as _List
import asyncio as _asyncio
from concurrent.futures import ThreadPoolExecutor as _ThreadPoolExecutor

class BatchRequest(_BaseModel):
    ids: _List[str]
    tf: str = "D"

@app.post("/batch_analyze")
def batch_analyze(req: BatchRequest, user: dict = Depends(require_user)):
    """
    批次分析多檔股票，回傳 {股票代號: 分析結果} 的 dict
    每檔獨立處理，單一失敗不影響其他，最多並發 5 個
    """
    tf = req.tf.upper()
    ids = [i.strip().upper() for i in req.ids if i.strip()][:30]  # 最多30檔

    def _analyze_one(stock_id):
        try:
            # 複用快取
            _cache_key = f"{stock_id}_{tf}"
            cached = _cache_get(_cache_key)
            if cached:
                # 只回傳前端需要的欄位，減少傳輸量
                return stock_id, _slim(cached)
            # 未快取則查詢
            result = _do_analyze(stock_id, tf, user=user)
            return stock_id, _slim(result)
        except Exception as e:
            print(f"batch_analyze {stock_id} 失敗：{e}")
            return stock_id, None

    def _slim(d):
        """只保留關注頁卡片需要的欄位"""
        if not d:
            return None
        # 從 summary 組出一行結論（取第一、二行）
        summary = d.get("summary", [])
        conclusion = "、".join(summary[:2]) if summary else ""
        # volume_ratio：取最近一根成交量 / 20日均量
        bars = d.get("bars", [])
        volume_ratio = None
        if bars and len(bars) >= 20:
            recent_vol = bars[-1].get("volume", 0) or 0
            avg_vol = sum(b.get("volume", 0) or 0 for b in bars[-20:]) / 20
            volume_ratio = round(recent_vol / avg_vol, 2) if avg_vol > 0 else None
        return {
            "price":        d.get("price"),
            "support":      d.get("support"),
            "resistance":   d.get("resistance"),
            "trend":        d.get("trend"),
            "pattern":      d.get("pattern"),
            "risk_level":   d.get("risk_level"),
            "risk_label":   d.get("risk_label"),
            "risk_color":   d.get("risk_color"),
            "conclusion":   conclusion,
            "rr_ratio":     d.get("risk_reward"),   # 正確 key
            "rr_basis":     d.get("rr_basis"),
            "stop_loss":    d.get("stop_loss"),
            "today_breakout": d.get("today_breakout"),
            "near_top":     d.get("near_top"),
            "near_bot":     d.get("near_bot"),
            "kbar_dir":     d.get("kbar_dir"),
            "volume_ratio": volume_ratio,
        }

    results = {}
    with _ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(_analyze_one, sid): sid for sid in ids}
        for fut in futures:
            sid, val = fut.result()
            results[sid] = val

    return results


# ── FinMind 股票資料快取 ──
_stock_info_cache: list = []
_stock_info_ts: float = 0.0

def get_all_stock_info() -> list:
    """取得全台股基本資料（帶快取，每天更新一次）"""
    import time
    global _stock_info_cache, _stock_info_ts
    if _stock_info_cache and (time.time() - _stock_info_ts) < 86400:
        return _stock_info_cache
    try:
        import urllib.request, json as _json
        url = (f"https://api.finmindtrade.com/api/v4/data"
               f"?dataset=TaiwanStockInfo&token={FINMIND_TOKEN}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = _json.loads(resp.read())
        if data.get("status") == 200:
            _stock_info_cache = data.get("data", [])
            _stock_info_ts = time.time()
    except Exception as e:
        print(f"FinMind StockInfo 失敗：{e}")
    return _stock_info_cache



@app.get("/api/search")
def search_stock(q: str, limit: int = 10, user: dict = Depends(require_user)):
    """
    股票搜尋：支援代號（2330）或中文名稱（台積電、律勝）
    回傳最多 limit 筆匹配結果
    """
    q = q.strip()
    if not q:
        return {"results": []}

    all_stocks = get_all_stock_info()

    # 先用 STOCK_NAMES 對照表補充（確保常用股都查得到）
    static_map = {v: k for k, v in STOCK_NAMES.items()}  # 名稱 → 代號

    results = []
    q_lower = q.lower()

    # 1. 完全匹配代號（最高優先）
    exact = [s for s in all_stocks
             if str(s.get("stock_id","")).lower() == q_lower]

    # 2. 代號前綴匹配（如輸入 "235"）
    prefix_id = [s for s in all_stocks
                 if str(s.get("stock_id","")).startswith(q)
                 and str(s.get("stock_id","")).lower() != q_lower]

    # 3. 名稱包含關鍵字
    name_match = [s for s in all_stocks
                  if q in str(s.get("stock_name",""))
                  and str(s.get("stock_id","")).lower() != q_lower]

    # 合併去重，只取4碼純數字股票（排除ETF代號過長）
    seen = set()
    for s in exact + prefix_id + name_match:
        sid = str(s.get("stock_id",""))
        if sid in seen:
            continue
        if not sid.isdigit() or len(sid) not in (4, 5, 6):
            continue
        seen.add(sid)
        results.append({
            "stock_id":   sid,
            "stock_name": s.get("stock_name",""),
            "type":       s.get("type",""),
        })
        if len(results) >= limit:
            break

    # fallback：若 FinMind 沒資料，用靜態對照表
    if not results:
        for name, sid in static_map.items():
            if q in name or q in sid:
                results.append({"stock_id": sid, "stock_name": name, "type": ""})
        results = results[:limit]

    return {"query": q, "results": results}


@app.get("/api/peers/{stock_id}")
def get_peers(stock_id: str, limit: int = 15, user: dict = Depends(require_user)):
    """同產業個股列表"""
    code = stock_id.strip().replace(".TW", "").replace(".TWO", "")
    all_stocks = get_all_stock_info()
    if not all_stocks:
        raise HTTPException(status_code=503, detail="FinMind 資料暫時無法取得")

    # 找自己的產業
    this = next((s for s in all_stocks if s.get("stock_id") == code), None)
    if not this or not this.get("industry_category"):
        raise HTTPException(status_code=404, detail=f"找不到 {code} 的產業資料")

    industry = this["industry_category"]

    # 同產業（排除自己，只取4碼純數字股票，避免ETF/權證）
    peers = [
        {"stock_id": s["stock_id"], "stock_name": s.get("stock_name", ""),
         "type": s.get("type", "")}
        for s in all_stocks
        if s.get("industry_category") == industry
        and s.get("stock_id") != code
        and str(s.get("stock_id", "")).isdigit()
        and len(str(s.get("stock_id", ""))) == 4
    ][:limit]

    return {
        "stock_id": code,
        "industry": industry,
        "peers": peers,
        "count": len(peers),
    }




def detect_kbar_pattern(opens, highs, lows, closes):
    """
    辨識最近 K 棒型態（單根/兩根/三根）
    回傳：
      kbar_pattern: str  已確認的型態名稱（空字串=無）
      kbar_warning: str  預警文字（明天若...將形成...）
    """
    n = len(closes)
    if n < 3:
        return "", "", "neutral"

    o1,h1,l1,c1 = opens[-1],highs[-1],lows[-1],closes[-1]  # 最新根
    o2,h2,l2,c2 = opens[-2],highs[-2],lows[-2],closes[-2]  # 前一根
    o3,h3,l3,c3 = opens[-3],highs[-3],lows[-3],closes[-3]  # 前兩根

    body1 = abs(c1 - o1)
    body2 = abs(c2 - o2)
    body3 = abs(c3 - o3)
    range1 = h1 - l1 or 0.001
    range2 = h2 - l2 or 0.001
    range3 = h3 - l3 or 0.001

    upper_shadow1 = h1 - max(o1, c1)
    lower_shadow1 = min(o1, c1) - l1
    upper_shadow2 = h2 - max(o2, c2)
    lower_shadow2 = min(o2, c2) - l2

    is_red1 = c1 > o1
    is_red2 = c2 > o2
    is_red3 = c3 > o3

    patterns = []
    warnings = []

    # ── 單根型態（最新K棒）──

    # 錘頭（底部，下引線長，出現在下跌後）
    if (lower_shadow1 >= body1 * 2 and upper_shadow1 <= body1 * 0.3
            and body1 / range1 < 0.4):
        if not is_red1:
            patterns.append("錘頭線（底部反轉訊號）")
            warnings.append("出現錘頭線，若明天收紅確認，底部支撐訊號成立")
        else:
            patterns.append("錘頭線（底部反轉，紅K更佳）")
            warnings.append("出現紅K錘頭線，底部支撐訊號，明天若繼續收紅則確認")

    # 流星/射擊之星（頂部，上引線長）
    elif (upper_shadow1 >= body1 * 2 and lower_shadow1 <= body1 * 0.3
            and body1 / range1 < 0.4):
        patterns.append("射擊之星（頂部壓力訊號）")
        warnings.append("出現射擊之星，若明天收黑確認，注意頂部形成風險")

    # 十字星（開收盤接近）
    elif body1 / range1 < 0.1 and range1 > 0:
        if h1 > max(h2, h3):  # 高點在頂部
            patterns.append("十字星（高點出現，方向未定）")
            warnings.append("高點出現十字星，方向未明，明天若收黑須注意拉回")
        else:
            patterns.append("十字星（整理，等待方向）")
            warnings.append("出現十字星，整理中，等待明天方向確認")

    # 大紅棒（強攻）
    elif is_red1 and body1 / range1 > 0.7 and body1 > body2 * 1.5:
        patterns.append("大紅棒（強勢攻擊）")
        warnings.append("出現大紅棒，若明天不跌破今日一半，多頭強勢延續")

    # 大黑棒（強殺）
    elif not is_red1 and body1 / range1 > 0.7 and body1 > body2 * 1.5:
        patterns.append("大黑棒（強勢賣壓）")
        warnings.append("出現大黑棒，若明天無法收復今日一半，空頭延續")

    # ── 兩根型態 ──

    # 多頭吞噬（紅吞黑）
    if (is_red1 and not is_red2
            and o1 <= c2 and c1 >= o2
            and body1 > body2):
        patterns.append("多頭吞噬（底部反轉）")
        warnings.append("出現多頭吞噬，明天若繼續收紅，底部反轉確認")

    # 空頭吞噬（黑吞紅）
    elif (not is_red1 and is_red2
            and o1 >= c2 and c1 <= o2
            and body1 > body2):
        patterns.append("空頭吞噬（頂部反轉）")
        warnings.append("出現空頭吞噬，明天若繼續收黑，頂部反轉確認")

    # 孕線（母子）
    elif (body2 > body1 * 2
            and max(o1,c1) < max(o2,c2)
            and min(o1,c1) > min(o2,c2)):
        if is_red2:
            patterns.append("孕線（多頭孕線，整理後可能續漲）")
            warnings.append("出現多頭孕線，若明天收紅突破母線高點，多頭延續")
        else:
            patterns.append("孕線（空頭孕線，整理後可能續跌）")
            warnings.append("出現空頭孕線，若明天收黑跌破母線低點，空頭延續")

    # 穿刺線（黑後紅，收超過前根中段）
    elif (is_red1 and not is_red2
            and o1 < l2
            and c1 > (o2 + c2) / 2
            and c1 < o2):
        patterns.append("穿刺線（底部潛在反轉）")
        warnings.append("出現穿刺線，明天若繼續收紅，底部反轉訊號增強")

    # 烏雲蓋頂（紅後黑，收超過前根中段）
    elif (not is_red1 and is_red2
            and o1 > h2
            and c1 < (o2 + c2) / 2
            and c1 > o2):
        patterns.append("烏雲蓋頂（頂部潛在反轉）")
        warnings.append("出現烏雲蓋頂，明天若繼續收黑，頂部反轉訊號增強")

    # ── 三根型態 ──

    # 早晨之星（底部反轉：黑棒+小實體+紅棒）
    if (not is_red3 and body3 > range3 * 0.4
            and body2 < range2 * 0.3
            and is_red1 and c1 > (o3 + c3) / 2):
        patterns.append("早晨之星（底部強力反轉）")
        warnings.append("出現早晨之星，底部反轉訊號，明天若繼續收紅則強力確認")

    # 黃昏之星（頂部反轉：紅棒+小實體+黑棒）
    elif (is_red3 and body3 > range3 * 0.4
            and body2 < range2 * 0.3
            and not is_red1 and c1 < (o3 + c3) / 2):
        patterns.append("黃昏之星（頂部強力反轉）")
        warnings.append("出現黃昏之星，頂部反轉訊號，若明天繼續收黑須注意出場")

    # 三紅兵（強勢延續）
    elif (is_red1 and is_red2 and is_red3
            and c1 > c2 > c3
            and body1 > range1 * 0.5
            and body2 > range2 * 0.5
            and body3 > range3 * 0.5):
        patterns.append("三紅兵（強勢多頭延續）")
        warnings.append("出現三紅兵，多頭趨勢強，明天若再收紅趨勢持續，注意追高風險")

    # 三烏鴉（弱勢延續）
    elif (not is_red1 and not is_red2 and not is_red3
            and c1 < c2 < c3
            and body1 > range1 * 0.5
            and body2 > range2 * 0.5
            and body3 > range3 * 0.5):
        patterns.append("三烏鴉（強勢空頭延續）")
        warnings.append("出現三烏鴉，空頭趨勢強，明天若再收黑持續下跌壓力")

    # 預警：今天+明天可能形成的型態
    if not patterns:
        # 今天是大黑棒，若明天開高收在中段以上 → 穿刺線
        if not is_red1 and body1 / range1 > 0.6:
            warnings.append("今天出現大黑棒，若明天開低後拉回收超過今日一半，將形成穿刺線（底部反轉）")
        # 今天是大紅棒，若明天開高收黑超過中段 → 烏雲蓋頂
        elif is_red1 and body1 / range1 > 0.6:
            warnings.append("今天出現大紅棒，若明天開高後反轉收黑超過今日一半，將形成烏雲蓋頂（頂部反轉）")
        # 今天是小實體（前一根是大棒）
        elif body1 < range1 * 0.3 and body2 > range2 * 0.5:
            if is_red2:
                warnings.append("出現孕線雛形（前大紅棒+今小實體），若明天收紅突破今日高點，多頭延續")
            else:
                warnings.append("出現孕線雛形（前大黑棒+今小實體），若明天收黑跌破今日低點，空頭延續")

    pattern_str = "、".join(patterns) if patterns else ""
    warning_str = warnings[0] if warnings else ""

    # 方向標記（供前端配色用）
    bullish_keys = ["錘頭","多頭吞噬","早晨之星","三紅兵","穿刺線","大紅棒","頭肩底","W底"]
    bearish_keys = ["射擊之星","空頭吞噬","黃昏之星","三烏鴉","烏雲蓋頂","大黑棒","頭肩頂","M頭"]
    kbar_dir = "bullish" if any(k in pattern_str for k in bullish_keys) \
               else "bearish" if any(k in pattern_str for k in bearish_keys) \
               else "neutral"

    return pattern_str, warning_str, kbar_dir


# ══════════════════════════════════════════════════════════
# 籌碼面 API
# ══════════════════════════════════════════════════════════
def _finmind_get(dataset: str, stock_id: str, start_date: str, end_date: str) -> list:
    """通用 FinMind 查詢"""
    import urllib.request, json as _json
    url = (f"https://api.finmindtrade.com/api/v4/data"
           f"?dataset={dataset}&data_id={stock_id}"
           f"&start_date={start_date}&end_date={end_date}"
           f"&token={FINMIND_TOKEN}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = _json.loads(resp.read())
    if data.get("status") != 200:
        return []
    return data.get("data", [])


@app.get("/api/chips/{stock_id}")
def get_chips(stock_id: str, days: int = 30, user: dict = Depends(require_user)):
    """
    籌碼面：三大法人買賣超 + 融資融券
    回傳最近 N 天資料 + 統計摘要
    """
    from datetime import date, timedelta
    code = stock_id.strip().replace(".TW", "").replace(".TWO", "")
    end   = date.today().strftime("%Y-%m-%d")
    start = (date.today() - timedelta(days=days + 10)).strftime("%Y-%m-%d")

    result = {}

    # ── 1. 三大法人 ──
    try:
        rows = _finmind_get("TaiwanStockInstitutionalInvestorsBuySell", code, start, end)
        if rows:
            # 整理成 {date: {外資,投信,自營}} 格式
            daily: dict = {}
            for r in rows:
                d = r.get("date","")[:10]
                name = r.get("name","")
                net = r.get("buy", 0) - r.get("sell", 0)
                if d not in daily:
                    daily[d] = {"foreign": 0, "invest": 0, "dealer": 0}
                name_lower = name.replace(" ","")
                if "外資" in name_lower or "Foreign" in name or "QFII" in name:
                    daily[d]["foreign"] += net
                elif "投信" in name_lower or "Investment" in name:
                    daily[d]["invest"] += net
                elif "自營" in name_lower or "Dealer" in name:
                    daily[d]["dealer"] += net

            sorted_days = sorted(daily.keys())[-days:]
            inst_list = []
            for d in sorted_days:
                v = daily[d]
                total = v["foreign"] + v["invest"] + v["dealer"]
                inst_list.append({
                    "date": d,
                    "foreign": v["foreign"],
                    "invest":  v["invest"],
                    "dealer":  v["dealer"],
                    "total":   total,
                })

            # 統計摘要（近5日、近20日）
            def summarize(lst, n):
                sub = lst[-n:]
                f = sum(r["foreign"] for r in sub)
                i = sum(r["invest"]  for r in sub)
                de= sum(r["dealer"]  for r in sub)
                return {"foreign": f, "invest": i, "dealer": de, "total": f+i+de, "days": len(sub)}

            result["institutional"] = {
                "daily":   inst_list,
                "summary_5":  summarize(inst_list, 5),
                "summary_20": summarize(inst_list, 20),
            }
    except Exception as e:
        result["institutional"] = {"error": str(e)}

    # ── 2. 融資融券 ──
    try:
        rows = _finmind_get("TaiwanStockMarginPurchaseShortSale", code, start, end)
        if rows:
            margin_list = []
            for r in sorted(rows, key=lambda x: x.get("date",""))[-days:]:
                # FinMind 欄位名稱可能有大小寫差異，使用 fallback 容錯
                def _get(row, *keys, default=0):
                    for k in keys:
                        v = row.get(k)
                        if v is not None:
                            return v
                    return default

                # 融資餘額、融券餘額
                margin_list.append({
                    "date":        r.get("date","")[:10],
                    "margin_buy":  _get(r,"MarginPurchaseBuy","margin_purchase_buy"),
                    "margin_sell": _get(r,"MarginPurchaseSell","margin_purchase_sell"),
                    "margin_bal":  _get(r,"MarginPurchaseTodayBalance","margin_purchase_today_balance","MarginPurchaseBalance"),
                    "short_buy":   _get(r,"ShortSaleBuy","short_sale_buy"),
                    "short_sell":  _get(r,"ShortSaleSell","short_sale_sell"),
                    "short_bal":   _get(r,"ShortSaleTodayBalance","short_sale_today_balance","ShortSaleBalance"),
                    "offset":      _get(r,"OffsetLoanAndShort","offset_loan_and_short"),
                })

            # 近5日融資增減
            if len(margin_list) >= 2:
                recent = margin_list[-5:]
                margin_chg = margin_list[-1]["margin_bal"] - margin_list[-min(6,len(margin_list))]["margin_bal"]
                short_chg  = margin_list[-1]["short_bal"]  - margin_list[-min(6,len(margin_list))]["short_bal"]
            else:
                margin_chg = short_chg = 0

            result["margin"] = {
                "daily":       margin_list,
                "margin_latest": margin_list[-1]["margin_bal"] if margin_list else 0,
                "short_latest":  margin_list[-1]["short_bal"]  if margin_list else 0,
                "margin_chg_5":  margin_chg,
                "short_chg_5":   short_chg,
                "_raw_fields":   list(rows[0].keys()) if rows else [],  # debug 用：顯示實際欄位名稱
            }
    except Exception as e:
        result["margin"] = {"error": str(e)}

    result["stock_id"] = code
    result["query_days"] = days
    return result






# ══════════════════════════════════════════════════════════
# 會員 API 端點
# ══════════════════════════════════════════════════════════

class LoginReq(BaseModel):
    email: str
    password: str

class RegisterReq(BaseModel):
    email: str
    password: str

class ChangePasswordReq(BaseModel):
    old_password: str
    new_password: str


@app.post("/auth/register")
def auth_register(req: RegisterReq, ref: str = "", request: Request = None):
    email = req.email.strip().lower()
    if not _re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        raise HTTPException(status_code=400, detail="Email 格式不正確")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="密碼至少 6 個字元")
    conn = _db_conn()
    try:
        conn.execute(
            "INSERT INTO members (email, password) VALUES (?, ?)",
            (email, _hash_pw(req.password))
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=409, detail="此 Email 已註冊")
    _get_or_create_referral_code(email)
    if ref:
        inviter_row = conn.execute("SELECT user_email FROM referral_codes WHERE code=?", (ref.upper().strip(),)).fetchone()
        if inviter_row and inviter_row["user_email"] != email:
            client_ip = request.client.host if request else ""
            dupe = conn.execute(
                "SELECT id FROM referral_logs WHERE invitee_email=? AND inviter_email=?",
                (email, inviter_row["user_email"])
            ).fetchone()
            if not dupe:
                conn.execute(
                    "INSERT INTO referral_logs (inviter_email, invitee_email, invitee_ip) VALUES (?,?,?)",
                    (inviter_row["user_email"], email, client_ip)
                )
                conn.commit()
    conn.close()
    return {"ok": True, "message": "註冊成功"}


@app.post("/register")
def register_free(req: RegisterReq, ref: str = "", request: Request = None):
    email = req.email.strip().lower()
    if not _re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        raise HTTPException(status_code=400, detail="Email 格式不正確")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="密碼至少 6 個字元")
    conn = _db_conn()
    try:
        conn.execute(
            "INSERT INTO members (email, password, plan) VALUES (?, ?, 'free')",
            (email, _hash_pw(req.password))
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=409, detail="此 Email 已註冊")
    _get_or_create_referral_code(email)
    if ref:
        inviter_row = conn.execute("SELECT user_email FROM referral_codes WHERE code=?", (ref.upper().strip(),)).fetchone()
        if inviter_row and inviter_row["user_email"] != email:
            client_ip = request.client.host if request else ""
            dupe = conn.execute(
                "SELECT id FROM referral_logs WHERE invitee_email=? AND inviter_email=?",
                (email, inviter_row["user_email"])
            ).fetchone()
            if not dupe:
                conn.execute(
                    "INSERT INTO referral_logs (inviter_email, invitee_email, invitee_ip) VALUES (?,?,?)",
                    (inviter_row["user_email"], email, client_ip)
                )
                conn.commit()
    conn.close()
    return {"ok": True, "message": "免費帳號建立成功"}


@app.post("/auth/login")
def auth_login(req: LoginReq):
    email = req.email.strip().lower()
    conn = _db_conn()
    row = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()
    if not row or not _verify_pw(req.password, row["password"]):
        conn.close()
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")
    blocked = conn.execute(
        "SELECT email FROM blocked_users WHERE email=? AND block_type='login'", (email,)
    ).fetchone()
    if blocked:
        conn.close()
        raise HTTPException(status_code=403, detail="帳號已被停用，請聯絡客服")
    session_id = secrets.token_hex(16)
    conn.execute("UPDATE members SET last_login=datetime('now','+8 hours'), session_id=? WHERE id=?", (session_id, row["id"]))
    conn.commit()
    conn.close()

    payload = {
        "sub": row["id"],
        "email": email,
        "plan": row["plan"],
        "ver": row["token_ver"],
        "sid": session_id,
        "exp": _time_mod.time() + JWT_EXPIRE_DAYS * 86400,
    }
    token = _jwt_create(payload)
    return {
        "token": token,
        "email": email,
        "plan": row["plan"],
        "expire_at": row["expire_at"],
    }


@app.get("/auth/me")
def auth_me(user: dict = Depends(require_user)):
    today = _date_cls.today().isoformat()
    conn = _db_conn()
    row = conn.execute(
        "SELECT count FROM query_log WHERE member_id=? AND date=?",
        (user["id"], today)
    ).fetchone()
    conn.close()
    used = row["count"] if row else 0
    plan = user["plan"]
    is_active = True
    if plan != "free" and user["expire_at"]:
        is_active = user["expire_at"] >= today
    plan_labels = {"free":"免費會員","monthly":"月費會員","quarterly":"季費會員","yearly":"年費會員","test":"測試會員"}
    plan_label  = plan_labels.get(plan, plan)
    days_left   = None
    is_expiring_soon = False
    if user["expire_at"] and plan != "free":
        try:
            delta = (datetime.fromisoformat(user["expire_at"]) - datetime.today()).days
            days_left = max(0, delta)
            is_expiring_soon = 0 <= days_left <= 3
        except Exception:
            pass
    return {
        "email": user["email"],
        "plan": plan,
        "plan_label": plan_label,
        "is_active": is_active,
        "expire_at": user["expire_at"],
        "queries_used": used,
        "queries_limit": FREE_DAILY_LIMIT if plan == "free" else 999,
        "days_left": days_left,
        "is_expiring_soon": is_expiring_soon,
        "referral_unlocked": user.get("referral_unlocked", 0),
        "referral_expire_date": user.get("referral_expire_date"),
    }


@app.post("/auth/logout")
def auth_logout(user: dict = Depends(require_user)):
    conn = _db_conn()
    conn.execute("UPDATE members SET token_ver = token_ver + 1 WHERE id=?", (user["id"],))
    conn.commit()
    conn.close()
    return {"ok": True}


@app.get("/api/referral/status")
def get_referral_status(user: dict = Depends(require_user)):
    email = user["email"]
    code = _get_or_create_referral_code(email)
    conn = _db_conn()
    completed = conn.execute(
        "SELECT COUNT(*) FROM referral_logs WHERE inviter_email=? AND status='completed'", (email,)
    ).fetchone()[0]
    exp_row = conn.execute(
        "SELECT referral_expire_date FROM members WHERE email=?", (email,)
    ).fetchone()
    conn.close()
    return {
        "code": code,
        "invite_link": f"{FRONTEND_URL}/landing.html?ref={code}",
        "completed_count": completed,
        "required_count": 3,
        "unlocked": bool(user.get("referral_unlocked", 0)),
        "referral_expire_date": exp_row["referral_expire_date"] if exp_row else None,
    }


@app.post("/auth/change-password")
def auth_change_password(req: ChangePasswordReq, user: dict = Depends(require_user)):
    if not _verify_pw(req.old_password, user["password"]):
        raise HTTPException(status_code=401, detail="舊密碼錯誤")
    if len(req.new_password) < 6:
        raise HTTPException(status_code=400, detail="新密碼至少 6 個字元")
    conn = _db_conn()
    conn.execute(
        "UPDATE members SET password=?, token_ver=token_ver+1 WHERE id=?",
        (_hash_pw(req.new_password), user["id"])
    )
    conn.commit()
    conn.close()
    return {"ok": True, "message": "密碼已更新，請重新登入"}


def _send_email(to: str, subject: str, html: str):
    """寄送 HTML 信件，失敗只 log 不 raise"""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASS:
        print(f"   ⚠️ SMTP 未設定，略過寄信 → {to}")
        return
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = SMTP_FROM
        msg["To"]      = to
        msg.attach(MIMEText(html, "html", "utf-8"))
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_FROM, [to], msg.as_string())
        print(f"   ✅ 寄信成功 → {to}：{subject}")
    except Exception as e:
        print(f"   ❌ 寄信失敗 → {to}：{e}")


def _ecpay_verify(params: dict) -> bool:
    """驗證綠界 CheckMacValue"""
    import urllib.parse, hashlib
    check_mac = params.get("CheckMacValue", "")
    filtered = {k: v for k, v in params.items() if k != "CheckMacValue"}
    sorted_params = sorted(filtered.items(), key=lambda x: x[0].lower())
    raw = "&".join(f"{k}={v}" for k, v in sorted_params)
    raw = f"HashKey={ECPAY_HASH_KEY}&{raw}&HashIV={ECPAY_HASH_IV}"
    raw = urllib.parse.quote_plus(raw).lower()
    expected = hashlib.sha256(raw.encode()).hexdigest().upper()
    return expected == check_mac.upper()


def _plan_days(item_name: str) -> int:
    """依商品名稱判斷天數"""
    if "年" in item_name:
        return 365
    elif "季" in item_name:
        return 90
    elif "測試" in item_name or "test" in item_name.lower():
        return 1
    else:
        return 30


@app.post("/pay/result")
async def pay_result(request: Request):
    """綠界 OrderResultURL（POST），驗證後 redirect 到前端結果頁"""
    from fastapi.responses import RedirectResponse
    body = await request.form()
    rtn_code = body.get("RtnCode", "0")
    if rtn_code == "1":
        return RedirectResponse(url=f"{FRONTEND_URL}/landing.html?pay=done", status_code=303)
    else:
        return RedirectResponse(url=f"{FRONTEND_URL}/landing.html?pay=fail", status_code=303)

@app.post("/create_order")
async def create_order(request: Request):
    """
    前端呼叫此端點產生綠界訂單，回傳付款網址
    Body: { email, plan }
    """
    from fastapi import Request
    import urllib.parse, hashlib, time as _t

    body = await request.json()
    email    = body.get("email", "").strip().lower()
    plan     = body.get("plan", "quarterly")
    password = body.get("password", "").strip()  # 用戶自設密碼

    if not email or not _re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        raise HTTPException(status_code=400, detail="Email 格式不正確")

    plan_info = {
        "monthly":   {"name": "線上有位月費方案", "amount": 399,  "days": 30},
        "quarterly": {"name": "線上有位季費方案", "amount": 999,  "days": 90},
        "yearly":    {"name": "線上有位年費方案", "amount": 3688, "days": 365},
        "test":      {"name": "線上有位測試方案", "amount": 6,    "days": 1},
    }
    if plan not in plan_info:
        raise HTTPException(status_code=400, detail="無效方案")

    info = plan_info[plan]
    trade_no = f"XYW{int(_t.time())}{secrets.token_hex(3).upper()}"

    params = {
        "MerchantID":        ECPAY_MERCHANT_ID,
        "MerchantTradeNo":   trade_no,
        "MerchantTradeDate": _taipei_now_str("%Y/%m/%d %H:%M:%S"),
        "PaymentType":       "aio",
        "TotalAmount":       str(info["amount"]),
        "TradeDesc":         urllib.parse.quote("線上有位訂閱"),
        "ItemName":          info["name"],
        "ReturnURL":         f"{BACKEND_URL}/webhook/ecpay",
        "OrderResultURL":    f"{BACKEND_URL}/pay/result",
        "ClientBackURL":     f"{FRONTEND_URL}/landing.html?pay=fail",
        "ChoosePayment":     "ALL",
        "EncryptType":       "1",
        "CustomField1":      email,
    }

    # 暫存密碼到 DB（後端重啟也不遺失）
    if password and len(password) >= 6:
        _po_conn = _db_conn()
        _po_conn.execute(
            "INSERT OR REPLACE INTO pending_orders "
            "(merchant_trade_no, email, hashed_password, plan) VALUES (?, ?, ?, ?)",
            (trade_no, email, _hash_pw(password), plan)
        )
        _po_conn.commit()
        _po_conn.close()

    # 產生 CheckMacValue
    sorted_params = sorted(params.items(), key=lambda x: x[0].lower())
    raw = "&".join(f"{k}={v}" for k, v in sorted_params)
    raw = f"HashKey={ECPAY_HASH_KEY}&{raw}&HashIV={ECPAY_HASH_IV}"
    raw = urllib.parse.quote_plus(raw).lower()
    check_mac = hashlib.sha256(raw.encode()).hexdigest().upper()
    params["CheckMacValue"] = check_mac

    # 建立自動提交的 HTML form（綠界不支援 GET redirect，需要 POST form）
    form_html = f"""<!DOCTYPE html><html><body>
<form id="f" method="POST" action="https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5">
{''.join(f'<input type="hidden" name="{k}" value="{v}"/>' for k,v in params.items())}
</form>
<script>document.getElementById('f').submit();</script>
</body></html>"""

    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=form_html)


@app.get("/api/picks/latest")
def get_latest_picks(request: Request, token: str = "", user: dict | None = Depends(get_current_user)):
    # 支援 ?token= query param（iframe 無法帶 Authorization header）
    if not user and token:
        payload = _jwt_verify(token)
        if payload:
            conn = _db_conn()
            row = conn.execute("SELECT * FROM members WHERE id=?", (payload["sub"],)).fetchone()
            conn.close()
            if row and row["token_ver"] == payload.get("ver", 0):
                user = dict(row)
    if not user:
        raise HTTPException(status_code=401, detail="請先登入")
    """
    選股名單：只有付費且有效的會員可以查看
    回傳最新的 stock_picker/output/latest.html
    """
    from fastapi.responses import HTMLResponse
    today = _date_cls.today().isoformat()
    plan = user["plan"]
    is_referral_unlocked = _is_referral_active(user)
    # 免費用戶無法使用（邀請解鎖視為付費）
    if plan == "free" and not is_referral_unlocked:
        raise HTTPException(status_code=403, detail="此功能需要付費方案")
    # 訂閱已到期
    if not is_referral_unlocked and user["expire_at"] and user["expire_at"] < today:
        raise HTTPException(status_code=403, detail="訂閱已到期，請續費後繼續使用")

    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker", "output", "latest.html"),
        "/app/stock_picker/output/latest.html",
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return HTMLResponse(content=f.read())

    # 尚無資料
    placeholder = """<!DOCTYPE html>
<html lang="zh-TW">
<head><meta charset="UTF-8">
<style>
body{font-family:-apple-system,sans-serif;background:#020817;color:#f1f5f9;
     display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
.box{text-align:center;padding:40px 20px}
.icon{font-size:48px;margin-bottom:16px}
.title{font-size:18px;font-weight:700;margin-bottom:8px}
.desc{font-size:13px;color:#64748b;line-height:1.6}
</style></head>
<body>
<div class="box">
  <div class="icon">🔍</div>
  <div class="title">選股名單尚未產生</div>
  <div class="desc">每個交易日 14:35 自動更新<br>請明日再回來查看</div>
</div>
</body></html>"""
    return HTMLResponse(content=placeholder)


@app.post("/webhook/ecpay")
async def webhook_ecpay(request: Request):
    body = await request.form()
    params = dict(body)
    print(f"   ECPay Webhook: {params}")

    # 驗證 MerchantID（CheckMacValue 因收款連結格式不同暫以 MerchantID 驗證）
    if params.get("MerchantID") != ECPAY_MERCHANT_ID:
        print(f"   ❌ MerchantID 不符：{params.get('MerchantID')}")
        return JSONResponse(content="0|Error")

    if params.get("RtnCode") != "1":
        return JSONResponse(content="1|OK")  # 非成功狀態，回應 OK 但不處理

    email      = params.get("CustomField1", "").strip().lower()
    trade_no_w = params.get("MerchantTradeNo", "")
    item_name  = params.get("ItemName", "")
    trade_no   = params.get("TradeNo", "")
    amount     = params.get("TradeAmt", "0")

    if not email:
        print("   ❌ CustomField1 (email) 為空")
        return JSONResponse(content="1|OK")

    # 冪等保護 + 取出暫存 hashed_password（同一 connection 做完再關）
    _tmp = _db_conn()
    _already = _tmp.execute(
        "SELECT 1 FROM processed_orders WHERE merchant_trade_no=?", (trade_no_w,)
    ).fetchone()
    _po = _tmp.execute(
        "SELECT hashed_password FROM pending_orders WHERE merchant_trade_no=?", (trade_no_w,)
    ).fetchone()
    if _po:
        _tmp.execute("DELETE FROM pending_orders WHERE merchant_trade_no=?", (trade_no_w,))
        _tmp.commit()
    _tmp.close()

    if _already:
        print(f"   ⚠️ 重複 Webhook，已處理過：{trade_no_w}")
        return JSONResponse(content="1|OK")

    hashed_password = _po["hashed_password"] if _po else _hash_pw(secrets.token_urlsafe(8))

    days = _plan_days(item_name)
    plan = "yearly" if days >= 365 else ("quarterly" if days >= 90 else "monthly")

    conn = _db_conn()
    row = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()

    if row:
        # 既有用戶：更新方案、延長到期日
        current_expire = row["expire_at"] or _date_cls.today().isoformat()
        base = max(current_expire, _date_cls.today().isoformat())
        new_expire = (datetime.fromisoformat(base) + timedelta(days=days)).strftime("%Y-%m-%d")
        if _po:
            conn.execute(
                "UPDATE members SET plan=?, expire_at=?, password=?, token_ver=token_ver+1 WHERE email=?",
                (plan, new_expire, hashed_password, email)
            )
        else:
            conn.execute(
                "UPDATE members SET plan=?, expire_at=?, token_ver=token_ver+1 WHERE email=?",
                (plan, new_expire, email)
            )
        conn.commit()
        conn.close()
        plan_label = {"monthly":"月費方案","quarterly":"季費方案","yearly":"年費方案","test":"測試方案"}.get(plan, plan)
        upgrade_ad = "" if plan == "yearly" else """
        <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:16px;margin:20px 0;text-align:center">
          <p style="margin:0 0 8px;font-weight:700;color:#166534">💡 升級年費方案，省更多！</p>
          <p style="margin:0 0 12px;font-size:13px;color:#15803d">年費 $3,688 = 月費 9.2 個月的價格，多送近 3 個月</p>
          <a href="https://softglow-ai.com/landing.html" style="background:#16a34a;color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-weight:700">立即升級年費</a>
        </div>"""
        _send_email(email, "【線上有位】升級成功！您的方案已開通",
            f"""<div style="font-family:-apple-system,sans-serif;max-width:560px;margin:0 auto;padding:24px">
              <div style="text-align:center;margin-bottom:24px">
                <h1 style="font-size:24px;color:#1D9E75;margin:0">線上<span style="color:#333">有位</span></h1>
                <p style="color:#666;font-size:13px;margin:4px 0 0">台股技術分析輔助系統</p>
              </div>
              <div style="background:#f0fdf4;border-radius:12px;padding:24px;margin-bottom:20px;border:1px solid #86efac">
                <h2 style="margin:0 0 16px;font-size:18px;color:#166534">🎉 升級成功！</h2>
                <p style="color:#555;margin:0 0 16px">感謝您升級線上有位！您的付費方案已成功開通。</p>
                <table style="width:100%;border-collapse:collapse">
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">方案</td><td style="padding:8px 0;font-weight:700;color:#333">{plan_label}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">到期日</td><td style="padding:8px 0;font-weight:700;color:#333">{new_expire}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">帳號</td><td style="padding:8px 0;font-weight:700;color:#333">{email}</td></tr>
                </table>
              </div>
              <div style="text-align:center;margin-bottom:20px">
                <a href="https://softglow-ai.com" style="background:#1D9E75;color:#fff;padding:12px 32px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px">立即登入使用</a>
              </div>
              {upgrade_ad}
              <div style="background:#fff8e1;border-radius:8px;padding:16px;margin-bottom:20px">
                <p style="margin:0 0 8px;font-weight:700;color:#92400e">📢 廣告合作推薦</p>
                <p style="margin:0;font-size:13px;color:#78350f">把線上有位推薦給朋友，讓更多人享受 AI 輔助的台股分析工具！分享您的使用心得，幫助我們持續優化服務。</p>
              </div>
              <div style="border-top:1px solid #e5e7eb;padding-top:16px;text-align:center;color:#9ca3af;font-size:12px">
                <p style="margin:0">如有問題請聯繫客服：<a href="mailto:watione@yahoo.com.tw" style="color:#1D9E75">watione@yahoo.com.tw</a></p>
                <p style="margin:4px 0 0">線上有位 © 2026</p>
              </div>
            </div>"""
        )
    else:
        # 新用戶：hashed_password 已從 pending_orders 取出（或隨機備用）
        new_expire = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")
        try:
            conn.execute(
                "INSERT INTO members (email, password, plan, expire_at) VALUES (?, ?, ?, ?)",
                (email, hashed_password, plan, new_expire)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            _rec = _db_conn()
            _rec.execute("INSERT OR IGNORE INTO processed_orders (merchant_trade_no) VALUES (?)", (trade_no_w,))
            _rec.commit()
            _rec.close()
            return JSONResponse(content="1|OK")
        conn.close()
        plan_label2 = {"monthly":"月費方案","quarterly":"季費方案","yearly":"年費方案","test":"測試方案"}.get(plan, plan)
        pwd_hint = "<tr><td style='padding:8px 0;color:#888;font-size:13px'>密碼</td><td style='padding:8px 0;font-weight:700;color:#333'>您訂購時自行設定的密碼</td></tr>"
        _send_email(email, "【線上有位】歡迎！您的帳號已開通",
            f"""<div style="font-family:-apple-system,sans-serif;max-width:560px;margin:0 auto;padding:24px">
              <div style="text-align:center;margin-bottom:24px">
                <h1 style="font-size:24px;color:#1D9E75;margin:0">線上<span style="color:#333">有位</span></h1>
                <p style="color:#666;font-size:13px;margin:4px 0 0">台股技術分析輔助系統</p>
              </div>
              <div style="background:#f0fdf4;border-radius:12px;padding:24px;margin-bottom:20px;border:1px solid #86efac">
                <h2 style="margin:0 0 16px;font-size:18px;color:#166534">🎉 歡迎加入線上有位！</h2>
                <p style="color:#555;margin:0 0 16px">感謝您的訂閱！以下是您的帳號資訊，請妥善保管：</p>
                <div style="background:#fff;border-radius:8px;padding:16px;margin-bottom:12px">
                  <table style="width:100%;border-collapse:collapse">
                    <tr><td style="padding:8px 0;color:#888;font-size:13px;width:80px">帳號</td><td style="padding:8px 0;font-weight:700;color:#333">{email}</td></tr>
                    {pwd_hint}
                    <tr><td style="padding:8px 0;color:#888;font-size:13px">方案</td><td style="padding:8px 0;font-weight:700;color:#333">{plan_label2}</td></tr>
                    <tr><td style="padding:8px 0;color:#888;font-size:13px">到期日</td><td style="padding:8px 0;font-weight:700;color:#333">{new_expire}</td></tr>
                  </table>
                </div>
                <p style="margin:0;font-size:12px;color:#555">如忘記密碼，可至「我的」頁面更改密碼，或聯繫客服協助重設。</p>
              </div>
              <div style="text-align:center;margin-bottom:20px">
                <a href="https://softglow-ai.com" style="background:#1D9E75;color:#fff;padding:12px 32px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px">立即登入使用 →</a>
              </div>
              <div style="background:#f8fafc;border-radius:8px;padding:16px;margin-bottom:16px">
                <p style="margin:0 0 12px;font-weight:700;color:#333">🚀 您可以使用以下功能：</p>
                <ul style="margin:0;padding-left:20px;color:#555;font-size:13px;line-height:2">
                  <li>輸入任意台股代號，即時取得技術分析報告</li>
                  <li>支撐壓力、軌道、型態、損益比一次掌握</li>
                  <li>K 線圖搭配均線、布林、RSI、MACD 等指標</li>
                  <li>每日 AI 自動篩選低基期潛力股（選股功能）</li>
                </ul>
              </div>
              <div style="background:#fff8e1;border-radius:8px;padding:16px;margin-bottom:16px">
                <p style="margin:0 0 8px;font-weight:700;color:#92400e">💡 升級年費，省更多！</p>
                <p style="margin:0 0 12px;font-size:13px;color:#78350f">年費 $3,688 相當於月費 9.2 個月，多享近 3 個月服務</p>
                <a href="https://softglow-ai.com/landing.html" style="background:#f59e0b;color:#fff;padding:8px 20px;border-radius:6px;text-decoration:none;font-weight:700;font-size:13px">了解年費方案</a>
              </div>
              <div style="background:#eff6ff;border-radius:8px;padding:16px;margin-bottom:20px">
                <p style="margin:0 0 8px;font-weight:700;color:#1e40af">📢 推薦好友，一起分析台股</p>
                <p style="margin:0;font-size:13px;color:#1e3a8a">把線上有位分享給投資朋友，一起利用 AI 找到好的進場位置！</p>
              </div>
              <div style="border-top:1px solid #e5e7eb;padding-top:16px;text-align:center;color:#9ca3af;font-size:12px">
                <p style="margin:0">如有問題請聯繫客服：<a href="mailto:watione@yahoo.com.tw" style="color:#1D9E75">watione@yahoo.com.tw</a></p>
                <p style="margin:4px 0 0">線上有位 © 2026</p>
              </div>
            </div>"""
        )

    # 記錄已處理，防止重複 Webhook 再次開通
    _rec_conn = _db_conn()
    _rec_conn.execute("INSERT OR IGNORE INTO processed_orders (merchant_trade_no) VALUES (?)", (trade_no_w,))
    _rec_conn.commit()
    _rec_conn.close()

    print(f"   ✅ Webhook 處理完成：{email} → {plan} 到 {new_expire}")
    return JSONResponse(content="1|OK")


# ══════════════════════════════════════════════════════════
# 聯絡留言板 API
# ══════════════════════════════════════════════════════════

class ContactMessage(BaseModel):
    name: str
    email: str
    message: str

class DeleteToken(BaseModel):
    token: str

CONTACT_ADMIN_PWD = "630428"


@app.post("/api/contact")
async def submit_contact(msg: ContactMessage):
    name    = msg.name.strip()[:50]
    email   = msg.email.strip()[:100]
    message = msg.message.strip()[:1000]

    if not name or not email or not message:
        raise HTTPException(status_code=400, detail="欄位不完整")

    # 檢查是否被封鎖留言
    with sqlite3.connect(DB_PATH) as _bc:
        _bc.row_factory = sqlite3.Row
        _brow = _bc.execute(
            "SELECT email FROM blocked_users WHERE email=? AND block_type='comment'", (email,)
        ).fetchone()
    if _brow:
        raise HTTPException(status_code=403, detail="您的帳號已被限制留言")

    now = _taipei_now_str()
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO contact_messages (name, email, message, created_at) VALUES (?,?,?,?)",
            (name, email, message, now)
        )
        new_id = cur.lastrowid

    # Web Push 通知管理員
    try:
        with sqlite3.connect(DB_PATH) as _pc:
            _pc.row_factory = sqlite3.Row
            _subs = _pc.execute(
                "SELECT * FROM push_subscriptions WHERE user_email='watione@yahoo.com.tw'"
            ).fetchall()
        for _sub in _subs:
            send_web_push(dict(_sub), "新留言", f"{email}：{message[:20]}", "/contact.html")
    except Exception as _pe:
        print(f"[contact] Web Push 失敗: {_pe}")

    # 寄通知信給管理員
    try:
        import ssl as _ssl
        html_body = f"""
        <div style="font-family:sans-serif;max-width:500px;margin:auto;padding:24px;
                    background:#f8f9fa;border-radius:12px;">
          <h2 style="color:#3b82f6;margin-bottom:4px;">📬 新留言通知</h2>
          <hr style="border:1px solid #e2e8f0;margin-bottom:20px;">
          <p><strong>姓名：</strong>{name}</p>
          <p><strong>Email：</strong>{email}</p>
          <p><strong>時間：</strong>{now} UTC</p>
          <p style="margin-top:16px;"><strong>內容：</strong></p>
          <div style="background:#fff;border-left:4px solid #3b82f6;
                      padding:12px 16px;border-radius:4px;white-space:pre-wrap;">{message}</div>
          <p style="margin-top:20px;color:#64748b;font-size:12px;">此信由 線上有位 系統自動發送</p>
        </div>"""
        _send_email("watione@yahoo.com.tw", f"【線上有位】新留言來自 {name}", html_body)
    except Exception as e:
        print(f"[contact] 寄信失敗: {e}")

    return {"ok": True, "id": new_id, "message": "訊息已收到"}


@app.get("/api/contact/messages")
async def get_contact_messages():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, name, email, message, created_at "
            "FROM contact_messages ORDER BY id DESC LIMIT 100"
        ).fetchall()
        reply_rows = conn.execute(
            "SELECT id, message_id, reply, created_at FROM contact_replies ORDER BY id ASC"
        ).fetchall()
    replies_map: dict = {}
    for r in reply_rows:
        mid = r["message_id"]
        replies_map.setdefault(mid, []).append(
            {"id": r["id"], "reply": r["reply"], "created_at": r["created_at"]}
        )
    return {
        "messages": [
            {"id": r["id"], "name": r["name"], "email": r["email"],
             "message": r["message"], "created_at": r["created_at"],
             "replies": replies_map.get(r["id"], [])}
            for r in rows
        ]
    }


@app.delete("/api/contact/{msg_id}")
async def delete_contact_message(msg_id: int, body: DeleteToken):
    # 留言者刪除：token="owner"（前端 localStorage 記住自己的 id）
    # 管理員刪除：token="630428"
    if body.token not in ("owner", CONTACT_ADMIN_PWD):
        raise HTTPException(status_code=403, detail="無刪除權限")

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "DELETE FROM contact_messages WHERE id = ?", (msg_id,)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="留言不存在")

    return {"ok": True}


class ReplyReq(BaseModel):
    token: str
    reply: str

class BlockReq(BaseModel):
    token: str
    email: str
    block_type: str  # 'comment' or 'login'


@app.post("/api/contact/{msg_id}/reply")
async def reply_contact_message(msg_id: int, body: ReplyReq):
    if body.token != CONTACT_ADMIN_PWD:
        raise HTTPException(status_code=403, detail="無權限")
    reply_text = body.reply.strip()
    if not reply_text:
        raise HTTPException(status_code=400, detail="回覆內容不能為空")
    now = _taipei_now_str()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        if not conn.execute("SELECT id FROM contact_messages WHERE id=?", (msg_id,)).fetchone():
            raise HTTPException(status_code=404, detail="留言不存在")
        cur = conn.execute(
            "INSERT INTO contact_replies (message_id, reply, created_at) VALUES (?,?,?)",
            (msg_id, reply_text, now)
        )
    return {"ok": True, "id": cur.lastrowid}


@app.post("/api/block")
async def block_user(body: BlockReq):
    if body.token != CONTACT_ADMIN_PWD:
        raise HTTPException(status_code=403, detail="無權限")
    if body.block_type not in ("comment", "login"):
        raise HTTPException(status_code=400, detail="block_type 必須為 comment 或 login")
    email = body.email.strip().lower()
    now = _taipei_now_str()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO blocked_users (email, block_type, created_at) VALUES (?,?,?) "
            "ON CONFLICT(email) DO UPDATE SET block_type=excluded.block_type, created_at=excluded.created_at",
            (email, body.block_type, now)
        )
    return {"ok": True}


@app.delete("/api/block/{email}")
async def unblock_user(email: str, token: str):
    if token != CONTACT_ADMIN_PWD:
        raise HTTPException(status_code=403, detail="無權限")
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("DELETE FROM blocked_users WHERE email=?", (email,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="未找到封鎖記錄")
    return {"ok": True}


@app.get("/api/block")
async def get_blocked_users(token: str):
    if token != CONTACT_ADMIN_PWD:
        raise HTTPException(status_code=403, detail="無權限")
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT email, block_type, created_at FROM blocked_users ORDER BY created_at DESC"
        ).fetchall()
    return {"blocked": [dict(r) for r in rows]}


def _update_notice_date(email: str, date_str: str):
    conn = _db_conn()
    conn.execute("UPDATE members SET last_expire_notice_date=? WHERE email=?", (date_str, email))
    conn.commit()
    conn.close()


def _get_or_create_referral_code(email: str) -> str:
    conn = _db_conn()
    row = conn.execute("SELECT code FROM referral_codes WHERE user_email=?", (email,)).fetchone()
    if row:
        conn.close()
        return row["code"]
    code = secrets.token_hex(4).upper()
    conn.execute("INSERT OR IGNORE INTO referral_codes (user_email, code) VALUES (?, ?)", (email, code))
    conn.commit()
    conn.close()
    return code


def _complete_referral_if_pending(user_email: str):
    conn = _db_conn()
    try:
        row = conn.execute(
            "SELECT * FROM referral_logs WHERE invitee_email=? AND status='pending'", (user_email,)
        ).fetchone()
        if not row:
            return
        conn.execute("UPDATE referral_logs SET status='completed' WHERE id=?", (row["id"],))
        conn.commit()
        inviter = row["inviter_email"]
        cnt = conn.execute(
            "SELECT COUNT(*) FROM referral_logs WHERE inviter_email=? AND status='completed'", (inviter,)
        ).fetchone()[0]
        if cnt >= 3:
            prev = conn.execute("SELECT referral_unlocked FROM members WHERE email=?", (inviter,)).fetchone()
            if prev and prev["referral_unlocked"] == 0:
                expire_date = (_date_cls.today() + timedelta(days=30)).isoformat()
                conn.execute(
                    "UPDATE members SET referral_unlocked=1, referral_expire_date=? WHERE email=?",
                    (expire_date, inviter)
                )
                conn.commit()
                _send_email(
                    inviter, "【線上有位】恭喜！已解鎖全功能 30 天",
                    f'<p>您已成功邀請 {cnt} 位好友完成首次查詢，全功能已自動解鎖 30 天（有效期至 {expire_date}）。</p>'
                    f'<p>繼續邀請好友可再次解鎖延長使用期限！</p>'
                    f'<p><a href="{FRONTEND_URL}">立即使用</a></p>'
                )
        print(f"[REFERRAL] {user_email} 完成，inviter={inviter} cnt={cnt}")
    finally:
        conn.close()


def _fetch_stock_news(stock_id: str, max_results: int = 3) -> list:
    """從鉅亨 RSS 抓與該股票相關的新聞（代號精確比對 + 中文股名比對）"""
    try:
        import sys as _sys
        _picker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker")
        if _picker_path not in _sys.path:
            _sys.path.insert(0, _picker_path)
        from crawler import fetch_cnyes_news
        stock_name = _name_cache.get(stock_id, "")
        all_news = fetch_cnyes_news(100)
        matched = [
            {"title": n["title"], "link": n["link"]}
            for n in all_news
            if stock_id in n.get("codes", [])
            or (stock_name and stock_name in n.get("title", ""))
        ]
        return matched[:max_results]
    except Exception as _e:
        print(f"[NEWS] _fetch_stock_news {stock_id} 失敗：{_e}")
        return []


def _build_report_html(stock_id: str, stock_name: str, report_date: str, d: dict,
                       news_items: list = None) -> str:
    price      = d.get("price", 0)
    trend      = d.get("trend", "盤整")
    risk_level = d.get("risk_level", "medium")
    risk_label = d.get("risk_label", "中風險")
    support    = d.get("support", 0)
    resistance = d.get("resistance", 0)
    stop_loss  = d.get("stop_loss", 0)
    rr_ratio   = d.get("risk_reward", 0)
    kbar_pattern = d.get("kbar_pattern", "")
    kline_pattern = d.get("kline_pattern", "")
    win_rate   = d.get("win_rate", 0.5)
    supp_desc  = d.get("support_desc", "")
    res_desc   = d.get("resistance_desc", "")

    # 9 text rules
    bullets = []
    if trend == "上升趨勢":
        bullets.append("均線三線多頭排列（MA5>MA20>MA60），中長期趨勢偏強，回測支撐是買點。")
    elif trend == "下降趨勢":
        bullets.append("均線三線空頭排列（MA5<MA20<MA60），技術結構偏弱，反彈壓力是出場點。")
    else:
        bullets.append("均線糾結，多空交戰，暫無明確方向，宜等待突破訊號。")

    if rr_ratio >= 2:
        bullets.append(f"損益比 {rr_ratio:.2f}，風險報酬比良好，值得評估進場。")
    elif rr_ratio >= 1:
        bullets.append(f"損益比 {rr_ratio:.2f}，風險報酬尚可，需謹慎評估。")
    else:
        bullets.append(f"損益比 {rr_ratio:.2f}，風險大於報酬，不建議此位置進場。")

    bullets.append(f"支撐位 {support}（{supp_desc}），壓力位 {resistance}（{res_desc}）。")
    bullets.append(f"操作防守位 {stop_loss}，跌破需停損出場。")

    if kbar_pattern:
        bullets.append(f"最新K棒型態：{kbar_pattern}，操作方向參考型態訊號。")
    if kline_pattern and "常態" not in kline_pattern:
        bullets.append(f"K線大數據型態：{kline_pattern}（歷史勝率 {int(win_rate*100)}%）。")

    risk_colors = {"low": "#3b82f6", "medium": "#fbbf24", "high": "#f87171"}
    risk_color = risk_colors.get(risk_level, "#fbbf24")

    bullets_html = "".join(
        f'<li style="padding:8px 0;border-bottom:1px solid #1e3a5a;font-size:14px;line-height:1.7;color:#e8e0d0">{b}</li>'
        for b in bullets
    )

    if news_items:
        news_rows = "".join(
            f'<li style="padding:8px 0;border-bottom:1px solid #1e3a5a">'
            f'<a href="{n["link"]}" target="_blank" rel="noopener" '
            f'style="color:#3b82f6;font-size:13px;line-height:1.6">{n["title"]}</a></li>'
            for n in news_items
        )
        news_html = (
            '<div class="card">'
            '<div style="font-size:15px;font-weight:700;margin-bottom:12px;color:#3b82f6">相關新聞</div>'
            f'<ul style="list-style:none">{news_rows}</ul>'
            '</div>'
        )
    else:
        news_html = ""

    json_ld = _json_mod.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{stock_id} {stock_name} 個股分析報告",
        "datePublished": report_date,
        "publisher": {"@type": "Organization", "name": "線上有位"},
        "description": f"{stock_id} {stock_name} {report_date} 技術分析：{trend}，支撐 {support}，壓力 {resistance}",
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{stock_id} {stock_name} 個股分析報告 {report_date} — 線上有位</title>
<meta name="description" content="{stock_id} {stock_name} {report_date} 技術分析報告：{trend}，支撐 {support}，壓力 {resistance}，損益比 {rr_ratio:.2f}">
<meta property="og:title" content="{stock_id} {stock_name} 分析報告">
<meta property="og:description" content="{trend}｜支撐 {support}｜壓力 {resistance}｜損益比 {rr_ratio:.2f}">
<meta property="og:type" content="article">
<script type="application/ld+json">{json_ld}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f1923;color:#e8e0d0;font-family:-apple-system,'Noto Sans TC',sans-serif;min-height:100vh;padding:24px 16px 48px}}
.container{{max-width:720px;margin:0 auto}}
.card{{background:#1a2634;border-radius:14px;padding:20px;margin-bottom:16px}}
.tag{{display:inline-block;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700;margin-bottom:8px}}
a{{color:#3b82f6;text-decoration:none}}
a:hover{{text-decoration:underline}}
</style>
</head>
<body>
<div class="container">
  <div style="margin-bottom:20px">
    <a href="{FRONTEND_URL}" style="font-size:13px;color:#6b8fbf">← 線上有位</a>
  </div>
  <div class="card">
    <span class="tag" style="background:{risk_color}22;color:{risk_color}">{risk_label}</span>
    <div style="font-size:26px;font-weight:700;margin-bottom:4px">{stock_id} {stock_name}</div>
    <div style="font-size:13px;color:#8faabf;margin-bottom:16px">分析日期：{report_date}</div>
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:16px">
      <div><div style="font-size:11px;color:#6b8fbf;margin-bottom:2px">現價</div><div style="font-size:28px;font-weight:700">{price}</div></div>
      <div><div style="font-size:11px;color:#6b8fbf;margin-bottom:2px">趨勢</div><div style="font-size:20px;font-weight:700">{trend}</div></div>
      <div><div style="font-size:11px;color:#6b8fbf;margin-bottom:2px">損益比</div><div style="font-size:20px;font-weight:700">{rr_ratio:.2f}</div></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
      <div style="background:#0f1923;border-radius:10px;padding:12px">
        <div style="font-size:11px;color:#6b8fbf;margin-bottom:4px">支撐位</div>
        <div style="font-size:18px;font-weight:700;color:#3b82f6">{support}</div>
        <div style="font-size:11px;color:#6b8fbf;margin-top:2px">{supp_desc}</div>
      </div>
      <div style="background:#0f1923;border-radius:10px;padding:12px">
        <div style="font-size:11px;color:#6b8fbf;margin-bottom:4px">壓力位</div>
        <div style="font-size:18px;font-weight:700;color:#fbbf24">{resistance}</div>
        <div style="font-size:11px;color:#6b8fbf;margin-top:2px">{res_desc}</div>
      </div>
    </div>
  </div>
  <div class="card">
    <div style="font-size:15px;font-weight:700;margin-bottom:12px;color:#3b82f6">技術分析摘要</div>
    <ul style="list-style:none">{bullets_html}</ul>
  </div>
  {news_html}
  <div class="card" style="text-align:center">
    <div style="font-size:14px;color:#8faabf;margin-bottom:12px">查看完整互動圖表與即時報價</div>
    <a href="{FRONTEND_URL}?q={stock_id}" style="display:inline-block;background:#3b82f6;color:#fff;padding:12px 28px;border-radius:30px;font-weight:700;font-size:15px">前往線上有位 →</a>
  </div>
  <div style="font-size:11px;color:#4a6a8f;text-align:center;margin-top:16px;line-height:1.6">
    ⚠️ 本報告僅供參考，不構成買賣建議。投資有風險，請自行評估。
  </div>
</div>
</body>
</html>"""


def send_web_push(subscription: dict, title: str, body: str, url: str = "/"):
    """送出 Web Push 通知（需 pywebpush + VAPID 金鑰）"""
    if not _WEBPUSH_AVAILABLE or not VAPID_PRIVATE_KEY:
        return
    try:
        _webpush_fn(
            subscription_info={
                "endpoint": subscription["endpoint"],
                "keys": {"p256dh": subscription["p256dh"], "auth": subscription["auth"]},
            },
            data=_json_mod.dumps({"title": title, "body": body, "url": url}),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_SUBJECT},
        )
    except Exception as _e:
        print(f"   ⚠️ Web Push 失敗：{_e}")


# ── 忘記密碼 ──────────────────────────────────────────────
class ForgotPwdReq(BaseModel):
    email: str

class ResetPwdReq(BaseModel):
    token: str
    new_password: str

@app.post("/forgot-password")
async def forgot_password(req: ForgotPwdReq, request: Request):
    import uuid as _uuid
    email = req.email.strip().lower()
    client_ip = request.client.host if request.client else "unknown"
    _tw_now = datetime.fromisoformat(_taipei_now_str())
    one_min_ago  = (_tw_now - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
    one_hour_ago = (_tw_now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

    conn = _db_conn()
    # Rate limit: 同一 IP 每分鐘最多 3 次
    ip_count = conn.execute(
        "SELECT COUNT(*) FROM password_reset_tokens WHERE ip=? AND created_at > ?",
        (client_ip, one_min_ago)
    ).fetchone()[0]
    if ip_count >= 3:
        conn.close()
        raise HTTPException(status_code=429, detail="請求太頻繁，請稍後再試")

    # 同一 email 一小時內只能寄一次（帳號存在才檢查）
    user = conn.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()
    if user:
        recent = conn.execute(
            "SELECT COUNT(*) FROM password_reset_tokens WHERE email=? AND created_at > ? AND used=0",
            (email, one_hour_ago)
        ).fetchone()[0]
        if recent > 0:
            conn.close()
            return {"ok": True, "message": "若此信箱已註冊，重設連結將寄出"}

        token = str(_uuid.uuid4())
        expires_at = (datetime.fromisoformat(_taipei_now_str()) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "INSERT INTO password_reset_tokens (token, email, expires_at, ip) VALUES (?, ?, ?, ?)",
            (token, email, expires_at, client_ip)
        )
        conn.commit()
        conn.close()
        reset_url = f"{FRONTEND_URL}/reset-password.html?token={token}"
        _send_email(email, "線上有位 — 密碼重設連結",
            f"""<div style="font-family:-apple-system,sans-serif;max-width:480px;margin:0 auto;padding:24px">
              <h2 style="color:#1D9E75">密碼重設</h2>
              <p>請點擊以下連結重設密碼（有效期 1 小時）：</p>
              <p><a href="{reset_url}" style="background:#1D9E75;color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-weight:700">重設密碼</a></p>
              <p style="font-size:12px;color:#888">若您未申請重設，請忽略此信。</p>
            </div>"""
        )
    else:
        conn.close()
    return {"ok": True, "message": "若此信箱已註冊，重設連結將寄出"}


@app.post("/reset-password")
async def reset_password(req: ResetPwdReq):
    token = req.token.strip()
    new_pw = req.new_password
    if len(new_pw) < 6:
        raise HTTPException(status_code=400, detail="密碼至少 6 個字元")
    now_str = _taipei_now_str()
    conn = _db_conn()
    row = conn.execute(
        "SELECT email, expires_at, used FROM password_reset_tokens WHERE token=?", (token,)
    ).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=400, detail="連結無效，請重新申請")
    if row["used"]:
        conn.close()
        raise HTTPException(status_code=400, detail="連結已使用，請重新申請")
    if row["expires_at"] < now_str:
        conn.close()
        raise HTTPException(status_code=400, detail="連結已過期，請重新申請忘記密碼")
    email = row["email"]
    email = email.strip().lower()
    conn.execute("UPDATE members SET password=?, token_ver=token_ver+1, password_changed_at=? WHERE email=?",
                 (_hash_pw(new_pw), now_str, email))
    conn.commit()
    conn.execute("UPDATE password_reset_tokens SET used=1 WHERE token=?", (token,))
    conn.commit()
    conn.close()
    return {"ok": True, "message": "密碼已重設，請重新登入"}


# ── 到價提醒 ──────────────────────────────────────────────
class AlertReq(BaseModel):
    stock_id:     str
    target_price: float
    direction:    str   # 'above' or 'below'

@app.get("/api/alerts")
def get_alerts(user: dict = Depends(require_paid_user)):
    conn = _db_conn()
    rows = conn.execute(
        "SELECT * FROM price_alerts WHERE user_email=? AND triggered=0 ORDER BY created_at DESC",
        (user["email"],)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/alerts")
def create_alert(req: AlertReq, request: Request, user: dict = Depends(require_paid_user)):
    if req.direction not in ("above", "below"):
        raise HTTPException(status_code=400, detail="direction 必須為 above 或 below")
    conn = _db_conn()
    count = conn.execute(
        "SELECT COUNT(*) FROM price_alerts WHERE user_email=? AND triggered=0",
        (user["email"],)
    ).fetchone()[0]
    if count >= 10:
        conn.close()
        raise HTTPException(status_code=400, detail="每人最多設定 10 個到價提醒")
    now_str = _taipei_now_str()
    conn.execute(
        "INSERT INTO price_alerts (user_email, stock_id, target_price, direction, created_at) VALUES (?, ?, ?, ?, ?)",
        (user["email"], req.stock_id.strip().upper(), req.target_price, req.direction, now_str)
    )
    conn.commit()
    conn.close()
    return {"ok": True}

@app.delete("/api/alerts/{alert_id}")
def delete_alert(alert_id: int, user: dict = Depends(require_user)):
    conn = _db_conn()
    row = conn.execute("SELECT user_email FROM price_alerts WHERE id=?", (alert_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="提醒不存在")
    if row["user_email"] != user["email"]:
        conn.close()
        raise HTTPException(status_code=403, detail="無權限刪除")
    conn.execute("DELETE FROM price_alerts WHERE id=?", (alert_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


# ── 全台股掃描結果 ──────────────────────────────────────────
@app.get("/api/scan/latest")
def get_scan_latest(user: dict = Depends(require_paid_user)):
    scan_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker", "output", "scan_result.html")
    if not os.path.exists(scan_path):
        raise HTTPException(status_code=503, detail="掃描結果每日15:30更新，請稍後再試")
    with open(scan_path, "r", encoding="utf-8") as f:
        html = f.read()
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html)


# ── Web Push ────────────────────────────────────────────
class WebPushSubReq(BaseModel):
    endpoint: str
    keys:     dict   # {p256dh: str, auth: str}

@app.get("/api/webpush/vapid-public-key")
def get_vapid_public_key():
    return {"publicKey": VAPID_PUBLIC_KEY}

@app.post("/api/webpush/subscribe")
def subscribe_webpush(req: WebPushSubReq, user: dict = Depends(require_user)):
    conn = _db_conn()
    conn.execute("""
        INSERT INTO push_subscriptions (user_email, endpoint, p256dh, auth)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(endpoint) DO UPDATE SET
            user_email=excluded.user_email,
            p256dh=excluded.p256dh,
            auth=excluded.auth
    """, (user["email"], req.endpoint,
          req.keys.get("p256dh", ""), req.keys.get("auth", "")))
    conn.commit()
    conn.close()
    return {"ok": True}


@app.get("/ads.txt")
async def ads_txt():
    return PlainTextResponse("google.com, pub-1768270548115739, DIRECT, f08c47fec0942fa0")


# ══════════════════════════════════════════════════════════
# 個股報告頁（Task 1）
# ══════════════════════════════════════════════════════════

class ReportReq(BaseModel):
    stock_id: str


@app.post("/api/report/generate")
def report_generate(req: ReportReq, user: dict = Depends(require_user)):
    plan = user["plan"]
    is_referral_unlocked = _is_referral_active(user)
    if not is_referral_unlocked and user.get("expire_at") and user["expire_at"] < _taipei_today():
        raise HTTPException(status_code=403, detail="訂閱已到期，請續費後繼續使用")
    is_free = plan == "free" and not is_referral_unlocked
    if is_free:
        allowed, _, _ = _check_query_limit(user["id"], plan)
        if not allowed:
            raise HTTPException(status_code=403, detail="完整報告為付費功能，升級或邀請3位好友即可使用")

    stock_id = req.stock_id.strip().upper()
    report_date = _taipei_today()

    # same-day cache（快取命中不計入次數）
    conn = _db_conn()
    cached = conn.execute(
        "SELECT report_html FROM stock_reports WHERE stock_id=? AND report_date=?",
        (stock_id, report_date)
    ).fetchone()
    conn.close()
    if cached:
        return {"ok": True, "url": f"{BACKEND_URL}/report/{stock_id}-{report_date}"}

    try:
        d = _do_analyze(stock_id, "D", user=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{e}")

    stock_name = d.get("stock_name", stock_id)
    news_items = _fetch_stock_news(stock_id)
    report_html = _build_report_html(stock_id, stock_name, report_date, d, news_items)

    conn = _db_conn()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO stock_reports (stock_id, report_date, stock_name, report_html) VALUES (?,?,?,?)",
            (stock_id, report_date, stock_name, report_html)
        )
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

    return {"ok": True, "url": f"{BACKEND_URL}/report/{stock_id}-{report_date}"}


@app.get("/report/{slug}")
def get_report(slug: str):
    from fastapi.responses import HTMLResponse
    m = _re.match(r"^([A-Za-z0-9]+)-(\d{4}-\d{2}-\d{2})$", slug)
    if m:
        stock_id, report_date = m.group(1).upper(), m.group(2)
    else:
        stock_id = slug.upper()
        report_date = _taipei_today()

    conn = _db_conn()
    row = conn.execute(
        "SELECT report_html FROM stock_reports WHERE stock_id=? AND report_date=? ORDER BY created_at DESC LIMIT 1",
        (stock_id, report_date)
    ).fetchone()
    if not row:
        row = conn.execute(
            "SELECT report_html FROM stock_reports WHERE stock_id=? ORDER BY created_at DESC LIMIT 1",
            (stock_id,)
        ).fetchone()
    conn.close()

    if row:
        return HTMLResponse(content=row["report_html"])

    # 即時產生
    try:
        d = _do_analyze(stock_id, "D", user=None)
        stock_name = d.get("stock_name", stock_id)
        news_items = _fetch_stock_news(stock_id)
        html = _build_report_html(stock_id, stock_name, report_date, d, news_items)
        conn = _db_conn()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO stock_reports (stock_id, report_date, stock_name, report_html) VALUES (?,?,?,?)",
                (stock_id, report_date, stock_name, html)
            )
            conn.commit()
        except Exception:
            pass
        finally:
            conn.close()
        return HTMLResponse(content=html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"無法取得 {stock_id} 報告：{e}")


# ══════════════════════════════════════════════════════════
# SEO：sitemap.xml + /rankings（Task 2）
# ══════════════════════════════════════════════════════════

_SEO_HARDCODED_STOCKS = [
    "2330","2317","2454","2308","2412","6505","2882","2881","2886","2891",
    "2884","2892","2883","2885","2887","2888","2890","5880","2801","2002",
    "1301","1303","1326","2303","2357","2382","2395","2402","2408","2409",
    "2449","2474","2476","2376","2379","2385","2392","3711","2301","2325",
    "3034","3037","3045","3702","4904","4938","5871","6415","6669","2610",
]


@app.get("/sitemap.xml")
def sitemap():
    now = _time_mod.time()
    c = SEO_CACHE["sitemap"]
    if c["data"] and c["expires"] > now:
        return PlainTextResponse(c["data"], media_type="application/xml")

    conn = _db_conn()
    reports = conn.execute(
        "SELECT stock_id, report_date FROM stock_reports ORDER BY created_at DESC LIMIT 200"
    ).fetchall()
    conn.close()

    locs = []
    for u in [FRONTEND_URL + "/", FRONTEND_URL + "/landing.html", BACKEND_URL + "/rankings"]:
        locs.append(f"  <url><loc>{u}</loc><changefreq>daily</changefreq><priority>0.8</priority></url>")
    for sid in _SEO_HARDCODED_STOCKS:
        locs.append(f"  <url><loc>{BACKEND_URL}/report/{sid}</loc><changefreq>daily</changefreq><priority>0.6</priority></url>")
    for r in reports:
        locs.append(f"  <url><loc>{BACKEND_URL}/report/{r['stock_id']}-{r['report_date']}</loc><changefreq>weekly</changefreq><priority>0.5</priority></url>")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "\n".join(locs) + "\n</urlset>"

    c["data"] = xml
    c["expires"] = now + 21600
    return PlainTextResponse(xml, media_type="application/xml")


def _fetch_rankings_data():
    """Fetch top-20 gainers/losers/volume from FinMind TaiwanStockPrice."""
    import urllib.request as _ur, json as _j
    from datetime import date as _d, timedelta as _td
    for days_back in range(1, 6):
        target = (_d.today() - _td(days=days_back)).strftime("%Y-%m-%d")
        try:
            url = (
                f"https://api.finmindtrade.com/api/v4/data"
                f"?dataset=TaiwanStockPrice&start_date={target}&end_date={target}"
                f"&token={FINMIND_TOKEN}"
            )
            req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with _ur.urlopen(req, timeout=15) as resp:
                raw = _j.loads(resp.read())
            rows = raw.get("data", [])
            rows = [
                r for r in rows
                if str(r.get("stock_id", "")).isdigit()
                and len(str(r.get("stock_id", ""))) == 4
                and r.get("Trading_Volume", 0) > 500000
                and r.get("open", 0) > 0
                and r.get("close", 0) > 0
            ]
            if not rows:
                continue
            all_info = get_all_stock_info()
            name_map = {s["stock_id"]: s.get("stock_name", "") for s in all_info}
            enriched = []
            for r in rows:
                spread = r.get("spread", 0)
                prev_close = r["close"] - spread
                if prev_close > 0:
                    change_pct = round(spread / prev_close * 100, 2)
                else:
                    change_pct = round((r["close"] - r["open"]) / r["open"] * 100, 2)
                enriched.append({
                    "stock_id": r["stock_id"],
                    "stock_name": name_map.get(r["stock_id"], ""),
                    "close": r["close"],
                    "change_pct": change_pct,
                    "volume": r.get("Trading_Volume", 0),
                })
            gainers = sorted(enriched, key=lambda x: x["change_pct"], reverse=True)[:20]
            losers = sorted(enriched, key=lambda x: x["change_pct"])[:20]
            by_volume = sorted(enriched, key=lambda x: x["volume"], reverse=True)[:20]
            return {"date": target, "gainers": gainers, "losers": losers, "by_volume": by_volume}
        except Exception as e:
            print(f"_fetch_rankings_data {target}: {e}")
            continue
    return None


def _rank_rows_html(stocks):
    out = []
    for i, s in enumerate(stocks, 1):
        pct = s["change_pct"]
        color = "#16a34a" if pct > 0 else ("#dc2626" if pct < 0 else "#666666")
        sign = "+" if pct > 0 else ""
        lots = s.get("volume", 0) // 1000
        vol_str = f"{lots/10000:.1f}萬" if lots >= 10000 else f"{lots:,}"
        link = f"{FRONTEND_URL}/?stock={s['stock_id']}"
        name = s.get("stock_name") or ""
        row = (
            f'<tr onclick="location.href=\'{link}\'">'
            f'<td class="r-num">{i}</td>'
            f'<td class="r-stock"><a href="{link}">{s["stock_id"]}</a>'
            f'<span class="r-name">{name}</span></td>'
            f'<td class="r-price">{s["close"]}</td>'
            f'<td class="r-pct" style="color:{color}">{sign}{pct}%</td>'
            f'<td class="r-vol">{vol_str}</td>'
            f'</tr>'
        )
        out.append(row)
    return "\n".join(out)


@app.get("/rankings")
def rankings():
    from fastapi.responses import HTMLResponse
    now = _time_mod.time()
    c = SEO_CACHE["rankings"]
    if c["data"] and c["expires"] > now:
        return HTMLResponse(c["data"])

    rdata = _fetch_rankings_data()
    date_str = rdata["date"] if rdata else "—"
    _err = '<tr><td colspan="5" style="text-align:center;color:#999;padding:24px">資料載入失敗，請稍後再試</td></tr>'
    gainers_html = _rank_rows_html(rdata["gainers"]) if rdata else _err
    losers_html  = _rank_rows_html(rdata["losers"])  if rdata else _err
    volume_html  = _rank_rows_html(rdata["by_volume"]) if rdata else _err

    json_ld = _json_mod.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "台股排行榜 — 線上有位",
        "description": "台股今日漲幅榜、跌幅榜、成交量榜 Top 20，每15分鐘更新",
        "publisher": {"@type": "Organization", "name": "線上有位"},
    }, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>台股排行榜 漲幅/跌幅/成交量 Top 20 — 線上有位</title>
<meta name="description" content="台股今日漲幅榜、跌幅榜、成交量榜 Top 20，資料來源 FinMind，每15分鐘更新">
<script type="application/ld+json">{json_ld}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#f5f0e8;color:#333;font-family:-apple-system,'Noto Sans TC',sans-serif;min-height:100vh;padding:20px 16px 60px}}
.wrap{{max-width:680px;margin:0 auto}}
.back{{font-size:13px;color:#666;text-decoration:none;display:inline-block;margin-bottom:20px}}
.back:hover{{color:#333}}
h1{{font-size:22px;font-weight:700;margin-bottom:4px}}
.sub{{font-size:13px;color:#888;margin-bottom:20px}}
.tabs{{display:flex;gap:0;margin-bottom:16px;border-bottom:2px solid #e5ddd0}}
.tab{{padding:10px 22px;font-size:14px;font-weight:600;border:none;background:none;color:#999;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px;transition:color .15s}}
.tab.active{{color:#333;border-bottom-color:#333}}
.tab:hover{{color:#555}}
.panel{{display:none}}
.panel.show{{display:block}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.06)}}
thead th{{padding:10px 12px;font-size:12px;color:#888;font-weight:600;text-align:left;border-bottom:1px solid #f0ebe0;background:#faf7f2}}
tbody tr{{border-bottom:1px solid #f5f0ea;cursor:pointer;transition:background .12s}}
tbody tr:last-child{{border-bottom:none}}
tbody tr:hover{{background:#faf6ee}}
td{{padding:11px 12px;vertical-align:middle}}
.r-num{{color:#ccc;font-size:13px;width:30px;text-align:center;padding-left:8px}}
.r-stock a{{font-size:14px;font-weight:700;color:#333;text-decoration:none}}
.r-stock a:hover{{color:#555}}
.r-name{{font-size:12px;color:#999;display:block;margin-top:1px}}
.r-price{{font-size:14px;color:#555;text-align:right}}
.r-pct{{font-size:14px;font-weight:700;text-align:right}}
.r-vol{{font-size:13px;color:#aaa;text-align:right;padding-right:14px}}
.disclaimer{{margin-top:32px;font-size:11px;color:#bbb;text-align:center;line-height:1.8}}
@media(max-width:480px){{
  .tab{{padding:8px 14px;font-size:13px}}
  td{{padding:9px 8px}}
  h1{{font-size:18px}}
  .r-vol{{display:none}}
  thead th:last-child{{display:none}}
}}
</style>
</head>
<body>
<div class="wrap">
  <a href="{FRONTEND_URL}" class="back">← 線上有位</a>
  <h1>台股排行榜</h1>
  <p class="sub">資料日期：{date_str}・每 15 分鐘更新</p>
  <div class="tabs">
    <button class="tab active" onclick="showTab('gainers',this)">漲幅榜</button>
    <button class="tab" onclick="showTab('losers',this)">跌幅榜</button>
    <button class="tab" onclick="showTab('volume',this)">成交量榜</button>
  </div>
  <div id="p-gainers" class="panel show">
    <table>
      <thead><tr><th>#</th><th>股票</th><th style="text-align:right">現價</th><th style="text-align:right">漲跌幅</th><th style="text-align:right">成交量</th></tr></thead>
      <tbody>{gainers_html}</tbody>
    </table>
  </div>
  <div id="p-losers" class="panel">
    <table>
      <thead><tr><th>#</th><th>股票</th><th style="text-align:right">現價</th><th style="text-align:right">漲跌幅</th><th style="text-align:right">成交量</th></tr></thead>
      <tbody>{losers_html}</tbody>
    </table>
  </div>
  <div id="p-volume" class="panel">
    <table>
      <thead><tr><th>#</th><th>股票</th><th style="text-align:right">現價</th><th style="text-align:right">漲跌幅</th><th style="text-align:right">成交量</th></tr></thead>
      <tbody>{volume_html}</tbody>
    </table>
  </div>
  <p class="disclaimer">⚠️ 本頁面資料僅供參考，不構成任何買賣建議。投資有風險，請自行評估。<br>資料來源：FinMind</p>
</div>
<script>
function showTab(name,btn){{
  document.querySelectorAll('.panel').forEach(function(p){{p.classList.remove('show')}});
  document.querySelectorAll('.tab').forEach(function(t){{t.classList.remove('active')}});
  document.getElementById('p-'+name).classList.add('show');
  btn.classList.add('active');
}}
</script>
</body>
</html>"""

    c["data"] = html
    c["expires"] = now + 900
    return HTMLResponse(html)
