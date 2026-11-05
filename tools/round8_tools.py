# Round 8 tools. Loaded by build.py with exec(), so num/sel/txt/tool are in scope.
# ---------- Home ----------
tool("square-footage-calculator", "Square footage", "Square Footage Calculator: Area in Sq Ft and Square Metres",
 "Free square footage calculator. Work out the area of a room or several rooms in square feet and square metres, with a cost estimate.",
 "Find the area of a room in square feet and square metres, and what it will cost to cover.",
 num("l", "Length", 12) + num("w", "Width", 10) + sel("u", "Units", [("ft", "Feet"), ("m", "Metres")]) + num("n", "Number of identical rooms", 1, "", "1") + num("c", "Price per unit area", 0, "optional, e.g. flooring"),
 """const a=v('l')*v('w')*Math.max(1,v('n')),ft=$('u').value==='ft',sqft=ft?a:a*10.7639,sqm=ft?a/10.7639:a;
show(nf(ft?sqft:sqm)+(ft?' sq ft':' m²'),'total area',[['Square feet',nf(sqft)],['Square metres',nf(sqm)],['Square yards',nf(sqft/9)],['Cost',v('c')?money(a*v('c')):'–'],['With 10% waste',v('c')?money(a*v('c')*1.1):nf((ft?sqft:sqm)*1.1)]]);""",
 "<h2>How to measure a room</h2><p>Measure the longest length and width of the floor, then multiply them. For an L-shaped room, split it into two rectangles, work out each one and add them together. When buying flooring, add about 10% for cuts and waste.</p>",
 [("How many square feet in a square metre?", "One square metre is 10.764 square feet."), ("How do I measure an irregular room?", "Divide it into rectangles, calculate each one separately and add the areas together.")], "Home")
tool("paint-calculator", "Paint calculator", "Paint Calculator: How Much Paint Do I Need?",
 "Free paint calculator. Work out how many litres or gallons of paint you need for a room, minus doors and windows, for one or more coats.",
 "Estimate how much paint you need to cover the walls of a room.",
 num("l", "Room length", 4, "m or ft") + num("w", "Room width", 3.5, "m or ft") + num("h", "Wall height", 2.5, "m or ft") + sel("u", "Units", [("m", "Metres (litres)"), ("ft", "Feet (US gallons)")]) + num("d", "Doors", 1, "", "1") + num("wi", "Windows", 1, "", "1") + num("k", "Coats", 2, "", "1"),
 """const m=$('u').value==='m',door=m?1.9:20,win=m?1.5:15,cov=m?11:375;const wall=Math.max(0,2*(v('l')+v('w'))*v('h')-v('d')*door-v('wi')*win),need=wall*Math.max(1,v('k'))/cov;
show(nf(need,1)+(m?' litres':' gallons'),'of paint',[['Wall area to paint',nf(wall,1)+(m?' m²':' sq ft')],['Coats',Math.max(1,v('k'))],[m?'2.5 L tins':'1 gal cans',Math.ceil(need/(m?2.5:1))],['Ceiling (1 coat, extra)',nf(v('l')*v('w')/cov,1)+(m?' L':' gal')]]);""",
 "<h2>Assumptions</h2><p>One litre of emulsion covers about 11 m² and one US gallon about 375 sq ft per coat on smooth walls. A standard door takes off about 1.9 m² (20 sq ft) and a window about 1.5 m² (15 sq ft). Rough or porous surfaces and dark-to-light colour changes need more paint.</p>",
 [("How many coats do I need?", "Two coats is standard for an even finish. New plaster or a big colour change may need a primer as well."), ("Does this include the ceiling?", "No. The ceiling estimate is shown separately.")], "Home")
tool("tile-calculator", "Tile calculator", "Tile Calculator: How Many Tiles Do I Need?",
 "Free tile calculator. Work out how many floor or wall tiles you need for an area, including grout gaps and a waste allowance, plus how many boxes.",
 "Work out how many tiles and boxes you need, with a waste allowance.",
 num("al", "Area length", 3, "m") + num("aw", "Area width", 2.5, "m") + num("tl", "Tile length", 30, "cm") + num("tw", "Tile width", 30, "cm") + num("g", "Grout gap", 3, "mm") + num("x", "Waste", 10, "%") + num("b", "Tiles per box", 10, "", "1"),
 """const tile=((v('tl')+v('g')/10)/100)*((v('tw')+v('g')/10)/100),area=v('al')*v('aw');const n=Math.ceil(area/Math.max(tile,1e-9)*(1+v('x')/100));
show(n.toLocaleString(),'tiles',[['Area',nf(area)+' m²'],['Tiles without waste',Math.ceil(area/Math.max(tile,1e-9))],['Boxes',Math.ceil(n/Math.max(1,v('b')))],['Tiles per m²',nf(1/Math.max(tile,1e-9),1)]]);""",
 "<h2>How much waste to allow</h2><p>Add 10% for a simple rectangular room with straight laying. Add 15% for diagonal or herringbone patterns, or a room with lots of corners and cuts. Keep a few spare tiles for future repairs, since batches vary in colour.</p>",
 [("Should I include the grout gap?", "Yes. Gaps add up over a large area and slightly reduce the number of tiles you need.")], "Home")
