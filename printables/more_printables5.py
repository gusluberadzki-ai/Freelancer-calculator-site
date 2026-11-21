# Round 11 printables. exec()'d by build_round.py, so lines/chks are in scope.
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def tbl(heads, widths, n, h=22):
    return ('<table><tr>' + "".join(f"<th style='width:{w}'>{x}</th>" if w else f"<th>{x}</th>" for x, w in zip(heads, widths)) + '</tr>'
            + (f"<tr style='height:{h}pt'>" + "<td></td>" * len(heads) + "</tr>") * n + '</table>')
def address():
    card = ('<div class="box" style="flex:1;margin-bottom:5pt"><div style="display:flex;justify-content:space-between"><b>Name</b><span class="small">Birthday ______</span></div>' + lines(1)
            + '<div class="small" style="margin-top:3pt">Address</div>' + lines(2) + '<div class="cols" style="gap:8pt"><div><div class="small">Phone</div>' + lines(1) + '</div><div><div class="small">Email</div>' + lines(1) + '</div></div></div>')
    book = '<div class="pg"><div class="sub"><h1>Address Book</h1><span>Letter: ______</span></div><div class="cols" style="flex:1"><div class="grow">' + card * 4 + '</div><div class="grow">' + card * 4 + '</div></div></div>'
    mbox = lambda m: f'<div class="box" style="flex:1;margin-bottom:5pt"><b style="color:var(--c)">{m}</b>' + lines(4) + '</div>'
    bdays = ('<div class="pg"><div class="sub"><h1>Birthdays & Anniversaries</h1><span>Perpetual · use every year</span></div><div class="cols" style="flex:1">'
             + "".join('<div class="grow">' + "".join(mbox(m) for m in MON[i::3]) + '</div>' for i in range(3)) + '</div></div>')
    cards = ('<div class="pg"><div class="sub"><h1>Christmas & Holiday Card List</h1><span>Year: ______</span></div>'
             + tbl(["Name", "Address checked", "Card sent", "Card received", "Gift"], ["", "15%", "12%", "13%", "18%"], 30) + '</div>')
    return [book, book, bdays, cards]
def pregnancy():
    weeks = "".join(f'<div class="box" style="margin-bottom:4pt;flex:1"><b>Weeks {a}-{a + 3}</b>  <span class="small">Weight ______  How I feel ______</span>' + lines(2) + '</div>' for a in range(4, 41, 4)[:5])
    weeks2 = "".join(f'<div class="box" style="margin-bottom:4pt;flex:1"><b>Weeks {a}-{a + 3}</b>  <span class="small">Weight ______  How I feel ______</span>' + lines(2) + '</div>' for a in range(24, 41, 4))
    p1 = ('<div class="pg"><div class="sub"><h1>Pregnancy Overview</h1><span>Due date: ______________</span></div><div class="cols"><div><div class="lbl">Midwife / doctor</div>' + lines(2) + '</div><div><div class="lbl">Hospital / birth centre</div>' + lines(2) + '</div></div>'
          '<div class="lbl">Appointments & scans</div>' + tbl(["Date", "Time", "Who / where", "Notes & results"], ["14%", "10%", "28%", ""], 14, 24)
          + '<div class="lbl">Questions to ask next time</div>' + chks(5) + '</div>')
    p2 = '<div class="pg"><div class="sub"><h1>Week by Week</h1><span>Weeks 4-23</span></div><div class="grow">' + weeks + '</div></div>'
    p3 = '<div class="pg"><div class="sub"><h1>Week by Week</h1><span>Weeks 24-40</span></div><div class="grow">' + weeks2 + '</div></div>'
    bag = lambda t, xs: f'<div class="box" style="margin-bottom:6pt;flex:1"><b>{t}</b>' + "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs) + chks(2) + '</div>'
    p4 = ('<div class="pg"><div class="sub"><h1>Hospital Bag Checklist</h1><span>Pack by week 36</span></div><div class="cols" style="flex:1"><div class="grow">'
          + bag("For me", ["Birth plan & notes", "Loose nightie / T-shirt", "Dressing gown & slippers", "Maternity pads", "Comfy underwear", "Nursing bras", "Toiletries & lip balm", "Phone charger (long cable)", "Snacks & drinks", "Going-home outfit"])
          + '</div><div class="grow">' + bag("For baby", ["Car seat (fitted)", "Vests & sleepsuits", "Hat & socks", "Nappies & wipes", "Muslin cloths", "Blanket", "Going-home outfit"])
          + bag("For my birth partner", ["Change of clothes", "Snacks & water", "Cash for parking", "Camera / phone"]) + '</div></div></div>')
    p5 = ('<div class="pg"><div class="sub"><h1>Birth Preferences</h1><span>Name: ______________</span></div>'
          + "".join(f'<div class="lbl">{t}</div>' + lines(n) for t, n in [("Birth partner(s)", 1), ("Where I'd like to give birth", 1), ("Pain relief I'd like to try", 3), ("Environment (lighting, music, movement)", 3), ("Delivery & after birth (cord, skin-to-skin, feeding)", 4), ("If things don't go to plan", 3), ("Anything else my team should know", 3)])
          + '</div>')
    kick = ('<div class="pg"><div class="sub"><h1>Baby Movement Log</h1><span>From around week 24</span></div><div class="small">Get to know your baby\'s usual pattern. If movements slow down or change, contact your midwife or maternity unit straight away. Don\'t wait.</div>'
            + tbl(["Date", "Start time", "Time to feel 10 movements", "Notes"], ["15%", "14%", "26%", ""], 26) + '</div>')
    return [p1, p2, p3, kick, p4, p5]
