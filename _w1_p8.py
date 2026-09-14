# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\main.py")
t = p.read_text(encoding="utf-8")
old = '''    is_paid = False
    if user:
        today = _date_cls.today().isoformat()
        is_paid = (user.get("plan") != "free" and user.get("expire_at", "") >= today) or _is_referral_active(user)

    if not is_paid:
        conn.close()
        raise HTTPException(status_code=403, detail="需付費會員才能查看內容")'''
new = '''    if not user:
        conn.close()
        raise HTTPException(status_code=403, detail="請先登入後查看討論內容")
    # 免費可看；留言／發文仍 require_paid_user'''
if t.count(old) != 1:
    raise SystemExit("forum_get_post count=%s" % t.count(old))
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("OK forum_get_post")
