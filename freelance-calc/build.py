"""Generates the RateKit calculator pages. Run: python3 build.py"""
import json, html, datetime, pathlib

BASE = "https://gusluberadzki-ai.github.io/Freelancer-calculator-site/freelance-calc/"
SITE = "RateKit"
OUT = pathlib.Path(__file__).parent
TODAY = datetime.date.today().isoformat()

# Each calculator: fields are (id, label, default, hint). `js` gets an object `v`
# with numeric field values and a `money()` formatter, and returns {big, label, rows}.
CALCS = [
 dict(slug="hourly-rate-calculator", nav="Hourly rate",
  title="Freelance Hourly Rate Calculator: What Should I Charge?",
  h1="Freelance hourly rate calculator",
  lead="Work out the hourly rate you need to hit your income goal after expenses, taxes, holidays and unbillable time.",
  fields=[("income","Take-home income you want per year",60000,""),
          ("expenses","Business expenses per year",6000,"software, equipment, insurance"),
          ("tax","Tax rate",25,"%, rough total"),
          ("weeks","Weeks off per year",6,"holidays + sick days"),
          ("hours","Hours worked per week",40,""),
          ("billable","Share of hours you can bill",65,"%, admin and sales eat the rest")],
  js="""const gross=(v.income/(1-v.tax/100))+v.expenses;
const billH=(52-v.weeks)*v.hours*(v.billable/100);
const rate=gross/billH;
return {big:money(rate),label:'minimum hourly rate',rows:[
['Revenue needed per year',money(gross)],['Billable hours per year',Math.round(billH)],
['Day rate (8h)',money(rate*8)],['Monthly revenue target',money(gross/12)]]};""",
  body="""<h2>How this hourly rate is calculated</h2>
<p>Most new freelancers take their old salary, divide by 2,080 hours and end up badly underpaid. That number ignores three things: you pay your own taxes and expenses, you don't get paid holidays, and a big chunk of your week goes on unbillable work like admin, invoicing and finding clients.</p>
<p>This calculator starts from the take-home income you want, grosses it up for tax, adds your business expenses, then divides by the hours you can actually bill. The result is your <strong>floor</strong>: charge less and you miss your goal.</p>
<h2>What share of time is billable?</h2>
<p>Established freelancers with steady clients often bill 70 to 80% of their working hours. If you're just starting out and spend a lot of time on sales, 50 to 60% is more realistic.</p>""",
  faq=[("Should I charge hourly or per project?","Hourly is safest when the scope is unclear. Once you can estimate well, per-project pricing lets you earn more by working faster. Use your hourly floor to sanity-check every project quote."),
       ("Is this rate before or after tax?","The result is what you invoice, before tax. The calculator already adds your tax rate on top of the take-home income you entered."),
       ("How often should I raise my rate?","Review it at least once a year, and raise it whenever you're consistently fully booked.")]),

 dict(slug="salary-to-hourly", nav="Salary ↔ hourly",
  title="Salary to Hourly Calculator (and Hourly to Salary)",
  h1="Salary to hourly converter",
  lead="Convert an annual salary into hourly, daily, weekly and monthly pay, or work backwards from an hourly wage.",
  fields=[("salary","Annual salary",50000,"leave 0 to use hourly"),
          ("hourly","Or hourly wage",0,"used if salary is 0"),
          ("hours","Hours per week",40,""),
          ("weeks","Paid weeks per year",52,"")],
  js="""const yearH=v.hours*v.weeks;
const year=v.salary>0?v.salary:v.hourly*yearH;
const hr=year/yearH;
return {big:money(v.salary>0?hr:year),label:v.salary>0?'per hour':'per year',rows:[
['Hourly',money(hr)],['Daily (8h)',money(hr*8)],['Weekly',money(hr*v.hours)],
['Monthly',money(year/12)],['Yearly',money(year)]]};""",
  body="""<h2>The quick formula</h2>
<p>For a standard 40-hour week with 52 paid weeks, a year has 2,080 working hours. Divide the salary by 2,080 to get the hourly wage, or multiply an hourly wage by 2,080 to get the annual salary. A quick mental shortcut: <strong>halve the salary and drop the thousands</strong>. $50,000 a year is roughly $25 an hour.</p>
<h2>Going freelance?</h2>
<p>An employee's hourly wage is not the same as a freelance rate. Freelancers pay for their own holidays, equipment and taxes, so they typically need 1.5 to 2 times the equivalent hourly wage. Use the <a href="contractor-vs-employee.html">contractor vs employee calculator</a> to compare properly.</p>""",
  faq=[("How many working hours are in a year?","2,080 at 40 hours a week for 52 weeks. If you only count weeks actually worked (for example 47 after holidays), it's 1,880."),
       ("Does this include tax?","No. It converts gross pay. Your take-home pay depends on where you live.")]),

 dict(slug="contractor-vs-employee", nav="Contractor vs employee",
  title="Contractor vs Employee Pay Calculator: Equivalent Rate",
  h1="Contractor vs employee rate calculator",
  lead="Find the contract day or hourly rate that matches a salaried job once benefits, holidays and gaps between contracts are counted.",
  fields=[("salary","Employee salary offered",60000,""),
          ("benefits","Value of benefits",15,"% of salary: pension, health, bonus"),
          ("holiday","Paid holiday days as employee",25,""),
          ("gap","Unpaid weeks between contracts",4,"per year"),
          ("costs","Extra contractor costs per year",3000,"accountant, insurance, kit")],
  js="""const total=v.salary*(1+v.benefits/100)+v.costs;
const days=(52-v.gap)*5-v.holiday;
const day=total/days;
return {big:money(day),label:'equivalent contract day rate',rows:[
['Hourly (8h day)',money(day/8)],['Total employee package',money(v.salary*(1+v.benefits/100))],
['Billable days per year',days],['Contract income needed',money(total)]]};""",
  body="""<h2>Why contractors charge more</h2>
<p>A salaried employee gets paid holidays, sick pay, pension contributions and often health cover. A contractor pays for all of that and also has quiet weeks between contracts. That's why a contract day rate that looks high is often worth about the same as a normal salary.</p>
<p>A common rule of thumb is that the day rate should be at least <strong>salary ÷ 200</strong> to break even, and salary ÷ 150 to come out clearly ahead.</p>""",
  faq=[("Is contracting worth it?","If your contract rate is well above the equivalent rate shown here, usually yes. If it's close, the extra risk and admin may not be worth it."),
       ("Does this account for tax differences?","No. Tax treatment of contractors differs a lot between countries, so compare after-tax figures with an accountant before deciding.")]),

 dict(slug="tax-set-aside-calculator", nav="Tax set-aside",
  title="How Much to Set Aside for Taxes as a Freelancer",
  h1="Freelance tax set-aside calculator",
  lead="See how much of each invoice to put aside for tax so the bill never surprises you.",
  fields=[("invoice","Invoice amount",2500,""),
          ("rate","Your total tax rate",28,"%, income + social contributions"),
          ("expenses","Deductible expenses in this invoice period",300,""),
          ("buffer","Safety buffer",3,"% extra, optional")],
  js="""const profit=Math.max(0,v.invoice-v.expenses);
const tax=profit*(v.rate+v.buffer)/100;
return {big:money(tax),label:'set aside from this invoice',rows:[
['Taxable profit',money(profit)],['Effective share of invoice',(v.invoice?tax/v.invoice*100:0).toFixed(1)+'%'],
['Yours to spend',money(v.invoice-tax)]]};""",
  body="""<h2>The simple system</h2>
<p>Open a separate savings account just for tax. Every time a client pays you, move the amount above into it straight away. When your tax bill arrives, the money is already there.</p>
<h2>What rate should I use?</h2>
<p>Use your marginal rate plus any social security or health contributions. If you don't know it, 25 to 30% is a cautious starting point in most countries. The buffer covers surprises, and anything left over at the end of the year is a bonus.</p>
<p><em>This is a planning tool, not tax advice. Check your actual rates with a local accountant.</em></p>""",
  faq=[("What percentage should a freelancer save for taxes?","Commonly 25 to 35% of profit, depending on country and income level."),
       ("Do I pay tax on the full invoice?","Usually only on profit, which is income minus allowable business expenses.")]),

 dict(slug="project-price-calculator", nav="Project price",
  title="Freelance Project Pricing Calculator: Quote a Fixed Price",
  h1="Project price calculator",
  lead="Turn an hours estimate into a fixed-price quote with a buffer for revisions and the unexpected.",
  fields=[("hours","Estimated hours",30,""),
          ("rate","Your hourly rate",75,""),
          ("buffer","Contingency buffer",20,"% for scope creep"),
          ("revisions","Revision rounds included",2,""),
          ("revh","Hours per revision round",3,""),
          ("costs","Direct costs",0,"fonts, stock photos, plugins")],
  js="""const h=v.hours+v.revisions*v.revh;
const price=h*v.rate*(1+v.buffer/100)+v.costs;
return {big:money(Math.ceil(price/50)*50),label:'suggested fixed price (rounded)',rows:[
['Total hours incl. revisions',h],['Base labour cost',money(h*v.rate)],
['Buffer',money(h*v.rate*v.buffer/100)],['50% deposit',money(Math.ceil(price/50)*25)]]};""",
  body="""<h2>How to price a project</h2>
<p>Estimate the hours, add the revision rounds you'll include, then add a contingency buffer. Projects almost always take longer than planned, and a 15 to 25% buffer protects your hourly rate. Round the final number: clients find $3,250 more natural than $3,217.</p>
<h2>Protect yourself</h2>
<p>Write the number of revision rounds into your contract, and charge your hourly rate for anything beyond them. Ask for a 30 to 50% deposit before starting.</p>""",
  faq=[("How much buffer should I add to a quote?","15 to 25% for familiar work, 30% or more for something new or vaguely defined."),
       ("Should I show the hourly breakdown to the client?","Usually not. Quote the project price and the deliverables, so the conversation is about value rather than hours.")]),

 dict(slug="late-payment-calculator", nav="Late payment fee",
  title="Late Invoice Interest Calculator for Freelancers",
  h1="Late payment interest calculator",
  lead="Work out the interest and late fee on an overdue invoice.",
  fields=[("amount","Invoice amount",3000,""),
          ("rate","Annual interest rate",8,"% per year, check your contract or local law"),
          ("days","Days overdue",30,""),
          ("fee","Fixed late fee",0,"if your contract has one")],
  js="""const interest=v.amount*(v.rate/100)*(v.days/365);
return {big:money(v.amount+interest+v.fee),label:'total now owed',rows:[
['Interest',money(interest)],['Daily interest',money(v.amount*(v.rate/100)/365)],
['Fixed fee',money(v.fee)],['Original invoice',money(v.amount)]]};""",
  body="""<h2>How late payment interest works</h2>
<p>Simple interest is calculated as <em>amount × annual rate × days overdue ÷ 365</em>. Many countries give businesses a legal right to charge interest on late B2B invoices even if the contract doesn't mention it, often at a central bank rate plus a few percent. Check the rules where you and your client are based.</p>
<h2>Getting paid faster</h2>
<p>State your payment terms and late-payment interest on every invoice, send a friendly reminder a few days before the due date, and follow up the day after it passes.</p>""",
  faq=[("Can I charge interest if it's not in my contract?","In many places yes for business-to-business invoices, but rules vary. Putting it in your terms removes any doubt."),
       ("Should I actually charge it?","It's often more useful as leverage: mentioning it in a reminder gets many invoices paid quickly.")]),
]

