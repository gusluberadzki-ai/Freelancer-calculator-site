"""Generates 20 small free tools under /tools/<slug>/. Run: python3 build.py
Each tool: inputs (HTML), a JS run() that writes into #out, plus explanatory text and FAQ for SEO."""
import pathlib, json, html, datetime
BASE = "https://gusluberadzki-ai.github.io/Freelancer-calculator-site/tools/"
OUT = pathlib.Path(__file__).parent

def num(id, label, val, hint="", step="any"):
    h = f" <small>({hint})</small>" if hint else ""
    return f'<div><label for="{id}">{label}{h}</label><input id="{id}" type="number" step="{step}" value="{val}"></div>'
def sel(id, label, opts):
    return f'<div><label for="{id}">{label}</label><select id="{id}">' + "".join(f'<option value="{v}">{t}</option>' for v, t in opts) + '</select></div>'
def txt(id, label, val=""):
    return f'<div style="grid-column:1/-1"><label for="{id}">{label}</label><textarea id="{id}">{html.escape(val)}</textarea></div>'
RES = '<div class="result" aria-live="polite"><div class="big" id="big">–</div><div id="lbl"></div><table id="rows"></table></div>'
# helper JS available to every tool
HELPERS = """const $=id=>document.getElementById(id);const v=id=>parseFloat($(id).value)||0;
const money=n=>isFinite(n)?n.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2}):'–';
const nf=(n,d=2)=>isFinite(n)?(+n.toFixed(d)).toLocaleString(undefined,{maximumFractionDigits:d}):'–';
function show(big,lbl,rows){$('big').textContent=big;$('lbl').textContent=lbl||'';$('rows').innerHTML=(rows||[]).map(r=>'<tr><td>'+r[0]+'</td><td>'+r[1]+'</td></tr>').join('')}
function copy(id,btn){navigator.clipboard&&navigator.clipboard.writeText($(id).value||$(id).textContent);if(btn){btn.textContent='Copied';setTimeout(()=>btn.textContent='Copy',1200)}}"""

T = []
def tool(slug, name, title, desc, lead, inputs, js, body, faq, cat, result=True):
    T.append(dict(slug=slug, name=name, title=title, desc=desc, lead=lead, inputs=inputs, js=js, body=body, faq=faq, cat=cat, result=result))

# ---------- Money ----------
tool("loan-calculator", "Loan calculator", "Loan Calculator: Monthly Payment and Total Interest",
 "Free loan calculator. Work out the monthly payment, total interest and total cost of any loan, car loan or personal loan.",
 "See your monthly payment and how much interest you'll pay over the life of a loan.",
 num("p", "Loan amount", 20000) + num("r", "Interest rate", 7.5, "% per year") + num("y", "Term", 5, "years") + num("f", "Upfront fees", 0),
 """const n=v('y')*12,i=v('r')/1200,P=v('p');const m=i?P*i/(1-Math.pow(1+i,-n)):P/n;
show(money(m),'monthly payment',[['Total of payments',money(m*n)],['Total interest',money(m*n-P)],['Total cost incl. fees',money(m*n+v('f'))],['Number of payments',n]]);""",
 "<h2>How loan payments are calculated</h2><p>This uses the standard amortisation formula: payment = P × r ÷ (1 − (1 + r)<sup>−n</sup>), where P is the amount borrowed, r is the monthly interest rate and n is the number of monthly payments. Early payments are mostly interest; later payments are mostly principal.</p>",
 [("How can I lower my monthly payment?", "Choose a longer term or find a lower interest rate. A longer term lowers the payment but increases the total interest you pay."),
  ("Does this include fees?", "Add any upfront fees in the fees box to see the total cost. Ongoing fees vary by lender and aren't included.")], "Money")
tool("compound-interest-calculator", "Compound interest", "Compound Interest Calculator with Monthly Contributions",
 "Free compound interest calculator. See how your savings or investments grow with regular monthly contributions.",
 "See how money grows over time with compound interest and regular contributions.",
 num("p", "Starting amount", 5000) + num("c", "Monthly contribution", 200) + num("r", "Annual return", 6, "%") + num("y", "Years", 20) + sel("k", "Compounding", [("12", "Monthly"), ("1", "Yearly"), ("365", "Daily")]),
 """const k=+$('k').value,r=v('r')/100,Y=v('y');let b=v('p'),paid=v('p');const months=Math.round(Y*12);
for(let m=1;m<=months;m++){b+=v('c');paid+=v('c');if(k===12)b*=1+r/12;else if(k===1&&m%12===0)b*=1+r;else if(k===365)b*=Math.pow(1+r/365,365/12);}
show(money(b),'balance after '+Y+' years',[['Total you put in',money(paid)],['Interest earned',money(b-paid)],['Growth multiple',nf(b/Math.max(paid,1))+'×']]);""",
 "<h2>The power of compounding</h2><p>Compound interest means you earn returns on your past returns, not just on what you put in. Over long periods this snowballs: the longer the time frame, the bigger the share of your final balance that comes from interest rather than contributions.</p>",
 [("What return should I use?", "It depends on what you invest in. Savings accounts pay less; long-term stock market returns have historically been higher but go up and down. Use a cautious figure for planning."),
  ("Are contributions added at the start or end of the month?", "This calculator adds each contribution at the start of the month, before that month's interest.")], "Money")
