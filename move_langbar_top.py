#!/usr/bin/env python3
"""
move_langbar_top.py — 把所有工具頁的語言切換從底部搬到頂部
用法：python move_langbar_top.py
"""
import os, re, glob

BASE = r"D:\xian-shang-you-wei\backend\frontend\tools"

# 匹配 lang-bar 區塊（單行開頭，跨行內容到 closing </div>）
LANGBAR_RE = re.compile(
    r'[ \t]*<div class="lang-bar">.*?</div>[ \t]*',
    re.DOTALL
)

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 找到 lang-bar
    m = LANGBAR_RE.search(content)
    if not m:
        return False  # 沒有 lang-bar，跳過

    langbar_html = m.group(0).strip()

    # 確認不是已經在 container 開頭（避免重複搬移）
    before = content[:m.start()].rstrip()
    if before.endswith('<div class="container">'):
        return "already"

    # 從原位置移除
    content = content[:m.start()] + content[m.end():]

    # 插入到 <div class="container"><div class="layout"> 之間
    target = '<div class="container"><div class="layout">'
    idx = content.find(target)
    if idx >= 0:
        insert_pos = idx + len('<div class="container">')
        content = content[:insert_pos] + "\n" + langbar_html + "\n" + content[insert_pos:]
    else:
        # fallback: 找 <div class="container"> 後面
        target2 = '<div class="container">'
        idx2 = content.find(target2)
        if idx2 < 0:
            return False
        insert_pos = idx2 + len(target2)
        content = content[:insert_pos] + "\n" + langbar_html + "\n" + content[insert_pos:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def main():
    print("=== 搬移語言切換到頂部 ===\n")

    # 收集所有 HTML 工具檔案
    files = []
    # zh-TW 根目錄
    for f in glob.glob(os.path.join(BASE, "*.html")):
        if os.path.basename(f) != "index.html":
            files.append(f)
    # 各語言子目錄
    for d in os.listdir(BASE):
        sub = os.path.join(BASE, d)
        if os.path.isdir(sub) and d not in (".", ".."):
            for f in glob.glob(os.path.join(sub, "*.html")):
                if os.path.basename(f) != "index.html":
                    files.append(f)

    print(f"找到 {len(files)} 個工具頁面\n")

    ok = 0
    skip = 0
    already = 0
    for f in files:
        result = process_file(f)
        if result == "already":
            already += 1
        elif result:
            ok += 1
        else:
            skip += 1
            print(f"  ⚠ 跳過: {os.path.relpath(f, BASE)}")

    print(f"\n✅ 完成：{ok} 頁已搬移，{already} 頁已在頂部，{skip} 頁跳過")

if __name__ == "__main__":
    main()
