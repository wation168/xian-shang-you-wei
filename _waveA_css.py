# -*- coding: utf-8 -*-
from pathlib import Path
import re
lt = Path(r"D:\xian-shang-you-wei\backend\frontend\landing.html").read_text(encoding="utf-8")
m = re.search(r"style\.textContent\s*=\s*'([^']+)'", lt)
print("FINAL CSS:", m.group(1) if m else "NOT FOUND")
print("count pay-done .hero-btns:", lt.count("pay-done .hero-btns"))
for m2 in re.finditer(r"pay-done[^;]{0,220}", lt):
    print("CHUNK:", m2.group(0))
