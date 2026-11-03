"""Builds the KDP interior (6x9in) and wrap cover for 'The Freelancer's Weekly Planner'.
Run: python3 build.py  (needs node + playwright)"""
import pathlib, subprocess, json
OUT = pathlib.Path(__file__).parent
TITLE, SUB, AUTHOR = "The Freelancer's Weekly Planner", "Undated 52-week planner for clients, hours, income and goals", "RateKit Press"
css = """@page{size:6in 9in;margin:0.5in}
*{box-sizing:border-box}body{margin:0;font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:#222;font-size:9.5pt}
.pg{height:8in;page-break-after:always;display:flex;flex-direction:column;overflow:hidden}
h1{font-size:22pt;margin:0}h2{font-size:13pt;margin:0 0 6pt;color:#0b6e4f;letter-spacing:.02em}
.lbl{font-size:7pt;text-transform:uppercase;letter-spacing:.1em;color:#777;margin:7pt 0 2pt}
.line{border-bottom:.6pt solid #bbb;height:17pt}
.box{border:.6pt solid #bbb;border-radius:3pt;padding:5pt;flex:1}
table{width:100%;border-collapse:collapse}td,th{border:.6pt solid #bbb;height:17pt;padding:0 4pt;font-size:8pt;text-align:left}
th{background:#eef5f2;font-weight:600}
.row{display:flex;gap:8pt}.row>*{flex:1}
.chk{display:flex;gap:5pt;align-items:center;border-bottom:.6pt solid #bbb;height:16pt}.chk i{width:8pt;height:8pt;border:.7pt solid #888;display:inline-block}
.date{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2pt solid #0b6e4f;padding-bottom:3pt;margin-bottom:4pt}
.center{justify-content:center;align-items:center;text-align:center}
"""
def lines(n): return "".join('<div class="line"></div>' for _ in range(n))
def chks(n): return "".join('<div class="chk"><i></i></div>' for _ in range(n))
pages = []
pages.append(f'<div class="pg center"><h1>{TITLE}</h1><p style="font-size:11pt;color:#555;margin-top:10pt">{SUB}</p><p style="margin-top:60pt">This planner belongs to</p><div class="line" style="width:70%"></div></div>')
pages.append('<div class="pg center"><p style="color:#999">This page is intentionally left blank.</p></div>')
pages.append('<div class="pg"><h2>How to use this planner</h2>' + "".join(f"<p>{t}</p>" for t in [
 "<b>Year at a glance.</b> Set your income goal and the three things you want your business to achieve this year.",
 "<b>Every week</b> has a two-page spread. On the left, plan your top priorities, client deadlines and tasks. On the right, log the hours you worked for each client, money invoiced and money received.",
 "<b>Every four weeks</b>, fill in a monthly review: what you earned, which clients paid best, and what to change.",
 "<b>Undated</b> so you can start any week of the year. Write the dates at the top of each spread.",
 "<b>Tip:</b> set aside a share of every payment for tax the day it arrives. The weekly money log has a column for it."]) + '</div>')
pages.append('<div class="pg"><h2>Year at a glance</h2><div class="lbl">Income goal for the year</div><div class="line"></div><div class="lbl">Monthly target</div><div class="line"></div>'
  '<div class="lbl">Three big goals</div>' + lines(3) + '<div class="lbl">Clients I want to work with</div>' + lines(4) +
  '<div class="lbl">Skills to learn</div>' + lines(3) + '<div class="lbl">My hourly rate now → by year end</div><div class="line"></div></div>')
