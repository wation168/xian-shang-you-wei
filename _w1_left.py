# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess
root = Path(r"D:\xian-shang-you-wei")
for rel in ["backend/frontend/index.html","backend/frontend/landing.html"]:
    t = (root/rel).read_text(encoding="utf-8")
    for s in ["每日 3", "每日3", "1 次", "1次", "guest_day_", "FREE_DAILY", "10 次"]:
        if s in t:
            print(rel, s, t.count(s))
print("---git---")
r=subprocess.run(["git","diff","--stat","backend/main.py","backend/frontend/index.html","backend/frontend/landing.html"], cwd=str(root), capture_output=True, text=True)
print(r.stdout)