tool("concrete-calculator", "Concrete calculator", "Concrete Calculator: Slab Volume and Bags Needed",
 "Free concrete calculator. Work out the volume of a slab, footing or patio in cubic metres, cubic yards and the number of premix bags.",
 "Work out how much concrete you need for a slab, and how many bags.",
 num("l", "Length", 3, "m") + num("w", "Width", 3, "m") + num("d", "Depth", 10, "cm") + num("x", "Extra for spillage", 5, "%") + num("b", "Bag yield", 0.01, "m³ per bag (20 kg ≈ 0.01)"),
 """const vol=v('l')*v('w')*v('d')/100*(1+v('x')/100);
show(nf(vol,3)+' m³','of concrete',[['Cubic yards',nf(vol*1.30795,2)],['Cubic feet',nf(vol*35.3147,1)],['Premix bags',Math.ceil(vol/Math.max(v('b'),1e-9))],['Approx. weight',nf(vol*2400,0)+' kg']]);""",
 "<h2>Typical depths</h2><p>Patios and paths are usually 7–10 cm (3–4 in) deep. Driveways and garage floors are usually 10–15 cm (4–6 in). For large jobs above about 1 m³, ready-mix delivery is often cheaper than bags.</p>",
 [("How many 20 kg bags make a cubic metre?", "About 100. A 20 kg bag of premix yields roughly 0.01 m³."), ("How many cubic yards in a cubic metre?", "One cubic metre is 1.308 cubic yards.")], "Home")
tool("electricity-cost-calculator", "Electricity cost", "Electricity Cost Calculator: What Does an Appliance Cost to Run?",
 "Free electricity cost calculator. Work out how much an appliance costs to run per hour, day, month and year from its wattage and your tariff.",
 "See what any appliance costs to run, from its wattage and your electricity price.",
 num("w", "Power", 2000, "watts") + num("h", "Hours used per day", 1) + num("d", "Days used per week", 7, "", "1") + num("p", "Electricity price", 0.25, "per kWh"),
 """const kwhD=v('w')/1000*v('h'),perDay=kwhD*v('p'),yr=perDay*v('d')*52;
show(money(yr),'per year',[['Per hour of use',money(v('w')/1000*v('p'))],['Per day of use',money(perDay)],['Per month',money(yr/12)],['Energy per year',nf(kwhD*v('d')*52,1)+' kWh']]);""",
 "<h2>How it works</h2><p>Cost = power in kilowatts × hours used × price per kWh. A 2,000 W heater used for one hour uses 2 kWh. The wattage is printed on the appliance label or in the manual. Devices on standby still draw a few watts.</p>",
 [("Where do I find my electricity price?", "It's on your bill or your supplier's app, shown as a price per kWh (unit rate).")], "Home")
# ---------- Health ----------
tool("bmr-calculator", "BMR calculator", "BMR Calculator: Basal Metabolic Rate and Daily Calories",
 "Free BMR calculator using the Mifflin-St Jeor equation. Find how many calories your body burns at rest and per day at your activity level.",
 "Find how many calories your body burns at rest, and per day with activity.",
 sel("s", "Sex", [("m", "Male"), ("f", "Female")]) + num("a", "Age", 30, "years", "1") + num("wt", "Weight", 75, "kg") + num("ht", "Height", 178, "cm") + sel("act", "Activity", [("1.2", "Sedentary"), ("1.375", "Light (1–3 days/week)"), ("1.55", "Moderate (3–5 days/week)"), ("1.725", "Very active"), ("1.9", "Athlete")]),
 """const b=10*v('wt')+6.25*v('ht')-5*v('a')+($('s').value==='m'?5:-161),t=b*+$('act').value;
show(Math.round(b).toLocaleString()+' kcal','BMR per day at rest',[['Daily calories with activity',Math.round(t).toLocaleString()],['To lose ~0.5 kg/week',Math.round(t-500).toLocaleString()],['To gain ~0.5 kg/week',Math.round(t+500).toLocaleString()]]);""",
 "<h2>What is BMR?</h2><p>Basal metabolic rate is the energy your body uses at complete rest just to keep you alive: breathing, circulation and keeping warm. It's usually 60–70% of the calories you burn in a day. This calculator uses the Mifflin-St Jeor equation, which studies have found to be the most accurate of the common formulas.</p>",
 [("Is BMR the same as TDEE?", "No. TDEE (total daily energy expenditure) is BMR multiplied by an activity factor. Both are shown above."), ("Is this medical advice?", "No. It's an estimate. Speak to a doctor or dietitian before major diet changes.")], "Health")
tool("body-fat-calculator", "Body fat calculator", "Body Fat Calculator (US Navy Method)",
 "Free body fat percentage calculator using the US Navy tape-measure method. Needs only height, neck, waist and hip measurements.",
 "Estimate your body fat percentage with a tape measure.",
 sel("s", "Sex", [("m", "Male"), ("f", "Female")]) + num("ht", "Height", 178, "cm") + num("n", "Neck", 38, "cm") + num("w", "Waist (at navel)", 85, "cm") + num("hp", "Hips (women)", 95, "cm") + num("wt", "Weight", 75, "kg, optional"),
 """const m=$('s').value==='m',L=Math.log10;let bf=m?495/(1.0324-0.19077*L(v('w')-v('n'))+0.15456*L(v('ht')))-450:495/(1.29579-0.35004*L(v('w')+v('hp')-v('n'))+0.221*L(v('ht')))-450;
if(!isFinite(bf)){show('–','check the measurements',[]);return}const cat=m?(bf<6?'Essential fat':bf<14?'Athletic':bf<18?'Fit':bf<25?'Average':'Above average'):(bf<14?'Essential fat':bf<21?'Athletic':bf<25?'Fit':bf<32?'Average':'Above average');
show(nf(bf,1)+'%','body fat',[['Category',cat],['Fat mass',v('wt')?nf(v('wt')*bf/100,1)+' kg':'–'],['Lean mass',v('wt')?nf(v('wt')*(1-bf/100),1)+' kg':'–']]);""",
 "<h2>How to measure</h2><p>Measure your neck just below the larynx, and your waist at the navel for men or at the narrowest point for women. Women also measure the widest part of the hips. Keep the tape level and snug but not tight. The Navy method is usually within 3–4% of lab methods.</p>",
 [("How accurate is it?", "Reasonably accurate for most people, but it can be off for very muscular or very lean bodies. Use it to track change over time.")], "Health")
