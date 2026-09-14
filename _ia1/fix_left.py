from pathlib import Path
p = Path(r"D:/xian-shang-you-wei/_ia1/apply.py")
t = p.read_text(encoding="utf-8")
old = '''leftover_src = (
    "          +'<div class=\\"mkt-src\\">'+_mktEsc((it.source||'')+' \\u00b7 \\u53f0\\u5317 '+(it.as_of||''))+'</div>'\\n"
    "          +'</div>';\\n"
)
'''
# file currently has real unicode in leftover_src; replace whole leftover block
start = t.find("leftover_src = (")
end = t.find("t = t.replace(leftover_src, \"\", 1)")
if start < 0 or end < 0:
    raise SystemExit("markers %s %s" % (start, end))
end = t.find("\n", end) + 1
new = r'''leftover_src = (
    "          +'<div class=\"mkt-src\">'+_mktEsc((it.source||'')+' \\u00b7 \\u53f0\\u5317 '+(it.as_of||''))+'</div>'\n"
    "          +'</div>';\n"
)
if t.count(leftover_src) != 1:
    raise SystemExit("leftover src %s" % t.count(leftover_src))
t = t.replace(leftover_src, "", 1)
'''
t = t[:start] + new + t[end:]
p.write_text(t, encoding="utf-8")
print("fixed leftover", start, end)
