# Round 6 tools. Loaded by build.py with exec(), so num/sel/txt/tool are in scope.
# ---------- Money ----------
tool("mortgage-calculator", "Mortgage calculator", "Mortgage Calculator: Monthly Payment with Taxes and Insurance",
 "Free mortgage calculator. See your monthly payment including property tax and insurance, total interest and how much a bigger deposit saves.",
 "Work out your monthly mortgage payment, total interest and the full monthly cost of owning a home.",
 num("h", "Home price", 350000) + num("d", "Deposit / down payment", 70000) + num("r", "Interest rate", 6.5, "% per year") + num("y", "Term", 30, "years") + num("t", "Property tax", 3500, "per year") + num("i", "Insurance", 1200, "per year"),
 """const P=Math.max(0,v('h')-v('d')),n=v('y')*12,i=v('r')/1200;const m=n?(i?P*i/(1-Math.pow(1+i,-n)):P/n):0;const extra=(v('t')+v('i'))/12;
show(money(m+extra),'total monthly cost',[['Principal & interest',money(m)],['Tax & insurance per month',money(extra)],['Loan amount',money(P)],['Loan-to-value',nf(P/Math.max(v('h'),1)*100,1)+'%'],['Total interest over the term',money(m*n-P)]]);""",
 "<h2>What goes into a mortgage payment</h2><p>Your lender's payment covers principal and interest, calculated with the standard amortisation formula. On top of that most owners pay property tax and home insurance, often collected monthly through an escrow account. A bigger deposit lowers both the loan and the total interest.</p>",
 [("How much deposit do I need?", "It depends on the lender and country. Many lenders ask for 5–20%. Under 20% often means paying mortgage insurance, which isn't included here."),
  ("Should I choose 15 or 30 years?", "A 15-year term has higher payments but far less total interest. Try both terms above to compare.")], "Money")
tool("inflation-calculator", "Inflation calculator", "Inflation Calculator: What Money Will Be Worth",
 "Free inflation calculator. See how inflation erodes buying power, and what today's money will be worth or cost in the future.",
 "See what an amount will cost in the future, and what today's money will really be worth.",
 num("a", "Amount today", 1000) + num("r", "Inflation rate", 3, "% per year") + num("y", "Years", 10),
 """const f=Math.pow(1+v('r')/100,v('y'));
show(money(v('a')*f),'needed in '+v('y')+' years to buy the same',[['Buying power of today\\'s amount then',money(v('a')/f)],['Loss of buying power',nf((1-1/f)*100,1)+'%'],['Prices rise by',nf((f-1)*100,1)+'%']]);""",
 "<h2>Why inflation matters</h2><p>At 3% inflation prices roughly double every 24 years. Cash that earns less than inflation loses real value each year, which is why long-term savings usually need to be invested.</p>",
 [("What inflation rate should I use?", "Central banks in many countries target about 2%. Long-run averages have been around 3%. Use a range to see the effect.")], "Money")
tool("retirement-calculator", "Retirement calculator", "Retirement Savings Calculator: Am I on Track?",
 "Free retirement calculator. See how much you'll have at retirement and how much yearly income it can support with the 4% rule.",
 "Project your retirement pot and the yearly income it could pay you.",
 num("a", "Current age", 30) + num("ra", "Retirement age", 65) + num("s", "Saved so far", 20000) + num("c", "Monthly saving", 400) + num("r", "Annual return", 6, "%") + num("w", "Withdrawal rate", 4, "% per year"),
 """const months=Math.max(0,(v('ra')-v('a'))*12),i=v('r')/1200;let b=v('s');for(let m=0;m<months;m++)b=(b+v('c'))*(1+i);
const inc=b*v('w')/100;show(money(b),'at age '+v('ra'),[['Yearly income at '+v('w')+'%',money(inc)],['Monthly income',money(inc/12)],['Total you put in',money(v('s')+v('c')*months)],['Growth from returns',money(b-v('s')-v('c')*months)]]);""",
 "<h2>The 4% rule</h2><p>A common rule of thumb says you can withdraw about 4% of your pot in the first year of retirement and adjust for inflation after that, with a good chance the money lasts 30 years. It's a guide, not a guarantee.</p>",
 [("Are these figures in today's money?", "No, they're in future money. To think in today's money, use a return that's about 2–3 points lower to allow for inflation."),
  ("Does this include a state pension?", "No. Add any state or workplace pension income on top.")], "Money")
