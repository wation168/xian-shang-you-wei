# -*- coding: utf-8 -*-
"""
為 pt 語言的8個「簡單」工具(公式跟兩國法規無關,純貨幣/單位問題)加上
葡萄牙/巴西地區下拉選單,比照 carbon-footprint.html 的下拉選單UI風格。

處理範圍(8個檔案,只有pt語言):
  gas-bill, home-energy-audit, dcf-calculator, startup-valuation,
  car-depreciation, income-replacement, liability-insurance, salary-raise

做法:
  1. 在 <div id="calcInputs"> 後面插入地區下拉選單(預設葡萄牙,跟現有€輸入框一致)
  2. 在 calculate() 函式開頭插入:讀取地區 → 決定符號(€/R$)與locale(pt-PT/pt-BR)
     → 同步更新所有 .input-prefix 顯示
  3. 把所有 'R$' + X.toLocaleString('en-GB', ...) 換成
     currencySymbol + X.toLocaleString(currencyLocale, ...)  (動態symbol/locale)

用法(先dry-run再apply):
  python fix_pt_region_dropdown.py --root "D:\\xian-shang-you-wei\\backend\\frontend"
  python fix_pt_region_dropdown.py --root "D:\\xian-shang-you-wei\\backend\\frontend" --apply
"""

import argparse
import re
import shutil
from pathlib import Path

TOOLS = [
    "gas-bill", "home-energy-audit", "dcf-calculator", "startup-valuation",
    "car-depreciation", "income-replacement", "liability-insurance", "salary-raise",
]

SELECT_HTML = (
    '<div class="input-group">\n'
    '  <label for="ptRegion">Região</label>\n'
    '  <div class="input-row"><select id="ptRegion" onchange="calculate()">'
    '<option value="PT" selected>🇵🇹 Portugal</option>'
    '<option value="BR">🇧🇷 Brasil</option></select></div>\n'
    '</div>\n'
    '  <small class="input-help">Selecione sua região para exibir valores em Euro (€) ou Real (R$)</small>\n'
)

CALC_INPUTS_RE = re.compile(r'(<div id="calcInputs">)')
CALCULATE_FN_RE = re.compile(r'(function calculate\(\)\s*\{)')
REGION_JS = (
    "\n  const ptRegion = document.getElementById('ptRegion')?.value || 'PT';\n"
    "  const currencySymbol = ptRegion === 'BR' ? 'R$' : '€';\n"
    "  const currencyLocale = ptRegion === 'BR' ? 'pt-BR' : 'pt-PT';\n"
    "  document.querySelectorAll('.input-prefix').forEach(function(el){ el.textContent = currencySymbol; });\n"
)
RS_ENGB_RE = re.compile(r"'R\$'\s*\+\s*(\w+)\.toLocaleString\('en-GB'")


def process_file(path: Path, apply: bool, backup_dir: Path):
    original = path.read_bytes()
    html = original.decode("utf-8")

    if 'id="ptRegion"' in html:
        return "already_done"

    if not CALC_INPUTS_RE.search(html):
        return "no_calcInputs_anchor"
    if not CALCULATE_FN_RE.search(html):
        return "no_calculate_fn"
    if not RS_ENGB_RE.search(html):
        return "no_rs_engb_pattern"

    new_html = CALC_INPUTS_RE.sub(lambda m: m.group(1) + SELECT_HTML, html, count=1)
    new_html = CALCULATE_FN_RE.sub(lambda m: m.group(1) + REGION_JS, new_html, count=1)
    replaced_count = len(RS_ENGB_RE.findall(new_html))
    new_html = RS_ENGB_RE.sub(r"currencySymbol + \1.toLocaleString(currencyLocale", new_html)

    if apply:
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_dir / path.name)
        path.write_bytes(new_html.encode("utf-8"))

    return f"ok({replaced_count}處toLocaleString改為動態)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup-dir", default=None)
    args = ap.parse_args()

    root = Path(args.root)
    backup_dir = Path(args.backup_dir) if args.backup_dir else root.parent / "_pt_region_dropdown_backup"

    for tool in TOOLS:
        path = root / "tools" / "pt" / f"{tool}.html"
        if not path.exists():
            print(f"[{tool}] 檔案不存在,跳過")
            continue
        result = process_file(path, args.apply, backup_dir)
        print(f"[{tool}] {result}")

    print(f"\n{'已套用' if args.apply else 'DRY-RUN,尚未寫入'}")
    if args.apply:
        print(f"已備份至: {backup_dir}")


if __name__ == "__main__":
    main()
