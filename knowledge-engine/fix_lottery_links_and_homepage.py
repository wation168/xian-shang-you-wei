#!/usr/bin/env python3
# fix_lottery_links_and_homepage.py
#
# 一次修四個問題：
# 1. 首頁 homepage.html：彩票連結放顯眼位置
# 2. 首頁 homepage.html：K棒型態語言 3 改 10
# 3. 工具頁 3240 頁：彩票橫幅從底部移到計算器下方
# 4. landing.html：Title 改寫（痛點式）
#
# 用法：
#   cd D:\xian-shang-you-wei
#   python knowledge-engine\fix_lottery_links_and_homepage.py --dry-run
#   python knowledge-engine\fix_lottery_links_and_homepage.py

import os
import re
import sys
import argparse

# ── 彩票連結對照表 ──
LOTTERY_LINKS = {
    'zh-TW': {'text': '🎰 15國彩票開獎＋12種智慧選號工具', 'url': 'https://lottery.softglow-ai.com/zh-TW/', 'sub': '威力彩・大樂透・Powerball・Mega Millions — 星座、生日、夢境、AI 等選號方式'},
    'en':    {'text': '🎰 15 Global Lotteries + 12 Smart Number Pickers', 'url': 'https://lottery.softglow-ai.com/en/', 'sub': 'Powerball · Mega Millions · EuroMillions — Zodiac, Birthday, Dream, AI & more'},
    'ja':    {'text': '🎰 世界15の宝くじ＋12種類の番号選択ツール', 'url': 'https://lottery.softglow-ai.com/ja/', 'sub': 'パワーボール・メガミリオンズ — 星座・誕生日・夢・AI選番'},
    'ko':    {'text': '🎰 세계 15개 복권 + 12가지 번호 선택 도구', 'url': 'https://lottery.softglow-ai.com/ko/', 'sub': 'Powerball · Mega Millions · EuroMillions — 별자리, 생일, 꿈, AI'},
    'de':    {'text': '🎰 15 Globale Lotterien + 12 Nummern-Tools', 'url': 'https://lottery.softglow-ai.com/en/', 'sub': 'Powerball · EuroMillions · Lotto 6aus49 — Sternzeichen, Geburtstag, Traum & AI'},
    'fr':    {'text': '🎰 15 Loteries Mondiales + 12 Outils de Selection', 'url': 'https://lottery.softglow-ai.com/en/', 'sub': 'Powerball · EuroMillions · Mega Millions — Astrologie, Anniversaire & IA'},
    'es':    {'text': '🎰 15 Loterias Globales + 12 Herramientas', 'url': 'https://lottery.softglow-ai.com/en/', 'sub': 'Powerball · EuroMillions · El Gordo — Zodiaco, Cumpleanos & IA'},
    'pt':    {'text': '🎰 15 Loterias Globais + 12 Ferramentas', 'url': 'https://lottery.softglow-ai.com/en/', 'sub': 'Powerball · Mega-Sena · EuroMillions — Signo, Aniversario & IA'},
    'id':    {'text': '🎰 15 Lotere Global + 12 Alat Pemilihan Angka', 'url': 'https://lottery.softglow-ai.com/en/', 'sub': 'Powerball · Mega Millions · EuroMillions — Zodiak, Ulang Tahun & AI'},
    'zh-CN': {'text': '🎰 15国彩票开奖＋12种智慧选号工具', 'url': 'https://lottery.softglow-ai.com/zh-TW/', 'sub': '威力彩・大乐透・Powerball・Mega Millions — 星座、生日、梦境、AI'},
}

def get_lottery_banner_html(lang):
    info = LOTTERY_LINKS.get(lang, LOTTERY_LINKS['en'])
    return (
        '<div style="margin:20px 0;padding:16px 20px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:12px;text-align:center">'
        f'<a href="{info["url"]}" target="_blank" rel="noopener" style="text-decoration:none;color:#fff">'
        f'<div style="font-size:16px;font-weight:700;margin-bottom:4px">{info["text"]}</div>'
        f'<div style="font-size:12px;opacity:0.9">{info["sub"]}</div>'
        '</a></div>'
    )

def detect_lang(filepath, content):
    parts = filepath.replace('\\', '/').split('/')
    for p in parts:
        if p in ('en', 'ja', 'ko', 'de', 'fr', 'es', 'pt', 'id', 'zh-CN'):
            return p
    m = re.search(r'<html\s+lang=["\']?([^"\'>\s]+)', content)
    if m:
        lang_map = {'zh-TW': 'zh-TW', 'zh-CN': 'zh-CN', 'en': 'en', 'ja': 'ja',
                     'ko': 'ko', 'de': 'de', 'fr': 'fr', 'es': 'es', 'pt': 'pt', 'id': 'id'}
        return lang_map.get(m.group(1), 'en')
    tool_path = filepath.replace('\\', '/').split('/tools/')[-1] if '/tools/' in filepath.replace('\\', '/') else ''
    if tool_path and '/' not in tool_path:
        return 'zh-TW'
    return 'en'


