# -*- coding: utf-8 -*-
"""
線上有位 案件016：市場族群模組（2026/09/25 正式接入 main.py；原稿在 scripts/market_groups.py）

設計原則
- 行情統一取得一次 → 後端統一計算一次 → 快取 → 所有使用者共用
- 低耦合：本模組不 import main.py。main.py 只需要把「抓即時報價」「取得產業別」
  兩個函式傳進來（依賴注入），再加一個排程與三個 API。
- 活躍度公式、族群清單都可替換，不寫死。

main.py 接入方式（09/25 已照這個接入，見 main.py「案件016 市場星系」區塊）：
    from market_groups import MarketGroupsEngine
    _MARKET_GROUPS = MarketGroupsEngine(
        db_path=DB_PATH,
        theme_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_theme_map.json"),
        fetch_quotes=_mis_batch_quotes,                    # 既有：一次 20 檔、20 秒快取
        get_industry_info=get_all_stock_info,              # 既有：FinMind TaiwanStockInfo（失敗自動用資料庫備份）
        ssl_context=_TWSE_SSL_CTX,
    )
    # lifespan() 內：
    _bg_scheduler.add_job(_MARKET_GROUPS.tick, "interval", minutes=5, max_instances=1, coalesce=True)
    # 路由：
    @app.get("/api/market/groups")          -> _MARKET_GROUPS.get_overview()
    @app.get("/api/market/groups/timeline") -> _MARKET_GROUPS.get_timeline(date)
    @app.get("/api/market/groups/{gid}")    -> _MARKET_GROUPS.get_group(gid)
"""
import csv
import io
import json
import sqlite3
import threading
import time
import urllib.request
from datetime import datetime, timedelta, timezone

TW = timezone(timedelta(hours=8))

TWSE_EOD_URL = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY_ALL"
TPEX_EOD_URL = "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes"
UMBRELLA_INDUSTRIES = {"電子工業"}
KEEP_DAYS = 10          # 時間軸保留天數（跟 intraday_ticks 一樣 10 天）


