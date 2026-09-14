# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
fails=[]
def ok(c,m):
    print(("OK" if c else "FAIL"), m)
    if not c: fails.append(m)
ok("Wave3" in idx and "prefers-reduced-motion" in idx, "w3 + reduced-motion")
ok("max-width:720px" in idx and "transform:none" in idx, "narrow reduce")
ok("three.js" not in idx.lower() and "THREE." not in idx, "no 3d engine")
ok("function _homeGo" in idx and "result-open" in idx, "Wave2 persist")
ok("deepLocked = !_hasPremium()" in idx and "lock-ov-deep" in idx, "Wave1 deep lock")
ok("GUEST_DAILY_LIMIT = 3" in main and "def _check_daily_credit" in main, "Wave1 credit")
ok("getContext('2d')" in idx, "kline canvas untouched presence")
print("SELFTEST", "OK" if not fails else fails)
