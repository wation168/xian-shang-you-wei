# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\main.py")
t = p.read_text(encoding="utf-8")
start = t.find("    today = _taipei_today()\n\n    if user:\n        plan = user[\"plan\"]\n        is_referral_unlocked")
end = t.find("    return _do_analyze(stock_id, tf, ma1, ma2, ma3, ma4, ma5, user=user)", start)
if start < 0 or end < 0:
    raise SystemExit("analyze block not found %s %s" % (start, end))
end = end + len("    return _do_analyze(stock_id, tf, ma1, ma2, ma3, ma4, ma5, user=user)")
new = '''    today = _taipei_today()

    if user:
        plan = user["plan"]
        if plan != "free" and user.get("expire_at") and user["expire_at"] < today and not _is_referral_active(user):
            raise HTTPException(status_code=403, detail="訂閱已到期，請續費後繼續使用")

    allowed, used, limit = _check_daily_credit(request, user)
    if not allowed:
        if user:
            raise HTTPException(
                status_code=429,
                detail=f"today_limit|今日完整分析／健檢次數已用完（{limit} 次），升級即可無限使用"
            )
        raise HTTPException(
            status_code=429,
            detail=f"guest_limit|免費試用已達上限（{limit} 次），登入後完整分析與健檢共用每日額度"
        )

    _inc_counter("analyze_count")

    if user:
        try:
            _complete_referral_if_pending(user["email"])
        except Exception as _ref_e:
            print(f"[REFERRAL] complete_referral_if_pending 失敗 {user['email']}：{_ref_e}")

    result = _do_analyze(stock_id, tf, ma1, ma2, ma3, ma4, ma5, user=user)
    _consume_daily_credit(request, user)
    _ok, used2, limit2 = _check_daily_credit(request, user)
    if isinstance(result, dict):
        result["credit"] = _credit_dict(used2, limit2)
    return result'''
t = t[:start] + new + t[end:]
p.write_text(t, encoding="utf-8")
print("analyze_quota OK", start, end)