tool("credit-card-payoff-calculator", "Credit card payoff", "Credit Card Payoff Calculator: How Long to Pay It Off",
 "Free credit card payoff calculator. See how many months it takes to clear your balance and how much interest you'll pay.",
 "Find out how long it takes to clear a credit card and how much interest you'll pay.",
 num("b", "Balance", 4000) + num("r", "APR", 22.9, "%") + num("p", "Monthly payment", 150),
 """let b=v('b'),i=v('r')/1200,n=0,int=0;if(v('p')<=b*i){show('Never','the payment doesn\\'t cover the interest',[['Minimum to make progress',money(b*i+1)]]);return}
while(b>0.005&&n<1200){const x=b*i;int+=x;b=b+x-v('p');n++}
show(n+' months','to pay it off ('+nf(n/12,1)+' years)',[['Total interest',money(int)],['Total paid',money(v('b')+int)],['Pay this to clear it in 12 months',money(v('b')*i/(1-Math.pow(1+i,-12)))]]);""",
 "<h2>Pay more than the minimum</h2><p>Minimum payments are set low so balances last for years. Even a small increase in your monthly payment can cut the payoff time and interest dramatically. Try changing the payment above.</p>",
 [("Does a 0% balance transfer help?", "Often, yes. With 0% interest every payment goes to the balance. Check the transfer fee and when the offer ends.")], "Money")
tool("roi-calculator", "ROI calculator", "ROI Calculator: Return on Investment and Annualised Return",
 "Free ROI calculator. Work out return on investment, profit and annualised return (CAGR) for any investment.",
 "Calculate the return on an investment, including the yearly (annualised) rate.",
 num("i", "Amount invested", 10000) + num("f", "Final value", 14500) + num("y", "Years held", 3),
 """const roi=(v('f')-v('i'))/Math.max(v('i'),1e-9);const c=v('y')>0?Math.pow(v('f')/Math.max(v('i'),1e-9),1/v('y'))-1:roi;
show(nf(roi*100)+'%','total return',[['Profit',money(v('f')-v('i'))],['Annualised return (CAGR)',nf(c*100)+'% per year']]);""",
 "<h2>ROI vs annualised return</h2><p>ROI tells you the total gain. Annualised return (CAGR) spreads that over the years you held the investment, which lets you compare investments held for different lengths of time.</p>",
 [("What is CAGR?", "Compound annual growth rate: the steady yearly rate that would turn your starting amount into the final value over the same period.")], "Money")
tool("fuel-cost-calculator", "Fuel cost calculator", "Fuel Cost Calculator: Trip Cost by Distance and Consumption",
 "Free fuel cost calculator. Work out the cost of a trip from distance, fuel economy and fuel price, and split it between passengers.",
 "Work out how much fuel a trip will cost and the cost per person.",
 num("d", "Distance", 300, "km or miles") + sel("u", "Fuel economy unit", [("l100", "Litres per 100 km"), ("mpg", "Miles per gallon (US)"), ("mpguk", "Miles per gallon (UK)")]) + num("e", "Fuel economy", 6.5) + num("p", "Fuel price", 1.8, "per litre or gallon") + num("n", "People sharing", 1) + sel("r", "Trip", [("1", "One way"), ("2", "Return")]),
 """const D=v('d')*+$('r').value;let fuel;const u=$('u').value;if(u==='l100')fuel=D*v('e')/100;else if(u==='mpg')fuel=D/Math.max(v('e'),1e-9);else fuel=D/Math.max(v('e'),1e-9);
const cost=fuel*v('p');show(money(cost),'total fuel cost',[['Fuel used',nf(fuel,1)+(u==='l100'?' litres':' gallons')],['Per person',money(cost/Math.max(1,v('n')))],['Per '+(u==='l100'?'km':'mile'),money(cost/Math.max(D,1e-9))]]);""",
 "<h2>How it works</h2><p>Fuel used is the distance times your car's consumption. With litres per 100 km, distance is in kilometres and the price is per litre. With miles per gallon, distance is in miles and the price is per gallon.</p>",
 [("Where do I find my car's fuel economy?", "Check the trip computer, the manual, or the official figure for your model. Real-world economy is usually a little worse than the official figure.")], "Money")
