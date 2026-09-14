# -*- coding: utf-8 -*-
from pathlib import Path
import re, subprocess
root = Path(r"D:\xian-shang-you-wei")
it = (root/"backend/frontend/index.html").read_text(encoding="utf-8")
lt = (root/"backend/frontend/landing.html").read_text(encoding="utf-8")
ht = (root/"backend/frontend/homepage.html").read_text(encoding="utf-8")

# 1 desktop
pos = it.find("async function _loadDesktopPicks()")
fn = it[pos:pos+2200]
assert "j.server_time" not in fn
assert "const _updLine = j.updated_at" in fn
assert "尚未更新（排程約每個交易日 09:06 台北）" in fn
assert "上次更新（台北）：${j.updated_at}" in fn
print("1) OK desktop updated_at only")

# 2 showPicksPage
sp = it.find("async function showPicksPage")
spfn = it[sp:sp+2500]
assert "const updatedAt = j.updated_at" in spfn
assert "${updatedAt}" in spfn  # used in empty
assert "尚未更新（排程約每個交易日 09:06 台北）" in spfn
# no bare undefined path: updatedAt always assigned
assert "server_time" not in spfn or "j.server_time" not in spfn
print("2) OK showPicksPage updatedAt")

# 3 CSS
css = re.search(r"\.pay-done[^\n]+", lt).group(0)
assert ".hero-btns .btn-primary" not in css
assert ".nav-cta" in css and ".price-btn" in css and ".cta-final .btn-primary" in css
assert 'openBuy' in css
print("3) OK pay-done CSS:", css)

# nit
gp = re.search(r"function goPayFromApp\(plan\) \{[\s\S]*?\n\}", it).group(0)
assert "doUpgrade" not in gp
assert "showUpgradeModal" in gp
print("nit OK goPayFromApp")

# git status three files
r = subprocess.run(["git","status","--short","backend/frontend/homepage.html","backend/frontend/landing.html","backend/frontend/index.html"], cwd=str(root), capture_output=True, text=True)
print("GIT:", r.stdout.strip() or "(clean?)")
r2 = subprocess.run(["git","diff","--stat","backend/frontend/homepage.html","backend/frontend/landing.html","backend/frontend/index.html"], cwd=str(root), capture_output=True, text=True)
print(r2.stdout)
