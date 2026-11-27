# Round 17 printables. exec()'d by build_round.py, so lines/chks are in scope.
WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
def tbl(heads, widths, n, h=22):
    return ('<table><tr>' + "".join(f"<th style='width:{w}'>{x}</th>" if w else f"<th>{x}</th>" for x, w in zip(heads, widths)) + '</tr>'
            + (f"<tr style='height:{h}pt'>" + "<td></td>" * len(heads) + "</tr>") * n + '</table>')
def box(t, body, flex=1, extra=""): return f'<div class="box" style="flex:{flex};margin-bottom:5pt;{extra}"><b>{t}</b>{body}</div>'
def items(xs): return "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs)
def lab(t, n): return f'<div class="lbl">{t}</div>' + lines(n)
def two(a, b): return f'<div class="cols"><div>{a}</div><div>{b}</div></div>'
def row(*bs): return '<div class="cols">' + "".join(bs) + '</div>'
def scale(lo, hi, n=5): return '<div style="display:flex;align-items:center;gap:6pt;margin-top:3pt;font-size:8pt"><span>' + lo + '</span>' + '<span style="width:14pt;height:14pt;border:1.2pt solid #bbb;border-radius:50%"></span>' * n + '<span>' + hi + '</span></div>'

def camping():
    plan = ('<div class="pg"><div class="sub"><h1>Camping Trip Plan</h1><span>Dates: ______________</span></div>' + row(box("Campsite", lines(1), 2), box("Pitch / site no.", lines(1)))
            + row(box("Address & directions", lines(2), 2), box("Check-in / out", lines(2)))
            + row(box("Booking ref", lines(1)), box("Cost", lines(1)), box("Who's coming", lines(1), 2))
            + row(box("Facilities", items(["Toilets & showers", "Electric hook-up", "Drinking water", "Shop nearby", "Campfires allowed", "Dogs allowed"])), box("Weather forecast", '<table><tr>' + "".join(f"<th style='text-align:center'>{d}</th>" for d in WD[:4]) + '</tr><tr style="height:40pt">' + "<td></td>" * 4 + '</tr></table>' + lines(1)))
            + '<div class="lbl">Itinerary</div>' + tbl(["Day", "Morning", "Afternoon", "Evening"], ["12%", "", "", ""], 4, 46)
            + two(lab("Nearby walks & things to do", 3), lab("Emergency: nearest hospital, ranger, phone", 3)) + '</div>')
    gear = ('<div class="pg"><div class="sub"><h1>Camping Gear Checklist</h1><span></span></div><div class="cols">'
            + "".join('<div>' + "".join(box(t, items(xs)) for t, xs in col) + '</div>' for col in [
                [("Shelter", ["Tent + poles + pegs", "Footprint / groundsheet", "Mallet", "Spare pegs & guy lines", "Tarp", "Windbreak"]),
                 ("Sleeping", ["Sleeping bags", "Mats / airbeds", "Pump", "Pillows", "Blankets", "Head torches"]),
                 ("Furniture", ["Chairs", "Table", "Lantern", "Rug / mat"])],
                [("Kitchen", ["Stove + gas", "Lighter / matches", "Pots & pan", "Kettle", "Plates, bowls, cups", "Cutlery & knife", "Chopping board", "Cool box + ice packs", "Water carrier", "Washing-up bowl & liquid", "Bin bags", "Tea towel"]),
                 ("Clothing", ["Waterproofs", "Warm layers", "Hats & gloves", "Spare socks", "Walking boots", "Sliders for showers"])],
                [("Wash & health", ["Towels", "Toiletries", "Toilet roll", "Sun cream", "Insect repellent", "First aid kit", "Medicines", "Hand sanitiser"]),
                 ("Tools & extras", ["Multi-tool", "Duct tape", "Power bank", "Cable / hook-up lead", "Map", "Cards & games", "Book", "Dog bed & lead"]),
                 ("Don't forget", lines(4))]]) + '</div></div>')
    meals = ('<div class="pg"><div class="sub"><h1>Camp Meal Plan</h1><span></span></div><table><tr><th style="width:12%">Day</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th><th style="width:18%">Snacks</th></tr>'
             + "".join(f"<tr style='height:76pt'><td>Day {i}</td>" + "<td></td>" * 4 + "</tr>" for i in range(1, 6)) + '</table>'
             + two(box("Food shopping list", lines(9)), box("Easy camp meal ideas", '<div class="small" style="line-height:1.9;margin-top:4pt">Bacon & egg rolls · porridge pots · wraps · one-pot chilli · pasta & pesto · foil-packet potatoes · sausages & beans · campfire banana boats · s\'mores · pancakes</div>')) + '</div>')
    log = ('<div class="pg"><div class="sub"><h1>Campsite Review</h1><span>Date: ______________</span></div>' + row(box("Campsite", lines(1), 2), box("Nights", lines(1)), box("Cost", lines(1)))
           + '<table><tr><th style="width:30%">Rate it</th><th style="text-align:center">★</th><th style="text-align:center">★★</th><th style="text-align:center">★★★</th><th style="text-align:center">★★★★</th><th style="text-align:center">★★★★★</th></tr>'
           + "".join(f"<tr style='height:20pt'><td>{x}</td>" + "<td></td>" * 5 + "</tr>" for x in ["Pitch", "Toilets & showers", "Quiet at night", "Views", "Kid-friendly", "Value"]) + '</table>'
           + two(lab("Best bits", 4), lab("What went wrong", 4)) + two(lab("Pack next time", 4), lab("Would we go back?", 4)) + '<div class="box" style="height:230pt"><b>Photo or sketch</b></div></div>')
    places = ('<div class="pg"><div class="sub"><h1>Campsites to Try</h1><span></span></div>' + tbl(["Campsite", "Where", "Why", "Price", "Booked / visited"], ["24%", "18%", "", "10%", "14%"], 26, 24) + '</div>')
    return [gear, plan, meals, log, log, log, places, plan]

