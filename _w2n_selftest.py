# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
fails=[]
def ok(c,m):
    print(("OK" if c else "FAIL"), m)
    if not c: fails.append(m)
ok("#homeDash{display:block" in idx or "#homeDash{display:block;" in idx, "homeDash always block")
ok("result-open" in idx and "result-open .hd-sec" in idx, "only hd-sec hides")
ok("function _homeGo" in idx and "homeIaGrid" in idx, "grid+_homeGo kept")
ok("deepLocked = !_hasPremium()" in idx, "Wave1 deepLocked")
ok("GUEST_DAILY_LIMIT = 3" in main, "Wave1 guest 3")
print("SELFTEST", "OK" if not fails else fails)
