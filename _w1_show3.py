# -*- coding: utf-8 -*-
from pathlib import Path
t = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
i = t.find("async def portfolio_analysis")
print("===PF TAIL===")
print(t[i:i+8500][-1800:])
j = t.find("async def forum_get_post")
if j<0:
    j = t.find("def forum_get_post")
print("===FGET pos", j)
print(t[j:j+1200] if j>=0 else "missing")
