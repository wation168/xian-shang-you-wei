# -*- coding: utf-8 -*-
from pathlib import Path
import re
it = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
lt = Path(r"D:\xian-shang-you-wei\backend\frontend\landing.html").read_text(encoding="utf-8")
desk = it[it.find("_loadDesktopPicks"):it.find("_loadDesktopPicks")+1200]
print(desk)
print("====SHOW====")
sp = it.find("async function showPicksPage")
print(it[sp:sp+2200])
print("====GOPAY====")
print(re.search(r"function goPayFromApp\(plan\) \{[\s\S]*?\n\}", it).group(0))
print("====CSS====")
m=re.search(r"\.pay-done[^`]*?\{[^}]+\}", lt)
print(m.group(0) if m else "no")