tool("savings-goal-calculator", "Savings goal", "Savings Goal Calculator: How Much to Save Each Month",
 "Work out how much you need to save each month to reach a savings goal by a target date, with or without interest.",
 "Find out how much to put aside each month to hit your goal.",
 num("g", "Savings goal", 10000) + num("h", "Already saved", 1000) + num("m", "Months to reach it", 24) + num("r", "Interest rate", 3, "% per year"),
 """const i=v('r')/1200,n=Math.max(1,v('m')),fv=v('g')-v('h')*Math.pow(1+i,n);const pmt=i?fv*i/(Math.pow(1+i,n)-1):fv/n;
show(money(Math.max(0,pmt)),'to save each month',[['Per week',money(Math.max(0,pmt)*12/52)],['Total you will deposit',money(Math.max(0,pmt)*n)],['Interest earned',money(Math.max(0,v('g')-v('h')-Math.max(0,pmt)*n))]]);""",
 "<h2>Make it automatic</h2><p>The easiest way to hit a savings goal is to set up an automatic transfer on payday for the amount shown above, into a separate savings account.</p>",
 [("Does interest make a big difference?", "Over a year or two, not much. Over five years or more it can noticeably reduce how much you need to save.")], "Money")
tool("vat-calculator", "VAT / sales tax", "VAT Calculator: Add or Remove VAT and Sales Tax",
 "Free VAT and sales tax calculator. Add tax to a net price or remove it from a gross price at any rate.",
 "Add VAT or sales tax to a price, or work out the tax inside a price that already includes it.",
 num("a", "Amount", 100) + num("r", "Tax rate", 20, "%") + sel("m", "I want to", [("add", "Add tax (amount is net)"), ("remove", "Remove tax (amount includes tax)")]),
 """const r=v('r')/100,a=v('a');let net,gross;if($('m').value==='add'){net=a;gross=a*(1+r)}else{gross=a;net=a/(1+r)}
show(money($('m').value==='add'?gross:net),$('m').value==='add'?'price including tax':'price excluding tax',[['Net (excl. tax)',money(net)],['Tax',money(gross-net)],['Gross (incl. tax)',money(gross)]]);""",
 "<h2>Removing VAT correctly</h2><p>To remove 20% VAT from a price, divide by 1.20. A common mistake is to subtract 20% of the gross price, which gives the wrong answer: £120 includes £20 VAT, not £24.</p>",
 [("How do I add VAT to a price?", "Multiply the net price by 1 plus the rate. At 20%, multiply by 1.2."),
  ("Does this work for US sales tax?", "Yes. Enter your combined state and local rate.")], "Money")
tool("discount-calculator", "Discount calculator", "Discount Calculator: Sale Price and Savings",
 "Free discount calculator. Find the sale price after a percentage off, including double discounts, and how much you save.",
 "Work out the sale price and your savings after a discount.",
 num("p", "Original price", 80) + num("d", "Discount", 25, "% off") + num("d2", "Extra discount", 0, "% off the sale price") + num("t", "Sales tax", 0, "%"),
 """const s=v('p')*(1-v('d')/100)*(1-v('d2')/100),tot=s*(1+v('t')/100);
show(money(tot),'you pay',[['Sale price before tax',money(s)],['You save',money(v('p')-s)],['Effective discount',nf((1-s/Math.max(v('p'),1e-9))*100)+'%']]);""",
 "<h2>Stacked discounts don't add up</h2><p>25% off followed by an extra 10% off is not 35% off. The second discount applies to the already reduced price, so the total discount is 32.5%.</p>",
 [("How do I calculate a percentage off?", "Multiply the price by (1 − discount ÷ 100). 25% off $80 is $80 × 0.75 = $60.")], "Money")
tool("profit-margin-calculator", "Profit margin", "Profit Margin and Markup Calculator",
 "Free profit margin calculator. Work out gross margin, markup and profit from cost and selling price, or find the price for a target margin.",
 "Find your margin and markup, or the selling price you need for a target margin.",
 num("c", "Cost", 40) + num("p", "Selling price", 100) + num("m", "Or target margin", 0, "% (fills in a price)"),
 """let c=v('c'),p=v('p');if(v('m')>0&&v('m')<100)p=c/(1-v('m')/100);
show(nf((p-c)/Math.max(p,1e-9)*100)+'%','gross margin',[['Selling price',money(p)],['Profit',money(p-c)],['Markup',nf((p-c)/Math.max(c,1e-9)*100)+'%']]);""",
 "<h2>Margin vs markup</h2><p>Margin is profit as a share of the selling price. Markup is profit as a share of the cost. Something that costs $40 and sells for $100 has a 60% margin but a 150% markup.</p>",
 [("What's a good profit margin?", "It varies hugely by industry. Digital products can run 80–90% margins; retail is often 20–50%.")], "Money")
tool("break-even-calculator", "Break-even", "Break-Even Calculator: Units and Revenue to Break Even",
 "Free break-even calculator. Find how many units you need to sell to cover fixed costs, and the break-even revenue.",
 "Work out how many sales you need before you start making a profit.",
 num("f", "Fixed costs", 5000, "per month") + num("p", "Price per unit", 50) + num("c", "Variable cost per unit", 20) + num("t", "Target profit", 0, "optional"),
 """const cm=v('p')-v('c');const u=cm>0?(v('f')+v('t'))/cm:NaN;
show(isFinite(u)?Math.ceil(u).toLocaleString()+' units':'Price must be above cost','to break even'+(v('t')?' and hit your target':''),[['Break-even revenue',money(Math.ceil(u)*v('p'))],['Contribution per unit',money(cm)],['Contribution margin',nf(cm/Math.max(v('p'),1e-9)*100)+'%']]);""",
 "<h2>How break-even works</h2><p>Each sale contributes its price minus its variable cost towards your fixed costs. Divide the fixed costs by that contribution and you get the number of sales needed to break even.</p>",
 [("What are fixed costs?", "Costs that don't change with sales volume, like rent, software subscriptions and salaries.")], "Money")
