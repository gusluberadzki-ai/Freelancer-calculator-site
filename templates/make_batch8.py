"""Round 13 spreadsheet products into products/. Run: python3 make_batch8.py (reuses helpers from make_batch2.py)"""
import pathlib, random
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
from openpyxl.chart import PieChart
today = dt.date.today(); y = today.year
mon = today - dt.timedelta(days=today.weekday())
random.seed(13)
def kpis(ws, rows, start=4, wa=28, wb_=14):
    for r, (a, f, nf_) in enumerate(rows, start):
        ws[f"A{r}"] = a; ws[f"B{r}"] = f; ws[f"B{r}"].number_format = nf_; ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
    ws.column_dimensions["A"].width = wa; ws.column_dimensions["B"].width = wb_

# 1. Home inventory for insurance
C = "495057"; title, header = kit(C); wb = Workbook(); inv = wb.active; inv.title = "Inventory"
title(inv, "Home Inventory", "Everything you own, room by room. Handy for insurance claims, moving and wills.")
header(inv, ["Item", "Room", "Category", "Brand / model", "Serial number", "Bought", "Price paid", "Replacement value", "Receipt?", "Photo?", "Warranty until", "Notes"], [24, 13, 14, 18, 15, 11, 12, 15, 9, 8, 13, 22])
rooms = ["Living room", "Kitchen", "Bedroom 1", "Bedroom 2", "Bathroom", "Office", "Garage", "Garden"]
cats = ["Electronics", "Furniture", "Appliances", "Jewellery", "Clothing", "Art & decor", "Tools", "Sports", "Other"]
items = [("TV 55\"", "Living room", "Electronics", "Sony Bravia", 1, 900, 750), ("Sofa", "Living room", "Furniture", "3-seater", 3, 1200, 1300), ("Laptop", "Office", "Electronics", "MacBook Air", 1, 1100, 1000),
         ("Fridge freezer", "Kitchen", "Appliances", "Bosch", 2, 650, 700), ("Washing machine", "Kitchen", "Appliances", "Samsung", 4, 450, 480), ("Engagement ring", "Bedroom 1", "Jewellery", "", 6, 2500, 3200),
         ("Bed & mattress", "Bedroom 1", "Furniture", "King size", 5, 900, 950), ("Road bike", "Garage", "Sports", "Trek", 2, 850, 800), ("Drill set", "Garage", "Tools", "Bosch", 3, 120, 130), ("Office chair", "Office", "Furniture", "Ergonomic", 1, 280, 300)]
for r, (it, rm, ca, bm, ya, pp, rv) in enumerate(items, 4):
    inv[f"A{r}"], inv[f"B{r}"], inv[f"C{r}"], inv[f"D{r}"] = it, rm, ca, bm
    inv[f"F{r}"] = today - dt.timedelta(days=365 * ya + random.randint(0, 200)); inv[f"G{r}"], inv[f"H{r}"] = pp, rv
    inv[f"I{r}"] = random.choice(["Yes", "No"]); inv[f"J{r}"] = random.choice(["Yes", "Yes", "No"])
    if ca in ("Electronics", "Appliances"): inv[f"K{r}"] = inv[f"F{r}"].value + dt.timedelta(days=365 * 3)
dv(inv, '"' + ",".join(rooms) + ',Other"', "B4:B2000"); dv(inv, '"' + ",".join(cats) + '"', "C4:C2000"); dv(inv, '"Yes,No"', "I4:J2000")
for r in range(4, 2001):
    inv[f"F{r}"].number_format = inv[f"K{r}"].number_format = "mmm yyyy"; inv[f"G{r}"].number_format = inv[f"H{r}"].number_format = M
inv.conditional_formatting.add("I4:J2000", CellIsRule(operator="equal", formula=['"No"'], fill=PatternFill("solid", fgColor="FFE3E3")))
inv.conditional_formatting.add("K4:K2000", FormulaRule(formula=['AND(K4<>"",K4<TODAY())'], font=Font(color="999999")))
inv.conditional_formatting.add("K4:K2000", FormulaRule(formula=['AND(K4<>"",K4>=TODAY(),K4-TODAY()<=60)'], font=Font(bold=True, color="E67700")))
sm = wb.create_sheet("Summary", 0); title(sm, "Home Inventory Summary", "Compare the total with your contents insurance cover.")
kpis(sm, [("Items recorded", '=COUNTA(Inventory!A4:A2000)', "0"), ("Total price paid", "=SUM(Inventory!G4:G2000)", M), ("Total replacement value", "=SUM(Inventory!H4:H2000)", M),
          ("Your contents cover", 15000, M), ("Covered?", '=IF(B6>B7,"Under-insured by "&TEXT(B6-B7,"#,##0"),"Yes, with "&TEXT(B7-B6,"#,##0")&" to spare")', "@"),
          ("Items missing a receipt", '=COUNTIFS(Inventory!A4:A2000,"<>",Inventory!I4:I2000,"<>Yes")', "0"), ("Items missing a photo", '=COUNTIFS(Inventory!A4:A2000,"<>",Inventory!J4:J2000,"<>Yes")', "0"),
          ("Warranties ending in 60 days", '=COUNTIFS(Inventory!K4:K2000,">="&TODAY(),Inventory!K4:K2000,"<="&TODAY()+60)', "0")])
