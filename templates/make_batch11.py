"""Round 16 spreadsheet products into products/. Run: python3 make_batch11.py (reuses helpers from make_batch2.py)"""
import pathlib, random
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
from openpyxl.chart import PieChart
today = dt.date.today(); y = today.year
mon = today - dt.timedelta(days=today.weekday())
random.seed(16)
def kpis(ws, rows, start=4, wa=28, wb_=14):
    for r, (a, f, nf_) in enumerate(rows, start):
        ws[f"A{r}"] = a; ws[f"B{r}"] = f; ws[f"B{r}"].number_format = nf_; ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
    ws.column_dimensions["A"].width = wa; ws.column_dimensions["B"].width = wb_
def yearsel(ws, row=3):
    ws[f"A{row}"] = "Year"; ws[f"B{row}"] = y; ws[f"B{row}"].fill = SOFT; ws[f"A{row}"].font = Font(bold=True)
def ycond(sheet, col, last, yc="$B$3"):
    return f"{sheet}!${col}$4:${col}${last},\">=\"&DATE({yc},1,1),{sheet}!${col}$4:${col}${last},\"<\"&DATE({yc}+1,1,1)"
def mcond(sheet, col, last, i, yc="$B$3"):
    return f"{sheet}!${col}$4:${col}${last},\">=\"&DATE({yc},{i + 1},1),{sheet}!${col}$4:${col}${last},\"<\"&DATE({yc},{i + 2},1)"

# 1. Pet expense & vet tracker
C = "AE3EC9"; title, header = kit(C); wb = Workbook(); pt = wb.active; pt.title = "Pets"
title(pt, "My pets", "One row per pet. Costs, next vet visit and due treatments update automatically.")
header(pt, ["Pet", "Species", "Breed", "Birthday", "Age", "Microchip", "Insurance (monthly)", "Spent this year", "Spent all time", "Next due treatment", "Due on"], [14, 11, 16, 11, 7, 16, 13, 13, 13, 22, 11])
pets = [("Biscuit", "Dog", "Cocker Spaniel", dt.date(y - 4, 5, 12), 28), ("Luna", "Cat", "Moggy", dt.date(y - 7, 2, 3), 14), ("Pip", "Rabbit", "Mini Lop", dt.date(y - 2, 8, 20), 0)]
for r, (n, s, b, bd, ins) in enumerate(pets, 4):
    pt[f"A{r}"], pt[f"B{r}"], pt[f"C{r}"], pt[f"D{r}"], pt[f"G{r}"] = n, s, b, bd, ins
dv(pt, '"Dog,Cat,Rabbit,Guinea pig,Bird,Fish,Reptile,Horse,Other"', "B4:B20")
for r in range(4, 21):
    pt[f"D{r}"].number_format = "dd mmm yy"
    pt[f"E{r}"] = f'=IF(D{r}="","",DATEDIF(D{r},TODAY(),"y"))'
    pt[f"H{r}"] = f'=IF(A{r}="","",SUMIFS(Expenses!$E$4:$E$3000,Expenses!$B$4:$B$3000,A{r},Expenses!$A$4:$A$3000,">="&DATE(YEAR(TODAY()),1,1)))'
    pt[f"I{r}"] = f'=IF(A{r}="","",SUMIFS(Expenses!$E$4:$E$3000,Expenses!$B$4:$B$3000,A{r}))'
    pt[f"K{r}"] = f'=IF(A{r}="","",IFERROR(_xlfn.MINIFS(Health!$F$4:$F$1000,Health!$B$4:$B$1000,A{r},Health!$F$4:$F$1000,">="&TODAY()-30),""))'
    pt[f"J{r}"] = f'=IF(OR(A{r}="",K{r}="",K{r}=0),"",INDEX(Health!$C$4:$C$1000,MATCH(1,INDEX((Health!$B$4:$B$1000=A{r})*(Health!$F$4:$F$1000=K{r}),0),0)))'
    for c in "GHI": pt[f"{c}{r}"].number_format = M
    pt[f"K{r}"].number_format = "dd mmm yy"
pt.conditional_formatting.add("K4:K20", FormulaRule(formula=['AND(ISNUMBER(K4),K4>0,K4<TODAY())'], fill=PatternFill("solid", fgColor="FFC9C9"), font=Font(bold=True, color="C0392B")))
pt.conditional_formatting.add("K4:K20", FormulaRule(formula=['AND(ISNUMBER(K4),K4>0,K4-TODAY()<=14,K4>=TODAY())'], fill=PatternFill("solid", fgColor="FFF3BF")))
ex = wb.create_sheet("Expenses", 1); title(ex, "Expenses", "Every pet cost: food, vet, insurance, grooming, toys and more.")
header(ex, ["Date", "Pet", "Category", "Description", "Amount", "Paid by insurance", "Notes"], [11, 14, 14, 26, 11, 14, 22])
cats = ["Food", "Vet", "Insurance", "Medication", "Grooming", "Toys & treats", "Bedding & litter", "Boarding / sitting", "Training", "Accessories", "Other"]
r = 4
for mth in range(1, 13):
    if dt.date(y, mth, 1) > today: break
    for n, s, _, _, ins in pets:
        food = {"Dog": 42, "Cat": 28, "Rabbit": 16}[s]
        ex[f"A{r}"] = dt.date(y, mth, 2); ex[f"B{r}"] = n; ex[f"C{r}"] = "Food"; ex[f"D{r}"] = "Monthly food"; ex[f"E{r}"] = food + random.choice([0, 0, 3, -2]); r += 1
        if ins: ex[f"A{r}"] = dt.date(y, mth, 1); ex[f"B{r}"] = n; ex[f"C{r}"] = "Insurance"; ex[f"D{r}"] = "Pet insurance"; ex[f"E{r}"] = ins; r += 1
        if random.random() < 0.35:
            c = random.choice(["Toys & treats", "Bedding & litter", "Grooming", "Accessories"]); ex[f"A{r}"] = dt.date(y, mth, random.randint(5, 26)); ex[f"B{r}"] = n; ex[f"C{r}"] = c; ex[f"E{r}"] = random.choice([8, 12, 15, 25, 40]); r += 1
