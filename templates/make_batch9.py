"""Round 14 spreadsheet products into products/. Run: python3 make_batch9.py (reuses helpers from make_batch2.py)"""
import pathlib, random
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
from openpyxl.chart import PieChart
today = dt.date.today(); y = today.year
mon = today - dt.timedelta(days=today.weekday())
random.seed(14)
def kpis(ws, rows, start=4, wa=28, wb_=14):
    for r, (a, f, nf_) in enumerate(rows, start):
        ws[f"A{r}"] = a; ws[f"B{r}"] = f; ws[f"B{r}"].number_format = nf_; ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
    ws.column_dimensions["A"].width = wa; ws.column_dimensions["B"].width = wb_
def hrow(ws, row, cols, color):
    for c, h in cols:
        ws[f"{c}{row}"] = h; ws[f"{c}{row}"].font = Font(bold=True, color="FFFFFF"); ws[f"{c}{row}"].fill = PatternFill("solid", fgColor=color)

# 1. Reading tracker with stats
C = "862E9C"; title, header = kit(C); wb = Workbook(); bk = wb.active; bk.title = "Books"
title(bk, "Reading Tracker", "Every book you read or want to read. Stats and charts update automatically.")
header(bk, ["Title", "Author", "Genre", "Format", "Pages", "Status", "Started", "Finished", "Days", "Rating (1-5)", "Pages / day", "Favourite quote / notes"], [28, 20, 14, 11, 8, 12, 11, 11, 7, 11, 11, 30])
genres = ["Fiction", "Mystery", "Fantasy", "Sci-fi", "Romance", "Non-fiction", "Biography", "Self-help", "History", "Classic"]
books = [("The Long Way Home", "A. Rivers", "Fiction", 320), ("Murder at the Lighthouse", "J. Kell", "Mystery", 290), ("Starfall", "M. Oduya", "Sci-fi", 410), ("Tiny Habits, Big Wins", "R. Lane", "Self-help", 240),
         ("The Silk Road Years", "P. Novak", "History", 520), ("Ember Crown", "S. Vale", "Fantasy", 610), ("Letters to June", "E. Hart", "Romance", 300), ("Quiet Minds", "D. Osei", "Non-fiction", 280),
         ("Pride of the North", "C. Bronte-Hall", "Classic", 380), ("A Life in Colour", "L. Moreau", "Biography", 350), ("The Glass Detective", "J. Kell", "Mystery", 310), ("Orbit", "M. Oduya", "Sci-fi", 450)]
d = today - dt.timedelta(days=300)
for r, (t, a, g, p) in enumerate(books, 4):
    bk[f"A{r}"], bk[f"B{r}"], bk[f"C{r}"], bk[f"D{r}"], bk[f"E{r}"] = t, a, g, random.choice(["Paperback", "Ebook", "Audiobook", "Hardback"]), p
    if r < 14:
        bk[f"F{r}"] = "Finished"; bk[f"G{r}"] = d; d = d + dt.timedelta(days=random.randint(8, 30)); bk[f"H{r}"] = d; bk[f"J{r}"] = random.choice([3, 4, 4, 5, 5]); d += dt.timedelta(days=2)
    elif r == 14: bk[f"F{r}"] = "Reading"; bk[f"G{r}"] = today - dt.timedelta(days=5)
    else: bk[f"F{r}"] = "Want to read"
dv(bk, '"' + ",".join(genres) + ',Other"', "C4:C2000"); dv(bk, '"Paperback,Hardback,Ebook,Audiobook"', "D4:D2000"); dv(bk, '"Want to read,Reading,Finished,Did not finish"', "F4:F2000"); dv(bk, '"1,2,3,4,5"', "J4:J2000")
for r in range(4, 2001):
    bk[f"G{r}"].number_format = bk[f"H{r}"].number_format = "dd mmm yy"
    bk[f"I{r}"] = f'=IF(OR(G{r}="",H{r}=""),"",H{r}-G{r}+1)'; bk[f"K{r}"] = f'=IF(OR(I{r}="",N(E{r})=0),"",E{r}/I{r})'; bk[f"K{r}"].number_format = "0"
for s, col in [("Finished", "D3F9D8"), ("Reading", "FFF3BF"), ("Did not finish", "F1F3F5")]:
    bk.conditional_formatting.add("F4:F2000", CellIsRule(operator="equal", formula=[f'"{s}"'], fill=PatternFill("solid", fgColor=col)))
