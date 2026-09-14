# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")
old = '<div class="modal-sub">每日 3 次免費查詢</div>'
new = '<div class="modal-sub">完整分析與健檢共用每日額度（以後端為準）</div>'
if old not in t:
    raise SystemExit("modal-sub missing")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("OK modal-sub")
