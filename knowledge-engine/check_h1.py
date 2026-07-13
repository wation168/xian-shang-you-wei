import re, os
TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend", "frontend", "tools")
for f in sorted(os.listdir(TOOLS))[:15]:
    if not f.endswith('.html') or f == 'index.html':
        continue
    t = open(os.path.join(TOOLS, f), 'r', encoding='utf-8').read(3000)
    m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.DOTALL)
    m2 = re.search(r'<title>(.*?)</title>', t)
    h1 = m.group(1)[:40] if m else 'NONE'
    ti = m2.group(1)[:50] if m2 else 'NONE'
    print(f'{f}  h1: {h1}  title: {ti}')

for lang in ['en', 'ja', 'ko', 'zh-CN']:
    d = os.path.join(TOOLS, lang)
    if not os.path.isdir(d):
        continue
    print(f'\n--- {lang} ---')
    for f in sorted(os.listdir(d))[:5]:
        if not f.endswith('.html') or f == 'index.html':
            continue
        t = open(os.path.join(d, f), 'r', encoding='utf-8').read(3000)
        m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.DOTALL)
        m2 = re.search(r'<title>(.*?)</title>', t)
        h1 = m.group(1)[:40] if m else 'NONE'
        ti = m2.group(1)[:50] if m2 else 'NONE'
        print(f'{f}  h1: {h1}  title: {ti}')
