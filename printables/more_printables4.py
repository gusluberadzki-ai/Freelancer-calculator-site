# Round 10 printables. exec()'d by build_round.py, so lines/chks are in scope.
def packing():
    def sect(t, xs, extra=2): return f'<div class="box" style="margin-bottom:6pt"><b>{t}</b>' + "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs) + chks(extra) + '</div>'
    left = sect("Documents & money", ["Passport / ID", "Tickets & bookings", "Travel insurance", "Cards & some cash", "Driving licence"]) + sect("Clothes", ["Tops", "Trousers / shorts", "Underwear & socks", "Pyjamas", "Jacket", "Shoes", "Swimwear"]) + sect("Tech", ["Phone & charger", "Plug adapter", "Headphones", "Power bank"], 1)
    right = sect("Toiletries", ["Toothbrush & paste", "Shampoo & shower gel", "Deodorant", "Sunscreen", "Razor", "Medicines & plasters", "Glasses / contacts"]) + sect("Hand luggage", ["Water bottle", "Snacks", "Book / Kindle", "Pen", "Travel pillow"]) + sect("Before you leave", ["Water the plants", "Take out the bins", "Lock windows", "Turn off heating", "Set out-of-office"], 1)
    p1 = ('<div class="pg"><div class="sub"><h1>Packing List</h1><span>Trip: ______________  Dates: __________</span></div><div class="cols" style="flex:1"><div class="grow">' + left + '</div><div class="grow">' + right + '</div></div></div>')
    days = "".join(f'<div class="box" style="margin-bottom:5pt;flex:1"><b>Day {i}</b>  <span class="small">Date ________  Where ______________</span>' + lines(3) + '</div>' for i in range(1, 7))
    p2 = ('<div class="pg"><div class="sub"><h1>Trip Itinerary</h1><span>Destination: ______________</span></div><div class="cols"><div><div class="lbl">Flights / trains</div>' + lines(3) + '</div><div><div class="lbl">Where we\'re staying</div>' + lines(3) + '</div></div>'
          '<div class="grow" style="margin-top:6pt">' + days + '</div></div>')
    p3 = ('<div class="pg"><div class="sub"><h1>Travel Budget</h1><span>Currency: ________</span></div><table><tr><th style="width:14%">Date</th><th>What</th><th style="width:18%">Category</th><th style="width:15%">Cost</th></tr>'
          + "<tr style='height:22pt'><td></td><td></td><td></td><td></td></tr>" * 24 + '</table><div class="cols" style="margin-top:6pt"><div class="box"><b>Budget</b>' + lines(1) + '</div><div class="box"><b>Spent</b>' + lines(1) + '</div><div class="box"><b>Left</b>' + lines(1) + '</div></div></div>')
    return [p1, p2, p3]
