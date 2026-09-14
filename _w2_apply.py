# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")

def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("FAIL %s count=%s\n%s" % (label, n, old[:200]))
    t = t.replace(old, new, 1)
    print("OK", label)

css = """
/* Wave2 home IA — 九宮格分類卡，非 2.5D */
.home-ia-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:4px 0 14px}
.home-ia-card{background:var(--bg2);border:.5px solid var(--border2);border-radius:12px;padding:14px 10px 12px;text-align:center;cursor:pointer;min-height:76px}
.home-ia-card:active{opacity:.85}
.home-ia-ico{font-size:22px;line-height:1.2;margin-bottom:4px}
.home-ia-ttl{font-size:13px;font-weight:700;color:var(--text)}
.home-ia-sub{font-size:10px;color:var(--text3);margin-top:3px;line-height:1.35}
.home-ia-upgrade{display:block;width:100%;margin:0 0 14px;padding:12px 14px;border:none;border-radius:12px;background:var(--green);color:#fff;font-size:14px;font-weight:700;cursor:pointer}
@media (max-width:720px){
  .home-ia-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
}
"""
rep("#homeDash.show{display:block}", "#homeDash.show{display:block}\n"+css, "css")

grid = """
    <div class="home-ia-grid" id="homeIaGrid">
      <div class="home-ia-card" onclick="_homeGo('quotes')"><div class="home-ia-ico">📈</div><div class="home-ia-ttl">行情</div><div class="home-ia-sub">常用／最近搜尋</div></div>
      <div class="home-ia-card" onclick="_homeGo('picks')"><div class="home-ia-ico">🔥</div><div class="home-ia-ttl">開盤精選</div><div class="home-ia-sub">熱門名單</div></div>
      <div class="home-ia-card" onclick="_homeGo('analyze')"><div class="home-ia-ico">🔍</div><div class="home-ia-ttl">個股分析</div><div class="home-ia-sub">搜尋後分析</div></div>
      <div class="home-ia-card" onclick="_homeGo('pattern')"><div class="home-ia-ico">🕯</div><div class="home-ia-ttl">型態</div><div class="home-ia-sub">K棒型態細節</div></div>
      <div class="home-ia-card" onclick="_homeGo('chips')"><div class="home-ia-ico">🏦</div><div class="home-ia-ttl">法人籌碼</div><div class="home-ia-sub">三大法人／資券</div></div>
      <div class="home-ia-card" onclick="_homeGo('deep')"><div class="home-ia-ico">📐</div><div class="home-ia-ttl">DEEP</div><div class="home-ia-sub">深度分析七欄</div></div>
      <div class="home-ia-card" onclick="_homeGo('deepanalysis')"><div class="home-ia-ico">🎯</div><div class="home-ia-ttl">深度選股</div><div class="home-ia-sub">每日條件名單</div></div>
      <div class="home-ia-card" onclick="_homeGo('portfolio')"><div class="home-ia-ico">💼</div><div class="home-ia-ttl">持股健檢</div><div class="home-ia-sub">成本與訊號</div></div>
      <div class="home-ia-card" onclick="_homeGo('watch')"><div class="home-ia-ico">⭐</div><div class="home-ia-ttl">自選</div><div class="home-ia-sub">關注清單</div></div>
    </div>
    <button type="button" class="home-ia-upgrade" id="homeIaUpgrade" onclick="_homeGo('upgrade')">升級會員，解鎖完整分析</button>
"""
rep(
'''<div id="homeDash">
    <div class="hd-sec">''',
'''<div id="homeDash">
'''+grid+'''    <div class="hd-sec">''',
"grid_html")

js = r'''
function _homeFocusSearch(hint){
  showPage('home');
  const inp = document.getElementById('stockInput');
  if(inp){ inp.focus(); try{ inp.scrollIntoView({behavior:'smooth',block:'center'}); }catch(e){} }
  if(hint && typeof setSt==='function') setSt(hint, false);
}
function _homeNeedStockThen(fn, hint){
  const id = (window.C && C._currentId) ? C._currentId : '';
  if(!id){ _homeFocusSearch(hint || '請先輸入股票代號再分析'); return; }
  showPage('home');
  fn(id);
}
function _homeGo(kind){
  if(kind==='quotes'){
    showPage('home');
    const el = document.getElementById('hotkeysEl');
    if(el){ try{ el.scrollIntoView({behavior:'smooth',block:'center'}); }catch(e){} }
    return;
  }
  if(kind==='picks'){ showPage('picks'); return; }
  if(kind==='analyze'){ _homeFocusSearch('輸入代號或名稱後按分析'); return; }
  if(kind==='pattern'){
    _homeNeedStockThen(function(){
      const t = document.getElementById('dcard-kbar');
      if(t){ try{ t.scrollIntoView({behavior:'smooth',block:'center'}); }catch(e){} }
    }, '請先分析一檔，再看型態細節');
    return;
  }
  if(kind==='chips'){
    _homeNeedStockThen(function(id){
      if(typeof loadChips==='function') loadChips(id);
      const t = document.getElementById('chipsSection');
      if(t){ t.style.display='block'; try{ t.scrollIntoView({behavior:'smooth',block:'center'}); }catch(e){} }
    }, '請先分析一檔，再看法人籌碼');
    return;
  }
  if(kind==='deep'){
    _homeNeedStockThen(function(){
      const t = document.getElementById('deepSection');
      if(t){ try{ t.scrollIntoView({behavior:'smooth',block:'center'}); }catch(e){} }
    }, '請先分析一檔，再看 DEEP');
    return;
  }
  if(kind==='deepanalysis'){ showPage('deepanalysis'); return; }
  if(kind==='portfolio'){ showPage('portfolio'); return; }
  if(kind==='watch'){ showPage('watch'); return; }
  if(kind==='upgrade'){
    if(typeof _hasPremium==='function' && _hasPremium()){ showPage('my'); return; }
    if(window._authUser && typeof showUpgradeModal==='function'){ showUpgradeModal(); return; }
    if(typeof showLoginModal==='function') showLoginModal();
    return;
  }
}

'''
rep("function _observeHomeDash(){", js+"function _observeHomeDash(){", "js")

p.write_text(t, encoding="utf-8")
print("W2_APPLY_OK")
