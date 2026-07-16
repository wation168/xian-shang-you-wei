#!/usr/bin/env python3
# fix_currency_rates.py - 補上 TWD/IDR 匯率到所有 currency-converter
import os, sys

root = r"D:\xian-shang-you-wei"
tools = os.path.join(root, "backend", "frontend", "tools")
if not os.path.isdir(tools):
    print("找不到 tools 目錄")
    sys.exit(1)

OLD = "'MXN': 17.05\n  };"
NEW = "'MXN': 17.05,\n    'TWD': 32.20,\n    'IDR': 15800.00\n  };"

count = 0
langs = ["", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]
for lang in langs:
    if lang:
        fp = os.path.join(tools, lang, "currency-converter.html")
    else:
        fp = os.path.join(tools, "currency-converter.html")
    if not os.path.isfile(fp):
        continue
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    if "TWD" not in content.split("exchangeRates")[1].split("};")[0] if "exchangeRates" in content else "":
        content = content.replace(OLD, NEW)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
        print(f"  OK {fp}")
    else:
        print(f"  skip {fp}")

print(f"\n done: {count} files")
