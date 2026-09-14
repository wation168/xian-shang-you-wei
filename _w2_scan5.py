# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
print(idx[idx.find("const dash = document.getElementById('homeDash')")-200:idx.find("const dash = document.getElementById('homeDash')")+400])
print("--- C ---")
i=idx.find("C._currentId")
print(idx[max(0,i-80):i+80])
