#!/usr/bin/env python3
# fix_mainpy_titles.py
# 1. Patch main.py dynamic page titles (stock/report/picks)
# 2. Add lottery cross-links to tool pages footer
#
# Usage:
#   cd D:\xian-shang-you-wei\knowledge-engine
#   python fix_mainpy_titles.py

import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
MAINPY = os.path.join(REPO_ROOT, "backend", "main.py")
if not os.path.isfile(MAINPY):
    MAINPY = os.path.join(REPO_ROOT, "main.py")
if not os.path.isfile(MAINPY):
    print("[ERROR] Cannot find main.py")
    sys.exit(1)

FRONTEND = os.path.join(REPO_ROOT, "backend", "frontend")
if not os.path.isdir(FRONTEND):
    FRONTEND = os.path.join(REPO_ROOT, "frontend")

print(f"main.py: {MAINPY}")
print(f"Frontend: {FRONTEND}")
print()

# ================================================================
# PART 1: Patch main.py titles
# ================================================================

def fix_mainpy():
    print("=" * 60)
    print("PART 1: Patch main.py dynamic page titles")
    print("=" * 60)

    with open(MAINPY, 'r', encoding='utf-8') as f:
        code = f.read()

    original = code
    changes = 0

    # --- Fix 1: /report/ page title ---
    # Look for <title> in _build_report_html or report-related HTML
    # Common patterns:
    #   <title>{name} ...
    #   <title>f"{stock_name}...
    #   f"<title>{...} 個股分析

    # Pattern: anything like <title>{something} 個股分析 | 線上有位</title>
    # or <title>{something} | 線上有位</title> in report context
    report_title_patterns = [
        # f-string style
        (r'(<title>)\{(\w+)\}\s*(?:（[^）]*）\s*)?個股分析\s*[|｜]\s*線上有位(</title>)',
         r'\1{\2} 能買嗎？多空雷達 × 支撐壓力位完整分析｜線上有位\3'),
        # Another common pattern
        (r'(<title>)[^<]*個股分析[^<]*線上有位(</title>)',
         None),  # skip if too generic
    ]

    for pat, repl in report_title_patterns:
        if repl and re.search(pat, code):
            code = re.sub(pat, repl, code, count=1)
            changes += 1
            print("  [OK] Report page title updated")
            break

    # --- Fix 2: /picks page title ---
    picks_patterns = [
        (r'<title>每日精選股[^<]*</title>',
         '<title>今日精選股｜AI 篩出的強勢股，附進場理由與停損位</title>'),
        (r'<title>精選股[^<]*</title>',
         '<title>今日精選股｜AI 篩出的強勢股，附進場理由與停損位</title>'),
    ]
    for pat, repl in picks_patterns:
        if re.search(pat, code):
            code = re.sub(pat, repl, code, count=0)
            changes += 1
            print("  [OK] Picks page title updated")
            break

    # --- Fix 3: /stock/landing title ---
    stock_patterns = [
        (r'<title>線上有位\s*[|｜]\s*台股個股分析</title>',
         '<title>台股 AI 分析｜多空雷達 × K棒型態 × 支撐壓力，一鍵出報告</title>'),
        (r'<title>線上有位\s*[|｜]\s*[^<]*</title>',
         '<title>台股 AI 分析｜多空雷達 × K棒型態 × 支撐壓力，一鍵出報告</title>'),
        (r'<title>台股個股分析\s*[|｜]\s*線上有位</title>',
         '<title>台股 AI 分析｜多空雷達 × K棒型態 × 支撐壓力，一鍵出報告</title>'),
    ]
    for pat, repl in stock_patterns:
        matches = re.findall(pat, code)
        if matches:
            code = re.sub(pat, repl, code)
            changes += 1
            print(f"  [OK] Stock landing title updated ({len(matches)} matches)")
            break

    # --- Fix 4: meta description for stock pages ---
    # Add/update meta description for landing
    stock_desc = "輸入股票代號，AI 自動分析多空雷達、K棒型態、支撐壓力位、葛蘭碧買點，一鍵產出完整報告。免費使用。還有 500+ 計算工具和全球彩票選號。"
    # Look for meta description near stock landing HTML
    stock_meta_pat = r'(台股.*?<meta\s+name="description"\s+content=")[^"]*(")'
    if re.search(stock_meta_pat, code, re.DOTALL):
        code = re.sub(stock_meta_pat, f'\\1{stock_desc}\\2', code, count=1, flags=re.DOTALL)
        changes += 1
        print("  [OK] Stock meta description updated")

    if code != original:
        with open(MAINPY, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"\n  Total changes: {changes}")
    else:
        print("\n  [INFO] No matching title patterns found in main.py")
        print("  You may need to manually search for <title> tags in main.py")
        print("  and replace with these new titles:")
        print()
        print("  /stock/landing:")
        print("    台股 AI 分析｜多空雷達 × K棒型態 × 支撐壓力，一鍵出報告")
        print()
        print("  /report/{slug}:")
        print("    {stock_name} 能買嗎？多空雷達 × 支撐壓力位完整分析｜線上有位")
        print()
        print("  /picks:")
        print("    今日精選股｜AI 篩出的強勢股，附進場理由與停損位")

    return changes


# ================================================================
# PART 2: Add lottery cross-links to tool pages
# ================================================================