tool("tip-calculator", "Tip calculator", "Tip Calculator: Split the Bill",
 "Free tip calculator. Work out the tip and split the bill between any number of people.",
 "Calculate the tip and split the bill fairly.",
 num("b", "Bill amount", 64) + num("t", "Tip", 18, "%") + num("n", "People", 2, "", "1") + sel("r", "Round each share", [("0", "Don't round"), ("1", "Up to the nearest whole")]),
 """const tip=v('b')*v('t')/100,tot=v('b')+tip,n=Math.max(1,Math.round(v('n')));let each=tot/n;if($('r').value==='1')each=Math.ceil(each);
show(money(each),'per person',[['Tip',money(tip)],['Total',money(tot)],['Total if rounded',money(each*n)]]);""",
 "<h2>How much to tip</h2><p>Customs vary a lot by country. In the US, 15–20% at restaurants is typical. In much of Europe, rounding up or leaving 5–10% is common.</p>",
 [("Should I tip on the pre-tax amount?", "Many people tip on the pre-tax total. Enter whichever amount you prefer.")], "Money")
# ---------- Health & everyday ----------
tool("bmi-calculator", "BMI calculator", "BMI Calculator (Metric and Imperial)",
 "Free BMI calculator in kg/cm or lb/ft. See your body mass index and the standard adult BMI category.",
 "Calculate your body mass index in metric or imperial units.",
 sel("u", "Units", [("m", "Metric (kg, cm)"), ("i", "Imperial (lb, in)")]) + num("w", "Weight", 70) + num("h", "Height", 175, "cm or inches"),
 """let kg=v('w'),m=v('h')/100;if($('u').value==='i'){kg=v('w')*0.45359237;m=v('h')*0.0254}const b=kg/(m*m);
const cat=b<18.5?'Underweight':b<25?'Healthy weight':b<30?'Overweight':'Obese';const lo=18.5*m*m,hi=24.9*m*m,k=$('u').value==='i'?2.20462:1;
show(nf(b,1),cat,[['Healthy range for your height',nf(lo*k,1)+' – '+nf(hi*k,1)+($('u').value==='i'?' lb':' kg')]]);""",
 "<h2>About BMI</h2><p>BMI is weight divided by height squared. It's a quick screening number for adults, but it doesn't account for muscle mass, age, sex or ethnicity, so talk to a doctor for a proper assessment.</p>",
 [("What is a healthy BMI?", "For most adults, 18.5 to 24.9 is considered a healthy range."), ("Is BMI accurate for athletes?", "Not always. Muscle weighs more than fat, so muscular people can have a high BMI without excess body fat.")], "Everyday")
tool("age-calculator", "Age calculator", "Age Calculator: Exact Age in Years, Months and Days",
 "Free age calculator. Find your exact age in years, months and days, total days lived and days until your next birthday.",
 "Find your exact age, and how long until your next birthday.",
 '<div><label for="d">Date of birth</label><input id="d" type="date" value="1995-06-15"></div><div><label for="at">Age on</label><input id="at" type="date"></div>',
 """if(!$('at').value)$('at').value=new Date().toISOString().slice(0,10);const a=new Date($('d').value+'T12:00'),b=new Date($('at').value+'T12:00');if(isNaN(a)||isNaN(b))return;
let y=b.getFullYear()-a.getFullYear(),mo=b.getMonth()-a.getMonth(),d=b.getDate()-a.getDate();if(d<0){mo--;d+=new Date(b.getFullYear(),b.getMonth(),0).getDate()}if(mo<0){y--;mo+=12}
let nb=new Date(b.getFullYear(),a.getMonth(),a.getDate(),12);if(nb<b)nb.setFullYear(nb.getFullYear()+1);const days=Math.round((b-a)/864e5);
show(y+' years',mo+' months and '+d+' days',[['Total months',(y*12+mo).toLocaleString()],['Total weeks',Math.floor(days/7).toLocaleString()],['Total days',days.toLocaleString()],['Next birthday in',Math.round((nb-b)/864e5)+' days']]);""",
 "<h2>How age is calculated</h2><p>Your age counts full years since your birth date, then the remaining full months and days. Total days counts every day between the two dates.</p>",
 [("Can I calculate age on a future date?", "Yes. Change the 'Age on' date to any date.")], "Everyday")
