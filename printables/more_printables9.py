# Round 15 printables. exec()'d by build_round.py, so lines/chks are in scope.
WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
def tbl(heads, widths, n, h=22):
    return ('<table><tr>' + "".join(f"<th style='width:{w}'>{x}</th>" if w else f"<th>{x}</th>" for x, w in zip(heads, widths)) + '</tr>'
            + (f"<tr style='height:{h}pt'>" + "<td></td>" * len(heads) + "</tr>") * n + '</table>')
def box(t, body, flex=1, extra=""): return f'<div class="box" style="flex:{flex};margin-bottom:5pt;{extra}"><b>{t}</b>{body}</div>'
def items(xs): return "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs)
def lab(t, n): return f'<div class="lbl">{t}</div>' + lines(n)
def two(a, b): return f'<div class="cols"><div>{a}</div><div>{b}</div></div>'
def row(*bs): return '<div class="cols">' + "".join(bs) + '</div>'
def kv(rows, h=20):
    return '<table>' + "".join(f"<tr style='height:{h}pt'><td style='width:34%;font-weight:600'>{k}</td><td></td></tr>" for k in rows) + '</table>'

def household():
    cover = ('<div class="pg"><div class="sub"><h1>Household Info Binder</h1><span>Keep somewhere everyone knows</span></div>'
             '<div class="box" style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center"><div style="font-size:30pt;font-weight:800;color:var(--c)">The ____________ Household</div>'
             '<div class="small" style="margin-top:14pt">Last updated: ______________</div></div>' + lab("What's inside", 0)
             + items(["Emergency contacts", "Household members & medical info", "Home & utilities", "Babysitter & house-sitter notes", "Pets", "Emergency plan & meeting points", "Important documents location"]) + '</div>')
    em = ('<div class="pg"><div class="sub"><h1>Emergency Contacts</h1><span>Emergency number: ________</span></div>' + kv(["Home address", "Nearest cross street / landmark", "Home phone", "Doctor / GP", "Dentist", "Nearest hospital", "Poison / health advice line", "Police (non-emergency)", "Vet"], 24)
          + '<div class="lbl">Family, neighbours & friends</div>' + tbl(["Name", "Relationship", "Phone", "Can help with"], ["24%", "18%", "20%", ""], 10, 24) + '</div>')
    mem = ('<div class="pg"><div class="sub"><h1>Household Members</h1><span></span></div>'
           + ('<div class="box" style="flex:1;margin-bottom:6pt"><div class="cols"><div><b>Name</b>' + lines(1) + '</div><div><b>Date of birth</b>' + lines(1) + '</div><div><b>Blood type</b>' + lines(1) + '</div></div>'
              '<div class="cols"><div><b>Allergies</b>' + lines(1) + '</div><div><b>Medications</b>' + lines(1) + '</div></div><div class="cols"><div><b>Conditions</b>' + lines(1) + '</div><div><b>Work / school & phone</b>' + lines(1) + '</div></div></div>') * 4 + '</div>')
    home = ('<div class="pg"><div class="sub"><h1>Home & Utilities</h1><span></span></div>' + kv(["Water stopcock / main shut-off", "Electricity fuse box / breaker", "Gas shut-off", "Boiler / heating (make & model)", "Fire extinguisher", "First aid kit", "Torch & spare batteries", "Spare keys held by", "Alarm company"], 22)
            + '<div class="lbl">Providers</div>' + tbl(["Service", "Company", "Account no.", "Phone"], ["20%", "26%", "24%", ""], 1, 0).replace("<tr style='height:0pt'><td></td><td></td><td></td><td></td></tr>", "")
            [:-8] + "".join(f"<tr style='height:22pt'><td>{s}</td><td></td><td></td><td></td></tr>" for s in ["Electricity", "Gas", "Water", "Internet", "Home insurance", "Plumber", "Electrician", "Landlord / agent"]) + '</table></div>')
    sit = ('<div class="pg"><div class="sub"><h1>Babysitter & Sitter Notes</h1><span>Date: ______________</span></div>' + row(box("We are at", lines(2)), box("Our phone", lines(2)), box("Back by", lines(2)))
           + two(box("Bedtimes & routine", lines(6)), box("Food, snacks & allergies", lines(6))) + two(box("House rules", lines(5)), box("Screen time", lines(5)))
           + two(box("Wi-Fi network", lines(1)), box("If something goes wrong, call", lines(1))) + lab("Other notes", 4) + '</div>')
    pets = ('<div class="pg"><div class="sub"><h1>Pets</h1><span></span></div>' + ('<div class="box" style="flex:1;margin-bottom:6pt"><div class="cols"><div><b>Name & type</b>' + lines(1) + '</div><div><b>Microchip</b>' + lines(1) + '</div></div>'
            '<div class="cols"><div><b>Food & amount</b>' + lines(2) + '</div><div><b>Medication</b>' + lines(2) + '</div></div><div class="cols"><div><b>Walks / routine</b>' + lines(1) + '</div><div><b>Vet & insurance</b>' + lines(1) + '</div></div></div>') * 3 + '</div>')
    plan = ('<div class="pg"><div class="sub"><h1>Emergency Plan</h1><span>Practise it twice a year</span></div>' + two(box("Meeting point near home", lines(2)), box("Meeting point away from home", lines(2)))
            + box("Out-of-area contact everyone calls", lines(1)) + '<div class="box" style="height:220pt;margin-bottom:5pt"><b>Escape routes: sketch your floor plan</b></div>'
            + two(box("Fire", items(["Smoke alarms tested monthly", "Two ways out of each room", "Get out, stay out, call for help", ""])), box("Grab bag", items(["Water & snacks", "Torch & radio", "Medication", "Copies of documents", "Phone charger & cash", "Spare keys"])))
            + box("Important documents are kept", lines(3)) + '</div>')
    return [cover, em, mem, home, sit, pets, plan]

