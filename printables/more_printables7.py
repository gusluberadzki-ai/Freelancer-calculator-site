# Round 13 printables. exec()'d by build_round.py, so lines/chks are in scope.
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def tbl(heads, widths, n, h=22):
    return ('<table><tr>' + "".join(f"<th style='width:{w}'>{x}</th>" if w else f"<th>{x}</th>" for x, w in zip(heads, widths)) + '</tr>'
            + (f"<tr style='height:{h}pt'>" + "<td></td>" * len(heads) + "</tr>") * n + '</table>')
def box(t, body, flex=1, extra=""): return f'<div class="box" style="flex:{flex};margin-bottom:5pt;{extra}"><b>{t}</b>{body}</div>'
def items(xs): return "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs)
def lab(t, n): return f'<div class="lbl">{t}</div>' + lines(n)
def two(a, b): return f'<div class="cols"><div>{a}</div><div>{b}</div></div>'
def plants():
    prof = ('<div class="box" style="flex:1;margin-bottom:6pt;display:flex;gap:8pt"><div style="width:30%;border:1pt dashed #ccc;border-radius:6pt"></div><div style="flex:1"><b>Plant: ____________________</b>'
            '<div class="small" style="margin-top:4pt">Bought / from ______________  Pot size ______</div>'
            '<div class="small" style="margin-top:4pt">Light ☐ bright direct ☐ bright indirect ☐ medium ☐ low</div>'
            '<div class="small" style="margin-top:4pt">Water every ______  Feed every ______  Humidity ☐ low ☐ medium ☐ high</div>'
            '<div class="small" style="margin-top:4pt">Toxic to pets? ☐ yes ☐ no   Repot due ______</div>' + lines(2) + '</div></div>')
    p1 = '<div class="pg"><div class="sub"><h1>Plant Profiles</h1><span></span></div><div class="grow">' + prof * 4 + '</div></div>'
    days = "".join(f"<th style='text-align:center;padding:1pt;font-size:7pt'>{d}</th>" for d in range(1, 32))
    p2 = ('<div class="pg"><div class="sub"><h1>Watering Tracker</h1><span>Month: ______________</span></div><div class="small">W = watered · F = fed · M = misted · R = repotted</div>'
          f'<table><tr><th style="width:20%">Plant</th>{days}</tr>' + ("<tr style='height:26pt'><td></td>" + "<td style='padding:0'></td>" * 31 + "</tr>") * 22 + '</table></div>')
    p3 = ('<div class="pg"><div class="sub"><h1>Plant Care Log</h1><span></span></div>' + tbl(["Date", "Plant", "What I did", "Health", "Notes (pests, new leaves, problems)"], ["12%", "18%", "20%", "10%", ""], 28) + '</div>')
    p4 = ('<div class="pg"><div class="sub"><h1>Wishlist & Propagation</h1><span></span></div><div class="lbl">Plant wishlist</div>' + tbl(["Plant", "Where to buy", "Price", "✓"], ["", "30%", "12%", "7%"], 10)
          + '<div class="lbl">Propagation tracker</div>' + tbl(["Plant", "Cutting taken", "Method", "Roots seen", "Potted up"], ["", "15%", "18%", "15%", "15%"], 10) + lab("Notes · what my plants like", 4) + '</div>')
    return [p1, p1, p2, p3, p4]
def dreams():
    page = ('<div class="pg"><div class="sub"><h1>Dream Journal</h1><span>Date: ______________</span></div>'
            '<div class="cols"><div class="box"><b>Bedtime</b> ______  <b>Woke</b> ______</div><div class="box"><b>Sleep quality</b>  ☆ ☆ ☆ ☆ ☆</div><div class="box"><b>Lucid?</b>  ☐ yes ☐ no</div></div>'
            + lab("Title", 1) + lab("What happened", 12) + '<div class="cols"><div>' + lab("People", 2) + '</div><div>' + lab("Places", 2) + '</div></div>'
            '<div class="cols"><div>' + lab("Feelings", 2) + '</div><div>' + lab("Symbols & recurring themes", 2) + '</div></div><div class="box" style="height:110pt"><b>Sketch</b></div></div>')
    sym = ('<div class="pg"><div class="sub"><h1>Recurring Dreams & Symbols</h1><span></span></div>' + tbl(["Symbol / theme", "Times seen", "Dates", "What it might mean to me"], ["24%", "12%", "20%", ""], 26) + '</div>')
    months = "".join("<tr>" + f"<td style='font-size:7pt;width:6%'>{d}</td>" + "<td style='height:16pt;padding:0'></td>" * 12 + "</tr>" for d in range(1, 32))
    year = ('<div class="pg"><div class="sub"><h1>Dream Recall Tracker</h1><span>Colour: ☐ remembered ☐ vivid ☐ lucid ☐ nightmare</span></div><table><tr><th></th>'
            + "".join(f"<th style='text-align:center;padding:2pt'>{m[:3]}</th>" for m in MON) + f'</tr>{months}</table></div>')
    tips = ('<div class="pg"><div class="sub"><h1>Better Recall</h1><span>Habits to try</span></div>' + box("Before sleep", items(["Keep this journal and a pen by the bed", "Tell yourself: I will remember my dreams", "No screens for 30 minutes", "Same bedtime most nights"]) + chks(2))
            + box("When you wake", items(["Stay still with eyes closed for a minute", "Write keywords first, details after", "Note feelings even if the story is gone", "Write before checking your phone"]) + chks(2))
            + box("Lucid dreaming practice", items(["Reality checks during the day", "Look for your dream signs", "Wake-back-to-bed (set an alarm after 5 hours)"]) + chks(2)) + lab("My dream goals", 5) + '</div>')
    return [page, page, page, tips, sym, year]