# ---------- Education ----------
tool("gpa-calculator", "GPA calculator", "GPA Calculator: Work Out Your Grade Point Average",
 "Free GPA calculator on the 4.0 scale. Enter your grades and credit hours to get your semester GPA instantly.",
 "Enter each course as grade and credits, one per line, to get your GPA on the 4.0 scale.",
 txt("t", "Courses (grade credits, one per line)", "A 3\nB+ 4\nA- 3\nB 3\nC+ 2"),
 """const S={'A+':4,'A':4,'A-':3.7,'B+':3.3,'B':3,'B-':2.7,'C+':2.3,'C':2,'C-':1.7,'D+':1.3,'D':1,'D-':.7,'F':0};let pts=0,cr=0,bad=0;
$('t').value.split('\\n').forEach(l=>{const m=l.trim().toUpperCase().match(/^([A-DF][+-]?)\\s+([\\d.]+)/);if(!m){if(l.trim())bad++;return}if(!(m[1] in S)){bad++;return}pts+=S[m[1]]*+m[2];cr+=+m[2]});
show(cr?nf(pts/cr,2):'–','GPA on the 4.0 scale',[['Total credits',nf(cr,1)],['Quality points',nf(pts,1)]].concat(bad?[['Lines not understood',bad]]:[]));""",
 "<h2>How GPA is calculated</h2><p>Each letter grade has a point value (A = 4.0, B = 3.0 and so on). Multiply each course's points by its credit hours, add them up, and divide by the total credits.</p>",
 [("Does my school use the same scale?", "Most US schools use this 4.0 scale, but some give A+ 4.3 or use different plus/minus values. Check your school's handbook.")], "Education")
tool("grade-calculator", "Grade calculator", "Final Grade Calculator: What Do I Need on the Final?",
 "Free final grade calculator. Find the score you need on your final exam to reach the course grade you want.",
 "Find out what you need on the final exam to get the grade you want.",
 num("c", "Current grade", 82, "%") + num("w", "Final exam weight", 30, "% of the course") + num("g", "Grade you want", 85, "%"),
 """const w=v('w')/100;const need=w?(v('g')-v('c')*(1-w))/w:NaN;
show(nf(need,1)+'%','needed on the final',[['If you score 100%',nf(v('c')*(1-w)+100*w,1)+'%'],['If you score 0%',nf(v('c')*(1-w),1)+'%'],['Verdict',need>100?'Not reachable with this final alone':need<=0?'Already secured':'Reachable']]);""",
 "<h2>The formula</h2><p>Needed = (wanted − current × (1 − weight)) ÷ weight. With 82% now, a final worth 30% and a target of 85%, you need 92%.</p>",
 [("What if my current grade already includes some weight?", "Enter your current grade as the average over everything except the final, and the final's share of the whole course.")], "Education")
