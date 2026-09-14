# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\main.py")
t = p.read_text(encoding="utf-8")

old = '''    results.sort(key=lambda x: x["pnl_pct"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return {"ok": True, "data": results}'''
new = '''    results.sort(key=lambda x: x["pnl_pct"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1

    _consume_portfolio_daily_credit(request, current_user)
    return {"ok": True, "data": results}'''
if t.count(old) != 1:
    raise SystemExit("pf return count=%s" % t.count(old))
t = t.replace(old, new, 1)
print("OK pf consume")

# forum single post
idx = t.find('@app.get("/forum/posts/{')
if idx < 0:
    idx = t.find("forum_get_post(")
print("forum_get_post at", idx)
print(t[idx:idx+900])
p.write_text(t, encoding="utf-8")