def selfcare():
    moods = "".join(f'<span style="display:inline-block;width:22pt;height:22pt;border:1pt solid #bbb;border-radius:50%;margin-right:6pt;text-align:center;line-height:22pt;color:#999">{e}</span>' for e in "12345")
    rows = lambda xs: "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs)
    daily = ('<div class="pg"><div class="sub"><h1>Daily Self-Care</h1><span>Date: ______________</span></div>'
             f'<div class="cols"><div class="box"><b>Mood today</b><div style="margin-top:5pt">{moods}</div></div><div class="box"><b>Energy</b><div style="margin-top:5pt">{moods}</div></div><div class="box"><b>Sleep</b><div class="small" style="margin-top:6pt">______ hours</div></div></div>'
             '<div class="cols"><div><div class="lbl">Today I am grateful for</div>' + lines(3) + '</div><div><div class="lbl">One thing I\'m looking forward to</div>' + lines(3) + '</div></div>'
             '<div class="cols"><div class="box"><b>Body</b>' + rows(["Drank enough water", "Moved for 20+ minutes", "Ate something nourishing", "Fresh air / daylight", "Took my medication"]) + '</div>'
             '<div class="box"><b>Mind</b>' + rows(["Screen-free time", "Read / learnt something", "Talked to someone I like", "Did something creative", "Five minutes of quiet"]) + '</div></div>'
             '<div class="lbl">What\'s on my mind</div>' + lines(5) + '<div class="lbl">A kind thing I did for myself today</div>' + lines(2) + '</div>')
    ideas = ["Go for a walk", "Run a bath", "Call a friend", "Tidy one small space", "Listen to an album", "Stretch for 10 min", "Cook a favourite meal", "Journal for 5 min", "Early night", "Read in bed",
             "Bake something", "Watch a comfort film", "Sit in the sun", "Unfollow accounts that drain me", "Say no to something", "Plan a day out", "Draw or doodle", "Declutter my phone", "Do a puzzle", "Dance in the kitchen"]
    menu = ('<div class="pg"><div class="sub"><h1>Self-Care Menu</h1><span>Pick one when you need it</span></div><div class="cols"><div class="box"><b>5 minutes</b>' + rows(ideas[:5]) + chks(2) + '</div><div class="box"><b>30 minutes</b>' + rows(ideas[5:10]) + chks(2) + '</div></div>'
            '<div class="cols"><div class="box"><b>An afternoon</b>' + rows(ideas[10:15]) + chks(2) + '</div><div class="box"><b>Boundaries & reset</b>' + rows(ideas[15:20]) + chks(2) + '</div></div>'
            '<div class="lbl">People I can talk to</div>' + lines(3) + '<div class="lbl">Signs I need to slow down</div>' + lines(3) + '</div>')
    days = ["M", "T", "W", "T", "F", "S", "S"]
    habits = ["Water", "Movement", "8 hours sleep", "Outside", "Journal", "No phone in bed", "Healthy meal", "", "", ""]
    week = ('<div class="pg"><div class="sub"><h1>Weekly Check-in</h1><span>Week of: ______________</span></div><table class="dots"><tr><th style="text-align:left">Habit</th>' + "".join(f"<th style='text-align:center;width:9%'>{d}</th>" for d in days) + '</tr>'
            + "".join(f"<tr style='height:26pt'><td>{h}</td>" + "<td></td>" * 7 + "</tr>" for h in habits) + '</table>'
            '<div class="cols"><div><div class="lbl">Best moment this week</div>' + lines(3) + '</div><div><div class="lbl">What drained me</div>' + lines(3) + '</div></div>'
            '<div class="cols"><div><div class="lbl">What I need more of</div>' + lines(3) + '</div><div><div class="lbl">Intention for next week</div>' + lines(3) + '</div></div></div>')
    pix = "".join("<tr>" + f"<td style='font-size:7pt;width:6%'>{d}</td>" + "<td style='height:16pt;padding:0'></td>" * 12 + "</tr>" for d in range(1, 32))
    year = ('<div class="pg"><div class="sub"><h1>Year of Self-Care</h1><span>Colour each day: ☐ great ☐ good ☐ okay ☐ hard</span></div>'
            '<table><tr><th></th>' + "".join(f"<th style='text-align:center;padding:2pt'>{m[:3]}</th>" for m in MON) + f'</tr>{pix}</table></div>')
    return [daily, daily, week, menu, year]