tool("macro-calculator", "Macro calculator", "Macro Calculator: Protein, Carbs and Fat per Day",
 "Free macro calculator. Split your daily calories into grams of protein, carbohydrate and fat for weight loss, maintenance or muscle gain.",
 "Turn your daily calories into protein, carb and fat targets.",
 num("c", "Daily calories", 2200) + sel("g", "Goal", [("30,40,30", "Balanced (30/40/30)"), ("40,30,30", "Fat loss, high protein (40/30/30)"), ("30,50,20", "Muscle gain (30/50/20)"), ("25,5,70", "Keto (25/5/70)")]) + num("m", "Meals per day", 3, "", "1"),
 """const [p,c,f]=$('g').value.split(',').map(Number),C=v('c'),pg=C*p/400,cg=C*c/400,fg=C*f/900,M=Math.max(1,v('m'));
show(Math.round(pg)+' g protein','per day',[['Carbohydrate',Math.round(cg)+' g'],['Fat',Math.round(fg)+' g'],['Protein per meal',Math.round(pg/M)+' g'],['Carbs per meal',Math.round(cg/M)+' g'],['Fat per meal',Math.round(fg/M)+' g']]);""",
 "<h2>Calories per gram</h2><p>Protein and carbohydrate both provide about 4 kcal per gram, and fat provides about 9 kcal per gram. The percentages above are shares of calories, not grams. Not sure of your calories? Use the BMR calculator first.</p>",
 [("How much protein do I need?", "Common guidance for active people is 1.6–2.2 g per kg of body weight per day.")], "Health")
tool("ideal-weight-calculator", "Ideal weight", "Ideal Weight Calculator: Healthy Weight for Your Height",
 "Free ideal weight calculator. See your healthy weight range from BMI plus the Devine, Robinson and Miller formulas for your height.",
 "See a healthy weight range for your height using several common formulas.",
 sel("s", "Sex", [("m", "Male"), ("f", "Female")]) + num("ht", "Height", 175, "cm"),
 """const h=v('ht'),inch=Math.max(0,h/2.54-60),m=$('s').value==='m',hm=h/100;const D=(m?50:45.5)+2.3*inch,R=(m?52:49)+(m?1.9:1.7)*inch,Mi=(m?56.2:53.1)+(m?1.41:1.36)*inch;
show(nf(18.5*hm*hm,1)+'–'+nf(24.9*hm*hm,1)+' kg','healthy BMI range',[['Devine formula',nf(D,1)+' kg'],['Robinson formula',nf(R,1)+' kg'],['Miller formula',nf(Mi,1)+' kg'],['In pounds (BMI range)',nf(18.5*hm*hm*2.2046,0)+'–'+nf(24.9*hm*hm*2.2046,0)+' lb']]);""",
 "<h2>There's no single ideal weight</h2><p>These formulas were designed for medication dosing and population studies, not as personal targets. Muscle, frame size and age all matter. The BMI range of 18.5 to 24.9 is the broadest guide.</p>",
 [("Which formula is best?", "None is definitive. The BMI range is the most widely used; the others give a single point estimate.")], "Health")
tool("heart-rate-zone-calculator", "Heart rate zones", "Heart Rate Zone Calculator: Training Zones by Age",
 "Free heart rate zone calculator. Find your maximum heart rate and five training zones using the Karvonen method with your resting heart rate.",
 "Find your five heart rate training zones.",
 num("a", "Age", 35, "years", "1") + num("r", "Resting heart rate", 60, "bpm", "1"),
 """const mx=208-0.7*v('a'),hr=mx-v('r'),z=(lo,hi)=>Math.round(v('r')+hr*lo)+'–'+Math.round(v('r')+hr*hi)+' bpm';
show(Math.round(mx)+' bpm','estimated max heart rate',[['Zone 1 Recovery (50–60%)',z(.5,.6)],['Zone 2 Endurance (60–70%)',z(.6,.7)],['Zone 3 Tempo (70–80%)',z(.7,.8)],['Zone 4 Threshold (80–90%)',z(.8,.9)],['Zone 5 Max (90–100%)',z(.9,1)]]);""",
 "<h2>The method</h2><p>Max heart rate is estimated with the Tanaka formula (208 − 0.7 × age), which is more accurate than 220 − age. Zones use the Karvonen method, which takes your resting heart rate into account so the zones fit your fitness level.</p>",
 [("How do I find my resting heart rate?", "Count your pulse for 60 seconds just after waking, before getting up. Average it over a few days.")], "Health")
