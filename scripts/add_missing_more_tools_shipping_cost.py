# -*- coding: utf-8 -*-
"""
add_missing_more_tools_shipping_cost.py
用途：shipping-cost.html是比「More Tools」樣板更早產生的舊頁面，
      fix_more_tools_and_cleanup.py跑過之後這1個檔案(10語言版本)
      仍然缺少這個區塊。這支腳本專門補上，邏輯完全重用同一套：
      直接呼叫generate_tools_v2.py本尊的more_pills()，不重寫。

用法：
  cd D:\\xian-shang-you-wei
  python scripts\\add_missing_more_tools_shipping_cost.py --dry-run
  python scripts\\add_missing_more_tools_shipping_cost.py --apply
"""
import os, re, sys, glob, argparse, shutil, codecs, importlib.util

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')

REPO_ROOT = r"D:\xian-shang-you-wei"
GEN_SCRIPT_PATH = os.path.join(REPO_ROOT, "generate_tools_v2.py")
BASE = os.path.join(REPO_ROOT, "backend", "frontend", "tools")
ALL_LANGS = ["en", "zh-TW", "ja", "de", "fr", "es", "pt", "ko", "id", "zh-CN"]
SLUG = "shipping-cost"

spec = importlib.util.spec_from_file_location("generate_tools_v2", GEN_SCRIPT_PATH)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
print(f"[已載入] {GEN_SCRIPT_PATH}，shipping-cost分類: {g.get_cat(SLUG)}")


def lang_dir(lang):
    return BASE if lang == "zh-TW" else os.path.join(BASE, lang)


def extract_h1(html):
    m = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    if not m:
        return None
    txt = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return txt if txt else None


def build_name_lookup_for_cat(cat):
    """只掃該分類需要的工具，不用掃全站323個，比較快"""
    slugs = set(g.CATS.get(cat, []))
    lookup = {}
    for lang in ALL_LANGS:
        lookup[lang] = {}
        d = lang_dir(lang)
        for s in slugs:
            fp = os.path.join(d, f"{s}.html")
            if os.path.exists(fp):
                with open(fp, "r", encoding="utf-8") as f:
                    html = f.read()
                title = extract_h1(html)
                if title:
                    lookup[lang][s] = title
    return lookup


def find_insert_point(html):
    """決定插入位置：優先插在</article>後面(FAQ前)，
    沒有article就插在第一個 <section class="faq"> 前面，
    再沒有就插在 </body> 前"""
    m = re.search(r'</article>', html)
    if m:
        return m.end()
    m = re.search(r'<section class="faq">', html)
    if m:
        return m.start()
    m = re.search(r'</body>', html)
    if m:
        return m.start()
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        print("請指定 --dry-run 或 --apply"); sys.exit(1)

    cat = g.get_cat(SLUG)
    lookup = build_name_lookup_for_cat(cat)
    for lang in ALL_LANGS:
        print(f"  {lang}: {len(lookup.get(lang, {}))} 個同分類工具標題已讀取")

    print("=" * 60)
    for lang in ALL_LANGS:
        fp = os.path.join(lang_dir(lang), f"{SLUG}.html")
        if not os.path.exists(fp):
            print(f"[跳過] 找不到檔案: {fp}")
            continue
        with open(fp, "rb") as f:
            html = f.read().decode("utf-8")

        if 'class="more-tools"' in html:
            print(f"[跳過] {lang}: 已經有more-tools區塊了，不重複加")
            continue

        pos = find_insert_point(html)
        if pos is None:
            print(f"[無法處理] {lang}: 找不到合適的插入點，需人工檢查")
            continue

        pills = g.more_pills(SLUG, lang, lookup.get(lang, {}))
        # 標題文字沒有既有版本可抓，用get_cat對應的中性標題(僅本檔案例外情況使用)
        title_fallback = {"en":"More Tools","zh-TW":"更多工具","ja":"その他のツール",
                           "de":"Weitere Werkzeuge","fr":"Plus d'outils","es":"Más herramientas",
                           "pt":"Mais ferramentas","ko":"더 많은 도구","id":"Alat Lainnya","zh-CN":"更多工具"}.get(lang,"More Tools")
        block = f'\n  <div class="more-tools"><h3>{title_fallback}</h3><div class="tools-grid">{pills}</div></div>'

        new_html = html[:pos] + block + html[pos:]

        print(f"[{'會插入' if a.dry_run else '已插入'}] {lang}: shipping-cost.html 插入{len(pills.split(chr(10)))}個同類工具連結")

        if a.apply:
            shutil.copy2(fp, fp + ".bak_addmore")
            with open(fp, "wb") as f:
                f.write(new_html.encode("utf-8"))

    if a.dry_run:
        print("\n這是dry-run，沒有任何檔案被修改。")


if __name__ == "__main__":
    main()