def homeschool():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    p1 = ('<div class="pg"><div class="sub"><h1>Homeschool Weekly Plan</h1><span>Week of: __________  Student: ________</span></div>'
          '<table><tr><th style="width:14%">Subject</th>' + "".join(f"<th>{d}</th>" for d in days) + '</tr>'
          + "".join(f"<tr style='height:56pt'><td><b>{s}</b></td>" + "<td></td>" * 5 + "</tr>" for s in ["Maths", "English", "Science", "History / Geography", "Reading", "Art / Music", "PE / outdoors", ""]) + '</table>'
          '<div class="cols" style="margin-top:6pt"><div class="box"><b>Field trips & activities</b>' + lines(2) + '</div><div class="box"><b>Supplies to get</b>' + chks(2) + '</div></div></div>')
    subj = "".join(f'<div class="box" style="flex:1;margin-bottom:5pt"><b>{s}</b>  <span class="small">Curriculum / book: ______________</span>' + lines(3) + '</div>' for s in ["Maths", "English", "Science", "History", "Geography", "Languages", "Arts"])
    p2 = '<div class="pg"><div class="sub"><h1>Year Overview & Goals</h1><span>School year: ________</span></div><div class="grow">' + subj + '</div></div>'
    p3 = ('<div class="pg"><div class="sub"><h1>Attendance & Hours</h1><span>Student: ______________</span></div><div class="small">Tick or write hours for each school day.</div>'
          '<table><tr><th style="width:12%">Month</th>' + "".join(f"<th style='text-align:center;padding:1pt;font-size:7pt'>{d}</th>" for d in range(1, 32)) + '<th style="width:7%">Total</th></tr>'
          + "".join(f"<tr style='height:26pt'><td>{m[:3]}</td>" + "<td style='padding:0'></td>" * 31 + "<td></td></tr>" for m in MON) + '</table>'
          '<div class="cols" style="margin-top:6pt"><div class="box"><b>Days required</b>' + lines(1) + '</div><div class="box"><b>Days completed</b>' + lines(1) + '</div><div class="box"><b>Total hours</b>' + lines(1) + '</div></div></div>')
    p4 = ('<div class="pg"><div class="sub"><h1>Reading Log & Grades</h1><span>Student: ______________</span></div><div class="lbl">Books read</div>'
          + tbl(["Title", "Author", "Finished", "Rating"], ["", "26%", "14%", "12%"], 14) + '<div class="lbl">Grades & assessments</div>' + tbl(["Date", "Subject", "Assignment / test", "Score"], ["13%", "20%", "", "12%"], 12) + '</div>')
    return [p1, p2, p3, p4]