CURRENCIES = ["USD $","EUR €","GBP £","PLN zł","CAD $","AUD $","INR ₹"]

def head(title, desc, path):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | {SITE}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<link rel="stylesheet" href="style.css">
<!-- ADSENSE: paste the AdSense <script> tag here once the account is approved -->
</head><body>
<header><a class="logo" href="./">Rate<span>Kit</span></a>
<nav><a href="./">All calculators</a></nav></header><main>"""

FOOT = f"""</main><footer>{SITE} offers free calculators for freelancers and contractors. Results are estimates, not financial or tax advice.
· <a href="privacy.html">Privacy</a> · <a href="../salary/">Salary tables</a> · <a href="../qr-code-generator/">QR codes</a> · <a href="../image-compressor/">Image compressor</a> · <a href="../invoice-generator/">Free invoice generator</a> · <a href="../freelance-tools/">Tools for freelancers</a> · <a href="../chrome-extension/">TickBill time tracker</a></footer></body></html>"""

def page(c):
    fields = "".join(
        f'<div><label for="{i}">{html.escape(l)} {"<small>("+html.escape(h)+")</small>" if h else ""}</label>'
        f'<input id="{i}" type="number" inputmode="decimal" step="any" value="{d}"></div>'
        for i, l, d, h in c["fields"])
    cur = "".join(f'<option value="{x.split()[0]}">{x}</option>' for x in CURRENCIES)
    faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in c["faq"])
    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c["faq"]]})
    related = "".join(f'<a href="{o["slug"]}.html"><strong>{o["nav"]}</strong><span>{html.escape(o["lead"][:70])}…</span></a>'
                      for o in CALCS if o is not c)
    ids = json.dumps([f[0] for f in c["fields"]])
    return head(c["title"], c["lead"], c["slug"]+".html") + f"""