for (mth, n, d_, a, cl) in [(3, "Biscuit", "Ear infection", 145, 90), (5, "Luna", "Annual check & booster", 78, 0), (8, "Pip", "Nail trim & check", 32, 0), (6, "Biscuit", "Boarding 5 nights", 175, 0)]:
    if dt.date(y, mth, 1) <= today:
        ex[f"A{r}"] = dt.date(y, mth, 14); ex[f"B{r}"] = n; ex[f"C{r}"] = "Vet" if "Boarding" not in d_ else "Boarding / sitting"; ex[f"D{r}"] = d_; ex[f"E{r}"] = a; ex[f"F{r}"] = cl or None; r += 1
dv(ex, "=Pets!$A$4:$A$20", "B4:B3000"); dv(ex, '"' + ",".join(cats) + '"', "C4:C3000")
for r in range(4, 3001): ex[f"A{r}"].number_format = "dd mmm yy"; ex[f"E{r}"].number_format = ex[f"F{r}"].number_format = M
hl = wb.create_sheet("Health", 2); title(hl, "Health & vet record", "Vaccinations, flea and worm treatments, check-ups and weight. Add a next due date to get reminders.")
header(hl, ["Date", "Pet", "Treatment / visit", "Vet / product", "Weight (kg)", "Next due", "Days to go", "Notes"], [11, 14, 24, 18, 11, 11, 10, 26])
hrows = [(-200, "Biscuit", "Annual vaccination", "Park Vets", 14.2, 365), (-25, "Biscuit", "Flea & worm treatment", "Spot-on", None, 5), (-150, "Luna", "Booster vaccination", "Park Vets", 4.6, 215),
         (-40, "Luna", "Worming tablet", "Tablet", None, 50), (-90, "Pip", "Myxo/RHD vaccination", "Park Vets", 1.9, 275), (-10, "Pip", "Nail trim", "Groomer", None, 50)]
for r, (dd, n, t, v, w, nd) in enumerate(hrows, 4):
    hl[f"A{r}"] = today + dt.timedelta(days=dd); hl[f"B{r}"] = n; hl[f"C{r}"] = t; hl[f"D{r}"] = v; hl[f"E{r}"] = w; hl[f"F{r}"] = today + dt.timedelta(days=dd + nd)
dv(hl, "=Pets!$A$4:$A$20", "B4:B1000")
for r in range(4, 1001):
    hl[f"A{r}"].number_format = hl[f"F{r}"].number_format = "dd mmm yy"
    hl[f"G{r}"] = f'=IF(F{r}="","",F{r}-TODAY())'
hl.conditional_formatting.add("G4:G1000", CellIsRule(operator="lessThan", formula=["0"], fill=PatternFill("solid", fgColor="FFC9C9")))
hl.conditional_formatting.add("G4:G1000", CellIsRule(operator="between", formula=["0", "14"], fill=PatternFill("solid", fgColor="FFF3BF")))
db = wb.create_sheet("Dashboard", 0); title(db, "Pet Costs Dashboard", "Pick a year. Updates from the Expenses tab."); yearsel(db)
Y = ycond("Expenses", "A", 3000)
kpis(db, [("Total spent", f"=SUMIFS(Expenses!$E$4:$E$3000,{Y})", M), ("Insurance paid back", f"=SUMIFS(Expenses!$F$4:$F$3000,{Y})", M), ("Net cost", "=B4-B5", M),
          ("Average per month", "=B6/IF(B3=YEAR(TODAY()),MONTH(TODAY()),12)", M), ("Vet bills", f'=SUMIFS(Expenses!$E$4:$E$3000,Expenses!$C$4:$C$3000,"Vet",{Y})', M),
          ("Treatments overdue", '=COUNTIF(Health!G4:G1000,"<0")', "0"), ("Treatments due in 14 days", '=COUNTIFS(Health!G4:G1000,">=0",Health!G4:G1000,"<=14")', "0")], start=4)
db["B6"].font = Font(bold=True, size=13, color=C)
header(db, ["Category", "Spent"], [28, 14], row=13, freeze=False)
for i, c in enumerate(cats):
    r = 14 + i; db[f"A{r}"] = c; db[f"B{r}"] = f"=SUMIFS(Expenses!$E$4:$E$3000,Expenses!$C$4:$C$3000,A{r},{Y})"; db[f"B{r}"].number_format = M
header(db, ["Month", "Spent"], [28, 14], row=27, freeze=False)
for i, m in enumerate(MONTHS):
    r = 28 + i; db[f"A{r}"] = m; db[f"B{r}"] = f"=SUMIFS(Expenses!$E$4:$E$3000,{mcond('Expenses', 'A', 3000, i)})"; db[f"B{r}"].number_format = M
pc = PieChart(); pc.title = "Where the money goes"; pc.height = 8; pc.width = 12
pc.add_data(Reference(db, min_col=2, min_row=13, max_row=24), titles_from_data=True); pc.set_categories(Reference(db, min_col=1, min_row=14, max_row=24)); db.add_chart(pc, "D3")
bc = BarChart(); bc.title = "Spending by month"; bc.height = 7; bc.width = 16; bc.legend = None
bc.add_data(Reference(db, min_col=2, min_row=27, max_row=39), titles_from_data=True); bc.set_categories(Reference(db, min_col=1, min_row=28, max_row=39)); db.add_chart(bc, "D20")
howto(wb, C, ["1. Pets: add each pet with species, breed, birthday, microchip and monthly insurance. Spending and the next treatment due fill in for each pet.",
              "2. Expenses: log every cost and pick the pet and category. Put any insurance payout in 'Paid by insurance'.",
              "3. Health: record vaccinations, flea and worm treatments, vet visits and weight. Add the next due date: overdue turns red, due within 14 days turns yellow.",
              "4. Dashboard: total and net cost, average per month, vet bills, spending by category and month, and treatments due.", "5. Delete the sample pets and entries first."])
wb.save(OUT / "Pet-Expense-Vet-Tracker.xlsx")

