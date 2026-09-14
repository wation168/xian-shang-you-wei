# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")

i = idx.find('id="homeDash"')
print("=== homeDash LINE", idx[:i].count("\n")+1)
print(idx[i:i+2500])

print("\n=== HEADER 600-720 ===")
print("\n".join(idx.splitlines()[599:730]))
