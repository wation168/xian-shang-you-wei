# -*- coding: utf-8 -*-
from pathlib import Path
t = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
print("JSONResponse count", t.count("JSONResponse"))
for i,line in enumerate(t.splitlines()[:80],1):
    if "JSONResponse" in line or "fastapi.responses" in line:
        print(i, line)
# if helper uses it but no import, add
if "from fastapi.responses import" not in t and "JSONResponse" in t:
    print("NEED IMPORT")
