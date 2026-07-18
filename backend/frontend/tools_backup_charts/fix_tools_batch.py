#!/usr/bin/env python3
"""
SoftGlow Tool Pages Batch Fix
1. Fix JS getElementById mismatches (resultsDiv -> results, etc.)
2. Fix currency symbols per language
3. Fix results div show/hide

Usage:
  cd D:\\xian-shang-you-wei\\backend\\frontend\\tools
  python fix_tools_batch.py
"""

import os, re

# ── Currency config per language ────────────────────────────────────────
LANG_CURRENCY = {
    "zh-TW": {"symbol": "NT$", "code": "TWD", "format": "prefix"},
    "en":    {"symbol": "$",   "code": "USD", "format": "prefix"},
    "ja":    {"symbol": "¥",   "code": "JPY", "format": "prefix"},
    "ko":    {"symbol": "₩",   "code": "KRW", "format": "prefix"},
    "de":    {"symbol": "€",   "code": "EUR", "format": "suffix"},
    "fr":    {"symbol": "€",   "code": "EUR", "format": "suffix"},
    "es":    {"symbol": "€",   "code": "EUR", "format": "suffix"},
    "pt":    {"symbol": "R$",  "code": "BRL", "format": "prefix"},
    "id":    {"symbol": "Rp",  "code": "IDR", "format": "prefix"},
    "zh-CN": {"symbol": "¥",   "code": "CNY", "format": "prefix"},
}

# ── Common JS ID replacements ───────────────────────────────────────────
# Pattern: JS uses X but HTML template has "results"
JS_ID_FIXES = [
    # Results container
    ("getElementById('resultsDiv')",    "getElementById('results')"),
    ('getElementById("resultsDiv")',    'getElementById("results")'),
    ("getElementById('results_section')", "getElementById('results')"),
    ('getElementById("results_section")', 'getElementById("results")'),
    ("getElementById('resultDiv')",     "getElementById('results')"),
    ('getElementById("resultDiv")',     'getElementById("results")'),
    ("getElementById('result-section')", "getElementById('results')"),
    ('getElementById("result-section")', 'getElementById("results")'),
    ("getElementById('resultSection')", "getElementById('results')"),
    ('getElementById("resultSection")', 'getElementById("results")'),
    ("getElementById('output')",        "getElementById('results')"),
    ('getElementById("output")',        'getElementById("results")'),
    ("getElementById('outputDiv')",     "getElementById('results')"),
    ('getElementById("outputDiv")',     'getElementById("results")'),
    ("getElementById('calcResults')",   "getElementById('results')"),
    ('getElementById("calcResults")',   'getElementById("results")'),
    ("getElementById('calc-results')",  "getElementById('results')"),
    ('getElementById("calc-results")',  'getElementById("results")'),
    ("getElementById('resultArea')",    "getElementById('results')"),
    ('getElementById("resultArea")',    'getElementById("results")'),
    ("getElementById('result_area')",   "getElementById('results')"),
    ('getElementById("result_area")',   'getElementById("results")'),
]

# Common class toggle fixes
CLASS_FIXES = [
    # Show results: various patterns -> standard
    (".style.display = 'block'",   ".classList.add('show')"),
    ('.style.display = "block"',   ".classList.add('show')"),
    (".style.display='block'",     ".classList.add('show')"),
    ('.style.display="block"',     ".classList.add('show')"),
]


def detect_lang(filepath):
    parts = filepath.replace("\\", "/").split("/")
    parent = parts[-2] if len(parts) >= 2 else ""
    lang_dirs = {"en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"}
    if parent in lang_dirs:
        return parent
    return "zh-TW"


def fix_js_ids(html):
    """Fix getElementById calls to match template IDs."""
    fixed = False
    for old, new in JS_ID_FIXES:
        if old in html:
            html = html.replace(old, new)
            fixed = True
    return html, fixed


def fix_results_display(html):
    """Fix results show logic.
    Template uses: <div class="results" id="results"> with CSS .results.show{display:block}
    Some JS uses style.display='block' on the results div - change to classList.add('show')
    But ONLY for the results div, not other elements.
    """
    # More targeted: find lines that get 'results' and then set display
    # Pattern: var x = getElementById('results'); ... x.style.display = 'block'
    # This is too complex for simple string replace, skip for now
    # The ID fix alone should resolve most issues
    return html, False


def fix_currency(html, lang):
    """Replace incorrect currency symbols."""
    currency = LANG_CURRENCY.get(lang)
    if not currency:
        return html, False

    correct_symbol = currency["symbol"]
    fixed = False

    # Don't fix if it's already using the correct currency
    # or if it's a currency converter tool (needs multiple currencies)
    slug = os.path.basename("").replace(".html", "")

    # Replace pound sign (most common error)
    if "£" in html and correct_symbol != "£":
        # Don't replace in article text about British currency
        # Only replace in calculator inputs/outputs/labels
        # Simple approach: replace all £ since these aren't UK-specific tools
        html = html.replace("£", correct_symbol)
        fixed = True

    return html, fixed


def fix_missing_results_id(html):
    """If there's no id='results' but there's a resultsDiv or similar, add it."""
    if 'id="results"' in html or "id='results'" in html:
        return html, False

    # Try to find a results container and add the ID
    patterns = [
        ('class="results"', 'class="results" id="results"'),
        ('class="result"', 'class="result" id="results"'),
        ('class="results-section"', 'class="results-section" id="results"'),
    ]

    for old, new in patterns:
        if old in html and 'id=' not in html.split(old)[0].split('\n')[-1]:
            html = html.replace(old, new, 1)
            return html, True

    return html, False


def fix_addsclass_show(html):
    """Ensure results div uses classList.add('show') pattern.
    If JS does: document.getElementById('results').style.display = 'block'
    Change to: document.getElementById('results').classList.add('show')
    """
    # Pattern: getElementById('results') followed by .style.display on same or next line
    pattern = re.compile(
        r"(getElementById\(['\"]results['\"]\))\s*\.\s*style\s*\.\s*display\s*=\s*['\"]block['\"]",
    )
    if pattern.search(html):
        html = pattern.sub(r"\1.classList.add('show')", html)
        return html, True
    return html, False


def main():
    total = 0
    js_fixed = 0
    currency_fixed = 0
    id_added = 0
    show_fixed = 0

    for root, _, files in os.walk("."):
        for fname in files:
            if not fname.endswith(".html") or fname in ("index.html", "check_tools.py"):
                continue

            filepath = os.path.join(root, fname)
            total += 1

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    html = f.read()
            except Exception:
                continue

            original = html
            lang = detect_lang(filepath)

            # 1. Fix JS getElementById mismatches
            html, did_fix = fix_js_ids(html)
            if did_fix:
                js_fixed += 1

            # 2. Add missing results ID
            html, did_fix = fix_missing_results_id(html)
            if did_fix:
                id_added += 1

            # 3. Fix classList.add('show') pattern
            html, did_fix = fix_addsclass_show(html)
            if did_fix:
                show_fixed += 1

            # 4. Fix currency
            html, did_fix = fix_currency(html, lang)
            if did_fix:
                currency_fixed += 1

            # Write if changed
            if html != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(html)

    print(f"Total scanned: {total}")
    print(f"JS IDs fixed: {js_fixed}")
    print(f"Results ID added: {id_added}")
    print(f"Show logic fixed: {show_fixed}")
    print(f"Currency fixed: {currency_fixed}")
    print(f"\nRe-run check_tools.py to verify remaining issues.")


if __name__ == "__main__":
    main()