# ---------- Time ----------
tool("hours-calculator", "Hours calculator", "Hours Calculator: Time Card and Hours Worked",
 "Free hours calculator and time card. Add up hours worked from start and end times with breaks, for a day or a whole week, and work out pay.",
 "Add up hours worked from start and end times, minus breaks, and see your pay.",
 "".join(f'<div><label>{d}</label><div style="display:flex;gap:4px"><input id="s{i}" type="time" value="{"09:00" if i < 5 else ""}"><input id="e{i}" type="time" value="{"17:30" if i < 5 else ""}"><input id="b{i}" type="number" value="{30 if i < 5 else 0}" title="Break minutes" style="max-width:70px"></div></div>' for i, d in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])) + num("rate", "Hourly rate", 0, "optional"),
 """const t=s=>{if(!s)return null;const[a,b]=s.split(':').map(Number);return a*60+b};let tot=0,rows=[];
for(let i=0;i<7;i++){const s=t($('s'+i).value),e=t($('e'+i).value);if(s===null||e===null)continue;let m=e-s;if(m<0)m+=1440;m=Math.max(0,m-v('b'+i));tot+=m;rows.push([['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][i],Math.floor(m/60)+'h '+String(m%60).padStart(2,'0')+'m'])}
rows.push(['Decimal hours',nf(tot/60)]);if(v('rate'))rows.push(['Pay',money(tot/60*v('rate'))]);show(Math.floor(tot/60)+'h '+String(tot%60).padStart(2,'0')+'m','total hours worked',rows);""",
 "<h2>How to use it</h2><p>Enter a start time, end time and unpaid break in minutes for each day. Leave a day blank if you didn't work. Night shifts that end after midnight are handled automatically. Decimal hours (for example 7.5) are what most payroll and invoicing systems need.</p>",
 [("How do I convert minutes to decimal hours?", "Divide the minutes by 60. 45 minutes is 0.75 hours, so 7h 45m is 7.75 hours."), ("Does it handle overnight shifts?", "Yes. If the end time is earlier than the start time, it assumes the shift ran past midnight.")], "Time")
tool("overtime-calculator", "Overtime calculator", "Overtime Calculator: Overtime Pay and Total Wages",
 "Free overtime calculator. Work out overtime pay at time and a half or double time, and your total weekly pay.",
 "Work out overtime pay and total weekly wages.",
 num("r", "Hourly rate", 20) + num("h", "Total hours worked this week", 46) + num("t", "Regular hours threshold", 40) + sel("m", "Overtime rate", [("1.5", "Time and a half (1.5×)"), ("2", "Double time (2×)"), ("1.25", "1.25×")]),
 """const reg=Math.min(v('h'),v('t')),ot=Math.max(0,v('h')-v('t')),m=+$('m').value;
show(money(reg*v('r')+ot*v('r')*m),'total pay this week',[['Regular pay',money(reg*v('r'))],['Overtime hours',nf(ot)],['Overtime rate',money(v('r')*m)+'/hour'],['Overtime pay',money(ot*v('r')*m)]]);""",
 "<h2>Overtime rules</h2><p>In the US, the Fair Labor Standards Act requires time and a half for non-exempt employees after 40 hours in a work week. Some states, such as California, also require daily overtime. In other countries overtime rules depend on your contract.</p>",
 [("Is overtime calculated per day or per week?", "Federally in the US it's per week. Some states and contracts also have daily thresholds.")], "Time")
tool("stopwatch", "Online stopwatch", "Online Stopwatch with Laps",
 "Free online stopwatch with lap times. Start, stop, lap and reset. Works full screen on phone and desktop.",
 "A simple stopwatch with lap times.",
 '<div style="grid-column:1/-1;text-align:center"><div id="sw" style="font:700 3.4rem ui-monospace,monospace;color:var(--accent)">00:00.00</div><div style="display:flex;gap:8px;justify-content:center;margin-top:10px"><button class="btn" type="button" id="go">Start</button><button class="btn ghost" type="button" id="lap">Lap</button><button class="btn ghost" type="button" id="rs">Reset</button></div><ol id="laps" style="text-align:left;max-width:300px;margin:16px auto;font-family:ui-monospace,monospace"></ol></div>',
 """if(window._sw)return;window._sw=1;let st=0,acc=0,on=false,last=0,iv;const f=ms=>{const m=Math.floor(ms/60000),s=Math.floor(ms/1000)%60,c=Math.floor(ms/10)%100;return String(m).padStart(2,'0')+':'+String(s).padStart(2,'0')+'.'+String(c).padStart(2,'0')};
const now=()=>acc+(on?performance.now()-st:0),tick=()=>$('sw').textContent=f(now());
$('go').onclick=()=>{if(on){acc=now();on=false;clearInterval(iv);$('go').textContent='Start'}else{st=performance.now();on=true;iv=setInterval(tick,31);$('go').textContent='Stop'}};
$('lap').onclick=()=>{const t=now();$('laps').insertAdjacentHTML('beforeend','<li>'+f(t-last)+' <small>('+f(t)+')</small></li>');last=t};
$('rs').onclick=()=>{on=false;clearInterval(iv);acc=0;last=0;$('laps').innerHTML='';$('go').textContent='Start';tick()};""",
 "<h2>About this stopwatch</h2><p>It uses your browser's high-resolution timer, so it stays accurate even if the display updates slowly. Lap times show the split for each lap and the total time in brackets.</p>",
 [("Does it keep running if I switch tabs?", "Yes. Time is measured from the start moment, so it stays correct even if the tab is in the background.")], "Time", result=False)