# ───────────────────────── 小工具 ─────────────────────────
def _num(v):
    if v is None:
        return None
    s = str(v).strip().strip('="').replace(",", "").replace("+", "")
    if s in ("", "-", "--", "---", "X", "N/A", "除權息", "除權", "除息"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def norm_date(s):
    """115/09/23、1150923、20260923、2026-09-23 → 2026-09-23；無法辨識就原樣回傳"""
    t = str(s or "").strip().replace("/", "").replace("-", "")
    if not t.isdigit():
        return str(s or "")
    if len(t) == 7:
        t = str(int(t[:3]) + 1911) + t[3:]
    return f"{t[:4]}-{t[4:6]}-{t[6:8]}" if len(t) == 8 else str(s)


def is_common_stock(code):
    """一般個股：4 位數字、不是 0 開頭（排除 0050 等 ETF）"""
    return len(code) == 4 and code.isdigit() and not code.startswith("0")


def default_activity(groups, total_turnover):
    """【暫定】活躍度＝族群成交占比 ÷ 最高占比 × 100。正式公式待帥哥鴻／GPT 拍板，可整支替換。"""
    max_share = max((g["turnover"] / total_turnover for g in groups), default=0) or 1
    for g in groups:
        g["activity_score"] = round(g["turnover"] / total_turnover / max_share * 100)


# ───────────────────────── 盤後資料（每天一次） ─────────────────────────
def fetch_eod(ssl_context=None, timeout=20):
    """證交所 STOCK_DAY_ALL＋櫃買盤後 → {code: {...}}。任一來源失敗就略過該來源。"""
    out, errors = {}, []
    try:
        req = urllib.request.Request(TWSE_EOD_URL, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Referer": "https://www.twse.com.tw/"})
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as r:
            text = r.read().decode("utf-8-sig", errors="replace")
        for row in csv.reader(io.StringIO(text)):
            if len(row) < 10:
                continue
            code = str(row[1]).strip().strip('="').strip()
            if not is_common_stock(code):
                continue
            out[code] = {"code": code, "name": str(row[2]).strip().strip('="').strip(), "market": "TWSE",
                         "volume_shares": _num(row[3]) or 0, "turnover": _num(row[4]),
                         "close": _num(row[8]), "change": _num(row[9]),
                         "trade_date": str(row[0]).strip().strip('="').strip()}
    except Exception as e:
        errors.append(f"TWSE: {e}")
    try:
        req = urllib.request.Request(TPEX_EOD_URL, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as r:
            arr = json.loads(r.read().decode("utf-8-sig", errors="replace")) or []
        for it in arr:
            code = str(it.get("SecuritiesCompanyCode", "")).strip()
            if not is_common_stock(code) or code in out:
                continue
            out[code] = {"code": code, "name": str(it.get("CompanyName", "")).strip(), "market": "TPEx",
                         "volume_shares": _num(it.get("TradingShares")) or 0,
                         "turnover": _num(it.get("TransactionAmount")),
                         "close": _num(it.get("Close")), "change": _num(it.get("Change")),
                         "trade_date": str(it.get("Date", ""))}
    except Exception as e:
        errors.append(f"TPEx: {e}")
    return out, errors


def industry_map(stock_info_rows):
    """FinMind TaiwanStockInfo 原始列 → {code: set(產業別)}（一檔可能多列）"""
    m = {}
    for r in stock_info_rows or []:
        code = str(r.get("stock_id", "")).strip()
        ind = str(r.get("industry_category", "") or "").strip()
        if code and ind:
            m.setdefault(code, set()).add(ind)
    return m


def load_themes(path, industries):
    with open(path, encoding="utf-8") as f:
        themes = json.load(f)["themes"]
    members, explicit = {}, set()
    for t in themes:
        for c in t.get("codes", []):
            explicit.add(c)
            members.setdefault(c, [])
            if t["group_id"] not in members[c]:
                members[c].append(t["group_id"])
        want = set(t.get("industries", []))
        if want:
            for code, inds in industries.items():
                if inds & want:
                    members.setdefault(code, [])
                    if t["group_id"] not in members[code]:
                        members[code].append(t["group_id"])
    return themes, members, explicit


# ───────────────────────── 快照計算（純函式，可單獨測） ─────────────────────────
def market_state(now, quote_date):
    if now.weekday() >= 5:
        return "holiday"
    hm = now.hour * 100 + now.minute
    if hm < 900:
        return "pre_open"
    if hm >= 905 and quote_date and quote_date != now.strftime("%Y-%m-%d"):
        return "holiday"
    return "open" if hm <= 1330 else "closed"


def stock_rows(eod, quotes, industries, members, live):
    rows = []
    for code, e in eod.items():
        if not is_common_stock(code):
            continue
        q = quotes.get(code) if live else None
        if live:
            if not q or not q.get("price") or not q.get("y"):
                continue
            price, prev = q["price"], q["y"]
            vol_lots = (q.get("volume") or 0) / 1000 if "volume" in q else (q.get("volume_lots") or 0)
            turnover = vol_lots * 1000 * price          # MIS 沒有成交金額 → 估算
        else:
            price = e.get("close")
            prev = price - e["change"] if (price is not None and e.get("change") is not None) else None
            vol_lots = (e.get("volume_shares") or 0) / 1000
            turnover = e.get("turnover") or ((e.get("volume_shares") or 0) * (price or 0))
        if not price or not turnover:
            continue
        change = round(price - prev, 2) if prev else None
        inds = sorted(industries.get(code, set()) - UMBRELLA_INDUSTRIES)
        rows.append({"code": code, "name": e.get("name", ""), "market": e.get("market", ""),
                     "price": price, "change": change,
                     "change_pct": round(change / prev * 100, 2) if (change is not None and prev) else None,
                     "volume": int(round(vol_lots)), "turnover": int(turnover),
                     "range20_pos": None, "range20_low": None, "range20_high": None,
                     "group_ids": list(members.get(code, [])),
                     "official_industry": "、".join(inds)})
    rows.sort(key=lambda r: -r["turnover"])
    return rows


def group_stats(pool, themes, activity_fn=default_activity):
    theme_by_id = {t["group_id"]: t for t in themes}
    total = sum(r["turnover"] for r in pool) or 1
    acc = {}
    for r in pool:
        for gid in r["group_ids"]:
            t = theme_by_id.get(gid)
            if not t:
                continue
            g = acc.setdefault(gid, {"group_id": gid, "name": t["name"],
                                     "cluster_id": t.get("cluster_id", ""), "cluster_name": t.get("cluster_name", ""),
                                     "turnover": 0, "active_count": 0, "up_count": 0, "down_count": 0,
                                     "flat_count": 0, "_pcts": [], "_stocks": []})
            g["turnover"] += r["turnover"]
            g["active_count"] += 1
            ch = r["change"]
            g["flat_count" if not ch else ("up_count" if ch > 0 else "down_count")] += 1
            if r["change_pct"] is not None:
                g["_pcts"].append(r["change_pct"])
            g["_stocks"].append(r)
    groups = list(acc.values())
    for g in groups:
        g["turnover_share"] = round(g["turnover"] / total, 4)
        g["avg_change_pct"] = round(sum(g["_pcts"]) / len(g["_pcts"]), 2) if g["_pcts"] else None
        g["top_codes"] = [s["code"] for s in sorted(g["_stocks"], key=lambda s: -s["turnover"])[:5]]
        del g["_pcts"], g["_stocks"]
    activity_fn(groups, total)
    groups.sort(key=lambda g: -g["activity_score"])
    return groups


def cluster_stats(pool, themes):
    """星團成交占比（去重）：同一檔股票在同一星團多個族群裡只算一次。"""
    cid_of = {t["group_id"]: (t.get("cluster_id", ""), t.get("cluster_name", "")) for t in themes}
    total = sum(r["turnover"] for r in pool) or 1
    acc = {}
    for r in pool:
        for cid in {cid_of[g][0] for g in r["group_ids"] if g in cid_of}:
            acc[cid] = acc.get(cid, 0) + r["turnover"]
    names = {c: n for c, n in cid_of.values()}
    return [{"cluster_id": c, "cluster_name": names.get(c, c), "turnover_share": round(v / total, 4)}
            for c, v in sorted(acc.items(), key=lambda x: -x[1])]


def build_snapshot(eod, quotes, industries, themes, members, n, now,
                   prev_groups=None, base_shares=None, activity_fn=default_activity):
    q_date = next((q.get("date") for q in quotes.values() if q.get("date")), "")
    state = market_state(now, q_date)
    today = now.strftime("%Y-%m-%d")
    live = state in ("open", "closed") and q_date == today and any(q.get("price") for q in quotes.values())
    pool = stock_rows(eod, quotes, industries, members, live)[:n]
    groups = group_stats(pool, themes, activity_fn)
    prev = {g["group_id"]: g["activity_score"] for g in (prev_groups or [])}
    for g in groups:
        g["activity_change"] = g["activity_score"] - prev[g["group_id"]] if g["group_id"] in prev else 0
        b = (base_shares or {}).get(g["group_id"])
        g["share_vs_prev_day"] = round(g["turnover_share"] / b, 2) if b else None
    eod_date = norm_date(next((e.get("trade_date") for e in eod.values() if e.get("trade_date")), ""))
    clusters = cluster_stats(pool, themes)
    return {"trade_date": today if live else eod_date, "market_state": state,
            "data_time": now.strftime("%H:%M") if (live and state == "open") else "收盤",
            "is_delayed": False, "live": live, "pool_size": len(pool),
            "source": "TWSE MIS 盤中（成交金額為估算）" if live else "證交所／櫃買 盤後",
            "groups": groups, "clusters": clusters, "stocks": pool}


# ───────────────────────── 引擎：排程＋快取＋儲存 ─────────────────────────
class MarketGroupsEngine:
    def __init__(self, db_path, theme_path, fetch_quotes, get_industry_info,
                 ssl_context=None, pool_size=200, universe_size=400,
                 activity_fn=default_activity, fetch_eod_fn=fetch_eod, now_fn=None, log=print):
        self.db_path = db_path
        self.theme_path = theme_path
        self.fetch_quotes = fetch_quotes
        self.get_industry_info = get_industry_info
        self.ssl_context = ssl_context
        self.pool_size = pool_size
        self.universe_size = universe_size
        self.activity_fn = activity_fn
        self.fetch_eod_fn = fetch_eod_fn
        self.now = now_fn or (lambda: datetime.now(TW))
        self.log = log
        self._lock = threading.Lock()
        self._running = False
        self._day = {}          # 每日準備好的資料
        self._latest = None     # 最新快照（所有使用者共用）
        self._holiday_date = None
        self._slimmed_before = None
        self._init_db()

    # ── 資料庫 ──
    def _db(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.execute("""CREATE TABLE IF NOT EXISTS market_snapshots (
            trade_date TEXT, hm TEXT, payload TEXT, created_at TEXT,
            PRIMARY KEY (trade_date, hm))""")
        return conn

    def _init_db(self):
        with self._db() as conn:
            conn.commit()

    def _save(self, snap, hm):
        slim = {k: v for k, v in snap.items() if k != "stocks"}
        slim["stocks"] = [{k: s[k] for k in ("code", "name", "price", "change_pct", "turnover", "group_ids")}
                          for s in snap["stocks"]]
        conn = self._db()
        try:
            conn.execute("INSERT OR REPLACE INTO market_snapshots VALUES (?,?,?,?)",
                         (snap["trade_date"], hm, json.dumps(slim, ensure_ascii=False),
                          self.now().strftime("%Y-%m-%d %H:%M:%S")))
            cut = (self.now() - timedelta(days=KEEP_DAYS)).strftime("%Y-%m-%d")
            conn.execute("DELETE FROM market_snapshots WHERE trade_date < ?", (cut,))
            # 個股明細只保留今天（族群時間軸不需要），舊日期的資料瘦身
            if self._slimmed_before != snap["trade_date"]:
                for td, hm_old, payload in conn.execute(
                        "SELECT trade_date, hm, payload FROM market_snapshots WHERE trade_date < ?",
                        (snap["trade_date"],)).fetchall():
                    obj = json.loads(payload)
                    if obj.pop("stocks", None) is not None:
                        conn.execute("UPDATE market_snapshots SET payload=? WHERE trade_date=? AND hm=?",
                                     (json.dumps(obj, ensure_ascii=False), td, hm_old))
                self._slimmed_before = snap["trade_date"]
            conn.commit()
        finally:
            conn.close()

    def _load_last(self):
        conn = self._db()
        try:
            row = conn.execute("SELECT payload FROM market_snapshots ORDER BY trade_date DESC, hm DESC LIMIT 1").fetchone()
        finally:
            conn.close()
        return json.loads(row[0]) if row else None

    # ── 每日準備 ──
    def _prepare_day(self, today):
        if self._day.get("date") == today:
            return True
        eod, errors = self.fetch_eod_fn(self.ssl_context)
        for e in errors:
            self.log(f"[MARKET_GROUPS] 盤後資料失敗：{e}")
        if len(eod) < 500:
            self.log(f"[MARKET_GROUPS] 盤後資料只有 {len(eod)} 筆，視為失敗，稍後重試")
            return False
        industries = industry_map(self.get_industry_info())
        if not industries:
            # 產業別還沒載入（FinMind 與備份都沒有）：照樣準備（指定個股的族群還是算得出來），
            # 但不把今天標成「已準備」，下一輪會重新準備，產業別一到就補上金融／航運等族群
            self.log("[MARKET_GROUPS] 產業別資料還沒載入，金融／航運等族群暫缺，下一輪重試")
        themes, members, explicit = load_themes(self.theme_path, industries)
        eod = {c: e for c, e in eod.items() if is_common_stock(c)}   # 不論資料來源，一律只留一般個股
        ranked = sorted((e for e in eod.values() if e.get("turnover")), key=lambda e: -e["turnover"])
        universe = [e["code"] for e in ranked[:self.universe_size]]
        universe += [c for c in sorted(explicit) if c in eod and c not in universe]
        base = build_snapshot(eod, {}, industries, themes, members, self.pool_size,
                              self.now().replace(hour=20, minute=0), activity_fn=self.activity_fn)
        self._day = {"date": today if industries else None, "eod": eod, "industries": industries, "themes": themes,
                     "members": members, "universe": universe,
                     "base_shares": {g["group_id"]: g["turnover_share"] for g in base["groups"]},
                     "base_snapshot": base}
        self.log(f"[MARKET_GROUPS] 今日準備完成：監控 {len(universe)} 檔、{len(themes)} 族群")
        return True

    # ── 伺服器剛啟動、資料庫也沒有任何快照時（例：第一次部署在週末）──
    def warmup(self):
        """先用最近一個交易日的盤後資料做一筆總覽，畫面不會空白；不寫入時間軸。"""
        if self._latest is not None or self._load_last() is not None:
            return False
        today = self.now().strftime("%Y-%m-%d")
        if not self._prepare_day(today):
            return False
        if self._latest is None:
            self._latest = dict(self._day["base_snapshot"])
        return True

    def group_dict(self):
        """全部族群的名稱／星團（給前端補名稱用，不含行情）。"""
        themes = self._day.get("themes")
        if not themes:
            try:
                with open(self.theme_path, encoding="utf-8") as f:
                    themes = json.load(f)["themes"]
            except Exception:
                themes = []
        return [{"group_id": t["group_id"], "name": t["name"], "cluster_id": t.get("cluster_id", ""),
                 "cluster_name": t.get("cluster_name", "")} for t in themes]

    def groups_of(self, codes):
        """個股 → 所屬族群（自選股用）。今天還沒準備時，只用指定個股對照。"""
        members = self._day.get("members")
        if members is None:
            # 不在使用者請求時去抓產業別（避免卡住），先用指定個股對照
            try:
                _, members, _ = load_themes(self.theme_path, {})
            except Exception:
                members = {}
        return {c: list(members.get(c, [])) for c in codes}

    # ── 排程：每 5 分鐘 ──
    def tick(self):
        with self._lock:
            if self._running:
                self.log("[MARKET_GROUPS] 上一輪還沒跑完，略過")
                return
            self._running = True
        try:
            now = self.now()
            hm_i = now.hour * 100 + now.minute
            if now.weekday() >= 5 or hm_i < 845 or hm_i > 1340:
                return
            today = now.strftime("%Y-%m-%d")
            if not self._prepare_day(today):
                return
            d = self._day
            if hm_i < 900:
                if self._latest is None:
                    self._latest = dict(d["base_snapshot"], market_state="pre_open")
                return
            quotes = self.fetch_quotes(d["universe"]) or {}
            prev = (self._latest["groups"] if (self._latest and self._latest.get("live")
                                                and self._latest.get("trade_date") == today) else None)
            snap = build_snapshot(d["eod"], quotes, d["industries"], d["themes"], d["members"],
                                  self.pool_size, now, prev, d["base_shares"], self.activity_fn)
            if snap["market_state"] == "holiday":
                self._holiday_date = today
                return
            if not snap["live"]:
                self.log("[MARKET_GROUPS] 本輪沒拿到今天的即時報價，保留上一筆")
                return
            slot = min(now.hour * 60 + now.minute, 13 * 60 + 30)
            slot -= slot % 5
            hm = f"{slot // 60:02d}:{slot % 60:02d}"
            self._latest = snap
            self._save(snap, hm)
        except Exception as e:
            self.log(f"[MARKET_GROUPS] tick 失敗：{e}")
        finally:
            with self._lock:
                self._running = False

    # ── 給 API 用（只讀快取／資料庫，不現抓現算） ──
    def get_overview(self):
        snap = self._latest or self._load_last()
        if not snap:
            return {"ok": False, "groups": []}
        now = self.now()
        today = now.strftime("%Y-%m-%d")
        hm = now.hour * 100 + now.minute
        out = {k: v for k, v in snap.items() if k != "stocks"}
        fresh = bool(snap.get("live")) and snap.get("trade_date") == today
        if fresh:
            out["market_state"] = "open" if hm <= 1330 else "closed"
        elif now.weekday() >= 5 or self._holiday_date == today:
            out["market_state"] = "holiday"
        elif hm < 900:
            out["market_state"] = "pre_open"
        else:
            # 平日開盤後卻沒有今天的快照：資料延遲（畫面顯示最近一筆，標示延遲）
            out["market_state"] = "open" if hm <= 1330 else "closed"
            out["is_delayed"] = True
        out["ok"] = True
        return out

    def get_timeline(self, trade_date=None):
        conn = self._db()
        try:
            if not trade_date:
                row = conn.execute("SELECT MAX(trade_date) FROM market_snapshots").fetchone()
                trade_date = row[0] if row else None
            rows = conn.execute("SELECT hm, payload FROM market_snapshots WHERE trade_date=? ORDER BY hm",
                                (trade_date,)).fetchall() if trade_date else []
        finally:
            conn.close()
        keep = ("group_id", "cluster_id", "activity_score", "activity_change", "share_vs_prev_day",
                "turnover", "turnover_share", "active_count", "up_count", "down_count", "flat_count",
                "avg_change_pct")

        def slim(obj, hm):
            return {"time": hm, "groups": [{k: g.get(k) for k in keep} for g in obj["groups"]],
                    "clusters": obj.get("clusters")}
        snaps = [slim(json.loads(p), hm) for hm, p in rows]
        fallback = False
        if not snaps and self._latest is not None and not self._latest.get("live") and not rows:
            # 還沒有任何盤中快照（剛部署）：先給一筆盤後資料，標示 fallback，不假裝是盤中時間
            snaps = [slim(self._latest, "盤後")]
            trade_date = self._latest.get("trade_date") or trade_date
            fallback = True
        return {"ok": bool(snaps), "trade_date": trade_date or "", "interval_min": 5, "snapshots": snaps,
                "fallback": fallback, "group_dict": self.group_dict()}

    def get_group(self, group_id):
        snap = self._latest or self._load_last()
        if not snap:
            return {"ok": False}
        g = next((x for x in snap["groups"] if x["group_id"] == group_id), None)
        if not g:
            return {"ok": False}
        stocks = [s for s in snap.get("stocks", []) if group_id in s.get("group_ids", [])]
        tl = self.get_timeline(snap.get("trade_date"))
        series = [{"time": s["time"], "activity_score": next((x["activity_score"] for x in s["groups"]
                                                              if x["group_id"] == group_id), 0)}
                  for s in tl["snapshots"]]
        peak = max(series, key=lambda x: x["activity_score"])["time"] if series else None
        return {"ok": True, **g, "peak_time": peak, "stocks": stocks, "timeline": series,
                "data_time": snap.get("data_time"), "trade_date": snap.get("trade_date")}