def fix_tool_pages(frontend_dir):
    tools_dir = os.path.join(frontend_dir, 'tools')
    if not os.path.isdir(tools_dir):
        print(f"  X tools dir not found: {tools_dir}")
        return 0

    html_files = []
    for root, dirs, files in os.walk(tools_dir):
        for f in files:
            if f.endswith('.html') and f != 'index.html':
                html_files.append(os.path.join(root, f))

    fixed = 0
    already = 0

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except Exception:
            continue

        if 'linear-gradient(135deg,#667eea' in content:
            already += 1
            continue

        lang = detect_lang(filepath, content)
        banner = get_lottery_banner_html(lang)
        modified = False

        # 策略 1：ad-calc 後面
        if not modified and 'id="ad-calc"' in content:
            m = re.search(r'(<div[^>]*id=["\']ad-calc["\'][^>]*>.*?</div>)', content, re.DOTALL)
            if m:
                pos = m.end()
                content = content[:pos] + '\n' + banner + '\n' + content[pos:]
                modified = True

        # 策略 2：<article 前面
        if not modified and '<article' in content:
            idx = content.find('<article')
            if idx > 0:
                content = content[:idx] + banner + '\n' + content[idx:]
                modified = True

        # 策略 3：FAQ 前面
        if not modified:
            for marker in ['class="faq"', 'class="article"']:
                idx = content.find(marker)
                if idx > 0:
                    tag_start = content.rfind('<', 0, idx)
                    if tag_start > 0:
                        content = content[:tag_start] + banner + '\n' + content[tag_start:]
                        modified = True
                        break

        # 移除底部舊彩票連結（不在新 banner 裡的）
        old_link_pattern = r'<a[^>]*href=["\']https?://lottery\.softglow-ai\.com[^"\']*["\'][^>]*>.*?</a>'
        for m in reversed(list(re.finditer(old_link_pattern, content, re.DOTALL))):
            # 檢查是否在新 banner 裡
            before = content[max(0, m.start()-200):m.start()]
            if 'linear-gradient' not in before:
                content = content[:m.start()] + content[m.end():]

        if modified:
            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            fixed += 1

    print(f"\n  [Tools] added banner: {fixed}, already had: {already}, total scanned: {len(html_files)}")
    return fixed