def homemaint():
    seasons = [("Spring", ["Clean gutters & downpipes", "Check roof for loose tiles", "Service air-con / fans", "Wash windows inside & out", "Check outside taps & hoses", "Test smoke & CO alarms"]),
               ("Summer", ["Clean the barbecue", "Check fences & gates", "Treat decking / garden furniture", "Clean extractor fan filters", "Check for damp & mould", "Trim trees & hedges"]),
               ("Autumn", ["Bleed radiators", "Service the boiler", "Sweep the chimney", "Clear leaves from drains", "Check window & door seals", "Store garden furniture"]),
               ("Winter", ["Insulate exposed pipes", "Know where the stopcock is", "Check loft insulation", "Test smoke & CO alarms", "Deep-clean the oven", "Check the fuse box"])]
    boxes = [f'<div class="box" style="margin-bottom:6pt;flex:1"><b>{t}</b>' + "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs) + chks(1) + '</div>' for t, xs in seasons]
    p1 = '<div class="pg"><div class="sub"><h1>Home Maintenance Checklist</h1><span>Year: ________</span></div><div class="cols" style="flex:1"><div class="grow">' + boxes[0] + boxes[1] + '</div><div class="grow">' + boxes[2] + boxes[3] + '</div></div></div>'
    monthly = ["Test smoke alarms", "Clean sink & shower drains", "Check washing machine filter", "Clean dishwasher filter", "Vacuum fridge coils / vents", "Check fire extinguisher"]
    p2 = ('<div class="pg"><div class="sub"><h1>Monthly Jobs</h1><span></span></div>'
          '<table class="dots"><tr><th style="text-align:left">Job</th>' + "".join(f"<th style='text-align:center;width:5.5%'>{m}</th>" for m in ["J","F","M","A","M","J","J","A","S","O","N","D"]) + '</tr>'
          + "".join(f"<tr style='height:26pt'><td style='text-align:left'>{j}</td>" + "<td></td>" * 12 + "</tr>" for j in monthly + [""] * 6) + '</table>'
          '<div class="lbl">Useful numbers</div><table><tr><th>Who</th><th style="width:30%">Phone</th><th style="width:25%">Last used</th></tr>' + "".join(f"<tr style='height:22pt'><td>{w}</td><td></td><td></td></tr>" for w in ["Plumber", "Electrician", "Boiler / heating engineer", "Roofer", "Handyman", "Locksmith", "Home insurance claims line"]) + '</table></div>')
    p3 = ('<div class="pg"><div class="sub"><h1>Repairs & Improvements Log</h1><span></span></div><table><tr><th style="width:13%">Date</th><th>Job</th><th style="width:22%">Done by</th><th style="width:13%">Cost</th><th style="width:14%">Warranty to</th></tr>'
          + "<tr style='height:24pt'><td></td><td></td><td></td><td></td><td></td></tr>" * 26 + '</table></div>')
    return [p1, p2, p3]
def lesson():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    head = "".join(f"<th style='text-align:center'>{d}</th>" for d in days)
    p1 = ('<div class="pg"><div class="sub"><h1>Weekly Lesson Plan</h1><span>Week of: ______________  Class: ________</span></div>'
          f'<table><tr><th style="width:11%">Period</th>{head}</tr>' + "".join(f"<tr style='height:62pt'><td style='vertical-align:top;padding-top:3pt'><b>{p}</b><br><span class='small'>____</span></td>" + "<td></td>" * 5 + "</tr>" for p in range(1, 9)) + '</table>'
          '<div class="cols" style="margin-top:6pt"><div class="box"><b>To prepare / photocopy</b>' + chks(3) + '</div><div class="box"><b>Notes & reminders</b>' + lines(3) + '</div></div></div>')
    p2 = ('<div class="pg"><div class="sub"><h1>Lesson Plan</h1><span>Date: __________  Class: ______</span></div><div class="cols"><div><div class="lbl">Subject / topic</div>' + lines(1) + '</div><div><div class="lbl">Duration</div>' + lines(1) + '</div></div>'
          '<div class="lbl">Learning objectives (by the end, students will be able to…)</div>' + lines(3) + '<div class="cols"><div><div class="lbl">Materials & resources</div>' + chks(5) + '</div><div><div class="lbl">Key vocabulary</div>' + lines(5) + '</div></div>'
          '<table style="margin-top:8pt"><tr><th style="width:16%">Time</th><th style="width:22%">Stage</th><th>Activity</th></tr>' + "".join(f"<tr style='height:40pt'><td></td><td>{s}</td><td></td></tr>" for s in ["Starter", "Teach / model", "Practice", "Independent work", "Plenary"]) + '</table>'
          '<div class="cols"><div><div class="lbl">Differentiation / support</div>' + lines(3) + '</div><div><div class="lbl">Reflection: what went well, what next?</div>' + lines(3) + '</div></div></div>')
    p3 = ('<div class="pg"><div class="sub"><h1>Class Record</h1><span>Class: ______  Term: ______</span></div><table><tr><th style="width:4%">#</th><th style="width:28%">Student</th>' + "<th></th>" * 10 + '</tr>'
          + "".join(f"<tr style='height:21pt'><td>{i}</td><td></td>" + "<td></td>" * 10 + "</tr>" for i in range(1, 31)) + '</table></div>')
    return [p1, p2, p3]
def cornell():
    p1 = ('<div class="pg"><div class="sub"><h1>Cornell Notes</h1><span>Subject: __________  Date: ________</span></div><div class="lbl">Topic</div>' + lines(1) +
          '<div style="display:flex;flex:1;margin-top:6pt;border-top:1pt solid var(--c)"><div style="width:30%;border-right:1pt solid var(--c);padding-right:6pt"><div class="lbl">Cues · questions · key words</div>' + lines(26) + '</div>'
          '<div style="flex:1;padding-left:8pt"><div class="lbl">Notes</div>' + lines(26) + '</div></div><div style="border-top:1pt solid var(--c)"><div class="lbl">Summary (in your own words)</div>' + lines(4) + '</div></div>')
    topics = "".join("<tr style='height:21pt'><td></td><td></td>" + "<td style='text-align:center;color:#bbb'>● ● ●</td>" + "<td></td><td></td></tr>" for _ in range(28))
    p2 = ('<div class="pg"><div class="sub"><h1>Revision Tracker</h1><span>Subject: __________  Exam: ________</span></div><div class="small">Colour the dots: red = don\'t know it, amber = getting there, green = confident.</div>'
          f'<table><tr><th>Topic</th><th style="width:14%">Notes made</th><th style="width:16%">Confidence</th><th style="width:14%">Revised</th><th style="width:14%">Practice Q</th></tr>{topics}</table></div>')
    p3 = ('<div class="pg"><div class="sub"><h1>Exam Countdown</h1><span></span></div><table><tr><th style="width:24%">Subject</th><th style="width:16%">Paper</th><th style="width:16%">Date</th><th style="width:12%">Time</th><th style="width:16%">Room</th><th>Days to go</th></tr>'
          + "<tr style='height:24pt'><td></td><td></td><td></td><td></td><td></td><td></td></tr>" * 12 + '</table>'
          '<div class="lbl">Weekly revision timetable</div><table><tr><th style="width:12%"></th>' + "".join(f"<th style='text-align:center'>{d}</th>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) + '</tr>'
          + "".join(f"<tr style='height:30pt'><td>{s}</td>" + "<td></td>" * 7 + "</tr>" for s in ["Morning", "Afternoon", "Evening"]) + '</table><div class="lbl">Goals this week</div>' + chks(4) + '</div>')
    return [p1, p2, p3]
def orders():
    p1 = ('<div class="pg"><div class="sub"><h1>Order Tracker</h1><span>Month: ______________</span></div><table><tr><th style="width:10%">Date</th><th style="width:11%">Order #</th><th style="width:19%">Customer</th><th>Item(s)</th><th style="width:9%">Total</th><th style="width:7%">Paid</th><th style="width:8%">Made</th><th style="width:8%">Sent</th></tr>'
          + "<tr style='height:23pt'>" + "<td></td>" * 8 + "</tr>" + ("<tr style='height:23pt'>" + "<td></td>" * 8 + "</tr>") * 25 + '</table>'
          '<div class="cols" style="margin-top:6pt"><div class="box"><b>Orders this month</b>' + lines(1) + '</div><div class="box"><b>Sales total</b>' + lines(1) + '</div><div class="box"><b>Best seller</b>' + lines(1) + '</div></div></div>')
    form = ('<div class="box" style="flex:1;margin-bottom:8pt;display:flex;flex-direction:column"><div style="display:flex;justify-content:space-between"><b style="color:var(--c);font-size:13pt">Order form</b><span class="small">Order # ______  Date ________</span></div>'
            '<div class="cols"><div><div class="lbl">Customer</div>' + lines(1) + '<div class="lbl">Phone / email</div>' + lines(1) + '</div><div><div class="lbl">Delivery address</div>' + lines(2) + '</div></div>'
            '<table style="margin-top:4pt"><tr><th>Item & personalisation</th><th style="width:10%">Qty</th><th style="width:15%">Price</th><th style="width:15%">Total</th></tr>' + "<tr><td></td><td></td><td></td><td></td></tr>" * 4 + '</table>'
            '<div style="display:flex;justify-content:space-between;margin-top:4pt" class="small"><span>Paid: ☐ cash ☐ card ☐ transfer   Due by: ________</span><b>Total: ________</b></div></div>')
    p2 = '<div class="pg"><div class="sub"><h1>Customer Order Forms</h1><span class="small">2 per page · cut along the box</span></div><div class="grow">' + form * 2 + '</div></div>'
    p3 = ('<div class="pg"><div class="sub"><h1>Customer Log</h1><span></span></div><table><tr><th style="width:22%">Name</th><th style="width:24%">Contact</th><th>Bought / preferences</th><th style="width:12%">Orders</th><th style="width:12%">Review?</th></tr>'
          + "<tr style='height:24pt'><td></td><td></td><td></td><td></td><td></td></tr>" * 26 + '</table></div>')
    return [p1, p2, p3]
PRODUCTS = [("Travel-Packing-List", "#0c8599", "#e3f6f8", packing), ("Home-Maintenance-Checklist", "#5c7cfa", "#edf1ff", homemaint), ("Teacher-Lesson-Planner", "#c2255c", "#fbe9f0", lesson),
            ("Cornell-Notes-Study-Pack", "#495057", "#f1f3f5", cornell), ("Small-Business-Order-Tracker", "#9c36b5", "#f6eafa", orders)]