bk.conditional_formatting.add("J4:J2000", CellIsRule(operator="equal", formula=["5"], font=Font(bold=True, color="E67700")))
st = wb.create_sheet("Stats", 0); title(st, "Reading Stats", "Pick a year. Counts use the Finished date.")
st["A3"] = "Year"; st["B3"] = y; st["B3"].fill = SOFT; st["A3"].font = Font(bold=True)
F = 'Books!$H$4:$H$2000,">="&DATE($B$3,1,1),Books!$H$4:$H$2000,"<"&DATE($B$3+1,1,1)'
kpis(st, [("Reading goal (books)", 24, "0"), ("Books finished", f"=COUNTIFS({F})", "0"), ("Progress to goal", "=IFERROR(B5/B4,0)", "0%"), ("Pages read", f"=SUMIFS(Books!$E$4:$E$2000,{F})", "#,##0"),
          ("Average rating", f'=IFERROR(AVERAGEIFS(Books!$J$4:$J$2000,{F}),"")', "0.0"), ("Average days per book", f'=IFERROR(AVERAGEIFS(Books!$I$4:$I$2000,{F}),"")', "0"),
          ("On track? (books by today)", '=IF(B3<>YEAR(TODAY()),"",ROUND(B4*(TODAY()-DATE(B3,1,1))/365,0))', "0"), ("Currently reading", '=COUNTIF(Books!F4:F2000,"Reading")', "0"), ("To-read pile", '=COUNTIF(Books!F4:F2000,"Want to read")', "0")])
st["B4"].fill = PatternFill("solid", fgColor="F3D9FA")
st.conditional_formatting.add("B6", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="DA77F2"))
header(st, ["Month", "Books", "Pages"], [28, 14, 10], row=15, freeze=False)
for i, m in enumerate(MONTHS):
    r = 16 + i; st[f"A{r}"] = m
    cond = f'Books!$H$4:$H$2000,">="&DATE($B$3,{i + 1},1),Books!$H$4:$H$2000,"<"&DATE($B$3,{i + 2},1)'
    st[f"B{r}"] = f"=COUNTIFS({cond})"; st[f"C{r}"] = f"=SUMIFS(Books!$E$4:$E$2000,{cond})"; st[f"C{r}"].number_format = "#,##0"
hrow(st, 15, [("E", "Genre"), ("F", "Books")], C); st.column_dimensions["E"].width = 14; st.column_dimensions["F"].width = 8
for i, g in enumerate(genres):
    st[f"E{16 + i}"] = g; st[f"F{16 + i}"] = f"=COUNTIFS(Books!$C$4:$C$2000,E{16 + i},{F})"
bc = BarChart(); bc.title = "Books per month"; bc.height = 7; bc.width = 16; bc.legend = None
bc.add_data(Reference(st, min_col=2, min_row=15, max_row=27), titles_from_data=True); bc.set_categories(Reference(st, min_col=1, min_row=16, max_row=27)); st.add_chart(bc, "H3")
pc = PieChart(); pc.title = "Genres"; pc.height = 7; pc.width = 11
pc.add_data(Reference(st, min_col=6, min_row=15, max_row=25), titles_from_data=True); pc.set_categories(Reference(st, min_col=5, min_row=16, max_row=25)); st.add_chart(pc, "H18")
howto(wb, C, ["1. Books: add every book with title, author, genre, format and pages. Set the status and fill in start and finish dates as you go. Days taken and pages per day are worked out for you.",
              "2. Stats: type the year and your reading goal. See books finished, progress, pages, average rating, how many you should have read by today, a monthly chart and your genre mix.",
              "3. Keep your to-read list in the same table with status 'Want to read'. Delete the sample books first."])
wb.save(OUT / "Reading-Tracker-Stats.xlsx")

# 2. Sleep tracker
C = "3B5BDB"; title, header = kit(C); wb = Workbook(); lg = wb.active; lg.title = "Sleep log"
title(lg, "Sleep Log", "One row per night. Hours slept and averages are worked out for you.")
header(lg, ["Night of", "Bedtime", "Fell asleep (mins)", "Wake time", "Hours asleep", "Quality (1-5)", "Times woke", "Caffeine after 2pm?", "Screen in bed?", "Exercise?", "Notes"], [12, 9, 15, 10, 12, 12, 11, 17, 13, 10, 26])
for k in range(28):
    r = 4 + k; dd = today - dt.timedelta(days=28 - k)
    bh = random.choice([22, 22, 23, 23, 23, 0]); bm = random.choice([0, 15, 30, 45])
    lg[f"A{r}"] = dd; lg[f"B{r}"] = dt.time(bh, bm); lg[f"C{r}"] = random.choice([5, 10, 15, 20, 30, 45]); lg[f"D{r}"] = dt.time(random.choice([6, 7, 7, 8]), random.choice([0, 15, 30, 45]))
    lg[f"G{r}"] = random.choice([0, 0, 1, 1, 2]); caf = random.random() < 0.3; scr = random.random() < 0.4
    lg[f"H{r}"] = "Yes" if caf else "No"; lg[f"I{r}"] = "Yes" if scr else "No"; lg[f"J{r}"] = random.choice(["Yes", "No"])
    lg[f"F{r}"] = max(1, min(5, 4 - caf - scr + random.choice([0, 0, 1, -1])))
