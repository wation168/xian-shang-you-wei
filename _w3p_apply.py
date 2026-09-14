# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")

def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("FAIL %s count=%s\n%s" % (label, n, old[:160]))
    t = t.replace(old, new, 1)
    print("OK", label)

rep(
""":root[data-theme="dark"]{
  --bg:#141412;--bg2:#1e1e1b;--bg3:#282824;
  --text:#eae9e3;--text2:#a0a099;--text3:#666560;
  --border:rgba(255,255,255,.08);--border2:rgba(255,255,255,.16);""",
""":root[data-theme="dark"]{
  --bg:#07111f;--bg2:#0d1c2d;--bg3:#10243a;
  --text:#edf6ff;--text2:#8da5bb;--text3:#6f8da7;
  --border:#21415e;--border2:#18334d;""",
"dark_tokens")

rep(
"""    --bg:#141412;--bg2:#1e1e1b;--bg3:#282824;
    --text:#eae9e3;--text2:#a0a099;--text3:#666560;
    --border:rgba(255,255,255,.08);--border2:rgba(255,255,255,.16);""",
"""    --bg:#07111f;--bg2:#0d1c2d;--bg3:#10243a;
    --text:#edf6ff;--text2:#8da5bb;--text3:#6f8da7;
    --border:#21415e;--border2:#18334d;""",
"auto_tokens")

# DEEP card decoration
rep(
'''<div class="home-ia-card" onclick="_homeGo('deep')"><div class="home-ia-ico">📐</div><div class="home-ia-ttl">DEEP</div><div class="home-ia-sub">深度分析七欄</div></div>''',
'''<div class="home-ia-card home-ia-card--deep" onclick="_homeGo('deep')"><div class="home-ia-ico">📐</div><div class="home-ia-ttl">DEEP</div><div class="home-ia-sub">深度分析七欄</div><div class="home-ia-deepcore">DEEP</div></div>''',
"deep_card")

rep(
'''<button type="button" class="home-ia-upgrade" id="homeIaUpgrade" onclick="_homeGo('upgrade')">升級會員，解鎖完整分析</button>''',
'''<button type="button" class="home-ia-upgrade" id="homeIaUpgrade" onclick="_homeGo('upgrade')">♛ 升級付費會員</button>''',
"upgrade_label")

skin = r'''
/* Proto skin (product HTML) — 視覺皮，無假行情模組 */
html[data-theme="dark"],html:not([data-theme]){
  background:radial-gradient(circle at 65% 8%,#123457 0,#07111f 38%,#050b14 100%);
}
html[data-theme="dark"] body,html:not([data-theme]) body{background:transparent}
.topbar{
  background:#071321dd !important;
  backdrop-filter:blur(10px);
  border-bottom:1px solid #18334d !important;
}
.search-box{
  background:#0d2238;
  border:1px solid #2685c5;
  border-radius:16px;
  box-shadow:0 0 30px #1489cc22;
}
.search-box input{color:#edf6ff}
.btn-analyze{
  background:linear-gradient(135deg,#3caeff,#2877ef) !important;
  color:#fff !important;
  border:none !important;
  border-radius:11px;
  font-weight:800;
}
.home-ia-card{
  position:relative;
  overflow:hidden;
  min-height:132px;
  text-align:left;
  padding:18px 16px 16px;
  border:1px solid #26506d;
  border-radius:16px;
  background:linear-gradient(145deg,#102a40,#0b1728);
  box-shadow:0 12px 28px #0005;
}
.home-ia-card:after{
  content:"";
  position:absolute;width:160px;height:160px;border-radius:50%;
  right:-70px;top:-80px;
  background:radial-gradient(circle,#36bfff33,transparent 65%);
  pointer-events:none;
}
.home-ia-card:hover{
  transform:translateY(-4px);
  border-color:#3e94c8;
  box-shadow:0 18px 38px #0008,0 0 25px #2497d122;
}
.home-ia-ttl{font-size:16px;color:#edf6ff}
.home-ia-sub{color:#8da7bb}
.home-ia-card--deep{
  background:radial-gradient(circle at 72% 55%,#274b9c88 0,transparent 22%),linear-gradient(145deg,#17183b,#10142b);
  border-color:#5c5ad1;
}
.home-ia-deepcore{
  position:absolute;right:16px;bottom:14px;width:56px;height:56px;border-radius:50%;
  display:grid;place-items:center;font-size:11px;font-weight:900;color:#b8eaff;
  border:2px solid #55c9ff;box-shadow:0 0 24px #358cff99,inset 0 0 20px #2c83ff55;
  z-index:1;
}
.home-ia-upgrade{
  border:1px solid #a6792c !important;
  border-radius:15px;
  padding:16px 18px;
  background:linear-gradient(145deg,#2c2415,#171a23) !important;
  color:#f5cb71 !important;
  box-shadow:0 10px 24px #0006;
}
@media (max-width:720px){
  .home-ia-card{min-height:120px}
  .home-ia-card:hover{transform:none}
}
@media (prefers-reduced-motion: reduce){
  .home-ia-card:hover{transform:none}
}
'''

# insert after Wave3 reduced-motion block if present, else after home-ia 720
mark = "@media (prefers-reduced-motion: reduce){\n  .home-ia-card,.risk-card,.metric,.deep-card,.rr-card{transition:none}\n  .home-ia-card:hover,.metric:hover,.deep-card:hover{transform:none}\n}"
if mark in t:
    t = t.replace(mark, mark + "\n" + skin, 1)
    print("OK skin after w3")
else:
    t = t.replace("</style>", skin + "\n</style>", 1)
    print("OK skin before /style")

p.write_text(t, encoding="utf-8")
print("PROTO_SKIN_DONE")