tool("unit-converter", "Unit converter", "Unit Converter: Length, Weight, Temperature, Volume",
 "Free unit converter for length, weight, temperature, volume and speed. Convert between metric and imperial units instantly.",
 "Convert between metric and imperial units.",
 sel("k", "Type", [("len", "Length"), ("mass", "Weight"), ("temp", "Temperature"), ("vol", "Volume"), ("spd", "Speed")]) + num("x", "Value", 1) + '<div><label for="fu">From</label><select id="fu"></select></div><div><label for="tu">To</label><select id="tu"></select></div>',
 """const U={len:{m:1,km:1000,cm:.01,mm:.001,mi:1609.344,yd:.9144,ft:.3048,in:.0254},mass:{kg:1,g:.001,mg:1e-6,lb:.45359237,oz:.028349523125,st:6.35029318,t:1000},
vol:{L:1,mL:.001,'US gal':3.785411784,'UK gal':4.54609,'US cup':.2365882365,'fl oz (US)':.0295735295625,m3:1000},spd:{'km/h':1/3.6,mph:.44704,'m/s':1,knot:.514444},temp:{'°C':0,'°F':0,K:0}};
const k=$('k').value;if($('fu').dataset.k!==k){const o=Object.keys(U[k]).map(u=>'<option>'+u+'</option>').join('');$('fu').innerHTML=o;$('tu').innerHTML=o;$('tu').selectedIndex=1;$('fu').dataset.k=k}
const f=$('fu').value,t=$('tu').value,x=v('x');let r;
if(k==='temp'){const c=f==='°C'?x:f==='°F'?(x-32)*5/9:x-273.15;r=t==='°C'?c:t==='°F'?c*9/5+32:c+273.15}else r=x*U[k][f]/U[k][t];
show(nf(r,6)+' '+t,x+' '+f+' =',Object.keys(U[k]).filter(u=>u!==f&&u!==t).slice(0,5).map(u=>{let q;if(k==='temp'){const c=f==='°C'?x:f==='°F'?(x-32)*5/9:x-273.15;q=u==='°C'?c:u==='°F'?c*9/5+32:c+273.15}else q=x*U[k][f]/U[k][u];return[u,nf(q,6)]}));""",
 "<h2>Common conversions</h2><ul><li>1 inch = 2.54 cm exactly</li><li>1 mile = 1.609 km</li><li>1 kg = 2.205 lb</li><li>°F = °C × 9/5 + 32</li></ul>",
 [("Are US and UK gallons the same?", "No. A US gallon is 3.785 litres and a UK (imperial) gallon is 4.546 litres.")], "Everyday")
tool("time-zone-converter", "Time zone converter", "Time Zone Converter and Meeting Planner",
 "Free time zone converter. See what time it is in other cities and plan meetings across time zones.",
 "Pick a time in one city and see it in others. Handy for client calls across time zones.",
 '<div><label for="t">Time</label><input id="t" type="datetime-local"></div>' + sel("z", "In time zone", [(z, z.split('/')[-1].replace('_', ' ')) for z in ["Europe/London", "Europe/Warsaw", "Europe/Berlin", "America/New_York", "America/Chicago", "America/Los_Angeles", "Asia/Dubai", "Asia/Kolkata", "Asia/Singapore", "Asia/Tokyo", "Australia/Sydney", "UTC"]]),
 """const Z=['Europe/London','Europe/Warsaw','Europe/Berlin','America/New_York','America/Chicago','America/Los_Angeles','Asia/Dubai','Asia/Kolkata','Asia/Singapore','Asia/Tokyo','Australia/Sydney','UTC'];
if(!$('t').value){const n=new Date();n.setMinutes(0);$('t').value=new Date(n-n.getTimezoneOffset()*6e4).toISOString().slice(0,16)}
const src=$('z').value,[d,tm]=$('t').value.split('T');if(!tm)return;const guess=new Date($('t').value+':00Z');
const off=z=>{const p=new Intl.DateTimeFormat('en-US',{timeZone:z,hourCycle:'h23',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}).formatToParts(guess).reduce((a,x)=>(a[x.type]=x.value,a),{});return Date.UTC(p.year,p.month-1,p.day,p.hour,p.minute)-guess.getTime()};
const utc=new Date(guess.getTime()-off(src));const fmt=z=>new Intl.DateTimeFormat(undefined,{timeZone:z,weekday:'short',hour:'2-digit',minute:'2-digit'}).format(utc);
show(fmt(src),src.split('/').pop().replace('_',' '),Z.filter(z=>z!==src).map(z=>[z.split('/').pop().replace('_',' '),fmt(z)]));""",
 "<h2>Daylight saving time</h2><p>Times account for daylight saving automatically, using your browser's built-in time zone data. Remember that Europe and North America switch on different dates, so the gap between them changes for a few weeks each spring and autumn.</p>",
 [("What's the best time for a call between Europe and the US?", "Usually between 2 pm and 5 pm UK time, which is morning on the US east coast.")], "Everyday")
