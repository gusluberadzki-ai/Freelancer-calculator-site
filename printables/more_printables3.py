# Round 8 printables. exec()'d by build.py, so lines/chks/PRODUCTS are in scope.
def christmas():
    gifts = ('<div class="pg"><div class="sub"><h1>Christmas Gift List</h1><span>Budget: ______________</span></div><table><tr><th style="width:20%">Name</th><th>Gift idea</th><th style="width:13%">Budget</th><th style="width:13%">Spent</th><th style="width:8%">Bought</th><th style="width:8%">Wrapped</th></tr>'
             + "<tr style='height:23pt'><td></td><td></td><td></td><td></td><td></td><td></td></tr>" * 24 + '<tr><th colspan="2" style="text-align:right">Total</th><td></td><td></td><td></td><td></td></tr></table></div>')
    menu = ('<div class="pg"><div class="sub"><h1>Christmas Menu & Shopping</h1><span>Guests: ______</span></div><div class="cols">'
            + "".join(f'<div class="box"><b>{x}</b>' + lines(4) + '</div>' for x in ["Starters", "Main", "Desserts"]) + '</div>'
            '<div class="cols" style="flex:1;margin-top:8pt"><div class="grow"><div class="lbl">Shopping list</div>' + chks(20) + '</div><div class="grow"><div class="lbl">Cooking timeline (Christmas Day)</div><table><tr><th style="width:22%">Time</th><th>Task</th></tr>'
            + "<tr style='height:22pt'><td></td><td></td></tr>" * 12 + '</table><div class="lbl">Drinks</div>' + lines(4) + '</div></div></div>')
    todo = [("Early December", ["Set the budget", "Write the gift list", "Order online gifts", "Buy cards & stamps", "Plan the menu"]),
            ("Mid December", ["Post cards", "Last posting dates", "Buy the tree", "Wrapping paper & tags", "Book any travel"]),
            ("Week before", ["Wrap gifts", "Food shop", "Clean the guest room", "Confirm guests", "Charge cameras"]),
            ("Christmas Eve", ["Defrost the turkey", "Prep veg", "Set the table", "Stockings", "Relax"])]
    blk = "".join(f'<div class="box" style="margin-bottom:6pt;flex:1"><b>{t}</b>' + "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs) + chks(2) + '</div>' for t, xs in todo)
    cards = ('<div class="pg"><div class="sub"><h1>December Countdown</h1><span></span></div><div class="cols" style="flex:1"><div class="grow">' + blk + '</div>'
             '<div class="grow"><div class="lbl">Card list</div><table><tr><th>Name</th><th style="width:16%">Sent</th><th style="width:16%">Received</th></tr>' + "<tr style='height:21pt'><td></td><td></td><td></td></tr>" * 30 + '</table></div></div></div>')
    return [gifts, menu, cards]
def newyear():
    q = ["Best moments of the year", "What I'm proud of", "What didn't go to plan, and what I learned", "Habits to leave behind", "Words for the year I'm finishing"]
    review = '<div class="pg"><div class="sub"><h1>Year in Review</h1><span>Year: ________</span></div>' + "".join(f'<div class="lbl">{x}</div>' + lines(5 if i < 3 else 3) for i, x in enumerate(q)) + '</div>'
    areas = ["Health", "Money", "Career", "Relationships", "Learning", "Home", "Fun & travel", "Mind"]
    goals = ('<div class="pg"><div class="sub"><h1>Goals for the New Year</h1><span>My word: ______________</span></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:8pt;flex:1">'
             + "".join(f'<div class="box"><b>{a}</b>' + chks(4) + '</div>' for a in areas) + '</div><div class="lbl">The one goal that would change everything</div>' + lines(2) + '</div>')
    ms = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    months = ('<div class="pg"><div class="sub"><h1>Monthly Focus</h1><span></span></div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:7pt;flex:1">'
              + "".join(f'<div class="box"><b>{m}</b>' + lines(4) + '</div>' for m in ms) + '</div></div>')
    return [review, goals, months]
def medication():
    prof = ('<div class="pg"><div class="sub"><h1>My Medications</h1><span>Name: ______________</span></div><table><tr><th style="width:22%">Medication</th><th style="width:12%">Dose</th><th style="width:16%">When</th><th>What it&#39;s for</th><th style="width:16%">Prescribed by</th><th style="width:12%">Start date</th></tr>'
            + "<tr style='height:26pt'><td></td><td></td><td></td><td></td><td></td><td></td></tr>" * 12 + '</table><div class="cols"><div><div class="lbl">Allergies</div>' + lines(3) + '<div class="lbl">Doctor & phone</div>' + lines(2) + '</div>'
            '<div><div class="lbl">Pharmacy & phone</div>' + lines(2) + '<div class="lbl">Emergency contact</div>' + lines(2) + '<div class="lbl">Blood type · conditions</div>' + lines(1) + '</div></div></div>')
    head = "".join(f"<th style='width:2.5%;text-align:center;padding:0'>{d}</th>" for d in range(1, 32))
    rows = "".join("<tr style='height:24pt'><td></td><td></td>" + "<td></td>" * 31 + "</tr>" for _ in range(16))
    grid = (f'<div class="pg"><div class="sub"><h1>Medication Tracker</h1><span>Month: ______________</span></div><div class="small">Tick each dose when taken. Write the time in the second column.</div>'
            f'<table class="dots"><tr><th style="text-align:left">Medication & dose</th><th style="width:7%">Time</th>{head}</tr>{rows}</table><div class="lbl">Side effects · notes</div>' + lines(4) + '</div>')
    return [prof, grid]
def mood():
    moods = [("Great", "#2f9e44"), ("Good", "#94d82d"), ("Okay", "#fcc419"), ("Low", "#ff922b"), ("Bad", "#e03131")]
    key = '<div style="display:flex;gap:12pt;margin:4pt 0 8pt">' + "".join(f'<span style="display:flex;align-items:center;gap:4pt"><i style="width:11pt;height:11pt;border-radius:2pt;background:{c};display:inline-block"></i>{m}</span>' for m, c in moods) + '</div>'
    ms = "JFMAMJJASOND"
    head = "".join(f"<th style='text-align:center'>{m}</th>" for m in ms)
    rows = "".join(f"<tr style='height:19.5pt'><td style='text-align:center;font-size:7.5pt'>{d}</td>" + "<td></td>" * 12 + "</tr>" for d in range(1, 32))
    year = f'<div class="pg"><div class="sub"><h1>Year in Pixels</h1><span>Year: ________</span></div><div class="small">Colour one square each day for your mood.</div>{key}<table class="dots"><tr><th style="width:6%"></th>{head}</tr>{rows}</table></div>'
    days = "".join(f'<tr style="height:19.5pt"><td style="text-align:center">{d}</td>' + "<td></td>" * 5 + '<td></td><td></td></tr>' for d in range(1, 32))
    month = ('<div class="pg"><div class="sub"><h1>Monthly Mood Tracker</h1><span>Month: ______________</span></div>' + key +
             '<table class="dots"><tr><th style="width:6%">Day</th>' + "".join(f"<th style='width:7%'>{m}</th>" for m, _ in moods) + '<th style="width:9%">Sleep (h)</th><th>What affected my mood</th></tr>' + days + '</table></div>')
    return [month, year]
PRODUCTS += [("Christmas-Planner", "#c92a2a", "#fdeaea", christmas), ("New-Year-Reset-Planner", "#1c7ed6", "#e7f1fc", newyear), ("Medication-Tracker", "#0c8599", "#e3f6f8", medication), ("Mood-Tracker", "#7048e8", "#f0ebfd", mood)]
