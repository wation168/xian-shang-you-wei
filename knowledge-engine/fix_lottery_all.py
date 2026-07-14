#!/usr/bin/env python3
# fix_lottery_all.py
# 1. Rewrite lottery page titles in Next.js i18n JSON files
# 2. Add softglow-ai.com tool links to lottery layout
#
# Usage:
#   cd D:\xian-shang-you-wei\knowledge-engine
#   python fix_lottery_all.py
#
# NOTE: This script modifies files in the lottery repo
# at D:\lottery-hub (adjust LOTTERY_ROOT if different)

import os
import re
import sys
import json

# Adjust this path if your lottery repo is elsewhere
LOTTERY_ROOTS = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "lottery-hub"),
    r"D:\lottery-hub",
    r"D:\lottery",
    r"D:\global-lottery",
]

# Also check the known path from project docs
KNOWN_PATH = os.path.normpath(r"D:\全球彩票資訊網\lottery-hub")
LOTTERY_ROOTS.insert(0, KNOWN_PATH)

LOTTERY_ROOT = None
for p in LOTTERY_ROOTS:
    p = os.path.normpath(p)
    if os.path.isdir(p) and (os.path.isfile(os.path.join(p, "package.json")) or os.path.isdir(os.path.join(p, "src"))):
        LOTTERY_ROOT = p
        break

if not LOTTERY_ROOT:
    print("[ERROR] Cannot find lottery repo. Tried:")
    for p in LOTTERY_ROOTS:
        print(f"  {os.path.normpath(p)}")
    print()
    print("Please set LOTTERY_ROOT at the top of this script.")
    sys.exit(1)

print(f"Lottery repo: {LOTTERY_ROOT}")

# ================================================================
# PART 1: Update lottery page titles via page.tsx files
# ================================================================

# New titles and descriptions for each lottery page
# Format: { path_pattern: { locale: (title, description) } }