pages.append('<div class="pg"><h2>Income tracker by month</h2><table><tr><th>Month</th><th>Invoiced</th><th>Received</th><th>Expenses</th><th>Tax saved</th><th>Profit</th></tr>' +
  "".join(f"<tr><td>{m}</td><td></td><td></td><td></td><td></td><td></td></tr>" for m in "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()) +
  '<tr><td><b>Total</b></td><td></td><td></td><td></td><td></td><td></td></tr></table><div class="lbl" style="margin-top:14pt">Notes</div>' + lines(8) + '</div>')
pages.append('<div class="pg"><h2>Client list</h2><table><tr><th style="width:30%">Client</th><th>Contact</th><th style="width:16%">Rate</th><th style="width:20%">Pays in (days)</th></tr>' + "<tr><td></td><td></td><td></td><td></td></tr>"*22 + '</table></div>')
for w in range(1, 53):
    left = (f'<div class="pg"><div class="date"><h2 style="margin:0">Week {w}</h2><span class="small">Dates: ____________ to ____________</span></div>'
      '<div class="lbl">Top 3 priorities</div>' + chks(3) +
      '<div class="lbl">Deadlines this week</div><table><tr><th style="width:24%">Day</th><th>Client / project</th><th style="width:20%">Done</th></tr>' + "<tr><td></td><td></td><td></td></tr>"*4 + '</table>'
      '<div class="lbl">To do</div>' + chks(13) +
      '<div class="lbl">Follow up / send invoices</div>' + chks(5) + '</div>')
    right = ('<div class="pg"><div class="lbl" style="margin-top:0">Time log</div><table><tr><th style="width:15%">Day</th><th>Client</th><th style="width:16%">Hours</th><th style="width:20%">Billable?</th></tr>' +
      "".join(f"<tr><td>{d}</td><td></td><td></td><td></td></tr>" for d in "Mon Tue Wed Thu Fri Sat Sun".split()) +
      '<tr><td><b>Total</b></td><td></td><td></td><td></td></tr></table>'
      '<div class="lbl">Money this week</div><table><tr><th>Invoiced</th><th>Received</th><th>Tax set aside</th></tr><tr><td></td><td></td><td></td></tr></table>'
      '<div class="lbl">Wins</div>' + lines(3) + '<div class="lbl">What I\'d do differently</div>' + lines(3) + '<div class="lbl">Notes</div>' + lines(7) + '</div>')
    pages += [left, right]
    if w % 4 == 0 and w <= 48:
        m = w // 4
        pages.append(f'<div class="pg"><h2>Monthly review {m}</h2><div class="row"><div><div class="lbl">Earned</div><div class="line"></div></div><div><div class="lbl">Hours billed</div><div class="line"></div></div><div><div class="lbl">Effective rate</div><div class="line"></div></div></div>'
          '<div class="lbl">Best client this month and why</div>' + lines(2) + '<div class="lbl">What worked</div>' + lines(3) + '<div class="lbl">What didn\'t</div>' + lines(3) +
          '<div class="lbl">Change next month</div>' + lines(3) + '<div class="lbl">Goals for next month</div>' + chks(3) + '</div>')
for _ in range(6): pages.append('<div class="pg"><h2>Notes</h2>' + lines(24) + '</div>')
if len(pages) % 2: pages.append('<div class="pg"><h2>Notes</h2>' + lines(24) + '</div>')
(OUT / "interior.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(pages)}</body></html>")
n = len(pages)
spine = n * 0.002252  # white paper, inches
W, H = 0.125 + 6 + spine + 6 + 0.125, 9.25
cover = f"""<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:{W}in {H}in;margin:0}}
body{{margin:0;width:{W}in;height:{H}in;display:flex;font-family:Inter,'Helvetica Neue',Arial,sans-serif}}
.back,.front{{width:{6.125}in;height:100%;background:#0b6e4f;color:#fff;position:relative}}
.spine{{width:{spine}in;height:100%;background:#084f39;color:#fff;display:flex;align-items:center;justify-content:center}}
.spine span{{writing-mode:vertical-rl;font-size:10pt;font-weight:700;letter-spacing:.05em;white-space:nowrap}}
.front .in{{position:absolute;left:0.6in;right:0.725in;top:1.6in}}
.front h1{{font-size:40pt;line-height:1.05;margin:0}}.front p{{font-size:14pt;opacity:.9;margin-top:18pt}}
.grid{{position:absolute;left:.6in;right:.725in;bottom:1.2in;display:grid;grid-template-columns:repeat(7,1fr);gap:6pt}}
.grid i{{height:28pt;border:1.2pt solid rgba(255,255,255,.45);border-radius:4pt}}.grid i:nth-child(3n){{background:rgba(255,255,255,.2)}}
.brand{{position:absolute;left:.6in;bottom:.6in;font-size:11pt;opacity:.8}}
.back .in{{position:absolute;left:.725in;right:.6in;top:1.2in;font-size:12pt;line-height:1.6}}
.back .barcode{{position:absolute;right:.6in;bottom:.6in;width:2in;height:1.2in;background:#fff}}
</style></head><body>
<div class="back"><div class="in"><p style="font-size:16pt;font-weight:700">Run your freelance business one week at a time.</p>
<p>52 undated weekly spreads to plan priorities, track deadlines, log hours per client and record what you invoice, what you're paid and what you set aside for tax.</p>
<p>Plus a year-at-a-glance goals page, a client list, a monthly income tracker, 12 monthly reviews and extra notes pages.</p><p>{n} pages · 6 × 9 in</p></div><div class="barcode"></div></div>
<div class="spine">{"<span>"+TITLE+"</span>" if n >= 100 else ""}</div>
<div class="front"><div class="in"><h1>{TITLE}</h1><p>{SUB}</p></div><div class="grid">{"<i></i>"*21}</div><div class="brand">{AUTHOR}</div></div>
</body></html>"""
(OUT / "cover.html").write_text(cover)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{OUT.resolve()}/interior.html');await p.pdf({{path:'{OUT.resolve()}/interior.pdf',preferCSSPageSize:true,printBackground:true}});
await p.goto('file://{OUT.resolve()}/cover.html');await p.pdf({{path:'{OUT.resolve()}/cover.pdf',preferCSSPageSize:true,printBackground:true}});
await b.close()}})()"""
subprocess.run(["node", "-e", js], check=True)
print(json.dumps({"pages": n, "spine_in": round(spine, 4), "cover_in": [round(W, 4), H]}))
