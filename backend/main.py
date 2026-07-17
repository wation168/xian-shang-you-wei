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

from fastapi import FastAPI, HTTPException, Depends, Header, Request, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pydantic import BaseModel
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import sqlite3, hashlib, hmac, secrets, time as _time_mod
import json as _json_mod
from datetime import datetime, timedelta, date as _date_cls
from zoneinfo import ZoneInfo
import re as _re
import ssl as _ssl

# TWSE MIS 憑證缺少 Subject Key Identifier，Python 嚴格 SSL 會拒絕；共用一個 no-verify context
_TWSE_SSL_CTX = _ssl.create_default_context()
_TWSE_SSL_CTX.check_hostname = False
_TWSE_SSL_CTX.verify_mode = _ssl.CERT_NONE


# ══════════════════════════════════════════════════════════
# 環境設定（上線用環境變數，本機用 fallback）
# ══════════════════════════════════════════════════════════
FINMIND_TOKEN = os.environ.get("FINMIND_TOKEN", "")
if not FINMIND_TOKEN:
    raise RuntimeError("❌ 請設定環境變數 FINMIND_TOKEN")

# JWT 密鑰（請在 Zeabur 設定環境變數 JWT_SECRET；每次重啟值相同，不影響 token 有效性）
JWT_SECRET = os.environ.get("JWT_SECRET", "change-me-in-production-please")
JWT_EXPIRE_DAYS = 15   # token 有效期（15 天）
if JWT_SECRET == "change-me-in-production-please":
    print("⚠️  [JWT] 使用預設 JWT_SECRET，正式環境請設定 JWT_SECRET 環境變數！")

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

# Threads OAuth
THREADS_APP_ID     = os.environ.get("THREADS_APP_ID",     "1011864388160019")
THREADS_APP_SECRET = os.environ.get("THREADS_APP_SECRET", "0af6b8665441f7940a5f4d0edbc7fe42")
THREADS_REDIRECT_URI = os.environ.get("THREADS_REDIRECT_URI", "https://api.softglow-ai.com/auth/threads/callback")
THREADS_SCOPE      = "threads_basic,threads_content_publish"

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
    "sitemap":    {"data": None, "expires": 0},
    "rankings":   {"data": None, "expires": 0},
    "picks":      {"data": None, "expires": 0},
    "top_gainers": {"data": None, "expires": 0},
}

# 開盤熱門股快取（每日 09:15 更新）
_OPENING_TOP20: dict = {"data": [], "updated_at": None}


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

    # 啟動時恢復今日開盤熱門股
    try:
        import json as _json_op
        _conn_op = _db_conn()
        _row_op = _conn_op.execute(
            "SELECT data, updated_at FROM opening_picks WHERE date=?",
            (_taipei_today(),)
        ).fetchone()
        _conn_op.close()
        if _row_op:
            _OPENING_TOP20["data"] = _json_op.loads(_row_op["data"])
            _OPENING_TOP20["updated_at"] = _row_op["updated_at"]
            print(f"   ✅ 開盤熱門股已從DB恢復（{len(_OPENING_TOP20['data'])} 筆）")
    except Exception as e:
        print(f"   ⚠️ 開盤熱門股恢復失敗：{e}")

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
    _alert_running   = False
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        import sys as _sys
        _picker_path = os.path.join(os.path.dirname(__file__), "stock_picker")

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
                            f'<div style="font-family:-apple-system,sans-serif;max-width:560px;margin:0 auto;padding:24px">'
                            f'<div style="text-align:center;margin-bottom:24px"><h1 style="font-size:24px;color:#1D9E75;margin:0">線上<span style="color:#333">有位</span></h1><p style="color:#666;font-size:13px;margin:4px 0 0">台股技術分析輔助系統</p></div>'
                            + _SOFTGLOW_AD +
                            f'<div style="background:#fff8e1;border-radius:12px;padding:24px;margin-bottom:20px;border:1px solid #fcd34d">'
                            f'<h2 style="margin:0 0 12px;font-size:18px;color:#92400e">⏰ 訂閱即將到期</h2>'
                            f'<p style="color:#555;margin:0 0 16px">您的訂閱將於 <b>{m["expire_at"]}</b> 到期（剩 3 天），請把握時間續訂，避免服務中斷。</p>'
                            f'<a href="{FRONTEND_URL}/stock/landing#pricing" style="background:#f59e0b;color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-weight:700">立即續訂</a></div>'
                            + _SOFTGLOW_AD +
                            f'<div style="border-top:1px solid #e5e7eb;padding-top:16px;text-align:center;color:#9ca3af;font-size:12px">'
                            f'<p style="margin:0">如有問題請聯繫客服：<a href="mailto:watione@yahoo.com.tw" style="color:#1D9E75">watione@yahoo.com.tw</a></p>'
                            f'<p style="margin:4px 0 0">線上有位 © 2026</p></div></div>')
                        _update_notice_date(m["email"], today_str)
                    elif delta == 0:
                        _send_email(m["email"], "【線上有位】訂閱已到期",
                            f'<div style="font-family:-apple-system,sans-serif;max-width:560px;margin:0 auto;padding:24px">'
                            f'<div style="text-align:center;margin-bottom:24px"><h1 style="font-size:24px;color:#1D9E75;margin:0">線上<span style="color:#333">有位</span></h1><p style="color:#666;font-size:13px;margin:4px 0 0">台股技術分析輔助系統</p></div>'
                            + _SOFTGLOW_AD +
                            f'<div style="background:#fef2f2;border-radius:12px;padding:24px;margin-bottom:20px;border:1px solid #fca5a5">'
                            f'<h2 style="margin:0 0 12px;font-size:18px;color:#991b1b">📅 訂閱已到期</h2>'
                            f'<p style="color:#555;margin:0 0 16px">您的訂閱已於今日（{today_str}）到期，部分功能已暫停。續訂後立即恢復所有功能。</p>'
                            f'<a href="{FRONTEND_URL}/stock/landing#pricing" style="background:#ef4444;color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-weight:700">立即續訂</a></div>'
                            + _SOFTGLOW_AD +
                            f'<div style="border-top:1px solid #e5e7eb;padding-top:16px;text-align:center;color:#9ca3af;font-size:12px">'
                            f'<p style="margin:0">如有問題請聯繫客服：<a href="mailto:watione@yahoo.com.tw" style="color:#1D9E75">watione@yahoo.com.tw</a></p>'
                            f'<p style="margin:4px 0 0">線上有位 © 2026</p></div></div>')
                        _update_notice_date(m["email"], today_str)
            except Exception as _e:
                print(f"   ❌ 到期提醒排程執行失敗：{_e}")
            finally:
                _expire_running = False


        def _run_intraday_alert_job():
            nonlocal _alert_running
            if _alert_running:
                return
            # 只在盤中 09:00–13:30 週一~五執行
            import time as _time_alert
            from datetime import datetime as _dtalert
            from zoneinfo import ZoneInfo as _ZIa
            _now_a = _dtalert.now(_ZIa("Asia/Taipei"))
            if _now_a.weekday() >= 5:
                return
            _hm = _now_a.hour * 100 + _now_a.minute
            if _hm < 900 or _hm > 1330:
                return
            _alert_running = True
            try:
                conn = _db_conn()
                alerts = conn.execute(
                    "SELECT * FROM price_alerts WHERE triggered=0"
                ).fetchall()
                conn.close()
                if not alerts:
                    return
                # 每股只呼叫一次 get_quote（利用 _QUOTE_CACHE）
                stock_prices: dict = {}
                for _a in alerts:
                    sid = _a["stock_id"]
                    if sid in stock_prices:
                        continue
                    try:
                        _code = sid.strip().upper()
                        _qc = _QUOTE_CACHE.get(_code)
                        if not (_qc and (_qc["expires"] == 0 or _time_alert.time() < _qc["expires"])):
                            get_quote(_code, user=None)
                            _qc = _QUOTE_CACHE.get(_code)
                        stock_prices[sid] = float(_qc["data"]["price"]) if (_qc and _qc["data"].get("price")) else None
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
                print(f"   ❌ 盤中到價提醒排程執行失敗：{_e}")
            finally:
                _alert_running = False

        def _reset_alert_triggered():
            try:
                conn = _db_conn()
                conn.execute("UPDATE price_alerts SET triggered=0, triggered_at=NULL WHERE triggered=1")
                conn.commit()
                conn.close()
            except Exception as _e:
                print(f"   ❌ 到價提醒重置失敗：{_e}")

        def _run_補單_job():
            """每日 08:00 掃 pending_orders，用 QueryTradeInfo 補查付款狀態，確認付款成功就補開通"""
            import urllib.request as _ur2, urllib.parse as _up2, hashlib as _hl2, time as _t2
            import datetime as _dt2
            print("   [補單] 開始掃描 pending_orders...")
            try:
                from zoneinfo import ZoneInfo as _ZI2
                _now = datetime.now(_ZI2("Asia/Taipei"))
                _cutoff = (_now - _dt2.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
                conn = _db_conn()
                rows = conn.execute(
                    "SELECT merchant_trade_no, email, plan, created_at FROM pending_orders ORDER BY created_at DESC"
                ).fetchall()
                conn.execute("DELETE FROM pending_orders WHERE created_at <= ?", (_cutoff,))
                conn.commit()
                conn.close()
                print(f"   [補單] 共 {len(rows)} 筆待確認")
                for row in rows:
                    trade_no = row["merchant_trade_no"]
                    email    = row["email"]
                    plan     = row["plan"] or "monthly"
                    try:
                        # 先確認是否已處理過
                        _tc = _db_conn()
                        _already = _tc.execute(
                            "SELECT 1 FROM processed_orders WHERE merchant_trade_no=?", (trade_no,)
                        ).fetchone()
                        _tc.close()
                        if _already:
                            print(f"   [補單] {trade_no} 已處理過，跳過")
                            continue
                        # 呼叫綠界 QueryTradeInfo
                        _ts = int(_t2.time())
                        _params = {
                            "MerchantID":      ECPAY_MERCHANT_ID,
                            "MerchantTradeNo": trade_no,
                            "TimeStamp":       str(_ts),
                        }
                        _sorted = sorted(_params.items(), key=lambda x: x[0].lower())
                        _raw = "&".join(f"{k}={v}" for k, v in _sorted)
                        _raw = f"HashKey={ECPAY_HASH_KEY}&{_raw}&HashIV={ECPAY_HASH_IV}"
                        _raw = _up2.quote_plus(_raw).lower()
                        _mac = _hl2.sha256(_raw.encode()).hexdigest().upper()
                        _params["CheckMacValue"] = _mac
                        _body = _up2.urlencode(_params).encode()
                        _req = _ur2.Request(
                            "https://payment.ecpay.com.tw/Cashier/QueryTradeInfo/V5",
                            data=_body,
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                        )
                        with _ur2.urlopen(_req, timeout=10) as _r:
                            _resp = dict(_up2.parse_qsl(_r.read().decode()))
                        _rtn = _resp.get("RtnCode", "0")
                        print(f"   [補單] {trade_no} email={email} RtnCode={_rtn}")
                        if _rtn != "1":
                            continue
                        # 付款成功 → 補開通
                        _days  = _plan_days(plan)
                        _plan2 = "yearly" if _days >= 365 else ("quarterly" if _days >= 90 else "monthly")
                        from zoneinfo import ZoneInfo as _ZI3
                        _expire = (datetime.now(_ZI3("Asia/Taipei")) + _dt2.timedelta(days=_days)).strftime("%Y-%m-%d")
                        _conn2 = _db_conn()
                        _existing = _conn2.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()
                        if _existing:
                            _conn2.execute(
                                "UPDATE members SET plan=?, expire_at=? WHERE email=?",
                                (_plan2, _expire, email)
                            )
                        else:
                            _conn2.execute(
                                "INSERT INTO members (email, password, plan, expire_at) VALUES (?,?,?,?)",
                                (email, _hash_pw(__import__("secrets").token_urlsafe(8)), _plan2, _expire)
                            )
                        _conn2.execute(
                            "INSERT OR IGNORE INTO processed_orders (merchant_trade_no) VALUES (?)", (trade_no,)
                        )
                        _conn2.execute("DELETE FROM pending_orders WHERE merchant_trade_no=?", (trade_no,))
                        _conn2.commit()
                        _conn2.close()
                        print(f"   [補單] ✅ 補開通成功：{email} → {_plan2} 到 {_expire}")
                        try:
                            _send_email(
                                SMTP_USER,
                                "【線上有位】補單通知",
                                f"<div style='font-family:sans-serif;padding:24px'>"
                                f"<h3 style='color:#e67e22'>【線上有位】補單通知</h3>"
                                f"<p>以下訂單 webhook 未即時觸發，已由每日補單排程自動開通：</p>"
                                f"<table style='font-size:14px'>"
                                f"<tr><td style='color:#888;padding:4px 8px'>Email</td><td style='padding:4px 8px'>{email}</td></tr>"
                                f"<tr><td style='color:#888;padding:4px 8px'>訂單號</td><td style='padding:4px 8px'>{trade_no}</td></tr>"
                                f"<tr><td style='color:#888;padding:4px 8px'>方案</td><td style='padding:4px 8px'>{_plan2}</td></tr>"
                                f"<tr><td style='color:#888;padding:4px 8px'>到期日</td><td style='padding:4px 8px'>{_expire}</td></tr>"
                                f"</table></div>"
                            )
                        except Exception:
                            pass
                    except Exception as _e:
                        print(f"   [補單] ❌ {trade_no} 查詢失敗：{_e}")
            except Exception as _e:
                print(f"   [補單] ❌ 排程失敗：{_e}")

        _bg_scheduler = BackgroundScheduler(timezone="Asia/Taipei")
        _bg_scheduler.add_job(_run_opening_scan_job,    "cron",     hour=9,  minute=6,  day_of_week="mon-fri")
        _bg_scheduler.add_job(_run_opening_scan_job,    "cron",     hour=13, minute=45, day_of_week="mon-fri")  # 收盤後更新今日收盤價
        _bg_scheduler.add_job(_run_deep_analysis_job,  "cron",     hour=17, minute=0,  day_of_week="mon-fri")  # 深度選股
        _bg_scheduler.add_job(_run_expire_notice_job,   "cron",     hour=9,  minute=0)
        _bg_scheduler.add_job(_reset_alert_triggered,   "cron",     hour=9,  minute=0,  day_of_week="mon-fri")
        _bg_scheduler.add_job(_run_intraday_alert_job,  "interval", minutes=5)
        _bg_scheduler.add_job(_clear_quote_cache,       "cron",     hour=9,  minute=0,  day_of_week="mon-fri")
        _bg_scheduler.add_job(_clear_quote_cache,       "cron",     hour=14, minute=0,  day_of_week="mon-fri")  # 收盤後清快取，確保盤後覆盤資料一致
        _bg_scheduler.add_job(_run_補單_job,            "cron",     hour=8,  minute=0)
        _bg_scheduler.add_job(_run_batch_report_job,    "cron",     hour=18, minute=30)
        _bg_scheduler.start()
        print("   ✅ APScheduler 排程已啟動（開盤熱門股 09:06、盤中到價提醒每5分鐘、到期通知 09:00、報價快取清除 09:00、補單 08:00）")

        # 啟動時補跑深度選股（若今日尚未產出）
        try:
            from zoneinfo import ZoneInfo as _ZI
            _now_tp = datetime.now(_ZI("Asia/Taipei"))
            _is_weekday = _now_tp.weekday() < 5
            _after_17 = _now_tp.hour >= 17
            if _is_weekday and _after_17:
                _dc2 = _db_conn()
                _row2 = _dc2.execute(
                    "SELECT updated_at FROM html_pages WHERE key='deep_analysis'"
                ).fetchone()
                _dc2.close()
                _today_str = _now_tp.strftime("%Y-%m-%d")
                _already_ran = _row2 and str(_row2["updated_at"]).startswith(_today_str)
                if not _already_ran:
                    print("   ⚠️ 今日深度選股尚未產出，啟動補跑...")
                    import threading as _th
                    _th.Thread(target=_run_deep_analysis_job, daemon=True).start()
                else:
                    print("   ✅ 今日深度選股已產出，不需補跑")
        except Exception as _ce:
            print(f"   ⚠️ 補跑深度選股檢查失敗：{_ce}")

        # 啟動時補跑開盤熱門股（若今日尚未產出且在交易時段內）
        try:
            from zoneinfo import ZoneInfo as _ZI_op
            _now_op = datetime.now(_ZI_op("Asia/Taipei"))
            _is_wd_op = _now_op.weekday() < 5
            _after_0906 = _now_op.hour > 9 or (_now_op.hour == 9 and _now_op.minute >= 6)
            _before_1400 = _now_op.hour < 14
            if _is_wd_op and _after_0906 and _before_1400:
                _today_op = _now_op.strftime("%Y-%m-%d")
                _dc_op = _db_conn()
                _row_op = _dc_op.execute(
                    "SELECT date FROM opening_picks WHERE date=?", (_today_op,)
                ).fetchone()
                _dc_op.close()
                if not _row_op:
                    print("   ⚠️ 今日開盤熱門股尚未產出，啟動補跑...")
                    import threading as _th_op
                    _th_op.Thread(target=_run_opening_scan_job, daemon=True).start()
                else:
                    print("   ✅ 今日開盤熱門股已產出，不需補跑")
        except Exception as _ce_op:
            print(f"   ⚠️ 補跑開盤熱門股檢查失敗：{_ce_op}")

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

# ── 前端靜態檔案 ──────────────────────────────────────────
_FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")

@app.get("/", include_in_schema=False)
async def serve_homepage(request: Request):
    from fastapi.responses import FileResponse, RedirectResponse
    import os as _os
    # 如果帶有台股 SPA 的參數，自動跳到 /stock/
    qs = str(request.query_params)
    if qs and ("stock=" in qs or "report=" in qs or "tab=" in qs):
        return RedirectResponse(f"/stock/?{qs}", status_code=302)
    # 優先回傳 homepage.html，不存在則 fallback 到 index.html
    hp = _os.path.join(_FRONTEND_DIR, "homepage.html")
    if _os.path.isfile(hp):
        return FileResponse(hp)
    return FileResponse(_os.path.join(_FRONTEND_DIR, "index.html"))

@app.get("/stock", include_in_schema=False)
@app.get("/stock/", include_in_schema=False)
async def serve_stock_app():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(_FRONTEND_DIR, "index.html"))

@app.get("/stock/landing", include_in_schema=False)
@app.get("/stock/landing.html", include_in_schema=False)
async def serve_stock_landing():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "landing.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/landing", include_in_schema=False)
@app.get("/landing.html", include_in_schema=False)
async def redirect_old_landing():
    from fastapi.responses import RedirectResponse
    return RedirectResponse("/stock/landing", status_code=301)