dv(lg, '"1,2,3,4,5"', "F4:F1500"); dv(lg, '"Yes,No"', "H4:J1500")
for r in range(4, 1501):
    lg[f"A{r}"].number_format = "ddd dd mmm"; lg[f"B{r}"].number_format = lg[f"D{r}"].number_format = "hh:mm"
    lg[f"E{r}"] = f'=IF(OR(B{r}="",D{r}=""),"",ROUND((MOD(D{r}-B{r},1))*24-N(C{r})/60,2))'; lg[f"E{r}"].number_format = "0.0"
lg.conditional_formatting.add("E4:E1500", CellIsRule(operator="lessThan", formula=["6"], font=Font(bold=True, color="C0392B")))
lg.conditional_formatting.add("E4:E1500", CellIsRule(operator="greaterThanOrEqual", formula=["7"], font=Font(color="2B8A3E")))
lg.conditional_formatting.add("F4:F1500", ColorScaleRule := __import__("openpyxl").formatting.rule.ColorScaleRule(start_type="num", start_value=1, start_color="FFC9C9", end_type="num", end_value=5, end_color="B2F2BB"))
sm = wb.create_sheet("Summary", 0); title(sm, "Sleep Summary", "How you're sleeping and what seems to help.")
L7 = 'Sleep log!$A$4:$A$1500'
kpis(sm, [("Sleep goal (hours)", 8, "0.0"), ("Average hours (all)", "=IFERROR(AVERAGE('Sleep log'!E4:E1500),0)", "0.0"), ("Average hours (last 7 nights)", "=IFERROR(AVERAGEIFS('Sleep log'!E4:E1500,'Sleep log'!A4:A1500,\">=\"&TODAY()-7),0)", "0.0"),
          ("Average quality (1-5)", "=IFERROR(AVERAGE('Sleep log'!F4:F1500),0)", "0.0"), ("Nights logged", "=COUNT('Sleep log'!E4:E1500)", "0"), ("Nights meeting goal", "=COUNTIF('Sleep log'!E4:E1500,\">=\"&B4)", "0"),
          ("Sleep debt last 7 nights (h)", "=MAX(0,B4*COUNTIFS('Sleep log'!A4:A1500,\">=\"&TODAY()-7,'Sleep log'!E4:E1500,\"<>\")-SUMIFS('Sleep log'!E4:E1500,'Sleep log'!A4:A1500,\">=\"&TODAY()-7))", "0.0"),
          ("Average time to fall asleep (mins)", "=IFERROR(AVERAGE('Sleep log'!C4:C1500),0)", "0")], wa=34)
sm["B4"].fill = PatternFill("solid", fgColor="DBE4FF")
header(sm, ["What affects my sleep", "Avg hours (Yes)", "Avg hours (No)", "Avg quality (Yes)", "Avg quality (No)"], [34, 14, 14, 15, 15], row=14, freeze=False)
for i, (lab, col) in enumerate([("Caffeine after 2pm", "H"), ("Screen in bed", "I"), ("Exercise that day", "J")]):
    r = 15 + i; sm[f"A{r}"] = lab
    for c, src, v in (("B", "E", "Yes"), ("C", "E", "No"), ("D", "F", "Yes"), ("E", "F", "No")):
        sm[f"{c}{r}"] = f"=IFERROR(AVERAGEIFS('Sleep log'!${src}$4:${src}$1500,'Sleep log'!${col}$4:${col}$1500,\"{v}\"),\"\")"; sm[f"{c}{r}"].number_format = "0.0"
header(sm, ["Weekday", "Avg hours", "Avg quality"], [34, 14, 14], row=19, freeze=False)
for i, dn in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
    r = 20 + i; sm[f"A{r}"] = dn
    sm[f"B{r}"] = f"=IFERROR(SUMPRODUCT((WEEKDAY('Sleep log'!$A$4:$A$1500,2)={i + 1})*('Sleep log'!$A$4:$A$1500<>\"\"),'Sleep log'!$E$4:$E$1500)/SUMPRODUCT((WEEKDAY('Sleep log'!$A$4:$A$1500,2)={i + 1})*('Sleep log'!$A$4:$A$1500<>\"\")*ISNUMBER('Sleep log'!$E$4:$E$1500)),\"\")"
    sm[f"C{r}"] = f"=IFERROR(SUMPRODUCT((WEEKDAY('Sleep log'!$A$4:$A$1500,2)={i + 1})*('Sleep log'!$A$4:$A$1500<>\"\"),'Sleep log'!$F$4:$F$1500)/SUMPRODUCT((WEEKDAY('Sleep log'!$A$4:$A$1500,2)={i + 1})*('Sleep log'!$A$4:$A$1500<>\"\")*ISNUMBER('Sleep log'!$F$4:$F$1500)),\"\")"
    sm[f"B{r}"].number_format = sm[f"C{r}"].number_format = "0.0"
