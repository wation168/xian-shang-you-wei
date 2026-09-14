# -*- coding: utf-8 -*-
from pathlib import Path
import re, subprocess
root = Path(r"D:\xian-shang-you-wei")
idx = (root/"backend/frontend/index.html").read_text(encoding="utf-8")
main = (root/"backend/main.py").read_text(encoding="utf-8")
fails=[]
def ok(c,m):
    print(("OK" if c else "FAIL"), m)
    if not c: fails.append(m)

for k in ["quotes","picks","analyze","pattern","chips","deep","deepanalysis","portfolio","watch","upgrade"]:
    ok("_homeGo('%s')" % k in idx or (k=="upgrade" and "homeIaUpgrade" in idx), "card "+k)
ok("function _homeGo" in idx, "_homeGo")
ok("home-ia-grid" in idx and "repeat(3" in idx and "repeat(2" in idx, "3col + 2col narrow")
ok("showUpgradeModal" in idx[idx.find("function _homeGo"):idx.find("function _homeGo")+1200], "upgrade uses modal")
ok("showPage('picks')" in idx and "showPage('deepanalysis')" in idx and "showPage('portfolio')" in idx, "pages wired")
ok("loadChips" in idx[idx.find("function _homeGo"):idx.find("function _homeGo")+1600], "chips wired")
ok("dcard-kbar" in idx[idx.find("function _homeGo"):idx.find("function _homeGo")+1600], "pattern wired")
ok("加權指數" not in idx[idx.find("home-ia-grid"):idx.find("home-ia-grid")+2500], "no fake taiex label in grid")
ok("GUEST_DAILY_LIMIT = 3" in main and "FREE_DAILY_LIMIT = 5" in main, "Wave1 limits")
ok("def _check_daily_credit" in main and "deepLocked = !_hasPremium()" in idx, "Wave1 credit+deepLocked")
ok("上次更新（台北）" in idx, "WaveA timestamp")
ok(".pay-done .hero-btns" not in (root/"backend/frontend/landing.html").read_text(encoding="utf-8"), "WaveA pay-done")

print("SELFTEST", "OK" if not fails else fails)
r=subprocess.run(["git","diff","--stat","backend/frontend/index.html","backend/main.py"], cwd=str(root), capture_output=True, text=True)
print(r.stdout)
print("grid cards", idx.count("home-ia-card"))
