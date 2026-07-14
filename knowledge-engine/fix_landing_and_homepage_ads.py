#!/usr/bin/env python3
# fix_landing_and_homepage_ads.py
# 1. Landing: 暗色 -> 白底 + 移除邀請 + 加快捷連結 + Title
# 2. Homepage: 加 5 個 AdSense 廣告位
#
# cd D:\xian-shang-you-wei
# python knowledge-engine\fix_landing_and_homepage_ads.py

import os, sys, re

frontend_dir = None
for c in [
    os.path.join(os.getcwd(), 'backend', 'frontend'),
    os.path.join(os.getcwd(), 'frontend'),
]:
    if os.path.isdir(os.path.join(c, 'tools')):
        frontend_dir = c
        break
if not frontend_dir:
    print("X Run from D:\\xian-shang-you-wei")
    sys.exit(1)

print(f"Frontend: {frontend_dir}")
print("=" * 50)

# ═══════════════════════════════════════════════════
# PART 1: Landing.html - Full Light Theme Conversion
# ═══════════════════════════════════════════════════
landing_path = os.path.join(frontend_dir, 'landing.html')
if os.path.isfile(landing_path):
    print("\n--- Landing.html ---")
    with open(landing_path, 'r', encoding='utf-8') as f:
        lc = f.read()
    lchanges = 0

    # ── 1A. Title + Description (from previous fix) ──
    old_t = '<title>台股 AI 分析｜多空雷達 × K棒型態 × 支撐壓力，一鍵出報告</title>'
    new_t = '<title>這支股票能買嗎？輸入代號 30 秒看支撐壓力｜線上有位</title>'
    if old_t in lc:
        lc = lc.replace(old_t, new_t)
        lchanges += 1
        print("  Title rewritten")

    old_d = '輸入股票代號，AI 分析多空雷達四格訊號、K棒型態辨識、支撐壓力位、葛蘭碧買點。免費產出完整報告。還有 500+ 計算工具和全球彩票選號。'
    new_d = '輸入台股代號，30 秒看支撐壓力、多空雷達、K棒型態、損益比。免費完整報告＋每日 AI 精選股。還有 500+ 計算工具和全球彩票選號。'
    if old_d in lc:
        lc = lc.replace(old_d, new_d)
        lchanges += 1
        print("  Description updated")

    # ── 1B. CSS Variables: Dark → Light ──
    css_replacements = [
        # Root variables
        ('--bg:#0a0a12', '--bg:#ffffff'),
        ('--bg2:#12121f', '--bg2:#f7fafc'),
        ('--bg3:#1a1a2e', '--bg3:#edf2f7'),
        ('--card:#16162a', '--card:#ffffff'),
        ('--border:rgba(255,255,255,.08)', '--border:rgba(0,0,0,.08)'),
        ('--text:#f0eeff', '--text:#1a202c'),
        ('--text2:#a89fc0', '--text2:#4a5568'),
        ('--text3:#5a5470', '--text3:#a0aec0'),
        ('--green:#00e5a0', '--green:#059669'),
        ('--green-d:#00b87f', '--green-d:#047857'),
        ('--green-glow:rgba(0,229,160,.15)', '--green-glow:rgba(5,150,105,.12)'),
    ]
    for old, new in css_replacements:
        if old in lc:
            lc = lc.replace(old, new)
            lchanges += 1

    # ── 1C. Nav background ──
    lc = lc.replace(
        'background:rgba(10,10,18,.92);backdrop-filter:blur(16px)',
        'background:rgba(255,255,255,.95);backdrop-filter:blur(16px)'
    )
    # Nav CTA button
    lc = lc.replace(
        '.nav-cta{background:var(--green);color:#000;',
        '.nav-cta{background:#2563EB;color:#fff;'
    )
    lc = lc.replace(
        '.nav-cta:hover{background:var(--green-d)',
        '.nav-cta:hover{background:#1d4ed8'
    )

    # ── 1D. Hero section ──
    # Hero background gradient
    lc = lc.replace(
        'background:radial-gradient(ellipse 70% 50% at 50% 0%, rgba(168,85,247,.18) 0%, transparent 60%), radial-gradient(ellipse 50% 40% at 80% 60%, rgba(0,229,160,.1) 0%, transparent 50%), radial-gradient(ellipse 40% 40% at 20% 80%, rgba(59,130,246,.1) 0%, transparent 50%)',
        'background:radial-gradient(ellipse 70% 50% at 50% 0%, rgba(37,99,235,.06) 0%, transparent 60%), radial-gradient(ellipse 50% 40% at 80% 60%, rgba(5,150,105,.04) 0%, transparent 50%)'
    )
    # Hero badge
    lc = lc.replace(
        'background:rgba(168,85,247,.15);color:var(--purple);border:1px solid rgba(168,85,247,.3)',
        'background:rgba(37,99,235,.08);color:#2563EB;border:1px solid rgba(37,99,235,.2)'
    )
    # Hero h1 green accent
    lc = lc.replace('.hero h1 .g{color:var(--green)}', '.hero h1 .g{color:#2563EB}')
    # Primary button
    lc = lc.replace(
        '.btn-primary{background:linear-gradient(135deg,var(--green),#00b8d4);color:#000;',
        '.btn-primary{background:#2563EB;color:#fff;'
    )
    lc = lc.replace(
        'box-shadow:0 4px 24px rgba(0,229,160,.35)',
        'box-shadow:0 4px 24px rgba(37,99,235,.25)'
    )
    lc = lc.replace(
        'box-shadow:0 8px 32px rgba(0,229,160,.45)',
        'box-shadow:0 8px 32px rgba(37,99,235,.35)'
    )
    # Secondary button
    lc = lc.replace(
        '.btn-secondary{background:rgba(255,255,255,.06);color:var(--text);border:1px solid var(--border)',
        '.btn-secondary{background:#fff;color:#1a202c;border:1px solid #e2e8f0'
    )
    lc = lc.replace(
        '.btn-secondary:hover{border-color:rgba(255,255,255,.25);background:rgba(255,255,255,.1)}',
        '.btn-secondary:hover{border-color:#2563EB;background:#f0f7ff}'
    )
    # Hero stat numbers
    lc = lc.replace('.hero-stat-num{font-size:32px;font-weight:900;color:var(--green)}',
                     '.hero-stat-num{font-size:32px;font-weight:900;color:#2563EB}')
    # Cost callout in hero
    lc = lc.replace(
        'background:rgba(248,113,113,.12);border:1px solid rgba(248,113,113,.25)',
        'background:rgba(37,99,235,.06);border:1px solid rgba(37,99,235,.15)'
    )
    lc = lc.replace('color:#fca5a5;', 'color:#4a5568;')
    lc = lc.replace('color:#f87171"', 'color:#2563EB"')

    # ── 1E. Pain section ──
    lc = lc.replace(
        '.pain{background:linear-gradient(135deg,#1a0a2e 0%,#0a0a18 100%)}',
        '.pain{background:#f7fafc}'
    )
    lc = lc.replace(
        '.pain-card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07)',
        '.pain-card{background:#fff;border:1px solid #e2e8f0'
    )

    # ── 1F. Feature cards ──
    lc = lc.replace(
        '.feature-card{background:var(--card);border:1px solid var(--border)',
        '.feature-card{background:#fff;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,.06)'
    )
    lc = lc.replace(
        '.feature-card:hover{transform:translateY(-5px);border-color:rgba(168,85,247,.3)}',
        '.feature-card:hover{transform:translateY(-5px);border-color:#2563EB;box-shadow:0 4px 12px rgba(37,99,235,.12)}'
    )

    # ── 1G. Steps ──
    lc = lc.replace(
        'background:linear-gradient(90deg,transparent,rgba(168,85,247,.3),rgba(0,229,160,.3),transparent)',
        'background:linear-gradient(90deg,transparent,rgba(37,99,235,.2),rgba(37,99,235,.2),transparent)'
    )
    lc = lc.replace(
        '.step-num{width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,rgba(168,85,247,.2),rgba(0,229,160,.2));border:1px solid rgba(255,255,255,.12)',
        '.step-num{width:56px;height:56px;border-radius:50%;background:rgba(37,99,235,.08);border:1px solid rgba(37,99,235,.15)'
    )

    # ── 1H. Mockup screens ──
    lc = lc.replace(
        '.mockup-screen{flex:1.2;min-width:300px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.4)}',
        '.mockup-screen{flex:1.2;min-width:300px;background:#fff;border:1px solid #e2e8f0;border-radius:var(--radius-lg);overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)}'
    )
    lc = lc.replace(
        '.mockup-topbar{background:rgba(255,255,255,.04);border-bottom:1px solid var(--border)',
        '.mockup-topbar{background:#f7fafc;border-bottom:1px solid #e2e8f0'
    )
    lc = lc.replace(
        '.mockup-url{flex:1;background:rgba(255,255,255,.06)',
        '.mockup-url{flex:1;background:#edf2f7'
    )
    # Mockup metrics
    lc = lc.replace(
        '.mk-metric{background:rgba(255,255,255,.04)',
        '.mk-metric{background:#f7fafc'
    )
    lc = lc.replace(
        '.mk-rr-bar{background:rgba(255,255,255,.06)',
        '.mk-rr-bar{background:#f7fafc'
    )
    # Chart areas
    lc = lc.replace('background:rgba(0,0,0,.2);border-radius:8px', 'background:#f0f4f8;border-radius:8px')
    lc = lc.replace('background:rgba(0,0,0,.15);border-radius:6px', 'background:#f0f4f8;border-radius:6px')
    # Conclusion box green
    lc = lc.replace('.mk-conclusion{background:rgba(0,229,160,.06);border-left:3px solid var(--green)',
                     '.mk-conclusion{background:rgba(5,150,105,.06);border-left:3px solid #059669')

    # ── 1I. Chat highlight ──
    lc = lc.replace(
        '.chat-highlight{background:linear-gradient(135deg,rgba(168,85,247,.08),rgba(236,72,153,.08));border:1px solid rgba(168,85,247,.2)',
        '.chat-highlight{background:linear-gradient(135deg,rgba(37,99,235,.04),rgba(168,85,247,.04));border:1px solid #e2e8f0'
    )
    lc = lc.replace(
        '.chat-highlight-preview{flex:1;min-width:260px;background:rgba(10,10,18,.7);border-radius:14px;border:1px solid rgba(168,85,247,.2)',
        '.chat-highlight-preview{flex:1;min-width:260px;background:#f7fafc;border-radius:14px;border:1px solid #e2e8f0'
    )
    lc = lc.replace('.cbd-other{background:rgba(30,12,56,.9);border:1px solid rgba(216,180,254,.15);color:#f0e6ff',
                     '.cbd-other{background:#edf2f7;border:1px solid #e2e8f0;color:#4a5568')
    lc = lc.replace('.cbd-me{background:linear-gradient(135deg,#be185d,#7c3aed);color:#fff',
                     '.cbd-me{background:#2563EB;color:#fff')

    # ── 1J. Pricing ──
    lc = lc.replace('.pricing{background:var(--bg2)}', '.pricing{background:#f7fafc}')
    lc = lc.replace('.price-card.featured{border-color:var(--green);box-shadow:0 0 40px rgba(0,229,160,.12)}',
                     '.price-card.featured{border-color:#2563EB;box-shadow:0 0 30px rgba(37,99,235,.1)}')
    lc = lc.replace('.price-badge{display:inline-block;font-size:11px;font-weight:700;background:var(--green);color:#000',
                     '.price-badge{display:inline-block;font-size:11px;font-weight:700;background:#2563EB;color:#fff')
    lc = lc.replace('.price-badge-free{background:var(--purple);color:#fff}',
                     '.price-badge-free{background:#7c3aed;color:#fff}')
    lc = lc.replace('.price-btn.primary{background:linear-gradient(135deg,var(--green),#00b8d4);color:#000}',
                     '.price-btn.primary{background:#2563EB;color:#fff}')
    lc = lc.replace('.price-btn.primary:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,229,160,.3)}',
                     '.price-btn.primary:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(37,99,235,.25)}')
    lc = lc.replace('.price-btn.secondary{background:rgba(255,255,255,.07);color:var(--text);border:1px solid var(--border)}',
                     '.price-btn.secondary{background:#fff;color:#1a202c;border:1px solid #e2e8f0}')
    lc = lc.replace('.price-btn.secondary:hover{background:rgba(255,255,255,.12)}',
                     '.price-btn.secondary:hover{background:#f0f7ff}')
    lc = lc.replace('.price-btn.free{background:linear-gradient(135deg,var(--purple),var(--pink));color:#fff}',
                     '.price-btn.free{background:#7c3aed;color:#fff}')

    # ── 1K. FAQ ──
    lc = lc.replace('.faq-item{background:var(--card);border:1px solid var(--border)',
                     '.faq-item{background:#fff;border:1px solid #e2e8f0')
    lc = lc.replace('.faq-q:hover{color:var(--green)}', '.faq-q:hover{color:#2563EB}')
    lc = lc.replace(".faq-q::after{content:'\\uff0b';font-size:18px;color:var(--text3)",
                     ".faq-q::after{content:'\\uff0b';font-size:18px;color:#a0aec0")
    lc = lc.replace(".faq-q.open::after{transform:rotate(45deg);color:var(--green)}",
                     ".faq-q.open::after{transform:rotate(45deg);color:#2563EB}")

    # ── 1L. CTA Final ──
    lc = lc.replace(
        '.cta-final{background:linear-gradient(135deg,#1a0a2e 0%,#0a1a2e 50%,#0a1a1a 100%)',
        '.cta-final{background:linear-gradient(135deg,#eef2ff 0%,#f0f7ff 50%,#f0fdf4 100%)'
    )
    lc = lc.replace(
        ".cta-final::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 60% at 50% 50%,rgba(0,229,160,.08) 0%,transparent 70%)}",
        ".cta-final::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 60% at 50% 50%,rgba(37,99,235,.04) 0%,transparent 70%)}"
    )

    # ── 1M. Ticker ──
    lc = lc.replace('.ticker-wrap{background:var(--bg2)', '.ticker-wrap{background:#f7fafc')

    # ── 1N. Misc rgba(255,255,255,...) → rgba(0,0,0,...) for light ──
    lc = lc.replace('rgba(255,255,255,.04)', 'rgba(0,0,0,.02)')
    lc = lc.replace('rgba(255,255,255,.06)', 'rgba(0,0,0,.03)')
    lc = lc.replace('rgba(255,255,255,.07)', 'rgba(0,0,0,.05)')
    lc = lc.replace('rgba(255,255,255,.05)', 'rgba(0,0,0,.04)')
    lc = lc.replace('rgba(255,255,255,.12)', 'rgba(0,0,0,.06)')
    lc = lc.replace('rgba(255,255,255,.25)', 'rgba(0,0,0,.12)')

    # Mockup specific color fixes for light
    lc = lc.replace('.mk-up{color:#4ade80}', '.mk-up{color:#059669}')

    # Radar section gradient
    lc = lc.replace(
        'background:linear-gradient(135deg,rgba(168,85,247,.08) 0%,rgba(59,130,246,.08) 100%);border-top:1px solid rgba(168,85,247,.2);border-bottom:1px solid rgba(168,85,247,.2)',
        'background:linear-gradient(135deg,rgba(37,99,235,.04) 0%,rgba(168,85,247,.04) 100%);border-top:1px solid #e2e8f0;border-bottom:1px solid #e2e8f0'
    )

    lchanges += 1
    print("  Theme: dark -> white (CSS vars + all sections)")

    # ── 2. 移除邀請方案 ──
    m = re.search(
        r'<div class="price-card reveal">\s*<div class="price-badge price-badge-free">.*?</div>\s*</div>',
        lc, re.DOTALL
    )
    if m:
        lc = lc[:m.start()] + lc[m.end():]
        lchanges += 1
        print("  Removed: invite price card")

    m = re.search(r'<!-- 邀請說明 -->.*?</section>', lc, re.DOTALL)
    if m:
        lc = lc[:m.start()] + lc[m.end():]
        lchanges += 1
        print("  Removed: invite explanation")

    m = re.search(
        r'<div class="faq-item reveal">\s*<div class="faq-q"[^>]*>.*?邀請.*?</div>\s*<div class="faq-a">.*?</div>\s*</div>',
        lc, re.DOTALL
    )
    if m:
        lc = lc[:m.start()] + lc[m.end():]
        lchanges += 1
        print("  Removed: invite FAQ")

    old_sub = '付款後立即開通帳號，或邀請 3 位好友免費解鎖 30 天'
    if old_sub in lc:
        lc = lc.replace(old_sub, '付款後立即開通帳號，手機電腦都能用')
        lchanges += 1
        print("  Updated: pricing subtitle")

    # ── 3. Quick links (light theme colors) ──
    LINKS_HTML = '''
  <!-- Quick Links -->
  <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:32px;padding:0 16px;animation:fadeUp .6s .4s ease both;opacity:0">
    <a href="/tools/" style="text-decoration:none;background:rgba(37,99,235,.06);border:1px solid rgba(37,99,235,.15);border-radius:12px;padding:14px 22px;display:flex;align-items:center;gap:8px;color:#2563EB;font-size:14px;font-weight:600;transition:all .2s" onmouseover="this.style.background='rgba(37,99,235,.12)'" onmouseout="this.style.background='rgba(37,99,235,.06)'">
      <span style="font-size:20px">🧮</span> 500+ 免費計算工具
    </a>
    <a href="/patterns/index.html" style="text-decoration:none;background:rgba(124,58,237,.06);border:1px solid rgba(124,58,237,.15);border-radius:12px;padding:14px 22px;display:flex;align-items:center;gap:8px;color:#7c3aed;font-size:14px;font-weight:600;transition:all .2s" onmouseover="this.style.background='rgba(124,58,237,.12)'" onmouseout="this.style.background='rgba(124,58,237,.06)'">
      <span style="font-size:20px">📊</span> 50 種 K 棒型態圖鑑
    </a>
    <a href="/blog/" style="text-decoration:none;background:rgba(5,150,105,.06);border:1px solid rgba(5,150,105,.15);border-radius:12px;padding:14px 22px;display:flex;align-items:center;gap:8px;color:#059669;font-size:14px;font-weight:600;transition:all .2s" onmouseover="this.style.background='rgba(5,150,105,.12)'" onmouseout="this.style.background='rgba(5,150,105,.06)'">
      <span style="font-size:20px">📚</span> 技術分析教學
    </a>
    <a href="https://lottery.softglow-ai.com/zh-TW/" target="_blank" rel="noopener" style="text-decoration:none;background:rgba(217,119,6,.06);border:1px solid rgba(217,119,6,.15);border-radius:12px;padding:14px 22px;display:flex;align-items:center;gap:8px;color:#d97706;font-size:14px;font-weight:600;transition:all .2s" onmouseover="this.style.background='rgba(217,119,6,.12)'" onmouseout="this.style.background='rgba(217,119,6,.06)'">
      <span style="font-size:20px">🎰</span> 全球彩票 + 選號工具
    </a>
  </div>'''

    if '500+ 免費計算工具' not in lc:
        idx = lc.find('涵蓋全台股支數')
        if idx > 0:
            section_end = lc.find('</section>', idx)
            if section_end > 0:
                lc = lc[:section_end] + LINKS_HTML + '\n' + lc[section_end:]
                lchanges += 1
                print("  Added: 4 quick links (light theme)")

    with open(landing_path, 'w', encoding='utf-8') as f:
        f.write(lc)
    print(f"  Saved ({lchanges} changes)")