# ---------- Health ----------
tool("calorie-calculator", "Calorie calculator", "Calorie Calculator: TDEE and Daily Calories to Lose Weight",
 "Free calorie calculator. Work out your BMR and TDEE with the Mifflin-St Jeor formula, and daily calories to lose, keep or gain weight.",
 "Estimate how many calories you burn each day and how many to eat for your goal.",
 sel("s", "Sex", [("m", "Male"), ("f", "Female")]) + num("a", "Age", 30) + num("w", "Weight", 75, "kg") + num("h", "Height", 178, "cm") +
 sel("l", "Activity", [("1.2", "Little or no exercise"), ("1.375", "Light: 1–3 days a week"), ("1.55", "Moderate: 3–5 days a week"), ("1.725", "Hard: 6–7 days a week"), ("1.9", "Very hard or physical job")]),
 """const b=10*v('w')+6.25*v('h')-5*v('a')+($('s').value==='m'?5:-161),t=b*+$('l').value;
show(Math.round(t).toLocaleString()+' kcal','per day to keep your weight (TDEE)',[['BMR (at complete rest)',Math.round(b).toLocaleString()+' kcal'],['Lose about 0.5 kg a week',Math.round(t-500).toLocaleString()+' kcal'],['Lose about 0.25 kg a week',Math.round(t-250).toLocaleString()+' kcal'],['Gain about 0.25 kg a week',Math.round(t+250).toLocaleString()+' kcal']]);""",
 "<h2>BMR and TDEE</h2><p>BMR is what your body burns at rest. TDEE multiplies it by your activity level to estimate what you burn in a normal day. This uses the Mifflin-St Jeor equation, which is among the most accurate for most adults.</p>",
 [("Is this medical advice?", "No. It's an estimate. Talk to a doctor or dietitian before a big change, especially if you have a health condition."),
  ("How fast should I lose weight?", "About 0.25–0.5 kg (0.5–1 lb) a week is a common, sustainable target.")], "Health")
tool("water-intake-calculator", "Water intake", "Water Intake Calculator: How Much Water Should I Drink?",
 "Free water intake calculator. Get a daily water target based on your weight and exercise, in litres, ounces and glasses.",
 "Get a daily water target based on your body weight and exercise.",
 num("w", "Weight", 70, "kg") + num("e", "Exercise", 30, "minutes per day") + sel("c", "Climate", [("0", "Mild"), ("0.5", "Hot or humid")]),
 """const L=v('w')*0.033+v('e')/30*0.35+ +$('c').value;
show(nf(L,1)+' L','per day',[['US fluid ounces',Math.round(L*33.814)],['Glasses (250 ml)',Math.round(L/0.25)],['Bottles (500 ml)',nf(L/0.5,1)]]);""",
 "<h2>How it's worked out</h2><p>A common guide is about 33 ml per kg of body weight, plus around 350 ml for every 30 minutes of exercise, and extra in hot weather. Food provides some of your water too.</p>",
 [("Do tea and coffee count?", "Yes, mostly. Water-rich food like fruit and soup also counts towards your intake.")], "Health")
tool("due-date-calculator", "Due date calculator", "Pregnancy Due Date Calculator",
 "Free pregnancy due date calculator. Estimate your due date from the first day of your last period, and see how many weeks pregnant you are.",
 "Estimate your due date and how far along you are from the first day of your last period.",
 '<div><label for="d">First day of last period</label><input id="d" type="date"></div>' + num("c", "Cycle length", 28, "days"),
 """if(!$('d').value){const t=new Date(Date.now()-60*864e5);$('d').value=t.toISOString().slice(0,10)}const l=new Date($('d').value+'T12:00');
const due=new Date(l.getTime()+(280+v('c')-28)*864e5),days=Math.floor((Date.now()-l)/864e5),f=d=>d.toLocaleDateString(undefined,{day:'numeric',month:'long',year:'numeric'});
show(f(due),'estimated due date',[['Weeks pregnant today',days>=0?Math.floor(days/7)+' weeks, '+days%7+' days':'–'],['End of first trimester',f(new Date(l.getTime()+13*7*864e5))],['End of second trimester',f(new Date(l.getTime()+27*7*864e5))],['Days to go',Math.max(0,Math.ceil((due-Date.now())/864e5))]]);""",
 "<h2>How due dates are estimated</h2><p>This uses Naegele's rule: 280 days (40 weeks) from the first day of your last period, adjusted for cycles longer or shorter than 28 days. Only about 1 in 25 babies arrive on their due date, so treat it as a guide.</p>",
 [("Is an ultrasound date more accurate?", "Yes. An early dating scan is usually more accurate than a date from your last period. Follow your midwife or doctor's date.")], "Health")
