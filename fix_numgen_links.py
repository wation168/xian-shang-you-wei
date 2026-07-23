# -*- coding: utf-8 -*-
import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "frontend", "lottery")
pattern = re.compile(r'(/lottery/(?:[a-z]{2}(?:-[A-Z]{2})?/)?)[a-z0-9]+-number-generator\.html')
fixed = 0

for root, dirs, files in os.walk(BASE):
    for fname in files:
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()
        new_html = pattern.sub(r'\1number-generator.html', html)
        if new_html != html:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_html)
            fixed += 1

print(f"Fixed {fixed} files")