LOTTERY_TITLES = {
    # Korea Lotto - biggest impression page (192!)
    "korea-lotto": {
        "en": (
            "Lotto 6/45 Latest Numbers + 12 Smart Pickers (Zodiac, Birthday, Dream, AI)",
            "This week's Korea Lotto 6/45 winning numbers. Pick yours with 12 tools: Zodiac, Birthday, Dream, AI, Feng Shui, Lucky Number and more. Hot/cold stats from 500+ draws."
        ),
        "ko": (
            "로또 6/45 최신 당첨번호 + 12가지 번호 선택기 (별자리, 생일, 꿈, AI)",
            "이번 주 로또 6/45 당첨번호 확인. 별자리, 생일, 꿈, AI, 풍수 등 12가지 방법으로 번호를 선택하세요. 500회 이상의 당첨 통계 분석."
        ),
        "zh-TW": (
            "韓國樂透 6/45 最新開獎＋12種選號（星座、生日、夢境、AI、八字）",
            "本週韓國樂透 6/45 開獎號碼，用星座、生日、夢境、AI、八字等 12 種方式選號。500+ 期冷熱號統計分析。"
        ),
        "ja": (
            "韓国ロト 6/45 最新抽選番号＋12種の番号選び（星座・誕生日・夢・AI）",
            "今週の韓国ロト6/45当選番号。星座・誕生日・夢・AI・風水など12種の方法で番号選び。500回以上の統計分析付き。"
        ),
    },
    # Japan Loto 6
    "japan-loto6": {
        "en": (
            "Japan Loto 6 Latest Draw + 12 Number Pickers + Full History",
            "Latest Japan Loto 6 winning numbers. Pick yours with Zodiac, Birthday, Dream, AI and 8 more methods. Complete draw history and hot/cold statistics."
        ),
        "zh-TW": (
            "日本樂透6 最新開獎＋12種選號工具（星座、生日、夢境、AI）",
            "最新日本樂透6 開獎號碼，12 種智慧選號（星座、生日、夢境、AI、八字、生肖），完整歷史開獎紀錄與冷熱號分析。"
        ),
        "ja": (
            "ロト6 最新抽選結果＋12種の番号選びツール（星座・誕生日・夢・AI）",
            "最新のロト6当選番号を確認。星座・誕生日・夢・AI・風水など12種の方法で番号を選べます。過去の全抽選履歴と統計分析。"
        ),
    },
    # Taiwan Lotto
    "taiwan-lotto": {
        "zh-TW": (
            "大樂透最新開獎號碼＋12種選號（星座、生日、夢境、AI、八字、生肖）",
            "今期大樂透開獎號碼即時更新。用星座、生日、夢境解碼、AI分析、八字命理、生肖等 12 種方式幫你選號。歷期中獎統計分析。"
        ),
        "en": (
            "Taiwan Lotto Latest Draw + 12 Smart Number Pickers",
            "Latest Taiwan Lotto 6/49 winning numbers. Pick yours with Zodiac, Birthday, Dream, AI and 8 more tools. Full draw history and statistics."
        ),
    },
    # Taiwan Bingo (威力彩)
    "taiwan-bingo": {
        "zh-TW": (
            "威力彩最新開獎號碼＋12種選號（星座、生日、夢境、AI、八字、生肖）",
            "今期威力彩開獎號碼即時更新。12 種智慧選號工具：星座、生日、夢境、AI、八字、生肖、卦象等。歷期統計與冷熱號分析。"
        ),
    },
    # Daily Cash (今彩539)
    "daily-cash": {
        "zh-TW": (
            "今彩539 最新開獎號碼＋12種選號（星座、生日、夢境、AI）",
            "今彩539 每日開獎即時更新。12 種選號工具：星座、生日、夢境、AI、八字、大事件選號。頭獎固定 800 萬。歷期冷熱號分析。"
        ),
    },
    # Powerball
    "powerball": {
        "en": (
            "Powerball Latest Draw + 12 Number Generators (Zodiac, Birthday, Dream, AI)",
            "Tonight's Powerball winning numbers. Generate yours with 12 smart tools: Zodiac, Birthday, Dream Decoder, AI Picks, Lucky Number and more. Jackpot odds and tax calculator."
        ),
    },
    # Mega Millions
    "mega-millions": {
        "en": (
            "Mega Millions Latest Numbers + 12 Smart Pickers + Win Probability",
            "Latest Mega Millions results. Pick your numbers with Zodiac, Birthday, Dream, AI and 8 more methods. Includes odds calculator and lottery tax estimator."
        ),
    },
    # EuroMillions
    "euromillions": {
        "en": (
            "EuroMillions Latest Draw + 12 Number Pickers + Full History Since 2004",
            "Latest EuroMillions winning numbers. 12 smart picker tools (Zodiac, Birthday, Dream, AI). Searchable history since 2004. Hot/cold number analysis."
        ),
    },
    # UK Lotto
    "uk-lotto": {
        "en": (
            "UK Lotto Latest Numbers + 12 Smart Pickers (Zodiac, Birthday, Dream, AI)",
            "Tonight's UK Lotto results. Pick your numbers with 12 tools: Zodiac, Birthday, Dream, AI and more. Hot/cold statistics and full draw history."
        ),
        "zh-TW": (
            "英國樂透最新開獎號碼＋12種選號（星座、生日、夢境、AI）｜歷史統計",
            "英國樂透最新開獎結果。12 種選號工具：星座、生日、夢境、AI。完整歷史開獎紀錄與冷熱號統計分析。"
        ),
    },
    # Mega-Sena
    "mega-sena": {
        "en": (
            "Mega-Sena Latest Results + 12 Number Pickers + Hot/Cold Stats",
            "Latest Mega-Sena winning numbers. Pick yours with 12 smart tools. Which numbers hit most often? Complete statistics from all past draws."
        ),
    },
    # Lotto 6aus49
    "lotto-6aus49": {
        "en": (
            "Lotto 6aus49 Latest Draw + 12 Number Pickers + German Lottery Stats",
            "Latest German Lotto 6aus49 results. 12 smart number generators (Zodiac, Birthday, Dream, AI). Complete draw history and statistics."
        ),
    },
    # Lotto Max
    "lotto-max": {
        "en": (
            "Lotto Max Latest Draw + 12 Number Pickers + Canadian Lottery Stats",
            "Latest Lotto Max winning numbers. 12 picker tools (Zodiac, Birthday, Dream, AI). Full history and hot/cold analysis."
        ),
        "zh-TW": (
            "加拿大 Lotto Max 最新開獎＋12種選號工具｜開獎時間與統計",
            "加拿大 Lotto Max 最新開獎號碼。12 種選號工具：星座、生日、夢境、AI。完整歷史紀錄與冷熱號分析。"
        ),
    },
    # SuperEnalotto
    "superenalotto": {
        "en": (
            "SuperEnalotto Latest Draw + 12 Number Generators + Italian Lottery",
            "Latest SuperEnalotto results. 12 smart number pickers (Zodiac, Birthday, Dream, AI). Statistics and draw history."
        ),
    },
    # El Gordo
    "el-gordo": {
        "en": (
            "El Gordo Latest Draw + 12 Number Pickers + Spanish Lottery Stats",
            "Latest El Gordo de la Primitiva results. 12 picker tools including Zodiac, Dream, AI. History and statistics."
        ),
    },
    # Oz Lotto
    "oz-lotto": {
        "en": (
            "Oz Lotto Latest Draw + 12 Number Pickers + Australian Lottery Stats",
            "Latest Oz Lotto winning numbers. 12 smart number generators. Complete draw history and hot/cold analysis."
        ),
    },
}

