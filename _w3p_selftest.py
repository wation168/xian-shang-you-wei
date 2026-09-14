# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
fails=[]
def ok(c,m):
    print(("OK" if c else "FAIL"), m)
    if not c: fails.append(m)
ok("--bg:#07111f" in idx, "proto bg token")
ok("home-ia-card--deep" in idx and "home-ia-deepcore" in idx, "DEEP deco")
ok("2685c5" in idx and "3caeff" in idx, "search glow")
ok("a6792c" in idx, "upgrade gold")
ok("22812" not in idx and "產業強弱" not in idx, "no fake market modules")
ok("function _homeGo" in idx and "result-open" in idx, "Wave2 persist")
ok("deepLocked = !_hasPremium()" in idx, "Wave1 deepLocked")
ok("GUEST_DAILY_LIMIT = 3" in main, "Wave1 credit")
ok("prefers-reduced-motion" in idx, "reduced motion")
print("SELFTEST", "OK" if not fails else fails)