else:
    print("  X landing.html not found")


# ═══════════════════════════════════════════════════
# PART 2: Homepage.html AdSense (5 slots)
# ═══════════════════════════════════════════════════
homepage_path = os.path.join(frontend_dir, 'homepage.html')
if not os.path.isfile(homepage_path):
    print("\n  X homepage.html not found")
    sys.exit(1)

print("\n--- Homepage.html (AdSense) ---")
with open(homepage_path, 'r', encoding='utf-8') as f:
    hc = f.read()
hchanges = 0

AD_BLOCK = '''<div style="max-width:1080px;margin:20px auto;padding:0 20px;text-align:center">
<ins class="adsbygoogle" style="display:block;min-width:280px;min-height:90px" data-ad-client="ca-pub-1768270548115739" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>try{(adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}</script>
</div>'''

AD_MARKERS = [
    ('🔥 熱門工具', 'ad before hot tools'),
    ('投資教學文章', 'ad before articles'),
    ('平台服務', 'ad before services'),
    ('K 線型態圖鑑', 'ad before K-bar'),
    ('關於 SoftGlow', 'ad before about'),
]

for marker_text, desc in AD_MARKERS:
    idx = hc.find(marker_text)
    if idx < 0:
        print(f"  X Marker not found: {marker_text}")
        continue
    search_back = hc[max(0, idx-500):idx]
    if 'adsbygoogle' in search_back:
        print(f"  Skip: {desc} (already has ad)")
        continue
    candidates = [search_back.rfind('<section'), search_back.rfind('<div style="max-width'), search_back.rfind('<h2')]
    best = max((c for c in candidates if c >= 0), default=-1)
    if best >= 0:
        actual = max(0, idx - 500) + best
        hc = hc[:actual] + AD_BLOCK + '\n\n' + hc[actual:]
        hchanges += 1
        print(f"  Added: {desc}")

if 'pagead2.googlesyndication.com' not in hc:
    hc = hc.replace('</body>',
        '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739" crossorigin="anonymous"></script>\n</body>')
    hchanges += 1
    print("  Added: AdSense script tag")

if hchanges > 0:
    with open(homepage_path, 'w', encoding='utf-8') as f:
        f.write(hc)
    print(f"  Saved ({hchanges} changes)")

print("\n" + "=" * 50)
print("Done!")
print("Next: git add -A && git commit -m 'landing white theme + homepage ads + remove invite' && git push")