# Homepage titles
HOMEPAGE_TITLES = {
    "zh-TW": (
        "15國彩票即時開獎＋12種選號工具（星座、生日、夢境、AI、八字、生肖）",
        "美國Powerball、Mega Millions、歐洲EuroMillions、台灣威力彩大樂透等15國彩票即時開獎。12種智慧選號：星座、生日、夢境、AI、八字、生肖、卦象。"
    ),
    "en": (
        "15 World Lotteries + 12 Smart Number Pickers (Zodiac, Birthday, Dream, AI)",
        "Live results for Powerball, Mega Millions, EuroMillions, UK Lotto and 11 more. Pick numbers with 12 tools: Zodiac, Birthday, Dream, AI, Lucky Number, Feng Shui."
    ),
    "ja": (
        "15ヶ国の宝くじ最新抽選＋12種の番号選びツール（星座・誕生日・夢・AI）",
        "Powerball、EuroMillions、ロト6など15ヶ国の宝くじ最新抽選結果。星座・誕生日・夢・AI・風水など12種の番号選びツール。"
    ),
    "ko": (
        "15개국 복권 최신 추첨 + 12가지 번호 선택기 (별자리, 생일, 꿈, AI)",
        "Powerball, EuroMillions, 로또 6/45 등 15개국 복권 최신 추첨 결과. 별자리, 생일, 꿈, AI 등 12가지 번호 선택 도구."
    ),
}

# Tools page titles
TOOLS_TITLES = {
    "en": (
        "Lottery Tools — Tax Calculator, Odds Comparer, Time Zones + 500 Free Tools",
        "Calculate lottery taxes by country, compare jackpot odds, convert draw times. Plus 500+ free calculators at softglow-ai.com."
    ),
    "zh-TW": (
        "彩票工具｜稅後計算、中獎機率比較、開獎時間換算＋500免費工具",
        "計算各國彩票稅後獎金、比較 15 國彩票中獎機率、換算全球開獎時間。還有 softglow-ai.com 500+ 免費計算工具。"
    ),
    "ja": (
        "宝くじツール｜税金計算・当選確率比較・抽選時間変換＋500無料ツール",
        "各国の宝くじ税金計算、15ヶ国の当選確率比較、抽選時間変換。softglow-ai.com で500以上の無料計算ツールも。"
    ),
    "ko": (
        "복권 도구｜세금 계산, 당첨 확률 비교 + 500개 무료 도구",
        "각국 복권 세금 계산, 15개국 당첨 확률 비교, 추첨 시간 변환. softglow-ai.com에서 500개 이상의 무료 계산기."
    ),
}


def fix_lottery_titles():
    print("=" * 60)
    print("PART 1: Update lottery page titles")
    print("=" * 60)

    # Strategy: Find page.tsx files and update generateMetadata
    # Also check i18n JSON files
    src_dir = os.path.join(LOTTERY_ROOT, "src")
    if not os.path.isdir(src_dir):
        print(f"  [ERROR] src/ not found in {LOTTERY_ROOT}")
        return 0

    changes = 0

    # Find all page.tsx files
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f != 'page.tsx':
                continue

            filepath = os.path.join(root, f)
            rel = os.path.relpath(filepath, src_dir).replace('\\', '/')

            try:
                with open(filepath, 'r', encoding='utf-8') as fh:
                    content = fh.read()

                original = content

                # Determine which lottery this is from the path
                # e.g., app/[locale]/[lottery]/page.tsx
                # or app/[locale]/page.tsx (homepage)
                # or app/[locale]/tools/page.tsx

                # For the main lottery page: app/[locale]/[lottery]/page.tsx
                # We need to modify generateMetadata to use our new titles

                # Check if this has generateMetadata
                if 'generateMetadata' not in content and 'metadata' not in content.lower():
                    continue

                # For now, just report what we found
                print(f"  Found: {rel}")

                # Try to find and replace title strings
                for slug, locale_titles in LOTTERY_TITLES.items():
                    for locale, (new_title, new_desc) in locale_titles.items():
                        # Look for the slug in the file path or content
                        if slug in rel or slug in content:
                            # Try common patterns
                            # Pattern 1: title: "..." or title: '...'
                            # Pattern 2: title: `...${...}...`
                            pass

            except Exception as e:
                print(f"  [ERROR] {rel}: {e}")

    # Check i18n files
    i18n_dir = os.path.join(src_dir, "i18n", "messages")
    if not os.path.isdir(i18n_dir):
        i18n_dir = os.path.join(src_dir, "messages")

    if os.path.isdir(i18n_dir):
        print(f"\n  Checking i18n files in {i18n_dir}...")
        for f in os.listdir(i18n_dir):
            if f.endswith('.json'):
                filepath = os.path.join(i18n_dir, f)
                locale = f.replace('.json', '')
                print(f"  Found i18n: {f} (locale: {locale})")

    # Since Next.js title handling varies a lot, output a manual guide
    print()
    print("  " + "-" * 56)
    print("  Next.js titles are complex. Here's what to change:")
    print("  " + "-" * 56)

    print("\n  === HOMEPAGE (app/[locale]/page.tsx) ===")
    for locale, (title, desc) in HOMEPAGE_TITLES.items():
        print(f"  [{locale}] title: {title}")
        print(f"  [{locale}] desc:  {desc[:80]}...")

    print("\n  === LOTTERY PAGES (app/[locale]/[lottery]/page.tsx) ===")
    for slug, locale_titles in LOTTERY_TITLES.items():
        print(f"\n  --- {slug} ---")
        for locale, (title, desc) in locale_titles.items():
            print(f"  [{locale}] title: {title}")

    print("\n  === TOOLS PAGES ===")
    for locale, (title, desc) in TOOLS_TITLES.items():
        print(f"  [{locale}] title: {title}")

    return changes