def hiking():
    page = ('<div class="pg"><div class="sub"><h1>Hike Log</h1><span>Date: ______________</span></div>' + two(lab("Trail / route", 1), lab("Location / park", 1))
            + '<div class="cols">' + "".join(box(t, lines(1)) for t in ["Distance", "Elevation gain", "Time", "Difficulty ☆☆☆☆☆"]) + '</div>'
            '<div class="cols">' + "".join(box(t, lines(1)) for t in ["Start time", "Weather", "Trail conditions", "Hiked with"]) + '</div>'
            + lab("Highlights", 5) + two(lab("Wildlife & plants spotted", 3), lab("Food & water notes", 3)) + '<div class="box" style="height:150pt;margin-top:4pt"><b>Route sketch / photo</b></div>'
            + lab("Would I do it again?  ☐ yes ☐ no  · Tips for next time", 2) + '</div>')
    gear = [("Navigation & safety", ["Map / offline app", "Compass", "Phone & power bank", "First aid kit", "Head torch", "Whistle", "Emergency blanket"]), ("Clothing", ["Waterproof jacket", "Warm layer", "Hat & gloves", "Spare socks", "Boots broken in", "Sun hat"]),
            ("Food & water", ["Water (1 L per 2 hours)", "Snacks", "Lunch", "Water filter"]), ("Other", ["Sunscreen", "Insect repellent", "Toilet kit", "Rubbish bag", "Trekking poles", "Camera"])]
    gp = ('<div class="pg"><div class="sub"><h1>Hiking Gear Checklist</h1><span>Leave a route plan with someone</span></div><div class="cols" style="flex:1"><div class="grow">' + "".join(box(t, items(xs) + chks(1)) for t, xs in gear[:2])
          + '</div><div class="grow">' + "".join(box(t, items(xs) + chks(1)) for t, xs in gear[2:]) + box("Route plan left with", lines(3)) + '</div></div></div>')
    bl = ('<div class="pg"><div class="sub"><h1>Trail Bucket List</h1><span></span></div>' + tbl(["Trail / peak", "Where", "Distance", "Best season", "Done"], ["", "24%", "12%", "16%", "10%"], 18, 24)
          + '<div class="lbl">Year totals</div><div class="cols">' + "".join(box(t, lines(1)) for t in ["Hikes", "Distance", "Elevation", "Peaks"]) + '</div></div>')
    summ = ('<div class="pg"><div class="sub"><h1>Hike Summary</h1><span>Year: ________</span></div>' + tbl(["Date", "Trail", "Distance", "Elevation", "Time", "Rating"], ["12%", "", "12%", "12%", "11%", "11%"], 30) + '</div>')
    return [gp, page, page, page, summ, bl]