# ---------- Math ----------
tool("average-calculator", "Average calculator", "Average Calculator: Mean, Median, Mode and Standard Deviation",
 "Free average calculator. Find the mean, median, mode, range and standard deviation of a list of numbers.",
 "Paste a list of numbers to get the mean, median, mode, range and standard deviation.",
 txt("t", "Numbers (separated by commas, spaces or new lines)", "12, 15, 15, 18, 21, 24, 30"),
 """const a=($('t').value.match(/-?\\d+(\\.\\d+)?/g)||[]).map(Number).sort((x,y)=>x-y),n=a.length;if(!n){show('–','enter some numbers',[]);return}
const s=a.reduce((x,y)=>x+y,0),mean=s/n,med=n%2?a[(n-1)/2]:(a[n/2-1]+a[n/2])/2,c={};a.forEach(x=>c[x]=(c[x]||0)+1);const mx=Math.max(...Object.values(c)),mode=mx>1?Object.keys(c).filter(k=>c[k]===mx).join(', '):'none';
const vp=a.reduce((x,y)=>x+(y-mean)**2,0);show(nf(mean,4),'mean (average)',[['Median',nf(med,4)],['Mode',mode],['Range',nf(a[n-1]-a[0],4)],['Sum',nf(s,4)],['Count',n],['Standard deviation (sample)',n>1?nf(Math.sqrt(vp/(n-1)),4):'–'],['Standard deviation (population)',nf(Math.sqrt(vp/n),4)]]);""",
 "<h2>Mean, median and mode</h2><p>The mean is the sum divided by the count. The median is the middle value when sorted, which is less affected by outliers. The mode is the most common value. Standard deviation measures how spread out the numbers are; use the sample version when your numbers are a sample of a bigger group.</p>",
 [("When should I use the median instead of the mean?", "When a few extreme values would distort the average, such as house prices or incomes.")], "Math")
tool("fraction-calculator", "Fraction calculator", "Fraction Calculator: Add, Subtract, Multiply and Divide",
 "Free fraction calculator. Add, subtract, multiply and divide fractions and mixed numbers, with the answer simplified and as a decimal.",
 "Add, subtract, multiply or divide two fractions.",
 num("a", "First numerator", 1, "", "1") + num("b", "First denominator", 2, "", "1") + sel("o", "Operation", [("+", "+ add"), ("-", "− subtract"), ("*", "× multiply"), ("/", "÷ divide")]) + num("c", "Second numerator", 1, "", "1") + num("d", "Second denominator", 3, "", "1"),
 """const g=(x,y)=>y?g(y,x%y):Math.abs(x),A=Math.round(v('a')),B=Math.round(v('b')),C=Math.round(v('c')),D=Math.round(v('d'));if(!B||!D){show('–','denominator cannot be 0',[]);return}
let n,d;const o=$('o').value;if(o==='+'){n=A*D+C*B;d=B*D}else if(o==='-'){n=A*D-C*B;d=B*D}else if(o==='*'){n=A*C;d=B*D}else{n=A*D;d=B*C}if(!d){show('–','cannot divide by 0',[]);return}
if(d<0){n=-n;d=-d}const k=g(n,d)||1;n/=k;d/=k;const w=Math.trunc(n/d),r=Math.abs(n%d);
show(d===1?String(n):n+'/'+d,'simplified',[['Decimal',nf(n/d,6)],['Mixed number',d===1||!w?'–':w+' '+r+'/'+d],['Percentage',nf(n/d*100,4)+'%']]);""",
 "<h2>How it works</h2><p>To add or subtract fractions, they're put over a common denominator first. To multiply, multiply the tops and the bottoms. To divide, flip the second fraction and multiply. The result is then simplified by dividing by the greatest common divisor.</p>",
 [("How do I enter a mixed number?", "Convert it to an improper fraction first: 2 1/3 is (2×3+1)/3 = 7/3.")], "Math")
tool("ratio-calculator", "Ratio calculator", "Ratio Calculator: Solve and Simplify Ratios",
 "Free ratio calculator. Simplify a ratio, or find the missing value in A:B = C:D, for recipes, scaling images and mixing.",
 "Find the missing value in a ratio, or simplify one.",
 num("a", "A", 16) + num("b", "B", 9) + num("c", "C", 1920) + '<div><label for="d">D</label><input id="d" placeholder="leave blank to solve"></div>',
 """const A=v('a'),B=v('b'),C=v('c'),Ds=$('d').value.trim();const g=(x,y)=>y?g(y,x%y):x;const sc=1e6,ga=g(Math.round(A*sc),Math.round(B*sc))||1;
const simp=nf(Math.round(A*sc)/ga,4)+':'+nf(Math.round(B*sc)/ga,4);if(Ds===''){show(nf(C*B/Math.max(A,1e-12),4),'D, so A:B = C:D',[['Simplified A:B',simp],['As a decimal',nf(A/Math.max(B,1e-12),6)]])}
else{const D=+Ds;show(nf(A*D/Math.max(B,1e-12),4),'C that makes A:B = C:'+D,[['Simplified A:B',simp]])}""",
 "<h2>Using ratios</h2><p>Ratios keep proportions the same when scaling. A 16:9 image that's 1920 pixels wide is 1080 pixels tall. A recipe for 4 that needs 300 g flour needs 450 g for 6 people.</p>",
 [("How do I simplify a ratio?", "Divide both sides by their greatest common divisor. 1920:1080 divided by 120 is 16:9.")], "Math")