def caregiver():
    prof = ('<div class="pg"><div class="sub"><h1>Care Profile</h1><span></span></div>' + kv(["Name", "Date of birth", "Address", "Emergency contact", "GP / doctor & phone", "Pharmacy", "Allergies", "Conditions / diagnoses", "Mobility & aids", "Hearing / sight", "Diet & swallowing", "Likes & comforts", "Dislikes & triggers"], 26)
            + lab("Important to know", 5) + '</div>')
    meds = ('<div class="pg"><div class="sub"><h1>Medication Schedule</h1><span>Checked with pharmacist: ________</span></div>' + tbl(["Medication", "Dose", "Morning", "Midday", "Evening", "Bedtime", "Purpose", "Prescriber"], ["20%", "10%", "8%", "8%", "8%", "8%", "", "14%"], 14, 26)
            + '<div class="lbl">Changes to medication</div>' + tbl(["Date", "Change", "By whom"], ["14%", "", "22%"], 6) + '</div>')
    days = "".join(f"<th style='text-align:center'>{d}</th>" for d in WD)
    week = ('<div class="pg"><div class="sub"><h1>Weekly Care Log</h1><span>Week of: ______________</span></div><table><tr><th style="width:22%"></th>' + days + '</tr>'
            + "".join(f"<tr style='height:30pt'><td>{t}</td>" + "<td></td>" * 7 + "</tr>" for t in ["Medication given ✓", "Breakfast", "Lunch", "Dinner", "Drinks (cups)", "Toilet / continence", "Sleep", "Mood", "Pain (0-10)", "Activity / outing", "Visitors", "Carer on duty"])
            + '</table>' + lab("Concerns to follow up", 4) + '</div>')
    appt = ('<div class="pg"><div class="sub"><h1>Appointments</h1><span></span></div>' + tbl(["Date & time", "With / where", "Reason", "Transport", "Outcome & next steps"], ["14%", "20%", "18%", "12%", ""], 16, 30) + '</div>')
    visit = ('<div class="pg"><div class="sub"><h1>Doctor Visit Notes</h1><span>Date: ______________</span></div>' + row(box("Seeing", lines(1)), box("Reason for visit", lines(1)))
             + lab("Questions to ask", 6) + lab("What the doctor said", 7) + two(lab("Tests / referrals", 4), lab("Medication changes", 4)) + lab("Next appointment", 1) + '</div>')
    team = ('<div class="pg"><div class="sub"><h1>Care Team & Rota</h1><span></span></div>' + tbl(["Name", "Role", "Phone", "Available"], ["24%", "20%", "20%", ""], 8, 24)
            + '<div class="lbl">Who\'s helping this week</div><table><tr><th style="width:18%"></th>' + days + '</tr>' + "".join(f"<tr style='height:28pt'><td>{t}</td>" + "<td></td>" * 7 + "</tr>" for t in ["Morning", "Afternoon", "Evening", "Night", "Shopping / errands"]) + '</table>'
            + two(box("Respite & support for me", lines(4)), box("Money & bills to sort", lines(4))) + '</div>')
    selfc = ('<div class="pg"><div class="sub"><h1>Carer Check-in</h1><span>You matter too</span></div>' + row(box("How I'm feeling (0-10)", lines(1)), box("Hours of sleep", lines(1)), box("Time for me this week", lines(1)))
             + lab("What's been hard", 5) + lab("What went well", 5) + lab("Help I could ask for", 4) + box("Small things that recharge me", items(["", "", "", "", ""])) + '</div>')
    return [prof, meds, week, week, appt, visit, team, selfc]

