from pathlib import Path
p = Path(r"D:/xian-shang-you-wei/_ia1/apply.py")
t = p.read_text(encoding="utf-8")
start = t.find("old_news_box = ")
end = t.find("# news item class")
if start < 0 or end < 0:
    raise SystemExit("n %s %s" % (start, end))
new = '''old_news_head = "box.innerHTML = '<div class=\\"mkt-meta\\">'+_mktEsc(meta.join(' \\u00b7 ')||'"
new_news_head = "box.innerHTML = '<h2>\\u4eca\\u5929\\u8981\\u805e</h2><div class=\\"v5-sub\\">'+_mktEsc(meta.join(' \\u00b7 ')||'"
if t.count(old_news_head) != 1:
    raise SystemExit("news head %s" % t.count(old_news_head))
t = t.replace(old_news_head, new_news_head, 1)

'''
p.write_text(t[:start] + new + t[end:], encoding="utf-8")
print("news matcher fixed")