# 2. Class & workshop booking tracker
C = "0CA678"; title, header = kit(C); wb = Workbook(); cl = wb.active; cl.title = "Classes"
title(cl, "Classes & sessions", "One row per class or workshop date. Bookings, spaces left and income fill in.")
header(cl, ["Session ID", "Date", "Time", "Class / workshop", "Venue", "Capacity", "Price", "Venue cost", "Booked", "Attended", "Spaces left", "Income", "Profit"], [11, 11, 8, 22, 14, 9, 9, 10, 8, 9, 10, 11, 11])
classes = [("Beginners Yoga", 12, 12, 30), ("Pottery Taster", 8, 35, 60), ("Pilates Flow", 14, 12, 30), ("Watercolour Workshop", 10, 28, 45)]
start = mon - dt.timedelta(weeks=5); r = 4; sid = []
for w in range(8):
    for k, (n, cap, pr, vc) in enumerate(classes):
        if (w + k) % 2: continue
        dd = start + dt.timedelta(weeks=w, days=[0, 2, 3, 5][k]); s = f"S{r - 3:03d}"; sid.append((s, dd, cap))
        cl[f"A{r}"], cl[f"B{r}"], cl[f"C{r}"], cl[f"D{r}"], cl[f"E{r}"], cl[f"F{r}"], cl[f"G{r}"], cl[f"H{r}"] = s, dd, dt.time([18, 10, 19, 14][k], 0), n, ["Studio A", "Clay Room", "Studio A", "Library Hall"][k], cap, pr, vc; r += 1
for r in range(4, 401):
    cl[f"B{r}"].number_format = "ddd dd mmm"; cl[f"C{r}"].number_format = "hh:mm"
    cl[f"I{r}"] = f'=IF(A{r}="","",COUNTIFS(Bookings!$C$4:$C$5000,A{r},Bookings!$F$4:$F$5000,"<>Cancelled"))'
    cl[f"J{r}"] = f'=IF(A{r}="","",COUNTIFS(Bookings!$C$4:$C$5000,A{r},Bookings!$H$4:$H$5000,"Yes"))'
    cl[f"K{r}"] = f'=IF(A{r}="","",N(F{r})-I{r})'
    cl[f"L{r}"] = f'=IF(A{r}="","",SUMIFS(Bookings!$E$4:$E$5000,Bookings!$C$4:$C$5000,A{r},Bookings!$F$4:$F$5000,"Paid"))'
    cl[f"M{r}"] = f'=IF(A{r}="","",L{r}-N(H{r}))'
    for c in "GHLM": cl[f"{c}{r}"].number_format = M
cl.conditional_formatting.add("K4:K400", CellIsRule(operator="lessThanOrEqual", formula=["0"], fill=PatternFill("solid", fgColor="FFC9C9"), font=Font(bold=True)))
cl.conditional_formatting.add("K4:K400", CellIsRule(operator="between", formula=["1", "2"], fill=PatternFill("solid", fgColor="FFF3BF")))
bk = wb.create_sheet("Bookings", 1); title(bk, "Bookings", "One row per person per session. Pick the session ID from the list.")
header(bk, ["Booked on", "Name", "Session ID", "Class (auto)", "Amount", "Payment", "Email / phone", "Attended?", "Notes"], [11, 18, 11, 22, 10, 11, 22, 10, 20])
names = ["Amy", "Ben", "Cara", "Dev", "Ella", "Femi", "Gina", "Hugo", "Iris", "Jon", "Kemi", "Leah", "Milo", "Nina", "Omar", "Pia", "Quinn", "Rosa", "Sven", "Tara"]
r = 4
for s, dd, cap in sid:
    n_b = random.randint(max(2, cap - 6), cap)
    for nm in random.sample(names, min(n_b, len(names))):
        pay = random.choice(["Paid"] * 8 + ["Unpaid", "Cancelled"])
        bk[f"A{r}"] = dd - dt.timedelta(days=random.randint(1, 14)); bk[f"B{r}"] = nm + " " + random.choice("ABCDEFGHKLMNPRST") + "."; bk[f"C{r}"] = s; bk[f"F{r}"] = pay
        if dd < today and pay != "Cancelled": bk[f"H{r}"] = "Yes" if random.random() < 0.9 else "No"
        r += 1
dv(bk, "=Classes!$A$4:$A$400", "C4:C5000"); dv(bk, '"Paid,Unpaid,Refunded,Cancelled"', "F4:F5000"); dv(bk, '"Yes,No"', "H4:H5000")
for r in range(4, 5001):
    bk[f"A{r}"].number_format = "dd mmm"
    bk[f"D{r}"] = f'=IF(C{r}="","",IFERROR(VLOOKUP(C{r},Classes!$A$4:$D$400,4,FALSE)&" · "&TEXT(VLOOKUP(C{r},Classes!$A$4:$B$400,2,FALSE),"dd mmm"),"Unknown ID"))'
    bk[f"E{r}"] = f'=IF(C{r}="","",IF(OR(F{r}="Cancelled",F{r}="Refunded"),0,IFERROR(VLOOKUP(C{r},Classes!$A$4:$G$400,7,FALSE),0)))'
    bk[f"E{r}"].number_format = M
bk.conditional_formatting.add("F4:F5000", CellIsRule(operator="equal", formula=['"Unpaid"'], fill=PatternFill("solid", fgColor="FFE8CC"), font=Font(bold=True)))
db = wb.create_sheet("Dashboard", 0); title(db, "Classes Dashboard", "Pick a year. Updates from the Classes and Bookings tabs."); yearsel(db)
Y = ycond("Classes", "B", 400)
kpis(db, [("Sessions run", f"=COUNTIFS({Y},Classes!$B$4:$B$400,\"<\"&TODAY())", "0"), ("Sessions coming up", f'=COUNTIFS(Classes!$B$4:$B$400,">="&TODAY())', "0"),
          ("Places booked", f"=SUMIFS(Classes!$I$4:$I$400,{Y})", "0"), ("Fill rate", f"=IFERROR(B6/SUMIFS(Classes!$F$4:$F$400,{Y}),0)", "0%"),
          ("Attendance rate (past sessions)", f'=IFERROR(SUMIFS(Classes!$J$4:$J$400,{Y},Classes!$B$4:$B$400,"<"&TODAY())/SUMIFS(Classes!$I$4:$I$400,{Y},Classes!$B$4:$B$400,"<"&TODAY()),0)', "0%"),
          ("Income (paid)", f"=SUMIFS(Classes!$L$4:$L$400,{Y})", M), ("Venue costs", f"=SUMIFS(Classes!$H$4:$H$400,{Y})", M), ("Profit", "=B9-B10", M),
          ("Unpaid bookings", '=COUNTIF(Bookings!F4:F5000,"Unpaid")', "0"), ("Unique customers", '=SUMPRODUCT((Bookings!B4:B5000<>"")/COUNTIF(Bookings!B4:B5000,Bookings!B4:B5000&""))', "0")], start=4, wa=32)
