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

rep(
'''    # 計入查詢次數（免費用戶）
    if user and user["plan"] == "free":
        _inc_query_count(user["id"])

    return result''',
'''    # Wave1：扣次改在 HTTP handler 成功後，此處不扣
    return result''',
"do_analyze_inc")

rep(
'    """API 端點：遊客可查 1 次，免費會員 3 次，付費無限"""',
'    """API 端點：遊客 daily_credit 3、免費完整分析 5（與健檢共用）、付費無限"""',
"analyze_doc")

rep(
'def get_kline(stock_id: str, tf: str = "D", user: dict = Depends(require_user)):',
'def get_kline(stock_id: str, tf: str = "D", user: dict | None = Depends(get_current_user)):',
"kline")

rep(
'def get_chips(stock_id: str, days: int = 30, user: dict = Depends(require_user)):',
'def get_chips(stock_id: str, days: int = 30, user: dict | None = Depends(get_current_user)):',
"chips")

rep(
'        "queries_limit": FREE_DAILY_LIMIT if plan == "free" else 999,',
'        "queries_limit": 999 if _is_premium(user) else FREE_DAILY_LIMIT,',
"auth_me_limit")

p.write_text(t, encoding="utf-8")
print("P3_DONE")
