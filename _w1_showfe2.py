# -*- coding: utf-8 -*-
from pathlib import Path
t = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
for i,line in enumerate(t.splitlines(),1):
    if "is_paid" in line or "isPaid" in line and ("forum" in line.lower() or "content" in line or "comment" in line):
        if "forum" in line.lower() or "content" in line or "post" in line.lower() or "is_paid" in line:
            print(f"{i}:{line.strip()[:180]}")
print("---desktop picks headers---")
i=t.find("async function _loadDesktopPicks")
print(t[i:i+700])
