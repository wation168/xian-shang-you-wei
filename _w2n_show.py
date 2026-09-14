# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
i = idx.find('id="homeDash"')
print("=== homeDash HTML ===")
print(idx[i:i+2800])
print("\n=== observe ===")
j = idx.find("function _observeHomeDash")
print(idx[j:j+500])
print("\n=== css homeDash ===")
for n,line in enumerate(idx.splitlines(),1):
    if "homeDash" in line or "home-ia" in line:
        if n < 600 or "home-ia" in line:
            print(f"{n}:{line.rstrip()[:160]}")