sm["B8"].font = Font(bold=True, color=C); sm.column_dimensions["B"].width = 30
header(sm, ["Room", "Items", "Value"], [28, 30, 14], row=14, freeze=False)
for i, rm in enumerate(rooms + ["Other"]):
    r = 15 + i; sm[f"A{r}"] = rm; sm[f"B{r}"] = f"=COUNTIF(Inventory!$B$4:$B$2000,A{r})"; sm[f"C{r}"] = f"=SUMIF(Inventory!$B$4:$B$2000,A{r},Inventory!$H$4:$H$2000)"; sm[f"C{r}"].number_format = M
sm.column_dimensions["E"].width = 16; sm.column_dimensions["F"].width = 10; sm.column_dimensions["G"].width = 14
for c, h in zip("EFG", ["Category", "Items", "Value"]):
    sm[f"{c}14"] = h; sm[f"{c}14"].font = Font(bold=True, color="FFFFFF"); sm[f"{c}14"].fill = PatternFill("solid", fgColor=C)
for i, ca in enumerate(cats):
    r = 15 + i; sm[f"E{r}"] = ca; sm[f"F{r}"] = f"=COUNTIF(Inventory!$C$4:$C$2000,E{r})"; sm[f"G{r}"] = f"=SUMIF(Inventory!$C$4:$C$2000,E{r},Inventory!$H$4:$H$2000)"; sm[f"G{r}"].number_format = M
sm.conditional_formatting.add("C15:C23", DataBarRule(start_type="num", start_value=0, end_type="max", color="ADB5BD"))
pc = PieChart(); pc.title = "Value by category"; pc.height = 8; pc.width = 12
pc.add_data(Reference(sm, min_col=7, min_row=14, max_row=23), titles_from_data=True); pc.set_categories(Reference(sm, min_col=5, min_row=15, max_row=23)); sm.add_chart(pc, "I3")
howto(wb, C, ["1. Inventory: walk round your home room by room and add each item worth recording: what it is, brand and model, serial number, when you bought it, what you paid and what it would cost to replace today.",
              "2. Mark whether you have a receipt and a photo. Keep the photos and receipts in a cloud folder and note the folder name in Notes. Missing ones are highlighted.",
              "3. Summary: enter your contents insurance cover to see if you're under-insured, plus totals by room and category and warranties about to end (orange).",
              "4. Update it when you buy something big. Save a copy somewhere outside your home (cloud storage or email it to yourself). Delete the sample items first."])
wb.save(OUT / "Home-Inventory-Insurance.xlsx")

