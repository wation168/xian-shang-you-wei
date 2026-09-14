# -*- coding: utf-8 -*-
from pathlib import Path

idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
land = Path(r"D:\xian-shang-you-wei\backend\frontend\landing.html")
it = idx.read_text(encoding="utf-8")
lt = land.read_text(encoding="utf-8")

# --- 1) Desktop picks: already should be j.updated_at only; harden exact block ---
old_desk = None
# Find current _updLine block
marker = "async function _loadDesktopPicks"
pos = it.find(marker)
if pos < 0:
    raise SystemExit("no _loadDesktopPicks")
chunk_end = it.find("async function", pos + 10)
chunk = it[pos:chunk_end if chunk_end > pos else pos + 2000]
# Replace whatever _updLine construction exists
import re
m = re.search(
    r"const items = j\.data \|\| \[\];\n(?:.*\n){0,8}?    if\(!items\.length\)\{",
    it[pos:],
)
if not m:
    raise SystemExit("desktop items block not found")
block = m.group(0)
new_block = """const items = j.data || [];
    // GPT: only updated_at; never server_time as last update
    const _updLine = j.updated_at
      ? `<div style=\"padding:8px 12px 0;font-size:11px;color:var(--text3)\">上次更新（台北）：${j.updated_at}</div>`
      : `<div style=\"padding:8px 12px 0;font-size:11px;color:var(--text3)\">尚未更新（排程約每個交易日 09:06 台北）</div>`;
    if(!items.length){"""
it = it[:pos] + it[pos:].replace(block, new_block, 1)
print("1) desktop picks updated_at-only OK")

# --- 2) showPicksPage empty state: fix updatedAt usage ---
# Current pattern after our edit had ${updatedAt} inside empty HTML which may be undefined object string
old_empty_frag = None
# Find showPicksPage updatedAt definition and empty branch
sp = it.find("async function showPicksPage")
if sp < 0:
    raise SystemExit("no showPicksPage")
# Normalize updatedAt construction
# Replace the updatedAt const block
m2 = re.search(
    r"const updatedAt = j\.updated_at\s*\n\s*\? `[\s\S]*?`\s*\n\s*: `[\s\S]*?`;",
    it[sp:sp+2500],
)
if not m2:
    # try single-line variants
    m2 = re.search(r"const updatedAt = j\.updated_at[\s\S]{0,400}?;", it[sp:sp+2500])
if not m2:
    raise SystemExit("updatedAt const not found: " + repr(it[sp:sp+500]))
old_upd = m2.group(0)
new_upd = """const updatedAt = j.updated_at
      ? `<div style=\"font-size:11px;color:var(--text3);margin-bottom:12px\">上次更新（台北）：${j.updated_at}</div>`
      : `<div style=\"font-size:11px;color:var(--text3);margin-bottom:12px\">尚未更新（排程約每個交易日 09:06 台北）</div>`;"""
it = it[:sp] + it[sp:].replace(old_upd, new_upd, 1)

# Empty state: ensure we inject updatedAt string (always defined now), remove duplicate schedule-only lines confusion
# Find empty items branch in showPicksPage
m3 = re.search(
    r"if \(!items\.length\) \{\s*el\.innerHTML = `[\s\S]*?`;\s*return;",
    it[sp:sp+4500],
)
if not m3:
    raise SystemExit("empty items branch not found")
old_empty = m3.group(0)
new_empty = """if (!items.length) {
      el.innerHTML = `
        <div style=\"padding:8px 0 16px\">
          ${deepCard}
          ${updatedAt}
          <div style=\"padding:40px 0;text-align:center\">
            <div style=\"font-size:40px;margin-bottom:12px\">🔍</div>
            <div style=\"font-size:15px;font-weight:700;margin-bottom:8px\">今日尚無開盤熱門股</div>
          </div>
        </div>`;
      return;"""
it = it[:sp] + it[sp:].replace(old_empty, new_empty, 1)
print("2) showPicksPage empty-state updatedAt OK")

# --- nit goPayFromApp ---
old_gopay = """function goPayFromApp(plan) {
  console.warn('[pay] short-link disabled; use in-app upgrade (create_order_recurring)');
  if (typeof showUpgradeModal === 'function') { showUpgradeModal(); return; }
  if (typeof doUpgrade === 'function') { doUpgrade(plan || 'monthly', {disabled:false, textContent:'', innerHTML:''}); return; }
  alert('請至「我的」頁面選擇方案升級（現行價格）。');
}"""
new_gopay = """function goPayFromApp(plan) {
  console.warn('[pay] short-link disabled; use in-app upgrade (create_order_recurring)');
  if (typeof showUpgradeModal === 'function') {
    showUpgradeModal();
    return;
  }
  alert('舊付款短網址已停用。請至「我的」頁面選擇方案升級（現行價格 499／999／3688）。');
}"""
if old_gopay not in it:
    # softer match
    m4 = re.search(r"function goPayFromApp\(plan\) \{[\s\S]*?\n\}", it)
    if not m4:
        raise SystemExit("goPayFromApp not found")
    it = it.replace(m4.group(0), new_gopay.strip(), 1)
    print("nit goPayFromApp replaced via regex")
else:
    it = it.replace(old_gopay, new_gopay, 1)
    print("nit goPayFromApp OK")

idx.write_text(it, encoding="utf-8")

# --- 3) pay=done CSS: do not disable hero App CTA ---
old_css = ".pay-done .nav-cta,.pay-done .price-btn,.pay-done .cta-final .btn-primary,.pay-done .hero-btns .btn-primary{opacity:.35;pointer-events:none;filter:grayscale(.2)}"
new_css = ".pay-done .nav-cta,.pay-done .price-btn,.pay-done .cta-final .btn-primary,.pay-done button.price-btn,.pay-done button[onclick*=\"openBuy\"]{opacity:.35;pointer-events:none;filter:grayscale(.2)}"
# hero-btns .btn-primary is now <a href=/stock/> — exclude it
if old_css not in lt:
    # find pay-done style
    m5 = re.search(r"\.pay-done[^\{]*\{[^}]+\}", lt)
    if not m5:
        raise SystemExit("pay-done css not found: " + lt[lt.find("pay-done"):lt.find("pay-done")+200])
    print("OLD CSS", m5.group(0))
    lt = lt.replace(m5.group(0), new_css, 1)
else:
    lt = lt.replace(old_css, new_css, 1)
land.write_text(lt, encoding="utf-8")
print("3) pay-done CSS OK (App CTA clickable)")

# verify
it2 = idx.read_text(encoding="utf-8")
lt2 = land.read_text(encoding="utf-8")
assert "j.updated_at || j.server_time" not in it2
assert "server_time" not in it2[it2.find("_loadDesktopPicks"):it2.find("_loadDesktopPicks")+900] or "查詢時間" not in it2[it2.find("_loadDesktopPicks"):it2.find("_loadDesktopPicks")+900]
desk = it2[it2.find("_loadDesktopPicks"):it2.find("_loadDesktopPicks")+1100]
assert "j.server_time" not in desk
assert "上次更新（台北）：${j.updated_at}" in desk
assert "hero-btns .btn-primary" not in lt2
assert "openBuy" in lt2[lt2.find("pay-done"):lt2.find("pay-done")+350]
assert "doUpgrade(plan" not in it2[it2.find("function goPayFromApp"):it2.find("function goPayFromApp")+350]
print("ALL CHECKS PASSED")