LOTTERY_LINK_HTML = '''<a class="related-link" href="https://lottery.softglow-ai.com/zh-TW/" target="_blank">15國彩票開獎＋12種選號工具</a>'''
LOTTERY_LINK_EN = '''<a class="related-link" href="https://lottery.softglow-ai.com/en/" target="_blank">15 Lotteries + 12 Number Pickers</a>'''
LOTTERY_LINK_JA = '''<a class="related-link" href="https://lottery.softglow-ai.com/ja/" target="_blank">15ヶ国の宝くじ＋12種の番号選びツール</a>'''
LOTTERY_LINK_KO = '''<a class="related-link" href="https://lottery.softglow-ai.com/ko/" target="_blank">15개국 복권 + 12가지 번호 선택기</a>'''

LANG_LOTTERY_MAP = {
    'zh-TW': LOTTERY_LINK_HTML,
    'zh-CN': LOTTERY_LINK_HTML.replace('zh-TW', 'zh-TW'),  # zh-CN users can read zh-TW
    'en': LOTTERY_LINK_EN,
    'ja': LOTTERY_LINK_JA,
    'ko': LOTTERY_LINK_KO,
    'de': LOTTERY_LINK_EN,
    'fr': LOTTERY_LINK_EN,
    'es': LOTTERY_LINK_EN,
    'pt': LOTTERY_LINK_EN,
    'id': LOTTERY_LINK_EN,
}

SOFTGLOW_LINK_FOR_LOTTERY = {
    'zh-TW': '<a href="https://softglow-ai.com/tools/" target="_blank" style="display:block;padding:12px 16px;margin:16px 0;background:#EBF5FF;border:1px solid #BEE3F8;border-radius:8px;color:#2563EB;font-size:14px;text-decoration:none;text-align:center;">500+ 免費計算工具（金融、房貸、健康、工程）→</a>',
    'en': '<a href="https://softglow-ai.com/tools/en/" target="_blank" style="display:block;padding:12px 16px;margin:16px 0;background:#EBF5FF;border:1px solid #BEE3F8;border-radius:8px;color:#2563EB;font-size:14px;text-decoration:none;text-align:center;">500+ Free Calculators (Finance, Health, Engineering) →</a>',
    'ja': '<a href="https://softglow-ai.com/tools/ja/" target="_blank" style="display:block;padding:12px 16px;margin:16px 0;background:#EBF5FF;border:1px solid #BEE3F8;border-radius:8px;color:#2563EB;font-size:14px;text-decoration:none;text-align:center;">500+ 無料計算ツール（金融・健康・工学）→</a>',
    'ko': '<a href="https://softglow-ai.com/tools/ko/" target="_blank" style="display:block;padding:12px 16px;margin:16px 0;background:#EBF5FF;border:1px solid #BEE3F8;border-radius:8px;color:#2563EB;font-size:14px;text-decoration:none;text-align:center;">500+ 무료 계산 도구 (금융, 건강, 공학) →</a>',
}


def get_lang_from_path(filepath, tools_dir):
    rel = os.path.relpath(filepath, tools_dir).replace('\\', '/')
    parts = rel.split('/')
    if len(parts) >= 2:
        lang_dir = parts[0]
        known_langs = ['en','ja','ko','de','fr','es','pt','id','zh-CN']
        if lang_dir in known_langs:
            return lang_dir
    return 'zh-TW'


def add_lottery_links_to_tools():
    print()
    print("=" * 60)
    print("PART 2: Add lottery cross-links to tool pages")
    print("=" * 60)

    tools_dir = os.path.join(FRONTEND, "tools")
    if not os.path.isdir(tools_dir):
        print(f"  [SKIP] Tools directory not found: {tools_dir}")
        return 0

    added = 0
    skipped = 0

    for root, dirs, files in os.walk(tools_dir):
        for f in files:
            if not f.endswith('.html'):
                continue
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as fh:
                    html = fh.read()

                # Skip if already has lottery link
                if 'lottery.softglow-ai.com' in html:
                    skipped += 1
                    continue

                lang = get_lang_from_path(filepath, tools_dir)
                lottery_link = LANG_LOTTERY_MAP.get(lang, LOTTERY_LINK_EN)

                # Insert lottery link before the last </div> in related-card
                # Or before </aside> if related-card exists
                if '<div class="related-card">' in html:
                    # Add before the closing of related-card's parent
                    # Find the last related-link and add after it
                    insert_pos = html.rfind('</a>\n</div>\n</aside>')
                    if insert_pos == -1:
                        insert_pos = html.rfind('</aside>')

                    if insert_pos > 0:
                        # Find the related-card closing div
                        rc_end = html.rfind('</div>', 0, insert_pos)
                        if rc_end > 0:
                            html = html[:rc_end] + '\n    ' + lottery_link + '\n  ' + html[rc_end:]
                            added += 1
                elif '</footer>' in html:
                    # No related-card, add before footer
                    html = html.replace('</footer>',
                        f'<div style="max-width:1080px;margin:0 auto;padding:0 20px 20px">{lottery_link}</div>\n</footer>')
                    added += 1

                with open(filepath, 'w', encoding='utf-8') as fh:
                    fh.write(html)

            except Exception as e:
                pass

    print(f"  Added lottery links: {added}")
    print(f"  Already had links:   {skipped}")
    return added


# ================================================================
# Main
# ================================================================

if __name__ == '__main__':
    c1 = fix_mainpy()
    c2 = add_lottery_links_to_tools()

    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"  main.py title changes: {c1}")
    print(f"  Tool pages + lottery links: {c2}")
    print()
    print("Next: git add -A && git commit && git push")
    print("Then run fix_lottery_all.py in the lottery repo")