tool("sleep-calculator", "Sleep calculator", "Sleep Calculator: Best Time to Go to Bed or Wake Up",
 "Free sleep calculator. Find the best times to go to bed or wake up based on 90-minute sleep cycles, so you wake up feeling refreshed.",
 "Find bedtimes that let you wake up at the end of a sleep cycle.",
 '<div><label for="t">I want to wake up at</label><input id="t" type="time" value="07:00"></div>' + num("f", "Minutes to fall asleep", 15),
 """const [h,m]=$('t').value.split(':').map(Number);const w=h*60+m,fmt=x=>{x=((x%1440)+1440)%1440;return String(Math.floor(x/60)).padStart(2,'0')+':'+String(x%60).padStart(2,'0')};
const opts=[6,5,4,3].map(c=>[fmt(w-c*90-v('f')),c+' cycles · '+nf(c*1.5,1)+' h sleep'+(c>=5?' ✓':'')]);
show(opts[0][0]+' or '+opts[1][0],'best bedtimes',opts.map(o=>[o[0],o[1]]));""",
 "<h2>Why sleep cycles matter</h2><p>Sleep runs in cycles of about 90 minutes. Waking at the end of a cycle, rather than in deep sleep, usually leaves you feeling less groggy. Most adults need 5 or 6 cycles a night.</p>",
 [("Is 90 minutes exact?", "No. Cycles vary from about 80 to 110 minutes between people and through the night, so use this as a starting point.")], "Health")
tool("running-pace-calculator", "Running pace", "Running Pace Calculator: Pace, Time and Speed",
 "Free running pace calculator. Work out your pace per km or mile from distance and time, plus predicted race times.",
 "Work out your pace from distance and time, and see predicted 5K to marathon times.",
 num("d", "Distance", 5, "km") + num("h", "Hours", 0) + num("m", "Minutes", 27) + num("s", "Seconds", 30),
 """const T=v('h')*3600+v('m')*60+v('s'),D=Math.max(v('d'),1e-9),f=x=>{x=Math.round(x);const h=Math.floor(x/3600),m=Math.floor(x%3600/60),s=x%60;return(h?h+':'+String(m).padStart(2,'0'):m)+':'+String(s).padStart(2,'0')};
const pred=d=>f(T*Math.pow(d/D,1.06));show(f(T/D)+' /km','pace',[['Pace per mile',f(T/D*1.609344)],['Speed',nf(D/(T/3600),2)+' km/h'],['Predicted 5K',pred(5)],['Predicted 10K',pred(10)],['Predicted half marathon',pred(21.0975)],['Predicted marathon',pred(42.195)]]);""",
 "<h2>Race predictions</h2><p>Predicted times use Riegel's formula: T2 = T1 × (D2 ÷ D1)<sup>1.06</sup>. It works best when you've trained for the longer distance.</p>",
 [("How do I convert pace per km to per mile?", "Multiply the pace by 1.609. A 5:30 /km pace is about 8:51 per mile.")], "Health")