<h1>{c["h1"]}</h1><p class="lead">{c["lead"]}</p>
<section class="calc"><div class="grid">{fields}
<div><label for="cur">Currency</label><select id="cur">{cur}</select></div></div>
<div class="result" aria-live="polite"><div class="big" id="big">–</div><div id="lbl"></div><table id="rows"></table></div></section>
<div class="ad"><!-- ad slot --></div>
{c["body"]}
<h2>Frequently asked questions</h2>{faq_html}
<h2>More calculators</h2><div class="cards">{related}</div>
<script type="application/ld+json">{faq_ld}</script>
<script>
const IDS={ids};
function money(n){{const c=document.getElementById('cur').value;
try{{return new Intl.NumberFormat(undefined,{{style:'currency',currency:c,maximumFractionDigits:n<100?2:0}}).format(isFinite(n)?n:0)}}catch(e){{return n.toFixed(2)}}}}
function calc(v){{{c["js"]}}}
function run(){{const v={{}};IDS.forEach(i=>v[i]=parseFloat(document.getElementById(i).value)||0);
const r=calc(v);document.getElementById('big').textContent=r.big;document.getElementById('lbl').textContent=r.label;
document.getElementById('rows').innerHTML=r.rows.map(x=>'<tr><td>'+x[0]+'</td><td>'+x[1]+'</td></tr>').join('');
try{{localStorage.setItem('rk-cur',document.getElementById('cur').value)}}catch(e){{}}}}
try{{const s=localStorage.getItem('rk-cur');if(s)document.getElementById('cur').value=s}}catch(e){{}}
document.querySelectorAll('input,select').forEach(e=>e.addEventListener('input',run));run();
</script>""" + FOOT

def index():
    cards = "".join(f'<a href="{c["slug"]}.html"><strong>{c["h1"].capitalize()}</strong><span>{html.escape(c["lead"])}</span></a>' for c in CALCS)
    return head("Free Calculators for Freelancers and Contractors",
                "Free freelance calculators: hourly rate, salary to hourly, contractor day rate, tax set-aside, project pricing and late payment interest.", "") + f"""