lc = LineChart(); lc.title = "Hours asleep"; lc.height = 8; lc.width = 20; lc.legend = None
lc.add_data(Reference(lg, min_col=5, min_row=3, max_row=31), titles_from_data=True); lc.set_categories(Reference(lg, min_col=1, min_row=4, max_row=31)); sm.add_chart(lc, "G3")
sm["A28"] = "A personal tracker, not medical advice. If you're often exhausted or snore loudly, talk to a doctor."; sm["A28"].font = Font(italic=True, color="777777")
howto(wb, C, ["1. Sleep log: each morning, enter last night's bedtime, roughly how long it took to fall asleep, your wake time and how well you slept. Hours asleep are worked out for you (past midnight is fine).",
              "2. Tick the habits (caffeine after 2pm, screen in bed, exercise) to see on the Summary tab which ones change your sleep.", "3. Summary: averages, last 7 nights, sleep debt against your goal, nights meeting your goal, best and worst weekdays and a chart.", "4. Delete the sample nights first."])
wb.save(OUT / "Sleep-Tracker.xlsx")

# 3. Short-let host tracker
C = "E8590C"; title, header = kit(C); wb = Workbook(); st = wb.active; st.title = "Settings"
title(st, "Your listing", "Fill these in once.")
for r, (n, v) in enumerate([("Property name", "Seaside Flat"), ("Platform fee (host side)", 0.03), ("Cleaning cost per stay", 35), ("Year", y)], 4):
    st[f"A{r}"] = n; st[f"B{r}"] = v; st[f"A{r}"].font = Font(bold=True); st[f"B{r}"].fill = SOFT
st["B5"].number_format = "0%"; st["B6"].number_format = M; st.column_dimensions["A"].width = 26; st.column_dimensions["B"].width = 18
bkg = wb.create_sheet("Bookings", 0); title(bkg, "Bookings", "One row per stay. Nights, net payout and nightly rate are worked out for you.")
header(bkg, ["Guest", "Platform", "Check-in", "Check-out", "Nights", "Guests", "Booking total", "Cleaning fee charged", "Platform fee", "Cleaning cost", "Net", "Per night", "Review", "Notes"], [16, 12, 11, 11, 8, 8, 13, 13, 12, 12, 11, 10, 9, 22])
d = dt.date(y, 1, 3)
while d < dt.date(y, 12, 20):
    n = random.choice([2, 3, 3, 4, 5, 7]); r = bkg.max_row + 1 if bkg.max_row >= 4 else 4
    bkg[f"A{r}"] = random.choice(["Emma", "Lukas", "Sofia", "James", "Chen", "Aylin", "Mateo", "Olivia", "Noor"]) + " " + random.choice("ABCDEFGHKLMNPRST") + "."
    bkg[f"B{r}"] = random.choice(["Airbnb", "Airbnb", "Booking.com", "Direct"]); bkg[f"C{r}"] = d; bkg[f"D{r}"] = d + dt.timedelta(days=n); bkg[f"F{r}"] = random.choice([2, 2, 3, 4])
    rate = 95 if d.month in (6, 7, 8) else 70; bkg[f"G{r}"] = rate * n; bkg[f"H{r}"] = 40; bkg[f"M{r}"] = random.choice([5, 5, 5, 4, None])
    d = d + dt.timedelta(days=n + random.choice([1, 3, 5, 8, 12]))
last_s = bkg.max_row
dv(bkg, '"Airbnb,Booking.com,Vrbo,Direct,Other"', "B4:B1000"); dv(bkg, '"1,2,3,4,5"', "M4:M1000")
for r in range(4, 1001):
    bkg[f"C{r}"].number_format = bkg[f"D{r}"].number_format = "dd mmm"
    bkg[f"E{r}"] = f'=IF(OR(C{r}="",D{r}=""),"",D{r}-C{r})'
    bkg[f"I{r}"] = f'=IF(A{r}="","",IF(B{r}="Direct",0,(N(G{r})+N(H{r}))*Settings!$B$5))'
    bkg[f"J{r}"] = f'=IF(A{r}="","",Settings!$B$6)'
    bkg[f"K{r}"] = f'=IF(A{r}="","",N(G{r})+N(H{r})-I{r}-J{r})'
    bkg[f"L{r}"] = f'=IF(OR(A{r}="",N(E{r})=0),"",G{r}/E{r})'
    for c in "GHIJKL": bkg[f"{c}{r}"].number_format = M