# ---------- Text ----------
tool("remove-duplicate-lines", "Remove duplicate lines", "Remove Duplicate Lines from a List Online",
 "Free tool to remove duplicate lines from text or a list. Optionally ignore case and trim spaces. Runs in your browser.",
 "Paste a list and remove the duplicate lines, keeping the first of each.",
 txt("t", "Your list", "apple\nbanana\nApple\ncherry\nbanana\n  cherry") + sel("c", "Ignore case", [("1", "Yes"), ("0", "No")]) + sel("w", "Trim spaces", [("1", "Yes"), ("0", "No")]) + txt("o", "Result") + '<div><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """const seen=new Set(),out=[];const L=$('t').value.split('\\n');L.forEach(l=>{let k=$('w').value==='1'?l.trim():l;const x=$('c').value==='1'?k.toLowerCase():k;if(!seen.has(x)){seen.add(x);out.push(k)}});
$('o').value=out.join('\\n');show(out.length+' lines','left after removing duplicates',[['Original lines',L.length],['Duplicates removed',L.length-out.length]]);""",
 "<h2>Uses</h2><p>Clean up email lists, keyword lists, product SKUs or any list you've merged from several sources.</p>",
 [("Is my text uploaded?", "No. Everything happens in your browser.")], "Text")
tool("sort-lines", "Sort lines", "Sort Lines Alphabetically Online",
 "Free tool to sort lines of text alphabetically, in reverse, by length, numerically or randomly. Runs in your browser.",
 "Sort a list A–Z, Z–A, by length, by number or shuffle it.",
 txt("t", "Your list", "pear\napple\nfig\nbanana\ncherry") + sel("m", "Sort", [("az", "A to Z"), ("za", "Z to A"), ("len", "Shortest first"), ("num", "Numbers (smallest first)"), ("rnd", "Shuffle")]) + txt("o", "Result") + '<div><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """let L=$('t').value.split('\\n').filter(l=>l.trim()!=='');const c=new Intl.Collator(undefined,{numeric:true,sensitivity:'base'}),m=$('m').value;
if(m==='az')L.sort(c.compare);else if(m==='za')L.sort((a,b)=>c.compare(b,a));else if(m==='len')L.sort((a,b)=>a.length-b.length);else if(m==='num')L.sort((a,b)=>(parseFloat(a)||0)-(parseFloat(b)||0));else for(let i=L.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[L[i],L[j]]=[L[j],L[i]]}
$('o').value=L.join('\\n');show(L.length+' lines','sorted',[]);""",
 "<h2>Natural sorting</h2><p>A to Z uses natural order, so \"item 2\" comes before \"item 10\", and capital letters don't jump ahead of lowercase ones.</p>",
 [("Are blank lines kept?", "No. Empty lines are removed before sorting.")], "Text")
tool("slug-generator", "Slug generator", "URL Slug Generator: Turn Titles into Clean URLs",
 "Free URL slug generator. Turn any title into a clean, SEO-friendly URL slug, with accents removed.",
 "Turn a title into a clean, lowercase URL slug.",
 txt("t", "Title", "10 Best Free Tools for Freelancers in 2026: Zażółć Gęślą!") + sel("s", "Separator", [("-", "Hyphen (-)"), ("_", "Underscore (_)")]) + '<div style="grid-column:1/-1"><label for="o">Slug</label><input id="o" readonly></div><div><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """const s=$('s').value;const r=$('t').value.replace(/[łŁ]/g,'l').replace(/[ßẞ]/g,'ss').replace(/[æÆ]/g,'ae').replace(/[øØ]/g,'o').normalize('NFKD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,s).replace(new RegExp('^\\\\'+s+'+|\\\\'+s+'+$','g'),'');
$('o').value=r;show(r.length+' characters','slug length',[]);""",
 "<h2>What makes a good slug</h2><p>Keep it short, lowercase and readable, with words separated by hyphens. Google treats hyphens as word separators but not underscores, so hyphens are the usual choice.</p>",
 [("Should I remove words like 'the' and 'a'?", "Often, yes. Shorter slugs are easier to read and share. Keep the main keyword.")], "Text")
tool("url-encoder", "URL encoder", "URL Encode and Decode Online",
 "Free URL encoder and decoder. Percent-encode text for use in URLs and query strings, or decode it back.",
 "Percent-encode text for URLs, or decode an encoded URL.",
 sel("m", "Mode", [("e", "Encode"), ("d", "Decode")]) + sel("k", "Encode as", [("c", "Query value (encodeURIComponent)"), ("u", "Full URL (encodeURI)")]) + txt("t", "Input", "https://example.com/search?q=freelance rates & tips") + txt("o", "Output") + '<div><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """try{const t=$('t').value;$('o').value=$('m').value==='e'?($('k').value==='c'?encodeURIComponent(t):encodeURI(t)):decodeURIComponent(t.replace(/\\+/g,' '));show($('m').value==='e'?'Encoded':'Decoded',$('o').value.length+' characters',[])}catch(e){$('o').value='';show('Invalid input','malformed percent-encoding',[])}""",
 "<h2>Which mode?</h2><p>Use query value to encode a single parameter value: it encodes &amp;, = and / too. Use full URL to make a whole address safe while keeping its structure.</p>",
 [("Why are spaces %20 and not +?", "Both mean a space in query strings. %20 is safe everywhere, so the encoder uses it; the decoder accepts both.")], "Developer")
# ---------- Developer ----------
tool("uuid-generator", "UUID generator", "UUID Generator: Random v4 UUIDs in Bulk",
 "Free UUID v4 generator. Create one or thousands of random UUIDs (GUIDs) instantly, in upper or lower case.",
 "Generate random version 4 UUIDs, one or many at a time.",
 num("n", "How many", 5, "", "1") + sel("c", "Case", [("l", "lowercase"), ("u", "UPPERCASE")]) + sel("h", "Hyphens", [("1", "Yes"), ("0", "No")]) + '<div style="display:flex;align-items:end;gap:8px"><button class="btn" type="button" onclick="run()">Generate again</button><button class="btn ghost" type="button" onclick="copy(\'o\',this)">Copy</button></div>' + txt("o", "UUIDs"),
 """const n=Math.min(5000,Math.max(1,Math.round(v('n'))));const g=()=>crypto.randomUUID?crypto.randomUUID():'10000000-1000-4000-8000-100000000000'.replace(/[018]/g,c=>(c^crypto.getRandomValues(new Uint8Array(1))[0]&15>>c/4).toString(16));
let a=Array.from({length:n},g);if($('h').value==='0')a=a.map(x=>x.replace(/-/g,''));if($('c').value==='u')a=a.map(x=>x.toUpperCase());$('o').value=a.join('\\n');show(n+' UUID'+(n>1?'s':''),'generated with a secure random source',[]);""",
 "<h2>What is a UUID?</h2><p>A UUID is a 128-bit identifier. Version 4 UUIDs are random, with so many possible values that collisions are practically impossible, so they're safe to use as database keys without coordination.</p>",
 [("Are these secure?", "They use your browser's cryptographic random number generator."), ("Is a GUID the same thing?", "Yes. GUID is Microsoft's name for a UUID.")], "Developer")
tool("hash-generator", "Hash generator", "SHA-256 Hash Generator (SHA-1, SHA-384, SHA-512)",
 "Free hash generator. Create SHA-256, SHA-1, SHA-384 and SHA-512 hashes of any text, in your browser.",
 "Create SHA hashes of any text. Nothing is uploaded.",
 txt("t", "Text", "hello world") + sel("a", "Algorithm", [("SHA-256", "SHA-256"), ("SHA-1", "SHA-1"), ("SHA-384", "SHA-384"), ("SHA-512", "SHA-512")]) + '<div style="grid-column:1/-1"><label for="o">Hash (hex)</label><input id="o" readonly style="font-family:monospace"></div><div><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """if(!crypto.subtle){show('Not available','needs a secure (https) page',[]);return}crypto.subtle.digest($('a').value,new TextEncoder().encode($('t').value)).then(b=>{const h=[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');$('o').value=h;show($('a').value,h.length*4+' bits',[['Base64',btoa(String.fromCharCode(...new Uint8Array(b)))]])});""",
 "<h2>What is a hash?</h2><p>A hash function turns any input into a fixed-length fingerprint. The same input always gives the same hash, and a tiny change gives a completely different one. Hashes are used to check file integrity and store passwords (with salting).</p>",
 [("Can a hash be reversed?", "No. You can only check a guess by hashing it and comparing."), ("Is SHA-1 safe?", "Not for security. Use SHA-256 or stronger.")], "Developer")
tool("unix-timestamp-converter", "Unix timestamp converter", "Unix Timestamp Converter: Epoch to Date and Back",
 "Free Unix timestamp converter. Convert epoch seconds or milliseconds to a readable date in your time zone and UTC, and back.",
 "Convert a Unix timestamp to a date, or a date to a timestamp.",
 '<div><label for="s">Unix timestamp</label><input id="s" placeholder="e.g. 1767225600"></div><div><label for="d">Or a date and time</label><input id="d" type="datetime-local"></div>',
 """const src=event&&event.target?event.target.id:'';let ms;if(src==='d'&&$('d').value)ms=new Date($('d').value).getTime();else{let x=$('s').value.trim();if(!x){x=String(Math.floor(Date.now()/1000));$('s').value=x}ms=+x*(x.replace('-','').length>11?1:1000)}
if(!isFinite(ms)){show('Invalid','enter a number',[]);return}const dt=new Date(ms);if(src==='d')$('s').value=Math.floor(ms/1000);
show(dt.toLocaleString(),'your local time',[['UTC',dt.toUTCString()],['ISO 8601',dt.toISOString()],['Seconds',Math.floor(ms/1000)],['Milliseconds',ms],['Relative',(()=>{const s=Math.round((ms-Date.now())/1000),a=Math.abs(s),u=a<3600?[Math.round(a/60),'minutes']:a<86400*2?[Math.round(a/3600),'hours']:[Math.round(a/86400),'days'];return s<0?u[0]+' '+u[1]+' ago':'in '+u[0]+' '+u[1]})()]]);""",
 "<h2>What is Unix time?</h2><p>Unix time counts the seconds since 1 January 1970 at 00:00 UTC. It's how most computers and databases store dates. JavaScript and some APIs use milliseconds instead, which this tool detects automatically.</p>",
 [("Seconds or milliseconds?", "Timestamps with 13 digits are milliseconds; 10 digits are seconds. The converter detects which one you entered.")], "Developer")
tool("number-base-converter", "Number base converter", "Binary, Decimal, Hex and Octal Converter",
 "Free number base converter. Convert between binary, decimal, hexadecimal and octal, including very large numbers.",
 "Convert numbers between binary, decimal, hex and octal.",
 '<div><label for="n">Number</label><input id="n" value="255"></div>' + sel("b", "Base of that number", [("10", "Decimal (10)"), ("2", "Binary (2)"), ("16", "Hexadecimal (16)"), ("8", "Octal (8)")]),
 """const b=+$('b').value,s=$('n').value.trim().toLowerCase().replace(/^0[xbo]/,'').replace(/[\\s_]/g,'');const dig='0123456789abcdef'.slice(0,b);
if(!s||[...s].some(c=>!dig.includes(c))){show('Invalid','not a valid base-'+b+' number',[]);return}let x=0n;for(const c of s)x=x*BigInt(b)+BigInt(dig.indexOf(c));
show(x.toString(10),'decimal',[['Binary',x.toString(2).replace(/\\B(?=(\\d{4})+(?!\\d))/g,' ')],['Hexadecimal',x.toString(16).toUpperCase()],['Octal',x.toString(8)],['Bits needed',x.toString(2).length]]);""",
 "<h2>How bases work</h2><p>Decimal uses ten digits, binary uses two (0 and 1), octal uses eight and hexadecimal uses sixteen (0–9 then A–F). One hex digit is exactly four binary digits, which is why programmers use hex.</p>",
 [("Does it handle big numbers?", "Yes. It uses arbitrary-precision integers, so there's no size limit.")], "Developer")
tool("roman-numeral-converter", "Roman numerals", "Roman Numeral Converter",
 "Free Roman numeral converter. Convert numbers to Roman numerals and Roman numerals back to numbers, from 1 to 3999.",
 "Convert numbers to Roman numerals and back.",
 '<div><label for="n">Number or Roman numeral</label><input id="n" value="2026"></div>',
 """const s=$('n').value.trim().toUpperCase(),V=[[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']];
const toR=n=>{let r='';for(const[a,b]of V)while(n>=a){r+=b;n-=a}return r};
if(/^\\d+$/.test(s)){const n=+s;if(n<1||n>3999){show('Out of range','use 1 to 3999',[]);return}show(toR(n),'Roman numeral',[])}
else if(/^[MDCLXVI]+$/.test(s)){const M={M:1000,D:500,C:100,L:50,X:10,V:5,I:1};let t=0;for(let i=0;i<s.length;i++){const a=M[s[i]],b=M[s[i+1]]||0;t+=a<b?-a:a}
show(String(t),toR(t)===s?'in numbers':'in numbers (non-standard form; standard is '+toR(t)+')',[])}else show('Invalid','enter a number or Roman numeral',[]);""",
 "<h2>The rules</h2><p>I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000. A smaller numeral before a larger one is subtracted (IV = 4, XC = 90). Standard numerals never repeat a symbol more than three times.</p>",
 [("Why stop at 3999?", "Standard Roman numerals have no symbol above M (1000), so 3999 (MMMCMXCIX) is the largest you can write without special notation.")], "Text")