tool("pomodoro-timer", "Pomodoro timer", "Pomodoro Timer: 25 Minute Focus Timer",
 "Free online Pomodoro timer. 25-minute focus sessions with short and long breaks, a sound when time's up, and a session counter.",
 "Work in focused 25-minute sessions with short breaks in between.",
 num("w", "Focus minutes", 25, "", "1") + num("s", "Short break", 5, "minutes", "1") + num("l", "Long break", 15, "minutes", "1"),
 """if(!window.P){window.P={left:v('w')*60,mode:'Focus',run:false,done:0,t:null};
$('go').onclick=()=>{P.run=!P.run;$('go').textContent=P.run?'Pause':'Start';if(P.run)P.t=setInterval(tick,1000);else clearInterval(P.t)};
$('rs').onclick=()=>{clearInterval(P.t);P.run=false;P.mode='Focus';P.left=v('w')*60;$('go').textContent='Start';draw()};}
function beep(){try{const a=new AudioContext(),o=a.createOscillator();o.connect(a.destination);o.frequency.value=880;o.start();o.stop(a.currentTime+.4)}catch(e){}}
function tick(){P.left--;if(P.left<=0){beep();if(P.mode==='Focus'){P.done++;P.mode=P.done%4?'Short break':'Long break';P.left=(P.done%4?v('s'):v('l'))*60}else{P.mode='Focus';P.left=v('w')*60}}draw()}
function draw(){const m=String(Math.floor(P.left/60)).padStart(2,'0'),s=String(P.left%60).padStart(2,'0');show(m+':'+s,P.mode,[['Sessions completed',P.done]]);document.title=m+':'+s+' · '+P.mode}
if(!P.run&&P.mode==='Focus'&&event&&event.target&&event.target.id==='w')P.left=v('w')*60;draw();""",
 '<div class="actions" style="display:flex;gap:10px;margin-top:-6px"><button class="btn" id="go" type="button">Start</button><button class="btn ghost" id="rs" type="button">Reset</button></div><h2>How the Pomodoro technique works</h2><p>Work on one task for 25 minutes, then take a 5-minute break. After four focus sessions, take a longer 15 to 30 minute break. The timer keeps running in the tab title so you can see it from other tabs.</p>',
 [("Will it make a sound?", "Yes, a short beep plays when each session ends. Keep the tab open.")], "Everyday")
