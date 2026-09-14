# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
for i,line in enumerate(idx.splitlines(),1):
    if "deepSection" in line:
        print(f"{i}:{line.strip()[:160]}")
print("--- lock-ov css ---")
i = idx.find(".lock-ov")
print("LINE", idx[:i].count("\n")+1)
print(idx[i:i+500])
