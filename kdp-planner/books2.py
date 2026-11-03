"""Round 6 KDP low-content books. Run: python3 books2.py (reuses render() from books.py)"""
import pathlib
_src = (pathlib.Path(__file__).parent / "books.py").read_text()
exec(_src[:_src.index("# 1. Password log book")])

def title_page(t, sub, owner="This book belongs to"):
    return [f'<div class="pg center"><h1>{t}</h1><p style="color:#555;margin-top:10pt">{sub}</p><p style="margin-top:60pt">{owner}</p>{lines(1)}</div>',
            '<div class="pg center"><p style="color:#999">This page is intentionally left blank.</p></div>']
NOTES = '<div class="pg"><h2>Notes</h2>' + lines(24) + '</div>'
LOG = []

# 1. Mileage log book (popular for tax records)
P = title_page("Mileage Log Book", "Vehicle mileage record for business, tax and expenses")
P.append('<div class="pg"><h2>Vehicle details</h2>' + "".join(f'<div class="lbl">{x}</div>' + lines(1) for x in ["Make & model", "Registration / plate", "Year", "Odometer at start", "Start date", "Insurance policy", "Business name"]) +
         '<div class="lbl" style="margin-top:10pt">How to use</div><p style="font-size:8.5pt;color:#555">Record every business trip: date, purpose, start and end odometer readings and miles. Total each page and carry the total forward. Keep fuel and service receipts on the last pages.</p></div>')
row = "<tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
for i in range(100):
    P.append('<div class="pg"><table><tr><th style="width:12%">Date</th><th>Destination / purpose</th><th style="width:14%">Start</th><th style="width:14%">End</th><th style="width:11%">Miles</th><th style="width:11%">Tolls / parking</th></tr>' + row * 22 +
             '<tr><th colspan="4" style="text-align:right">Page total</th><th></th><th></th></tr><tr><th colspan="4" style="text-align:right">Carried forward</th><th></th><th></th></tr></table></div>')
for t in ("Fuel log", "Service & repairs"):
    for _ in range(3): P.append(f'<div class="pg"><h2>{t}</h2><table><tr><th style="width:14%">Date</th><th>Details</th><th style="width:16%">Odometer</th><th style="width:16%">Cost</th></tr>' + "<tr><td></td><td></td><td></td><td></td></tr>" * 24 + '</table></div>')
P.append('<div class="pg"><h2>Yearly summary</h2><table><tr><th>Month</th><th>Business miles</th><th>Total miles</th><th>Expenses</th></tr>' + "".join(f"<tr><td>{m}</td><td></td><td></td><td></td></tr>" for m in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]) + '<tr><th>Total</th><th></th><th></th><th></th></tr></table></div>')
P += [NOTES] * 2
LOG.append(render("mileage-log-book", "Mileage Log Book", "Vehicle mileage record for business, tax and expenses. 2,200 trip entries.", "RateKit Press", "#1d4e89", "#e5edf7", P,
       '<p style="font-size:16pt;font-weight:700">Every business mile, recorded.</p><p>100 log pages with room for 2,200 trips: date, purpose, odometer readings, miles, tolls and parking, with page totals carried forward.</p><p>Plus vehicle details, fuel and service logs, and a yearly summary for your tax return.</p>'))

# 2. Blood pressure log book
P = title_page("Blood Pressure Log Book", "Daily blood pressure and heart rate tracker")
P.append('<div class="pg"><h2>My details</h2>' + "".join(f'<div class="lbl">{x}</div>' + lines(1) for x in ["Name", "Date of birth", "Doctor", "Doctor phone", "Emergency contact", "Target blood pressure"]) +
         '<div class="lbl">Medications</div><table><tr><th>Medication</th><th>Dose</th><th>When</th></tr>' + "<tr><td></td><td></td><td></td></tr>" * 6 + '</table></div>')