def routines():
    def chart(title, steps, icon):
        rows = "".join(f"<tr style='height:40pt'><td style='font-size:12pt'><span style='font-size:16pt;margin-right:6pt'>{i}</span>{s}</td>" + "<td style='text-align:center;color:#ddd;font-size:16pt'>☆</td>" * 7 + "</tr>" for i, s in zip(icon, steps))
        return (f'<div class="pg"><div class="sub"><h1>{title}</h1><span>Name: ______________</span></div><table><tr><th>I can…</th>'
                + "".join(f"<th style='text-align:center;width:8%'>{d}</th>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) + f'</tr>{rows}</table>'
                '<div class="cols" style="margin-top:8pt"><div class="box"><b>Stars this week: ______</b></div><div class="box"><b>My reward</b>' + lines(2) + '</div></div></div>')
    m = chart("Morning Routine", ["Get out of bed", "Go to the toilet", "Get dressed", "Eat breakfast", "Brush my teeth", "Brush my hair", "Pack my bag", "Shoes & coat on", ""], ["🛏", "🚽", "👕", "🥣", "🪥", "💇", "🎒", "👟", "⭐"])
    a = chart("After School", ["Unpack my bag", "Wash my hands", "Have a snack", "Homework / reading", "Play time", "Tidy my toys", "Help set the table", ""], ["🎒", "🧼", "🍎", "📖", "⚽", "🧸", "🍽", "⭐"])
    b = chart("Bedtime Routine", ["Tidy my room", "Bath or shower", "Pyjamas on", "Brush my teeth", "Choose clothes for tomorrow", "Story time", "Lights out", ""], ["🧸", "🛁", "👚", "🪥", "👕", "📚", "🌙", "⭐"])
    cards = "".join(f'<div style="border:1.5pt dashed #bbb;border-radius:8pt;height:120pt;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:40pt">{i}<div style="font-size:11pt;margin-top:6pt">{t}</div></div>'
                    for i, t in [("🛏", "Wake up"), ("👕", "Get dressed"), ("🥣", "Breakfast"), ("🪥", "Teeth"), ("🎒", "Bag"), ("👟", "Shoes"), ("🛁", "Bath"), ("📚", "Story"), ("🌙", "Sleep")])
    c = f'<div class="pg"><div class="sub"><h1>Picture Cards</h1><span>Cut out and stick in order</span></div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10pt;flex:1">{cards}</div></div>'
    return [m, a, b, c]
def envelopes():
    def env(cat):
        rows = "".join("<tr style='height:17pt'><td></td><td></td><td></td></tr>" for _ in range(9))
        return (f'<div class="box" style="flex:1;margin-bottom:6pt"><div style="display:flex;justify-content:space-between"><b style="font-size:12pt;color:var(--c)">{cat or "__________"}</b><span class="small">Budget ________</span></div>'
                f'<table style="margin-top:3pt"><tr><th style="width:22%">Date</th><th>Spent on</th><th style="width:26%">Left</th></tr>{rows}</table></div>')
    p1 = '<div class="pg"><div class="sub"><h1>Cash Envelope Tracker</h1><span>Month: ______________</span></div><div class="cols" style="flex:1"><div class="grow">' + env("Groceries") + env("Fuel / transport") + '</div><div class="grow">' + env("Eating out") + env("Fun money") + '</div></div></div>'
    p2 = '<div class="pg"><div class="sub"><h1>Cash Envelope Tracker</h1><span>Month: ______________</span></div><div class="cols" style="flex:1"><div class="grow">' + env("") + env("") + '</div><div class="grow">' + env("") + env("") + '</div></div></div>'
    cats = ["Groceries", "Fuel / transport", "Eating out", "Fun money", "Household", "Gifts", "Clothes", "Personal care", "", ""]
    plan = ('<div class="pg"><div class="sub"><h1>Monthly Cash Plan</h1><span>Month: ______________</span></div><div class="cols">' + box("Take-home pay", lines(1)) + box("Bills paid by card", lines(1)) + box("Cash to withdraw", lines(1)) + '</div>'
            '<table><tr><th>Envelope</th><th style="width:15%">Week 1</th><th style="width:15%">Week 2</th><th style="width:15%">Week 3</th><th style="width:15%">Week 4</th><th style="width:13%">Total</th></tr>'
            + "".join(f"<tr style='height:26pt'><td>{c}</td><td></td><td></td><td></td><td></td><td></td></tr>" for c in cats) + '</table>'
            '<div class="lbl">Leftover cash goes to</div>' + items(["Savings ________", "Debt payment ________", "Next month's envelope ________"]) + '</div>')
    def label(cat): return f'<div style="border:1.5pt dashed #bbb;border-radius:8pt;height:130pt;padding:10pt;display:flex;flex-direction:column;justify-content:space-between"><b style="font-size:16pt;color:var(--c)">{cat}</b><div class="small">Budget: ________<br><br>Month: ________</div></div>'
    labs = f'<div class="pg"><div class="sub"><h1>Envelope Labels</h1><span>Cut out and stick on envelopes</span></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:10pt">' + "".join(label(c or "__________") for c in cats[:8]) + '</div></div>'
    fill = "".join(f'<span style="display:inline-flex;align-items:center;justify-content:center;width:13.5%;height:34pt;border:1pt solid #ccc;margin:2pt;border-radius:50%;font-size:9pt;color:#999">{v}</span>' for v in [5, 10, 20, 50, 5, 10, 20, 50, 5, 10, 20, 50, 5, 10, 20, 50, 5, 10, 20, 50, 5, 10, 20, 50, 20, 50, 100, 20, 20, 50])
    sav = ('<div class="pg"><div class="sub"><h1>Savings Challenge</h1><span>Goal: ______________</span></div><div class="small">Colour a circle each time you put that amount in your savings envelope. Total: 770.</div>'
           f'<div style="display:flex;flex-wrap:wrap;margin-top:8pt">{fill}</div>' + lab("What I'm saving for", 2) + lab("Date started · date finished", 1) + '</div>')
    return [plan, p1, p2, labs, sav]
PRODUCTS = [("Houseplant-Care-Journal", "#2f9e44", "#ebfbee", plants), ("Dream-Journal", "#5f3dc4", "#f3f0ff", dreams), ("Hiking-Trail-Journal", "#5c940d", "#f4fce3", hiking),
            ("Kids-Routine-Charts", "#f76707", "#fff4e6", routines), ("Cash-Envelope-Budget", "#0b7285", "#e3fafc", envelopes)]
