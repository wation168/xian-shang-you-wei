# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\main.py")
t = p.read_text(encoding="utf-8")

def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("FAIL %s count=%s\n%s" % (label, n, old[:240]))
    t = t.replace(old, new, 1)
    print("OK", label)

# referral taipei
rep(
    "    return exp >= _date_cls.today().isoformat()",
    "    return exp >= _taipei_today()",
    "referral_taipei")

# helper after _credit_dict
old_cd = '''def _credit_dict(used: int, limit: int) -> dict:
    return {"used": used, "limit": limit, "remaining": max(0, limit - used)}
'''
new_cd = '''def _credit_dict(used: int, limit: int) -> dict:
    return {"used": used, "limit": limit, "remaining": max(0, limit - used)}


def _quota_429(code: str, msg: str, used: int, limit: int):
    """429 + credit，給 FE modal／_syncCreditFromPayload。"""
    return JSONResponse(
        status_code=429,
        content={"detail": f"{code}|{msg}", "credit": _credit_dict(used, limit)},
    )
'''
if "def _quota_429" not in t:
    rep(old_cd, new_cd, "quota_429_helper")

# JSONResponse import
if "JSONResponse" not in t.split("def _quota_429")[0][:8000] and "from fastapi.responses import JSONResponse" not in t:
    # try common import line
    if "from fastapi.responses import" in t:
        i = t.find("from fastapi.responses import")
        line_end = t.find("\n", i)
        line = t[i:line_end]
        if "JSONResponse" not in line:
            t = t[:line_end] + ", JSONResponse" + t[line_end:]
            print("OK patched import line")
    else:
        t = t.replace("from fastapi import ", "from fastapi.responses import JSONResponse\nfrom fastapi import ", 1)
        print("OK added JSONResponse import")

# analyze 429 blocks
rep(
'''    allowed, used, limit = _check_daily_credit(request, user)
    if not allowed:
        if user:
            raise HTTPException(
                status_code=429,
                detail=f"today_limit|今日完整分析／健檢次數已用完（{limit} 次），升級即可無限使用"
            )
        raise HTTPException(
            status_code=429,
            detail=f"guest_limit|免費試用已達上限（{limit} 次），登入後完整分析與健檢共用每日額度"
        )''',
'''    allowed, used, limit = _check_daily_credit(request, user)
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
        )''',
"analyze_429")

rep(
'''    allowed, used, limit = _check_daily_credit(request, current_user)
    if not allowed:
        raise HTTPException(status_code=429, detail=f"today_limit|今日完整分析／健檢次數已用完（{limit} 次）")''',
'''    allowed, used, limit = _check_daily_credit(request, current_user)
    if not allowed:
        return _quota_429(
            "today_limit",
            f"今日完整分析／健檢次數已用完（{limit} 次）",
            used, limit,
        )''',
"pf_429")

rep(
    "def report_generate(req: ReportReq, request: Request = None, user: dict = Depends(require_user)):",
    "def report_generate(req: ReportReq, request: Request, user: dict = Depends(require_user)):",
    "report_request_required")

p.write_text(t, encoding="utf-8")
print("BE_DONE")