def crafts():
    proj = ('<div class="pg"><div class="sub"><h1>Project Planner</h1><span>Started: ________  Finished: ________</span></div><div class="cols"><div><div class="lbl">Project</div>' + lines(1) + '</div><div><div class="lbl">For / occasion</div>' + lines(1) + '</div></div>'
            '<div class="cols"><div><div class="lbl">Pattern / source</div>' + lines(1) + '</div><div><div class="lbl">Size / measurements</div>' + lines(1) + '</div></div>'
            '<div class="cols"><div class="box" style="flex:1"><b>Sketch / inspiration</b><div style="height:150pt"></div></div><div class="box" style="flex:1"><b>Swatch / colour notes</b><div style="height:150pt"></div></div></div>'
            '<div class="lbl">Materials</div>' + tbl(["Item", "Colour / type", "Qty", "Have", "Cost"], ["", "24%", "10%", "8%", "12%"], 8) +
            '<div class="cols"><div><div class="lbl">Steps</div>' + chks(6) + '</div><div><div class="lbl">Notes · what I\'d change next time</div>' + lines(6) + '</div></div></div>')
    stash = ('<div class="pg"><div class="sub"><h1>Stash Inventory</h1><span>Yarn · fabric · supplies</span></div>'
             + tbl(["Item", "Brand", "Colour", "Weight / size", "Qty", "Where stored"], ["", "16%", "14%", "14%", "8%", "16%"], 30) + '</div>')
    lst = ('<div class="pg"><div class="sub"><h1>Project Queue & Shopping</h1><span></span></div><div class="lbl">Projects I want to make</div>'
           + tbl(["Project", "Pattern / link", "Priority", "Started", "Done"], ["", "30%", "10%", "10%", "8%"], 14) + '<div class="lbl">Shopping list</div>'
           + tbl(["Item", "For project", "Shop", "Price", "✓"], ["", "26%", "18%", "10%", "6%"], 12) + '</div>')
    rows = "".join("<tr>" + "<td style='height:13pt;padding:0'></td>" * 30 + "</tr>" for _ in range(42))
    grid = ('<div class="pg"><div class="sub"><h1>Pattern Grid</h1><span>Project: ______________</span></div><div class="small">For colourwork, cross-stitch, pixel patterns or quilt layouts.</div>'
            f'<table style="flex:1">{rows}</table></div>')
    return [proj, proj, stash, lst, grid]
PRODUCTS = [("Address-Book-Birthday-Tracker", "#1c7ed6", "#e7f5ff", address), ("Pregnancy-Planner", "#e64980", "#fff0f6", pregnancy), ("Self-Care-Wellness-Journal", "#0ca678", "#e6fcf5", selfcare),
            ("Homeschool-Planner", "#f08c00", "#fff4e6", homeschool), ("Craft-Sewing-Project-Planner", "#7048e8", "#f3f0ff", crafts)]
