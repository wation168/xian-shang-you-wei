# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
p = r"D:/xian-shang-you-wei/backend/frontend/index.html"
t = open(p, encoding="utf-8").read()

subs = [
    (
        ".search-box input{color:#edf6ff}",
        ".search-box input{color:#1a1a18;background:#fff}\n.search-box input::placeholder{color:#6b7280;opacity:1}",
    ),
    (
        ".m-hint{font-size:9px;font-style:italic;color:var(--blue,#3b82f6);opacity:.8;margin-top:3px;line-height:1.3}",
        ".m-hint{font-size:12px;font-style:normal;color:var(--text2);opacity:1;margin-top:4px;line-height:1.45}",
    ),
    (
        ".home-ia-ttl{font-size:16px;color:#edf6ff}",
        ".home-ia-ttl{font-size:16px;color:var(--text)}",
    ),
    (
        ".status{font-size:11px;color:var(--text3);padding:4px 16px;min-height:20px}",
        ".status{font-size:13px;color:var(--text2);padding:4px 16px;min-height:22px}",
    ),
]
for old, new in subs:
    n = t.count(old)
    if n != 1:
        raise SystemExit("count %s for %r" % (n, old[:60]))
    t = t.replace(old, new, 1)

# asserts
assert ".search-box input{color:#edf6ff}" not in t
assert "color:#1a1a18" in t
assert ".search-box input::placeholder{color:#6b7280;opacity:1}" in t
assert ".m-hint{font-size:9px" not in t
assert ".m-hint{font-size:12px" in t
assert ".home-ia-ttl{font-size:16px;color:#edf6ff}" not in t
assert ".status{font-size:11px;color:var(--text3)" not in t
assert 'id="homeFlow"' in t
assert "#homeFlow{display:none}" not in t
assert "_loadHomeMarket" in t

open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok", len(t))
print("search_light_text_gone", ".search-box input{color:#edf6ff}" not in t)
print("search_dark_on_white", "color:#1a1a18;background:#fff" in t)
print("hint_12", ".m-hint{font-size:12px" in t)
print("ia_ttl_theme", ".home-ia-ttl{font-size:16px;color:var(--text)}" in t)
print("status_13", ".status{font-size:13px;color:var(--text2)" in t)