def gamenight():
    def score(t, players=6, rounds=12):
        return ('<div class="pg"><div class="sub"><h1>' + t + '</h1><span>Game: ____________ · Date: ______</span></div><table><tr><th style="width:11%">Round</th>'
                + "".join("<th style='height:30pt'></th>" for _ in range(players)) + '</tr>' + "".join(f"<tr style='height:33pt'><td>{i}</td>" + "<td></td>" * players + "</tr>" for i in range(1, rounds + 1))
                + '<tr style="height:32pt"><td><b>Total</b></td>' + "<td></td>" * players + '</tr></table>' + two(lab("Winner", 1), lab("Notes & house rules", 1)) + '</div>')
    dice = ('<div class="pg"><div class="sub"><h1>Dice Score Sheet</h1><span>Date: ______________</span></div><table><tr><th style="width:30%">Category</th>' + "<th></th>" * 5 + '</tr>'
            + "".join(f"<tr style='height:27pt'><td>{c}</td>" + "<td></td>" * 5 + "</tr>" for c in ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"])
            + "<tr style='height:21pt;background:var(--s)'><td><b>Top total</b></td>" + "<td></td>" * 5 + "</tr><tr style='height:21pt'><td>Bonus (63 or more = 35)</td>" + "<td></td>" * 5 + "</tr>"
            + "".join(f"<tr style='height:27pt'><td>{c}</td>" + "<td></td>" * 5 + "</tr>" for c in ["Three of a kind", "Four of a kind", "Full house (25)", "Small straight (30)", "Large straight (40)", "Five of a kind (50)", "Chance"])
            + "<tr style='height:26pt;background:var(--s)'><td><b>Grand total</b></td>" + "<td></td>" * 5 + "</tr></table><div class='small' style='margin-top:6pt'>Write player names across the top. Works with any five-dice game.</div></div>")
    cards = ('<div class="pg"><div class="sub"><h1>Card Game Tally</h1><span>Date: ______________</span></div><div class="cols">'
             + "".join('<div class="box"><b>Game: ____________</b><table style="margin-top:4pt"><tr>' + "<th style='height:22pt'></th>" * 4 + '</tr>' + "<tr style='height:19pt'>" + "<td></td>" * 4 + "</tr>" * 1 * 0 + "".join("<tr style='height:19pt'>" + "<td></td>" * 4 + "</tr>" for _ in range(22)) + "<tr style='height:22pt;background:var(--s)'>" + "<td></td>" * 4 + '</tr></table></div>' for _ in range(2))
             + '</div><div class="small" style="margin-top:6pt">Two games per page: rummy, hearts, crazy eights, whist, canasta or your family favourite.</div></div>')
    league = ('<div class="pg"><div class="sub"><h1>Game Night League</h1><span>Season: ______________</span></div>' + tbl(["Date", "Game", "1st (3 pts)", "2nd (2 pts)", "3rd (1 pt)", "Host"], ["11%", "", "16%", "16%", "16%", "12%"], 14, 24)
              + '<div class="lbl">League table</div>' + tbl(["Player", "Played", "Wins", "Points", "Position"], ["", "12%", "12%", "12%", "12%"], 8, 22) + '</div>')
    games = ('<div class="pg"><div class="sub"><h1>Our Games Collection</h1><span></span></div>' + tbl(["Game", "Players", "Time", "Ages", "Rating", "Last played"], ["", "11%", "10%", "9%", "12%", "14%"], 20, 22)
             + two(lab("Games to buy or try", 4), lab("Snacks for game night", 4)) + '</div>')
    return [score("Score Sheet"), score("Score Sheet"), score("Score Sheet", 8, 12), dice, dice, cards, league, games]

def yearreview():
    q = lambda t, n: lab(t, n)
    big = ('<div class="pg"><div class="sub"><h1>My Year in Review</h1><span>Year: ________</span></div>' + row(box("My year in three words", lines(1)), box("Overall, this year was", '<div class="small" style="margin-top:4pt">☆ ☆ ☆ ☆ ☆</div>'))
           + two(q("Biggest wins & proudest moments", 7), q("Hardest moments, and how I got through", 7)) + two(q("Best memories", 7), q("What I learned", 7))
           + two(q("People who made my year", 5), q("What I'm letting go of", 5)) + '</div>')
    months = ('<div class="pg"><div class="sub"><h1>Month by Month</h1><span>One highlight from each month</span></div><div class="cols" style="flex-wrap:wrap">'
              + "".join(f'<div class="box" style="flex:0 0 31%;height:150pt;margin-bottom:6pt"><b>{m}</b></div>' for m in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]) + '</div></div>')
    areas = ('<div class="pg"><div class="sub"><h1>Life Areas Check-in</h1><span>Rate each area 1-10, then and now</span></div><table><tr><th style="width:20%">Area</th><th style="width:10%;text-align:center">Start of year</th><th style="width:10%;text-align:center">Now</th><th>What changed</th><th style="width:28%">Next year I want</th></tr>'
             + "".join(f"<tr style='height:54pt'><td>{a}</td>" + "<td></td>" * 4 + "</tr>" for a in ["Health & body", "Mind & mood", "Family", "Friends", "Love", "Work / study", "Money", "Home", "Fun & hobbies", "Growth"]) + '</table></div>')
    faves = ('<div class="pg"><div class="sub"><h1>Favourites of the Year</h1><span></span></div><div class="cols">'
             + "".join('<div>' + "".join(box(t, lines(3)) for t in col) + '</div>' for col in [["Book", "Film", "TV show", "Song / album", "Podcast", "Meal"], ["Place I went", "Day out", "Purchase", "New habit", "Thing I made", "Photo I took"]])
             + '</div>' + q("Moments I want to remember forever", 4) + '</div>')
    goals = ('<div class="pg"><div class="sub"><h1>Last Year\'s Goals</h1><span>How did they go?</span></div>' + tbl(["Goal", "Done / partly / not yet", "What helped or got in the way"], ["32%", "18%", ""], 10, 30)
             + two(q("Surprise achievements I didn't plan", 4), q("Habits that stuck", 4)) + '</div>')
    ahead = ('<div class="pg"><div class="sub"><h1>Looking Ahead</h1><span>Next year: ________</span></div>' + row(box("My word for next year", lines(1)), box("How I want to feel", lines(1)))
             + '<div class="lbl">Top goals</div>' + tbl(["Goal", "Why it matters", "First small step", "By when"], ["28%", "", "26%", "12%"], 5, 32)
             + two(q("Things to start", 5), q("Things to stop", 5)) + two(q("Places to go & things to try", 5), q("A letter to myself one year from now", 5)) + '</div>')
    return [big, months, areas, faves, goals, ahead, ahead, big]