# 2. Utility bills & energy usage tracker
C = "F08C00"; title, header = kit(C); wb = Workbook(); rd = wb.active; rd.title = "Meter readings"
title(rd, "Meter readings", "Take a reading at the start of each month. Usage and cost are worked out for you.")
header(rd, ["Month", "Electricity reading", "Electricity used", "Gas reading", "Gas used", "Water reading", "Water used"], [12, 18, 15, 13, 11, 14, 12])
e, g, w = 23410, 8120, 1520
use_e = [310, 290, 270, 230, 200, 185, 180, 190, 215, 255, 290, 320]; use_g = [1050, 950, 750, 500, 300, 175, 150, 160, 275, 550, 850, 1025]; use_w = [9, 9, 10, 10, 11, 12, 13, 12, 10, 10, 9, 9]
start = dt.date(y - 1, today.month, 1)
for i in range(13):
    r = 4 + i; m = start.month - 1 + i
    rd[f"A{r}"] = dt.date(start.year + m // 12, m % 12 + 1, 1)
    if i <= 11: rd[f"B{r}"], rd[f"D{r}"], rd[f"F{r}"] = e, g, w
    if i < 12: e += use_e[(m) % 12]; g += use_g[m % 12]; w += use_w[m % 12]
for r in range(4, 64):
    rd[f"A{r}"].number_format = "mmm yyyy"
    if r > 4:
        for rc, uc in (("B", "C"), ("D", "E"), ("F", "G")):
            rd[f"{uc}{r}"] = f'=IF(OR({rc}{r}="",{rc}{r - 1}=""),"",{rc}{r}-{rc}{r - 1})'
rt = wb.create_sheet("Tariffs"); title(rt, "Tariffs", "Unit prices and standing charges from your bills.")
header(rt, ["Utility", "Unit", "Price per unit", "Standing charge per day"], [14, 10, 14, 22], freeze=False)
for r, (u, un, p, s) in enumerate([("Electricity", "kWh", 0.27, 0.6), ("Gas", "kWh", 0.07, 0.31), ("Water", "m³", 3.1, 0.25)], 4):
    rt[f"A{r}"], rt[f"B{r}"], rt[f"C{r}"], rt[f"D{r}"] = u, un, p, s; rt[f"C{r}"].number_format = "0.0000"; rt[f"D{r}"].number_format = M
rt["A8"] = "Gas meter in m³? Multiply by about 11.2 to get kWh, or check your bill for the conversion."; rt["A8"].font = Font(italic=True, color="777777")
cs = wb.create_sheet("Costs", 0); title(cs, "Energy & Water Costs", "Cost per month from your readings and tariffs. Usage is the month that ends on each reading date.")
header(cs, ["Month", "Electricity", "Gas", "Water", "Total", "vs same month last year"], [12, 13, 11, 11, 12, 22], freeze=False)
for i in range(12):
    r = 4 + i; s = 5 + i
    cs[f"A{r}"] = f"='Meter readings'!A{s - 1}"; cs[f"A{r}"].number_format = "mmm yyyy"
    days = f"('Meter readings'!A{s}-'Meter readings'!A{s - 1})"
    for c, uc, tr in (("B", "C", 4), ("C", "E", 5), ("D", "G", 6)):
        cs[f"{c}{r}"] = f"=IF('Meter readings'!{uc}{s}=\"\",\"\",'Meter readings'!{uc}{s}*Tariffs!$C${tr}+{days}*Tariffs!$D${tr})"; cs[f"{c}{r}"].number_format = M
    cs[f"E{r}"] = f'=IF(B{r}="","",SUM(B{r}:D{r}))'; cs[f"E{r}"].number_format = M
    cs[f"F{r}"] = "Add last year's bill here" if i == 0 else None
cs["A17"] = "Year total"; cs["A17"].font = Font(bold=True)
for c in "BCDE": cs[f"{c}17"] = f"=SUM({c}4:{c}15)"; cs[f"{c}17"].number_format = M; cs[f"{c}17"].font = Font(bold=True)
cs["A18"] = "Monthly average";
for c in "BCDE": cs[f"{c}18"] = f"=IFERROR(AVERAGE({c}4:{c}15),0)"; cs[f"{c}18"].number_format = M
for i in range(1, 12): cs[f"F{4 + i}"] = None
cs["F4"] = None
cs["H3"] = "Direct debit check"; cs["H3"].font = Font(bold=True, size=12, color=C); cs.column_dimensions["H"].width = 26; cs.column_dimensions["I"].width = 13
kp = [("Monthly direct debit", 150), ("Paid in 12 months", "=I4*12"), ("Actual cost (12 months)", "=E17"), ("Difference", "=I5-I6")]
for r, (a, f) in enumerate(kp, 4): cs[f"H{r}"] = a; cs[f"I{r}"] = f; cs[f"I{r}"].number_format = M
cs["I4"].fill = SOFT; cs["H8"] = '=IF(I7>=0,"You are in credit","You owe more than you pay")'; cs["H8"].font = Font(bold=True)
cs.conditional_formatting.add("I7", CellIsRule(operator="lessThan", formula=["0"], font=Font(bold=True, color="C0392B")))
cs.conditional_formatting.add("I7", CellIsRule(operator="greaterThanOrEqual", formula=["0"], font=Font(bold=True, color="2B8A3E")))
cs["F3"].value = "Share of total"
for i in range(12): cs[f"F{4 + i}"] = f'=IF(OR(E{4 + i}="",$E$17=0),"",E{4 + i}/$E$17)'; cs[f"F{4 + i}"].number_format = "0.0%"
bc = BarChart(); bc.type = "col"; bc.grouping = "stacked"; bc.overlap = 100; bc.title = "Monthly cost"; bc.height = 8; bc.width = 20
bc.add_data(Reference(cs, min_col=2, max_col=4, min_row=3, max_row=15), titles_from_data=True); bc.set_categories(Reference(cs, min_col=1, min_row=4, max_row=15)); cs.add_chart(bc, "H11")
howto(wb, C, ["1. Tariffs: copy your unit prices and daily standing charges from your latest bills.", "2. Meter readings: on (or near) the 1st of each month, type the month and your meter readings. Usage for the month is worked out for you.",
              "3. Costs: see what each month really cost, the year total and a stacked chart. The direct debit check shows if your monthly payment covers what you use.",
              "4. Taking monthly photos of your meters is good evidence if a bill looks wrong. Delete the sample readings first and keep your first reading in row 4."])
wb.save(OUT / "Utility-Bills-Energy-Tracker.xlsx")

# 3. Staff holiday & leave tracker
C = "0CA678"; title, header = kit(C); wb = Workbook(); st = wb.active; st.title = "Staff"
title(st, "Staff & allowances", "Each person's yearly holiday allowance in days.")
header(st, ["Name", "Team", "Allowance (days)", "Carried over", "Total", "Taken", "Booked (future)", "Remaining", "Sick days"], [16, 14, 15, 12, 9, 9, 15, 11, 10])
staff = [("Alex", "Sales", 25, 2), ("Sam", "Sales", 25, 0), ("Riley", "Ops", 28, 3), ("Jordan", "Ops", 25, 1), ("Taylor", "Design", 22, 0), ("Casey", "Design", 25, 0)]
for r, s in enumerate(staff, 4):
    for c, v in enumerate(s, 1): st.cell(r, c, v)
LV = "Leave!"
for r in range(4, 54):
    st[f"E{r}"] = f'=IF(A{r}="","",N(C{r})+N(D{r}))'
    st[f"F{r}"] = f'=IF(A{r}="","",SUMIFS({LV}$F$4:$F$2000,{LV}$A$4:$A$2000,A{r},{LV}$B$4:$B$2000,"Holiday",{LV}$C$4:$C$2000,"<="&TODAY()))'
    st[f"G{r}"] = f'=IF(A{r}="","",SUMIFS({LV}$F$4:$F$2000,{LV}$A$4:$A$2000,A{r},{LV}$B$4:$B$2000,"Holiday",{LV}$C$4:$C$2000,">"&TODAY()))'
    st[f"H{r}"] = f'=IF(A{r}="","",E{r}-F{r}-G{r})'
    st[f"I{r}"] = f'=IF(A{r}="","",SUMIFS({LV}$F$4:$F$2000,{LV}$A$4:$A$2000,A{r},{LV}$B$4:$B$2000,"Sick"))'
st.conditional_formatting.add("H4:H53", CellIsRule(operator="lessThan", formula=["0"], font=Font(bold=True, color="C0392B"), fill=PatternFill("solid", fgColor="FFE3E3")))
st.conditional_formatting.add("H4:H53", DataBarRule(start_type="num", start_value=0, end_type="max", color="63E6BE"))
ph = wb.create_sheet("Public holidays"); title(ph, "Public holidays", "Dates that are not counted as leave. Update for your country each year.")
header(ph, ["Date", "Holiday"], [14, 26])
for r, (d, n) in enumerate([((12, 25), "Christmas Day"), ((12, 26), "Boxing Day"), ((1, 1), "New Year's Day")], 4):
    yy = y if d[0] == 12 else y + 1
    ph[f"A{r}"] = dt.date(yy, *d); ph[f"B{r}"] = n
for r in range(4, 44): ph[f"A{r}"].number_format = "ddd dd mmm yyyy"
lv = wb.create_sheet("Leave", 1); title(lv, "Leave requests", "Working days are counted for you, skipping weekends and public holidays.")
header(lv, ["Name", "Type", "First day", "Last day", "Half day?", "Working days", "Approved?", "Notes"], [16, 13, 13, 13, 10, 13, 11, 24])
reqs = [("Alex", "Holiday", -40, -36, "No"), ("Sam", "Sick", -20, -19, "No"), ("Riley", "Holiday", -10, -8, "No"), ("Jordan", "Holiday", 9, 13, "No"), ("Taylor", "Holiday", 30, 30, "Yes"), ("Alex", "Holiday", 31, 34, "No"), ("Casey", "Other", 3, 3, "No")]
for r, (n, t, a, b, h) in enumerate(reqs, 4):
    lv[f"A{r}"], lv[f"B{r}"], lv[f"C{r}"], lv[f"D{r}"], lv[f"E{r}"] = n, t, today + dt.timedelta(days=a), today + dt.timedelta(days=b), h; lv[f"G{r}"] = "Yes"
dv(lv, "=Staff!$A$4:$A$53", "A4:A2000"); dv(lv, '"Holiday,Sick,Parental,Unpaid,Training,Other"', "B4:B2000"); dv(lv, '"Yes,No"', "E4:E2000"); dv(lv, '"Yes,No,Pending"', "G4:G2000")
for r in range(4, 2001):
    lv[f"C{r}"].number_format = lv[f"D{r}"].number_format = "ddd dd mmm"
    lv[f"F{r}"] = f"=IF(OR(C{r}=\"\",D{r}=\"\"),\"\",NETWORKDAYS(C{r},D{r},'Public holidays'!$A$4:$A$43)-IF(E{r}=\"Yes\",0.5,0))"
lv.conditional_formatting.add("G4:G2000", CellIsRule(operator="equal", formula=['"Pending"'], fill=PatternFill("solid", fgColor="FFF3BF")))
cal = wb.create_sheet("Who's off", 0); title(cal, "Who's Off", "8 weeks from the start date. H = holiday, S = sick, O = other leave.")
cal["A3"] = "Start date"; cal["B3"] = mon; cal["B3"].number_format = "dd mmm yyyy"; cal["B3"].fill = SOFT; cal["A3"].font = Font(bold=True)
cal.column_dimensions["A"].width = 16
ND = 56
for d in range(ND):
    col = 2 + d; cal.column_dimensions[L(col)].width = 3.4
    x = cal.cell(5, col, f"=$B$3+{d}"); x.number_format = "d"; x.font = Font(size=8, bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=C); x.alignment = Alignment(horizontal="center")
    if d % 7 == 0: w = cal.cell(4, col, f'=TEXT($B$3+{d},"d mmm")'); w.font = Font(size=8, bold=True, color=C)
cal["A5"] = "Name"; cal["A5"].font = Font(bold=True, color="FFFFFF"); cal["A5"].fill = PatternFill("solid", fgColor=C)
for i in range(20):
    r = 6 + i; cal[f"A{r}"] = f'=IF(Staff!A{4 + i}="","",Staff!A{4 + i})'
    for d in range(ND):
        cl = L(2 + d)
        f = (f'IF($A{r}="","",IF(COUNTIFS(Leave!$A$4:$A$2000,$A{r},Leave!$C$4:$C$2000,"<="&{cl}$5,Leave!$D$4:$D$2000,">="&{cl}$5,Leave!$B$4:$B$2000,"Holiday")>0,"H",'
             f'IF(COUNTIFS(Leave!$A$4:$A$2000,$A{r},Leave!$C$4:$C$2000,"<="&{cl}$5,Leave!$D$4:$D$2000,">="&{cl}$5,Leave!$B$4:$B$2000,"Sick")>0,"S",'
             f'IF(COUNTIFS(Leave!$A$4:$A$2000,$A{r},Leave!$C$4:$C$2000,"<="&{cl}$5,Leave!$D$4:$D$2000,">="&{cl}$5)>0,"O",""))))')
        x = cal.cell(r, 2 + d, "=" + f); x.alignment = Alignment(horizontal="center"); x.font = Font(size=8, bold=True)
cal["A27"] = "Off that day"; cal["A27"].font = Font(bold=True)
for d in range(ND):
    cl = L(2 + d); x = cal.cell(27, 2 + d, f'=COUNTIF({cl}6:{cl}25,"?")'); x.alignment = Alignment(horizontal="center"); x.font = Font(size=8)
rng = f"B6:{L(1 + ND)}25"
cal.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"H"'], fill=PatternFill("solid", fgColor="96F2D7")))
cal.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"S"'], fill=PatternFill("solid", fgColor="FFC9C9")))
cal.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"O"'], fill=PatternFill("solid", fgColor="D0EBFF")))
cal.conditional_formatting.add(rng, FormulaRule(formula=['AND($A6<>"",WEEKDAY(B$5,2)>5)'], fill=PatternFill("solid", fgColor="F1F3F5")))
cal.conditional_formatting.add(f"B27:{L(1 + ND)}27", CellIsRule(operator="greaterThanOrEqual", formula=["2"], font=Font(bold=True, color="C0392B")))
cal.freeze_panes = "B6"
howto(wb, C, ["1. Staff: add each person with their yearly holiday allowance and any days carried over.", "2. Public holidays: list the bank holidays for your country. They are not counted as leave days.",
              "3. Leave: add each request with type, first and last day, and whether it's a half day. Working days are counted for you (weekends and public holidays skipped).",
              "4. Staff shows taken, booked and remaining holiday (red if overdrawn) and sick days. Who's Off is an 8-week calendar; days with 2 or more people off are flagged in red.",
              "5. Start a new copy each holiday year. Delete the sample staff and requests first."])
wb.save(OUT / "Staff-Holiday-Leave-Tracker.xlsx")

# 4. Tutor lesson & payment tracker
C = "7048E8"; title, header = kit(C); wb = Workbook(); stu = wb.active; stu.title = "Students"
title(stu, "Students", "Your students, rates and what each one owes.")
header(stu, ["Student", "Parent / contact", "Subject", "Level", "Rate per hour", "Lessons", "Hours", "Billed", "Paid", "Owed"], [16, 18, 13, 12, 13, 9, 8, 11, 11, 11])
studs = [("Ella", "Mrs Park", "Maths", "GCSE", 35), ("Noah", "Mr Silva", "Physics", "A-level", 40), ("Aisha", "Ms Khan", "English", "Year 9", 30), ("Ben", "Mrs Wood", "Maths", "Year 6", 28), ("Zoe", "self", "Piano", "Grade 4", 32)]
for r, s in enumerate(studs, 4):
    for c, v in enumerate(s, 1): stu.cell(r, c, v)
for r in range(4, 54):
    stu[f"E{r}"].number_format = M
    stu[f"F{r}"] = f'=IF(A{r}="","",COUNTIFS(Lessons!$B$4:$B$2000,A{r},Lessons!$F$4:$F$2000,"<>Cancelled (free)"))'
    stu[f"G{r}"] = f'=IF(A{r}="","",SUMIF(Lessons!$B$4:$B$2000,A{r},Lessons!$D$4:$D$2000))'
    stu[f"H{r}"] = f'=IF(A{r}="","",SUMIF(Lessons!$B$4:$B$2000,A{r},Lessons!$G$4:$G$2000))'
    stu[f"I{r}"] = f'=IF(A{r}="","",SUMIF(Payments!$B$4:$B$2000,A{r},Payments!$C$4:$C$2000))'
    stu[f"J{r}"] = f'=IF(A{r}="","",H{r}-I{r})'
    for c in "HIJ": stu[f"{c}{r}"].number_format = M
stu.conditional_formatting.add("J4:J53", CellIsRule(operator="greaterThan", formula=["0"], font=Font(bold=True, color="C0392B")))
stu.conditional_formatting.add("J4:J53", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="2B8A3E")))
ls = wb.create_sheet("Lessons"); title(ls, "Lesson log", "Every lesson taught. The fee comes from the student's rate.")
header(ls, ["Date", "Student", "Topic covered", "Hours", "Where", "Status", "Fee", "Homework set", "Notes for next time"], [12, 14, 26, 8, 12, 17, 10, 22, 24])
r = 4
for w in range(8):
    for i, s in enumerate(studs):
        if (w + i) % 5 == 4: continue
        ls[f"A{r}"] = mon - dt.timedelta(weeks=7 - w) + dt.timedelta(days=i); ls[f"B{r}"] = s[0]; ls[f"D{r}"] = 1 if s[0] != "Noah" else 1.5
        ls[f"E{r}"] = random.choice(["Online", "Their home", "My home"]); ls[f"F{r}"] = "Taught" if random.random() > 0.08 else "Cancelled (paid)"
        ls[f"C{r}"] = random.choice(["Fractions", "Algebra", "Past paper", "Essay plan", "Forces", "Scales & pieces", "Revision"]); r += 1