bkg.freeze_panes = "B4"
ex = wb.create_sheet("Expenses", 1); title(ex, "Running costs", "Bills, supplies and repairs for the property.")
header(ex, ["Date", "Category", "Description", "Amount"], [12, 16, 28, 12])
for r, (m, c, de, a) in enumerate([(1, "Supplies", "Toiletries & coffee", 45), (2, "Utilities", "Electricity & water", 120), (3, "Repairs", "Shower head", 30), (4, "Insurance", "Host insurance", 240), (5, "Utilities", "Internet", 35), (6, "Furnishing", "New towels", 80)], 4):
    ex[f"A{r}"] = dt.date(y, m, 10); ex[f"B{r}"] = c; ex[f"C{r}"] = de; ex[f"D{r}"] = a
dv(ex, '"Supplies,Utilities,Repairs,Insurance,Furnishing,Tax,Mortgage / rent,Other"', "B4:B1000")
for r in range(4, 1001): ex[f"A{r}"].number_format = "dd mmm yy"; ex[f"D{r}"].number_format = M
db = wb.create_sheet("Dashboard", 0); db["A1"] = '=Settings!B4&" · "&Settings!B7'; db["A1"].font = Font(bold=True, size=18, color=C); db["A2"] = "Occupancy, income and costs for the year."; db["A2"].font = Font(italic=True, color="777777")
B = 'Bookings!$C$4:$C$1000,">="&DATE(Settings!$B$7,1,1),Bookings!$C$4:$C$1000,"<"&DATE(Settings!$B$7+1,1,1)'
kpis(db, [("Stays", f"=COUNTIFS({B})", "0"), ("Nights booked", f"=SUMIFS(Bookings!$E$4:$E$1000,{B})", "0"), ("Occupancy", "=B5/(DATE(Settings!B7+1,1,1)-DATE(Settings!B7,1,1))", "0%"),
          ("Average nightly rate", f"=IFERROR(SUMIFS(Bookings!$G$4:$G$1000,{B})/B5,0)", M), ("Net from bookings", f"=SUMIFS(Bookings!$K$4:$K$1000,{B})", M),
          ("Running costs", '=SUMIFS(Expenses!$D$4:$D$1000,Expenses!$A$4:$A$1000,">="&DATE(Settings!$B$7,1,1),Expenses!$A$4:$A$1000,"<"&DATE(Settings!$B$7+1,1,1))', M), ("Profit", "=B8-B9", M),
          ("Average review", f'=IFERROR(AVERAGEIFS(Bookings!$M$4:$M$1000,{B}),"")', "0.0"), ("Average stay (nights)", "=IFERROR(B5/B4,0)", "0.0")])
db["B10"].font = Font(bold=True, size=13, color=C)
header(db, ["Month", "Nights", "Occupancy", "Net income"], [28, 14, 11, 13], row=15, freeze=False)
for i, m in enumerate(MONTHS):
    r = 16 + i; db[f"A{r}"] = m
    cond = f'Bookings!$C$4:$C$1000,">="&DATE(Settings!$B$7,{i + 1},1),Bookings!$C$4:$C$1000,"<"&DATE(Settings!$B$7,{i + 2},1)'
    db[f"B{r}"] = f"=SUMIFS(Bookings!$E$4:$E$1000,{cond})"; db[f"C{r}"] = f"=MIN(1,B{r}/DAY(DATE(Settings!$B$7,{i + 2},0)))"; db[f"C{r}"].number_format = "0%"
    db[f"D{r}"] = f"=SUMIFS(Bookings!$K$4:$K$1000,{cond})"; db[f"D{r}"].number_format = M
db.conditional_formatting.add("C16:C27", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="FFA94D"))
bc = BarChart(); bc.title = "Net income by month"; bc.height = 7; bc.width = 18; bc.legend = None
bc.add_data(Reference(db, min_col=4, min_row=15, max_row=27), titles_from_data=True); bc.set_categories(Reference(db, min_col=1, min_row=16, max_row=27)); db.add_chart(bc, "F3")
howto(wb, C, ["1. Settings: property name, the host fee your platform charges, what each clean costs you and the year.", "2. Bookings: one row per stay with platform, dates, guests, booking total and cleaning fee charged. Nights, platform fee, net payout and nightly rate are worked out (direct bookings have no platform fee).",
              "3. Expenses: bills, supplies, repairs and insurance.", "4. Dashboard: occupancy, average nightly rate, net income, costs, profit, reviews and month-by-month occupancy. Stays count in the month they check in.",
              "5. Check your platform's real fee structure and local tax rules. Delete the sample data first."])
