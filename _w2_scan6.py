# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
for i,line in enumerate(idx.splitlines(),1):
    if "_currentId" in line or "window.C" in line or "var C " in line or "C =" in line[:20]:
        print(f"{i}:{line.strip()[:160]}")