db["B11"].font = Font(bold=True, size=13, color=C)
header(db, ["Class", "Sessions", "Booked", "Fill rate", "Profit"], [32, 10, 9, 10, 12], row=16, freeze=False)
for i, (n, *_ ) in enumerate(classes + [("", 0, 0, 0)] * 4):
    r = 17 + i
    if n: db[f"A{r}"] = n
    db[f"B{r}"] = f'=IF(A{r}="","",COUNTIFS(Classes!$D$4:$D$400,A{r},{Y}))'; db[f"C{r}"] = f'=IF(A{r}="","",SUMIFS(Classes!$I$4:$I$400,Classes!$D$4:$D$400,A{r},{Y}))'
    db[f"D{r}"] = f'=IF(OR(A{r}="",B{r}=0),"",C{r}/SUMIFS(Classes!$F$4:$F$400,Classes!$D$4:$D$400,A{r},{Y}))'; db[f"D{r}"].number_format = "0%"
    db[f"E{r}"] = f'=IF(A{r}="","",SUMIFS(Classes!$M$4:$M$400,Classes!$D$4:$D$400,A{r},{Y}))'; db[f"E{r}"].number_format = M
db.conditional_formatting.add("D17:D24", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="38D9A9"))
bc = BarChart(); bc.title = "Profit by class"; bc.height = 7; bc.width = 15; bc.legend = None
bc.add_data(Reference(db, min_col=5, min_row=16, max_row=20), titles_from_data=True); bc.set_categories(Reference(db, min_col=1, min_row=17, max_row=20)); db.add_chart(bc, "G3")
howto(wb, C, ["1. Classes: one row per session with a unique ID (S001, S002...), date, time, class name, venue, capacity, price per person and venue cost.",
              "2. Bookings: one row per person per session. Pick the session ID, set payment (Paid, Unpaid, Refunded, Cancelled) and tick attendance after the class. Class name and amount fill in.",
              "3. Classes then shows booked places, attendance, spaces left (yellow = nearly full, red = full), income and profit for each session.",
              "4. Dashboard: sessions run and coming up, fill and attendance rates, income, profit, unpaid bookings, customers and a breakdown by class.",
              "5. For yoga and fitness teachers, craft workshops, tutors and community groups. Delete the sample data first."])
wb.save(OUT / "Class-Workshop-Booking-Tracker.xlsx")

# 3. Tip tracker for servers
C = "F08C00"; title, header = kit(C); wb = Workbook(); sh = wb.active; sh.title = "Shifts"
title(sh, "Shift & tips log", "One row per shift. Hourly earnings with tips are worked out for you.")
header(sh, ["Date", "Day", "Job / venue", "Shift", "Start", "End", "Hours", "Base pay rate", "Base pay", "Cash tips", "Card tips", "Tip-out given", "Net tips", "Total earned", "Per hour", "Covers / tables", "Notes"],
       [11, 6, 14, 10, 7, 7, 7, 10, 10, 9, 9, 10, 9, 11, 9, 10, 20])
d = today - dt.timedelta(days=70); r = 4
while d < today:
    if d.weekday() in (0, 1) or random.random() < 0.15: d += dt.timedelta(days=1); continue
    ev = d.weekday() >= 3
    sh[f"A{r}"] = d; sh[f"C{r}"] = "The Olive Tree" if random.random() < 0.8 else "Hotel Bar"; sh[f"D{r}"] = "Dinner" if ev else random.choice(["Lunch", "Dinner"])
    st_ = dt.time(17, 0) if sh[f"D{r}"].value == "Dinner" else dt.time(11, 30); sh[f"E{r}"] = st_
    sh[f"F{r}"] = dt.time(23, random.choice([0, 30])) if sh[f"D{r}"].value == "Dinner" else dt.time(16, 0); sh[f"H{r}"] = 12.5
    big = 1.6 if d.weekday() >= 4 else 1.0
    sh[f"J{r}"] = round(random.uniform(15, 40) * big); sh[f"K{r}"] = round(random.uniform(30, 75) * big); sh[f"L{r}"] = round((sh[f"J{r}"].value + sh[f"K{r}"].value) * 0.1); sh[f"P{r}"] = random.randint(8, 22)
    r += 1; d += dt.timedelta(days=1)
dv(sh, '"Breakfast,Brunch,Lunch,Dinner,Late,Double,Event"', "D4:D3000")
for r in range(4, 3001):
    sh[f"A{r}"].number_format = "dd mmm yy"; sh[f"E{r}"].number_format = sh[f"F{r}"].number_format = "hh:mm"
    sh[f"B{r}"] = f'=IF(A{r}="","",CHOOSE(WEEKDAY(A{r},2),"Mon","Tue","Wed","Thu","Fri","Sat","Sun"))'
    sh[f"G{r}"] = f'=IF(OR(E{r}="",F{r}=""),"",ROUND(MOD(F{r}-E{r},1)*24,2))'
    sh[f"I{r}"] = f'=IF(G{r}="","",G{r}*N(H{r}))'
    sh[f"M{r}"] = f'=IF(A{r}="","",N(J{r})+N(K{r})-N(L{r}))'
    sh[f"N{r}"] = f'=IF(A{r}="","",N(I{r})+M{r})'
    sh[f"O{r}"] = f'=IF(OR(G{r}="",N(G{r})=0),"",N{r}/G{r})'
    for c in "HIJKLMNO": sh[f"{c}{r}"].number_format = M
sh.conditional_formatting.add("O4:O3000", ColorScaleRule := __import__("openpyxl").formatting.rule.ColorScaleRule(start_type="min", start_color="FFF4E6", end_type="max", end_color="FFA94D"))
db = wb.create_sheet("Dashboard", 0); title(db, "Tips Dashboard", "Pick a year. See your best days and shifts and set money aside for tax.")
yearsel(db); db["D3"] = "Tax to set aside (% of tips)"; db["E3"] = 0.20; db["E3"].number_format = "0%"; db["E3"].fill = SOFT; db["D3"].font = Font(bold=True)
Y = ycond("Shifts", "A", 3000)
kpis(db, [("Shifts worked", f"=COUNTIFS({Y})", "0"), ("Hours worked", f"=SUMIFS(Shifts!$G$4:$G$3000,{Y})", "0.0"), ("Base pay", f"=SUMIFS(Shifts!$I$4:$I$3000,{Y})", M),
          ("Net tips", f"=SUMIFS(Shifts!$M$4:$M$3000,{Y})", M), ("Total earned", "=B6+B7", M), ("Average per hour (with tips)", "=IFERROR(B8/B5,0)", M),
          ("Average tips per shift", "=IFERROR(B7/B4,0)", M), ("Tips this week", '=SUMIFS(Shifts!$M$4:$M$3000,Shifts!$A$4:$A$3000,">="&TODAY()-WEEKDAY(TODAY(),3))', M),
          ("Set aside for tax", "=B7*E3", M)], start=4, wa=30)
