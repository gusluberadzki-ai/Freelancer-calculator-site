# Round 7 printables. exec()'d by build.py, so lines/chks/PRODUCTS are in scope.
def babylog():
    rows = "".join("<tr style='height:22pt'>" + "<td></td>" * 7 + "</tr>" for _ in range(16))
    return ['<div class="pg"><div class="sub"><h1>Baby Daily Log</h1><span>Date: ______________</span></div>'
            '<div class="lbl">Feeding</div><table><tr><th style="width:12%">Time</th><th style="width:12%">Left (min)</th><th style="width:12%">Right (min)</th><th style="width:13%">Bottle (ml/oz)</th><th style="width:12%">Wet</th><th style="width:12%">Dirty</th><th>Notes</th></tr>' + rows + '</table>'
            '<div class="cols"><div><div class="lbl">Sleep</div><table><tr><th>From</th><th>To</th><th>Total</th></tr>' + "<tr><td></td><td></td><td></td></tr>" * 7 + '</table></div>'
            '<div><div class="lbl">Today</div>' + "".join(f'<div class="chk"><i></i>{x}</div>' for x in ["Vitamin D", "Tummy time", "Bath", "Medicine"]) + '<div class="lbl">Mood · temperature · notes</div>' + lines(3) + '</div></div></div>']
def student():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    blk = "".join(f'<div class="box" style="margin-bottom:5pt;flex:1"><b>{d}</b><table style="margin-top:3pt"><tr><th style="width:26%">Subject</th><th>Homework / to do</th><th style="width:14%">Due</th><th style="width:9%">✓</th></tr>' + "<tr><td></td><td></td><td></td><td></td></tr>" * 4 + '</table></div>' for d in days)
    return ['<div class="pg"><div class="sub"><h1>Student Weekly Planner</h1><span>Week of: ______________</span></div><div class="cols" style="flex:1"><div class="grow" style="flex:2.2">' + blk + '</div>'
            '<div class="grow"><div class="box" style="margin-bottom:5pt"><b>Tests & deadlines</b>' + chks(6) + '</div><div class="box" style="margin-bottom:5pt"><b>Weekend</b>' + lines(5) + '</div>'
            '<div class="box" style="margin-bottom:5pt"><b>Goals this week</b>' + chks(4) + '</div><div class="box" style="flex:1"><b>Notes</b>' + lines(6) + '</div></div></div></div>']
def pets():
    p1 = ('<div class="pg"><div class="sub"><h1>Pet Profile</h1><span></span></div><div class="cols"><div>' + "".join(f'<div class="lbl">{x}</div>' + lines(1) for x in ["Name", "Species / breed", "Date of birth", "Colour / markings", "Microchip number", "Insurance & policy no."]) + '</div>'
          '<div><div class="box" style="height:150pt;display:flex;align-items:center;justify-content:center;color:#aaa">Photo</div>' + "".join(f'<div class="lbl">{x}</div>' + lines(1) for x in ["Vet & phone", "Emergency vet", "Food & amount"]) + '</div></div>'
          '<div class="lbl">Vaccinations</div><table><tr><th>Vaccine</th><th style="width:22%">Date</th><th style="width:22%">Next due</th></tr>' + "<tr><td></td><td></td><td></td></tr>" * 6 + '</table>'
          '<div class="lbl">Medications & allergies</div>' + lines(4) + '</div>')
    p2 = ('<div class="pg"><div class="sub"><h1>Pet Care Log</h1><span>Month: ______________</span></div><table><tr><th style="width:14%">Date</th><th style="width:16%">Type</th><th>Details (vet visit, grooming, flea/worm treatment, weight…)</th><th style="width:14%">Cost</th></tr>'
          + "<tr style='height:22pt'><td></td><td></td><td></td><td></td></tr>" * 24 + '</table><div class="lbl">Weight tracker</div><table><tr>' + "".join("<th style='text-align:center'>" + m + "</th>" for m in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]) + '</tr><tr style="height:24pt">' + "<td></td>" * 12 + '</tr></table></div>')
    return [p1, p2]
def wedding():
    tl = [("12+ months before", ["Set the budget", "Draft the guest list", "Choose a date", "Book the venue", "Hire a planner (optional)"]),
          ("9–12 months", ["Book photographer & videographer", "Book caterer", "Choose the wedding party", "Buy the dress / suit", "Send save-the-dates"]),
          ("6–9 months", ["Book florist", "Book band / DJ", "Plan the honeymoon", "Register for gifts", "Book hair & make-up"]),
          ("3–6 months", ["Order invitations", "Order the cake", "Book transport", "Buy the rings", "Plan the ceremony"]),
          ("1–3 months", ["Send invitations", "Final dress fitting", "Get the marriage licence", "Write vows", "Confirm all vendors"]),
          ("Final weeks", ["Final guest count", "Seating plan", "Pack for the honeymoon", "Prepare vendor payments", "Rehearsal"])]
    blk = lambda part: "".join(f'<div class="box" style="margin-bottom:6pt;flex:1"><b>{t}</b>' + "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs) + chks(2) + '</div>' for t, xs in part)
    p1 = '<div class="pg"><div class="sub"><h1>Wedding Planning Checklist</h1><span>Date: ______________</span></div><div class="cols" style="flex:1"><div class="grow">' + blk(tl[:3]) + '</div><div class="grow">' + blk(tl[3:]) + '</div></div></div>'
    p2 = ('<div class="pg"><div class="sub"><h1>Vendor Contacts</h1><span></span></div><table><tr><th style="width:20%">Vendor</th><th>Company & contact</th><th style="width:18%">Phone</th><th style="width:14%">Deposit</th><th style="width:14%">Balance due</th></tr>'
          + "".join(f"<tr style='height:30pt'><td>{v}</td><td></td><td></td><td></td><td></td></tr>" for v in ["Venue", "Caterer", "Photographer", "Videographer", "Florist", "Band / DJ", "Cake", "Hair & make-up", "Officiant", "Transport", "Stationery", "Planner", "", ""]) + '</table></div>')
    return [p1, p2]
PRODUCTS += [("Baby-Daily-Log", "#4c6ef5", "#edf0fe", babylog), ("Student-Weekly-Planner", "#0ca678", "#e6f8f2", student), ("Pet-Care-Log", "#f08c00", "#fff4e0", pets), ("Wedding-Planning-Checklist", "#ae3ec9", "#f7eafa", wedding)]