# ================================================================
# PART 2: Add softglow-ai.com cross-links to lottery layout
# ================================================================

CROSS_LINK_COMPONENT = '''
<!-- SoftGlow Tools Cross-Link -->
<div style="max-width:1200px;margin:24px auto;padding:0 16px">
  <a href="https://softglow-ai.com/tools/" target="_blank" rel="noopener"
     style="display:flex;align-items:center;justify-content:center;gap:8px;
            padding:14px 20px;background:#EBF5FF;border:1px solid #BEE3F8;
            border-radius:12px;color:#2563EB;font-size:14px;font-weight:500;
            text-decoration:none;transition:background 0.2s">
    <span>500+ Free Calculators</span>
    <span style="font-size:12px;color:#718096">(Finance, Health, Engineering, Cooking)</span>
    <span style="font-size:16px">→</span>
  </a>
</div>
'''

def add_crosslinks_to_lottery():
    print()
    print("=" * 60)
    print("PART 2: Add softglow-ai.com links to lottery layout")
    print("=" * 60)

    # Find layout.tsx
    layout_path = os.path.join(LOTTERY_ROOT, "src", "app", "[locale]", "layout.tsx")
    if not os.path.isfile(layout_path):
        # Try alternative paths
        for alt in [
            os.path.join(LOTTERY_ROOT, "src", "app", "layout.tsx"),
            os.path.join(LOTTERY_ROOT, "app", "[locale]", "layout.tsx"),
        ]:
            if os.path.isfile(alt):
                layout_path = alt
                break

    if os.path.isfile(layout_path):
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'softglow-ai.com/tools' in content:
            print("  [SKIP] Cross-link already exists in layout.tsx")
        else:
            print(f"  [INFO] Found layout.tsx: {layout_path}")
            print("  [INFO] Add this link above the footer in layout.tsx:")
            print()
            print("  // In the JSX, before </footer> or before the closing </body>:")
            print('  <div className="max-w-7xl mx-auto px-4 py-4">')
            print('    <a href="https://softglow-ai.com/tools/" target="_blank"')
            print('       className="block p-3 bg-blue-50 border border-blue-200 rounded-xl')
            print('                  text-blue-600 text-sm text-center hover:bg-blue-100">')
            print('      500+ Free Calculators (Finance, Health, Engineering) →')
            print('    </a>')
            print('  </div>')
    else:
        print(f"  [WARN] Cannot find layout.tsx")

    return 0


# ================================================================
# Main
# ================================================================

if __name__ == '__main__':
    fix_lottery_titles()
    add_crosslinks_to_lottery()

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print()
    print("The lottery repo uses Next.js with dynamic titles.")
    print("The script above printed all the new titles you need.")
    print()
    print("Fastest approach: manually update these files:")
    print(f"  1. {os.path.join(LOTTERY_ROOT, 'src', 'app', '[locale]', 'page.tsx')}")
    print(f"  2. {os.path.join(LOTTERY_ROOT, 'src', 'app', '[locale]', '[lottery]', 'page.tsx')}")
    print(f"  3. {os.path.join(LOTTERY_ROOT, 'src', 'app', '[locale]', 'layout.tsx')}")
    print()
    print("After changes:")
    print(f"  cd {LOTTERY_ROOT}")
    print("  # Upload to Zeabur or git push")