wb.save(OUT / "Short-Let-Host-Tracker.xlsx")

# 4. OKR & goal tracker
C = "0B7285"; title, header = kit(C); wb = Workbook(); ok = wb.active; ok.title = "Goals"
title(ok, "Goals & Key Results", "Set up to 5 goals per quarter, each with measurable key results. Progress fills in as you update the current value.")
ok["A3"] = "Quarter"; ok["B3"] = f"Q{(today.month - 1) // 3 + 1} {y}"; ok["B3"].fill = SOFT; ok["A3"].font = Font(bold=True)
header(ok, ["Goal (objective)", "Key result", "Start", "Target", "Current", "Progress", "Confidence", "Owner", "Due", "Status", "Notes"], [30, 34, 9, 9, 9, 10, 12, 12, 11, 13, 24], row=5)
goals = [("Grow the business", [("Monthly revenue", 2000, 3500, 2600), ("New clients", 0, 6, 3), ("Website visitors per month", 800, 2000, 1250)]),
         ("Get fitter", [("Run 5K under (minutes)", 32, 27, 29.5), ("Workouts per week", 1, 4, 3)]),
         ("Learn Spanish", [("Duolingo streak (days)", 0, 90, 41), ("Conversation lessons", 0, 12, 4)]),
         ("Save more", [("Emergency fund", 1000, 3000, 1800), ("Spending cut per month", 0, 200, 150)])]
r = 6
for g, krs in goals:
    for kr, s, t, c in krs:
        ok[f"A{r}"], ok[f"B{r}"], ok[f"C{r}"], ok[f"D{r}"], ok[f"E{r}"] = g, kr, s, t, c; ok[f"G{r}"] = random.choice(["High", "Medium", "Medium", "Low"]); ok[f"H{r}"] = "Me"; ok[f"I{r}"] = dt.date(y, ((today.month - 1) // 3 + 1) * 3, 28) if today.month < 12 else dt.date(y, 12, 28); r += 1
dv(ok, '"High,Medium,Low"', "G6:G60")
for r in range(6, 61):
    ok[f"F{r}"] = f'=IF(OR(B{r}="",D{r}="",D{r}=C{r}),"",MAX(0,MIN(1,(N(E{r})-N(C{r}))/(D{r}-C{r}))))'; ok[f"F{r}"].number_format = "0%"
    ok[f"I{r}"].number_format = "dd mmm"
    ok[f"J{r}"] = f'=IF(F{r}="","",IF(F{r}>=1,"Done",IF(F{r}>=0.7,"On track",IF(F{r}>=0.4,"At risk","Off track"))))'
ok.conditional_formatting.add("F6:F60", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="3BC9DB"))
for s, col in [("Done", "B2F2BB"), ("On track", "D3F9D8"), ("At risk", "FFE8CC"), ("Off track", "FFC9C9")]:
    ok.conditional_formatting.add("J6:J60", CellIsRule(operator="equal", formula=[f'"{s}"'], fill=PatternFill("solid", fgColor=col)))
sm = wb.create_sheet("Summary", 0); title(sm, "Goal Summary", "Each goal's progress is the average of its key results.")
header(sm, ["Goal", "Key results", "Average progress", "Off track / at risk"], [30, 13, 16, 18], freeze=False)
for i, (g, _) in enumerate(goals + [("", [])] * 6):
    r = 4 + i
    if g: sm[f"A{r}"] = g
    sm[f"B{r}"] = f'=IF(A{r}="","",COUNTIF(Goals!$A$6:$A$60,A{r}))'
    sm[f"C{r}"] = f'=IF(OR(A{r}="",B{r}=0),"",AVERAGEIF(Goals!$A$6:$A$60,A{r},Goals!$F$6:$F$60))'; sm[f"C{r}"].number_format = "0%"
    sm[f"D{r}"] = f'=IF(A{r}="","",COUNTIFS(Goals!$A$6:$A$60,A{r},Goals!$J$6:$J$60,"Off track")+COUNTIFS(Goals!$A$6:$A$60,A{r},Goals!$J$6:$J$60,"At risk"))'
sm.conditional_formatting.add("C4:C13", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="3BC9DB"))
sm["A15"] = "Overall progress"; sm["A15"].font = Font(bold=True); sm["C15"] = '=IFERROR(AVERAGE(Goals!F6:F60),0)'; sm["C15"].number_format = "0%"; sm["C15"].font = Font(bold=True, size=13, color=C)
sm["A16"] = "Key results done"; sm["C16"] = '=COUNTIF(Goals!J6:J60,"Done")'
bc = BarChart(); bc.type = "bar"; bc.title = "Progress by goal"; bc.height = 7; bc.width = 16; bc.legend = None
bc.add_data(Reference(sm, min_col=3, min_row=3, max_row=7), titles_from_data=True); bc.set_categories(Reference(sm, min_col=1, min_row=4, max_row=7)); bc.y_axis.scaling.min = 0; bc.y_axis.scaling.max = 1; sm.add_chart(bc, "F3")
ci = wb.create_sheet("Weekly check-in"); title(ci, "Weekly check-in", "Five minutes every week keeps goals alive.")
header(ci, ["Week of", "Biggest win", "What got in the way", "Focus next week", "Energy (1-5)"], [12, 30, 30, 30, 12])
for r in range(4, 60): ci[f"A{r}"] = f"=A{r - 1}+7" if r > 4 else mon; ci[f"A{r}"].number_format = "dd mmm"
dv(ci, '"1,2,3,4,5"', "E4:E59")
howto(wb, C, ["1. Goals: write each goal (objective) on several rows, one per key result. Give every key result a start value, a target and the current value. Lower-is-better targets (like a race time) work too.",
              "2. Progress and status fill in automatically: Done, On track (70%+), At risk (40%+) or Off track. Update the current values every week or two.",
              "3. Summary shows each goal's average progress and how many key results need attention. Use the Weekly check-in to reflect.", "4. Works for personal goals, teams and small businesses. Copy the file for each new quarter. Delete the sample goals first."])