tool("scientific-notation-converter", "Scientific notation", "Scientific Notation Converter",
 "Free scientific notation converter. Convert numbers to and from scientific and engineering notation, and E notation.",
 "Convert a number to scientific notation, or back to a plain number.",
 '<div style="grid-column:1/-1"><label for="n">Number (e.g. 0.000452, 6.02e23, 3.2×10^5)</label><input id="n" value="299792458"></div>' + num("s", "Significant figures", 4, "", "1"),
 """const s=$('n').value.replace(/\\s|,/g,'').replace(/[x×]10\\^?/i,'e'),x=Number(s);if(!isFinite(x)){show('Invalid','enter a number',[]);return}
const sf=Math.min(21,Math.max(1,Math.round(v('s')))),e=x?Math.floor(Math.log10(Math.abs(x))):0,m=x/Math.pow(10,e),ee=Math.floor(e/3)*3;
show(+m.toPrecision(sf)+' × 10^'+e,'scientific notation',[['E notation',x.toExponential(sf-1)],['Engineering',+(x/Math.pow(10,ee)).toPrecision(sf)+' × 10^'+ee],['Plain number',x.toLocaleString(undefined,{maximumFractionDigits:20})]]);""",
 "<h2>The format</h2><p>Scientific notation writes a number as a value between 1 and 10 multiplied by a power of ten. 299,792,458 becomes 2.998 × 10⁸. Engineering notation uses powers that are multiples of three, which match units like kilo, mega and micro.</p>",
 [("What is E notation?", "A way of typing scientific notation: 6.02e23 means 6.02 × 10²³.")], "Math")
# ---------- Everyday ----------
tool("pet-age-calculator", "Dog and cat age", "Dog and Cat Age Calculator: Pet Age in Human Years",
 "Free dog and cat age calculator. Convert your pet's age to human years using vet guidelines that account for size.",
 "Convert your dog's or cat's age into human years.",
 sel("p", "Pet", [("cat", "Cat"), ("s", "Dog, small (under 9 kg)"), ("m", "Dog, medium (9–23 kg)"), ("l", "Dog, large (23–40 kg)"), ("g", "Dog, giant (over 40 kg)")]) + num("a", "Pet's age", 5, "years"),
 """const a=v('a'),p=$('p').value,per={cat:4,s:4,m:5,l:6,g:7}[p];let h=a<=1?a*15:a<=2?15+(a-1)*9:24+(a-2)*per;
show(Math.round(h)+' human years','approximate equivalent',[['Life stage',a<1?'Baby':a<2?'Junior':h<40?'Adult':h<60?'Mature':'Senior'],['Each extra year adds',per+' human years']]);""",
 "<h2>Why not just multiply by 7?</h2><p>Pets grow up very fast in their first two years: a one-year-old dog or cat is roughly like a 15-year-old person, and a two-year-old like a 24-year-old. After that each year counts for about 4 to 7 human years, with larger dogs ageing faster.</p>",
 [("Do big dogs age faster?", "Yes. Large and giant breeds have shorter lifespans and are considered senior from around 6–8 years old.")], "Everyday")
tool("rent-affordability-calculator", "Rent affordability", "Rent Affordability Calculator: How Much Rent Can I Afford?",
 "Free rent affordability calculator. See how much rent you can afford with the 30% rule, the 40x rule and a budget-based method.",
 "See how much rent fits your income using three common rules.",
 num("i", "Gross annual income", 60000) + num("t", "Take-home pay per month", 3800) + num("d", "Monthly debt payments", 300),
 """const g=v('i')/12;show(money(g*0.3),'per month (30% rule)',[['40× rule (landlord check)',money(v('i')/40)],['50/30/20 budget (needs − debts)',money(Math.max(0,v('t')*0.5-v('d')))],['Annual rent at 30%',money(v('i')*0.3)]]);""",
 "<h2>Three rules of thumb</h2><p>The 30% rule says rent should be no more than 30% of gross income. Many US landlords require yearly income of at least 40 times the monthly rent. The 50/30/20 budget puts all needs, including rent and minimum debt payments, at 50% of take-home pay, which is the most conservative.</p>",
 [("Should utilities count?", "If they're not included in the rent, budget for them separately from these figures.")], "Money")
tool("emergency-fund-calculator", "Emergency fund", "Emergency Fund Calculator: How Much Should I Save?",
 "Free emergency fund calculator. Work out how much you need for 3 to 12 months of essential expenses and how long it will take to save.",
 "Work out your emergency fund target and how long it will take to build.",
 num("e", "Essential monthly expenses", 2500) + sel("m", "Months of cover", [("3", "3 months (stable job)"), ("6", "6 months (recommended)"), ("9", "9 months (freelancer / single income)"), ("12", "12 months (very irregular income)")]) + num("h", "Already saved", 2000) + num("s", "Can save per month", 400),
 """const g=v('e')*+$('m').value,left=Math.max(0,g-v('h')),mo=v('s')>0?Math.ceil(left/v('s')):Infinity;
show(money(g),'emergency fund target',[['Still to save',money(left)],['Months to reach it',isFinite(mo)?mo:'–'],['Already covered',nf(v('h')/Math.max(v('e'),1),1)+' months']]);""",
 "<h2>How big should it be?</h2><p>Three to six months of essential costs (rent, food, bills, minimum debt payments) is the usual advice. Freelancers and people with one household income should aim higher, because income can stop without warning. Keep it in an easy-access savings account, not invested.</p>",
 [("What counts as essential?", "Housing, utilities, groceries, insurance, transport and minimum debt payments. Leave out subscriptions and eating out.")], "Money")