def symptoms():
    days = ('<div class="pg"><div class="sub"><h1>Food & Symptom Diary</h1><span>Date: ______________</span></div>'
            + row(box("Sleep (hrs)", lines(1)), box("Stress (0-10)", lines(1)), box("Water", '<div style="font-size:14pt;letter-spacing:6pt;margin-top:3pt">○○○○○○○○</div>'), box("Exercise", lines(1)))
            + tbl(["Time", "Food & drink (and amount)", "Symptoms", "Severity 0-10", "Time after eating"], ["10%", "", "26%", "12%", "13%"], 16, 27)
            + two(box("Bowel / stomach notes", lines(3)), box("Medication / supplements", lines(3))) + lab("Notes · possible triggers", 2) + '</div>')
    week = ('<div class="pg"><div class="sub"><h1>Weekly Symptom Overview</h1><span>Week of: ______________</span></div><table><tr><th style="width:22%">Symptom</th>' + "".join(f"<th style='text-align:center'>{d}</th>" for d in WD) + '</tr>'
            + "".join(f"<tr style='height:28pt'><td>{s}</td>" + "<td></td>" * 7 + "</tr>" for s in ["Bloating", "Stomach pain", "Heartburn / reflux", "Nausea", "Headache", "Fatigue", "Skin flare", "Mood", "", ""])
            + '</table><div class="small">Rate each 0 (none) to 10 (worst).</div>' + two(lab("Patterns I notice", 5), lab("Questions for my doctor", 5)) + '</div>')
    trig = ('<div class="pg"><div class="sub"><h1>Suspected Trigger Tracker</h1><span></span></div>' + tbl(["Food / trigger", "Times eaten", "Times followed by symptoms", "Which symptoms", "Verdict"], ["22%", "12%", "16%", "", "16%"], 14, 26)
            + '<div class="lbl">Reintroduction test (only with your doctor or dietitian\'s guidance)</div>' + tbl(["Day", "Food & amount", "Symptoms", "OK?"], ["10%", "", "34%", "8%"], 6, 24) + '</div>')
    safe = ('<div class="pg"><div class="sub"><h1>My Safe Foods & Meal Ideas</h1><span></span></div>' + two(box("Foods that agree with me", items([""] * 12)), box("Foods to be careful with", items([""] * 12)))
            + lab("Go-to meals", 6) + '<div class="small" style="margin-top:6pt">A personal diary to share with your doctor or dietitian. It does not diagnose anything.</div></div>')
    return [days, days, days, days, week, trig, safe]

