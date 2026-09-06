# -*- coding: utf-8 -*-
"""
修正 pt/home-energy-audit.html:
1. 這個檔案用 .toFixed(2) 而非 .toLocaleString(),跟另外7個工具格式不同,
   所以主腳本(fix_pt_region_dropdown.py)的規則抓不到,正確跳過。這支腳本
   專門處理這個檔案的 'R$' + X.toFixed(2) 格式,改成動態 currencySymbol。
2. 順便一併修正順手發現的2處英文殘留:
   - 'highest_consumer' 那行的 '/month' → '/mês'
   - 'consumption_breakdown' 那行 'Analyzed X appliances' → 葡萄牙文

用法(先dry-run再apply):
  python fix_home_energy_audit_pt.py --root "D:\\xian-shang-you-wei\\backend\\frontend"
  python fix_home_energy_audit_pt.py --root "D:\\xian-shang-you-wei\\backend\\frontend" --apply
"""

import argparse
import re
import shutil
from pathlib import Path

CALC_INPUTS_RE = re.compile(r'(<div id="calcInputs">)')
CALCULATE_FN_RE = re.compile(r'(function calculate\(\)\s*\{)')
REGION_JS = (
    "\n  const ptRegion = document.getElementById('ptRegion')?.value || 'PT';\n"
    "  const currencySymbol = ptRegion === 'BR' ? 'R$' : '€';\n"
    "  document.querySelectorAll('.input-prefix').forEach(function(el){ el.textContent = currencySymbol; });\n"
)
SELECT_HTML = (
    '<div class="input-group">\n'
    '  <label for="ptRegion">Região</label>\n'
    '  <div class="input-row"><select id="ptRegion" onchange="calculate()">'
    '<option value="PT" selected>🇵🇹 Portugal</option>'
    '<option value="BR">🇧🇷 Brasil</option></select></div>\n'
    '</div>\n'
    '  <small class="input-help">Selecione sua região para exibir valores em Euro (€) ou Real (R$)</small>\n'
)

# 一般格式: 'R$' + IDENT.toFixed(2)
RS_TOFIXED_RE = re.compile(r"'R\$'\s*\+\s*(\w+(?:\.\w+)?\.toFixed\(2\))")
# 內嵌格式: ' (R$' + highestConsumer.cost.toFixed(2) + '/month)'
EMBEDDED_RE = re.compile(
    r"' \(R\$' \+ (highestConsumer\.cost\.toFixed\(2\)) \+ '/month\)'"
)
ANALYZED_RE = re.compile(
    r"'Analyzed ' \+ costs\.length \+ ' appliances'"
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup-dir", default=None)
    args = ap.parse_args()

    root = Path(args.root)
    backup_dir = Path(args.backup_dir) if args.backup_dir else root.parent / "_home_energy_audit_pt_backup"
    path = root / "tools" / "pt" / "home-energy-audit.html"

    if not path.exists():
        print(f"找不到檔案: {path}")
        return

    html = path.read_bytes().decode("utf-8")
    changes = []

    if 'id="ptRegion"' in html:
        print("已經加過地區選單,不重複加")
    else:
        if not CALC_INPUTS_RE.search(html) or not CALCULATE_FN_RE.search(html):
            print("找不到預期的calcInputs或calculate()結構,停止,需人工確認")
            return
        html = CALC_INPUTS_RE.sub(lambda m: m.group(1) + SELECT_HTML, html, count=1)
        html = CALCULATE_FN_RE.sub(lambda m: m.group(1) + REGION_JS, html, count=1)
        changes.append("加入地區選單+JS")

    rs_matches = RS_TOFIXED_RE.findall(html)
    if rs_matches:
        html = RS_TOFIXED_RE.sub(r"currencySymbol + \1", html)
        changes.append(f"{len(rs_matches)}處 'R$'+toFixed 改為動態符號")

    if EMBEDDED_RE.search(html):
        html = EMBEDDED_RE.sub(r"' (' + currencySymbol + \1 + '/mês)'", html)
        changes.append("highest_consumer那行的/month改為/mês")

    if ANALYZED_RE.search(html):
        html = ANALYZED_RE.sub(r"'Analisados ' + costs.length + ' aparelhos'", html)
        changes.append("consumption_breakdown那行英文改為葡萄牙文")

    if not changes:
        print("沒有需要修改的地方(可能已經修過)")
        return

    print("將進行以下修改:")
    for c in changes:
        print(f"  - {c}")

    if args.apply:
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_dir / "home-energy-audit.html.bak")
        path.write_bytes(html.encode("utf-8"))
        print(f"\n已套用,備份至: {backup_dir}")
    else:
        print("\nDRY-RUN,尚未寫入")


if __name__ == "__main__":
    main()