tool("fire-calculator", "FIRE calculator", "FIRE Calculator: When Can I Retire Early?",
 "Free FIRE calculator. Find your financial independence number and how many years until you can retire early, based on savings rate.",
 "Find your FIRE number and how many years until you reach it.",
 num("x", "Yearly spending", 40000) + num("s", "Invested so far", 50000) + num("c", "Invested per year", 20000) + num("r", "Real return", 5, "% after inflation") + num("w", "Safe withdrawal rate", 4, "%"),
 """const T=v('x')/(v('w')/100),r=v('r')/100;let b=v('s'),y=0;while(b<T&&y<100){b=b*(1+r)+v('c');y++}
show(y>=100?'100+ years':y+' years','to financial independence',[['FIRE number',money(T)],['Lean FIRE (75% spending)',money(T*.75)],['Fat FIRE (150% spending)',money(T*1.5)],['Savings rate',v('c')+v('x')>0?nf(v('c')/(v('c')+v('x'))*100,1)+'%':'–']]);""",
 "<h2>The idea</h2><p>FIRE stands for financial independence, retire early. Your FIRE number is about 25 times yearly spending (a 4% withdrawal rate). The biggest lever is your savings rate: the more you save and the less you spend, the faster you get there.</p>",
 [("Why use a real return?", "Using a return after inflation keeps everything in today's money, so the FIRE number stays meaningful.")], "Money")
tool("sales-commission-calculator", "Sales commission", "Sales Commission Calculator",
 "Free sales commission calculator. Work out commission from a flat rate or tiers, plus base salary and total earnings.",
 "Work out commission and total pay from sales.",
 num("s", "Sales amount", 50000) + num("r", "Commission rate", 5, "%") + num("q", "Quota for bonus rate", 40000, "optional") + num("r2", "Rate above quota", 8, "%") + num("b", "Base pay for the period", 2000),
 """const S=v('s'),Q=v('q');const com=Q>0&&S>Q?Q*v('r')/100+(S-Q)*v('r2')/100:S*v('r')/100;
show(money(com+v('b')),'total earnings',[['Commission',money(com)],['Base pay',money(v('b'))],['Effective commission rate',nf(com/Math.max(S,1e-9)*100)+'%']]);""",
 "<h2>Tiered commission</h2><p>Many plans pay a higher rate on sales above a quota. Here the normal rate applies up to the quota and the higher rate applies only to sales above it. Leave the quota at 0 for a flat rate.</p>",
 [("Is commission taxed differently?", "In most countries commission is taxed as normal income, though withholding may differ.")], "Money")
