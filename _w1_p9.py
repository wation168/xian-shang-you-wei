# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")

def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("FAIL %s count=%s\n%s" % (label, n, old[:240]))
    t = t.replace(old, new, 1)
    print("OK", label)

rep(
"""  // 遊客第二次起：每日 1 次前端限制（有 token 就直接送，由後端決定）
  if(!_getToken() && localStorage.getItem('guest_visited')){
    const _gk='guest_day_'+new Date().toISOString().slice(0,10);
    if(parseInt(localStorage.getItem(_gk)||'0',10)>=1){_showGuestLimitModal();return;}
  }""",
"  // Wave1：次數以後端 daily_credit／429 為準，前端不再自算額度\n",
"fe_wall")

rep(
"""  // 免費會員記錄當日查詢次數（付費不計）
  if(_authUser && !_hasPremium()) _incFreeQueryCount();
  // 遊客：標記首次訪問並記錄每日次數
  if(!_authUser){
    localStorage.setItem('guest_visited','1');
    const _gk='guest_day_'+new Date().toISOString().slice(0,10);
    localStorage.setItem(_gk,String(parseInt(localStorage.getItem(_gk)||'0',10)+1));
  }""",
"  if(d && d.credit){ _syncCreditFromPayload(d); }\n",
"fe_inc")

js = """
function _taipeiDayKey(){
  return new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Taipei',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
}
function _syncCreditFromPayload(j){
  if(!j) return;
  if(j.credit){ window._dailyCredit = j.credit; return; }
  if(typeof j.queries_used === 'number' && typeof j.queries_limit === 'number'){
    window._dailyCredit = {used:j.queries_used, limit:j.queries_limit, remaining:Math.max(0, j.queries_limit - j.queries_used)};
  }
}
function _creditExhausted(){
  const c = window._dailyCredit;
  if(!c) return false;
  return (c.remaining|0) <= 0;
}

"""
if "_taipeiDayKey" not in t:
    rep("function _applyResultMasks(){", js + "function _applyResultMasks(){", "fe_helpers")

rep(
"""  } else if(_authUser){
    const cnt = _getFreeQueryCount();
    locked = cnt > 3;
    msg = '升級或邀請3位好友查看完整分析';
    action = showUpgradeModal;""",
"""  } else if(_authUser){
    locked = _creditExhausted();
    msg = '今日完整分析額度已用完，升級後無限使用';
    action = showUpgradeModal;""",
"fe_mask")

t = t.replace(
    "if(me.ok){ _authUser = await me.json(); _applyResultMasks(); }",
    "if(me.ok){ _authUser = await me.json(); _syncCreditFromPayload(_authUser); _applyResultMasks(); }",
)
print("me.ok replacements done")

p.write_text(t, encoding="utf-8")
print("FE_CORE_DONE")
