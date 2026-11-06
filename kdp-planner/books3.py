"""Round 7 KDP books: 5 low-content books + 2 longer premium books.
Run: python3 books3.py  (reuses CSS/lines() from books.py; adds trim size + gutter support)"""
import pathlib, subprocess, json
_src = (pathlib.Path(__file__).parent / "books.py").read_text()
exec(_src[:_src.index("# 1. Password log book")])

AUTHOR = "RateKit Press"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def gutter(n):  # KDP minimum inside margin by page count (no bleed)
    return 0.375 if n <= 150 else 0.5 if n <= 300 else 0.625 if n <= 500 else 0.75


def render2(slug, title, sub, color, soft, pages, back, trim=(6, 9), number=False, extra_css=""):
    tw, th = trim
    if len(pages) % 2:
        pages.append('<div class="pg"><h2>Notes</h2>' + lines(24 if th == 9 else 32) + '</div>')
    n = len(pages)
    if number:  # page numbers in the outside bottom corner
        pages = [p[:-6] + f'<div class="pn">{i + 1}</div></div>' if i > 1 else p for i, p in enumerate(pages)]
    g = max(gutter(n), 0.5)
    css = CSS.replace("@page{size:6in 9in;margin:0.5in}", f"@page{{size:{tw}in {th}in;margin:0.5in}}@page :right{{margin-left:{g}in;margin-right:0.45in}}@page :left{{margin-left:0.45in;margin-right:{g}in}}") \
             .replace("height:8in", f"height:{th - 1}in")
    css += ".pg{position:relative}.pn{position:absolute;bottom:-2pt;right:0;font-size:7pt;color:#999}" + extra_css
    (OUT / f"{slug}-interior.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>:root{{--c:{color};--s:{soft}}}{css}</style></head><body>{''.join(pages)}</body></html>")
    spine = n * 0.002252; pw = tw + 0.125; W = 2 * pw + spine; H = th + 0.25
    big = tw > 7
    (OUT / f"{slug}-cover.html").write_text(f"""<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:{W}in {H}in;margin:0}}
body{{margin:0;width:{W}in;height:{H}in;display:flex;font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:#fff}}
.b,.f{{width:{pw}in;height:100%;background:{color};position:relative}}.s{{width:{spine}in;background-color:{color};filter:brightness(.8);display:flex;align-items:center;justify-content:center}}
.s span{{writing-mode:vertical-rl;font-size:{14 if spine > 0.6 else 9}pt;font-weight:700;white-space:nowrap}}.f .in{{position:absolute;left:.6in;right:.725in;top:{2.2 if big else 1.8}in}}.f h1{{font-size:{56 if big else 40}pt;line-height:1.05;margin:0}}.f p{{font-size:{18 if big else 14}pt;opacity:.9;margin-top:18pt}}
.f .br{{position:absolute;left:.6in;bottom:.6in;font-size:11pt;opacity:.8}}.b .in{{position:absolute;left:.725in;right:.6in;top:1.2in;font-size:{14 if big else 12}pt;line-height:1.6}}
.deco{{position:absolute;left:.6in;right:.725in;bottom:1.3in;height:{2.2 if big else 1.4}in;border:1.5pt solid #fff8;border-radius:10pt}}.deco:after{{content:"";position:absolute;inset:14pt;border:1pt dashed #fff6;border-radius:6pt}}
.tag{{display:inline-block;border:1pt solid #fffa;border-radius:20pt;padding:3pt 12pt;font-size:10pt;letter-spacing:.12em;text-transform:uppercase;margin-bottom:16pt}}
</style></head><body><div class="b"><div class="in">{back}<p>{n} pages · {tw} × {th} in</p></div></div>
<div class="s">{"<span>" + title + " · " + AUTHOR + "</span>" if n >= 100 else ""}</div>
<div class="f"><div class="in">{'<div class="tag">Premium edition</div>' if big or n > 300 else ''}<h1>{title}</h1><p>{sub}</p></div><div class="deco"></div><div class="br">{AUTHOR}</div></div></body></html>""")
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
for(const k of ['interior','cover']){{await p.goto('file://{OUT.resolve()}/{slug}-'+k+'.html');await p.pdf({{path:'{OUT.resolve()}/{slug}-'+k+'.pdf',preferCSSPageSize:true,printBackground:true}});}}await b.close()}})()"""
    subprocess.run(["node", "-e", js], check=True)
    print(json.dumps({"book": slug, "pages": n, "trim": trim, "cover_in": [round(W, 3), H], "spine_in": round(spine, 3), "gutter_in": g}))


def title_page(t, sub, owner="This book belongs to"):
    return [f'<div class="pg center"><h1>{t}</h1><p style="color:#555;margin-top:10pt">{sub}</p><p style="margin-top:60pt">{owner}</p>{lines(1)}</div>',
            '<div class="pg center"><p style="color:#999">This page is intentionally left blank.</p></div>']


def fields(names, n=1): return "".join(f'<div class="lbl">{x}</div>' + lines(n) for x in names)
def table(heads, rows, widths=None, h=None):
    w = widths or [None] * len(heads)
    th = "".join(f'<th{f" style=width:{x}%" if x else ""}>{t}</th>' for t, x in zip(heads, w))
    tr = f"<tr{f' style=height:{h}pt' if h else ''}>" + "<td></td>" * len(heads) + "</tr>"
    return f"<table><tr>{th}</tr>{tr * rows}</table>"
def tpage(t, heads, rows, widths=None, h=None): return f'<div class="pg"><h2>{t}</h2>{table(heads, rows, widths, h)}</div>'
def notes(n=24): return f'<div class="pg"><h2>Notes</h2>{lines(n)}</div>'
def row2(*cols): return '<div style="display:flex;gap:10pt">' + "".join(f'<div style="flex:1">{c}</div>' for c in cols) + '</div>'
def stars(): return '<span style="color:#999;font-size:12pt">☆ ☆ ☆ ☆ ☆</span>'
def hdr(t, right="Date: ____________"): return f'<div style="display:flex;justify-content:space-between;align-items:baseline"><h2>{t}</h2><span>{right}</span></div>'
def month_grid(cell_h):
    return ('<table style="table-layout:fixed"><tr>' + "".join(f"<th style='text-align:center'>{d}</th>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) + "</tr>"
            + (f"<tr style='height:{cell_h}pt'>" + "<td></td>" * 7 + "</tr>") * 6 + "</table>")
def checks(items): return "".join(f'<div style="display:flex;gap:6pt;align-items:flex-end;height:17pt;border-bottom:.6pt solid #ddd"><span>☐</span><span>{x}</span></div>' for x in items)


# 1. Address book (large print)
P = title_page("Address Book", "Large print A–Z address and phone book", "If found, please return to")
P.append('<div class="pg"><h2>Emergency contacts</h2>' + table(["Name", "Relationship", "Phone"], 12, [40, 25, 35], 26) + '</div>')
def addr(): return '<div class="entry">' + "".join(f'<div class="r"><span>{x}</span></div>' for x in ["Name", "Address", "", "Phone", "Mobile", "Email", "Birthday"]) + '</div>'
for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    for i in range(4 if ch not in "QUVXYZ" else 2):
        P.append(f'<div class="pg"><div class="tab">{ch}</div><div style="width:85%;display:flex;flex-direction:column;flex:1">' + addr() * 3 + '</div></div>')
for a in range(0, 12, 3):
    P.append('<div class="pg"><h2>Birthdays & anniversaries</h2>' + "".join(f'<div class="lbl" style="color:var(--c);font-weight:700">{m}</div>' + table(["Day", "Name", "Occasion"], 6, [14, 56, 30]) for m in MONTHS[a:a + 3]) + '</div>')
P += [tpage("Christmas card list", ["Name", "Sent", "Received"], 24, [60, 20, 20]) for _ in range(2)] + [notes()] * 2
render2("address-book", "Address Book", "Large print A–Z address and phone book with birthday calendar", "#3d5a80", "#e3eaf3", P,
        '<p style="font-size:16pt;font-weight:700">Everyone you care about, in one easy-to-read book.</p><p>A–Z tabbed pages with room for 270 contacts: name, address, phone, mobile, email and birthday.</p><p>Plus emergency contacts, a birthday and anniversary calendar and a Christmas card list. Large, clear print.</p>')

# 2. Reading journal
P = title_page("Reading Journal", "A book lover's log for 100 books")
P.append('<div class="pg"><h2>52-book challenge</h2><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:5pt;flex:1">' + "".join(f'<div style="border:.6pt solid #bbb;border-radius:3pt;font-size:7pt;padding:3pt;color:#999">{i}</div>' for i in range(1, 53)) + '</div></div>')
for a in (1, 51):
    P.append('<div class="pg"><h2>Books I\'ve read</h2><table><tr><th style="width:9%">#</th><th>Title</th><th style="width:16%">Page</th></tr>' + "".join(f"<tr><td>{i}</td><td></td><td>{i * 2 + 7}</td></tr>" for i in range(a, a + 25)) + '</table></div>')
    P.append('<div class="pg"><h2>Books I\'ve read</h2><table><tr><th style="width:9%">#</th><th>Title</th><th style="width:16%">Page</th></tr>' + "".join(f"<tr><td>{i}</td><td></td><td>{i * 2 + 7}</td></tr>" for i in range(a + 25, a + 50)) + '</table></div>')
P.append('<div class="pg"><h2>How to use</h2><p style="line-height:1.7">Log each book on a two-page spread: details and rating on the left, thoughts and favourite quotes on the right. Note it in the index so you can find it again. Use the challenge grid to tick off a book a week.</p></div>')
for i in range(1, 101):
    P.append(f'<div class="pg">{hdr(f"Book {i}", stars())}' + fields(["Title", "Author"]) + row2(fields(["Genre"]), fields(["Format"])) + row2(fields(["Started"]), fields(["Finished"])) + row2(fields(["Pages"]), fields(["Recommended by"]))
             + '<div class="lbl">Summary</div>' + lines(6) + '<div class="lbl">Characters I loved</div>' + lines(3) + '</div>')
    P.append('<div class="pg"><h2>Thoughts</h2>' + lines(12) + '<div class="lbl">Favourite quotes</div>' + lines(6) + '<div class="lbl">Would I read it again?   Yes ☐   No ☐   Maybe ☐</div></div>')
P += [tpage("To be read", ["Title", "Author", "✓"], 24, [55, 35, 10]) for _ in range(3)] + [tpage("Books lent & borrowed", ["Book", "Lent to / from", "Date", "Back"], 24, [40, 30, 15, 15])]
render2("reading-journal-book", "Reading Journal", "A book lover's log and review notebook for 100 books", "#6b4c3b", "#f2ebe6", P,
        '<p style="font-size:16pt;font-weight:700">Remember every book you read.</p><p>100 two-page book reviews with ratings, dates, summary, favourite characters, thoughts and quotes.</p><p>Plus an indexed book list, a 52-book challenge, to-be-read lists and a lending log. A perfect gift for readers.</p>')

# 3. Newborn baby log
P = title_page("Baby's First 120 Days", "Newborn log for feeding, sleep and diapers")
P.append('<div class="pg"><h2>About baby</h2>' + fields(["Name", "Date & time of birth", "Weight at birth", "Length at birth", "Place of birth", "Paediatrician", "Paediatrician phone", "Allergies"]) + '</div>')
P.append(tpage("Growth", ["Date", "Age", "Weight", "Length", "Head"], 24))
P.append(tpage("Doctor visits & vaccinations", ["Date", "Reason / vaccine", "Notes"], 24, [16, 44, 40]))
for d in range(1, 121):
    P.append(f'<div class="pg">{hdr(f"Day {d}")}<div style="display:flex;gap:8pt;flex:1"><div style="flex:3">'
             + '<div class="lbl">Feeding</div>' + table(["Time", "L / R / Bottle", "Amount / min"], 12)
             + '<div class="lbl">Sleep</div>' + table(["From", "To", "Total"], 6) + '</div>'
             + '<div style="flex:2"><div class="lbl">Diapers</div>' + table(["Time", "Wet", "Dirty"], 12, [44, 28, 28])
             + '<div class="lbl">Medicine / temp.</div>' + lines(2) + '<div class="lbl">Notes</div>' + lines(3) + '</div></div></div>')
P.append('<div class="pg"><h2>Milestones</h2>' + table(["Milestone", "Date"], 1, [70, 30]).replace("<tr><td></td><td></td></tr>", "") .replace("</table>", "".join(f"<tr><td>{m}</td><td></td></tr>" for m in ["First smile", "First laugh", "Holds head up", "Rolls over", "Sleeps through the night", "First bath", "First outing", "Grasps a toy", "Recognises faces", "Coos and babbles", "", "", "", ""]) + "</table>") + '</div>')
P += [notes()] * 2
render2("baby-log-book", "Baby's First 120 Days", "Newborn log book for feeding, sleep, diapers and milestones", "#4f7cac", "#e6eef7", P,
        '<p style="font-size:16pt;font-weight:700">Know exactly when baby last ate, slept and needed a change.</p><p>120 daily pages for feeds (breast or bottle), sleep and diapers, plus medicine and notes.</p><p>Also a growth chart, doctor and vaccination log and first milestones. Handy for night feeds and sharing with your partner or doctor.</p>')

# 4. Dog health record
P = title_page("My Dog's Health Record", "Vet visits, vaccinations, medication and care log", "Owner")
P.append('<div class="pg"><h2>About my dog</h2><div style="border:.6pt dashed #bbb;height:1.8in;display:flex;align-items:center;justify-content:center;color:#aaa;margin-bottom:6pt">Photo</div>' + row2(fields(["Name", "Breed", "Colour / markings", "Microchip no."]), fields(["Date of birth", "Sex · neutered?", "Adopted / from", "Licence / tag no."])) + fields(["Insurance & policy no.", "Allergies"]) + '</div>')
P.append('<div class="pg"><h2>Important contacts</h2>' + "".join(f'<div class="lbl" style="color:var(--c);font-weight:700">{x}</div>' + lines(2) for x in ["Vet", "Emergency vet (24h)", "Groomer", "Dog walker / sitter", "Boarding kennel", "Trainer", "Pet poison hotline"]) + '</div>')
P.append(tpage("Vaccinations", ["Date", "Vaccine", "Vet", "Next due"], 24, [17, 40, 23, 20]))
P.append(tpage("Flea, tick & worming", ["Date", "Product", "Dose", "Next due"], 24, [17, 40, 23, 20]))
P.append(tpage("Medication", ["Start", "Medication", "Dose / how often", "End"], 24, [15, 35, 35, 15]))
P.append(tpage("Weight", ["Date", "Weight", "Notes"], 24, [20, 20, 60]))
for i in range(1, 61):
    P.append(f'<div class="pg">{hdr(f"Vet visit {i}")}' + row2(fields(["Vet / clinic"]), fields(["Weight"])) + fields(["Reason for visit"], 2) + fields(["Diagnosis"], 3) + fields(["Treatment & medication"], 3) + row2(fields(["Cost"]), fields(["Follow-up date"])) + fields(["Notes"], 4) + '</div>')
for t in ("Grooming log", "Food & diet changes"):
    P += [tpage(t, ["Date", "Details", "Notes"], 24, [17, 48, 35])] * 2
P.append('<div class="pg"><h2>Pet sitter instructions</h2>' + fields(["Feeding (what, how much, when)", "Walks & exercise", "Medication", "Habits, fears & commands", "House rules"], 3) + '</div>')
P.append(tpage("Training & commands", ["Command / trick", "Started", "Mastered"], 24, [60, 20, 20]))
P += [notes()] * 3
render2("dog-health-record", "My Dog's Health Record", "Vet visits, vaccinations, medication, weight and care log", "#2f6f5e", "#e3f0ec", P,
        '<p style="font-size:16pt;font-weight:700">Your dog\'s whole health history in one place.</p><p>60 vet visit pages plus logs for vaccinations, flea, tick and worming treatment, medication, weight, grooming and diet.</p><p>Also a profile with photo page, key contacts, pet sitter instructions and training tracker.</p>')

# 5. Garden journal
GRID = 'background-image:linear-gradient(#bbb 1px,transparent 1px),linear-gradient(90deg,#bbb 1px,transparent 1px);background-size:14.4pt 14.4pt;border:.6pt solid #bbb;flex:1'
P = title_page("Garden Journal", "Planner and log book for gardeners")
P.append('<div class="pg"><h2>My garden</h2>' + fields(["Location", "Growing zone", "Last spring frost", "First autumn frost", "Soil type", "Sun exposure"]) + '<div class="lbl">Goals for this year</div>' + lines(8) + '</div>')
for y in range(1, 4):
    P.append(f'<div class="pg"><h2>Garden layout · plan {y}</h2><div style="{GRID}"></div></div>')
P.append(tpage("Seed inventory", ["Plant / variety", "Source", "Year", "Qty"], 24, [45, 25, 15, 15]))
P.append(tpage("Seed inventory", ["Plant / variety", "Source", "Year", "Qty"], 24, [45, 25, 15, 15]))
for m in MONTHS:
    P.append(f'<div class="pg"><h2>{m}</h2><div class="lbl">To sow</div>{lines(4)}<div class="lbl">To plant out</div>{lines(4)}<div class="lbl">Jobs to do</div>' + checks([""] * 8) + f'<div class="lbl">Notes</div>{lines(4)}</div>')
for i in range(1, 41):
    P.append(f'<div class="pg">{hdr(f"Plant profile {i}", stars())}' + row2(fields(["Plant"]), fields(["Variety"])) + row2(fields(["Sown"]), fields(["Planted out"])) + row2(fields(["Location"]), fields(["Sun / water"]))
             + row2(fields(["Germinated"]), fields(["First harvest"])) + fields(["Care & feeding"], 3) + fields(["Pests & problems"], 2) + fields(["Results · grow again?"], 3) + '</div>')
for _ in range(4): P.append(tpage("Planting log", ["Date", "Plant", "Where", "Notes"], 24, [15, 30, 20, 35]))
for _ in range(4): P.append(tpage("Harvest log", ["Date", "Crop", "Amount", "Notes"], 24, [15, 30, 20, 35]))
for _ in range(3): P.append(tpage("Weather log", ["Date", "Weather", "High / low", "Rain"], 24, [15, 45, 20, 20]))
P += [notes()] * 3
render2("garden-journal", "Garden Journal", "Planner and log book for vegetable and flower gardeners", "#55703a", "#eaf0e2", P,
        '<p style="font-size:16pt;font-weight:700">Plan it. Grow it. Remember what worked.</p><p>40 plant profiles, 12 monthly to-do pages, grid pages for garden layouts and logs for seeds, planting, harvests and weather.</p><p>Undated, for any year. A lovely gift for gardeners.</p>')

# 6. PREMIUM: Undated daily planner, 6x9, full year (~400 pages)
HOURS = ["6", "7", "8", "9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
P = title_page("The Daily Planner", "One full year, one page a day. Undated.")
P.append('<div class="pg"><h2>How to use this planner</h2><p style="line-height:1.7">Each month opens with a calendar and a goals page. Then every day has its own page: write the date, your top three priorities, your schedule from 6 am to 9 pm, a to-do list, a habit check, water and a line of gratitude. At the end of each month, look back on the review page.</p><p style="line-height:1.7">It\'s undated, so you can start on any day of the year and never waste a page.</p></div>')
P.append('<div class="pg"><h2>This year</h2>' + fields(["My word for the year"]) + "".join(f'<div class="lbl">{x}</div>' + lines(3) for x in ["Health", "Work & money", "Relationships", "Growth & learning", "Fun & adventure"]) + '</div>')
P.append('<div class="pg"><h2>Year at a glance</h2><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6pt;flex:1">' + "".join(f'<div style="border:.6pt solid #bbb;border-radius:3pt;padding:3pt"><div class="lbl" style="margin:0">{m}</div></div>' for m in MONTHS) + '</div></div>')
P.append('<div class="pg"><h2>Important dates</h2>' + table(["Date", "Occasion"], 24, [25, 75]) + '</div>')
P.append(tpage("Habits to build", ["Habit", "Why"], 24, [40, 60]))
for mi, m in enumerate(MONTHS):
    P.append(f'<div class="pg"><h2>Month {mi + 1}: ________________</h2>{month_grid(62)}<div class="lbl">Focus</div>{lines(3)}</div>')
    P.append(f'<div class="pg"><h2>Month {mi + 1} goals</h2>' + "".join(f'<div class="lbl">{x}</div>' + lines(3) for x in ["Top 3 goals", "Habits to track", "Bills & deadlines", "Things to look forward to"]) + '<div class="lbl">Habit tracker (days 1–31)</div>'
             + '<table style="table-layout:fixed"><tr><th style="width:24%">Habit</th>' + "".join(f"<th style='font-size:5pt;padding:0;text-align:center'>{d}</th>" for d in range(1, 32)) + '</tr>' + ("<tr><td></td>" + "<td style='padding:0'></td>" * 31 + "</tr>") * 10 + '</table></div>')
    for d in range(DAYS[mi] + (1 if mi == 1 else 0) - (1 if mi == 1 else 0)):
        P.append('<div class="pg"><div style="display:flex;justify-content:space-between;align-items:baseline"><span style="font-size:13pt;font-weight:700;color:var(--c)">Date ____ / ____ / ______</span><span style="letter-spacing:4pt;color:#777;font-size:8pt">M T W T F S S</span></div>'
                 + '<div style="display:flex;gap:10pt;flex:1;margin-top:4pt"><div style="flex:1.1"><div class="lbl">Schedule</div>'
                 + "".join(f'<div style="display:flex;align-items:flex-end;height:24pt;border-bottom:.6pt solid #ccc"><span style="width:14pt;font-size:7pt;color:#999">{h}</span></div>' for h in HOURS)
                 + '<div class="lbl">Water</div><div style="letter-spacing:5pt;color:#999">◯◯◯◯◯◯◯◯</div></div>'
                 + '<div style="flex:1"><div class="lbl">Top 3 priorities</div>' + "".join(f'<div style="display:flex;align-items:flex-end;height:18pt;border-bottom:.6pt solid #ccc"><b style="color:var(--c);width:10pt">{i}</b></div>' for i in (1, 2, 3))
                 + '<div class="lbl">To do</div>' + checks([""] * 10) + '<div class="lbl">Grateful for</div>' + lines(3) + '<div class="lbl">Notes</div>' + lines(5) + '</div></div></div>')
    P.append(f'<div class="pg"><h2>Month {mi + 1} review</h2>' + "".join(f'<div class="lbl">{x}</div>' + lines(4) for x in ["Wins", "What didn\'t go to plan", "What I learned", "Next month I will"]) + '<div class="lbl">Rate this month</div>' + stars() + '</div>')
P.append('<div class="pg"><h2>Year in review</h2>' + "".join(f'<div class="lbl">{x}</div>' + lines(4) for x in ["Best moments", "Biggest achievements", "What I\'m proud of", "Lessons", "Next year"]) + '</div>')
P += [notes()] * 4
render2("daily-planner-premium", "The Daily Planner", "A full undated year: 365 daily pages, monthly calendars, goals, habit trackers and reviews", "#22333b", "#e6ebed", P,
        '<p style="font-size:16pt;font-weight:700">Plan every single day of your year.</p><p>365 undated daily pages with an hourly schedule from 6 am to 9 pm, top three priorities, to-do list, water tracker and gratitude.</p><p>Each month opens with a calendar, goals and a habit tracker, and ends with a review. Plus yearly goals, important dates and a year in review.</p>')

# 7. PREMIUM: Home & family organizer, 8.5x11 (~210 pages, numbered, with contents)
CSS_BIG = "body{font-size:10.5pt}h1{font-size:30pt}h2{font-size:16pt}td,th{height:21pt;font-size:9pt}.line{height:21pt}.lbl{font-size:8pt}"
SECTIONS, P = [], [f'<div class="pg center"><div style="font-size:9pt;letter-spacing:.2em;text-transform:uppercase;color:#999">Premium edition</div><h1 style="margin-top:8pt">The Home & Family Organizer</h1><p style="color:#555;margin-top:10pt;font-size:13pt">Everything your household needs to know, in one book</p><p style="margin-top:80pt">The ____________________ family</p></div>',
                   '<div class="pg center"><p style="color:#999">Keep this book somewhere safe. It holds private information.</p></div>', "CONTENTS"]
def section(name, pages):
    SECTIONS.append((name, len(P) + 1)); P.extend(pages)
def bigt(t, heads, rows, widths=None): return tpage(t, heads, rows, widths)
section("Household information", ['<div class="pg"><h2>Our home</h2>' + row2(fields(["Address", "Moved in", "Landlord / mortgage lender", "Account number"]), fields(["Home phone", "Wi-Fi network", "Wi-Fi password", "Alarm code location"])) + '<div class="lbl">Where things are</div>' + table(["Item", "Location"], 10, [40, 60]) + '</div>',
                                  bigt("Utilities & services", ["Service", "Provider", "Account no.", "Phone", "Due"], 28, [18, 24, 22, 22, 14])])
section("Emergency plan", [bigt("Emergency contacts", ["Name", "Relationship", "Phone", "Notes"], 28, [28, 20, 22, 30]),
                           '<div class="pg"><h2>Emergency plan</h2>' + fields(["Meeting place near home", "Meeting place out of area", "Out-of-town contact", "Water shut-off", "Gas shut-off", "Electrical panel", "Fire extinguishers", "First aid kit", "Pet plan"], 2) + '</div>',
                           '<div class="pg"><h2>Emergency kit checklist</h2>' + row2(checks(["Water (1 gal/person/day)", "Non-perishable food", "Torch & batteries", "First aid kit", "Medications", "Radio", "Phone chargers", "Cash", "Copies of documents", "Blankets", "Whistle", "Dust masks"]), checks(["Wipes & bin bags", "Tools / wrench", "Local maps", "Pet food", "Baby supplies", "Spare glasses", "Change of clothes", "Matches", "Rain gear", "", "", ""])) + '</div>'])
section("Family members", ['<div class="pg"><h2>Family member</h2>' + row2(fields(["Name", "Date of birth", "Blood type", "Phone"]), fields(["Doctor", "Dentist", "School / work", "Insurance no."])) + fields(["Allergies", "Medical conditions"], 2) + '<div class="lbl">Medications</div>' + table(["Medication", "Dose", "Prescribed by"], 5) + '<div class="lbl">Sizes</div>' + table(["Clothes", "Shoes", "Rings", "Other"], 1) + '</div>' for _ in range(6)])
section("Medical log", [bigt("Medical & dental appointments", ["Date", "Who", "Doctor", "Reason", "Follow-up"], 28, [13, 15, 20, 37, 15]) for _ in range(6)] + [bigt("Vaccination record", ["Who", "Vaccine", "Date", "Next due"], 28, [25, 35, 20, 20]) for _ in range(2)])
section("Birthdays & anniversaries", ['<div class="pg"><h2>Birthdays & anniversaries</h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:8pt">' + "".join(f'<div><div class="lbl" style="color:var(--c);font-weight:700">{m}</div>' + table(["Day", "Name"], 5, [18, 82]) + '</div>' for m in MONTHS[a:a + 6]) + '</div></div>' for a in (0, 6)])
mp = []
for mi in range(12):
    mp.append(f'<div class="pg"><h2>Month {mi + 1}: ________________</h2>{month_grid(78)}<div class="lbl">Notes</div>{lines(5)}</div>')
    mp.append(f'<div class="pg"><h2>Month {mi + 1} budget</h2>' + row2(fields(["Income"]), fields(["Planned spend"]), fields(["Savings goal"])) + table(["Category", "Budget", "Actual", "Difference"], 22, [40, 20, 20, 20]) + '</div>')
    mp.append(f'<div class="pg"><h2>Month {mi + 1} bills</h2>' + table(["Bill", "Due", "Amount", "Paid ✓", "Notes"], 26, [30, 12, 16, 12, 30]) + '</div>')
section("Monthly calendars, budgets & bills", mp)
wk = []
for w in range(1, 53):
    wk.append(f'<div class="pg">{hdr(f"Week {w} · meals", "Week of: ____________")}<div style="display:flex;gap:10pt;flex:1"><div style="flex:2">'
              + '<table style="table-layout:fixed"><tr><th style="width:16%"></th><th>Breakfast</th><th>Lunch</th><th>Dinner</th></tr>' + "".join(f"<tr style='height:64pt'><th>{d}</th><td></td><td></td><td></td></tr>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) + '</table></div>'
              + '<div style="flex:1"><div class="lbl" style="margin-top:0">Grocery list</div>' + checks([""] * 26) + '</div></div></div>')
section("Weekly meal planner & grocery lists", wk)
section("Favourite recipes", ['<div class="pg"><h2>Recipe</h2>' + row2(fields(["Name"]), fields(["Serves · time"])) + row2('<div class="lbl">Ingredients</div>' + lines(20), '<div class="lbl">Method</div>' + lines(20)) + fields(["Notes"], 3) + '</div>' for _ in range(10)])
section("Cleaning", ['<div class="pg"><h2>Cleaning schedule</h2>' + row2('<div class="lbl">Daily</div>' + checks(["Make beds", "Dishes", "Wipe counters", "Tidy living areas", "Sweep kitchen", "", ""]) + '<div class="lbl">Weekly</div>' + checks(["Vacuum", "Mop floors", "Bathrooms", "Change bedding", "Dust", "Laundry", "Bins out", "", ""]),
                                                                                    '<div class="lbl">Monthly</div>' + checks(["Clean oven", "Fridge clear-out", "Wash windows", "Skirting boards", "Vacuum sofa", "Descale kettle", "", ""]) + '<div class="lbl">Seasonal</div>' + checks(["Carpets", "Gutters", "Curtains", "Mattresses", "Garage", "Wardrobe swap", "", ""])) + '</div>']
        + [bigt("Deep-clean tracker", ["Room", "Task", "Last done", "Next"], 28, [20, 44, 18, 18]) for _ in range(2)])
section("Home maintenance", [bigt("Maintenance schedule", ["Task", "How often", "Last done", "Next due"], 28, [40, 20, 20, 20])] + [bigt("Repairs & improvements log", ["Date", "Work done", "Contractor", "Cost"], 28, [14, 46, 24, 16]) for _ in range(3)] + [bigt("Trusted tradespeople", ["Trade", "Name", "Phone", "Notes"], 28, [18, 26, 22, 34])])
section("Home inventory", [f'<div class="pg"><h2>Home inventory · room: ____________</h2>' + table(["Item", "Make / model / serial", "Bought", "Value"], 28, [30, 40, 15, 15]) + '</div>' for _ in range(10)])
section("Important documents", [bigt("Where our documents are", ["Document", "Location", "Notes"], 28, [35, 35, 30]), bigt("Insurance policies", ["Type", "Company", "Policy no.", "Renewal"], 28, [20, 30, 30, 20])])
section("Passwords & accounts", ['<div class="pg"><h2>Passwords & accounts</h2>' + "".join('<div class="entry">' + "".join(f'<div class="r"><span>{x}</span></div>' for x in ["Website", "Username", "Password", "Notes"]) + '</div>' for _ in range(6)) + '</div>' for _ in range(6)])
section("Address book", [bigt("Addresses", ["Name", "Address", "Phone / email"], 14, [26, 44, 30]).replace("height:21pt", "") for _ in range(8)])
section("Vehicles", ['<div class="pg"><h2>Vehicle</h2>' + row2(fields(["Make & model", "Year", "Plate"]), fields(["VIN", "Insurance", "Breakdown cover"])) + '<div class="lbl">Service log</div>' + table(["Date", "Mileage", "Work done", "Cost"], 18, [15, 15, 50, 20]) + '</div>' for _ in range(4)])
section("Pets", ['<div class="pg"><h2>Pet</h2>' + row2(fields(["Name", "Species / breed", "Date of birth"]), fields(["Vet", "Microchip", "Insurance"])) + fields(["Feeding", "Medication"], 2) + '<div class="lbl">Vaccinations & vet visits</div>' + table(["Date", "Reason", "Next due"], 12, [18, 62, 20]) + '</div>' for _ in range(4)])
section("Holidays, gifts & celebrations", [bigt("Gift list", ["Person", "Occasion", "Ideas", "Budget", "Bought ✓"], 28, [20, 16, 36, 14, 14]) for _ in range(4)]
        + ['<div class="pg"><h2>Holiday / event planner</h2>' + row2(fields(["Event", "Date", "Budget"]), fields(["Guests", "Venue", "Theme"])) + row2('<div class="lbl">To do</div>' + checks([""] * 14), '<div class="lbl">Menu & shopping</div>' + checks([""] * 14)) + fields(["Notes"], 3) + '</div>' for _ in range(4)])
section("Travel", ['<div class="pg"><h2>Trip planner</h2>' + row2(fields(["Destination", "Dates", "Travel / flights"]), fields(["Accommodation", "Confirmation no.", "Budget"])) + '<div class="lbl">Itinerary</div>' + table(["Day", "Plans"], 10, [15, 85]) + fields(["Notes"], 2) + '</div>' for _ in range(4)]
        + ['<div class="pg"><h2>Packing list</h2>' + row2('<div class="lbl">Clothes</div>' + checks(["Tops", "Trousers / shorts", "Underwear", "Socks", "Pyjamas", "Jacket", "Shoes", "Swimwear", "", ""]), '<div class="lbl">Toiletries</div>' + checks(["Toothbrush & paste", "Shampoo", "Deodorant", "Medication", "Sunscreen", "Glasses / lenses", "", "", "", ""]), '<div class="lbl">Essentials</div>' + checks(["Passports", "Tickets", "Wallet & cards", "Phone & charger", "Adapters", "Keys", "Insurance docs", "", "", ""])) + fields(["Before we leave"], 6) + '</div>'] * 2)
section("Kids' school & activities", ['<div class="pg"><h2>School & activities</h2>' + row2(fields(["Child", "School", "Teacher"]), fields(["School phone", "Start / finish", "Bus / pickup"])) + '<table style="table-layout:fixed;margin-top:6pt"><tr><th></th>' + "".join(f"<th>{d}</th>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) + "</tr>" + "".join(f"<tr style='height:44pt'><th>{t}</th>" + "<td></td>" * 7 + "</tr>" for t in ["Before", "Morning", "Afternoon", "After", "Evening"]) + '</table>' + fields(["Friends & parents' numbers"], 4) + '</div>' for _ in range(4)])
section("Family goals & notes", ['<div class="pg"><h2>Family goals</h2>' + "".join(f'<div class="lbl">{x}</div>' + lines(4) for x in ["This year as a family we want to", "Money goals", "Home projects", "Trips & adventures", "Traditions to keep"]) + '</div>'] + [notes(32)] * 9)
toc = '<div class="pg"><h2>Contents</h2><table>' + "".join(f"<tr><td>{n}</td><td style='width:12%;text-align:right'>{p}</td></tr>" for n, p in SECTIONS) + '</table></div>'
P[P.index("CONTENTS")] = toc
render2("home-family-organizer", "The Home & Family Organizer", "Household binder in a book: contacts, calendars, budgets, meal plans, cleaning, maintenance, medical records and more", "#7a3e48", "#f5e9eb", P,
        '<p style="font-size:18pt;font-weight:700">Run your household from one book.</p><p>Emergency plan, family medical records, 12 monthly calendars with budgets and bill trackers, 52 weekly meal plans with grocery lists, cleaning and maintenance schedules, home inventory, documents locator, passwords, vehicles, pets, gifts, travel and school schedules.</p><p>Large 8.5 × 11 in format with numbered pages and a contents page.</p>',
        trim=(8.5, 11), number=True, extra_css=CSS_BIG)