db["B8"].font = Font(bold=True, size=13, color=C)
header(db, ["Day", "Shifts", "Avg tips", "Avg per hour"], [30, 10, 11, 12], row=15, freeze=False)
for i, dn in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
    r = 16 + i; db[f"A{r}"] = dn
    db[f"B{r}"] = f'=COUNTIFS(Shifts!$B$4:$B$3000,A{r},{Y})'
    db[f"C{r}"] = f'=IFERROR(SUMIFS(Shifts!$M$4:$M$3000,Shifts!$B$4:$B$3000,A{r},{Y})/B{r},"")'
    db[f"D{r}"] = f'=IFERROR(SUMIFS(Shifts!$N$4:$N$3000,Shifts!$B$4:$B$3000,A{r},{Y})/SUMIFS(Shifts!$G$4:$G$3000,Shifts!$B$4:$B$3000,A{r},{Y}),"")'
    db[f"C{r}"].number_format = db[f"D{r}"].number_format = M
header(db, ["Shift type", "Shifts", "Avg tips", "Avg per hour"], [30, 10, 11, 12], row=24, freeze=False)
for i, s in enumerate(["Breakfast", "Brunch", "Lunch", "Dinner", "Late", "Double", "Event"]):
    r = 25 + i; db[f"A{r}"] = s
    db[f"B{r}"] = f'=COUNTIFS(Shifts!$D$4:$D$3000,A{r},{Y})'
    db[f"C{r}"] = f'=IFERROR(SUMIFS(Shifts!$M$4:$M$3000,Shifts!$D$4:$D$3000,A{r},{Y})/B{r},"")'
    db[f"D{r}"] = f'=IFERROR(SUMIFS(Shifts!$N$4:$N$3000,Shifts!$D$4:$D$3000,A{r},{Y})/SUMIFS(Shifts!$G$4:$G$3000,Shifts!$D$4:$D$3000,A{r},{Y}),"")'
    db[f"C{r}"].number_format = db[f"D{r}"].number_format = M
header(db, ["Month", "Tips", "Total earned"], [30, 10, 12], row=33, freeze=False)
for i, m in enumerate(MONTHS):
    r = 34 + i; db[f"A{r}"] = m
    db[f"B{r}"] = f"=SUMIFS(Shifts!$M$4:$M$3000,{mcond('Shifts', 'A', 3000, i)})"; db[f"C{r}"] = f"=SUMIFS(Shifts!$N$4:$N$3000,{mcond('Shifts', 'A', 3000, i)})"
    db[f"B{r}"].number_format = db[f"C{r}"].number_format = M
bc = BarChart(); bc.title = "Average tips by day"; bc.height = 7; bc.width = 15; bc.legend = None
bc.add_data(Reference(db, min_col=3, min_row=15, max_row=22), titles_from_data=True); bc.set_categories(Reference(db, min_col=1, min_row=16, max_row=22)); db.add_chart(bc, "G3")
bc2 = BarChart(); bc2.title = "Tips by month"; bc2.height = 7; bc2.width = 15; bc2.legend = None
bc2.add_data(Reference(db, min_col=2, min_row=33, max_row=45), titles_from_data=True); bc2.set_categories(Reference(db, min_col=1, min_row=34, max_row=45)); db.add_chart(bc2, "G18")
howto(wb, C, ["1. Shifts: one row per shift with date, venue, shift type, start and end time (past midnight is fine), base hourly pay, cash and card tips, and any tip-out you gave to bar or kitchen staff.",
              "2. Hours, base pay, net tips, total earned and earnings per hour are worked out. The per-hour column is shaded so your best shifts stand out.",
              "3. Dashboard: pick the year and your tax set-aside rate. See totals, average per hour and per shift, this week's tips, your best days and shift types, and a monthly chart.",
              "4. Check how tips are taxed where you live. Delete the sample shifts first."])
wb.save(OUT / "Tip-Tracker-Servers.xlsx")

# 4. Social media content calendar
C = "D6336C"; title, header = kit(C); wb = Workbook(); st = wb.active; st.title = "Setup"
title(st, "Setup", "Your platforms, content pillars and posting goals.")
header(st, ["Platform", "Posts per week goal"], [18, 18], freeze=False)
plats = [("Instagram", 4), ("TikTok", 3), ("Facebook", 2), ("LinkedIn", 2), ("Pinterest", 5), ("YouTube", 1), ("", None), ("", None)]
for r, (p, g) in enumerate(plats, 4): st[f"A{r}"] = p or None; st[f"B{r}"] = g
header(st, ["Content pillar", "Target share"], [18, 18], row=13, freeze=False)
pillars = [("Educate", 0.35), ("Behind the scenes", 0.2), ("Promote", 0.2), ("Community", 0.15), ("Entertain", 0.1), ("", None)]
for r, (p, g) in enumerate(pillars, 14):
    st[f"A{r}"] = p or None; st[f"B{r}"] = g; st[f"B{r}"].number_format = "0%"
pl = wb.create_sheet("Content plan", 0); title(pl, "Content calendar", "Plan every post. Filter by platform, status or pillar.")
header(pl, ["Publish date", "Day", "Time", "Platform", "Format", "Pillar", "Topic / hook", "Caption / script notes", "Hashtags / keywords", "Link / CTA", "Status", "Likes", "Comments", "Shares / saves", "Reach", "Engagement rate"],
       [12, 6, 7, 11, 11, 15, 28, 30, 20, 16, 11, 8, 10, 12, 9, 12])
topics = {"Educate": ["3 mistakes beginners make", "How we price our products", "Quick tip: batch your tasks", "Tool I can't live without"], "Behind the scenes": ["Packing orders", "Studio tour", "A day in my life", "How it's made"],
          "Promote": ["New product launch", "Weekend discount", "Customer favourite", "Gift guide"], "Community": ["Customer shout-out", "Ask me anything", "Poll: which colour?", "Thank you for 1k"], "Entertain": ["Trend remix", "Bloopers", "Expectation vs reality"]}