def kidsreading():
    log = ('<div class="pg"><div class="sub"><h1>My Reading Log</h1><span>Name: ______________</span></div>' + tbl(["Date", "Book title", "Pages / minutes", "How I liked it", "Grown-up ✓"], ["11%", "", "15%", "18%", "12%"], 22, 28)
           + '<div class="small">How I liked it: draw 1 to 5 stars.</div></div>')
    stars = "".join(f'<div style="border:1.5pt solid #ddd;border-radius:50%;width:44pt;height:44pt;display:flex;align-items:center;justify-content:center;color:#bbb;font-size:10pt">{i}</div>' for i in range(1, 51))
    chal = (f'<div class="pg"><div class="sub"><h1>50 Book Challenge</h1><span>Name: ______________</span></div><div class="small">Colour a circle for every book you finish!</div><div style="display:grid;grid-template-columns:repeat(8,1fr);gap:9pt;margin:12pt 0;justify-items:center">{stars}</div>'
            + row(box("When I reach 10 books", lines(1)), box("25 books", lines(1)), box("50 books", lines(1))) + '</div>')
    rev = ('<div class="pg"><div class="sub"><h1>Book Review</h1><span>Date: ______________</span></div>' + two(lab("Title", 1), lab("Author", 1))
           + '<div class="box" style="height:190pt;margin:4pt 0"><b>Draw your favourite part</b></div>' + lab("The main characters are", 2) + lab("What happened", 4) + lab("My favourite part was", 2)
           + '<div class="cols"><div class="box"><b>I give it</b> ☆ ☆ ☆ ☆ ☆</div><div class="box"><b>I would tell a friend to read it</b> ☐ yes ☐ no</div></div></div>')
    bingo_items = ["A funny book", "A book about animals", "A book with a map", "Read outside", "Read to a pet or toy", "A poetry book", "A book from the library", "A comic or graphic novel", "Read with a torch",
                   "A true story", "A book from a series", "A book older than you", "FREE ✓", "A book about space", "Read to a grown-up", "A book with a dragon", "A scary book", "A book set in another country",
                   "Read in the car", "A book by a new author", "Reread a favourite", "A book about a sport", "A book with a girl hero", "A book with a boy hero", "A book chosen by a friend"]
    bg = "".join(f'<div style="border:1.5pt solid #ddd;border-radius:6pt;height:84pt;display:flex;align-items:center;justify-content:center;text-align:center;font-size:10pt;padding:4pt">{t}</div>' for t in bingo_items)
    bingo = f'<div class="pg"><div class="sub"><h1>Reading Bingo</h1><span>Name: ______________</span></div><div class="small">Cross off a square when you do it. Get a line, then try for the whole card!</div><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:7pt;margin-top:10pt">{bg}</div></div>'
    wish = ('<div class="pg"><div class="sub"><h1>Books I Want to Read</h1><span></span></div>' + tbl(["Title", "Author", "Who told me about it", "Read ✓"], ["", "24%", "24%", "10%"], 18, 26)
            + '<div class="lbl">New words I learned</div>' + tbl(["Word", "What it means"], ["26%", ""], 6, 24) + '</div>')
    marks = "".join(f'<div style="border:1.5pt dashed #bbb;border-radius:8pt;height:100%;display:flex;flex-direction:column;align-items:center;padding:10pt;box-sizing:border-box"><b style="color:var(--c);font-size:14pt">{t}</b><div style="font-size:30pt;margin:10pt 0">{e}</div><div class="small" style="text-align:center;margin-top:auto">This book belongs to<br><br>________________</div></div>'
                    for t, e in [("Keep reading!", "📚"), ("Book worm", "🐛"), ("Adventure awaits", "🗺️"), ("Read & dream", "🌙"), ("Page turner", "🚀")])
    bm = f'<div class="pg"><div class="sub"><h1>Bookmarks</h1><span>Cut out and colour in</span></div><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8pt;flex:1">{marks}</div></div>'
    return [log, log, chal, rev, rev, bingo, wish, bm]

