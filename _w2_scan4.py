# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
for i,line in enumerate(idx.splitlines(),1):
    if "homeDash" in line:
        print(f"{i}:{line.strip()[:180]}")
print("--- loadHotkeys ---")
i=idx.find("async function loadHotkeys")
print(idx[i:i+700])