def cycle():
    cal = ('<div class="pg"><div class="sub"><h1>Cycle Tracker</h1><span>Year: ________</span></div><div class="small">Shade the days of your period. Use the key for spotting, symptoms and mood.</div>'
           + '<table style="font-size:7pt"><tr><th style="width:10%">Month</th>' + "".join(f"<th style='text-align:center;padding:2pt 0'>{d}</th>" for d in range(1, 32)) + '</tr>'
           + "".join(f"<tr style='height:40pt'><td>{m}</td>" + "<td></td>" * 31 + "</tr>" for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]) + '</table>'
           + row(box("Key", '<div class="small" style="line-height:1.9;margin-top:3pt">■ heavy · ▣ medium · □ light · • spotting · C cramps · H headache · M low mood · E energy high</div>', 2), box("My average cycle", lines(1))) + '</div>')
    log = ('<div class="pg"><div class="sub"><h1>Cycle Log</h1><span></span></div>' + tbl(["Cycle", "Period start", "Period end", "Days of bleeding", "Cycle length", "Notes"], ["8%", "14%", "14%", "13%", "13%", ""], 13, 26)
           + two(box("Average period length", lines(1)), box("Average cycle length", lines(1))) + lab("Patterns I've noticed", 4) + '</div>')
    month = ('<div class="pg"><div class="sub"><h1>Monthly Symptom Tracker</h1><span>Month: ______________</span></div><table style="font-size:7pt"><tr><th style="width:17%">Day</th>' + "".join(f"<th style='text-align:center;padding:2pt 0'>{d}</th>" for d in range(1, 32)) + '</tr>'
             + "".join(f"<tr style='height:20pt'><td>{s}</td>" + "<td></td>" * 31 + "</tr>" for s in ["Flow", "Cramps", "Headache", "Bloating", "Tender breasts", "Back pain", "Acne", "Cravings", "Tired", "Energy", "Mood", "Anxious", "Sleep", "Exercise", "Medication", "Discharge", "Temperature", "Notes"]) + '</table>'
             + '<div class="small" style="margin-top:5pt">Rate 0-3 or tick. Bring this page to appointments: it helps your doctor or nurse.</div></div>')
    daily = ('<div class="pg"><div class="sub"><h1>How I Feel Through My Cycle</h1><span></span></div>' + "".join(box(t, '<div class="small">' + s + '</div>' + lines(4)) for t, s in [
        ("Period (days 1-5 or so)", "Energy, mood, cravings, what helps"), ("After my period", "Energy, mood, what I feel like doing"), ("Around ovulation", "Energy, mood, any signs"), ("Before my period", "PMS signs, mood, what helps")])
        + two(lab("Comfort list: things that help", 4), lab("Questions for my doctor", 4)) + '</div>')
    sup = ('<div class="pg"><div class="sub"><h1>Period Kit & Supplies</h1><span></span></div>' + two(box("Kit for my bag", items(["Pads / tampons / cup", "Spare underwear", "Pain relief", "Wipes", "Small bag for disposal", "Hot water bottle (home)", "Snack"])),
           box("Supplies to restock", tbl(["Item", "Have", "Buy"], ["", "18%", "18%"], 8, 20))) + '<div class="lbl">Medication & contraception</div>' + tbl(["Name", "Dose", "When", "Started", "Notes"], ["24%", "14%", "16%", "14%", ""], 6, 24) + lab("Notes", 10) + '</div>')
    return [cal, log, month, month, month, daily, sup, cal]

