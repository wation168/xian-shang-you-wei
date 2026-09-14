# -*- coding: utf-8 -*-
from pathlib import Path
t = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
i = t.find("today = _taipei_today()")
# first occurrence after analyze docstring
j = t.find("def analyze(")
k = t.find("today = _taipei_today()", j)
print("pos", k)
print(t[k:k+2600])
