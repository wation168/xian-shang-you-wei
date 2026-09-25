/* 正式站資料接口（2026/09/25，案件016）：取代 Demo 的 Mock adapter，公開方法與回傳形狀不變。
   - 市場星系：/api/market/groups、/api/market/groups/timeline（公開，後端快取，不現抓現算）
   - 族群成分股：/api/market/groups/{id}（登入即可，免費會員也可以）
   - 我的自選：登入 → /api/market/my-watch（只讀自己的清單）；未登入 → 本機 watchList＋/api/intraday（跟舊首頁同一套）
   - 登入狀態沿用舊首頁的 localStorage auth_token（同網域共用） */
window.MarketData=(()=>{
const API=(()=>{const h=location.hostname;return (h==='localhost'||h==='127.0.0.1'||h.startsWith('192.168'))?'http://localhost:8000':'https://api.softglow-ai.com'})();
const calls={},reads={},dict=new Map();let live=false;
const count=n=>calls[n]=(calls[n]||0)+1;
const token=()=>{try{return localStorage.getItem('auth_token')||''}catch(e){return ''}};
async function get(path,auth=false){const key=path.split('?')[0];reads[key]=(reads[key]||0)+1;const headers={},t=auth?token():'';if(t)headers.Authorization='Bearer '+t;let r;try{r=await fetch(API+path,{headers,cache:'no-store',signal:AbortSignal.timeout(15000)})}catch(e){throw new Error('網路連線失敗，請稍後再試')}if(r.status===401){const e=new Error('請先登入');e.status=401;throw e}if(!r.ok){let msg='資料讀取失敗';try{const j=await r.json();if(j&&typeof j.detail==='string')msg=j.detail}catch(_){}throw new Error(msg)}return r.json()}
function remember(groups){for(const g of groups||[])if(g&&g.group_id&&g.name)dict.set(g.group_id,{name:g.name,cluster_id:g.cluster_id,cluster_name:g.cluster_name})}
function fill(g){const d=dict.get(g.group_id);return {stable_rank:null,top_codes:null,turnover_share:null,up_count:null,down_count:null,flat_count:null,share_vs_prev_day:null,...g,name:g.name||d?.name||g.group_id,cluster_id:g.cluster_id||d?.cluster_id||'',cluster_name:g.cluster_name||d?.cluster_name||g.cluster_id||'',name_missing:!(g.name||d?.name)}}
const hm=t=>t==='收盤'?(live?'13:30':'盤後'):t;
async function guestWatch(){let list=[];try{list=JSON.parse(localStorage.getItem('watchList')||'[]')}catch(e){}const codes=[...new Set(list.map(x=>String(x&&x.id||'').trim().toUpperCase()).filter(c=>/^[0-9A-Z]{4,6}$/.test(c)))].slice(0,30);if(!codes.length)return {watchlist:[],watchlist_data_time:null};const j=await get('/api/intraday?ids='+codes.join(','));const data=j&&j.data||{};const names=new Map(list.map(x=>[String(x&&x.id||'').toUpperCase(),x&&x.name]));const out=codes.map(c=>{const q=data[c]||{};return {code:c,name:names.get(c)||q.name||c,price:q.price??null,change_pct:q.change_pct??null,group_ids:[]}});const anyLive=Object.values(data).some(q=>q&&q.live);return {watchlist:out,watchlist_data_time:anyLive?new Date(Date.now()+8*3600e3).toISOString().slice(11,16):'收盤'}}
async function watch(){if(token()){try{const j=await get('/api/market/my-watch',true);return {watchlist:j.watchlist||[],watchlist_data_time:j.watchlist_data_time??null}}catch(e){if(e.status!==401)return {watchlist:null,watchlist_data_time:null}}}try{return await guestWatch()}catch(e){return {watchlist:null,watchlist_data_time:null}}}
return Object.freeze({
 async getMarketOverview(){count('getMarketOverview');const [o,w]=await Promise.all([get('/api/market/groups'),watch()]);const ok=!!(o&&o.ok);live=!!(o&&o.live);remember(o&&o.groups);const groups=(o&&o.groups||[]).map(fill);
  return {trade_date:o&&o.trade_date||'',market_state:ok?(o.market_state||'closed'):'closed',data_time:ok?hm(o.data_time):'—',is_delayed:!!(o&&o.is_delayed),awaiting_first_snapshot:!ok,pool_size:o&&o.pool_size||0,groups,clusters:o&&o.clusters||null,cluster_reference_groups:groups,change_scale:o&&o.change_scale||{flat:.3,small:1,normal:2,strong:3.5},
   market_summary:{index_value:null,index_change_pct:null,market_turnover:null,up_count:null,down_count:null,flat_count:null,data_time:null,...(o&&o.market_summary||{})},
   source:ok?((o.source||'')+(live&&o.market_state==='open'?' · 每 5 分鐘更新':(live?'':' · 最近交易日'))):'市場資料準備中',data_label:'新版試跑',data_note:'',demo_scenarios:[],demo_scenario:'live',live,...w}},
 async getTimeline(){count('getTimeline');const t=await get('/api/market/groups/timeline');remember(t&&t.group_dict);return {trade_date:t&&t.trade_date||'',interval_min:t&&t.interval_min||5,fallback:!!(t&&t.fallback),snapshots:(t&&t.snapshots||[]).map(s=>({time:s.time,clusters:s.clusters||null,groups:(s.groups||[]).map(fill)}))}},
 async getGroupDetail(id){count('getGroupDetail');if(!/^[a-z0-9_]{1,40}$/.test(String(id)))throw new Error('找不到此族群');if(!token())throw new Error('登入後即可查看成分股（免費會員也可以）：請點右下「設定」登入');let d;try{d=await get('/api/market/groups/'+encodeURIComponent(id),true)}catch(e){if(e.status===401)throw new Error('登入已過期，請點「設定」重新登入後再查看成分股');throw e}return {group_id:id,trade_date:d.trade_date,data_time:hm(d.data_time),stocks:(d.stocks||[]).map(s=>({code:s.code,name:s.name,price:s.price??null,change_pct:s.change_pct??null,range20_pos:s.range20_pos??null,group_ids:s.group_ids||[]}))}},
 async setScenario(){count('setScenario')},
 async getDiagnostics(){count('getDiagnostics');return {calls:{...calls},resourceReads:{...reads},scenario:'live'}},
 async resetDiagnostics(){Object.keys(calls).forEach(k=>delete calls[k]);Object.keys(reads).forEach(k=>delete reads[k]);count('resetDiagnostics')}
})})();
