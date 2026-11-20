# Round 9 printables. exec()'d by build_round9.py, so lines/chks are in scope.
def moving():
    tl = [("8 weeks before", ["Set a moving budget", "Get 3 removal quotes", "Declutter room by room", "Book time off work", "Start using up freezer food"]),
          ("6 weeks before", ["Book removals / van", "Order boxes & tape", "Tell your landlord / agent", "Measure the new place", "Sort school or nursery"]),
          ("4 weeks before", ["Start packing spare rooms", "Arrange post redirection", "Book utility readings", "Find a vet / doctor nearby", "Sell or donate big items"]),
          ("2 weeks before", ["Confirm removal times", "Pack all but essentials", "Arrange parking permit", "Back up computer files", "Cancel local memberships"]),
          ("Moving week", ["Defrost the freezer", "Pack an essentials box", "Clean the old home", "Take meter photos", "Hand over keys"]),
          ("After the move", ["Set up internet", "Register to vote", "Update your ID address", "Check all boxes arrived", "Meet the neighbours"])]
    blk = lambda part: "".join(f'<div class="box" style="margin-bottom:6pt;flex:1"><b>{t}</b>' + "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs) + chks(1) + '</div>' for t, xs in part)
    p1 = '<div class="pg"><div class="sub"><h1>Moving House Checklist</h1><span>Moving day: ______________</span></div><div class="cols" style="flex:1"><div class="grow">' + blk(tl[:3]) + '</div><div class="grow">' + blk(tl[3:]) + '</div></div></div>'
    who = ["Bank", "Employer / payroll", "Doctor & dentist", "Car insurance", "Home insurance", "Driving licence", "Tax office", "Electricity", "Gas", "Water", "Internet & TV", "Mobile phone", "Subscriptions & deliveries", "Pension", "Friends & family", "", ""]
    p2 = ('<div class="pg"><div class="sub"><h1>Change of Address</h1><span>New address: _______________________</span></div><table><tr><th style="width:30%">Who</th><th>Account / reference</th><th style="width:17%">Date told</th><th style="width:8%">✓</th></tr>'
          + "".join(f"<tr style='height:24pt'><td>{w}</td><td></td><td></td><td></td></tr>" for w in who) + '</table>'
          '<div class="cols"><div><div class="lbl">Meter readings · old home</div><table><tr><th>Meter</th><th>Reading</th></tr>' + "".join(f"<tr><td>{m}</td><td></td></tr>" for m in ["Electricity", "Gas", "Water"]) + '</table></div>'
          '<div><div class="lbl">Meter readings · new home</div><table><tr><th>Meter</th><th>Reading</th></tr>' + "".join(f"<tr><td>{m}</td><td></td></tr>" for m in ["Electricity", "Gas", "Water"]) + '</table></div></div></div>')
    p3 = ('<div class="pg"><div class="sub"><h1>Box Inventory</h1><span>Page ____</span></div><div class="small">Number every box, write the room on the box and list what is inside here.</div>'
          '<table><tr><th style="width:9%">Box #</th><th style="width:18%">Room</th><th>Contents</th><th style="width:10%">Fragile</th><th style="width:10%">Arrived</th></tr>'
          + "<tr style='height:23pt'><td></td><td></td><td></td><td></td><td></td></tr>" * 28 + '</table></div>')
    return [p1, p2, p3]
def garden():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    head = "".join(f"<th style='text-align:center;padding:0;width:5.6%'>{m}</th>" for m in months)
    p1 = ('<div class="pg"><div class="sub"><h1>Planting Calendar</h1><span>Year: ________</span></div><div class="small">Shade S = sow, P = plant out, H = harvest.</div>'
          f'<table class="dots"><tr><th style="text-align:left">Plant / variety</th>{head}</tr>' + ("<tr style='height:26pt'><td></td>" + "<td></td>" * 12 + "</tr>") * 22 + '</table>'
          '<div class="lbl">Last frost date · first frost date</div>' + lines(1) + '</div>')
    grid = "".join("<tr>" + "<td style='height:17pt;padding:0'></td>" * 20 + "</tr>" for _ in range(26))
    p2 = ('<div class="pg"><div class="sub"><h1>Garden Layout</h1><span>Bed / area: ______________</span></div><div class="small">Each square = ______ (e.g. 30 cm / 1 ft). Sketch beds, paths and what grows where.</div>'
          f'<table>{grid}</table><div class="cols"><div><div class="lbl">Notes · sun & shade</div>' + lines(3) + '</div><div><div class="lbl">Crop rotation · next year</div>' + lines(3) + '</div></div></div>')
    p3 = ('<div class="pg"><div class="sub"><h1>Seed Inventory</h1><span></span></div><table><tr><th>Plant</th><th style="width:20%">Variety</th><th style="width:14%">Source</th><th style="width:12%">Bought</th><th style="width:12%">Use by</th><th style="width:10%">Qty left</th></tr>'
          + "<tr style='height:22pt'><td></td><td></td><td></td><td></td><td></td><td></td></tr>" * 14 + '</table>'
          '<div class="lbl">Harvest log</div><table><tr><th style="width:14%">Date</th><th>Crop</th><th style="width:18%">Amount</th><th>Notes</th></tr>' + "<tr style='height:22pt'><td></td><td></td><td></td><td></td></tr>" * 12 + '</table></div>')
    return [p1, p2, p3]
def recipes():
    card = ('<div class="box" style="flex:1;display:flex;flex-direction:column;margin-bottom:8pt"><div style="display:flex;justify-content:space-between"><b style="font-size:13pt;color:var(--c)">Recipe: ____________________</b>'
            '<span class="small">Serves ___ · Prep ___ · Cook ___</span></div><div class="cols" style="flex:1"><div style="flex:.8"><div class="lbl">Ingredients</div>' + lines(7) + '</div>'
            '<div style="flex:1.2"><div class="lbl">Method</div>' + lines(7) + '</div></div></div>')
    p_cards = '<div class="pg"><div class="sub"><h1>Recipe Cards</h1><span class="small">Cut along the box edges</span></div><div class="grow">' + card * 2 + '</div></div>'
    page = ('<div class="pg"><div class="sub"><h1>Recipe</h1><span>☆ ☆ ☆ ☆ ☆</span></div><div class="cols"><div><div class="lbl">Name</div>' + lines(1) + '</div><div><div class="lbl">From</div>' + lines(1) + '</div></div>'
            '<div class="cols"><div><div class="lbl">Serves</div>' + lines(1) + '</div><div><div class="lbl">Prep time</div>' + lines(1) + '</div><div><div class="lbl">Cook time</div>' + lines(1) + '</div><div><div class="lbl">Oven</div>' + lines(1) + '</div></div>'
            '<div class="cols" style="flex:1"><div style="flex:.8"><div class="lbl">Ingredients</div>' + chks(16) + '</div><div style="flex:1.2"><div class="lbl">Method</div>'
            + "".join(f'<div class="chk"><b style="color:var(--c);width:12pt">{i}</b></div>' for i in range(1, 17)) + '</div></div><div class="lbl">Notes · changes next time</div>' + lines(3) + '</div>')
    idx = ('<div class="pg"><div class="sub"><h1>Recipe Index</h1><span></span></div><table><tr><th style="width:8%">Page</th><th>Recipe</th><th style="width:22%">Category</th><th style="width:12%">Rating</th></tr>'
           + "<tr style='height:22pt'><td></td><td></td><td></td><td>☆☆☆☆☆</td></tr>" * 30 + '</table></div>')
    return [idx, page, page, p_cards]
def chores():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    head = "".join(f"<th style='text-align:center;width:9%'>{d}</th>" for d in days)
    star = "<td style='text-align:center;color:#ccc;font-size:14pt'>☆</td>"
    tasks = ["Make my bed", "Brush teeth (am)", "Brush teeth (pm)", "Get dressed", "Tidy my room", "Feed the pet", "Homework / reading", "Set the table", "Clear my plate", "Put clothes in the wash", "", "", ""]
    p1 = ('<div class="pg"><div class="sub"><h1>My Chore Chart</h1><span>Name: ______________  Week: ________</span></div>'
          f'<table><tr><th>Job</th>{head}</tr>' + "".join(f"<tr style='height:34pt'><td style='font-size:11pt'>{t}</td>" + star * 7 + "</tr>" for t in tasks) + '</table>'
          '<div class="cols" style="margin-top:8pt"><div class="box"><b>Stars this week: ______</b><div class="small" style="margin-top:4pt">Goal: ______ stars</div></div>'
          '<div class="box"><b>My reward</b>' + lines(2) + '</div></div></div>')
    cells = "".join("<tr>" + "".join("<td style='height:48pt;text-align:center;font-size:22pt;color:#ddd'>☆</td>" for _ in range(6)) + "</tr>" for _ in range(6))
    p2 = ('<div class="pg"><div class="sub"><h1>Reward Chart</h1><span>Name: ______________</span></div><div class="lbl">I am working towards</div>' + lines(1) +
          f'<table style="margin-top:8pt">{cells}</table><div class="cols" style="margin-top:8pt"><div class="box"><b>When I fill the chart I get</b>' + lines(3) + '</div>'
          '<div class="box"><b>Grown-up sign-off</b>' + lines(3) + '</div></div></div>')
    fam = ["Mum", "Dad", "", "", ""]
    p3 = ('<div class="pg"><div class="sub"><h1>Family Chore Rota</h1><span>Week of: ______________</span></div>'
          f'<table><tr><th>Chore</th>{head}</tr>' + "<tr style='height:30pt'><td></td>" + "<td></td>" * 7 + "</tr>" + ("<tr style='height:30pt'><td></td>" + "<td></td>" * 7 + "</tr>") * 15 + '</table>'
          '<div class="lbl">Who\'s who (initials)</div>' + lines(2) + '</div>')
    return [p1, p2, p3]
PRODUCTS = [("Moving-House-Checklist", "#1971c2", "#e7f1fb", moving), ("Garden-Planner", "#2f9e44", "#e9f6ec", garden), ("Recipe-Book-Cards", "#e8590c", "#fdeee4", recipes), ("Kids-Chore-Reward-Chart", "#f59f00", "#fff5db", chores)]
