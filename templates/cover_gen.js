// node cover_gen.js — renders 2000x1600 product covers
const {chromium}=require('playwright');
const items=[
 {file:'products/crm-cover.png',title:'Client CRM & Project Pipeline',sub:'Clients · Follow-ups · Quotes · Win rate',
  head:['Stage','Projects','Value','Weighted'],rows:[['Proposal sent','3','$12,500','$3,750'],['Negotiating','2','$8,000','$4,800'],['In progress','4','$9,600','$9,600']],c1:'#1f4e8c',c2:'#2a6fc9'},
 {file:'products/budget-cover.png',title:'Monthly Budget Planner',sub:'Budget vs actual · Savings rate · Year overview',
  head:['Category','Budget','Actual','Left'],rows:[['Groceries','$450','$386','$64'],['Transport','$160','$150','$10'],['Eating out','$150','$171','−$21']],c1:'#7a3b8f',c2:'#a352bd'}];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2000,height:1600}});
for(const it of items){await p.setContent(`<body style="margin:0;width:2000px;height:1600px;background:linear-gradient(135deg,${it.c1},${it.c2});font-family:system-ui,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff">
<h1 style="font-size:112px;margin:0;text-align:center;line-height:1.05">${it.title}</h1><p style="font-size:50px;margin:24px 0 60px;opacity:.9">${it.sub}</p>
<div style="background:#fff;color:#222;border-radius:24px;width:1500px;box-shadow:0 30px 80px rgba(0,0,0,.3);overflow:hidden"><table style="width:100%;border-collapse:collapse;font-size:40px">
<tr>${it.head.map(h=>`<th style="background:${it.c1};color:#fff;padding:18px">${h}</th>`).join('')}</tr>
${it.rows.map((r,i)=>`<tr>${r.map((c,j)=>`<td style="color:#222;padding:16px 24px;border-bottom:2px solid #eee;text-align:${j?'right':'left'};font-weight:${j?400:600};background:${i%2?'#f3f3f1':'#fff'}">${c}</td>`).join('')}</tr>`).join('')}</table></div>
<div style="display:flex;gap:24px;margin-top:60px">${['Google Sheets','Excel','Instant download'].map(t=>`<span style="background:rgba(255,255,255,.18);padding:16px 32px;border-radius:50px;font-size:40px">${t}</span>`).join('')}</div></body>`);
await p.screenshot({path:it.file});}await b.close()})();