dv(ls, "=Students!$A$4:$A$53", "B4:B2000"); dv(ls, '"Online,Their home,My home,Centre"', "E4:E2000"); dv(ls, '"Taught,Cancelled (paid),Cancelled (free),No-show"', "F4:F2000")
for r in range(4, 2001):
    ls[f"A{r}"].number_format = "ddd dd mmm"
    ls[f"G{r}"] = f'=IF(OR(B{r}="",F{r}="Cancelled (free)"),IF(B{r}="","",0),N(D{r})*IFERROR(INDEX(Students!$E$4:$E$53,MATCH(B{r},Students!$A$4:$A$53,0)),0))'; ls[f"G{r}"].number_format = M
ls.conditional_formatting.add("F4:F2000", FormulaRule(formula=['LEFT($F4,9)="Cancelled"'], font=Font(color="999999")))
pm = wb.create_sheet("Payments"); title(pm, "Payments", "Money received.")
header(pm, ["Date", "Student", "Amount", "Method", "Note"], [12, 14, 11, 14, 26])
for r, (d, s, a) in enumerate([(-35, "Ella", 140), (-34, "Noah", 240), (-30, "Aisha", 120), (-28, "Ben", 112), (-25, "Zoe", 128), (-7, "Ella", 140), (-6, "Noah", 180), (-3, "Zoe", 96)], 4):
    pm[f"A{r}"], pm[f"B{r}"], pm[f"C{r}"], pm[f"D{r}"] = today + dt.timedelta(days=d), s, a, random.choice(["Bank transfer", "Cash"])
