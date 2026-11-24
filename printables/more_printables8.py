# Round 14 printables. exec()'d by build_round.py, so lines/chks are in scope.
WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
def tbl(heads, widths, n, h=22):
    return ('<table><tr>' + "".join(f"<th style='width:{w}'>{x}</th>" if w else f"<th>{x}</th>" for x, w in zip(heads, widths)) + '</tr>'
            + (f"<tr style='height:{h}pt'>" + "<td></td>" * len(heads) + "</tr>") * n + '</table>')
def box(t, body, flex=1, extra=""): return f'<div class="box" style="flex:{flex};margin-bottom:5pt;{extra}"><b>{t}</b>{body}</div>'
def items(xs): return "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs)
def lab(t, n): return f'<div class="lbl">{t}</div>' + lines(n)
def two(a, b): return f'<div class="cols"><div>{a}</div><div>{b}</div></div>'
def row(*bs): return '<div class="cols">' + "".join(bs) + '</div>'

def roadtrip():
    plan = ('<div class="pg"><div class="sub"><h1>Road Trip Planner</h1><span>Dates: ______________</span></div>'
            + row(box("From", lines(1)), box("To", lines(1)), box("Total distance", lines(1)), box("Travellers", lines(1)))
            + '<div class="lbl">Route & stops</div>' + tbl(["Day", "From → To", "Distance", "Drive time", "Overnight / booking ref"], ["8%", "", "12%", "12%", "28%"], 10, 24)
            + two(lab("Must-see stops", 5), lab("Food stops & snacks", 5)) + '</div>')
    bud = ('<div class="pg"><div class="sub"><h1>Trip Budget & Fuel Log</h1><span></span></div>'
           + '<table><tr><th>Category</th><th style="width:20%">Budget</th><th style="width:20%">Spent</th><th style="width:20%">Difference</th></tr>'
           + "".join(f"<tr style='height:22pt'><td>{c}</td><td></td><td></td><td></td></tr>" for c in ["Fuel", "Tolls & parking", "Accommodation", "Food & drinks", "Activities & tickets", "Souvenirs", "Emergencies", "Total"]) + '</table>'
           + '<div class="lbl">Fuel log</div>' + tbl(["Date", "Where", "Odometer", "Litres / gallons", "Cost"], ["12%", "", "16%", "16%", "14%"], 12) + '</div>')
    car = [("Car check", ["Tyre pressure & tread", "Oil & coolant", "Screen wash", "Lights working", "Spare tyre & jack", "Breakdown cover number", "Licence & insurance docs"]),
           ("In the car", ["Phone holder & chargers", "Offline maps", "Sunglasses", "Tissues & wipes", "Rubbish bag", "Blanket & pillow", "Water bottles"]),
           ("Snack bag", ["Fruit", "Crackers", "Sandwiches", "Sweets for emergencies", "Reusable cups"]), ("Kids' bag", ["Tablet & headphones", "Books & colouring", "Travel games", "Change of clothes", "Sick bags", "Favourite toy"])]
    pk = ('<div class="pg"><div class="sub"><h1>Road Trip Checklist</h1><span></span></div><div class="cols" style="flex:1"><div class="grow">' + "".join(box(t, items(x) + chks(1)) for t, x in car[:2])
          + '</div><div class="grow">' + "".join(box(t, items(x) + chks(1)) for t, x in car[2:]) + '</div></div></div>')
    spots = ["Red car", "Cow", "Bridge", "Tractor", "Police car", "Church", "Motorbike", "Horse", "Bus", "Windmill", "Lorry", "Sheep", "Train", "River", "Castle", "Petrol station", "Yellow car", "Dog", "Plane", "Bicycle"]
    bingo = "".join(f'<div style="border:1.5pt solid #ddd;border-radius:6pt;height:58pt;display:flex;align-items:center;justify-content:center;text-align:center;font-size:11pt">{s}</div>' for s in spots)
    kids = ('<div class="pg"><div class="sub"><h1>Car Spotting Bingo</h1><span>Name: ______________</span></div><div class="small">Cross off each one you see. First to get a full row wins!</div>'
            f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:7pt;margin:8pt 0">{bingo}</div>'
            + two(box("Number plate game: letters A to Z", '<div style="font-size:13pt;letter-spacing:5pt;margin-top:6pt;line-height:1.8">' + " ".join("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + '</div>'), box("Are we nearly there? Colour a box every hour", '<div style="display:flex;flex-wrap:wrap;gap:4pt;margin-top:6pt">' + '<span style="width:28pt;height:28pt;border:1.5pt solid #ccc;border-radius:4pt"></span>' * 12 + '</div>'))
            + '</div>')
    mem = ('<div class="pg"><div class="sub"><h1>Trip Memories</h1><span></span></div>' + row(box("Best view", lines(2)), box("Best meal", lines(2)), box("Funniest moment", lines(2)))
           + lab("Day by day", 14) + '<div class="box" style="height:170pt;margin-top:4pt"><b>Photos / tickets / postcards</b></div></div>')
    return [plan, bud, pk, kids, kids, mem]

def meetings():
    mt = ('<div class="pg"><div class="sub"><h1>Meeting Notes</h1><span>Date: __________  Time: ______</span></div>'
          + row(box("Meeting", lines(1), 2), box("Facilitator", lines(1)), box("Note taker", lines(1))) + lab("Attendees", 2)
          + '<div class="cols" style="flex:1"><div style="flex:1">' + lab("Agenda", 13) + '</div><div style="flex:1.6">' + lab("Notes", 13) + '</div></div>' + lab("Decisions made", 4)
          + '<div class="lbl">Action items</div>' + tbl(["Action", "Owner", "Due", "✓"], ["", "18%", "14%", "7%"], 7) + lab("Next meeting", 1) + '</div>')
    wk = ('<div class="pg"><div class="sub"><h1>Work Week</h1><span>Week of: ______________</span></div>' + row(box("Top 3 priorities", items(["", "", ""])), box("Deadlines this week", lines(3)))
          + '<div class="cols" style="flex:1">' + "".join(f'<div class="box" style="flex:1"><b>{d}</b>' + lines(26) + "</div>" for d in WD[:5]) + '</div>'
          + two(lab("Waiting on", 3), lab("Ideas & follow-ups", 3)) + '</div>')
    o1 = ('<div class="pg"><div class="sub"><h1>One-to-One</h1><span>Date: ______________</span></div>' + row(box("With", lines(1)), box("Role", lines(1)))
          + lab("Wins since last time", 4) + lab("Challenges / blockers", 4) + lab("Goals & development", 4) + lab("Feedback (both ways)", 4) + '<div class="lbl">Agreed actions</div>' + tbl(["Action", "Who", "By when"], ["", "20%", "18%"], 6) + '</div>')
    proj = ('<div class="pg"><div class="sub"><h1>Project Overview</h1><span></span></div>' + row(box("Project", lines(1), 2), box("Start", lines(1)), box("Deadline", lines(1)))
            + two(lab("Goal / what success looks like", 4), lab("Stakeholders", 4)) + '<div class="lbl">Milestones</div>' + tbl(["Milestone", "Owner", "Due", "Status"], ["", "18%", "14%", "16%"], 8)
            + '<div class="lbl">Tasks</div>' + tbl(["Task", "Owner", "Due", "✓"], ["", "18%", "14%", "7%"], 10) + lab("Risks & notes", 3) + '</div>')
    log = ('<div class="pg"><div class="sub"><h1>Action Item Tracker</h1><span></span></div>' + tbl(["Date raised", "Action", "From meeting", "Owner", "Due", "Done"], ["11%", "", "18%", "13%", "11%", "8%"], 28) + '</div>')
    return [wk, mt, mt, mt, o1, proj, log]

def birthday():
    ov = ('<div class="pg"><div class="sub"><h1>Birthday Party Planner</h1><span></span></div>' + row(box("Birthday child", lines(1)), box("Turning", lines(1)), box("Date & time", lines(1)))
          + row(box("Venue", lines(1), 2), box("Theme", lines(1)), box("Budget", lines(1))) + two(lab("Party ideas", 6), lab("Games & activities", 6))
          + '<div class="lbl">Countdown</div>' + two(box("4-6 weeks before", items(["Set budget & guest list", "Book venue / entertainer", "Choose theme", "Send invitations"])), box("2 weeks before", items(["Order cake", "Buy decorations", "Plan food", "Party bags"])))
          + two(box("Week before", items(["Confirm numbers & allergies", "Charge camera", "Shopping list", "Plan the timeline"])), box("On the day", items(["Set up & decorate", "Collect cake", "Music ready", "Thank-you list"]))) + '</div>')
    gl = ('<div class="pg"><div class="sub"><h1>Guest List & RSVPs</h1><span></span></div>' + tbl(["Child's name", "Parent & phone", "Invited", "RSVP", "Allergies", "Gift"], ["20%", "", "9%", "9%", "16%", "18%"], 26, 23) + '</div>')
    bd = ('<div class="pg"><div class="sub"><h1>Budget & Shopping</h1><span></span></div><table><tr><th>Item</th><th style="width:18%">Budget</th><th style="width:18%">Actual</th><th style="width:8%">✓</th></tr>'
          + "".join(f"<tr style='height:22pt'><td>{c}</td><td></td><td></td><td></td></tr>" for c in ["Venue", "Cake", "Food & drinks", "Decorations", "Entertainment", "Party bags", "Invitations", "Tableware", "Total"]) + '</table>'
          + two(box("Food & drinks", items(["", "", "", "", "", "", "", ""])), box("Decorations & supplies", items(["Balloons", "Banner", "Candles & lighter", "Plates, cups, napkins", "Tablecloth", "Bin bags", "", ""]))) + '</div>')
    tl = ('<div class="pg"><div class="sub"><h1>Party Day Timeline</h1><span></span></div>' + tbl(["Time", "What's happening", "Who's in charge"], ["14%", "", "24%"], 16, 26)
          + row(box("Helpers", lines(3)), box("Emergency contacts", lines(3))) + '</div>')
    def card(): return ('<div style="border:1.5pt dashed #bbb;border-radius:10pt;padding:12pt;display:flex;flex-direction:column;justify-content:space-between">'
                        '<b style="font-size:20pt;color:var(--c);text-align:center">You\'re invited!</b><div class="small" style="line-height:2.2">To: ______________________<br>Come and celebrate ______________\'s birthday<br>Date: ____________  Time: ________<br>Where: _______________________<br>RSVP: ________________________</div></div>')
    inv = f'<div class="pg"><div class="sub"><h1>Invitations</h1><span>Cut out</span></div><div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:10pt;flex:1">{card() * 4}</div></div>'
    ty = ('<div class="pg"><div class="sub"><h1>Thank-you Tracker</h1><span></span></div>' + tbl(["From", "Gift", "Thank-you sent"], ["30%", "", "16%"], 20, 24) + lab("Party memories", 5) + '</div>')
    return [ov, gl, bd, tl, inv, ty]

def bible():
    page = ('<div class="pg"><div class="sub"><h1>Bible Study</h1><span>Date: ______________</span></div>' + row(box("Passage", lines(1), 2), box("Topic", lines(1)))
            + lab("Key verse (write it out)", 3) + two(lab("What does it say? (observe)", 6), lab("What does it mean? (interpret)", 6))
            + lab("How does it apply to my life?", 5) + two(lab("Prayer", 4), lab("Questions to explore", 4)) + '</div>')
    soap = ('<div class="pg"><div class="sub"><h1>S.O.A.P. Journal</h1><span>Date: ______________</span></div>' + "".join(box(t, '<div class="small">' + s + '</div>' + lines(n)) for t, s, n in
            [("S · Scripture", "Write out the verse or verses that stood out.", 4), ("O · Observation", "What do you notice? Who, what, where, why?", 5), ("A · Application", "What is God saying to you today? What will you do?", 5), ("P · Prayer", "Write a short prayer in response.", 4)]) + '</div>')
    pr = ('<div class="pg"><div class="sub"><h1>Prayer List</h1><span></span></div>' + tbl(["Date", "Prayer request", "For", "Answered", "Date answered"], ["11%", "", "18%", "10%", "14%"], 26) + '</div>')
    books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
             "Ecclesiastes", "Song of Songs", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
             "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon",
             "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"]
    rt = ('<div class="pg"><div class="sub"><h1>Bible Reading Tracker</h1><span>Tick each book when finished</span></div><div style="columns:3;column-gap:10pt;font-size:9.5pt">'
          + "".join(f'<div class="chk" style="break-inside:avoid;margin:1.5pt 0"><i></i>{b}</div>' for b in books) + '</div>' + lab("Started · finished", 1) + '</div>')
    ser = ('<div class="pg"><div class="sub"><h1>Sermon Notes</h1><span>Date: ______________</span></div>' + row(box("Speaker", lines(1)), box("Church / event", lines(1)), box("Passage", lines(1)))
           + lab("Title / big idea", 2) + lab("Main points", 12) + two(lab("What stood out", 4), lab("My response this week", 4)) + '</div>')
    mv = ('<div class="pg"><div class="sub"><h1>Memory Verses</h1><span></span></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:8pt">'
          + ('<div style="border:1.5pt dashed #bbb;border-radius:8pt;padding:8pt;height:200pt;overflow:hidden"><div class="small">Reference: ________________</div>' + lines(4) + '<div class="small" style="margin-top:4pt">Learned ☐</div></div>') * 6 + '</div></div>')
    return [rt, page, page, soap, soap, ser, pr, mv]

def puppy():
    prof = ('<div class="pg"><div class="sub"><h1>Meet My Puppy</h1><span></span></div><div class="cols"><div class="box" style="flex:1;height:180pt"><b>Photo</b></div><div style="flex:1.3">'
            + lab("Name", 1) + lab("Breed", 1) + lab("Birthday · came home", 1) + lab("Breeder / rescue", 1) + lab("Microchip no.", 1) + '</div></div>'
            + two(lab("Vet & phone", 2), lab("Food & amount per day", 2)) + '<div class="lbl">Vaccinations & treatments</div>' + tbl(["Date", "Vaccine / flea / worming", "Next due"], ["16%", "", "20%"], 8)
            + lab("Weight check", 2) + '</div>')
    pot = ('<div class="pg"><div class="sub"><h1>Toilet Training Log</h1><span>Week of: ______________</span></div><div class="small">✓ = outside  ✗ = accident. Take your puppy out after waking, eating, playing and every 1-2 hours.</div><table><tr><th style="width:12%">Time</th>'
           + "".join(f"<th style='text-align:center'>{d}</th>" for d in WD) + '</tr>'
           + "".join(f"<tr style='height:23pt'><td class='small'>{t}</td>" + "<td></td>" * 7 + "</tr>" for t in ["6 am", "7 am", "8 am", "9 am", "10 am", "11 am", "12 pm", "1 pm", "2 pm", "3 pm", "4 pm", "5 pm", "6 pm", "7 pm", "8 pm", "9 pm", "10 pm", "Night"])
           + '</table>' + row(box("Accidents this week", lines(1)), box("Longest dry spell", lines(1))) + '</div>')
    cmds = ["Name / look at me", "Sit", "Down", "Stay", "Come (recall)", "Leave it", "Drop it", "Wait at doors", "Loose-lead walking", "Settle on mat", "Paw", "Crate / bed"]
    stages = ["Learning", "With lure", "No lure", "With distractions", "Anywhere ✓"]
    tr = ('<div class="pg"><div class="sub"><h1>Commands & Tricks</h1><span>Tick each stage as your puppy masters it</span></div><table><tr><th>Command</th>' + "".join(f"<th style='text-align:center;width:13%'>{s}</th>" for s in stages) + '</tr>'
          + "".join(f"<tr style='height:28pt'><td>{c}</td>" + "<td></td>" * 5 + "</tr>" for c in cmds + ["", ""]) + '</table>' + lab("Training tips that work for my puppy", 3) + '</div>')
    soc = [("People", ["Men with beards", "Children", "People in hats", "Uniforms", "Wheelchairs / walkers", "Crowds"]), ("Places", ["Car ride", "Vet visit", "Town centre", "Pet shop", "Park", "Café"]),
           ("Sounds", ["Hoover", "Doorbell", "Traffic", "Fireworks (recording)", "Thunder (recording)", "Washing machine"]), ("Handling & other animals", ["Paws & nails", "Ears & teeth", "Brushing", "Calm adult dog", "Cats", "Bath"])]
    sc = ('<div class="pg"><div class="sub"><h1>Socialisation Checklist</h1><span>Short, positive, lots of treats</span></div><div class="cols" style="flex:1"><div class="grow">' + "".join(box(t, items(x)) for t, x in soc[:2])
          + '</div><div class="grow">' + "".join(box(t, items(x)) for t, x in soc[2:]) + '</div></div>' + lab("How it went", 3) + '</div>')
    dl = ('<div class="pg"><div class="sub"><h1>Daily Puppy Log</h1><span>Date: ______________</span></div>' + row(box("Meals", items(["Breakfast", "Lunch", "Dinner"])), box("Walks / play", lines(3)), box("Naps", lines(3)))
          + lab("Training practised today", 4) + lab("New experiences", 3) + lab("Funny moments", 3) + '<div class="lbl">Mood</div>' + '<div style="font-size:22pt;letter-spacing:12pt">😴 😊 🤪 😟</div>' + '</div>')
    gr = ('<div class="pg"><div class="sub"><h1>Growth & Milestones</h1><span></span></div>' + tbl(["Date", "Age", "Weight", "Milestone / first time"], ["14%", "12%", "12%", ""], 16, 26)
          + '<div class="box" style="height:150pt;margin-top:6pt"><b>Paw print</b></div></div>')
    return [prof, pot, pot, tr, sc, dl, dl, gr]

PRODUCTS = [("Road-Trip-Planner", "#e8590c", "#fff4e6", roadtrip), ("Meeting-Notes-Work-Planner", "#364fc7", "#edf2ff", meetings), ("Kids-Birthday-Party-Planner", "#d6336c", "#fff0f6", birthday),
            ("Bible-Study-Journal", "#5f3dc4", "#f3f0ff", bible), ("Puppy-Training-Journal", "#a0522d", "#fdf3ea", puppy)]
