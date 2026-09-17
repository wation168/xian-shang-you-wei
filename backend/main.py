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
_INSECURE_JWT_DEFAULT = "change-me-in-production-please"
_JWT_MIN_LEN = 32
JWT_SECRET = os.environ.get("JWT_SECRET", "").strip()
JWT_EXPIRE_DAYS = 15   # token 有效天數（15 天）
# P0 fail-closed: missing, insecure default, or too-short secret must not sign tokens
if (not JWT_SECRET) or (JWT_SECRET == _INSECURE_JWT_DEFAULT) or (len(JWT_SECRET) < _JWT_MIN_LEN):
    print("[JWT] FATAL: JWT_SECRET missing, insecure default, or shorter than 32 chars; refusing to start. Set JWT_SECRET env.")
    raise SystemExit(1)

# 管理後台金鑰（安全性修正 2026/07/26：原本共用 JWT_SECRET 前16碼，已改成獨立金鑰）
# 請在 Zeabur 設定環境變數 ADMIN_API_KEY（建議用一長串隨機字串）
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "")
if not ADMIN_API_KEY:
    print("⚠️  [ADMIN] 未設定 ADMIN_API_KEY，管理後台端點（/admin/*）將全部無法存取，請至 Zeabur 設定此環境變數。")

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
# 2026/08/16修正：原本站內幾處「管理員通知信」（補單/新留言/扣款成功/取消訂閱）
# 都直接寄到SMTP_USER這個變數，但SMTP_USER其實是SMTP登入帳號，不保證是真人信箱——
# 08/05切換到Resend後，SMTP_USER的值固定是Resend規定的SMTP登入帳號"resend"字面值，
# 不是一個能收信的地址，導致這幾種管理員通知信從切換後就一直寄不出去（帥哥鴻回報「訂閱信件問題」的根因）。
# 改成獨立的ADMIN_NOTIFY_EMAIL環境變數，跟SMTP登入帳號脫鉤，請在Zeabur設定成真正要收通知的信箱。
ADMIN_NOTIFY_EMAIL = os.environ.get("ADMIN_NOTIFY_EMAIL", "")

# SQLite 資料庫路徑（Zeabur 持久化硬碟）
DB_PATH = os.environ.get("DB_PATH", "/data/members.db")

# Web Push VAPID 金鑰（請在 Zeabur 設定環境變數，或用 py-vapid 產生一次）
VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY", "")
VAPID_PUBLIC_KEY  = os.environ.get("VAPID_PUBLIC_KEY",  "")
VAPID_SUBJECT     = os.environ.get("VAPID_SUBJECT", f"mailto:{os.environ.get('SMTP_FROM','admin@example.com')}")

# Threads OAuth
THREADS_APP_ID     = os.environ.get("THREADS_APP_ID",     "1011864388160019")
# 安全性修正（2026/07/26）：舊版此處寫死真實密鑰，已移除。Threads 自動發文功能已暫停，
# 若之後要重新啟用，請先去 Meta 開發者後台重新產生 App Secret，再設定 Zeabur 環境變數 THREADS_APP_SECRET。
THREADS_APP_SECRET = os.environ.get("THREADS_APP_SECRET", "")
THREADS_REDIRECT_URI = os.environ.get("THREADS_REDIRECT_URI", "https://api.softglow-ai.com/auth/threads/callback")
THREADS_SCOPE      = "threads_basic,threads_content_publish"

# LINE Login（2026/08/15 新增：帥哥鴻要求「用google或line登入」加入遊戲排行榜）
# 需要在 LINE Developers Console（https://developers.line.biz/console/）建立一個
# 「LINE Login」channel，把Channel ID / Channel Secret設成Zeabur環境變數
# LINE_CHANNEL_ID / LINE_CHANNEL_SECRET，並在該channel的Callback URL設定裡
# 加上 LINE_REDIRECT_URI 這個網址，否則LINE登入按鈕點了會失敗（Google登入不受影響，
# 因為GOOGLE_CLIENT_ID已經是現成、正在運作的設定）。
LINE_CHANNEL_ID     = os.environ.get("LINE_CHANNEL_ID", "")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
# LINE Bot（Messaging API，2026/08/15新增，群組/聊天室打股號查報告用）——
# 跟上面LINE Login用的LINE_CHANNEL_ID/SECRET是完全不同的LINE channel
# （LINE Login跟Messaging API是不同channel類型，不能共用），不要搞混
LINE_BOT_CHANNEL_SECRET       = os.environ.get("LINE_BOT_CHANNEL_SECRET", "")
LINE_BOT_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_BOT_CHANNEL_ACCESS_TOKEN", "")
LINE_REDIRECT_URI   = os.environ.get("LINE_REDIRECT_URI", "https://api.softglow-ai.com/auth/line/callback")

# pywebpush（選裝）
try:
    from pywebpush import webpush as _webpush_fn, WebPushException as _WebPushException
    _WEBPUSH_AVAILABLE = True
except ImportError:
    _WEBPUSH_AVAILABLE = False

# 免費用戶每日查詢次數
FREE_DAILY_LIMIT = 5   # 免費會員：完整分析＋健檢共用 daily_credit
GUEST_DAILY_LIMIT = 3   # 遊客：個股查詢／完整分析 daily_credit

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

    # 啟動時載入全台股名稱快取（2026/09/17改：FinMind失敗時改用資料庫備份＋證交所／櫃買官方清單，並自動重試）
    try:
        _load_stock_name_cache("啟動", allow_official=False)
    except Exception as e:
        print(f"   ⚠️ 股名快取載入失敗（{e}）")
    if len(_name_cache) < _NAME_CACHE_MIN:
        import threading as _th_nm
        _th_nm.Thread(target=_load_stock_name_cache, args=("啟動背景補抓",), daemon=True).start()

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
                    "WHERE plan != 'free' AND expire_at IS NOT NULL AND expire_at >= ? "
                    "AND merchant_trade_no IS NULL",
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
                            _render_email(
                                title="訂閱即將到期",
                                title_icon="⏰",
                                body_html=(
                                    f'<p style="color:#444;margin:0 0 12px;font-size:14px;line-height:1.7">親愛的會員您好，</p>'
                                    f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                                    f'您的付費方案將於 <b>{m["expire_at"]}</b> 到期（剩 3 天）。為避免即時分析、深度選股、到價提醒等會員功能中斷，'
                                    f'建議您把握時間續訂。若您已設定定期定額自動續約，系統將自動為您扣款，可忽略本提醒。</p>'
                                ),
                                cta_text="立即續訂",
                                cta_url=f"{FRONTEND_URL}/stock/landing#pricing",
                                with_ad=True,
                                accent="#f59e0b",
                                card_bg="#fff8e1", card_border="#fcd34d", title_color="#92400e",
                            ))
                        _update_notice_date(m["email"], today_str)
                    elif delta == 0:
                        _send_email(m["email"], "【線上有位】訂閱已到期",
                            _render_email(
                                title="訂閱已到期",
                                title_icon="📅",
                                body_html=(
                                    f'<p style="color:#444;margin:0 0 12px;font-size:14px;line-height:1.7">親愛的會員您好，</p>'
                                    f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                                    f'您的付費方案已於今日（{today_str}）到期，即時分析、深度選股、到價提醒等會員功能已暫停使用。'
                                    f'完成續訂後，所有功能將立即恢復，您的持股追蹤與提醒設定都會保留。歡迎隨時回來繼續使用。</p>'
                                ),
                                cta_text="立即續訂",
                                cta_url=f"{FRONTEND_URL}/stock/landing#pricing",
                                with_ad=True,
                                accent="#ef4444",
                                card_bg="#fef2f2", card_border="#fca5a5", title_color="#991b1b",
                            ))
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
                # 每股只呼叫一次 get_quote（利用 _QUOTE_CACHE，2026/07/30 改用共用函式）
                stock_prices: dict = {}
                for _a in alerts:
                    sid = _a["stock_id"]
                    if sid in stock_prices:
                        continue
                    try:
                        _qd = _get_live_quote_data(sid)
                        stock_prices[sid] = float(_qd["price"]) if _qd else None
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
                        _render_email(
                            title="到價提醒觸發",
                            title_icon="🔔",
                            body_html=(
                                f'<p style="color:#444;margin:0 0 12px;font-size:14px;line-height:1.7">親愛的會員您好，</p>'
                                f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                                f'您設定追蹤的個股已觸及提醒條件，詳情如下。請留意本提醒僅供參考，不構成投資建議，交易決策請自行判斷。</p>'
                                f'<div style="background:#fff;border-radius:8px;padding:14px 16px;border:1px solid #f0f0f0">'
                                f'<p style="margin:0;font-size:15px;color:#166534;font-weight:700">{_body}</p></div>'
                            ),
                            cta_text="立即查看",
                            cta_url=f"{FRONTEND_URL}/stock",
                            with_ad=True,
                            card_bg="#f0fdf4", card_border="#86efac", title_color="#166534",
                        ))
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

        _補單_checked: dict = {}  # trade_no -> 上次查詢時間（避免一直查同一筆未付款訂單，綠界查太快會回 403）

        def _run_補單_job():
            """每 10 分鐘掃 pending_orders，用綠界 QueryTradeInfo 補查「已付款但沒收到/沒通過開通通知」的訂單並補開通。
            2026/09/17 重寫：原版檢查 RtnCode，但 QueryTradeInfo 根本不回傳 RtnCode（是 TradeStatus），
            所以補單從來沒成功過；且方案天數判斷錯誤（季費被當月費）、會直接覆蓋到期日、每天才跑一次。"""
            import time as _t2
            try:
                conn = _db_conn()
                # 保留 7 天內的暫存訂單（原本 24 小時就刪）
                conn.execute("DELETE FROM pending_orders WHERE created_at <= datetime('now','+8 hours','-7 days')")
                conn.commit()
                rows = conn.execute(
                    "SELECT merchant_trade_no, email, plan, created_at FROM pending_orders "
                    "WHERE merchant_trade_no LIKE 'XYWR%' "
                    "AND created_at <= datetime('now','+8 hours','-5 minutes') "
                    "AND created_at >= datetime('now','+8 hours','-2 days') "
                    "ORDER BY created_at DESC"
                ).fetchall()
                conn.close()
            except Exception as _e:
                print(f"   [補單] ❌ 讀取失敗：{_e}")
                return
            _now = _t2.time()
            queried = 0
            for row in rows:
                trade_no = row["merchant_trade_no"]
                email    = (row["email"] or "").strip().lower()
                plan     = row["plan"] if row["plan"] in ("monthly", "quarterly", "yearly", "daily_test") else "monthly"
                try:
                    _tc = _db_conn()
                    _done = _tc.execute(
                        "SELECT 1 FROM processed_orders WHERE merchant_trade_no=? OR merchant_trade_no LIKE ?",
                        (trade_no, f"R_{trade_no}_%")
                    ).fetchone()
                    _tc.close()
                    if _done:
                        continue
                    # 同一筆未付款訂單：建立1小時內每次都查，之後每6小時查一次
                    _last = _補單_checked.get(trade_no, 0)
                    try:
                        _age_h = (datetime.now(ZoneInfo("Asia/Taipei")).replace(tzinfo=None)
                                  - datetime.fromisoformat(row["created_at"])).total_seconds() / 3600
                    except Exception:
                        _age_h = 0
                    if _last and (_now - _last) < (600 if _age_h < 1 else 6 * 3600):
                        continue
                    if queried >= 10:
                        break
                    queried += 1
                    _t2.sleep(2)
                    _resp = _ecpay_query_trade(trade_no)
                    _補單_checked[trade_no] = _now
                    if _resp.get("TradeStatus") != "1":
                        continue
                    pay_date = _resp.get("PaymentDate", "")
                    idem_key = f"R_{trade_no}_{pay_date}"
                    _cl = _db_conn()
                    _claimed = _cl.execute(
                        "INSERT OR IGNORE INTO processed_orders (merchant_trade_no) VALUES (?)", (idem_key,)
                    ).rowcount
                    _cl.commit()
                    if not _claimed:
                        _cl.close()
                        continue
                    days = {"monthly": 30, "quarterly": 90, "yearly": 365, "daily_test": 1}[plan]
                    today = _taipei_today()
                    m = _cl.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()
                    prev_plan   = m["plan"] if m else ""
                    prev_expire = (m["expire_at"] if m else "") or ""
                    prev_trade  = (m["merchant_trade_no"] if m else "") or ""
                    dup = bool(m and prev_trade.startswith("XYWR") and prev_trade != trade_no
                               and prev_plan != "free" and prev_expire >= today)
                    base = max(prev_expire or today, today)
                    new_expire = (datetime.fromisoformat(base) + timedelta(days=days)).strftime("%Y-%m-%d")
                    if m:
                        _cl.execute(
                            "UPDATE members SET plan=?, expire_at=?, merchant_trade_no=? WHERE email=?",
                            (plan, new_expire, prev_trade if dup else trade_no, email)
                        )
                    else:
                        _cl.execute(
                            "INSERT INTO members (email, password, plan, expire_at, merchant_trade_no) VALUES (?,?,?,?,?)",
                            (email, _hash_pw(secrets.token_urlsafe(12)), plan, new_expire, trade_no)
                        )
                    _cl.commit()
                    _cl.close()
                    print(f"   [補單] ✅ 補開通：{email} {trade_no} → {plan} 到 {new_expire}")
                    plan_label = {"monthly": "月費方案", "quarterly": "季費方案", "yearly": "年費方案", "daily_test": "每日測試方案"}[plan]
                    try:
                        _send_email(email, "【線上有位】付款已確認，會員已開通",
                            _render_email(
                                title="付款已確認，會員已開通",
                                title_icon="✅",
                                body_html=(
                                    f'<p style="color:#444;margin:0 0 12px;font-size:14px;line-height:1.7">親愛的會員您好，</p>'
                                    f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                                    f'系統已確認您的付款，{plan_label}已開通，到期日為 <b>{new_expire}</b>。'
                                    f'開通時間有延遲，造成不便敬請見諒。重新整理頁面即可使用完整會員功能。</p>'
                                ),
                                cta_text="立即使用",
                                cta_url=f"{FRONTEND_URL}/stock/",
                                with_ad=False,
                            )
                        )
                    except Exception:
                        pass
                    try:
                        if ADMIN_NOTIFY_EMAIL:
                            _send_admin_payment_notice(
                                email=email, trade_no=trade_no, ecpay_tx_no=_resp.get("TradeNo", ""),
                                amount=_resp.get("TradeAmt", ""), plan_label=plan_label + "（補單排程開通）",
                                is_renewal=False, period_no="1", pay_time=pay_date,
                                payment_type=_resp.get("PaymentType", ""), prev_plan=prev_plan,
                                prev_expire=prev_expire, prev_trade=prev_trade, new_expire=new_expire,
                                is_new_account=not bool(m), inv_type="—", inv_carrier="—",
                                recent_orders="—", dup_warning=dup, simulate=False,
                            )
                    except Exception:
                        pass
                except Exception as _e:
                    print(f"   [補單] ❌ {trade_no} 處理失敗：{_e}")

        _bg_scheduler = BackgroundScheduler(timezone="Asia/Taipei")
        _bg_scheduler.add_job(_run_opening_scan_job,    "cron",     hour=9,  minute=6,  day_of_week="mon-fri")
        _bg_scheduler.add_job(_run_opening_scan_job,    "cron",     hour=13, minute=45, day_of_week="mon-fri")  # 收盤後更新今日收盤價
        # 2026/09/17：深度選股（_run_deep_analysis_job，平日17:00）帥哥鴻決定下架，由12金叉選股接手
        _bg_scheduler.add_job(_run_multi_signal_scan_job, "cron",  hour=17, minute=20, day_of_week="mon-fri")  # 12金叉選股法（文件B十六節）
        _bg_scheduler.add_job(_run_expire_notice_job,   "cron",     hour=9,  minute=0)
        _bg_scheduler.add_job(_reset_alert_triggered,   "cron",     hour=9,  minute=0,  day_of_week="mon-fri")
        _bg_scheduler.add_job(_run_intraday_alert_job,  "interval", minutes=5)
        _bg_scheduler.add_job(_run_intraday_snapshot_job, "interval", minutes=5)  # 江波圖方案B：記錄盤中價格
        _bg_scheduler.add_job(_clear_quote_cache,       "cron",     hour=9,  minute=0,  day_of_week="mon-fri")
        _bg_scheduler.add_job(_clear_quote_cache,       "cron",     hour=14, minute=0,  day_of_week="mon-fri")  # 收盤後清快取，確保盤後覆盤資料一致
        _bg_scheduler.add_job(_run_補單_job,            "interval", minutes=10)  # 2026/09/17：原每天08:00，改每10分鐘
        _bg_scheduler.add_job(_ensure_stock_name_cache,  "interval", minutes=10)  # 2026/09/17：股名快取不足時自動重抓
        # 2026/08/16取消：帥哥鴻確認當初這支每日批次預產生報告是為了SEO覆蓋率，
        # 但實際上不是所有股票都會有人搜尋，天天跑一輪去硬產生冷門股報告不划算；
        # 加上get_report()已修復成「查詢當下沒有今天的資料就即時分析」，資料正確性
        # 不再依賴這支批次工作。函式定義保留在下面（_run_batch_report_job），
        # 只是不再排程自動執行；如果之後想針對特定股票手動預產生，
        # 用既有的 POST /admin/batch-generate-reports 管理端點即可。
        _bg_scheduler.start()
        print("   ✅ APScheduler 排程已啟動（開盤熱門股 09:06、盤中到價提醒每5分鐘、到期通知 09:00、報價快取清除 09:00、補單 08:00、12金叉選股 17:20）")

        # 啟動時補跑12金叉選股（2026/09/15新增：平日17:20之後重新部署/重啟時，
        # 如果今天multi_signal_results還沒有資料就補跑一次，避免漏掉當天）
        try:
            from zoneinfo import ZoneInfo as _ZI_ms
            _now_ms = datetime.now(_ZI_ms("Asia/Taipei"))
            if _now_ms.weekday() < 5 and (_now_ms.hour, _now_ms.minute) >= (17, 20):
                _dc_ms = _db_conn()
                _row_ms = _dc_ms.execute(
                    "SELECT COUNT(*) FROM multi_signal_results WHERE scan_date=?",
                    (_now_ms.strftime("%Y-%m-%d"),)
                ).fetchone()
                _dc_ms.close()
                if not _row_ms or _row_ms[0] == 0:
                    print("   ⚠️ 今日12金叉選股尚未產出，啟動補跑（延遲60秒，等服務完全啟動）...")
                    import threading as _th_ms
                    _th_ms.Thread(target=_run_multi_signal_scan_job,
                                  kwargs={"start_delay": 60}, daemon=True).start()
                else:
                    print(f"   ✅ 今日12金叉選股已產出（{_row_ms[0]}筆），不需補跑")
        except Exception as _mse:
            print(f"   ⚠️ 補跑12金叉選股檢查失敗：{_mse}")

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


# ---- ECPay 簽章驗證模組（獨立檔案 ecpay_verify.py，邏輯不寫在 main.py） ----
try:
    import ecpay_verify as _ecpay_verify_mod
    if getattr(_ecpay_verify_mod, "router", None) is not None:
        app.include_router(_ecpay_verify_mod.router)
    print("✅ ecpay_verify 模組已載入")
except Exception as _e:
    _ecpay_verify_mod = None
    print(f"⚠️ ecpay_verify 模組載入失敗（webhook 仍會照舊運作）：{_e}")


# ---- Lottery subdomain 301 redirect middleware ----
from starlette.middleware.base import BaseHTTPMiddleware

class LotteryRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        host = request.headers.get("host", "")
        path = request.url.path
        # 2026/08/13修正：這個middleware原本會把lottery子網域下「所有」路徑都當成
        # 舊版彩票頁面網址硬轉址，結果連/api/開頭的路徑（例如排程用的cron端點）也被
        # 一起攔截轉成亂七八糟的網址，回應301但轉去不存在的頁面。/api/開頭的路徑
        # 一律放行給後面的正常路由處理，不做轉址。
        if "lottery.softglow-ai.com" in host and not path.startswith("/api/"):
            from starlette.responses import RedirectResponse
            parts = [p for p in path.strip("/").split("/") if p]
            _known_locales = ("en","ja","ko","fr","de","es","pt","id","zh-CN")
            if parts and parts[0] in _known_locales:
                locale = parts[0]
                rest = parts[1:]
            elif parts and parts[0] == "zh-TW":
                locale = "zh-TW"
                rest = parts[1:]
            else:
                # 舊網址沒有語言前綴（第一段直接是彩票/工具代號），預設視為繁中版
                # 2026/08/02修正：避免第一段被誤判成語言代碼、導致整批網址錯轉去彩票首頁
                locale = "zh-TW"
                rest = parts
            lottery_slug = rest[0] if len(rest) > 0 else ""
            page_type = rest[1] if len(rest) > 1 else ""
            if locale in _known_locales:
                if page_type == "number-generator":
                    # 選號產生器新版改為全站共用一頁，不再逐彩票分頁（2026/08/02修正）
                    new_path = f"/lottery/{locale}/number-generator.html"
                elif page_type:
                    new_path = f"/lottery/{locale}/{lottery_slug}-{page_type}.html"
                elif lottery_slug:
                    new_path = f"/lottery/{locale}/{lottery_slug}.html"
                else:
                    new_path = f"/lottery/{locale}/"
                # 2026/08/08修正：該語言若沒有這款外國彩票的頁面（例如ja只做了日本樂透6，
                # 沒做mega-sena/korea-lotto/uk-lotto/euromillions），fallback到en版，
                # 跟網站自己首頁導覽的邏輯一致（ja/index.html裡這些外國彩票連結本來就指向en版）
                if new_path.endswith(".html") and locale != "en":
                    _full_path = os.path.join(_FRONTEND_DIR, "lottery", new_path[len("/lottery/"):])
                    if not os.path.isfile(_full_path):
                        new_path = new_path.replace(f"/lottery/{locale}/", "/lottery/en/", 1)
            else:
                if page_type == "number-generator":
                    new_path = "/lottery/number-generator.html"
                elif page_type:
                    new_path = f"/lottery/{lottery_slug}-{page_type}.html"
                elif lottery_slug:
                    new_path = f"/lottery/{lottery_slug}.html"
                else:
                    new_path = "/lottery/"
            return RedirectResponse(url=f"https://softglow-ai.com{new_path}", status_code=301)
        return await call_next(request)

app.add_middleware(LotteryRedirectMiddleware)

# ---- www → non-www 301 redirect middleware ----
class WwwRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        host = request.headers.get("host", "")
        if host.startswith("www."):
            from starlette.responses import RedirectResponse
            new_url = str(request.url).replace("://www.", "://", 1)
            return RedirectResponse(url=new_url, status_code=301)
        return await call_next(request)

app.add_middleware(WwwRedirectMiddleware)

# ---- API subdomain noindex middleware（api.softglow-ai.com 是後端API專用子網域，不應被搜尋引擎索引）----
class ApiNoindexMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        host = request.headers.get("host", "")
        if "api.softglow-ai.com" in host:
            response.headers["X-Robots-Tag"] = "noindex"
        return response

app.add_middleware(ApiNoindexMiddleware)

# ---- 網頁不快取（2026/09/17）----
# 原本 HTML 沒有 Cache-Control，手機瀏覽器（特別是 iPhone Safari）會自己決定快取多久，
# 改版上線後客人還在用舊版頁面（例：舊版升級按鈕在手機按了沒反應）。
# 改成每次都先跟伺服器確認有沒有新版（沒變時伺服器回 304，幾乎不耗流量）。
class HtmlNoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        ctype = response.headers.get("content-type", "")
        if ctype.startswith("text/html") and "cache-control" not in response.headers:
            response.headers["Cache-Control"] = "no-cache"
        return response

app.add_middleware(HtmlNoCacheMiddleware)

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
    if qs and ("stock=" in qs or "report=" in qs or "tab=" in qs or "q=" in qs):
        return RedirectResponse(f"/stock/?{qs}", status_code=302)
    # 優先回傳 homepage.html，不存在則 fallback 到 index.html
    hp = _os.path.join(_FRONTEND_DIR, "homepage.html")
    if _os.path.isfile(hp):
        return FileResponse(hp)
    return FileResponse(_os.path.join(_FRONTEND_DIR, "index.html"))

@app.get("/api/app-version", include_in_schema=False)
def api_app_version():
    """前端用來判斷網站是否已改版（index.html 的修改時間＋大小）"""
    try:
        st = os.stat(os.path.join(_FRONTEND_DIR, "index.html"))
        v = f"{int(st.st_mtime)}-{st.st_size}"
    except Exception:
        v = ""
    return JSONResponse({"v": v}, headers={"Cache-Control": "no-store"})

@app.get("/stock", include_in_schema=False)
@app.get("/stock/", include_in_schema=False)
async def serve_stock_app():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(_FRONTEND_DIR, "index.html"))

try:
    from quiz.main import app as _quiz_app
    app.mount("/quiz-api", _quiz_app)
    print("✅ quiz 學測評量子服務已掛載")
except Exception as _e:
    print(f"⚠️ quiz 學測評量子服務載入失敗（不影響主站）：{_e}")

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

@app.get("/patterns", include_in_schema=False)
@app.get("/patterns/", include_in_schema=False)
async def serve_patterns_index():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "patterns", "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

# ── Patterns slug redirect map (old sitemap slug → actual filename) ──
_PATTERN_REDIRECTS = {
    "abandoned-baby-bear": "abandoned-baby-bearish",
    "dark-cloud-cover": "dark-cloud",
    "falling-three": "falling-three-methods",
    "kicking-bearish": "kicker-bearish",
    "kicking-bullish": "kicker-bullish",
    "marubozu-bearish": "bearish-marubozu",
    "marubozu-bullish": "bullish-marubozu",
    "rising-three": "rising-three-methods",
    "tri-star-bearish": "tri-star",
    "tri-star-bullish": "tri-star",
}

@app.get("/patterns/{filename}.html", include_in_schema=False)
async def serve_patterns_html(filename: str):
    from fastapi.responses import FileResponse, RedirectResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "patterns", f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    # Check redirect map
    new_slug = _PATTERN_REDIRECTS.get(filename)
    if new_slug:
        return RedirectResponse(f"/patterns/{new_slug}.html", status_code=301)
    # Unknown pattern → redirect to index
    return RedirectResponse("/patterns/", status_code=301)

@app.get("/patterns/{locale}", include_in_schema=False)
@app.get("/patterns/{locale}/", include_in_schema=False)
async def serve_patterns_locale_index(locale: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "patterns", locale, "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/patterns/{locale}/{filename}.html", include_in_schema=False)
async def serve_patterns_locale_html(locale: str, filename: str):
    from fastapi.responses import FileResponse, RedirectResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "patterns", locale, f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    new_slug = _PATTERN_REDIRECTS.get(filename)
    if new_slug:
        return RedirectResponse(f"/patterns/{locale}/{new_slug}.html", status_code=301)
    return RedirectResponse(f"/patterns/{locale}/", status_code=301)

def _serve_locale_file(dirname: str, filename: str, locale: str | None = None, valid_locales: tuple | None = None):
    """
    2026/07/30：共用的靜態頁面服務邏輯，取代 blog/comparisons 每個路由各自複製貼上的
    「檢查locale合法性→組路徑→檔案存在就回傳→不存在回404」邏輯，行為完全不變。
    """
    import os as _os
    from fastapi.responses import FileResponse
    if locale is not None:
        if valid_locales and locale not in valid_locales:
            return JSONResponse({"detail": "Not Found"}, status_code=404)
        path = _os.path.join(_FRONTEND_DIR, dirname, locale, filename)
    else:
        path = _os.path.join(_FRONTEND_DIR, dirname, filename)
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)


@app.get("/blog/{filename}.html", include_in_schema=False)
async def serve_blog_html(filename: str):
    return _serve_locale_file("blog", f"{filename}.html")

@app.get("/blog", include_in_schema=False)
@app.get("/blog/", include_in_schema=False)
async def serve_blog_index():
    return _serve_locale_file("blog", "index.html")

_BLOG_LOCALES = ("en", "ja", "ko", "es", "pt", "id", "de", "fr", "zh-CN")

@app.get("/blog/{locale}/{filename}.html", include_in_schema=False)
async def serve_blog_locale_html(locale: str, filename: str):
    return _serve_locale_file("blog", f"{filename}.html", locale, _BLOG_LOCALES)

@app.get("/blog/{locale}", include_in_schema=False)
@app.get("/blog/{locale}/", include_in_schema=False)
async def serve_blog_locale_index(locale: str):
    return _serve_locale_file("blog", "index.html", locale, _BLOG_LOCALES)

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

@app.get("/tools/tools-chart.js", include_in_schema=False)
async def serve_tools_chart_js():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "tools", "tools-chart.js")
    if _os.path.isfile(path):
        return FileResponse(path, media_type="application/javascript")
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/quiz/{filename}.html", include_in_schema=False)
async def serve_quiz_html(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "quiz", f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

# ── Tools slug redirect map (old renamed slug → actual filename) ──
_TOOLS_REDIRECTS = {
    "tax-bracket": "income-tax",
    "heloc-calculator": "heloc-vs-personal-loan",
    "protein-intake": "protein-calculator",
    "pension-calculator": "pension-vs-lump-sum",
    "roofing-calculator": "roof-area",
    "water-usage": "water-intake",
    "pet-insurance": "pet-insurance-calc",
}
# zh-CN 專屬：中國稅制沒有 sales tax，僅有增值稅，故導向 vat-calculator（多國增值稅比較工具）
_TOOLS_REDIRECTS_ZH_CN = {
    "sales-tax": "vat-calculator",
}

@app.get("/tools/{filename}.html", include_in_schema=False)
async def serve_tools_html(filename: str):
    from fastapi.responses import FileResponse, RedirectResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "tools", f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    new_slug = _TOOLS_REDIRECTS.get(filename)
    if new_slug:
        return RedirectResponse(f"/tools/{new_slug}.html", status_code=301)
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
    from fastapi.responses import FileResponse, RedirectResponse
    import os as _os
    if locale not in _TOOLS_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "tools", locale, f"{filename}.html")
    try:
        if _os.path.isfile(path):
            return FileResponse(path)
    except Exception:
        pass
    new_slug = _TOOLS_REDIRECTS.get(filename)
    if locale == "zh-CN" and not new_slug:
        new_slug = _TOOLS_REDIRECTS_ZH_CN.get(filename)
    if new_slug:
        return RedirectResponse(f"/tools/{locale}/{new_slug}.html", status_code=301)
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


# ---- Games 遊戲路由（2026/08/15 新增，沿用 /tools/ 的路由模式）----
@app.get("/games/games.css", include_in_schema=False)
async def serve_games_css():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "games", "games.css")
    if _os.path.isfile(path):
        return FileResponse(path, media_type="text/css")
    return JSONResponse({"detail": "Not Found"}, status_code=404)

# 2026/08/15 新增：games-auth.js（排行榜/登入共用JS）原本沒有對應路由會直接404，
# 用跟games.css一樣的模式補上，用{filename}.js讓之後如果再加其他共用JS也不用重複加路由
@app.get("/games/{filename}.js", include_in_schema=False)
async def serve_games_js(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "games", f"{filename}.js")
    if _os.path.isfile(path):
        return FileResponse(path, media_type="application/javascript")
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/games/{filename}.html", include_in_schema=False)
async def serve_games_html(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "games", f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/games", include_in_schema=False)
@app.get("/games/", include_in_schema=False)
async def serve_games_index():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "games", "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

# ---- Games 遊戲區多語言路由（2026/08/17 新增，沿用 /tools/ 與 /glossary/ 同一套模式）----
# 遊戲區從單一繁中擴充到10語言。網址結構刻意跟工具頁完全一致：
#   * 繁中維持在 /games/xxx.html（根目錄、無語言前綴），原有網址完全不變，SEO資產不流失
#   * 其餘9語言在 /games/{locale}/xxx.html，各語言獨立網址並互相標註 hreflang，
#     讓 Google 可以個別收錄各語言版本（若用「同一網址靠JS切換語言」則不會被分別收錄）
#   * 遊戲邏輯本身統一放在 /games/shared/xxx.js，10語言共用同一份檔案 —— 這是這次
#     多語言化最關鍵的架構決定：邏輯只有一份，修一次bug全部語言同時生效，不會出現
#     10個語言版本各自帶一份複製的遊戲引擎、之後改東西要改10次的維護地獄。
#     頁面內的文字則由各語言HTML自帶的 window.GAME_I18N / window.GA_LANG_PACK 字典提供。
_GAMES_LOCALES = ("en","ja","ko","es","pt","id","de","fr","zh-CN")

@app.get("/games/shared/{filename}.js", include_in_schema=False)
async def serve_games_shared_js(filename: str):
    """10語言共用的遊戲邏輯JS。注意本路由要跟既有的 /games/{filename}.js 並存：
    兩者路徑深度不同（多一層 shared/），FastAPI 不會互相搶匹配。"""
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "games", "shared", f"{filename}.js")
    if _os.path.isfile(path):
        return FileResponse(path, media_type="application/javascript")
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/games/{locale}/{filename}.html", include_in_schema=False)
async def serve_games_locale_html(locale: str, filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    if locale not in _GAMES_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "games", locale, f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/games/{locale}", include_in_schema=False)
@app.get("/games/{locale}/", include_in_schema=False)
async def serve_games_locale_index(locale: str):
    from fastapi.responses import FileResponse, RedirectResponse
    import os as _os
    if locale not in _GAMES_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "games", locale, "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    # 該語言索引頁還沒建立時，退回繁中總覽而不是丟404（跟 /tools/{locale} 同樣的處理方式）
    return RedirectResponse(url="/games/", status_code=302)


# ---- Lottery 彩票路由 ----
_LOTTERY_LOCALES = ("en","ja","ko","fr","de","es","pt","id","zh-CN")

@app.get("/lottery/data/{filename}", include_in_schema=False)
async def serve_lottery_data(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    if not filename.endswith(".json"):
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "lottery", "data", filename)
    if _os.path.isfile(path):
        return FileResponse(path, media_type="application/json")
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/lottery/{filename}.html", include_in_schema=False)
async def serve_lottery_html(filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "lottery", f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/lottery", include_in_schema=False)
@app.get("/lottery/", include_in_schema=False)
async def serve_lottery_index():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "lottery", "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/lottery/{locale}/{filename}.html", include_in_schema=False)
async def serve_lottery_locale_html(locale: str, filename: str):
    from fastapi.responses import FileResponse
    import os as _os
    if locale not in _LOTTERY_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "lottery", locale, f"{filename}.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/lottery/{locale}", include_in_schema=False)
@app.get("/lottery/{locale}/", include_in_schema=False)
async def serve_lottery_locale_index(locale: str):
    from fastapi.responses import FileResponse, RedirectResponse
    import os as _os
    if locale not in _LOTTERY_LOCALES:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    path = _os.path.join(_FRONTEND_DIR, "lottery", locale, "index.html")
    if _os.path.isfile(path):
        return FileResponse(path)
    return RedirectResponse(url="/lottery/", status_code=302)

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
    return _serve_locale_file("comparisons", f"{filename}.html")

@app.get("/comparisons", include_in_schema=False)
@app.get("/comparisons/", include_in_schema=False)
async def serve_comparisons_index():
    return _serve_locale_file("comparisons", "index.html")

@app.get("/comparisons/{locale}/{filename}.html", include_in_schema=False)
async def serve_comparisons_locale_html(locale: str, filename: str):
    return _serve_locale_file("comparisons", f"{filename}.html", locale, _COMP_LOCALES)

@app.get("/comparisons/{locale}", include_in_schema=False)
@app.get("/comparisons/{locale}/", include_in_schema=False)
async def serve_comparisons_locale_index(locale: str):
    return _serve_locale_file("comparisons", "index.html", locale, _COMP_LOCALES)

# ---- Home（多語系首頁＋法律頁面）路由 ----
@app.get("/home/{locale}/{filename}.html", include_in_schema=False)
async def serve_home_locale_html(locale: str, filename: str):
    return _serve_locale_file("home", f"{filename}.html", locale, _COMP_LOCALES)

@app.get("/home/{locale}", include_in_schema=False)
@app.get("/home/{locale}/", include_in_schema=False)
async def serve_home_locale_index(locale: str):
    return _serve_locale_file("home", "homepage.html", locale, _COMP_LOCALES)

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
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
        ]
    })

@app.get("/favicon.ico", include_in_schema=False)
async def serve_favicon():
    from fastapi.responses import FileResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "favicon.ico")
    if _os.path.isfile(path):
        return FileResponse(path, media_type="image/x-icon")
    from fastapi.responses import JSONResponse
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/icon-192.png", include_in_schema=False)
async def serve_icon_192():
    from fastapi.responses import FileResponse, JSONResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "icon-192.png")
    if _os.path.isfile(path):
        return FileResponse(path, media_type="image/png")
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/icon-512.png", include_in_schema=False)
async def serve_icon_512():
    from fastapi.responses import FileResponse, JSONResponse
    import os as _os
    path = _os.path.join(_FRONTEND_DIR, "icon-512.png")
    if _os.path.isfile(path):
        return FileResponse(path, media_type="image/png")
    return JSONResponse({"detail": "Not Found"}, status_code=404)

@app.get("/robots.txt", include_in_schema=False)
async def serve_robots(request: Request):
    from fastapi.responses import PlainTextResponse
    host = request.headers.get("host", "")
    if "api.softglow-ai.com" in host:
        # api 子網域是後端API專用，不應被搜尋引擎索引
        return PlainTextResponse("User-agent: *\nDisallow: /")
    return PlainTextResponse("User-agent: *\nAllow: /\nDisallow: /*?q=\nDisallow: /ws/\n\nSitemap: https://softglow-ai.com/sitemap.xml")


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


def _dow_trend(highs, lows, order: int = 5):
    """
    道氏波峰波谷趨勢判斷（2026/08/06 導入，取代原 MA20/MA60 均線判斷）。

    以近期波峰(swing high)與波谷(swing low)的高低結構判斷趨勢：
      - 頭頭高 且 底底高 → 上升趨勢
      - 頭頭低 且 底底低 → 下降趨勢
      - 其餘（結構背離、方向不明）→ 盤整

    order=5 為回測（做多三批 + 空方 + 多天期，2021-2026 台股資料）驗證出的
    最佳敏感度：鑑別力明顯優於 MA20/MA60（+1.38% vs -0.05%），且跨股票、跨年份、
    跨多空皆穩定勝出。

    回傳 "上升趨勢" / "下降趨勢" / "盤整"；
    若資料不足以判斷（K棒太少或找不到足夠峰谷），回傳 None，由呼叫端 fallback 回舊邏輯。
    """
    try:
        h = np.asarray(highs, dtype=float)
        l = np.asarray(lows, dtype=float)
    except Exception:
        return None
    if len(h) < 60 or len(l) < 60:
        return None
    peaks = argrelextrema(h, np.greater_equal, order=order)[0]
    troughs = argrelextrema(l, np.less_equal, order=order)[0]
    if len(peaks) < 2 or len(troughs) < 2:
        return None
    higher_high = h[peaks[-1]] > h[peaks[-2]]
    higher_low = l[troughs[-1]] > l[troughs[-2]]
    lower_high = h[peaks[-1]] < h[peaks[-2]]
    lower_low = l[troughs[-1]] < l[troughs[-2]]
    if higher_high and higher_low:
        return "上升趨勢"
    if lower_high and lower_low:
        return "下降趨勢"
    return "盤整"


def _parse_tw_num(s):
    """解析TWSE/TPEX月報表數字欄位，'--'/空字串/'X' 一律當0。"""
    return float(str(s).replace(",", "")) if str(s).strip() not in ("--", "", "X") else 0.0


def _fetch_tw_month_report_row(url: str, data_key: str, roc_date: str, source_label: str, code: str):
    """
    2026/07/30：抽出的共用函式，取代 fetch_df_finmind() 裡原本上市(TWSE)/上櫃(TPEX)
    兩段幾乎一樣的月報表抓取+解析程式碼，只有URL/JSON資料key/log標籤不同。
    找到當日資料回傳 (open, high, low, close, volume)，找不到或抓取失敗回傳 None。

    2026/08/06 修復：原本依賴呼叫者 fetch_df_finmind() 內 import 的 _ur/_j，
    但本函式是獨立頂層函式，Python 作用域規則下看不到呼叫者的區域變數，
    導致每次執行都拋 NameError、被自己的 except 默默吃掉回傳 None——
    這個「收盤後補今日K棒」的最終備援其實從7/30重構後就從未真正成功執行過。
    現在自己 import，不再依賴呼叫者。
    """
    import urllib.request as _ur, json as _j
    try:
        req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with _ur.urlopen(req, timeout=8) as r:
            raw = _j.loads(r.read())
        for row in raw.get(data_key, []):
            if str(row[0]).strip() == roc_date:
                return (_parse_tw_num(row[3]), _parse_tw_num(row[4]),
                        _parse_tw_num(row[5]), _parse_tw_num(row[6]), _parse_tw_num(row[1]))
        return None
    except Exception as _e:
        print(f"   {source_label} 月報補棒失敗 {code}：{_e}")
        return None


def _expected_latest_trading_date(now_tw) -> str:
    """
    2026/08/14 新增：資料新鮮度檢查用。

    緣起：帥哥鴻回報「早上08:00看6770，個股現價/K棒還停在更早之前」，
    查Zeabur log證實main.py當下印出「[QUOTE] 1303 finmind 尚無今日資料，僅補 y_val」——
    FinMind自己的資料庫在那個時間點還沒把「上一個交易日」的資料更新進來，
    系統原本沒有任何機制偵測這種狀況，直接把舊資料當最新結果顯示，完全沒有提示。

    這裡刻意只抓最保守的下限：「不管現在幾點，資料來源現在至少應該要有『上一個交易日』
    的資料」，不去判斷「今天收盤後是否該有今天的資料」（那個時間點FinMind實際更新時間
    不確定，抓太緊容易在盤中/剛收盤時誤報)。只排除週末，不含國定假日——
    假日當天資料源沒有新資料是正常的，所以下游用這個值判斷「落後」時，
    訊息要同時涵蓋「資料源還沒更新」跟「剛好是休市日」兩種可能，不武斷宣稱一定是bug。
    """
    d = now_tw.date() - timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d.strftime("%Y-%m-%d")


# ── 日K原始資料：快取＋備援（2026/09/17新增）──
_DAILY_ROWS_CACHE: dict = {}          # {(code, start): (存入時間, rows, 來源)}
_DAILY_ROWS_TTL = 1800                # 30分鐘；盤中今日K棒另由即時報價補，不受這個快取影響
_FINMIND_FAIL_UNTIL = {"t": 0.0}      # FinMind 回報額度用完時，暫停打它5分鐘，避免越打越久


def _yahoo_daily_rows(code: str, start: str) -> list:
    """Yahoo 日K（FinMind 失敗時的備援），轉成跟 FinMind TaiwanStockPrice 一樣的欄位"""
    import urllib.request as _ur, json as _j
    from datetime import date as _d, datetime as _dt, timedelta as _td
    days = (_d.today() - _d.fromisoformat(start)).days
    rng = "10y" if days > 1830 else "5y" if days > 1100 else "3y" if days > 370 else "1y"
    suffixes = [".TWO", ".TW"] if _market_cache.get(code) == "otc" else [".TW", ".TWO"]
    for sfx in suffixes:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{code}{sfx}?range={rng}&interval=1d"
            req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with _ur.urlopen(req, timeout=12) as resp:
                j = _j.loads(resp.read())
            res = ((j.get("chart") or {}).get("result") or [None])[0]
            if not res or not res.get("timestamp"):
                continue
            q = res["indicators"]["quote"][0]
            rows = []
            for i, ts in enumerate(res["timestamp"]):
                o, h, l, c, v = (q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i])
                if None in (o, h, l, c):
                    continue
                ds = (_dt.utcfromtimestamp(ts) + _td(hours=8)).strftime("%Y-%m-%d")
                if ds < start:
                    continue
                rows.append({"date": ds, "open": round(o, 2), "max": round(h, 2), "min": round(l, 2),
                             "close": round(c, 2), "Trading_Volume": int(v or 0)})
            if rows:
                return rows
        except Exception as e:
            print(f"   Yahoo 日K備援失敗 {code}{sfx}：{e}")
    return []


def _daily_price_rows(code: str, start: str, end: str) -> list:
    """回傳 FinMind TaiwanStockPrice 格式的日K rows；失敗回 []"""
    import urllib.request as _ur, urllib.error as _ue, json as _j
    key = (code, start)
    now = _time_mod.time()
    hit = _DAILY_ROWS_CACHE.get(key)
    if hit and now - hit[0] < _DAILY_ROWS_TTL:
        return hit[1]
    err = None
    if now >= _FINMIND_FAIL_UNTIL["t"]:
        try:
            url = (f"https://api.finmindtrade.com/api/v4/data"
                   f"?dataset=TaiwanStockPrice&data_id={code}"
                   f"&start_date={start}&end_date={end}&token={FINMIND_TOKEN}")
            req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with _ur.urlopen(req, timeout=15) as resp:
                raw = _j.loads(resp.read())
            if raw.get("status") == 200 and raw.get("data"):
                rows = raw["data"]
                _DAILY_ROWS_CACHE[key] = (now, rows, "finmind")
                if len(_DAILY_ROWS_CACHE) > 600:
                    for k in sorted(_DAILY_ROWS_CACHE, key=lambda k: _DAILY_ROWS_CACHE[k][0])[:200]:
                        _DAILY_ROWS_CACHE.pop(k, None)
                return rows
            err = f"status={raw.get('status')} msg={raw.get('msg')}"
        except _ue.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", "ignore")[:200]
            except Exception:
                pass
            err = f"HTTP {e.code} {body}"
            if e.code in (402, 429):
                _FINMIND_FAIL_UNTIL["t"] = now + 300
        except Exception as e:
            err = str(e)
        print(f"   ⚠️ FinMind 日K抓取失敗 {code}：{err}")
    else:
        err = "FinMind 額度暫停中"
    if hit:
        print(f"   ↩️ {code} 改用 {int((now - hit[0]) / 60)} 分鐘前的日K快取")
        return hit[1]
    rows = _yahoo_daily_rows(code, start)
    if rows:
        print(f"   ↩️ {code} FinMind失敗（{err}），改用 Yahoo 日K備援（{len(rows)} 筆）")
        _DAILY_ROWS_CACHE[key] = (now - _DAILY_ROWS_TTL + 300, rows, "yahoo")   # 備援資料只快取5分鐘
        return rows
    return []


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
    # 2026/09/17修正：伺服器時區是 UTC，原本 date.today() 在台灣 00:00～08:00 會是「前一天」，
    # 下面「盤前刪掉今日那筆」就會誤刪最近一個交易日的真實收盤 K 棒。一律用台北日期。
    _tw_today_d = datetime.now(ZoneInfo("Asia/Taipei")).date()
    start     = (_tw_today_d - timedelta(days=days)).strftime("%Y-%m-%d")
    today_str = _tw_today_d.strftime("%Y-%m-%d")

    try:
        # 2026/09/17修正：原本這裡直接打FinMind、失敗就回空表 → 個股分析顯示404「找不到股票」。
        # FinMind額度用完（HTTP 402）或暫時故障時，整站個股分析、K線都會一起掛。
        # 改成 _daily_price_rows()：同一檔30分鐘內共用快取（分析＋K線原本每查一次打兩次FinMind），
        # FinMind失敗時先用舊快取，再退回Yahoo日K，並把失敗原因印在log。
        rows = _daily_price_rows(code, start, today_str)
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows)
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
        _is_pre_market = now_tw.time() < _dtime(9, 0)
        if _is_pre_market:
            df = df[df.index != today_ts]

        if in_or_just_after:
            try:
                # 2026/09/14修正（二）：原本這裡「只」直接打FinMind tick_snapshot，完全沒有
                # 備援——一旦FinMind這支API本身出問題（額度用完/被限流/回傳400等），今日K棒
                # 就完全補不進去，即使上面的時機判斷已經修好也沒用，因為根本拿不到原始資料。
                # 這正是2026/09/14發現「/api/kline能正確顯示今天K棒、但分析基準價卻卡在
                # 上一交易日」的深層原因：/api/kline補今日K棒用的是_get_live_quote_data()，
                # 這個共用函式會先試TWSE官方即時揭示（twse_mid），只有TWSE MIS失敗（例如冷門股
                # 沒有買賣報價）才會退回FinMind tick_snapshot當備援，對熱門股幾乎不會用到FinMind
                # 這條路，穩定得多；而這裡（分析基準價）原本卻是唯一、沒有備援地直接依賴FinMind，
                # FinMind一出狀況全部股票都會中招。現在改成呼叫同一個共用函式，跟kline統一資料源，
                # 不再自己重複維護一套更脆弱的邏輯，之後同一種bug只需要修一處。
                _qd = _get_live_quote_data(code)
                if _qd and _qd.get("price"):
                    cp  = float(_qd.get("price") or 0)
                    op  = float(_qd.get("open") or cp)
                    hi  = float(_qd.get("high") or cp)
                    lo  = float(_qd.get("low") or cp)
                    vol = float(_qd.get("volume") or 0)
                    if not (is_weekday and _dtime(9, 0) <= now_tw.time() <= _dtime(13, 30)):
                        cp = 0
                    if cp > 0:
                        today_bar = pd.DataFrame(
                            [[op, hi, lo, cp, vol]],
                            index=[today_ts],
                            columns=["Open", "High", "Low", "Close", "Volume"]
                        )
                        df = df[df.index != today_ts]
                        df = pd.concat([df, today_bar])
                        print(f"   即時報價補今日 K 棒：{code} close={cp}")
            except Exception as _e:
                print(f"   即時報價補棒失敗 {code}：{_e}")

        # ── TWSE/TPEX 月報補今日 K 棒（上述來源均無資料時的最終 fallback）──
        # 2026/07/30：上市/上櫃兩段原本各自複製貼上一份幾乎一樣的抓取/解析邏輯，
        # 只有URL、JSON資料key、log標籤不同，改用共用函式 _fetch_tw_month_report_row()，
        # 抓取/解析行為完全不變，只是不用維護兩份。
        if today_ts not in df.index:
            today_obj = _tw_today_d
            roc_year  = today_obj.year - 1911
            roc_date  = f"{roc_year}/{today_obj.month:02d}/{today_obj.day:02d}"
            yyyymmdd  = today_obj.strftime("%Y%m%d")
            mm        = today_obj.strftime("%m")

            filled = False
            _is_otc = _market_cache.get(code, "") in ("otc", "rotc")
            if not _is_otc:
                _mr_url = (f"https://www.twse.com.tw/exchangeReport/STOCK_DAY"
                           f"?response=json&date={yyyymmdd}&stockNo={code}")
                _mr_row = _fetch_tw_month_report_row(_mr_url, "data", roc_date, "TWSE", code)
            else:
                _tpex_d = f"{roc_year}/{mm}"
                _mr_url = (f"https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info"
                           f"/st43_result.php?l=zh-tw&d={_tpex_d}&stkno={code}")
                _mr_row = _fetch_tw_month_report_row(_mr_url, "aaData", roc_date, "TPEX", code)

            if _mr_row:
                # 2026/08/06 修復：原本這裡複製了即時快照那段的 in_session 檢查，
                # 邏輯反了——TWSE/TPEX 月報表本來就是「收盤結算後」才會有當日資料，
                # 只要 _mr_row 有回傳就代表官方資料已存在，不該用「是否盤中」去擋，
                # 這正是「13:31後仍卡在前一天收盤價」的根因之一（另一根因見上方NameError修復）。
                op, hi, lo, cp, vol = _mr_row
                if cp > 0:
                    today_bar = pd.DataFrame(
                        [[op, hi, lo, cp, vol]],
                        index=[today_ts],
                        columns=["Open", "High", "Low", "Close", "Volume"]
                    )
                    df = pd.concat([df, today_bar])
                    print(f"   {'TWSE' if not _is_otc else 'TPEX'} 月報補今日 K 棒：{code} close={cp}")
                    filled = True

        # ── 收盤後最終備援（2026/09/17新增）──
        # 帥哥鴻回報（6173信昌電）：收盤後到官方日報／FinMind更新前這段空窗，分析基準仍停在前一天
        # （例：昨收315算出防守位305.55，今天收303.5已跌破，畫面卻還顯示「報酬大於風險」）。
        # 13:30後證交所即時揭示的成交價就是今天的收盤價，且回傳資料日期，確認是今天才補。
        if today_ts not in df.index and is_weekday and now_tw.time() >= _dtime(13, 31):
            try:
                _mq = _mis_batch_quotes([code]).get(code) or {}
                if _mq.get("date") == today_str and _mq.get("price") and _mq.get("close_final"):
                    cp = float(_mq["price"])
                    op = float(_mq.get("open") or cp)
                    hi = max(float(_mq.get("high") or cp), cp)
                    lo = min(float(_mq.get("low") or cp), cp)
                    vol = float(_mq.get("volume") or 0)
                    df = pd.concat([df, pd.DataFrame([[op, hi, lo, cp, vol]], index=[today_ts],
                                                     columns=["Open", "High", "Low", "Close", "Volume"])])
                    print(f"   證交所即時揭示補今日收盤 K 棒：{code} close={cp}")
            except Exception as _mq_e:
                print(f"   即時揭示補收盤K棒失敗 {code}：{_mq_e}")

        # ── 資料新鮮度檢查（2026/08/14 新增）──
        # 上面幾段補棒都失敗時，df 最新一筆可能還停在「上一個交易日更早之前」，
        # 之前完全沒有偵測機制，會悄悄把舊資料當最新結果分析。
        # 這裡只做「有沒有明顯落後」的判斷，記在 df.attrs 供 _do_analyze() 讀取後
        # 加註提示，不在這裡直接印警告或改資料本身。
        try:
            if not df.empty:
                _expected_date = _expected_latest_trading_date(now_tw)
                _actual_date = df.index.max().strftime("%Y-%m-%d")
                df.attrs["data_stale"] = _actual_date < _expected_date
                df.attrs["data_stale_latest"] = _actual_date
                df.attrs["data_stale_expected"] = _expected_date
        except Exception as _stale_e:
            print(f"   資料新鮮度檢查失敗（不影響原本分析）{code}：{_stale_e}")

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

for _c_sn, _n_sn in STOCK_NAMES.items():
    _name_to_code.setdefault(_n_sn, _c_sn)


def get_stock_name(symbol: str) -> str:
    """取得台股中文名稱：靜態表 → 快取 → FinMind → 回傳代號"""
    code = symbol.replace(".TWO", "").replace(".TW", "").strip()

    # 1. 靜態對照表（最快）
    if code in STOCK_NAMES:
        return STOCK_NAMES[code]

    # 2. 快取（啟動時已預載全台股，通常直接命中）
    if code in _name_cache:
        return _name_cache[code]

    # 3. 快取沒命中 → 先回傳代號，背景補抓整份清單（有節流，不會每次都打）
    #    2026/09/17：啟動時 FinMind 額度用完，整份股名快取是空的，股名全部消失，
    #    原本註解寫「查詢時重試」但其實沒有重試，這裡補上。
    if code.isdigit():
        _trigger_name_cache_reload()
    return code


# ── 股名快取載入（2026/09/17新增）──
# 來源順序：FinMind TaiwanStockInfo → 資料庫備份（上次成功的清單）→ 證交所／櫃買官方清單
from contextlib import contextmanager as _contextmanager_nm
_NAME_CACHE_MIN = 1500                     # 全台股約 2000+ 檔，少於這個數字視為沒載入完整
_NAME_RELOAD_STATE = {"last": 0.0, "running": False}
_NAME_RELOAD_GAP = 300                     # 背景重抓至少間隔 5 分鐘


@_contextmanager_nm
def _name_cache_db():
    """用法：with _name_cache_db() as conn（自動 commit + close）"""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("""CREATE TABLE IF NOT EXISTS stock_name_backup (
        stock_id TEXT PRIMARY KEY, stock_name TEXT NOT NULL, market TEXT DEFAULT '',
        updated_at TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS stock_info_backup (
        id INTEGER PRIMARY KEY, data TEXT NOT NULL, updated_at TEXT)""")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _put_names(pairs, overwrite: bool = False) -> int:
    """pairs: [(代號, 名稱, 市場別)]；回傳新增筆數"""
    n = 0
    for sid, sname, mkt in pairs:
        sid = str(sid or "").strip()
        sname = str(sname or "").strip()
        if not sid or not sname:
            continue
        if overwrite or sid not in _name_cache:
            if sid not in _name_cache:
                n += 1
            _name_cache[sid] = sname
        _name_to_code.setdefault(sname, sid)
        if mkt and (overwrite or sid not in _market_cache):
            _market_cache[sid] = mkt
    return n


def _names_from_finmind() -> list:
    """回傳 FinMind TaiwanStockInfo 原始清單；失敗回 []"""
    import urllib.request as _ur, urllib.error as _ue, json as _j
    if _time_mod.time() < _FINMIND_FAIL_UNTIL["t"]:
        print("   股名：FinMind 額度暫停中，略過")
        return []
    try:
        url = (f"https://api.finmindtrade.com/api/v4/data"
               f"?dataset=TaiwanStockInfo&token={FINMIND_TOKEN}")
        req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with _ur.urlopen(req, timeout=15) as resp:
            data = _j.loads(resp.read())
        if data.get("status") == 200 and data.get("data"):
            return data["data"]
        print(f"   ⚠️ 股名：FinMind 回應異常 status={data.get('status')} msg={data.get('msg','')}")
    except _ue.HTTPError as e:
        if e.code in (402, 429):
            _FINMIND_FAIL_UNTIL["t"] = _time_mod.time() + 300
        print(f"   ⚠️ 股名：FinMind HTTP {e.code}")
    except Exception as e:
        print(f"   ⚠️ 股名：FinMind 失敗 {e}")
    return []


def _names_from_official() -> list:
    """證交所（上市）＋櫃買（上櫃）官方清單 → [(代號, 名稱, 市場別)]"""
    import urllib.request as _ur, csv as _csv, io as _io, json as _j
    out = []
    try:
        req = _ur.Request("https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY_ALL", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://www.twse.com.tw/",
        })
        with _ur.urlopen(req, timeout=15, context=_TWSE_SSL_CTX) as r:
            raw = r.read().decode("utf-8-sig", errors="replace")
        cnt = 0
        for row in _csv.reader(_io.StringIO(raw)):
            if len(row) < 3:
                continue
            cells = [str(x).strip().strip('="').strip() for x in row[:3]]
            # 欄位順序：日期,代號,名稱,...（既有程式註解）；若官方改成 代號,名稱,... 也能判斷
            for ci in (1, 0):
                code, name = cells[ci], cells[ci + 1]
                if (code.isalnum() and 4 <= len(code) <= 6 and code[:4].isdigit()
                        and name and not name.replace(",", "").replace(".", "").isdigit()):
                    out.append((code, name, "twse"))
                    cnt += 1
                    break
        print(f"   股名：證交所清單 {cnt} 筆")
    except Exception as e:
        print(f"   ⚠️ 股名：證交所清單失敗 {e}")
    try:
        req = _ur.Request("https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes",
                          headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with _ur.urlopen(req, timeout=15, context=_TWSE_SSL_CTX) as r:
            arr = _j.loads(r.read().decode("utf-8-sig", errors="replace"))
        cnt = 0
        for it in arr or []:
            code = str(it.get("SecuritiesCompanyCode", "")).strip()
            name = str(it.get("CompanyName", "")).strip()
            if code and name:
                out.append((code, name, "otc"))
                cnt += 1
        print(f"   股名：櫃買清單 {cnt} 筆")
    except Exception as e:
        print(f"   ⚠️ 股名：櫃買清單失敗 {e}")
    return out


def _load_stock_name_cache(reason: str = "", allow_official: bool = True) -> int:
    """載入股名快取，回傳目前快取筆數"""
    global _stock_info_cache, _stock_info_ts
    if _NAME_RELOAD_STATE["running"]:
        return len(_name_cache)
    _NAME_RELOAD_STATE["running"] = True
    _NAME_RELOAD_STATE["last"] = _time_mod.time()
    try:
        now_s = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")
        # ① FinMind
        info = _names_from_finmind()
        if info:
            added = _put_names([(i.get("stock_id"), i.get("stock_name"), str(i.get("type", "")).lower())
                                for i in info])
            _stock_info_cache = info
            _stock_info_ts = _time_mod.time()
            print(f"   ✅ 股名快取（{reason}）FinMind 載入完成，新增 {added} 筆，共 {len(_name_cache)} 筆")
            try:
                with _name_cache_db() as conn:
                    seen = set()
                    rows = []
                    for i in info:
                        sid = str(i.get("stock_id", "")).strip()
                        nm = str(i.get("stock_name", "")).strip()
                        if sid and nm and sid not in seen:
                            seen.add(sid)
                            rows.append((sid, nm, str(i.get("type", "")).lower(), now_s))
                    conn.executemany("INSERT OR REPLACE INTO stock_name_backup VALUES (?,?,?,?)", rows)
                    conn.execute("INSERT OR REPLACE INTO stock_info_backup (id, data, updated_at) VALUES (1,?,?)",
                                 (_json_mod.dumps(info, ensure_ascii=False), now_s))
            except Exception as e:
                print(f"   ⚠️ 股名備份寫入失敗 {e}")
            return len(_name_cache)
        # ② 資料庫備份
        try:
            with _name_cache_db() as conn:
                rows = conn.execute("SELECT stock_id, stock_name, market FROM stock_name_backup").fetchall()
            if rows:
                added = _put_names(rows)
                print(f"   ✅ 股名快取（{reason}）改用資料庫備份，新增 {added} 筆，共 {len(_name_cache)} 筆")
        except Exception as e:
            print(f"   ⚠️ 股名備份讀取失敗 {e}")
        # ③ 官方清單（備份也不夠時才抓）
        if allow_official and len(_name_cache) < _NAME_CACHE_MIN:
            off = _names_from_official()
            if off:
                added = _put_names(off)
                print(f"   ✅ 股名快取（{reason}）改用官方清單，新增 {added} 筆，共 {len(_name_cache)} 筆")
                try:
                    with _name_cache_db() as conn:
                        conn.executemany(
                            "INSERT OR IGNORE INTO stock_name_backup VALUES (?,?,?,?)",
                            [(c, n, m, now_s) for c, n, m in off])
                except Exception as e:
                    print(f"   ⚠️ 股名備份寫入失敗 {e}")
        if len(_name_cache) < _NAME_CACHE_MIN:
            print(f"   ⚠️ 股名快取（{reason}）仍不完整（{len(_name_cache)} 筆），10分鐘後自動重試")
        return len(_name_cache)
    finally:
        _NAME_RELOAD_STATE["running"] = False


def _ensure_stock_name_cache():
    """排程用：快取不完整，或還沒拿到 FinMind 完整資料（產業別等）時重抓"""
    if len(_name_cache) < _NAME_CACHE_MIN or not _stock_info_cache:
        _load_stock_name_cache("排程重試")


def _trigger_name_cache_reload():
    """查不到股名時，背景補抓（至少間隔5分鐘）"""
    if len(_name_cache) >= _NAME_CACHE_MIN:
        return
    if _NAME_RELOAD_STATE["running"] or _time_mod.time() - _NAME_RELOAD_STATE["last"] < _NAME_RELOAD_GAP:
        return
    import threading as _th
    _NAME_RELOAD_STATE["last"] = _time_mod.time()
    _th.Thread(target=_load_stock_name_cache, args=("查詢時補抓",), daemon=True).start()


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
def calc_risk_level(price, support, resistance, rr_ratio, near_top, near_bot, pattern, vol_ratio=None):
    """回傳風險等級與條列摘要（含量能判斷）"""
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
        risk_label = "方向未明"
        risk_color = "gray"

    # 量能修正：縮量（量比 < 0.6）時，低風險升為留意、留意升為高風險
    if vol_ratio is not None:
        try:
            vr = float(vol_ratio)
            if vr < 0.6:
                if risk_level == "low":
                    risk_level = "medium"
                    risk_label = "留意（縮量）"
                    risk_color = "amber"
                elif risk_level == "watch":
                    risk_level = "medium"
                    risk_label = "留意（縮量）"
                    risk_color = "amber"
        except (ValueError, TypeError):
            pass

    return risk_level, risk_label, risk_color


def build_summary(price, support, support_desc, resistance, resistance_desc,
                  trend, pattern, rr_ratio, risk_level, risk_label,
                  near_top, near_bot, stop_loss, target1, rr_basis="失效位置",
                  kline_pattern="常態 K 線（無觸發極端型態）", win_rate=0.50):
    """條列式分析摘要"""
    sup_dist = (price - support) / price * 100
    res_dist = (resistance - price) / price * 100
    stop_dist = (price - stop_loss) / price * 100

    lines = []

    # 趨勢（加細節）
    # 2026/08/06 修正：trend 已改用道氏波峰波谷判斷（非均線），
    # 原文案「均線多頭/空頭排列」與實際判斷方式不符，改中性用詞
    # （呼應同日 _do_analyze 內 conflict_note 的同一次修正）
    trend_map = {
        "上升趨勢": "近期高低點結構走高，屬多方結構，回測支撐時是觀察多方是否延續的位置",
        "下降趨勢": "近期高低點結構走低，屬空方結構，反彈至壓力時是觀察空方是否延續的位置",
        "盤整":     "高低點結構不明，多空拉鋸，方向需等突破或跌破確認",
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
        "突破型態": f"股價突破壓力 {resistance}；若縮量拉回不破，壓力轉為支撐，突破結構維持",
        "跌破型態": f"股價跌破支撐 {support}，前支撐轉為壓力，原多方結構失效",
        "支撐整理": f"現價靠近支撐 {support}（-{sup_dist:.1f}%），支撐守住則結構偏多，跌破則支撐型態失效",
        "壓力整理": f"現價靠近壓力 {resistance}（+{res_dist:.1f}%），上方空間有限；是否放量突破是觀察重點，支撐參考 {support}",
        "整理中":   f"現價位於支撐 {support} 與壓力 {resistance} 之間，方向訊號尚未出現",
    }
    lines.append(f"型態：{pattern_detail.get(pattern, pattern)}")

    # 風險（防守位）
    lines.append(f"失效位置 {stop_loss}（跌破代表目前型態失效，距現價 -{stop_dist:.1f}%）")

    # 損益比（說明計算基礎）
    if rr_ratio >= 2:
        rr_comment = "損益比高於 2"
    elif rr_ratio >= 1.5:
        rr_comment = "損益比尚可"
    elif rr_ratio >= 1:
        rr_comment = "損益比偏低"
    else:
        rr_comment = "損益比不佳，風險大於報酬"
    lines.append(f"風險報酬 {rr_ratio}（以{rr_basis}計算，{rr_comment}）")

    lines.append(f"最新 K 線型態：{kline_pattern}")
    lines.append(f"型態經驗參考值：{win_rate*100:.0f}%（一般型態經驗值，非本股統計）")
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

    if   price > resist_now * (1+thr):  pos,pdesc="breakout_up",  f"已突破上軌 {resist_now}，等幅推算價位 {round(resist_now+channel_width,2)}"
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
        pdesc = f"收斂三角整理，上破 {resist_now:.1f} 推算價位 {target_up}，下破 {support_now:.1f} 推算價位 {target_dn}"
    elif expanding:
        ctype, cdesc = "expanding", "擴散三角形（波動加大）"
        pdesc = f"擴散三角，上緣 {resist_now:.1f} / 下緣 {support_now:.1f}，波動加大、方向不易判斷"
    elif asc_tri:
        ctype, cdesc = "ascending_tri", "上升三角形（偏多）"
        target = round(resist_now + channel_width, 2)
        pdesc = f"上升三角，壓力 {resist_now:.1f} 反覆測試，突破後推算價位 {target}"
    elif desc_tri:
        ctype, cdesc = "descending_tri", "下降三角形（偏空）"
        target = round(support_now - channel_width, 2)
        pdesc = f"下降三角，支撐 {support_now:.1f} 反覆測試，跌破後推算價位 {target}"
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
                    "position_desc": f"{'已突破頸線' if broken else '接近頸線'} {neck:.1f}，推算價位 {target}{_vol_note}",
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
                    "position_desc": f"{'已跌破頸線' if broken else '接近頸線'} {neck:.1f}，下行推算價位 {target}",
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
                    "position_desc": f"頭肩頂，{'已跌破頸線' if broken else '頸線'} {neck:.1f}，下行推算價位 {target}",
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
                    "position_desc": f"頭肩底，{'已突破頸線' if broken else '頸線'} {neck:.1f}，上行推算價位 {target}",
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


def detect_gann_sell(closes, highs, lows, volumes, ma_period=20, max_bars=2):
    """
    葛蘭碧八大法則賣點偵測（賣5/6/7/8合併版）
    與 detect_gann_recross（買1~4）對稱，負責「該減碼/出場」的空方訊號。
    時效限制：訊號觸發根起 ≤ max_bars 根內有效（預設2根）

    賣5：收盤從均線上方跌破到下方，且均線走平/下彎（跌破均線，多方防線失守），觸發根起 ≤2根
    賣6：收盤在均線下方，高點曾反彈觸碰均線 ±1% 後再度下跌（反彈無力），觸發根起 ≤2根
    賣7：收盤連續在均線下方，最近一次反彈接近均線後受阻下跌（弱勢整理），觸發根起 ≤2根
    賣8：收盤正乖離均線過大（短線急漲、漲太多太快），獲利了結訊號（不需在均線下方）

    回傳：(訊號是否成立, 均線值, 均線名稱, 賣點類型描述, 是否為乖離型賣8)
    """
    n = len(closes)
    if n < ma_period + 5:
        return False, None, None, None, False

    ma = np.full(n, np.nan)
    for i in range(ma_period - 1, n):
        ma[i] = closes[i - ma_period + 1: i + 1].mean()

    curr_ma = ma[-1]
    if np.isnan(curr_ma):
        return False, None, None, None, False

    name = f"MA{ma_period}"

    TOUCH_BAND = 0.01     # 賣6/7：高點距均線 ±1% 算觸碰
    DEVIATE_BAND = 0.15   # 賣8：正乖離 ≥15% 視為過大（短線急漲）

    # ── 賣8：正乖離過大（優先判斷，因為它在均線上方也成立）──
    # 現價相對均線的乖離率；只在「明顯高於均線」時才觸發獲利了結提示
    deviation = (closes[-1] - curr_ma) / curr_ma if curr_ma > 0 else 0
    if deviation >= DEVIATE_BAND:
        return True, round(float(curr_ma), 2), name, f"賣8（正乖離{round(deviation*100,1)}%過大，短線過熱）", True

    # 均線方向：水平或向下才算弱勢（上升趨勢中的拉回不算賣訊）
    ma_slope_down = ma[-1] <= ma[-(min(5, n))]

    # ── 賣5：找最近一次「從上方跌破到下方」的觸發根 ──
    trigger_s5 = None
    for i in range(n - 1, ma_period, -1):
        if np.isnan(ma[i]) or np.isnan(ma[i - 1]):
            continue
        if closes[i - 1] > ma[i - 1] and closes[i] < ma[i]:
            trigger_s5 = i
            break
    if trigger_s5 is not None and (n - 1 - trigger_s5) <= max_bars and ma_slope_down:
        # 跌破當天量能：帶量下跌更需警惕
        _avg_vol_20 = float(np.mean(volumes[max(0,trigger_s5-20):trigger_s5])) if trigger_s5 > 0 else 1
        _trigger_vol = float(volumes[trigger_s5])
        _vol_big = _trigger_vol > _avg_vol_20 * 1.2  # 帶量跌破
        sell_type = "賣5（跌破均線，多方防線失守）"
        if _vol_big:
            sell_type += "⚠帶量下跌，賣壓沉重"
        return True, round(float(curr_ma), 2), name, sell_type, False

    # ── 賣6：收盤在均線下方，高點反彈觸碰均線後再下跌 ──
    trigger_s6 = None
    for i in range(n - 1, ma_period, -1):
        if np.isnan(ma[i]):
            continue
        if closes[i] < ma[i] and highs[i] >= ma[i] * (1 - TOUCH_BAND):
            # 確認前一根也在均線下方（不是剛跌破，那是賣5）
            if not np.isnan(ma[i - 1]) and closes[i - 1] < ma[i - 1]:
                trigger_s6 = i
                break
    if trigger_s6 is not None and (n - 1 - trigger_s6) <= max_bars:
        return True, round(float(curr_ma), 2), name, "賣6（反彈遇均線受阻，反彈無力）", False

    # ── 賣7：連續在均線下方，最近高點接近均線後受阻下跌 ──
    if n >= ma_period + 5:
        recent_5_below = all(
            not np.isnan(ma[-(j + 1)]) and closes[-(j + 1)] < ma[-(j + 1)]
            for j in range(5)
        )
        had_touch = any(
            not np.isnan(ma[-(j + 1)]) and highs[-(j + 1)] >= ma[-(j + 1)] * (1 - TOUCH_BAND)
            for j in range(1, 6)
        )
        price_falling = closes[-1] < closes[-2]
        if recent_5_below and had_touch and price_falling:
            trigger_s7 = None
            for j in range(1, 6):
                i = n - 1 - j
                if not np.isnan(ma[i]) and highs[i] >= ma[i] * (1 - TOUCH_BAND):
                    trigger_s7 = i
                    break
            if trigger_s7 is not None and (n - 1 - trigger_s7) <= max_bars:
                return True, round(float(curr_ma), 2), name, "賣7（均線下方弱勢，反彈受阻）", False

    return False, None, None, None, False


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

def _analysis_basis_behind(data: dict) -> bool:
    """收盤後（或隔天開盤前）分析基準日還沒跟上最近交易日 → True（快取只留10分鐘，等資料更新後重算）"""
    try:
        from zoneinfo import ZoneInfo
        now = datetime.now(ZoneInfo("Asia/Taipei"))
        basis = str((data or {}).get("price_basis_date") or "")
        if not basis:
            return False
        if now.weekday() < 5 and (now.hour, now.minute) >= (13, 30):
            expected = now.strftime("%Y-%m-%d")
        else:
            expected = _expected_latest_trading_date(now)
        return basis < expected
    except Exception:
        return False

def _cache_get(key: str):
    entry = _analyze_cache.get(key)
    # 2026/09/17修正：原本用「讀取當下」的時效判斷，盤中算好的結果（本來15分鐘）一到收盤後
    # 就變成「留到隔天09:00」，分析基準卡在盤中數字／前一天。改成建立時就決定到期時間。
    if entry and _time.time() < entry.get("exp", entry["ts"] + 900):
        return entry["data"]
    return None

def _cache_set(key: str, data: dict):
    ttl = _get_analyze_cache_ttl()
    if _analysis_basis_behind(data):
        ttl = min(ttl, 600)
    # 2026/09/17：法人資料當下沒抓到（FinMind 忙碌／額度），不要把「資料更新中」留到隔天，10分鐘後重抓
    if isinstance(data, dict) and "institutional" in data and not data.get("institutional"):
        ttl = min(ttl, 600)
    now_ts = _time.time()
    _analyze_cache[key] = {"ts": now_ts, "exp": now_ts + ttl, "data": data}
    if len(_analyze_cache) > 200:
        expired = [k for k, v in _analyze_cache.items() if v.get("exp", 0) < now_ts]
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
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id         TEXT NOT NULL,
            report_date      TEXT NOT NULL,
            stock_name       TEXT NOT NULL DEFAULT '',
            report_html      TEXT NOT NULL,
            price_basis_date TEXT DEFAULT NULL,
            created_at       TEXT DEFAULT (datetime('now','+8 hours')),
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
        -- 自選股（2026/09/13新增：修正自選股原本只存localStorage、從未跟帳號綁定的問題，
        -- 換裝置/瀏覽器登入同一帳號自選股會整組消失。以下改存DB，跟portfolios同一套風格）
        CREATE TABLE IF NOT EXISTS watchlist_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email  TEXT NOT NULL,
            stock_id    TEXT NOT NULL,
            stock_name  TEXT DEFAULT '',
            group_name  TEXT NOT NULL DEFAULT '預設',
            added_date  TEXT DEFAULT '',
            created_at  TEXT DEFAULT (datetime('now','+8 hours')),
            UNIQUE(user_email, stock_id)
        );
        CREATE TABLE IF NOT EXISTS watchlist_groups (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email  TEXT NOT NULL,
            group_name  TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now','+8 hours')),
            UNIQUE(user_email, group_name)
        );
        CREATE INDEX IF NOT EXISTS idx_watchlist_items_user ON watchlist_items(user_email);
        CREATE INDEX IF NOT EXISTS idx_watchlist_groups_user ON watchlist_groups(user_email);
        CREATE TABLE IF NOT EXISTS html_pages (
            key         TEXT PRIMARY KEY,
            content     TEXT NOT NULL,
            updated_at  TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS app_settings (
            key         TEXT PRIMARY KEY,
            value       TEXT NOT NULL,
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
        CREATE TABLE IF NOT EXISTS deep_pick_log (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id         TEXT NOT NULL,
            stock_name       TEXT NOT NULL DEFAULT '',
            cross_date       TEXT NOT NULL,
            pick_date        TEXT NOT NULL,
            pick_price       REAL NOT NULL,
            score            INTEGER DEFAULT 0,
            confidence       TEXT DEFAULT '',
            return_20d_pct   REAL DEFAULT NULL,
            return_20d_date  TEXT DEFAULT NULL,
            return_20d_price REAL DEFAULT NULL,
            created_at       TEXT DEFAULT (datetime('now','+8 hours')),
            UNIQUE(stock_id, cross_date)
        );
        -- 2026/09/15新增（文件B十六節「12金叉選股法」）：多方法選股結果，
        -- 每天每檔股票每個方法一筆，跟deep_pick_log完全獨立、互不覆蓋。
        CREATE TABLE IF NOT EXISTS multi_signal_results (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_date   TEXT NOT NULL,
            stock_id    TEXT NOT NULL,
            stock_name  TEXT NOT NULL DEFAULT '',
            method      TEXT NOT NULL,
            category    TEXT NOT NULL DEFAULT '',
            passed      INTEGER NOT NULL DEFAULT 0,
            value       REAL DEFAULT NULL,
            extra_json  TEXT DEFAULT '{}',
            created_at  TEXT DEFAULT (datetime('now','+8 hours')),
            UNIQUE(scan_date, stock_id, method)
        );
        CREATE INDEX IF NOT EXISTS idx_msr_date_method ON multi_signal_results(scan_date, method, passed);
        -- 12金叉整批共用資料快取（全市場法人買賣超），個股解析即時查詢時直接讀，不必再上網抓
        CREATE TABLE IF NOT EXISTS multi_signal_ctx (
            key        TEXT PRIMARY KEY,
            data_date  TEXT,
            content    TEXT,
            updated_at TEXT DEFAULT (datetime('now','+8 hours'))
        );
        -- 12金叉選股「營收轉成長」用的月營收快取（公開資訊觀測站彙總表，每月份抓過就不再重抓）
        CREATE TABLE IF NOT EXISTS multi_signal_revenue (
            stock_id TEXT NOT NULL,
            ym       TEXT NOT NULL,
            revenue  REAL, mom REAL, yoy REAL, cum_yoy REAL,
            PRIMARY KEY (stock_id, ym)
        );
        CREATE TABLE IF NOT EXISTS multi_signal_revenue_fetch (
            ym           TEXT PRIMARY KEY,
            fetched_date TEXT NOT NULL,
            count        INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS line_push_groups (
            group_id   TEXT PRIMARY KEY,
            first_seen TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE TABLE IF NOT EXISTS game_scores (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id   INTEGER NOT NULL,
            game_slug   TEXT NOT NULL,
            score       INTEGER NOT NULL,
            created_at  TEXT DEFAULT (datetime('now','+8 hours'))
        );
        CREATE INDEX IF NOT EXISTS idx_game_scores_slug ON game_scores(game_slug);
        CREATE INDEX IF NOT EXISTS idx_game_scores_member ON game_scores(member_id, game_slug);
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
        ("stock_reports",   "price_basis_date", "TEXT DEFAULT NULL"),
        ("members",         "line_user_id",    "TEXT DEFAULT NULL"),
        # 2026/09/15新增（文件A決策③，帥哥鴻拍板）：持股健檢改用自選股資料，不再是獨立的
        # portfolios表——自選股新增「股數」「買入價」兩個選填欄位，有填的股票才會被
        # /portfolio/analysis納入計算，沒填的維持單純自選觀察。
        ("watchlist_items", "shares",          "REAL DEFAULT NULL"),
        ("watchlist_items", "cost_price",      "REAL DEFAULT NULL"),
    ]
    for table, col, coldef in new_columns:
        try:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {coldef}")
            conn.commit()
            print(f"   ✅ 資料庫補欄位：{table}.{col}")
        except Exception:
            pass  # 欄位已存在，忽略

    # 2026/09/15補（文件A決策③後續）：持股健檢改讀watchlist_items之後，舊portfolios表裡
    # 使用者原本存的持股（股票代號＋買入價）不會自動出現在新的持股健檢畫面——等於舊資料
    # 被藏起來了。這裡做「只跑一次」的搬移：舊持股併進watchlist_items（已在自選股裡的
    # 補上買入價，不在的新增到「預設」族群），舊portfolios表不刪除。
    # 用db_migrations表記錄已跑過，之後使用者自己移除持股健檢追蹤不會被重啟時又搬回來。
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS db_migrations (name TEXT PRIMARY KEY, done_at TEXT)")
        _mig = "20260915_portfolios_to_watchlist"
        if not conn.execute("SELECT 1 FROM db_migrations WHERE name=?", (_mig,)).fetchone():
            _moved = 0
            for _r in conn.execute(
                "SELECT user_email, stock_id, stock_name, cost_price, created_at FROM portfolios"
            ).fetchall():
                _cur = conn.execute(
                    "UPDATE watchlist_items SET cost_price=? "
                    "WHERE user_email=? AND stock_id=? AND (cost_price IS NULL OR cost_price<=0)",
                    (_r["cost_price"], _r["user_email"], _r["stock_id"]))
                if _cur.rowcount:
                    _moved += 1
                    continue
                _cur = conn.execute(
                    "INSERT OR IGNORE INTO watchlist_items "
                    "(user_email, stock_id, stock_name, group_name, added_date, cost_price) "
                    "VALUES (?,?,?,?,?,?)",
                    (_r["user_email"], _r["stock_id"], _r["stock_name"] or "", "預設",
                     str(_r["created_at"] or "")[:10], _r["cost_price"]))
                _moved += _cur.rowcount
            conn.execute("INSERT INTO db_migrations (name, done_at) VALUES (?, datetime('now','+8 hours'))", (_mig,))
            conn.commit()
            print(f"   ✅ 舊持股健檢資料搬進自選股：{_moved} 筆")
    except Exception as _me:
        print(f"   ⚠️ 舊持股健檢資料搬移失敗（不影響啟動）：{_me}")

    # line_user_id 需要唯一索引（同一個LINE帳號不能對應到兩筆會員），
    # NULL值在SQLite的UNIQUE INDEX裡不會互相衝突，所以既有的Email/Google會員不受影響
    try:
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_members_line_user_id ON members(line_user_id)")
        conn.commit()
    except Exception:
        pass

    # 自動建立管理員帳號（已存在則不覆蓋）
    # 安全性修正（2026/07/26）：舊版此處在環境變數未設定時會 fallback 到寫死的真實密碼 "630428"，已移除。
    # 現在若未設定 ADMIN_DEFAULT_PWD，會直接跳過建立管理員帳號，不會再用預設密碼建帳號。
    ADMIN_EMAIL  = os.environ.get("ADMIN_EMAIL", "watione@yahoo.com.tw")
    ADMIN_PWD    = os.environ.get("ADMIN_DEFAULT_PWD", "")
    ADMIN_EXPIRE = "2099-12-31"
    existing = conn.execute("SELECT id FROM members WHERE email=?", (ADMIN_EMAIL,)).fetchone()
    if not existing:
        if not ADMIN_PWD:
            print("⚠️  [ADMIN] 未設定環境變數 ADMIN_DEFAULT_PWD，略過建立管理員帳號。")
        else:
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
    today = _taipei_today()
    if user["plan"] == "free":
        raise HTTPException(status_code=403, detail="此功能需付費方案")
    if user.get("expire_at") and user["expire_at"] < today:
        raise HTTPException(status_code=403, detail="訂閱已到期，請續費後使用")
    return user


# ══════════════════════════════════════════════════════════
# 小遊戲排行榜 API（2026/08/15 新增：帥哥鴻反饋「沒有比賽機制，
# 可以設定登入加入比賽排名」）
#
# 沿用既有會員系統（require_user／JWT），不另外做一套帳號系統：
#   - 送分（POST /api/games/score）需要登入，分數綁在會員帳號上
#   - 排行榜（GET /api/games/leaderboard/{slug}）公開瀏覽，不需登入
#   - 個人排名（GET /api/games/my-rank/{slug}）需要登入
#
# 每款遊戲的「分數越低越好」或「越高越好」不一樣（反應時間、翻牌步數
# 是越小越好；打地鼠/鋼琴塊/貪食蛇是越大越好），用 _GAME_SCORE_DIRECTION
# 統一設定，排行榜排序、個人最佳成績計算都依這個方向判斷，不是每個
# API各自寫死排序邏輯。
#
# _GAME_SCORE_BOUNDS 是基本防呆用的合理範圍檢查（擋掉明顯亂改的離譜
# 數值，例如反應時間0毫秒或負數），不是完整的防作弊機制——真要防
# 刷分數需要伺服器端重新驗證遊戲過程，這款輕量小遊戲先不做到那麼
# 複雜，之後如果真的發現有人大量刷榜再加強。
# ══════════════════════════════════════════════════════════
_GAME_SCORE_DIRECTION = {
    "reaction-time-test": "asc",   # 反應時間（毫秒），越低越好
    "memory-match":       "asc",   # 翻牌步數，越少越好
    "whack-a-mole":       "desc",  # 打地鼠分數，越高越好
    "piano-tiles":        "desc",  # 鋼琴塊分數，越高越好
    "snake":               "desc", # 貪食蛇分數，越高越好
}
_GAME_SCORE_BOUNDS = {
    "reaction-time-test": (30, 5000),
    "memory-match":       (8, 300),
    "whack-a-mole":       (0, 2000),
    "piano-tiles":        (0, 5000),
    "snake":              (0, 500),
}
_GAME_NAMES_ZH = {
    "reaction-time-test": "反應力測試",
    "memory-match":       "記憶翻牌",
    "whack-a-mole":       "打地鼠",
    "piano-tiles":        "鋼琴塊",
    "snake":              "貪食蛇",
}


class _GameScoreReq(BaseModel):
    game_slug: str
    score: int


def _game_display_name(row: dict) -> str:
    """排行榜顯示名稱：優先用暱稱，沒設定暱稱就用匿名代號（不能公開顯示Email，保護隱私）"""
    nick = (row.get("nickname") or "").strip()
    if nick:
        return nick
    return "玩家" + str(row.get("id", 0)).zfill(4)[-4:]


def _game_rank_query(game_slug: str, direction: str, agg: str, better_than_value):
    """回傳「目前排在這個分數前面的人數 + 1」＝該分數的名次（純SQL輔助函式）"""
    cmp_op = "<" if direction == "asc" else ">"
    return (
        f"""
        SELECT COUNT(*) + 1 AS rank FROM (
            SELECT member_id, {agg}(score) AS best
            FROM game_scores WHERE game_slug=?
            GROUP BY member_id
        ) WHERE best {cmp_op} ?
        """,
        (game_slug, better_than_value)
    )


@app.post("/api/games/score")
def submit_game_score(req: _GameScoreReq, user: dict = Depends(require_user)):
    game_slug = req.game_slug.strip()
    if game_slug not in _GAME_SCORE_DIRECTION:
        raise HTTPException(status_code=400, detail="未知的遊戲")
    lo, hi = _GAME_SCORE_BOUNDS[game_slug]
    if not (lo <= req.score <= hi):
        raise HTTPException(status_code=400, detail="分數超出合理範圍")

    direction = _GAME_SCORE_DIRECTION[game_slug]
    agg = "MIN" if direction == "asc" else "MAX"

    conn = _db_conn()
    conn.execute(
        "INSERT INTO game_scores (member_id, game_slug, score) VALUES (?, ?, ?)",
        (user["id"], game_slug, req.score)
    )
    conn.commit()

    best_row = conn.execute(
        f"SELECT {agg}(score) AS best FROM game_scores WHERE member_id=? AND game_slug=?",
        (user["id"], game_slug)
    ).fetchone()
    personal_best = best_row["best"] if best_row else req.score
    is_new_best = (req.score == personal_best)

    sql, params = _game_rank_query(game_slug, direction, agg, personal_best)
    rank_row = conn.execute(sql, params).fetchone()
    rank = rank_row["rank"] if rank_row else None
    conn.close()

    return {
        "ok": True,
        "score": req.score,
        "personal_best": personal_best,
        "is_new_best": is_new_best,
        "rank": rank,
    }


@app.get("/api/games/leaderboard/{game_slug}")
def get_game_leaderboard(game_slug: str, limit: int = 20):
    if game_slug not in _GAME_SCORE_DIRECTION:
        raise HTTPException(status_code=400, detail="未知的遊戲")
    limit = max(1, min(limit, 100))
    direction = _GAME_SCORE_DIRECTION[game_slug]
    agg = "MIN" if direction == "asc" else "MAX"
    order = "ASC" if direction == "asc" else "DESC"

    conn = _db_conn()
    rows = conn.execute(
        f"""
        SELECT m.id AS id, m.nickname AS nickname, best.best AS score
        FROM (
            SELECT member_id, {agg}(score) AS best
            FROM game_scores WHERE game_slug=?
            GROUP BY member_id
        ) best
        JOIN members m ON m.id = best.member_id
        ORDER BY best.best {order}
        LIMIT ?
        """,
        (game_slug, limit)
    ).fetchall()
    conn.close()

    leaderboard = [
        {"rank": i + 1, "name": _game_display_name(dict(r)), "score": r["score"]}
        for i, r in enumerate(rows)
    ]
    return {
        "game_slug": game_slug,
        "game_name": _GAME_NAMES_ZH.get(game_slug, game_slug),
        "direction": direction,
        "leaderboard": leaderboard,
    }


@app.get("/api/games/my-rank/{game_slug}")
def get_my_game_rank(game_slug: str, user: dict = Depends(require_user)):
    if game_slug not in _GAME_SCORE_DIRECTION:
        raise HTTPException(status_code=400, detail="未知的遊戲")
    direction = _GAME_SCORE_DIRECTION[game_slug]
    agg = "MIN" if direction == "asc" else "MAX"

    conn = _db_conn()
    best_row = conn.execute(
        f"SELECT {agg}(score) AS best FROM game_scores WHERE member_id=? AND game_slug=?",
        (user["id"], game_slug)
    ).fetchone()
    if not best_row or best_row["best"] is None:
        conn.close()
        return {"game_slug": game_slug, "has_score": False}

    personal_best = best_row["best"]
    sql, params = _game_rank_query(game_slug, direction, agg, personal_best)
    rank_row = conn.execute(sql, params).fetchone()
    conn.close()
    return {
        "game_slug": game_slug,
        "has_score": True,
        "personal_best": personal_best,
        "rank": rank_row["rank"] if rank_row else None,
    }


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
    return exp >= _taipei_today()


def _is_premium(user: dict | None) -> bool:
    """付費或邀請解鎖（未過期）。與深度選股／論壇寫入同一套。"""
    if not user:
        return False
    if _is_referral_active(user):
        return True
    if user.get("plan") == "free":
        return False
    exp = user.get("expire_at")
    if exp and exp < _taipei_today():
        return False
    return True


def _client_ip(request) -> str:
    if request is None:
        return "unknown"
    try:
        return request.client.host if request.client else "unknown"
    except Exception:
        return "unknown"


def _daily_credit_key(request, user) -> tuple[int, str, int]:
    if user is None:
        return 0, _client_ip(request), GUEST_DAILY_LIMIT
    return int(user["id"]), "", FREE_DAILY_LIMIT


def _check_daily_credit(request, user) -> tuple[bool, int, int]:
    """daily_credit：(allowed, used, limit)。paid／referral 不消耗。"""
    if _is_premium(user):
        return True, 0, 999
    member_id, ip, limit = _daily_credit_key(request, user)
    today = _taipei_today()
    conn = _db_conn()
    row = conn.execute(
        "SELECT count FROM query_log WHERE member_id=? AND date=? AND ip=?",
        (member_id, today, ip),
    ).fetchone()
    used = row["count"] if row else 0
    conn.close()
    return used < limit, used, limit


def _consume_daily_credit(request, user) -> None:
    """成功後扣 1。SELECT 再 UPDATE／INSERT，不依賴 ON CONFLICT。"""
    if _is_premium(user):
        return
    member_id, ip, _limit = _daily_credit_key(request, user)
    today = _taipei_today()
    conn = _db_conn()
    row = conn.execute(
        "SELECT id, count FROM query_log WHERE member_id=? AND date=? AND ip=?",
        (member_id, today, ip),
    ).fetchone()
    if row:
        conn.execute("UPDATE query_log SET count=count+1 WHERE id=?", (row["id"],))
    else:
        conn.execute(
            "INSERT INTO query_log (member_id, date, ip, count) VALUES (?, ?, ?, 1)",
            (member_id, today, ip),
        )
    conn.commit()
    conn.close()


_PORTFOLIO_CREDIT_DEDUP: dict[str, float] = {}
_PORTFOLIO_DEDUP_SEC = 45.0


def _consume_portfolio_daily_credit(request, user) -> None:
    if _is_premium(user) or not user:
        return
    key = f"{user['id']}:{_taipei_today()}"
    now = _time_mod.time()
    last = _PORTFOLIO_CREDIT_DEDUP.get(key, 0.0)
    if now - last < _PORTFOLIO_DEDUP_SEC:
        return
    _PORTFOLIO_CREDIT_DEDUP[key] = now
    _consume_daily_credit(request, user)


def _credit_dict(used: int, limit: int) -> dict:
    return {"used": used, "limit": limit, "remaining": max(0, limit - used)}


def _quota_429(code: str, msg: str, used: int, limit: int):
    """429 + credit，給 FE modal／_syncCreditFromPayload。"""
    return JSONResponse(
        status_code=429,
        content={"detail": f"{code}|{msg}", "credit": _credit_dict(used, limit)},
    )

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
def get_kline(stock_id: str, tf: str = "D", user: dict | None = Depends(get_current_user)):
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

    # 日K：若最後一根不是今日，嘗試從 _QUOTE_CACHE 補今日即時K棒（2026/07/30 改用共用函式）
    chart_note = None
    if tf.upper() == "D" and records:
        from zoneinfo import ZoneInfo as _ZI
        _tw_today = datetime.now(_ZI("Asia/Taipei")).strftime("%Y-%m-%d")
        if records[-1]["date"] != _tw_today:
            _code = stock_id.strip().upper().replace(".TW", "").replace(".TWO", "")
            _q = _get_live_quote_data(_code)
            if _q:
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
                else:
                    chart_note = "今日K棒資料更新中，稍後重新整理即可看到"
            else:
                # 2026/07/30：三層報價來源同時暫時失敗時，不再讓圖表悄悄停留在昨天，改為明確告知前端
                chart_note = "今日K棒資料更新中，稍後重新整理即可看到"

    return {"symbol": symbol, "tf": tf, "count": len(records), "bars": records, "chart_note": chart_note}


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
    golden = k_now > d_now + 0.5 and k_prev <= d_prev + 0.5   # 差距>0.5才算金叉
    death  = k_now < d_now - 0.5 and k_prev >= d_prev - 0.5   # 差距>0.5才算死叉
    if k_now >= 80:
        zone, zone_dir = "超買區（>80），注意高檔鈍化風險", "warning"
    elif k_now <= 20:
        zone, zone_dir = "超賣區（<20），關注底部反彈機會", "bullish"
    elif k_now >= 50:
        zone, zone_dir = "多方優勢區（50~80）", "bullish"
    else:
        zone, zone_dir = "空方優勢區（20~50）", "bearish"
    cross = "，本日金叉（多方訊號）" if golden else ("，本日死叉（空方訊號）" if death else "")
    direction = "bullish" if golden else ("bearish" if death else zone_dir)
    return {
        "text": f"K={k_now:.1f}，D={d_now:.1f}，位於{zone}{cross}",
        "direction": direction, "k": k_now, "d": d_now,
        "k_change": round(k_now - k_prev, 1),
        "d_change": round(d_now - d_prev, 1),
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
        "today_vol": round(vols[-1]) if vols else 0,
        "yesterday_vol": round(vols[-2]) if len(vols) >= 2 else 0,
        "today_vs_yesterday": round(vols[-1] / vols[-2], 2) if len(vols) >= 2 and vols[-2] > 0 else 1.0,
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
        # 2026/09/17修正：FinMind 買賣超單位是「股」，這裡要換成「張」（÷1000）。
        # 原本沒換，個股分析「法人動向」顯示成 +8,366,418張（實際約 8,366 張），
        # 風險提示「賣超超過500張」與綜合解說的法人張數也跟著錯。
        def _lots(key): return int(round(sum(r.get(key, 0) for r in inst_5d) / 1000))
        foreign5 = _lots("foreign")
        invest5  = _lots("invest")
        dealer5  = _lots("dealer")
        total5   = _lots("total")
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
        risks.append(f"損益比 {rr_ratio}，現價距壓力 {resistance} 空間不足，風險大於報酬")
    k_val = kd_info.get("k")
    if k_val and k_val >= 80:
        risks.append(f"KD={k_val:.0f} 進入超買區，高檔容易鈍化，短線過熱")
    elif kd_info.get("death_cross"):
        risks.append(f"KD 剛發生死叉（K={k_val:.0f}），動能轉弱，留意後續賣壓")
    dif_val = macd_info.get("dif")
    if dif_val is not None and dif_val < -0.5:
        risks.append(f"MACD DIF={dif_val:.3f} 在 0 軸深處，空頭動能強，反彈需謹慎")
    elif macd_info.get("direction") == "slightly_bearish":
        risks.append("MACD 多頭轉弱，接近死叉，注意動能確認")
    supp_dist = (price - support) / price * 100
    if supp_dist > 8:
        risks.append(f"支撐 {support} 距現價 {supp_dist:.1f}%，與支撐距離較大，短線波動空間大")
    total5 = inst.get("total_5d", 0)
    if total5 < -500:
        risks.append(f"法人近5日賣超 {total5:,} 張，籌碼持續流出")
    if kbar_info.get("direction") == "bearish":
        risks.append(f"K棒出現{kbar_info.get('type','')}，空頭訊號，止跌訊號尚未出現")
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
        # 做法A（2026/08/04）：盤中快取命中時，即時報價「只更新 display_price（畫面現價）
        # 與 change/change_pct」，不再覆蓋 price / analysis_price（分析基準）。
        # 分析基準永遠鎖定當初算好的收盤 K 棒，即時價只影響畫面現價那個數字。
        if _is_trading_session():
            _qd_c = _get_live_quote_data(stock_id)
            if _qd_c:
                _live = float(_qd_c["price"])
                if _live > 0:
                    cached = dict(cached)
                    cached["display_price"] = round(_live, 2)   # 只動畫面現價
                    cached["change"]        = _qd_c.get("change")
                    cached["change_pct"]    = _qd_c.get("change_pct")
                    # 這次補抓成功，清掉先前「報價更新中」的提示
                    if cached.get("price_note") == "報價更新中，現價暫以前一交易日收盤價顯示":
                        cached["price_note"] = None
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
            detail=f"暫時抓不到 {stock_id} 的股價資料（市場別：{mtype}），"
                   f"可能是資料來源暫時忙碌，請稍後再試；若代號正確仍持續出現，請聯絡客服。"
        )

    # 2026/08/14 新增：資料新鮮度旗標，要在 df 被切片/dropna 之前先讀出來，
    # 避免 pandas .attrs 在後續操作中遺失（.attrs 官方文件標註為實驗性、不保證會傳遞）。
    _data_stale        = bool(getattr(df, "attrs", {}).get("data_stale"))
    _data_stale_latest = df.attrs.get("data_stale_latest") if _data_stale else None

    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    opens      = df["Open"].values.astype(float)
    closes     = df["Close"].values.astype(float)
    closes_full= closes.copy()   # 保留完整序列供 MA 計算
    highs      = df["High"].values.astype(float)
    lows       = df["Low"].values.astype(float)
    volumes    = df["Volume"].values.astype(float)
    price      = round(float(closes[-1]), 2)

    # 現價漲跌%：用最近兩根收盤價計算，不依賴即時報價（收盤後也能顯示）
    price_change_pct = None
    if len(closes) >= 2 and closes[-2] > 0:
        price_change_pct = round((closes[-1] - closes[-2]) / closes[-2] * 100, 2)

    # ── 做法A（2026/08/04）：分析基準與顯示現價徹底切開 ──
    # price（＝分析基準）永遠鎖定「最近一根確定收盤 K 棒」，即時報價「不再覆蓋」它，
    # 也「不再改動 closes[-1] / closes_full[-1]」——所以下游全部分析
    # （支撐距離、防守位、損益比、乖離率、雷達）都建立在穩定的收盤基準上，
    # 即時報價抓不到 / 抓成昨收，都不會再污染分析結論。
    # 即時報價只放進 display_price（畫面現價用），與分析完全脫鉤。
    #
    # analysis_price ：分析基準（確定收盤），下游計算與 result 分析欄位都用它（＝price 變數）
    # display_price  ：畫面現價（盤中即時，抓不到就等於收盤基準）
    # price_basis_date：分析基準是哪一天的收盤（給前端時間標示用）
    _sid = stock_id.strip().upper()
    analysis_price   = price                              # 分析基準＝確定收盤，永不被即時價覆蓋
    price_basis_date = _taipei_today()                    # 收盤 K 棒基準日（下方會依 df 實際日期校正）
    try:
        _basis_dt = df.index[-1]
        price_basis_date = _basis_dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    display_price  = price                                # 預設＝收盤基準；抓到即時價才覆蓋
    _live_quote_ok = False                                # 是否真的拿到即時報價（僅影響 display 與快取時效）
    _qd = _get_live_quote_data(_sid)
    if _qd:
        _live_price = float(_qd["price"])
        if _live_price > 0:
            display_price  = round(_live_price, 2)        # 只更新畫面現價，不碰 price / closes[-1]
            _live_quote_ok = True

    # 股名
    stock_name = get_stock_name(symbol)

    # 均線
    ma_periods = [p for p in [ma1, ma2, ma3, ma4, ma5] if p and p > 0]
    ma_values = {f"ma{p}": safe_float(calc_ma(closes, p)[-1]) for p in ma_periods}

    # 趨勢（2026/08/06 改用道氏波峰波谷，取代原 MA20/MA60 均線判斷）
    # 道氏經回測（2021-2026 台股、做多三批+空方+多天期）驗證鑑別力明顯優於均線；
    # 資料不足以判斷時，自動 fallback 回原 MA20/MA60 邏輯，確保不會壞掉或變空白。
    trend = _dow_trend(highs, lows, order=5)
    if trend is None:
        _ma20_last = calc_ma(closes, 20)[-1]
        _ma60_last = calc_ma(closes, 60)[-1]
        if not np.isnan(_ma20_last) and not np.isnan(_ma60_last):
            trend = "上升趨勢" if _ma20_last > _ma60_last * 1.003 else "下降趨勢" if _ma20_last < _ma60_last * 0.997 else "盤整"
        else:
            avail = [(p, calc_ma(closes, p)[-1]) for p in sorted(ma_periods)
                     if not np.isnan(calc_ma(closes, p)[-1])]
            trend = "觀察中"
            if len(avail) >= 2:
                s, l = avail[0][1], avail[-1][1]
                trend = "上升趨勢" if s > l * 1.005 else "下降趨勢" if s < l * 0.995 else "盤整"
    else:
        # 2026/08/08：MA20/MA60 校正層——道氏波峰波谷判斷的是「短期結構」，
        # 容易把長期空頭中的技術性反彈誤判成「上升趨勢」（反之亦然，長期多頭中
        # 的拉回也可能被誤判成「下降趨勢」）。加一層均線方向校正：若波峰波谷判斷
        # 跟 MA20/MA60 的相對位置矛盾（例如判上升趨勢，但短均線還在季線下方、
        # 尚未站上），代表這波結構訊號力道不足，降級為「盤整」而非直接翻轉方向
        # （翻轉方向風險較高，容易造成另一種誤判）。緩衝帶用 1%（經 6547/6770/2454/
        # 2303/4908 五支股票回測比較 0.3%/1%/2%/3% 後選定：1% 比 0.3% 觸發頻率降
        # 約10-15%，但抓假訊號效果仍保留85-90%以上；放寬到2%以上效果會明顯流失）。
        _ma20_last = calc_ma(closes, 20)[-1]
        _ma60_last = calc_ma(closes, 60)[-1]
        if not np.isnan(_ma20_last) and not np.isnan(_ma60_last):
            if trend == "上升趨勢" and _ma20_last < _ma60_last * 0.99:
                trend = "盤整"
            elif trend == "下降趨勢" and _ma20_last > _ma60_last * 1.01:
                trend = "盤整"

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
                alt_res_desc = "軌道上緣推算"
            else:
                # 波段等幅投影：(近60根高點 - 近60根低點) + 近60根高點
                _swing_high = float(highs[-60:].max()) if len(highs) >= 60 else float(highs.max())
                _swing_low  = float(lows[-60:].min())  if len(lows)  >= 60 else float(lows.min())
                _swing_proj = round(_swing_high + (_swing_high - _swing_low), 2)
                if _swing_proj > price * (1 + MIN_RES_DIST):
                    alt_res = _swing_proj
                    alt_res_desc = "波段等幅推算價位（突破後推算）"
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
    kbar_pattern, kbar_warning, kbar_dir, kbar_win_rate = detect_kbar_pattern(opens, highs, lows, closes, volumes)

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

    # ── 葛蘭碧賣點偵測（賣5/6/7/8，MA20 / MA60，≤2根時效）──
    gann_s20_sig, gann_s20_val, gann_s20_name, gann_s20_type, gann_s20_dev = detect_gann_sell(closes, highs, lows, volumes, 20)
    gann_s60_sig, gann_s60_val, gann_s60_name, gann_s60_type, gann_s60_dev = detect_gann_sell(closes, highs, lows, volumes, 60)
    # 優先用 MA20（短均線對賣壓較敏感），其次 MA60
    gann_sell = None
    if gann_s20_sig:
        gann_sell = {"ma": gann_s20_name, "val": gann_s20_val, "type": gann_s20_type, "is_deviate": gann_s20_dev}
    elif gann_s60_sig:
        gann_sell = {"ma": gann_s60_name, "val": gann_s60_val, "type": gann_s60_type, "is_deviate": gann_s60_dev}

    # ── 量價出場警訊（複用 detect_kbar_pattern 型態結果 + 補爆量判斷）──
    # 設計原則（帥哥鴻定案）：
    #  1. 型態複用 kbar_pattern，判斷標準與畫面顯示一致，不重寫、不改 detect_kbar_pattern
    #  2. 「爆量」= 當日量 ≥ 近20日均量 × 1.5
    #  3. 不限股價位置（有此量價現象就提醒）
    #  4. 因型態是收盤才確認、當天來不及出，警訊寫成「隔天盤前行動指令」而非事後描述
    #  5. 與買賣結論並列、不強制覆蓋（避免多頭回測誤殺）
    vp_exit_warn = None   # 量價出場警訊（dict 或 None）
    _bearish_kbar_keys = ("大黑棒", "射擊之星", "流星", "空頭吞噬", "黃昏之星", "烏雲罩頂", "跌停", "長上影黑K")
    _is_bearish_shape = bool(kbar_pattern) and any(k in kbar_pattern for k in _bearish_kbar_keys)
    if _is_bearish_shape and len(volumes) >= 20:
        _vp_today_vol = float(volumes[-1])
        _vp_ma20_vol  = float(np.mean(volumes[-20:]))
        _vp_vol_x = round(_vp_today_vol / _vp_ma20_vol, 2) if _vp_ma20_vol > 0 else 0
        if _vp_vol_x >= 1.5:
            # 明日觀察點：今日大黑棒/長上影的一半價位（收復不了視為賣壓延續）
            _vp_today_mid = round((float(highs[-1]) + float(lows[-1])) / 2, 2)
            vp_exit_warn = {
                "shape": kbar_pattern,
                "vol_x": _vp_vol_x,
                "watch": _vp_today_mid,
            }

    # 突破壓力 / 跌破支撐訊號
    breakout_idx, breakdown_idx, breakout_stale, breakdown_stale = calc_breakout_signals(
        closes, highs, lows, volumes, support, resistance)

    # 防守位：2026/08/13改為隨乖離率（現價偏離MA20的幅度）動態調整
    # （分析引擎第三批候選A，已用60檔台股2022/06~2026/08真實K線資料回測476筆金叉訊號：
    #  停損率31.3%→24.4%、勝率49.6%→48.9%（誤差範圍內）、平均報酬+0.26%→+0.31%，
    #  帥哥鴻拍板採用。回測腳本見 scripts/backtest_stop_rr.py，候選B/AB回測後不建議採用未採納）
    #   乖離 ≥10%（現價已大幅偏離月線，過熱）→ 停損收緊到現價 -3%
    #   乖離 5%~10%（正常偏熱）→ 停損維持現價 -5%
    #   乖離 <5%（貼近月線，剛起漲）→ 停損放寬到現價 -8%（避免被月線附近正常雜訊洗出場）
    _ma20_now = ma_values.get("ma20")
    if _ma20_now and _ma20_now > 0:
        deviation_pct = (price - _ma20_now) / _ma20_now * 100
        if deviation_pct >= 10:
            _stop_pct = 0.03
        elif deviation_pct >= 5:
            _stop_pct = 0.05
        else:
            _stop_pct = 0.08
        raw_stop = round(price * (1 - _stop_pct), 2)
    else:
        # MA20資料不足時的保底：沿用原本以支撐為錨的邏輯，避免掛掉
        sup_dist_pct = (price - support) / price * 100
        raw_stop = round(price * 0.95, 2) if sup_dist_pct > 5 else round(support * 0.985, 2)
    stop_nearest = round(price * 0.98, 2)   # 最近：不能超過現價 -2%（太緊容易被洗）
    stop_farthest = round(price * 0.90, 2)  # 最遠：不超過現價 -10%（太遠失去意義）
    # raw_stop 夾在 stop_farthest ~ stop_nearest 之間
    stop_loss = max(stop_farthest, min(raw_stop, stop_nearest))

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
    rr_basis  = "失效位置"             # 說明計算基礎，供前端顯示（2026/09/17 防守位改稱失效位置）

    # 快速計算量比（供風險評估用）
    _quick_vol_ratio = None
    if len(volumes) >= 20:
        _qv5  = sum(float(v) for v in volumes[-5:]) / 5
        _qv20 = sum(float(v) for v in volumes[-20:]) / 20
        _quick_vol_ratio = round(_qv5 / _qv20, 2) if _qv20 > 0 else 1.0

    # 風險等級（含量能判斷）
    risk_level, risk_label, risk_color = calc_risk_level(
        price, support, resistance, rr_ratio, near_top, near_bot, pattern, vol_ratio=_quick_vol_ratio)

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
            conflict_note = f"⚠ 注意：趨勢偏多但股價在下降軌道內，短線結構偏弱，支撐可能失守，方向需再確認"
        elif trend == "下降趨勢" and channel_type == "up":
            conflict_note = f"⚠ 注意：趨勢偏空但股價在上升軌道內，反彈動能存在但趨勢仍弱，趨勢尚未轉向"

    # 軌道趨勢矛盾警告（插在最前面，醒目位置）
    if conflict_note:
        summary_lines.insert(0, conflict_note)

    # 反轉/三角型態加進摘要
    if reversal:
        summary_lines.insert(0, f"圖形型態：{reversal['desc']}，{reversal['position_desc']}")

    # K棒方向判斷（含操作建議）
    kbar_bullish = any(k in kbar_pattern for k in ["錘頭","多頭吞噬","早晨之星","三紅兵","穿刺線","大紅棒","漲停","長下影紅K"]) if kbar_pattern else False
    kbar_bearish = any(k in kbar_pattern for k in ["射擊之星","空頭吞噬","黃昏之星","三烏鴉","烏雲蓋頂","大黑棒","跌停","長上影黑K"]) if kbar_pattern else False
    kbar_neutral = not kbar_bullish and not kbar_bearish

    # K棒操作說明對照（具體化）
    # 2026/09/17（案件008）：改成描述式——說明型態代表什麼、明天觀察什麼、什麼條件代表失效，不下買賣指示
    KBAR_ACTION = {
        "錘頭線":       f"下檔出現承接；明天若收紅且量縮，型態較完整，跌破 {stop_loss} 則型態失效",
        "射擊之星":     f"高檔出現賣壓，屬頂部反轉訊號；觀察支撐 {support} 是否守住",
        "十字星":       f"多空力道暫時平衡，方向未定，明天收盤是觀察重點",
        "大紅棒":       f"今日強攻；明天若縮量整理且不跌破今日收盤 {round(float(closes[-1]),2)}，多方結構延續",
        "大黑棒":       f"今日強殺，空方力道強；觀察能否在支撐 {support} 附近出現止跌訊號",
        "長上影黑K":     f"衝高後遭賣壓壓回；明天若無法收復今日高點的一半，轉弱訊號加重，關鍵失效位置 {stop_loss}",
        "長下影紅K":     f"殺低後出現承接；明天若延續收紅，止跌訊號較明確，跌破 {stop_loss} 則型態失效",
        "多頭吞噬":     f"底部反轉訊號；明天收紅可確認型態，跌破 {stop_loss} 則型態失效",
        "空頭吞噬":     f"頂部反轉訊號；明天若收黑則轉弱訊號確認，觀察支撐 {support} 是否守住",
        "孕線":         f"整理型態，觀察後續突破今日高點或跌破今日低點的方向",
        "穿刺線":       f"底部潛在反轉；明天若繼續收紅，多方條件增加，跌破 {stop_loss} 則型態失效",
        "烏雲蓋頂":     f"頂部潛在反轉；明天若收黑則轉弱訊號確認，觀察支撐 {support}",
        "早晨之星":     f"底部強力反轉訊號；前方壓力 {resistance}，跌破 {stop_loss} 則型態失效",
        "黃昏之星":     f"頂部強力反轉訊號；觀察股價回到支撐 {support} 附近時是否出現止跌K棒",
        "三紅兵":       f"多方強勢延續；連漲三天後短線乖離擴大，過熱風險增加",
        "三烏鴉":       f"空方強勢延續；觀察跌勢是否止穩、支撐 {support} 是否守住",
    }

    # 找對應的操作說明
    kbar_action = ""
    for key, action in KBAR_ACTION.items():
        if kbar_pattern and key in kbar_pattern:
            kbar_action = action
            break

    # 孕線特化：若昨天已出現突破/跌破訊號，今天的孕線其實是「突破隔日拉回」而非單純整理，
    # 用 breakout_idx / breakdown_idx 判斷並改寫成對應的拉回敘事
    if kbar_pattern and "孕線" in kbar_pattern:
        _n_bars = len(closes)
        if breakout_idx is not None and breakout_idx == _n_bars - 2:
            _bo_price = round(float(closes[breakout_idx]), 2)
            kbar_action = f"昨日已放量突破，今日縮量拉回整理，屬正常拉回而非反轉；不跌破昨日突破價 {_bo_price} 則突破結構維持，跌破則突破失敗"
        elif breakdown_idx is not None and breakdown_idx == _n_bars - 2:
            _bd_price = round(float(closes[breakdown_idx]), 2)
            kbar_action = f"昨日已放量跌破，今日縮量反彈整理，屬弱勢反彈而非止跌；站回昨日跌破價 {_bd_price} 才代表跌破失敗"

    near_sup = pattern in ("支撐整理",) or (price - support) / price < 0.04
    near_res = pattern in ("壓力整理",) or (resistance - price) / price < 0.04

    # 軌道下緣靠近判斷（距現價 ≤3%）
    ch_near_sup = False
    ch_sup_desc = ""
    if channel and channel.get("position") == "near_support":
        ch_near_sup = True
        ch_sup_val = channel.get("support_now", support)
        ch_sup_desc = f"靠近軌道下緣支撐 {ch_sup_val}"

    # 2026/09/17（案件008）：結論改描述式，「操作：」改「觀察重點：」，只寫條件與失效位置，不寫買賣動作
    if near_sup:
        if rr_ratio >= 1.5 and kbar_bullish:
            conclusion = f"靠近支撐 {support}，出現多頭K棒（{kbar_pattern}），損益比 {rr_ratio}。觀察重點：{kbar_action or f'支撐是否守住；跌破 {stop_loss} 代表型態失效，前方壓力 {resistance}'}"
        elif rr_ratio >= 1.5 and kbar_neutral:
            conclusion = f"靠近支撐 {support}，K棒方向未定（{kbar_pattern or '無明確型態'}）。觀察重點：明天收盤方向；跌破 {stop_loss} 代表型態失效"
        elif rr_ratio >= 1.5 and kbar_bearish:
            conclusion = f"靠近支撐 {support}，但出現空頭K棒（{kbar_pattern}），支撐恐失守。觀察重點：{kbar_action or f'收盤是否跌破 {support}，跌破則支撐型態失效'}"
        else:
            conclusion = f"靠近支撐 {support}，但損益比 {rr_ratio} 偏低（壓力 {resistance} 太遠或太近）。觀察重點：支撐是否守住；失效位置 {stop_loss}"
    elif ch_near_sup and not near_res:
        ch_sup_val = channel.get("support_now", support)
        if kbar_bullish:
            conclusion = f"{ch_sup_desc}，出現多頭K棒（{kbar_pattern}），位置風險相對低。觀察重點：{kbar_action or f'軌道支撐是否守住；跌破 {stop_loss} 代表型態失效，前方壓力 {resistance}'}"
        elif kbar_bearish:
            conclusion = f"{ch_sup_desc}，但出現空頭K棒（{kbar_pattern}），軌道支撐恐失守。觀察重點：{kbar_action or f'收盤是否跌破軌道下緣 {ch_sup_val}，跌破則軌道結構失效'}"
        else:
            conclusion = f"{ch_sup_desc}，位置風險相對低。觀察重點：是否出現止跌K棒確認守住；失效位置 {stop_loss}，前方壓力 {resistance}"
    elif gann_recross:
        # 葛蘭碧多方訊號（含訊號類型）
        ma_name  = gann_recross["ma"]
        ma_val   = gann_recross["val"]
        g_stop   = gann_recross["stop"]
        buy_type = gann_recross.get("type", "葛蘭碧多方訊號")
        if kbar_bullish:
            conclusion = f"{buy_type}：{ma_name}（{ma_val}），出現多頭K棒（{kbar_pattern}），多方條件增加。觀察重點：是否站穩 {ma_name}；跌破 {g_stop}（{ma_name} 下方）代表訊號失效，前方壓力 {resistance}"
        elif kbar_bearish:
            conclusion = f"{buy_type}：{ma_name}（{ma_val}），但出現空頭K棒（{kbar_pattern}），力道存疑。觀察重點：明天能否站穩 {ma_name}；失效位置 {g_stop}"
        else:
            conclusion = f"{buy_type}：{ma_name}（{ma_val}），出現多方訊號。觀察重點：明天能否站穩 {ma_name}；跌破 {g_stop} 代表訊號失效，前方壓力 {resistance}"
    elif near_res:
        if kbar_bullish:
            conclusion = f"靠近壓力 {resistance}，出現多頭K棒（{kbar_pattern}）。觀察重點：{kbar_action or f'能否放量突破 {resistance}；未突破前仍屬壓力區，失效位置 {stop_loss}'}"
        elif kbar_bearish:
            conclusion = f"靠近壓力 {resistance}，出現空頭K棒（{kbar_pattern}），拉回風險高。觀察重點：{kbar_action or f'是否回落至支撐 {support} 附近及能否守住'}"
        else:
            conclusion = f"靠近壓力 {resistance}，上方空間有限。觀察重點：是否放量突破 {resistance}，或回測支撐 {support}；失效位置 {stop_loss}"
    elif pattern == "突破型態":
        if today_breakout:
            if kbar_bearish:
                conclusion = f"今日突破前高 {prev_high}，但出現空頭K棒（{kbar_pattern}），留意假突破。觀察重點：明天能否守住 {prev_high}；失效位置 {stop_loss}"
            else:
                conclusion = f"今日放量突破前高 {prev_high}，突破型態成立。觀察重點：回測時是否守住 {prev_high}，守住則突破結構延續；失效位置 {stop_loss}，下一壓力參考 {resistance}"
        else:
            conclusion = f"股價突破壓力 {prev_high}。觀察重點：{'縮量回測是否守住突破位置；失效位置 ' + str(stop_loss) if not kbar_bearish else f'出現{kbar_pattern}，留意假突破；失效位置 {stop_loss}'}"
    elif pattern == "跌破型態":
        conclusion = f"股價跌破支撐 {support}，前支撐轉為壓力，原多方結構失效。觀察重點：{'跌勢是否止穩、能否重新站回 ' + str(support) if not kbar_bullish else f'出現{kbar_pattern}，觀察是否為假跌破、能否守回 {support}'}"
    else:
        if kbar_bullish:
            conclusion = f"位於軌道中段，出現多頭K棒（{kbar_pattern}）。觀察重點：{kbar_action or f'能否突破壓力 {resistance}；失效位置 {stop_loss}'}"
        elif kbar_bearish:
            conclusion = f"位於軌道中段，出現空頭K棒（{kbar_pattern}）。觀察重點：{kbar_action or f'是否回落至支撐 {support} 附近及能否止跌'}"
        else:
            conclusion = f"位於軌道中段，方向未明。觀察重點：收盤突破 {resistance} 或跌破 {support} 的方向；失效位置 {stop_loss}"

    # 移除舊的 warning，改用整合結論
    warning = conclusion

    # ── 出場保護補句（帥哥鴻定案：並列呈現、不覆蓋買賣結論，交回使用者隔天盤中執行）──
    # 優先序：量價出場警訊（最急迫）＞ 葛蘭碧賣點（次要，且與量價警訊去重）
    _exit_notes = []
    if vp_exit_warn:
        # 隔天盤前行動指令：不是「今天出現→立刻減碼」（已收盤來不及），
        # 而是「今日收盤確認賣壓型態→明日守不住觀察價就在收盤前減碼一半」
        _exit_notes.append(
            f"⚠️ 轉弱訊號：今日收盤出現「{vp_exit_warn['shape']}」＋爆量（{vp_exit_warn['vol_x']}倍近月均量），"
            f"屬賣壓警訊。明日觀察：若無法收復今日 K 棒中值 {vp_exit_warn['watch']} 附近，轉弱訊號加重；"
            f"跌破 {stop_loss} 代表目前型態失效。"
        )
    # 葛蘭碧賣點：只有在「量價警訊沒觸發」時才補（避免對同一根賣壓 K 棒重複講）
    if gann_sell and not vp_exit_warn:
        _sell_ma   = gann_sell["ma"]
        _sell_val  = gann_sell["val"]
        _sell_type = gann_sell["type"]
        if gann_sell.get("is_deviate"):
            # 賣8 乖離過大：短線過熱、獲利了結提示（非趨勢反轉，措辭用「留意回吐、可減碼」）
            _exit_notes.append(
                f"⚠️ 過熱提醒：{_sell_type}，股價短線急漲、正乖離 {_sell_ma}（{_sell_val}）過大，"
                f"短線回檔風險增加，明日若開高走低代表賣壓出現。"
            )
        else:
            # 賣5/6/7：均線弱勢訊號
            _exit_notes.append(
                f"⚠️ 轉弱提醒：{_sell_type}（{_sell_ma}={_sell_val}）。"
                f"明日若持續無法站回 {_sell_ma}，代表均線壓力有效；跌破 {stop_loss} 代表目前型態失效。"
            )
    if _exit_notes:
        warning = conclusion + "\n" + "\n".join(_exit_notes)

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
    # 2026/09/17：深度分析的K棒卡片原本用另一套分類（_classify_kbar_simple），常常跟主結論的
    # K棒型態（detect_kbar_pattern）說法相反（例：主結論「空頭吞噬」、卡片「小黑棒」）。
    # 有偵測到明確型態時，卡片一律改用同一份型態結果；連K天數、量能註記仍沿用原本的計算。
    if kbar_pattern:
        kbar_simple["type"] = kbar_pattern.split("、")[0]
        kbar_simple["direction"] = kbar_dir if kbar_dir in ("bullish", "bearish") else "neutral"
        kbar_simple["meaning"] = "；".join(kbar_pattern.split("、")[1:]) or (kbar_warning or kbar_simple.get("meaning", ""))
    ma_alignment = _ma_alignment_desc(ma_values)
    kd_status    = _kd_status_desc(k_arr, d_arr)
    macd_status  = _macd_status_desc(macd_line, macd_sig, macd_hist)
    vol_analysis = _vol_analysis_desc(volumes, closes, opens)
    institutional = _fetch_institutional_safe(stock_id)
    risk_factors  = _individualized_risk(
        price, support, resistance, rr_ratio,
        kd_status, macd_status, kbar_simple, institutional
    )

    # ── 歷史回測：過去同型態出現時的漲跌統計 ──
    _kbar_backtest = None
    if kbar_pattern and len(closes) > 60:
        _bt_key = None
        for _bk in ["一字線","錘頭","射擊之星","多頭吞噬","空頭吞噬","早晨之星","黃昏之星",
                     "三紅兵","三烏鴉","穿刺線","烏雲蓋頂","大紅棒","大黑棒","長上影黑K","長下影紅K"]:
            if _bk in kbar_pattern:
                _bt_key = _bk
                break
        if _bt_key:
            _bt_ups, _bt_downs, _bt_total = 0, 0, 0
            for _bi in range(3, min(len(closes) - 3, 200)):
                _seg_o = opens[:len(opens)-_bi]
                _seg_h = highs[:len(highs)-_bi]
                _seg_l = lows[:len(lows)-_bi]
                _seg_c = closes[:len(closes)-_bi]
                if len(_seg_c) < 5:
                    break
                _p_str, _, _, _ = detect_kbar_pattern(_seg_o, _seg_h, _seg_l, _seg_c)
                if _bt_key in _p_str:
                    _next_idx = len(closes) - _bi
                    if _next_idx < len(closes):
                        if closes[_next_idx] > closes[_next_idx - 1]:
                            _bt_ups += 1
                        else:
                            _bt_downs += 1
                        _bt_total += 1
                    if _bt_total >= 5:
                        break
            if _bt_total >= 2:
                _kbar_backtest = {
                    "pattern": _bt_key, "total": _bt_total,
                    "ups": _bt_ups, "downs": _bt_downs,
                    "win_pct": round(_bt_ups / _bt_total * 100) if _bt_total > 0 else 50,
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

    # 2026/09/17：現價日期。拿到即時報價時，是「最近一個已開盤的交易日」（平日09:00後＝今天）
    _display_price_date = price_basis_date
    if _live_quote_ok:
        try:
            _nw = datetime.now(ZoneInfo("Asia/Taipei"))
            _display_price_date = (_nw.strftime("%Y-%m-%d") if (_nw.weekday() < 5 and _nw.hour >= 9)
                                   else _expected_latest_trading_date(_nw))
            if _display_price_date < price_basis_date:
                _display_price_date = price_basis_date
        except Exception:
            pass

    # 做法A：分析基準與顯示現價的落差說明（給前端顯示，白話告知使用者）
    _basis_gap = None
    if display_price and analysis_price and analysis_price > 0:
        _gap_pct = round((display_price - analysis_price) / analysis_price * 100, 2)
        if abs(_gap_pct) >= 0.01:
            _basis_gap = _gap_pct
    _basis_md = price_basis_date[5:].replace("-", "/") if price_basis_date and len(price_basis_date) >= 10 else price_basis_date
    # 2026/09/15修正：帥哥鴻回報「個股分析明顯是用當下做分析,這跟盤後分析不同步,但也沒有看到警語」。
    # 查證後發現：fetch_df_finmind()的「盤中補今日K棒」機制（給K線圖顯示用）會把今天即時報價
    # 補進資料序列最後一筆，導致_do_analyze()裡price_basis_date=df.index[-1]在盤中就可能等於
    # 「今天」——這時原本掉進最下面的else分支，會講出「本分析以09/15收盤價為基準計算」這種
    # 話，今天根本還沒收盤，用詞是錯的。這裡先不動資料來源（那要拆分析基準跟K線圖的資料流，
    # 影響面大，帥哥鴻裁示先加警語就好），只在文案這層攔截這個情境，講清楚「這是盤中即時資料，
    # 不是正式收盤價」，不要讓使用者誤以為分析是用已經收盤定案的數字做的。
    _today_str = _taipei_today()
    if _data_stale:
        # 2026/08/14 新增：資料源明顯落後（連上一個交易日的資料都還沒有），
        # 不管盤中盤後都優先顯示這個提示，蓋過下面兩種正常情境的說明。
        _price_basis_note = (
            f"⚠️ 資料來源可能尚未更新，目前顯示的是 {_basis_md} 的收盤資料，"
            f"與預期的最近交易日有落差（也可能剛好遇到休市日）。如有疑慮，建議稍後再重新查看。"
        )
    elif _is_trading_session() and price_basis_date == _today_str:
        _price_basis_note = "⏱️ 現在是盤中，以下分析（支撐、壓力、失效位置、損益比）用的是今天即時資料試算，還不是正式收盤價，收盤後數字可能會再變動，僅供參考。"
    elif _is_trading_session() and _live_quote_ok and _basis_gap is not None:
        _price_basis_note = f"上方現價為即時參考；以下分析（支撐、壓力、失效位置、損益比）以 {_basis_md} 收盤價為基準計算，兩者盤中可能有落差，屬正常。"
    elif _live_quote_ok and _display_price_date > price_basis_date and _basis_gap is not None:
        # 2026/09/17：收盤後官方資料還沒更新的空窗，現價已是新的一天、分析仍是前一天
        _price_basis_note = (
            f"最新收盤資料還在更新中：以下分析（支撐、壓力、失效位置、損益比）仍以 {_basis_md} 收盤價為基準，"
            f"上方現價是 {_display_price_date[5:].replace('-', '/')} 的價格，兩者有落差。約10分鐘後重新查詢會自動更新。"
        )
    else:
        _price_basis_note = f"本分析以 {_basis_md} 收盤價為基準計算。"

    result = {
        "symbol": symbol, "stock_id": stock_id, "stock_name": stock_name, "tf": tf,
        "price": price,
        "price_change_pct": price_change_pct,  # 現價漲跌%（近兩根收盤價計算，不依賴即時報價）
        "analysis_price": analysis_price,      # 做法A：分析基準（確定收盤），下游分析欄位皆用此
        "display_price": display_price,        # 做法A：畫面現價（盤中即時，抓不到＝收盤基準）
        "display_price_date": _display_price_date,  # 2026/09/17：畫面現價是哪一天的價格
        "price_basis_date": price_basis_date,  # 做法A：分析基準是哪一天的收盤
        "price_basis_note": _price_basis_note, # 做法A：白話說明（給使用者看，第10點）
        "data_stale": _data_stale,             # 2026/08/14新增：資料源是否明顯落後（供前端另外標示用）
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
        "gann_sell": gann_sell,
        "vp_exit_warn": vp_exit_warn,
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
        "kbar_backtest": _kbar_backtest,
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

        # 雷達一：趨勢 — 2026/08/06 改用道氏波峰波谷（與上方主欄位 trend 同一套判斷）
        # 原本獨立算 MA20>MA60，跟主欄位的道氏趨勢是兩套邏輯，會出現「上升趨勢」但
        # 雷達顯示「月線<季線❌」互相矛盾的畫面；回測已證實道氏鑑別力優於MA20/MA60
        # （backtest_trend.py，+1.38% vs -0.05%），直接沿用同一份 trend 判斷結果，
        # 不再另外計算，兩處保證永遠一致。
        _tp_trend = bool(trend == "上升趨勢")

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
        _tp_vol   = bool(float(_vol_r) >= 1.3)

        # T1: 雷達四：位置 — MA5 乖離 -3%~+3%（剛站上均線，未過熱）
        _bias5  = round((price - float(_ma5_v))  / float(_ma5_v)  * 100, 2) if _ma5_v  and float(_ma5_v)  > 0 else None
        _bias20 = round((price - float(_ma20_v)) / float(_ma20_v) * 100, 2) if _ma20_v and float(_ma20_v) > 0 else None
        _tp_position = bool(_bias5 is not None and -3.0 <= _bias5 <= 3.0)

        _tp_score = int(bool(_tp_trend)) + int(bool(_tp_macd)) + int(bool(_tp_vol)) + int(bool(_tp_position))
        _tp_label = {4: "雷達全亮🔥", 3: "差一格⚡", 2: "訊號弱👀", 1: "雷達靜默", 0: "雷達靜默"}.get(_tp_score, "")

        # 進場訊號：雷達四格全亮
        _bias_entry = bool(_tp_score == 4)

        # T7: 出場訊號（加入 MA5 跌破 MA20）
        _ma5_cross_below_ma20 = False
        if _ma5_v and _ma20_v and float(_ma5_v) < float(_ma20_v):
            # 確認前一天 MA5 還在 MA20 上方（今天剛跌破）
            _ma5_full = calc_ma(closes, 5)
            _ma20_full = calc_ma(closes, 20)
            if len(_ma5_full) >= 2 and len(_ma20_full) >= 2:
                _prev_ma5 = _ma5_full[-2] if not np.isnan(_ma5_full[-2]) else None
                _prev_ma20 = _ma20_full[-2] if not np.isnan(_ma20_full[-2]) else None
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

    # ── kbar_action 結合雷達+量能上下文（雷達算完後才能做）──
    _radar = result.get("radar") or {}
    _r_score = _radar.get("score", 0)
    _r_vol_r = _radar.get("vol_ratio", 1.0)
    if kbar_action:
        kbar_bullish_check = any(k in kbar_pattern for k in ["錘頭","多頭吞噬","早晨之星","三紅兵","穿刺線","大紅棒","長下影紅K"]) if kbar_pattern else False
        kbar_bearish_check = any(k in kbar_pattern for k in ["射擊之星","空頭吞噬","黃昏之星","三烏鴉","烏雲蓋頂","大黑棒","長上影黑K"]) if kbar_pattern else False
        # 雷達強度修飾
        if _r_score >= 3 and kbar_bullish_check:
            kbar_action += f"（雷達 {_r_score}/4 亮，訊號較可靠）"
        elif _r_score <= 1 and kbar_bullish_check:
            kbar_action += f"（但雷達僅 {_r_score}/4，力道待確認）"
        elif _r_score >= 3 and kbar_bearish_check:
            kbar_action += f"（雷達 {_r_score}/4 亮但K棒空頭，留意背離）"
        # 量能修飾
        if _r_vol_r >= 1.5:
            kbar_action += f"，量比 {_r_vol_r}x 放量確認"
        elif _r_vol_r < 0.8:
            kbar_action += f"，量比僅 {_r_vol_r}x 縮量，明日需量增確認"
        result["kbar_action"] = kbar_action

    # 明確告知：支撐／壓力／K棒型態／操作建議這整包分析，是以「最近一根完整收盤 K 棒」
    # 為基準計算的，不是逐筆即時運算。（做法A後 price_basis_note 已詳細說明基準日，
    # 此句保留作為 warning 內的簡短提示，與 price_basis_note 相輔。）
    # 2026/09/15修正：跟上面_price_basis_note同一個根因——盤中補今日K棒時，這句話會變成
    # 「用今天還沒收盤的資料」卻自稱「收盤資料」，用詞不實。這裡跟着判斷一次，措辭對齊。
    if _is_trading_session() and price_basis_date == _today_str:
        result["warning"] = (result.get("warning") or "") + "（本分析以今日盤中即時資料試算，非正式收盤價，僅供參考）"
    else:
        result["warning"] = (result.get("warning") or "") + "（本分析以最近收盤資料計算，盤中僅供參考）"

    # 做法A（2026/08/04）：分析基準已與即時報價脫鉤——即時報價抓不到，
    # 只代表「畫面現價」暫時等於收盤基準，分析（支撐/防守位/損益比/雷達）本身完全正確，
    # 不再有「分析建立在錯的價格基準上」的問題，因此不再需要縮短快取為 60 秒的補救。
    # 盤中即時價抓失敗時，只在畫面現價旁提示，分析照常快取。
    if _is_trading_session() and not _live_quote_ok:
        result["price_note"] = "現價更新中，暫以收盤價顯示（分析不受影響）"

    # ── 綜合解說（2026/09/17新增，文件B階段7模版版）──
    # 所有結論統一由 _build_verdict 產出：主結論、風險標籤、報告頁都讀這一份，
    # 不再各自判斷（原本主結論只看價格位置＋K棒、風險標籤只看離支撐壓力多遠，
    # 會出現「突破確立可持有」配「觀望」、深度選股高信心配「建議出場」這種互相打架的畫面）。
    try:
        _ms_res = None
        if tf.upper() == "D":
            _ms_dates = [d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)[:10] for d in df.index]
            _ms_res = _ms_evaluate(stock_id, _ms_dates, highs, lows, closes, volumes, _ms_ctx_cached())
        _vd = _build_verdict(result, _ms_res)
        result["verdict"] = _vd
        result["position_conclusion"] = conclusion   # 舊版「只看價格位置」的結論，保留給除錯對照，畫面不再顯示
        result["risk_level"] = _vd["risk_level"]
        result["risk_label"] = _vd["stance_label"]
        result["risk_color"] = {"low": "green", "medium": "amber", "high": "red"}.get(_vd["risk_level"], "gray")
        _basis_suffix = ("（本分析以今日盤中即時資料試算，非正式收盤價，僅供參考）"
                         if (_is_trading_session() and price_basis_date == _today_str)
                         else "（本分析以最近收盤資料計算，盤中僅供參考）")
        _w = f"{_vd['headline']}\n觀察重點：{_vd['action']}{_basis_suffix}"
        if _exit_notes:
            _w += "\n" + "\n".join(_exit_notes)
        result["warning"] = _w
        result["conflict_note_raw"] = result.get("conflict_note")
        result["conflict_note"] = ""   # 矛盾已併入解說，前端主結論不再另外插一條
    except Exception as _vde:
        print(f"[verdict] {stock_id} 綜合解說失敗（沿用舊結論）：{_vde}")
    _cache_set(_cache_key, result)

    # Wave1：扣次改在 HTTP handler 成功後，此處不扣
    return result


@app.get("/api/analyze/{stock_id}")
def analyze(stock_id: str, tf: str = "D",
            ma1: int = 5, ma2: int = 10, ma3: int = 20, ma4: int = 60, ma5: int = 120,
            request: Request = None,
            user: dict | None = Depends(get_current_user)):
    """API 端點：遊客 daily_credit 3、免費完整分析 5（與健檢共用）、付費無限"""
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
        if plan != "free" and user.get("expire_at") and user["expire_at"] < today and not _is_referral_active(user):
            raise HTTPException(status_code=403, detail="訂閱已到期，請續費後繼續使用")

    allowed, used, limit = _check_daily_credit(request, user)
    if not allowed:
        if user:
            return _quota_429(
                "today_limit",
                f"今日完整分析／健檢次數已用完（{limit} 次），升級即可無限使用",
                used, limit,
            )
        return _quota_429(
            "guest_limit",
            f"免費試用已達上限（{limit} 次），登入後完整分析與健檢共用每日額度",
            used, limit,
        )

    _inc_counter("analyze_count")

    if user:
        try:
            _complete_referral_if_pending(user["email"])
        except Exception as _ref_e:
            print(f"[REFERRAL] complete_referral_if_pending 失敗 {user['email']}：{_ref_e}")

    result = _do_analyze(stock_id, tf, ma1, ma2, ma3, ma4, ma5, user=user)
    if isinstance(result, dict):
        # 快取裡是完整版，這裡複製一份再依會員身分遮掉看不到的解說段落
        result = dict(result)
        result["verdict"] = _verdict_for_user(result.get("verdict"), user)
    _consume_daily_credit(request, user)
    _ok, used2, limit2 = _check_daily_credit(request, user)
    if isinstance(result, dict):
        result["credit"] = _credit_dict(used2, limit2)
    return result


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
        target = (datetime.now(ZoneInfo("Asia/Taipei")).date() - timedelta(days=days_back)).strftime("%Y-%m-%d")
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
        # 修正（2026/08/03）：只有latest真的是「今天」時，y才代表「昨收」，用prev。
        # 若latest不是今天（FinMind當日資料尚未發布），y應直接顯示「目前可取得的最新一筆」
        # （也就是latest本身），不能再往前退一天用prev，否則會多顯示一天前的舊資料。
        y = (_sf(prev.get("close")) if prev else _sf(latest.get("close"))) if is_today \
            else _sf(latest.get("close"))

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

    # 防呆：代號含非 ASCII（例如誤存成中文股名）時，三個外部 API 的網址都會組不出來，
    # 造成 'ascii' codec can't encode 例外並重複刷 log。這裡直接短路，不再對外呼叫。
    try:
        code.encode("ascii")
    except UnicodeEncodeError:
        _safe_print(f"[QUOTE] 代號含非 ASCII 字元，略過外部查詢：{code}")
        return {
            "stock_id": code, "price": None, "change": None, "change_pct": None,
            "open": None, "high": None, "low": None, "volume": None,
            "in_session": _is_trading_session(), "price_source": "invalid_code",
            "price_note": "股票代號格式錯誤",
        }

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
    # 2026/08/14 修正：原本直接靜默回傳舊快取，畫面上完全看不出這是舊資料。
    # 現在附上明確提示，不覆蓋原本快取內容本身（複製一份修改，避免污染 _QUOTE_CACHE）。
    if price_val is None and code in _QUOTE_CACHE:
        _stale_cached = dict(_QUOTE_CACHE[code]["data"])
        _stale_cached["price_note"] = "即時報價來源暫時無法取得，目前顯示為先前快取資料"
        return _stale_cached

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


def _get_live_quote_data(code: str) -> dict | None:
    """統一的『查快取→過期就補抓一次get_quote()→回傳報價資料或None』邏輯。
    2026/07/30：取代main.py內原本8處幾乎相同的重複程式碼（get_quote()呼叫方各自複製貼上
    「查快取/重抓/例外處理」），邏輯本身不變，只是集中維護、行為統一，之後同一種bug只需修一處。
    回傳 _QUOTE_CACHE 裡的 data dict（含price/change/change_pct/open/high/low/volume...），
    沒有拿到有效報價（price）時回傳 None。"""
    code = code.strip().upper()
    _qc = _QUOTE_CACHE.get(code)
    if not _qc or _qc.get("expires", 0) < _time_mod.time():
        try:
            get_quote(code, user=None)
            _qc = _QUOTE_CACHE.get(code)
        except Exception:
            _qc = None
    if _qc and _qc.get("data", {}).get("price"):
        return _qc["data"]
    return None


# ══════════════════════════════════════════════════════════
# 江波圖（盤中走勢小線圖）＋現價＋漲跌%　2026/09/17
# 方案A：Yahoo 5 分鐘資料畫線，現價用 TWSE MIS 即時價補最後一點
# 方案B：Yahoo 連不到時，改用本站每 5 分鐘自己記錄的價格（intraday_ticks）
# ══════════════════════════════════════════════════════════
_INTRADAY_CACHE: dict = {}      # code -> (ts, data)
_INTRADAY_WANTED: dict = {}     # code -> 最近一次被請求的時間（方案B排程只記錄這些股票）
_MIS_BATCH_CACHE: dict = {}     # code -> (ts, quote)
_YAHOO_INTRA_STATE = {"fails": 0, "until": 0.0}
_INTRADAY_MAX_IDS = 60


def _tw_now():
    from zoneinfo import ZoneInfo as _ZIi
    return datetime.now(_ZIi("Asia/Taipei"))


def _intraday_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("""CREATE TABLE IF NOT EXISTS intraday_ticks (
        code TEXT, d TEXT, hm TEXT, price REAL, prev REAL,
        PRIMARY KEY (code, d, hm))""")
    return conn


def _intraday_record(quotes: dict):
    """把盤中即時價記到 intraday_ticks（以 5 分鐘為一格），給方案B用"""
    now = _tw_now()
    if now.weekday() >= 5:
        return
    hm_i = now.hour * 100 + now.minute
    if hm_i < 900 or hm_i > 1335:
        return
    today = now.strftime("%Y-%m-%d")
    slot = min(now.hour * 60 + now.minute, 13 * 60 + 30)
    slot -= slot % 5
    hm = f"{slot // 60:02d}:{slot % 60:02d}"
    rows = [(c, today, hm, q["price"], q.get("y")) for c, q in quotes.items()
            if q.get("price") and q.get("date") == today]
    if not rows:
        return
    try:
        with _intraday_db() as conn:
            conn.executemany("INSERT OR REPLACE INTO intraday_ticks (code,d,hm,price,prev) VALUES (?,?,?,?,?)", rows)
    except Exception as e:
        print(f"[INTRADAY] 記錄失敗：{e}")


def _mis_batch_quotes(codes) -> dict:
    """一次向 TWSE MIS 取多檔即時價；回傳 {code: {price, y, date}}（20 秒快取）"""
    import urllib.request as _ur, json as _json, time as _t
    now_ts = _t.time()
    out, need = {}, []
    for c in codes:
        hit = _MIS_BATCH_CACHE.get(c)
        if hit and now_ts - hit[0] < 20:
            out[c] = hit[1]
        else:
            need.append(c)

    def _f(v):
        try:
            x = float(str(v).strip())
            return x if x > 0 else None
        except Exception:
            return None

    def _first(raw):
        for p in str(raw or "").split("_"):
            x = _f(p)
            if x:
                return x
        return None

    fresh = {}
    for i in range(0, len(need), 20):
        chunk = need[i:i + 20]
        ex_ch = "|".join(f"tse_{c}.tw|otc_{c}.tw" for c in chunk)
        try:
            req = _ur.Request(
                f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={ex_ch}&json=1&delay=0",
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                         "Referer": "https://mis.twse.com.tw/stock/index.jsp",
                         "Accept": "application/json"})
            with _ur.urlopen(req, timeout=8, context=_TWSE_SSL_CTX) as resp:
                arr = _json.loads(resp.read()).get("msgArray", []) or []
        except Exception as e:
            print(f"[INTRADAY] MIS 批次失敗：{e}")
            continue
        for it in arr:
            c = str(it.get("c", "")).strip().upper()
            y = _f(it.get("y"))
            if not c or not y:
                continue
            price = _f(it.get("z"))
            if not price:
                b1, a1 = _first(it.get("b")), _first(it.get("a"))
                price = round((b1 + a1) / 2, 2) if (b1 and a1) else None
            d = str(it.get("d", ""))
            d = f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 else ""
            _vol = _f(it.get("v"))
            q = {"price": price, "y": y, "date": d, "name": str(it.get("n", "")).strip(),
                 "open": _f(it.get("o")), "high": _f(it.get("h")), "low": _f(it.get("l")),
                 "volume": int(_vol * 1000) if _vol else 0,
                 "close_final": bool(_f(it.get("z")))}
            if c not in fresh or (price and not fresh[c].get("price")):
                fresh[c] = q
    for c, q in fresh.items():
        _MIS_BATCH_CACHE[c] = (now_ts, q)
        out[c] = q
    if fresh:
        _intraday_record(fresh)
    return out


def _yahoo_intraday(code: str):
    """Yahoo 5 分鐘資料 → {date, prev_close, points:[[hm, price],...]}；失敗回 None"""
    import urllib.request as _ur, json as _j, time as _t
    from datetime import timedelta as _td
    if _t.time() < _YAHOO_INTRA_STATE["until"]:
        return None
    sfxs = [".TWO", ".TW"] if _market_cache.get(code, "") in ("otc", "rotc") else [".TW", ".TWO"]
    for sfx in sfxs:
        try:
            req = _ur.Request(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{code}{sfx}?range=5d&interval=5m",
                headers={"User-Agent": "Mozilla/5.0"})
            with _ur.urlopen(req, timeout=6) as resp:
                j = _j.loads(resp.read())
        except Exception as e:
            if "404" in str(e):
                continue
            _YAHOO_INTRA_STATE["fails"] += 1
            if _YAHOO_INTRA_STATE["fails"] >= 5:
                _YAHOO_INTRA_STATE["until"] = _t.time() + 600
                _YAHOO_INTRA_STATE["fails"] = 0
                print(f"[INTRADAY] Yahoo 連續失敗，暫停 10 分鐘改用本站記錄（最後錯誤：{e}）")
            return None
        res = ((j.get("chart") or {}).get("result") or [None])[0]
        if not res or not res.get("timestamp"):
            continue
        _YAHOO_INTRA_STATE["fails"] = 0
        closes = ((res.get("indicators") or {}).get("quote") or [{}])[0].get("close") or []
        days: dict = {}
        for ts, c in zip(res["timestamp"], closes):
            if c is None:
                continue
            tw = datetime.utcfromtimestamp(ts) + _td(hours=8)
            hm = tw.strftime("%H:%M")
            if hm < "09:00" or hm > "13:30":
                continue
            days.setdefault(tw.strftime("%Y-%m-%d"), []).append([hm, round(float(c), 2)])
        if not days:
            continue
        ds = sorted(days)
        last = ds[-1]
        meta = res.get("meta") or {}
        if len(ds) >= 2:
            prev = days[ds[-2]][-1][1]
        else:
            prev = meta.get("previousClose") or meta.get("chartPreviousClose")
        pts = days[last]
        # 收盤後 Yahoo 最後一格可能不是收盤價，用 regularMarketPrice 校正
        rmp = meta.get("regularMarketPrice")
        rmt = meta.get("regularMarketTime")
        if rmp and rmt and (datetime.utcfromtimestamp(rmt) + _td(hours=8)).strftime("%Y-%m-%d") == last:
            pts[-1][1] = round(float(rmp), 2)
        return {"date": last, "prev_close": round(float(prev), 2) if prev else None, "points": pts}
    return None


def _snapshot_intraday(code: str, date: str | None = None):
    """方案B：從本站記錄讀出走勢（date 為 None 時取最近一天）"""
    try:
        with _intraday_db() as conn:
            if not date:
                r = conn.execute("SELECT MAX(d) FROM intraday_ticks WHERE code=?", (code,)).fetchone()
                date = r[0] if r else None
                if not date:
                    return None
            rows = conn.execute("SELECT hm, price, prev FROM intraday_ticks WHERE code=? AND d=? ORDER BY hm",
                                (code, date)).fetchall()
    except Exception:
        return None
    if not rows:
        return None
    prev = next((r[2] for r in reversed(rows) if r[2]), None)
    return {"date": date, "prev_close": prev, "points": [[r[0], r[1]] for r in rows]}


def _intraday_one(code: str, mis: dict | None) -> dict:
    now = _tw_now()
    today = now.strftime("%Y-%m-%d")
    hm_now = now.strftime("%H:%M")
    live_day = now.weekday() < 5 and hm_now >= "09:00"
    src = "yahoo"
    base = _yahoo_intraday(code)
    mis_today = bool(mis and mis.get("date") == today and mis.get("price") and live_day)
    if mis_today and (not base or base["date"] != today):
        snap = _snapshot_intraday(code, today)
        if snap:
            base, src = snap, "snapshot"
        elif not base or base["date"] < today:
            base, src = {"date": today, "prev_close": None, "points": []}, "live"
    if not base:
        base = _snapshot_intraday(code)
        src = "snapshot" if base else "none"
    if not base:
        base = {"date": (mis or {}).get("date") or "", "prev_close": None, "points": []}
    pts = [list(p) for p in base["points"]]
    prev = base.get("prev_close")
    if mis_today and base["date"] == today:
        prev = mis.get("y") or prev
        hm = min(hm_now, "13:30")
        if pts and pts[-1][0] >= hm:
            pts[-1][1] = mis["price"]
        else:
            pts.append([hm, mis["price"]])
    elif mis and not prev and mis.get("date") == base["date"]:
        prev = mis.get("y")
    price = pts[-1][1] if pts else ((mis or {}).get("price") or (mis or {}).get("y"))
    chg = pct = None
    if price and prev:
        chg = round(price - prev, 2)
        pct = round(chg / prev * 100, 2)
    return {
        "code": code,
        "name": _name_cache.get(code) or (mis or {}).get("name") or "",
        "price": price, "prev_close": prev, "change": chg, "change_pct": pct,
        "date": base["date"], "points": pts, "source": src,
        "live": bool(mis_today and _is_trading_session()),
    }


@app.get("/api/intraday")
def api_intraday(ids: str = ""):
    """江波圖批次：/api/intraday?ids=2330,2317 → {ok, data:{code:{price,change_pct,points,...}}}"""
    import re as _re, time as _t
    from concurrent.futures import ThreadPoolExecutor as _TPE
    codes = []
    for c in ids.split(","):
        c = c.strip().upper().replace(".TWO", "").replace(".TW", "")
        if c and _re.fullmatch(r"[0-9A-Z]{4,6}", c) and c not in codes:
            codes.append(c)
    codes = codes[:_INTRADAY_MAX_IDS]
    now_ts = _t.time()
    in_sess = _is_trading_session()
    ttl = 60 if in_sess else 900
    out, need = {}, []
    for c in codes:
        _INTRADAY_WANTED[c] = now_ts
        hit = _INTRADAY_CACHE.get(c)
        if hit and now_ts - hit[0] < ttl:
            out[c] = hit[1]
        else:
            need.append(c)
    if need:
        mis = _mis_batch_quotes(need)
        with _TPE(max_workers=8) as ex:
            for d in ex.map(lambda c: _intraday_one(c, mis.get(c)), need):
                if d.get("price"):
                    _INTRADAY_CACHE[d["code"]] = (now_ts, d)
                out[d["code"]] = d
    if len(_INTRADAY_WANTED) > 3000:
        for k, v in sorted(_INTRADAY_WANTED.items(), key=lambda x: x[1])[:1000]:
            _INTRADAY_WANTED.pop(k, None)
    return JSONResponse({"ok": True, "data": out}, headers={"Cache-Control": "no-store"})


def _run_intraday_snapshot_job():
    """方案B：盤中每 5 分鐘，把最近 30 分鐘有人看的股票價格記下來"""
    import time as _t
    now = _tw_now()
    if now.weekday() >= 5:
        return
    hm = now.hour * 100 + now.minute
    if hm < 900 or hm > 1335:
        if 1400 <= hm < 1405:
            try:
                cut = (now - timedelta(days=10)).strftime("%Y-%m-%d")
                with _intraday_db() as conn:
                    conn.execute("DELETE FROM intraday_ticks WHERE d < ?", (cut,))
            except Exception:
                pass
        return
    cutoff = _t.time() - 1800
    codes = [c for c, ts in sorted(_INTRADAY_WANTED.items(), key=lambda x: -x[1]) if ts >= cutoff][:300]
    if not codes:
        return
    for c in codes:
        _MIS_BATCH_CACHE.pop(c, None)
    _mis_batch_quotes(codes)


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

    # 1. 盤中：先從 get_quote 快取取（包含 TWSE MIS 原始資料，2026/07/30 改用共用函式）
    if in_sess:
        d = _get_live_quote_data(code)
        if d:
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
    """驗證管理者 key，需與環境變數 ADMIN_API_KEY 相符（未設定時一律拒絕）"""
    if not ADMIN_API_KEY or key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="無權限")

@app.get("/admin/backup-db")
def backup_db(key: str = ""):  # 2026/07/30：唯一保留query string的admin端點，見下方註解
    """下載 members.db 備份，key = 環境變數 ADMIN_API_KEY 的值
    2026/07/30：其餘12個admin端點皆已改用 X-Admin-Key header 傳遞金鑰，
    唯獨這個端點維持 query string，因為前端改用 fetch+blob 下載大型二進位檔案
    時在正式環境會出現 net::ERR_FAILED（推測是Zeabur反向代理層對fetch()串流
    大型檔案的處理跟直接瀏覽器導覽不同），優先確保備份功能穩定可用。"""
    from fastapi.responses import FileResponse
    _check_admin(key)
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=404, detail="資料庫不存在")
    from datetime import date
    filename = f"members_backup_{date.today().isoformat()}.db"
    return FileResponse(DB_PATH, media_type="application/octet-stream", filename=filename)


@app.get("/admin/members")
def admin_list_members(key: str = Header(default="", alias="X-Admin-Key")):
    """列出所有會員"""
    _check_admin(key)
    conn = _db_conn()
    rows = conn.execute(
        "SELECT id, email, plan, expire_at, created_at, last_login FROM members ORDER BY id DESC"
    ).fetchall()
    conn.close()
    today = _taipei_today()
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
def admin_grant(key: str = Header(default="", alias="X-Admin-Key"), email: str = "", plan: str = "monthly", days: int = 30):
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
            _render_email(
                title="恭喜！您的方案已開通",
                title_icon="🎉",
                body_html=(
                    f'<p style="color:#444;margin:0 0 12px;font-size:14px;line-height:1.7">親愛的會員您好，</p>'
                    f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                    f'您的付費方案已由管理員為您手動開通，即刻起可登入使用即時個股分析、深度選股、到價提醒等完整會員功能。</p>'
                    f'<table style="width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden">'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">方案</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{plan_label}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">到期日</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{new_expire}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px">帳號</td><td style="padding:10px 14px;font-weight:700;font-size:14px;text-align:right">{to}</td></tr>'
                    f'</table>'
                    f'{extra_html}'
                ),
                cta_text="立即登入使用",
                cta_url=f"{FRONTEND_URL}/stock",
                with_ad=True,
                card_bg="#f0fdf4", card_border="#86efac", title_color="#166534",
            )
        )

    conn = _db_conn()
    row = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()
    if row:
        # 2026/09/17修正：原本一律「今天+天數」，對已付費會員按「延長」反而會把到期日縮短
        # （例如到期日 2027-03-15 的人補 30 天變成 2026-10-17）。改成從現有到期日往後加。
        _today_g = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d")
        _cur_g = row["expire_at"] or ""
        if plan != "free" and row["plan"] != "free" and _cur_g > _today_g:
            new_expire = (datetime.fromisoformat(_cur_g) + timedelta(days=days)).strftime("%Y-%m-%d")
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
            f"""<div style="background:#fffbeb;border:1px solid #fcd34d;border-radius:8px;padding:16px;margin-top:16px">
              <p style="margin:0 0 6px;font-weight:700;color:#92400e">🔑 您的初始登入密碼</p>
              <p style="margin:0;font-size:18px;letter-spacing:2px;font-weight:700;color:#333">{password}</p>
              <p style="margin:8px 0 0;font-size:12px;color:#78350f">為了帳號安全，登入後請至「我的帳號」儘快修改為您自己的密碼。</p>
            </div>"""
        )
        return {"ok": True, "action": "created", "email": email, "password": password, "plan": plan, "expire_at": new_expire}


@app.get("/admin/member-billing")
def admin_member_billing(key: str = Header(default="", alias="X-Admin-Key"), email: str = ""):
    """2026/09/17：查會員目前方案／到期日／綁定訂單，以及這個 Email 付款成功過的定期定額訂單"""
    _check_admin(key)
    email = email.strip().lower()
    conn = _db_conn()
    m = conn.execute("SELECT id, email, plan, expire_at, merchant_trade_no FROM members WHERE email=?", (email,)).fetchone()
    if not m:
        conn.close()
        raise HTTPException(status_code=404, detail="找不到這個會員")
    trades = set()
    for r in conn.execute("SELECT merchant_trade_no FROM pending_orders WHERE email=? AND merchant_trade_no LIKE 'XYWR%'", (email,)):
        trades.add(r["merchant_trade_no"])
    try:
        for r in conn.execute("SELECT DISTINCT merchant_trade_no FROM ecpay_verify_log WHERE matched=1 AND params_json LIKE ?",
                              (f'%"CustomField1": "{email}"%',)):
            trades.add(r["merchant_trade_no"])
    except Exception:
        pass
    if m["merchant_trade_no"]:
        trades.add(m["merchant_trade_no"])
    orders = []
    for t in sorted(trades):
        paid = conn.execute("SELECT processed_at FROM processed_orders WHERE merchant_trade_no LIKE ? ORDER BY processed_at LIMIT 1",
                            (f"R_{t}_%",)).fetchone()
        if paid or t == m["merchant_trade_no"]:
            orders.append({"trade_no": t, "paid_at": paid["processed_at"] if paid else ""})
    conn.close()
    return {"email": m["email"], "plan": m["plan"], "expire_at": m["expire_at"],
            "merchant_trade_no": m["merchant_trade_no"], "orders": orders}


@app.post("/admin/set-expire")
def admin_set_expire(key: str = Header(default="", alias="X-Admin-Key"), email: str = "",
                     expire_at: str = "", plan: str = "", trade_no: str = ""):
    """2026/09/17：直接設定會員到期日（可同時改方案、綁定的定期訂單）。不寄信、不登出會員。
    用途例：客人重複付款，已在綠界後台退刷＋停用其中一筆後，把到期日調回正確日期。"""
    _check_admin(key)
    email = email.strip().lower()
    try:
        expire_at = datetime.strptime(expire_at.strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
    except Exception:
        raise HTTPException(status_code=400, detail="到期日格式錯誤")
    if plan and plan not in ("free", "monthly", "quarterly", "yearly"):
        raise HTTPException(status_code=400, detail="方案錯誤")
    conn = _db_conn()
    m = conn.execute("SELECT plan, expire_at, merchant_trade_no FROM members WHERE email=?", (email,)).fetchone()
    if not m:
        conn.close()
        raise HTTPException(status_code=404, detail="找不到這個會員")
    new_plan = plan or m["plan"]
    new_trade = m["merchant_trade_no"] if trade_no == "" else (None if trade_no == "-" else trade_no.strip())
    conn.execute("UPDATE members SET plan=?, expire_at=?, merchant_trade_no=? WHERE email=?",
                 (new_plan, expire_at, new_trade, email))
    conn.commit()
    conn.close()
    print(f"[管理員設定到期日] {email} {m['plan']}/{m['expire_at']}/{m['merchant_trade_no']} → {new_plan}/{expire_at}/{new_trade}")
    return {"ok": True, "email": email,
            "before": {"plan": m["plan"], "expire_at": m["expire_at"], "merchant_trade_no": m["merchant_trade_no"]},
            "after": {"plan": new_plan, "expire_at": expire_at, "merchant_trade_no": new_trade}}


@app.post("/admin/reset-password")
def admin_reset_password(key: str = Header(default="", alias="X-Admin-Key"), email: str = "", new_password: str = ""):
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
            _render_email(
                title="您的密碼已重設",
                title_icon="🔑",
                body_html=(
                    f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                    f'您的帳號密碼已由管理員重設，請使用以下新密碼登入：</p>'
                    f'<div style="background:#fffbeb;border:1px solid #fcd34d;border-radius:8px;padding:16px;text-align:center">'
                    f'<p style="margin:0 0 6px;font-size:12px;color:#92400e">新密碼</p>'
                    f'<p style="margin:0;font-size:20px;letter-spacing:2px;font-weight:700;color:#333">{new_pw}</p></div>'
                    f'<p style="color:#444;margin:16px 0 0;font-size:14px;line-height:1.7">'
                    f'為了您的帳號安全，登入後請儘快至「我的帳號」修改為您自己的密碼。'
                    f'若您並未申請重設密碼，請立即來信客服協助處理。</p>'
                ),
                cta_text="立即登入",
                cta_url=f"{FRONTEND_URL}/stock",
                with_ad=False,
                card_bg="#eff6ff", card_border="#bfdbfe", title_color="#1e40af",
            )
        )
    except Exception as _e:
        print(f"[admin_reset] 寄信失敗: {_e}")
    return {"ok": True, "email": email, "new_password": new_pw}


class _DeleteMemberReq(BaseModel):
    email: str = ""

@app.post("/admin/delete-member")
def admin_delete_member(req: _DeleteMemberReq, key: str = Header(default="", alias="X-Admin-Key")):
    """刪除會員帳號"""
    _check_admin(key)
    email = req.email.strip().lower()
    conn = _db_conn()
    conn.execute("DELETE FROM members WHERE email=?", (email,))
    conn.commit()
    conn.close()
    return {"ok": True, "deleted": email}

@app.post("/admin/clear-cache")
def admin_clear_cache(key: str = Header(default="", alias="X-Admin-Key")):
    """清除 _analyze_cache 和 _QUOTE_CACHE（強制下次查詢重新抓）"""
    _check_admin(key)
    n = len(_analyze_cache)
    _analyze_cache.clear()
    q = len(_QUOTE_CACHE)
    _QUOTE_CACHE.clear()
    return {"cleared": n + q, "message": f"快取已清除（分析 {n} 筆 + 報價 {q} 筆）"}


@app.get("/admin/cache-stats")
def admin_cache_stats(key: str = Header(default="", alias="X-Admin-Key")):
    """查看目前各全域快取的即時筆數，用來追蹤是否有快取無限增長（記憶體洩漏排查用）"""
    _check_admin(key)
    return {
        "_QUOTE_CACHE": len(_QUOTE_CACHE),
        "_analyze_cache": len(_analyze_cache),
        "_CHIPS_CACHE": len(_CHIPS_CACHE),
        "_market_cache": len(_market_cache),
        "_name_cache": len(_name_cache),
        "_stock_info_cache": len(_stock_info_cache),
    }


@app.get("/admin/run-opening-scan")
async def admin_run_opening_scan(key: str = Header(..., alias="X-Admin-Key")):
    _check_admin(key)
    try:
        import threading as _thr
        _thr.Thread(target=_run_opening_scan_job, daemon=True).start()
        return {"message": "開盤熱門股抓取完成"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════════════════════════
# 會員福利（2026/09/17，取代原本寫死的「早鳥批次升級」）
#  ① 批次發送：後台貼 Email 名單（或勾選免費會員）→ 開通／延長天數＋寄信
#  ② 兌換碼：後台自己設定代碼、方案、天數、名額、截止日 → 貼到 LINE 群，
#     會員登入後在「我的」頁輸入就自動開通，每個帳號每組代碼只能用一次
#  規則：已是有效付費會員 → 從原本到期日往後加天數（不改方案、不縮短）；
#        免費或已過期 → 開通指定方案，到期日＝今天＋天數
# ══════════════════════════════════════════════════════════
_BONUS_PLANS = {"monthly": "月費方案", "quarterly": "季費方案", "yearly": "年費方案"}
_PROMO_FAILS: dict = {}   # member_id -> [失敗時間...]（防亂猜代碼）


def _promo_db_init(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS promo_codes (
            code        TEXT PRIMARY KEY,
            title       TEXT DEFAULT '',
            plan        TEXT NOT NULL,
            days        INTEGER NOT NULL,
            max_uses    INTEGER DEFAULT 0,
            used_count  INTEGER DEFAULT 0,
            expire_date TEXT DEFAULT '',
            active      INTEGER DEFAULT 1,
            created_at  TEXT
        );
        CREATE TABLE IF NOT EXISTS promo_redemptions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            code        TEXT NOT NULL,
            member_id   INTEGER NOT NULL,
            email       TEXT,
            old_plan    TEXT,
            old_expire  TEXT,
            new_plan    TEXT,
            new_expire  TEXT,
            redeemed_at TEXT,
            UNIQUE(code, member_id)
        );
        CREATE TABLE IF NOT EXISTS bonus_grants (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            email       TEXT,
            title       TEXT,
            plan        TEXT,
            days        INTEGER,
            old_plan    TEXT,
            old_expire  TEXT,
            new_plan    TEXT,
            new_expire  TEXT,
            created_at  TEXT
        );
    """)


def _bonus_apply(conn, row, plan: str, days: int) -> dict:
    """在同一個 conn 裡幫會員加天數（不 commit、不登出），回傳前後狀態"""
    from datetime import timedelta as _td
    today = _taipei_today()
    old_plan, old_exp = row["plan"] or "free", row["expire_at"] or ""
    if old_plan != "free" and old_exp >= today:
        new_plan = old_plan
        new_exp = (datetime.fromisoformat(old_exp) + _td(days=days)).strftime("%Y-%m-%d")
        stacked = True
    else:
        new_plan = plan
        new_exp = (datetime.fromisoformat(today) + _td(days=days)).strftime("%Y-%m-%d")
        stacked = False
    conn.execute("UPDATE members SET plan=?, expire_at=? WHERE id=?", (new_plan, new_exp, row["id"]))
    return {"old_plan": old_plan, "old_expire": old_exp, "new_plan": new_plan,
            "new_expire": new_exp, "stacked": stacked}


def _send_bonus_email(email: str, title: str, days: int, r: dict):
    if not email or email.endswith("@line.softglow-ai.com"):
        return False
    title = title or "會員福利"
    # 2026/09/17：月／季／年費功能完全一樣，福利一律只講「付費功能＋天數」，避免會員誤會拿到年費
    plan_label = _BONUS_PLANS.get(r["new_plan"], r["new_plan"]) if r["stacked"] else "付費功能"
    how = (f"已在您原本的到期日（{r['old_expire']}）後面再加 {days} 天，方案維持不變。"
           if r["stacked"] else f"已為您開通 {days} 天的付費功能。")
    _send_email(email, f"【線上有位】🎁 {title}：{days} 天付費功能已開通",
        _render_email(
            title=f"恭喜！您獲得「{title}」",
            title_icon="🎁",
            body_html=(
                f'<p style="color:#444;margin:0 0 12px;font-size:14px;line-height:1.7">親愛的會員您好，</p>'
                f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                f'感謝您支持線上有位！{how}即刻起可使用即時個股分析、12金叉選股、到價提醒等完整會員功能。</p>'
                f'<table style="width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden">'
                f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">方案</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{plan_label}</td></tr>'
                f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">到期日</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{r["new_expire"]}</td></tr>'
                f'<tr><td style="padding:10px 14px;color:#888;font-size:13px">帳號</td><td style="padding:10px 14px;font-weight:700;font-size:14px;text-align:right">{email}</td></tr>'
                f'</table>'
            ),
            cta_text="立即登入使用",
            cta_url=f"{FRONTEND_URL}/stock",
            with_ad=True,
            card_bg="#f0fdf4", card_border="#86efac", title_color="#166534",
        )
    )
    return True


def _bonus_check(plan: str, days: int):
    if plan not in _BONUS_PLANS:
        raise HTTPException(status_code=400, detail="方案只能是月費／季費／年費")
    try:
        days = int(days)
    except Exception:
        raise HTTPException(status_code=400, detail="天數格式錯誤")
    if days < 1 or days > 366:
        raise HTTPException(status_code=400, detail="天數要在 1～366 之間")
    return days


class _BatchUpgradeReq(BaseModel):
    emails: list
    plan: str = "monthly"
    days: int = 30
    title: str = ""
    send_email: bool = True


@app.post("/admin/batch-upgrade")
def admin_batch_upgrade(req: _BatchUpgradeReq, key: str = Header(default="", alias="X-Admin-Key")):
    """批次發送會員福利（已付費會員疊加天數），可選擇是否寄通知信"""
    _check_admin(key)
    days = _bonus_check(req.plan, req.days)
    title = (req.title or "").strip()[:30] or "會員福利"
    emails, seen = [], set()
    for raw in req.emails or []:
        for e in _re.split(r"[\s,;，；、]+", str(raw)):
            e = e.strip().lower()
            if e and e not in seen:
                seen.add(e)
                emails.append(e)
    if not emails:
        raise HTTPException(status_code=400, detail="請至少填一個 Email")
    if len(emails) > 1000:
        raise HTTPException(status_code=400, detail="一次最多 1000 個 Email")
    results, to_mail = [], []
    conn = _db_conn()
    try:
        _promo_db_init(conn)
        now_s = _taipei_now_str()
        for email in emails:
            row = conn.execute("SELECT id, email, plan, expire_at FROM members WHERE email=?", (email,)).fetchone()
            if not row:
                results.append({"email": email, "ok": False, "reason": "帳號不存在（請對方先註冊）"})
                continue
            r = _bonus_apply(conn, row, req.plan, days)
            conn.execute(
                "INSERT INTO bonus_grants (email,title,plan,days,old_plan,old_expire,new_plan,new_expire,created_at) VALUES (?,?,?,?,?,?,?,?,?)",
                (email, title, req.plan, days, r["old_plan"], r["old_expire"], r["new_plan"], r["new_expire"], now_s))
            results.append({"email": email, "ok": True, "expire_at": r["new_expire"],
                            "plan": r["new_plan"], "stacked": r["stacked"], "email_sent": False})
            to_mail.append((len(results) - 1, email, r))
        conn.commit()
    finally:
        conn.close()
    if req.send_email:
        for idx, email, r in to_mail:
            try:
                results[idx]["email_sent"] = _send_bonus_email(email, title, days, r)
            except Exception:
                pass
    ok = [x for x in results if x.get("ok")]
    return {"ok": True, "total": len(emails), "success": len(ok),
            "stacked": sum(1 for x in ok if x.get("stacked")), "results": results}


class _PromoCreateReq(BaseModel):
    code: str = ""
    title: str = ""
    plan: str = "monthly"
    days: int = 7
    max_uses: int = 0
    expire_date: str = ""


@app.post("/admin/promo-codes")
def admin_promo_create(req: _PromoCreateReq, key: str = Header(default="", alias="X-Admin-Key")):
    """新增兌換碼（代碼留空自動產生）"""
    _check_admin(key)
    days = _bonus_check(req.plan, req.days)
    code = (req.code or "").strip().upper()
    if code and not _re.fullmatch(r"[A-Z0-9]{4,20}", code):
        raise HTTPException(status_code=400, detail="代碼只能用英文字母和數字，4～20 碼")
    if not code:
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        code = "".join(secrets.choice(alphabet) for _ in range(8))
    exp = (req.expire_date or "").strip()
    if exp:
        try:
            exp = datetime.fromisoformat(exp).strftime("%Y-%m-%d")
        except Exception:
            raise HTTPException(status_code=400, detail="截止日格式錯誤")
    max_uses = max(0, int(req.max_uses or 0))
    title = (req.title or "").strip()[:30]
    conn = _db_conn()
    try:
        _promo_db_init(conn)
        if conn.execute("SELECT 1 FROM promo_codes WHERE code=?", (code,)).fetchone():
            raise HTTPException(status_code=409, detail=f"代碼 {code} 已經存在")
        conn.execute(
            "INSERT INTO promo_codes (code,title,plan,days,max_uses,used_count,expire_date,active,created_at) VALUES (?,?,?,?,?,0,?,1,?)",
            (code, title, req.plan, days, max_uses, exp, _taipei_now_str()))
        conn.commit()
    finally:
        conn.close()
    return {"ok": True, "code": code, "link": f"{FRONTEND_URL}/stock/?promo={code}"}


@app.get("/admin/promo-codes")
def admin_promo_list(key: str = Header(default="", alias="X-Admin-Key")):
    _check_admin(key)
    conn = _db_conn()
    try:
        _promo_db_init(conn)
        rows = [dict(r) for r in conn.execute("SELECT * FROM promo_codes ORDER BY created_at DESC")]
    finally:
        conn.close()
    today = _taipei_today()
    for r in rows:
        r["link"] = f"{FRONTEND_URL}/stock/?promo={r['code']}"
        if not r["active"]:
            r["status"] = "已停用"
        elif r["expire_date"] and r["expire_date"] < today:
            r["status"] = "已過期"
        elif r["max_uses"] and r["used_count"] >= r["max_uses"]:
            r["status"] = "名額已滿"
        else:
            r["status"] = "可使用"
    return {"codes": rows}


class _PromoToggleReq(BaseModel):
    code: str
    active: bool


@app.post("/admin/promo-codes/toggle")
def admin_promo_toggle(req: _PromoToggleReq, key: str = Header(default="", alias="X-Admin-Key")):
    _check_admin(key)
    conn = _db_conn()
    try:
        _promo_db_init(conn)
        cur = conn.execute("UPDATE promo_codes SET active=? WHERE code=?", (1 if req.active else 0, req.code.strip().upper()))
        conn.commit()
    finally:
        conn.close()
    if not cur.rowcount:
        raise HTTPException(status_code=404, detail="找不到這個代碼")
    return {"ok": True}


@app.get("/admin/promo-codes/redemptions")
def admin_promo_redemptions(code: str, key: str = Header(default="", alias="X-Admin-Key")):
    _check_admin(key)
    conn = _db_conn()
    try:
        _promo_db_init(conn)
        rows = [dict(r) for r in conn.execute(
            "SELECT email, old_plan, old_expire, new_plan, new_expire, redeemed_at FROM promo_redemptions WHERE code=? ORDER BY id DESC",
            (code.strip().upper(),))]
    finally:
        conn.close()
    return {"code": code.strip().upper(), "items": rows}


class _PromoRedeemReq(BaseModel):
    code: str


@app.post("/api/promo/redeem")
def api_promo_redeem(req: _PromoRedeemReq, user: dict = Depends(require_user)):
    """會員輸入兌換碼領福利"""
    import time as _t
    mid = user["id"]
    now_ts = _t.time()
    fails = [x for x in _PROMO_FAILS.get(mid, []) if now_ts - x < 600]
    _PROMO_FAILS[mid] = fails
    if len(fails) >= 10:
        raise HTTPException(status_code=429, detail="輸入錯誤太多次，請 10 分鐘後再試")

    def _fail(msg, status=400):
        _PROMO_FAILS.setdefault(mid, []).append(now_ts)
        raise HTTPException(status_code=status, detail=msg)

    code = (req.code or "").strip().upper()
    if not _re.fullmatch(r"[A-Z0-9]{4,20}", code):
        _fail("兌換碼格式不正確")
    conn = _db_conn()
    try:
        _promo_db_init(conn)
        pc = conn.execute("SELECT * FROM promo_codes WHERE code=?", (code,)).fetchone()
        if not pc or not pc["active"]:
            _fail("找不到這個兌換碼，或活動已結束", 404)
        if pc["expire_date"] and pc["expire_date"] < _taipei_today():
            _fail("這個兌換碼已經過期了")
        if conn.execute("SELECT 1 FROM promo_redemptions WHERE code=? AND member_id=?", (code, mid)).fetchone():
            raise HTTPException(status_code=409, detail="您已經領過這個兌換碼的福利了")
        conn.execute("BEGIN IMMEDIATE")
        cur = conn.execute(
            "UPDATE promo_codes SET used_count=used_count+1 WHERE code=? AND active=1 AND (max_uses=0 OR used_count<max_uses)",
            (code,))
        if not cur.rowcount:
            conn.rollback()
            raise HTTPException(status_code=410, detail="這個兌換碼的名額已經領完了")
        row = conn.execute("SELECT id, email, plan, expire_at FROM members WHERE id=?", (mid,)).fetchone()
        r = _bonus_apply(conn, row, pc["plan"], int(pc["days"]))
        try:
            conn.execute(
                "INSERT INTO promo_redemptions (code,member_id,email,old_plan,old_expire,new_plan,new_expire,redeemed_at) VALUES (?,?,?,?,?,?,?,?)",
                (code, mid, row["email"], r["old_plan"], r["old_expire"], r["new_plan"], r["new_expire"], _taipei_now_str()))
        except sqlite3.IntegrityError:
            conn.rollback()
            raise HTTPException(status_code=409, detail="您已經領過這個兌換碼的福利了")
        conn.commit()
    finally:
        conn.close()
    plan_label = _BONUS_PLANS.get(r["new_plan"], r["new_plan"])
    days = int(pc["days"])
    msg = (f"已在原本到期日後加 {days} 天，新的到期日是 {r['new_expire']}"
           if r["stacked"] else f"已開通 {days} 天{plan_label}，到期日 {r['new_expire']}")
    print(f"[PROMO] {row['email']} 兌換 {code}：{r['old_plan']}/{r['old_expire']} → {r['new_plan']}/{r['new_expire']}")
    return {"ok": True, "title": pc["title"] or "會員福利", "days": days, "plan": r["new_plan"],
            "plan_label": plan_label, "expire_at": r["new_expire"], "stacked": r["stacked"], "message": msg}


_HOT_STOCKS = [
    "2330","2317","2454","2308","2412","6505","2882","2881","2886","2891",
    "2884","2892","2883","2885","2887","2888","2890","5880","2801","2002",
    "1301","1303","1326","2303","2357","2382","2395","3034","3037","3045",
    "4904","4938","5871","6415","6669","2610","2618","2615","2603","2609",
    "1216","2912","2207","1101","1102","3008","6488","6770","3661",
]


@app.post("/admin/prebuild-reports")
def admin_prebuild_reports(key: str = Header(default="", alias="X-Admin-Key")):
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
            # 2026/09/13 首頁IA-Home-3新增：今日異動%。優先用即時報價換算的change_pct
            # （盤中快取更新時寫入），沒有的話退回收盤價算出的price_change_pct
            # （近兩根收盤價比較），兩者都是真實計算值，不是另外造的假欄位。
            "change_pct":   d.get("change_pct") if d.get("change_pct") is not None else d.get("price_change_pct"),
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
        if data.get("status") == 200 and data.get("data"):
            _stock_info_cache = data.get("data", [])
            _stock_info_ts = time.time()
            return _stock_info_cache
        print(f"FinMind StockInfo 回應異常：status={data.get('status')} msg={data.get('msg','')}")
    except Exception as e:
        print(f"FinMind StockInfo 失敗：{e}")
    # 2026/09/17：FinMind 失敗且記憶體是空的 → 用資料庫備份（上次成功的清單）
    if not _stock_info_cache:
        try:
            with _name_cache_db() as conn:
                row = conn.execute("SELECT data FROM stock_info_backup WHERE id=1").fetchone()
            if row:
                _stock_info_cache = _json.loads(row[0])
                _stock_info_ts = time.time() - 86400 + 600   # 10分鐘後再試 FinMind
                print(f"FinMind StockInfo 改用資料庫備份（{len(_stock_info_cache)} 筆）")
        except Exception as e:
            print(f"StockInfo 備份讀取失敗：{e}")
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




def detect_kbar_pattern(opens, highs, lows, closes, volumes=None):
    """
    辨識最近 K 棒型態（單根/兩根/三根），含量能確認
    回傳：
      kbar_pattern: str  已確認的型態名稱（空字串=無）
      kbar_warning: str  預警文字（明天若...將形成...）
    """
    n = len(closes)
    if n < 3:
        return "", "", "neutral", 0.50

    o1,h1,l1,c1 = opens[-1],highs[-1],lows[-1],closes[-1]  # 最新根
    o2,h2,l2,c2 = opens[-2],highs[-2],lows[-2],closes[-2]  # 前一根
    o3,h3,l3,c3 = opens[-3],highs[-3],lows[-3],closes[-3]  # 前兩根

    # 量能確認（今日量 vs 前一日量）
    _vol_up = False   # 今日量 > 昨日量
    _vol_down = False # 今日量 < 昨日量 * 0.7
    if volumes is not None and len(volumes) >= 2:
        v1, v2 = float(volumes[-1]), float(volumes[-2])
        if v2 > 0:
            _vol_up = v1 > v2 * 1.1     # 量增 10% 以上
            _vol_down = v1 < v2 * 0.7    # 量縮 30% 以上

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

    # ── 跳空判斷（今日K棒範圍與昨日完全不重疊）──
    # 2026/08/06 新增：原本完全沒有跳空偵測，缺這塊資訊
    _gap_up = l1 > h2
    _gap_down = h1 < l2
    _gap_tag = "跳空" if (_gap_up or _gap_down) else ""

    # ── 單根型態（最新K棒）──

    # 一字線（漲跌停鎖死：開=高=低=收，全日幾乎零波動）
    # 2026/08/06 新增：原本完全沒有這個型態，數值特徵(body/range<0.1)跟十字星重疊，
    # 一直被誤判成十字星——但一字線代表極端一致的單邊情緒（搶著買或搶著賣到鎖死），
    # 跟十字星代表的「方向不明、多空拉鋸」意義完全相反，混在一起會誤導使用者。
    # 用 range/price 是否極小（而非 body/range 比例）當判斷依據，才能跟十字星區分開。
    if range1 / (c1 or 1) < 0.002:
        if c1 > c2 * 1.001:
            patterns.append(f"{_gap_tag}一字線（漲停鎖死，強勢惜售）")
            warnings.append("今日一字鎖死漲停，若明天開盤不跳空回補，多方強勢未變")
        elif c1 < c2 * 0.999:
            patterns.append(f"{_gap_tag}一字線（跌停鎖死，恐慌出逃）")
            warnings.append("今日一字鎖死跌停，若明天無法收復，空方強勢未變")
        else:
            patterns.append(f"{_gap_tag}一字線（平盤鎖死，極端惜售惜買）")
            warnings.append("今日一字線但接近平盤，方向不明，觀察明天開盤方向")

    # 錘頭（底部，下引線長，出現在下跌後）
    elif (lower_shadow1 >= body1 * 2 and upper_shadow1 <= body1 * 0.3
            and body1 / range1 < 0.4):
        if not is_red1:
            patterns.append(f"{_gap_tag}錘頭線（底部反轉訊號）")
            warnings.append("出現錘頭線，若明天收紅確認，底部支撐訊號成立")
        else:
            patterns.append(f"{_gap_tag}錘頭線（底部反轉，紅K更佳）")
            warnings.append("出現紅K錘頭線，底部支撐訊號，明天若繼續收紅則確認")

    # 流星/射擊之星（頂部，上引線長）
    elif (upper_shadow1 >= body1 * 2 and lower_shadow1 <= body1 * 0.3
            and body1 / range1 < 0.4):
        patterns.append(f"{_gap_tag}射擊之星（頂部壓力訊號）")
        warnings.append("出現射擊之星，若明天收黑確認，注意頂部形成風險")

    # 十字星（開收盤接近，但範圍正常，非鎖死一字線）
    elif body1 / range1 < 0.1 and range1 > 0:
        if h1 > max(h2, h3):  # 高點在頂部
            patterns.append(f"{_gap_tag}十字星（高點出現，方向未定）")
            warnings.append("高點出現十字星，方向未明，明天若收黑須注意拉回")
        else:
            patterns.append(f"{_gap_tag}十字星（整理，等待方向）")
            warnings.append("出現十字星，整理中，等待明天方向確認")

    # 長上影黑K（假突破，高檔賣壓）／長下影紅K（假跌破，低檔承接）
    # 2026/08/07 新增：帥哥鴻用 3231 緯創 2026/08/05 實際K棒（開198／高202.5／低190／收193）
    # 發現的真實偵測漏洞——body1/range1=0.40，不夠格是大黑棒(>0.7)，上下影線比例也不到
    # 錘頭/射擊之星要求的2倍，導致這種「衝高被拉回、收黑、帶明顯上影線」的關鍵反轉訊號
    # 完全沒被任何型態捕捉到，kbar_pattern留空，連帶vp_exit_warn（爆量出場警訊）也不會觸發
    # （因為它是靠kbar_pattern字串比對關鍵字才會啟動）。
    # 這裡補上 body1/range1 在 0.1~0.7 之間、但帶有明顯單邊影線（≥range1*0.3）的情況：
    elif not is_red1 and body1 / range1 <= 0.7 and upper_shadow1 >= range1 * 0.3:
        patterns.append(f"{_gap_tag}長上影黑K（假突破，高檔賣壓）")
        warnings.append("今日收黑且帶明顯上影線，疑似衝高遭壓回，若明天無法收復今日高點一半，賣壓恐延續")

    elif is_red1 and body1 / range1 <= 0.7 and lower_shadow1 >= range1 * 0.3:
        patterns.append(f"{_gap_tag}長下影紅K（假跌破，低檔承接）")
        warnings.append("今日收紅且帶明顯下影線，疑似殺低後獲得承接，若明天延續收紅，止跌訊號增強")

    # 大紅棒（強攻）— 2026/08/06 拿掉「body1 > body2*1.5」這個門檻：
    # body1/range1>0.7 本身已經是「實體佔全天振幅七成以上」的絕對強度判斷，足以定義
    # 大紅棒，不需要再跟昨天比較。原本「比昨天大1.5倍」會導致連續強勢（例如連續兩天
    # 都是大紅棒）時，第二天因為沒有比第一天更大而被漏判成常態K線，是明確的邏輯錯誤。
    elif is_red1 and body1 / range1 > 0.7:
        patterns.append(f"{_gap_tag}大紅棒（強勢攻擊）")
        warnings.append("出現大紅棒，若明天不跌破今日一半，多頭強勢延續")

    # 大黑棒（強殺）— 同上，拿掉「比昨天大1.5倍」的門檻
    elif not is_red1 and body1 / range1 > 0.7:
        patterns.append(f"{_gap_tag}大黑棒（強勢賣壓）")
        warnings.append("出現大黑棒，若明天無法收復今日一半，空頭延續")

    # ── 兩根型態 ──

    # 多頭吞噬（紅吞黑）
    if (is_red1 and not is_red2
            and o1 <= c2 and c1 >= o2
            and body1 > body2):
        _vol_tag = "，量增確認" if _vol_up else ("，量未配合" if _vol_down else "")
        patterns.append(f"多頭吞噬（底部反轉{_vol_tag}）")
        warnings.append("出現多頭吞噬，明天若繼續收紅，底部反轉確認")

    # 空頭吞噬（黑吞紅）
    elif (not is_red1 and is_red2
            and o1 >= c2 and c1 <= o2
            and body1 > body2):
        _vol_tag = "，量增確認" if _vol_up else ""
        patterns.append(f"空頭吞噬（頂部反轉{_vol_tag}）")
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
        warnings.append("出現黃昏之星，頂部反轉訊號，若明天繼續收黑則轉弱確認")

    # 三紅兵（強勢延續）
    elif (is_red1 and is_red2 and is_red3
            and c1 > c2 > c3
            and body1 > range1 * 0.5
            and body2 > range2 * 0.5
            and body3 > range3 * 0.5):
        patterns.append("三紅兵（強勢多頭延續）")
        warnings.append("出現三紅兵，多頭趨勢強，明天若再收紅趨勢持續，短線乖離擴大")

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
    bullish_keys = ["錘頭","多頭吞噬","早晨之星","三紅兵","穿刺線","大紅棒","頭肩底","W底","漲停","長下影紅K"]
    bearish_keys = ["射擊之星","空頭吞噬","黃昏之星","三烏鴉","烏雲蓋頂","大黑棒","頭肩頂","M頭","跌停","長上影黑K"]
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
        # 2026/08/07 新增：靜態預設值，屬保守估計（介於錘頭/射擊之星與穿刺線/烏雲蓋頂之間）；
        # 個股實際勝率仍以 _kbar_backtest（同股票歷史同型態統計）動態算出的結果為準，
        # 這裡只是資料不足時的靜態備援
        "長上影黑K": 0.54, "長下影紅K": 0.54,
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
def get_chips(stock_id: str, days: int = 30, user: dict | None = Depends(get_current_user)):
    """
    籌碼面：三大法人買賣超 + 融資融券
    回傳最近 N 天資料 + 統計摘要
    快取：24 小時（key = stock_id + 日期，隔天自動換 key 失效）
    """
    from datetime import date, timedelta
    code = stock_id.strip().replace(".TW", "").replace(".TWO", "")
    _today = _taipei_today().replace("-", "")
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
    if len(_CHIPS_CACHE) > 200:
        _cc_cutoff = _time_mod.time()
        _cc_expired = [k for k, v in _CHIPS_CACHE.items() if v["expires"] < _cc_cutoff]
        for _k in _cc_expired:
            _CHIPS_CACHE.pop(_k, None)
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


def _register_account(req: RegisterReq, ref: str, request: Request, success_message: str):
    """/auth/register 與 /register 共用邏輯：兩者行為完全相同（plan 欄位DB預設值即為'free'），
    只有回傳訊息文字不同，故合併為共用函式，2026/07/30 抽出。"""
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
    return {"ok": True, "message": success_message}


@app.post("/auth/register")
def auth_register(req: RegisterReq, ref: str = "", request: Request = None):
    return _register_account(req, ref, request, "註冊成功")


@app.post("/register")
def register_free(req: RegisterReq, ref: str = "", request: Request = None):
    return _register_account(req, ref, request, "免費帳號建立成功")


def _is_login_blocked(conn, email: str):
    """封鎖名單查詢，auth_login/auth_google共用，2026/07/30抽出，SQL與行為完全不變。"""
    return conn.execute(
        "SELECT email FROM blocked_users WHERE email=? AND block_type='login'", (email,)
    ).fetchone()


def _issue_login_session(conn, row, email: str):
    """建立session、簽發JWT、組回傳格式，auth_login/auth_google共用，2026/07/30抽出。
    呼叫前conn仍須是開啟狀態、row須已確認存在；本函式負責commit並close conn。"""
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


@app.post("/auth/login")
def auth_login(req: LoginReq):
    email = req.email.strip().lower()
    conn = _db_conn()
    row = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()
    if not row or not _verify_pw(req.password, row["password"]):
        conn.close()
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")
    if _is_login_blocked(conn, email):
        conn.close()
        raise HTTPException(status_code=403, detail="帳號已被停用，請聯絡客服")
    return _issue_login_session(conn, row, email)


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
    if _is_login_blocked(conn, email):
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

    return _issue_login_session(conn, row, email)


# ══════════════════════════════════════════════════════════
# LINE Login（2026/08/15 新增，供遊戲排行榜登入用）
#
# 跟Google登入的差別：Google用JS SDK在前端直接拿到id token、POST給後端驗證即可，
# 是「彈窗式」不用整頁跳轉；LINE Login走的是標準OAuth導向流程（沒有等同的JS SDK
# 彈窗方案），流程是：
#   1) 前端點「LINE登入」→ 導向 GET /auth/line（本站後端）
#   2) /auth/line 導向LINE的授權頁，使用者在LINE上同意授權
#   3) LINE導回 /auth/line/callback（帶code、state）
#   4) 後端用code換access_token，再用access_token查LINE個人資料（userId/displayName）
#   5) 用line_user_id找/建立會員、簽發JWT，最後導回原本頁面，網址帶著?line_token=xxx
#   6) 前端games-auth.js負責從網址讀出line_token、存進localStorage、洗掉網址參數
#
# 這一段程式碼即使LINE_CHANNEL_ID/LINE_CHANNEL_SECRET沒設定也不會讓網站壞掉
# （/auth/line會回503並說明原因），但要讓LINE登入真的能用，需要先去LINE
# Developers Console建立LINE Login channel、設定Callback URL為LINE_REDIRECT_URI，
# 並在Zeabur設定LINE_CHANNEL_ID/LINE_CHANNEL_SECRET這兩個環境變數。
# ══════════════════════════════════════════════════════════
@app.get("/auth/line")
async def auth_line_start(return_url: str = Query(default="/games/")):
    import urllib.parse as _urlparse
    if not LINE_CHANNEL_ID:
        raise HTTPException(status_code=503, detail="LINE登入尚未設定，請聯絡網站管理員")
    if not return_url.startswith("/"):
        return_url = "/games/"  # 防止open redirect：只允許導回本站的相對路徑
    state = secrets.token_urlsafe(16) + "|" + return_url
    params = {
        "response_type": "code",
        "client_id": LINE_CHANNEL_ID,
        "redirect_uri": LINE_REDIRECT_URI,
        "state": state,
        "scope": "profile openid",
    }
    from fastapi.responses import RedirectResponse
    url = "https://access.line.me/oauth2/v2.1/authorize?" + _urlparse.urlencode(params)
    return RedirectResponse(url)


@app.get("/auth/line/callback")
async def auth_line_callback(code: str = Query(default=""), state: str = Query(default=""), error: str = Query(default="")):
    import urllib.request, urllib.parse as _urlparse, json as _json
    from fastapi.responses import RedirectResponse

    return_url = "/games/"
    if "|" in state:
        _, _ru = state.split("|", 1)
        if _ru.startswith("/"):
            return_url = _ru

    def _fail():
        return RedirectResponse(f"{FRONTEND_URL}{return_url}?line_login=fail")

    if error or not code or not LINE_CHANNEL_ID or not LINE_CHANNEL_SECRET:
        return _fail()

    token_url = "https://api.line.me/oauth2/v2.1/token"
    post_data = _urlparse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": LINE_REDIRECT_URI,
        "client_id": LINE_CHANNEL_ID,
        "client_secret": LINE_CHANNEL_SECRET,
    }).encode()
    req = urllib.request.Request(token_url, data=post_data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            token_data = _json.loads(resp.read())
    except Exception:
        return _fail()

    access_token = token_data.get("access_token", "")
    if not access_token:
        return _fail()

    try:
        profile_req = urllib.request.Request(
            "https://api.line.me/v2/profile",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        with urllib.request.urlopen(profile_req, timeout=10) as profile_resp:
            profile = _json.loads(profile_resp.read())
    except Exception:
        return _fail()

    line_user_id = profile.get("userId", "")
    display_name = (profile.get("displayName") or "").strip()[:16]
    if not line_user_id:
        return _fail()

    conn = _db_conn()
    row = conn.execute("SELECT * FROM members WHERE line_user_id=?", (line_user_id,)).fetchone()
    if not row:
        # LINE預設不提供Email（要另外向LINE申請email範圍權限），這裡用line_user_id
        # 組一個內部專用的合成Email，純粹是為了滿足members表email欄位UNIQUE NOT NULL
        # 的限制，不是真實可聯絡Email——這類帳號無法用忘記密碼、Email通知等功能，
        # 僅供登入排行榜使用，跟Email/Google帳號的使用情境不同。
        synth_email = f"line_{line_user_id}@line.softglow-ai.com"
        rand_pwd = secrets.token_urlsafe(16)
        conn.execute(
            "INSERT INTO members (email, password, plan, nickname, line_user_id) VALUES (?, ?, 'free', ?, ?)",
            (synth_email, _hash_pw(rand_pwd), display_name or None, line_user_id)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM members WHERE line_user_id=?", (line_user_id,)).fetchone()
    elif display_name and not (row["nickname"] or "").strip():
        # 第一次登入後如果玩家自己都還沒設定過暱稱，用LINE顯示名稱補上，之後仍可以自己在站上改
        conn.execute("UPDATE members SET nickname=? WHERE id=?", (display_name, row["id"]))
        conn.commit()
        row = conn.execute("SELECT * FROM members WHERE line_user_id=?", (line_user_id,)).fetchone()

    session = _issue_login_session(conn, row, row["email"])
    return RedirectResponse(f"{FRONTEND_URL}{return_url}?line_token={session['token']}")


# ══════════════════════════════════════════════════════════
# LINE Bot（Messaging API）—— 群組/聊天室打股票代號或名稱查報告
# 2026/08/15新增。設計原則：
#   1) 使用者輸入「整段訊息」剛好就是股票代號（如2330、2330W、2330週）
#      或股票名稱（如台積電）時bot才回應；其餘訊息一律不回應，避免在群組洗版
#   2) 直接呼叫既有 _do_analyze()（跟網站分析引擎/report頁完全同一份邏輯），
#      不重寫第二套分析或格式化邏輯，避免欄位對不上
#   3) 回覆內容精簡（股名+現價+漲跌%），完整報告用連結指向既有公開頁
#      /report/{stock_id}（本來就不需要登入即可看）
#
# 這一段程式碼即使LINE_BOT_CHANNEL_SECRET/LINE_BOT_CHANNEL_ACCESS_TOKEN沒設定
# 也不會讓網站壞掉（webhook收到請求會直接回200但不處理），但要讓bot真的能用：
#   1. 去LINE Developers Console建立一個「Messaging API」類型的channel
#      （⚠️跟LINE Login是不同channel類型，不能共用同一個既有channel）
#   2. Webhook URL設定為 {BACKEND_URL}/webhook/line-bot，並打開Webhook
#   3. 在LINE Official Account Manager的「回應設定」把「自動回應訊息」關掉，
#      不然LINE官方的罐頭自動回覆會搶在bot前面回話
#   4. 在Zeabur設定LINE_BOT_CHANNEL_SECRET/LINE_BOT_CHANNEL_ACCESS_TOKEN
#      這兩個環境變數（Channel Secret跟Channel Access Token都在該channel的
#      Basic settings/Messaging API頁籤可以拿到）
#   5. 要在群組裡用，需要把這個LINE官方帳號加入該群組（一般帳號手動加入即可）
# ══════════════════════════════════════════════════════════

def _line_bot_verify_signature(body: bytes, signature: str) -> bool:
    if not LINE_BOT_CHANNEL_SECRET or not signature:
        return False
    import base64 as _b64
    mac = hmac.new(LINE_BOT_CHANNEL_SECRET.encode(), body, hashlib.sha256).digest()
    expected = _b64.b64encode(mac).decode()
    return hmac.compare_digest(expected, signature)


def _line_bot_resolve_stock(text: str):
    """把使用者輸入解析成(stock_id, tf)；訊息必須整段就是代號或名稱才觸發，
    避免在群組聊天裡對每句夾帶數字的話都亂回應。回傳None代表不觸發。"""
    t = (text or "").strip()
    if not t or len(t) > 12:
        return None
    tf = "D"
    core = t
    core_upper = core.upper()
    if core_upper.endswith("W") and core_upper[:-1].isdigit():
        tf, core = "W", core[:-1]
    elif core_upper.endswith("M") and core_upper[:-1].isdigit():
        tf, core = "M", core[:-1]
    elif "週" in core or "周" in core:
        tf, core = "W", core.replace("週", "").replace("周", "").strip()
    elif "月" in core:
        tf, core = "M", core.replace("月", "").strip()
    core = core.strip()
    if core.isdigit() and 4 <= len(core) <= 6:
        return core, tf
    if core in _name_to_code:
        return _name_to_code[core], tf
    for cid, cname in STOCK_NAMES.items():
        if cname == core:
            return cid, tf
    return None


def _line_bot_reply(reply_token: str, text: str):
    import urllib.request
    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/reply",
        data=_json_mod.dumps({"replyToken": reply_token, "messages": [{"type": "text", "text": text[:4900]}]}).encode(),
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {LINE_BOT_CHANNEL_ACCESS_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
    except Exception as e:
        print(f"⚠️ LINE bot reply失敗: {e}")


def _line_bot_push(to_id: str, text: str):
    """主動推播訊息（跟_line_bot_reply不同——reply要靠webhook事件給的短效replyToken，
       push可以在任何時間點主動發送，例如排程任務結束後通知群組。
       2026/08/16新增，供深度選股完成通知使用。LINE免費方案每月200則推播額度，
       每天群組推播1則遠低於額度，不用擔心費用。"""
    import urllib.request
    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/push",
        data=_json_mod.dumps({"to": to_id, "messages": [{"type": "text", "text": text[:4900]}]}).encode(),
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {LINE_BOT_CHANNEL_ACCESS_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
        return True
    except Exception as e:
        print(f"⚠️ LINE bot push失敗（to={to_id}）: {e}")
        return False


def _line_bot_register_group(group_id: str):
    """記錄機器人所在的LINE群組ID，供之後主動推播（如深度選股完成通知）使用。
       2026/08/16新增：只要群組裡有人傳訊息給機器人（不限是否觸發股票分析回覆），
       就會呼叫這裡把groupId記下來，INSERT OR IGNORE避免重複記錄出錯。
       目前機制沒有排除/取消機制，如果機器人被踢出某個群組，該群組ID會留在
       表裡但推播只會失敗（LINE API回錯，不會影響其他群組），影響有限，先不處理。"""
    if not group_id or not LINE_BOT_CHANNEL_ACCESS_TOKEN:
        return
    try:
        conn = _db_conn()
        conn.execute(
            "INSERT OR IGNORE INTO line_push_groups (group_id) VALUES (?)",
            (group_id,)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ LINE群組ID記錄失敗: {e}")


def _line_bot_push_multi_signal_notice(scan_date: str, count: int, strong_count: int):
    """12金叉選股排程跑完後呼叫（2026/09/17取代原本深度選股的推播）：
       今天有股票出現轉強訊號才推播，同一天只推一次（管理員重跑不會重複推）。"""
    if not count or count <= 0:
        print("[multi_signal] 今日沒有轉強股票，不推播LINE通知")
        return
    if not LINE_BOT_CHANNEL_ACCESS_TOKEN:
        return
    try:
        conn = _db_conn()
        try:
            row = conn.execute("SELECT value FROM app_settings WHERE key='ms_line_pushed_date'").fetchone()
            if row and row["value"] == scan_date:
                print("[multi_signal] 今天已推播過LINE通知，略過")
                return
            group_ids = [r["group_id"] for r in conn.execute("SELECT group_id FROM line_push_groups").fetchall()]
        finally:
            conn.close()
    except Exception as e:
        print(f"⚠️ 讀取LINE推播群組清單失敗: {e}")
        return
    if not group_ids:
        print("[multi_signal] 尚未記錄任何LINE群組ID（需先有人在群組內傳過訊息給機器人），略過本次推播")
        return
    text = (
        f"📊 今日12金叉選股已出爐：{count} 檔出現轉強訊號"
        + (f"，其中 {strong_count} 檔同時符合 3 項以上" if strong_count else "") + "\n"
        f"完整名單請登入App查看 👉 {FRONTEND_URL}/stock/?page=multisignal\n"
        f"僅供參考，不構成投資建議"
    )
    sent = 0
    for gid in group_ids:
        if _line_bot_push(gid, text):
            sent += 1
    try:
        conn = _db_conn()
        conn.execute("INSERT OR REPLACE INTO app_settings (key, value) VALUES ('ms_line_pushed_date', ?)", (scan_date,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ 記錄LINE推播日期失敗: {e}")
    print(f"[multi_signal] LINE推播完成，{sent}/{len(group_ids)} 個群組成功")


@app.post("/webhook/line-bot", include_in_schema=False)
async def line_bot_webhook(request: Request):
    body = await request.body()
    if not LINE_BOT_CHANNEL_SECRET or not LINE_BOT_CHANNEL_ACCESS_TOKEN:
        return PlainTextResponse("OK")  # 尚未設定，直接放行不處理，不讓網站壞掉

    signature = request.headers.get("x-line-signature", "")
    if not _line_bot_verify_signature(body, signature):
        raise HTTPException(status_code=400, detail="invalid signature")

    try:
        payload = _json_mod.loads(body)
    except Exception:
        return PlainTextResponse("OK")

    for event in payload.get("events", []):
        try:
            # 2026/08/16新增：不管這則事件是不是會觸發股票分析回覆，只要來源是群組，
            # 就先把groupId記下來（供之後深度選股完成通知主動推播用），跟下面的
            # 股票代號比對邏輯彼此獨立，不會互相影響
            _source = event.get("source", {}) or {}
            if _source.get("type") == "group":
                _line_bot_register_group(_source.get("groupId", ""))

            if event.get("type") != "message":
                continue
            message = event.get("message", {})
            if message.get("type") != "text":
                continue
            reply_token = event.get("replyToken", "")
            if not reply_token:
                continue

            resolved = _line_bot_resolve_stock(message.get("text", ""))
            if not resolved:
                continue  # 不是純代號/純名稱，不回應，避免洗版

            stock_id, tf = resolved
            try:
                d = _do_analyze(stock_id, tf, user=None)
            except HTTPException:
                _line_bot_reply(reply_token, f"❌ 找不到股票代號：{stock_id}\n請確認代號是否正確（例：2330）")
                continue
            except Exception as e:
                print(f"⚠️ LINE bot分析失敗 {stock_id}: {e}")
                _line_bot_reply(reply_token, f"⚠️ {stock_id} 分析暫時失敗，請稍後再試")
                continue

            stock_name = d.get("stock_name", stock_id)
            disp_price = d.get("display_price", d.get("price", "—"))
            chg_pct = d.get("change_pct")
            chg_str = f"（{'+' if (chg_pct or 0) >= 0 else ''}{chg_pct}%）" if chg_pct is not None else ""
            tf_label = {"D": "日K", "W": "週K", "M": "月K"}.get(tf, "日K")
            # 2026/09/15修正：原本連去{BACKEND_URL}/report/{stock_id}是獨立的SEO靜態報告頁
            # （沒有App導覽列/登入等功能，用完就是死路一條）。帥哥鴻回報「個股連結現在是在
            # 個股分析（指這個靜態報告頁），不是連去個股查詢首頁」，改成帶?stock=參數連到
            # 前端App首頁，會自動觸發個股分析並保留完整App導覽（可繼續看自選股、深度選股等）。
            reply_text = (
                f"📊 {stock_id} {stock_name}（{tf_label}）\n"
                f"現價 {disp_price}{chg_str}\n"
                f"完整報告 👉 {FRONTEND_URL}/?stock={stock_id}\n"
                f"僅供參考，不構成投資建議"
            )
            _line_bot_reply(reply_token, reply_text)
        except Exception as e:
            print(f"⚠️ LINE bot事件處理失敗: {e}")

    return PlainTextResponse("OK")


@app.get("/auth/me")
def auth_me(user: dict = Depends(require_user)):
    today = _taipei_today()
    conn = _db_conn()
    row = conn.execute(
        "SELECT count FROM query_log WHERE member_id=? AND date=? AND ip=''",
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
    # 2026/09/17：付款成功時訂單編號已存進 members.merchant_trade_no，以它為主要判斷
    # （pending_orders 會被定期清掉，原本清掉後「取消定期訂閱」按鈕就消失了）
    is_recurring = bool(recurring_row) or str(user.get("merchant_trade_no") or "").startswith("XYWR")
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
        "queries_limit": 999 if _is_premium(user) else FREE_DAILY_LIMIT,
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


def _render_email(title, body_html, accent="#1D9E75", title_icon="",
                  cta_text="", cta_url="", with_ad=True, card_bg="#f0fdf4",
                  card_border="#86efac", title_color="#166534"):
    """
    統一信件模板（帥哥鴻定案 2026/08/05）：
      頁首(品牌+副標) → [廣告] → 主卡片(標題+body_html) → CTA → [廣告] → 署名 → 頁尾客服
    參數：
      title       主標題文字（不含 icon）
      body_html   卡片內獨有內容（各封信自行組）
      accent      品牌色（CTA 按鈕、連結）
      title_icon  標題前的 emoji（可空）
      cta_text    CTA 按鈕文字（空=不顯示按鈕）
      cta_url     CTA 連結
      with_ad     是否插入保健品廣告（密碼類信件設 False）
      card_bg/card_border/title_color  主卡片配色（依信件語氣調整）
    """
    ad_block = _SOFTGLOW_AD if with_ad else ""
    icon_prefix = f"{title_icon} " if title_icon else ""
    cta_block = ""
    if cta_text and cta_url:
        cta_block = (
            f'<div style="margin-top:24px;text-align:center">'
            f'<a href="{cta_url}" style="background:{accent};color:#fff;padding:13px 36px;'
            f'border-radius:8px;text-decoration:none;font-weight:700;font-size:15px;display:inline-block">{cta_text}</a>'
            f'</div>'
        )
    return (
        f'<div style="font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;'
        f'max-width:560px;margin:0 auto;padding:24px;background:#ffffff">'
        # 頁首
        f'<div style="text-align:center;margin-bottom:24px">'
        f'<h1 style="font-size:26px;color:#1D9E75;margin:0">線上<span style="color:#333">有位</span></h1>'
        f'<p style="color:#888;font-size:12px;margin:4px 0 0;letter-spacing:1px">SoftGlow &middot; 台股技術分析輔助系統</p>'
        f'</div>'
        # 廣告（上）
        f'{ad_block}'
        # 主卡片
        f'<div style="background:{card_bg};border-radius:12px;padding:24px 24px 20px;border:1px solid {card_border}">'
        f'<h2 style="margin:0 0 12px;color:{title_color};font-size:19px">{icon_prefix}{title}</h2>'
        f'{body_html}'
        f'</div>'
        # CTA
        f'{cta_block}'
        # 廣告（下）
        f'{ad_block}'
        # 署名 + 頁尾
        f'<div style="border-top:1px solid #eee;margin-top:28px;padding-top:20px;text-align:center">'
        f'<p style="margin:0;font-size:14px;color:#333;font-weight:600">&mdash; 線上有位 SoftGlow 團隊 敬上</p>'
        f'<p style="margin:12px 0 0;font-size:12px;color:#9ca3af;line-height:1.8">'
        f'如未收到相關通知、發票，或有任何帳號問題，<br>'
        f'歡迎來信客服：<a href="mailto:wation168@gmail.com" style="color:#1D9E75;text-decoration:none">wation168@gmail.com</a><br>'
        f'線上有位 SoftGlow &copy; 2026'
        f'</p></div>'
        f'</div>'
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


def _ecpay_query_trade(trade_no: str) -> dict:
    """呼叫綠界 QueryTradeInfo/V5 查單筆訂單。回傳綠界的欄位 dict；失敗回 {}。
    注意：這支 API 回傳的是 TradeStatus（1=已付款、0=未付款、10200095=未成立），沒有 RtnCode。"""
    import urllib.request as _ur_q, urllib.parse as _up_q, hashlib as _hl_q, time as _t_q
    if not (ECPAY_HASH_KEY and ECPAY_HASH_IV and ECPAY_MERCHANT_ID and trade_no):
        return {}
    try:
        _p = {"MerchantID": ECPAY_MERCHANT_ID, "MerchantTradeNo": trade_no, "TimeStamp": str(int(_t_q.time()))}
        _raw = "&".join(f"{k}={v}" for k, v in sorted(_p.items(), key=lambda x: x[0].lower()))
        _raw = _up_q.quote_plus(f"HashKey={ECPAY_HASH_KEY}&{_raw}&HashIV={ECPAY_HASH_IV}").lower()
        _p["CheckMacValue"] = _hl_q.sha256(_raw.encode()).hexdigest().upper()
        _req = _ur_q.Request(
            "https://payment.ecpay.com.tw/Cashier/QueryTradeInfo/V5",
            data=_up_q.urlencode(_p).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with _ur_q.urlopen(_req, timeout=8) as _r:
            return dict(_up_q.parse_qsl(_r.read().decode("utf-8", "replace"), keep_blank_values=True))
    except Exception as _e:
        print(f"[綠界查單] {trade_no} 查詢失敗：{_e}")
        return {}


def _ecpay_trade_paid(trade_no: str) -> bool:
    return _ecpay_query_trade(trade_no).get("TradeStatus", "") == "1"


def _parse_ecpay_body(raw: bytes) -> dict:
    """綠界 webhook 原始內容 → dict（一律 UTF-8；綠界的中文欄位可能未經百分比編碼）"""
    import urllib.parse as _up_eb
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    return {k: v for k, v in _up_eb.parse_qsl(text, keep_blank_values=True, encoding="utf-8")}


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

    # 補即時價（走 FinMind，與個股分析同源，不走被擋的 MIS，2026/07/30 改用共用函式）
    for item in top20:
        try:
            _qd = _get_live_quote_data(item["stock_id"])
            if _qd:
                _p = float(_qd["price"])
                _chg = float(_qd.get("change", 0))
                _prev = _p - _chg
                if _p > 0:
                    item["price"] = round(_p, 2)
                    if _prev > 0:
                        item["change_pct"] = round(_chg / _prev * 100, 2)
        except Exception:
            pass

    return top20


# 2026/09/17：深度選股下架（帥哥鴻決定由12金叉選股接手），原本這裡的
# _run_deep_analysis_job／20天成效追蹤（_log_deep_pick_events、_update_deep_pick_returns）／
# 門檻設定（_apply_deep_cfg_overrides）一併移除。deep_pick_log 資料表保留在DB不刪，
# 需要查舊程式可從 main.py.bak_20260917_綜合解說前 找回。


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


def _picks_payload(rows, updated_at, user):
    st = _taipei_now_str("%Y-%m-%d %H:%M")
    if _is_premium(user):
        return {"data": rows, "updated_at": updated_at, "server_time": st,
                "tier": "paid", "masked": False, "preview": False}
    if user:
        masked = [_deep_mask_item(dict(x)) if isinstance(x, dict) else x for x in rows]
        return {"data": masked, "updated_at": updated_at, "server_time": st,
                "tier": "free", "masked": True, "preview": False}
    n = len(rows or [])
    placeholders = [{
        "stock_id": "＊＊＊＊", "stock_name": "＊＊＊＊",
        "masked": True, "preview": True,
    } for _ in range(min(3, n) if n else 2)]
    return {"data": placeholders, "updated_at": updated_at, "server_time": st,
            "approx_count": n, "tier": "guest", "masked": True, "preview": True}

# 2026/09/13修正：這個 @app.get 裝饰器先前誤掛在上面的 _picks_payload（純輔助函式，
# 三個參數都沒有型別／預設值）身上，導致 FastAPI 把 rows/updated_at/user 當成
# 三個必填的 query 參數，正式站呼叫這支API時一律回傳422（Field required）。
# 資金雷達色塊點擊「載入失敗」、首頁異常訊號卡靜默顯示假的「今日尚無資料」都是這個bug造成。
# 裝饰器改掛回真正處理請求的 get_opening_picks，_picks_payload 只當內部輔助函式使用。
@app.get("/api/picks/opening")
def get_opening_picks(user: dict | None = Depends(get_current_user)):
    """開盤熱門股（成交量前20；遊客弱預覽／免費藏名／付費全開）
    盤中補即時報價，盤後補當日收盤價，都用 MIS API。
    """
    import urllib.request as _urq, json as _jq
    base_data = _OPENING_TOP20.get("data", [])
    updated_at = _OPENING_TOP20.get("updated_at")

    if not base_data:
        return _picks_payload(base_data, updated_at, user)

    enriched = []
    for item in base_data:
        code = item.get("stock_id", "")
        new_item = dict(item)
        try:
            # 先查 _QUOTE_CACHE（個股分析同源，不走被擋的 MIS，2026/07/30 改用共用函式）
            _qd = _get_live_quote_data(code)
            if _qd:
                _p   = float(_qd["price"])
                _chg = float(_qd.get("change", 0))
                _prev = _p - _chg
                if _p > 0:
                    new_item["price"] = round(_p, 2)
                    new_item["change_pct"] = round(_chg / _prev * 100, 2) if _prev > 0 else 0
        except Exception:
            pass
        enriched.append(new_item)

    return _picks_payload(enriched, updated_at, user)


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

# 安全性修正（2026/07/27）：移除寫死的 "630428"，統一改用 ADMIN_API_KEY 環境變數比對
CONTACT_ADMIN_PWD = ADMIN_API_KEY


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
        if ADMIN_NOTIFY_EMAIL:
            _send_email(ADMIN_NOTIFY_EMAIL, f"【線上有位】新留言來自 {name}", html_body)
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
    # 管理員刪除：token=ADMIN_API_KEY
    if body.token != "owner" and (not CONTACT_ADMIN_PWD or body.token != CONTACT_ADMIN_PWD):
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
    if not CONTACT_ADMIN_PWD or body.token != CONTACT_ADMIN_PWD:
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
    if not CONTACT_ADMIN_PWD or body.token != CONTACT_ADMIN_PWD:
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
async def unblock_user(email: str, token: str = Header(default="", alias="X-Admin-Key")):
    if not CONTACT_ADMIN_PWD or token != CONTACT_ADMIN_PWD:
        raise HTTPException(status_code=403, detail="無權限")
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("DELETE FROM blocked_users WHERE email=?", (email,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="未找到封鎖記錄")
    return {"ok": True}


@app.get("/api/block")
async def get_blocked_users(token: str = Header(default="", alias="X-Admin-Key")):
    if not CONTACT_ADMIN_PWD or token != CONTACT_ADMIN_PWD:
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

        # 2026/09/17：邀請好友活動已結束，預設不再發放新獎勵（已發放的解鎖天數照常有效）。
        # 若日後重啟活動，在 Zeabur 設定環境變數 REFERRAL_CAMPAIGN_ACTIVE=1 即可。
        if new_cycles > 0 and os.environ.get("REFERRAL_CAMPAIGN_ACTIVE", "0") != "1":
            print(f"[REFERRAL] 活動已結束，不發放獎勵 inviter={inviter} cnt={cnt}")
            new_cycles = 0

        if new_cycles > 0:
            add_days  = new_cycles * 30
            today_str = _taipei_today()
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



# ── Data-1 市場列／產業／新聞（公開源；失敗回空；禁止假數）──
_MARKET_CACHE: dict = {
    "overview": {"data": None, "expires": 0.0},
    "industries": {"data": None, "expires": 0.0},
    "news": {"data": None, "expires": 0.0},
    "mi_index": {"data": None, "expires": 0.0},
    "taifex": {"data": None, "expires": 0.0},
}
_MARKET_UA = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json,text/javascript,*/*;q=0.8",
    "Referer": "https://www.twse.com.tw/",
}

def _market_parse_num(val):
    if val is None:
        return None
    s = str(val).strip()
    if s in ("", "-", "--", "NULL", "null", "N/A", "-"):
        return None
    s = s.replace(",", "").replace("%", "").replace("+", "")
    try:
        return float(s)
    except Exception:
        return None


def _market_http_json(url: str, timeout: float = 10, ssl_ctx=None):
    import urllib.request as _ur
    import json as _json
    req = _ur.Request(url, headers=_MARKET_UA)
    with _ur.urlopen(req, timeout=timeout, context=(ssl_ctx or _TWSE_SSL_CTX)) as resp:
        raw = resp.read()
    if not raw:
        return None
    return _json.loads(raw.decode("utf-8-sig"))


def _market_cache_get(key: str):
    slot = _MARKET_CACHE.get(key) or {}
    data = slot.get("data")
    exp = float(slot.get("expires") or 0)
    if data is not None and exp > _time_mod.time():
        return data
    return None


def _market_cache_set(key: str, data, ttl: float):
    _MARKET_CACHE[key] = {"data": data, "expires": _time_mod.time() + ttl}


def _fetch_mi_index_latest(max_back: int = 10):
    """證交所盤後價格指數。往回找最近有 data 的交易日。"""
    hit = _market_cache_get("mi_index")
    if hit is not None:
        return hit
    from datetime import timedelta
    from zoneinfo import ZoneInfo
    day = datetime.now(ZoneInfo("Asia/Taipei")).date()
    last_err = None
    for i in range(max_back):
        ymd = (day - timedelta(days=i)).strftime("%Y%m%d")
        url = (
            "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX"
            f"?response=json&date={ymd}&type=IND"
        )
        try:
            j = _market_http_json(url, timeout=12)
        except Exception as e:
            last_err = e
            continue
        tables = (j or {}).get("tables") or []
        first = tables[0] if tables else {}
        if (j or {}).get("stat") == "OK" and first.get("data"):
            payload = {"date": ymd, "tables": tables}
            _market_cache_set("mi_index", payload, 900)
            return payload
    print(f"[MARKET] MI_INDEX 無資料 last_err={last_err}")
    _market_cache_set("mi_index", None, 45)
    return None


def _mi_index_rows(mi: dict, want_names: set[str] | None = None, category_only: bool = False) -> list[dict]:
    tables = (mi or {}).get("tables") or []
    if not tables:
        return []
    rows_out = []
    exclude = ("兩倍", "反向", "日報酬", "槓桿")
    for row in tables[0].get("data") or []:
        if not row:
            continue
        name = str(row[0] or "").strip()
        if not name:
            continue
        if any(x in name for x in exclude):
            continue
        if category_only:
            if not name.endswith("類指數"):
                continue
        elif want_names is not None and name not in want_names:
            continue
        value = _market_parse_num(row[1] if len(row) > 1 else None)
        pts = _market_parse_num(row[3] if len(row) > 3 else None)
        pct = _market_parse_num(row[4] if len(row) > 4 else None)
        if value is None or pct is None:
            continue
        if pts is not None:
            pts = abs(pts) if pct >= 0 else -abs(pts)
        rows_out.append({
            "name": name,
            "value": value,
            "change": pts,
            "change_pct": pct,
        })
    return rows_out


def _fetch_mis_indices() -> list[dict]:
    url = (
        "https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
        "?ex_ch=tse_t00.tw|otc_o00.tw|tse_t13.tw|tse_t17.tw&json=1&delay=0"
    )
    try:
        j = _market_http_json(url, timeout=8, ssl_ctx=_TWSE_SSL_CTX)
    except Exception as e:
        print(f"[MARKET] MIS 失敗：{e}")
        return []
    items = []
    id_map = {
        "t00": "taiex",
        "o00": "otc",
        "t13": "elec",
        "t17": "finance",
    }
    for x in (j or {}).get("msgArray") or []:
        code = str(x.get("c") or "")
        z = _market_parse_num(x.get("z"))
        y = _market_parse_num(x.get("y"))
        if z is None or y is None or y == 0:
            continue
        chg = round(z - y, 2)
        pct = round(chg / y * 100, 2)
        items.append({
            "id": id_map.get(code, code),
            "code": code,
            "name": str(x.get("n") or code),
            "value": z,
            "prev": y,
            "change": chg,
            "change_pct": pct,
            "time": x.get("t") or x.get("%") or "",
            "trade_date": x.get("d") or "",
            "volume": _market_parse_num(x.get("r")),
            "amount": _market_parse_num(x.get("m")),
            "source": "TWSE MIS",
        })
    return items


def _fetch_tx_near() -> dict | None:
    hit = _market_cache_get("taifex")
    if hit is not None:
        return hit or None
    url = "https://openapi.taifex.com.tw/v1/DailyMarketReportFut"
    try:
        j = _market_http_json(url, timeout=15)
    except Exception as e:
        print(f"[MARKET] TAIFEX 失敗：{e}")
        _market_cache_set("taifex", None, 60)
        return None
    if not isinstance(j, list):
        _market_cache_set("taifex", None, 60)
        return None
    rows = [
        r for r in j
        if r.get("Contract") == "TX" and r.get("TradingSession") == "一般"
    ]
    if not rows:
        _market_cache_set("taifex", None, 60)
        return None
    rows.sort(key=lambda r: str(r.get("ContractMonth(Week)") or ""))
    r = rows[0]
    last = _market_parse_num(r.get("Last"))
    if last is None:
        _market_cache_set("taifex", None, 60)
        return None
    item = {
        "id": "txf",
        "code": "TX",
        "name": "臺股期貨近月",
        "value": last,
        "change": _market_parse_num(r.get("Change")),
        "change_pct": _market_parse_num(r.get("%")),
        "volume": _market_parse_num(r.get("Volume")),
        "trade_date": str(r.get("Date") or ""),
        "contract_month": str(r.get("ContractMonth(Week)") or ""),
        "session": "一般",
        "source": "TAIFEX OpenAPI",
    }
    _market_cache_set("taifex", item, 900)
    return item


def _overview_from_mi(mi: dict) -> list[dict]:
    want = {
        "發行量加權股價指數": ("taiex", "t00"),
        "電子工業類指數": ("elec", "t13"),
        "金融保險類指數": ("finance", "t17"),
    }
    out = []
    for row in _mi_index_rows(mi, want_names=set(want)):
        iid, code = want[row["name"]]
        out.append({
            "id": iid,
            "code": code,
            "name": row["name"],
            "value": row["value"],
            "change": row["change"],
            "change_pct": row["change_pct"],
            "trade_date": mi.get("date") or "",
            "source": "TWSE MI_INDEX",
        })
    return out


@app.get("/api/market/overview")
def api_market_overview():
    """加權／櫃買／電子／金融／台指期近月。無資料不填假數。"""
    hit = _market_cache_get("overview")
    if hit is not None:
        return hit
    items: list[dict] = []
    source_bits = []
    label = "最後交易日收盤"
    mis = _fetch_mis_indices()
    if mis:
        items.extend(mis)
        source_bits.append("TWSE MIS")
        if any(x.get("time") for x in mis):
            label = "證交所揭示（可能為最後交易日）"
    have_ids = {x.get("id") for x in items}
    if "taiex" not in have_ids or "elec" not in have_ids or "finance" not in have_ids:
        mi = _fetch_mi_index_latest()
        if mi:
            for row in _overview_from_mi(mi):
                if row["id"] not in have_ids:
                    items.append(row)
                    have_ids.add(row["id"])
            source_bits.append("TWSE MI_INDEX")
    tx = _fetch_tx_near()
    if tx:
        items.append(tx)
        source_bits.append("TAIFEX OpenAPI")
    # 穩定順序
    order = {"taiex": 0, "otc": 1, "txf": 2, "elec": 3, "finance": 4}
    items.sort(key=lambda x: order.get(x.get("id"), 9))
    as_of = _taipei_now_str()
    kept = []
    for itx in items:
        if itx.get("value") is None or not itx.get("source") or not itx.get("name"):
            continue
        itx = dict(itx)
        itx["as_of"] = as_of
        itx["timezone"] = "Asia/Taipei"
        kept.append(itx)
    items = kept
    trade_dates = [x.get("trade_date") for x in items if x.get("trade_date")]
    payload = {
        "ok": bool(items),
        "as_of": as_of if items else "",
        "timezone": "Asia/Taipei",
        "source": " / ".join(dict.fromkeys(source_bits)) if items else "",
        "label": label if items else "",
        "trade_date": trade_dates[0] if trade_dates else "",
        "items": items,
    }
    _market_cache_set("overview", payload, 90 if payload["ok"] else 30)
    return payload


@app.get("/api/market/industries")
def api_market_industries():
    """證交所官方類股指數強弱（最後交易日收盤）。"""
    hit = _market_cache_get("industries")
    if hit is not None:
        return hit
    mi = _fetch_mi_index_latest()
    rows = _mi_index_rows(mi, category_only=True) if mi else []
    rows.sort(key=lambda x: (x.get("change_pct") is None, -(x.get("change_pct") or 0)))
    as_of = _taipei_now_str()
    src = "TWSE MI_INDEX 類股指數"
    td = (mi or {}).get("date") or ""
    stamped = []
    for r in rows:
        if r.get("change_pct") is None or r.get("value") is None or not r.get("name"):
            continue
        stamped.append({
            "name": r["name"],
            "value": r["value"],
            "change": r.get("change"),
            "change_pct": r["change_pct"],
            "source": src,
            "as_of": as_of,
            "timezone": "Asia/Taipei",
            "trade_date": td,
        })
    payload = {
        "ok": bool(stamped),
        "as_of": as_of if stamped else "",
        "timezone": "Asia/Taipei",
        "source": src if stamped else "",
        "label": "證交所類股指數・最後交易日收盤" if stamped else "",
        "trade_date": td if stamped else "",
        "items": stamped,
        "gainers": stamped[:8] if stamped else [],
        "losers": list(reversed(stamped[-8:])) if stamped else [],
    }
    _market_cache_set("industries", payload, 900 if payload["ok"] else 30)
    return payload


@app.get("/api/market/news")
def api_market_news(limit: int = 12):
    """鉅亨 RSS 原標題。失敗回空，不發明標題。"""
    hit = _market_cache_get("news")
    if hit is not None:
        return hit
    try:
        n = int(limit)
    except Exception:
        n = 12
    n = max(1, min(n, 30))
    items = []
    try:
        import sys as _sys
        _picker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker")
        if _picker_path not in _sys.path:
            _sys.path.insert(0, _picker_path)
        from crawler import fetch_cnyes_news
        raw = fetch_cnyes_news(80, days=3) or []
        seen = set()
        for rec in raw:
            title = str((rec or {}).get("title") or "").strip()
            link = str((rec or {}).get("link") or "").strip()
            if not title or not link or title in seen:
                continue
            if not (link.startswith("http://") or link.startswith("https://")):
                continue
            seen.add(title)
            items.append({
                "title": title,
                "link": link,
                "pub_date": str((rec or {}).get("pub_date") or ""),
                "source": "鉅亨",
                "as_of": _taipei_now_str(),
                "timezone": "Asia/Taipei",
            })
            if len(items) >= n:
                break
    except Exception as e:
        print(f"[MARKET] news 失敗：{e}")
        items = []
    payload = {
        "ok": bool(items),
        "as_of": _taipei_now_str(),
        "timezone": "Asia/Taipei",
        "source": "鉅亨 RSS" if items else "",
        "label": "來源：鉅亨" if items else "",
        "items": items,
    }
    _market_cache_set("news", payload, 600 if payload["ok"] else 45)
    return payload


def _fetch_market_breadth_twse() -> dict | None:
    """上市個股（TWSE STOCK_DAY_ALL）當日漲跌家數統計。

    2026/09/13 新增（線上有位首頁改版：市場氣氛／漲跌家數，帥哥鴻+GPT已確認要做）。
    範圍刻意只算「上市」，跟首頁「加權指數」同一個母體，口徑一致。
    上櫃（TPEx tpex_mainboard_daily_close_quotes）目前只核實過
    SecuritiesCompanyCode／CompanyName／TradingShares／Date 這幾個欄位
    （見 stock_picker/crawler.py 的 _fetch_volume_top_from_tpex 註解），
    沒有實際核對過「收盤」「漲跌」欄位名稱，寧可先不混進來，
    也不要用猜的欄位名稱算出可能是錯的上櫃漲跌方向。之後要補上櫃，
    先用瀏覽器或curl實際打一次那支API確認欄位再動工。

    CSV欄位與 _fetch_opening_volume_top20() 同一份資料源：
    日期(0) 代號(1) 名稱(2) 成交股數(3) 成交金額(4) 開盤(5) 最高(6) 最低(7) 收盤(8) 漲跌(9)
    """
    import urllib.request as _ur3, csv as _csv3, io as _io3

    try:
        url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY_ALL"
        req = _ur3.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer":    "https://www.twse.com.tw/",
        })
        with _ur3.urlopen(req, timeout=15, context=_TWSE_SSL_CTX) as r:
            raw_text = r.read().decode("utf-8-sig", errors="replace")
        reader = _csv3.reader(_io3.StringIO(raw_text))
        up = down = flat = 0
        trade_date = ""
        for row in reader:
            try:
                if len(row) < 10:
                    continue
                code = str(row[1]).strip().strip('="')
                if not code.isdigit() or len(code) != 4:
                    continue
                close_str  = str(row[8]).strip().strip('="').replace(",", "")
                change_str = str(row[9]).strip().strip('="').replace(",", "")
                if close_str in ("", "--", "X") or change_str in ("", "--", "X"):
                    continue
                change = float(change_str)
                if not trade_date:
                    trade_date = str(row[0]).strip().strip('="')
                if change > 0:
                    up += 1
                elif change < 0:
                    down += 1
                else:
                    flat += 1
            except Exception:
                continue
        total = up + down + flat
        # 上市普通股實際約 1000+ 檔，抓到的數量明顯過少代表這次抓取本身有問題，
        # 寧可整支API回傳「無資料」讓前端隱藏這塊，也不要顯示一個算錯的家數統計。
        if total < 500:
            print(f"[BREADTH] 有效筆數過少（{total}），視為抓取失敗")
            return None
        return {"up": up, "down": down, "flat": flat, "total": total, "trade_date": trade_date}
    except Exception as e:
        print(f"[BREADTH] TWSE STOCK_DAY_ALL 失敗：{e}")
        return None


@app.get("/api/market/breadth")
def api_market_breadth():
    """上市個股當日漲跌家數／市場氣氛（僅上市，與加權指數同母體，見上方函式註解）。
    2026/09/13 新增。"""
    hit = _market_cache_get("breadth")
    if hit is not None:
        return hit
    b = _fetch_market_breadth_twse()
    as_of = _taipei_now_str()
    if not b:
        payload = {"ok": False, "as_of": "", "source": "", "label": "",
                   "up": 0, "down": 0, "flat": 0, "total": 0, "mood": ""}
        _market_cache_set("breadth", payload, 60)
        return payload
    up, down, flat, total = b["up"], b["down"], b["flat"], b["total"]
    if up > down * 1.15:
        mood = "偏多"
    elif down > up * 1.15:
        mood = "偏空"
    else:
        mood = "多空拉鋸"
    payload = {
        "ok": True,
        "as_of": as_of,
        "timezone": "Asia/Taipei",
        "source": "TWSE STOCK_DAY_ALL（僅上市，與加權指數同母體）",
        "label": "上市個股漲跌家數",
        "trade_date": b.get("trade_date") or "",
        "up": up, "down": down, "flat": flat, "total": total,
        "up_pct": round(up / total * 100, 1) if total else 0,
        "down_pct": round(down / total * 100, 1) if total else 0,
        "flat_pct": round(flat / total * 100, 1) if total else 0,
        "mood": mood,
    }
    _market_cache_set("breadth", payload, 900)
    return payload


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

# 報告模板版本標記：每次改動 _build_report_html 的 HTML/CSS 結構就要更新這個字串，
# report_generate 靠這個標記判斷 stock_reports 裡的快取是不是舊模板產生的，
# 是的話強制重新產生，不然光改版面/文案，使用者會一直看到卡住的舊快取（直到當天
# 收盤基準換了才會被上面的 price_basis_date 檢查順便救回來，不夠即時）。
_REPORT_TPL_VERSION = "v2026-09-17-wording"
# 2026/09/14修正（案件003驗收時發現）：上面這個版本標記在08/07之後就沒再更新過，但
# 09/14這輪其實已經改了.stat-hint解說文字的CSS（字級/顏色/拿掉斜體，見_build_report_html
# 內文字說明），忘記同步把版本標記跟著往前推——結果部署後、當天已經被瀏覽過而快取進
# stock_reports的舊報告，因為快取裡嵌的report_tpl標記字串跟目前程式碼設定的_REPORT_TPL_VERSION
# 剛好還是同一個字串，被上面的快取有效性檢查誤判成「模板沒變」，繼續原封不動吐出改版前的
# 舊HTML（真人實測/report/2317時發現字體樣式仍是修正前的10px斜體藍字，查code才抓到這個
# 根因）。這裡把版本字串往前推一版，讓所有今天以前產生的舊快取全部視為過期，下次任何人
# 造訪都會強制重新產生、套用新CSS，之後這個標記務必跟著每次_build_report_html的HTML/CSS
# 改動一起更新，不能漏掉。

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
    # 加入 KD 方向變化
    _kd_k_chg = kd_status.get("k_change")
    _kd_d_chg = kd_status.get("d_change")
    if _kd_k_chg is not None and kd_text:
        _k_arrow = "↑" if _kd_k_chg > 0 else ("↓" if _kd_k_chg < 0 else "→")
        _d_arrow = "↑" if _kd_d_chg > 0 else ("↓" if _kd_d_chg < 0 else "→")
        kd_text = kd_text.replace(
            f"K={kd_status.get('k', 0):.1f}",
            f"K={kd_status.get('k', 0):.1f}({_k_arrow}{abs(_kd_k_chg):.1f})"
        ).replace(
            f"D={kd_status.get('d', 0):.1f}",
            f"D={kd_status.get('d', 0):.1f}({_d_arrow}{abs(_kd_d_chg):.1f})"
        )
    kd_color    = "#4ade80" if kd_dir in ("bullish",) else ("#f87171" if kd_dir == "bearish" else "#fbbf24")
    macd_dir    = macd_status.get("direction", "neutral")
    macd_text   = macd_status.get("text", "")
    macd_color  = {"bullish": "#4ade80", "slightly_bullish": "#86efac",
                   "bearish": "#f87171", "slightly_bearish": "#fca5a5"}.get(macd_dir, "#8faabf")
    vol_text    = vol_analysis.get("text", "")
    # 加入今日 vs 昨日量比較
    _tv = vol_analysis.get("today_vol", 0)
    _yv = vol_analysis.get("yesterday_vol", 0)
    if _tv > 0 and _yv > 0:
        _tv_ratio = _tv / _yv
        _tv_arrow = "↑" if _tv_ratio > 1.05 else ("↓" if _tv_ratio < 0.95 else "→")
        _tv_pct = round(abs(_tv_ratio - 1) * 100)
        vol_text += f"，今日 {_tv:,} 張 vs 昨日 {_yv:,} 張 {_tv_arrow}{_tv_pct}%"
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
            tp_position_text  = f"雷達全亮且靠近支撐（距支撐 -{sup_dist}%），多方條件齊備、位置風險相對低"
            tp_position_color = "#16a34a"
            tp_position_bg    = "#f0fdf4"
        elif res_dist < 5:
            tp_position_icon  = "⚠️"
            tp_position_text  = f"雷達全亮但已漲一段（距壓力僅 +{res_dist}%），位置偏高，支撐參考 {support}"
            tp_position_color = "#d97706"
            tp_position_bg    = "#fffbeb"
        else:
            tp_position_icon  = "👀"
            tp_position_text  = f"雷達全亮，位於中段（距支撐 -{sup_dist}%，距壓力 +{res_dist}%），多方結構維持"
            tp_position_color = "#2563eb"
            tp_position_bg    = "#eff6ff"
    elif tp_score == 3:
        if sup_dist <= 5:
            tp_position_icon  = "👀"
            tp_position_text  = f"三格亮，靠近支撐（距支撐 -{sup_dist}%），尚差一項條件"
            tp_position_color = "#2563eb"
            tp_position_bg    = "#eff6ff"
        else:
            tp_position_icon  = "⏳"
            tp_position_text  = f"三格亮，尚差一項條件"
            tp_position_color = "#6b7280"
            tp_position_bg    = "#f9fafb"
    else:
        tp_position_icon  = "🚫"
        tp_position_text  = f"多空雷達未齊（{tp_score}/4），多方條件不足"
        tp_position_color = "#dc2626"
        tp_position_bg    = "#fff1f2"
    wr_pct      = int(win_rate * 100)
    wr_color    = "#4ade80" if wr_pct >= 56 else ("#fbbf24" if wr_pct >= 52 else "#8faabf")
    kp_bullish  = any(x in kline_pattern for x in ["多頭", "早晨", "錘子", "突破", "量增大紅", "連三紅"])
    kp_bearish  = any(x in kline_pattern for x in ["空頭", "黃昏", "流星", "跌破", "量增大黑", "連三黑"])
    kp_color    = "#4ade80" if kp_bullish else ("#f87171" if kp_bearish else "#fbbf24")

    # ── 趨勢文字（帶入實際數據，消除模板感）──
    _r_ma20 = round(float(d.get("ma_values", {}).get("ma20", 0)), 1)
    _r_ma60 = round(float(d.get("ma_values", {}).get("ma60", 0)), 1)
    _r_slope = tp_ma20_slope  # "up"/"down"/"flat"
    if trend == "上升趨勢":
        _ma_gap_pct = round((_r_ma20 - _r_ma60) / _r_ma60 * 100, 1) if _r_ma60 > 0 else 0
        _slope_word = "趨勢加速擴大中" if _r_slope == "up" else ("但動能趨緩" if _r_slope == "down" else "穩定進行中")
        trend_desc = f"MA20({_r_ma20}) 站上 MA60({_r_ma60})，兩線差距 {_ma_gap_pct}%，多頭排列{_slope_word}。趨勢未反轉前，均線是多方結構的觀察位置。"
    elif trend == "下降趨勢":
        _ma_gap_pct = round((_r_ma60 - _r_ma20) / _r_ma60 * 100, 1) if _r_ma60 > 0 else 0
        _slope_word = "空方加速" if _r_slope == "down" else ("但跌勢趨緩" if _r_slope == "up" else "")
        trend_desc = f"MA20({_r_ma20}) 在 MA60({_r_ma60}) 下方，差距 {_ma_gap_pct}%，空頭排列{_slope_word}。反彈遇均線壓力明顯，空方結構尚未改變。"
    else:
        trend_desc = f"MA20({_r_ma20}) 與 MA60({_r_ma60}) 相近糾結，多空交戰方向未明，需等均線分離或突破關鍵位確認方向。"

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
                f"明日若收盤跌破今日低點 {today_low}，代表突破失敗。"
            )

    # 合併結論邏輯：優先用 _do_analyze 產出的結論（d["warning"]），避免兩套平行邏輯矛盾
    # 2026/08/20修正：舊版kbar_action/today_breakout排在_conclusion_op前面，導致上面這行
    # 註解講的「優先用d["warning"]」形同虛設——只要出現K棒型態（很常見），報告顯示的操作
    # 建議就完全略過d["warning"]，跟個股解析頁（直接顯示完整的d.warning）兜不起來，同一支
    # 股票兩邊看到不同結論，帥哥鴻實際使用時發現「常常都是不一樣的解說」。改成真正落實
    # 「優先用d["warning"]」，kbar_action/today_breakout/雷達分數只在d["warning"]完全沒有
    # 內容時才當備援，兩邊顯示的核心結論就會一致。
    _conclusion_text = d.get("warning", "")
    # 從結論中提取「操作：」後面的文字
    _conclusion_op = ""
    _op_mark = "觀察重點：" if "觀察重點：" in _conclusion_text else "操作："
    if _op_mark in _conclusion_text:
        _conclusion_op = _conclusion_text.split(_op_mark, 1)[1].strip()

    if _conclusion_op:
        # 使用結論的操作建議（位置分析更精準，且與個股解析頁一致），前面加上位置描述
        _conclusion_pos = _conclusion_text.split(_op_mark)[0].strip().rstrip("。，")
        op_text = f"{_conclusion_pos}。\n\n觀察重點：{_conclusion_op}"
    elif _conclusion_text:
        # d["warning"]有內容但沒有「操作：」片段（少見情況），整段當op_text，一樣跟解析頁一致
        op_text = _conclusion_text
    elif kbar_action:
        op_text = kbar_action
    elif today_breakout:
        op_text = f"今日突破前高 {prev_high}，突破型態成立。失效位置 {stop_loss}，前方壓力 {resistance}，損益比 {rr_ratio:.2f}。"
    elif tp_score == 0:
        op_text = f"多空雷達四格全滅，技術面偏弱。趨勢翻多、MACD 翻正、量能放大是後續觀察的轉強條件。"
    elif tp_score <= 1:
        op_text = f"多空雷達訊號不足，方向未明。失效位置 {stop_loss}，觀察雷達訊號是否陸續補齊。"
    else:
        op_text = f"趨勢盤整，方向未明。觀察能否突破壓力 {resistance}；失效位置 {stop_loss}，損益比 {rr_ratio:.2f}。"

    # 突破風險提示（開高走低）是額外補充資訊，跟主結論不衝突，只要today_breakout成立就補上，
    # 不綁在特定分支（舊版只有kbar_action分支才會補到，容易漏掉）
    op_text = op_text + _breakout_risk_text

    # ── 乖離率進出場提示 ──
    _bias_text = ""
    _bias5_str  = f"{tp_bias5:+.1f}%" if tp_bias5 is not None else "-"
    _bias20_str = f"{tp_bias20:+.1f}%" if tp_bias20 is not None else "-"
    _bias5_color  = "#f87171" if tp_bias5 and tp_bias5 > 10 else ("#facc15" if tp_bias5 and tp_bias5 > 5 else ("#4ade80" if tp_bias5 and tp_bias5 < -3 else "var(--text)"))
    _bias20_color = "#f87171" if tp_bias20 and tp_bias20 > 8 else ("#4ade80" if tp_bias20 and tp_bias20 < -8 else "var(--text)")
    if tp_bias_entry:
        _bias_text = f"\n\n✅ 乖離率：雷達全亮，MA5 乖離 {_bias5_str}（剛站上均線，未過熱）。"
    elif tp_bias_exit_warning == "大":
        _bias_text = f"\n\n🔴 過熱程度【大】：MA5 正乖離 {_bias5_str} 已超過 +10%，股價嚴重偏離均線，高檔回檔風險高。"
    elif tp_bias_exit_warning == "中":
        _bias_text = f"\n\n🟡 過熱程度【中】：MA5 正乖離 {_bias5_str} 介於 5%~10%，股價偏離均線，若出現黑K或量縮代表轉弱。"
    elif tp_bias_exit_warning == "小":
        _bias_text = f"\n\n🟢 轉弱程度【小】：KD 死叉且 MACD 動能向下，屬趨勢轉弱初期；失效位置 {stop_loss}。"
    # ── 基本面補充（有數據時才顯示）──
    _fund_text = ""
    _r_per = d.get("per")
    _r_div = d.get("dividend_yield")
    _r_eps = d.get("eps_ttm")
    if _r_per is not None and _r_div is not None:
        try:
            _per_f = float(_r_per)
            _div_f = float(_r_div)
            if _per_f > 0:
                _fund_text = f"\n\n📊 基本面：本益比 {_per_f:.1f}，殖利率 {_div_f:.1f}%"
                if _per_f > 30:
                    _fund_text += "（估值偏高）"
                elif _per_f < 12 and _div_f > 3:
                    _fund_text += "（估值偏低且高殖利率，基本面支持）"
                elif _per_f < 12:
                    _fund_text += "（估值偏低）"
                if _r_eps is not None:
                    _fund_text += f"，EPS {float(_r_eps):.2f}"
        except (ValueError, TypeError):
            pass
    op_text = op_text + _bias_text + _fund_text

    # ── 多空雷達補充說明 ──
    _tp_missing = []
    if not tp_trend: _tp_missing.append(f"趨勢（需高低點結構轉多，目前 {trend}；參考 MA20 {tp_ma20} / MA60 {tp_ma60}）")
    if not tp_macd:  _tp_missing.append(f"MACD（需柱體翻正，目前 {tp_hist}）")
    if not tp_vol:   _tp_missing.append(f"量能（需量比 ≥1.3，目前 {tp_vol_ratio}x）")
    if tp_score == 3:
        tp_supplement_html = ""
    elif _tp_missing:
        _missing_str = "、".join(_tp_missing)
        tp_supplement_html = (
            f'<div style="margin-top:10px;padding:10px 12px;background:#fefce8;border-radius:8px;border-left:3px solid #fbbf24;font-size:12px;color:#78350f;line-height:1.7">'
            f'📋 <b>多空雷達尚缺：</b>{_missing_str}，補齊代表多方條件更完整。</div>'
        )
    else:
        tp_supplement_html = ""

    # kbar tag 顏色：依多頭/空頭/中性
    _kbar_bullish_keys = ["錘頭","多頭吞噬","早晨之星","三紅兵","穿刺線","大紅棒","漲停","長下影紅K"]
    _kbar_bearish_keys = ["射擊之星","空頭吞噬","黃昏之星","三烏鴉","烏雲蓋頂","大黑棒","跌停","長上影黑K"]
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
    # 歷史回測顯示
    _bt = d.get("kbar_backtest")
    kbar_backtest_html = ""
    if _bt and _bt.get("total", 0) >= 2:
        _bt_color = "#4ade80" if _bt["win_pct"] >= 55 else ("#fbbf24" if _bt["win_pct"] >= 45 else "#f87171")
        kbar_backtest_html = (
            f'<div style="margin-top:8px;font-size:12px;color:var(--text3);padding:8px 10px;'
            f'background:var(--bg2);border-radius:6px;border-left:3px solid {_bt_color}">'
            f'📊 歷史回測：過去{_bt["total"]}次出現「{_bt["pattern"]}」'
            f'→ 隔日上漲 {_bt["ups"]} 次、下跌 {_bt["downs"]} 次'
            f'（上漲比例 <b style="color:{_bt_color}">{_bt["win_pct"]}%</b>，歷史統計不代表未來）</div>'
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
<!-- report_tpl:{_REPORT_TPL_VERSION} -->
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
<title>{stock_name}({stock_id}) 技術面觀察：多空雷達 × 支撐壓力 {report_date}｜線上有位</title>
<meta name="description" content="輸入股票代號，系統自動整理多空雷達、K棒型態、支撐壓力位、葛蘭碧訊號，一鍵產出完整報告。免費使用。還有 500+ 計算工具和全球彩票選號。">
<meta property="og:title" content="{stock_id} {stock_name} 分析報告">
<meta property="og:description" content="{trend}｜支撐 {support}｜壓力 {resistance}｜損益比 {rr_ratio:.2f}">
<meta property="og:type" content="article">
<link rel="canonical" href="{FRONTEND_URL}/report/{stock_id}">
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
/* 2026/09/14修正：帥哥鴻反饋「個股報告字體真的不好觀看，尤其是各解說下方」——
   算了一下WCAG對比度，原本10px斜體＋var(--blue)藍字再疊opacity:.8，在淺色卡片背景
   (--stat-bg:#f0ebe2)下實際對比度只有約2.6:1，遠低於小字必須達到的4.5:1標準，
   14個解說欄位全部受影響（支撐/壓力/停損/多空雷達四燈號/K棒型態/KD-MACD等每一段
   說明文字下方）。改用--text2（同背景下約8.9:1，遠超標準）、拿掉斜體（中文字用
   斜體瀏覽器只會做假斜體，中文字型本來就沒有斜體字重，效果是變醜不是變好讀）、
   拿掉opacity（避免疊加又把顏色洗淡）、字級10px→12px。 */
.stat-hint{{font-size:12px;color:var(--text2);margin-top:4px;line-height:1.45}}
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
    <div style="font-size:13px;color:var(--text3);margin-bottom:4px">分析日期：{report_date}</div>
    <div style="font-size:11px;color:var(--text3);margin-bottom:16px">資料來源：FinMind + Yahoo Finance｜K線 {len(d.get('bars', []))} 根</div>
    <div class="row">
      <div class="stat">
        <div class="stat-label">現價</div>
        <div class="stat-value" id="livePrice">{price}</div>
        <div style="font-size:13px;margin-top:3px;min-height:18px" id="liveChange"></div>
        <div class="stat-hint">盤中為即時報價，收盤後為最近兩根收盤價的漲跌幅</div>
      </div>
      <div class="stat">
        <div class="stat-label">趨勢</div>
        <div class="stat-value" style="font-size:15px;color:{ma_color}">{trend}</div>
        <div class="stat-hint">用道氏理論的波峰波谷判斷目前多空方向</div>
      </div>
      <div class="stat">
        <div class="stat-label">損益比</div>
        <div class="stat-value" style="color:{rr_color}">{rr_ratio:.2f}</div>
        <div class="stat-hint">潛在獲利÷潛在虧損，數字越高代表越划算</div>
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
          <div style="font-size:12px;font-weight:600;color:{tp_trend_color}">{trend} {tp_trend_icon}</div>
          <div style="font-size:12px;color:var(--text3);margin-top:2px">參考：MA20=<b>{tp_ma20}</b> / MA60=<b>{tp_ma60}</b></div>
          <div class="stat-hint">月線是否站上季線，判斷中期多空</div>
        </div>
        <div style="flex:1;min-width:100px;padding:8px 12px;border-radius:8px;background:{tp_macd_bg};text-align:center">
          <div style="font-size:11px;color:var(--text3);margin-bottom:3px">② MACD</div>
          <div style="font-size:12px;font-weight:600;color:{tp_macd_color}">動能{'↗' if tp_macd else '↘'} {tp_macd_icon}</div>
          <div style="font-size:12px;color:var(--text3);margin-top:2px">MACD柱體=<b>{tp_hist}</b></div>
          <div class="stat-hint">柱體翻正代表買方動能增強</div>
        </div>
        <div style="flex:1;min-width:100px;padding:8px 12px;border-radius:8px;background:{tp_vol_bg};text-align:center">
          <div style="font-size:11px;color:var(--text3);margin-bottom:3px">③ 資金籌碼</div>
          <div style="font-size:12px;font-weight:600;color:{tp_vol_color}">量{'放大' if tp_vol else '縮'} {tp_vol_icon}</div>
          <div style="font-size:12px;color:var(--text3);margin-top:2px">量比=<b>{tp_vol_ratio}x</b></div>
          <div class="stat-hint">近5日均量相對20日均量放大倍數</div>
        </div>
        <div style="flex:1;min-width:100px;padding:8px 12px;border-radius:8px;background:{tp_pos_bg};text-align:center">
          <div style="font-size:11px;color:var(--text3);margin-bottom:3px">④ 位置</div>
          <div style="font-size:12px;font-weight:600;color:{tp_pos_color}">{'適中' if tp_pos else '偏離'} {tp_pos_icon}</div>
          <div style="font-size:12px;color:var(--text3);margin-top:2px">MA5乖離=<b>{tp_bias5 if tp_bias5 is not None else '-'}%</b></div>
          <div class="stat-hint">現價偏離月均線太多代表追高風險高</div>
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
        <div class="stat-hint">股價較不容易跌破的價位，回測時是觀察多方能否守住的位置</div>
      </div>
      <div class="stat">
        <div class="stat-label">壓力位</div>
        <div class="stat-value" style="color:#fbbf24">{resistance}</div>
        <div style="font-size:11px;color:var(--text3);margin-top:2px">{res_desc}，距現價 +{res_dist}%</div>
        <div class="stat-hint">股價較不容易站穩突破的價位，是上漲的阻力</div>
      </div>
    </div>
    <div style="background:var(--stat-bg);border-radius:10px;padding:12px">
      <div class="stat-label" style="margin-bottom:4px">關鍵失效位置</div>
      <div style="font-size:18px;font-weight:700;color:#f87171">{stop_loss}</div>
      <div style="font-size:11px;color:var(--text3);margin-top:2px">距現價 -{stop_dist}%，跌破代表目前型態失效</div>
      <div class="stat-hint">收盤跌破代表目前技術型態不再成立</div>
    </div>
  </section>

  <!-- 3. 趨勢判斷 -->
  <section class="card" id="trend-analysis">
    <h2>趨勢判斷</h2>
    <div class="stat-hint" style="margin-bottom:8px">用道氏理論的波峰波谷結構判斷目前中長期多空方向</div>
    <div class="irow">
      <div class="idot" style="background:{ma_color}"></div>
      <div style="font-size:13px;line-height:1.6;color:var(--text)">{ma_text}</div>
    </div>
    <div style="padding:10px 0 0;font-size:13px;line-height:1.7;color:var(--text3)">{trend_desc}</div>
  </section>

  <!-- 4. K線型態 -->
  <section class="card" id="kline-pattern">
    <h2>K線型態</h2>
    <div class="stat-hint" style="margin-bottom:8px">今日蠟燭圖形狀所隱含的多空意義，經驗參考值為一般型態經驗，非本股統計</div>
    {kbar_tag_html}{kbar_warning_html}
    <div class="irow" style="border-bottom:none">
      <div class="idot" style="background:{kp_color}"></div>
      <div>
        <div style="font-size:14px;font-weight:600;color:{kp_color};margin-bottom:2px">{kline_pattern or "常態 K 線"}</div>
        <div style="font-size:12px;color:var(--text3)">型態經驗參考值 <span style="color:{wr_color};font-weight:700">{wr_pct}%</span></div>
      </div>
    </div>
    {kbar_action_html}{kbar_backtest_html}
  </section>

  <!-- 5. 動能指標 -->
  <section class="card" id="momentum">
    <h2>動能指標</h2>
    <div class="stat-hint" style="margin-bottom:8px">KD判斷短線超買超賣，MACD判斷多空動能，量能反映買賣力道強弱</div>
    {kd_row_html}{macd_row_html}{vol_row_html}
  </section>

  <!-- 6. 風險評估 -->
  <section class="card" id="risk-assessment">
    <h2>風險評估</h2>
    <div class="row" style="margin-bottom:12px">
      <div class="stat" style="flex:0 0 auto">
        <div class="stat-label">風險等級</div>
        <div class="stat-value" style="color:{risk_color}">{risk_label}</div>
        <div class="stat-hint">依失效位置距現價的百分比區分：5%內低、5~10%中、10%以上高</div>
      </div>
      <div class="stat" style="flex:0 0 auto">
        <div class="stat-label">損益比</div>
        <div class="stat-value" style="color:{rr_color}">{rr_ratio:.2f}</div>
        <div style="font-size:11px;color:var(--text3);margin-top:2px">{"良好" if rr_ratio >= 2 else ("尚可" if rr_ratio >= 1 else "偏低")}</div>
      </div>
    </div>
    <ul style="list-style:none">{risk_items_html}</ul>
    <div class="stat-hint">系統依技術面自動偵測到值得留意的風險與注意事項</div>
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
          <span style="padding:2px 8px;border-radius:20px;background:{tp_macd_bg};color:{tp_macd_color}">② 動能 {tp_macd_icon}</span>
          <span style="padding:2px 8px;border-radius:20px;background:{tp_vol_bg};color:{tp_vol_color}">③ 量能 {tp_vol_icon}</span>
          <span style="padding:2px 8px;border-radius:20px;background:{tp_pos_bg};color:{tp_pos_color}">④ 位置 {tp_pos_icon}</span>
        </div>
        <div style="margin-top:8px;font-size:11px;color:var(--text3)">
          MA5 乖離：<strong style="color:{_bias5_color}">{_bias5_str}</strong>
          &nbsp;｜&nbsp;MA20 乖離：<strong style="color:{_bias20_color}">{_bias20_str}</strong>
        </div>
      </div>
    </div>
  </section>

  <!-- 7. 觀察重點（2026/09/17 原「操作建議」）-->
  <section class="card" id="operation-advice">
    <h2>觀察重點</h2>
    <div class="stat-hint" style="margin-bottom:8px">綜合多空雷達、K棒型態與支撐壓力位置，整理目前成立的條件與失效位置，不構成投資建議</div>
    <div style="font-size:14px;line-height:1.8;color:var(--text);padding:12px;background:var(--stat-bg);border-radius:10px;white-space:pre-line">{op_text}</div>
    {tp_supplement_html}
    <div style="margin-top:12px;display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--text3)">
      <span>失效位置：<strong style="color:#f87171">{stop_loss}</strong></span>
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
            _render_email(
                title="密碼重設",
                title_icon="🔒",
                body_html=(
                    f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                    f'我們收到了您的密碼重設申請。請點擊下方按鈕設定新密碼，'
                    f'此連結的有效時間為 <b>1 小時</b>，逾時請重新申請。</p>'
                    f'<p style="color:#444;margin:0;font-size:13px;line-height:1.7;color:#888">'
                    f'若您並未申請重設密碼，可安心忽略此信，您的帳號密碼不會有任何變動。</p>'
                ),
                cta_text="重設密碼",
                cta_url=reset_url,
                with_ad=False,
                card_bg="#eff6ff", card_border="#bfdbfe", title_color="#1e40af",
            )
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
def report_generate(req: ReportReq, request: Request, user: dict = Depends(require_user)):
    if user.get("expire_at") and user["expire_at"] < _taipei_today() and not _is_referral_active(user) and user.get("plan") != "free":
        raise HTTPException(status_code=403, detail="訂閱已到期，請續費後繼續使用")
    allowed, used, limit = _check_daily_credit(request, user)
    if not allowed:
        raise HTTPException(status_code=403, detail=f"今日完整分析／健檢／報告次數已用完（{limit} 次）")

    stock_id = req.stock_id.strip().upper()
    report_date = _taipei_today()

    # 先拿最新分析（_do_analyze 本身有短TTL快取，不會每次都重打FinMind），
    # 用它的 price_basis_date 判斷同一天的報告快取是否已經過期（收盤基準換了新的一天）。
    # 2026/08/07 修正：原本先檢查 stock_reports 當日快取命中就直接return，完全不管
    # 快取當下的收盤資料是不是最新的，導致一大早（FinMind還沒更新前）產生的報告會
    # 整天卡在舊的收盤基準，即使資料源已經更新也不會反映。
    try:
        d = _do_analyze(stock_id, "D", user=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{e}")
    current_basis = d.get("price_basis_date")
    _consume_daily_credit(request, user)

    conn = _db_conn()
    cached = conn.execute(
        "SELECT report_html, price_basis_date FROM stock_reports WHERE stock_id=? AND report_date=?",
        (stock_id, report_date)
    ).fetchone()
    conn.close()
    _cached_html = cached["report_html"] or "" if cached else ""
    _is_current_tpl = f"report_tpl:{_REPORT_TPL_VERSION}" in _cached_html
    if cached and 'id="basic-info"' in _cached_html and _is_current_tpl:
        cached_basis = cached["price_basis_date"]
        # 舊資料沒有存 price_basis_date（None）時，維持舊行為直接信任快取，避免無謂重產生
        if cached_basis is None or cached_basis == current_basis:
            return {"ok": True, "url": f"{BACKEND_URL}/report/{stock_id}"}
        # 快取的收盤基準比現在舊 → 收盤資料已更新，強制重新產生
    elif cached:
        # 舊格式（無七欄位）或舊模板版本（少了report_tpl標記）→ 刪除快取，強制重新生成
        conn = _db_conn()
        conn.execute(
            "DELETE FROM stock_reports WHERE stock_id=? AND report_date=?",
            (stock_id, report_date)
        )
        conn.commit()
        conn.close()

    stock_name = d.get("stock_name", stock_id)
    news_items = _fetch_stock_news(stock_id)
    report_html = _inject_report_ads(_build_report_html(stock_id, stock_name, report_date, d, news_items))

    conn = _db_conn()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO stock_reports (stock_id, report_date, stock_name, report_html, price_basis_date) VALUES (?,?,?,?,?)",
            (stock_id, report_date, stock_name, report_html, current_basis)
        )
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

    return {"ok": True, "url": f"{BACKEND_URL}/report/{stock_id}"}


@app.get("/report/", include_in_schema=False)
def get_report_empty():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=FRONTEND_URL, status_code=301)

@app.get("/report/{slug}")
def get_report(slug: str):
    from fastapi.responses import HTMLResponse, RedirectResponse
    # 帶日期的舊 URL（如 /report/2330-2026-07-24）→ 301 到固定 URL
    m = _re.match(r"^([A-Za-z0-9]+)-(\d{4}-\d{2}-\d{2})$", slug)
    if m:
        return RedirectResponse(url=f"/report/{m.group(1).upper()}", status_code=301)

    stock_id = slug.upper()
    report_date = _taipei_today()

    # Validate stock code format (1-6 alphanumeric chars)
    if not _re.match(r"^[A-Z0-9]{1,6}$", stock_id):
        return HTMLResponse("<html><body><h1>404</h1><p>Invalid stock code.</p><a href='/'>← Home</a></body></html>", status_code=404)

    try:
        conn = _db_conn()
        # 只找「今天」的報告，且必須是最新模板版本才算數（今天以外一律視為過期，
        # 不能拿來當「已經有資料了」的理由）
        row = conn.execute(
            "SELECT report_html, report_date FROM stock_reports WHERE stock_id=? AND report_date=? ORDER BY created_at DESC LIMIT 1",
            (stock_id, report_date)
        ).fetchone()
        conn.close()
    except Exception:
        return HTMLResponse("<html><body><h1>503</h1><p>Service temporarily unavailable.</p><a href='/'>← Home</a></body></html>", status_code=503)

    # 舊模板版本的快取（沒有 report_tpl 標記）視同沒有，強制走下面的即時產生，
    # 不然改版面/文案後，公開頁會一直卡在改版前的舊HTML，要等使用者剛好重新
    # 觸發 report_generate 才會更新，不夠即時。
    if row and f"report_tpl:{_REPORT_TPL_VERSION}" not in (row["report_html"] or ""):
        row = None

    if row:
        # 今天已經有（模板版本正確的）報告了，直接用，不用每次都重新分析。
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

    # 2026/08/16修正：以前的邏輯是「今天沒有就找最舊的一筆頂著用」，結果只要
    # 這支股票曾經產生過報告，就會被那筆舊資料卡住，下面的「即時產生」永遠
    # 排不到——像2545、6770、3481這種不在每日批次200支名單內、也沒被使用者
    # 觸發過report_generate()重新整理的冷門股，就會一直顯示很舊的分析日期。
    # 改成「今天沒有現成的就先試著即時產生」，只有即時產生本身失敗（例如上游
    # FinMind暫時取不到資料）才退回舊資料頂著，總比開天窗好；同時把失敗原因
    # print出來，才看得到Zeabur log，不然完全不知道是為什麼退回舊資料。
    try:
        d = _do_analyze(stock_id, "D", user=None)
        stock_name = d.get("stock_name", stock_id)
        news_items = _fetch_stock_news(stock_id)
        html = _inject_report_ads(_build_report_html(stock_id, stock_name, report_date, d, news_items))
        conn = _db_conn()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO stock_reports (stock_id, report_date, stock_name, report_html, price_basis_date) VALUES (?,?,?,?,?)",
                (stock_id, report_date, stock_name, html, d.get("price_basis_date"))
            )
            conn.commit()
        except Exception:
            pass
        finally:
            conn.close()
        html = html.replace('</body>', REPORT_INJECT + '</body>', 1)
        return HTMLResponse(content=html)
    except Exception as e:
        print(f"[get_report] {stock_id} 即時分析失敗，退回舊資料頂著顯示：{e}")
        # 即時產生失敗，退回資料庫裡「最新的一筆」（不限日期）頂著顯示，
        # 至少讓使用者看到舊分析，而不是直接404。
        try:
            conn = _db_conn()
            fallback_row = conn.execute(
                "SELECT report_html, report_date FROM stock_reports WHERE stock_id=? ORDER BY report_date DESC, created_at DESC LIMIT 1",
                (stock_id,)
            ).fetchone()
            conn.close()
        except Exception:
            fallback_row = None
        if fallback_row:
            html = fallback_row["report_html"] or ""
            html = html.replace('</body>', REPORT_INJECT + '</body>', 1)
            return HTMLResponse(content=html)
        raise HTTPException(status_code=404, detail=f"無法取得 {stock_id} 報告：{e}")


# ══════════════════════════════════════════════════════════
# SEO：/picks + /rankings + sitemap.xml
# ══════════════════════════════════════════════════════════

@app.get("/picks")
def picks_page():
    """每日條件篩選台股 SSR 頁（公開，15分鐘快取；2026/09/17 改稱條件篩選，不稱精選）"""
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
                entry_tag += '<span style="font-size:10px;padding:2px 8px;border-radius:20px;background:rgba(0,229,160,.15);color:#00e5a0;font-weight:600;margin-left:4px">訊號1</span>'
            if "buy2" in entry_sigs:
                entry_tag += '<span style="font-size:10px;padding:2px 8px;border-radius:20px;background:rgba(251,191,36,.15);color:#fbbf24;font-weight:600;margin-left:4px">訊號2</span>'
            risk_row = ""
            if is_buy2_only:
                _sup = p.get("support", "-")
                risk_row = f'<tr><td colspan="4" style="padding:0 14px 10px;font-size:12px;color:#fbbf24">⚠️ 高風險突破型態，跌破近期低點 {_sup} 元代表突破失敗。</td></tr>'
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
        "name": f"台股條件篩選名單 {date_str} — 線上有位",
        "description": f"依均線金叉、KD指標、量能、MACD篩選的台股強勢候選，{date_str} 共 {count} 支",
        "url": f"{BACKEND_URL}/picks",
        "numberOfItems": count,
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "url": f"{BACKEND_URL}/report/{p['stock_id']}",
             "name": f"{p['stock_id']} {p.get('stock_name','')}"}
            for i, p in enumerate(picks)
        ],
    }, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>今日條件篩選結果｜均線、KD、量能同時轉強的台股 {date_str}｜線上有位</title>
<meta name="description" content="系統每日依均線金叉、KD黃金交叉、量能放大等條件篩選台股，列出符合條件的股票與訊號說明。{date_str} 共 {count} 支符合。還有 500+ 免費計算工具。">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{BACKEND_URL}/picks">
<meta property="og:title" content="今日條件篩選結果 {date_str}｜線上有位">
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
  <h1>📈 每日條件篩選結果</h1>
  <p class="sub">資料日期：{generated_at or "尚未產生"}・每日 16:30 更新・共 {count} 支符合條件</p>
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

    # 取得已成功產生過報告的股票清單
    # 2026/07/28修正：原本用 get_all_stock_info() 把全市場股票全部塞進 sitemap。
    # 其中少數股票即時產報時抓不到資料（例如1230似乎抓不TWSE資料），
    # 讓Google爬到後回傳404，被記錄為 coverage 問題。
    # 改成只列已經在 stock_reports 表確認成功過的代號，保證 sitemap 網址100%打得開。
    # 未來有新產報成功會隨 SEO_CACHE 過期重新產生時自動補上，不需人工操作。
    try:
        conn2 = _db_conn()
        all_stock_ids = [r[0] for r in conn2.execute(
            "SELECT DISTINCT stock_id FROM stock_reports"
        ).fetchall()]
        conn2.close()
        if not all_stock_ids:
            all_stock_ids = _SEO_HARDCODED_STOCKS
    except Exception:
        all_stock_ids = _SEO_HARDCODED_STOCKS

    locs = []
    for u in [FRONTEND_URL + "/", FRONTEND_URL + "/stock/", FRONTEND_URL + "/rankings",
              FRONTEND_URL + "/multi-signal"]:   # 2026/09/17：12金叉選股公開頁（取代已下架的 /deep-analysis）
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

    # ── Lottery 彩票頁（動態掃描磁碟，多語言）──
    _lottery_base = os.path.join(os.path.dirname(__file__), "frontend", "lottery")
    if os.path.isdir(_lottery_base):
        locs.append(f"  <url><loc>{FRONTEND_URL}/lottery/</loc><changefreq>daily</changefreq><priority>0.8</priority></url>")
        for _lf in sorted(os.listdir(_lottery_base)):
            if _lf.endswith(".html") and _lf != "index.html":
                locs.append(f'  <url><loc>{FRONTEND_URL}/lottery/{_lf}</loc><changefreq>daily</changefreq><priority>0.7</priority></url>')
        for _lang_dir in sorted(os.listdir(_lottery_base)):
            _lang_path = os.path.join(_lottery_base, _lang_dir)
            if os.path.isdir(_lang_path) and _lang_dir not in (".", "..", "data"):
                for _lf in sorted(os.listdir(_lang_path)):
                    if _lf.endswith(".html"):
                        locs.append(f'  <url><loc>{FRONTEND_URL}/lottery/{_lang_dir}/{_lf}</loc><changefreq>daily</changefreq><priority>0.6</priority></url>')

    # ── Games 小遊戲專區（2026/08/15 新增，動態掃描磁碟）──
    # connect-four.html 已改成導向 gomoku.html 的redirect頁（不是真的遊戲頁面），
    # sitemap不應該收錄，避免搜尋引擎把一個空的導向頁當成正式頁面索引。
    _games_base = os.path.join(os.path.dirname(__file__), "frontend", "games")
    _games_sitemap_exclude = {"index.html", "connect-four.html"}
    if os.path.isdir(_games_base):
        locs.append(f"  <url><loc>{FRONTEND_URL}/games/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>")
        for _gmf in sorted(os.listdir(_games_base)):
            if _gmf.endswith(".html") and _gmf not in _games_sitemap_exclude:
                locs.append(f"  <url><loc>{FRONTEND_URL}/games/{_gmf}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>")
        # 2026/08/17 新增：各語言版本遊戲頁（shared/ 底下只有共用JS不是頁面，要排除）
        for _lang_dir in sorted(os.listdir(_games_base)):
            _lang_path = os.path.join(_games_base, _lang_dir)
            if os.path.isdir(_lang_path) and _lang_dir not in (".", "..", "shared"):
                locs.append(f"  <url><loc>{FRONTEND_URL}/games/{_lang_dir}/</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>")
                for _gmf in sorted(os.listdir(_lang_path)):
                    if _gmf.endswith(".html") and _gmf not in _games_sitemap_exclude:
                        locs.append(f"  <url><loc>{FRONTEND_URL}/games/{_lang_dir}/{_gmf}</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>")

    # 熱門股優先 priority 0.8，其餘 0.6
    hardcoded_set = set(_SEO_HARDCODED_STOCKS)
    for sid in all_stock_ids:
        priority = "0.8" if sid in hardcoded_set else "0.6"
        locs.append(f"  <url><loc>{FRONTEND_URL}/report/{sid}</loc><changefreq>daily</changefreq><priority>{priority}</priority></url>")
    # 不再列帶日期的 URL（舊 URL 已由路由 301 到固定 URL）

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
<meta name="description" content="台股今日漲幅榜、跌幅榜、成交量榜 Top 20，即時更新。搭配個股技術分析報告（多空雷達＋K棒型態＋支撐壓力），一鍵查看任一股。">
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
    # 2026/09/17：銷售頁填的發票載具（手機條碼／Email），原本沒存，管理員信一直顯示「未提供」
    _inv_t = str(body.get("invoice_type") or "").strip()
    _inv_c = str(body.get("invoice_carrier") or "").strip()[:100]
    if _inv_t == "phone" and _re.fullmatch(r"/[0-9A-Z.+\-]{7}", _inv_c.upper()):
        invoice_type, invoice_carrier = "手機條碼載具", _inv_c.upper()
    elif _inv_t == "email" and _re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", _inv_c):
        invoice_type, invoice_carrier = "Email載具", _inv_c.lower()
    else:
        invoice_type, invoice_carrier = "", ""

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
    # P0 fail-closed: do not emit checkout without ECPay secrets
    if not ECPAY_HASH_KEY or not ECPAY_HASH_IV:
        raise HTTPException(status_code=400, detail="Payment gateway not configured")
    if not ECPAY_MERCHANT_ID:
        raise HTTPException(status_code=400, detail="Payment merchant not configured")

    # 2026/09/17新增：防止重複訂閱／重複付款
    # ① 已是有效付費會員 → 不再產生新的定期定額（否則會變成兩筆訂閱、每期扣兩次）
    _dup_conn = _db_conn()
    _mem = _dup_conn.execute("SELECT plan, expire_at, merchant_trade_no FROM members WHERE email=?", (email,)).fetchone()
    _recent = _dup_conn.execute(
        "SELECT merchant_trade_no FROM pending_orders WHERE email=? AND merchant_trade_no LIKE 'XYWR%' "
        "AND created_at >= datetime('now','+8 hours','-30 minutes') ORDER BY created_at DESC LIMIT 3",
        (email,)
    ).fetchall()
    _dup_conn.close()
    # （2026/09/17：只擋「定期訂閱中」的會員；福利／手動贈送天數的會員可以訂閱，天數會接在後面）
    if (_mem and _mem["plan"] != "free" and (_mem["expire_at"] or "") >= _taipei_today()
            and str(_mem["merchant_trade_no"] or "").startswith("XYWR") and plan != "daily_test"):
        raise HTTPException(
            status_code=409,
            detail=f"您目前已是付費會員（到期日 {_mem['expire_at']}），定期訂閱會自動續約，不需要重複購買。"
                   f"如有疑問請來信 wation168@gmail.com"
        )
    # ② 30分鐘內已有訂單且綠界查得到「已付款」→ 付款其實成功了，只是開通通知還在路上，擋下第二次刷卡
    for _r in _recent:
        if await _asyncio.to_thread(_ecpay_trade_paid, _r["merchant_trade_no"]):
            raise HTTPException(
                status_code=409,
                detail="您剛才的付款已經成功，系統正在開通中，請勿重複付款。"
                       "請約1分鐘後重新整理頁面；若5分鐘後仍未開通，請來信 wation168@gmail.com"
            )

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
        # 2026/09/17：付款完成回到 App（會自動輪詢確認開通狀態），不再回銷售頁
        "ClientBackURL":       f"{FRONTEND_URL}/stock/?pay=done",
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
    # P0: always record pending for upgrades (password optional for logged-in App flow)
    _po_conn = _db_conn()
    _hashed = _hash_pw(password) if password and len(password) >= 6 else ""
    _po_conn.execute(
        "INSERT OR REPLACE INTO pending_orders "
        "(merchant_trade_no, email, hashed_password, plan, invoice_type, invoice_carrier, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        # 2026/09/17：正式站舊資料表的 created_at 預設是 UTC，明確寫入台北時間，防重複下單的時間判斷才準
        (trade_no, email, _hashed, plan, invoice_type, invoice_carrier, _taipei_now_str())
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
    # 2026/09/17修正（重複扣款事件根因）：綠界第一次通知的內容是「未編碼的UTF-8中文」
    # （例如 RtnMsg=交易成功），Starlette 的 request.form() 會用 latin-1 解碼成亂碼
    # （äº¤æ...），導致簽章永遠對不上→被拒絕→客人付款後沒升級；綠界約10幾分鐘後
    # 重送時 RtnMsg 改成英文 paid 才驗過。客人在這段空窗以為沒成功又刷第二次。
    # 改成自己讀原始內容、用 UTF-8 解析，第一次通知就能驗過、即時開通。
    params = _parse_ecpay_body(await request.body())
    print(f"[定期定額 Webhook] {params}")

    # 驗證 CheckMacValue 簽章（邏輯全在 ecpay_verify.py；缺模組／驗簽失敗一律拒）
    # P0: verification module required; empty secrets / bad sig handled inside check_webhook (fail-closed)
    if _ecpay_verify_mod is None:
        print("[定期定額] FATAL: ecpay_verify module missing; refusing webhook")
        return PlainTextResponse(content="0|Error")
    if not _ecpay_verify_mod.check_webhook(
        params, ECPAY_HASH_KEY, ECPAY_HASH_IV, DB_PATH, "ecpay_recurring"
    ):
        return PlainTextResponse(content="0|Error")

    if params.get("MerchantID") != ECPAY_MERCHANT_ID:
        print(f"[定期定額] ❌ MerchantID 不符")
        return PlainTextResponse(content="0|Error")

    rtn_code = params.get("RtnCode", "0")
    if rtn_code != "1":
        print(f"[定期定額] 非成功狀態 RtnCode={rtn_code}，略過")
        return PlainTextResponse(content="1|OK")

    email        = params.get("CustomField1", "").strip().lower()
    trade_no_w   = params.get("MerchantTradeNo", "")
    amount       = params.get("PeriodAmount", "") or params.get("TradeAmt", "") or params.get("Amount", "") or "0"
    item_name    = params.get("ItemName", "")
    # 2026/09/17修正：首期通知（ReturnURL）帶 PaymentDate；第2期起的續約通知（PeriodReturnURL）
    # 綠界文件列的是 ProcessDate/Gwsr/TotalSuccessTimes，沒有 PaymentDate。原本冪等 key 只用
    # PaymentDate，續約時永遠是空字串 → 第3期起會被當成「重複通知」略過、不延長到期日。
    payment_date = params.get("PaymentDate", "") or params.get("ProcessDate", "")
    is_renewal   = (not params.get("PaymentDate")) and bool(params.get("ProcessDate") or params.get("Gwsr") or params.get("TotalSuccessTimes"))
    period_no    = params.get("TotalSuccessTimes", "") or ("" if is_renewal else "1")
    ecpay_tx_no  = params.get("TradeNo", "") or params.get("Gwsr", "") or params.get("gwsr", "")
    idem_key     = f"R_{trade_no_w}_{payment_date}" if payment_date else \
                   f"R_{trade_no_w}_{ecpay_tx_no}_{params.get('TotalSuccessTimes', '')}"

    if not email:
        print("[定期定額] ❌ email 為空")
        return PlainTextResponse(content="1|OK")

    # 冪等保護
    _tmp = _db_conn()
    _already = _tmp.execute(
        "SELECT 1 FROM processed_orders WHERE merchant_trade_no=?",
        (idem_key,)
    ).fetchone()
    _po = _tmp.execute(
        "SELECT hashed_password, invoice_type, invoice_carrier, plan, created_at FROM pending_orders WHERE merchant_trade_no=?", (trade_no_w,)
    ).fetchone()
    # 同一個 Email 近24小時建立了幾筆訂單（給管理員判斷是否重複下單）
    try:
        _recent_orders = _tmp.execute(
            "SELECT COUNT(*) FROM pending_orders WHERE email=? AND created_at >= datetime('now','+8 hours','-24 hours')",
            (email,)
        ).fetchone()[0]
    except Exception:
        _recent_orders = 0
    _tmp.close()
    _inv_type    = (_po["invoice_type"]    or "電子發票") if _po else "電子發票"
    _inv_carrier = (_po["invoice_carrier"] or "未提供")   if _po else "未提供"

    if _already:
        print(f"[定期定額] ⚠️ 重複 Webhook {trade_no_w} key={idem_key}")
        return PlainTextResponse(content="1|OK")
    # 先搶下處理權（避免綠界重送／補單排程同時處理，造成天數加兩次）
    _claim = _db_conn()
    _claimed = _claim.execute(
        "INSERT OR IGNORE INTO processed_orders (merchant_trade_no) VALUES (?)", (idem_key,)
    ).rowcount
    _claim.commit()
    _claim.close()
    if not _claimed:
        print(f"[定期定額] ⚠️ 同一筆正在／已經處理 {trade_no_w} key={idem_key}")
        return PlainTextResponse(content="1|OK")

    # 判斷天數與方案：優先用下單時記錄的方案（最可靠），沒有才用 item_name + 金額判斷
    _amount_int = int(amount) if str(amount).isdigit() else 0
    _plan_day_map = {"monthly": 30, "quarterly": 90, "yearly": 365, "daily_test": 1}
    _po_plan = (_po["plan"] if _po else "") or ""
    if _po_plan in _plan_day_map:
        plan = _po_plan
        days = _plan_day_map[plan]
    else:
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

    _today_tw = _taipei_today()
    prev_plan   = row["plan"] if row else ""
    prev_expire = (row["expire_at"] if row else "") or ""
    prev_trade  = (row["merchant_trade_no"] if row else "") or ""
    # 疑似重複訂閱：這是「首期」通知，但會員早就有另一筆仍有效的定期定額訂單
    dup_warning = bool(
        row and not is_renewal and prev_trade.startswith("XYWR") and prev_trade != trade_no_w
        and prev_plan != "free" and prev_expire >= _today_tw
    )

    if row:
        # 既有會員：延長到期日
        current_expire = prev_expire or _today_tw
        base = max(current_expire, _today_tw)
        new_expire = (datetime.fromisoformat(base) + timedelta(days=days)).strftime("%Y-%m-%d")
        # 重複訂閱時，會員綁定的訂單編號維持第一筆（之後退刷／停用的是新這筆）
        keep_trade = prev_trade if dup_warning else trade_no_w
        conn.execute(
            "UPDATE members SET plan=?, expire_at=?, merchant_trade_no=? WHERE email=?",
            (plan, new_expire, keep_trade, email)
        )
        conn.commit()
        conn.close()
        # 寄續約通知信
        _send_email(email, "【線上有位】自動續約成功",
            _render_email(
                title="自動續約成功",
                title_icon="✅",
                body_html=(
                    f'<p style="color:#444;margin:0 0 8px;font-size:14px;line-height:1.7">親愛的會員您好，</p>'
                    f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                    f'您的{plan_label}已透過綠界定期定額，於今日完成本期自動扣款與續約。感謝您持續支持線上有位，'
                    f'您的完整會員功能不中斷，可繼續使用即時個股分析、深度選股、到價提醒等服務。</p>'
                    f'<table style="width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden">'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">方案</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{plan_label}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">本期扣款金額</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">NT${amount}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">新到期日</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{new_expire}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">發票開立方式</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{_inv_type}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px">載具／統編</td><td style="padding:10px 14px;font-weight:700;font-size:14px;text-align:right">{_inv_carrier}</td></tr>'
                    f'</table>'
                    f'<div style="background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:14px 16px;margin-top:16px">'
                    f'<p style="margin:0;font-size:13px;color:#92400e;line-height:1.7">'
                    f'<b>關於自動續約：</b>本方案為定期定額，系統會於每期到期時自動扣款續約，您無需手動操作。'
                    f'若您日後想停止自動續約，可登入會員中心點選「取消訂閱」，或來信客服協助辦理，'
                    f'取消後現有效期仍可使用至到期日為止。</p></div>'
                ),
                cta_text="立即使用",
                cta_url=f"{FRONTEND_URL}/stock",
                with_ad=True,
                card_bg="#f0fdf4", card_border="#86efac", title_color="#166534",
            )
        )
    else:
        # 首次授權成功（第一期）：建立帳號
        # P0 follow-up: empty pending password must not become empty members.password
        _pending_hash = (_po["hashed_password"] if _po else "") or ""
        hashed_password = _pending_hash if _pending_hash else _hash_pw(secrets.token_urlsafe(8))
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
            try:  # 釋放處理權，讓綠界重送或補單排程還能再處理
                _rel = _db_conn()
                _rel.execute("DELETE FROM processed_orders WHERE merchant_trade_no=?", (idem_key,))
                _rel.commit()
                _rel.close()
            except Exception:
                pass
            return PlainTextResponse(content="1|OK")
        conn.close()
        _send_email(email, "【線上有位】歡迎！您的帳號已開通（定期訂閱）",
            _render_email(
                title="歡迎加入！帳號已開通",
                title_icon="🎉",
                body_html=(
                    f'<p style="color:#444;margin:0 0 8px;font-size:14px;line-height:1.7">親愛的會員您好，</p>'
                    f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                    f'感謝您訂閱線上有位！您的定期訂閱首期扣款已完成，帳號已正式開通，'
                    f'即刻起可登入使用即時個股分析、深度選股、到價提醒等完整會員功能。</p>'
                    f'<table style="width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden">'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">帳號</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{email}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">密碼</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">您訂購時自行設定的密碼</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">方案</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{plan_label}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">本期扣款金額</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">NT${amount}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">到期日</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{new_expire}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px;border-bottom:1px solid #f0f0f0">發票開立方式</td><td style="padding:10px 14px;font-weight:700;font-size:14px;border-bottom:1px solid #f0f0f0;text-align:right">{_inv_type}</td></tr>'
                    f'<tr><td style="padding:10px 14px;color:#888;font-size:13px">載具／統編</td><td style="padding:10px 14px;font-weight:700;font-size:14px;text-align:right">{_inv_carrier}</td></tr>'
                    f'</table>'
                    f'<div style="background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:14px 16px;margin-top:16px">'
                    f'<p style="margin:0;font-size:13px;color:#92400e;line-height:1.7">'
                    f'<b>關於定期訂閱：</b>本方案為定期定額，系統將於每期到期時自動扣款續約，您無需手動操作。'
                    f'若日後想停止，可登入會員中心點選「取消訂閱」，取消後現有效期仍可使用至到期日為止。</p></div>'
                ),
                cta_text="立即登入使用",
                cta_url=f"{FRONTEND_URL}/stock",
                with_ad=True,
                card_bg="#f0fdf4", card_border="#86efac", title_color="#166534",
            )
        )

    # 記錄已處理
    _rec = _db_conn()
    _rec.execute("INSERT OR IGNORE INTO processed_orders (merchant_trade_no) VALUES (?)",
                 (idem_key,))
    _rec.commit()
    _rec.close()

    # 管理員通知（2026/09/17 帥哥鴻反映內容太少，補齊客人與訂單資訊）
    try:
        if ADMIN_NOTIFY_EMAIL:
            _send_admin_payment_notice(
                email=email, trade_no=trade_no_w, ecpay_tx_no=ecpay_tx_no, amount=amount,
                plan_label=plan_label, is_renewal=is_renewal, period_no=period_no,
                pay_time=payment_date, payment_type=params.get("PaymentType", ""),
                prev_plan=prev_plan, prev_expire=prev_expire, prev_trade=prev_trade,
                new_expire=new_expire, is_new_account=not bool(row),
                inv_type=_inv_type, inv_carrier=_inv_carrier,
                recent_orders=_recent_orders, dup_warning=dup_warning,
                simulate=params.get("SimulatePaid", "") == "1",
            )
    except Exception as _ae:
        print(f"[定期定額] 管理員通知寄送失敗：{_ae}")

    return PlainTextResponse(content="1|OK")


def _send_admin_payment_notice(**d):
    """付款成功的管理員通知信（完整客人＋訂單資訊，方便直接對帳/回覆客人）"""
    import html as _h
    email = d["email"]
    conn = _db_conn()
    m = conn.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()
    conn.close()
    m = dict(m) if m else {}
    if m.get("line_user_id"):
        login_way = "LINE 登入"
    elif email.endswith("@gmail.com"):
        login_way = "Google 或 Email 密碼（Gmail 信箱）"
    else:
        login_way = "Email 密碼"
    plan_names = {"free": "免費會員", "monthly": "月費", "quarterly": "季費", "yearly": "年費", "daily_test": "每日測試"}
    if d["dup_warning"]:
        kind = "⚠️ 疑似重複訂閱（客人已有另一筆有效訂閱）"
    elif d["is_renewal"]:
        kind = f"自動續約（第 {d['period_no'] or '?'} 期）"
    else:
        kind = "首期付款・新開通" if d["is_new_account"] else "首期付款・既有帳號升級"
    rows = [
        ("事件", kind),
        ("會員 Email", email),
        ("會員編號", m.get("id", "")),
        ("暱稱", m.get("nickname") or "（未設定）"),
        ("帳號建立時間", m.get("created_at", "")),
        ("最後登入", m.get("last_login") or ""),
        ("登入方式", login_way),
        ("方案", d["plan_label"]),
        ("本次金額", f"NT${d['amount']}"),
        ("付款時間", d["pay_time"]),
        ("付款方式", d["payment_type"] or "信用卡"),
        ("本站訂單編號", d["trade_no"]),
        ("綠界交易序號", d["ecpay_tx_no"]),
        ("付款前方案／到期日", f"{plan_names.get(d['prev_plan'], d['prev_plan'] or '（新帳號）')}／{d['prev_expire'] or '—'}"),
        ("付款前綁定訂單", d["prev_trade"] or "—"),
        ("新到期日", d["new_expire"]),
        ("發票方式／載具", f"{d['inv_type']}／{d['inv_carrier']}"),
        ("此 Email 近24小時建立訂單數", d["recent_orders"]),
    ]
    if d.get("simulate"):
        rows.insert(0, ("注意", "綠界模擬付款（非真實扣款）"))
    tr = "".join(
        f'<tr><td style="padding:6px 10px;color:#666;border-bottom:1px solid #eee;white-space:nowrap">{_h.escape(str(k))}</td>'
        f'<td style="padding:6px 10px;border-bottom:1px solid #eee;font-weight:600">{_h.escape(str(v))}</td></tr>'
        for k, v in rows
    )
    warn = ""
    if d["dup_warning"]:
        warn = (
            '<div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:12px;margin:12px 0;color:#991b1b">'
            f'<b>這位客人已有有效訂閱（{_h.escape(d["prev_trade"])}），這筆 {_h.escape(d["trade_no"])} 很可能是重複付款。</b><br>'
            '處理方式：①到綠界後台對「本站訂單編號」這筆辦理退刷，並停用這筆定期定額 → '
            '②到本站管理後台「📅 設定到期日」查詢這位客人，把到期日調回正確日期、綁定訂單選仍有效的那筆。</div>'
        )
    body = (
        f'<div style="font-family:sans-serif;padding:16px;max-width:640px">'
        f'<h3 style="margin:0 0 8px">【線上有位】定期定額付款通知</h3>{warn}'
        f'<table style="border-collapse:collapse;font-size:14px;width:100%">{tr}</table>'
        f'<p style="font-size:12px;color:#888;margin-top:12px">持卡人姓名、手機、卡號末四碼綠界不會在通知中提供，'
        f'請到綠界廠商後台用「本站訂單編號」查詢。<br>'
        f'管理後台：<a href="{FRONTEND_URL}/admin.html">{FRONTEND_URL}/admin.html</a></p></div>'
    )
    prefix = "⚠️重複訂閱" if d["dup_warning"] else ("續約" if d["is_renewal"] else "新訂閱")
    _send_email(ADMIN_NOTIFY_EMAIL, f"【{prefix}】{email} {d['plan_label']} NT${d['amount']}", body)


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
    today_str = _taipei_today()
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
                _render_email(
                    title="定期訂閱已取消",
                    title_icon="📭",
                    body_html=(
                        f'<p style="color:#444;margin:0 0 12px;font-size:14px;line-height:1.7">親愛的會員您好，</p>'
                        f'<p style="color:#444;margin:0 0 16px;font-size:14px;line-height:1.7">'
                        f'您的定期訂閱已成功取消，系統之後不會再自動扣款。'
                        f'您本期已付費的剩餘天數（至 <b>{member["expire_at"]}</b>）仍可正常使用所有會員功能，不受影響。</p>'
                        f'<p style="color:#444;margin:0;font-size:14px;line-height:1.7">'
                        f'感謝您這段時間的支持。若您日後想重新啟用，隨時可以再次於網站訂閱，'
                        f'期待再次為您服務。若有任何問題，也歡迎來信客服。</p>'
                    ),
                    cta_text="重新訂閱",
                    cta_url=f"{FRONTEND_URL}/stock/landing#pricing",
                    with_ad=True,
                    card_bg="#fef2f2", card_border="#fca5a5", title_color="#991b1b",
                    accent="#ef4444",
                )
            )
            # 管理員通知
            try:
                if ADMIN_NOTIFY_EMAIL:
                    _send_email(ADMIN_NOTIFY_EMAIL, f"【取消訂閱】{email}",
                        f"<p>{email} 已取消定期訂閱</p><p>到期日：{member['expire_at']}</p>")
            except Exception:
                pass
            return JSONResponse(content={"ok": True, "msg": "已成功取消定期訂閱"})
        else:
            print(f"[取消定期定額] 綠界回應異常: {result}")
            raise HTTPException(status_code=500, detail="取消失敗，請聯繫客服 wation168@gmail.com")
    except httpx.TimeoutException:
        raise HTTPException(status_code=500, detail="連線綠界逾時，請稍後再試")


# ══════════════════════════════════════════════════════════════
# 持股健檢 API
# ══════════════════════════════════════════════════════════════

@app.get("/portfolio")
def get_portfolio(current_user: dict = Depends(get_current_user)):
    """取得用戶持股清單（2026/09/15改為讀取watchlist_items裡有填股數/買入價的項目，
    詳見/portfolio/add與文件A決策③——持股健檢不再是獨立的portfolios表）"""
    email = current_user["email"]
    conn = _db_conn()
    rows = conn.execute(
        "SELECT stock_id, stock_name, cost_price, shares, created_at FROM watchlist_items "
        "WHERE user_email=? AND cost_price IS NOT NULL AND cost_price>0 ORDER BY created_at",
        (email,)
    ).fetchall()
    conn.close()
    return {"ok": True, "data": [dict(r) for r in rows]}


@app.post("/portfolio/add")
async def add_portfolio(request: Request, current_user: dict = Depends(get_current_user)):
    """新增持股。2026/09/15修正（文件A決策③，帥哥鴻拍板）：持股健檢改用自選股資料，
    這裡新增/更新的其實是watchlist_items同一檔自選股的股數/買入價欄位，不再是獨立的
    portfolios表——這檔股票如果本來不在自選清單裡，會順便一併加入（預設族群）；
    本來就在自選清單裡的話，直接補上股數/買入價，不影響原本的族群設定。"""
    email   = current_user["email"]
    is_paid = _ws_is_paid(current_user)
    body    = await request.json()
    stock_id   = str(body.get("stock_id", "")).strip()
    cost_price = float(body.get("cost_price", 0))
    stock_name = str(body.get("stock_name", "")).strip()
    try:
        shares = float(body.get("shares")) if body.get("shares") not in (None, "") else None
    except Exception:
        shares = None

    if not stock_id or cost_price <= 0:
        raise HTTPException(status_code=400, detail="請輸入正確的股號與成本價")

    # 名稱轉代號：非純數字視為中文股名，從對照表解析（比照 create_alert 的作法）
    # 若不轉換，中文股名會被直接存進 watchlist_items，之後每次持股分析都會拿中文去組
    # 外部 API 網址，造成 UnicodeEncodeError 並反覆失敗
    if not stock_id.replace(".", "").isdigit():
        resolved = _name_to_code.get(stock_id)
        if not resolved:
            resolved = next((code for name, code in _name_to_code.items() if stock_id in name), None)
        if resolved:
            stock_id = resolved
        else:
            raise HTTPException(status_code=404, detail=f"找不到股票：{stock_id}")
    stock_id = stock_id.upper()

    # 2026/09/14修正（案件004持股健檢範圍測試發現，帥哥鴻真實帳號實測輸入不存在的代號
    # 「99999」也能成功新增）：上面只檢查輸入格式是否為純數字／能否從公司名稱對照表解析，
    # 從未確認這個代號「實際存在且查得到資料」——純數字但根本不是真實股票代號（如打錯字）
    # 會直接跳過驗證，寫進DB後永久卡在持股清單裡，/portfolio/analysis每次都查不到報價／
    # K線，畫面上現價、支撐壓力、KD、MACD全部顯示「—」，使用者也無法從畫面判斷是自己打錯
    # 代號還是系統故障。修法：比照portfolio_analysis自己判斷「這檔股票查不查得到資料」的
    # 方式（fetch_df_finmind近3個月K線，空dataframe＝查無此股），新增前先驗證一次，
    # 查無資料就直接回404，理由訊息比照/api/analyze既有的「找不到股票」措辭，行為保持一致。
    try:
        _add_check_df = fetch_df_finmind(stock_id, "3mo", "D")
    except Exception:
        _add_check_df = None
    if _add_check_df is None or _add_check_df.empty:
        raise HTTPException(status_code=404, detail=f"找不到股票：{stock_id}，請確認代號是否正確")

    conn = _db_conn()
    existing = conn.execute(
        "SELECT id, cost_price FROM watchlist_items WHERE user_email=? AND stock_id=?",
        (email, stock_id)
    ).fetchone()
    already_holding = bool(existing and existing["cost_price"])
    # 免費會員限 1 支（已經是持股的話只是改股數/成本價，不算新增一支，不受限制）
    if not is_paid and not already_holding:
        holding_count = conn.execute(
            "SELECT COUNT(*) FROM watchlist_items WHERE user_email=? AND cost_price IS NOT NULL AND cost_price>0",
            (email,)
        ).fetchone()[0]
        if holding_count >= 1:
            conn.close()
            raise HTTPException(status_code=403, detail="免費版最多追蹤 1 支，升級付費方案可無限新增")
    try:
        if existing:
            conn.execute(
                "UPDATE watchlist_items SET cost_price=?, shares=? WHERE user_email=? AND stock_id=?",
                (cost_price, shares, email, stock_id)
            )
        else:
            count = conn.execute(
                "SELECT COUNT(*) FROM watchlist_items WHERE user_email=?", (email,)
            ).fetchone()[0]
            if count >= WATCHLIST_MAX:
                conn.close()
                raise HTTPException(status_code=400, detail=f"自選股最多 {WATCHLIST_MAX} 檔，請先移除幾檔再新增")
            conn.execute(
                "INSERT INTO watchlist_items (user_email, stock_id, stock_name, group_name, added_date, cost_price, shares) "
                "VALUES (?,?,?,?,?,?,?)",
                (email, stock_id, stock_name, "預設", _taipei_today(), cost_price, shares)
            )
        conn.commit()
    except HTTPException:
        raise
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()

    return {"ok": True, "msg": f"已新增 {stock_id}"}


@app.delete("/portfolio/{stock_id}")
def delete_portfolio(stock_id: str, current_user: dict = Depends(get_current_user)):
    """移除持股健檢追蹤。2026/09/15修正（文件A決策③）：改為清空watchlist_items這檔股票的
    股數/買入價欄位，不再整筆刪除——這檔股票如果本來也在自選股清單，仍會保留在自選股裡，
    只是不再納入持股健檢（回到單純自選觀察）。"""
    email = current_user["email"]
    conn = _db_conn()
    conn.execute(
        "UPDATE watchlist_items SET cost_price=NULL, shares=NULL WHERE user_email=? AND stock_id=?",
        (email, stock_id)
    )
    conn.commit()
    conn.close()
    return {"ok": True, "msg": f"已移除 {stock_id} 的持股健檢追蹤"}


@app.get("/portfolio/analysis")
async def portfolio_analysis(request: Request, current_user: dict = Depends(require_user)):
    """批次分析持股。免費與分析共用 daily_credit，每次載入扣1（45秒去重）。
    2026/09/15修正（文件A決策③，帥哥鴻拍板）：資料來源改成watchlist_items裡有填
    cost_price（買入價）的項目，不再是獨立的portfolios表——「持股」現在就是「有填股數/
    買入價的自選股」，沒填的自選股不會出現在這裡。"""
    allowed, used, limit = _check_daily_credit(request, current_user)
    if not allowed:
        return _quota_429(
            "today_limit",
            f"今日完整分析／健檢次數已用完（{limit} 次）",
            used, limit,
        )
    import sys as _sys
    _picker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker")
    if _picker_path not in _sys.path:
        _sys.path.insert(0, _picker_path)

    email = current_user["email"]
    conn = _db_conn()
    rows = conn.execute(
        "SELECT stock_id, stock_name, cost_price, shares FROM watchlist_items "
        "WHERE user_email=? AND cost_price IS NOT NULL AND cost_price>0 ORDER BY id",
        (email,)
    ).fetchall()
    conn.close()

    if not rows:
        return {"ok": True, "data": []}

    results = []
    for row in rows:
        sid        = row["stock_id"]
        cost_price = row["cost_price"]
        shares     = row["shares"]
        stock_name = row["stock_name"] or ""
        # 若名稱與股號相同或空白，從即時報價補抓名稱
        if not stock_name or stock_name == sid:
            stock_name = sid  # 預設先用股號

        # 取即時報價：優先走 get_quote（TWSE MIS → FinMind 備援），比 get_quote_live 更可靠
        # 2026/07/30 改用共用函式，get_quote_live 備援邏輯保留不動
        _qd = None
        try:
            def _safe_price(v):
                try:
                    f = float(v)
                    return f if f > 0 else None
                except Exception:
                    return None
            _qd = _get_live_quote_data(sid)
            if _qd:
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
                    _uc.execute("UPDATE watchlist_items SET stock_name=? WHERE user_email=? AND stock_id=?",
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
        # 2026/09/14修正（案件004持股健檢範圍測試發現，帥哥鴻真實帳號實測台積電change_pct
        # 顯示0導致前端「今日漲跌」那行整個消失）：這裡原本完全沒用上面第10589行已經呼叫過
        # 的_get_live_quote_data()結果（_qd，裡面本來就含TWSE優先/FinMind備援抓到的
        # change_pct），而是另外重新查一次_QUOTE_CACHE原始快取——_qd是None時（代表上面已經
        # 退回get_quote_live()這條備援路徑）_QUOTE_CACHE根本不會有這檔的資料，就算_qd有值，
        # 也可能在兩次查詢之間快取剛好過期，兩種情況都會讓change_pct靜默變回0.0。
        # 修法：優先直接用_qd裡已經抓到的change_pct，那是跟上面price同一次抓到、保證新鮮的
        # 資料；只有_qd整個沒拿到時，才退回原本用_QUOTE_CACHE手動算的邏輯當最後手段。
        change_pct = 0.0
        try:
            if _qd and _qd.get("change_pct") is not None:
                change_pct = float(_qd.get("change_pct"))
            else:
                _qd2 = (_QUOTE_CACHE.get(sid.upper()) or {}).get("data") or {}
                _y = float(_qd2.get("y") or 0)
                if _y > 0 and price > 0:
                    change_pct = round((price - _y) / _y * 100, 2)
        except Exception:
            pass

        # 損益金額（2026/09/15新增：現在有股數資料了，可以算實際損益金額，不只是%數）
        pnl_amount = round((price - cost_price) * shares, 0) if (shares and price > 0) else None

        results.append({
            "stock_id":        sid,
            "stock_name":      stock_name,
            "cost_price":      cost_price,
            "shares":          shares,
            "pnl_amount":      pnl_amount,
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

    _consume_portfolio_daily_credit(request, current_user)
    return {"ok": True, "data": results}


# ══════════════════════════════════════════════════════════════
# 自選股 API（2026/09/13新增）
# 背景：自選股功能明明要求登入才能加入/移除，卻從頭到尾只存在瀏覽器localStorage，
# 從未真正跟帳號綁定——同一個人在別的裝置或瀏覽器登入，自選股清單就整組消失。
# 帥哥鴻反饋後決定「全部修正」：已登入用戶一律走這裡的DB，不再是純前端假象。
# 沿用/portfolio*系列端點同樣的require_user（未登入直接401，不像get_current_user
# 那樣可能回傳None讓呼叫端誤用而炸500）、_db_conn()、try/except→HTTPException(500)風格。
# ══════════════════════════════════════════════════════════════

WATCHLIST_MAX = 30  # 比照前端watchList.length>30的舊上限，伺服器端也要擋，不能只信任前端


def _ws_group_names(conn, email: str) -> list:
    """族群名稱清單：「預設」永遠排最前面，即使該用戶在watchlist_groups裡還沒有任何紀錄
    （比照前端getWatchGroupNames()的預設補值邏輯，兩邊行為要一致）。"""
    rows = conn.execute(
        "SELECT group_name FROM watchlist_groups WHERE user_email=? ORDER BY created_at, id",
        (email,)
    ).fetchall()
    return ["預設"] + [r["group_name"] for r in rows if r["group_name"] != "預設"]


def _ws_list_data(conn, email: str) -> list:
    """自選股清單，新到舊排序（比照前端addWatch()用unshift塞在最前面的慣例）。
    2026/09/15新增：一併帶出shares/cost_price（持股健檢用的選填股數/買入價，
    見/api/watchlist/add與/portfolio/analysis），前端watchList項目會多這兩個欄位。"""
    rows = conn.execute(
        "SELECT stock_id, stock_name, group_name, added_date, shares, cost_price FROM watchlist_items "
        "WHERE user_email=? ORDER BY id DESC",
        (email,)
    ).fetchall()
    return [
        {"id": r["stock_id"], "name": r["stock_name"], "group": r["group_name"], "date": r["added_date"],
         "shares": r["shares"], "cost_price": r["cost_price"]}
        for r in rows
    ]


def _ws_is_paid(current_user: dict) -> bool:
    """動態計算是否為有效付費會員（members表無is_active欄位，需即時計算）。
    比照原本/portfolio/add既有的算法（2026/09/15持股健檢併入自選股資料後抽成共用函式，
    給/api/watchlist/add跟/portfolio/add的免費會員1支持股健檢限制共用）。"""
    today_str = _taipei_today()
    plan      = current_user.get("plan", "free")
    expire_at = current_user.get("expire_at") or ""
    return (plan != "free") and bool(expire_at) and (expire_at >= today_str)


@app.get("/api/watchlist")
def get_watchlist(current_user: dict = Depends(require_user)):
    """取得目前登入用戶的自選股清單與族群名稱"""
    email = current_user["email"]
    conn = _db_conn()
    data = _ws_list_data(conn, email)
    group_names = _ws_group_names(conn, email)
    conn.close()
    return {"ok": True, "data": data, "group_names": group_names}


@app.post("/api/watchlist/add")
async def add_watchlist(request: Request, current_user: dict = Depends(require_user)):
    """新增一檔自選股（對應前端addWatch()）。
    2026/09/15新增（文件A決策③，帥哥鴻拍板）：body可選帶shares（股數）／cost_price（買入價），
    有帶cost_price就視為同時把這檔設定成「持股健檢」追蹤標的——免費會員最多1支（比照原本
    portfolios表的限制），已經是持股的話覆蓋原本沒有限制（改股數/成本價不算新增一支）。
    沒帶cost_price（一般的「加自選」按鈕，多選Modal等）完全不受影響，行為跟以前一樣。"""
    email = current_user["email"]
    body = await request.json()
    stock_id = str(body.get("id", "")).strip().upper()
    stock_name = str(body.get("name", "")).strip()
    added_date = str(body.get("date", "")).strip() or _taipei_today()
    group = str(body.get("group", "")).strip() or "預設"
    if not stock_id:
        raise HTTPException(status_code=400, detail="缺少股票代號")

    def _to_float_or_none(v):
        try:
            f = float(v)
            return f if f > 0 else None
        except Exception:
            return None
    cost_price = _to_float_or_none(body.get("cost_price"))
    shares     = _to_float_or_none(body.get("shares"))

    conn = _db_conn()
    existing = conn.execute(
        "SELECT id, cost_price FROM watchlist_items WHERE user_email=? AND stock_id=?",
        (email, stock_id)
    ).fetchone()
    if not existing:
        count = conn.execute(
            "SELECT COUNT(*) FROM watchlist_items WHERE user_email=?", (email,)
        ).fetchone()[0]
        if count >= WATCHLIST_MAX:
            conn.close()
            raise HTTPException(status_code=400, detail=f"自選股最多 {WATCHLIST_MAX} 檔，請先移除幾檔再新增")
    already_holding = bool(existing and existing["cost_price"])
    if cost_price and not already_holding and not _ws_is_paid(current_user):
        holding_count = conn.execute(
            "SELECT COUNT(*) FROM watchlist_items WHERE user_email=? AND cost_price IS NOT NULL AND cost_price>0",
            (email,)
        ).fetchone()[0]
        if holding_count >= 1:
            conn.close()
            raise HTTPException(status_code=403, detail="免費版最多追蹤 1 支持股健檢，升級付費方案可無限新增")
    try:
        # INSERT OR IGNORE：已存在的股票不覆蓋既有的族群設定，只是單純確保這檔在清單裡
        conn.execute(
            "INSERT OR IGNORE INTO watchlist_items (user_email, stock_id, stock_name, group_name, added_date) "
            "VALUES (?,?,?,?,?)",
            (email, stock_id, stock_name, group, added_date)
        )
        if cost_price:
            # 不管是剛剛才INSERT進去、還是本來就在清單裡，這裡都要把股數/買入價補上去
            conn.execute(
                "UPDATE watchlist_items SET cost_price=?, shares=? WHERE user_email=? AND stock_id=?",
                (cost_price, shares, email, stock_id)
            )
        if group not in ("預設", "全部"):
            conn.execute(
                "INSERT OR IGNORE INTO watchlist_groups (user_email, group_name) VALUES (?,?)",
                (email, group)
            )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()
    return {"ok": True, "msg": f"已加入 {stock_id}"}


@app.delete("/api/watchlist/{stock_id}")
def delete_watchlist(stock_id: str, current_user: dict = Depends(require_user)):
    """移除一檔自選股（對應前端removeWatch()）"""
    email = current_user["email"]
    conn = _db_conn()
    conn.execute(
        "DELETE FROM watchlist_items WHERE user_email=? AND stock_id=?",
        (email, stock_id.strip().upper())
    )
    conn.commit()
    conn.close()
    return {"ok": True, "msg": f"已移除 {stock_id}"}


@app.post("/api/watchlist/group")
async def set_watchlist_group(request: Request, current_user: dict = Depends(require_user)):
    """更新單一自選股所屬族群（對應前端setStockGroup()）。若指定的族群是還沒建立過的
    自訂族群，這裡順便補建，讓「只靠改股票族群、沒特別去建立族群」建出來的空族群也能留存。"""
    email = current_user["email"]
    body = await request.json()
    stock_id = str(body.get("stock_id", "")).strip().upper()
    group = str(body.get("group", "")).strip() or "預設"
    if not stock_id:
        raise HTTPException(status_code=400, detail="缺少股票代號")

    conn = _db_conn()
    try:
        conn.execute(
            "UPDATE watchlist_items SET group_name=? WHERE user_email=? AND stock_id=?",
            (group, email, stock_id)
        )
        if group not in ("預設", "全部"):
            conn.execute(
                "INSERT OR IGNORE INTO watchlist_groups (user_email, group_name) VALUES (?,?)",
                (email, group)
            )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()
    return {"ok": True}


@app.post("/api/watchlist/group/add")
async def add_watchlist_group(request: Request, current_user: dict = Depends(require_user)):
    """新增一個尚未指派任何股票的空族群（對應前端addWatchGroupName()）"""
    email = current_user["email"]
    body = await request.json()
    name = str(body.get("name", "")).strip()
    if not name:
        raise HTTPException(status_code=400, detail="請輸入族群名稱")
    if name in ("預設", "全部"):
        # 這兩個名稱本來就永遠存在（見_ws_group_names），視同已建立成功
        return {"ok": True}
    conn = _db_conn()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO watchlist_groups (user_email, group_name) VALUES (?,?)",
            (email, name)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()
    return {"ok": True}


@app.post("/api/watchlist/group/rename")
async def rename_watchlist_group(request: Request, current_user: dict = Depends(require_user)):
    """族群改名（對應前端renameWatchGroupName()）：「預設」「全部」不可改名，
    改名後同步更新所有屬於這個族群的自選股，整段包在同一個connection裡一起commit。"""
    email = current_user["email"]
    body = await request.json()
    old_name = str(body.get("old_name", "")).strip()
    new_name = str(body.get("new_name", "")).strip()
    if not old_name or not new_name:
        raise HTTPException(status_code=400, detail="缺少族群名稱")
    if old_name in ("預設", "全部"):
        raise HTTPException(status_code=400, detail="「預設」與「全部」不可改名")

    conn = _db_conn()
    try:
        conn.execute(
            "UPDATE watchlist_groups SET group_name=? WHERE user_email=? AND group_name=?",
            (new_name, email, old_name)
        )
        conn.execute(
            "UPDATE watchlist_items SET group_name=? WHERE user_email=? AND group_name=?",
            (new_name, email, old_name)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=400, detail="已經有相同名稱的族群了")
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()
    return {"ok": True}


@app.post("/api/watchlist/group/delete")
async def delete_watchlist_group(request: Request, current_user: dict = Depends(require_user)):
    """刪除族群（對應前端deleteWatchGroupName()）：「預設」「全部」不可刪除；
    被刪除族群內的股票歸回「預設」，股票本身不會被移除，整段包在同一個connection裡一起commit。"""
    email = current_user["email"]
    body = await request.json()
    name = str(body.get("name", "")).strip()
    if not name:
        raise HTTPException(status_code=400, detail="缺少族群名稱")
    if name in ("預設", "全部"):
        raise HTTPException(status_code=400, detail="「預設」與「全部」不可刪除")

    conn = _db_conn()
    try:
        conn.execute(
            "UPDATE watchlist_items SET group_name='預設' WHERE user_email=? AND group_name=?",
            (email, name)
        )
        conn.execute(
            "DELETE FROM watchlist_groups WHERE user_email=? AND group_name=?",
            (email, name)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()
    return {"ok": True}


@app.post("/api/watchlist/merge")
async def merge_watchlist(request: Request, current_user: dict = Depends(require_user)):
    """登入後一次性把瀏覽器localStorage裡（此功能修正前留下、或離線時沒同步到）的自選股／
    族群併入伺服器帳號資料。原則：伺服器已有的資料優先（INSERT OR IGNORE，不讓過時的本地
    資料蓋掉其他裝置已經做的族群調整或刪除），local端超過30檔上限的部分不併入。
    完成後直接回傳跟GET /api/watchlist一樣的合併後結果，前端可以直接拿來取代記憶體狀態，
    不用再多打一次GET。"""
    email = current_user["email"]
    body = await request.json()
    items = body.get("items") or []
    group_names = body.get("group_names") or []
    if not isinstance(items, list):
        items = []
    if not isinstance(group_names, list):
        group_names = []

    conn = _db_conn()
    try:
        for g in group_names:
            g = str(g or "").strip()
            if not g or g in ("預設", "全部"):
                continue
            conn.execute(
                "INSERT OR IGNORE INTO watchlist_groups (user_email, group_name) VALUES (?,?)",
                (email, g)
            )

        existing_count = conn.execute(
            "SELECT COUNT(*) FROM watchlist_items WHERE user_email=?", (email,)
        ).fetchone()[0]
        for it in items:
            if existing_count >= WATCHLIST_MAX:
                break  # 伺服器端上限：local端多出來的部分不併入，不能只信任前端
            if not isinstance(it, dict):
                continue
            stock_id = str(it.get("id", "")).strip().upper()
            if not stock_id:
                continue
            stock_name = str(it.get("name", "")).strip()
            group = str(it.get("group", "")).strip() or "預設"
            added_date = str(it.get("date", "")).strip() or _taipei_today()
            cur = conn.execute(
                "INSERT OR IGNORE INTO watchlist_items "
                "(user_email, stock_id, stock_name, group_name, added_date) VALUES (?,?,?,?,?)",
                (email, stock_id, stock_name, group, added_date)
            )
            if cur.rowcount:
                existing_count += 1
            if group not in ("預設", "全部"):
                conn.execute(
                    "INSERT OR IGNORE INTO watchlist_groups (user_email, group_name) VALUES (?,?)",
                    (email, group)
                )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

    data = _ws_list_data(conn, email)
    names = _ws_group_names(conn, email)
    conn.close()
    return {"ok": True, "data": data, "group_names": names}


# ══════════════════════════════════════════════════════════════
# 深度選股端點
# ══════════════════════════════════════════════════════════════

@app.get("/deep-analysis")
def deep_analysis_page():
    """2026/09/17：深度選股已下架，舊網址（官網、文章、LINE舊訊息裡的連結）一律轉到12金叉選股公開頁"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/multi-signal", status_code=301)


def _deep_is_premium(user: dict | None) -> bool:
    """深度選股完整代號：與 _is_premium 同一套。"""
    return _is_premium(user)


def _deep_mask_item(item: dict) -> dict:
    """
    伺服器端遮罩單筆深度選股結果。

    只把「股票代號」與「股票名稱」換成遮罩字串，其餘欄位（現價/支撐/壓力/停損/
    信心/風險/量比/警示等）原樣保留——與前端 showDeepAnalysisPage() 只對
    stock_id / stock_name 套用 blur 的顯示行為完全一致，免費會員畫面不會有落差。

    另外會掃過所有字串欄位（含 list / dict 巢狀），把可能夾帶在文字裡的真實代號或
    名稱一併替換，避免有人從 warnings / score_factors 這類敘述欄位反推出是哪一檔。
    """
    if not isinstance(item, dict):
        return item

    MASK = "＊＊＊＊"
    real_id = str(item.get("stock_id") or "")
    real_name = str(item.get("stock_name") or "")

    def _scrub(v):
        if isinstance(v, str):
            if real_id:
                v = v.replace(real_id, MASK)
            if real_name:
                v = v.replace(real_name, MASK)
            return v
        if isinstance(v, list):
            return [_scrub(x) for x in v]
        if isinstance(v, dict):
            return {k: _scrub(x) for k, x in v.items()}
        return v

    masked = {k: _scrub(v) for k, v in item.items()}
    masked["stock_id"] = MASK
    masked["stock_name"] = MASK
    masked["masked"] = True
    return masked


@app.get("/api/deep-analysis")
def api_deep_analysis(user: dict | None = Depends(get_current_user)):
    """2026/09/17：深度選股已下架，舊版前端（使用者瀏覽器快取）若還呼叫這裡，直接回傳12金叉資料"""
    return api_multi_signal(user)


@app.get("/deep-analysis-status")
def deep_analysis_status():
    """首頁跑馬燈用的輕量狀態（2026/09/17起改讀12金叉；只有今天的資料才 available）"""
    return multi_signal_status()


# ══════════════════════════════════════════════════════════
# 12金叉選股法（文件B十四～十六節，2026/09/15新增）
# 每個方法對候選池每檔股票各自判斷「通過/未通過」，寫進multi_signal_results，
# 2026/09/17起深度選股下架，12金叉選股正式接手（LINE推播、公開頁 /multi-signal、首頁入口）。
#
# 判斷標準（2026/09/15帥哥鴻拍板）：每個方法都必須是「當天」發生的金叉/突破/轉強，
# 不往回找、不加低檔條件——目標是找出今天剛轉強的機會股。
# 唯一例外是基本面：月營收一個月才公布一次，沒有「每天」可言。2026/09/17帥哥鴻改定義：
# 原本「最新月營收年增由負轉正」會踩到內線先拉、營收公布剛好利多出盡，改成
# 「最近3個月營收都年增，但股價還沒漲（近20天漲幅<10%、不在近60日高檔）」，條件成立期間每天都算。
#
# 12個方法：技術面9（MACD/KD/RSI/月季線/海龜/趨勢/量能/布林/OBV）＋籌碼面1（法人）
#           ＋型態面1（W底/頭肩底突破頸線）＋基本面1（營收成長但股價未漲）
# ══════════════════════════════════════════════════════════

MULTI_SIGNAL_CFG = {
    "candidate_n":       150,   # 候選池：成交量前150檔（上市+上櫃，文件B十六節拍板）
    "history_days":      200,   # 抓幾個日曆天的日K（約135個交易日）
    "min_bars":          80,    # 交易日數不足這個數就整檔跳過
    "cross_lookback":    1,     # MACD/KD/月季線/OBV：只認當天穿越
    "rsi_mid":           50,    # RSI：當天由50以下往上穿越50
    "turtle_entry":      20,    # 海龜：當天收盤突破「前20日最高價」
    "turtle_exit":       10,    # 海龜：跌破前10日最低價＝出場線（記錄供參考）
    "turtle_lookback":   1,     # 海龜：只認當天剛突破
    "turtle_long_entry": 55,    # 海龜系統二（55日），只記錄供參考
    "vol_ratio":         1.3,   # 量能：5日均量/20日均量 當天由<1.3升到≥1.3（沿用原多空雷達門檻）
    "obv_ma":            20,    # OBV：當天向上穿越自己的20日均線
    "inst_buy_days":     3,     # 法人：三大法人合計「連買3天」成立的當天
    "zz_pct":            4.0,   # 型態：ZigZag轉折門檻（%）
    "pattern_bottom_tol": 4.0,  # W底：兩個底相差幾%以內算同一價位
    "pattern_shoulder_tol": 6.0,  # 頭肩底：左右肩相差幾%以內
    "api_delay":         0.35,  # 每檔間隔秒數（跟深度選股同款節流）
    # 2026/09/17新增
    "state_lookback":    20,    # 個股解析「轉強中」：最近幾個交易日內轉強、而且現在還維持
    "rev_months":        3,     # 基本面：最近幾個月營收年增都要>0
    "rev_max_gain20":    10.0,  # 基本面：近20個交易日漲幅要小於幾%（還沒被拉過）
    "rev_max_pos60":     60.0,  # 基本面：收盤價在近60日高低區間的位置要在幾%以下（不在高檔）
}

# method代碼 → (中文名稱, 類別)。類別是交叉統計「涵蓋幾個類別」用的。
MULTI_SIGNAL_METHODS = {
    "macd":        ("MACD金叉",     "技術面"),
    "kd":          ("KD金叉",       "技術面"),
    "rsi":         ("RSI突破50",    "技術面"),
    "ma_cross":    ("月季線金叉",   "技術面"),
    "turtle":      ("海龜突破",     "技術面"),
    "trend":       ("趨勢轉多",     "技術面"),
    "volume":      ("量能放大",     "技術面"),
    "bollinger":   ("布林突破",     "技術面"),
    "obv":         ("OBV轉強",      "技術面"),
    "institution": ("法人連買",     "籌碼面"),
    "pattern":     ("底部型態突破", "型態面"),
    "revenue":     ("營收成長・股價未漲", "基本面"),
}

MULTI_SIGNAL_FREE_MAX = 2   # 免費會員看得到「同時符合幾個以下」的股票（2026/09/17帥哥鴻拍板）

_MULTI_SIGNAL_STATUS = {"running": False, "started_at": None, "finished_at": None,
                        "scan_date": None, "total": 0, "done": 0, "ok": 0,
                        "skipped": 0, "failed": 0, "rows": 0, "errors": [], "msg": ""}
import threading as _ms_threading
_MULTI_SIGNAL_LOCK = _ms_threading.Lock()


def _ms_num(x):
    """numpy/None → 可存DB/JSON的float（NaN/inf回傳None）"""
    try:
        f = float(x)
    except Exception:
        return None
    if np.isnan(f) or np.isinf(f):
        return None
    return round(f, 4)


def _find_cross_index(fast, slow, lookback: int):
    """
    通用金叉判斷（文件B十五節1定案標準：只看當下位置，不做延遲確認）：
      ① 現在 fast 必須在 slow 之上，否則直接回傳 None
      ② 往回 lookback 個交易日內，找「最近一次」fast 由下往上穿越 slow 的索引
      ③ 從穿越那天到現在，fast 不可再跌回 slow 之下（含等於）
    lookback=1 就是「只認今天這根K棒剛穿越」。
    邏輯跟 stock_picker/finmind_filter.py 的 _find_ma_golden_cross_index 一致，
    這裡是可吃 numpy 陣列（含NaN）的通用版，供 MACD、KD、OBV 共用。
    """
    n = min(len(fast), len(slow))
    if n < 2:
        return None

    def _bad(v):
        return v is None or (isinstance(v, float) and np.isnan(v)) or \
            (isinstance(v, np.floating) and np.isnan(v))

    if _bad(fast[n - 1]) or _bad(slow[n - 1]) or fast[n - 1] <= slow[n - 1]:
        return None
    start = max(1, n - lookback)
    cross_idx = None
    for i in range(start, n):
        if _bad(fast[i]) or _bad(slow[i]) or _bad(fast[i - 1]) or _bad(slow[i - 1]):
            continue
        if fast[i - 1] <= slow[i - 1] and fast[i] > slow[i]:
            cross_idx = i
    if cross_idx is None:
        return None
    for i in range(cross_idx, n):
        if _bad(fast[i]) or _bad(slow[i]):
            continue
        if fast[i] <= slow[i]:
            return None
    return cross_idx


def _calc_atr(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 20):
    """ATR（Wilder平滑），海龜法則的N值。資料不足回傳None。"""
    n = len(closes)
    if n < period + 1:
        return None
    tr = np.maximum(highs[1:] - lows[1:],
                    np.maximum(np.abs(highs[1:] - closes[:-1]), np.abs(lows[1:] - closes[:-1])))
    atr = float(np.mean(tr[:period]))
    for v in tr[period:]:
        atr = (atr * (period - 1) + float(v)) / period
    return atr


def _turtle_breakout(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray,
                     entry: int, exit_: int, lookback: int):
    """
    海龜系統一（Donchian通道）突破判斷：
      ① 突破日：當天收盤價 > 前 entry 日（不含當天）最高價，且前一天還沒突破
      ② 取最近 lookback 個交易日內「最近一次」突破（lookback=1＝只認今天）
      ③ 突破後到今天，任何一天收盤價 < 前 exit_ 日最低價 ＝ 海龜出場，訊號失效
    回傳 (突破日索引 or None, 突破當天的通道上緣價)
    註：原版海龜是盤中觸價進出場，這裡是收盤後批次排程，統一用收盤價判斷。
    """
    n = len(closes)
    if n < entry + 2:
        return None, None

    def _is_break(i):
        if i - entry < 0:
            return False
        return closes[i] > float(np.max(highs[i - entry:i]))

    start = max(entry + 1, n - lookback)
    bi = None
    for i in range(start, n):
        if _is_break(i) and not _is_break(i - 1):
            bi = i
    if bi is None:
        return None, None
    level = float(np.max(highs[bi - entry:bi]))
    for j in range(bi + 1, n):
        if j - exit_ < 0:
            continue
        if closes[j] < float(np.min(lows[j - exit_:j])):
            return None, level
    return bi, level


def _zigzag_pivots(highs: np.ndarray, lows: np.ndarray, pct: float):
    """
    ZigZag轉折點（文件B十節：圖表型態辨識的第一步）。
    價格從上一個極值反向走超過 pct% 才確認一個轉折。
    回傳 (已確認的轉折list[(idx, price, 'H'/'L')], 目前進行中那一段的方向'up'/'down'/None)。
    最後一段還在進行中的極值（尚未被反向確認）不會放進list。
    """
    n = len(highs)
    if n < 3:
        return [], None
    th = pct / 100.0
    pivots = []
    trend = None
    hi_i, lo_i = 0, 0
    for i in range(1, n):
        if trend is None:
            if highs[i] > highs[hi_i]:
                hi_i = i
            if lows[i] < lows[lo_i]:
                lo_i = i
            if highs[hi_i] >= lows[lo_i] * (1 + th) and lo_i < hi_i:
                pivots.append((lo_i, float(lows[lo_i]), "L"))
                trend = "up"
            elif lows[lo_i] <= highs[hi_i] * (1 - th) and hi_i < lo_i:
                pivots.append((hi_i, float(highs[hi_i]), "H"))
                trend = "down"
        elif trend == "up":
            if highs[i] > highs[hi_i]:
                hi_i = i
            elif lows[i] <= highs[hi_i] * (1 - th):
                pivots.append((hi_i, float(highs[hi_i]), "H"))
                trend = "down"
                lo_i = i
        else:
            if lows[i] < lows[lo_i]:
                lo_i = i
            elif highs[i] >= lows[lo_i] * (1 + th):
                pivots.append((lo_i, float(lows[lo_i]), "L"))
                trend = "up"
                hi_i = i
    return pivots, trend


def _detect_bottom_pattern(highs, lows, closes, cfg):
    """
    底部型態＋「當天」突破頸線（文件B十節：ZigZag轉折＋幾何規則比對）。
    目前涵蓋兩種最常見的底部轉強型態：
      W底（雙重底）：…L1 → H1 → L2，兩個底相差 ≤ pattern_bottom_tol%，頸線＝H1
      頭肩底        ：…L1 → H1 → L2(頭) → H2 → L3，頭比兩肩低≥3%，
                      左右肩相差 ≤ pattern_shoulder_tol%，頸線＝H1、H2較高者
    通過條件：今天收盤 > 頸線、昨天收盤 ≤ 頸線（今天剛突破），
              且型態右底之後到昨天都沒有收盤站上過頸線（不是突破後拉回再突破）。
    回傳 dict（有找到）或 None。
    """
    n = len(closes)
    if n < 30:
        return None
    # 只看到昨天為止的轉折（今天的K棒是用來判斷突破，不拿來當型態的一部分）
    pivots, _ = _zigzag_pivots(highs[:-1], lows[:-1], cfg["zz_pct"])
    # 目前這段在往上走時，最後一個已確認轉折是底(L)；若最後是H代表正在下跌段，不可能今天突破頸線
    if not pivots or pivots[-1][2] != "L":
        return None
    c_now, c_prev = float(closes[-1]), float(closes[-2])

    def _fresh_break(neck, after_idx):
        if not (c_now > neck >= c_prev):
            return False
        seg = closes[after_idx + 1:n - 1]
        return not (len(seg) and float(np.max(seg)) > neck)

    found = None
    # 頭肩底優先（型態較完整）
    if len(pivots) >= 5:
        (l1i, l1, _), (h1i, h1, _), (l2i, l2, _), (h2i, h2, _), (l3i, l3, _) = pivots[-5:]
        shoulder_diff = abs(l1 - l3) / min(l1, l3) * 100
        if (l2 <= min(l1, l3) * 0.97 and shoulder_diff <= cfg["pattern_shoulder_tol"]
                and n - 1 - l1i <= 120):
            neck = max(h1, h2)
            if _fresh_break(neck, l3i):
                found = {"type": "頭肩底", "neckline": round(neck, 2),
                         "left_shoulder": round(l1, 2), "head": round(l2, 2),
                         "right_shoulder": round(l3, 2), "start_idx": l1i}
    if not found and len(pivots) >= 3:
        (l1i, l1, _), (h1i, h1, _), (l2i, l2, _) = pivots[-3:]
        bottom_diff = abs(l1 - l2) / min(l1, l2) * 100
        if bottom_diff <= cfg["pattern_bottom_tol"] and 5 <= l2i - l1i <= 80:
            neck = h1
            if _fresh_break(neck, l2i):
                found = {"type": "W底", "neckline": round(neck, 2),
                         "bottom1": round(l1, 2), "bottom2": round(l2, 2), "start_idx": l1i}
    if found:
        low = min(v for k, v in found.items() if k in ("bottom1", "bottom2", "head"))
        found["target"] = round(found["neckline"] * 2 - low, 2)   # 等幅測量目標價（頸線＋型態深度）
    return found


def _ms_http_get(url: str, timeout: int = 15) -> bytes:
    """抓證交所/櫃買/公開資訊觀測站資料用。證交所憑證偶爾驗證失敗，失敗時退回不驗證的連線。"""
    import urllib.request as _ur_ms
    req = _ur_ms.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with _ur_ms.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception:
        with _ur_ms.urlopen(req, timeout=timeout, context=_TWSE_SSL_CTX) as r:
            return r.read()


def _ms_int(s) -> int:
    try:
        return int(float(str(s).replace(",", "").replace("+", "").strip() or 0))
    except Exception:
        return 0


def _ms_fetch_institutional_bulk(scan_date: str, days: int) -> dict:
    """
    一次抓全市場三大法人買賣超（證交所T86＋櫃買中心），不逐檔打FinMind，
    避免跟17:00深度選股搶FinMind每小時額度。每個交易日只要2次請求。
    從scan_date往回找，湊滿 days 個有資料的交易日（最多往回看15個日曆天）。
    回傳 {"dates": [新→舊], "data": {stock_id: {date: 三大法人合計(張，保留1位小數，不足1張的買賣超也保留正負號)}}}
    """
    from datetime import date as _d_ms, timedelta as _td_ms
    out: dict = {}
    got_dates = []
    d = _d_ms.fromisoformat(scan_date)
    for _ in range(15):
        if len(got_dates) >= days:
            break
        if d.weekday() < 5:
            ds = d.isoformat()
            day_rows = {}
            try:
                j = _json_mod.loads(_ms_http_get(
                    f"https://www.twse.com.tw/rwd/zh/fund/T86?date={d.strftime('%Y%m%d')}"
                    f"&selectType=ALLBUT0999&response=json"))
                if str(j.get("stat", "")).upper() == "OK":
                    for row in j.get("data") or []:
                        if row and len(row) >= 3:
                            day_rows[str(row[0]).strip()] = round(_ms_int(row[-1]) / 1000, 1)
            except Exception as e:
                print(f"[multi_signal] 證交所法人 {ds} 取得失敗：{e}")
            try:
                j = _json_mod.loads(_ms_http_get(
                    f"https://www.tpex.org.tw/www/zh-tw/insti/dailyTrade?type=Daily&sect=EW"
                    f"&date={d.strftime('%Y/%m/%d')}&response=json"))
                tb = (j.get("tables") or [{}])[0]
                if str(j.get("stat", "")).lower() == "ok":
                    for row in tb.get("data") or []:
                        if row and len(row) >= 3:
                            day_rows[str(row[0]).strip()] = round(_ms_int(row[-1]) / 1000, 1)
            except Exception as e:
                print(f"[multi_signal] 櫃買法人 {ds} 取得失敗：{e}")
            if day_rows:
                got_dates.append(ds)
                for sid, v in day_rows.items():
                    out.setdefault(sid, {})[ds] = v
            _time_mod.sleep(0.5)
        d -= _td_ms(days=1)
    return {"dates": got_dates, "data": out}


def _ms_parse_mops_revenue(html: str) -> dict:
    """解析公開資訊觀測站月營收彙總表（t21sc03），回傳 {代號: {...}}。欄位順序已於2026/09/15實測確認：
    代號,名稱,當月營收,上月營收,去年當月營收,上月比較增減%,去年同月增減%,當月累計,去年累計,前期比較增減%,備註"""
    import re as _re_ms
    out = {}
    for tr in _re_ms.findall(r"<tr[^>]*>(.*?)</tr>", html, flags=_re_ms.S | _re_ms.I):
        cells = [_re_ms.sub(r"<[^>]+>", "", c).replace("&nbsp;", "").strip()
                 for c in _re_ms.findall(r"<td[^>]*>(.*?)</td>", tr, flags=_re_ms.S | _re_ms.I)]
        if len(cells) < 10 or not _re_ms.fullmatch(r"\d{4}", cells[0]):
            continue

        def _f(s):
            try:
                return float(s.replace(",", ""))
            except Exception:
                return None
        out[cells[0]] = {"revenue": _f(cells[2]), "mom": _f(cells[5]),
                         "yoy": _f(cells[6]), "cum_yoy": _f(cells[9])}
    return out


def _ms_load_revenue(scan_date: str, fetch: bool = True) -> dict:
    """
    月營收（上市＋上櫃，含KY股）。每個月份整份彙總表只有4個檔案，抓過就存進DB，
    之後同月份不再重抓；只有「上個月」（公司陸續公布中）每天重抓一次補新公布的公司。
    回傳 {代號: {ym: {revenue, mom, yoy, cum_yoy}}}，只含最近4個月份（月初上個月還沒全部公布，
    多抓一個月，每檔各自取有資料的最近3個月）。
    fetch=False：只讀DB不上網抓（個股解析即時查詢用，避免拖慢查詢）。
    """
    from datetime import date as _d_ms
    d = _d_ms.fromisoformat(scan_date)
    months = []
    y, m = d.year, d.month
    for _ in range(4):
        m -= 1
        if m == 0:
            y, m = y - 1, 12
        months.append((y, m))
    conn = _db_conn()
    try:
        for idx, (yy, mm) in enumerate(months):
            ym = f"{yy}-{mm:02d}"
            row = conn.execute(
                "SELECT fetched_date FROM multi_signal_revenue_fetch WHERE ym=?", (ym,)
            ).fetchone()
            need = (row is None) or (idx <= 1 and row["fetched_date"] != scan_date)
            if not need or not fetch:
                continue
            got = 0
            # _0＝國內公司、_1＝外國公司（KY股，例如世芯-KY、中租-KY），兩份格式相同（2026/09/15實測）
            for market, suffix in (("sii", 0), ("sii", 1), ("otc", 0), ("otc", 1)):
                try:
                    raw = _ms_http_get(
                        f"https://mopsov.twse.com.tw/nas/t21/{market}/t21sc03_{yy - 1911}_{mm}_{suffix}.html", timeout=20)
                    parsed = _ms_parse_mops_revenue(raw.decode("big5", errors="ignore"))
                    for sid, v in parsed.items():
                        conn.execute(
                            "INSERT OR REPLACE INTO multi_signal_revenue (stock_id, ym, revenue, mom, yoy, cum_yoy) "
                            "VALUES (?,?,?,?,?,?)",
                            (sid, ym, v["revenue"], v["mom"], v["yoy"], v["cum_yoy"]))
                    got += len(parsed)
                except Exception as e:
                    print(f"[multi_signal] 月營收 {ym} {market}_{suffix} 取得失敗：{e}")
                _time_mod.sleep(0.5)
            if got:
                conn.execute("INSERT OR REPLACE INTO multi_signal_revenue_fetch (ym, fetched_date, count) VALUES (?,?,?)",
                             (ym, scan_date, got))
            conn.commit()
        yms = [f"{yy}-{mm:02d}" for yy, mm in months]
        rows = conn.execute(
            f"SELECT stock_id, ym, revenue, mom, yoy, cum_yoy FROM multi_signal_revenue "
            f"WHERE ym IN ({','.join('?' * len(yms))})", yms).fetchall()
    finally:
        conn.close()
    out: dict = {}
    for r in rows:
        out.setdefault(r["stock_id"], {})[r["ym"]] = {
            "revenue": r["revenue"], "mom": r["mom"], "yoy": r["yoy"], "cum_yoy": r["cum_yoy"]}
    return out


def _multi_signal_check_one_stock(stock_id: str, stock_name: str = "", ctx: dict | None = None):
    """
    排程用：自己抓日K，再交給 _ms_evaluate 跑12個方法。日K資料不足回傳None（整檔跳過）。
    """
    import sys as _sys_ms
    _sp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker")
    if _sp not in _sys_ms.path:
        _sys_ms.path.insert(0, _sp)
    from crawler import fetch_price_history

    prices = fetch_price_history(stock_id, days=MULTI_SIGNAL_CFG["history_days"])
    rows = [p for p in prices
            if p["close"] > 0 and p["open"] > 0 and p["high"] > 0 and p["low"] > 0]
    return _ms_evaluate(
        stock_id,
        [p["date"] for p in rows],
        np.array([p["high"] for p in rows], dtype=float),
        np.array([p["low"] for p in rows], dtype=float),
        np.array([p["close"] for p in rows], dtype=float),
        np.array([p["volume"] for p in rows], dtype=float),
        ctx,
    )


def _ms_evaluate(stock_id: str, dates: list, highs, lows, closes, vols, ctx: dict | None = None):
    """
    對一檔股票跑12個方法（2026/09/17從 _multi_signal_check_one_stock 拆出來，
    讓個股解析 _do_analyze 可以直接用手上已經有的K線資料算，不必再打一次FinMind）。
    回傳每個方法一筆的list，資料不足回傳None。每筆：
      {method, category, passed(bool：今天剛轉強，選股頁用),
       state("today"今天剛轉強／"active"轉強中／"none"未轉強，個股解析用),
       days(轉強中第幾天，active才有), value, extra}
    ctx：整批共用的資料（法人買賣超、月營收）；沒傳的話那兩個方法記為資料缺。
    """
    import sys as _sys_ms
    _sp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker")
    if _sp not in _sys_ms.path:
        _sys_ms.path.insert(0, _sp)
    from finmind_filter import _ma, _find_ma_golden_cross_index

    ctx = ctx or {}
    cfg = MULTI_SIGNAL_CFG
    n = len(closes)
    if n < cfg["min_bars"]:
        return None
    closes = np.asarray(closes, dtype=float)
    highs = np.asarray(highs, dtype=float)
    lows = np.asarray(lows, dtype=float)
    vols = np.asarray(vols, dtype=float)
    data_date = dates[-1]
    price = float(closes[-1])
    prev_close = float(closes[-2])
    slb = cfg["state_lookback"]
    results: list = []

    def _add(method, passed, value, extra, state=None, days=None):
        extra = dict(extra or {})
        extra.setdefault("data_date", data_date)
        extra.setdefault("close", _ms_num(price))
        extra.setdefault("prev_close", _ms_num(prev_close))
        if state is None:
            state = "today" if passed else "none"
        if passed:
            state, days = "today", 0
        results.append({"method": method, "category": MULTI_SIGNAL_METHODS[method][1],
                        "passed": bool(passed), "state": state,
                        "days": days if state == "active" else None,
                        "value": _ms_num(value), "extra": extra})

    def _today(idx):
        return {"cross_date": data_date} if idx is not None else {}

    def _cross_state(fast, slow):
        """交叉型指標的「轉強中」：現在還在上方，且最近 slb 天內有乾淨穿越"""
        idx = _find_cross_index(fast, slow, slb)
        if idx is None:
            return "none", None, None
        return "active", n - 1 - idx, dates[idx]

    def _since(cond_list):
        """條件目前成立的話，連續成立了幾天（今天算第0天之前的天數）"""
        d = 0
        for v in reversed(cond_list[:-1]):
            if v:
                d += 1
            else:
                break
        return d

    lb = cfg["cross_lookback"]

    # ── 1. MACD（12,26,9）DIF當天向上穿越DEA ──
    dif, dea, hist = calc_macd(closes)
    mi = _find_cross_index(dif, dea, lb)
    stt, dd, cd = _cross_state(dif, dea)
    _add("macd", mi is not None, hist[-1],
         {"dif": _ms_num(dif[-1]), "dea": _ms_num(dea[-1]), "hist": _ms_num(hist[-1]),
          "above_zero": bool(_ms_num(dif[-1]) is not None and dif[-1] > 0),
          **_today(mi), **({"since_date": cd} if cd else {})}, stt, dd)

    # ── 2. KD（9,3,3）K當天向上穿越D ──
    k_arr, d_arr = calc_kd(highs, lows, closes)
    ki = _find_cross_index(k_arr, d_arr, lb)
    stt, dd, cd = _cross_state(k_arr, d_arr)
    _add("kd", ki is not None, k_arr[-1],
         {"k": _ms_num(k_arr[-1]), "d": _ms_num(d_arr[-1]),
          **_today(ki), **({"since_date": cd} if cd else {})}, stt, dd)

    # ── 3. RSI（14）當天由50以下往上穿越50 ──
    rsi = calc_rsi(closes, 14)
    rsi_now, rsi_prev = _ms_num(rsi[-1]), _ms_num(rsi[-2])
    rsi_ok = rsi_now is not None and rsi_prev is not None and rsi_prev <= cfg["rsi_mid"] < rsi_now
    above = [bool(v > cfg["rsi_mid"]) if not np.isnan(v) else False for v in rsi]
    rsi_state = "active" if (rsi_now is not None and rsi_now > cfg["rsi_mid"]) else "none"
    _add("rsi", rsi_ok, rsi_now, {"rsi_prev": rsi_prev, "threshold": cfg["rsi_mid"],
                                  **({"cross_date": data_date} if rsi_ok else {})},
         rsi_state, _since(above) if rsi_state == "active" else None)

    # ── 4. 月季線金叉（複用深度選股的_ma/_find_ma_golden_cross_index，只認當天）──
    close_list = [float(c) for c in closes]
    ma20_l, ma60_l = _ma(close_list, 20), _ma(close_list, 60)
    gi = _find_ma_golden_cross_index(ma20_l, ma60_l, lb)
    gi_act = _find_ma_golden_cross_index(ma20_l, ma60_l, slb)
    ma20, ma60 = ma20_l[-1], ma60_l[-1]
    _add("ma_cross", gi is not None, ((ma20 - ma60) / ma60 * 100) if (ma20 and ma60) else None,
         {"ma20": ma20, "ma60": ma60, **_today(gi),
          **({"since_date": dates[gi_act]} if gi_act is not None else {})},
         "active" if gi_act is not None else "none",
         (n - 1 - gi_act) if gi_act is not None else None)

    # ── 5. 海龜突破（當天收盤突破前20日最高價）──
    ti, level = _turtle_breakout(highs, lows, closes, cfg["turtle_entry"],
                                 cfg["turtle_exit"], cfg["turtle_lookback"])
    ta, _lv_a = _turtle_breakout(highs, lows, closes, cfg["turtle_entry"], cfg["turtle_exit"], slb)
    atr = _calc_atr(highs, lows, closes, 20)
    _r2 = lambda x: round(float(x), 2) if x is not None and not np.isnan(float(x)) else None
    t_extra = {"entry_days": cfg["turtle_entry"],
               "exit_level": _r2(np.min(lows[-cfg["turtle_exit"]:])), "atr20": _ms_num(atr)}
    if ti is not None:
        le = cfg["turtle_long_entry"]
        t_extra.update({
            "cross_date": data_date, "breakout_level": _r2(level),
            "stop_2n": _r2(price - 2 * atr) if atr else None,
            "also_55d_breakout": bool(ti - le >= 0 and closes[ti] > float(np.max(highs[ti - le:ti]))),
        })
    elif ta is not None:
        t_extra.update({"since_date": dates[ta], "breakout_level": _r2(_lv_a)})
    _add("turtle", ti is not None, ((price - level) / level * 100) if (ti is not None and level) else None,
         t_extra, "active" if ta is not None else "none", (n - 1 - ta) if ta is not None else None)

    # ── 6. 趨勢（原多空雷達一，道氏波峰波谷）：今天判定為上升趨勢、昨天不是 ──
    tr_now = _dow_trend(highs, lows)
    tr_prev = _dow_trend(highs[:-1], lows[:-1])
    tr_ok = tr_now == "上升趨勢" and tr_prev != "上升趨勢"
    _add("trend", tr_ok, None, {"trend": tr_now, "trend_prev": tr_prev,
                                **({"cross_date": data_date} if tr_ok else {})},
         "active" if tr_now == "上升趨勢" else "none")

    # ── 7. 量能（原多空雷達三，注意是量能不是籌碼）：5日均量/20日均量 今天≥1.3、昨天<1.3 ──
    def _vr(end):
        if end < 20:
            return None
        v5, v20 = vols[end - 5:end].mean(), vols[end - 20:end].mean()
        return (v5 / v20) if v20 > 0 else None
    vr_now, vr_prev = _vr(n), _vr(n - 1)
    vr_ok = vr_now is not None and vr_prev is not None and vr_prev < cfg["vol_ratio"] <= vr_now
    vr_hist = [(_vr(e) or 0) >= cfg["vol_ratio"] for e in range(max(20, n - slb - 1), n + 1)]
    vr_state = "active" if (vr_now is not None and vr_now >= cfg["vol_ratio"]) else "none"
    _add("volume", vr_ok, vr_now, {"vol_ratio_prev": _ms_num(vr_prev), "threshold": cfg["vol_ratio"],
                                   "vol_today_lots": int(vols[-1] // 1000),
                                   **({"cross_date": data_date} if vr_ok else {})},
         vr_state, _since(vr_hist) if vr_state == "active" else None)

    # ── 8. 布林通道（20,2）：今天收盤向上穿越中軌或上軌 ──
    bb_mid, bb_up, bb_low = calc_bollinger(closes)
    cross_mid = closes[-2] <= bb_mid[-2] and closes[-1] > bb_mid[-1]
    cross_up = closes[-2] <= bb_up[-2] and closes[-1] > bb_up[-1]
    bb_ok = bool(cross_mid or cross_up)
    bb_above = [bool(c > m) if not np.isnan(m) else False for c, m in zip(closes[-slb - 1:], bb_mid[-slb - 1:])]
    bb_state = "active" if (not np.isnan(bb_mid[-1]) and closes[-1] > bb_mid[-1]) else "none"
    _add("bollinger", bb_ok, bb_mid[-1],
         {"mid": _ms_num(bb_mid[-1]), "upper": _ms_num(bb_up[-1]), "lower": _ms_num(bb_low[-1]),
          "which": ("上軌" if cross_up else "中軌") if bb_ok else None,
          **({"cross_date": data_date} if bb_ok else {})},
         bb_state, _since(bb_above) if bb_state == "active" else None)

    # ── 9. OBV能量潮：OBV今天向上穿越自己的20日均線 ──
    obv = calc_obv(closes, vols)
    obv_ma = pd.Series(obv).rolling(cfg["obv_ma"]).mean().values
    oi = _find_cross_index(obv, obv_ma, lb)
    stt, dd, cd = _cross_state(obv, obv_ma)
    _add("obv", oi is not None, None,
         {"obv_lots": _ms_num(obv[-1] / 1000), "obv_ma_lots": _ms_num(obv_ma[-1] / 1000),
          **_today(oi), **({"since_date": cd} if cd else {})}, stt, dd)

    # ── 10. 法人籌碼：三大法人合計「連買N天」剛好在今天成立（前一天之前還沒連滿N天）──
    inst = ctx.get("inst") or {}
    need = cfg["inst_buy_days"]
    inst_dates = inst.get("dates") or []
    per = (inst.get("data") or {}).get(stock_id)
    if per is not None and inst_dates and inst_dates[0] == data_date and len(inst_dates) >= need + 1:
        seq = [per.get(dd) for dd in inst_dates]     # 新→舊
        streak = 0
        for v in seq:
            if v is not None and v > 0:
                streak += 1
            else:
                break
        inst_ok = streak == need
        _add("institution", inst_ok, seq[0],
             {"streak": streak, "need": need, "recent_lots": seq[:5], "recent_dates": inst_dates[:5],
              "sum_lots": _ms_num(sum(v for v in seq[:5] if v is not None)),
              **({"cross_date": data_date} if inst_ok else {})},
             "active" if streak >= need else "none", (streak - need) if streak >= need else None)
    else:
        _add("institution", False, None,
             {"missing": True, "note": "法人資料缺（今日尚未公布或取得失敗）"})

    # ── 11. 圖表型態：W底／頭肩底，今天收盤剛突破頸線 ──
    pat = _detect_bottom_pattern(highs, lows, closes, cfg)
    p_extra = {}
    if pat:
        p_extra = {k: v for k, v in pat.items() if k != "start_idx"}
        p_extra["start_date"] = dates[pat["start_idx"]]
        p_extra["cross_date"] = data_date
    _add("pattern", pat is not None, pat["neckline"] if pat else None, p_extra)

    # ── 12. 基本面（2026/09/17帥哥鴻改定義）：營收成長中、但股價還沒反應 ──
    # 原本的「最新月營收年增由負轉正」會踩到「內線先拉、營收公布剛好利多出盡」，改成：
    #   ① 最近3個月營收年增率都 > 0（成長不是一次性）
    #   ② 近20個交易日漲幅 < 10%（還沒被拉過）
    #   ③ 收盤價在近60日高低區間的下方60%以內（不在高檔）
    # 這是「狀態型」條件（營收一個月才公布一次），成立期間每天都算通過。
    rev = (ctx.get("revenue") or {}).get(stock_id) or {}
    yms = sorted(rev.keys(), reverse=True)[:cfg["rev_months"]]
    yoys = [rev[m].get("yoy") for m in yms]
    if len(yms) >= cfg["rev_months"] and all(v is not None for v in yoys):
        base20 = float(closes[-21]) if n >= 21 else float(closes[0])
        chg20 = (price - base20) / base20 * 100 if base20 > 0 else 0
        hi60, lo60 = float(np.max(highs[-60:])), float(np.min(lows[-60:]))
        pos60 = (price - lo60) / (hi60 - lo60) * 100 if hi60 > lo60 else 50
        grow = all(v > 0 for v in yoys)
        not_run = chg20 < cfg["rev_max_gain20"] and pos60 <= cfg["rev_max_pos60"]
        rv_ok = bool(grow and not_run)
        _add("revenue", rv_ok, yoys[0],
             {"ym": yms[0], "yoys": yoys, "yms": yms, "chg20": round(chg20, 2), "pos60": round(pos60, 1),
              "grow": grow, "not_run": not_run,
              "mom": rev[yms[0]].get("mom"), "cum_yoy": rev[yms[0]].get("cum_yoy")},
             "today" if rv_ok else "none")
    else:
        _add("revenue", False, None, {"missing": True, "note": "月營收資料不足（非一般上市櫃公司，如ETF，或尚未公布）"})

    return results


_MS_CTX_CACHE = {"loaded_at": 0, "ctx": None}


def _ms_ctx_cached() -> dict:
    """
    個股解析即時查詢用的12金叉共用資料：法人（最近一次排程存下的全市場資料）＋月營收（只讀DB）。
    記憶體快取10分鐘，避免每次查詢都讀DB、解JSON。
    """
    now = _time_mod.time()
    if _MS_CTX_CACHE["ctx"] is not None and now - _MS_CTX_CACHE["loaded_at"] < 600:
        return _MS_CTX_CACHE["ctx"]
    ctx = {}
    try:
        conn = _db_conn()
        try:
            row = conn.execute("SELECT content FROM multi_signal_ctx WHERE key='inst'").fetchone()
        finally:
            conn.close()
        if row and row["content"]:
            ctx["inst"] = _json_mod.loads(row["content"])
    except Exception as e:
        print(f"[multi_signal] 讀取法人快取失敗：{e}")
    try:
        ctx["revenue"] = _ms_load_revenue(_taipei_today(), fetch=False)
    except Exception as e:
        print(f"[multi_signal] 讀取月營收快取失敗：{e}")
    _MS_CTX_CACHE.update({"loaded_at": now, "ctx": ctx})
    return ctx


def _run_multi_signal_scan_job(start_delay: float = 0, stock_ids: list | None = None, force: bool = False):
    """
    平日17:20執行（原本排在深度選股17:00之後；深度選股已於2026/09/17下架）：
    成交量前150檔 × 12個方法，結果寫進 multi_signal_results。
    同一天重跑會覆蓋（INSERT OR REPLACE），單檔失敗不影響其他檔。
    stock_ids：測試用，指定只跑哪幾檔（管理端點可帶）。
    """
    from zoneinfo import ZoneInfo as _ZI_ms2
    if start_delay:
        _time_mod.sleep(start_delay)   # 延遲放在搶鎖之前，等待期間不會擋住管理員手動觸發
    if not _MULTI_SIGNAL_LOCK.acquire(blocking=False):
        print("[multi_signal] 已有一輪在執行中，跳過本次")
        return
    st = _MULTI_SIGNAL_STATUS
    try:
        now = datetime.now(_ZI_ms2("Asia/Taipei"))
        if now.weekday() >= 5 and not (stock_ids or force):   # 管理員手動觸發(force)週末也能跑
            return
        scan_date = now.strftime("%Y-%m-%d")
        st.update({"running": True, "started_at": now.strftime("%Y-%m-%d %H:%M:%S"),
                   "finished_at": None, "scan_date": scan_date, "total": 0, "done": 0,
                   "ok": 0, "skipped": 0, "failed": 0, "rows": 0, "errors": [], "msg": "執行中"})
        print(f"[multi_signal] 開始執行 {now.strftime('%H:%M')}")

        import sys as _sys_ms
        _sp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_picker")
        if _sp not in _sys_ms.path:
            _sys_ms.path.insert(0, _sp)
        import crawler as _crawler_ms
        if FINMIND_TOKEN:
            _crawler_ms.FINMIND_TOKEN = FINMIND_TOKEN

        if stock_ids:
            top_ids = [str(s).strip() for s in stock_ids if str(s).strip()]
            name_dict = {}
        else:
            top_ids, name_dict = _crawler_ms.fetch_twse_volume_top(n=MULTI_SIGNAL_CFG["candidate_n"])
        if not top_ids:
            st["msg"] = "取得成交量排行失敗，本輪跳過"
            print("[multi_signal] 取得成交量排行失敗，跳過")
            return
        st["total"] = len(top_ids)

        # 整批共用資料：法人（證交所/櫃買一次抓全市場）、月營收（公開資訊觀測站彙總表，有DB快取）
        ctx = {}
        try:
            ctx["inst"] = _ms_fetch_institutional_bulk(scan_date, MULTI_SIGNAL_CFG["inst_buy_days"] + 2)
            if ctx["inst"].get("dates"):
                _cc = _db_conn()
                try:
                    _cc.execute("INSERT OR REPLACE INTO multi_signal_ctx (key, data_date, content, updated_at) "
                                "VALUES ('inst', ?, ?, datetime('now','+8 hours'))",
                                (ctx["inst"]["dates"][0], _json_mod.dumps(ctx["inst"], ensure_ascii=False)))
                    _cc.commit()
                finally:
                    _cc.close()
                _MS_CTX_CACHE["loaded_at"] = 0
            print(f"[multi_signal] 法人資料日期：{ctx['inst']['dates']}")
        except Exception as e:
            print(f"[multi_signal] 法人資料取得失敗：{e}")
        try:
            ctx["revenue"] = _ms_load_revenue(scan_date)
            print(f"[multi_signal] 月營收資料：{len(ctx['revenue'])} 家公司")
        except Exception as e:
            print(f"[multi_signal] 月營收資料取得失敗：{e}")

        data_dates: dict = {}
        conn = _db_conn()
        try:
            for i, sid in enumerate(top_ids, 1):
                sname = name_dict.get(sid) or _name_cache.get(sid, "") or ""
                try:
                    res = _multi_signal_check_one_stock(sid, sname, ctx)
                    if res is None:
                        st["skipped"] += 1
                    else:
                        for r in res:
                            conn.execute(
                                "INSERT OR REPLACE INTO multi_signal_results "
                                "(scan_date, stock_id, stock_name, method, category, passed, value, extra_json) "
                                "VALUES (?,?,?,?,?,?,?,?)",
                                (scan_date, sid, sname, r["method"], r["category"],
                                 1 if r["passed"] else 0, r["value"],
                                 _json_mod.dumps(r["extra"], ensure_ascii=False))
                            )
                        conn.commit()
                        st["ok"] += 1
                        st["rows"] += len(res)
                        dd = res[0]["extra"].get("data_date")
                        data_dates[dd] = data_dates.get(dd, 0) + 1
                        passed = [r["method"] for r in res if r["passed"]]
                        if passed:
                            print(f"[multi_signal] ({i}/{len(top_ids)}) {sid} 通過：{','.join(passed)}")
                except Exception as e:
                    st["failed"] += 1
                    if len(st["errors"]) < 20:
                        st["errors"].append(f"{sid}: {e}")
                    print(f"[multi_signal] ({i}/{len(top_ids)}) {sid} 失敗：{e}")
                st["done"] = i
                if i < len(top_ids) and MULTI_SIGNAL_CFG["api_delay"]:
                    _time_mod.sleep(MULTI_SIGNAL_CFG["api_delay"])
        finally:
            conn.close()

        stale = {d: c for d, c in data_dates.items() if d != scan_date}
        inst_dates = (ctx.get("inst") or {}).get("dates") or []
        st["msg"] = (f"完成：{st['ok']}檔寫入（{st['rows']}筆），{st['skipped']}檔資料不足跳過，"
                     f"{st['failed']}檔失敗；K線資料日期 {data_dates}；"
                     f"法人資料日期 {inst_dates[:3]}；月營收 {len(ctx.get('revenue') or {})} 家")
        if stale:
            st["msg"] += f"（⚠️ 有{sum(stale.values())}檔的最新K棒不是今天，可能是FinMind尚未更新或非交易日）"
        if not inst_dates or inst_dates[0] != scan_date:
            st["msg"] += "（⚠️ 今天的法人資料還沒抓到，法人方法今天全部不通過）"
        print(f"[multi_signal] {st['msg']}")

        # LINE群組推播（2026/09/17接手原本深度選股的推播；只在正式全市場掃描、而且資料是今天的才推）
        if not stock_ids and data_dates.get(scan_date):
            try:
                _pl = _ms_build_payload(scan_date).get("data") or []
                _line_bot_push_multi_signal_notice(
                    scan_date, len(_pl), sum(1 for x in _pl if x["passed_count"] >= 3))
            except Exception as _le:
                print(f"[multi_signal] LINE推播失敗（不影響選股本身）：{_le}")
    except Exception as e:
        st["msg"] = f"排程失敗：{e}"
        print(f"[multi_signal] ❌ 排程失敗：{e}")
    finally:
        st["running"] = False
        st["finished_at"] = datetime.now(_ZI_ms2("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")
        _MULTI_SIGNAL_LOCK.release()


def _ms_detail_text(method: str, ex: dict) -> str:
    """每個方法通過時，給小白看的一句白話依據（前端直接顯示）"""
    try:
        if method == "macd":
            pos = "0軸上方" if ex.get("above_zero") else "0軸下方"
            return f"DIF {ex.get('dif')} 今天向上穿越 DEA {ex.get('dea')}（{pos}）"
        if method == "kd":
            return f"K {ex.get('k'):.0f} 今天向上穿越 D {ex.get('d'):.0f}"
        if method == "rsi":
            return f"RSI 從 {ex.get('rsi_prev'):.0f} 升到 50 以上"
        if method == "ma_cross":
            return f"月線 {ex.get('ma20')} 今天向上穿越季線 {ex.get('ma60')}"
        if method == "turtle":
            s = f"收盤突破前20日最高價 {ex.get('breakout_level')}"
            if ex.get("also_55d_breakout"):
                s += "，同時創55日新高"
            if ex.get("exit_level"):
                s += f"；海龜通道下緣 {ex.get('exit_level')}"
            return s
        if method == "trend":
            return f"波峰波谷由「{ex.get('trend_prev') or '不明'}」轉為頭頭高、底底高"
        if method == "volume":
            return (f"5日均量放大到20日均量的 {ex.get('vol_ratio'):.2f} 倍"
                    f"（昨天 {ex.get('vol_ratio_prev')} 倍），今天成交 {ex.get('vol_today_lots'):,} 張")
        if method == "bollinger":
            return f"收盤站上布林{ex.get('which')}（中軌 {ex.get('mid')}／上軌 {ex.get('upper')}）"
        if method == "obv":
            return "OBV能量潮今天向上穿越20日均線，資金開始流入"
        if method == "institution":
            lots = ex.get("recent_lots") or []
            return f"三大法人連買 {ex.get('streak')} 天，今天 {lots[0]:+,.0f} 張" if lots else "三大法人連買成立"
        if method == "pattern":
            return f"{ex.get('type')}今天突破頸線 {ex.get('neckline')}，等幅推算價位約 {ex.get('target')}"
        if method == "revenue":
            yo = "／".join(f"{v:+.1f}%" for v in (ex.get("yoys") or []))
            return (f"近{len(ex.get('yoys') or [])}個月營收年增 {yo}，股價近20天只漲 {ex.get('chg20')}%、"
                    f"位於近60日區間 {ex.get('pos60')}%，還沒反應")
    except Exception:
        pass
    return ""


def _ms_build_payload(scan_date: str = "") -> dict:
    """讀DB組出「12金叉選股」頁面資料：每檔股票通過哪些方法、幾個方法、幾個類別"""
    conn = _db_conn()
    try:
        if not scan_date:
            row = conn.execute("SELECT MAX(scan_date) FROM multi_signal_results").fetchone()
            scan_date = (row[0] if row else "") or ""
        rows = conn.execute(
            "SELECT stock_id, stock_name, method, category, passed, value, extra_json, created_at "
            "FROM multi_signal_results WHERE scan_date=? ORDER BY stock_id",
            (scan_date,)
        ).fetchall() if scan_date else []
    finally:
        conn.close()

    methods = {m: {"method": m, "label": lab, "category": cat, "total": 0, "passed": 0, "missing": 0}
               for m, (lab, cat) in MULTI_SIGNAL_METHODS.items()}
    stocks: dict = {}
    updated_at = None
    for r in rows:
        m = r["method"]
        if m not in methods:
            continue
        try:
            ex = _json_mod.loads(r["extra_json"] or "{}")
        except Exception:
            ex = {}
        updated_at = max(updated_at or "", r["created_at"] or "")
        info = methods[m]
        info["total"] += 1
        if ex.get("missing"):
            info["missing"] += 1
        s = stocks.setdefault(r["stock_id"], {
            "stock_id": r["stock_id"], "stock_name": r["stock_name"] or _name_cache.get(r["stock_id"], ""),
            "price": ex.get("close"), "prev_close": ex.get("prev_close"), "price_date": ex.get("data_date"),
            "signals": [], "categories": set()})
        if r["passed"]:
            info["passed"] += 1
            s["signals"].append({"method": m, "label": info["label"], "category": r["category"],
                                 "detail": _ms_detail_text(m, {**ex, "vol_ratio": r["value"]})})
            s["categories"].add(r["category"])
    order = list(MULTI_SIGNAL_METHODS.keys())
    items = []
    for s in stocks.values():
        if not s["signals"]:
            continue
        s["signals"].sort(key=lambda x: order.index(x["method"]))
        pc, p = s.get("prev_close"), s.get("price")
        s["change_pct"] = round((p - pc) / pc * 100, 2) if (p and pc) else None
        s["passed_count"] = len(s["signals"])
        s["category_count"] = len(s["categories"])
        s["categories"] = sorted(s["categories"])
        items.append(s)
    items.sort(key=lambda x: (-x["passed_count"], -x["category_count"], x["stock_id"]))
    return {"scan_date": scan_date, "updated_at": updated_at, "stock_count": len(stocks),
            "row_count": len(rows), "method_total": len(MULTI_SIGNAL_METHODS),
            "methods": list(methods.values()), "data": items}


# ══════════════════════════════════════════════════════════
# 個股綜合解說（模版版，2026/09/17新增，文件B階段7）
#
# 為什麼要做：原本個股解析同時有好幾套各自判斷的文字——主結論（只看價格位置＋K棒）、
# 深度分析卡片（另一套K棒分類、均線排列、KD、MACD各說各話）、風險標籤（只看離支撐壓力多遠），
# 加上深度選股又是另一套標準，常常出現「深度選股說高信心，個股解析說觀望/建議出場」。
# 這裡把個股解析算出來的所有資料＋12金叉狀態，集中成「一份」判斷，所有畫面都讀這一份。
#
# 模版怎麼改：
#   ● 句子都在 VERDICT_TEXT，{大括號} 會自動帶入數字，只改字不用動程式。
#   ● 每條多空理由的權重在 VERDICT_WEIGHTS，數字越大影響結論越多。
#   ● 各段要付費還是加購在 VERDICT_SECTION_TIER（目前全部 "paid"，之後要拆加購把某段改成 "addon"）。
# ══════════════════════════════════════════════════════════

VERDICT_SECTION_TIER = {
    "headline": "free",      # 一句話結論：所有人都看得到（取代原本的「主結論」）
    "status": "paid",        # 現在的狀況
    "bull": "paid",          # 看多理由
    "bear": "paid",          # 看空理由
    "conflicts": "paid",     # 矛盾與最大問題
    "levels": "paid",        # 關鍵價位
    "scenarios": "paid",     # 接下來的情境
    "action": "free",        # 操作參考（原本主結論就有「操作：」，所有人都看得到，維持不變）
    "signals": "paid",       # 12金叉逐項燈號
}

VERDICT_WEIGHTS = {
    "trend_up": 2, "trend_down": 2,
    "ma_bull": 1, "ma_bear": 1,
    "breakout": 2, "breakdown": 2,
    "kbar_bull": 1, "kbar_bear": 1, "vp_exit": 2,
    "kd_gold": 1, "kd_death": 1,
    "macd_bull": 1, "macd_bear": 1,
    "inst_buy": 1, "inst_sell": 1,
    "vol_up": 1,
    "gann_buy": 1, "gann_sell": 1,
    "near_sup_rr": 1, "near_res": 1, "rr_low": 1,
    "channel_conflict": 1,
    "overheat": 1, "kd_high": 1,
    "ms_many": 2, "ms_some": 1,
    "revenue": 1,
}

VERDICT_TEXT = {
    # 一句話結論（依立場）
    "head_bull": "{name}多方條件明顯佔優（看多理由{bull}項、看空理由{bear}項），{ms_part}目前屬多方結構。",
    "head_bull_wait": "{name}整體偏多，但{wait_reason}，短線位置偏高、過熱風險增加。",
    "head_bull_caution": "{name}偏多，但有{bear}個看空理由要留意，最大的問題是：{top_problem}。",
    "head_neutral": "{name}多空拉鋸（看多{bull}項、看空{bear}項），方向還不明確，關鍵在突破 {resistance} 或跌破 {support}。",
    "head_bear": "{name}空方條件佔優（看空理由{bear}項、看多理由{bull}項），目前屬空方結構，止跌訊號尚未出現。",
    "ms_part_many": "今天12金叉有{n}項同時轉強，",
    "ms_part_some": "今天12金叉有{n}項轉強，",
    "wait_near_res": "距離壓力 {resistance} 只剩 {res_pct}%",
    "wait_overheat": "股價已經高於月線 {bias20}%，短線漲多",
    "wait_kd_high": "KD 已經在 {k} 的高檔",

    # 現在的狀況
    "status_price": "目前價格 {price}，位在支撐 {support} 和壓力 {resistance} 之間，大約{pos_word}（{pos}%）。",
    "status_trend": "趨勢：{trend_text}。",
    "status_ma": "均線：{ma_text}。",
    "status_ms": "12金叉：今天剛轉強 {today} 項、持續轉強中 {active} 項，涵蓋{cats}。",
    "status_basis": "{basis}",

    # 看多理由
    "trend_up": "近期高低點一路墊高（頭頭高、底底高），屬於上升趨勢",
    "ma_bull": "均線多頭排列（{ma_text}）",
    "breakout": "今天突破前高 {prev_high}",
    "kbar_bull": "出現多頭K棒：{kbar}",
    "kd_gold": "KD 黃金交叉（K {k}）",
    "macd_bull": "MACD 偏多：{macd_text}",
    "inst_buy": "三大法人近5日買超 {inst_total} 張{inst_streak}",
    "vol_up": "量能放大，5日均量是20日均量的 {vol_ratio} 倍",
    "gann_buy": "葛蘭碧多方訊號：{gann}",
    "near_sup_rr": "股價靠近支撐 {support}，風報比 {rr} 不錯",
    "ms_many": "12金叉今天有 {n} 項同時轉強：{list}",
    "ms_some": "12金叉今天轉強：{list}",
    "revenue": "營收連續 {m} 個月年增（最新 {yoy}%），但股價近20天只漲 {chg20}%，還沒反應",

    # 看空理由
    "trend_down": "近期高低點一路走低（頭頭低、底底低），屬於下降趨勢",
    "ma_bear": "均線空頭排列（{ma_text}）",
    "breakdown": "股價跌破支撐 {support}",
    "kbar_bear": "出現空頭K棒：{kbar}",
    "vp_exit": "爆量收出「{shape}」（{vol_x} 倍均量），賣壓沉重",
    "kd_death": "KD 死亡交叉（K {k}）",
    "macd_bear": "MACD 偏空：{macd_text}",
    "inst_sell": "三大法人近5日賣超 {inst_total} 張",
    "gann_sell": "葛蘭碧空方訊號：{gann}",
    "near_res": "距離壓力 {resistance} 只剩 {res_pct}%，上漲空間有限",
    "rr_low": "風報比只有 {rr}，潛在風險大於潛在空間",
    "channel_conflict": "{conflict}",
    "overheat": "股價高於月線 {bias20}%，短線過熱",
    "kd_high": "KD 在 {k} 的高檔，容易鈍化",

    # 矛盾
    "cf_price_inst": "價格偏多，但三大法人在賣（近5日 {inst_total} 張）——價格和籌碼方向不一致",
    "cf_break_kbar": "今天突破了，但收出空頭K棒——要小心假突破",
    "cf_break_novol": "今天突破了，但量能沒有放大（{vol_ratio} 倍）——沒量的突破比較容易失敗",
    "cf_kd_high_gold": "KD 金叉，但發生在 {k} 的高檔——比較像末升段，不是起漲",
    "cf_macd_below0": "MACD 金叉，但還在0軸下方——比較像空頭裡的反彈，還不是正式轉多",
    "cf_trend_ma": "高低點結構是「{trend}」，但均線是「{ma_label}」——長短線看法不一致",
    "cf_single_face": "12金叉的轉強訊號全部來自技術面，籌碼和基本面沒有跟上",
    "cf_kbar_winrate": "這個K棒型態在這檔股票的歷史紀錄裡，隔天上漲的機率只有 {win}%",
    "cf_rev_weak": "營收在成長，但股價趨勢偏弱——基本面好、市場還沒買單",
    "top_problem_none": "目前沒有明顯矛盾",

    # 關鍵價位
    "lv_support": "支撐 {v}（{desc}）",
    "lv_resistance": "壓力 {v}（{desc}）",
    "lv_stop": "失效位置 {v}（距現價 {pct}%，收盤跌破代表目前型態失效）",
    "lv_target1": "前方壓力區 {v}",
    "lv_target2": "延伸觀察價位 {v}",
    "lv_ma20": "月線 {v}",
    "lv_turtle": "海龜通道下緣 {v}（收盤跌破代表突破失敗）",
    "lv_neck": "{ptype}頸線 {v}",

    # 情境（條件式，不是預測）
    "sc_bull_up": "收盤站穩 {resistance} 並且放量 → 突破成立，下一個觀察價位 {target2}",
    "sc_bull_down": "收盤跌破失效位置 {stop_loss} → 這波轉強失敗，多方結構失效",
    "sc_neutral_up": "收盤突破 {resistance} → 轉為偏多結構",
    "sc_neutral_down": "收盤跌破 {support} → 轉為偏空結構",
    "sc_bear_up": "收盤站回月線 {ma20} 以上 → 出現止跌訊號",
    "sc_bear_down": "繼續跌破 {support} → 空方結構延續，下一個支撐需重新確認",

    # 觀察重點（2026/09/17 案件008：原「操作參考」，改成只寫條件與失效位置，不寫買賣動作；key 名稱沿用）
    "act_bull": "多方結構維持；觀察重點是失效位置 {stop_loss} 是否守住，前方壓力區 {target1}",
    "act_bull_wait": "短線位置偏高；觀察回到支撐 {support} 附近時是否出現止跌K棒，失效位置 {stop_loss}",
    "act_bull_caution": "偏多但雜音多；收盤跌破 {stop_loss} 代表這波轉強失效",
    "act_neutral": "方向未明；觀察收盤突破 {resistance} 或跌破 {support} 的方向",
    "act_bear": "空方結構；觀察能否止跌，收盤跌破 {support} 代表弱勢延續",
}


# ══════════════════════════════════════════════════════════
# 📘 教學說明（2026/09/17 帥哥鴻定案 B 方案：綜合解說每一條可展開「這代表什麼？」）
# 原則（案件008）：只解釋指標／型態的一般意義，可帶入今天的數字，不寫買賣動作。
# 改字只要改這裡；{大括號} 會帶入數字，缺欄位時整句仍會顯示（大括號原文去掉）。
# 分層：VERDICT_EDU_TIER——basic（一句話結論、觀察重點、看解說的順序）所有人；full 其餘付費。
# ══════════════════════════════════════════════════════════
VERDICT_EDU_TIER = {"basic": "free", "full": "paid"}

VERDICT_EDU_GUIDE = [
    "先看一句話結論：多方佔優、空方佔優，還是多空拉鋸",
    "再看看多／看空理由：每一條是哪個指標給出的訊號",
    "接著看矛盾：訊號互相打架的地方，通常就是需要特別留意的地方",
    "最後看關鍵價位與情境：出現什麼條件，現在的判讀就需要改變",
]

VERDICT_EDU = {
    # 一句話結論（依立場）
    "head_bull": "系統把每個指標轉成「看多」或「看空」的理由並加權計分。看多分數明顯高於看空，代表目前多方條件較多；但分數描述的是現在的狀態，不是對未來的預測。",
    "head_bull_wait": "多方條件佔優，但同時出現「位置偏高」的訊號（接近壓力、乖離偏大或 KD 高檔）。這種組合常見的狀況是：方向偏多，但短線已經走了一段，容易先整理。",
    "head_bull_caution": "看多分數較高，但看空理由也不少。可以把它理解成「多方佔上風，但雜音不少」，下面列出的看空理由就是需要留意的地方。",
    "head_neutral": "看多和看空的分數差距不大，代表指標之間意見分歧。拉鋸時，市場常見的走法是先在區間內整理，直到突破壓力或跌破支撐才出現方向。",
    "head_bear": "看空分數明顯高於看多，代表目前空方條件較多。空方結構中，判斷止跌通常要看股價能不能重新站回月線、或出現明確的止跌 K 棒。",
    # 觀察重點
    "action": "「觀察重點」整理的是接下來要看的條件，而不是要做的動作。多數條件都以收盤價確認，因為盤中價格常常短暫穿過關鍵價位又回來（假突破、假跌破）。",
    # 現在的狀況
    "status_price": "位置百分比是把「支撐到壓力」當成 0～100%。現在 {pos}% 表示{pos_hint}。",
    "status_trend": "趨勢用「道氏理論」判斷：近期的高點和低點都越來越高，叫上升趨勢（頭頭高、底底高）；都越來越低叫下降趨勢；看不出方向就是盤整。",
    "status_ma": "均線是一段期間收盤價的平均。短天期均線在上、長天期在下叫「多頭排列」，代表最近買進的人成本越來越高；反過來叫「空頭排列」。均線反應較慢，適合看中期方向。",
    "status_ms": "12金叉是 12 種常見的轉強條件。「今天剛轉強」是今天才出現的訊號，「轉強中」是前幾天出現、目前仍維持。涵蓋的面向越多（技術、籌碼、型態、營收），代表不同角度的訊號越一致。",
    "status_basis": "分析基準是支撐、壓力、失效位置這些數字所用的收盤資料日期。盤中或收盤後官方資料更新前，現價和分析基準可能不是同一天。",
    # 看多理由
    "trend_up": "上升趨勢代表近期每一次拉回的低點都比前一次高，買方願意用更高的價格承接。這個結構被破壞的訊號，是跌破前一個低點。",
    "ma_bull": "均線多頭排列代表短、中、長期的平均成本依序往上，中期方向向上。它反應比較慢，適合看大方向，不適合抓短線轉折。",
    "breakout": "突破前高代表股價站上前一次上漲沒能越過的價位。突破是否有效，常見的確認方式是：有沒有放量、之後回測時守不守得住突破的位置。",
    "kbar_bull": "{kbar_edu}",
    "kd_gold": "KD 黃金交叉是 K 值由下往上穿過 D 值，代表短線動能轉強。目前 K 值 {k}，{kd_zone_hint}",
    "macd_bull": "MACD 在 0 軸以上代表多方結構還在；DIF 在 DEA 上方代表動能偏多。如果柱體在縮小，代表上漲的力道正在減弱。",
    "inst_buy": "三大法人合計買超 {inst_total} 張，但要拆開看：外資 {f5}、投信 {i5}、自營商 {d5}。{inst_hint}",
    "vol_up": "量能放大代表參與的人變多。股價上漲同時放量，通常被視為買盤積極；如果放量卻收黑，意思就不同了。",
    "gann_buy": "葛蘭碧法則是用股價和均線的相對位置判斷訊號，一共有 4 個多方、4 個空方訊號。這裡出現的是多方訊號，代表股價和均線的關係符合其中一種轉強型態。",
    "near_sup_rr": "股價靠近支撐時，離失效位置近、離壓力遠，所以損益比通常比較高。支撐是否真的守住，要看接下來的收盤。",
    "ms_many": "12金叉有 3 項以上同時在今天轉強，代表多個不同指標在同一天出現訊號，比單一指標更值得留意。",
    "ms_some": "12金叉今天有少數項目轉強。單一或少數訊號的參考性比多項同時出現弱，可以搭配其他理由一起看。",
    "revenue": "營收連續年增但股價還沒漲，代表基本面在變好、市場價格還沒反應。這種落差有可能之後被補上，也可能反映市場有其他疑慮。",
    "fund": "本益比、殖利率、EPS 是基本面指標：本益比越高代表市場給的評價越高；殖利率是現金股利除以股價。它們描述的是估值，和短線走勢不一定同步。",
    # 看空理由
    "trend_down": "下降趨勢代表近期每一次反彈的高點都比前一次低，賣方持續在更低的價格出售。這個結構被破壞的訊號，是站上前一個高點。",
    "ma_bear": "均線空頭排列代表短、中、長期的平均成本依序往下，最近買進的人多半處在帳面虧損，反彈時容易遇到賣壓。",
    "breakdown": "跌破支撐代表原本有買盤承接的價位失守，原來的支撐常會變成之後的壓力。",
    "kbar_bear": "{kbar_edu}",
    "vp_exit": "爆量收出賣壓型態的 K 棒，代表大量成交發生在賣方佔優的情況下，常被視為高檔換手或出貨的訊號。隔天能不能收復這根 K 棒的中間價位，是判斷賣壓是否延續的常見方式。",
    "kd_death": "KD 死亡交叉是 K 值由上往下穿過 D 值，代表短線動能轉弱。目前 K 值 {k}，{kd_zone_hint}",
    "macd_bear": "MACD 在 0 軸以下代表空方結構；DIF 在 DEA 下方代表動能偏空。柱體縮小則代表下跌力道在減弱。",
    "inst_sell": "外資、投信同時賣超，代表兩大法人近期都在減碼這檔股票。法人部位大，持續賣超時股價較容易有壓力。",
    "gann_sell": "葛蘭碧法則的空方訊號，代表股價和均線的關係出現轉弱型態，例如跌破均線、或離均線太遠（乖離過大）。",
    "near_res": "股價離壓力只剩一小段，上方空間有限。壓力是過去賣壓集中的價位，接近時常出現拉回或整理，要放量才比較容易突破。",
    "rr_low": "損益比 ＝ 前方空間 ÷ 到失效位置的距離。低於 1 代表往下的距離比往上的空間還大，也就是目前位置的風險結構不理想。",
    "channel_conflict": "軌道是用近期高低點畫出的上下通道。趨勢方向和軌道方向不一致時，代表長短期的結構在打架，判讀的可信度會降低。",
    "overheat": "乖離率是股價離均線多遠。離月線 {bias20}% 屬於偏大，就像跑太快總要喘口氣，這時比較容易出現回檔或整理，讓股價和均線重新靠近。",
    "kd_high": "KD 在 80 以上是高檔區，代表短線漲勢強。但強勢股的 KD 常常在高檔「鈍化」（一直維持高檔），所以高檔本身不是轉弱，出現死亡交叉才比較明確。",
    # 矛盾
    "cf_price_inst": "價格往上但法人在賣，代表上漲的買盤可能來自散戶或短線資金。價格和籌碼方向一致時，訊號的可信度比較高。",
    "cf_break_kbar": "突破當天卻收出空頭 K 棒，代表突破後馬上遇到賣壓。這是「假突破」常見的樣子，通常要看隔天能不能守住突破位置。",
    "cf_break_novol": "沒有量的突破，代表參與的人不多，比較容易被後續的賣壓壓回。常見的觀察是突破後幾天有沒有補量。",
    "cf_kd_high_gold": "KD 在高檔出現金叉，比較像漲勢末段的延續，而不是起漲點；低檔（20 以下）出現的金叉，通常才被視為轉折。",
    "cf_macd_below0": "MACD 在 0 軸下方出現金叉，代表空頭結構裡的反彈。要站回 0 軸以上，才比較接近正式轉多。",
    "cf_trend_ma": "高低點結構和均線排列方向不同，通常發生在趨勢剛轉換的時候：高低點反應快，均線反應慢。",
    "cf_single_face": "轉強訊號全部來自技術面，代表只有價格和成交量在動，籌碼和基本面還沒有同步。不同面向一起出現時，訊號比較完整。",
    "cf_kbar_winrate": "同一檔股票過去出現這個 K 棒型態後，隔天上漲的比例偏低。歷史統計不代表未來，但可以提醒這個型態在這檔股票上不一定可靠。",
    "cf_rev_weak": "營收成長但股價趨勢偏弱，代表基本面和市場價格方向不一致，可能是市場還沒反應，也可能是市場在意其他因素。",
    "top_problem": "「最大的問題」是從看空理由中挑出影響權重最高的一條，代表目前最需要留意的訊號。",
    # 關鍵價位
    "lv_support": "支撐是過去買盤集中、股價不容易跌破的價位。系統會綜合近期低點、密集成交區、均線來找。",
    "lv_resistance": "壓力是過去賣盤集中、股價不容易站穩的價位，通常是前波高點或密集套牢區。",
    "lv_stop": "失效位置是系統依支撐與型態算出的價位。收盤跌破，代表目前這個技術型態的前提不成立，原本的判讀要重新看。它是判讀條件，不是叫你在這裡做任何動作。",
    "lv_target1": "前方壓力區是股價往上時第一個可能遇到賣壓的位置，也是計算損益比時用的「前方空間」。",
    "lv_target2": "延伸觀察價位是突破第一個壓力後，下一個可能遇到賣壓的位置，通常由軌道或等幅推算而來。",
    "lv_ma20": "月線是 20 日均線，約等於最近一個月買進的人的平均成本，是短中期多空的常見分界。",
    "lv_turtle": "海龜通道是用過去一段期間的最高價、最低價畫出的通道。突破上緣代表創新高；跌回下緣以下，代表這次突破沒有延續。",
    "lv_neck": "頸線是 W 底、頭肩底這類型態的關鍵線。收盤站上頸線才算型態完成；「等幅推算」是把型態高度往上加，得到一個觀察價位。",
    # 情境
    "scenarios": "情境是「如果出現某個條件，結構會怎麼變化」的整理，不是預測。都以收盤價確認，比較能過濾盤中的假突破、假跌破。",
}

# K 棒型態教學（依型態名稱比對，一檔可能同時出現多個型態）
KBAR_EDU = [
    ("長上影黑K", "長上影黑K：盤中曾經往上衝，最後被賣回來，留下長長的上影線，代表上方有賣壓。"),
    ("長下影紅K", "長下影紅K：盤中曾經往下殺，最後被買回來，留下長長的下影線，代表下方有承接。"),
    ("空頭吞噬", "空頭吞噬：今天的黑K把前一根紅K整根包住，出現在漲一段之後，是常見的短線轉弱訊號。判斷是否成立，常看隔天能不能收回今天高點的一半。"),
    ("多頭吞噬", "多頭吞噬：今天的紅K把前一根黑K整根包住，出現在跌一段之後，是常見的止跌轉強訊號，通常看隔天是否繼續收紅確認。"),
    ("射擊之星", "射擊之星：小實體加上很長的上影線，出現在高檔，代表買方衝高後被賣方壓回，是頂部反轉型態之一。"),
    ("錘頭", "錘頭線：小實體加上很長的下影線，出現在低檔，代表賣方殺低後被買方撐回，是底部反轉型態之一。"),
    ("十字星", "十字星：開盤價和收盤價幾乎一樣，代表多空力量暫時平衡，常出現在方向轉換之前，要看下一根 K 棒決定方向。"),
    ("大紅棒", "大紅棒：實體很長的紅K，代表買方從開盤到收盤都佔優勢，是強勢的表現。"),
    ("大黑棒", "大黑棒：實體很長的黑K，代表賣方從開盤到收盤都佔優勢，是弱勢的表現。"),
    ("孕線", "孕線：今天的 K 棒完全落在前一根 K 棒的範圍內，代表波動收斂、多空暫時休息，之後往哪邊突破是觀察重點。"),
    ("穿刺線", "穿刺線：跌勢中出現紅K，收盤回到前一根黑K實體的一半以上，是潛在的止跌訊號。"),
    ("烏雲蓋頂", "烏雲蓋頂：漲勢中出現黑K，收盤跌進前一根紅K實體的一半以下，是潛在的轉弱訊號。"),
    ("早晨之星", "早晨之星：黑K、小實體、紅K三根組成，出現在低檔，是較強的底部反轉型態。"),
    ("黃昏之星", "黃昏之星：紅K、小實體、黑K三根組成，出現在高檔，是較強的頂部反轉型態。"),
    ("三紅兵", "三紅兵：連續三根收盤越來越高的紅K，代表多方持續推進；但連漲之後，短線乖離也會變大。"),
    ("三烏鴉", "三烏鴉：連續三根收盤越來越低的黑K，代表空方持續壓低。"),
    ("漲停", "漲停：股價漲到當日上限，代表買盤非常強；隔天能不能延續，常看開盤後的量價。"),
    ("跌停", "跌停：股價跌到當日下限，代表賣壓非常重。"),
]


def _vedu(key: str, **kw) -> str:
    t = VERDICT_EDU.get(key, "")
    try:
        return t.format(**kw)
    except Exception:
        import re as _re_e
        return _re_e.sub(r"\{[^}]*\}", "", t)


def _kbar_edu_text(kbar: str) -> str:
    parts = [txt for key, txt in KBAR_EDU if key in (kbar or "")]
    return "\n".join(parts) if parts else "K 棒是用開盤、最高、最低、收盤四個價格畫出的圖形，實體和影線的長短，反映當天買賣雙方誰比較強。"


def _vt(key: str, **kw) -> str:
    """套模版；缺欄位時不讓整段壞掉，直接回傳模版原文去掉大括號"""
    t = VERDICT_TEXT.get(key, "")
    try:
        return t.format(**kw)
    except Exception:
        return t


def _ms_summary(ms: list | None) -> dict:
    """把 _ms_evaluate 的結果整理成解說/前端用的精簡格式"""
    if not ms:
        return {"available": False}
    items = []
    for r in ms:
        label, cat = MULTI_SIGNAL_METHODS.get(r["method"], (r["method"], r["category"]))
        ex = r.get("extra") or {}
        items.append({
            "method": r["method"], "label": label, "category": cat,
            "state": r.get("state", "none"), "days": r.get("days"),
            "missing": bool(ex.get("missing")),
            "detail": _ms_detail_text(r["method"], {**ex, "vol_ratio": r.get("value")})
                      if r.get("passed") else _ms_state_text(r, ex),
        })
    today = [x for x in items if x["state"] == "today"]
    active = [x for x in items if x["state"] == "active"]
    cats = sorted({x["category"] for x in today + active})
    return {
        "available": True, "data_date": (ms[0].get("extra") or {}).get("data_date"),
        "today_count": len(today), "active_count": len(active),
        "today_categories": sorted({x["category"] for x in today}),
        "categories": cats, "items": items, "total": len(MULTI_SIGNAL_METHODS),
    }


def _ms_state_text(r: dict, ex: dict) -> str:
    """「轉強中／未轉強」的白話說明"""
    if ex.get("missing"):
        return ex.get("note", "資料不足")
    m, st, d = r["method"], r.get("state"), r.get("days")
    if st != "active":
        if m == "revenue":
            if ex.get("grow") and not ex.get("not_run"):
                return f"營收有成長，但股價已先漲（近20天 {ex.get('chg20')}%／位於近60日區間 {ex.get('pos60')}%）"
            return "近3個月營收沒有全部年增"
        if m == "institution":
            return f"法人目前連買 {ex.get('streak', 0)} 天"
        return "未轉強"
    slb = MULTI_SIGNAL_CFG.get("state_lookback", 20)
    day_txt = (f"已持續 {slb} 天以上" if d >= slb else f"已持續 {d} 天") if d else "持續中"
    since = ex.get("since_date")
    return f"轉強中（{day_txt}{'，' + since[5:] + ' 開始' if since else ''}）"


def _build_verdict_edu(r, stance, kv, bull, bear, conflicts, status_keys, level_keys, pos, kd, inst) -> dict:
    """綜合解說的📘教學說明，逐條對齊 sections 的順序"""
    k_val = kd.get("k")
    if k_val is None:
        kd_zone_hint = ""
    elif k_val >= 80:
        kd_zone_hint = "位在 80 以上的高檔區，高檔的交叉訊號通常比低檔更敏感。"
    elif k_val >= 50:
        kd_zone_hint = "位在 50～80 的偏高區，前面已經漲過一段，轉弱訊號比在低檔出現更值得留意。"
    elif k_val >= 20:
        kd_zone_hint = "位在 20～50 的偏低區。"
    else:
        kd_zone_hint = "位在 20 以下的低檔區，低檔的金叉通常被視為較有意義的轉折。"
    f5, i5, d5 = inst.get("foreign_5d"), inst.get("invest_5d"), inst.get("dealer_5d")
    fmt = lambda v: f"{v:+,} 張" if isinstance(v, (int, float)) else "—"
    inst_hint = ""
    if isinstance(f5, (int, float)) and isinstance(d5, (int, float)):
        if f5 < 0 and d5 > 0:
            inst_hint = "外資在賣、自營商在買，方向不一致；自營商多為短線進出，參考性通常比外資、投信低。"
        elif f5 > 0 and (i5 or 0) > 0:
            inst_hint = "外資和投信同時買超，是法人方向比較一致的情況。"
        else:
            inst_hint = "各法人方向不完全一致時，合計數字的參考性會降低。"
    if pos is None:
        pos_hint = ""
    elif pos >= 70:
        pos_hint = "離壓力比較近、離支撐比較遠：往上的空間剩不多，往下拉回的空間比較大"
    elif pos <= 30:
        pos_hint = "離支撐比較近：往下的距離不遠，往上的空間比較大"
    else:
        pos_hint = "大約在區間中間，上下空間差不多"
    ekw = {**kv, "kd_zone_hint": kd_zone_hint, "f5": fmt(f5), "i5": fmt(i5), "d5": fmt(d5),
           "inst_hint": inst_hint, "pos": pos, "pos_hint": pos_hint,
           "kbar_edu": _kbar_edu_text(r.get("kbar_pattern") or "")}
    srt = lambda arr: [k for k, _, _ in sorted(arr, key=lambda x: -x[1])]
    return {
        "guide": VERDICT_EDU_GUIDE,
        "headline": _vedu("head_" + stance, **ekw),
        "action": _vedu("action", **ekw),
        "status": [_vedu(k, **ekw) for k in status_keys],
        "bull": [_vedu(k, **ekw) for k in srt(bull)],
        "bear": [_vedu(k, **ekw) for k in srt(bear)],
        "conflicts": [_vedu(k, **ekw) for k, _ in conflicts],
        "top_problem": _vedu("top_problem", **ekw),
        "levels": [_vedu(k, **ekw) for k in level_keys],
        "scenarios": _vedu("scenarios", **ekw),
    }


def _build_verdict(r: dict, ms: list | None) -> dict:
    """
    r：_do_analyze 的 result；ms：_ms_evaluate 的結果（週K/月K時為None）。
    回傳 {stance, stance_label, risk_level, headline, sections{...}, ...}
    """
    name = r.get("stock_name") or r.get("stock_id") or ""
    price = float(r.get("price") or 0)
    support = r.get("support")
    resistance = r.get("resistance")
    stop_loss = r.get("stop_loss")
    rr = r.get("risk_reward") or 0
    trend = r.get("trend") or "盤整"
    ma = r.get("ma_alignment") or {}
    kd = r.get("kd_status") or {}
    macd = r.get("macd_status") or {}
    vol = r.get("vol_analysis") or {}
    inst = r.get("institutional") or {}
    radar = r.get("radar") or {}
    kbar = r.get("kbar_pattern") or ""
    kdir = r.get("kbar_dir") or "neutral"
    ms_s = _ms_summary(ms)
    ms_by = {x["method"]: x for x in ms_s.get("items", [])}

    k_val = kd.get("k")
    vol_ratio = vol.get("ratio") or radar.get("vol_ratio") or 1.0
    bias20 = radar.get("bias20")
    ma20 = radar.get("ma20") or (r.get("ma_values") or {}).get("ma20")
    res_pct = round((resistance - price) / price * 100, 1) if (resistance and price) else None
    inst_total = inst.get("total_5d")
    kv = dict(name=name, price=price, support=support, resistance=resistance, stop_loss=stop_loss,
              rr=rr, k=round(k_val) if k_val is not None else "—", vol_ratio=vol_ratio, bias20=bias20,
              res_pct=res_pct, ma20=ma20, target2=r.get("target2"), prev_high=r.get("prev_high"),
              ma_text=ma.get("text", ""), macd_text=macd.get("text", ""), kbar=kbar,
              inst_total=f"{inst_total:+,}" if isinstance(inst_total, (int, float)) else "—")

    bull, bear = [], []   # (key, weight, text)

    def B(key, **extra):
        bull.append((key, VERDICT_WEIGHTS.get(key, 1), _vt(key, **{**kv, **extra})))

    def S(key, **extra):
        bear.append((key, VERDICT_WEIGHTS.get(key, 1), _vt(key, **{**kv, **extra})))

    ma_dir = ma.get("direction")
    if trend == "上升趨勢":
        B("trend_up")
    elif trend == "下降趨勢":
        S("trend_down")
    if ma_dir == "bullish":
        B("ma_bull")
    elif ma_dir == "bearish":
        S("ma_bear")
    is_break = r.get("pattern") == "突破型態"
    if is_break and r.get("prev_high"):
        B("breakout")
    if r.get("pattern") == "跌破型態":
        S("breakdown")
    if kdir == "bullish":
        B("kbar_bull")
    elif kdir == "bearish":
        S("kbar_bear")
    vpw = r.get("vp_exit_warn")
    if vpw:
        S("vp_exit", shape=vpw.get("shape"), vol_x=vpw.get("vol_x"))
    if kd.get("golden_cross"):
        B("kd_gold")
    if kd.get("death_cross"):
        S("kd_death")
    mdir = macd.get("direction") or ""
    if mdir in ("bullish", "slightly_bullish"):
        B("macd_bull")
    elif mdir in ("bearish", "slightly_bearish"):
        S("macd_bear")
    if isinstance(inst_total, (int, float)) and inst_total != 0:
        cb = inst.get("consecutive_buy_days") or 0
        if inst_total > 0:
            B("inst_buy", inst_streak=f"，連買 {cb} 天" if cb >= 2 else "")
        elif inst.get("foreign_5d", 0) < 0 and inst.get("invest_5d", 0) <= 0:
            S("inst_sell")
    if vol_ratio and vol_ratio >= 1.3 and (r.get("price_change_pct") or 0) >= 0:
        B("vol_up")
    g = r.get("gann_recross")
    if g:
        B("gann_buy", gann=f"{g.get('type')}（{g.get('ma')} {g.get('val')}）")
    gs = r.get("gann_sell")
    if gs and not vpw:
        S("gann_sell", gann=f"{gs.get('type')}（{gs.get('ma')} {gs.get('val')}）")
    near_res = res_pct is not None and res_pct < 4 and not is_break
    if support and price and (price - support) / price < 0.04 and rr >= 1.5:
        B("near_sup_rr")
    if near_res:
        S("near_res")
    if rr < 1 and not is_break:
        S("rr_low")
    if r.get("conflict_note"):
        S("channel_conflict", conflict=r["conflict_note"].replace("⚠ 注意：", ""))
    overheat = bias20 is not None and bias20 >= 10
    if overheat:
        S("overheat")
    kd_high = k_val is not None and k_val >= 80
    if kd_high:
        S("kd_high")
    today_items = [x for x in ms_s.get("items", []) if x["state"] == "today"]
    n_today = len(today_items)
    tl = "、".join(x["label"] for x in today_items)
    if n_today >= 3:
        B("ms_many", n=n_today, list=tl)
    elif n_today >= 1:
        B("ms_some", n=n_today, list=tl)
    for _fn in (r.get("fund_notes") or []):
        if "支持" in _fn:
            bull.append(("fund", 1, _fn))
        else:
            bear.append(("fund", 1, _fn))
    rv = ms_by.get("revenue")
    if rv and rv["state"] == "today":
        ex = next((m.get("extra") for m in (ms or []) if m["method"] == "revenue"), {}) or {}
        B("revenue", m=len(ex.get("yoys") or []), yoy=ex.get("yoys", ["—"])[0], chg20=ex.get("chg20"))

    # ── 矛盾 ──
    conflicts = []
    if (trend == "上升趨勢" or is_break) and isinstance(inst_total, (int, float)) and inst_total < 0:
        conflicts.append(("cf_price_inst", _vt("cf_price_inst", **kv)))
    if is_break and (kdir == "bearish" or vpw):
        conflicts.append(("cf_break_kbar", _vt("cf_break_kbar", **kv)))
    if is_break and vol_ratio < 1.0:
        conflicts.append(("cf_break_novol", _vt("cf_break_novol", **kv)))
    if kd.get("golden_cross") and kd_high:
        conflicts.append(("cf_kd_high_gold", _vt("cf_kd_high_gold", **kv)))
    macd_ms = ms_by.get("macd")
    if macd_ms and macd_ms["state"] == "today" and macd.get("dif") is not None and macd.get("dif") < 0:
        conflicts.append(("cf_macd_below0", _vt("cf_macd_below0", **kv)))
    ma_label = {"bullish": "多頭排列", "bearish": "空頭排列"}.get(ma_dir)
    if ma_label and ((trend == "上升趨勢" and ma_dir == "bearish") or (trend == "下降趨勢" and ma_dir == "bullish")):
        conflicts.append(("cf_trend_ma", _vt("cf_trend_ma", trend=trend, ma_label=ma_label)))
    if n_today >= 2 and set(ms_s.get("today_categories", [])) == {"技術面"}:
        conflicts.append(("cf_single_face", _vt("cf_single_face")))
    bt = r.get("kbar_backtest") or {}
    if kdir == "bullish" and bt.get("total", 0) >= 3 and bt.get("win_pct", 50) < 45:
        conflicts.append(("cf_kbar_winrate", _vt("cf_kbar_winrate", win=bt.get("win_pct"))))
    if rv and rv["state"] == "today" and trend == "下降趨勢":
        conflicts.append(("cf_rev_weak", _vt("cf_rev_weak")))

    # ── 立場 ──
    bull_w = sum(w for _, w, _ in bull)
    bear_w = sum(w for _, w, _ in bear)
    net = bull_w - bear_w
    # 最大問題：看空理由裡權重最高的，其次是第一個矛盾
    top_problem = ""
    if bear:
        top_problem = sorted(bear, key=lambda x: -x[1])[0][2]
    elif conflicts:
        top_problem = conflicts[0][1]
    kv2 = {**kv, "bull": len(bull), "bear": len(bear), "top_problem": top_problem or _vt("top_problem_none")}
    ms_part = ""
    if n_today >= 3:
        ms_part = _vt("ms_part_many", n=n_today)
    elif n_today >= 1:
        ms_part = _vt("ms_part_some", n=n_today)

    wait_reason = None
    if near_res:
        wait_reason = _vt("wait_near_res", **kv)
    elif overheat:
        wait_reason = _vt("wait_overheat", **kv)
    elif kd_high:
        wait_reason = _vt("wait_kd_high", **kv)

    if net >= 3 and wait_reason:
        stance, label, level = "bull_wait", "偏多・等拉回", "medium"
        headline = _vt("head_bull_wait", **kv2, wait_reason=wait_reason)
    elif net >= 3 and bear_w >= 3:
        stance, label, level = "bull_caution", "偏多・有雜音", "medium"
        headline = _vt("head_bull_caution", **kv2)
    elif net >= 3:
        stance, label, level = "bull", "偏多", "low"
        headline = _vt("head_bull", **kv2, ms_part=ms_part)
    elif net <= -3:
        stance, label, level = "bear", "偏空結構", "high"
        headline = _vt("head_bear", **kv2)
    else:
        stance, label, level = "neutral", "多空拉鋸・方向未明", "watch"
        headline = _vt("head_neutral", **kv2)

    # ── 現在的狀況 ──
    pos = None
    if support and resistance and resistance > support and price:
        pos = round(min(100, max(0, (price - support) / (resistance - support) * 100)))
    pos_word = "—" if pos is None else ("靠近支撐" if pos < 30 else "靠近壓力" if pos > 70 else "中間位置")
    trend_text = {"上升趨勢": "上升趨勢（頭頭高、底底高）", "下降趨勢": "下降趨勢（頭頭低、底底低）"}.get(
        trend, "盤整（高低點結構不明）")
    status, status_keys = [], []
    if pos is not None:
        status.append(_vt("status_price", **kv, pos=pos, pos_word=pos_word)); status_keys.append("status_price")
    status.append(_vt("status_trend", trend_text=trend_text)); status_keys.append("status_trend")
    if ma.get("text"):
        status.append(_vt("status_ma", **kv)); status_keys.append("status_ma")
    if ms_s.get("available"):
        cats = "、".join(ms_s["categories"]) or "無"
        status.append(_vt("status_ms", today=ms_s["today_count"], active=ms_s["active_count"], cats=cats)); status_keys.append("status_ms")
    if r.get("price_basis_note"):
        status.append(_vt("status_basis", basis=r["price_basis_note"])); status_keys.append("status_basis")

    # ── 關鍵價位 ──
    levels, level_keys = [], []

    def _LV(key, **kw):
        levels.append(_vt(key, **kw)); level_keys.append(key)
    if support:
        _LV("lv_support", v=support, desc=r.get("support_desc") or "")
    if resistance:
        _LV("lv_resistance", v=resistance, desc=r.get("resistance_desc") or "")
    if stop_loss and price:
        _LV("lv_stop", v=stop_loss, pct=round((stop_loss - price) / price * 100, 1))
    if r.get("target1"):
        _LV("lv_target1", v=r["target1"])
    if r.get("target2"):
        _LV("lv_target2", v=r["target2"])
    if ma20 and ma20 != support:
        _LV("lv_ma20", v=ma20)
    for m in (ms or []):
        ex = m.get("extra") or {}
        if m["method"] == "turtle" and m.get("state") in ("today", "active") and ex.get("exit_level"):
            _LV("lv_turtle", v=ex["exit_level"])
        if m["method"] == "pattern" and m.get("passed") and ex.get("neckline"):
            _LV("lv_neck", ptype=ex.get("type", ""), v=ex["neckline"])

    # ── 情境 ──
    if stance.startswith("bull"):
        scenarios = [_vt("sc_bull_up", **kv), _vt("sc_bull_down", **kv)]
    elif stance == "bear":
        scenarios = [_vt("sc_bear_up", **kv) if ma20 else _vt("sc_neutral_up", **kv), _vt("sc_bear_down", **kv)]
    else:
        scenarios = [_vt("sc_neutral_up", **kv), _vt("sc_neutral_down", **kv)]
    action = _vt("act_" + stance, **{**kv, "target1": r.get("target1")})

    # ── 📘 教學說明（跟各段落逐條對齊；沒有說明的放空字串）──
    try:
        edu = _build_verdict_edu(r, stance, kv, bull, bear, conflicts, status_keys, level_keys, pos, kd, inst)
    except Exception as _edu_e:
        print(f"[verdict] 教學說明產生失敗：{_edu_e}")
        edu = {}

    return {
        "version": 1,
        "edu": edu,
        "stance": stance, "stance_label": label, "risk_level": level,
        "bull_score": bull_w, "bear_score": bear_w,
        "headline": headline, "action": action,
        "sections": {
            "headline": headline,
            "status": status,
            "bull": [t for _, _, t in sorted(bull, key=lambda x: -x[1])],
            "bear": [t for _, _, t in sorted(bear, key=lambda x: -x[1])],
            "conflicts": [t for _, t in conflicts],
            "top_problem": top_problem or _vt("top_problem_none"),
            "levels": levels,
            "scenarios": scenarios,
            "action": action,
            "signals": ms_s,
        },
        "tiers": dict(VERDICT_SECTION_TIER),
    }


def _verdict_for_user(v: dict | None, user: dict | None) -> dict | None:
    """依會員身分遮掉看不到的段落（目前：付費看全部；免費/未登入只看一句話結論＋12金叉項數）"""
    if not v:
        return v
    paid = _is_premium(user)
    # 加購層之後接上：addon = paid and _has_addon(user)
    addon = paid
    allow = {"free": True, "paid": paid, "addon": addon}
    secs = v.get("sections") or {}
    out_secs, locked = {}, []
    for k, val in secs.items():
        tier = VERDICT_SECTION_TIER.get(k, "paid")
        if k == "top_problem":
            tier = VERDICT_SECTION_TIER.get("conflicts", "paid")
        if allow.get(tier, False):
            out_secs[k] = val
        else:
            locked.append(k)
    if "signals" in locked and isinstance(secs.get("signals"), dict):
        s = secs["signals"]
        out_secs["signals"] = {"available": s.get("available"), "today_count": s.get("today_count"),
                               "active_count": s.get("active_count"), "total": s.get("total"),
                               "locked": True}
    # 📘 教學說明分層：basic（看解說的順序、一句話結論、觀察重點）所有人；其餘依 VERDICT_EDU_TIER["full"]
    edu = v.get("edu") or {}
    edu_full = allow.get(VERDICT_EDU_TIER.get("full", "paid"), False)
    if edu_full:
        out_edu = edu
    else:
        out_edu = {k: edu[k] for k in ("guide", "headline", "action") if k in edu}
    return {**{k: v[k] for k in v if k not in ("sections", "edu")}, "sections": out_secs, "edu": out_edu,
            "edu_locked": bool(edu) and not edu_full,
            "locked_sections": locked, "locked": bool(locked)}


@app.get("/multi-signal-status")
def multi_signal_status():
    """首頁跑馬燈用：今天12金叉有幾檔轉強、幾檔同時符合3項以上"""
    p = _ms_build_payload()
    if not p.get("scan_date") or p["scan_date"] != _taipei_today():
        return {"available": False}
    items = p.get("data") or []
    return {"available": True, "updated_at": p.get("updated_at"), "count": len(items),
            "high_confidence_count": sum(1 for x in items if x["passed_count"] >= 3)}


@app.get("/multi-signal")
def multi_signal_public_page():
    """
    12金叉選股公開頁（SEO／導流用，2026/09/17取代原本 /deep-analysis 公開頁）。
    跟原本深度選股一樣顯示「上一次」的掃描結果（延遲一個交易日），當天即時名單只在App內給付費會員看。
    """
    import html as _h
    conn = _db_conn()
    try:
        dates = [r[0] for r in conn.execute(
            "SELECT DISTINCT scan_date FROM multi_signal_results ORDER BY scan_date DESC LIMIT 2").fetchall()]
    finally:
        conn.close()
    today = _taipei_today()
    show_date = next((d for d in dates if d < today), None)
    p = _ms_build_payload(show_date) if show_date else {"data": [], "methods": []}
    items = p.get("data") or []
    methods = p.get("methods") or []
    now_s = _taipei_now_str("%Y-%m-%d %H:%M")
    cat_color = {"技術面": "#3B82F6", "籌碼面": "#DC2626", "型態面": "#7C3AED", "基本面": "#D97706"}
    rows = []
    for s in items[:60]:
        sig = "".join(
            f'<li><b style="color:{cat_color.get(x["category"], "#555")}">{_h.escape(x["label"])}</b>'
            f'<span>{_h.escape((x.get("detail") or "").replace("今天", "當天"))}</span></li>' for x in s["signals"])
        chg = s.get("change_pct")
        chg_html = (f'<span class="{"up" if chg > 0 else "dn"}">{chg:+.2f}%</span>' if chg else "")
        rows.append(
            f'<div class="card"><div class="hd"><div><div class="nm">{_h.escape(s["stock_name"] or "")} {chg_html}</div>'
            f'<div class="id">{_h.escape(s["stock_id"])}　收盤 {s.get("price") or "—"}</div></div>'
            f'<div class="cnt"><b>{s["passed_count"]}</b><small>/ 12 項</small></div></div>'
            f'<ul>{sig}</ul>'
            f'<a class="go" href="/stock/?stock={_h.escape(s["stock_id"])}">看這檔的完整分析 ›</a></div>')
    mt = "".join(f'<span class="mt">{_h.escape(m["label"])} <b>{m["passed"]}</b></span>' for m in methods)
    body = "".join(rows) or '<p class="empty">目前還沒有可公開的歷史名單（每個交易日 17:20 更新，公開頁顯示前一個交易日的結果）。</p>'
    title_date = show_date or now_s[:10]
    html_doc = f"""<!DOCTYPE html><html lang="zh-TW"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>12金叉選股｜{title_date} 台股轉強股名單（MACD、KD、均線、法人、營收）｜線上有位</title>
<meta name="description" content="線上有位12金叉選股：每天收盤後用MACD、KD、RSI、月季線、海龜突破、法人連買、底部型態、營收成長等12種方法掃描成交量前150檔，找出當天剛轉強的台股。{title_date} 共 {len(items)} 檔。">
<link rel="canonical" href="{FRONTEND_URL}/multi-signal">
<style>
body{{margin:0;background:#0f172a;color:#e2e8f0;font-family:-apple-system,"PingFang TC","Noto Sans TC",sans-serif}}
.wrap{{max-width:980px;margin:0 auto;padding:20px 16px 40px}}
h1{{font-size:22px;margin:6px 0}} .sub{{color:#94a3b8;font-size:13px;line-height:1.7}}
.note{{background:#1e293b;border:1px solid #334155;border-radius:10px;padding:10px 12px;font-size:12px;color:#cbd5e1;margin:12px 0}}
.mts{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 16px}} .mt{{background:#1e293b;border-radius:14px;padding:4px 10px;font-size:12px;color:#cbd5e1}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
.card{{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:14px}}
.hd{{display:flex;justify-content:space-between;gap:8px}} .nm{{font-size:18px;font-weight:800}} .id{{color:#94a3b8;font-size:12px;margin-top:2px}}
.cnt{{text-align:center;color:#a78bfa}} .cnt b{{font-size:22px;display:block}} .cnt small{{font-size:10px}}
ul{{list-style:none;padding:0;margin:10px 0 0}} li{{font-size:13px;line-height:1.6;padding:2px 0}} li span{{color:#94a3b8;margin-left:6px}}
.up{{color:#f87171;font-size:13px}} .dn{{color:#4ade80;font-size:13px}}
.go{{display:block;text-align:right;color:#4ade80;font-size:12px;font-weight:700;margin-top:10px;text-decoration:none}}
.cta{{display:block;text-align:center;background:#16a34a;color:#fff;border-radius:10px;padding:12px;font-weight:800;text-decoration:none;margin:16px 0}}
.empty{{color:#94a3b8}} .ft{{color:#64748b;font-size:11px;line-height:1.7;margin-top:20px}}
</style></head><body><div class="wrap">
<h1>📊 12金叉選股</h1>
<div class="sub">每天收盤後，用 12 種方法（技術面9項＋法人籌碼＋底部型態＋營收）掃描成交量前 150 檔，找出「當天剛轉強」的股票。同一檔符合的方法越多、涵蓋的面向越多，訊號越值得注意。</div>
<div class="note">⏱️ 本頁顯示 <b>{title_date}</b> 的結果（延遲一個交易日公開）。當天 17:20 的即時名單、每檔股票的綜合解說，請登入App查看。　查詢時間：{now_s}</div>
<a class="cta" href="/stock/?page=multisignal">打開App看今天的即時名單 ›</a>
<div class="mts">{mt}</div>
<div class="grid">{body}</div>
<div class="ft">本頁為自動化篩選結果，只代表該交易日出現轉強訊號，不代表一定會上漲，僅供研究參考，不構成投資建議。股市有風險，請自行評估並嚴設停損。</div>
</div></body></html>"""
    return HTMLResponse(content=html_doc)


@app.get("/api/multi-signal")
def api_multi_signal(user: dict | None = Depends(get_current_user)):
    """
    12金叉選股（用戶頁面用）。2026/09/17帥哥鴻調整分層：
      付費有效 → 全部完整
      免費會員 → 同時符合「2個以下」的股票完整看得到；3個以上的在伺服器端就遮罩代號／名稱
      未登入   → 只給方法統計＋幾張遮罩佔位卡（_picks_payload 弱預覽），登入後才看得到
    """
    p = _ms_build_payload()
    items = p.pop("data")
    free_max = MULTI_SIGNAL_FREE_MAX
    base = {**p, "server_time": _taipei_now_str("%Y-%m-%d %H:%M"),
            "max_count": max([x["passed_count"] for x in items] or [0]),
            "free_max": free_max}
    if _deep_is_premium(user):
        return {**base, "data": items, "masked": False, "tier": "paid", "preview": False}
    if user:
        return {**base, "data": [x if x["passed_count"] <= free_max else _deep_mask_item(dict(x))
                                 for x in items],
                "masked": any(x["passed_count"] > free_max for x in items),
                "tier": "free", "preview": False}
    pv = _picks_payload(items, p.get("updated_at"), user)
    return {**base, "data": pv["data"], "approx_count": pv.get("approx_count"),
            "masked": True, "tier": "guest", "preview": True}


class _MultiSignalRunReq(BaseModel):
    stock_ids: list[str] | None = None   # 測試用：只跑指定股票；不帶＝正式跑成交量前150


@app.post("/admin/run-multi-signal-scan")
async def admin_run_multi_signal_scan(req: _MultiSignalRunReq | None = None,
                                      key: str = Header(..., alias="X-Admin-Key")):
    """管理員手動觸發12金叉選股掃描（背景執行，約2～4分鐘）"""
    _check_admin(key)
    if _MULTI_SIGNAL_LOCK.locked():
        return {"ok": False, "msg": "已有一輪在執行中，請稍後用「查看結果」確認進度"}
    ids = (req.stock_ids if req else None) or None
    t = _ms_threading.Thread(target=_run_multi_signal_scan_job,
                             kwargs={"stock_ids": ids, "force": True}, daemon=True)
    t.start()
    return {"ok": True, "msg": "12金叉選股已開始執行（背景）" + (f"，測試{len(ids)}檔" if ids else "")}


@app.get("/admin/multi-signal-results")
def admin_multi_signal_results(scan_date: str = "", key: str = Header(default="", alias="X-Admin-Key")):
    """查看12金叉選股某一天的結果（不帶日期＝最近一次有資料的日期）＋最近一輪執行狀態"""
    _check_admin(key)
    p = _ms_build_payload(scan_date)
    ranking = [{"stock_id": s["stock_id"], "stock_name": s["stock_name"],
                "passed_count": s["passed_count"], "category_count": s["category_count"],
                "passed_methods": [x["label"] for x in s["signals"]]} for s in p["data"]]
    by_method = {}
    for s in p["data"]:
        for x in s["signals"]:
            by_method.setdefault(x["method"], []).append(
                {"stock_id": s["stock_id"], "stock_name": s["stock_name"]})
    methods = [{**m, "passed_stocks": by_method.get(m["method"], [])} for m in p["methods"]]
    return {"scan_date": p["scan_date"], "stock_count": p["stock_count"], "row_count": p["row_count"],
            "methods": methods, "ranking": ranking, "status": dict(_MULTI_SIGNAL_STATUS)}


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
        # 2026/09/15修正：原本呼叫一個不存在的 _decode_token（NameError被下面的except吞掉），
        # 而且關掉DB連線後又拿它查暱稱，導致登入會員進聊天室永遠顯示「訪客」、沒有付費徽章。
        # 改成跟 get_current_user 同一套：_jwt_verify 驗證、sub 是會員id、token_ver 要一致。
        try:
            payload = _jwt_verify(token) or {}
            if payload.get("sub") is not None:
                conn = _db_conn()
                row = conn.execute("SELECT * FROM members WHERE id=?", (payload["sub"],)).fetchone()
                conn.close()
                if row and row["token_ver"] == payload.get("ver", 0):
                    u = dict(row)
                    username = u.get("nickname") or str(u.get("email", "")).split("@")[0] or "訪客"
                    is_paid = _is_premium(u)
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
    """取得主題列表（訪客只看標題，登入即可看全文，發文／留言才需要付費會員——
    2026/09/14修正：這行docstring原本誤寫成「付費會員看全文」，跟下面第11488行
    `if user:`（只檢查有沒有登入，沒有檢查是否付費）的實際邏輯不符，也跟前端UI提示文字
    「🔒登入後可看內文，留言需付費」矛盾。案件004論壇範圍測試時發現這個文件與實際行為
    不一致，查證後確認程式邏輯本身是對的、只是說明文字寫錯，這裡只更新文字，不改邏輯）"""
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
        today = _taipei_today()
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
        if user:
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

    if not user:
        conn.close()
        raise HTTPException(status_code=403, detail="請先登入後查看討論內容")
    # 免費可看；留言／發文仍 require_paid_user

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
                    "INSERT OR REPLACE INTO stock_reports (stock_id, report_date, stock_name, report_html, price_basis_date) VALUES (?,?,?,?,?)",
                    (sid, today, sname, report_html, d.get("price_basis_date"))
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
    key: str = Header(..., alias="X-Admin-Key"),
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