P.append('<div class="pg"><h2>Blood pressure categories (adults)</h2><table><tr><th>Category</th><th>Systolic (top)</th><th></th><th>Diastolic (bottom)</th></tr>'
         '<tr><td>Normal</td><td>under 120</td><td>and</td><td>under 80</td></tr><tr><td>Elevated</td><td>120–129</td><td>and</td><td>under 80</td></tr><tr><td>High, stage 1</td><td>130–139</td><td>or</td><td>80–89</td></tr>'
         '<tr><td>High, stage 2</td><td>140 or higher</td><td>or</td><td>90 or higher</td></tr><tr><td>Seek care urgently</td><td>over 180</td><td>and/or</td><td>over 120</td></tr></table>'
         '<p style="font-size:8pt;color:#555;margin-top:8pt">Source: American Heart Association categories. Always follow your doctor\'s advice. Measure at the same times each day, seated, after 5 minutes of rest.</p></div>')
for i in range(104):
    P.append('<div class="pg"><table><tr><th style="width:14%">Date</th><th style="width:12%">Time</th><th style="width:14%">Systolic</th><th style="width:14%">Diastolic</th><th style="width:12%">Pulse</th><th>Notes</th></tr>' + "<tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>" * 24 + '</table></div>')
P += [NOTES] * 3
LOG.append(render("blood-pressure-log-book", "Blood Pressure Log Book", "Daily tracker for blood pressure and heart rate, with 2,400 readings", "RateKit Press", "#b02a37", "#fbe7e9", P,
       '<p style="font-size:16pt;font-weight:700">Track your readings. Share them with your doctor.</p><p>104 log pages with room for about 2,500 readings: date, time, systolic, diastolic, pulse and notes.</p><p>Plus your details, a medication list and a blood pressure category chart. Large, easy-to-read layout.</p>'))

# 3. Recipe book
P = title_page("My Recipe Book", "Blank cookbook to write in your favourite recipes")
P.append('<div class="pg"><h2>Contents</h2><table><tr><th style="width:12%">Page</th><th>Recipe</th></tr>' + "".join(f"<tr><td>{i}</td><td></td></tr>" for i in range(1, 26)) + '</table></div>')
P.append('<div class="pg"><h2>Contents</h2><table><tr><th style="width:12%">Page</th><th>Recipe</th></tr>' + "".join(f"<tr><td>{i}</td><td></td></tr>" for i in range(26, 51)) + '</table></div>')
P.append('<div class="pg"><h2>Kitchen conversions</h2><table><tr><th>US</th><th>Metric</th></tr>' + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in [("1 teaspoon", "5 ml"), ("1 tablespoon", "15 ml"), ("1/4 cup", "60 ml"), ("1/3 cup", "80 ml"), ("1/2 cup", "120 ml"), ("1 cup", "240 ml"), ("1 oz", "28 g"), ("1 lb", "454 g"), ("350 °F", "175 °C"), ("400 °F", "200 °C"), ("425 °F", "220 °C")]) + '</table></div>')
for i in range(1, 51):
    P.append(f'<div class="pg"><div style="display:flex;justify-content:space-between"><h2>Recipe {i}</h2><span style="color:#999">☆ ☆ ☆ ☆ ☆</span></div>' + lines(1) +
             '<div style="display:flex;gap:10pt">' + "".join(f'<div style="flex:1"><div class="lbl">{x}</div>' + lines(1) + '</div>' for x in ["Serves", "Prep", "Cook", "Oven"]) + '</div>'
             '<div class="lbl">Ingredients</div>' + lines(14) + '<div class="lbl">Notes</div>' + lines(5) + '</div>')
    P.append(f'<div class="pg"><h2>Method</h2>' + "".join(f'<div style="display:flex;gap:6pt;align-items:flex-end"><b style="width:12pt;color:var(--c)">{s}</b><div class="line" style="flex:1"></div></div>' + lines(1) for s in range(1, 11)) + '<div class="lbl">Source / from</div>' + lines(1) + '</div>')