<h1>Money calculators for freelancers</h1>
<p class="lead">Free, fast and private. Everything runs in your browser and nothing you type is stored or sent anywhere.</p>
<div class="cards">{cards}</div>
<h2>Built for freelancers and contractors</h2>
<p>Pricing your work is the hardest part of going independent. These calculators answer the questions every freelancer runs into: what to charge per hour, how a contract rate compares to a salary, how much tax to put aside, and how to quote a fixed-price project.</p>""" + FOOT

def privacy():
    return head("Privacy policy", "RateKit privacy policy.", "privacy.html") + """
<h1>Privacy policy</h1>
<p>Calculations run entirely in your browser. We don't collect or store the numbers you enter.</p>
<p>This site may show ads from Google AdSense. Google and its partners may use cookies to show ads based on your visits to this and other websites. You can opt out of personalised advertising at <a href="https://adssettings.google.com">Google Ads Settings</a>.</p>
<p>Your currency choice is saved in your browser's local storage for convenience.</p>""" + FOOT

(OUT/"index.html").write_text(index())
(OUT/"privacy.html").write_text(privacy())
for c in CALCS:
    (OUT/f'{c["slug"]}.html').write_text(page(c))
urls = [""] + [c["slug"]+".html" for c in CALCS]
(OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>\n")
print("built", len(CALCS), "calculators")
