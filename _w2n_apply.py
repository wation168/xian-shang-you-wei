# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")

def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("FAIL %s count=%s\n%s" % (label, n, old[:180]))
    t = t.replace(old, new, 1)
    print("OK", label)

rep(
"#homeDash{display:none;padding:4px 0 8px}\n#homeDash.show{display:block}",
"#homeDash{display:block;padding:4px 0 8px}\n#homeDash.show{display:block}\n#homeDash.result-open .hd-sec{display:none}",
"css")

rep(
"""  const sync = () => { dash.classList.toggle('show', !resultEl.classList.contains('show')); };""",
"""  const sync = () => {
    dash.classList.add('show');
    dash.classList.toggle('result-open', resultEl.classList.contains('show'));
  };""",
"observe")

p.write_text(t, encoding="utf-8")
print("DONE")