@app.get("/patterns/{filename}.html", include_in_schema=False)
async def serve_patterns_html(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "patterns", f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/patterns", include_in_schema=False)
@app.get("/patterns/", include_in_schema=False)
async def serve_patterns_index():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "patterns", "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/patterns/{locale}/{filename}.html", include_in_schema=False)
async def serve_patterns_locale_html(locale: str, filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "patterns", locale, f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/blog/{filename}.html", include_in_schema=False)
async def serve_blog_html(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "blog", f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/blog", include_in_schema=False)
@app.get("/blog/", include_in_schema=False)
async def serve_blog_index():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "blog", "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/blog/{locale}/{filename}.html", include_in_schema=False)
async def serve_blog_locale_html(locale: str, filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    if locale not in ("en", "ja", "ko"):
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "blog", locale, f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/blog/{locale}", include_in_schema=False)
@app.get("/blog/{locale}/", include_in_schema=False)
async def serve_blog_locale_index(locale: str):
    from fastapi.responses import FileResponse
    import os as _os
    if locale not in ("en", "ja", "ko"):
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "blog", locale, "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

# ---- Tools 路由 ----
_TOOLS_LOCALES = ("en","ja","ko","es","pt","id","de","fr","zh-CN")

@app.get("/tools/tools.css", include_in_schema=False)
async def serve_tools_css():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "tools", "tools.css")
    if _os.path.isfile(path):
        return FileResponse(path, media_type="text/css")
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/tools/{filename}.html", include_in_schema=False)
async def serve_tools_html(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "tools", f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/tools", include_in_schema=False)
@app.get("/tools/", include_in_schema=False)
async def serve_tools_index():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "tools", "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/tools/{locale}/{filename}.html", include_in_schema=False)
async def serve_tools_locale_html(locale: str, filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    if locale not in _TOOLS_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "tools", locale, f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/tools/{locale}", include_in_schema=False)
@app.get("/tools/{locale}/", include_in_schema=False)
async def serve_tools_locale_index(locale: str):
    from fastapi.responses import FileResponse, RedirectResponse
    import os as _os
    if locale not in _TOOLS_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    # 優先回傳該語言的 index.html
    path = _os.path.join(_FRONTEND_DIR, "tools", locale, "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    # 沒有則 fallback 到主索引
    return RedirectResponse(url="/tools/", status_code=302)

# ---- Glossary 術語百科路由 ----
_GLOSSARY_LOCALES = ("en","ja","ko","es","pt","id","de","fr","zh-CN")

@app.get("/glossary/{filename}.html", include_in_schema=False)
async def serve_glossary_html(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "glossary", f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/glossary", include_in_schema=False)
@app.get("/glossary/", include_in_schema=False)
async def serve_glossary_index():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "glossary", "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/glossary/{locale}/{filename}.html", include_in_schema=False)
async def serve_glossary_locale_html(locale: str, filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    if locale not in _GLOSSARY_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "glossary", locale, f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/glossary/{locale}", include_in_schema=False)
@app.get("/glossary/{locale}/", include_in_schema=False)
async def serve_glossary_locale_index(locale: str):
    from fastapi.responses import FileResponse, RedirectResponse
    import os as _os
    if locale not in _GLOSSARY_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "glossary", locale, "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return RedirectResponse(url="/glossary/", status_code=302)

# ---- Comparisons 路由 ----
_COMP_LOCALES = ("en","ja","ko","es","pt","id","de","fr","zh-CN","zh-TW")

@app.get("/comparisons/{filename}.html", include_in_schema=False)
async def serve_comparisons_html(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "comparisons", f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/comparisons", include_in_schema=False)
@app.get("/comparisons/", include_in_schema=False)
async def serve_comparisons_index():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "comparisons", "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/comparisons/{locale}/{filename}.html", include_in_schema=False)
async def serve_comparisons_locale_html(locale: str, filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    if locale not in _COMP_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "comparisons", locale, f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/comparisons/{locale}", include_in_schema=False)
@app.get("/comparisons/{locale}/", include_in_schema=False)
async def serve_comparisons_locale_index(locale: str):
    from fastapi.responses import FileResponse
    import os as _os
    if locale not in _COMP_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "comparisons", locale, "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

# ---- JS 靜態檔路由 (cookie-consent.css, softglow-cookies.js 等) ----
@app.get("/js/{js_filename:path}", include_in_schema=False)
async def serve_js_files(js_filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    if not js_filename.endswith((".css", ".js", ".json")):
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "js", js_filename)
    if _os.path.isfile(path):
        _media = {"css": "text/css", "js": "application/javascript", "json": "application/json"}
        ext = js_filename.rsplit(".", 1)[-1]
        return FileResponse(path, media_type=_media.get(ext, "application/octet-stream"))
    return JSONResponse({"detail": "Not Found"}, status_code=404)

# ---- Common 靜態檔路由 (CSS/JS/JSON) ----
@app.get("/common/{filename}", include_in_schema=False)
async def serve_common_file(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    # Only allow known extensions
    if not filename.endswith((".css", ".js", ".json")):
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "common", filename)
    if _os.path.isfile(path):
        _media = {"css": "text/css", "js": "application/javascript", "json": "application/json"}
        ext = filename.rsplit(".", 1)[-1]
        return FileResponse(path, media_type=_media.get(ext, "application/octet-stream"))
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/{filename}.html", include_in_schema=False)
async def serve_html(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    from fastapi.responses import JSONResponse
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/intro.html", include_in_schema=False)
async def serve_intro():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(_FRONTEND_DIR, "intro.html"))

@app.get("/manifest.json", include_in_schema=False)
async def serve_manifest():
    from fastapi.responses import JSONResponse
    return JSONResponse({
        "name": "線上有位",
        "short_name": "線上有位",
        "description": "台股技術分析輔助工具",
        "start_url": "/stock/",
        "display": "standalone",
        "background_color": "#1a1a18",
        "theme_color": "#1D9E75",
        "orientation": "portrait-primary",
        "icons": [
            {"src": "https://stock-navigator.zeabur.app/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "https://stock-navigator.zeabur.app/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
        ]
    })

@app.get("/favicon.ico", include_in_schema=False)
async def serve_favicon():
    from fastapi.responses import RedirectResponse
    return RedirectResponse("https://stock-navigator.zeabur.app/favicon.ico")

@app.get("/robots.txt", include_in_schema=False)
async def serve_robots():
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse("User-agent: *\nAllow: /\n\nSitemap: https://softglow-ai.com/sitemap.xml")


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
    # A3: 用 pandas rolling 取代 Python loop，大量 K 棒時快 10 倍
    return pd.Series(closes).rolling(period).mean().values



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

        # ── 過濾暫停交易日（開高低收任一為 0，視為無效 K 棒）──
        df = df[(df["Open"] > 0) & (df["High"] > 0) & (df["Low"] > 0) & (df["Close"] > 0)]

        # ── 過濾週末 K 棒（FinMind 偶爾回傳週六資料）──
        df = df[df.index.dayofweek < 5]

        # ── 盤中補今日 K 棒（FinMind tick_snapshot）──
        tz = ZoneInfo("Asia/Taipei")
        now_tw = datetime.now(tz)
        is_weekday = now_tw.weekday() < 5
        in_or_just_after = is_weekday and _dtime(9, 0) <= now_tw.time() <= _dtime(14, 30)
        today_ts = pd.Timestamp(today_str)

        # 盤前（09:00 以前）才刪今日那筆，避免補入假資料
        # 盤中或盤後保留 FinMind 原始收盤價，不刪除
        _qt = _QUOTE_CACHE.get(code)
        _in_session = bool(_qt and (_qt.get("data") or {}).get("in_session"))
        _is_pre_market = now_tw.time() < _dtime(9, 0)
        if _is_pre_market:
            df = df[df.index != today_ts]

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
                    _qt = _QUOTE_CACHE.get(code)
                    if not _qt or not (_qt.get("data") or {}).get("in_session"):
                        cp = 0
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
                            _qt = _QUOTE_CACHE.get(code)
                            if not _qt or not (_qt.get("data") or {}).get("in_session"):
                                cp = 0
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
                            _qt = _QUOTE_CACHE.get(code)
                            if not _qt or not (_qt.get("data") or {}).get("in_session"):
                                cp = 0
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

    # 3. 快取沒命中 → 直接回傳代號（A4: 不再打全量 API，啟動時已預載）
    # 若真的是新上市股票，下次重啟服務時 lifespan 會自動載入
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

    # T2: 根據均線趨勢動態調整權重
    _ma20 = np.mean(closes[-20:]) if len(closes) >= 20 else None
    _ma60 = np.mean(closes[-60:]) if len(closes) >= 60 else None
    _trend_up = _ma20 is not None and _ma60 is not None and _ma20 > _ma60
    _trend_dn = _ma20 is not None and _ma60 is not None and _ma20 < _ma60
    _dyn_adj = {}
    if _trend_up:
        # 上升趨勢：均線支撐更可靠
        _dyn_adj = {"ma20": 3, "ma60": 3, "channel_low": 5}
    elif _trend_dn:
        # 下降趨勢：只有放量止跌才有意義
        _dyn_adj = {"volume_surge": 5, "pullback_low_surge": 7, "ma20": 0, "ma60": 0}
    # 盤整：platform_low 更重要（已有高權重，不需額外調整）

    below = [(p, src, desc) for p, src, desc in candidates if p < price]

    if below:
        prices_only = [p for p, _, _ in below]
        price_range = (price - min(prices_only)) or 1
        def score(item):
            p, src, _ = item
            w = _dyn_adj.get(src, SOURCE_WEIGHT.get(src, 1))  # T2: 動態權重優先
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
    _res_vol_confirmed = False  # T3: 壓力量能確認
    if valid_hi_idx:
        # 取最近30根內的轉折高點，沒有就取最近的一個
        recent_hi = [i for i in valid_hi_idx if i >= n - 60]
        pool = recent_hi if recent_hi else valid_hi_idx
        # 最近且最低的（最近壓力）
        nearest_hi = min(pool, key=lambda i: (highs[i], -(i)))
        resistance = round(float(highs[nearest_hi]), 2)
        # T3: 檢查壓力點的成交量是否爆量（> 均量 1.5 倍）
        _avg_vol = float(np.mean(volumes[max(0,nearest_hi-20):nearest_hi+1])) if nearest_hi > 0 else 1
        _hi_vol = float(volumes[nearest_hi]) if nearest_hi < len(volumes) else 0
        _res_vol_confirmed = _hi_vol > _avg_vol * 1.5
        _vol_tag = "，爆量高點" if _res_vol_confirmed else ""
        resistance_desc = f"轉折高點（{n - nearest_hi}根前{_vol_tag}）"
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
    c1, o1, h1, l1     = closes[-2], opens[-2], highs[-2], lows[-2]
    c2, o2, h2, l2     = closes[-3], opens[-3], highs[-3], lows[-3]

    body0         = abs(c0 - o0)
    body1         = abs(c1 - o1)
    body2         = abs(c2 - o2)
    upper_shadow0 = h0 - max(c0, o0)
    lower_shadow0 = min(c0, o0) - l0
    range0        = max(h0 - l0, 0.001)
    range1        = max(h1 - l1, 0.001)
    range2        = max(h2 - l2, 0.001)

    avg_vol      = sum(volumes[-6:-1]) / 5 if n >= 6 else (sum(volumes[:-1]) / max(len(volumes)-1, 1))
    vol_surge    = v0 > avg_vol * 1.3
    is_downtrend = closes[-1] < closes[-5] if n >= 5 else False
    is_uptrend   = closes[-1] > closes[-5] if n >= 5 else False

    # 1. 量增大紅棒 / 量增大黑棒（最優先）
    if vol_surge and (body0 >= range0 * 0.5) and (c0 > o0):
        return "量增大紅棒（突破確認）", 0.62
    if vol_surge and (body0 >= range0 * 0.5) and (c0 < o0):
        return "量增大黑棒（跌破確認）", 0.62

    # 2. 連三紅 / 連三黑（三根連續同向收盤遞升/遞降）
    if (c0 > o0) and (c1 > o1) and (c2 > o2) and c0 > c1 and c1 > c2:
        return "連三紅（多頭強勢格局）", 0.60
    if (c0 < o0) and (c1 < o1) and (c2 < o2) and c0 < c1 and c1 < c2:
        return "連三黑（空頭強勢格局）", 0.60

    # 3. 早晨之星（下跌後底部三根反轉：大黑→小實體→大紅）
    if (is_downtrend
            and c2 < o2 and body2 >= range2 * 0.4    # 第1棒：實體夠大的黑棒
            and body1 <= range1 * 0.3                 # 第2棒（星）：小實體
            and c0 > o0                                # 第3棒：紅棒
            and c0 > (c2 + o2) / 2):                  # 第3棒收盤超過第1棒中點
        return "早晨之星（底部反轉訊號）", 0.60

    # 4. 黃昏之星（上漲後頂部三根反轉：大紅→小實體→大黑）
    if (is_uptrend
            and c2 > o2 and body2 >= range2 * 0.4    # 第1棒：實體夠大的紅棒
            and body1 <= range1 * 0.3                 # 第2棒（星）：小實體
            and c0 < o0                                # 第3棒：黑棒
            and c0 < (c2 + o2) / 2):                  # 第3棒收盤低於第1棒中點
        return "黃昏之星（頂部反轉訊號）", 0.60

    # 5. 多頭吞噬（前黑棒被今紅棒完全吞噬，下跌趨勢中）
    if (is_downtrend
            and c1 < o1               # 前棒：黑
            and c0 > o0               # 今棒：紅
            and o0 <= c1              # 今開 ≤ 前收
            and c0 >= o1):            # 今收 ≥ 前開（完全吞噬）
        return "多頭吞噬（強力底部訊號）", 0.58

    # 6. 空頭吞噬（前紅棒被今黑棒完全吞噬，上升趨勢中）
    if (is_uptrend
            and c1 > o1               # 前棒：紅
            and c0 < o0               # 今棒：黑
            and o0 >= c1              # 今開 ≥ 前收
            and c0 <= o1):            # 今收 ≤ 前開（完全吞噬）
        return "空頭吞噬（強力頂部訊號）", 0.58

    # 7. 錘子線：下影線夠長（>=40%全幅）、下影線>=實體1.5倍、上影線短（<=20%全幅）
    if (is_downtrend and (lower_shadow0 >= range0 * 0.4)
            and (lower_shadow0 >= body0 * 1.5)
            and (upper_shadow0 <= range0 * 0.2)):
        return "低檔錘子線（底部承接力道強）", 0.53

    # 8. 流星線：上影線夠長（>=40%全幅）、上影線>=實體1.5倍、下影線短（<=20%全幅）
    if (is_uptrend and (upper_shadow0 >= range0 * 0.4)
            and (upper_shadow0 >= body0 * 1.5)
            and (lower_shadow0 <= range0 * 0.2)):
        return "高檔流星線（多頭上攻力竭）", 0.53

    # 9. 十字星 Doji（實體 ≤ 全幅 10%，多空分歧）
    if body0 <= range0 * 0.1:
        return "十字星 Doji（多空分歧，等待方向確認）", 0.52

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


def detect_reversal_pattern(highs, lows, closes, volumes=None):
    """偵測反轉型態：W底、M頭、頭肩底、頭肩頂"""
    LOOKBACK = min(len(closes), 120)
    _offset  = len(closes) - LOOKBACK
    _h = highs[-LOOKBACK:]; _l = lows[-LOOKBACK:]
    _v = volumes[-LOOKBACK:] if volumes is not None and len(volumes) >= LOOKBACK else None
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
                # T8: 量能驗證 — 第二底量應比第一底少（量縮止跌），突破頸線應放量
                _vol_confirmed = True
                _vol_note = ""
                if _v is not None:
                    _vol_bot1 = float(_v[l1]) if l1 < len(_v) else 0
                    _vol_bot2 = float(_v[l2]) if l2 < len(_v) else 0
                    if _vol_bot2 > _vol_bot1 * 1.1:
                        _vol_confirmed = False
                        _vol_note = "，量能未確認（第二底量未縮）"
                return {
                    "type": "double_bottom", "desc": "W底（雙底）",
                    "neckline": round(neck, 2), "target": float(target), "broken": broken,
                    "vol_confirmed": _vol_confirmed,  # T8
                    "position_desc": f"{'已突破頸線' if broken else '接近頸線'} {neck:.1f}，目標 {target}{_vol_note}",
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


def detect_gann_recross(closes, highs, lows, volumes, ma_period=20, max_bars=2):
    """
    葛蘭碧八大法則買點偵測（買1/2/3/4合併版）
    時效限制：訊號觸發根起 ≤ max_bars 根內有效（預設2根）
    MA60 額外條件：MA20 必須在 MA60 上方（多頭排列）

    買1/4：收盤從均線下方穿越到上方（站回/超跌反彈），觸發根起 ≤2根
    買2  ：收盤在均線上方，低點曾觸碰均線 ±1% 後反彈，觸發根起 ≤2根
    買3  ：收盤連續在均線上方，低點最近一次接近均線後止跌向上，觸發根起 ≤2根

    回傳：(訊號是否成立, 均線值, 均線名稱, 防守建議, 買點類型描述)
    """
    n = len(closes)
    if n < ma_period + 5:
        return False, None, None, None, None

    ma = np.full(n, np.nan)
    for i in range(ma_period - 1, n):
        ma[i] = closes[i - ma_period + 1: i + 1].mean()

    curr_ma = ma[-1]
    if np.isnan(curr_ma):
        return False, None, None, None, None

    # MA60 額外條件：需要 MA20 在 MA60 上方
    if ma_period == 60:
        ma20 = np.full(n, np.nan)
        for i in range(19, n):
            ma20[i] = closes[i - 19: i + 1].mean()
        if np.isnan(ma20[-1]) or ma20[-1] <= ma[-1]:
            return False, None, None, None, None

    # 均線方向：水平或向上才算有效（下降趨勢中的反彈不算）
    ma_slope_ok = ma[-1] >= ma[-(min(5, n))]
    if not ma_slope_ok:
        return False, None, None, None, None

    name = f"MA{ma_period}"
    stop = round(float(curr_ma) * 0.985, 2)

    TOUCH_BAND = 0.01   # 買2/3：低點距均線 ±1% 算觸碰

    # ── 買1/4：找最近一次「從下方穿越到上方」的觸發根 ──
    # 往回掃，找 closes[i-1] < ma[i-1] 且 closes[i] > ma[i] 的最近那根
    trigger_b1 = None
    for i in range(n - 1, ma_period, -1):
        if np.isnan(ma[i]) or np.isnan(ma[i - 1]):
            continue
        if closes[i - 1] < ma[i - 1] and closes[i] > ma[i]:
            trigger_b1 = i
            break
    if trigger_b1 is not None and (n - 1 - trigger_b1) <= max_bars:
        # T5: 站回均線當天量能過濾
        _avg_vol_20 = float(np.mean(volumes[max(0,trigger_b1-20):trigger_b1])) if trigger_b1 > 0 else 1
        _trigger_vol = float(volumes[trigger_b1])
        _vol_weak = _trigger_vol < _avg_vol_20 * 0.8  # 縮量站回
        buy_type = "買1（站回均線）" if ma[-1] >= ma[-(min(5, n))] else "買4（超跌反彈）"
        if _vol_weak:
            buy_type += "⚠縮量，需量增確認"
        return True, round(float(curr_ma), 2), name, stop, buy_type

    # ── 買2：收盤在均線上方，低點觸碰均線後反彈 ──
    # 找最近一次 closes[i] > ma[i] 且 lows[i] <= ma[i] * (1 + TOUCH_BAND) 的那根
    trigger_b2 = None
    for i in range(n - 1, ma_period, -1):
        if np.isnan(ma[i]):
            continue
        if closes[i] > ma[i] and lows[i] <= ma[i] * (1 + TOUCH_BAND):
            # 確認前一根也在均線上方（不是剛穿越，那是買1）
            if not np.isnan(ma[i - 1]) and closes[i - 1] > ma[i - 1]:
                trigger_b2 = i
                break
    if trigger_b2 is not None and (n - 1 - trigger_b2) <= max_bars:
        return True, round(float(curr_ma), 2), name, stop, "買2（回測不破）"

    # ── 買3：連續在均線上方，最近低點接近均線後止跌 ──
    # 條件：最近5根收盤都在均線上方，且其中有一根低點接近均線，且最新根收盤 > 前一根收盤
    if n >= ma_period + 5:
        recent_5_above = all(
            not np.isnan(ma[-(j + 1)]) and closes[-(j + 1)] > ma[-(j + 1)]
            for j in range(5)
        )
        had_touch = any(
            not np.isnan(ma[-(j + 1)]) and lows[-(j + 1)] <= ma[-(j + 1)] * (1 + TOUCH_BAND)
            for j in range(1, 6)
        )
        price_rising = closes[-1] > closes[-2]
        if recent_5_above and had_touch and price_rising:
            # 找觸碰那根當觸發根
            trigger_b3 = None
            for j in range(1, 6):
                i = n - 1 - j
                if not np.isnan(ma[i]) and lows[i] <= ma[i] * (1 + TOUCH_BAND):
                    trigger_b3 = i
                    break
            if trigger_b3 is not None and (n - 1 - trigger_b3) <= max_bars:
                return True, round(float(curr_ma), 2), name, stop, "買3（上方止跌）"

    return False, None, None, None, None


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

def _get_analyze_cache_ttl() -> int:
    """動態快取 TTL：盤中 15 分鐘，盤後到隔天 09:00 台北時間"""
    from zoneinfo import ZoneInfo
    import datetime as _dt
    now = datetime.now(ZoneInfo("Asia/Taipei"))
    weekday = now.weekday()  # 0=週一, 6=週日
    hour = now.hour + now.minute / 60
    is_trading = weekday < 5 and 9.0 <= hour < 13.5
    if is_trading:
        return 900  # 盤中 15 分鐘
    # 盤後：計算到隔天 09:00（跳過週末）
    next_open = now.replace(hour=9, minute=0, second=0, microsecond=0)
    if hour >= 9:
        next_open += _dt.timedelta(days=1)
    while next_open.weekday() >= 5:
        next_open += _dt.timedelta(days=1)
    return max(60, int((next_open - now).total_seconds()))

def _cache_get(key: str):
    entry = _analyze_cache.get(key)
    if entry and (_time.time() - entry["ts"]) < _get_analyze_cache_ttl():
        return entry["data"]
    return None

def _cache_set(key: str, data: dict):
    _analyze_cache[key] = {"ts": _time.time(), "data": data}
    if len(_analyze_cache) > 200:
        cutoff = _time.time() - _get_analyze_cache_ttl()
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

# B5: context manager 版本，自動 close + commit（新程式碼優先用這個）
from contextlib import contextmanager as _contextmanager
@_contextmanager
def _db():
    """用法：with _db() as conn: conn.execute(...)"""
    conn = _db_conn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

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
        CREATE TABLE IF NOT EXISTS counters (
            key   TEXT PRIMARY KEY,
            value INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS opening_picks (
            date       TEXT PRIMARY KEY,
            data       TEXT,
            updated_at TEXT
        );
        CREATE TABLE IF NOT EXISTS portfolios (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email  TEXT NOT NULL,
            stock_id    TEXT NOT NULL,
            stock_name  TEXT DEFAULT '',
            cost_price  REAL NOT NULL,
            created_at  TEXT DEFAULT (datetime('now','+8 hours')),
            UNIQUE(user_email, stock_id)
        );
        CREATE TABLE IF NOT EXISTS html_pages (
            key         TEXT PRIMARY KEY,
            content     TEXT NOT NULL,
            updated_at  TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS chat_messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT NOT NULL,
            is_paid    INTEGER DEFAULT 0,
            stock_tag  TEXT DEFAULT '',
            message    TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS threads_tokens (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            token        TEXT NOT NULL,
            account_name TEXT NOT NULL DEFAULT '',
            created_at   TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS forum_posts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER DEFAULT NULL,
            nickname   TEXT NOT NULL DEFAULT '匿名',
            title      TEXT NOT NULL,
            content    TEXT NOT NULL,
            stock_code TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','+8 hours')),
            updated_at TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS forum_comments (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id    INTEGER NOT NULL,
            user_id    INTEGER DEFAULT NULL,
            nickname   TEXT NOT NULL DEFAULT '匿名',
            content    TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now','+8 hours'))
        );
    """)
    conn.commit()

    # 自動補上新欄位（舊資料庫升級用）
    new_columns = [
        ("members", "session_id", "TEXT DEFAULT NULL"),
        ("members", "token_ver",  "INTEGER DEFAULT 0"),
        ("members", "expire_at",  "TEXT DEFAULT NULL"),
        ("members", "last_login", "TEXT DEFAULT NULL"),
        ("members", "merchant_trade_no", "TEXT DEFAULT NULL"),
        ("query_log", "ip",                   "TEXT NOT NULL DEFAULT ''"),
        ("members",   "password_changed_at",  "TEXT DEFAULT NULL"),
        ("members",   "last_expire_notice_date", "TEXT DEFAULT NULL"),
        ("members",   "referral_unlocked",       "INTEGER DEFAULT 0"),
        ("members",   "referral_expire_date",    "TEXT DEFAULT NULL"),
        ("members",   "referral_rewarded_count", "INTEGER DEFAULT 0"),
        ("query_log",       "report_count",    "INTEGER DEFAULT 0"),
        ("pending_orders",  "invoice_type",    "TEXT DEFAULT NULL"),
        ("pending_orders",  "invoice_carrier", "TEXT DEFAULT NULL"),
        ("chat_messages",   "msg_type",        "TEXT DEFAULT 'text'"),
        ("chat_messages",   "image_data",      "TEXT DEFAULT NULL"),
        ("members",         "nickname",        "TEXT DEFAULT NULL"),
    ]
    for table, col, coldef in new_columns:
        try:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {coldef}")
            conn.commit()
            print(f"   ✅ 資料庫補欄位：{table}.{col}")
        except Exception:
            pass  # 欄位已存在，忽略

    # 自動建立管理員帳號（已存在則不覆蓋）
    # B4: 密碼改從環境變數讀取，不再寫死在原始碼
    ADMIN_EMAIL  = os.environ.get("ADMIN_EMAIL", "watione@yahoo.com.tw")
    ADMIN_PWD    = os.environ.get("ADMIN_DEFAULT_PWD", "630428")
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
    if not row:
        print(f"[AUTH] user not found: sub={payload.get('sub')}")
        return None
    if row["token_ver"] != payload.get("ver", 0):
        print(f"[AUTH] token_ver mismatch: db={row['token_ver']} jwt={payload.get('ver', 0)} email={row['email']}")
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

REPORT_INJECT = """<style>#reportShareBtn{position:fixed;top:16px;right:16px;z-index:1001;background:#1D9E75;color:#fff;border:none;border-radius:20px;padding:8px 16px;font-size:14px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.2);font-family:inherit;}#chat-entry-btn{position:fixed;bottom:20px;right:16px;z-index:9999;background:linear-gradient(135deg,#db2777,#7c3aed);color:#fff;border:none;border-radius:24px;padding:10px 18px;font-size:14px;font-weight:600;cursor:pointer;box-shadow:0 4px 16px rgba(124,58,237,.4);display:flex;align-items:center;gap:6px;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,'Noto Sans TC',sans-serif}#chat-entry-btn:hover{opacity:.9}</style><button id="reportShareBtn" onclick="var url=window.location.href;var title=document.title||'線上有位個股報告';if(navigator.share){navigator.share({title:title,url:url});}else{navigator.clipboard.writeText(url).then(function(){var b=document.getElementById('reportShareBtn');b.textContent='✓ 已複製';setTimeout(function(){b.textContent='🔗 分享';},2000);});}">🔗 分享</button><a id="chat-entry-btn" href="/chat.html" target="_blank">💬 聊天室</a><div style="background:#fffbeb;border:1px solid #fcd34d;border-radius:8px;padding:8px 14px;margin:12px 0;font-size:12px;color:#92400e">📌 分析以最新 K 線為基準，收盤後 K 線確定分析最準確。報告快取當日，如需最新分析請回主頁重新產出。</div>"""


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

    # 日K：若最後一根不是今日，嘗試從 _QUOTE_CACHE 補今日即時K棒
    if tf.upper() == "D" and records:
        from zoneinfo import ZoneInfo as _ZI
        _tw_today = datetime.now(_ZI("Asia/Taipei")).strftime("%Y-%m-%d")
        if records[-1]["date"] != _tw_today:
            _code = stock_id.strip().upper().replace(".TW", "").replace(".TWO", "")
            _qc = _QUOTE_CACHE.get(_code)
            # 快取不存在或已過期，主動呼叫 get_quote() 取得即時報價
            if not (_qc and (_qc["expires"] == 0 or _time_mod.time() < _qc["expires"])):
                try:
                    get_quote(_code, user=None)
                    _qc = _QUOTE_CACHE.get(_code)
                except Exception:
                    _qc = None
            if _qc and (_qc["expires"] == 0 or _time_mod.time() < _qc["expires"]):
                _q = _qc["data"]
                _c = _q.get("price")
                _o = _q.get("open") or _c
                _h = _q.get("high") or _c
                _l = _q.get("low") or _c
                _v = _q.get("volume") or 0
                if _c:
                    records.append({
                        "date": _tw_today,
                        "open": _o, "high": _h, "low": _l, "close": _c,
                        "volume": int(_v) if _v else 0,
                    })

    return {"symbol": symbol, "tf": tf, "count": len(records), "bars": records}


def _classify_kbar_simple(opens, highs, lows, closes, volumes) -> dict:
    """簡易K棒分類：大紅/小紅/十字星/小黑/大黑/錘子線/流星線 + 連K天數 + 量能說明"""
    if len(closes) < 3:
        return {}
    o, h, l, c = float(opens[-1]), float(highs[-1]), float(lows[-1]), float(closes[-1])
    body     = c - o
    body_pct = body / o * 100 if o > 0 else 0
    rng      = h - l or 0.001
    upper    = h - max(o, c)
    lower    = min(o, c) - l
    is_red   = c >= o
    avg_vol  = float(np.mean(volumes[-6:-1])) if len(volumes) >= 6 else float(np.mean(volumes[:-1]))
    today_vol = float(volumes[-1])
    vol_surge = avg_vol > 0 and today_vol > avg_vol * 1.3

    if abs(body) / rng < 0.15:
        ktype, meaning, direction = "十字星", "多空交戰，方向不明，等待次日確認", "neutral"
    elif lower >= abs(body) * 2 and upper <= abs(body) * 0.5:
        note = "量縮更具底部意義" if not vol_surge else "量增止跌訊號更強"
        ktype, meaning, direction = "錘子線", f"下引線長，低位有強撐；{note}", "bullish"
    elif upper >= abs(body) * 2 and lower <= abs(body) * 0.5:
        ktype, meaning, direction = "流星線", "上引線長，高位賣壓重，注意回調風險", "bearish"
    elif is_red and body_pct >= 2.0:
        note = "量增突破力道強" if vol_surge else "注意是否有量能配合"
        ktype, meaning = "大紅棒", f"多頭強攻，實體漲幅 {body_pct:.1f}%；{note}"
        direction = "bullish"
    elif is_red:
        ktype, meaning, direction = "小紅棒", "溫和上漲，多頭動能一般，觀察是否持續", "slightly_bullish"
    elif body_pct <= -2.0:
        ktype, meaning, direction = "大黑棒", f"空頭強殺，實體跌幅 {abs(body_pct):.1f}%，留意賣壓是否持續", "bearish"
    else:
        ktype, meaning, direction = "小黑棒", "溫和下跌，觀察支撐是否守住", "slightly_bearish"

    streak = 0
    for i in range(-1, -min(11, len(closes)), -1):
        bar_red = float(closes[i]) >= float(opens[i])
        if (is_red and bar_red) or (not is_red and not bar_red):
            streak += 1
        else:
            break

    vol_note = ""
    if avg_vol > 0:
        ratio = today_vol / avg_vol
        if vol_surge and is_red:
            vol_note = f"量增紅K（今量是均量 {ratio:.1f}x），多頭最強格局"
        elif vol_surge and not is_red:
            vol_note = f"量增黑K（今量是均量 {ratio:.1f}x），賣壓沉重"
        elif ratio < 0.7:
            vol_note = f"縮量（今量僅均量 {ratio:.1f}x），{'拉回偏健康' if is_red else '跌勢衰竭跡象'}"

    return {
        "type": ktype, "meaning": meaning, "direction": direction,
        "body_pct": round(body_pct, 2),
        "streak": streak, "streak_dir": "紅" if is_red else "黑",
        "vol_note": vol_note,
    }


def _ma_alignment_desc(ma_values: dict) -> dict:
    """描述均線多空排列"""
    ma5  = ma_values.get("ma5")
    ma20 = ma_values.get("ma20")
    ma60 = ma_values.get("ma60")
    if None in (ma5, ma20, ma60):
        if ma5 and ma20:
            d = "bullish" if ma5 > ma20 else "bearish"
            return {"text": f"MA5({ma5:.1f}) {'>' if ma5>ma20 else '<'} MA20({ma20:.1f})，{'短線多頭' if ma5>ma20 else '短線偏空'}", "direction": d}
        return {"text": "均線資料不足", "direction": "neutral"}
    if ma5 > ma20 > ma60:
        return {"text": f"多頭排列 MA5({ma5:.1f}) > MA20({ma20:.1f}) > MA60({ma60:.1f})", "direction": "bullish"}
    if ma5 < ma20 < ma60:
        return {"text": f"空頭排列 MA5({ma5:.1f}) < MA20({ma20:.1f}) < MA60({ma60:.1f})", "direction": "bearish"}
    if ma5 > ma20 and ma20 < ma60:
        return {"text": f"短多長空，MA5({ma5:.1f}) > MA20 但 MA20({ma20:.1f}) < MA60({ma60:.1f})，趨勢轉換中", "direction": "neutral"}
    if ma5 < ma20 and ma20 > ma60:
        return {"text": f"短空中多，MA5({ma5:.1f}) 回落但 MA20({ma20:.1f}) 仍在 MA60({ma60:.1f}) 以上", "direction": "slightly_bearish"}
    return {"text": f"均線糾結，MA5={ma5:.1f} MA20={ma20:.1f} MA60={ma60:.1f}，等待方向明確", "direction": "neutral"}


def _kd_status_desc(k_arr, d_arr) -> dict:
    """描述KD位置與金死叉"""
    vk = k_arr[~np.isnan(k_arr)]
    vd = d_arr[~np.isnan(d_arr)]
    if len(vk) < 2 or len(vd) < 2:
        return {"text": "KD資料不足", "direction": "neutral", "k": None, "d": None}
    k_now, d_now   = float(vk[-1]), float(vd[-1])
    k_prev, d_prev = float(vk[-2]), float(vd[-2])
    golden = k_now > d_now and k_prev <= d_prev
    death  = k_now < d_now and k_prev >= d_prev
    if k_now >= 80:
        zone, zone_dir = "超買區（>80），注意高檔鈍化風險", "warning"
    elif k_now <= 20:
        zone, zone_dir = "超賣區（<20），關注底部反彈機會", "bullish"
    elif k_now >= 50:
        zone, zone_dir = "多方優勢區（50~80）", "bullish"
    else:
        zone, zone_dir = "空方優勢區（20~50）", "bearish"
    cross = "，本日金叉（多方進場訊號）" if golden else ("，本日死叉（空方訊號）" if death else "")
    direction = "bullish" if golden else ("bearish" if death else zone_dir)
    return {
        "text": f"K={k_now:.1f}，D={d_now:.1f}，位於{zone}{cross}",
        "direction": direction, "k": k_now, "d": d_now,
        "golden_cross": golden, "death_cross": death,
    }


def _macd_status_desc(macd_line, macd_sig, macd_hist) -> dict:
    """描述MACD DIF/DEA關係"""
    vl = macd_line[~np.isnan(macd_line)]
    vs = macd_sig[~np.isnan(macd_sig)]
    vh = macd_hist[~np.isnan(macd_hist)]
    if len(vl) < 2 or len(vs) < 2 or len(vh) < 2:
        return {"text": "MACD資料不足", "direction": "neutral", "dif": None, "dea": None}
    dif, dea = float(vl[-1]), float(vs[-1])
    hist_rising = float(vh[-1]) > float(vh[-2])
    above_zero  = dif > 0
    dif_above   = dif > dea
    hist_txt    = "柱體擴大↑" if hist_rising else "柱體縮小↓"
    if above_zero and dif_above and hist_rising:
        signal, direction = "多頭強勢", "bullish"
    elif above_zero and dif_above:
        signal, direction = "多頭但動能趨緩", "slightly_bullish"
    elif above_zero:
        signal, direction = "多頭轉弱，注意死叉風險", "slightly_bearish"
    elif hist_rising:
        signal, direction = "空頭反彈，觀察能否穿越0軸", "neutral"
    else:
        signal, direction = "空頭格局", "bearish"
    return {
        "text": f"DIF={dif:.3f}（{'0軸以上' if above_zero else '0軸以下'}），DEA={dea:.3f}（{'DIF在DEA上方' if dif_above else 'DIF在DEA下方'}），{hist_txt} → {signal}",
        "direction": direction, "dif": dif, "dea": dea,
    }


def _vol_analysis_desc(volumes, closes, opens) -> dict:
    """分析近5日 vs 20日量能（Trading_Volume 單位為股，除以1000轉換為張）"""
    vols = [float(v) / 1000 for v in volumes if v > 0]
    if len(vols) < 20:
        return {"text": "量能資料不足", "ratio": 1.0, "avg_5": 0, "avg_20": 0}
    avg_5  = sum(vols[-5:]) / 5
    avg_20 = sum(vols[-20:]) / 20
    ratio  = avg_5 / avg_20 if avg_20 > 0 else 1.0
    is_red = len(closes) >= 1 and len(opens) >= 1 and float(closes[-1]) >= float(opens[-1])
    if ratio >= 1.5:
        note = "量增紅K最強格局" if is_red else "量增黑K，賣壓沉重"
    elif ratio >= 1.2:
        note = "量略放大" + ("，持續追蹤" if is_red else "，注意跌破支撐")
    elif ratio <= 0.7:
        note = "縮量" + ("拉回偏健康" if is_red else "，跌勢衰竭跡象")
    else:
        note = "量能正常範圍"
    return {
        "text": f"近5日均量 {round(avg_5):,} 張，20日均量 {round(avg_20):,} 張，比值 {ratio:.2f}x，{note}",
        "ratio": round(ratio, 2), "avg_5": round(avg_5), "avg_20": round(avg_20),
    }


def _fetch_institutional_safe(stock_id: str) -> dict:
    """Best-effort FinMind 法人資料，失敗回傳 {}"""
    try:
        import sys as _sys, os as _os
        _sp = _os.path.join(_os.path.dirname(__file__), "stock_picker")
        if _sp not in _sys.path:
            _sys.path.insert(0, _sp)
        from crawler import fetch_institutional
        rows = fetch_institutional(stock_id, days=20)
        if not rows:
            return {}
        consecutive_buy = 0
        for r in reversed(rows):
            if r["total"] > 0:
                consecutive_buy += 1
            else:
                break
        inst_5d  = rows[-5:] if len(rows) >= 5 else rows
        foreign5 = sum(r.get("foreign", 0) for r in inst_5d)
        invest5  = sum(r.get("invest",  0) for r in inst_5d)
        dealer5  = sum(r.get("dealer",  0) for r in inst_5d)
        total5   = sum(r.get("total",   0) for r in inst_5d)
        def _dir(v): return "買超" if v > 0 else ("賣超" if v < 0 else "持平")
        extra = f"，法人連買 {consecutive_buy} 日" if consecutive_buy >= 2 else ""
        return {
            "consecutive_buy_days": consecutive_buy,
            "total_5d": total5, "foreign_5d": foreign5,
            "invest_5d": invest5, "dealer_5d": dealer5,
            "foreign_dir": _dir(foreign5), "invest_dir": _dir(invest5),
            "summary": f"近5日三大法人合計 {total5:+,} 張（外資 {foreign5:+,}・投信 {invest5:+,}・自營 {dealer5:+,}）{extra}",
        }
    except Exception as _e:
        print(f"[analyze] institutional best-effort failed {stock_id}: {_e}")
        return {}


def _individualized_risk(price, support, resistance, rr_ratio,
                          kd_info: dict, macd_info: dict,
                          kbar_info: dict, inst: dict) -> list[str]:
    """根據各股實際數據產生個股化風險提示"""
    risks = []
    if rr_ratio < 1.0:
        risks.append(f"損益比 {rr_ratio}，現價距壓力 {resistance} 空間不足，進場時機需審慎")
    k_val = kd_info.get("k")
    if k_val and k_val >= 80:
        risks.append(f"KD={k_val:.0f} 進入超買區，高檔容易鈍化，追高風險增加")
    elif kd_info.get("death_cross"):
        risks.append(f"KD 剛發生死叉（K={k_val:.0f}），動能轉弱，留意後續賣壓")
    dif_val = macd_info.get("dif")
    if dif_val is not None and dif_val < -0.5:
        risks.append(f"MACD DIF={dif_val:.3f} 在 0 軸深處，空頭動能強，反彈需謹慎")
    elif macd_info.get("direction") == "slightly_bearish":
        risks.append("MACD 多頭轉弱，接近死叉，注意動能確認")
    supp_dist = (price - support) / price * 100
    if supp_dist > 8:
        risks.append(f"支撐 {support} 距現價 {supp_dist:.1f}%，停損空間較大，建議控制部位大小")
    total5 = inst.get("total_5d", 0)
    if total5 < -500:
        risks.append(f"法人近5日賣超 {total5:,} 張，籌碼持續外流，需謹慎追多")
    if kbar_info.get("direction") == "bearish":
        risks.append(f"K棒出現{kbar_info.get('type','')}，空頭訊號，建議等止跌確認後再進場")
    if not risks:
        risks.append(f"技術面無明顯警示，持續追蹤均線支撐 {support} 是否守住")
    return risks


def _do_analyze(stock_id: str, tf: str = "D",
                ma1: int = 5, ma2: int = 10, ma3: int = 20, ma4: int = 60, ma5: int = 120,
                user: dict | None = None):
    """核心分析邏輯（不含驗證），供 analyze() 和 batch_analyze() 共用"""
    # 快取：同股票+時間框架+當天，盤中 15 分鐘更新，收盤後固定到隔天
    _cache_key = f"{stock_id.strip().upper()}_{tf.upper()}_{_taipei_today().replace('-', '')}"
    cached = _cache_get(_cache_key)
    if cached:
        # 盤中即使快取命中，仍用最新報價覆蓋 price/change/change_pct
        # 避免 _analyze_cache 15 分鐘內鎖住舊成交價
        if _is_trading_session():
            _sid_c = stock_id.strip().upper()
            _qc_c  = _QUOTE_CACHE.get(_sid_c)
            if not _qc_c or _qc_c.get("expires", 0) < _time_mod.time():
                try:
                    get_quote(_sid_c, user=None)
                    _qc_c = _QUOTE_CACHE.get(_sid_c)
                except Exception:
                    _qc_c = None
            if _qc_c and _qc_c.get("data", {}).get("price"):
                _live = float(_qc_c["data"]["price"])
                if _live > 0:
                    cached = dict(cached)
                    cached["price"]      = round(_live, 2)
                    cached["change"]     = _qc_c["data"].get("change")
                    cached["change_pct"] = _qc_c["data"].get("change_pct")
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

    # 一律用即時報價覆蓋現價（FinMind 最新成交價/收盤價，避免 Yahoo K 線延遲導致現價過期）
    _sid = stock_id.strip().upper()
    _qc = _QUOTE_CACHE.get(_sid)
    if not _qc or _qc.get("expires", 0) < _time_mod.time():
        try:
            get_quote(_sid, user=None)
            _qc = _QUOTE_CACHE.get(_sid)
        except Exception:
            _qc = None
    if _qc and _qc.get("data", {}).get("price"):
        _live_price = float(_qc["data"]["price"])
        if _live_price > 0:
            price = round(_live_price, 2)

    # 股名
    stock_name = get_stock_name(symbol)

    # 均線
    ma_periods = [p for p in [ma1, ma2, ma3, ma4, ma5] if p and p > 0]
    ma_values = {f"ma{p}": safe_float(calc_ma(closes, p)[-1]) for p in ma_periods}

    # 趨勢（統一用 MA20 vs MA60，與多空雷達①趨勢一致）
    _ma20_last = calc_ma(closes, 20)[-1]
    _ma60_last = calc_ma(closes, 60)[-1]
    if not np.isnan(_ma20_last) and not np.isnan(_ma60_last):
        trend = "上升趨勢" if _ma20_last > _ma60_last * 1.005 else "下降趨勢" if _ma20_last < _ma60_last * 0.995 else "盤整"
    else:
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
    reversal = detect_reversal_pattern(highs, lows, closes, volumes)
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
            # fallback：軌道上緣估算 → 波段等幅推算（創新高時無前高可用）
            if channel and channel.get("target1") and channel["target1"] > price * (1 + MIN_RES_DIST):
                alt_res = round(float(channel["target1"]), 2)
                alt_res_desc = "軌道目標價"
            else:
                # 波段等幅投影：(近60根高點 - 近60根低點) + 近60根高點
                _swing_high = float(highs[-60:].max()) if len(highs) >= 60 else float(highs.max())
                _swing_low  = float(lows[-60:].min())  if len(lows)  >= 60 else float(lows.min())
                _swing_proj = round(_swing_high + (_swing_high - _swing_low), 2)
                if _swing_proj > price * (1 + MIN_RES_DIST):
                    alt_res = _swing_proj
                    alt_res_desc = "波段等幅目標（突破後推算）"
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

    # K棒型態辨識（B3: 統一為單一函式，同時回傳型態名、預警、方向、勝率）
    kbar_pattern, kbar_warning, kbar_dir, kbar_win_rate = detect_kbar_pattern(opens, highs, lows, closes)

    # 葛蘭碧（加量能過濾）
    ma20_arr = calc_ma(closes, 20)
    buy_idx, sell_idx, buy_stops = calc_gann_filtered(closes, highs, lows, volumes, 20)

    # 葛蘭碧買點偵測（買1/2/3/4，MA20 / MA60，≤2根時效）
    gann_ma20_signal, gann_ma20_val, gann_ma20_name, gann_ma20_stop, gann_ma20_type = detect_gann_recross(closes, highs, lows, volumes, 20)
    gann_ma60_signal, gann_ma60_val, gann_ma60_name, gann_ma60_stop, gann_ma60_type = detect_gann_recross(closes, highs, lows, volumes, 60)
    # 優先用 MA60（需 MA20 在 MA60 上方），其次 MA20
    gann_recross = None
    if gann_ma60_signal:
        gann_recross = {"ma": gann_ma60_name, "val": gann_ma60_val, "stop": gann_ma60_stop, "type": gann_ma60_type}
    elif gann_ma20_signal:
        gann_recross = {"ma": gann_ma20_name, "val": gann_ma20_val, "stop": gann_ma20_stop, "type": gann_ma20_type}

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
    min_stop  = round(price * 0.98, 2)   # 最近不能超過現價 -2%（太緊容易被洗）
    max_stop  = round(price * 0.90, 2)   # 最遠不超過現價 -10%（太遠失去意義）
    # B2: 修正邏輯 — raw_stop 夾在 max_stop ~ min_stop 之間
    # 原寫法 min(min_stop, max(...)) 會讓結果永遠 ≤ min_stop，防守位被壓死在 -2%
    stop_loss = max(max_stop, min(raw_stop, min_stop))

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

    # B3: K 線型態勝率統一從 detect_kbar_pattern 取得（不再呼叫 detect_kline_patterns）
    k_pattern = kbar_pattern or "常態 K 線（無觸發極端型態）"
    h_win_rate = kbar_win_rate

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
        # 葛蘭碧買點訊號（含買點類型）
        ma_name  = gann_recross["ma"]
        ma_val   = gann_recross["val"]
        g_stop   = gann_recross["stop"]
        buy_type = gann_recross.get("type", "葛蘭碧買點")
        if kbar_bullish:
            conclusion = f"{buy_type}：{ma_name}（{ma_val}），出現多頭K棒（{kbar_pattern}）。操作：可設防守位 {g_stop}（{ma_name} 下方）試多，目標壓力 {resistance}"
        elif kbar_bearish:
            conclusion = f"{buy_type}：{ma_name}（{ma_val}），但出現空頭K棒（{kbar_pattern}），力道存疑。操作：等明天確認站穩 {ma_name} 再進場，防守位 {g_stop}"
        else:
            conclusion = f"{buy_type}：{ma_name}（{ma_val}），潛在買點。操作：明天若確認站穩 {ma_name} 可設防守位 {g_stop} 試多，目標壓力 {resistance}"
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

    # ── 深度分析欄位 ──
    kbar_simple  = _classify_kbar_simple(opens, highs, lows, closes, volumes)
    ma_alignment = _ma_alignment_desc(ma_values)
    kd_status    = _kd_status_desc(k_arr, d_arr)
    macd_status  = _macd_status_desc(macd_line, macd_sig, macd_hist)
    vol_analysis = _vol_analysis_desc(volumes, closes, opens)
    institutional = _fetch_institutional_safe(stock_id)
    risk_factors  = _individualized_risk(
        price, support, resistance, rr_ratio,
        kd_status, macd_status, kbar_simple, institutional
    )

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
        "target_price": round(float(channel["target1"]), 2) if channel and channel.get("target1") else None,
        "support_too_close": bool((price - support) / price < 0.02) if price > 0 else False,
        "risk_reward": rr_ratio, "rr_basis": rr_basis,
        "risk_level": risk_level, "risk_label": risk_label, "risk_color": risk_color,
        "summary": summary_lines,
        "warning": warning,
        "conflict_note": conflict_note,
        "kbar_pattern": kbar_pattern, "kbar_warning": kbar_warning,
        "kbar_dir": kbar_dir, "kbar_action": kbar_action,
        "gann_recross": gann_recross,
        "today_breakout": today_breakout, "prev_high": prev_high,
        "today_open": round(float(opens[-1]), 2) if len(opens) > 0 else None,
        "today_low":  round(float(lows[-1]),  2) if len(lows)  > 0 else None,
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
        # 深度分析
        "kbar_simple":   kbar_simple,
        "ma_alignment":  ma_alignment,
        "kd_status":     kd_status,
        "macd_status":   macd_status,
        "vol_analysis":  vol_analysis,
        "institutional": institutional,
        "risk_factors":  risk_factors,
    }

    # 基本面（非同步，抓失敗不影響結果）
    try:
        import sys as _sys, os as _os
        _sys.path.insert(0, _os.path.join(_os.path.dirname(__file__), "stock_picker"))
        from finmind_filter import _fetch_fundamentals
        _fund = _fetch_fundamentals(stock_id, token=FINMIND_TOKEN)
        result["per"]            = _fund.get("per")
        result["pbr"]            = _fund.get("pbr")
        result["dividend_yield"] = _fund.get("dividend_yield")
        result["eps_ttm"]        = _fund.get("eps_ttm")
        result["eps_yoy"]        = _fund.get("eps_yoy")
    except Exception as _fe:
        result["per"] = result["pbr"] = result["dividend_yield"] = result["eps_ttm"] = result["eps_yoy"] = None

    # T10: 基本面納入風險調整
    _fund_risk_adj = 0  # 正值=風險增加, 負值=風險降低
    _fund_notes = []
    try:
        _per = result.get("per")
        _div_yield = result.get("dividend_yield")
        if _per is not None and float(_per) > 30 and near_top:
            _fund_risk_adj += 1
            _fund_notes.append(f"本益比偏高({_per})且靠近壓力，留意估值風險")
        if _div_yield is not None and float(_div_yield) > 5.0 and near_bot:
            _fund_risk_adj -= 1
            _fund_notes.append(f"殖利率{_div_yield}%且靠近支撐，基本面支持")
        if _per is not None and float(_per) < 0:
            _fund_risk_adj += 1
            _fund_notes.append("EPS 為負，基本面偏弱")
    except Exception:
        pass
    result["fund_risk_adj"] = _fund_risk_adj
    result["fund_notes"] = _fund_notes

    # T10: 基本面風險提示附加到結論
    if _fund_notes:
        result["warning"] = result.get("warning", "") + "。" + "；".join(_fund_notes)

    # T6: 有效損益比（用 K 棒型態勝率加權）
    _effective_rr = round(rr_ratio * (h_win_rate / 0.5), 2) if h_win_rate and rr_ratio else rr_ratio
    result["effective_rr"] = _effective_rr


    # ── 多空雷達（線上有位版）────────────────────────────
    try:
        _ma5_v  = ma_values.get("ma5")
        _ma20_v = ma_values.get("ma20")
        _ma60_v = ma_values.get("ma60")
        _hist_v = float(macd_hist[-1]) if len(macd_hist) > 0 and not np.isnan(macd_hist[-1]) else 0.0
        _vol_r  = vol_analysis.get("ratio", 1.0)

        # 雷達一：趨勢 — MA20 > MA60（月線站季線上方）
        _tp_trend = bool(_ma20_v and _ma60_v and _ma20_v > _ma60_v)

        # T4: 趨勢斜率判斷 — MA20 近 5 根的方向
        _ma20_arr = calc_ma(closes, 20)
        _ma20_slope = "flat"
        if len(_ma20_arr) >= 5 and not np.isnan(_ma20_arr[-1]) and not np.isnan(_ma20_arr[-5]):
            _slope_pct = (_ma20_arr[-1] - _ma20_arr[-5]) / _ma20_arr[-5] * 100
            if _slope_pct > 0.3:
                _ma20_slope = "up"
            elif _slope_pct < -0.3:
                _ma20_slope = "down"

        # 雷達二：MACD — 配合 KD 方向判斷
        try:
            _hist_prev = float(macd_hist[-2]) if len(macd_hist) > 1 else 0.0
            if np.isnan(_hist_prev): _hist_prev = 0.0
        except Exception:
            _hist_prev = 0.0
        _kd_golden = kd_status.get("golden_cross", False)
        _kd_death  = kd_status.get("death_cross", False)
        _k_now     = kd_status.get("k") or 50
        _d_now     = kd_status.get("d") or 50
        if _k_now > _d_now:
            _tp_macd = bool(_hist_v > _hist_prev)   # KD 多頭排列：柱體往上就配合
        elif _k_now < _d_now:
            _tp_macd = bool(_hist_v < _hist_prev)   # KD 空頭排列：柱體往下就配合
        else:
            _tp_macd = bool(_hist_v > 0)             # 無法判斷，維持原條件

        # 雷達三：資金籌碼 — 近5日均量 > 20日均量（量能放大）
        _tp_vol   = bool(float(_vol_r) >= 1.2)

        # T1: 雷達四：位置 — MA5 乖離 -3%~+3%（剛站上均線，未過熱）
        _bias5  = round((price - float(_ma5_v))  / float(_ma5_v)  * 100, 2) if _ma5_v  and float(_ma5_v)  > 0 else None
        _bias20 = round((price - float(_ma20_v)) / float(_ma20_v) * 100, 2) if _ma20_v and float(_ma20_v) > 0 else None
        _tp_position = bool(_bias5 is not None and -3.0 <= _bias5 <= 3.0)

        _tp_score = int(bool(_tp_trend)) + int(bool(_tp_macd)) + int(bool(_tp_vol)) + int(bool(_tp_position))
        _tp_label = {4: "雷達全亮🔥", 3: "差一格⚡", 2: "訊號弱👀", 1: "雷達靜默", 0: "雷達靜默"}.get(_tp_score, "")

        # 進場訊號：雷達四格全亮
        _bias_entry = bool(_tp_score == 4)

        # T7: 出場訊號（加入 MA5 跌破 MA20）
        _ma5_arr = calc_ma(closes, 20)  # 這裡要用 ma5
        _ma5_cross_below_ma20 = False
        if _ma5_v and _ma20_v and float(_ma5_v) < float(_ma20_v):
            # 確認前一天 MA5 還在 MA20 上方（今天剛跌破）
            _ma5_full = calc_ma(closes, 5)
            if len(_ma5_full) >= 2 and len(_ma20_arr) >= 2:
                _prev_ma5 = _ma5_full[-2] if not np.isnan(_ma5_full[-2]) else None
                _prev_ma20 = _ma20_arr[-2] if not np.isnan(_ma20_arr[-2]) else None
                if _prev_ma5 and _prev_ma20 and _prev_ma5 >= _prev_ma20:
                    _ma5_cross_below_ma20 = True

        # 出場訊號四級警示
        if _bias5 is not None and _bias5 > 10.0:
            _bias_exit_warning = "大"
        elif _bias5 is not None and _bias5 > 5.0:
            _bias_exit_warning = "中"
        elif _ma5_cross_below_ma20:
            _bias_exit_warning = "中"   # T7: MA5 跌破 MA20 視為中級警示
        elif _kd_death and _hist_v < _hist_prev:
            _bias_exit_warning = "小"
        else:
            _bias_exit_warning = False

        result["radar"] = {
            "trend":     _tp_trend,
            "macd":      _tp_macd,
            "volume":    _tp_vol,
            "position":  _tp_position,     # T1: 第四格
            "score":     _tp_score,
            "label":     _tp_label,
            "ma5":       round(float(_ma5_v),  2) if _ma5_v  else None,
            "ma20":      round(float(_ma20_v), 2) if _ma20_v else None,
            "ma60":      round(float(_ma60_v), 2) if _ma60_v else None,
            "vol_ratio": round(float(_vol_r), 2),
            "macd_hist": round(_hist_v, 4),
            "bias5":     _bias5,
            "bias20":    _bias20,
            "bias_entry":           _bias_entry,
            "bias_exit_warning":    _bias_exit_warning,
            "ma20_slope":           _ma20_slope,           # T4: 趨勢斜率
            "ma5_cross_below_ma20": _ma5_cross_below_ma20, # T7: 均線死叉
        }
    except Exception as _tpe:
        result["radar"] = {"score": 0, "label": "計算失敗", "error": str(_tpe)}

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

    # 累計分析次數
    _inc_counter("analyze_count")

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
    快取：15 分鐘（SEO_CACHE["top_gainers"]）
    """
    import urllib.request, json as _json
    from datetime import date, timedelta

    # ── 15 分鐘快取 ──
    _tg = SEO_CACHE["top_gainers"]
    if _tg["data"] and _tg["expires"] > _time_mod.time():
        return _tg["data"]

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
            payload = {"date": target, "gainers": result}
            SEO_CACHE["top_gainers"] = {"data": payload, "expires": _time_mod.time() + 900}
            return payload
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


# ══════════════════════════════════════════════════════════
# 即時報價快取
# 盤中 09:00–13:30：15 分鐘過期（expires = timestamp）
# 盤後 / 非交易時間：永久快取（expires = 0）
# 每日 09:00 排程清除，確保開盤抓新價
# ══════════════════════════════════════════════════════════
_QUOTE_CACHE: dict = {}  # { "2330": {"data": {...}, "expires": float} }
_CHIPS_CACHE: dict = {}  # { "2330_20260521": {"data": {...}, "expires": float} }

def _is_trading_session() -> bool:
    """是否在盤中 09:00–13:30（台北時間，週一到週五）"""
    from zoneinfo import ZoneInfo
    from datetime import time as _t
    now = datetime.now(ZoneInfo("Asia/Taipei"))
    return now.weekday() < 5 and _t(9, 0) <= now.time() <= _t(13, 30)

def _clear_quote_cache():
    """清除所有即時報價快取與分析快取（每日 09:00、14:00 由排程呼叫）"""
    _QUOTE_CACHE.clear()
    _analyze_cache.clear()
    print("[CACHE] 清除 _QUOTE_CACHE + _analyze_cache 完成")


@app.get("/api/quote/live/{stock_id}")
def get_quote_live(stock_id: str):
    """
    FinMind 即時報價 proxy（不需登入）
    盤中：tick_snapshot（即時）
    盤後/非交易日：TaiwanStockPrice 最新收盤
    """
    import urllib.request as _ur, json as _j
    from datetime import timedelta as _td
    from zoneinfo import ZoneInfo as _ZI

    code  = stock_id.strip().replace(".TW", "").replace(".TWO", "")
    tz    = _ZI("Asia/Taipei")
    now_tw = datetime.now(tz)
    today  = now_tw.strftime("%Y-%m-%d")
    _h, _m = now_tw.hour, now_tw.minute
    is_weekday = now_tw.weekday() < 5
    in_session = is_weekday and (9, 0) <= (_h, _m) <= (13, 30)

    # ── 共用 _QUOTE_CACHE（key 加 "_live" 與 /api/quote 格式區分）──
    _live_key = code + "_live"
    _now_ts = _time_mod.time()
    _lc = _QUOTE_CACHE.get(_live_key)
    if _lc and (_lc["expires"] == 0 or _now_ts < _lc["expires"]):
        return _lc["data"]

    def _sf(v):
        try:
            f = float(v or 0)
            return f if f > 0 else None
        except Exception:
            return None

    def _cache_live(result):
        _exp = (_time_mod.time() + 900) if in_session else (_time_mod.time() + 21600)
        _QUOTE_CACHE[_live_key] = {"data": result, "expires": _exp}
        return result

    empty = {"z": None, "y": None, "o": None, "h": None, "l": None, "v": None, "t": ""}

    # ── 1. 盤中：tick_snapshot 即時快照 ──
    if in_session:
        try:
            snap_url = (f"https://api.finmindtrade.com/api/v4/taiwan_stock_tick_snapshot"
                        f"?data_id={code}&token={FINMIND_TOKEN}")
            snap_req = _ur.Request(snap_url, headers={"User-Agent": "Mozilla/5.0"})
            with _ur.urlopen(snap_req, timeout=6) as sr:
                snap = _j.loads(sr.read())
            snap_rows = snap.get("data", [])
            print(f"[LIVE {code}] tick_snapshot rows={len(snap_rows)}")
            if snap_rows:
                r  = snap_rows[0]
                cp = _sf(r.get("price") or r.get("close"))
                if cp:
                    # 昨收：用 TaiwanStockPrice 補
                    y_val = None
                    try:
                        start = (now_tw - _td(days=5)).strftime("%Y-%m-%d")
                        day_url = (f"https://api.finmindtrade.com/api/v4/data"
                                   f"?dataset=TaiwanStockPrice&data_id={code}"
                                   f"&start_date={start}&token={FINMIND_TOKEN}")
                        day_req = _ur.Request(day_url, headers={"User-Agent": "Mozilla/5.0"})
                        with _ur.urlopen(day_req, timeout=6) as dr:
                            day_data = _j.loads(dr.read())
                        day_rows = day_data.get("data", [])
                        if day_rows:
                            y_val = _sf(day_rows[-1].get("close"))
                    except Exception:
                        pass
                    result = {
                        "z": cp,
                        "y": y_val,
                        "o": _sf(r.get("open")  or cp),
                        "h": _sf(r.get("high")  or cp),
                        "l": _sf(r.get("low")   or cp),
                        "v": _sf(r.get("total_volume") or r.get("volume")),
                        "t": today,
                    }
                    print(f"[LIVE {code}] snap z={cp} y={y_val}")
                    return _cache_live(result)
        except Exception as _e:
            if not (hasattr(_e, 'code') and getattr(_e, 'code', 0) == 400):
                print(f"[LIVE {code}] tick_snapshot 失敗：{_e}")

    # ── 2. 盤後 / 非交易日：TaiwanStockPrice 最新收盤 ──
    try:
        start = (now_tw - _td(days=5)).strftime("%Y-%m-%d")
        url = (f"https://api.finmindtrade.com/api/v4/data"
               f"?dataset=TaiwanStockPrice&data_id={code}"
               f"&start_date={start}&token={FINMIND_TOKEN}")
        req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with _ur.urlopen(req, timeout=8) as r:
            data = _j.loads(r.read())
        rows = data.get("data", [])
        print(f"[LIVE {code}] TaiwanStockPrice rows={len(rows)} today={today}")
        if not rows:
            return empty

        latest   = rows[-1]
        is_today = str(latest.get("date", ""))[:10] == today
        prev     = rows[-2] if len(rows) >= 2 else None

        z = _sf(latest.get("close")) if is_today else None
        y = _sf(prev.get("close")) if prev else _sf(latest.get("close"))

        result = {
            "z": z,
            "y": y,
            "o": _sf(latest.get("open"))            if is_today else None,
            "h": _sf(latest.get("max"))             if is_today else None,
            "l": _sf(latest.get("min"))             if is_today else None,
            "v": _sf(latest.get("Trading_Volume"))  if is_today else None,
            "t": today if is_today else "",
        }
        print(f"[LIVE {code}] daily is_today={is_today} z={result['z']} y={result['y']}")
        return _cache_live(result)
    except Exception as _e:
        print(f"[LIVE {code}] TaiwanStockPrice 失敗：{_e}")
        return empty


@app.get("/api/quote/{stock_id}")
def get_quote(stock_id: str, user: dict | None = Depends(get_current_user)):
    """
    即時報價（公開 endpoint，不需登入）
    快取策略：
      盤中 09:00–13:30 → 15 分鐘過期
      盤後 / 非交易時間 → 6 小時過期
    每日 09:00 排程清除全部快取，確保開盤第一筆抓新價
    來源優先順序：TWSE MIS z（完全免費）→ FinMind tick_snapshot → FinMind TaiwanStockPrice
    """
    import urllib.request as _ur, json as _json

    def _safe_print(msg):
        try:
            print(msg.encode("utf-8", errors="replace").decode("utf-8", errors="replace"))
        except Exception:
            pass

    code = stock_id.strip().replace(".TW", "").replace(".TWO", "").upper()
    now_ts = _time_mod.time()
    in_session = _is_trading_session()

    # ── 查快取 ──
    cached = _QUOTE_CACHE.get(code)
    if cached:
        exp = cached["expires"]
        if exp == 0 or now_ts < exp:
            return cached["data"]

    # ── 快取未命中，抓新資料 ──
    def _sf(v):
        try:
            f = float(v or 0)
            return f if f > 0 else None
        except Exception:
            return None

    price_val = open_val = high_val = low_val = vol_val = y_val = None
    price_source = "none"

    # 1. TWSE MIS（完全免費，先試 tse_ 再試 otc_）
    twse_data = None
    for ex in ("tse", "otc"):
        try:
            mis_url = (f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
                       f"?ex_ch={ex}_{code}.tw&json=1&delay=0")
            mis_req = _ur.Request(mis_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer":    "https://mis.twse.com.tw/stock/index.jsp",
                "Accept":     "application/json",
            })
            with _ur.urlopen(mis_req, timeout=6, context=_TWSE_SSL_CTX) as resp:
                arr = _json.loads(resp.read()).get("msgArray", [])
            if arr:
                z_raw = str(arr[0].get("z", "-")).strip()
                if z_raw not in ("-", ""):
                    twse_data = arr[0]
                    break
                if not twse_data:
                    twse_data = arr[0]
        except Exception as _mis_e:
            _safe_print(f"[QUOTE] {code} TWSE MIS {ex}_ 呼叫失敗：{_mis_e}")
            continue

    def _val(k):
        v = str(twse_data.get(k, "-")).strip() if twse_data else "-"
        return None if v in ("-", "") else v

    y_val = _sf(_val("y"))  # 昨收，永遠從 TWSE 拿

    z = _sf(_val("z"))
    if z:
        price_val    = z
        open_val     = _sf(_val("o"))
        high_val     = _sf(_val("h"))
        low_val      = _sf(_val("l"))
        vol_raw      = _val("v")
        vol_val      = int(float(vol_raw) * 1000) if vol_raw else None
        price_source = "twse_z"
        _safe_print(f"[QUOTE] {code} twse_z price={price_val}")
    else:
        # z="-" 時改用委買第一檔（b）與委賣第一檔（a）的中間價
        try:
            b_raw = _val("b")  # "32.2000_32.1500_..."
            a_raw = _val("a")  # "32.2500_32.3000_..."
            # 取第一檔：跳過 0.0000（漲停時市價單的 TWSE 編碼）
            def _first_nonzero(raw):
                if not raw:
                    return None
                for part in raw.split("_"):
                    part = part.strip()
                    if not part:
                        continue
                    try:
                        v = float(part)
                        if v > 0:
                            return v
                    except ValueError:
                        pass
                return None
            b1 = _first_nonzero(b_raw)
            a1 = _first_nonzero(a_raw)
            if b1 is not None and a1 is not None:
                price_val    = round((b1 + a1) / 2, 2)
                open_val     = _sf(_val("o"))
                high_val     = _sf(_val("h"))
                low_val      = _sf(_val("l"))
                vol_raw      = _val("v")
                vol_val      = int(float(vol_raw) * 1000) if vol_raw else None
                price_source = "twse_mid"
                _safe_print(f"[QUOTE] {code} twse_mid b={b1} a={a1} mid={price_val}")
            else:
                # 漲停（a='-'）或跌停（b='-'）：用 u/w 欄位直接取極限價
                u_val = _sf(_val("u"))  # 漲停參考價
                w_val = _sf(_val("w"))  # 跌停參考價
                h_val = _sf(_val("h"))
                l_val = _sf(_val("l"))
                if a1 is None and u_val and h_val and abs(h_val - u_val) < 0.01:
                    # 漲停：委賣消失 + 今日最高 = 漲停價
                    price_val    = u_val
                    open_val     = _sf(_val("o"))
                    high_val     = h_val
                    low_val      = l_val
                    vol_raw      = _val("v")
                    vol_val      = int(float(vol_raw) * 1000) if vol_raw else None
                    price_source = "twse_limit_up"
                    _safe_print(f"[QUOTE] {code} 漲停 price={price_val}")
                elif b1 is None and w_val and l_val and abs(l_val - w_val) < 0.01:
                    # 跌停：委買消失 + 今日最低 = 跌停價
                    price_val    = w_val
                    open_val     = _sf(_val("o"))
                    high_val     = h_val
                    low_val      = l_val
                    vol_raw      = _val("v")
                    vol_val      = int(float(vol_raw) * 1000) if vol_raw else None
                    price_source = "twse_limit_down"
                    _safe_print(f"[QUOTE] {code} 跌停 price={price_val}")
                elif in_session:
                    z_raw_dbg = twse_data.get("z", "NO_FIELD") if twse_data else "NO_DATA"
                    n_dbg     = twse_data.get("n", "?")         if twse_data else "?"
                    _safe_print(f"[QUOTE] {code}（{n_dbg}）b/a 無有效值 z='{z_raw_dbg}'，需走 FinMind 備援")
        except Exception as _mid_e:
            _safe_print(f"[QUOTE] {code} twse_mid 計算失敗：{_mid_e}")

    # 2. FinMind tick_snapshot（備援，盤中即時，消耗額度）
    if price_val is None:
        try:
            snap_url = (f"https://api.finmindtrade.com/api/v4/taiwan_stock_tick_snapshot"
                        f"?data_id={code}&token={FINMIND_TOKEN}")
            snap_req = _ur.Request(snap_url, headers={"User-Agent": "Mozilla/5.0"})
            with _ur.urlopen(snap_req, timeout=6) as sr:
                snap = _json.loads(sr.read())
            rows = snap.get("data", [])
            if rows:
                r = rows[0]
                cp = _sf(r.get("price") or r.get("close"))
                if cp:
                    price_val    = cp
                    open_val     = _sf(r.get("open")  or cp)
                    high_val     = _sf(r.get("high")  or cp)
                    low_val      = _sf(r.get("low")   or cp)
                    vol_val      = _sf(r.get("total_volume") or r.get("volume"))
                    price_source = "tick_snapshot"
                    _safe_print(f"[QUOTE] {code} tick_snapshot price={price_val}")
        except Exception as _e:
            _safe_print(f"[QUOTE] tick_snapshot 失敗 {code}：{_e}")

    # 3. FinMind TaiwanStockPrice（最終 fallback，盤後收盤價）
    if price_val is None:
        try:
            from zoneinfo import ZoneInfo as _ZI
            from datetime import date as _d, timedelta as _td
            _tw_today = datetime.now(_ZI("Asia/Taipei")).date()
            start = (_tw_today - _td(days=5)).strftime("%Y-%m-%d")
            fm_url = (f"https://api.finmindtrade.com/api/v4/data"
                      f"?dataset=TaiwanStockPrice&data_id={code}"
                      f"&start_date={start}&token={FINMIND_TOKEN}")
            fm_req = _ur.Request(fm_url, headers={"User-Agent": "Mozilla/5.0"})
            with _ur.urlopen(fm_req, timeout=8) as r:
                rows = _json.loads(r.read()).get("data", [])
            if rows:
                latest = rows[-1]
                from zoneinfo import ZoneInfo as _ZI2
                _fm_today = datetime.now(_ZI2("Asia/Taipei")).strftime("%Y-%m-%d")
                _is_today_fm = str(latest.get("date", ""))[:10] == _fm_today
                if _is_today_fm:
                    price_val    = _sf(latest.get("close"))
                    open_val     = _sf(latest.get("open"))
                    high_val     = _sf(latest.get("max"))
                    low_val      = _sf(latest.get("min"))
                    vol_val      = _sf(latest.get("Trading_Volume"))
                    price_source = "finmind_close"
                    _safe_print(f"[QUOTE] {code} finmind_close price={price_val}")
                else:
                    _safe_print(f"[QUOTE] {code} finmind 尚無今日資料，僅補 y_val")
                if not y_val and len(rows) >= 2:
                    y_val = _sf(rows[-2].get("close"))
                elif not y_val and not _is_today_fm:
                    y_val = _sf(latest.get("close"))
        except Exception as _e:
            _safe_print(f"[QUOTE] FinMind TaiwanStockPrice 失敗 {code}：{_e}")

    # ── 漲跌幅（以昨收 y_val 為基準）──
    change = change_pct = None
    if price_val and y_val:
        try:
            change     = round(price_val - y_val, 2)
            change_pct = round(change / y_val * 100, 2)
        except Exception:
            pass

    # A. 三層來源全失敗時，fallback 使用上一筆快取（如果有）
    if price_val is None and code in _QUOTE_CACHE:
        return _QUOTE_CACHE[code]["data"]

    result = {
        "stock_id":     code,
        "price":        price_val,
        "change":       change,
        "change_pct":   change_pct,
        "open":         open_val,
        "high":         high_val,
        "low":          low_val,
        "volume":       int(vol_val) if vol_val else None,
        "in_session":   in_session,
        "price_source": price_source,
        # E. change/change_pct 為 null 時提示「盤後」，避免空白
        "price_note":   None if (change is not None) else "盤後",
    }

    # D. price=null 時不寫快取，避免短暫失敗鎖住 null 長達 15 分鐘
    if price_val is not None:
        expires = (_time_mod.time() + 900) if in_session else (_time_mod.time() + 21600)
        _QUOTE_CACHE[code] = {"data": result, "expires": expires}

    return result


@app.get("/api/realtime/{stock_id}")
def get_realtime(stock_id: str):
    """
    即時看盤 proxy：
    盤中 → get_quote 快取（已含 TWSE MIS 五檔）+ FinMind tick
    盤後 → FinMind TaiwanStockPrice 收盤價
    """
    import urllib.request as _ur, json as _json
    from zoneinfo import ZoneInfo as _ZI
    from datetime import timedelta as _td

    code = stock_id.strip().upper().replace(".TW","").replace(".TWO","")
    in_sess = _is_trading_session()
    q = {}

    # 1. 盤中：先從 get_quote 快取取（包含 TWSE MIS 原始資料）
    if in_sess:
        cached = _QUOTE_CACHE.get(code)
        if not cached or (_time_mod.time() >= cached.get("expires", 0)):
            try:
                get_quote(code, user=None)
                cached = _QUOTE_CACHE.get(code)
            except Exception:
                pass
        if cached and cached.get("data"):
            d = cached["data"]
            q = {
                "n": _name_cache.get(code, code),
                "z": str(d.get("price") or ""),
                "y": str(d.get("y") or ""),
                "o": str(d.get("open") or ""),
                "h": str(d.get("high") or ""),
                "l": str(d.get("low") or ""),
                "v": str(d.get("volume") or ""),
                "b": d.get("b", ""),
                "g": d.get("g", ""),
                "a": d.get("a", ""),
                "f": d.get("f", ""),
                "ct": d.get("ct", ""),
            }

    # 2. 盤後或盤中快取沒資料：FinMind TaiwanStockPrice
    if not q.get("z"):
        try:
            _tw_today = datetime.now(_ZI("Asia/Taipei"))
            start = (_tw_today - _td(days=5)).strftime("%Y-%m-%d")
            fm_url = (f"https://api.finmindtrade.com/api/v4/data"
                      f"?dataset=TaiwanStockPrice&data_id={code}"
                      f"&start_date={start}&token={FINMIND_TOKEN}")
            fm_req = _ur.Request(fm_url, headers={"User-Agent": "Mozilla/5.0"})
            with _ur.urlopen(fm_req, timeout=8) as resp:
                fm_data = _json.loads(resp.read())
            rows = fm_data.get("data", [])
            if rows:
                latest = rows[-1]
                q["n"]  = _name_cache.get(code, code)
                q["z"]  = str(latest.get("close", ""))
                q["o"]  = str(latest.get("open", ""))
                q["h"]  = str(latest.get("max", ""))
                q["l"]  = str(latest.get("min", ""))
                q["v"]  = str(int(float(latest.get("Trading_Volume", 0)) // 1000))
                q["y"]  = str(rows[-2].get("close", "")) if len(rows) >= 2 else ""
                q["b"]  = q.get("b", "")
                q["a"]  = q.get("a", "")
                q["ct"] = q.get("ct", "")
        except Exception as e:
            print(f"[REALTIME] {code} FinMind 失敗：{e}")

    if q.get("z") or q.get("y"):
        if not q.get("n"):
            q["n"] = _name_cache.get(code, code)
        return JSONResponse({"ok": True, "data": q})

    return JSONResponse({"ok": False, "data": None})


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
    from zoneinfo import ZoneInfo
    new_expire = (datetime.now(ZoneInfo("Asia/Taipei")) + timedelta(days=days)).strftime("%Y-%m-%d")

    plan_label = {"monthly": "月費方案", "quarterly": "季費方案", "yearly": "年費方案", "free": "免費方案"}.get(plan, plan)

    def _send_grant_email(to: str, extra_html: str = ""):
        _send_email(to, "【線上有位】🎉 您的方案已開通",
            f"""<div style="font-family:-apple-system,sans-serif;max-width:560px;margin:0 auto;padding:24px">
              <div style="text-align:center;margin-bottom:24px">
                <h1 style="font-size:24px;color:#1D9E75;margin:0">線上<span style="color:#333">有位</span></h1>
                <p style="color:#666;font-size:13px;margin:4px 0 0">台股技術分析輔助系統</p>
              </div>
              {_SOFTGLOW_AD}
              <div style="background:#f0fdf4;border-radius:12px;padding:24px;margin-bottom:20px;border:1px solid #86efac">
                <h2 style="margin:0 0 16px;font-size:18px;color:#166534">🎉 恭喜！升級成功</h2>
                <p style="color:#555;margin:0 0 16px">您的付費方案已由管理員手動開通，立即登入即可使用。</p>
                <table style="width:100%;border-collapse:collapse">
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">方案</td><td style="padding:8px 0;font-weight:700;color:#333">{plan_label}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">到期日</td><td style="padding:8px 0;font-weight:700;color:#333">{new_expire}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">帳號</td><td style="padding:8px 0;font-weight:700;color:#333">{to}</td></tr>
                </table>
              </div>
              {extra_html}
              {_SOFTGLOW_AD}
              <div style="text-align:center;margin-bottom:20px">
                <a href="{FRONTEND_URL}" style="background:#1D9E75;color:#fff;padding:12px 32px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px">立即登入使用</a>
              </div>
              <div style="border-top:1px solid #e5e7eb;padding-top:16px;text-align:center;color:#9ca3af;font-size:12px">
                <p style="margin:0">如有問題請聯繫客服：<a href="mailto:watione@yahoo.com.tw" style="color:#1D9E75">watione@yahoo.com.tw</a></p>
                <p style="margin:4px 0 0">線上有位 © 2026</p>
              </div>
            </div>"""
        )

    conn = _db_conn()
    row = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()
    if row:
        conn.execute(
            "UPDATE members SET plan=?, expire_at=?, token_ver=token_ver+1 WHERE email=?",
            (plan, new_expire, email)
        )
        conn.commit()
        conn.close()
        _send_grant_email(email)
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
        _send_grant_email(email,
            f"""<div style="background:#fffbeb;border:1px solid #fcd34d;border-radius:8px;padding:16px;margin-bottom:20px">
              <p style="margin:0 0 6px;font-weight:700;color:#92400e">🔑 您的初始密碼</p>
              <p style="margin:0;font-size:18px;letter-spacing:2px;font-weight:700;color:#333">{password}</p>
              <p style="margin:8px 0 0;font-size:12px;color:#78350f">登入後請至「我的帳號」修改密碼</p>
            </div>"""
        )
        return {"ok": True, "action": "created", "email": email, "password": password, "plan": plan, "expire_at": new_expire}


@app.post("/admin/reset-password")
def admin_reset_password(key: str = "", email: str = "", new_password: str = ""):
    """重設某用戶密碼，可指定新密碼或自動產生"""
    _check_admin(key)
    email = email.strip().lower()
    conn = _db_conn()
    row = conn.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="找不到此用戶")
    new_pw = new_password.strip() if new_password.strip() else secrets.token_urlsafe(8)
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

@app.post("/admin/clear-cache")
def admin_clear_cache(key: str = ""):
    """清除 _analyze_cache 和 _QUOTE_CACHE（強制下次查詢重新抓）"""
    _check_admin(key)
    n = len(_analyze_cache)
    _analyze_cache.clear()
    q = len(_QUOTE_CACHE)
    _QUOTE_CACHE.clear()
    return {"cleared": n + q, "message": f"快取已清除（分析 {n} 筆 + 報價 {q} 筆）"}


@app.get("/admin/run-opening-scan")
async def admin_run_opening_scan(key: str = Query(...)):
    _check_admin(key)
    try:
        import threading as _thr
        _thr.Thread(target=_run_opening_scan_job, daemon=True).start()
        return {"message": "開盤熱門股抓取完成"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        new_expire = (datetime.now(ZoneInfo("Asia/Taipei")) + timedelta(days=req.days)).strftime("%Y-%m-%d")
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
                html = _inject_report_ads(_build_report_html(sid, stock_name, report_date, d, news_items))
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


def _inc_counter(key: str):
    conn = _db_conn()
    conn.execute(
        "INSERT INTO counters (key, value) VALUES (?, 1) "
        "ON CONFLICT(key) DO UPDATE SET value=value+1",
        (key,)
    )
    conn.commit()
    conn.close()

def _record_visit():
    _inc_counter("visit_count")

@app.get("/api/stats")
def api_stats():
    conn = _db_conn()
    query_count = conn.execute("SELECT COALESCE(SUM(count), 0) FROM query_log").fetchone()[0]
    def _cval(key):
        r = conn.execute("SELECT value FROM counters WHERE key=?", (key,)).fetchone()
        return r[0] if r else 0
    visit_count   = _cval("visit_count")
    page_views    = _cval("page_views")
    analyze_count = _cval("analyze_count")
    conn.close()
    return {
        "visit_count":   int(visit_count),
        "query_count":   int(query_count),
        "page_views":    int(page_views),
        "analyze_count": int(analyze_count),
    }

@app.post("/api/page-view")
def api_page_view():
    _inc_counter("page_views")
    _record_visit()
    return {"ok": True}

# B1: 重複根路由已刪除，首頁由第 520 行 serve_homepage() 處理（回傳 homepage.html）

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
        # volume_ratio：直接讀 vol_analysis（已除以 1000，與報告頁同一來源）
        vol_analysis = d.get("vol_analysis") or {}
        volume_ratio = vol_analysis.get("ratio")
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
    直接從啟動時載入的 _name_cache 記憶體搜尋，完全不打 FinMind
    """
    q = q.strip()
    if not q:
        return {"results": []}

    q_lower = q.lower()
    results = []
    seen: set = set()

    def _add(sid: str, sname: str):
        if sid in seen:
            return
        if not sid.isdigit() or len(sid) not in (4, 5, 6):
            return
        seen.add(sid)
        results.append({
            "stock_id":   sid,
            "stock_name": sname,
            "type":       _market_cache.get(sid, ""),
        })

    # 1. 完全匹配代號（最高優先）
    for sid, sname in _name_cache.items():
        if sid.lower() == q_lower:
            _add(sid, sname)

    # 2. 代號前綴（如輸入 "235"）
    for sid, sname in _name_cache.items():
        if len(results) >= limit: break
        if sid.startswith(q) and sid.lower() != q_lower:
            _add(sid, sname)

    # 3. 名稱包含關鍵字
    for sid, sname in _name_cache.items():
        if len(results) >= limit: break
        if q in sname and sid.lower() != q_lower:
            _add(sid, sname)

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

    # B3: 統一勝率對照表（與原 detect_kline_patterns 一致，消除兩套判斷矛盾）
    _WIN_RATE_MAP = {
        "大紅棒": 0.62, "大黑棒": 0.62,
        "三紅兵": 0.60, "三烏鴉": 0.60,
        "早晨之星": 0.60, "黃昏之星": 0.60,
        "多頭吞噬": 0.58, "空頭吞噬": 0.58,
        "錘頭": 0.53, "射擊之星": 0.53,
        "穿刺線": 0.55, "烏雲蓋頂": 0.55,
        "十字星": 0.52, "孕線": 0.52,
    }
    win_rate = 0.50
    for key, rate in _WIN_RATE_MAP.items():
        if key in pattern_str:
            win_rate = rate
            break

    return pattern_str, warning_str, kbar_dir, win_rate


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
    快取：24 小時（key = stock_id + 日期，隔天自動換 key 失效）
    """
    from datetime import date, timedelta
    code = stock_id.strip().replace(".TW", "").replace(".TWO", "")
    _today = date.today().strftime("%Y%m%d")
    _chips_key = f"{code}_{_today}"
    _cc = _CHIPS_CACHE.get(_chips_key)
    if _cc and _cc["expires"] > _time_mod.time():
        return _cc["data"]

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
    _CHIPS_CACHE[_chips_key] = {"data": result, "expires": _time_mod.time() + 86400}
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
    client_ip = request.client.host if request else ""
    # 帶邀請碼時，先檢查同 IP 是否已有人用過同一邀請碼（INSERT 前攔截）
    inviter_email = None
    if ref:
        inviter_row = conn.execute(
            "SELECT user_email FROM referral_codes WHERE code=?", (ref.upper().strip(),)
        ).fetchone()
        if inviter_row and inviter_row["user_email"] != email:
            inviter_email = inviter_row["user_email"]
            if client_ip and conn.execute(
                "SELECT id FROM referral_logs WHERE inviter_email=? AND invitee_ip=?",
                (inviter_email, client_ip)
            ).fetchone():
                conn.close()
                raise HTTPException(
                    status_code=400,
                    detail="此網路環境已有使用該邀請碼的帳號，請改用手機電信網路重新嘗試"
                )
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
    if inviter_email:
        dupe = conn.execute(
            "SELECT id FROM referral_logs WHERE invitee_email=? AND inviter_email=?",
            (email, inviter_email)
        ).fetchone()
        if not dupe:
            conn.execute(
                "INSERT INTO referral_logs (inviter_email, invitee_email, invitee_ip) VALUES (?,?,?)",
                (inviter_email, email, client_ip)
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
    client_ip = request.client.host if request else ""
    inviter_email = None
    if ref:
        inviter_row = conn.execute(
            "SELECT user_email FROM referral_codes WHERE code=?", (ref.upper().strip(),)
        ).fetchone()
        if inviter_row and inviter_row["user_email"] != email:
            inviter_email = inviter_row["user_email"]
            if client_ip and conn.execute(
                "SELECT id FROM referral_logs WHERE inviter_email=? AND invitee_ip=?",
                (inviter_email, client_ip)
            ).fetchone():
                conn.close()
                raise HTTPException(
                    status_code=400,
                    detail="此網路環境已有使用該邀請碼的帳號，請改用手機電信網路重新嘗試"
                )
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
    if inviter_email:
        dupe = conn.execute(
            "SELECT id FROM referral_logs WHERE invitee_email=? AND inviter_email=?",
            (email, inviter_email)
        ).fetchone()
        if not dupe:
            conn.execute(
                "INSERT INTO referral_logs (inviter_email, invitee_email, invitee_ip) VALUES (?,?,?)",
                (inviter_email, email, client_ip)
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


class GoogleLoginReq(BaseModel):
    google_token: str


@app.post("/auth/google")
def auth_google(req: GoogleLoginReq):
    try:
        from google.oauth2 import id_token as _gid
        from google.auth.transport import requests as _greq
        _gcid = os.environ.get("GOOGLE_CLIENT_ID", "584257110691-jtn1tf282q4vsfn7c7vhp9c12m6ino1n.apps.googleusercontent.com")
        idinfo = _gid.verify_oauth2_token(req.google_token, _greq.Request(), _gcid)
    except Exception:
        raise HTTPException(status_code=401, detail="Google token 驗證失敗，請重新登入")

    email = idinfo.get("email", "").strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="無法取得 Google 帳號 Email")

    conn = _db_conn()
    blocked = conn.execute(
        "SELECT email FROM blocked_users WHERE email=? AND block_type='login'", (email,)
    ).fetchone()
    if blocked:
        conn.close()
        raise HTTPException(status_code=403, detail="帳號已被停用，請聯絡客服")

    row = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()
    if not row:
        rand_pwd = secrets.token_urlsafe(16)
        conn.execute(
            "INSERT INTO members (email, password, plan) VALUES (?, ?, 'free')",
            (email, _hash_pw(rand_pwd))
        )
        conn.commit()
        _get_or_create_referral_code(email)
        row = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()

    session_id = secrets.token_hex(16)
    conn.execute(
        "UPDATE members SET last_login=datetime('now','+8 hours'), session_id=? WHERE id=?",
        (session_id, row["id"])
    )
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
    # 判斷是否為定期定額會員（pending_orders 或 processed_orders 有 XYWR% 訂單）
    recurring_row = conn.execute(
        "SELECT 1 FROM pending_orders WHERE email=? AND merchant_trade_no LIKE 'XYWR%' LIMIT 1",
        (user["email"],)
    ).fetchone()
    if not recurring_row:
        recurring_row = conn.execute(
            "SELECT 1 FROM processed_orders WHERE merchant_trade_no LIKE 'R_XYWR%' AND "
            "merchant_trade_no IN ("
            "  SELECT 'R_'||merchant_trade_no||'_1' FROM pending_orders WHERE email=? AND merchant_trade_no LIKE 'XYWR%'"
            ") LIMIT 1",
            (user["email"],)
        ).fetchone()
    is_recurring = bool(recurring_row)
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
            delta = (datetime.fromisoformat(user["expire_at"]) - datetime.now(ZoneInfo("Asia/Taipei")).replace(tzinfo=None)).days
            days_left = max(0, delta)
            is_expiring_soon = 0 <= days_left <= 3
        except Exception:
            pass
    return {
        "email": user["email"],
        "nickname": user.get("nickname") or "",
        "plan": plan,
        "plan_label": plan_label,
        "is_active": is_active,
        "is_recurring": is_recurring,
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


class _NicknameReq(BaseModel):
    nickname: str

@app.post("/auth/nickname")
def update_nickname(body: _NicknameReq, user: dict = Depends(require_user)):
    import re
    nickname = body.nickname.strip()
    if not nickname:
        raise HTTPException(status_code=400, detail="暱稱不得為空")
    if len(nickname) > 16:
        raise HTTPException(status_code=400, detail="暱稱最多 16 字")
    if re.search(r'[<>&"\'\\]', nickname):
        raise HTTPException(status_code=400, detail="暱稱含有不允許的字元")
    conn = _db_conn()
    conn.execute("UPDATE members SET nickname=? WHERE id=?", (nickname, user["id"]))
    conn.commit()
    conn.close()
    return {"ok": True, "nickname": nickname}


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
        "invite_link": f"{FRONTEND_URL}/stock/landing?ref={code}",
        "completed_count": completed,
        "required_count": 3,
        "rewarded_count": user.get("referral_rewarded_count", 0),
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


# ── Soft Glow 產品推薦區塊（用於信件中，table 排版相容各郵件客戶端）──
_SOFTGLOW_AD = (
    '<div style="border-top:1px solid #e8f0ec;border-bottom:1px solid #e8f0ec;padding:16px 0;margin:16px 0">'
    '<p style="text-align:center;font-size:10px;font-weight:700;letter-spacing:2px;color:#1D9E75;margin:0 0 12px;text-transform:uppercase">SOFT GLOW &middot; 緩光&nbsp;&nbsp;健康守護系列</p>'
    '<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse"><tr>'
    '<td width="25%" style="text-align:center;padding:4px 2px">'
    '<a href="https://watione1.guidemee.cc/products/yWh2aDIQ" style="text-decoration:none;color:#222">'
    '<img src="https://watione1.guidemee.cc/tenancy/assets/oj9qkl/products/Oa9XaH7E5jgkNP7j2YkDaoFpLQPy7K-metaR2VtaW5pX0dlbmVyYXRlZF9JbWFnZV9xYjhoc3hxYjhoc3hxYjhoLnBuZw==-.png" width="80" height="80" style="border-radius:8px;object-fit:cover;display:block;margin:0 auto 6px" />'
    '<p style="font-size:11px;margin:0 0 2px;font-weight:500">深海之源魚油</p>'
    '<p style="font-size:10px;color:#16a34a;margin:0">Omega-3 84%</p></a></td>'
    '<td width="25%" style="text-align:center;padding:4px 2px">'
    '<a href="https://watione1.guidemee.cc/products/fjG6XpYz" style="text-decoration:none;color:#222">'
    '<img src="https://watione1.guidemee.cc/tenancy/assets/oj9qkl/products/M9X1tgv26e2Lbxr0m4ckHaeIhrkGd3-metaR2VtaW5pX0dlbmVyYXRlZF9JbWFnZV9jNGVweGZjNGVweGZjNGVwLnBuZw==-.png" width="80" height="80" style="border-radius:8px;object-fit:cover;display:block;margin:0 auto 6px" />'
    '<p style="font-size:11px;margin:0 0 2px;font-weight:500">雪肌彈力膠原</p>'
    '<p style="font-size:10px;color:#db2777;margin:0">六大專利成分</p></a></td>'
    '<td width="25%" style="text-align:center;padding:4px 2px">'
    '<a href="https://watione1.guidemee.cc/products/BnlNTsYz" style="text-decoration:none;color:#222">'
    '<img src="https://watione1.guidemee.cc/tenancy/assets/oj9qkl/products/zwfzYPbxjyLkS623gPq2IjdLgOVNLZ-metaR2VtaW5pX0dlbmVyYXRlZF9JbWFnZV9rMmpvZ29rMmpvZ29rMmpvLnBuZw==-.png" width="80" height="80" style="border-radius:8px;object-fit:cover;display:block;margin:0 auto 6px" />'
    '<p style="font-size:11px;margin:0 0 2px;font-weight:500">纖體飲</p>'
    '<p style="font-size:10px;color:#ea580c;margin:0">漢方配方</p></a></td>'
    '<td width="25%" style="text-align:center;padding:4px 2px">'
    '<a href="https://watione1.guidemee.cc/products/Gct3MfMg" style="text-decoration:none;color:#222">'
    '<img src="https://watione1.guidemee.cc/tenancy/assets/oj9qkl/products/skSjmETidhxTjLNnLCeH5WdNNHM0YX-metaR2VtaW5pX0dlbmVyYXRlZF9JbWFnZV9vcTR5N3dvcTR5N3dvcTR5LnBuZw==-.png" width="80" height="80" style="border-radius:8px;object-fit:cover;display:block;margin:0 auto 6px" />'
    '<p style="font-size:11px;margin:0 0 2px;font-weight:500">晶。水漾葉黃素</p>'
    '<p style="font-size:10px;color:#7c3aed;margin:0">護眼配方</p></a></td>'
    '</tr></table>'
    '<p style="font-size:10px;color:#bbb;margin:12px 0 0;text-align:center">全館滿 2000 元免運 &middot; 新會員首購 95 折&nbsp;&nbsp;'
    '<a href="https://watione1.guidemee.cc" style="color:#aaa">前往選購</a></p>'
    '</div>'
)


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


def _plan_days(item_name: str, amount: int = 0) -> int:
    """依商品名稱判斷天數，amount 為金額 fallback"""
    if "年" in item_name:
        return 365
    elif "季" in item_name:
        return 90
    elif "測試" in item_name or "test" in item_name.lower():
        return 1
    # 金額 fallback（綠界 webhook 可能改動 ItemName）
    if amount >= 3000:
        return 365
    elif amount >= 900:
        return 90
    elif amount <= 10:
        return 1
    return 30


@app.post("/pay/result")
async def pay_result(request: Request):
    """綠界 OrderResultURL（POST），驗證後 redirect 到前端結果頁"""
    from fastapi.responses import RedirectResponse
    body = await request.form()
    rtn_code = body.get("RtnCode", "0")
    if rtn_code == "1":
        return RedirectResponse(url=f"{FRONTEND_URL}/stock/landing?pay=done", status_code=303)
    else:
        return RedirectResponse(url=f"{FRONTEND_URL}/stock/landing?pay=fail", status_code=303)

@app.post("/create_order")
async def create_order(request: Request):
    """
    前端呼叫此端點產生綠界訂單，回傳付款網址
    Body: { email, plan }
    """
    from fastapi import Request
    import urllib.parse, hashlib, time as _t

    body = await request.json()
    email            = body.get("email", "").strip().lower()
    plan             = body.get("plan", "quarterly")
    password         = body.get("password", "").strip()
    invoice_type     = body.get("invoice_type", "").strip()
    invoice_carrier  = body.get("invoice_carrier", "").strip()

    if not email or not _re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        raise HTTPException(status_code=400, detail="Email 格式不正確")

    plan_info = {
        "monthly":   {"name": "線上有位月費方案", "amount": 499,  "days": 30},
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
        "TradeDesc":         "線上有位訂閱",
        "ItemName":          info["name"],
        "ReturnURL":         f"{BACKEND_URL}/webhook/ecpay",
        "OrderResultURL":    f"{BACKEND_URL}/pay/result",
        "ClientBackURL":     f"{FRONTEND_URL}/stock/landing?pay=fail",
        "ChoosePayment":     "ALL",
        "EncryptType":       "1",
        "CustomField1":      email,
    }

    # 暫存密碼到 DB（後端重啟也不遺失）
    if password and len(password) >= 6:
        _po_conn = _db_conn()
        _po_conn.execute(
            "INSERT OR REPLACE INTO pending_orders "
            "(merchant_trade_no, email, hashed_password, plan, invoice_type, invoice_carrier) VALUES (?, ?, ?, ?, ?, ?)",
            (trade_no, email, _hash_pw(password), plan, invoice_type, invoice_carrier)
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


def _fetch_opening_volume_top20() -> list:
    """抓台股成交量前20名（TWSE STOCK_DAY_ALL CSV 格式）
    v8.12 修正：移除 ?response=json（海外IP被擋403），改用 CSV 解析
    CSV 欄位：日期(0), 代號(1), 名稱(2), 成交股數(3), 成交金額(4),
              開盤(5), 最高(6), 最低(7), 收盤(8), 漲跌(9), 成交筆數(10)
    """
    import urllib.request as _ur2, csv as _csv2, io as _io2

    results = []

    # ── 方法一：TWSE CSV（不帶 ?response=json，同 crawler.py v8.12 修法）──
    try:
        url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY_ALL"
        req = _ur2.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer":    "https://www.twse.com.tw/",
        })
        with _ur2.urlopen(req, timeout=15, context=_TWSE_SSL_CTX) as r:
            raw_text = r.read().decode("utf-8-sig", errors="replace")
        reader = _csv2.reader(_io2.StringIO(raw_text))
        rows = list(reader)
        for row in rows:
            try:
                if len(row) < 10:
                    continue
                code = str(row[1]).strip().strip('="')
                name = str(row[2]).strip().strip('="')
                if not code.isdigit() or len(code) != 4:
                    continue
                vol_str    = str(row[3]).strip().strip('="').replace(",", "")
                close_str  = str(row[8]).strip().strip('="').replace(",", "")
                change_str = str(row[9]).strip().strip('="').replace(",", "")
                if not vol_str or vol_str in ("--", "X", ""):
                    continue
                vol    = int(float(vol_str)) // 1000       # 股 → 張
                close  = float(close_str)  if close_str  not in ("--", "X", "") else 0
                change = float(change_str) if change_str not in ("--", "X", "") else 0
                prev   = close - change
                change_pct = round(change / prev * 100, 2) if prev > 0 else 0
                results.append({
                    "stock_id":   code,
                    "name":       name,
                    "volume":     vol,
                    "price":      close,
                    "change_pct": change_pct,
                })
            except Exception:
                continue
        if results:
            print(f"[OPENING] TWSE CSV 成功，{len(results)} 支")
    except Exception as _e1:
        print(f"[OPENING] TWSE CSV 失敗：{_e1}")

    # ── 方法二：fallback 用 crawler.py 的 fetch_twse_volume_top ──
    if not results:
        try:
            import sys as _sys2, os as _os2
            _sys2.path.insert(0, _os2.path.join(_os2.path.dirname(_os2.path.abspath(__file__)), "stock_picker"))
            from crawler import fetch_twse_volume_top as _ftvt
            top_ids, name_dict = _ftvt(n=20)
            if top_ids:
                for _code in top_ids:
                    results.append({
                        "stock_id":   _code,
                        "name":       name_dict.get(_code, _code),
                        "volume":     0,
                        "price":      0,
                        "change_pct": 0,
                    })
                print(f"[OPENING] crawler.py fallback 成功，{len(results)} 支")
        except Exception as _e2:
            print(f"[OPENING] crawler.py fallback 也失敗：{_e2}")

    if not results:
        print("[OPENING] 所有方法均失敗，回傳空")
        return []

    results.sort(key=lambda x: x["volume"], reverse=True)
    top20 = results[:20]

    # 補即時價（走 FinMind，與個股分析同源，不走被擋的 MIS）
    for item in top20:
        try:
            _c = item["stock_id"]
            _qc = _QUOTE_CACHE.get(_c)
            if not (_qc and _qc.get("data", {}).get("price") and _time_mod.time() < _qc.get("expires", 0)):
                try:
                    get_quote(_c, user=None)
                    _qc = _QUOTE_CACHE.get(_c)
                except Exception:
                    _qc = None
            if _qc and _qc.get("data", {}).get("price"):
                _p = float(_qc["data"]["price"])
                _chg = float(_qc["data"].get("change", 0))
                _prev = _p - _chg
                if _p > 0:
                    item["price"] = round(_p, 2)
                    if _prev > 0:
                        item["change_pct"] = round(_chg / _prev * 100, 2)
        except Exception:
            pass

    return top20


def _run_deep_analysis_job():
    """每個交易日 17:00 執行：深度選股掃描"""
    from zoneinfo import ZoneInfo as _ZI3
    now = datetime.now(_ZI3("Asia/Taipei"))
    if now.weekday() >= 5:
        return
    print(f"[deep_analysis] 開始執行 {now.strftime('%H:%M')}")
    try:
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker"))
        from crawler import fetch_twse_volume_top
        from finmind_filter import run_deep_scan
        from generator import generate_deep_analysis

        # 取成交量前150做候選
        top_ids, name_dict = fetch_twse_volume_top(n=150)
        if not top_ids:
            print("[deep_analysis] 取得成交量排行失敗，跳過")
            return

        results = run_deep_scan(top_ids, name_dict=name_dict, finmind_token=FINMIND_TOKEN)
        generate_deep_analysis(results)
        print(f"[deep_analysis] 完成，{len(results)} 檔入選")
        # 把 HTML 存進 DB（避免 Zeabur 重啟後檔案消失）
        _da_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker", "output", "deep_analysis.html")
        if os.path.exists(_da_path):
            with open(_da_path, "r", encoding="utf-8") as _f:
                _da_html = _f.read()
            _dc = _db_conn()
            _dc.execute("INSERT OR REPLACE INTO html_pages (key, content, updated_at) VALUES (?, ?, datetime('now','+8 hours'))", ("deep_analysis", _da_html))
            _dc.commit()
            _dc.close()
            print("[deep_analysis] HTML 已存入 DB")
    except Exception as e:
        print(f"[deep_analysis] 執行失敗：{e}")
        import traceback
        traceback.print_exc()


def _run_opening_scan_job():
    """每個交易日 09:15 執行：更新開盤成交量前20名快取"""
    from zoneinfo import ZoneInfo as _ZI2
    now = datetime.now(_ZI2("Asia/Taipei"))
    if now.weekday() >= 5:
        return
    try:
        data = _fetch_opening_volume_top20()
        _OPENING_TOP20["data"] = data
        _OPENING_TOP20["updated_at"] = now.strftime("%Y-%m-%d %H:%M")
        import json as _json_scan
        _conn_scan = _db_conn()
        _conn_scan.execute(
            "INSERT OR REPLACE INTO opening_picks (date, data, updated_at) VALUES (?,?,?)",
            (now.strftime("%Y-%m-%d"), _json_scan.dumps(data, ensure_ascii=False), now.strftime("%Y-%m-%d %H:%M"))
        )
        _conn_scan.commit()
        _conn_scan.close()
        first = data[0]["stock_id"] if data else "N/A"
        print(f"[OPENING_SCAN] 完成，{len(data)} 筆，量No.1={first}")
    except Exception as _e:
        print(f"[OPENING_SCAN] 失敗：{_e}")
        import traceback
        traceback.print_exc()


@app.get("/api/picks/opening")
def get_opening_picks():
    """開盤熱門股（成交量前20，無需登入）
    盤中補即時報價，盤後補當日收盤價，都用 MIS API。
    """
    import urllib.request as _urq, json as _jq
    base_data = _OPENING_TOP20.get("data", [])
    updated_at = _OPENING_TOP20.get("updated_at")

    if not base_data:
        return {"data": base_data, "updated_at": updated_at}

    enriched = []
    for item in base_data:
        code = item.get("stock_id", "")
        new_item = dict(item)
        try:
            # 先查 _QUOTE_CACHE（個股分析同源，不走被擋的 MIS）
            _qc = _QUOTE_CACHE.get(code)
            if not (_qc and _qc.get("data", {}).get("price") and _time_mod.time() < _qc.get("expires", 0)):
                # 快取沒有，呼叫 get_quote 補抓（走 FinMind tick_snapshot）
                try:
                    get_quote(code, user=None)
                    _qc = _QUOTE_CACHE.get(code)
                except Exception:
                    _qc = None
            if _qc and _qc.get("data", {}).get("price"):
                _p   = float(_qc["data"]["price"])
                _chg = float(_qc["data"].get("change", 0))
                _prev = _p - _chg
                if _p > 0:
                    new_item["price"] = round(_p, 2)
                    new_item["change_pct"] = round(_chg / _prev * 100, 2) if _prev > 0 else 0
        except Exception:
            pass
        enriched.append(new_item)

    return {"data": enriched, "updated_at": updated_at}


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
        "SELECT hashed_password, invoice_type, invoice_carrier FROM pending_orders WHERE merchant_trade_no=?", (trade_no_w,)
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
          <a href="https://softglow-ai.com/stock/landing" style="background:#16a34a;color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-weight:700">立即升級年費</a>
        </div>"""
        _send_email(email, "【線上有位】升級成功！您的方案已開通",
            f"""<div style="font-family:-apple-system,sans-serif;max-width:560px;margin:0 auto;padding:24px">
              <div style="text-align:center;margin-bottom:24px">
                <h1 style="font-size:24px;color:#1D9E75;margin:0">線上<span style="color:#333">有位</span></h1>
                <p style="color:#666;font-size:13px;margin:4px 0 0">台股技術分析輔助系統</p>
              </div>
              {_SOFTGLOW_AD}
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
                <p style="margin:0 0 8px;font-weight:700;color:#92400e">✨ 精選好物推薦</p>
                <p style="margin:0;font-size:13px;color:#78350f">把線上有位推薦給朋友，讓更多人享受 AI 輔助的台股分析工具！分享您的使用心得，幫助我們持續優化服務。</p>
              </div>
              {_SOFTGLOW_AD}
              <div style="border-top:1px solid #e5e7eb;padding-top:16px;text-align:center;color:#9ca3af;font-size:12px">
                <p style="margin:0">如有問題請聯繫客服：<a href="mailto:watione@yahoo.com.tw" style="color:#1D9E75">watione@yahoo.com.tw</a></p>
                <p style="margin:4px 0 0">線上有位 © 2026</p>
              </div>
            </div>"""
        )
    else:
        # 新用戶：hashed_password 已從 pending_orders 取出（或隨機備用）
        new_expire = (datetime.now(ZoneInfo("Asia/Taipei")) + timedelta(days=days)).strftime("%Y-%m-%d")
        try:
            conn.execute(
                "INSERT INTO members (email, password, plan, expire_at, merchant_trade_no) VALUES (?, ?, ?, ?, ?)",
                (email, hashed_password, plan, new_expire, trade_no_w)
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
              {_SOFTGLOW_AD}
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
                <a href="https://softglow-ai.com/stock/landing" style="background:#f59e0b;color:#fff;padding:8px 20px;border-radius:6px;text-decoration:none;font-weight:700;font-size:13px">了解年費方案</a>
              </div>
              <div style="background:#eff6ff;border-radius:8px;padding:16px;margin-bottom:20px">
                <p style="margin:0 0 8px;font-weight:700;color:#1e40af">📢 推薦好友，一起分析台股</p>
                <p style="margin:0;font-size:13px;color:#1e3a8a">把線上有位分享給投資朋友，一起利用 AI 找到好的進場位置！</p>
              </div>
              {_SOFTGLOW_AD}
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

    # 寄管理員通知信
    try:
        _amt_map = {499: "月費方案", 999: "季費方案", 3688: "年費方案", 6: "測試方案"}
        _amt_int = int(amount) if str(amount).isdigit() else 0
        _plan_name = _amt_map.get(_amt_int, f"未知方案（NT${amount}）")
        _inv_type = (_po["invoice_type"] or "") if _po else ""
        _inv_carrier = (_po["invoice_carrier"] or "未提供") if _po else "未提供"
        _inv_label = "手機條碼" if _inv_type == "phone" else ("Email 載具" if _inv_type == "email" else "未提供")
        _pay_time = _taipei_now_str("%Y-%m-%d %H:%M:%S")
        _send_email(
            SMTP_USER,
            "【線上有位】新訂單通知",
            f"""<div style="font-family:-apple-system,sans-serif;max-width:480px;margin:0 auto;padding:24px">
              <h2 style="color:#1D9E75;margin:0 0 16px">【線上有位】新訂單通知</h2>
              <table style="width:100%;border-collapse:collapse;font-size:14px">
                <tr><td style="padding:8px 0;color:#888;width:100px">付款時間</td><td style="padding:8px 0;font-weight:700">{_pay_time}</td></tr>
                <tr><td style="padding:8px 0;color:#888">訂單編號</td><td style="padding:8px 0;font-weight:700">{trade_no_w}</td></tr>
                <tr><td style="padding:8px 0;color:#888">付款金額</td><td style="padding:8px 0;font-weight:700">NT$ {amount}</td></tr>
                <tr><td style="padding:8px 0;color:#888">用戶 Email</td><td style="padding:8px 0;font-weight:700">{email}</td></tr>
                <tr><td style="padding:8px 0;color:#888">訂閱方案</td><td style="padding:8px 0;font-weight:700">{_plan_name}</td></tr>
                <tr><td style="padding:8px 0;color:#888">發票類型</td><td style="padding:8px 0;font-weight:700">{_inv_label}</td></tr>
                <tr><td style="padding:8px 0;color:#888">發票載具</td><td style="padding:8px 0;font-weight:700">{_inv_carrier}</td></tr>
              </table>
            </div>"""
        )
    except Exception as _ae:
        print(f"   ⚠️ 管理員通知信失敗：{_ae}")

    print(f"   ✅ Webhook 處理完成：{email} → {plan} 到 {new_expire}")
    return JSONResponse(content="1|OK")


# ══════════════════════════════════════════════════════════
# 聯絡留言板 API
# ══════════════════════════════════════════════════════════

class ContactMessage(BaseModel):
    name: str
    email: str
    message: str
    website: str = ""

class DeleteToken(BaseModel):
    token: str

CONTACT_ADMIN_PWD = "630428"


@app.post("/api/contact")
async def submit_contact(msg: ContactMessage):
    if msg.website:
        return {"ok": True, "id": 0, "message": "訊息已收到"}

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
        _send_email(SMTP_USER, f"【線上有位】新留言來自 {name}", html_body)
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

        # 每 3 人一個獎勵週期，用 referral_rewarded_count 記錄已發放次數，避免重複
        earned_rewards  = cnt // 3
        inviter_row = conn.execute(
            "SELECT referral_unlocked, referral_expire_date, referral_rewarded_count FROM members WHERE email=?",
            (inviter,)
        ).fetchone()
        if not inviter_row:
            print(f"[REFERRAL] {user_email} 完成，inviter={inviter} cnt={cnt}（inviter 不存在）")
            return

        rewarded_so_far = inviter_row["referral_rewarded_count"] or 0
        new_cycles      = earned_rewards - rewarded_so_far  # 本次新達標的週期數

        if new_cycles > 0:
            add_days  = new_cycles * 30
            today_str = _date_cls.today().isoformat()
            # 從現有到期日或今天起計算
            cur_exp   = inviter_row["referral_expire_date"]
            base_date = max(cur_exp, today_str) if cur_exp else today_str
            from datetime import date as _d2
            base      = _d2.fromisoformat(base_date)
            new_exp   = (base + timedelta(days=add_days)).isoformat()

            conn.execute(
                "UPDATE members SET referral_unlocked=1, referral_expire_date=?, "
                "referral_rewarded_count=? WHERE email=?",
                (new_exp, rewarded_so_far + new_cycles, inviter)
            )
            conn.commit()
            _send_email(
                inviter, "【線上有位】恭喜！邀請獎勵解鎖成功",
                f'<p>您已成功邀請 <b>{cnt}</b> 位好友完成首次查詢，'
                f'本次新增 <b>{add_days}</b> 天全功能使用權（有效期至 <b>{new_exp}</b>）。</p>'
                f'<p>每再邀請 3 位好友就自動再延長 30 天，繼續加油！</p>'
                f'<p><a href="{FRONTEND_URL}">立即使用</a></p>'
            )

        print(f"[REFERRAL] {user_email} 完成，inviter={inviter} cnt={cnt} "
              f"earned={earned_rewards} rewarded={rewarded_so_far} new_cycles={new_cycles}")
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



# === AdSense 報告頁廣告注入 ===
def _inject_report_ads(html: str) -> str:
    """在報告頁 HTML 注入 AdSense 廣告"""
    PUB = "ca-pub-1768270548115739"
    SLOT_ARTICLE = "2793159185"
    SLOT_BOTTOM = "4182262477"

    preconnect = '<link rel="preconnect" href="https://pagead2.googlesyndication.com">\n'
    html = html.replace('</head>', preconnect + '</head>', 1)

    in_article_ad = (
        '<div style="margin:20px auto;text-align:center;max-width:728px;">'
        '<ins class="adsbygoogle" style="display:block;text-align:center;min-height:250px;"'
        ' data-ad-layout="in-article" data-ad-format="fluid"'
        f' data-ad-client="{PUB}" data-ad-slot="{SLOT_ARTICLE}"></ins>'
        '<script>try{(adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}</script>'
        '</div>'
    )

    parts = html.split('</section>')
    if len(parts) > 4:
        parts[3] = parts[3] + in_article_ad
        html = '</section>'.join(parts)

    bottom_ad = (
        '<div style="margin:24px auto;text-align:center;max-width:728px;">'
        '<ins class="adsbygoogle" style="display:block;min-height:250px;"'
        f' data-ad-client="{PUB}" data-ad-slot="{SLOT_BOTTOM}"'
        ' data-ad-format="auto" data-full-width-responsive="true"></ins>'
        '<script>try{(adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}</script>'
        '</div>'
    )

    body_pos = html.rfind('</body>')
    if body_pos > 0:
        html = html[:body_pos] + bottom_ad + html[body_pos:]

    ad_script = (
        '<script>'
        'setTimeout(function(){var s=document.createElement("script");s.async=true;'
        f's.src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB}";'
        's.crossOrigin="anonymous";document.head.appendChild(s);},2000);'
        '</script>'
    )

    body_pos = html.rfind('</body>')
    if body_pos > 0:
        html = html[:body_pos] + ad_script + html[body_pos:]

    return html
# === End AdSense 報告頁廣告注入 ===

def _build_report_html(stock_id: str, stock_name: str, report_date: str, d: dict,
                       news_items: list = None) -> str:
    # ── 取欄位 ──
    price         = d.get("price", 0)
    trend         = d.get("trend", "盤整")
    risk_level    = d.get("risk_level", "medium")
    risk_label    = d.get("risk_label", "中風險")
    support       = d.get("support", 0)
    resistance    = d.get("resistance", 0)
    stop_loss     = d.get("stop_loss", 0)
    rr_ratio      = d.get("risk_reward", 0)
    kbar_pattern  = d.get("kbar_pattern", "")
    kbar_action   = d.get("kbar_action", "")
    kbar_warning  = d.get("kbar_warning", "")
    today_breakout = d.get("today_breakout", False)
    today_open    = d.get("today_open")
    today_low     = d.get("today_low")
    prev_high     = d.get("prev_high")
    kline_pattern = d.get("kline_pattern", "")
    win_rate      = d.get("win_rate", 0.5)
    supp_desc     = d.get("support_desc", "")
    res_desc      = d.get("resistance_desc", "")
    market        = _market_cache.get(stock_id, "")
    market_label  = "上市" if market == "tse" else ("上櫃" if market == "otc" else "")

    # 深度分析欄位
    ma_alignment = d.get("ma_alignment") or {}
    kd_status    = d.get("kd_status") or {}
    macd_status  = d.get("macd_status") or {}
    vol_analysis = d.get("vol_analysis") or {}
    risk_factors = d.get("risk_factors") or []

    # ── 色彩計算 ──
    risk_colors = {"low": "#3b82f6", "medium": "#fbbf24", "high": "#f87171"}
    risk_color  = risk_colors.get(risk_level, "#fbbf24")
    ma_dir      = ma_alignment.get("direction", "neutral")
    ma_text     = ma_alignment.get("text", trend)
    ma_color    = "#4ade80" if ma_dir == "bullish" else ("#f87171" if ma_dir == "bearish" else "#fbbf24")
    kd_dir      = kd_status.get("direction", "neutral")
    kd_text     = kd_status.get("text", "")
    kd_color    = "#4ade80" if kd_dir in ("bullish",) else ("#f87171" if kd_dir == "bearish" else "#fbbf24")
    macd_dir    = macd_status.get("direction", "neutral")
    macd_text   = macd_status.get("text", "")
    macd_color  = {"bullish": "#4ade80", "slightly_bullish": "#86efac",
                   "bearish": "#f87171", "slightly_bearish": "#fca5a5"}.get(macd_dir, "#8faabf")
    vol_text    = vol_analysis.get("text", "")
    rr_color    = "#4ade80" if rr_ratio >= 2 else ("#fbbf24" if rr_ratio >= 1 else "#f87171")

    # ── 多空雷達變數 ──
    _tp        = d.get("radar") or {}
    tp_trend   = _tp.get("trend", False)
    tp_macd    = _tp.get("macd",  False)
    tp_vol     = _tp.get("volume", False)
    tp_pos     = _tp.get("position", False)   # T1: 第四格
    tp_score   = _tp.get("score", 0)
    tp_label   = _tp.get("label", "計算中...")
    tp_ma20    = _tp.get("ma20", "-")
    tp_ma60    = _tp.get("ma60", "-")
    tp_hist    = _tp.get("macd_hist", 0)
    tp_vol_ratio = _tp.get("vol_ratio", 1.0)
    tp_stars   = "⭐" * tp_score + "☆" * (4 - tp_score)   # T1: 滿分 4 格
    tp_bias5   = _tp.get("bias5")
    tp_bias20  = _tp.get("bias20")
    tp_bias_entry        = _tp.get("bias_entry", False)
    tp_bias_exit_warning = _tp.get("bias_exit_warning", False)
    tp_ma20_slope        = _tp.get("ma20_slope", "flat")    # T4: 趨勢斜率
    tp_ma5_cross         = _tp.get("ma5_cross_below_ma20", False)  # T7: 均線死叉

    _tp_colors = {4: ("#dcfce7","#166534"), 3: ("#dcfce7","#166534"), 2: ("#fef9c3","#854d0e"), 1: ("#f3f4f6","#374151"), 0: ("#fee2e2","#991b1b")}
    tp_badge_bg, tp_badge_color = _tp_colors.get(tp_score, ("#f3f4f6","#374151"))

    tp_trend_icon  = "✅" if tp_trend else "❌"
    tp_macd_icon   = "✅" if tp_macd  else "❌"
    tp_vol_icon    = "✅" if tp_vol   else "❌"
    tp_pos_icon    = "✅" if tp_pos   else "❌"    # T1
    tp_trend_color = "#16a34a" if tp_trend else "#dc2626"
    tp_macd_color  = "#16a34a" if tp_macd  else "#dc2626"
    tp_vol_color   = "#16a34a" if tp_vol   else "#dc2626"
    tp_pos_color   = "#16a34a" if tp_pos   else "#dc2626"  # T1
    tp_trend_bg    = "#f0fdf4" if tp_trend else "#fff1f2"
    tp_macd_bg     = "#f0fdf4" if tp_macd  else "#fff1f2"
    tp_vol_bg      = "#f0fdf4" if tp_vol   else "#fff1f2"
    tp_pos_bg      = "#f0fdf4" if tp_pos   else "#fff1f2"  # T1

    # ── 距離 % ──
    sup_dist  = round((price - support)    / price * 100, 1) if price and support    else 0
    res_dist  = round((resistance - price) / price * 100, 1) if price and resistance else 0
    stop_dist = round((price - stop_loss)  / price * 100, 1) if price and stop_loss  else 0

    # ── 多空雷達 + 位置綜合判斷 ──
    if tp_score == 4:
        if sup_dist <= 5 and res_dist >= 5:
            tp_position_icon  = "🎯"
            tp_position_text  = f"雷達全亮且靠近支撐（距支撐 -{sup_dist}%），進場時機相對佳"
            tp_position_color = "#16a34a"
            tp_position_bg    = "#f0fdf4"
        elif res_dist < 5:
            tp_position_icon  = "⚠️"
            tp_position_text  = f"雷達全亮但已漲一段（距壓力僅 +{res_dist}%），追高風險高，等回測支撐 {support} 再進場"
            tp_position_color = "#d97706"
            tp_position_bg    = "#fffbeb"
        else:
            tp_position_icon  = "👀"
            tp_position_text  = f"雷達全亮，位於中段（距支撐 -{sup_dist}%，距壓力 +{res_dist}%），可持有，不追高"
            tp_position_color = "#2563eb"
            tp_position_bg    = "#eff6ff"
    elif tp_score == 3:
        if sup_dist <= 5:
            tp_position_icon  = "👀"
            tp_position_text  = f"三格亮，靠近支撐（距支撐 -{sup_dist}%），等第四格補齊再進場"
            tp_position_color = "#2563eb"
            tp_position_bg    = "#eff6ff"
        else:
            tp_position_icon  = "⏳"
            tp_position_text  = f"三格亮，差一格，耐心等待雷達全亮"
            tp_position_color = "#6b7280"
            tp_position_bg    = "#f9fafb"
    else:
        tp_position_icon  = "🚫"
        tp_position_text  = f"多空雷達未齊（{tp_score}/4），暫不適合進場，持續觀察"
        tp_position_color = "#dc2626"
        tp_position_bg    = "#fff1f2"
    wr_pct      = int(win_rate * 100)
    wr_color    = "#4ade80" if wr_pct >= 56 else ("#fbbf24" if wr_pct >= 52 else "#8faabf")
    kp_bullish  = any(x in kline_pattern for x in ["多頭", "早晨", "錘子", "突破", "量增大紅", "連三紅"])
    kp_bearish  = any(x in kline_pattern for x in ["空頭", "黃昏", "流星", "跌破", "量增大黑", "連三黑"])
    kp_color    = "#4ade80" if kp_bullish else ("#f87171" if kp_bearish else "#fbbf24")

    # ── 趨勢文字 ──
    if trend == "上升趨勢":
        trend_desc = "均線三線多頭排列，短均站在長均之上，回測均線是買點；趨勢未明確反轉前，以順勢操作為主。"
    elif trend == "下降趨勢":
        trend_desc = "均線三線空頭排列，短均在長均之下，反彈壓力明顯；逆勢做多風險較高，等待趨勢反轉再評估。"
    else:
        trend_desc = "均線糾結，多空交戰，方向未明；宜等待均線方向明確或突破關鍵位後再跟進。"

    # ── 操作建議文字 ──
    # 突破型態：開高走低風險判斷
    _report_time = datetime.now(ZoneInfo("Asia/Taipei"))
    _report_date_str = _report_time.strftime("%Y-%m-%d")
    _report_time_str = _report_time.strftime("%Y-%m-%d %H:%M")
    _breakout_risk_text = ""
    if today_breakout and today_open and today_low and price:
        _is_open_high_walk_low = float(today_open) > float(price) * 1.005  # 開盤比現價高 0.5% 以上視為開高走低
        if _is_open_high_walk_low:
            _breakout_risk_text = (
                f"\n\n⚠️ 風險提示（{_report_time_str} 資料）：今日出現開高走低，需留意賣壓湧現假突破風險。"
                f"明日若收盤跌破今日低點 {today_low}，視為突破失敗訊號，應出場。"
            )

    if kbar_action:
        op_text = kbar_action + _breakout_risk_text
    elif today_breakout:
        op_text = (f"今日突破前高 {prev_high}，突破型態確立。可持有，防守位 {stop_loss}，目標壓力 {resistance}，損益比 {rr_ratio:.2f}。"
                   + _breakout_risk_text)
    elif tp_score == 0:
        op_text = f"多空雷達三格全滅，技術面偏弱，暫不適合進場。等待趨勢翻多、MACD 翻正、量能放大後再評估。"
    elif tp_score <= 1:
        op_text = f"多空雷達訊號不足，觀望為主。防守位 {stop_loss}，待雷達訊號補齊後再考慮進場。"
    elif trend == "上升趨勢" and rr_ratio >= 2:
        op_text = f"趨勢向上，損益比 {rr_ratio:.2f} 合理。防守位 {stop_loss}，目標壓力 {resistance}。"
    elif trend == "下降趨勢" or rr_ratio < 1:
        op_text = f"趨勢偏弱或損益比 {rr_ratio:.2f} 不理想，建議觀望。等待趨勢反轉訊號，跌破 {stop_loss} 嚴格停損。"
    else:
        op_text = f"趨勢盤整，等待方向確認。關注能否突破壓力 {resistance}，防守位 {stop_loss}，損益比 {rr_ratio:.2f}。"

    # ── 乖離率進出場提示 ──
    _bias_text = ""
    _bias5_str  = f"{tp_bias5:+.1f}%" if tp_bias5 is not None else "-"
    _bias20_str = f"{tp_bias20:+.1f}%" if tp_bias20 is not None else "-"
    _bias5_color  = "#f87171" if tp_bias5 and tp_bias5 > 10 else ("#facc15" if tp_bias5 and tp_bias5 > 5 else ("#4ade80" if tp_bias5 and tp_bias5 < -3 else "var(--text)"))
    _bias20_color = "#f87171" if tp_bias20 and tp_bias20 > 8 else ("#4ade80" if tp_bias20 and tp_bias20 < -8 else "var(--text)")
    if tp_bias_entry:
        _bias_text = f"\n\n✅ 乖離率進場訊號：雷達全亮，MA5 乖離 {_bias5_str}（剛站上均線，未過熱），為相對佳進場位。"
    elif tp_bias_exit_warning == "大":
        _bias_text = f"\n\n🔴 出場風險【大】：MA5 正乖離 {_bias5_str} 已超過 +10%，股價嚴重偏離均線，高檔風險極高，建議減碼或出場。"
    elif tp_bias_exit_warning == "中":
        _bias_text = f"\n\n🟡 出場風險【中】：MA5 正乖離 {_bias5_str} 介於 5%~10%，股價偏離均線，若出現黑K或量縮應注意出場。"
    elif tp_bias_exit_warning == "小":
        _bias_text = f"\n\n🟢 出場風險【小】：KD 死叉且 MACD 動能向下，趨勢轉弱初期，建議提高警覺，設好防守位 {stop_loss}。"
    op_text = op_text + _bias_text

    # ── 多空雷達補充說明 ──
    _tp_missing = []
    if not tp_trend: _tp_missing.append(f"趨勢（需 MA20 {tp_ma20} > MA60 {tp_ma60}）")
    if not tp_macd:  _tp_missing.append(f"MACD（需柱體翻正，目前 {tp_hist}）")
    if not tp_vol:   _tp_missing.append(f"量能（需量比 ≥1.2，目前 {tp_vol_ratio}x）")
    if tp_score == 3:
        tp_supplement_html = ""
    elif _tp_missing:
        _missing_str = "、".join(_tp_missing)
        tp_supplement_html = (
            f'<div style="margin-top:10px;padding:10px 12px;background:#fefce8;border-radius:8px;border-left:3px solid #fbbf24;font-size:12px;color:#78350f;line-height:1.7">'
            f'📋 <b>多空雷達尚缺：</b>{_missing_str}，補齊後進場訊號更強。</div>'
        )
    else:
        tp_supplement_html = ""

    # kbar tag 顏色：依多頭/空頭/中性
    _kbar_bullish_keys = ["錘頭","多頭吞噬","早晨之星","三紅兵","穿刺線","大紅棒"]
    _kbar_bearish_keys = ["射擊之星","空頭吞噬","黃昏之星","三烏鴉","烏雲蓋頂","大黑棒"]
    if any(k in (kbar_pattern or "") for k in _kbar_bullish_keys):
        _kbar_tag_bg, _kbar_tag_color = "#166534", "#bbf7d0"   # 深綠底＋淺綠字
    elif any(k in (kbar_pattern or "") for k in _kbar_bearish_keys):
        _kbar_tag_bg, _kbar_tag_color = "#7f1d1d", "#fecaca"   # 深紅底＋淺紅字
    else:
        _kbar_tag_bg, _kbar_tag_color = "#374151", "#e5e7eb"   # 深灰底＋淺灰字

    market_tag_html = (
        f'<span class="tag" style="background:#1e3a5a;color:var(--text3);margin-left:6px">{market_label}</span>'
        if market_label else ""
    )
    kbar_tag_html = (
        f'<div style="margin-bottom:10px"><span class="tag" style="background:{_kbar_tag_bg};color:{_kbar_tag_color}">{kbar_pattern}</span></div>'
        if kbar_pattern else ""
    )
    kbar_warning_html = (
        f'<div style="font-size:13px;color:#fbbf24;line-height:1.6;margin-bottom:10px">{kbar_warning}</div>'
        if kbar_warning else ""
    )
    kbar_action_html = (
        f'<div style="margin-top:10px;padding:10px;background:var(--stat-bg);border-radius:8px;'
        f'font-size:13px;color:var(--text);line-height:1.6">{kbar_action}</div>'
        if kbar_action else ""
    )
    kd_row_html = (
        f'<div class="irow"><div class="idot" style="background:{kd_color}"></div>'
        f'<div style="font-size:13px;line-height:1.6;color:var(--text)">'
        f'<span style="color:var(--text3);font-size:11px">KD｜</span>{kd_text}</div></div>'
        if kd_text else ""
    )
    macd_row_html = (
        f'<div class="irow"><div class="idot" style="background:{macd_color}"></div>'
        f'<div style="font-size:13px;line-height:1.6;color:var(--text)">'
        f'<span style="color:var(--text3);font-size:11px">MACD｜</span>{macd_text}</div></div>'
        if macd_text else ""
    )
    vol_row_html = (
        f'<div class="irow" style="border-bottom:none"><div class="idot" style="background:#8faabf"></div>'
        f'<div style="font-size:13px;line-height:1.6;color:var(--text)">'
        f'<span style="color:var(--text3);font-size:11px">量能｜</span>{vol_text}</div></div>'
        if vol_text else ""
    )
    risk_items_html = "".join(
        f'<li style="padding:6px 0;border-bottom:1px solid var(--irow-border);font-size:13px;color:var(--text);line-height:1.6">'
        f'&#9651; {r}</li>'
        for r in risk_factors
    ) if risk_factors else '<li style="padding:6px 0;font-size:13px;color:var(--text3)">無明顯技術面警示</li>'

    if news_items:
        news_rows = "".join(
            f'<li style="padding:8px 0;border-bottom:1px solid var(--irow-border)">'
            f'<a href="{n["link"]}" target="_blank" rel="noopener" '
            f'style="color:#3b82f6;font-size:13px;line-height:1.6">{n["title"]}</a></li>'
            for n in news_items
        )
        news_html = (
            '<section class="card">'
            '<h2>相關新聞</h2>'
            f'<ul style="list-style:none">{news_rows}</ul>'
            '</section>'
        )
    else:
        news_html = ""

    json_ld = _json_mod.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{stock_id} {stock_name} 個股分析報告",
        "datePublished": report_date,
        "publisher": {"@type": "Organization", "name": "線上有位"},
        "description": f"{stock_id} {stock_name} {report_date} 技術分析：{trend}，支撐 {support}，壓力 {resistance}，損益比 {rr_ratio:.2f}",
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8MBD31GNL8"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-8MBD31GNL8');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{stock_name}({stock_id}) 能買嗎？多空雷達 × 支撐壓力完整分析 {report_date}｜線上有位</title>
<meta name="description" content="輸入股票代號，AI 自動分析多空雷達、K棒型態、支撐壓力位、葛蘭碧買點，一鍵產出完整報告。免費使用。還有 500+ 計算工具和全球彩票選號。">
<meta property="og:title" content="{stock_id} {stock_name} 分析報告">
<meta property="og:description" content="{trend}｜支撐 {support}｜壓力 {resistance}｜損益比 {rr_ratio:.2f}">
<meta property="og:type" content="article">
<script type="application/ld+json">{json_ld}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#f5f0e8;--bg2:#ede8df;--bg3:#e6dfd4;
  --card:#fff;--border:#d6cfc4;
  --text:#1a1a1a;--text2:#374151;--text3:#6b7280;
  --accent:#1D9E75;--blue:#3b82f6;
  --stat-bg:#f0ebe2;--irow-border:#e0d9d0;
  --h2:#1D9E75;
}}
@media(prefers-color-scheme:dark){{
  :root:not([data-theme="light"]){{
    --bg:#0f1923;--bg2:#1a2634;--bg3:#1e3a5a;
    --card:#1a2634;--border:#1e3a5a;
    --text:#e8e0d0;--text2:#c8c0b0;--text3:#8faabf;
    --accent:#1D9E75;--blue:#3b82f6;
    --stat-bg:#0f1923;--irow-border:#1e3a5a;
    --h2:#3b82f6;
  }}
}}
:root[data-theme="dark"]{{
  --bg:#0f1923;--bg2:#1a2634;--bg3:#1e3a5a;
  --card:#1a2634;--border:#1e3a5a;
  --text:#e8e0d0;--text2:#c8c0b0;--text3:#8faabf;
  --accent:#1D9E75;--blue:#3b82f6;
  --stat-bg:#0f1923;--irow-border:#1e3a5a;
  --h2:#3b82f6;
}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,'Noto Sans TC',sans-serif;min-height:100vh;padding:24px 16px 48px}}
.container{{max-width:720px;margin:0 auto}}
.card{{background:var(--card);border-radius:14px;padding:20px;margin-bottom:16px;border:1px solid var(--border)}}
.tag{{display:inline-block;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700;margin-bottom:8px}}
.row{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px}}
.stat{{background:var(--stat-bg);border-radius:10px;padding:12px;flex:1;min-width:90px}}
.stat-label{{font-size:11px;color:var(--text3);margin-bottom:4px}}
.stat-value{{font-size:18px;font-weight:700}}
.irow{{display:flex;align-items:flex-start;gap:8px;padding:8px 0;border-bottom:1px solid var(--irow-border)}}
.idot{{width:8px;height:8px;border-radius:50%;flex-shrink:0;margin-top:5px}}
h2{{font-size:15px;font-weight:700;margin-bottom:14px;color:var(--h2)}}
a{{color:var(--blue);text-decoration:none}}
a:hover{{text-decoration:underline}}
/* 廣告4格 */
.ad-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:24px auto;max-width:720px}}
@media(min-width:600px){{.ad-grid{{grid-template-columns:repeat(4,1fr)}}}}
.ad-card{{background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden;cursor:pointer;transition:transform .15s}}
.ad-card:hover{{transform:translateY(-2px)}}
.ad-card img{{width:100%;aspect-ratio:1;object-fit:cover}}
.ad-card-body{{padding:8px 10px 10px}}
.ad-card-tag{{font-size:10px;font-weight:700;color:var(--accent);margin-bottom:4px}}
.ad-card-name{{font-size:12px;font-weight:700;color:var(--text);margin-bottom:2px}}
.ad-card-desc{{font-size:11px;color:var(--text3);line-height:1.4}}
/* 亮暗切換鍵 */
#themeBtn{{position:fixed;top:14px;right:14px;z-index:999;background:var(--card);border:1px solid var(--border);border-radius:50%;width:36px;height:36px;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.15);transition:background .2s}}
</style>
</head>
<body>
<button id="themeBtn" onclick="toggleTheme()" title="切換主題">🌓</button>
<script>
(function(){{
  var t=localStorage.getItem('report-theme');
  if(t) document.documentElement.setAttribute('data-theme',t);
}})();
function toggleTheme(){{
  var r=document.documentElement;
  var cur=r.getAttribute('data-theme');
  var sys=window.matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';
  var next;
  if(!cur) next=(sys==='dark'?'light':'dark');
  else if(cur==='dark') next='light';
  else next='dark';
  r.setAttribute('data-theme',next);
  localStorage.setItem('report-theme',next);
}}
</script>
<div class="container">
  <div style="margin-bottom:20px">
    <a href="{FRONTEND_URL}" style="font-size:13px;color:var(--text3)">&#8592; 線上有位</a>
  </div>

  <!-- 1. 基本資訊 -->
  <section class="card" id="basic-info">
    <span class="tag" style="background:{risk_color}22;color:{risk_color}">{risk_label}</span>{market_tag_html}
    <div style="font-size:26px;font-weight:700;margin-bottom:4px">{stock_id} {stock_name}</div>
    <div style="font-size:13px;color:var(--text3);margin-bottom:16px">分析日期：{report_date}</div>
    <div class="row">
      <div class="stat">
        <div class="stat-label">現價</div>
        <div class="stat-value" id="livePrice">{price}</div>
        <div style="font-size:13px;margin-top:3px;min-height:18px" id="liveChange"></div>
      </div>
      <div class="stat">
        <div class="stat-label">趨勢</div>
        <div class="stat-value" style="font-size:15px;color:{ma_color}">{trend}</div>
      </div>
      <div class="stat">
        <div class="stat-label">損益比</div>
        <div class="stat-value" style="color:{rr_color}">{rr_ratio:.2f}</div>
      </div>
    </div>
    <!-- 多空雷達 -->
    <div style="margin-top:16px;padding:14px;background:var(--bg2,#f8f8f8);border-radius:12px">
      <div style="font-size:13px;font-weight:700;color:var(--text2);margin-bottom:10px">
        多空雷達
        <span style="margin-left:8px;font-size:15px">{tp_stars}</span>
        <span style="margin-left:6px;font-size:12px;padding:2px 10px;border-radius:20px;background:{tp_badge_bg};color:{tp_badge_color};font-weight:700">{tp_label}</span>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <div style="flex:1;min-width:100px;padding:8px 12px;border-radius:8px;background:{tp_trend_bg};text-align:center">
          <div style="font-size:11px;color:var(--text3);margin-bottom:3px">① 趨勢</div>
          <div style="font-size:12px;font-weight:600;color:{tp_trend_color}">月線{'>' if tp_trend else '<'}季線 {tp_trend_icon}</div>
          <div style="font-size:10px;color:var(--text3);margin-top:2px">MA20={tp_ma20} / MA60={tp_ma60}</div>
        </div>
        <div style="flex:1;min-width:100px;padding:8px 12px;border-radius:8px;background:{tp_macd_bg};text-align:center">
          <div style="font-size:11px;color:var(--text3);margin-bottom:3px">② MACD</div>
          <div style="font-size:12px;font-weight:600;color:{tp_macd_color}">柱體{'正' if tp_macd else '負'} {tp_macd_icon}</div>
          <div style="font-size:10px;color:var(--text3);margin-top:2px">Histogram={tp_hist}</div>
        </div>
        <div style="flex:1;min-width:100px;padding:8px 12px;border-radius:8px;background:{tp_vol_bg};text-align:center">
          <div style="font-size:11px;color:var(--text3);margin-bottom:3px">③ 資金籌碼</div>
          <div style="font-size:12px;font-weight:600;color:{tp_vol_color}">量{'放大' if tp_vol else '縮'} {tp_vol_icon}</div>
          <div style="font-size:10px;color:var(--text3);margin-top:2px">量比={tp_vol_ratio}x</div>
        </div>
        <div style="flex:1;min-width:100px;padding:8px 12px;border-radius:8px;background:{tp_pos_bg};text-align:center">
          <div style="font-size:11px;color:var(--text3);margin-bottom:3px">④ 位置</div>
          <div style="font-size:12px;font-weight:600;color:{tp_pos_color}">{'適中' if tp_pos else '偏離'} {tp_pos_icon}</div>
          <div style="font-size:10px;color:var(--text3);margin-top:2px">MA5乖離={tp_bias5 if tp_bias5 is not None else '-'}%</div>
        </div>
      </div>
      {f'<div style="margin-top:8px;padding:6px 10px;border-radius:6px;background:#fffbeb;font-size:11px;color:#92400e">T4 趨勢斜率：MA20 方向{"↗ 向上" if tp_ma20_slope == "up" else "↘ 向下" if tp_ma20_slope == "down" else "→ 持平"}{"，短均跌破中均 ⚠" if tp_ma5_cross else ""}</div>' if tp_ma20_slope != "flat" or tp_ma5_cross else ''}
    </div>
  </section>


  <!-- 2. 技術位置 -->
  <section class="card" id="tech-position">
    <h2>技術位置</h2>
    <div class="row">
      <div class="stat">
        <div class="stat-label">支撐位</div>
        <div class="stat-value" style="color:#3b82f6">{support}</div>
        <div style="font-size:11px;color:var(--text3);margin-top:2px">{supp_desc}，距現價 -{sup_dist}%</div>
      </div>
      <div class="stat">
        <div class="stat-label">壓力位</div>
        <div class="stat-value" style="color:#fbbf24">{resistance}</div>
        <div style="font-size:11px;color:var(--text3);margin-top:2px">{res_desc}，距現價 +{res_dist}%</div>
      </div>
    </div>
    <div style="background:var(--stat-bg);border-radius:10px;padding:12px">
      <div class="stat-label" style="margin-bottom:4px">操作防守位（停損線）</div>
      <div style="font-size:18px;font-weight:700;color:#f87171">{stop_loss}</div>
      <div style="font-size:11px;color:var(--text3);margin-top:2px">距現價 -{stop_dist}%，跌破需停損出場</div>
    </div>
  </section>

  <!-- 3. 趨勢判斷 -->
  <section class="card" id="trend-analysis">
    <h2>趨勢判斷</h2>
    <div class="irow">
      <div class="idot" style="background:{ma_color}"></div>
      <div style="font-size:13px;line-height:1.6;color:var(--text)">{ma_text}</div>
    </div>
    <div style="padding:10px 0 0;font-size:13px;line-height:1.7;color:var(--text3)">{trend_desc}</div>
  </section>

  <!-- 4. K線型態 -->
  <section class="card" id="kline-pattern">
    <h2>K線型態</h2>
    {kbar_tag_html}{kbar_warning_html}
    <div class="irow" style="border-bottom:none">
      <div class="idot" style="background:{kp_color}"></div>
      <div>
        <div style="font-size:14px;font-weight:600;color:{kp_color};margin-bottom:2px">{kline_pattern or "常態 K 線"}</div>
        <div style="font-size:12px;color:var(--text3)">大數據歷史勝率 <span style="color:{wr_color};font-weight:700">{wr_pct}%</span></div>
      </div>
    </div>
    {kbar_action_html}
  </section>


  <!-- 5. 動能指標 -->
  <section class="card" id="momentum">
    <h2>動能指標</h2>
    {kd_row_html}{macd_row_html}{vol_row_html}
  </section>

  <!-- 6. 風險評估 -->
  <section class="card" id="risk-assessment">
    <h2>風險評估</h2>
    <div class="row" style="margin-bottom:12px">
      <div class="stat" style="flex:0 0 auto">
        <div class="stat-label">風險等級</div>
        <div class="stat-value" style="color:{risk_color}">{risk_label}</div>
      </div>
      <div class="stat" style="flex:0 0 auto">
        <div class="stat-label">損益比</div>
        <div class="stat-value" style="color:{rr_color}">{rr_ratio:.2f}</div>
        <div style="font-size:11px;color:var(--text3);margin-top:2px">{"良好" if rr_ratio >= 2 else ("尚可" if rr_ratio >= 1 else "偏低")}</div>
      </div>
    </div>
    <ul style="list-style:none">{risk_items_html}</ul>
  </section>

  <!-- 多空雷達判斷 -->
  <section class="card" style="border-left:4px solid {tp_position_color};background:{tp_position_bg}">
    <div style="display:flex;align-items:flex-start;gap:10px">
      <span style="font-size:22px;line-height:1">{tp_position_icon}</span>
      <div>
        <div style="font-size:13px;font-weight:700;color:{tp_position_color};margin-bottom:4px">
          多空雷達判斷 {tp_stars}
          <span style="margin-left:6px;font-size:11px;padding:2px 8px;border-radius:20px;background:{tp_badge_bg};color:{tp_badge_color}">{tp_label}</span>
        </div>
        <div style="font-size:13px;color:var(--text);line-height:1.6">{tp_position_text}</div>
        <div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;font-size:11px">
          <span style="padding:2px 8px;border-radius:20px;background:{tp_trend_bg};color:{tp_trend_color}">① 趨勢 {tp_trend_icon}</span>
          <span style="padding:2px 8px;border-radius:20px;background:{tp_macd_bg};color:{tp_macd_color}">② MACD {tp_macd_icon}</span>
          <span style="padding:2px 8px;border-radius:20px;background:{tp_vol_bg};color:{tp_vol_color}">③ 量能 {tp_vol_icon}</span>
        </div>
        <div style="margin-top:8px;font-size:11px;color:var(--text3)">
          MA5 乖離：<strong style="color:{_bias5_color}">{_bias5_str}</strong>
          &nbsp;｜&nbsp;MA20 乖離：<strong style="color:{_bias20_color}">{_bias20_str}</strong>
        </div>
      </div>
    </div>
  </section>

  <!-- 7. 操作建議 -->
  <section class="card" id="operation-advice">
    <h2>操作建議</h2>
    <div style="font-size:14px;line-height:1.8;color:var(--text);padding:12px;background:var(--stat-bg);border-radius:10px;white-space:pre-line">{op_text}</div>
    {tp_supplement_html}
    <div style="margin-top:12px;display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--text3)">
      <span>停損：<strong style="color:#f87171">{stop_loss}</strong></span>
      <span>支撐：<strong style="color:#3b82f6">{support}</strong></span>
      <span>壓力：<strong style="color:#fbbf24">{resistance}</strong></span>
    </div>
  </section>


  {news_html}

  <section class="card" style="text-align:center">
    <div style="font-size:14px;color:var(--text3);margin-bottom:12px">查看完整互動圖表與即時報價</div>
    <a href="{FRONTEND_URL}?q={stock_id}" style="display:inline-block;background:#3b82f6;color:#fff;padding:12px 28px;border-radius:30px;font-weight:700;font-size:15px">前往線上有位 &#8594;</a>
  </section>

  <!-- 4格精選好物 -->
  <div style="font-size:11px;color:var(--text3);text-align:center;margin-bottom:8px;letter-spacing:.5px">✨ 精選好物 · SOFT GLOW 緩光健康系列</div>
  <div class="ad-grid">
    <a class="ad-card" href="https://watione1.guidemee.cc/products/yWh2aDIQ" target="_blank" rel="noopener" style="text-decoration:none">
      <img src="https://watione1.guidemee.cc/tenancy/assets/oj9qkl/products/Oa9XaH7E5jgkNP7j2YkDaoFpLQPy7K-metaR2VtaW5pX0dlbmVyYXRlZF9JbWFnZV9xYjhoc3hxYjhoc3hxYjhoLnBuZw==-.png" alt="深海之源魚油膠囊" loading="lazy">
      <div class="ad-card-body">
        <div class="ad-card-tag" style="color:#16a34a">Omega-3 84%</div>
        <div class="ad-card-name">深海之源魚油膠囊</div>
        <div class="ad-card-desc">rTG型態高吸收，IFOS 五星認證</div>
      </div>
    </a>
    <a class="ad-card" href="https://watione1.guidemee.cc/products/fjG6XpYz" target="_blank" rel="noopener" style="text-decoration:none">
      <img src="https://watione1.guidemee.cc/tenancy/assets/oj9qkl/products/M9X1tgv26e2Lbxr0m4ckHaeIhrkGd3-metaR2VtaW5pX0dlbmVyYXRlZF9JbWFnZV9jNGVweGZjNGVweGZjNGVwLnBuZw==-.png" alt="雪肌彈力膠原蛋白" loading="lazy">
      <div class="ad-card-body">
        <div class="ad-card-tag" style="color:#db2777">六大專利成分</div>
        <div class="ad-card-name">雪肌彈力膠原蛋白</div>
        <div class="ad-card-desc">由內透亮，醫美指定使用</div>
      </div>
    </a>
    <a class="ad-card" href="https://watione1.guidemee.cc/products/BnlNTsYz" target="_blank" rel="noopener" style="text-decoration:none">
      <img src="https://watione1.guidemee.cc/tenancy/assets/oj9qkl/products/zwfzYPbxjyLkS623gPq2IjdLgOVNLZ-metaR2VtaW5pX0dlbmVyYXRlZF9JbWFnZV9rMmpvZ29rMmpvZ29rMmpvLnBuZw==-.png" alt="纖體飲" loading="lazy">
      <div class="ad-card-body">
        <div class="ad-card-tag" style="color:#ea580c">漢方配方</div>
        <div class="ad-card-name">纖體飲</div>
        <div class="ad-card-desc">溫和調整體態，讓身體慢慢順</div>
      </div>
    </a>
    <a class="ad-card" href="https://watione1.guidemee.cc/products/Gct3MfMg" target="_blank" rel="noopener" style="text-decoration:none">
      <img src="https://watione1.guidemee.cc/tenancy/assets/oj9qkl/products/skSjmETidhxTjLNnLCeH5WdNNHM0YX-metaR2VtaW5pX0dlbmVyYXRlZF9JbWFnZV9vcTR5N3dvcTR5N3dvcTR5LnBuZw==-.png" alt="晶。水漾葉黃素" loading="lazy">
      <div class="ad-card-body">
        <div class="ad-card-tag" style="color:#7c3aed">護眼配方</div>
        <div class="ad-card-name">晶。水漾葉黃素</div>
        <div class="ad-card-desc">葉黃素＋蝦紅素，適合久盯螢幕族</div>
      </div>
    </a>
  </div>
  <div style="font-size:11px;color:var(--text3);text-align:center;margin-bottom:16px">全館滿 2000 元免運 · 新會員首購 95 折</div>

  <!-- 延伸工具推薦 (SEO internal links) -->
  <div style="margin:20px 0;padding:16px 20px;background:var(--card-bg);border:1px solid var(--border);border-radius:12px">
    <div style="font-size:14px;font-weight:600;color:var(--text);margin-bottom:10px">📊 延伸工具推薦</div>
    <div style="font-size:12px;color:var(--text3);margin-bottom:8px">搭配以下免費工具，讓分析更完整：</div>
    <div style="display:flex;flex-wrap:wrap;gap:6px">
      <a href="/tools/stop-loss.html" style="display:inline-block;padding:6px 12px;background:rgba(59,130,246,.1);border-radius:16px;font-size:12px;color:#3b82f6;text-decoration:none">停損計算器</a>
      <a href="/tools/risk-reward.html" style="display:inline-block;padding:6px 12px;background:rgba(59,130,246,.1);border-radius:16px;font-size:12px;color:#3b82f6;text-decoration:none">風險報酬比</a>
      <a href="/tools/position-size.html" style="display:inline-block;padding:6px 12px;background:rgba(59,130,246,.1);border-radius:16px;font-size:12px;color:#3b82f6;text-decoration:none">部位大小計算器</a>
      <a href="/tools/rsi-calculator.html" style="display:inline-block;padding:6px 12px;background:rgba(59,130,246,.1);border-radius:16px;font-size:12px;color:#3b82f6;text-decoration:none">RSI 計算器</a>
      <a href="/tools/macd-calculator.html" style="display:inline-block;padding:6px 12px;background:rgba(59,130,246,.1);border-radius:16px;font-size:12px;color:#3b82f6;text-decoration:none">MACD 計算器</a>
      <a href="/tools/bollinger-bands.html" style="display:inline-block;padding:6px 12px;background:rgba(59,130,246,.1);border-radius:16px;font-size:12px;color:#3b82f6;text-decoration:none">布林通道</a>
      <a href="/tools/fibonacci-retracement.html" style="display:inline-block;padding:6px 12px;background:rgba(59,130,246,.1);border-radius:16px;font-size:12px;color:#3b82f6;text-decoration:none">費波那契回撤</a>
      <a href="/tools/pe-ratio.html" style="display:inline-block;padding:6px 12px;background:rgba(59,130,246,.1);border-radius:16px;font-size:12px;color:#3b82f6;text-decoration:none">本益比計算器</a>
      <a href="/tools/dividend-yield.html" style="display:inline-block;padding:6px 12px;background:rgba(59,130,246,.1);border-radius:16px;font-size:12px;color:#3b82f6;text-decoration:none">殖利率計算器</a>
      <a href="/tools/support-resistance.html" style="display:inline-block;padding:6px 12px;background:rgba(59,130,246,.1);border-radius:16px;font-size:12px;color:#3b82f6;text-decoration:none">支撐壓力分析</a>
    </div>
  </div>

  <div style="font-size:11px;color:var(--text3);text-align:center;margin-top:8px;line-height:1.6">
    &#9888; 本報告僅供參考，不構成買賣建議。投資有風險，請自行評估。
  </div>
</div>
<script>
(function(){{
  var STOCK = "{stock_id}";
  var API   = "{BACKEND_URL}";
  function fetchQuote(){{
    fetch(API + "/api/quote/" + STOCK)
      .then(function(r){{ return r.json(); }})
      .then(function(d){{
        if (d.price == null) return;
        document.getElementById("livePrice").textContent = d.price;
        var chg = d.change, pct = d.change_pct;
        if (chg !== null && chg !== undefined && pct !== null && pct !== undefined){{
          var sign  = chg >= 0 ? "+" : "";
          var color = chg >= 0 ? "#4ade80" : "#f87171";
          document.getElementById("liveChange").innerHTML =
            '<span style="color:' + color + '">' + sign + chg.toFixed(2) +
            ' (' + sign + pct.toFixed(2) + '%)</span>';
        }} else if (d.price_note) {{
          document.getElementById("liveChange").textContent = d.price_note;
        }}
        if (d.in_session){{
          setTimeout(fetchQuote, 15 * 60 * 1000);
        }}
      }})
      .catch(function(e){{ console.warn('[quote]', e); }});
  }}
  fetchQuote();
}})();
</script>
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
        "SELECT * FROM price_alerts WHERE user_email=? ORDER BY created_at DESC",
        (user["email"],)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/alerts")
def create_alert(req: AlertReq, request: Request, user: dict = Depends(require_paid_user)):
    if req.direction not in ("above", "below"):
        raise HTTPException(status_code=400, detail="direction 必須為 above 或 below")
    # 名稱轉代號：非純數字視為中文股名，從對照表解析
    sid_clean = req.stock_id.strip()
    if not sid_clean.replace(".", "").isdigit():
        resolved = _name_to_code.get(sid_clean)
        if not resolved:
            resolved = next((code for name, code in _name_to_code.items() if sid_clean in name), None)
        if resolved:
            sid_clean = resolved
        else:
            raise HTTPException(status_code=404, detail=f"找不到股票：{sid_clean}")
    stock_id_final = sid_clean.upper()
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
        (user["email"], stock_id_final, req.target_price, req.direction, now_str)
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
        if 'id="basic-info"' in (cached["report_html"] or ""):
            return {"ok": True, "url": f"{BACKEND_URL}/report/{stock_id}-{report_date}"}
        # 舊格式（無七欄位）→ 刪除快取，強制重新生成
        conn = _db_conn()
        conn.execute(
            "DELETE FROM stock_reports WHERE stock_id=? AND report_date=?",
            (stock_id, report_date)
        )
        conn.commit()
        conn.close()

    try:
        d = _do_analyze(stock_id, "D", user=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{e}")

    stock_name = d.get("stock_name", stock_id)
    news_items = _fetch_stock_news(stock_id)
    report_html = _inject_report_ads(_build_report_html(stock_id, stock_name, report_date, d, news_items))

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


@app.get("/report/", include_in_schema=False)
def get_report_empty():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=FRONTEND_URL, status_code=301)

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
            "SELECT report_html, report_date FROM stock_reports WHERE stock_id=? ORDER BY created_at DESC LIMIT 1",
            (stock_id,)
        ).fetchone()
    conn.close()

    if row and str(row["report_date"] if "report_date" in row.keys() else '')[:10] != report_date:
        row = None  # 報告日期不符，強制重算

    if row:
        html = row["report_html"] or ""
        if "G-8MBD31GNL8" not in html:
            _ga = ('<!-- Google tag (gtag.js) -->'
                   '<script async src="https://www.googletagmanager.com/gtag/js?id=G-8MBD31GNL8"></script>'
                   '<script>window.dataLayer=window.dataLayer||[];'
                   'function gtag(){dataLayer.push(arguments);}'
                   "gtag('js',new Date());gtag('config','G-8MBD31GNL8');</script>")
            html = html.replace("<head>", "<head>" + _ga, 1)
        html = html.replace('</body>', REPORT_INJECT + '</body>', 1)
        return HTMLResponse(content=html)

    # 即時產生
    try:
        d = _do_analyze(stock_id, "D", user=None)
        stock_name = d.get("stock_name", stock_id)
        news_items = _fetch_stock_news(stock_id)
        html = _inject_report_ads(_build_report_html(stock_id, stock_name, report_date, d, news_items))
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
        html = html.replace('</body>', REPORT_INJECT + '</body>', 1)
        return HTMLResponse(content=html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"無法取得 {stock_id} 報告：{e}")


# ══════════════════════════════════════════════════════════
# SEO：/picks + /rankings + sitemap.xml
# ══════════════════════════════════════════════════════════

@app.get("/picks")
def picks_page():
    """每日精選台股 SSR 頁（公開，15分鐘快取）"""
    import time as _tm, json as _jmod
    from fastapi.responses import HTMLResponse

    now = _tm.time()
    c = SEO_CACHE["picks"]
    picks_json = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "stock_picker", "output", "picks_data.json")

    # 若 JSON 在快取建立後更新過，強制重建
    if c["data"] and c["expires"] > now:
        try:
            if os.path.exists(picks_json) and os.path.getmtime(picks_json) > c.get("built_at", 0):
                c["data"] = None  # JSON 有新版本，捨棄舊快取
        except Exception:
            pass

    if c["data"] and c["expires"] > now:
        return HTMLResponse(c["data"])

    picks_data: dict = {}
    if os.path.exists(picks_json):
        try:
            with open(picks_json, "r", encoding="utf-8") as _f:
                picks_data = _jmod.load(_f)
        except Exception:
            pass

    # generated_at 來自 picks_data.json（非快取建立時間）
    generated_at = picks_data.get("generated_at", "")
    picks        = picks_data.get("picks", [])
    date_str     = generated_at[:10] if generated_at else ""
    count        = len(picks)

    def _sig_color(sig: str) -> str:
        if "金叉" in sig or "MA" in sig:  return ("#14532d", "#86efac")
        if "MACD" in sig:                  return ("#1e3a5f", "#93c5fd")
        if "量" in sig:                    return ("#3b1f6b", "#c4b5fd")
        if "法人" in sig:                  return ("#1f3a2e", "#6ee7b7")
        return ("#374151", "#d1d5db")

    def _score_color(score: int) -> str:
        if score >= 80: return "#16a34a"
        if score >= 65: return "#d97706"
        return "#64748b"

    rows_html = ""
    if picks:
        for i, p in enumerate(picks, 1):
            sid   = p.get("stock_id", "")
            sname = p.get("stock_name", "")
            score = p.get("score", 0)
            sigs  = p.get("signals", [])
            sc    = _score_color(score)
            stock_url = f"{FRONTEND_URL}/?stock={sid}"
            sig_tags = ""
            for sg in sigs:
                bg, fg = _sig_color(sg)
                sig_tags += (f'<span style="font-size:10px;padding:2px 9px;border-radius:20px;'
                             f'background:{bg};color:{fg};font-weight:600">{sg}</span> ')
            is_buy2_only = p.get("is_buy2", False)
            entry_sigs = p.get("entry_signals", [])
            entry_tag = ""
            if "buy1" in entry_sigs:
                entry_tag += '<span style="font-size:10px;padding:2px 8px;border-radius:20px;background:rgba(0,229,160,.15);color:#00e5a0;font-weight:600;margin-left:4px">買1</span>'
            if "buy2" in entry_sigs:
                entry_tag += '<span style="font-size:10px;padding:2px 8px;border-radius:20px;background:rgba(251,191,36,.15);color:#fbbf24;font-weight:600;margin-left:4px">買2</span>'
            risk_row = ""
            if is_buy2_only:
                _sup = p.get("support", "-")
                risk_row = f'<tr><td colspan="4" style="padding:0 14px 10px;font-size:12px;color:#fbbf24">⚠️ 高風險突破型態，建議停損設於近期低點 {_sup} 元以下，嚴守停損。</td></tr>'
            rows_html += f"""
<tr onclick="location.href='{stock_url}'" style="cursor:pointer">
  <td class="r-num">{i}</td>
  <td class="r-stock">
    <a href="{stock_url}">{sid}</a>
    <span class="r-name">{sname}</span>{entry_tag}
  </td>
  <td style="text-align:right">
    <span style="font-size:15px;font-weight:700;color:{sc}">{score}</span>
  </td>
  <td style="padding-right:14px">{sig_tags}</td>
</tr>{risk_row}{f'<tr><td colspan="4" style="padding:0 14px 10px;font-size:12px;color:#a89fc0;line-height:1.6">{p.get("ai_summary","")}</td></tr>' if p.get("ai_summary") else ""}"""
    else:
        rows_html = '<tr><td colspan="4" style="text-align:center;color:#999;padding:32px">尚無選股資料，待每日 16:30 更新</td></tr>'

    json_ld = _jmod.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"台股精選名單 {date_str} — 線上有位",
        "description": f"依均線金叉、KD指標、量能、MACD篩選的台股強勢候選，{date_str} 共 {count} 支",
        "url": f"{BACKEND_URL}/picks",
        "numberOfItems": count,
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "url": f"{BACKEND_URL}/report/{p['stock_id']}-{date_str}",
             "name": f"{p['stock_id']} {p.get('stock_name','')}"}
            for i, p in enumerate(picks)
        ],
    }, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>今日精選股｜AI 篩出的強勢股＋進場理由與停損位 {date_str}｜線上有位</title>