wb.save(OUT / "OKR-Goal-Tracker.xlsx")

# 5. Teacher gradebook
C = "C2255C"; title, header = kit(C); wb = Workbook(); stg = wb.active; stg.title = "Settings"
title(stg, "Grade boundaries", "Percentage needed for each grade. Change to match your school.")
header(stg, ["From %", "Grade"], [10, 10], freeze=False)
for r, (p, g) in enumerate([(0, "F"), (0.5, "E"), (0.6, "D"), (0.7, "C"), (0.8, "B"), (0.9, "A")], 4):
    stg[f"A{r}"] = p; stg[f"B{r}"] = g; stg[f"A{r}"].number_format = "0%"
stg["D4"] = "Keep the list in ascending order. The lowest must be 0%."; stg["D4"].font = Font(italic=True, color="777777")
gb = wb.create_sheet("Gradebook", 0); title(gb, "Class Gradebook", "Enter each assignment's max score and weight, then the students' scores.")
gb["A3"] = "Class"; gb["B3"] = "Year 9 Science"; gb["B3"].fill = SOFT; gb["A3"].font = Font(bold=True)
NA = 12; first = 3
for lab_, rr in (("Assignment", 5), ("Type", 6), ("Max score", 7), ("Weight", 8), ("Class average", 9)):
    gb[f"A{rr}"] = lab_; gb[f"A{rr}"].font = Font(bold=True)
asg = [("Cells quiz", "Quiz", 20, 1), ("Lab report 1", "Lab", 30, 2), ("Homework 1", "Homework", 10, 1), ("Forces test", "Test", 50, 3), ("Homework 2", "Homework", 10, 1), ("Project", "Project", 40, 3)]
for j in range(NA):
    cl = L(first + j); gb.column_dimensions[cl].width = 11
    if j < len(asg):
        gb[f"{cl}5"], gb[f"{cl}6"], gb[f"{cl}7"], gb[f"{cl}8"] = asg[j]
    for rr in (5, 6): gb[f"{cl}{rr}"].fill = PatternFill("solid", fgColor="FCE4EC"); gb[f"{cl}{rr}"].alignment = Alignment(horizontal="center", wrap_text=True)
    gb[f"{cl}9"] = f'=IF({cl}5="","",IFERROR(AVERAGE({cl}11:{cl}50)/{cl}7,""))'; gb[f"{cl}9"].number_format = "0%"
dv(gb, '"Quiz,Test,Homework,Lab,Project,Essay,Participation"', f"{L(first)}6:{L(first + NA - 1)}6")
lastc = L(first + NA - 1); tc = first + NA
for i, h in enumerate(["Weighted %", "Grade", "Missing"]):
    x = gb.cell(10, tc + i, h); x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=C); gb.column_dimensions[L(tc + i)].width = 12
