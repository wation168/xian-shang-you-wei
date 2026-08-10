# -*- coding: utf-8 -*-
"""
fix_more_tools_and_cleanup.py
用途：
  1) 用 generate_tools_v2.py 裡「真正的」CATS字典 + get_cat() + more_pills()
     重建每個工具頁的「More Tools」區塊內容 —— 不重寫、不複製這份邏輯，
     直接import原始腳本呼叫，永遠只有一份來源，兩邊不會對不上。
  2) 清除舊版殘留的「Related Tools」區塊（blog-section/blog-grid/blog-card，
     連到 /tools/... 而非 /blog/... 的那種過期殘骸），用結構特徵比對，
     不依賴任何語言的標題文字，10個語言都能命中。

不呼叫任何API：
  - 分類/選工具邏輯：直接呼叫 generate_tools_v2.py 本尊的函式
  - 工具顯示名稱：從各語言既有檔案的<h1>標籤現抓，不自己翻譯/不自己猜
  - More Tools標題文字：保留原檔案裡本來就有的<h3>內容，完全不動

用法：
  cd D:\\xian-shang-you-wei
  python scripts\\fix_more_tools_and_cleanup.py --dry-run
  python scripts\\fix_more_tools_and_cleanup.py --apply
"""
import os, re, sys, glob, argparse, shutil, codecs, importlib.util

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, errors='replace')

REPO_ROOT = r"D:\xian-shang-you-wei"
GEN_SCRIPT_PATH = os.path.join(REPO_ROOT, "generate_tools_v2.py")
BASE = os.path.join(REPO_ROOT, "backend", "frontend", "tools")
BACKUP_DIR = os.path.join(REPO_ROOT, "backup_more_tools_")
ALL_LANGS = ["en", "zh-TW", "ja", "de", "fr", "es", "pt", "ko", "id", "zh-CN"]

# ====== 直接載入generate_tools_v2.py本尊，呼叫它真正的函式 ======
# (有 if __name__=="__main__": main() 保護，import不會誤觸發主程式/API key檢查)
spec = importlib.util.spec_from_file_location("generate_tools_v2", GEN_SCRIPT_PATH)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
print(f"[已載入] {GEN_SCRIPT_PATH} 內的CATS字典，共 {len(g.CATS)} 分類")


def lang_dir(lang):
    return BASE if lang == "zh-TW" else os.path.join(BASE, lang)


def extract_h1(html):
    m = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    if not m:
        return None
    txt = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return txt if txt else None


def build_name_lookup():
    """掃描全部語言全部工具檔案，建立 {lang: {slug: 標題文字}} 對照表
    （給 g.more_pills() 當作 names 參數用，內容全部來自既有檔案，不呼叫API）"""
    lookup = {}
    for lang in ALL_LANGS:
        lookup[lang] = {}
        d = lang_dir(lang)
        if not os.path.isdir(d):
            print(f"[警告] 找不到資料夾: {d}")
            continue
        files = glob.glob(os.path.join(d, "*.html"))
        for fp in files:
            slug = os.path.splitext(os.path.basename(fp))[0]
            if slug == "index":
                continue
            with open(fp, "r", encoding="utf-8") as f:
                html = f.read()
            title = extract_h1(html)
            if title:
                lookup[lang][slug] = title
    return lookup


MORE_TOOLS_RE = re.compile(
    r'(<div class="more-tools"><h3>.*?</h3><div class="tools-grid">).*?(</div></div>)',
    re.DOTALL
)

# 舊版殘留「Related Tools」區塊：blog-section包住blog-grid/blog-card，
# 且卡片連到 /tools/...（正常的延伸閱讀用blog_cards()連到 /blog/...，不會誤刪）
# 用結構特徵比對，不依賴任何語言的標題文字
LEGACY_RELATED_RE = re.compile(
    r'<div class="blog-section"><h3>[^<]*</h3>'
    r'<div class="blog-grid">(?=(?:(?!</div></div>).)*?href="/tools/)'
    r'(?:(?!</div></div>).)*?</div></div>',
    re.DOTALL
)


def process_file(fp, slug, lang, lookup, apply_changes, backup_root):
    with open(fp, "rb") as f:
        raw = f.read()
    html = raw.decode("utf-8")
    original = html

    changes = []

    # 1) 重建 More Tools 區塊內容（呼叫g.more_pills()本尊，標題文字保留原檔案不動）
    m = MORE_TOOLS_RE.search(html)
    if m:
        new_pills = g.more_pills(slug, lang, lookup.get(lang, {}))
        html2 = html[:m.start()] + m.group(1) + new_pills + m.group(2) + html[m.end():]
        if html2 != html:
            changes.append("more-tools重建")
        html = html2
    else:
        changes.append("[跳過]找不到more-tools區塊")

    # 2) 清除舊版殘留 Related Tools 區塊
    if LEGACY_RELATED_RE.search(html):
        html2 = LEGACY_RELATED_RE.sub('', html, count=1)
        if html2 != html:
            changes.append("清除舊版Related Tools殘留")
        html = html2

    if html == original:
        return None  # 無變化

    if apply_changes:
        rel = os.path.relpath(fp, BASE)
        backup_path = os.path.join(backup_root, rel)
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(fp, backup_path)
        with open(fp, "wb") as f:
            f.write(html.encode("utf-8"))

    return changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--langs", default="")
    a = ap.parse_args()

    if not a.dry_run and not a.apply:
        print("請指定 --dry-run 或 --apply"); sys.exit(1)

    langs = [l.strip() for l in a.langs.split(",")] if a.langs else ALL_LANGS

    print("=" * 60)
    print("步驟1：建立跨語言名稱對照表（掃描既有檔案<h1>，不呼叫API）")
    lookup = build_name_lookup()
    for lang in ALL_LANGS:
        print(f"  {lang}: {len(lookup.get(lang, {}))} 個工具標題已讀取")

    backup_root = BACKUP_DIR + __import__("time").strftime("%Y%m%d_%H%M%S")

    print("=" * 60)
    mode = "APPLY（正式寫入）" if a.apply else "DRY-RUN（僅列出，不寫入）"
    print(f"步驟2：處理工具頁 [{mode}]（分類邏輯直接呼叫generate_tools_v2.py本尊）")
    if a.apply:
        os.makedirs(backup_root, exist_ok=True)
        print(f"備份目錄: {backup_root}")

    total_changed = 0
    total_skipped = 0
    total_files = 0
    skip_examples = []

    for lang in langs:
        d = lang_dir(lang)
        if not os.path.isdir(d):
            continue
        files = sorted(glob.glob(os.path.join(d, "*.html")))
        for fp in files:
            slug = os.path.splitext(os.path.basename(fp))[0]
            if slug == "index":
                continue
            total_files += 1
            result = process_file(fp, slug, lang, lookup, a.apply, backup_root)
            if result is None:
                total_skipped += 1
                continue
            if any(c.startswith("[跳過]") for c in result):
                skip_examples.append((fp, result))
                continue
            total_changed += 1

    print("=" * 60)
    print(f"總檔案數: {total_files}")
    print(f"會修改/已修改: {total_changed}")
    print(f"無變化跳過: {total_skipped}")
    print(f"結構異常跳過: {len(skip_examples)}")
    if skip_examples:
        print("\n結構異常範例（前10筆，需人工檢查）:")
        for fp, reason in skip_examples[:10]:
            print(f"  {fp}: {reason}")

    if a.dry_run:
        print("\n這是dry-run，沒有任何檔案被修改。確認數字合理後執行 --apply。")


if __name__ == "__main__":
    main()
