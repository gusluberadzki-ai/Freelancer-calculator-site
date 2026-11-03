# Round 6 printables. exec()'d by build.py, so lines/chks/PRODUCTS are in scope.
import calendar as _cal
def budget():
    def sec(t, n, cols=("Item", "Budget", "Actual")):
        return (f'<div class="lbl">{t}</div><table><tr>' + "".join(f"<th{' style=\"width:22%\"' if i else ''}>{c}</th>" for i, c in enumerate(cols)) + "</tr>"
                + ("<tr>" + "<td></td>" * len(cols) + "</tr>") * n + f'<tr><th>Total</th>' + "<th></th>" * (len(cols) - 1) + "</tr></table>")
    p1 = ('<div class="pg"><div class="sub"><h1>Monthly Budget</h1><span>Month: ______________</span></div>'
          '<div class="cols"><div>' + sec("Income", 4) + sec("Fixed bills", 9) + sec("Savings", 4) + '</div><div>' + sec("Variable spending", 10) + sec("Debt payments", 5) +
          '<div class="lbl">Summary</div><table><tr><td>Total income</td><td style="width:30%"></td></tr><tr><td>Total spending</td><td></td></tr><tr><td>Savings + debt</td><td></td></tr><tr><th>Left over</th><th></th></tr></table></div></div>'
          '<div class="lbl">Notes</div>' + lines(3) + '</div>')
    p2 = ('<div class="pg"><div class="sub"><h1>Expense Tracker</h1><span>Month: ______________</span></div><table><tr><th style="width:12%">Date</th><th>Description</th><th style="width:20%">Category</th><th style="width:15%">Amount</th></tr>'
          + "<tr><td></td><td></td><td></td><td></td></tr>" * 32 + '<tr><th colspan="3">Total</th><th></th></tr></table></div>')
    return [p1, p2]
def meals():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    t = "<table><tr><th style='width:9%'></th><th>Breakfast</th><th>Lunch</th><th>Dinner</th><th style='width:16%'>Snacks</th></tr>" + "".join(f"<tr style='height:38pt'><th>{d}</th><td></td><td></td><td></td><td></td></tr>" for d in days) + "</table>"
    g = "".join(f'<div class="box" style="flex:1"><b>{a}</b>' + chks(7) + '</div>' for a in ["Fruit & veg", "Meat & fish", "Dairy & eggs"])
    g2 = "".join(f'<div class="box" style="flex:1"><b>{a}</b>' + chks(7) + '</div>' for a in ["Pantry", "Frozen", "Other"])
    return ['<div class="pg"><div class="sub"><h1>Meal Planner</h1><span>Week of: ______________</span></div>' + t +
            '<div class="lbl">Grocery list</div><div class="cols">' + g + '</div><div class="cols" style="margin-top:6pt">' + g2 + '</div></div>']
def cleaning():
    def blk(t, items, n=4):
        return f'<div class="box" style="margin-bottom:6pt"><b>{t}</b>' + "".join(f'<div class="chk"><i></i>{x}</div>' for x in items) + chks(n) + '</div>'
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    daily = "<table><tr><th>Daily</th>" + "".join(f"<th style='width:8%;text-align:center'>{d}</th>" for d in days) + "</tr>" + "".join(f"<tr><td>{x}</td>" + "<td></td>" * 7 + "</tr>" for x in ["Make beds", "Wash dishes", "Wipe kitchen counters", "Quick tidy", "Sweep kitchen floor", "Laundry (1 load)", "Wipe bathroom sink", "", "", ""]) + "</table>"
    return ['<div class="pg"><div class="sub"><h1>Cleaning Schedule</h1><span>Week of: ______________</span></div>' + daily +
            '<div class="cols" style="margin-top:8pt"><div>' + blk("Weekly", ["Vacuum all rooms", "Mop floors", "Clean bathrooms", "Change bedding", "Dust surfaces", "Empty bins", "Water plants", "Clean mirrors"], 4) + '</div><div>' +
            blk("Monthly", ["Clean oven & microwave", "Wipe skirting boards", "Clean windows", "Wash bins", "Clean fridge", "Descale kettle", "Wash pillows"], 4) + '</div></div>'
            '<div class="cols"><div>' + blk("Seasonal", ["Declutter wardrobe", "Wash curtains", "Clean under furniture", "Clean gutters", "Deep-clean carpets"], 2) + '</div><div><div class="lbl">Notes</div>' + lines(10) + '</div></div></div>']
