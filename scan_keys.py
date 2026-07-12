# -*- coding: utf-8 -*-
"""
scan_keys.py — 掃描 output/tools 裡每個工具的「結果欄位代碼」與標題。
跑完把結果貼給 Claude，Claude 就能一次把全部 35 個工具的翻譯字典補齊。
"""
import os, re, json, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else "output/tools"
out = {}
for fn in sorted(os.listdir(ROOT)):
    if fn.endswith(".html"):
        h = open(os.path.join(ROOT, fn), encoding="utf-8").read()
        keys = re.findall(r'data-key="([^"]+)"', h)
        m = re.search(r"<h1>(.*?)</h1>", h, re.S)
        out[fn.replace(".html", "")] = {
            "title": m.group(1).strip() if m else "",
            "result_keys": keys,
        }
print(json.dumps(out, ensure_ascii=False, indent=1))
