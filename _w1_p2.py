# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\main.py")
t = p.read_text(encoding="utf-8")
if "def _is_premium(" in t:
    print("helpers already present")
    raise SystemExit(0)
anchor = "def _check_query_limit(member_id: int, plan: str) -> tuple[bool, int, int]:"
if t.count(anchor) != 1:
    raise SystemExit("check_query_limit count=%s" % t.count(anchor))
helpers = r'''
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

'''
t = t.replace(anchor, helpers + anchor, 1)
p.write_text(t, encoding="utf-8")
print("helpers OK")
