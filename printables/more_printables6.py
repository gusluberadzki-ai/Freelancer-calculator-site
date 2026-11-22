# Round 12 printables. exec()'d by build_round.py, so lines/chks are in scope.
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def tbl(heads, widths, n, h=22):
    return ('<table><tr>' + "".join(f"<th style='width:{w}'>{x}</th>" if w else f"<th>{x}</th>" for x, w in zip(heads, widths)) + '</tr>'
            + (f"<tr style='height:{h}pt'>" + "<td></td>" * len(heads) + "</tr>") * n + '</table>')
def box(t, body, flex=1): return f'<div class="box" style="flex:{flex};margin-bottom:5pt"><b>{t}</b>{body}</div>'
def items(xs): return "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs)
def summer():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    p1 = ('<div class="pg"><div class="sub"><h1>Holiday Week Planner</h1><span>Week of: ______________</span></div>'
          '<table><tr><th style="width:12%"></th>' + "".join(f"<th style='text-align:center'>{d}</th>" for d in days) + '</tr>'
          + "".join(f"<tr style='height:70pt'><td><b>{p}</b></td>" + "<td></td>" * 7 + "</tr>" for p in ["Morning", "Lunch", "Afternoon", "Evening"]) + '</table>'
          '<div class="cols" style="margin-top:6pt">' + box("Days out booked", lines(3)) + box("Childcare / who's in charge", lines(3)) + box("Packed lunch ideas", lines(3)) + '</div></div>')
    ideas = [("Outdoors", ["Picnic in the park", "Nature scavenger hunt", "Bike ride", "Build a den", "Pond dipping", "Stargazing"]), ("Rainy day", ["Board game marathon", "Bake cookies", "Build a blanket fort", "Craft afternoon", "Indoor treasure hunt", "Film & popcorn"]),
             ("Free & cheap", ["Library visit", "Splash park", "Chalk drawings", "Car boot sale hunt", "Free museum", "Family sports day"]), ("Big days out", ["Theme park", "Beach day", "Zoo / farm", "Camping night", "Swimming pool", "Visit family"])]
    p2 = ('<div class="pg"><div class="sub"><h1>Summer Bucket List</h1><span>Tick them off together</span></div><div class="cols" style="flex:1"><div class="grow">' + "".join(box(t, items(xs) + chks(2)) for t, xs in ideas[:2])
          + '</div><div class="grow">' + "".join(box(t, items(xs) + chks(2)) for t, xs in ideas[2:]) + '</div></div></div>')
    p3 = ('<div class="pg"><div class="sub"><h1>My Summer Journal</h1><span>Name: ______________</span></div><div class="box" style="height:210pt"><b>Draw the best thing I did</b></div>'
          '<div class="lbl">What happened</div>' + lines(6) + '<div class="cols"><div><div class="lbl">Best food</div>' + lines(2) + '</div><div><div class="lbl">Funniest moment</div>' + lines(2) + '</div></div>'
          '<div class="lbl">Rate today</div><div style="font-size:22pt;color:#ccc">☆ ☆ ☆ ☆ ☆</div></div>')
    rd = "".join("<tr>" + "<td style='height:42pt;text-align:center;color:#ddd;font-size:18pt'>📖</td>" * 6 + "</tr>" for _ in range(5))
    p4 = ('<div class="pg"><div class="sub"><h1>Summer Reading Challenge</h1><span>Name: ______________</span></div><div class="small">Colour a book for every 20 minutes of reading.</div>'
          f'<table style="margin-top:6pt">{rd}</table><div class="lbl">Books I read</div>' + tbl(["Title", "Author", "Stars"], ["", "30%", "16%"], 10) + '</div>')
    return [p1, p2, p3, p4]
