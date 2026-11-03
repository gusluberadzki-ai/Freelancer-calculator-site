"""Generates one page per salary and per hourly wage. Run: python3 build.py"""
import pathlib, datetime, html
BASE = "https://gusluberadzki-ai.github.io/Freelancer-calculator-site/salary/"
OUT = pathlib.Path(__file__).parent
H = 2080
def m(x, d=2): return f"${x:,.{d}f}"
def k(x): return f"{x//1000}k" if x % 1000 == 0 else str(x)
def head(t, d, p):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(t)}</title><meta name="description" content="{html.escape(d)}"><link rel="canonical" href="{BASE}{p}">
<link rel="stylesheet" href="../freelance-calc/style.css"><!-- ADSENSE: paste the AdSense <script> tag here once approved --></head><body>
<header><a class="logo" href="../freelance-calc/">Rate<span>Kit</span></a><nav><a href="./">All amounts</a><a href="../freelance-calc/salary-to-hourly.html">Converter</a></nav></header><main>"""
FOOT = """<h2>Other free tools</h2><div class="cards"><a href="../freelance-calc/hourly-rate-calculator.html"><strong>Freelance hourly rate calculator</strong><span>What to charge as a freelancer.</span></a>
<a href="../freelance-calc/contractor-vs-employee.html"><strong>Contractor vs employee</strong><span>Compare a contract rate with a salary.</span></a>
<a href="../invoice-generator/"><strong>Free invoice generator</strong><span>Make a PDF invoice in seconds.</span></a></div>
</main><footer>Figures are gross (before tax) and assume 40 hours a week, 52 weeks a year unless stated. · <a href="../freelance-calc/privacy.html">Privacy</a></footer></body></html>"""
def table(rows): return '<div class="result"><table>' + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows) + "</table></div>"
salaries = list(range(20000, 200001, 1000)) + list(range(205000, 300001, 5000))
wages = list(range(10, 101)) + [105, 110, 115, 120, 125, 130, 140, 150, 175, 200]
urls = []
for s in salaries:
    p = f"{s}-a-year-is-how-much-an-hour.html"; urls.append(p); hr = s / H
    i = salaries.index(s); prev, nxt = salaries[max(0, i-1)], salaries[min(len(salaries)-1, i+1)]
    near = [x for x in salaries[max(0, i-4):i+5] if x != s]
    body = f"""<h1>${s:,} a year is how much an hour?</h1>
<p class="lead">${s:,} a year is <strong>{m(hr)} an hour</strong>, based on a 40-hour week and 52 paid weeks (2,080 hours).</p>
{table([("Hourly", m(hr)), ("Daily (8 hours)", m(hr*8)), ("Weekly", m(s/52)), ("Every two weeks", m(s/26)), ("Twice a month", m(s/24)), ("Monthly", m(s/12)), ("Yearly", m(s, 0))])}
<div class="ad"><!-- ad slot --></div>
<h2>If you work fewer hours</h2>
{table([(f"{h} hours a week", m(s/(h*52)) + " / hour") for h in (35, 37.5, 30, 20)])}
<h2>If you take unpaid time off</h2>
<p>If only {50} weeks are paid (two weeks unpaid), ${s:,} works out to {m(s/(40*50))} an hour. With 48 paid weeks, it's {m(s/(40*48))} an hour.</p>
<h2>Freelancing instead?</h2>
<p>To earn the same as a ${s:,} salary as a freelancer, you'd typically need to charge around <strong>{m(hr*1.5,0)} to {m(hr*2,0)} an hour</strong>, because freelancers pay for their own holidays, equipment and benefits and can't bill every hour. Get an exact figure with the <a href="../freelance-calc/contractor-vs-employee.html">contractor vs employee calculator</a>.</p>
<h2>Nearby salaries</h2><p>{" · ".join(f'<a href="{x}-a-year-is-how-much-an-hour.html">${x:,}</a>' for x in near)}</p>"""
    (OUT/p).write_text(head(f"${s:,} a Year Is How Much an Hour? ({m(hr)}/hr) | RateKit", f"${s:,} a year is {m(hr)} an hour. See the daily, weekly, biweekly and monthly pay for a ${s:,} salary.", p) + body + FOOT)
for w in wages:
    p = f"{w}-an-hour-is-how-much-a-year.html"; urls.append(p); y = w * H
    i = wages.index(w); near = [x for x in wages[max(0, i-4):i+5] if x != w]
    body = f"""<h1>${w} an hour is how much a year?</h1>
<p class="lead">${w} an hour is <strong>{m(y,0)} a year</strong>, working 40 hours a week for 52 weeks.</p>
{table([("Yearly", m(y, 0)), ("Monthly", m(y/12)), ("Twice a month", m(y/24)), ("Every two weeks", m(y/26)), ("Weekly", m(w*40)), ("Daily (8 hours)", m(w*8))])}
<div class="ad"><!-- ad slot --></div>
<h2>Part-time and overtime</h2>
{table([(f"{h} hours a week", m(w*h*52, 0) + " / year") for h in (20, 30, 35, 45, 50)] + [("Overtime rate (1.5×)", m(w*1.5) + " / hour")])}
<h2>With time off</h2><p>Working 50 weeks a year, ${w} an hour is {m(w*40*50,0)}. Working 48 weeks, it's {m(w*40*48,0)}.</p>
<h2>Nearby hourly rates</h2><p>{" · ".join(f'<a href="{x}-an-hour-is-how-much-a-year.html">${x}/hr</a>' for x in near)}</p>"""
    (OUT/p).write_text(head(f"${w} an Hour Is How Much a Year? ({m(y,0)}) | RateKit", f"${w} an hour is {m(y,0)} a year. See monthly, biweekly, weekly and daily pay for ${w}/hour.", p) + body + FOOT)
idx = ('<h1>Salary and hourly pay tables</h1><p class="lead">Pick an amount to see the hourly, weekly, monthly and yearly equivalents.</p>'
  '<h2>Yearly salary to hourly</h2><p>' + " · ".join(f'<a href="{s}-a-year-is-how-much-an-hour.html">${k(s)}</a>' for s in salaries) + '</p>'
  '<h2>Hourly wage to yearly</h2><p>' + " · ".join(f'<a href="{w}-an-hour-is-how-much-a-year.html">${w}</a>' for w in wages) + '</p>')
(OUT/"index.html").write_text(head("Salary to Hourly and Hourly to Salary Tables | RateKit", "Every salary from $20,000 to $300,000 converted to hourly pay, and every hourly wage from $10 to $200 converted to a yearly salary.", "") + idx + FOOT)
today = datetime.date.today().isoformat()
(OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod></url>" for u in [""] + urls) + "</urlset>\n")
print(len(urls), "pages")
