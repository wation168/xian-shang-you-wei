/* tools-chart.js — SoftGlow Dynamic Charts v1.0
   Auto-renders a chart after calculate() is called on any tool page.
   No external dependencies. Pure Canvas API. */
(function(){
'use strict';
var slug=(document.querySelector('meta[name="sg-slug"]')||{}).content;
if(!slug||typeof window.calculate!=='function')return;

/* ── Chart Type Mapping ── */
var G='growth',AM='amort',B='bar',P='pie',D='decline';
var TYPE_MAP={
  'compound-interest':G,'dca-calculator':G,'retirement':G,'401k-contribution':G,
  'savings-goal':G,'education-fund':G,'annuity-income':G,'cagr':G,'rule-of-72':G,
  'roth-ira':G,'ira-contribution':G,'future-value':G,'present-value':G,
  'pension-estimator':G,'social-security':G,'emergency-fund':G,
  'mortgage':AM,'car-loan':AM,'student-loan':AM,'personal-loan':AM,
  'mortgage-refinance':AM,'home-equity-loan':AM,'loan-comparison':AM,
  'credit-card-payoff':AM,'debt-payoff':AM,'amortization-schedule':AM,
  'roi-calculator':B,'stock-gain-loss':B,'risk-reward':B,'dividend-yield':B,
  'sharpe-ratio':B,'pe-ratio':B,'trading-fee':B,'break-even':B,
  'profit-margin':B,'markup-calculator':B,'average-down':B,'stock-split':B,
  'margin-calculator':B,'pip-value':B,'options-profit':B,'dcf-calculator':B,
  'intrinsic-value':B,'price-to-book':B,'earnings-per-share':B,
  'asset-allocation':P,'budget-planner':P,'debt-to-income':P,'expense-ratio':P,
  'net-worth':P,'portfolio-rebalance':P,
  'inflation':D,'purchasing-power':D,'cost-of-living':D
};
var chartType=TYPE_MAP[slug];
if(!chartType)return;

/* ── Colors ── */
var C={
  blue:'#2563EB',blueLt:'rgba(37,99,235,0.15)',
  green:'#10B981',greenLt:'rgba(16,185,129,0.15)',
  red:'#EF4444',redLt:'rgba(239,68,68,0.15)',
  orange:'#F59E0B',orangeLt:'rgba(245,158,11,0.15)',
  purple:'#7C3AED',purpleLt:'rgba(124,58,237,0.15)',
  gray:'#94A3B8',grayLt:'#F1F5F9',
  text:'#334155',textLt:'#94A3B8',
  grid:'#E2E8F0',bg:'#F8FAFC'
};

/* ── Create DOM ── */
var wrap=document.createElement('div');
wrap.id='sg-chart-wrap';
wrap.style.cssText='margin:20px 0;padding:20px;background:'+C.bg+';border:1px solid '+C.grid+';border-radius:12px;display:none;';
var title=document.createElement('div');
title.style.cssText='font-size:15px;font-weight:600;color:'+C.text+';margin-bottom:12px;';
title.textContent='📊';
wrap.appendChild(title);
var cvs=document.createElement('canvas');
cvs.style.cssText='width:100%;max-width:600px;display:block;margin:0 auto;';
wrap.appendChild(cvs);

var results=document.getElementById('results');
if(results)results.parentNode.insertBefore(wrap,results.nextSibling);

/* ── Hook calculate() ── */
var orig=window.calculate;
window.calculate=function(){
  orig.apply(this,arguments);
  setTimeout(render,150);
};

/* ── Utility ── */
function getVal(id){var el=document.getElementById(id);return el?parseFloat(el.value)||0:0;}
function fmt(n){return n>=1e6?(n/1e6).toFixed(1)+'M':n>=1e3?(n/1e3).toFixed(1)+'K':n.toFixed(0);}
function fmtPct(n){return n.toFixed(1)+'%';}

/* ── Render Router ── */
function render(){
  if(!results||!results.classList.contains('show'))return;
  wrap.style.display='block';
  var dpr=window.devicePixelRatio||1;
  var w=Math.min(wrap.clientWidth-40,600);
  var h=Math.round(w*0.55);
  cvs.width=w*dpr;cvs.height=h*dpr;
  cvs.style.width=w+'px';cvs.style.height=h+'px';
  var ctx=cvs.getContext('2d');
  ctx.scale(dpr,dpr);
  ctx.clearRect(0,0,w,h);

  switch(chartType){
    case G:drawGrowth(ctx,w,h);break;
    case AM:drawAmort(ctx,w,h);break;
    case B:drawBar(ctx,w,h);break;
    case P:drawPie(ctx,w,h);break;
    case D:drawDecline(ctx,w,h);break;
  }
}

/* ── Growth Line Chart ── */
function drawGrowth(ctx,W,H){
  title.textContent='📊 投資成長曲線';
  var P0=getVal('principal')||getVal('initialAmount')||getVal('currentSavings')||getVal('amount')||10000;
  var r=(getVal('rate')||getVal('annualReturn')||getVal('interestRate')||5)/100;
  var n=getVal('compounds')||getVal('frequency')||12;
  var t=getVal('years')||getVal('period')||getVal('time')||10;
  if(t<=0)t=10;if(t>50)t=50;
  var monthly=getVal('monthlyDeposit')||getVal('contribution')||getVal('monthlyContribution')||0;

  var data=[];var maxV=P0;
  for(var y=0;y<=t;y++){
    var val=P0*Math.pow(1+r/n,n*y);
    if(monthly>0)val+=monthly*((Math.pow(1+r/n,n*y)-1)/(r/n));
    data.push(val);
    if(val>maxV)maxV=val;
  }

  var pad={t:30,r:20,b:35,l:60};
  var cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;

  // Grid
  ctx.strokeStyle=C.grid;ctx.lineWidth=1;
  for(var i=0;i<=4;i++){
    var gy=pad.t+ch*(1-i/4);
    ctx.beginPath();ctx.moveTo(pad.l,gy);ctx.lineTo(W-pad.r,gy);ctx.stroke();
    ctx.fillStyle=C.textLt;ctx.font='11px sans-serif';ctx.textAlign='right';
    ctx.fillText(fmt(maxV*i/4),pad.l-6,gy+4);
  }
  // X labels
  var step=Math.max(1,Math.ceil(t/8));
  ctx.textAlign='center';
  for(var y=0;y<=t;y+=step){
    var gx=pad.l+cw*(y/t);
    ctx.fillStyle=C.textLt;ctx.fillText(y+'',gx,H-pad.b+16);
  }

  // Principal baseline area
  ctx.beginPath();
  ctx.moveTo(pad.l,pad.t+ch);
  for(var y=0;y<=t;y++){
    var x=pad.l+cw*(y/t);
    var yy=pad.t+ch*(1-P0/maxV);
    ctx.lineTo(x,yy);
  }
  ctx.lineTo(pad.l+cw,pad.t+ch);ctx.closePath();
  ctx.fillStyle=C.grayLt;ctx.fill();

  // Growth area
  ctx.beginPath();
  ctx.moveTo(pad.l,pad.t+ch);
  for(var y=0;y<=t;y++){
    var x=pad.l+cw*(y/t);
    var yy=pad.t+ch*(1-data[y]/maxV);
    ctx.lineTo(x,yy);
  }
  ctx.lineTo(pad.l+cw,pad.t+ch);ctx.closePath();
  ctx.fillStyle=C.blueLt;ctx.fill();

  // Growth line
  ctx.beginPath();
  for(var y=0;y<=t;y++){
    var x=pad.l+cw*(y/t);
    var yy=pad.t+ch*(1-data[y]/maxV);
    y===0?ctx.moveTo(x,yy):ctx.lineTo(x,yy);
  }
  ctx.strokeStyle=C.blue;ctx.lineWidth=2.5;ctx.stroke();

  // End dot + label
  var ex=pad.l+cw,ey=pad.t+ch*(1-data[t]/maxV);
  ctx.beginPath();ctx.arc(ex,ey,5,0,Math.PI*2);ctx.fillStyle=C.blue;ctx.fill();
  ctx.fillStyle=C.text;ctx.font='bold 12px sans-serif';ctx.textAlign='right';
  ctx.fillText(fmt(data[t]),ex-8,ey-8);

  // Legend
  ctx.font='11px sans-serif';ctx.textAlign='left';
  ctx.fillStyle=C.blue;ctx.fillRect(pad.l,4,12,12);
  ctx.fillStyle=C.text;ctx.fillText('Total Value',pad.l+16,14);
  ctx.fillStyle=C.grayLt;ctx.fillRect(pad.l+100,4,12,12);
  ctx.strokeStyle=C.grid;ctx.strokeRect(pad.l+100,4,12,12);
  ctx.fillStyle=C.text;ctx.fillText('Principal',pad.l+116,14);
}

/* ── Amortization Chart ── */
function drawAmort(ctx,W,H){
  title.textContent='📊 還款結構分析';
  var loan=getVal('loanAmount')||getVal('principal')||getVal('amount')||getVal('homePrice')||1000000;
  var r=(getVal('rate')||getVal('interestRate')||getVal('annualRate')||3)/100/12;
  var months=(getVal('years')||getVal('term')||getVal('loanTerm')||30)*12;
  if(r<=0||months<=0)return;

  var pmt=loan*r*Math.pow(1+r,months)/(Math.pow(1+r,months)-1);
  var totalInt=pmt*months-loan;
  var bars=Math.min(Math.round(months/12),30);
  var data=[];var bal=loan;

  for(var yr=1;yr<=bars;yr++){
    var yrPrin=0,yrInt=0;
    for(var m=0;m<12&&bal>0;m++){
      var intPay=bal*r;
      var prinPay=Math.min(pmt-intPay,bal);
      yrPrin+=prinPay;yrInt+=intPay;bal-=prinPay;
    }
    data.push({p:yrPrin,i:yrInt});
  }

  var pad={t:30,r:20,b:35,l:55};
  var cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
  var maxY=pmt*12*1.1;
  var bw=Math.max(4,cw/bars-3);

  // Grid
  ctx.strokeStyle=C.grid;ctx.lineWidth=1;
  for(var g=0;g<=4;g++){
    var gy=pad.t+ch*(1-g/4);
    ctx.beginPath();ctx.moveTo(pad.l,gy);ctx.lineTo(W-pad.r,gy);ctx.stroke();
    ctx.fillStyle=C.textLt;ctx.font='11px sans-serif';ctx.textAlign='right';
    ctx.fillText(fmt(maxY*g/4),pad.l-6,gy+4);
  }

  for(var b=0;b<bars;b++){
    var x=pad.l+(cw/(bars))*(b+0.5)-bw/2;
    var hP=ch*(data[b].p/maxY);
    var hI=ch*(data[b].i/maxY);
    // Interest (bottom)
    ctx.fillStyle=C.redLt;
    ctx.fillRect(x,pad.t+ch-hI,bw,hI);
    // Principal (stacked on top)
    ctx.fillStyle=C.blueLt;
    ctx.fillRect(x,pad.t+ch-hI-hP,bw,hP);
    ctx.strokeStyle=C.blue;ctx.lineWidth=0.5;
    ctx.strokeRect(x,pad.t+ch-hI-hP,bw,hP);
    ctx.strokeStyle=C.red;
    ctx.strokeRect(x,pad.t+ch-hI,bw,hI);

    if(bars<=15||(b+1)%Math.ceil(bars/8)===0){
      ctx.fillStyle=C.textLt;ctx.font='10px sans-serif';ctx.textAlign='center';
      ctx.fillText((b+1)+'',x+bw/2,H-pad.b+14);
    }
  }

  // Legend
  ctx.font='11px sans-serif';ctx.textAlign='left';
  ctx.fillStyle=C.blue;ctx.fillRect(pad.l,4,12,12);
  ctx.fillStyle=C.text;ctx.fillText('Principal',pad.l+16,14);
  ctx.fillStyle=C.red;ctx.fillRect(pad.l+80,4,12,12);
  ctx.fillStyle=C.text;ctx.fillText('Interest',pad.l+96,14);
}

/* ── Bar Chart (result comparison) ── */
function drawBar(ctx,W,H){
  title.textContent='📊 計算結果視覺化';
  var items=[];
  var highlights=document.querySelectorAll('.result-highlight .result-value, .result-item .result-value');
  var labels=document.querySelectorAll('.result-highlight .result-label, .result-item .result-label');
  for(var i=0;i<Math.min(highlights.length,5);i++){
    var txt=(highlights[i].textContent||'').replace(/[^0-9.\-]/g,'');
    var val=parseFloat(txt);
    if(!isNaN(val)&&val!==0){
      var lbl=(labels[i]?labels[i].textContent:'Item '+(i+1)).substring(0,12);
      items.push({label:lbl,value:val});
    }
  }
  if(items.length===0)return;

  var colors=[C.blue,C.green,C.orange,C.red,C.purple];
  var maxV=Math.max.apply(null,items.map(function(d){return Math.abs(d.value);}));
  var pad={t:20,r:20,b:10,l:100};
  var cw=W-pad.l-pad.r;
  var barH=Math.min(36,((H-pad.t-pad.b)/items.length)-8);

  for(var i=0;i<items.length;i++){
    var y=pad.t+i*(barH+8);
    var bw=cw*(Math.abs(items[i].value)/maxV)*0.85;
    ctx.fillStyle=colors[i%colors.length]+'30';
    ctx.fillRect(pad.l,y,bw,barH);
    ctx.fillStyle=colors[i%colors.length];
    ctx.fillRect(pad.l,y,bw,4);

    ctx.fillStyle=C.text;ctx.font='12px sans-serif';ctx.textAlign='right';
    ctx.fillText(items[i].label,pad.l-8,y+barH/2+4);
    ctx.fillStyle=colors[i%colors.length];ctx.font='bold 12px sans-serif';ctx.textAlign='left';
    ctx.fillText(fmt(items[i].value),pad.l+bw+8,y+barH/2+4);
  }
}

/* ── Pie/Donut Chart ── */
function drawPie(ctx,W,H){
  title.textContent='📊 分配比例';
  var items=[];
  var highlights=document.querySelectorAll('.result-highlight .result-value, .result-item .result-value');
  var labels=document.querySelectorAll('.result-highlight .result-label, .result-item .result-label');
  for(var i=0;i<Math.min(highlights.length,6);i++){
    var txt=(highlights[i].textContent||'').replace(/[^0-9.\-]/g,'');
    var val=parseFloat(txt);
    if(!isNaN(val)&&val>0){
      items.push({label:(labels[i]?labels[i].textContent:'').substring(0,10),value:val});
    }
  }
  if(items.length<2){drawBar(ctx,W,H);return;}

  var total=items.reduce(function(s,d){return s+d.value;},0);
  var colors=[C.blue,C.green,C.orange,C.red,C.purple,'#EC4899'];
  var cx=W/2,cy=H/2,r=Math.min(cx,cy)-40;
  var startA=-Math.PI/2;

  for(var i=0;i<items.length;i++){
    var sweep=2*Math.PI*(items[i].value/total);
    ctx.beginPath();ctx.moveTo(cx,cy);
    ctx.arc(cx,cy,r,startA,startA+sweep);
    ctx.closePath();ctx.fillStyle=colors[i%colors.length];ctx.fill();

    // Label
    var midA=startA+sweep/2;
    var lx=cx+Math.cos(midA)*(r*0.65);
    var ly=cy+Math.sin(midA)*(r*0.65);
    ctx.fillStyle='#fff';ctx.font='bold 11px sans-serif';ctx.textAlign='center';
    ctx.fillText(fmtPct(items[i].value/total*100),lx,ly+4);
    startA+=sweep;
  }

  // Donut hole
  ctx.beginPath();ctx.arc(cx,cy,r*0.4,0,Math.PI*2);ctx.fillStyle='#fff';ctx.fill();

  // Legend below
  ctx.font='10px sans-serif';ctx.textAlign='left';
  var lx=10;
  for(var i=0;i<items.length;i++){
    ctx.fillStyle=colors[i%colors.length];ctx.fillRect(lx,H-16,10,10);
    ctx.fillStyle=C.text;ctx.fillText(items[i].label,lx+14,H-7);
    lx+=items[i].label.length*7+30;
    if(lx>W-60){lx=10;/* wrap */}
  }
}

/* ── Decline/Inflation Chart ── */
function drawDecline(ctx,W,H){
  title.textContent='📊 購買力變化';
  var P0=getVal('amount')||getVal('principal')||getVal('currentValue')||100000;
  var r=(getVal('rate')||getVal('inflationRate')||3)/100;
  var t=getVal('years')||getVal('period')||10;
  if(t<=0)t=10;if(t>50)t=50;

  var data=[];
  for(var y=0;y<=t;y++){data.push(P0/Math.pow(1+r,y));}
  var minV=data[t]*0.9;

  var pad={t:30,r:20,b:35,l:60};
  var cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;

  // Grid
  ctx.strokeStyle=C.grid;ctx.lineWidth=1;
  for(var i=0;i<=4;i++){
    var val=minV+(P0-minV)*(i/4);
    var gy=pad.t+ch*(1-i/4);
    ctx.beginPath();ctx.moveTo(pad.l,gy);ctx.lineTo(W-pad.r,gy);ctx.stroke();
    ctx.fillStyle=C.textLt;ctx.font='11px sans-serif';ctx.textAlign='right';
    ctx.fillText(fmt(val),pad.l-6,gy+4);
  }

  // Area
  ctx.beginPath();ctx.moveTo(pad.l,pad.t+ch);
  for(var y=0;y<=t;y++){
    var x=pad.l+cw*(y/t);
    var yy=pad.t+ch*(1-(data[y]-minV)/(P0-minV));
    ctx.lineTo(x,yy);
  }
  ctx.lineTo(pad.l+cw,pad.t+ch);ctx.closePath();
  ctx.fillStyle=C.redLt;ctx.fill();

  // Line
  ctx.beginPath();
  for(var y=0;y<=t;y++){
    var x=pad.l+cw*(y/t);
    var yy=pad.t+ch*(1-(data[y]-minV)/(P0-minV));
    y===0?ctx.moveTo(x,yy):ctx.lineTo(x,yy);
  }
  ctx.strokeStyle=C.red;ctx.lineWidth=2.5;ctx.stroke();

  // X labels
  var step=Math.max(1,Math.ceil(t/8));
  ctx.textAlign='center';
  for(var y=0;y<=t;y+=step){
    ctx.fillStyle=C.textLt;ctx.font='10px sans-serif';
    ctx.fillText(y+'',pad.l+cw*(y/t),H-pad.b+14);
  }

  // End label
  ctx.fillStyle=C.red;ctx.font='bold 12px sans-serif';ctx.textAlign='right';
  ctx.fillText(fmt(data[t]),pad.l+cw-5,pad.t+ch*(1-(data[t]-minV)/(P0-minV))-8);
}

})();