P += [NOTES] * 2
LOG.append(render("recipe-book", "My Recipe Book", "Blank cookbook to write in 50 of your favourite family recipes", "RateKit Press", "#a8551f", "#f8ece2", P,
       '<p style="font-size:16pt;font-weight:700">Keep your family recipes in one place.</p><p>50 two-page recipe spreads with servings, prep and cook times, ingredients, step-by-step method and notes.</p><p>Plus a contents list to find each recipe and a handy kitchen conversion chart. A thoughtful gift.</p>'))

# 4. Gratitude journal
P = title_page("Gratitude Journal", "5 minutes a day for a happier, more mindful you")
P.append('<div class="pg"><h2>How to use this journal</h2><p style="line-height:1.7">Each morning, write three things you\'re grateful for and what would make today great. Each evening, note three good things that happened and one thing you\'d do differently. Most people notice a difference within a few weeks.</p></div>')
for d in range(1, 121):
    P.append(f'<div class="pg"><div style="display:flex;justify-content:space-between"><h2>Day {d}</h2><span>Date: ____________</span></div>'
             + "".join(f'<div class="lbl">{q}</div>' + lines(n) for q, n in [("I am grateful for", 3), ("What would make today great", 3), ("Today\'s affirmation", 1), ("Three good things that happened", 3), ("How could today have been better?", 2)])
             + '<div class="lbl">Mood</div><div style="font-size:14pt">😞 😐 🙂 😊 😄</div></div>')
LOG.append(render("gratitude-journal-book", "Gratitude Journal", "120 days of morning and evening prompts. 5 minutes a day.", "RateKit Press", "#5c7f67", "#e8f1eb", P,
       '<p style="font-size:16pt;font-weight:700">Five minutes a day. A happier you.</p><p>120 guided daily pages with simple morning and evening prompts: gratitude, intentions, affirmations, good things and reflection.</p><p>Undated, so you can start any day. A lovely gift.</p>'))

# 5. Workout log book
P = title_page("Workout Log Book", "Gym and fitness journal for strength training and cardio")
P.append('<div class="pg"><h2>My goals & starting point</h2>' + "".join(f'<div class="lbl">{x}</div>' + lines(2) for x in ["Main goal", "Why it matters", "Start date"]) +
         '<table style="margin-top:6pt"><tr><th>Measurement</th><th>Start</th><th>Month 3</th><th>Month 6</th></tr>' + "".join(f"<tr><td>{m}</td><td></td><td></td><td></td></tr>" for m in ["Weight", "Chest", "Waist", "Hips", "Arm", "Thigh", "Body fat %"]) + '</table></div>')
for i in range(1, 121):
    P.append(f'<div class="pg"><div style="display:flex;justify-content:space-between"><h2>Workout {i}</h2><span>Date: ________</span></div><div style="display:flex;gap:10pt"><div style="flex:1"><div class="lbl">Focus</div>{lines(1)}</div><div style="flex:1"><div class="lbl">Duration</div>{lines(1)}</div></div>'
             '<table style="margin-top:6pt"><tr><th style="width:34%">Exercise</th><th>Set 1</th><th>Set 2</th><th>Set 3</th><th>Set 4</th></tr>' + "<tr style='height:21pt'><td></td><td></td><td></td><td></td><td></td></tr>" * 10 + '</table>'
             '<div class="lbl">Cardio · type / time / distance</div>' + lines(1) + '<div class="lbl">Notes · energy · sleep</div>' + lines(2) + '</div>')
P += [NOTES] * 2
LOG.append(render("workout-log-book", "Workout Log Book", "Gym and fitness journal with 120 workout pages for strength and cardio", "RateKit Press", "#212529", "#e9ecef", P,
       '<p style="font-size:16pt;font-weight:700">Track every rep. See your progress.</p><p>120 workout pages: exercises, weight and reps for 4 sets, cardio, duration and notes.</p><p>Plus a goals page and body measurements tracker. Fits in your gym bag.</p>'))
