# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")
anchor = """@media (max-width:720px){
  .home-ia-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
}"""
if t.count(anchor) != 1:
    raise SystemExit("anchor count=%s" % t.count(anchor))
css = """
@media (max-width:720px){
  .home-ia-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
}

/* Wave3 輕量 2.5D：不碰 chart／K線 JS；reduced-motion／窄螢幕降特效 */
.topbar{box-shadow:0 8px 24px rgba(15,23,42,.06)}
#desktopMain{perspective:1200px}
.home-ia-card,.risk-card,.metric,.deep-card,.rr-card{
  box-shadow:0 6px 16px rgba(15,23,42,.07),0 1px 0 rgba(255,255,255,.04) inset;
  transform:translateZ(0);
  transition:transform .18s ease, box-shadow .18s ease;
}
.home-ia-card:hover,.metric:hover,.deep-card:hover{
  transform:translateY(-3px);
  box-shadow:0 12px 26px rgba(15,23,42,.12);
}
#deepSection{
  border-radius:14px;
  box-shadow:0 10px 28px rgba(15,45,30,.10);
  padding:6px 4px 8px;
}
#deepSection .lock-ov-deep{z-index:6}

@media (max-width:720px){
  .home-ia-card:hover,.metric:hover,.deep-card:hover{transform:none;box-shadow:0 6px 16px rgba(15,23,42,.07)}
  .home-ia-card,.risk-card,.metric,.deep-card,.rr-card{transition:none}
}
@media (prefers-reduced-motion: reduce){
  .home-ia-card,.risk-card,.metric,.deep-card,.rr-card{transition:none}
  .home-ia-card:hover,.metric:hover,.deep-card:hover{transform:none}
}
"""
p.write_text(t.replace(anchor, css, 1), encoding="utf-8")
print("W3_CSS_OK")