dv(pm, "=Students!$A$4:$A$53", "B4:B2000"); dv(pm, '"Bank transfer,Cash,Card,PayPal"', "D4:D2000")
for r in range(4, 2001): pm[f"A{r}"].number_format = "dd mmm yy"; pm[f"C{r}"].number_format = M
db = wb.create_sheet("Dashboard", 0); title(db, "Tutoring Dashboard", "Your teaching business at a glance.")
kpis(db, [("Active students", '=COUNTA(Students!A4:A53)', "0"), ("Lessons logged", '=COUNTIF(Lessons!F4:F2000,"Taught")', "0"), ("Hours taught", '=SUMIF(Lessons!F4:F2000,"Taught",Lessons!D4:D2000)', "0.0"),
          ("Total billed", "=SUM(Lessons!G4:G2000)", M), ("Total received", "=SUM(Payments!C4:C2000)", M), ("Owed to you", '=SUMIF(Students!J4:J53,">0")', M), ("Average per hour", "=IFERROR(B7/SUM(Lessons!D4:D2000),0)", M)])
db.conditional_formatting.add("B9", CellIsRule(operator="greaterThan", formula=["0"], font=Font(bold=True, color="C0392B")))
header(db, ["Month", "Lessons", "Hours", "Billed", "Received"], [28, 14, 10, 12, 12], row=13, freeze=False)
for i in range(6):
    r = 14 + i; db[f"A{r}"] = f"=EDATE(DATE(YEAR(TODAY()),MONTH(TODAY()),1),{i - 5})"; db[f"A{r}"].number_format = "mmm yyyy"
    rng = lambda col: f'Lessons!$A$4:$A$2000,">="&A{r},Lessons!$A$4:$A$2000,"<"&EDATE(A{r},1)'
    db[f"B{r}"] = f'=COUNTIFS({rng(0)},Lessons!$F$4:$F$2000,"Taught")'; db[f"C{r}"] = f'=SUMIFS(Lessons!$D$4:$D$2000,{rng(0)},Lessons!$F$4:$F$2000,"Taught")'
    db[f"D{r}"] = f"=SUMIFS(Lessons!$G$4:$G$2000,{rng(0)})"; db[f"E{r}"] = f'=SUMIFS(Payments!$C$4:$C$2000,Payments!$A$4:$A$2000,">="&A{r},Payments!$A$4:$A$2000,"<"&EDATE(A{r},1))'
    db[f"D{r}"].number_format = db[f"E{r}"].number_format = M
