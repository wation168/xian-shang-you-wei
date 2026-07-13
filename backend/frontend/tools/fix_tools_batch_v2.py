import os, re

JS_ID_FIXES = [
    ("getElementById('resultsDiv')",        "getElementById('results')"),
    ('getElementById("resultsDiv")',        'getElementById("results")'),
    ("getElementById('results_section')",   "getElementById('results')"),
    ('getElementById("results_section")',   'getElementById("results")'),
    ("getElementById('resultDiv')",         "getElementById('results')"),
    ('getElementById("resultDiv")',         'getElementById("results")'),
    ("getElementById('result-section')",    "getElementById('results')"),
    ('getElementById("result-section")',    'getElementById("results")'),
    ("getElementById('resultSection')",     "getElementById('results')"),
    ('getElementById("resultSection")',     'getElementById("results")'),
    ("getElementById('output')",            "getElementById('results')"),
    ('getElementById("output")',            'getElementById("results")'),
    ("getElementById('outputDiv')",         "getElementById('results')"),
    ('getElementById("outputDiv")',         'getElementById("results")'),
    ("getElementById('calcResults')",       "getElementById('results')"),
    ('getElementById("calcResults")',       'getElementById("results")'),
    ("getElementById('calc-results')",      "getElementById('results')"),
    ('getElementById("calc-results")',      'getElementById("results")'),
    ("getElementById('resultArea')",        "getElementById('results')"),
    ('getElementById("resultArea")',        'getElementById("results")'),
    ("getElementById('result_area')",       "getElementById('results')"),
    ('getElementById("result_area")',       'getElementById("results")'),
    ("getElementById('resultsSection')",    "getElementById('results')"),
    ('getElementById("resultsSection")',    'getElementById("results")'),
    ("getElementById('results_container')", "getElementById('results')"),
    ('getElementById("results_container")', 'getElementById("results")'),
    ("getElementById('calculation-results')", "getElementById('results')"),
    ('getElementById("calculation-results")', 'getElementById("results")'),
    ("getElementById('calc_results')",      "getElementById('results')"),
    ('getElementById("calc_results")',      'getElementById("results")'),
    ("getElementById('calculationResults')", "getElementById('results')"),
    ('getElementById("calculationResults")', 'getElementById("results")'),
    ("getElementById('result')",            "getElementById('results')"),
    ('getElementById("result")',            'getElementById("results")'),
]

LANG_CURRENCY = {
    "zh-TW": "NT$", "en": "$", "ja": "\u00a5", "ko": "\u20a9",
    "de": "\u20ac", "fr": "\u20ac", "es": "\u20ac",
    "pt": "R$", "id": "Rp", "zh-CN": "\u00a5",
}

def detect_lang(filepath):
    parts = filepath.replace("\\", "/").split("/")
    parent = parts[-2] if len(parts) >= 2 else ""
    if parent in {"en","ja","ko","de","fr","es","pt","id","zh-CN"}:
        return parent
    return "zh-TW"

total = js_fixed = cur_fixed = 0
for root, _, files in os.walk("."):
    for fname in files:
        if not fname.endswith(".html") or fname in ("index.html","check_tools.py","fix_tools_batch.py","fix_tools_batch_v2.py"):
            continue
        fp = os.path.join(root, fname)
        total += 1
        try:
            html = open(fp, "r", encoding="utf-8").read()
        except:
            continue
        orig = html
        lang = detect_lang(fp)
        for old, new in JS_ID_FIXES:
            if old in html:
                html = html.replace(old, new)
        if html != orig:
            js_fixed += 1
        sym = LANG_CURRENCY.get(lang, "$")
        if "\u00a3" in html and sym != "\u00a3":
            html = html.replace("\u00a3", sym)
            cur_fixed += 1
        if html != orig:
            open(fp, "w", encoding="utf-8").write(html)

print(f"Total: {total}")
print(f"JS fixed: {js_fixed}")
print(f"Currency fixed: {cur_fixed}")