fmts = {"Instagram": ["Reel", "Carousel", "Story", "Image"], "TikTok": ["Short video"], "Facebook": ["Image", "Video", "Text"], "LinkedIn": ["Text", "Carousel", "Article"], "Pinterest": ["Pin", "Idea pin"], "YouTube": ["Long video", "Short"]}
d = mon - dt.timedelta(weeks=3); r = 4
while d < mon + dt.timedelta(weeks=3):
    for p in random.sample(["Instagram", "TikTok", "Facebook", "LinkedIn", "Pinterest"], random.choice([1, 2])):
        pil = random.choices(list(topics), [35, 20, 20, 15, 10])[0]
        pl[f"A{r}"] = d; pl[f"C{r}"] = dt.time(random.choice([8, 12, 18, 19]), 0); pl[f"D{r}"] = p; pl[f"E{r}"] = random.choice(fmts[p]); pl[f"F{r}"] = pil; pl[f"G{r}"] = random.choice(topics[pil])
        if d < today:
            pl[f"K{r}"] = "Posted"; rc = random.randint(300, 3000); pl[f"O{r}"] = rc; pl[f"L{r}"] = int(rc * random.uniform(0.02, 0.09)); pl[f"M{r}"] = int(rc * random.uniform(0.002, 0.01)); pl[f"N{r}"] = int(rc * random.uniform(0.002, 0.02))
        else: pl[f"K{r}"] = random.choice(["Idea", "Drafted", "Scheduled", "Scheduled"])
        r += 1
    d += dt.timedelta(days=1)
dv(pl, "=Setup!$A$4:$A$11", "D4:D2000"); dv(pl, '"Reel,Carousel,Story,Image,Short video,Video,Long video,Short,Text,Article,Pin,Idea pin,Live,Other"', "E4:E2000")
dv(pl, "=Setup!$A$14:$A$19", "F4:F2000"); dv(pl, '"Idea,Drafted,Designed,Scheduled,Posted"', "K4:K2000")
for r in range(4, 2001):
    pl[f"A{r}"].number_format = "dd mmm yy"; pl[f"C{r}"].number_format = "hh:mm"
    pl[f"B{r}"] = f'=IF(A{r}="","",CHOOSE(WEEKDAY(A{r},2),"Mon","Tue","Wed","Thu","Fri","Sat","Sun"))'
    pl[f"P{r}"] = f'=IF(N(O{r})=0,"",(N(L{r})+N(M{r})+N(N{r}))/O{r})'; pl[f"P{r}"].number_format = "0.0%"
for s, col in [("Posted", "D3F9D8"), ("Scheduled", "D0EBFF"), ("Drafted", "FFF3BF"), ("Designed", "FFF3BF"), ("Idea", "F1F3F5")]:
    pl.conditional_formatting.add("K4:K2000", CellIsRule(operator="equal", formula=[f'"{s}"'], fill=PatternFill("solid", fgColor=col)))
pl.conditional_formatting.add("A4:A2000", FormulaRule(formula=['AND(ISNUMBER(A4),A4<TODAY(),K4<>"Posted",K4<>"")'], fill=PatternFill("solid", fgColor="FFC9C9")))
pl.auto_filter.ref = "A3:P2000"
wk = wb.create_sheet("This week", 1); title(wk, "Week at a glance", "Type any Monday to see that week's plan.")
wk["A3"] = "Week starting"; wk["B3"] = mon; wk["B3"].number_format = "ddd dd mmm yy"; wk["B3"].fill = SOFT; wk["A3"].font = Font(bold=True)
header(wk, ["Platform", "Goal", "Planned", "Posted", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], [16, 8, 9, 8, 7, 7, 7, 7, 7, 7, 7], row=5, freeze=False)
P = "'Content plan'!"
for i in range(8):
    r = 6 + i; wk[f"A{r}"] = f'=IF(Setup!A{4 + i}="","",Setup!A{4 + i})'; wk[f"B{r}"] = f'=IF(A{r}="","",Setup!B{4 + i})'
    wk[f"C{r}"] = f'=IF(A{r}="","",COUNTIFS({P}$D$4:$D$2000,A{r},{P}$A$4:$A$2000,">="&$B$3,{P}$A$4:$A$2000,"<"&$B$3+7))'
    wk[f"D{r}"] = f'=IF(A{r}="","",COUNTIFS({P}$D$4:$D$2000,A{r},{P}$A$4:$A$2000,">="&$B$3,{P}$A$4:$A$2000,"<"&$B$3+7,{P}$K$4:$K$2000,"Posted"))'
    for j in range(7):
        c = L(5 + j); wk[f"{c}{r}"] = f'=IF(A{r}="","",IF(COUNTIFS({P}$D$4:$D$2000,A{r},{P}$A$4:$A$2000,$B$3+{j})=0,"",COUNTIFS({P}$D$4:$D$2000,A{r},{P}$A$4:$A$2000,$B$3+{j})))'
wk.conditional_formatting.add("C6:C13", FormulaRule(formula=['AND(ISNUMBER(C6),ISNUMBER(B6),C6<B6)'], font=Font(bold=True, color="C0392B")))
wk.conditional_formatting.add("E6:K13", FormulaRule(formula=['ISNUMBER(E6)'], fill=PatternFill("solid", fgColor="FFDEEB")))
an = wb.create_sheet("Analytics", 0); title(an, "Content Analytics", "What's working. Uses posted content only.")
kpis(an, [("Posts published", f'=COUNTIF({P}K4:K2000,"Posted")', "0"), ("Scheduled / in progress", f'=COUNTIFS({P}K4:K2000,"<>Posted",{P}K4:K2000,"<>")', "0"),
          ("Overdue (date passed, not posted)", f'=COUNTIFS({P}A4:A2000,"<"&TODAY(),{P}K4:K2000,"<>Posted",{P}K4:K2000,"<>")', "0"),
          ("Total reach", f"=SUM({P}O4:O2000)", "#,##0"), ("Average engagement rate", f'=IFERROR((SUM({P}L4:L2000)+SUM({P}M4:M2000)+SUM({P}N4:N2000))/SUM({P}O4:O2000),0)', "0.0%")], start=4, wa=34)