def bucket():
    def page(o):
        col = lambda a, b: "".join(f'<div class="chk" style="margin:3.5pt 0"><b style="width:18pt;color:var(--c)">{i}</b><i></i><span style="flex:1;border-bottom:.6pt solid #ccc;height:12pt"></span></div>' for i in range(a, b))
        return f'<div class="pg"><div class="sub"><h1>My Bucket List</h1><span>{o + 1} - {o + 50}</span></div><div class="cols" style="flex:1"><div>' + col(o + 1, o + 26) + '</div><div>' + col(o + 26, o + 51) + '</div></div></div>'
    p1, p2 = page(0), page(50)
    cats = ["Travel", "Adventure", "Learn", "Create", "Give back", "Food & drink"]
    p3 = '<div class="pg"><div class="sub"><h1>Ideas by Category</h1><span></span></div><div class="cols" style="flex:1">' + "".join('<div class="grow">' + "".join(box(c, lines(6)) for c in cats[i::2]) + '</div>' for i in range(2)) + '</div></div>'
    one = ('<div class="pg"><div class="sub"><h1>Bucket List Memory</h1><span>Done on: ______________</span></div><div class="lbl">What I did</div>' + lines(1) + '<div class="cols"><div><div class="lbl">Where</div>' + lines(1) + '</div><div><div class="lbl">Who with</div>' + lines(1) + '</div></div>'
           '<div class="box" style="height:230pt;margin-top:8pt"><b>Photo / ticket / sketch</b></div><div class="lbl">How it felt</div>' + lines(5) + '<div class="lbl">What I\'d tell someone about to do it</div>' + lines(3) + '</div>')
    plan = ('<div class="pg"><div class="sub"><h1>Make It Happen</h1><span>Goal #____</span></div><div class="lbl">The dream</div>' + lines(2) + '<div class="cols"><div><div class="lbl">Target date</div>' + lines(1) + '</div><div><div class="lbl">Budget</div>' + lines(1) + '</div></div>'
            '<div class="lbl">Steps</div>' + tbl(["Step", "By when", "✓"], ["", "18%", "7%"], 10, 24) + '<div class="cols"><div><div class="lbl">What could stop me</div>' + lines(3) + '</div><div><div class="lbl">How I\'ll get round it</div>' + lines(3) + '</div></div>'
            '<div class="lbl">Savings tracker</div><div style="display:flex;flex-wrap:wrap">' + "".join(f'<span style="display:inline-block;width:9.4%;height:22pt;border:1pt solid #ccc;margin:1pt;border-radius:4pt"></span>' for _ in range(20)) + '</div></div>')
    return [p1, p2, p3, plan, one, one]
def baby():
    firsts = ["First smile", "First laugh", "Rolled over", "Sat up alone", "First tooth", "First solid food", "Crawled", "First word", "Pulled to stand", "First steps", "Waved bye-bye", "First haircut", "Slept through the night", "First holiday", "First birthday", ""]
    p1 = ('<div class="pg"><div class="sub"><h1>Baby\'s Firsts</h1><span>Name: ______________</span></div>'
          + tbl(["Milestone", "Date", "Age", "Notes"], ["28%", "14%", "11%", ""], 0) .replace("</table>", "")
          + "".join(f"<tr style='height:30pt'><td><b>{f}</b></td><td></td><td></td><td></td></tr>" for f in firsts) + '</table></div>')
    p2 = ('<div class="pg"><div class="sub"><h1>All About Me</h1><span>Born: ______________</span></div><div class="cols"><div class="box" style="flex:1.2;height:200pt"><b>My first photo</b></div><div style="flex:1">'
          + "".join(f'<div class="lbl">{t}</div>' + lines(1) for t in ["Time", "Weight", "Length", "Hospital / place", "Hair & eyes"]) + '</div></div>'
          '<div class="cols"><div><div class="lbl">My name means</div>' + lines(2) + '</div><div><div class="lbl">Who came to visit first</div>' + lines(2) + '</div></div>'
          '<div class="cols"><div><div class="lbl">In the news that day</div>' + lines(3) + '</div><div><div class="lbl">Number 1 song</div>' + lines(1) + '<div class="lbl">Price of milk</div>' + lines(1) + '</div></div>'
          '<div class="lbl">A note from mum & dad</div>' + lines(5) + '</div>')
    month = lambda m: box(f"Month {m}", '<div class="small">Weight ____  Length ____</div>' + lines(3))
    p3 = '<div class="pg"><div class="sub"><h1>Month by Month</h1><span>Months 1-6</span></div><div class="cols" style="flex:1"><div class="grow">' + "".join(month(m) for m in (1, 2, 3)) + '</div><div class="grow">' + "".join(month(m) for m in (4, 5, 6)) + '</div></div></div>'
    p4 = p3.replace("Months 1-6", "Months 7-12")
    for m in range(6, 0, -1): p4 = p4.replace(f"<b>Month {m}</b>", f"<b>Month {m + 6}</b>")
    p5 = ('<div class="pg"><div class="sub"><h1>Growth & Health</h1><span></span></div><div class="lbl">Growth record</div>' + tbl(["Date", "Age", "Weight", "Length", "Head", "Notes"], ["14%", "10%", "12%", "12%", "11%", ""], 12)
          + '<div class="lbl">Vaccinations & check-ups</div>' + tbl(["Date", "Vaccine / check-up", "Given by", "Notes"], ["14%", "", "22%", "26%"], 12) + '</div>')
    p6 = ('<div class="pg"><div class="sub"><h1>My First Birthday</h1><span>Date: ______________</span></div><div class="box" style="height:220pt"><b>Party photo</b></div><div class="cols">'
          + "".join(f'<div><div class="lbl">{t}</div>' + lines(2) + '</div>' for t in ["Who came", "My cake"]) + '</div><div class="cols">' + "".join(f'<div><div class="lbl">{t}</div>' + lines(2) + '</div>' for t in ["Favourite toy", "Favourite food"]) + '</div>'
          '<div class="cols">' + "".join(f'<div><div class="lbl">{t}</div>' + lines(2) + '</div>' for t in ["Words I can say", "Things I love to do"]) + '</div><div class="lbl">Wishes for my second year</div>' + lines(4) + '</div>')
    return [p2, p1, p3, p4, p5, p6]