def gratitude():
    pg = ('<div class="pg"><div class="sub"><h1>Gratitude Journal</h1><span>Date: ______________</span></div>'
          + "".join(f'<div class="box" style="margin-bottom:8pt;flex:1"><div class="lbl" style="margin-top:0">{q}</div>' + lines(n) + '</div>' for q, n in [("Morning · Today I am grateful for", 3), ("Morning · What would make today great?", 3), ("Morning · Daily affirmation: I am…", 1), ("Evening · Three good things that happened today", 3), ("Evening · How could today have been even better?", 2)])
          + '<div class="small" style="text-align:center">Mood:  😞  😐  🙂  😊  😄</div></div>')
    return [pg, pg, pg, pg]
def goals():
    p1 = ('<div class="pg"><div class="sub"><h1>Goal Planner</h1><span>Goal #___</span></div><div class="lbl">My goal (specific & measurable)</div>' + lines(2) +
          '<div class="cols"><div><div class="lbl">Why it matters to me</div>' + lines(4) + '</div><div><div class="lbl">Deadline</div>' + lines(1) + '<div class="lbl">How I\'ll measure it</div>' + lines(2) + '</div></div>'
          '<div class="lbl">Action steps</div><table><tr><th style="width:6%">#</th><th>Step</th><th style="width:18%">By when</th><th style="width:10%">Done</th></tr>' + "".join(f"<tr><td>{i}</td><td></td><td></td><td></td></tr>" for i in range(1, 16)) + '</table>'
          '<div class="cols"><div><div class="lbl">Possible obstacles</div>' + lines(6) + '</div><div><div class="lbl">How I\'ll overcome them</div>' + lines(6) + '</div></div>'
          '<div class="cols"><div><div class="lbl">Who can help</div>' + lines(4) + '</div><div><div class="lbl">Reward when I reach it</div>' + lines(4) + '</div></div></div>')
    p2 = ('<div class="pg"><div class="sub"><h1>Monthly Goal Review</h1><span>Month: ______________</span></div><div class="lbl">Top 3 goals this month</div>' + chks(3) +
          '<div class="lbl">Progress</div><table><tr><th>Goal</th><th style="width:14%;text-align:center">Wk 1</th><th style="width:14%;text-align:center">Wk 2</th><th style="width:14%;text-align:center">Wk 3</th><th style="width:14%;text-align:center">Wk 4</th></tr>' + "<tr style='height:30pt'><td></td><td></td><td></td><td></td><td></td></tr>" * 5 + '</table>'
          '<div class="cols"><div><div class="lbl">Wins</div>' + lines(10) + '</div><div><div class="lbl">Lessons</div>' + lines(10) + '</div></div><div class="lbl">Focus for next month</div>' + lines(6) + '<div class="lbl">Habits to keep / start / stop</div>' + lines(5) + '</div>')
    return [p1, p2]
def bills():
    mh = "".join(f"<th style='width:5.8%;text-align:center;padding:0'>{m}</th>" for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    return ['<div class="pg"><div class="sub"><h1>Bill Tracker</h1><span>Year: ________</span></div><div class="small">Tick each month when the bill is paid.</div>'
            f'<table class="dots"><tr><th style="text-align:left">Bill</th><th style="width:8%">Due day</th><th style="width:9%">Amount</th>{mh}</tr>'
            + ("<tr style='height:24pt'><td></td><td></td><td></td>" + "<td></td>" * 12 + "</tr>") * 24 + '</table><div class="lbl">Notes</div>' + lines(3) + '</div>']
def calendar27():
    pages = []
    for m in range(1, 13):
        weeks = _cal.Calendar(0).monthdayscalendar(2027, m)
        rows = "".join("<tr>" + "".join(f"<td style='vertical-align:top;padding:3pt 4pt;height:{int(560/len(weeks))}pt'>{d or ''}</td>" for d in w) + "</tr>" for w in weeks)
        pages.append(f'<div class="pg"><div class="sub"><h1>{_cal.month_name[m]}</h1><span style="font-size:18pt;color:var(--c);font-weight:700">2027</span></div>'
                     '<table style="table-layout:fixed"><tr>' + "".join(f"<th style='text-align:center'>{d}</th>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) + f'</tr>{rows}</table>'
                     '<div class="lbl">Notes</div>' + lines(3) + '</div>')
    return pages
PRODUCTS += [("Monthly-Budget-Planner", "#0b7285", "#e3f6f8", budget), ("Meal-Planner-Printable", "#e8590c", "#fff0e6", meals), ("Cleaning-Schedule", "#1098ad", "#e5f7fa", cleaning),
             ("Gratitude-Journal", "#c2255c", "#fbe9f0", gratitude), ("Goal-Planner", "#364fc7", "#e9edfc", goals), ("Bill-Tracker", "#2f9e44", "#e7f6ea", bills), ("2027-Monthly-Calendar", "#495057", "#eef0f2", calendar27)]
