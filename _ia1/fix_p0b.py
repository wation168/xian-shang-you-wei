# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
p = r"D:/xian-shang-you-wei/backend/frontend/index.html"
t = open(p, encoding="utf-8").read()

old1 = ".search-box input{color:#1a1a18}"
new1 = ".search-box input{color:#1a1a18;background:#fff}"
if t.count(old1) != 1:
    raise SystemExit("search override count %s" % t.count(old1))
t = t.replace(old1, new1, 1)

old2 = ".status{font-size:11px;color:var(--text3);padding:4px 16px;min-height:20px}"
new2 = ".status{font-size:13px;color:var(--text2);padding:4px 16px;min-height:22px}"
if t.count(old2) != 1:
    raise SystemExit("status count %s" % t.count(old2))
t = t.replace(old2, new2, 1)

assert ".search-box input{color:#edf6ff}" not in t
assert "color:#1a1a18;background:#fff" in t
assert ".search-box input::placeholder{color:#6b7280;opacity:1}" in t
assert ".m-hint{font-size:12px" in t and ".m-hint{font-size:9px" not in t
assert ".home-ia-ttl{font-size:16px;color:#edf6ff}" not in t
assert ".status{font-size:13px;color:var(--text2)" in t
assert 'id="homeFlow"' in t
assert "#homeFlow{display:none}" not in t

open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok", len(t))
