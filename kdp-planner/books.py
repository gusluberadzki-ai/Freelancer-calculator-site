"""Builds extra KDP low-content books (6x9, white paper). Run: python3 books.py"""
import pathlib, subprocess, json
OUT = pathlib.Path(__file__).parent / "books"; OUT.mkdir(exist_ok=True)
CSS = """@page{size:6in 9in;margin:0.5in}*{box-sizing:border-box}body{margin:0;font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:#222;font-size:9.5pt}
.pg{height:8in;page-break-after:always;display:flex;flex-direction:column;overflow:hidden}h1{font-size:22pt;margin:0}h2{font-size:13pt;margin:0 0 6pt;color:var(--c)}
.lbl{font-size:7pt;text-transform:uppercase;letter-spacing:.1em;color:#777;margin:6pt 0 1pt}.line{border-bottom:.6pt solid #bbb;height:17pt}
table{width:100%;border-collapse:collapse}td,th{border:.6pt solid #bbb;height:17pt;padding:0 4pt;font-size:8pt;text-align:left}th{background:var(--s);font-weight:600}
.center{justify-content:center;align-items:center;text-align:center}.entry{border:.7pt solid #bbb;border-radius:4pt;padding:4pt 7pt;margin-bottom:7pt;flex:1;display:flex;flex-direction:column;justify-content:space-evenly}
.entry .r{display:flex;gap:6pt;align-items:flex-end;border-bottom:.6pt solid #ccc;height:19pt}.entry .r span{font-size:7pt;text-transform:uppercase;letter-spacing:.08em;color:#777;width:62pt;flex:none;padding-bottom:2pt}
.tab{position:absolute;right:0;font-weight:800;color:#fff;background:var(--c);width:26pt;text-align:center;border-radius:4pt 0 0 4pt;padding:4pt 0;font-size:12pt}"""
def lines(n): return '<div class="line"></div>' * n
def render(slug, title, sub, author, color, soft, pages, back):
    if len(pages) % 2: pages.append('<div class="pg"><h2>Notes</h2>' + lines(24) + '</div>')
    (OUT / f"{slug}-interior.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>:root{{--c:{color};--s:{soft}}}{CSS}</style></head><body>{''.join(pages)}</body></html>")
    n = len(pages); spine = n * 0.002252; W = 12.25 + spine
    (OUT / f"{slug}-cover.html").write_text(f"""<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:{W}in 9.25in;margin:0}}
body{{margin:0;width:{W}in;height:9.25in;display:flex;font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:#fff}}
.b,.f{{width:6.125in;height:100%;background:{color};position:relative}}.s{{width:{spine}in;background:#0003;background-color:{color};filter:brightness(.8);display:flex;align-items:center;justify-content:center}}
.s span{{writing-mode:vertical-rl;font-size:9pt;font-weight:700;white-space:nowrap}}.f .in{{position:absolute;left:.6in;right:.725in;top:1.8in}}.f h1{{font-size:40pt;line-height:1.05;margin:0}}.f p{{font-size:14pt;opacity:.9;margin-top:18pt}}
.f .br{{position:absolute;left:.6in;bottom:.6in;font-size:11pt;opacity:.8}}.b .in{{position:absolute;left:.725in;right:.6in;top:1.2in;font-size:12pt;line-height:1.6}}
.deco{{position:absolute;left:.6in;right:.725in;bottom:1.3in;height:1.4in;border:1.5pt solid #fff8;border-radius:10pt}}.deco:after{{content:"";position:absolute;inset:14pt;border:1pt dashed #fff6;border-radius:6pt}}
</style></head><body><div class="b"><div class="in">{back}<p>{n} pages · 6 × 9 in</p></div></div>
<div class="s">{"<span>" + title + "</span>" if n >= 100 else ""}</div>
<div class="f"><div class="in"><h1>{title}</h1><p>{sub}</p></div><div class="deco"></div><div class="br">{author}</div></div></body></html>""")
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
for(const k of ['interior','cover']){{await p.goto('file://{OUT.resolve()}/{slug}-'+k+'.html');await p.pdf({{path:'{OUT.resolve()}/{slug}-'+k+'.pdf',preferCSSPageSize:true,printBackground:true}});}}await b.close()}})()"""
    subprocess.run(["node", "-e", js], check=True)
    print(json.dumps({"book": slug, "pages": n, "cover_in": [round(W, 4), 9.25], "spine_in": round(spine, 4)}))

# 1. Password log book
P = [f'<div class="pg center"><h1>Password Log Book</h1><p style="color:#555;margin-top:10pt">Internet address and password organiser</p><p style="margin-top:60pt">If found, please return to</p>{lines(2)}</div>',
     '<div class="pg center"><p style="color:#999">Keep this book somewhere safe and private.</p></div>',
     '<div class="pg"><h2>Important accounts</h2>' + "".join(f'<div class="lbl">{x}</div>' + lines(2) for x in ["Email", "Bank", "Phone / mobile carrier", "Internet provider", "Wi-Fi network & password", "Computer login", "Cloud storage", "Router admin"]) + '</div>']
def entry(): return '<div class="entry">' + "".join(f'<div class="r"><span>{x}</span></div>' for x in ["Website", "Username", "Email", "Password", "Notes"]) + '</div>'
for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    for i in range(4 if ch not in "QXYZ" else 2):
        P.append(f'<div class="pg" style="position:relative"><div class="tab">{ch}</div><div style="width:85%;display:flex;flex-direction:column;flex:1">' + "".join(entry() for _ in range(4)) + '</div></div>')
P.append('<div class="pg"><h2>Software licence keys</h2><table><tr><th>Software</th><th>Licence key</th><th style="width:20%">Bought</th></tr>' + "<tr><td></td><td></td><td></td></tr>" * 22 + '</table></div>')
P += ['<div class="pg"><h2>Notes</h2>' + lines(24) + '</div>'] * 3
render("password-log-book", "Password Log Book", "Alphabetical internet address and password organiser with A–Z tabs", "RateKit Press", "#2d3a4a", "#e8ecf1", P,
       '<p style="font-size:16pt;font-weight:700">Never forget a password again.</p><p>A to Z tabbed pages with room for over 380 websites: address, username, email, password and notes for each.</p><p>Plus pages for your most important accounts, home network settings and software licence keys.</p>')

# 2. Budget planner journal
B = ['<div class="pg center"><h1>Monthly Budget Planner</h1><p style="color:#555;margin-top:10pt">Undated 12-month budget book and expense tracker</p><p style="margin-top:60pt">This planner belongs to</p>' + lines(1) + '</div>',
     '<div class="pg center"><p style="color:#999">This page is intentionally left blank.</p></div>',
     '<div class="pg"><h2>Financial goals</h2>' + "".join(f'<div class="lbl">{x}</div>' + lines(3) for x in ["This year I want to save", "Debts to pay off", "Big purchases to plan for", "Habits to change"]) + '<div class="lbl">Emergency fund target</div>' + lines(1) + '</div>',
     '<div class="pg"><h2>Debt tracker</h2><table><tr><th>Debt</th><th>Balance</th><th>Rate</th><th>Min. payment</th><th>Paid off</th></tr>' + "<tr><td></td><td></td><td></td><td></td><td></td></tr>" * 12 + '</table><h2 style="margin-top:14pt">Savings goals</h2><table><tr><th>Goal</th><th>Target</th><th>By</th><th>Saved</th></tr>' + "<tr><td></td><td></td><td></td><td></td></tr>" * 8 + '</table></div>']
for m in range(1, 13):
    B.append(f'<div class="pg"><h2>Month {m}: budget</h2><div class="lbl">Month & year</div>' + lines(1) +
      '<table style="margin-top:6pt"><tr><th>Income</th><th style="width:25%">Expected</th><th style="width:25%">Actual</th></tr>' + "<tr><td></td><td></td><td></td></tr>" * 4 +
      '</table><table style="margin-top:8pt"><tr><th>Expenses</th><th style="width:25%">Budget</th><th style="width:25%">Actual</th></tr>' +
      "".join(f"<tr><td>{c}</td><td></td><td></td></tr>" for c in ["Housing", "Utilities", "Groceries", "Transport", "Insurance", "Phone & internet", "Eating out", "Shopping", "Health", "Fun", "Savings", "Debt payments", "", ""]) +
      '<tr><td><b>Total</b></td><td></td><td></td></tr></table></div>')
    B.append(f'<div class="pg"><h2>Month {m}: bills</h2><table><tr><th>Bill</th><th style="width:16%">Due</th><th style="width:20%">Amount</th><th style="width:14%">Paid</th></tr>' + "<tr><td></td><td></td><td></td><td></td></tr>" * 12 +
      '</table><h2 style="margin-top:12pt">Month review</h2><div class="lbl">Income − spending = left over</div>' + lines(1) + '<div class="lbl">What went well</div>' + lines(2) + '<div class="lbl">Change next month</div>' + lines(2) + '</div>')
    for half in (1, 2):
        B.append(f'<div class="pg"><h2>Month {m}: expense log {half}/2</h2><table><tr><th style="width:15%">Date</th><th>Description</th><th style="width:22%">Category</th><th style="width:17%">Amount</th></tr>' + "<tr><td></td><td></td><td></td><td></td></tr>" * 25 + '</table></div>')
B.append('<div class="pg"><h2>Year in review</h2><table><tr><th>Month</th><th>Income</th><th>Spent</th><th>Saved</th></tr>' + "".join(f"<tr><td>{i}</td><td></td><td></td><td></td></tr>" for i in range(1, 13)) + '<tr><td><b>Total</b></td><td></td><td></td><td></td></tr></table><div class="lbl" style="margin-top:12pt">Biggest wins this year</div>' + lines(4) + '</div>')
B += ['<div class="pg"><h2>Notes</h2>' + lines(24) + '</div>'] * 4
render("budget-planner-book", "Monthly Budget Planner", "Undated 12-month budget book with expense tracker, bill organiser and savings goals", "RateKit Press", "#7a3b8f", "#f1e6f5", B,
       '<p style="font-size:16pt;font-weight:700">Take control of your money, one month at a time.</p><p>12 undated months, each with a budget page, a bill tracker, two pages of expense logs and a monthly review.</p><p>Plus financial goals, a debt tracker, savings goals and a year in review.</p>')
