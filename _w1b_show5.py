# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
# around renderAnalysisCards end
i = idx.find("function renderAnalysisCards")
print(idx[i+2200:i+4200])
