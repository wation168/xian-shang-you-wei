# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")

def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("FAIL %s count=%s\n%s" % (label, n, old[:220]))
    t = t.replace(old, new, 1)
    print("OK", label)

rep(
"""    const res = await fetch(`${getAPI()}/api/picks/opening?_t=${ts}`, {
      headers: { 'Cache-Control': 'no-cache', 'Pragma': 'no-cache' }
    });""",
"""    const res = await fetch(`${getAPI()}/api/picks/opening?_t=${ts}`, {
      headers: { 'Cache-Control': 'no-cache', 'Pragma': 'no-cache', ...(_authHeaders()||{}) }
    });""",
"picks_auth")

rep(
"""    const items = j.data || [];
    // 2026/07/27：時間一律顯示，不管有沒有資料。
    const updatedAt = j.updated_at
      ? `<div style="font-size:11px;color:var(--text3);margin-bottom:12px">上次更新（台北）：${j.updated_at}</div>`
      : `<div style="font-size:11px;color:var(--text3);margin-bottom:12px">尚未更新（排程約每個交易日 09:06 台北）</div>`;""",
"""    const items = j.data || [];
    const _tierNote = j.preview
      ? `<div style="font-size:12px;color:var(--text2);margin-bottom:8px">弱預覽：約 ${j.approx_count ?? items.length} 檔　點開請先登入</div>`
      : (j.masked ? `<div style="font-size:12px;color:var(--text2);margin-bottom:8px">免費預覽已藏股名，升級可看完整名單</div>` : '');
    const updatedAt = j.updated_at
      ? `<div style="font-size:11px;color:var(--text3);margin-bottom:12px">上次更新（台北）：${j.updated_at}</div>`
      : `<div style="font-size:11px;color:var(--text3);margin-bottom:12px">尚未更新（排程約每個交易日 09:06 台北）</div>`;""",
"picks_note")

# inject _tierNote next to updatedAt in picks render — updatedAt already used
t = t.replace("${updatedAt}\n          <div style=\"padding:40px 0;text-align:center\">",
              "${updatedAt}${_tierNote}\n          <div style=\"padding:40px 0;text-align:center\">", 1)
print("empty-state tier note?", "${_tierNote}" in t)

rep(
"""      試用次數已達今日上限（以伺服器紀錄為準）。<br>加入<strong>免費會員</strong>可獲每日 <strong>3 次</strong>查詢；升級付費方案可無限查詢""",
"""      試用次數已達今日上限（以後端紀錄為準）。<br>登入免費會員後，完整分析與持股健檢共用每日額度；升級可無限使用""",
"guest_modal")

# deep: add auth already has _authHeaders. Add preview note after items
rep(
"""    const items = j.data || [];
    // 2026/07/27：時間一律顯示，不管有沒有資料。有 updated_at 就顯示資料更新時間；
    // 沒有（今天還沒跑出來）就顯示後端回傳的查詢時間並標明尚未更新，
    // 使用者才分得出「今天還沒跑」跟「系統壞掉」。
    const updatedAt = j.updated_at
      ? `<div style="font-size:11px;color:var(--text3);margin-bottom:12px">更新時間：${j.updated_at}</div>`
      : `<div style="font-size:11px;color:var(--text3);margin-bottom:12px">尚未更新　查詢時間：${j.server_time || '—'}</div>`;""",
"""    const items = j.data || [];
    const _tierNote = j.preview
      ? `<div style="font-size:12px;color:var(--text2);margin-bottom:8px">弱預覽：約 ${j.approx_count ?? items.length} 檔　點開請先登入</div>`
      : (j.masked ? `<div style="font-size:12px;color:var(--text2);margin-bottom:8px">免費預覽已藏股名</div>` : '');
    const updatedAt = j.updated_at
      ? `<div style="font-size:11px;color:var(--text3);margin-bottom:12px">上次更新（台北）：${j.updated_at}</div>`
      : `<div style="font-size:11px;color:var(--text3);margin-bottom:12px">尚未更新（排程約每個交易日 17:00 台北）</div>`;""",
"deep_note")

# insert _tierNote into deep header
rep(
"""      ${updatedAt}`;""",
"""      ${updatedAt}${_tierNote}`;""",
"deep_header_note")

p.write_text(t, encoding="utf-8")
print("FE_UI_DONE")