bc = BarChart(); bc.title = "Billed vs received"; bc.height = 7; bc.width = 16
bc.add_data(Reference(db, min_col=4, max_col=5, min_row=13, max_row=19), titles_from_data=True); bc.set_categories(Reference(db, min_col=1, min_row=14, max_row=19)); db.add_chart(bc, "G3")
howto(wb, C, ["1. Students: add each student with their contact, subject, level and hourly rate.", "2. Lessons: log every lesson with the hours and status. Cancelled (free) lessons aren't charged; Cancelled (paid) and No-show are charged at the normal rate.",
              "3. Payments: record money as it comes in. Students shows billed, paid and owed for each student (red = owes you).",
              "4. Dashboard: hours taught, money billed and received, what you're owed, your real hourly rate and a monthly chart. Works for tutors, music teachers, coaches and instructors.", "5. Delete the sample data first."])
wb.save(OUT / "Tutor-Lesson-Payment-Tracker.xlsx")

# 5. Compound interest & savings calculator
C = "2B8A3E"; title, header = kit(C); wb = Workbook(); cc = wb.active; cc.title = "Calculator"
title(cc, "Compound Interest Calculator", "See how your savings grow with regular deposits and interest on interest.")
inputs = [("Starting amount", 2000, M), ("Monthly deposit", 150, M), ("Yearly interest / return", 0.04, "0.00%"), ("Years", 20, "0"), ("Yearly increase in deposit", 0.02, "0.0%"), ("Inflation (for today's money)", 0.02, "0.0%"), ("Savings goal (optional)", 60000, M)]
for r, (a, v, nf_) in enumerate(inputs, 4):
    cc[f"A{r}"] = a; cc[f"B{r}"] = v; cc[f"B{r}"].number_format = nf_; cc[f"A{r}"].font = Font(bold=True); cc[f"B{r}"].fill = SOFT