def bizplan():
    p1 = ('<div class="pg"><div class="sub"><h1>One-Page Business Plan</h1><span>Year: ________</span></div><div class="cols"><div><div class="lbl">Business name</div>' + lines(1) + '</div><div><div class="lbl">Tagline</div>' + lines(1) + '</div></div>'
          '<div class="cols">' + box("What I sell", lines(4)) + box("Who buys it (ideal customer)", lines(4)) + '</div><div class="cols">' + box("Why they choose me", lines(4)) + box("Where I sell", lines(4)) + '</div>'
          '<div class="cols">' + box("Prices", lines(4)) + box("Costs", lines(4)) + '</div><div class="lbl">Big goals this year</div>' + items(["Revenue: ______________", "Customers: ______________", "Launch: ______________"]) + chks(2) + '</div>')
    q = lambda n: box(f"Quarter {n}", '<div class="small">Focus</div>' + lines(1) + '<div class="small">Goals</div>' + chks(4) + '<div class="small">Revenue target ______  Actual ______</div>')
    p2 = '<div class="pg"><div class="sub"><h1>Quarterly Goals</h1><span>Year: ________</span></div><div class="cols" style="flex:1"><div class="grow">' + q(1) + q(2) + '</div><div class="grow">' + q(3) + q(4) + '</div></div></div>'
    p3 = ('<div class="pg"><div class="sub"><h1>Monthly Business Review</h1><span>Month: ______________</span></div><div class="cols">' + box("Revenue", lines(1)) + box("Expenses", lines(1)) + box("Profit", lines(1)) + box("Orders", lines(1)) + '</div>'
          '<div class="cols"><div><div class="lbl">Wins this month</div>' + lines(4) + '</div><div><div class="lbl">What didn\'t work</div>' + lines(4) + '</div></div>'
          '<div class="cols"><div><div class="lbl">Best-selling products</div>' + lines(3) + '</div><div><div class="lbl">Marketing I did</div>' + lines(3) + '</div></div>'
          '<div class="lbl">Top 3 priorities next month</div>' + chks(3) + '<div class="lbl">Ideas to try</div>' + lines(3) + '</div>')
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    p4 = ('<div class="pg"><div class="sub"><h1>Marketing Planner</h1><span>Week of: ______________</span></div><table><tr><th style="width:11%"></th>' + "".join(f"<th>{d}</th>" for d in days) + '</tr>'
          + "".join(f"<tr style='height:52pt'><td><b>{p}</b></td>" + "<td></td>" * 7 + "</tr>" for p in ["Instagram", "TikTok", "Email", "Website / blog", "Other"]) + '</table>'
          '<div class="cols" style="margin-top:6pt">' + box("Content ideas", lines(5)) + box("Hashtags & keywords", lines(5)) + '</div></div>')
    p5 = ('<div class="pg"><div class="sub"><h1>Income & Expenses</h1><span>Month: ______________</span></div><div class="cols"><div><div class="lbl">Income</div>' + tbl(["Date", "From", "Amount"], ["20%", "", "24%"], 26, 20)
          + '</div><div><div class="lbl">Expenses</div>' + tbl(["Date", "For", "Amount"], ["20%", "", "24%"], 26, 20) + '</div></div><div class="cols">' + box("Total income", lines(1)) + box("Total expenses", lines(1)) + box("Profit", lines(1)) + '</div></div>')
    return [p1, p2, p3, p4, p5]