def fix_homepage(frontend_dir):
    homepage = os.path.join(frontend_dir, 'homepage.html')
    if not os.path.isfile(homepage):
        print(f"  X homepage.html not found in {frontend_dir}")
        return False

    with open(homepage, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # ── 1. K棒型態語言 3 -> 10 ──
    m = re.search(
        r'(<a[^>]*patterns/en\.html[^>]*>English</a>.*?한국어</a>)',
        content, re.DOTALL
    )
    if m:
        new_langs = (
            '<a href="/patterns/en.html" style="color:#2563EB">English</a> '
            '<a href="/patterns/ja.html" style="color:#2563EB">日本語</a> '
            '<a href="/patterns/ko.html" style="color:#2563EB">한국어</a> '
            '<a href="/patterns/de.html" style="color:#2563EB">Deutsch</a> '
            '<a href="/patterns/fr.html" style="color:#2563EB">Français</a> '
            '<a href="/patterns/es.html" style="color:#2563EB">Español</a> '
            '<a href="/patterns/pt.html" style="color:#2563EB">Português</a> '
            '<a href="/patterns/id.html" style="color:#2563EB">Indonesia</a> '
            '<a href="/patterns/zh-CN.html" style="color:#2563EB">简体中文</a>'
        )
        content = content[:m.start()] + new_langs + content[m.end():]
        changes += 1
        print("  [Homepage] K-bar langs: 3 -> 10")
    else:
        print("  [Homepage] K-bar langs: pattern not found, may already be 10")

    # ── 2. 彩票醒目橫幅（計算工具分類上方）──
    if 'linear-gradient(135deg,#667eea' in content and '15' in content:
        print("  [Homepage] Lottery banner: already exists")
    else:
        lottery_banner = (
            '<!-- Lottery Banner -->\n'
            '<div style="max-width:1080px;margin:0 auto 40px;padding:0 20px">\n'
            '<a href="https://lottery.softglow-ai.com/zh-TW/" target="_blank" rel="noopener" '
            'style="text-decoration:none;display:block;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);'
            'border-radius:16px;padding:28px 32px;color:#fff;transition:transform 0.2s,box-shadow 0.2s">\n'
            '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px">\n'
            '<div>\n'
            '<div style="font-size:22px;font-weight:700;margin-bottom:6px">🎰 全球 15 國彩票開獎 ＋ 12 種智慧選號工具</div>\n'
            '<div style="font-size:14px;opacity:0.9">威力彩・大樂透・Powerball・Mega Millions・EuroMillions — 星座、生日、夢境、AI、八字、生肖等選號方式</div>\n'
            '</div>\n'
            '<div style="background:rgba(255,255,255,0.2);padding:10px 24px;border-radius:8px;font-weight:600;font-size:15px;white-space:nowrap">查看開獎 →</div>\n'
            '</div>\n'
            '</a>\n'
            '</div>\n'
        )

        # 插在「計算工具分類」之前
        idx = content.find('計算工具分類')
        if idx > 0:
            # 往前找到 section 開頭
            search_area = content[max(0, idx-500):idx]
            candidates = [search_area.rfind('<section'), search_area.rfind('<div class="container"')]
            best = max(c for c in candidates if c >= 0) if any(c >= 0 for c in candidates) else -1
            if best >= 0:
                actual = max(0, idx - 500) + best
                content = content[:actual] + lottery_banner + content[actual:]
                changes += 1
                print("  [Homepage] Lottery banner: inserted above tool categories")
            else:
                # fallback: 在計算工具分類的 h2 前面
                h2_idx = content.rfind('<h2', 0, idx)
                if h2_idx > 0:
                    content = content[:h2_idx] + lottery_banner + content[h2_idx:]
                    changes += 1
                    print("  [Homepage] Lottery banner: inserted before h2")
                else:
                    print("  [Homepage] Lottery banner: could not find insert point")
        else:
            print("  [Homepage] Lottery banner: marker not found")

    if changes > 0:
        with open(homepage, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [Homepage] saved ({changes} changes)")
    return changes > 0


def fix_landing(frontend_dir):
    landing = os.path.join(frontend_dir, 'landing.html')
    if not os.path.isfile(landing):
        print(f"  X landing.html not found")
        return False

    with open(landing, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # Title 改寫
    old_title = '<title>台股 AI 分析｜多空雷達 × K棒型態 × 支撐壓力，一鍵出報告</title>'
    new_title = '<title>這支股票能買嗎？輸入代號 30 秒看支撐壓力｜線上有位</title>'

    if old_title in content:
        content = content.replace(old_title, new_title)
        changes += 1
        print("  [Landing] Title rewritten")
    else:
        # 嘗試 regex
        m = re.search(r'<title>.*?</title>', content)
        if m:
            current = m.group(0)
            print(f"  [Landing] Title already different: {current}")
        else:
            print("  [Landing] No title tag found")

    # meta description 確認（已經改過的就不動）
    old_desc = '輸入股票代號，AI 分析多空雷達四格訊號、K棒型態辨識、支撐壓力位、葛蘭碧買點。免費產出完整報告。還有 500+ 計算工具和全球彩票選號。'
    new_desc = '輸入台股代號，30 秒看支撐壓力、多空雷達、K棒型態、損益比。免費完整報告＋每日 AI 精選股。還有 500+ 計算工具和全球彩票選號。'

    if old_desc in content:
        content = content.replace(old_desc, new_desc)
        changes += 1
        print("  [Landing] Meta description updated")

    if changes > 0:
        with open(landing, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [Landing] saved ({changes} changes)")
    return changes > 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--frontend-dir', default=None)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if args.frontend_dir:
        frontend_dir = args.frontend_dir
    else:
        candidates = [
            os.path.join(os.getcwd(), 'backend', 'frontend'),
            os.path.join(os.getcwd(), 'frontend'),
            os.path.join(os.getcwd()),
        ]
        frontend_dir = None
        for c in candidates:
            if os.path.isdir(os.path.join(c, 'tools')):
                frontend_dir = c
                break
        if not frontend_dir:
            print("X Cannot find frontend dir (needs tools/ subfolder)")
            print("  Run from D:\\xian-shang-you-wei or use --frontend-dir")
            sys.exit(1)

    print(f"Frontend dir: {frontend_dir}")
    print("=" * 50)

    if args.dry_run:
        tools_dir = os.path.join(frontend_dir, 'tools')
        count = sum(1 for r, d, fs in os.walk(tools_dir) for f in fs if f.endswith('.html') and f != 'index.html')
        print(f"\n[DRY RUN] Would process:")
        print(f"  Tool pages: {count}")
        print(f"  homepage.html: {os.path.isfile(os.path.join(frontend_dir, 'homepage.html'))}")
        print(f"  landing.html:  {os.path.isfile(os.path.join(frontend_dir, 'landing.html'))}")
        return

    print("\n--- Fix 1: Landing Title ---")
    fix_landing(frontend_dir)

    print("\n--- Fix 2: Homepage ---")
    fix_homepage(frontend_dir)

    print("\n--- Fix 3: Tool Pages ---")
    fix_tool_pages(frontend_dir)

    print("\n" + "=" * 50)
    print("Done! Next steps:")
    print("  1. Open homepage.html in browser, check lottery banner + K-bar 10 langs")
    print("  2. Open any tool page, check lottery banner after calculator")
    print("  3. git add -A && git commit -m 'fix: lottery links + landing title + 10 lang patterns' && git push")


if __name__ == '__main__':
    main()