<meta name="description" content="AI 每日從台股篩出均線金叉、KD黃金交叉、量能爆發的強勢股，附進場理由與建議停損位。{date_str} 共 {count} 支入選。還有 500+ 免費計算工具。">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{BACKEND_URL}/picks">
<meta property="og:title" content="今日精選股｜AI 篩出的強勢股＋進場理由 {date_str}｜線上有位">
<meta property="og:description" content="依均線金叉、KD指標、量能、MACD篩選強勢候選股，{date_str} 共 {count} 支入選">
<meta property="og:url" content="{BACKEND_URL}/picks">
<meta property="og:type" content="website">
<script type="application/ld+json">{json_ld}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739" crossorigin="anonymous"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#f5f0e8;color:#333;font-family:-apple-system,'Noto Sans TC',sans-serif;min-height:100vh;padding:20px 16px 60px}}
.wrap{{max-width:720px;margin:0 auto}}
.back{{font-size:13px;color:#666;text-decoration:none;display:inline-block;margin-bottom:20px}}
.back:hover{{color:#333}}
h1{{font-size:22px;font-weight:700;margin-bottom:4px}}
.sub{{font-size:13px;color:#888;margin-bottom:24px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.06)}}
thead th{{padding:10px 12px;font-size:12px;color:#888;font-weight:600;text-align:left;border-bottom:1px solid #f0ebe0;background:#faf7f2}}
tbody tr{{border-bottom:1px solid #f5f0ea;transition:background .12s}}
tbody tr:last-child{{border-bottom:none}}
tbody tr:hover{{background:#faf6ee}}
td{{padding:12px 12px;vertical-align:middle}}
.r-num{{color:#ccc;font-size:13px;width:30px;text-align:center;padding-left:8px}}
.r-stock a{{font-size:15px;font-weight:700;color:#333;text-decoration:none}}
.r-stock a:hover{{color:#555}}
.r-name{{font-size:12px;color:#999;display:block;margin-top:2px}}
.crit{{margin-top:24px;padding:14px 16px;background:#fff;border-radius:10px;font-size:12px;color:#888;line-height:1.8;box-shadow:0 1px 4px rgba(0,0,0,.04)}}
.disclaimer{{margin-top:16px;font-size:11px;color:#bbb;line-height:1.8}}
@media(max-width:480px){{td{{padding:10px 8px}}h1{{font-size:18px}}}}
</style>
</head>
<body>
<div class="wrap">
  <a href="{FRONTEND_URL}" class="back">← 線上有位</a>
  <h1>📈 每日精選台股</h1>
  <p class="sub">資料日期：{generated_at or "尚未產生"}・每日 16:30 更新・共 {count} 支入選</p>
  <table>
    <thead>
      <tr>
        <th>#</th>
        <th>股票</th>
        <th style="text-align:right">評分</th>
        <th>技術訊號</th>
      </tr>
    </thead>
    <tbody>{rows_html}</tbody>
  </table>
  <div class="crit">
    <strong>篩選條件：</strong>
    均線金叉（MA5穿MA20 或 MA20穿MA60）或 KD金叉 ＋ 量能放大（近5日均量 ≥ 20日均量×1.5）＋ MACD DIF &gt; 0
  </div>
  <!-- AdSense 廣告 -->
  <ins class="adsbygoogle"
       style="display:block;margin:24px 0"
       data-ad-client="ca-pub-1768270548115739"
       data-ad-slot="2793159185"
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  <div style="margin:20px 0;padding:14px 18px;background:#f0f7ff;border-radius:10px">
    <div style="font-size:13px;font-weight:600;margin-bottom:8px">📊 延伸工具</div>
    <div style="display:flex;flex-wrap:wrap;gap:6px">
      <a href="/tools/stop-loss.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">停損計算器</a>
      <a href="/tools/risk-reward.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">風險報酬比</a>
      <a href="/tools/position-size.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">部位大小</a>
      <a href="/tools/rsi-calculator.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">RSI</a>
      <a href="/tools/macd-calculator.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">MACD</a>
      <a href="/tools/pe-ratio.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">本益比</a>
    </div>
  </div>
  <p class="disclaimer">⚠️ 本頁面資料僅供參考，不構成任何買賣建議。投資有風險，請自行評估。資料來源：FinMind / TWSE</p>
  <!-- AdSense 底部廣告 -->
  <ins class="adsbygoogle"
       style="display:block;margin:24px 0"
       data-ad-client="ca-pub-1768270548115739"
       data-ad-slot="4182262477"
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
  <script>try{{(adsbygoogle=window.adsbygoogle||[]).push({{}})}}catch(e){{}}</script>
</div>
</body>
</html>"""

    c["data"]     = html
    c["expires"]  = now + 900
    c["built_at"] = now  # 記錄快取建立時間，供 mtime 比對用
    return HTMLResponse(html)

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

    # 取得全台股清單
    try:
        all_stocks = get_all_stock_info()
        all_stock_ids = [s["stock_id"] for s in all_stocks if str(s.get("stock_id","")).isdigit() and len(str(s.get("stock_id",""))) == 4]
    except Exception:
        all_stock_ids = _SEO_HARDCODED_STOCKS

    locs = []
    for u in [FRONTEND_URL + "/", FRONTEND_URL + "/stock/", FRONTEND_URL + "/rankings"]:
        locs.append(f"  <url><loc>{u}</loc><changefreq>daily</changefreq><priority>0.8</priority></url>")

    # ── Tools 工具頁（動態掃描磁碟，避免硬編碼漏頁）──
    _tools_base = os.path.join(os.path.dirname(__file__), "frontend", "tools")
    # zh-TW 根目錄
    locs.append(f"  <url><loc>{FRONTEND_URL}/tools/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>")
    if os.path.isdir(_tools_base):
        for _tf in sorted(os.listdir(_tools_base)):
            if _tf.endswith(".html") and _tf != "index.html":
                _slug = _tf.replace(".html", "")
                locs.append(f"  <url><loc>{FRONTEND_URL}/tools/{_tf}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>")
        # 子語言目錄
        for _lang_dir in sorted(os.listdir(_tools_base)):
            _lang_path = os.path.join(_tools_base, _lang_dir)
            if os.path.isdir(_lang_path) and _lang_dir not in (".", ".."):
                locs.append(f"  <url><loc>{FRONTEND_URL}/tools/{_lang_dir}/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>")
                for _tf in sorted(os.listdir(_lang_path)):
                    if _tf.endswith(".html") and _tf != "index.html":
                        locs.append(f"  <url><loc>{FRONTEND_URL}/tools/{_lang_dir}/{_tf}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>")

    # ── 必備頁面（AdSense 審查加分）──
    for pg in ["about.html", "contact.html", "privacy.html", "terms.html", "disclaimer.html", "refund.html"]:
        locs.append(f"  <url><loc>{FRONTEND_URL}/{pg}</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>")

    # ── Blog 教學文章（繁中 + en/ja/ko）──
    _blog_files = ["kd-indicator","macd-indicator","rsi-indicator","moving-average-guide",
                   "candlestick-patterns","support-resistance","stop-loss-guide",
                   "profit-loss-ratio","position-risk","institutional-investors","stock-selection-guide"]
    locs.append(f"  <url><loc>{FRONTEND_URL}/blog/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>")
    for _bf in _blog_files:
        locs.append(f"  <url><loc>{FRONTEND_URL}/blog/{_bf}.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>")
    for _bl in ("en", "ja", "ko"):
        locs.append(f"  <url><loc>{FRONTEND_URL}/blog/{_bl}/</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>")
        for _bf in _blog_files:
            locs.append(f"  <url><loc>{FRONTEND_URL}/blog/{_bl}/{_bf}.html</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>")

    # ── K棒型態教學（V3 動態掃描磁碟，10 語言）──
    _patterns_base = os.path.join(os.path.dirname(__file__), "frontend", "patterns")
    if os.path.isdir(_patterns_base):
        # zh-TW root patterns
        for _pf in sorted(os.listdir(_patterns_base)):
            if _pf.endswith(".html"):
                locs.append(f"  <url><loc>{FRONTEND_URL}/patterns/{_pf}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>")
        # Sub-language directories
        for _lang_dir in sorted(os.listdir(_patterns_base)):
            _lang_path = os.path.join(_patterns_base, _lang_dir)
            if os.path.isdir(_lang_path) and _lang_dir not in (".", ".."):
                for _pf in sorted(os.listdir(_lang_path)):
                    if _pf.endswith(".html"):
                        locs.append(f"  <url><loc>{FRONTEND_URL}/patterns/{_lang_dir}/{_pf}</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>")

    # ── Glossary 術語百科（動態掃描磁碟，10 語言）──
    _glossary_base = os.path.join(os.path.dirname(__file__), "frontend", "glossary")
    if os.path.isdir(_glossary_base):
        locs.append(f"  <url><loc>{FRONTEND_URL}/glossary/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>")
        for _gf in sorted(os.listdir(_glossary_base)):
            if _gf.endswith(".html") and _gf != "index.html":
                locs.append(f"  <url><loc>{FRONTEND_URL}/glossary/{_gf}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>")
        for _lang_dir in sorted(os.listdir(_glossary_base)):
            _lang_path = os.path.join(_glossary_base, _lang_dir)
            if os.path.isdir(_lang_path) and _lang_dir not in (".", ".."):
                for _gf in sorted(os.listdir(_lang_path)):
                    if _gf.endswith(".html"):
                        locs.append(f"  <url><loc>{FRONTEND_URL}/glossary/{_lang_dir}/{_gf}</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>")

    # ── Comparison 比較頁（V3 動態掃描磁碟，10 語言）──
    _comp_base = os.path.join(os.path.dirname(__file__), "frontend", "comparisons")
    if os.path.isdir(_comp_base):
        # zh-TW root comparisons
        for _cf in sorted(os.listdir(_comp_base)):
            if _cf.endswith(".html"):
                locs.append(f"  <url><loc>{FRONTEND_URL}/comparisons/{_cf}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>")
        # Sub-language directories
        for _lang_dir in sorted(os.listdir(_comp_base)):
            _lang_path = os.path.join(_comp_base, _lang_dir)
            if os.path.isdir(_lang_path) and _lang_dir not in (".", ".."):
                for _cf in sorted(os.listdir(_lang_path)):
                    if _cf.endswith(".html"):
                        locs.append(f"  <url><loc>{FRONTEND_URL}/comparisons/{_lang_dir}/{_cf}</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>")
    # 熱門股優先 priority 0.8，其餘 0.6
    hardcoded_set = set(_SEO_HARDCODED_STOCKS)
    for sid in all_stock_ids:
        priority = "0.8" if sid in hardcoded_set else "0.6"
        locs.append(f"  <url><loc>{FRONTEND_URL}/report/{sid}</loc><changefreq>daily</changefreq><priority>{priority}</priority></url>")
    for r in reports:
        locs.append(f"  <url><loc>{FRONTEND_URL}/report/{r['stock_id']}-{r['report_date']}</loc><changefreq>weekly</changefreq><priority>0.5</priority></url>")

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
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8MBD31GNL8"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-8MBD31GNL8');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>台股今日漲跌排行｜漲幅、跌幅、成交量 Top 20 即時更新｜線上有位</title>
<meta name="description" content="台股今日漲幅榜、跌幅榜、成交量榜 Top 20，即時更新。搭配 AI 個股分析報告（多空雷達＋K棒型態＋支撐壓力），一鍵查看任一股。">
<script type="application/ld+json">{json_ld}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739" crossorigin="anonymous"></script>
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
  <div style="margin:20px 0;padding:14px 18px;background:#f0f7ff;border-radius:10px">
    <div style="font-size:13px;font-weight:600;margin-bottom:8px">📊 延伸工具</div>
    <div style="display:flex;flex-wrap:wrap;gap:6px">
      <a href="/tools/stop-loss.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">停損計算器</a>
      <a href="/tools/risk-reward.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">風險報酬比</a>
      <a href="/tools/position-size.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">部位大小</a>
      <a href="/tools/rsi-calculator.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">RSI</a>
      <a href="/tools/macd-calculator.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">MACD</a>
      <a href="/tools/pe-ratio.html" style="padding:5px 10px;background:#fff;border-radius:14px;font-size:12px;color:#2563EB;text-decoration:none;border:1px solid #dbeafe">本益比</a>
    </div>
  </div>
  <p class="disclaimer">⚠️ 本頁面資料僅供參考，不構成任何買賣建議。投資有風險，請自行評估。<br>資料來源：FinMind</p>
  <!-- AdSense 廣告 -->
  <ins class="adsbygoogle"
       style="display:block;margin:24px 0"
       data-ad-client="ca-pub-1768270548115739"
       data-ad-slot="2793159185"
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
  <script>try{{(adsbygoogle=window.adsbygoogle||[]).push({{}})}}catch(e){{}}</script>
  <!-- AdSense 底部廣告 -->
  <ins class="adsbygoogle"
       style="display:block;margin:24px 0"
       data-ad-client="ca-pub-1768270548115739"
       data-ad-slot="4182262477"
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
  <script>try{{(adsbygoogle=window.adsbygoogle||[]).push({{}})}}catch(e){{}}</script>
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


# ─────────────────────────────────────────────
# 定期定額：產生授權網址
# ─────────────────────────────────────────────
@app.post("/create_order_recurring")
async def create_order_recurring(request: Request):
    """
    前端呼叫此端點，產生綠界定期定額授權頁面（首次刷卡授權）
    Body: { email, plan, password }
    plan: monthly / quarterly / yearly
    """
    import urllib.parse, hashlib, time as _t

    body = await request.json()
    email    = body.get("email", "").strip().lower()
    plan     = body.get("plan", "monthly")
    password = body.get("password", "").strip()

    if not email or not _re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        raise HTTPException(status_code=400, detail="Email 格式不正確")

    plan_info = {
        "monthly":    {"name": "線上有位月費訂閱", "amount": 499,  "days": 30,  "freq": "M", "exec_times": 99},
        "quarterly":  {"name": "線上有位季費訂閱", "amount": 999,  "days": 90,  "freq": "M", "exec_times": 99, "frequency": "3"},
        "yearly":     {"name": "線上有位年費訂閱", "amount": 3688, "days": 365, "freq": "Y", "exec_times": 99},
        "daily_test": {"name": "線上有位每日測試", "amount": 30,   "days": 1,   "freq": "D", "exec_times": 5},
    }
    if plan not in plan_info:
        raise HTTPException(status_code=400, detail="無效方案")

    info = plan_info[plan]
    trade_no = f"XYWR{int(_t.time())}{secrets.token_hex(3).upper()}"

    # 首次扣款日期（今天）
    from zoneinfo import ZoneInfo
    today_str = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y/%m/%d")

    params = {
        "MerchantID":          ECPAY_MERCHANT_ID,
        "MerchantTradeNo":     trade_no,
        "MerchantTradeDate":   _taipei_now_str("%Y/%m/%d %H:%M:%S"),
        "PaymentType":         "aio",
        "ChoosePayment":       "Credit",
        "EncryptType":         "1",
        "ReturnURL":           f"{BACKEND_URL}/webhook/ecpay_recurring",
        "ClientBackURL":       f"{FRONTEND_URL}/stock/landing?pay=done",
        "TotalAmount":         str(info["amount"]),
        "TradeDesc":           "線上有位定期訂閱",
        "ItemName":            info["name"],
        "PeriodAmount":        str(info["amount"]),
        "PeriodType":          info["freq"],
        "Frequency":           str(info.get("frequency", "1")),
        "ExecTimes":           str(info["exec_times"]),
        "PeriodReturnURL":     f"{BACKEND_URL}/webhook/ecpay_recurring",
        "CustomField1":        email,
    }

    # 暫存密碼
    if password and len(password) >= 6:
        _po_conn = _db_conn()
        _po_conn.execute(
            "INSERT OR REPLACE INTO pending_orders "
            "(merchant_trade_no, email, hashed_password, plan, invoice_type, invoice_carrier) VALUES (?, ?, ?, ?, ?, ?)",
            (trade_no, email, _hash_pw(password), plan, "", "")
        )
        _po_conn.commit()
        _po_conn.close()

    # CheckMacValue
    sorted_params = sorted(params.items(), key=lambda x: x[0].lower())
    raw = "&".join(f"{k}={v}" for k, v in sorted_params)
    raw = f"HashKey={ECPAY_HASH_KEY}&{raw}&HashIV={ECPAY_HASH_IV}"
    raw = urllib.parse.quote_plus(raw).lower()
    check_mac = hashlib.sha256(raw.encode()).hexdigest().upper()
    params["CheckMacValue"] = check_mac

    form_html = f"""<!DOCTYPE html><html><body>
<form id="f" method="POST" action="https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5">
{''.join(f'<input type="hidden" name="{k}" value="{v}"/>' for k,v in params.items())}
</form>
<script>document.getElementById('f').submit();</script>
</body></html>"""

    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=form_html)


# ─────────────────────────────────────────────
# 定期定額：定期扣款 Webhook（每期自動續約）
# ─────────────────────────────────────────────
@app.post("/webhook/ecpay_recurring")
async def webhook_ecpay_recurring(request: Request):
    """
    綠界每期扣款成功後打過來，自動幫會員延長到期日
    """
    body = await request.form()
    params = dict(body)
    print(f"[定期定額 Webhook] {params}")

    if params.get("MerchantID") != ECPAY_MERCHANT_ID:
        print(f"[定期定額] ❌ MerchantID 不符")
        return JSONResponse(content="0|Error")

    rtn_code = params.get("RtnCode", "0")
    if rtn_code != "1":
        print(f"[定期定額] 非成功狀態 RtnCode={rtn_code}，略過")
        return JSONResponse(content="1|OK")

    email        = params.get("CustomField1", "").strip().lower()
    trade_no_w   = params.get("MerchantTradeNo", "")
    exec_log     = params.get("ExecLog", "")        # 第幾次扣款
    amount       = params.get("PeriodAmount", "") or params.get("TradeAmt", "") or params.get("Amount", "0")
    item_name    = params.get("ItemName", "")
    payment_date = params.get("PaymentDate", "")    # 扣款日期，用於冪等 key

    if not email:
        print("[定期定額] ❌ email 為空")
        return JSONResponse(content="1|OK")

    # 冪等保護
    _tmp = _db_conn()
    _already = _tmp.execute(
        "SELECT 1 FROM processed_orders WHERE merchant_trade_no=?",
        (f"R_{trade_no_w}_{payment_date}",)
    ).fetchone()
    _po = _tmp.execute(
        "SELECT hashed_password, invoice_type, invoice_carrier FROM pending_orders WHERE merchant_trade_no=?", (trade_no_w,)
    ).fetchone()
    _tmp.close()
    _inv_type    = (_po["invoice_type"]    or "電子發票") if _po else "電子發票"
    _inv_carrier = (_po["invoice_carrier"] or "未提供")   if _po else "未提供"

    if _already:
        print(f"[定期定額] ⚠️ 重複 Webhook {trade_no_w} exec={exec_log}")
        return JSONResponse(content="1|OK")

    # 判斷天數與方案（item_name + amount 雙重保障）
    _amount_int = int(amount) if str(amount).isdigit() else 0
    days = _plan_days(item_name, _amount_int)
    if days >= 365:
        plan = "yearly"
    elif days >= 90:
        plan = "quarterly"
    elif days <= 1:
        plan = "daily_test"
    else:
        plan = "monthly"
    plan_label = {"monthly": "月費方案", "quarterly": "季費方案", "yearly": "年費方案", "daily_test": "每日測試方案"}.get(plan, plan)

    conn = _db_conn()
    row = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()

    if row:
        # 既有會員：延長到期日
        current_expire = row["expire_at"] or _date_cls.today().isoformat()
        base = max(current_expire, _date_cls.today().isoformat())
        new_expire = (datetime.fromisoformat(base) + timedelta(days=days)).strftime("%Y-%m-%d")
        conn.execute(
            "UPDATE members SET plan=?, expire_at=?, merchant_trade_no=? WHERE email=?",
            (plan, new_expire, trade_no_w, email)
        )
        conn.commit()
        conn.close()
        # 寄續約通知信
        _send_email(email, "【線上有位】自動續約成功",
            f"""<div style="font-family:-apple-system,sans-serif;max-width:560px;margin:0 auto;padding:24px">
              <h1 style="font-size:24px;color:#1D9E75;margin:0 0 8px">線上<span style="color:#333">有位</span></h1>
              <p style="color:#666;font-size:13px;margin:0 0 24px">台股技術分析輔助系統</p>
              <div style="background:#f0fdf4;border-radius:12px;padding:24px;border:1px solid #86efac">
                <h2 style="margin:0 0 16px;color:#166534">✅ 自動續約成功</h2>
                <p style="color:#555;margin:0 0 16px">您的{plan_label}已自動續約，感謝您持續支持！</p>
                <table style="width:100%;border-collapse:collapse">
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">方案</td><td style="padding:8px 0;font-weight:700">{plan_label}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">扣款金額</td><td style="padding:8px 0;font-weight:700">NT${amount}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">新到期日</td><td style="padding:8px 0;font-weight:700">{new_expire}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">發票開立方式</td><td style="padding:8px 0;font-weight:700">{_inv_type}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">載具/統編</td><td style="padding:8px 0;font-weight:700">{_inv_carrier}</td></tr>
                </table>
              </div>
              <div style="margin-top:24px;text-align:center">
                <a href="https://softglow-ai.com" style="background:#1D9E75;color:#fff;padding:12px 32px;border-radius:8px;text-decoration:none;font-weight:700">立即使用</a>
              </div>
              <p style="margin-top:24px;font-size:12px;color:#9ca3af;text-align:center">如需取消訂閱，請聯繫客服：watione@yahoo.com.tw</p>
            </div>"""
        )
    else:
        # 首次授權成功（第一期）：建立帳號
        hashed_password = _po["hashed_password"] if _po else _hash_pw(secrets.token_urlsafe(8))
        new_expire = (datetime.now(ZoneInfo("Asia/Taipei")) + timedelta(days=days)).strftime("%Y-%m-%d")
        try:
            conn.execute(
                "INSERT INTO members (email, password, plan, expire_at, merchant_trade_no) VALUES (?, ?, ?, ?, ?)",
                (email, hashed_password, plan, new_expire, trade_no_w)
            )
            conn.commit()
        except Exception as e:
            print(f"[定期定額] 建立帳號失敗: {e}")
            conn.close()
            return JSONResponse(content="1|OK")
        conn.close()
        _send_email(email, "【線上有位】歡迎！您的帳號已開通（定期訂閱）",
            f"""<div style="font-family:-apple-system,sans-serif;max-width:560px;margin:0 auto;padding:24px">
              <h1 style="font-size:24px;color:#1D9E75;margin:0 0 8px">線上<span style="color:#333">有位</span></h1>
              <div style="background:#f0fdf4;border-radius:12px;padding:24px;border:1px solid #86efac;margin-top:16px">
                <h2 style="margin:0 0 16px;color:#166534">🎉 帳號已開通（定期訂閱）</h2>
                <table style="width:100%;border-collapse:collapse">
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">帳號</td><td style="padding:8px 0;font-weight:700">{email}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">密碼</td><td style="padding:8px 0;font-weight:700">您訂購時自行設定的密碼</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">方案</td><td style="padding:8px 0;font-weight:700">{plan_label}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">扣款金額</td><td style="padding:8px 0;font-weight:700">NT${amount}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">到期日</td><td style="padding:8px 0;font-weight:700">{new_expire}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">發票開立方式</td><td style="padding:8px 0;font-weight:700">{_inv_type}</td></tr>
                  <tr><td style="padding:8px 0;color:#888;font-size:13px">載具/統編</td><td style="padding:8px 0;font-weight:700">{_inv_carrier}</td></tr>
                </table>
              </div>
              <div style="margin-top:24px;text-align:center">
                <a href="https://softglow-ai.com" style="background:#1D9E75;color:#fff;padding:12px 32px;border-radius:8px;text-decoration:none;font-weight:700">立即登入使用</a>
              </div>
            </div>"""
        )

    # 記錄已處理
    _rec = _db_conn()
    _rec.execute("INSERT OR IGNORE INTO processed_orders (merchant_trade_no) VALUES (?)",
                 (f"R_{trade_no_w}_{payment_date}",))
    _rec.commit()
    _rec.close()

    # 管理員通知
    try:
        _send_email(SMTP_USER, f"【定期定額】{email} 扣款成功 NT${amount}",
            f"<p>定期定額扣款成功</p><p>Email: {email}<br>方案: {plan_label}<br>金額: NT${amount}<br>次數: {exec_log}</p>")
    except Exception:
        pass

    return JSONResponse(content="1|OK")


# ─────────────────────────────────────────────
# 取消定期定額
# ─────────────────────────────────────────────
@app.post("/cancel_recurring")
async def cancel_recurring(request: Request, current_user: dict = Depends(get_current_user)):
    """
    用戶登入後呼叫，取消綠界定期定額
    需要 Authorization: Bearer <token>
    """
    import urllib.parse, hashlib

    if not current_user:
        raise HTTPException(status_code=401, detail="請先登入")

    email = current_user["email"]

    # 從 DB 查會員，確認是付費用戶
    conn = _db_conn()
    row = conn.execute(
        "SELECT merchant_trade_no FROM processed_orders "
        "WHERE merchant_trade_no LIKE 'XYWR%' "
        "ORDER BY rowid DESC LIMIT 1"
    ).fetchone()

    member = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()
    conn.close()

    if not member or member["plan"] == "free":
        raise HTTPException(status_code=400, detail="您目前沒有有效的定期訂閱")
    today_str = _date_cls.today().isoformat()
    if not member["expire_at"] or member["expire_at"] < today_str:
        raise HTTPException(status_code=400, detail="您目前沒有有效的定期訂閱")

    # 從 members 直接讀訂單號（付款成功時已存入）
    merchant_trade_no = member.get("merchant_trade_no") if isinstance(member, dict) else member["merchant_trade_no"]

    if not merchant_trade_no:
        # 舊帳號沒有存訂單號，fallback 查 pending_orders
        conn3 = _db_conn()
        row3 = conn3.execute(
            "SELECT merchant_trade_no FROM pending_orders WHERE email=? AND merchant_trade_no LIKE 'XYWR%' ORDER BY rowid DESC LIMIT 1",
            (email,)
        ).fetchone()
        conn3.close()
        merchant_trade_no = row3["merchant_trade_no"] if row3 else None

    if not merchant_trade_no:
        raise HTTPException(status_code=400, detail="找不到定期訂閱訂單，請洽客服協助取消")

    # 呼叫綠界全方位金流 CreditCardPeriodAction API 終止（form-urlencoded）
    import time as _time_cancel
    timestamp = str(int(_time_cancel.time()))
    action_params = {
        "MerchantID":      str(ECPAY_MERCHANT_ID),
        "MerchantTradeNo": str(merchant_trade_no),
        "Action":          "Cancel",
        "TimeStamp":       timestamp,
    }
    print(f"[取消定期定額] 送出參數: MerchantID={action_params['MerchantID']} MerchantTradeNo={action_params['MerchantTradeNo']} TimeStamp={timestamp}")
    sorted_p = sorted(action_params.items(), key=lambda x: x[0].lower())
    raw = "&".join(f"{k}={v}" for k, v in sorted_p)
    raw = f"HashKey={ECPAY_HASH_KEY}&{raw}&HashIV={ECPAY_HASH_IV}"
    raw = urllib.parse.quote_plus(raw).lower()
    check_mac = hashlib.sha256(raw.encode()).hexdigest().upper()
    action_params["CheckMacValue"] = check_mac

    import httpx
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://payment.ecpay.com.tw/Cashier/CreditCardPeriodAction",
                data=action_params,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
        result = resp.text
        print(f"[取消定期定額] {email} 結果: {result}")
        if _re.search(r"RtnCode=1(?:[&\s]|$)", result):
            _send_email(email, "【線上有位】定期訂閱已取消",
                f"""<div style="font-family:-apple-system,sans-serif;max-width:560px;margin:0 auto;padding:24px">
                  <h1 style="font-size:24px;color:#1D9E75;margin:0 0 8px">線上<span style="color:#333">有位</span></h1>
                  <div style="background:#fef2f2;border-radius:12px;padding:24px;border:1px solid #fca5a5;margin-top:16px">
                    <h2 style="margin:0 0 12px;color:#991b1b">已取消定期訂閱</h2>
                    <p style="color:#555;margin:0 0 12px">您的定期訂閱已成功取消，不會再自動扣款。</p>
                    <p style="color:#555;margin:0;font-size:13px">本期剩餘天數（至 {member['expire_at']}）仍可繼續使用。</p>
                  </div>
                  <p style="margin-top:24px;font-size:13px;color:#9ca3af;text-align:center">
                    如有問題請聯繫客服：watione@yahoo.com.tw
                  </p>
                </div>"""
            )
            # 管理員通知
            try:
                _send_email(SMTP_USER, f"【取消訂閱】{email}",
                    f"<p>{email} 已取消定期訂閱</p><p>到期日：{member['expire_at']}</p>")
            except Exception:
                pass
            return JSONResponse(content={"ok": True, "msg": "已成功取消定期訂閱"})
        else:
            print(f"[取消定期定額] 綠界回應異常: {result}")
            raise HTTPException(status_code=500, detail="取消失敗，請聯繫客服 watione@yahoo.com.tw")
    except httpx.TimeoutException:
        raise HTTPException(status_code=500, detail="連線綠界逾時，請稍後再試")


# ══════════════════════════════════════════════════════════════
# 持股健檢 API
# ══════════════════════════════════════════════════════════════

@app.get("/portfolio")
def get_portfolio(current_user: dict = Depends(get_current_user)):
    """取得用戶持股清單"""
    email = current_user["email"]
    conn = _db_conn()
    rows = conn.execute(
        "SELECT stock_id, stock_name, cost_price, created_at FROM portfolios WHERE user_email=? ORDER BY created_at",
        (email,)
    ).fetchall()
    conn.close()
    return {"ok": True, "data": [dict(r) for r in rows]}


@app.post("/portfolio/add")
async def add_portfolio(request: Request, current_user: dict = Depends(get_current_user)):
    """新增持股"""
    email   = current_user["email"]
    # 動態計算是否為有效付費會員（members 表無 is_active 欄位，需即時計算）
    today_str = _date_cls.today().isoformat()
    plan      = current_user.get("plan", "free")
    expire_at = current_user.get("expire_at") or ""
    is_paid   = (plan != "free") and bool(expire_at) and (expire_at >= today_str)
    body    = await request.json()
    stock_id   = str(body.get("stock_id", "")).strip()
    cost_price = float(body.get("cost_price", 0))
    stock_name = str(body.get("stock_name", "")).strip()

    if not stock_id or cost_price <= 0:
        raise HTTPException(status_code=400, detail="請輸入正確的股號與成本價")

    conn = _db_conn()
    # 免費會員限 1 支
    if not is_paid:
        count = conn.execute(
            "SELECT COUNT(*) FROM portfolios WHERE user_email=?", (email,)
        ).fetchone()[0]
        if count >= 1:
            conn.close()
            raise HTTPException(status_code=403, detail="免費版最多追蹤 1 支，升級付費方案可無限新增")
    try:
        conn.execute(
            "INSERT OR REPLACE INTO portfolios (user_email, stock_id, stock_name, cost_price) VALUES (?,?,?,?)",
            (email, stock_id, stock_name, cost_price)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()

    return {"ok": True, "msg": f"已新增 {stock_id}"}


@app.delete("/portfolio/{stock_id}")
def delete_portfolio(stock_id: str, current_user: dict = Depends(get_current_user)):
    """刪除持股"""
    email = current_user["email"]
    conn = _db_conn()
    conn.execute(
        "DELETE FROM portfolios WHERE user_email=? AND stock_id=?", (email, stock_id)
    )
    conn.commit()
    conn.close()
    return {"ok": True, "msg": f"已刪除 {stock_id}"}


@app.get("/portfolio/analysis")
async def portfolio_analysis(current_user: dict = Depends(get_current_user)):
    """批次分析持股：損益、技術位置、技術訊號、近5日漲幅"""
    import sys as _sys
    _picker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker")
    if _picker_path not in _sys.path:
        _sys.path.insert(0, _picker_path)

    email = current_user["email"]
    conn = _db_conn()
    rows = conn.execute(
        "SELECT stock_id, stock_name, cost_price FROM portfolios WHERE user_email=?",
        (email,)
    ).fetchall()
    conn.close()

    if not rows:
        return {"ok": True, "data": []}

    results = []
    for row in rows:
        sid        = row["stock_id"]
        cost_price = row["cost_price"]
        stock_name = row["stock_name"] or ""
        # 若名稱與股號相同或空白，從即時報價補抓名稱
        if not stock_name or stock_name == sid:
            stock_name = sid  # 預設先用股號

        # 取即時報價：優先走 get_quote（TWSE MIS → FinMind 備援），比 get_quote_live 更可靠
        try:
            def _safe_price(v):
                try:
                    f = float(v)
                    return f if f > 0 else None
                except Exception:
                    return None
            # 先嘗試從 _QUOTE_CACHE 取（get_quote 已存入）
            _qc = _QUOTE_CACHE.get(sid.upper())
            if not _qc or (_qc["expires"] != 0 and _time_mod.time() >= _qc["expires"]):
                get_quote(sid, user=None)
                _qc = _QUOTE_CACHE.get(sid.upper())
            if _qc and _qc.get("data"):
                _qd = _qc["data"]
                price = _safe_price(_qd.get("price")) or _safe_price(_qd.get("z")) or _safe_price(_qd.get("y")) or 0.0
            else:
                q = get_quote_live(sid)
                price = _safe_price(q.get("z")) or _safe_price(q.get("y")) or 0.0
            # 順便補名稱（從 _name_cache 取）
            cached_name = _name_cache.get(sid, "")
            if cached_name and cached_name != sid:
                stock_name = cached_name
                # 同步更新 DB
                try:
                    _uc = _db_conn()
                    _uc.execute("UPDATE portfolios SET stock_name=? WHERE user_email=? AND stock_id=?",
                                (stock_name, email, sid))
                    _uc.commit()
                    _uc.close()
                except Exception:
                    pass
        except Exception:
            price = 0.0

        # 近90日K線（用現有 fetch_df_finmind）
        try:
            df = fetch_df_finmind(sid, "3mo", "D")
            closes = df["Close"].tolist() if df is not None and len(df) >= 5 else []
            highs  = df["High"].tolist()  if df is not None and len(df) >= 5 else []
            lows   = df["Low"].tolist()   if df is not None and len(df) >= 5 else []
            vols   = df["Volume"].tolist() if df is not None and len(df) >= 5 else []
        except Exception:
            closes, highs, lows, vols = [], [], [], []

        # 損益
        pnl_pct = round((price - cost_price) / cost_price * 100, 2) if cost_price > 0 and price > 0 else 0.0

        # 近5日漲幅（用即時報價當最新價，與損益計算一致）
        gain_5d = 0.0
        if len(closes) >= 6 and price > 0:
            gain_5d = round((price - closes[-6]) / closes[-6] * 100, 2) if closes[-6] > 0 else 0.0
        elif len(closes) >= 6:
            gain_5d = round((closes[-1] - closes[-6]) / closes[-6] * 100, 2) if closes[-6] > 0 else 0.0

        # 支撐壓力（近20日高低點）
        support    = round(min(lows[-20:]),  2) if len(lows)   >= 20 else None
        resistance = round(max(highs[-20:]), 2) if len(highs)  >= 20 else None

        # 距離支撐/壓力 %
        dist_support    = round((price - support)    / price * 100, 2) if support    and price > 0 else None
        dist_resistance = round((resistance - price) / price * 100, 2) if resistance and price > 0 else None

        # 位置判斷
        if support and resistance and price > 0:
            range_pct = (price - support) / (resistance - support) if resistance != support else 0.5
            if range_pct <= 0.33:
                position = "偏低（靠近支撐）"
            elif range_pct >= 0.67:
                position = "偏高（靠近壓力）"
            else:
                position = "中段"
        else:
            position = "—"

        # KD 訊號（使用 main.py 原生 calc_kd）
        kd_signal = "—"
        if len(closes) >= 15 and len(highs) >= 15 and len(lows) >= 15:
            try:
                _h = np.array(highs, dtype=float)
                _l = np.array(lows,  dtype=float)
                _c = np.array(closes, dtype=float)
                k_arr, d_arr = calc_kd(_h, _l, _c)
                K = round(float(k_arr[-1]), 2)
                D = round(float(d_arr[-1]), 2)
                K1 = float(k_arr[-2]) if len(k_arr) >= 2 else K
                D1 = float(d_arr[-2]) if len(d_arr) >= 2 else D
                if K1 < D1 and K > D:
                    kd_label = "KD金叉"
                elif K1 > D1 and K < D:
                    kd_label = "KD死叉"
                elif K > D:
                    kd_label = "K>D偏多"
                else:
                    kd_label = "K<D偏空"
                kd_signal = f"{kd_label}（K={K} D={D}）"
            except Exception:
                pass

        # MACD 訊號（使用 main.py 原生 calc_macd）
        macd_signal = "—"
        if len(closes) >= 35:
            try:
                _c = np.array(closes, dtype=float)
                dif_arr, dea_arr, hist_arr = calc_macd(_c)
                dif  = round(float(dif_arr[-1]),  3)
                dea  = round(float(dea_arr[-1]),  3)
                hist = round(float(hist_arr[-1]), 3)
                hist1 = float(hist_arr[-2]) if len(hist_arr) >= 2 else hist
                if dif > 0 and hist > hist1:
                    macd_label = "軸上增強🚀"
                elif dif > 0:
                    macd_label = "軸上📈"
                elif dif > -0.5:
                    macd_label = "偏弱😐"
                else:
                    macd_label = "軸下📉"
                macd_signal = f"{macd_label}（DIF={dif}）"
            except Exception:
                pass

        # 均線排列（MA5/MA20/MA60）
        ma_trend = "—"
        if len(closes) >= 60:
            try:
                _c = np.array(closes, dtype=float)
                ma5  = calc_ma(_c, 5)[-1]
                ma20 = calc_ma(_c, 20)[-1]
                ma60 = calc_ma(_c, 60)[-1]
                if ma5 > ma20 > ma60:
                    ma_trend = "多頭排列🔼"
                elif ma5 < ma20 < ma60:
                    ma_trend = "空頭排列🔽"
                else:
                    ma_trend = "糾結↔️"
            except Exception:
                pass

        # 今日漲跌幅（現價 vs 昨收）
        change_pct = 0.0
        try:
            _qd2 = (_QUOTE_CACHE.get(sid.upper()) or {}).get("data") or {}
            _y = float(_qd2.get("y") or 0)
            if _y > 0 and price > 0:
                change_pct = round((price - _y) / _y * 100, 2)
        except Exception:
            pass

        results.append({
            "stock_id":        sid,
            "stock_name":      stock_name,
            "cost_price":      cost_price,
            "price":           price,
            "pnl_pct":         pnl_pct,
            "change_pct":      change_pct,
            "gain_5d":         gain_5d,
            "support":         support,
            "resistance":      resistance,
            "dist_support":    dist_support,
            "dist_resistance": dist_resistance,
            "position":        position,
            "kd_signal":       kd_signal,
            "macd_signal":     macd_signal,
            "ma_trend":        ma_trend,
            "closes":          closes[-5:] if len(closes) >= 5 else closes,
        })

    # 組合強弱排行（依近5日漲幅）
    results.sort(key=lambda x: x["pnl_pct"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return {"ok": True, "data": results}


# ══════════════════════════════════════════════════════════════
# 深度選股端點
# ══════════════════════════════════════════════════════════════

@app.get("/deep-analysis")
def deep_analysis_page():
    """回傳深度選股 HTML 頁面（優先從 DB 讀，重啟不消失）"""
    import os
    # 優先從 DB 讀
    _dc = _db_conn()
    _row = _dc.execute("SELECT content FROM html_pages WHERE key='deep_analysis'").fetchone()
    _dc.close()
    if _row:
        return HTMLResponse(content=_row["content"])
    # DB 無資料時 fallback 讀檔
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "stock_picker", "output", "deep_analysis.html"
    )
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="""
    <html><body style="background:#0f172a;color:#94a3b8;font-family:sans-serif;padding:40px;text-align:center">
    <h2>深度選股報告尚未產出</h2>
    <p>每個交易日 17:00 自動更新</p>
    </body></html>""", status_code=200)


@app.post("/admin/run-deep-analysis")
async def admin_run_deep_analysis(key: str = Query(...)):
    """管理員手動觸發深度選股（背景執行）"""
    _check_admin(key)
    import threading
    t = threading.Thread(target=_run_deep_analysis_job, daemon=True)
    t.start()
    return {"ok": True, "msg": "深度選股已開始執行（背景）"}


# ──────────────────────────────────────────
# 全站綜合聊天室 WebSocket
# ──────────────────────────────────────────

class _ChatManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.connections:
            self.connections.remove(ws)

    async def broadcast(self, msg: dict):
        import json
        dead = []
        for ws in self.connections:
            try:
                await ws.send_text(json.dumps(msg, ensure_ascii=False))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

_chat_manager = _ChatManager()


@app.get("/chat/history")
async def chat_history():
    """取得最近 50 則訊息"""
    conn = _db_conn()
    rows = conn.execute(
        "SELECT id, username, is_paid, stock_tag, message, created_at, "
        "COALESCE(msg_type,'text'), COALESCE(image_data,'') "
        "FROM chat_messages ORDER BY id DESC LIMIT 50"
    ).fetchall()
    conn.close()
    return {"messages": [
        {"id": r[0], "username": r[1], "is_paid": bool(r[2]),
         "stock_tag": r[3], "message": r[4],
         "created_at": r[5][:16] if r[5] else '',
         "msg_type": r[6], "image_data": r[7] or None}
        for r in reversed(rows)
    ]}


@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket, token: str = ""):
    """全站綜合聊天室 WebSocket"""
    import json

    # 驗證身份（token 選填，有登入才有付費徽章）
    username = "訪客"
    is_paid = False
    if token:
        try:
            payload = _decode_token(token)
            email = payload.get("sub", "")
            conn = _db_conn()
            row = conn.execute(
                "SELECT email, expire_at FROM members WHERE email=?", (email,)
            ).fetchone()
            conn.close()
            if row:
                username = email.split("@")[0]
                # 有設暱稱優先用暱稱
                nick = conn.execute("SELECT nickname FROM members WHERE email=?", (email,)).fetchone()
                if nick and nick[0]:
                    username = nick[0]
                from datetime import datetime
                from zoneinfo import ZoneInfo
                now_tw = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")
                is_paid = bool(row[1] and row[1] > now_tw)
        except Exception:
            pass

    await _chat_manager.connect(ws)
    # 推送在線人數
    await _chat_manager.broadcast({"type": "online", "count": len(_chat_manager.connections)})

    try:
        while True:
            raw = await ws.receive_text()
            try:
                data = json.loads(raw)
            except Exception:
                continue

            message = str(data.get("message", "")).strip()[:300]
            stock_tag = str(data.get("stock_tag", "")).strip()[:10]
            msg_type = str(data.get("msg_type", "text"))
            image_data = data.get("image_data", None)

            # 圖片訊息：有 image_data 才算有效；文字訊息：message 不得為空
            if msg_type == "image":
                if not image_data or not str(image_data).startswith("data:image/"):
                    continue
                # 限制圖片大小（base64 約 4MB）
                if len(str(image_data)) > 4 * 1024 * 1024:
                    continue
            else:
                msg_type = "text"
                if not message:
                    continue

            # 存入 DB
            conn = _db_conn()
            conn.execute(
                "INSERT INTO chat_messages (username, is_paid, stock_tag, message, msg_type, image_data) VALUES (?,?,?,?,?,?)",
                (username, int(is_paid), stock_tag, message, msg_type, image_data if msg_type == "image" else None)
            )
            conn.commit()
            conn.close()

            from datetime import datetime
            from zoneinfo import ZoneInfo
            created_at = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%H:%M")

            await _chat_manager.broadcast({
                "type": "message",
                "msg_type": msg_type,
                "username": username,
                "is_paid": is_paid,
                "stock_tag": stock_tag,
                "message": message,
                "image_data": image_data if msg_type == "image" else None,
                "created_at": created_at,
            })

    except WebSocketDisconnect:
        _chat_manager.disconnect(ws)
        await _chat_manager.broadcast({"type": "online", "count": len(_chat_manager.connections)})


# ──────────────────────────────────────────
# 留言板 API
# ──────────────────────────────────────────

@app.get("/forum/posts")
async def forum_get_posts(
    stock_code: str = "",
    page: int = 1,
    user: dict | None = Depends(get_current_user)
):
    """取得主題列表（非會員可看標題，付費會員看全文）"""
    limit = 20
    offset = (page - 1) * limit
    conn = _db_conn()
    if stock_code:
        rows = conn.execute(
            "SELECT p.id, p.nickname, p.title, p.content, p.stock_code, p.created_at, "
            "(SELECT COUNT(*) FROM forum_comments c WHERE c.post_id=p.id) as comment_count "
            "FROM forum_posts p WHERE p.stock_code=? ORDER BY p.id DESC LIMIT ? OFFSET ?",
            (stock_code.upper(), limit, offset)
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM forum_posts WHERE stock_code=?", (stock_code.upper(),)).fetchone()[0]
    else:
        rows = conn.execute(
            "SELECT p.id, p.nickname, p.title, p.content, p.stock_code, p.created_at, "
            "(SELECT COUNT(*) FROM forum_comments c WHERE c.post_id=p.id) as comment_count "
            "FROM forum_posts p ORDER BY p.id DESC LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM forum_posts").fetchone()[0]
    conn.close()

    is_paid = False
    if user:
        today = _date_cls.today().isoformat()
        is_paid = (user.get("plan") != "free" and user.get("expire_at", "") >= today) or _is_referral_active(user)

    posts = []
    for r in rows:
        post = {
            "id": r[0],
            "nickname": r[1],
            "title": r[2],
            "stock_code": r[4],
            "created_at": r[5][:16] if r[5] else "",
            "comment_count": r[6],
        }
        if is_paid:
            post["content"] = r[3]
        posts.append(post)

    return {"posts": posts, "total": total, "page": page, "is_paid": is_paid}


@app.post("/forum/posts")
async def forum_create_post(
    request: Request,
    user: dict = Depends(require_paid_user)
):
    """發表新主題（需付費會員）"""
    data = await request.json()
    title = str(data.get("title", "")).strip()[:100]
    content = str(data.get("content", "")).strip()[:2000]
    stock_code = str(data.get("stock_code", "")).strip()[:10].upper()
    nickname = str(data.get("nickname", "")).strip()[:20] or user.get("nickname") or user["email"].split("@")[0]

    if not title or not content:
        raise HTTPException(status_code=400, detail="標題和內容不能為空")

    conn = _db_conn()
    conn.execute(
        "INSERT INTO forum_posts (user_id, nickname, title, content, stock_code) VALUES (?,?,?,?,?)",
        (user["id"], nickname, title, content, stock_code)
    )
    conn.commit()
    post_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return {"ok": True, "post_id": post_id}


@app.get("/forum/posts/{post_id}")
async def forum_get_post(post_id: int, user: dict | None = Depends(get_current_user)):
    """取得單篇主題和留言（需付費會員）"""
    conn = _db_conn()
    row = conn.execute("SELECT * FROM forum_posts WHERE id=?", (post_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="找不到此主題")

    is_paid = False
    if user:
        today = _date_cls.today().isoformat()
        is_paid = (user.get("plan") != "free" and user.get("expire_at", "") >= today) or _is_referral_active(user)

    if not is_paid:
        conn.close()
        raise HTTPException(status_code=403, detail="需付費會員才能查看內容")

    comments = conn.execute(
        "SELECT id, nickname, content, created_at FROM forum_comments WHERE post_id=? ORDER BY id ASC",
        (post_id,)
    ).fetchall()
    conn.close()

    return {
        "post": {
            "id": row["id"],
            "nickname": row["nickname"],
            "title": row["title"],
            "content": row["content"],
            "stock_code": row["stock_code"],
            "created_at": row["created_at"][:16] if row["created_at"] else "",
        },
        "comments": [
            {"id": c[0], "nickname": c[1], "content": c[2], "created_at": c[3][:16] if c[3] else ""}
            for c in comments
        ]
    }


@app.post("/forum/posts/{post_id}/comments")
async def forum_create_comment(
    post_id: int,
    request: Request,
    user: dict = Depends(require_paid_user)
):
    """新增留言（需付費會員）"""
    data = await request.json()
    content = str(data.get("content", "")).strip()[:1000]
    nickname = str(data.get("nickname", "")).strip()[:20] or user.get("nickname") or user["email"].split("@")[0]

    if not content:
        raise HTTPException(status_code=400, detail="留言不能為空")

    conn = _db_conn()
    row = conn.execute("SELECT id FROM forum_posts WHERE id=?", (post_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="找不到此主題")

    conn.execute(
        "INSERT INTO forum_comments (post_id, user_id, nickname, content) VALUES (?,?,?,?)",
        (post_id, user["id"], nickname, content)
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@app.get("/forum/stock-discussion-count")
async def forum_stock_discussion_count(codes: str = ""):
    """查詢多支股票的討論數（分析頁提示用）codes=2330,2317"""
    if not codes:
        return {"counts": {}}
    code_list = [c.strip().upper() for c in codes.split(",") if c.strip()][:10]
    conn = _db_conn()
    result = {}
    for code in code_list:
        count = conn.execute(
            "SELECT COUNT(*) FROM forum_posts WHERE stock_code=?", (code,)
        ).fetchone()[0]
        if count > 0:
            result[code] = count
    conn.close()
    return {"counts": result}


# ──────────────────────────────────────────
# 批次預產生報告頁（SEO 用）
# ──────────────────────────────────────────

def _run_batch_report_job():
    """每天 18:30 自動跑下一批 200 支，全部跑完後停止"""
    try:
        all_stocks = get_all_stock_info()
        stock_list = [
            s for s in all_stocks
            if str(s.get("stock_id", "")).isdigit() and len(str(s.get("stock_id", ""))) == 4
        ]
        today = _taipei_today()
        # 找出今天還沒產生的
        conn = _db_conn()
        done_ids = set(r[0] for r in conn.execute(
            "SELECT stock_id FROM stock_reports WHERE report_date=?", (today,)
        ).fetchall())
        conn.close()
        pending = [s for s in stock_list if str(s["stock_id"]) not in done_ids]
        if not pending:
            print(f"[batch_report] 今日 {today} 全部 {len(stock_list)} 支已完成")
            return
        batch = pending[:200]
        print(f"[batch_report] 開始，今日剩餘 {len(pending)} 支，本次跑 {len(batch)} 支")
        done = 0
        for s in batch:
            sid = str(s["stock_id"])
            sname = s.get("stock_name", sid)
            try:
                d = _do_analyze(sid, "D", user=None)
                news_items = _fetch_stock_news(sid)
                report_html = _inject_report_ads(_build_report_html(sid, sname, today, d, news_items))
                conn = _db_conn()
                conn.execute(
                    "INSERT OR REPLACE INTO stock_reports (stock_id, report_date, stock_name, report_html) VALUES (?,?,?,?)",
                    (sid, today, sname, report_html)
                )
                conn.commit()
                conn.close()
                done += 1
                import time as _t; _t.sleep(0.5)
            except Exception as _e:
                print(f"[batch_report] {sid} 失敗：{_e}")
        print(f"[batch_report] 完成，本次產生 {done} 支，剩餘 {len(pending)-done} 支")
    except Exception as e:
        print(f"[batch_report] 執行失敗：{e}")

@app.post("/admin/batch-generate-reports")
async def admin_batch_generate_reports(
    key: str = Query(...),
    batch_size: int = Query(default=200),
    offset: int = Query(default=0)
):
    """批次預產生股票報告頁，每次跑 batch_size 支，從 offset 開始"""
    _check_admin(key)
    import threading

    def _run():
        try:
            all_stocks = get_all_stock_info()
            stock_list = [
                s for s in all_stocks
                if str(s.get("stock_id", "")).isdigit() and len(str(s.get("stock_id", ""))) == 4
            ]
            batch = stock_list[offset: offset + batch_size]
            today = _taipei_today()
            done = 0
            skipped = 0
            for s in batch:
                sid = str(s["stock_id"])
                sname = s.get("stock_name", sid)
                try:
                    conn = _db_conn()
                    cached = conn.execute(
                        "SELECT 1 FROM stock_reports WHERE stock_id=? AND report_date=?",
                        (sid, today)
                    ).fetchone()
                    conn.close()
                    if cached:
                        skipped += 1
                        continue
                    d = _do_analyze(sid, "D", user=None)
                    news_items = _fetch_stock_news(sid)
                    report_html = _inject_report_ads(_build_report_html(sid, sname, today, d, news_items))
                    conn = _db_conn()
                    conn.execute(
                        "INSERT OR REPLACE INTO stock_reports (stock_id, report_date, stock_name, report_html) VALUES (?,?,?,?)",
                        (sid, today, sname, report_html)
                    )
                    conn.commit()
                    conn.close()
                    done += 1
                    import time as _t; _t.sleep(0.5)
                except Exception as _e:
                    print(f"[batch] {sid} 失敗：{_e}")
            print(f"[batch] 完成：done={done}, skipped={skipped}, total={len(batch)}")
        except Exception as e:
            print(f"[batch] 執行失敗：{e}")

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return {"ok": True, "msg": f"批次產生已開始，offset={offset}，batch_size={batch_size}"}


# ══════════════════════════════════════════════════════════
# Threads OAuth
# ══════════════════════════════════════════════════════════

@app.get("/auth/threads", include_in_schema=False)
def auth_threads_redirect():
    """產生 Threads OAuth 授權網址並 redirect"""
    from fastapi.responses import RedirectResponse
    import urllib.parse
    params = urllib.parse.urlencode({
        "client_id": THREADS_APP_ID,
        "redirect_uri": THREADS_REDIRECT_URI,
        "scope": THREADS_SCOPE,
        "response_type": "code",
    })
    auth_url = f"https://threads.net/oauth/authorize?{params}"
    return RedirectResponse(url=auth_url)


@app.get("/auth/threads/callback", include_in_schema=False)
async def auth_threads_callback(code: str = Query(...)):
    """接收 Threads OAuth code，換取 access_token 並存入 DB"""
    from fastapi.responses import HTMLResponse
    import urllib.request, urllib.parse, json as _json

    # 換取 access_token
    token_url = "https://graph.threads.net/oauth/access_token"
    post_data = urllib.parse.urlencode({
        "client_id": THREADS_APP_ID,
        "client_secret": THREADS_APP_SECRET,
        "redirect_uri": THREADS_REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": code,
    }).encode()
    req = urllib.request.Request(token_url, data=post_data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            token_data = _json.loads(resp.read())
    except Exception as e:
        return HTMLResponse(content=f"<h2>❌ 換取 token 失敗：{e}</h2>", status_code=500)

    access_token = token_data.get("access_token", "")
    user_id = str(token_data.get("user_id", ""))

    if not access_token:
        return HTMLResponse(content="<h2>❌ 未取得 access_token</h2>", status_code=500)

    # 取得帳號名稱
    account_name = user_id
    try:
        me_url = (
            f"https://graph.threads.net/v1.0/me"
            f"?fields=id,username&access_token={access_token}"
        )
        me_req = urllib.request.Request(me_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(me_req, timeout=10) as me_resp:
            me_data = _json.loads(me_resp.read())
        account_name = me_data.get("username") or user_id
    except Exception:
        pass

    # 存入 DB
    conn = _db_conn()
    conn.execute(
        "INSERT INTO threads_tokens (token, account_name, created_at) VALUES (?, ?, datetime('now','+8 hours'))",
        (access_token, account_name),
    )
    conn.commit()
    conn.close()

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head><meta charset="UTF-8"><title>Threads 授權成功</title>
<style>body{{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#f0f0f0}}
.box{{background:#fff;padding:2rem 3rem;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.1);text-align:center}}</style>
</head>
<body><div class="box">
<h2>✅ Threads 授權成功</h2>
<p>帳號：<strong>@{account_name}</strong></p>
<p>Access Token 已儲存，可關閉此視窗。</p>
</div></body></html>"""
    return HTMLResponse(content=html)