x = gb.cell(10, 1, "Student"); x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=C)
x = gb.cell(10, 2, "Notes"); x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=C)
for j in range(NA): x = gb.cell(10, first + j, f'=IF({L(first + j)}5="","",{L(first + j)}5)'); x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=C)
gb.column_dimensions["A"].width = 20; gb.column_dimensions["B"].width = 14
names = ["Amelia", "Ben", "Chloe", "Daniel", "Eva", "Finn", "Grace", "Harry", "Isla", "Jack", "Kai", "Lily", "Mason", "Nora", "Oscar", "Poppy", "Ruby", "Sam"]
WP, GR, MS = L(tc), L(tc + 1), L(tc + 2)
for i in range(40):
    r = 11 + i
    if i < len(names):
        gb[f"A{r}"] = names[i]; skill = random.uniform(0.45, 0.98)
        for j, (_, _, mx, _) in enumerate(asg):
            if random.random() > 0.05: gb.cell(r, first + j, round(min(mx, max(0, mx * random.gauss(skill, 0.08)))))
    rng = f"{L(first)}{r}:{lastc}{r}"
    gb[f"{WP}{r}"] = f'=IF(OR(A{r}="",COUNT({rng})=0),"",SUMPRODUCT({rng}/({L(first)}$7:{lastc}$7+({L(first)}$7:{lastc}$7=0)),{L(first)}$8:{lastc}$8*ISNUMBER({rng}))/SUMPRODUCT({L(first)}$8:{lastc}$8*ISNUMBER({rng})))'
    gb[f"{WP}{r}"].number_format = "0%"
    gb[f"{GR}{r}"] = f'=IF({WP}{r}="","",LOOKUP({WP}{r},Settings!$A$4:$A$20,Settings!$B$4:$B$20))'
    gb[f"{MS}{r}"] = f'=IF(A{r}="","",SUMPRODUCT(({L(first)}$5:{lastc}$5<>"")*(ISBLANK({rng}))))'
gb.conditional_formatting.add(f"{WP}11:{WP}50", CellIsRule(operator="lessThan", formula=["0.6"], font=Font(bold=True, color="C0392B")))
gb.conditional_formatting.add(f"{MS}11:{MS}50", CellIsRule(operator="greaterThan", formula=["0"], fill=PatternFill("solid", fgColor="FFF3BF")))
gb.conditional_formatting.add(f"{L(first)}11:{lastc}50", FormulaRule(formula=[f'AND(ISNUMBER({L(first)}11),{L(first)}$7>0,{L(first)}11/{L(first)}$7<0.5)'], font=Font(color="C0392B")))
gb.freeze_panes = gb.cell(11, first)
sm = wb.create_sheet("Class summary", 1); title(sm, "Class summary", "Updates from the Gradebook.")
kpis(sm, [("Students", "=COUNTA(Gradebook!A11:A50)", "0"), ("Class average", f"=IFERROR(AVERAGE(Gradebook!{WP}11:{WP}50),0)", "0%"), ("Highest", f"=MAX(Gradebook!{WP}11:{WP}50)", "0%"), ("Lowest", f'=IFERROR(SMALL(Gradebook!{WP}11:{WP}50,1),"")', "0%"),
          ("Students below 60%", f'=COUNTIF(Gradebook!{WP}11:{WP}50,"<0.6")', "0"), ("Missing pieces of work", f"=SUM(Gradebook!{MS}11:{MS}50)", "0")])
header(sm, ["Grade", "Students"], [28, 14], row=12, freeze=False)
for i in range(6):
    r = 13 + i; sm[f"A{r}"] = f"=INDEX(Settings!$B$4:$B$9,{6 - i})"; sm[f"B{r}"] = f"=COUNTIF(Gradebook!${GR}$11:${GR}$50,A{r})"
bc = BarChart(); bc.title = "Grade distribution"; bc.height = 7; bc.width = 14; bc.legend = None
bc.add_data(Reference(sm, min_col=2, min_row=12, max_row=18), titles_from_data=True); bc.set_categories(Reference(sm, min_col=1, min_row=13, max_row=18)); sm.add_chart(bc, "D3")
howto(wb, C, ["1. Settings: set your grade boundaries (percentage needed for each grade).", "2. Gradebook: name the class, then for each assignment enter its name, type, max score and weight (e.g. tests count 3, homework 1). Up to 12 assignments and 40 students.",
              "3. Enter scores. Leave a cell empty if work is missing: it's counted as missing, not as zero, and doesn't drag the average down. Type 0 if the work was submitted and scored zero.",
              "4. Weighted % and grade fill in for each student. Below 60% shows in red. Class summary shows averages and grade distribution.", "5. Copy the Gradebook tab for each class or term. Delete the sample students first."])
wb.save(OUT / "Teacher-Gradebook.xlsx")
print("built 5")
