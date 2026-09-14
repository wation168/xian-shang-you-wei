# -*- coding: utf-8 -*-
from pathlib import Path
import re
root = Path(r"D:\xian-shang-you-wei")
main = (root/"backend/main.py").read_text(encoding="utf-8")
# list all api routes
print("=== API routes ===")
for i,line in enumerate(main.splitlines(),1):
    if "@app.get(" in line or "@app.post(" in line:
        print(f"{i}:{line.strip()[:140]}")
print("\n=== keyword hits in main ===")
keys = ["taiex","twii","加權","櫃買","台指","電子指數","金融指數","news","rss","產業","sector","industry","index","IX0001","TAIEX","otc"]
for k in keys:
    c = main.lower().count(k.lower()) if k.isascii() else main.count(k)
    if c:
        print(k, c)