def fishing():
    trip = ('<div class="pg"><div class="sub"><h1>Fishing Trip Log</h1><span>Date: ______________</span></div>' + row(box("Location / water", lines(1), 2), box("Peg / spot", lines(1)), box("Time", lines(1)))
            + row(box("Weather", lines(1)), box("Air temp", lines(1)), box("Water temp", lines(1)), box("Wind", lines(1)), box("Moon", lines(1)))
            + row(box("Water clarity", '<div class="small" style="margin-top:3pt">☐ clear ☐ coloured ☐ muddy</div>'), box("Tide / level", lines(1)), box("Fished with", lines(1)))
            + '<div class="lbl">Catches</div>' + tbl(["Time", "Species", "Length", "Weight", "Bait / lure", "Method / depth", "Kept / released"], ["9%", "18%", "10%", "10%", "17%", "", "12%"], 10, 24)
            + two(lab("What worked", 3), lab("What didn't", 3)) + '<div class="box" style="height:110pt;margin-top:4pt"><b>Spot sketch / photo</b></div></div>')
    pb = ('<div class="pg"><div class="sub"><h1>Personal Bests</h1><span></span></div>' + tbl(["Species", "Weight", "Length", "Date", "Where", "Bait"], ["20%", "12%", "12%", "12%", "", "16%"], 14, 28)
          + '<div class="lbl">Target species this year</div>' + tbl(["Species", "Goal", "Caught ✓"], ["", "30%", "14%"], 6, 24) + '</div>')
    spots = ('<div class="pg"><div class="sub"><h1>Spot Notes</h1><span></span></div>' + ('<div class="box" style="flex:1;margin-bottom:6pt"><div class="cols"><div><b>Name</b>' + lines(1) + '</div><div><b>Permit / day ticket</b>' + lines(1) + '</div></div>'
             '<div class="cols"><div><b>Directions & parking</b>' + lines(2) + '</div><div><b>Best season / tide / time</b>' + lines(2) + '</div></div><div><b>Notes (depth, snags, species)</b>' + lines(1) + '</div></div>') * 4 + '</div>')
    gear = [("Rods & reels", ["Rod(s)", "Reel(s)", "Spare spool", "Rod rest / holder"]), ("Terminal tackle", ["Hooks", "Line & leaders", "Weights / sinkers", "Floats", "Swivels", "Lures", "Bait"]),
            ("Tools", ["Landing net", "Unhooking mat", "Disgorger / pliers", "Scales & tape", "Line cutters", "Head torch"]), ("Comfort & safety", ["Licence / permit", "Chair", "Waterproofs", "Sunglasses (polarised)", "Hat & sunscreen", "Food & water", "First aid kit", "Phone charged"])]
    gp = ('<div class="pg"><div class="sub"><h1>Tackle Checklist</h1><span></span></div><div class="cols" style="flex:1"><div class="grow">' + "".join(box(t, items(x) + chks(1)) for t, x in gear[:2])
          + '</div><div class="grow">' + "".join(box(t, items(x) + chks(1)) for t, x in gear[2:]) + '</div></div></div>')
    yearl = ('<div class="pg"><div class="sub"><h1>Season Summary</h1><span>Year: ________</span></div>' + tbl(["Date", "Location", "Hours", "Fish caught", "Best fish", "Rating"], ["12%", "", "9%", "12%", "22%", "10%"], 26, 24)
             + row(box("Trips", lines(1)), box("Total fish", lines(1)), box("Best day", lines(1))) + '</div>')
    return [gp, trip, trip, trip, trip, pb, spots, yearl]

PRODUCTS = [("Household-Info-Binder", "#c92a2a", "#fff5f5", household), ("Caregiver-Planner", "#0c8599", "#e3fafc", caregiver), ("Food-Symptom-Diary", "#5c940d", "#f4fce3", symptoms),
            ("Kids-Reading-Log", "#7048e8", "#f3f0ff", kidsreading), ("Fishing-Log-Book", "#1864ab", "#e7f5ff", fishing)]
