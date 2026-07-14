#!/usr/bin/env python3
# fix_landing_links.py
# 1. 移除邀請方案卡片 + 邀請說明區塊
# 2. Hero stats 下方加四個醒目連結（工具/教學/K棒/彩票）
#
# cd D:\xian-shang-you-wei
# python knowledge-engine\fix_landing_links.py

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

path = os.path.join(frontend_dir, 'landing.html')
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ── 1. 移除邀請方案卡片 ──
# 整個 price-card（限時免費 邀請方案）
old_invite_card = re.search(
    r'<div class="price-card reveal">\s*<div class="price-badge price-badge-free">.*?</div>\s*</div>',
    content, re.DOTALL
)
if old_invite_card:
    content = content[:old_invite_card.start()] + content[old_invite_card.end():]
    changes += 1
    print("  Removed: invite price card")

# ── 2. 移除邀請說明區塊 ──
old_invite_section = re.search(
    r'<!-- 邀請說明 -->.*?</section>',
    content, re.DOTALL
)
if old_invite_section:
    content = content[:old_invite_section.start()] + content[old_invite_section.end():]
    changes += 1
    print("  Removed: invite explanation section")

# ── 3. 移除 FAQ 裡邀請相關的問答 ──
invite_faq = re.search(
    r'<div class="faq-item reveal">\s*<div class="faq-q"[^>]*>.*?邀請.*?</div>\s*<div class="faq-a">.*?</div>\s*</div>',
    content, re.DOTALL
)
if invite_faq:
    content = content[:invite_faq.start()] + content[invite_faq.end():]
    changes += 1
    print("  Removed: invite FAQ item")

# ── 4. 移除方案副標裡的邀請文字 ──
old_sub = '付款後立即開通帳號，或邀請 3 位好友免費解鎖 30 天'
new_sub = '付款後立即開通帳號，手機電腦都能用'
if old_sub in content:
    content = content.replace(old_sub, new_sub)
    changes += 1
    print("  Updated: pricing subtitle")

# ── 5. Hero stats 下方加四個連結卡片 ──
LINKS_HTML = '''
  <!-- Quick Links -->
  <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:32px;padding:0 16px;animation:fadeUp .6s .4s ease both;opacity:0">
    <a href="/tools/" style="text-decoration:none;background:rgba(37,99,235,.15);border:1px solid rgba(37,99,235,.3);border-radius:12px;padding:14px 22px;display:flex;align-items:center;gap:8px;color:#93c5fd;font-size:14px;font-weight:600;transition:all .2s" onmouseover="this.style.background='rgba(37,99,235,.25)'" onmouseout="this.style.background='rgba(37,99,235,.15)'">
      <span style="font-size:20px">🧮</span> 500+ 免費計算工具
    </a>
    <a href="/patterns/index.html" style="text-decoration:none;background:rgba(168,85,247,.15);border:1px solid rgba(168,85,247,.3);border-radius:12px;padding:14px 22px;display:flex;align-items:center;gap:8px;color:#c4b5fd;font-size:14px;font-weight:600;transition:all .2s" onmouseover="this.style.background='rgba(168,85,247,.25)'" onmouseout="this.style.background='rgba(168,85,247,.15)'">
      <span style="font-size:20px">📊</span> 50 種 K 棒型態圖鑑
    </a>
    <a href="/blog/" style="text-decoration:none;background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.3);border-radius:12px;padding:14px 22px;display:flex;align-items:center;gap:8px;color:#6ee7b7;font-size:14px;font-weight:600;transition:all .2s" onmouseover="this.style.background='rgba(16,185,129,.25)'" onmouseout="this.style.background='rgba(16,185,129,.15)'">
      <span style="font-size:20px">📚</span> 技術分析教學
    </a>
    <a href="https://lottery.softglow-ai.com/zh-TW/" target="_blank" rel="noopener" style="text-decoration:none;background:rgba(245,158,11,.15);border:1px solid rgba(245,158,11,.3);border-radius:12px;padding:14px 22px;display:flex;align-items:center;gap:8px;color:#fcd34d;font-size:14px;font-weight:600;transition:all .2s" onmouseover="this.style.background='rgba(245,158,11,.25)'" onmouseout="this.style.background='rgba(245,158,11,.15)'">
      <span style="font-size:20px">🎰</span> 全球彩票 + 選號工具
    </a>
  </div>
'''

# 檢查是否已加過
if '500+ 免費計算工具' in content:
    print("  Quick links: already exists")
else:
    # 插在 hero-stats </div> 結束後、</section> 之前
    marker = '</div>\n</section>\n\n<!-- TICKER -->'
    if marker in content:
        content = content.replace(marker, '</div>' + LINKS_HTML + '\n</section>\n\n<!-- TICKER -->')
        changes += 1
        print("  Added: 4 quick links after hero stats")
    else:
        # fallback: 找 hero-stats 結尾
        idx = content.find('涵蓋全台股支數')
        if idx > 0:
            # 找接下來的 </section>
            section_end = content.find('</section>', idx)
            if section_end > 0:
                content = content[:section_end] + LINKS_HTML + '\n' + content[section_end:]
                changes += 1
                print("  Added: 4 quick links (fallback)")
        else:
            print("  X Could not find insert point for quick links")

# ── 6. CTA final 裡的邀請文字也清理 ──
old_cta_sub = '或先免費體驗，不需信用卡 · 付款後立即開通 · 手機電腦均可使用'
if old_cta_sub in content:
    # 不含邀請文字，保留不動
    pass

# 寫回
if changes > 0:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\nSaved! {changes} changes to landing.html")
else:
    print("\nNo changes needed")

print("\nNext: git add -A && git commit -m 'landing: remove invite, add quick links' && git push")