header(an, ["Platform", "Posts", "Reach", "Engagement rate"], [34, 9, 10, 15], row=11, freeze=False)
for i in range(8):
    r = 12 + i; an[f"A{r}"] = f'=IF(Setup!A{4 + i}="","",Setup!A{4 + i})'
    an[f"B{r}"] = f'=IF(A{r}="","",COUNTIFS({P}$D$4:$D$2000,A{r},{P}$K$4:$K$2000,"Posted"))'
    an[f"C{r}"] = f'=IF(A{r}="","",SUMIFS({P}$O$4:$O$2000,{P}$D$4:$D$2000,A{r}))'
    an[f"D{r}"] = f'=IF(OR(A{r}="",N(C{r})=0),"",(SUMIFS({P}$L$4:$L$2000,{P}$D$4:$D$2000,A{r})+SUMIFS({P}$M$4:$M$2000,{P}$D$4:$D$2000,A{r})+SUMIFS({P}$N$4:$N$2000,{P}$D$4:$D$2000,A{r}))/C{r})'; an[f"D{r}"].number_format = "0.0%"
header(an, ["Pillar", "Share of posts", "Target", "Engagement rate"], [34, 13, 9, 15], row=21, freeze=False)
for i in range(6):
    r = 22 + i; an[f"A{r}"] = f'=IF(Setup!A{14 + i}="","",Setup!A{14 + i})'
    an[f"B{r}"] = f'=IF(A{r}="","",IFERROR(COUNTIF({P}$F$4:$F$2000,A{r})/COUNTA({P}$F$4:$F$2000),0))'; an[f"B{r}"].number_format = "0%"
    an[f"C{r}"] = f'=IF(A{r}="","",Setup!B{14 + i})'; an[f"C{r}"].number_format = "0%"
    an[f"D{r}"] = f'=IF(A{r}="","",IFERROR((SUMIFS({P}$L$4:$L$2000,{P}$F$4:$F$2000,A{r})+SUMIFS({P}$M$4:$M$2000,{P}$F$4:$F$2000,A{r})+SUMIFS({P}$N$4:$N$2000,{P}$F$4:$F$2000,A{r}))/SUMIFS({P}$O$4:$O$2000,{P}$F$4:$F$2000,A{r}),""))'; an[f"D{r}"].number_format = "0.0%"
bc = BarChart(); bc.title = "Engagement rate by pillar"; bc.height = 7; bc.width = 15; bc.legend = None
bc.add_data(Reference(an, min_col=4, min_row=21, max_row=26), titles_from_data=True); bc.set_categories(Reference(an, min_col=1, min_row=22, max_row=26)); an.add_chart(bc, "F3")
howto(wb, C, ["1. Setup: list your platforms with a weekly posting goal, and your content pillars (the themes you post about) with a target share.",
              "2. Content plan: one row per post with date, time, platform, format, pillar, hook, caption notes, hashtags and link. Move the status from Idea to Posted. Dates that pass without posting turn red.",
              "3. After posting, add likes, comments, shares or saves and reach. Engagement rate is worked out.",
              "4. This week: type a Monday to see planned and posted counts against your goals and which days have posts.",
              "5. Analytics: reach and engagement by platform and by pillar, so you can do more of what works. Delete the sample posts first."])
wb.save(OUT / "Social-Media-Content-Calendar.xlsx")

# 5. Expense report & reimbursement tracker
C = "495057"; title, header = kit(C); wb = Workbook(); stg = wb.active; stg.title = "Settings"
title(stg, "Settings", "Your details and the rates your employer uses.")
for r, (n, v, f) in enumerate([("Employee name", "Your name", None), ("Department", "Sales", None), ("Manager", "Manager name", None), ("Mileage rate per km / mile", 0.45, M), ("Currency", "CHF", None)], 4):
    stg[f"A{r}"] = n; stg[f"B{r}"] = v; stg[f"A{r}"].font = Font(bold=True); stg[f"B{r}"].fill = SOFT
    if f: stg[f"B{r}"].number_format = f
stg.column_dimensions["A"].width = 28; stg.column_dimensions["B"].width = 18
cats = ["Travel", "Mileage", "Hotel", "Meals", "Client entertainment", "Parking & tolls", "Supplies", "Phone & internet", "Training", "Other"]
ex = wb.create_sheet("Expenses", 0); title(ex, "Expenses", "One row per receipt. Mark each one as you submit it and when it's paid back.")
header(ex, ["Date", "Category", "Description", "Client / project", "Amount", "Distance (mileage)", "Claim amount", "Receipt?", "Report no.", "Submitted", "Reimbursed on", "Status", "Days waiting"], [11, 18, 26, 16, 10, 12, 12, 9, 10, 11, 12, 12, 11])
samples = [(-62, "Travel", "Train to client meeting", "Acme", 48.6, None, "R-01", -55, -40), (-61, "Meals", "Lunch with client", "Acme", 64.0, None, "R-01", -55, -40), (-45, "Mileage", "Site visit return trip", "Northwind", None, 120, "R-02", -38, -20),
           (-44, "Parking & tolls", "Car park", "Northwind", 12.5, None, "R-02", -38, -20), (-30, "Hotel", "Conference hotel 2 nights", "Internal", 290, None, "R-03", -25, None), (-29, "Meals", "Conference dinner", "Internal", 38.4, None, "R-03", -25, None),
           (-28, "Travel", "Taxi to venue", "Internal", 22, None, "R-03", -25, None), (-12, "Supplies", "Printer ink", "Internal", 34.9, None, None, None, None), (-6, "Mileage", "Client workshop", "Globex", None, 86, None, None, None),
           (-3, "Client entertainment", "Coffee meeting", "Globex", 15.8, None, None, None, None)]
for r, (dd, c, de, cp, a, dist, rep, sub, reimb) in enumerate(samples, 4):
    ex[f"A{r}"] = today + dt.timedelta(days=dd); ex[f"B{r}"] = c; ex[f"C{r}"] = de; ex[f"D{r}"] = cp; ex[f"E{r}"] = a; ex[f"F{r}"] = dist; ex[f"H{r}"] = "Yes" if c != "Mileage" else "n/a"
    ex[f"I{r}"] = rep; ex[f"J{r}"] = today + dt.timedelta(days=sub) if sub else None; ex[f"K{r}"] = today + dt.timedelta(days=reimb) if reimb else None
