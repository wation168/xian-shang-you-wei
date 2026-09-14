# -*- coding: utf-8 -*-
from pathlib import Path
import re
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
it = p.read_text(encoding="utf-8")
marker = "async function _loadDesktopPicks()"
pos = it.find(marker)
if pos < 0:
    raise SystemExit("function not found")
# next function after this
nxt = it.find("\nasync function ", pos + 10)
nxt2 = it.find("\nfunction ", pos + 10)
ends = [x for x in (nxt, nxt2) if x > pos]
end = min(ends) if ends else pos + 2500
chunk = it[pos:end]
print("BEFORE LEN", len(chunk))
print(chunk[:800])
# replace _updLine section inside this function only
m = re.search(
    r"const items = j\.data \|\| \[\];\n(?:[^\n]*\n){0,12}?    if\(!items\.length\)\{",
    chunk,
)
if not m:
    raise SystemExit("items block missing in real function\n" + chunk[:1200])
new_mid = """const items = j.data || [];
    // GPT: only updated_at; never server_time as last update
    const _updLine = j.updated_at
      ? `<div style=\"padding:8px 12px 0;font-size:11px;color:var(--text3)\">上次更新（台北）：${j.updated_at}</div>`
      : `<div style=\"padding:8px 12px 0;font-size:11px;color:var(--text3)\">尚未更新（排程約每個交易日 09:06 台北）</div>`;
    if(!items.length){"""
chunk2 = chunk.replace(m.group(0), new_mid, 1)
it2 = it[:pos] + chunk2 + it[end:]
# ensure no server_time in this function for last-update
fn = it2[pos:pos+len(chunk2)]
if "j.server_time" in fn:
    print("WARN still has server_time in desktop picks fn")
else:
    print("desktop picks clean of server_time")
if "上次更新（台北）：${j.updated_at}" not in fn:
    raise SystemExit("label missing after fix")
p.write_text(it2, encoding="utf-8")
print("FIXED real _loadDesktopPicks")
# show empty state truncated
sp = it2.find("async function showPicksPage")
print(it2[sp:sp+1800][-400:])
