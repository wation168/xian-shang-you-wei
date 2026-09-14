# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
print("homeIaGrid", idx.count('id="homeIaGrid"'))
print("home-ia-card onclick", idx.count("onclick=\"_homeGo("))
print("_homeGo fn", "function _homeGo" in idx)
print("upgrade cta", "homeIaUpgrade" in idx)
print("2col", "repeat(2" in idx)
print("Wave1 deepLocked", "deepLocked = !_hasPremium()" in idx)
print("Wave1 credit", "GUEST_DAILY_LIMIT = 3" in main, "FREE_DAILY_LIMIT = 5" in main)
print("no 加權 in grid area", "加權指數" not in idx)
print("stockInput", "id=\"stockInput\"" in idx)
print("hotkeys", "id=\"hotkeysEl\"" in idx)