dv(ex, '"' + ",".join(cats) + '"', "B4:B2000"); dv(ex, '"Yes,No,n/a"', "H4:H2000")
for r in range(4, 2001):
    for c in "AJK": ex[f"{c}{r}"].number_format = "dd mmm yy"
    ex[f"G{r}"] = f'=IF(B{r}="","",IF(B{r}="Mileage",N(F{r})*Settings!$B$7,N(E{r})))'
    ex[f"L{r}"] = f'=IF(B{r}="","",IF(K{r}<>"","Reimbursed",IF(J{r}<>"","Submitted","Not submitted")))'
    ex[f"M{r}"] = f'=IF(OR(J{r}="",K{r}<>""),"",TODAY()-J{r})'
    ex[f"E{r}"].number_format = ex[f"G{r}"].number_format = M
for s, col in [("Reimbursed", "D3F9D8"), ("Submitted", "D0EBFF"), ("Not submitted", "FFF3BF")]:
    ex.conditional_formatting.add("L4:L2000", CellIsRule(operator="equal", formula=[f'"{s}"'], fill=PatternFill("solid", fgColor=col)))
ex.conditional_formatting.add("H4:H2000", CellIsRule(operator="equal", formula=['"No"'], font=Font(bold=True, color="C0392B")))
ex.conditional_formatting.add("M4:M2000", CellIsRule(operator="greaterThan", formula=["30"], font=Font(bold=True, color="C0392B")))
rp = wb.create_sheet("Report", 1)
rp["A1"] = "Expense Claim"; rp["A1"].font = Font(bold=True, size=20, color=C)
for r, (n, f) in enumerate([("Employee", "=Settings!B4"), ("Department", "=Settings!B5"), ("Approver", "=Settings!B6"), ("Report no.", "R-03"), ("Date of claim", "=TODAY()")], 3):
    rp[f"A{r}"] = n; rp[f"A{r}"].font = Font(bold=True); rp[f"B{r}"] = f
rp["B6"].fill = SOFT; rp["B7"].number_format = "dd mmm yyyy"; rp["D6"] = "← type the report number to fill this claim"; rp["D6"].font = Font(italic=True, color="777777")
header(rp, ["No.", "Date", "Category", "Description", "Client / project", "Claim amount"], [6, 12, 18, 30, 18, 14], row=9, freeze=False)
for i in range(25):
    r = 10 + i; k = i + 1
    rp[f"A{r}"] = f'=IF(COUNTIF(Expenses!$I$4:$I$2000,$B$6)>={k},{k},"")'
    rowf = f'_xlfn.AGGREGATE(15,6,(ROW(Expenses!$I$4:$I$2000)-3)/(Expenses!$I$4:$I$2000=$B$6),{k})'
    for c, src in (("B", "A"), ("C", "B"), ("D", "C"), ("E", "D"), ("F", "G")):
        rp[f"{c}{r}"] = f'=IF($A{r}="","",INDEX(Expenses!${src}$4:${src}$2000,{rowf}))'
    rp[f"B{r}"].number_format = "dd mmm yy"; rp[f"F{r}"].number_format = M
rp["E36"] = "Total claimed"; rp["E36"].font = Font(bold=True); rp["F36"] = "=SUM(F10:F34)"; rp["F36"].number_format = M; rp["F36"].font = Font(bold=True, size=13, color=C)
rp["A39"] = "Employee signature: ______________________     Date: __________"; rp["A41"] = "Approved by: ______________________     Date: __________"
rp.print_area = "A1:F41"; rp.page_setup.fitToWidth = 1
db = wb.create_sheet("Summary", 0); title(db, "Expense Summary", "What you're owed and where the money went.")
kpis(db, [("Not yet submitted", '=SUMIFS(Expenses!G4:G2000,Expenses!L4:L2000,"Not submitted")', M), ("Submitted, waiting to be paid", '=SUMIFS(Expenses!G4:G2000,Expenses!L4:L2000,"Submitted")', M),
          ("Total owed to you", "=B4+B5", M), ("Reimbursed this year", '=SUMIFS(Expenses!G4:G2000,Expenses!K4:K2000,">="&DATE(YEAR(TODAY()),1,1))', M),
          ("Oldest unpaid claim (days)", '=IFERROR(MAX(Expenses!M4:M2000),0)', "0"), ("Missing receipts", '=COUNTIF(Expenses!H4:H2000,"No")', "0"),
          ("Average days to get paid", '=IFERROR(SUMPRODUCT((Expenses!K4:K2000<>"")*(Expenses!J4:J2000<>""),Expenses!K4:K2000-Expenses!J4:J2000)/SUMPRODUCT((Expenses!K4:K2000<>"")*(Expenses!J4:J2000<>"")),"")', "0")], start=4, wa=32)
db["B6"].font = Font(bold=True, size=13, color=C)
header(db, ["Category", "This year"], [32, 14], row=13, freeze=False)
for i, c in enumerate(cats):
    r = 14 + i; db[f"A{r}"] = c; db[f"B{r}"] = f'=SUMIFS(Expenses!$G$4:$G$2000,Expenses!$B$4:$B$2000,A{r},Expenses!$A$4:$A$2000,">="&DATE(YEAR(TODAY()),1,1))'; db[f"B{r}"].number_format = M
pc = PieChart(); pc.title = "Spending by category"; pc.height = 8; pc.width = 12
pc.add_data(Reference(db, min_col=2, min_row=13, max_row=23), titles_from_data=True); pc.set_categories(Reference(db, min_col=1, min_row=14, max_row=23)); db.add_chart(pc, "D3")
howto(wb, C, ["1. Settings: your name, department, approver and the mileage rate your employer pays.",
              "2. Expenses: one row per receipt with date, category, description, client or project and amount. For mileage enter the distance and the claim is worked out. Note whether you have the receipt.",
              "3. When you submit a claim, give those rows a report number (R-01, R-02...) and the date submitted. Add the date paid when the money arrives. Status and days waiting update, and claims waiting over 30 days turn red.",
              "4. Report: type a report number to get a printable claim form with every expense on it and the total.",
              "5. Summary: what you're owed, what's been paid back, the oldest unpaid claim, missing receipts and spending by category. Delete the sample data first."])
wb.save(OUT / "Expense-Report-Reimbursement-Tracker.xlsx")
print("built 5")