# ---------- Text ----------
tool("case-converter", "Case converter", "Case Converter: UPPERCASE, lowercase, Title Case, Sentence case",
 "Free case converter. Change text to uppercase, lowercase, title case, sentence case, camelCase or snake_case instantly.",
 "Paste text and convert its letter case in one click.",
 txt("t", "Your text", "the quick brown fox jumps over the lazy dog. it was a sunny day.") + '<div style="grid-column:1/-1;display:flex;gap:6px;flex-wrap:wrap" id="modes">' + "".join(f'<button class="btn ghost" type="button" data-m="{m}">{l}</button>' for m, l in [("up", "UPPERCASE"), ("low", "lowercase"), ("title", "Title Case"), ("sent", "Sentence case"), ("camel", "camelCase"), ("snake", "snake_case"), ("kebab", "kebab-case")]) + '</div>' + txt("o", "Result") + '<div><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """const SMALL=new Set('a an and as at but by for in nor of on or the to up via'.split(' '));window.M=window.M||'title';
if(!window._b){window._b=1;$('modes').onclick=e=>{if(e.target.dataset.m){M=e.target.dataset.m;run()}}}
const t=$('t').value,w=s=>s.toLowerCase().match(/[\\p{L}\\p{N}]+/gu)||[];let r;
switch(M){case'up':r=t.toUpperCase();break;case'low':r=t.toLowerCase();break;
case'title':r=t.toLowerCase().replace(/[\\p{L}\\p{N}']+/gu,(x,i)=>i>0&&SMALL.has(x)?x:x[0].toUpperCase()+x.slice(1));break;
case'sent':r=t.toLowerCase().replace(/(^\\s*|[.!?]\\s+)(\\p{L})/gu,(m,a,b)=>a+b.toUpperCase());break;
case'camel':r=w(t).map((x,i)=>i?x[0].toUpperCase()+x.slice(1):x).join('');break;case'snake':r=w(t).join('_');break;case'kebab':r=w(t).join('-');break}
$('o').value=r;document.querySelectorAll('#modes button').forEach(b=>b.classList.toggle('ghost',b.dataset.m!==M));""",
 "<h2>When to use each case</h2><ul><li><b>Title Case</b> for headings and titles</li><li><b>Sentence case</b> for normal text and most UI labels</li><li><b>camelCase, snake_case, kebab-case</b> for code, file names and URLs</li></ul>",
 [("Does Title Case keep small words lowercase?", "Yes. Words like 'a', 'and', 'of' and 'the' stay lowercase unless they start the title.")], "Text", result=False)
tool("lorem-ipsum-generator", "Lorem ipsum generator", "Lorem Ipsum Generator: Placeholder Text",
 "Free lorem ipsum generator. Create placeholder paragraphs, sentences or words for designs and mock-ups, then copy with one click.",
 "Generate placeholder text for designs, websites and mock-ups.",
 num("n", "How many", 3, "", "1") + sel("u", "Of", [("p", "Paragraphs"), ("s", "Sentences"), ("w", "Words")]) + sel("st", "Start with 'Lorem ipsum dolor sit amet'", [("1", "Yes"), ("0", "No")]) + txt("o", "Result") + '<div><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """const W='lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum'.split(' ');
let seed=7;const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;const word=()=>W[Math.floor(rnd()*W.length)];
const sent=()=>{const n=8+Math.floor(rnd()*9),a=[...Array(n)].map(word);a[0]=a[0][0].toUpperCase()+a[0].slice(1);return a.join(' ')+'.'};
const para=()=>[...Array(4+Math.floor(rnd()*3))].map(sent).join(' ');const n=Math.max(1,Math.min(200,Math.round(v('n'))));let r;
if($('u').value==='p')r=[...Array(n)].map(para).join('\\n\\n');else if($('u').value==='s')r=[...Array(n)].map(sent).join(' ');else r=[...Array(n)].map(word).join(' ');
if($('st').value==='1')r='Lorem ipsum dolor sit amet'+($('u').value==='w'?' ':', ')+r.replace(/^\\w/,c=>c.toLowerCase());$('o').value=r;""",
 "<h2>What is lorem ipsum?</h2><p>Lorem ipsum is scrambled Latin used as placeholder text since the 1500s. It fills a layout so you can judge the design without being distracted by real words.</p>",
 [("Is lorem ipsum real Latin?", "It's based on a passage by Cicero, but words have been removed and changed, so it doesn't mean anything.")], "Text", result=False)
tool("password-generator", "Password generator", "Strong Password Generator (Random and Secure)",
 "Free strong password generator. Create random, secure passwords or passphrases in your browser. Nothing is sent or stored.",
 "Create strong random passwords. They're generated on your device using secure randomness and never leave your browser.",
 num("n", "Length", 16, "characters", "1") + sel("s", "Use", [("all", "Letters, numbers and symbols"), ("an", "Letters and numbers"), ("pin", "Numbers only (PIN)"), ("phrase", "Passphrase of words")]) + '<div style="grid-column:1/-1"><label for="o">Password</label><input id="o" readonly style="font-family:ui-monospace,monospace;font-size:1.2rem"></div><div style="display:flex;gap:8px"><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button><button class="btn ghost" type="button" id="re">New password</button></div>',
 """if(!window._r){window._r=1;$('re').onclick=run}const R=n=>{const a=new Uint32Array(1);crypto.getRandomValues(a);return a[0]%n};
const WL='apple brave cloud dance eagle flame grape house input jolly koala lemon magic noble ocean piano quest river stone tiger urban vivid whale xenon young zebra amber blaze coral delta ember frost glide haven ivory jumbo karma lunar maple nectar orbit pearl quilt raven solar torch ultra vapor willow yodel zesty'.split(' ');
const s=$('s').value,n=Math.max(4,Math.min(128,Math.round(v('n'))));let pool,out='',bits;
if(s==='phrase'){const k=Math.max(3,Math.round(n/4));out=[...Array(k)].map(()=>WL[R(WL.length)]).join('-')+'-'+R(100);bits=k*Math.log2(WL.length)+Math.log2(100)}
else{pool=s==='pin'?'0123456789':'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789'+(s==='all'?'!@#$%^&*-_=+?':'');for(let i=0;i<n;i++)out+=pool[R(pool.length)];bits=n*Math.log2(pool.length)}
$('o').value=out;show(Math.round(bits)+' bits',bits>=80?'Very strong':bits>=60?'Strong':bits>=40?'OK for low-value accounts':'Weak',[]);""",
 "<h2>What makes a password strong</h2><p>Length matters most. A random 16-character password, or a passphrase of four or more random words, is far stronger than a short password with symbols. Use a different password for every account and keep them in a password manager.</p>",
 [("Is it safe to generate passwords online?", "This page generates passwords locally with your browser's cryptographic random number generator. Nothing is sent over the internet.")], "Text")
tool("random-picker", "Random name picker", "Random Name Picker and Number Generator",
 "Free random name picker and random number generator. Pick winners from a list or generate random numbers in a range.",
 "Pick a random winner from a list, or generate random numbers.",
 txt("t", "Names or items (one per line)", "Alice\nBen\nChloe\nDaniel\nEmma") + num("k", "How many to pick", 1, "", "1") + num("a", "Or random number from", 1, "", "1") + num("b", "to", 100, "", "1") + '<div style="display:flex;gap:8px;align-items:end"><button class="btn" type="button" id="pick">Pick from list</button><button class="btn ghost" type="button" id="numb">Random number</button></div>',
 """const R=n=>{const a=new Uint32Array(1);crypto.getRandomValues(a);return a[0]%n};
if(!window._p){window._p=1;$('pick').onclick=()=>{const L=$('t').value.split('\\n').map(x=>x.trim()).filter(Boolean),k=Math.min(L.length,Math.max(1,Math.round(v('k'))));const c=[...L],w=[];for(let i=0;i<k;i++)w.push(c.splice(R(c.length),1)[0]);show(w.join(', ')||'–',k>1?'winners':'winner',[['Picked from',L.length+' entries']])};
$('numb').onclick=()=>{const a=Math.round(Math.min(v('a'),v('b'))),b=Math.round(Math.max(v('a'),v('b')));show(String(a+R(b-a+1)),'random number between '+a+' and '+b,[])}}
if($('big').textContent==='–')show('Ready','press a button',[]);""",
 "<h2>Fair and random</h2><p>Picks use your browser's cryptographic random number generator, so every entry has an equal chance. When you pick several winners, nobody can be picked twice.</p>",
 [("Can I use it for giveaways?", "Yes. Paste the entrants' names, one per line, and pick. Take a screenshot of the result for transparency.")], "Text")
# ---------- Developer ----------
tool("json-formatter", "JSON formatter", "JSON Formatter and Validator",
 "Free JSON formatter, validator and minifier. Pretty-print or minify JSON and find syntax errors, all in your browser.",
 "Format, validate or minify JSON. Your data never leaves your browser.",
 txt("t", "JSON", '{"name":"RateKit","tools":20,"free":true,"tags":["calculator","pdf"]}') + sel("m", "Output", [("2", "Pretty (2 spaces)"), ("4", "Pretty (4 spaces)"), ("0", "Minified")]) + '<div style="display:flex;align-items:end"><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>' + txt("o", "Result"),
 """try{const j=JSON.parse($('t').value);const m=+$('m').value;$('o').value=m?JSON.stringify(j,null,m):JSON.stringify(j);show('Valid JSON',Array.isArray(j)?'array with '+j.length+' items':typeof j==='object'&&j?'object with '+Object.keys(j).length+' keys':typeof j,[['Size',new Blob([$('o').value]).size.toLocaleString()+' bytes']])}
catch(e){$('o').value='';show('Invalid JSON',e.message,[])}""",
 "<h2>Common JSON errors</h2><ul><li>Trailing commas after the last item</li><li>Single quotes instead of double quotes</li><li>Keys without quotes</li><li>Comments, which JSON doesn't allow</li></ul>",
 [("Is my JSON uploaded?", "No. Parsing and formatting happen locally in your browser.")], "Developer")
tool("base64-encoder", "Base64 encoder", "Base64 Encode and Decode Online",
 "Free Base64 encoder and decoder. Convert text to Base64 and back, with full UTF-8 support, instantly in your browser.",
 "Encode text to Base64 or decode Base64 back to text.",
 sel("m", "Mode", [("e", "Encode text to Base64"), ("d", "Decode Base64 to text")]) + sel("u", "URL-safe", [("0", "No"), ("1", "Yes (- and _ instead of + and /)")]) + txt("t", "Input", "Hello, world! Zażółć ✓") + txt("o", "Output") + '<div><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """const url=$('u').value==='1';try{if($('m').value==='e'){let b=btoa(String.fromCharCode(...new TextEncoder().encode($('t').value)));if(url)b=b.replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'');$('o').value=b;show('Encoded',b.length+' characters',[])}
else{let s=$('t').value.trim().replace(/-/g,'+').replace(/_/g,'/');while(s.length%4)s+='=';const r=new TextDecoder('utf-8',{fatal:true}).decode(Uint8Array.from(atob(s),c=>c.charCodeAt(0)));$('o').value=r;show('Decoded',r.length+' characters',[])}}
catch(e){$('o').value='';show('Not valid Base64','check the input',[])}""",
 "<h2>What is Base64?</h2><p>Base64 turns any data into plain letters, numbers and a few symbols so it can travel safely through systems that only handle text, such as email or URLs. It's an encoding, not encryption: anyone can decode it.</p>",
 [("Does it support emoji and accents?", "Yes. Text is converted to UTF-8 before encoding.")], "Developer")
tool("color-converter", "Color converter", "Color Converter: HEX to RGB to HSL",
 "Free colour converter and picker. Convert between HEX, RGB and HSL, and see tints, shades and a contrast check.",
 "Pick a colour or paste a code to convert between HEX, RGB and HSL.",
 '<div><label for="c">Pick a colour</label><input id="c" type="color" value="#0b6e4f" style="height:46px;padding:4px"></div><div><label for="h">Or paste HEX / rgb()</label><input id="h" value="#0b6e4f"></div><div style="grid-column:1/-1;display:flex;gap:4px" id="sw"></div>',
 """const src=event&&event.target?event.target.id:'c';let hex=$('c').value;
if(src==='h'){const s=$('h').value.trim();let m=s.match(/^#?([0-9a-f]{3}|[0-9a-f]{6})$/i),n=s.match(/rgba?\\(\\s*(\\d+)[,\\s]+(\\d+)[,\\s]+(\\d+)/i);
if(m){let x=m[1];if(x.length===3)x=x.split('').map(c=>c+c).join('');hex='#'+x.toLowerCase()}else if(n)hex='#'+[n[1],n[2],n[3]].map(q=>Math.min(255,+q).toString(16).padStart(2,'0')).join('');else return;$('c').value=hex}else $('h').value=hex;
const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);const R=r/255,G=g/255,B=b/255,mx=Math.max(R,G,B),mn=Math.min(R,G,B),l=(mx+mn)/2,d=mx-mn;
let h=0,s=0;if(d){s=d/(1-Math.abs(2*l-1));h=mx===R?((G-B)/d)%6:mx===G?(B-R)/d+2:(R-G)/d+4;h=Math.round(h*60);if(h<0)h+=360}
const lum=x=>{x/=255;return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4)},L=.2126*lum(r)+.7152*lum(g)+.0722*lum(b),cw=1.05/(L+.05),cb=(L+.05)/.05;
show(hex.toUpperCase(),'',[['RGB',`rgb(${r}, ${g}, ${b})`],['HSL',`hsl(${h}, ${Math.round(s*100)}%, ${Math.round(l*100)}%)`],['Contrast with white',nf(cw,2)+':1'+(cw>=4.5?' ✓ AA':'')],['Contrast with black',nf(cb,2)+':1'+(cb>=4.5?' ✓ AA':'')]]);
$('sw').innerHTML=[.8,.6,.4,.2,0,-.2,-.4,-.6].map(t=>{const f=c=>Math.round(t>0?c+(255-c)*t:c*(1+t));const x='#'+[r,g,b].map(c=>f(c).toString(16).padStart(2,'0')).join('');return`<div title="${x}" style="flex:1;height:36px;border-radius:6px;background:${x}"></div>`}).join('');""",
 "<h2>HEX, RGB and HSL</h2><p>HEX and RGB describe the same thing: amounts of red, green and blue from 0 to 255. HSL describes hue (0–360°), saturation and lightness, which is easier for making lighter or darker versions of a colour.</p>",
 [("What contrast ratio do I need?", "WCAG AA asks for at least 4.5:1 for normal text and 3:1 for large text.")], "Developer")
tool("character-counter", "Character counter", "Character Counter for Twitter/X, Instagram, SEO and SMS",
 "Free character counter with limits for X (Twitter), Instagram, LinkedIn, meta descriptions, title tags and SMS.",
 "Count characters and check your text against common platform limits.",
 txt("t", "Your text", "Free tools for freelancers: calculators, invoices, PDFs and more."),
 """const t=$('t').value,n=[...t].length;const L=[['Title tag (SEO)',60],['Meta description (SEO)',160],['X / Twitter post',280],['SMS (one message)',160],['Instagram caption',2200],['LinkedIn post',3000]];
show(n.toLocaleString(),'characters',L.map(([k,m])=>[k,n<=m?(m-n)+' left ✓':(n-m)+' over ✗']).concat([['Words',(t.match(/\\S+/g)||[]).length]]));""",
 "<h2>Why limits matter</h2><p>Search engines cut off titles after about 60 characters and descriptions after about 160, and social platforms truncate or reject posts that are too long. Check before you publish.</p>",
 [("Do emoji count as one character?", "This counter counts each emoji as one character, which matches what most platforms show you.")], "Text")

exec((OUT / "more_tools.py").read_text())
exec((OUT / "round8_tools.py").read_text())

CSS = """.grid textarea{width:100%;min-height:130px;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);font:inherit}
.btn{display:inline-block;cursor:pointer;border:0;border-radius:8px;padding:10px 16px;font-weight:600;font-size:.95rem;background:var(--accent);color:#fff}.btn.ghost{background:transparent;border:1px solid var(--line);color:var(--ink)}
.grid>*{min-width:0}#rows td{overflow-wrap:anywhere}"""
def head(t, d, p):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(t)} | RateKit</title><meta name="description" content="{html.escape(d)}"><link rel="canonical" href="{BASE}{p}">
<link rel="stylesheet" href="../../freelance-calc/style.css"><style>{CSS}</style>
<!-- ADSENSE: paste the AdSense <script> tag here once approved --></head><body>
<header><a class="logo" href="../../freelance-calc/">Rate<span>Kit</span></a><nav><a href="../">All tools</a><a href="../../blog/">Guides</a></nav></header><main>"""
FOOT = """<p class="allaccess" style="background:var(--accent-soft);border-radius:10px;padding:12px 14px;margin-top:28px;font-size:.93rem"><strong>RateKit All-Access:</strong> Pro in every RateKit app plus 50+ spreadsheet and printable templates, CHF 6/month. <a href="../../pro/">See what's included</a></p></main><footer>RateKit offers free tools for freelancers and small businesses. Results are estimates. · <a href="../../freelance-calc/privacy.html">Privacy</a></footer></body></html>"""
for t in T:
    d = OUT / t["slug"]; d.mkdir(exist_ok=True)
    others = [o for o in T if o["cat"] == t["cat"] and o is not t][:4] or T[:4]
    faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in t["faq"])
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]})
    (d / "index.html").write_text(head(t["title"], t["desc"], t["slug"] + "/") + f"""
<h1>{t['name']}</h1><p class="lead">{t['lead']}</p>
<section class="calc"><div class="grid">{t['inputs']}</div>{RES if t['result'] else '<div id="big" hidden></div><div id="lbl" hidden></div><table id="rows" hidden></table>'}</section>
<div class="ad"><!-- ad slot --></div>{t['body']}<h2>Frequently asked questions</h2>{faq_html}
<h2>Related tools</h2><div class="cards">{''.join(f'<a href="../{o["slug"]}/"><strong>{o["name"]}</strong><span>{html.escape(o["lead"][:80])}</span></a>' for o in others)}</div>
<script type="application/ld+json">{ld}</script>
<script>{HELPERS}
function run(){{{t['js']}}}
document.addEventListener('input',run);document.addEventListener('change',run);run();</script>""" + FOOT)
cats = {}
for t in T: cats.setdefault(t["cat"], []).append(t)
extra = [("Invoice generator", "../invoice-generator/"), ("Merge and split PDF", "../pdf-tools/"), ("Image compressor", "../image-compressor/"), ("Background remover", "../background-remover/"),
         ("QR code generator", "../qr-code-generator/"), ("Percentage calculator", "../percentage-calculator/"), ("Date calculator", "../date-calculator/"), ("Word counter", "../word-counter/"),
         ("Freelance hourly rate", "../freelance-calc/hourly-rate-calculator.html"), ("Salary to hourly", "../salary/")]
idx = '<h1>Free online tools</h1><p class="lead">Fast, private tools that run in your browser. No sign-up, nothing uploaded.</p>'
for c, ts in cats.items():
    idx += f"<h2>{c}</h2><div class='cards'>" + "".join(f'<a href="{t["slug"]}/"><strong>{t["name"]}</strong><span>{html.escape(t["lead"][:80])}</span></a>' for t in ts) + "</div>"
idx += "<h2>More tools</h2><div class='cards'>" + "".join(f'<a href="{u}"><strong>{n}</strong></a>' for n, u in extra) + "</div>"
(OUT / "index.html").write_text(head("Free Online Tools: Calculators, Converters and Generators", "Free online tools: loan, interest, VAT, BMI and age calculators, unit and time zone converters, password generator, JSON formatter and more.", "").replace('href="../../', 'href="../').replace('<a href="../">All tools</a>', '<a href="./">All tools</a>') + idx + FOOT.replace('../../', '../'))
today = datetime.date.today().isoformat()
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod></url>" for u in [""] + [t["slug"] + "/" for t in T]) + "</urlset>\n")
print(len(T), "tools")
