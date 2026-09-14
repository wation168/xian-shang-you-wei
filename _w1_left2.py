# -*- coding: utf-8 -*-
from pathlib import Path
t = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
for s in ["每日 3", "1次"]:
    i = 0
    while True:
        j = t.find(s, i)
        if j<0: break
        print("---", s, j, "---")
        print(t[max(0,j-80):j+80].replace("\n"," "))
        i=j+1
