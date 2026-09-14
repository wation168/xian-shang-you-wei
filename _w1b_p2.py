# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")

def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("FAIL %s count=%s\n%s" % (label, n, old[:260]))
    t = t.replace(old, new, 1)
    print("OK", label)

# helper next to _creditExhausted
old_h = '''function _creditExhausted(){
  const c = window._dailyCredit;
  if(!c) return false;
  return (c.remaining|0) <= 0;
}'''
new_h = '''function _creditExhausted(){
  const c = window._dailyCredit;
  if(!c) return false;
  return (c.remaining|0) <= 0;
}
function _handleQuotaLimit(j, detail){
  if(j && j.credit) _syncCreditFromPayload(j);
  const d = (typeof detail === 'string' ? detail : '') + (j && j.detail ? String(j.detail) : '');
  const isGuest = !_authUser || d.includes('guest_limit');
  if(isGuest) _showGuestLimitModal();
  else _showFreeLimitModal();
  try{ setSt('', false); }catch(e){}
  return true;
}'''
rep(old_h, new_h, "handle_quota")

# analyzeStock 429
rep(
'''      if(r.status===429){
        if(detail.includes('guest_limit')){
          // 遊客次數已到，顯示登入提示
          _showGuestLimitModal();
          setSt('',false);
        } else if(detail.includes('today_limit')){
          // 免費會員次數已到
          _showFreeLimitModal();
          setSt('',false);
        } else {
          setSt(`❌ ${detail.replace(/^[^|]+\\|/,'')}`,true);
        }
        return;
      }''',
'''      if(r.status===429){
        let _j429=null;
        try{ _j429=JSON.parse(txt); }catch(e){}
        _handleQuotaLimit(_j429, detail);
        return;
      }''',
"analyze_429")

# _pfLoad
rep(
'''    const r = await fetch(`${getAPI()}/portfolio/analysis`, { headers: _authHeaders() });
    if(!r.ok) throw new Error('載入失敗');
    const j = await r.json();''',
'''    const r = await fetch(`${getAPI()}/portfolio/analysis`, { headers: _authHeaders() });
    if(!r.ok){
      const txt = await r.text().catch(()=> '');
      let j429=null, detail=`HTTP ${r.status}`;
      try{ j429=JSON.parse(txt); detail=j429.detail||j429.message||detail; }catch(e){}
      if(r.status===429 || String(detail).includes('guest_limit') || String(detail).includes('today_limit')){
        _handleQuotaLimit(j429, detail);
        el.innerHTML = '<div style="text-align:center;padding:24px 0;color:var(--text3);font-size:13px">今日健檢額度已用完</div>';
        return;
      }
      throw new Error('載入失敗');
    }
    const j = await r.json();''',
"pf_429")

# B2 deep lock at end of _applyResultMasks — insert before closing brace of function
# Find unique tail
old_mask_tail = '''    } else if(sumOv){ sumOv.style.display = 'none'; }
  }
}'''
# This might match too loosely. Check count.
print("mask tail count", t.count(old_mask_tail))

# free modal copy
rep(
'''      免費會員每日 <strong>3 次</strong>查詢已用完<br>升級或邀請好友可繼續使用''',
'''      今日完整分析／健檢額度已用完（以後端為準）<br>升級或邀請好友可繼續使用''',
"free_modal")

p.write_text(t, encoding="utf-8")
print("FE_PARTIAL")
