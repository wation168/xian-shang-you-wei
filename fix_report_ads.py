#!/usr/bin/env python3
"""
fix_report_ads.py (v2)
為 main.py 的個股報告頁加入 AdSense 廣告

做法：
  1. 加入 _inject_report_ads() helper 函式
  2. 不動 return 語句，改在呼叫端包裝

用法：
  cd D:\\xian-shang-you-wei\\backend
  python fix_report_ads.py
"""
import re
import os
import shutil

MAIN_PY = "main.py"

# AdSense 廣告注入函式
AD_HELPER = r'''
# === AdSense 報告頁廣告注入 ===
def _inject_report_ads(html: str) -> str:
    """在報告頁 HTML 注入 AdSense 廣告"""
    PUB = "ca-pub-1768270548115739"
    SLOT_ARTICLE = "2793159185"
    SLOT_BOTTOM = "4182262477"

    preconnect = '<link rel="preconnect" href="https://pagead2.googlesyndication.com">\n'
    html = html.replace('</head>', preconnect + '</head>', 1)

    in_article_ad = (
        '<div style="margin:20px auto;text-align:center;max-width:728px;">'
        '<ins class="adsbygoogle" style="display:block;text-align:center;min-height:250px;"'
        ' data-ad-layout="in-article" data-ad-format="fluid"'
        f' data-ad-client="{PUB}" data-ad-slot="{SLOT_ARTICLE}"></ins>'
        '<script>try{(adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}</script>'
        '</div>'
    )

    parts = html.split('</section>')
    if len(parts) > 4:
        parts[3] = parts[3] + in_article_ad
        html = '</section>'.join(parts)

    bottom_ad = (
        '<div style="margin:24px auto;text-align:center;max-width:728px;">'
        '<ins class="adsbygoogle" style="display:block;min-height:250px;"'
        f' data-ad-client="{PUB}" data-ad-slot="{SLOT_BOTTOM}"'
        ' data-ad-format="auto" data-full-width-responsive="true"></ins>'
        '<script>try{(adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}</script>'
        '</div>'
    )

    body_pos = html.rfind('</body>')
    if body_pos > 0:
        html = html[:body_pos] + bottom_ad + html[body_pos:]

    ad_script = (
        '<script>'
        'setTimeout(function(){var s=document.createElement("script");s.async=true;'
        f's.src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB}";'
        's.crossOrigin="anonymous";document.head.appendChild(s);},2000);'
        '</script>'
    )

    body_pos = html.rfind('</body>')
    if body_pos > 0:
        html = html[:body_pos] + ad_script + html[body_pos:]

    return html
# === End AdSense 報告頁廣告注入 ===

'''


def fix_main_py():
    if not os.path.exists(MAIN_PY):
        print(f"[ERROR] 找不到 {MAIN_PY}")
        return

    with open(MAIN_PY, "r", encoding="utf-8") as f:
        content = f.read()

    if "_inject_report_ads" in content:
        print("[INFO] _inject_report_ads 已存在，跳過")
        return

    backup = MAIN_PY + ".ads.bak"
    shutil.copy2(MAIN_PY, backup)
    print(f"[OK] 備份 → {backup}")

    changes = 0

    # 1. 在 _build_report_html 前插入 helper 函式
    match = re.search(r'^def _build_report_html', content, re.MULTILINE)
    if not match:
        print("[ERROR] 找不到 _build_report_html")
        os.remove(backup)
        return

    content = content[:match.start()] + AD_HELPER + content[match.start():]
    changes += 1
    print("[FIX] 插入 _inject_report_ads 函式")

    # 2. 找呼叫 _build_report_html 的地方，在那裡包裝
    #    例如: html = _build_report_html(...)
    #    改成: html = _inject_report_ads(_build_report_html(...))
    #
    #    或: return HTMLResponse(_build_report_html(...))
    #    改成: return HTMLResponse(_inject_report_ads(_build_report_html(...)))

    # Pattern A: 變數賦值
    pattern_a = r'(\s*\w+\s*=\s*)(_build_report_html\([^)]*\))'
    matches_a = list(re.finditer(pattern_a, content))

    # Pattern B: 直接在 HTMLResponse 裡呼叫
    pattern_b = r'(HTMLResponse\()(_build_report_html\([^)]*\))'
    matches_b = list(re.finditer(pattern_b, content))

    if matches_a:
        # 從後往前替換避免位移
        for m in reversed(matches_a):
            old = m.group(2)
            new = f"_inject_report_ads({old})"
            start = m.start(2)
            end = m.end(2)
            content = content[:start] + new + content[end:]
            changes += 1
            print(f"[FIX] 包裝呼叫: {old[:50]}...")
    elif matches_b:
        for m in reversed(matches_b):
            old = m.group(2)
            new = f"_inject_report_ads({old})"
            start = m.start(2)
            end = m.end(2)
            content = content[:start] + new + content[end:]
            changes += 1
            print(f"[FIX] 包裝呼叫: HTMLResponse({old[:50]}...)")
    else:
        # Pattern C: 找 report 路由裡的 _build_report_html 呼叫
        # 更寬鬆的搜尋
        all_calls = list(re.finditer(r'_build_report_html\(', content))
        if all_calls:
            print(f"\n[WARN] 找到 {len(all_calls)} 處呼叫 _build_report_html，但格式不符自動包裝")
            for m in all_calls:
                line_start = content.rfind('\n', 0, m.start()) + 1
                line = content[line_start:content.find('\n', m.start())]
                print(f"  行 {content[:m.start()].count(chr(10))+1}: {line.strip()[:80]}")
            print("\n[手動修改] 請在上面的呼叫處加上 _inject_report_ads() 包裝")
            print("  例如: html = _build_report_html(...)")
            print("  改成: html = _inject_report_ads(_build_report_html(...))")
        else:
            print("[WARN] 找不到 _build_report_html 的呼叫處")

    # 寫入
    with open(MAIN_PY, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n[DONE] 共修改 {changes} 處")
    print(f"[BACKUP] {backup}")
    print("\n[NEXT] 語法檢查:")
    print(f'  python -c "import ast; ast.parse(open(\'main.py\',encoding=\'utf-8\').read()); print(\'OK\')"')


if __name__ == "__main__":
    fix_main_py()