cc.column_dimensions["A"].width = 30; cc.column_dimensions["B"].width = 14
cc["D3"] = "Results"; cc["D3"].font = Font(bold=True, size=12, color=C); cc.column_dimensions["D"].width = 28; cc.column_dimensions["E"].width = 15
res = [("Final balance", "=INDEX(Schedule!E5:E54,B7)", M), ("Total you paid in", "=INDEX(Schedule!F5:F54,B7)", M), ("Interest earned", "=E4-E5", M), ("Interest share of balance", "=IFERROR(E6/E4,0)", "0%"),
       ("Final balance in today's money", "=E4/(1+B9)^B7", M), ("Year you reach the goal", '=IFERROR(INDEX(Schedule!A5:A54,MATCH(TRUE,INDEX(Schedule!E5:E54>=B10,0),0)),"Not within "&B7&" years")', "0"),
       ("Monthly deposit needed for goal", "=IFERROR(MAX(0,(B10-B4*(1+B6/12)^(B7*12))*(B6/12)/((1+B6/12)^(B7*12)-1)),0)", M)]
for r, (a, f, nf_) in enumerate(res, 4):
    cc[f"D{r}"] = a; cc[f"E{r}"] = f; cc[f"E{r}"].number_format = nf_; cc[f"D{r}"].font = Font(bold=True)