def golf():
    holes = lambda a, b: "".join(f"<th style='text-align:center'>{i}</th>" for i in range(a, b))
    def half(t, a): return ('<div class="lbl">' + t + '</div><table style="font-size:8pt"><tr><th style="width:14%">Hole</th>' + holes(a, a + 9) + "<th style='text-align:center'>" + ("Out" if a == 1 else "In") + "</th></tr>"
                            + "".join(f"<tr style='height:21pt'><td>{r}</td>" + "<td></td>" * 10 + "</tr>" for r in ["Par", "Yards", "Score", "Putts", "Fairway ✓", "Green ✓", "Penalties"]) + '</table>')
    card = ('<div class="pg"><div class="sub"><h1>Round Scorecard</h1><span>Date: ______________</span></div>' + row(box("Course", lines(1), 2), box("Tees", lines(1)), box("Handicap", lines(1)))
            + row(box("Playing with", lines(1), 2), box("Weather", lines(1))) + half("Front nine", 1) + half("Back nine", 10)
            + row(box("Total score", lines(1)), box("Total putts", lines(1)), box("Fairways hit", lines(1)), box("Greens in reg.", lines(1))) + two(lab("What went well", 3), lab("Work on next", 3)) + '</div>')
    log = ('<div class="pg"><div class="sub"><h1>Rounds Log</h1><span></span></div>' + tbl(["Date", "Course", "Score", "+/- par", "Putts", "FIR", "GIR", "Notes"], ["10%", "", "8%", "9%", "8%", "7%", "7%", "22%"], 28, 22) + '</div>')
    prac = ('<div class="pg"><div class="sub"><h1>Practice Session</h1><span>Date: ______________</span></div>' + row(box("Where", lines(1)), box("Time spent", lines(1)), box("Focus", lines(1), 2))
            + '<div class="lbl">Drills</div>' + tbl(["Drill", "Club", "Reps / balls", "Success", "Notes"], ["26%", "12%", "14%", "12%", ""], 8, 26)
            + two(box("Putting: makes from", tbl(["Distance", "Made / tried"], ["", "40%"], 5, 18)), box("Chipping & bunker", lines(6))) + lab("Swing thoughts & feel", 3) + '</div>')
    clubs = ('<div class="pg"><div class="sub"><h1>My Club Distances</h1><span></span></div>' + '<table><tr><th style="width:24%">Club</th><th>Carry</th><th>Total</th><th>Shot shape</th><th style="width:30%">Notes</th></tr>'
             + "".join(f"<tr style='height:23pt'><td>{c}</td>" + "<td></td>" * 4 + "</tr>" for c in ["Driver", "3 wood", "5 wood / hybrid", "4 iron", "5 iron", "6 iron", "7 iron", "8 iron", "9 iron", "Pitching wedge", "Gap wedge", "Sand wedge", "Lob wedge", "Putter", ""]) + '</table>'
             + lab("Equipment notes (grips, balls, fitting)", 4) + '</div>')
    courses = ('<div class="pg"><div class="sub"><h1>Courses Played</h1><span></span></div>' + tbl(["Course", "Where", "Date", "Best score", "Rating", "Notes"], ["24%", "16%", "11%", "11%", "10%", ""], 14, 24)
               + '<div class="lbl">Bucket-list courses</div>' + tbl(["Course", "Where", "Played ✓"], ["32%", "", "12%"], 8, 22) + '</div>')
    goals = ('<div class="pg"><div class="sub"><h1>Season Goals & Stats</h1><span>Season: ________</span></div>' + row(box("Starting handicap", lines(1)), box("Goal handicap", lines(1)), box("Best round", lines(1)))
             + tbl(["Month", "Rounds", "Avg score", "Avg putts", "FIR %", "GIR %", "Handicap"], ["", "11%", "12%", "12%", "11%", "11%", "12%"], 12, 22) + two(lab("Goals", 4), lab("Lessons & tips", 4)) + '</div>')
    return [card, card, card, card, log, prac, clubs, courses] + [goals]

PRODUCTS = [("Camping-Trip-Planner", "#2f9e44", "#ebfbee", camping), ("Game-Night-Score-Sheets", "#e8590c", "#fff4e6", gamenight), ("Year-in-Review-Journal", "#5f3dc4", "#f3f0ff", yearreview),
            ("Period-Cycle-Tracker", "#c2255c", "#fff0f6", cycle), ("Golf-Score-Log-Book", "#0b7285", "#e3fafc", golf)]
