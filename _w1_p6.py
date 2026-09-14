# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\main.py")
t = p.read_text(encoding="utf-8")

def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("FAIL %s count=%s\n%s" % (label, n, old[:280]))
    t = t.replace(old, new, 1)
    print("OK", label)

rep(
'''def _deep_is_premium(user: dict | None) -> bool:
    """
    深度選股專用：判斷此使用者是否有權看到完整股票代號/名稱。

    判斷條件與 require_paid_user() 完全一致（邀請制解鎖 > 付費方案 > 到期日），
    差別只在這裡不拋 403，而是回傳 True/False——因為深度選股要讓免費會員與
    未登入者也能看到遮罩版預覽（導流用），不是整個擋掉。
    """
    if not user:
        return False
    if _is_referral_active(user):
        return True
    if user.get("plan") == "free":
        return False
    exp = user.get("expire_at")
    if exp and exp < _date_cls.today().isoformat():
        return False
    return True''',
'''def _deep_is_premium(user: dict | None) -> bool:
    """深度選股完整代號：與 _is_premium 同一套。"""
    return _is_premium(user)''',
"deep_is")

rep(
'''    if not _row or not _row["content"]:
        return {"data": [], "updated_at": None,
                "server_time": _server_time, "masked": not _is_premium}
    import json as _json_api
    try:
        _data = _json_api.loads(_row["content"])
    except Exception:
        _data = []

    if not _is_premium:
        _data = [_deep_mask_item(_it) for _it in _data]
        return {"data": _data, "updated_at": _row["updated_at"],
                "server_time": _server_time, "masked": True}

    return {"data": _data, "updated_at": _row["updated_at"],
            "server_time": _server_time, "masked": False}''',
'''    if not _row or not _row["content"]:
        empty = _picks_payload([], None, user)
        empty["server_time"] = _server_time
        return empty
    import json as _json_api
    try:
        _data = _json_api.loads(_row["content"])
    except Exception:
        _data = []

    if _is_premium:
        return {"data": _data, "updated_at": _row["updated_at"],
                "server_time": _server_time, "masked": False, "tier": "paid", "preview": False}
    if user:
        _data = [_deep_mask_item(_it) for _it in _data]
        return {"data": _data, "updated_at": _row["updated_at"],
                "server_time": _server_time, "masked": True, "tier": "free", "preview": False}
    # 遊客弱預覽：不可全空白
    payload = _picks_payload(_data, _row["updated_at"], user)
    payload["server_time"] = _server_time
    return payload''',
"deep_tiers")

rep(
'''def report_generate(req: ReportReq, user: dict = Depends(require_user)):
    plan = user["plan"]
    is_referral_unlocked = _is_referral_active(user)
    if not is_referral_unlocked and user.get("expire_at") and user["expire_at"] < _taipei_today():
        raise HTTPException(status_code=403, detail="訂閱已到期，請續費後繼續使用")
    is_free = plan == "free" and not is_referral_unlocked
    if is_free:
        allowed, _, _ = _check_query_limit(user["id"], plan)
        if not allowed:
            raise HTTPException(status_code=403, detail="完整報告為付費功能，升級或邀請3位好友即可使用")''',
'''def report_generate(req: ReportReq, request: Request = None, user: dict = Depends(require_user)):
    if user.get("expire_at") and user["expire_at"] < _taipei_today() and not _is_referral_active(user) and user.get("plan") != "free":
        raise HTTPException(status_code=403, detail="訂閱已到期，請續費後繼續使用")
    allowed, used, limit = _check_daily_credit(request, user)
    if not allowed:
        raise HTTPException(status_code=403, detail=f"今日完整分析／健檢／報告次數已用完（{limit} 次）")''',
"report_head")

rep(
'    current_basis = d.get("price_basis_date")',
'    current_basis = d.get("price_basis_date")\n    _consume_daily_credit(request, user)',
"report_consume")

rep(
'''async def portfolio_analysis(current_user: dict = Depends(get_current_user)):
    """批次分析持股：損益、技術位置、技術訊號、近5日漲幅"""''',
'''async def portfolio_analysis(request: Request, current_user: dict = Depends(require_user)):
    """批次分析持股。免費與分析共用 daily_credit，每次載入扣1（45秒去重）。"""
    allowed, used, limit = _check_daily_credit(request, current_user)
    if not allowed:
        raise HTTPException(status_code=429, detail=f"today_limit|今日完整分析／健檢次數已用完（{limit} 次）")''',
"portfolio_sig")

rep(
'''        if is_paid:
            post["content"] = r[3]''',
'''        if user:
            post["content"] = r[3]''',
"forum_list")

rep(
'''    today = _date_cls.today().isoformat()
    conn = _db_conn()
    row = conn.execute(
        "SELECT count FROM query_log WHERE member_id=? AND date=?",
        (user["id"], today)
    ).fetchone()''',
'''    today = _taipei_today()
    conn = _db_conn()
    row = conn.execute(
        "SELECT count FROM query_log WHERE member_id=? AND date=? AND ip=''",
        (user["id"], today)
    ).fetchone()''',
"auth_me_today")

p.write_text(t, encoding="utf-8")
print("P6_DONE")