cc["E4"].font = Font(bold=True, size=13, color=C)
cc["D12"] = "Goal deposit assumes a flat monthly deposit and monthly compounding."; cc["D12"].font = Font(italic=True, color="777777")
sc = wb.create_sheet("Schedule"); title(sc, "Year by year", "Monthly deposits, compounded monthly. Rows beyond your chosen years are blank.")
header(sc, ["Year", "Start balance", "Deposits this year", "Interest this year", "End balance", "Total paid in", "Total interest", "In today's money"], [7, 14, 16, 16, 14, 14, 14, 16], row=4)
cin = "Calculator!"
for i in range(50):
    r = 5 + i; yr = i + 1
    sc[f"A{r}"] = f'=IF({yr}>{cin}$B$7,"",{yr})'
    sc[f"B{r}"] = f'=IF(A{r}="","",{cin + "$B$4" if i == 0 else f"E{r - 1}"})'
    dep = f"{cin}$B$5*(1+{cin}$B$8)^({yr}-1)"; mr = f"({cin}$B$6/12)"
    sc[f"C{r}"] = f'=IF(A{r}="","",{dep}*12)'
    sc[f"E{r}"] = f'=IF(A{r}="","",IF({mr}=0,B{r}+C{r},B{r}*(1+{mr})^12+{dep}*((1+{mr})^12-1)/{mr}))'
    sc[f"D{r}"] = f'=IF(A{r}="","",E{r}-B{r}-C{r})'
    sc[f"F{r}"] = f'=IF(A{r}="","",{cin + "$B$4" if i == 0 else f"F{r - 1}"}+C{r})'
    sc[f"G{r}"] = f'=IF(A{r}="","",E{r}-F{r})'
    sc[f"H{r}"] = f'=IF(A{r}="","",E{r}/(1+{cin}$B$9)^A{r})'
    for c in "BCDEFGH": sc[f"{c}{r}"].number_format = M
sc.conditional_formatting.add("E5:E54", FormulaRule(formula=[f'AND(E5<>"",{cin}$B$10>0,E5>={cin}$B$10)'], fill=PatternFill("solid", fgColor="B2F2BB")))
lc = LineChart(); lc.title = "Balance vs money paid in"; lc.height = 8; lc.width = 20
lc.add_data(Reference(sc, min_col=5, max_col=6, min_row=4, max_row=24), titles_from_data=True); lc.set_categories(Reference(sc, min_col=1, min_row=5, max_row=24)); cc.add_chart(lc, "A15")
cmp_ = wb.create_sheet("Compare rates"); title(cmp_, "Compare rates", "Same deposits, different interest rates. Change the rates in row 4.")
cmp_["A4"] = "Rate"; cmp_["A4"].font = Font(bold=True); cmp_.column_dimensions["A"].width = 16
for j, rt in enumerate([0.01, 0.03, 0.05, 0.07]):
    cl = L(2 + j); cmp_[f"{cl}4"] = rt; cmp_[f"{cl}4"].number_format = "0.0%"; cmp_[f"{cl}4"].fill = SOFT; cmp_.column_dimensions[cl].width = 14
for k, yrs in enumerate([5, 10, 15, 20, 25, 30, 40]):
    r = 5 + k; cmp_[f"A{r}"] = f"After {yrs} years"; cmp_[f"A{r}"].font = Font(bold=True)
    for j in range(4):
        cl = L(2 + j); mr = f"({cl}$4/12)"; n = yrs * 12
        cmp_[f"{cl}{r}"] = f"=IF({mr}=0,{cin}$B$4+{cin}$B$5*{n},{cin}$B$4*(1+{mr})^{n}+{cin}$B$5*((1+{mr})^{n}-1)/{mr})"; cmp_[f"{cl}{r}"].number_format = M
cmp_["A13"] = "Uses the starting amount and a flat monthly deposit from the Calculator tab."; cmp_["A13"].font = Font(italic=True, color="777777")
howto(wb, C, ["1. Calculator: enter your starting amount, monthly deposit, expected yearly interest or return, number of years and (optionally) how much your deposit rises each year.",
              "2. Results show your final balance, how much was your money vs interest, the value in today's money after inflation, when you hit your goal and the monthly deposit needed to reach it.",
              "3. Schedule shows every year. Compare rates shows the same plan at four different rates side by side.", "4. Returns are not guaranteed: this is a planning tool, not financial advice."])
wb.save(OUT / "Compound-Interest-Savings-Calculator.xlsx")
print("built 5")