def language():
    p1 = ('<div class="pg"><div class="sub"><h1>Language Learning Plan</h1><span>Language: ______________</span></div><div class="cols"><div><div class="lbl">Why I\'m learning</div>' + lines(3) + '</div><div><div class="lbl">My level now → goal</div>' + lines(3) + '</div></div>'
          '<div class="cols">' + box("Apps & courses", lines(4)) + box("Books, shows & podcasts", lines(4)) + '</div><div class="lbl">Goals</div>' + tbl(["Goal", "By when", "✓"], ["", "18%", "7%"], 6, 24)
          + '<div class="lbl">Study streak · colour a box each day you practise</div><div style="display:flex;flex-wrap:wrap">' + "".join(f'<span style="display:inline-block;width:6.2%;height:18pt;border:1pt solid #ccc;margin:1pt;border-radius:3pt;font-size:6pt;color:#bbb;text-align:right;padding-right:2pt">{i}</span>' for i in range(1, 61)) + '</div></div>')
    p2 = ('<div class="pg"><div class="sub"><h1>Vocabulary</h1><span>Topic: ______________</span></div><table><tr><th>Word / phrase</th><th style="width:30%">Meaning</th><th style="width:30%">Example sentence</th><th style="width:7%">✓</th></tr>'
          + "<tr style='height:22pt'><td></td><td></td><td></td><td></td></tr>" * 30 + '</table></div>')
    p3 = ('<div class="pg"><div class="sub"><h1>Grammar Notes</h1><span>Topic: ______________</span></div><div class="lbl">The rule</div>' + lines(4) + '<div class="box" style="height:170pt;margin-top:6pt"><b>Table / conjugation</b></div>'
          '<div class="lbl">Examples</div>' + lines(5) + '<div class="lbl">Exceptions & mistakes I make</div>' + lines(4) + '</div>')
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    p4 = ('<div class="pg"><div class="sub"><h1>Weekly Practice Log</h1><span>Week of: ______________</span></div><table class="dots"><tr><th style="text-align:left">Skill</th>' + "".join(f"<th style='text-align:center;width:9%'>{d}</th>" for d in days) + '<th style="width:9%">Mins</th></tr>'
          + "".join(f"<tr style='height:30pt'><td>{s}</td>" + "<td></td>" * 8 + "</tr>" for s in ["Vocabulary", "Grammar", "Listening", "Reading", "Speaking", "Writing", "App lesson", ""]) + '</table>'
          '<div class="cols"><div><div class="lbl">New words this week</div>' + lines(6) + '</div><div><div class="lbl">Phrases to use</div>' + lines(6) + '</div></div>'
          '<div class="lbl">What I can do now that I couldn\'t last week</div>' + lines(2) + '</div>')
    p5 = ('<div class="pg"><div class="sub"><h1>Conversation Prep</h1><span>Date: __________  With: __________</span></div><div class="lbl">Topics to talk about</div>' + chks(4)
          + '<div class="cols"><div><div class="lbl">Useful phrases</div>' + lines(8) + '</div><div><div class="lbl">Questions to ask</div>' + lines(8) + '</div></div>'
          '<div class="lbl">New words I heard</div>' + tbl(["Word", "Meaning"], ["", "50%"], 6) + '<div class="lbl">How it went · what to work on</div>' + lines(3) + '</div>')
    return [p1, p2, p2, p3, p4, p5]
PRODUCTS = [("Kids-Summer-Holiday-Planner", "#f59f00", "#fff9db", summer), ("Bucket-List-Journal", "#0b7285", "#e3fafc", bucket), ("Baby-First-Year-Milestones", "#4dabf7", "#e7f5ff", baby),
            ("Small-Business-Planner", "#2b8a3e", "#ebfbee", bizplan), ("Language-Learning-Journal", "#c2255c", "#fff0f6", language)]
