/* Fixed maximum circles and reserved text slots. Replay never invokes solve. */
window.MarketLayout=(()=>{
const ctx=document.createElement('canvas').getContext('2d');
function measure(text,size=11){ctx.font=`500 ${size}px "Microsoft JhengHei", "Noto Sans TC", sans-serif`;return ctx.measureText(String(text)).width*1.06+4}
function wrap(text,size,limit){let line='',lines=[];for(const c of String(text)){if(line&&measure(line+c,size)>limit){lines.push(line);line=c}else line+=c}if(line)lines.push(line);return lines}
const radius=(score,mobile,scale=1)=>Math.max(mobile?6:7,(mobile?35:64)*scale*Math.sqrt(Math.max(0,Math.min(100,score??0))/100));
const intersects=(a,b,gap=0)=>a.x<b.x+b.w+gap&&a.x+a.w+gap>b.x&&a.y<b.y+b.h+gap&&a.y+a.h+gap>b.y;
function circleRect(c,b,gap=0){const x=Math.max(b.x,Math.min(c.cx,b.x+b.w)),y=Math.max(b.y,Math.min(c.cy,b.y+b.h));return Math.hypot(c.cx-x,c.cy-y)<c.rEnvelope+gap}
const distance=(c,b)=>Math.max(0,Math.hypot(Math.max(b.x-c.cx,0,c.cx-b.x-b.w),Math.max(b.y-c.cy,0,c.cy-b.y-b.h))-c.rEnvelope);
// A label follows its shrinking disk (dx/dy per px of radius lost, up to travel px). It must stay clearly
// nearer its owner than any other disk at every step: own distance < 0.6 x other distance, with margin.
function crowded(owner,b,o){const own=distance(owner,b),t=b.travel||0;if(distance(o,b)-t>Math.max(7,(own+4)/.6))return false;for(const f of [0,.5,1]){const m={x:b.x+(b.dx||0)*t*f,y:b.y+(b.dy||0)*t*f,w:b.w,h:b.h};if(circleRect(o,m,7)||distance(o,m)*.6<=own+4)return true}return false}
// Reserve a full label before accepting a disk position: below, above, right, left.
function labelSlot(n,disk,bounds,disks,slots){const tw=n.labelW,th=n.labelH,r=disk.rEnvelope,travel=Math.max(0,r-6);return [{x:disk.cx-tw/2,y:disk.cy+r+5,dx:0,dy:-1},{x:disk.cx-tw/2,y:disk.cy-r-th-5,dx:0,dy:1},{x:disk.cx+r+5,y:disk.cy-th/2,dx:-1,dy:0},{x:disk.cx-r-tw-5,y:disk.cy-th/2,dx:1,dy:0}].map(p=>({...p,w:tw,h:th,travel})).find(b=>b.x>=bounds.x&&b.x+b.w<=bounds.x+bounds.w&&b.y>=bounds.y&&b.y+b.h<=bounds.y+bounds.h&&!disks.some(o=>o!==disk&&crowded(disk,b,o))&&!slots.some(s=>intersects(s,b,5)))||null}
function solve({groups,maxScores={},width,mobile=false,clusterShares={},maxHeight=520,expanded=false,focusClusters=[]}){
 const all=[...new Set(groups.map(g=>g.cluster_id))].map(id=>({id,name:groups.find(g=>g.cluster_id===id).cluster_name||id,members:groups.filter(g=>g.cluster_id===id).sort((a,b)=>(maxScores[b.group_id]??b.activity_score)-(maxScores[a.group_id]??a.activity_score)||a.group_id.localeCompare(b.group_id)),share:clusterShares[id]??null}));
 const weight=c=>c.members.reduce((s,g)=>s+(maxScores[g.group_id]??g.activity_score??0),0);
 all.sort((a,b)=>(b.share??-1)-(a.share??-1)||weight(b)-weight(a)||a.id.localeCompare(b.id));
 const stripColumns=Math.max(1,Math.floor(width/48)); let full=all.slice(),scale=1;
 if(mobile&&!expanded){let sum=0;full=[];for(const c of all){full.push(c);sum+=c.share??0;if(sum>=.7)break}}
 if(mobile&&!expanded)full=all.filter(c=>full.includes(c)||focusClusters.includes(c.id));
 // Compact mobile rows reserve at least 44px per touch target.
 // cap: mobile height budget; a pack that already exceeds it stops early and reports Infinity.
 function pack(list,cap=Infinity,side=false){const gap=scale>.4?14:4;const columns=mobile?1:Math.min(list.length,list.length>=6?3:2),zoneW=(width-16)/Math.max(1,columns),bottoms=Array(columns).fill(8),clusters=[],nodes=[];
 for(const c of list){const col=bottoms.indexOf(Math.min(...bottoms)),x=8+col*zoneW,y=bottoms[col],w=zoneW-8;
 const ns=c.members.map(g=>{const maxScore=maxScores[g.group_id]??g.activity_score??0,lines=wrap(g.name,11,mobile?95:120);return {id:g.group_id,name:g.name,cluster:c.id,maxScore,rEnvelope:radius(maxScore,mobile,scale),font:11,lines,labelW:Math.max(mobile?0:Math.max(measure("-100.00%",11),measure("\u8cc7\u6599\u6e96\u5099\u4e2d",11)),...lines.map(l=>measure(l,11))),labelH:(lines.length+(mobile?0:1))*15,wantsLabel:!mobile||maxScore>=20}});
 if(mobile){let rowY=y+26,row=[],rowW=0;
 const flush=()=>{if(!row.length)return;const top=Math.max(22,...row.map(n=>Math.max(n.rEnvelope+9,side?n.labelH/2:0))),rowH=side?top*2+4:top+Math.max(...row.map(n=>Math.max(22,n.rEnvelope+3+(n.wantsLabel?n.labelH:0))+4));let left=x+(w-rowW)/2;for(const n of row){n.cx=side&&n.wantsLabel?left+Math.max(22,n.rEnvelope+9):left+n.cellW/2;n.cy=rowY+top;n.slot=n.wantsLabel?{x:side?n.cx+n.rEnvelope+3:n.cx-n.labelW/2,y:side?n.cy-n.labelH/2:n.cy+n.rEnvelope+3,w:n.labelW,h:n.labelH}:null;nodes.push(n);left+=n.cellW}rowY+=rowH;row=[];rowW=0};
 for(const n of ns){n.cellW=side&&n.wantsLabel?Math.max(48,Math.max(22,n.rEnvelope+9)+n.rEnvelope+n.labelW+15):Math.max(48,n.rEnvelope*2+18,n.wantsLabel?n.labelW+12:0);if(rowW+n.cellW>w-8)flush();row.push(n);rowW+=n.cellW}flush();
 const h=rowY-y+2,header={id:c.id,x:x+8,y:y+4,w:w-16,h:16,font:11,name:c.name};clusters.push({id:c.id,name:c.name,x:x+w/2,y:y+h/2+8,rx:w/2,ry:(h-16)/2,header});bottoms[col]=y+h+4;continue;
 }
 let h=Math.max(130,ns.reduce((s,n)=>s+(2*Math.max(22,n.rEnvelope)+gap)**2,0)/Math.max(100,w-24)/.72+55),placed=[];
 // Disks are sampled in a deterministic spiral, largest nearest the center. A spot that also leaves
 // room for the complete outside label is required whenever the label is eligible.
 for(let attempt=0;attempt<100;attempt++){if(y+h+12>cap)return {height:Infinity};placed=[];const reserved=[],bounds={x:x+4,y:y+45,w:w-8,h:h-50};let fits=true;for(const n of ns){let spot=null;const edge=Math.max(22,n.rEnvelope)+9;for(let k=0;k<Math.ceil((Math.hypot(w,h)/2+40)**2/16);k++){const a=k*2.399963,r=4*Math.sqrt(k),cx=x+w/2+Math.cos(a)*r,cy=y+42+(h-48)/2+Math.sin(a)*r;if(cx-edge<x+5||cx+edge>x+w-5||cy-edge<y+46||cy+edge>y+h-5)continue;if(placed.some(p=>Math.hypot(p.cx-cx,p.cy-cy)<Math.max(22,p.rEnvelope)+Math.max(22,n.rEnvelope)+gap))continue;const disk={cx,cy,rEnvelope:n.rEnvelope};if(placed.some(p=>p.slot&&crowded(p,p.slot,disk)))continue;if(!n.wantsLabel){spot={...n,cx,cy,slot:null};break}const slot=labelSlot(n,disk,bounds,[...placed,disk],reserved);if(slot){spot={...n,cx,cy,slot};break}}if(!spot){fits=false;break}placed.push(spot);if(spot.slot)reserved.push(spot.slot)}if(fits)break;h+=22}
 const header={id:c.id,x:x+8,y:y+5,w:w-16,h:32,font:11,name:c.name};clusters.push({id:c.id,name:c.name,x:x+w/2,y:y+h/2+15,rx:w/2,ry:(h-28)/2,header});nodes.push(...placed);bottoms[col]=y+h+12;
 }
 const height=list.length?Math.max(160,...bottoms):0,slots=nodes.filter(n=>n.slot).map(n=>n.slot);
 for(const n of nodes){if(n.slot||!n.wantsLabel)continue;const c=clusters.find(c=>c.id===n.cluster);n.slot=labelSlot(n,n,{x:c.x-c.rx+4,y:c.header.y+40,w:c.rx*2-8,h:c.ry*2-22},nodes,slots);if(n.slot)slots.push(n.slot)}
 return {width,height,nodes,clusters,headers:clusters.map(c=>c.header),scale,mobile};
 }
 const budget=()=>mobile&&!expanded?maxHeight-Math.ceil((all.length-full.length)/stripColumns)*88:Infinity;
 const bestPack=()=>{const below=pack(full,budget());if(!mobile)return below;const beside=pack(full,budget(),true);return beside.height<below.height?beside:below};
 let result=bestPack();
 // Mobile order: compact rows, shrink to the 6px minimum, then remove only
 // non-focus clusters as a last resort. Required label room is never discarded; the galaxy stays nonempty.
 if(mobile&&!expanded){while(result.height>budget()){const removable=full.filter(c=>!focusClusters.includes(c.id)).at(-1);/* 2026/09/26：先縮到約一半（最大球約 16px），還放不下就先把非焦點星團收進下方小列，最後才繼續縮到 6px，避免手機星球全部變成小點 */if(scale>.46)scale=Math.max(.45,scale-.05);else if(removable&&full.length>1)full=full.filter(c=>c!==removable);else if(scale>.11)scale=Math.max(.1,scale-.05);else break;result=bestPack()}}
 if(result.height===Infinity)result=pack(full);
 return {...result,stripColumns,strip:all.filter(c=>!full.includes(c)).map(c=>({clusterId:c.id,name:c.name})),fullClusters:full.map(c=>c.id)};
}
function audit(l){const collisions=[],outside=[];for(let i=0;i<l.nodes.length;i++){const a=l.nodes[i];if(a.cx-a.rEnvelope<0||a.cx+a.rEnvelope>l.width||a.cy-a.rEnvelope<0||a.cy+a.rEnvelope>l.height)outside.push(a.id);for(const b of l.nodes.slice(i+1))if(Math.hypot(a.cx-b.cx,a.cy-b.cy)<a.rEnvelope+b.rEnvelope)collisions.push([a.id,b.id]);if(a.slot){for(const b of l.nodes)if(circleRect(b,a.slot))collisions.push([a.id+':label',b.id]);for(const b of l.nodes.slice(i+1))if(b.slot&&intersects(a.slot,b.slot))collisions.push([a.id+':label',b.id+':label'])}}
 return {collisions,outside};}
return {solve,radius,measure,wrap,circleRect,distance,audit};
})();