# ---------- Text ----------
tool("text-to-binary", "Text to binary", "Text to Binary Converter (and Binary to Text)",
 "Free text to binary converter. Turn text into binary code, hex or decimal bytes, and decode binary back to text. Supports UTF-8.",
 "Convert text to binary and back.",
 sel("m", "Mode", [("e", "Text to binary"), ("d", "Binary to text")]) + txt("t", "Input", "Hello") + txt("o", "Output") + '<div><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """if($('m').value==='e'){const b=[...new TextEncoder().encode($('t').value)];$('o').value=b.map(x=>x.toString(2).padStart(8,'0')).join(' ');show(b.length+' bytes','encoded as UTF-8',[['Hex',b.map(x=>x.toString(16).padStart(2,'0')).join(' ')],['Decimal',b.join(' ')]])}
else{const g=($('t').value.match(/[01]{8}/g)||[]);try{$('o').value=new TextDecoder('utf-8',{fatal:true}).decode(Uint8Array.from(g.map(x=>parseInt(x,2))));show(g.length+' bytes','decoded',[])}catch(e){$('o').value='';show('Invalid','not valid UTF-8 binary',[])}}""",
 "<h2>How text becomes binary</h2><p>Each character is turned into one or more bytes using UTF-8, and each byte is written as eight binary digits. Plain English letters take one byte each; accented letters and emoji take two to four.</p>",
 [("What does 01001000 mean?", "It's 72 in decimal, which is the letter H.")], "Text")
tool("morse-code-translator", "Morse code translator", "Morse Code Translator: Text to Morse and Back",
 "Free Morse code translator. Convert text to Morse code and Morse code to text, and play it as sound.",
 "Translate text to Morse code and back, and hear it played.",
 txt("t", "Text or Morse (use . and -, / between words)", "SOS help") + txt("o", "Result") + '<div style="display:flex;gap:8px"><button class="btn" type="button" id="pl">Play sound</button><button class="btn ghost" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """const M={A:'.-',B:'-...',C:'-.-.',D:'-..',E:'.',F:'..-.',G:'--.',H:'....',I:'..',J:'.---',K:'-.-',L:'.-..',M:'--',N:'-.',O:'---',P:'.--.',Q:'--.-',R:'.-.',S:'...',T:'-',U:'..-',V:'...-',W:'.--',X:'-..-',Y:'-.--',Z:'--..',0:'-----',1:'.----',2:'..---',3:'...--',4:'....-',5:'.....',6:'-....',7:'--...',8:'---..',9:'----.','.':'.-.-.-',',':'--..--','?':'..--..','!':'-.-.--','/':'-..-.','@':'.--.-.','&':'.-...',':':'---...','=':'-...-','+':'.-.-.','-':'-....-','(':'-.--.',')':'-.--.-',"'":'.----.','"':'.-..-.'};
const t=$('t').value.trim(),isM=/^[.\\-\\s/|]+$/.test(t);let morse;if(isM){const R={};for(const k in M)R[M[k]]=k;$('o').value=t.split(/\\s*[\\/|]\\s*|\\s{3,}/).map(w=>w.trim().split(/\\s+/).map(c=>R[c]||'?').join('')).join(' ');morse=t;show('Decoded','Morse to text',[])}
else{morse=t.toUpperCase().split(/\\s+/).map(w=>[...w].map(c=>M[c]||'').filter(Boolean).join(' ')).join(' / ');$('o').value=morse;show('Encoded','text to Morse',[['Dots',(morse.match(/\\./g)||[]).length],['Dashes',(morse.match(/-/g)||[]).length]])}
$('pl').onclick=()=>{const A=new(window.AudioContext||window.webkitAudioContext)(),u=.08;let at=A.currentTime+.05;for(const c of morse){if(c==='.'||c==='-'){const o=A.createOscillator(),g=A.createGain();o.frequency.value=650;o.connect(g);g.connect(A.destination);const d=c==='.'?u:3*u;g.gain.setValueAtTime(.3,at);g.gain.setValueAtTime(0,at+d);o.start(at);o.stop(at+d);at+=d+u}else if(c===' ')at+=2*u;else if(c==='/')at+=2*u}};""",
 "<h2>Morse timing</h2><p>A dash is three times as long as a dot. The gap between parts of a letter is one dot, between letters three dots, and between words seven dots. The player above uses the standard timing at about 15 words per minute.</p>",
 [("How do I separate words in Morse?", "Use a slash (/) between words and a single space between letters.")], "Text")
tool("word-frequency-counter", "Word frequency counter", "Word Frequency Counter: Most Used Words in a Text",
 "Free word frequency counter. Find the most common words and phrases in any text, with an option to ignore common stop words. Useful for SEO and editing.",
 "Find which words you use most in a piece of text.",
 txt("t", "Your text", "Paste an article here to see which words you repeat most. Repeated words can make writing feel flat, and keyword density matters for SEO.") + sel("s", "Stop words", [("1", "Ignore common words (the, and, of…)"), ("0", "Count every word")]) + sel("g", "Count", [("1", "Single words"), ("2", "Two-word phrases"), ("3", "Three-word phrases")]),
 """const SW=new Set('a an and are as at be but by for from has have i if in into is it its of on or so that the their them there they this to was we were will with you your not can do our more than then what which who'.split(' '));
const w=($('t').value.toLowerCase().match(/[\\p{L}\\p{N}']+/gu)||[]),k=+$('g').value,c={};let tot=0;for(let i=0;i+k<=w.length;i++){const p=w.slice(i,i+k);if($('s').value==='1'&&p.some(x=>SW.has(x)))continue;const key=p.join(' ');c[key]=(c[key]||0)+1;tot++}
const top=Object.entries(c).sort((a,b)=>b[1]-a[1]).slice(0,15);show(top.length?top[0][0]:'–','most frequent',top.map(([x,n])=>[x,n+' × ('+nf(n/Math.max(tot,1)*100,1)+'%)']));""",
 "<h2>Keyword density</h2><p>The percentage shows how often each word or phrase appears compared with all counted words. For SEO, a main keyword at about 1–2% reads naturally. Much higher can look like keyword stuffing.</p>",
 [("Is my text uploaded?", "No. Counting happens in your browser.")], "Text")
tool("reverse-text", "Reverse text", "Reverse Text Generator: Backwards, Upside Down and Mirror",
 "Free reverse text generator. Write text backwards, reverse word order, flip it upside down or mirror it, then copy and paste.",
 "Flip, reverse or turn text upside down for fun posts and puzzles.",
 txt("t", "Your text", "Hello world") + sel("m", "Style", [("c", "Backwards (characters)"), ("w", "Reverse word order"), ("u", "Upside down"), ("e", "Reverse each word")]) + txt("o", "Result") + '<div><button class="btn" type="button" onclick="copy(\'o\',this)">Copy</button></div>',
 """const t=$('t').value,m=$('m').value,U={a:'ɐ',b:'q',c:'ɔ',d:'p',e:'ǝ',f:'ɟ',g:'ƃ',h:'ɥ',i:'ᴉ',j:'ɾ',k:'ʞ',l:'l',m:'ɯ',n:'u',o:'o',p:'d',q:'b',r:'ɹ',s:'s',t:'ʇ',u:'n',v:'ʌ',w:'ʍ',x:'x',y:'ʎ',z:'z','.':'˙',',':"'",'?':'¿','!':'¡','(':')',')':'(',"'":',',_:'‾'};
let o;if(m==='c')o=[...t].reverse().join('');else if(m==='w')o=t.split(/(\\s+)/).reverse().join('');else if(m==='e')o=t.split(/(\\s+)/).map(x=>[...x].reverse().join('')).join('');else o=[...t.toLowerCase()].reverse().map(c=>U[c]||c).join('');
$('o').value=o;show([...o].length+' characters','ready to copy',[]);""",
 "<h2>Fun uses</h2><p>Upside-down and backwards text works in most social apps, usernames and messages because it uses ordinary Unicode characters. Reversed text is also handy for puzzles, escape-room clues and checking palindromes.</p>",
 [("Will upside-down text work on Instagram?", "Yes, it uses standard Unicode characters that most apps display.")], "Text")
