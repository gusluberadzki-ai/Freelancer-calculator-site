"""Round 11 spreadsheet products into products/. Run: python3 make_batch6.py (reuses helpers from make_batch2.py)"""
import pathlib
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
from openpyxl.chart import PieChart
today = dt.date.today(); y = today.year
mon = today - dt.timedelta(days=today.weekday())
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# 1. Employee shift rota
C = "364FC7"; title, header = kit(C); wb = Workbook(); sf = wb.active; sf.title = "Shifts"
title(sf, "Shift types", "Set up your shift codes once. Hours are worked out from the start and end times.")
header(sf, ["Code", "Shift", "Start", "End", "Paid hours", "Unpaid break (h)"], [8, 18, 9, 9, 11, 14], freeze=False)
for r, (c, n, s, e, b) in enumerate([("E", "Early", "07:00", "15:00", 0.5), ("M", "Middle", "10:00", "18:00", 0.5), ("L", "Late", "14:00", "22:00", 0.5), ("N", "Night", "22:00", "06:00", 0.5), ("H", "Half day", "09:00", "13:00", 0), ("HOL", "Holiday (paid)", "", "", 0), ("OFF", "Day off", "", "", 0)], 4):
    sf[f"A{r}"], sf[f"B{r}"], sf[f"F{r}"] = c, n, b
    if s: sf[f"C{r}"], sf[f"D{r}"] = dt.time(*map(int, s.split(":"))), dt.time(*map(int, e.split(":")))
sf["E9"] = 8; sf["E10"] = 0
for r in range(4, 21):
    sf[f"C{r}"].number_format = sf[f"D{r}"].number_format = "hh:mm"
    if r not in (9, 10): sf[f"E{r}"] = f'=IF(OR(C{r}="",D{r}=""),"",ROUND((MOD(D{r}-C{r},1))*24-N(F{r}),2))'
sf["H4"] = "Holiday is counted as 8 paid hours. Change E9 if your paid holiday day is different."; sf["H4"].font = Font(italic=True, color="777777")
st = wb.create_sheet("Staff"); title(st, "Staff", "Hourly rate and contracted hours for each person.")
header(st, ["Name", "Role", "Hourly rate", "Contracted hours / week", "Max hours / week"], [18, 16, 12, 14, 12])
for r, s in enumerate([("Alex", "Supervisor", 16.5, 37.5, 45), ("Sam", "Barista", 12.4, 30, 40), ("Riley", "Barista", 12.4, 20, 30), ("Jordan", "Kitchen", 13.1, 37.5, 45), ("Taylor", "Kitchen", 13.1, 16, 24), ("Casey", "Weekend staff", 11.8, 12, 20)], 4):
    for c, v in enumerate(s, 1): st.cell(r, c, v)
for r in range(4, 34): st[f"C{r}"].number_format = M
ro = wb.create_sheet("Rota", 0)
title(ro, "Weekly Staff Rota", "Pick a shift code for each person and day. Hours, cost and cover update automatically.")
ro["A3"] = "Week starting"; ro["B3"] = mon; ro["B3"].number_format = "dd mmm yyyy"; ro["B3"].fill = SOFT; ro["A3"].font = Font(bold=True)
header(ro, ["Name", "Role"] + DAYS + ["Hours", "Contract", "+/-", "Cost"], [16, 14] + [8] * 7 + [9, 10, 8, 12], row=5)
for i in range(7):
    x = ro.cell(4, 3 + i, f"=$B$3+{i}"); x.number_format = "dd mmm"; x.font = Font(bold=True, color=C); x.alignment = Alignment(horizontal="center")
sample = [["E", "E", "OFF", "E", "E", "M", "OFF"], ["L", "L", "L", "OFF", "OFF", "E", "E"], ["OFF", "M", "M", "H", "OFF", "L", "OFF"], ["E", "E", "E", "E", "E", "OFF", "OFF"], ["OFF", "OFF", "L", "L", "OFF", "OFF", "H"], ["OFF", "OFF", "OFF", "OFF", "OFF", "M", "M"]]
dv(ro, "=Shifts!$A$4:$A$20", "C6:I35")
dv(ro, "=Staff!$A$4:$A$33", "A6:A35")
codes = "Shifts!$A$4:$A$20"; hrs = "Shifts!$E$4:$E$20"
for r in range(6, 36):
    if r - 6 < len(sample):
        ro[f"A{r}"] = st[f"A{r - 2}"].value
        for i, v in enumerate(sample[r - 6]): ro.cell(r, 3 + i, v)
    ro[f"B{r}"] = f'=IF(A{r}="","",IFERROR(INDEX(Staff!$B$4:$B$33,MATCH(A{r},Staff!$A$4:$A$33,0)),""))'
    ro[f"J{r}"] = f'=IF(A{r}="","",SUMPRODUCT(COUNTIF(C{r}:I{r},{codes}),{hrs}))'
    ro[f"K{r}"] = f'=IF(A{r}="","",IFERROR(INDEX(Staff!$D$4:$D$33,MATCH(A{r},Staff!$A$4:$A$33,0)),0))'
    ro[f"L{r}"] = f'=IF(A{r}="","",J{r}-K{r})'; ro[f"L{r}"].number_format = "+0.0;-0.0;0"
    ro[f"M{r}"] = f'=IF(A{r}="","",J{r}*IFERROR(INDEX(Staff!$C$4:$C$33,MATCH(A{r},Staff!$A$4:$A$33,0)),0))'; ro[f"M{r}"].number_format = M
    ro[f"J{r}"].number_format = "0.0"
    for c in range(3, 10): ro.cell(r, c).alignment = Alignment(horizontal="center")
ro["A36"] = "Totals"; ro["A36"].font = Font(bold=True); ro["J36"] = "=SUM(J6:J35)"; ro["M36"] = "=SUM(M6:M35)"; ro["M36"].number_format = M; ro["J36"].number_format = "0.0"
for c, col in [("E", "FFE8CC"), ("M", "D3F9D8"), ("L", "D0EBFF"), ("N", "E5DBFF"), ("H", "FFF3BF"), ("HOL", "FFC9C9"), ("OFF", "F1F3F5")]:
    ro.conditional_formatting.add("C6:I35", CellIsRule(operator="equal", formula=[f'"{c}"'], fill=PatternFill("solid", fgColor=col)))
ro.conditional_formatting.add("J6:J35", FormulaRule(formula=['AND($A6<>"",$J6>IFERROR(INDEX(Staff!$E$4:$E$33,MATCH($A6,Staff!$A$4:$A$33,0)),999))'], font=Font(bold=True, color="C0392B"), fill=PatternFill("solid", fgColor="FFE3E3")))
ro["A38"] = "Cover per day"; ro["A38"].font = Font(bold=True, size=12, color=C)
for i, (code, name) in enumerate([("E", "Early"), ("M", "Middle"), ("L", "Late"), ("N", "Night"), ("H", "Half day")]):
    r = 39 + i; ro[f"A{r}"] = name; ro[f"B{r}"] = code
    for d in range(7): ro.cell(r, 3 + d, f"=COUNTIF({L(3 + d)}$6:{L(3 + d)}$35,$B{r})").alignment = Alignment(horizontal="center")
ro["A44"] = "Staff working"; ro["A44"].font = Font(bold=True)
for d in range(7):
    cl = L(3 + d); ro.cell(44, 3 + d, f"=SUM({cl}39:{cl}43)").font = Font(bold=True)
ro["A45"] = "Hours on the day"
for d in range(7):
    cl = L(3 + d); x = ro.cell(45, 3 + d, f"=SUMPRODUCT(COUNTIF({cl}6:{cl}35,{codes}),{hrs})"); x.number_format = "0.0"
ro.conditional_formatting.add("C39:I43", CellIsRule(operator="equal", formula=["0"], font=Font(color="C0392B")))
ro.freeze_panes = "C6"
bc = BarChart(); bc.title = "Hours this week"; bc.height = 7; bc.width = 16; bc.legend = None
bc.add_data(Reference(ro, min_col=10, min_row=5, max_row=11), titles_from_data=True); bc.set_categories(Reference(ro, min_col=1, min_row=6, max_row=11)); ro.add_chart(bc, "O5")
howto(wb, C, ["1. Shifts: set up your shift codes with start and end times and any unpaid break. Night shifts that end after midnight work fine.", "2. Staff: add each person with their hourly rate, contracted hours and the most hours they should work in a week.",
              "3. Rota: set the week start date, pick names from the list and choose a shift code for each day. Hours, difference from contract and wage cost fill in.", "4. Anyone over their max hours turns red. 'Cover per day' shows how many people are on each shift, and a red 0 shows a gap.",
              "5. For the next week, right-click the Rota tab, choose Duplicate / Move or Copy, and change the week start date. Delete the sample staff and shifts first."])
wb.save(OUT / "Employee-Shift-Rota.xlsx")

# 2. Sales tracker & dashboard
C = "087F5B"; title, header = kit(C); wb = Workbook(); pr = wb.active; pr.title = "Products"
title(pr, "Products", "Your products with price and cost per unit.")
header(pr, ["Product", "Category", "Price", "Cost per unit", "Margin"], [24, 14, 11, 13, 10])
prods = [("Scented candle", "Home", 18, 6.2), ("Soap bar", "Bath", 7, 1.9), ("Gift box", "Gifts", 35, 14), ("Bath salts", "Bath", 12, 3.4), ("Wax melts", "Home", 6, 1.5), ("Reed diffuser", "Home", 22, 8.1)]
for r, p in enumerate(prods, 4):
    for c, v in enumerate(p, 1): pr.cell(r, c, v)
for r in range(4, 54):
    pr[f"C{r}"].number_format = pr[f"D{r}"].number_format = M
    pr[f"E{r}"] = f'=IF(N(C{r})=0,"",(C{r}-D{r})/C{r})'; pr[f"E{r}"].number_format = "0%"
sl = wb.create_sheet("Sales", 0); title(sl, "Sales log", "One row per order line. Price and cost fill in from Products.")
header(sl, ["Date", "Product", "Qty", "Channel", "Discount %", "Unit price", "Revenue", "Cost", "Profit", "Customer / note"], [12, 22, 7, 13, 10, 11, 12, 11, 11, 22])
chans = ["Website", "Etsy", "Market stall", "Wholesale", "Instagram"]
import random; random.seed(11)
rows = []
for k in range(40):
    d = today - dt.timedelta(days=random.randint(0, 150)); p = random.choice(prods)[0]
    rows.append((d, p, random.choice([1, 1, 1, 2, 2, 3, 6]), random.choice(chans), random.choice([0, 0, 0, 0.1])))
rows.sort()
for r, (d, p, q, ch, ds) in enumerate(rows, 4):
    sl[f"A{r}"], sl[f"B{r}"], sl[f"C{r}"], sl[f"D{r}"], sl[f"E{r}"] = d, p, q, ch, ds
dv(sl, "=Products!$A$4:$A$53", "B4:B2000"); dv(sl, '"' + ",".join(chans) + ',Other"', "D4:D2000")
for r in range(4, 2001):
    sl[f"A{r}"].number_format = "yyyy-mm-dd"; sl[f"E{r}"].number_format = "0%"
    sl[f"F{r}"] = f'=IF(B{r}="","",IFERROR(INDEX(Products!$C$4:$C$53,MATCH(B{r},Products!$A$4:$A$53,0)),0))'
    sl[f"G{r}"] = f'=IF(B{r}="","",C{r}*F{r}*(1-N(E{r})))'
    sl[f"H{r}"] = f'=IF(B{r}="","",C{r}*IFERROR(INDEX(Products!$D$4:$D$53,MATCH(B{r},Products!$A$4:$A$53,0)),0))'
    sl[f"I{r}"] = f'=IF(B{r}="","",G{r}-H{r})'
    for c in "FGHI": sl[f"{c}{r}"].number_format = M
db = wb.create_sheet("Dashboard", 0); title(db, "Sales Dashboard", "Pick a year. Everything below updates from the Sales log.")
db["A3"] = "Year"; db["B3"] = y; db["B3"].fill = SOFT; db["A3"].font = Font(bold=True)
S = "Sales!$A$4:$A$2000"
YR = f'{S},">="&DATE($B$3,1,1),{S},"<"&DATE($B$3+1,1,1)'
kp = [("Revenue", f"=SUMIFS(Sales!$G$4:$G$2000,{YR})", M), ("Profit", f"=SUMIFS(Sales!$I$4:$I$2000,{YR})", M), ("Units sold", f"=SUMIFS(Sales!$C$4:$C$2000,{YR})", "0"),
      ("Orders", f'=COUNTIFS({YR},Sales!$B$4:$B$2000,"<>")', "0"), ("Average order", "=IFERROR(B5/B8,0)", M), ("Profit margin", "=IFERROR(B6/B5,0)", "0%")]
for r, (a, f, nf_) in enumerate(kp, 5):
    db[f"A{r}"] = a; db[f"B{r}"] = f; db[f"B{r}"].number_format = nf_; db[f"A{r}"].font = Font(bold=True); db[f"B{r}"].fill = SOFT; db[f"B{r}"].font = Font(bold=True, size=12)
header(db, ["Month", "Revenue", "Profit", "Units"], [16, 14, 14, 10], row=12, freeze=False)
for i, m in enumerate(MONTHS):
    r = 13 + i; db[f"A{r}"] = m
    cond = f'{S},">="&DATE($B$3,{i + 1},1),{S},"<"&DATE($B$3,{i + 2},1)'
    db[f"B{r}"] = f"=SUMIFS(Sales!$G$4:$G$2000,{cond})"; db[f"C{r}"] = f"=SUMIFS(Sales!$I$4:$I$2000,{cond})"; db[f"D{r}"] = f"=SUMIFS(Sales!$C$4:$C$2000,{cond})"
    db[f"B{r}"].number_format = db[f"C{r}"].number_format = M
db["A25"] = "Total"; db["A25"].font = Font(bold=True)
for c in "BCD": db[f"{c}25"] = f"=SUM({c}13:{c}24)"; db[f"{c}25"].font = Font(bold=True); db[f"{c}25"].number_format = M if c != "D" else "0"
db.column_dimensions["F"].width = 22; db.column_dimensions["G"].width = 13; db.column_dimensions["H"].width = 13
for col, h in zip("FGH", ["Product", "Revenue", "Units"]):
    x = db[f"{col}27"]; x.value = h; x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=C)
for i in range(12):
    r = 28 + i
    db[f"F{r}"] = f'=IF(Products!A{4 + i}="","",Products!A{4 + i})'
    db[f"G{r}"] = f'=IF(F{r}="","",SUMIFS(Sales!$G$4:$G$2000,{YR},Sales!$B$4:$B$2000,F{r}))'; db[f"G{r}"].number_format = M
    db[f"H{r}"] = f'=IF(F{r}="","",SUMIFS(Sales!$C$4:$C$2000,{YR},Sales!$B$4:$B$2000,F{r}))'
for col, h in zip("AB", ["Channel", "Revenue"]):
    x = db[f"{col}27"]; x.value = h; x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=C)
for i, ch in enumerate(chans + ["Other"]):
    r = 28 + i; db[f"A{r}"] = ch; db[f"B{r}"] = f"=SUMIFS(Sales!$G$4:$G$2000,{YR},Sales!$D$4:$D$2000,A{r})"; db[f"B{r}"].number_format = M
db.conditional_formatting.add("G28:G39", DataBarRule(start_type="num", start_value=0, end_type="max", color="63E6BE"))
db.conditional_formatting.add("B28:B33", DataBarRule(start_type="num", start_value=0, end_type="max", color="63E6BE"))
bc = BarChart(); bc.title = "Revenue and profit by month"; bc.height = 8; bc.width = 20
bc.add_data(Reference(db, min_col=2, max_col=3, min_row=12, max_row=24), titles_from_data=True); bc.set_categories(Reference(db, min_col=1, min_row=13, max_row=24)); db.add_chart(bc, "F3")
howto(wb, C, ["1. Products: list everything you sell with its price and what one unit costs you to make or buy. Margin is worked out for you.", "2. Sales: add one row per order line. Pick the product and channel, enter the quantity and any discount. Revenue, cost and profit fill in.",
              "3. Dashboard: type a year at the top to see revenue, profit, units, orders, average order and margin, plus a month-by-month chart, best-selling products and sales by channel.", "4. Delete the sample products and sales first. The log has room for about 2,000 order lines."])
wb.save(OUT / "Sales-Tracker-Dashboard.xlsx")

# 3. Investment portfolio tracker
C = "5F3DC4"; title, header = kit(C); wb = Workbook(); ho = wb.active; ho.title = "Holdings"
title(ho, "Portfolio Holdings", "Update the current price now and then. Value, gain and weight are worked out for you.")
header(ho, ["Ticker", "Name", "Asset class", "Account", "Units", "Avg cost", "Current price", "Cost basis", "Value", "Gain / loss", "Gain %", "Weight"], [9, 26, 14, 11, 9, 11, 12, 13, 13, 13, 9, 9])
classes = ["Global stocks", "Home stocks", "Bonds", "Property", "Cash", "Other"]
hold = [("VWRL", "Global all-world ETF", "Global stocks", "ISA", 120, 88.4, 104.2), ("HOME", "Home market index fund", "Home stocks", "ISA", 300, 7.1, 7.65), ("AGGB", "Global bond ETF", "Bonds", "Pension", 85, 46.9, 45.1),
        ("PROP", "Global property ETF", "Property", "Pension", 40, 21.3, 23.8), ("CASH", "Savings account", "Cash", "Bank", 1, 2500, 2500)]
for r, h in enumerate(hold, 4):
    for c, v in enumerate(h, 1): ho.cell(r, c, v)
dv(ho, '"' + ",".join(classes) + '"', "C4:C103")
for r in range(4, 104):
    ho[f"H{r}"] = f'=IF(A{r}="","",E{r}*F{r})'; ho[f"I{r}"] = f'=IF(A{r}="","",E{r}*G{r})'; ho[f"J{r}"] = f'=IF(A{r}="","",I{r}-H{r})'
    ho[f"K{r}"] = f'=IF(OR(A{r}="",N(H{r})=0),"",J{r}/H{r})'; ho[f"L{r}"] = f'=IF(A{r}="","",IFERROR(I{r}/SUM($I$4:$I$103),0))'
    for c in "FGHIJ": ho[f"{c}{r}"].number_format = M
    ho[f"K{r}"].number_format = "+0.0%;-0.0%;0.0%"; ho[f"L{r}"].number_format = "0.0%"
ho.conditional_formatting.add("J4:K103", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B")))
ho.conditional_formatting.add("J4:K103", CellIsRule(operator="greaterThan", formula=["0"], font=Font(color="2B8A3E")))
al = wb.create_sheet("Allocation", 0); title(al, "Portfolio Overview", "Set your target mix. The table shows how far off you are and what to buy or sell to rebalance.")
for r, (a, f, nf_) in enumerate([("Total value", "=SUM(Holdings!I4:I103)", M), ("Total invested (cost)", "=SUM(Holdings!H4:H103)", M), ("Gain / loss", "=B4-B5", M), ("Return", "=IFERROR(B6/B5,0)", "+0.0%;-0.0%"), ("Total contributed (log)", "=SUM(Contributions!B4:B1000)", M)], 4):
    al[f"A{r}"] = a; al[f"B{r}"] = f; al[f"B{r}"].number_format = nf_; al[f"A{r}"].font = Font(bold=True); al[f"B{r}"].fill = SOFT
header(al, ["Asset class", "Target %", "Value", "Actual %", "Difference", "Buy (+) / sell (-)"], [22, 10, 14, 10, 11, 16], row=11, freeze=False)
for i, (cl, t) in enumerate(zip(classes, [0.5, 0.15, 0.2, 0.05, 0.1, 0])):
    r = 12 + i; al[f"A{r}"] = cl; al[f"B{r}"] = t
    al[f"C{r}"] = f"=SUMIF(Holdings!$C$4:$C$103,A{r},Holdings!$I$4:$I$103)"; al[f"D{r}"] = f"=IFERROR(C{r}/$B$4,0)"; al[f"E{r}"] = f"=D{r}-B{r}"; al[f"F{r}"] = f"=B{r}*$B$4-C{r}"
    al[f"B{r}"].number_format = al[f"D{r}"].number_format = "0.0%"; al[f"E{r}"].number_format = "+0.0%;-0.0%;0.0%"; al[f"C{r}"].number_format = al[f"F{r}"].number_format = M; al[f"B{r}"].fill = SOFT
al["A18"] = "Total"; al["B18"] = "=SUM(B12:B17)"; al["B18"].number_format = "0%"; al["C18"] = "=SUM(C12:C17)"; al["C18"].number_format = M; al["A18"].font = Font(bold=True)
al.conditional_formatting.add("B18", CellIsRule(operator="notEqual", formula=["1"], font=Font(bold=True, color="C0392B")))
al.conditional_formatting.add("E12:E17", FormulaRule(formula=["ABS(E12)>=0.05"], font=Font(bold=True, color="C0392B")))
al["A20"] = "Target % should add up to 100%. A difference of 5 points or more turns red, a common point to rebalance."; al["A20"].font = Font(italic=True, color="777777")
pc = PieChart(); pc.title = "Current mix"; pc.height = 8; pc.width = 12
pc.add_data(Reference(al, min_col=3, min_row=11, max_row=17), titles_from_data=True); pc.set_categories(Reference(al, min_col=1, min_row=12, max_row=17)); al.add_chart(pc, "H3")
co = wb.create_sheet("Contributions"); title(co, "Contributions", "Money you put in (or take out as a negative).")
header(co, ["Date", "Amount", "Account", "Note"], [12, 12, 12, 30])
for r, (d, a, ac) in enumerate([(-150, 1000, "ISA"), (-120, 500, "ISA"), (-90, 500, "Pension"), (-60, 500, "ISA"), (-30, 500, "Pension")], 4):
    co[f"A{r}"] = today + dt.timedelta(days=d); co[f"B{r}"] = a; co[f"C{r}"] = ac
for r in range(4, 1001): co[f"A{r}"].number_format = "yyyy-mm-dd"; co[f"B{r}"].number_format = M
hs = wb.create_sheet("Value history"); title(hs, "Value history", "Once a month, type today's date and copy the total value from Allocation!B4.")
header(hs, ["Date", "Total value", "Change"], [12, 14, 12])
for r, (d, v) in enumerate([(-120, 19800), (-90, 20350), (-60, 20120), (-30, 21040), (0, 21710)], 4):
    hs[f"A{r}"] = today + dt.timedelta(days=d); hs[f"B{r}"] = v
for r in range(4, 124):
    hs[f"A{r}"].number_format = "mmm yyyy"; hs[f"B{r}"].number_format = M
    if r > 4: hs[f"C{r}"] = f'=IF(OR(B{r}="",B{r - 1}=""),"",B{r}/B{r - 1}-1)'; hs[f"C{r}"].number_format = "+0.0%;-0.0%"
lc = LineChart(); lc.title = "Portfolio value"; lc.height = 7; lc.width = 18; lc.legend = None
lc.add_data(Reference(hs, min_col=2, min_row=3, max_row=40), titles_from_data=True); lc.set_categories(Reference(hs, min_col=1, min_row=4, max_row=40)); hs.add_chart(lc, "E3")
howto(wb, C, ["1. Holdings: one row per fund, share or account with units owned, your average cost per unit and the current price. Value, gain and weight are worked out for you.",
              "2. In Google Sheets you can fetch prices automatically: in Current price type =GOOGLEFINANCE(A4) (works for many tickers). In Excel use the Stocks data type, or type prices in by hand.",
              "3. Allocation: set a target % for each asset class (they should add up to 100%). You'll see your current mix and how much to buy or sell in each class to get back to target.",
              "4. Contributions logs money paid in. Value history is a monthly snapshot for the chart. Rename the asset classes in the Holdings list and Allocation tab if you like.",
              "5. This is a record-keeping tool, not financial advice. Delete the sample rows first."])
wb.save(OUT / "Investment-Portfolio-Tracker.xlsx")

# 4. Blood pressure & health log
C = "C92A2A"; title, header = kit(C); wb = Workbook(); lg = wb.active; lg.title = "Log"
title(lg, "Blood Pressure Log", "Log each reading. The category and averages are worked out for you.")
header(lg, ["Date", "Time", "Systolic", "Diastolic", "Pulse", "Arm", "Category", "Weight", "Medication taken", "Notes"], [12, 8, 9, 9, 8, 8, 18, 9, 14, 26])
random.seed(4)
for k in range(28):
    r = 4 + k; d = today - dt.timedelta(days=27 - k // 1)
    lg[f"A{r}"] = d; lg[f"B{r}"] = dt.time(8 if k % 2 == 0 else 20, random.choice([0, 15, 30])); lg[f"C{r}"] = random.randint(118, 142); lg[f"D{r}"] = random.randint(74, 91); lg[f"E{r}"] = random.randint(62, 80)
    lg[f"F{r}"] = "Left"; lg[f"I{r}"] = "Yes"; lg[f"H{r}"] = round(78.4 - k * 0.05, 1) if k % 7 == 0 else None
dv(lg, '"Left,Right"', "F4:F2000"); dv(lg, '"Yes,No,Not on any"', "I4:I2000")
for r in range(4, 2001):
    lg[f"A{r}"].number_format = "yyyy-mm-dd"; lg[f"B{r}"].number_format = "hh:mm"
    lg[f"G{r}"] = (f'=IF(OR(C{r}="",D{r}=""),"",IF(OR(C{r}>180,D{r}>120),"Very high - get help",IF(OR(C{r}>=140,D{r}>=90),"High stage 2",'
                   f'IF(OR(C{r}>=130,D{r}>=80),"High stage 1",IF(C{r}>=120,"Elevated","Normal")))))')
for txt, col in [("Normal", "D3F9D8"), ("Elevated", "FFF3BF"), ("High stage 1", "FFE8CC"), ("High stage 2", "FFC9C9"), ("Very high", "FA5252")]:
    lg.conditional_formatting.add("G4:G2000", FormulaRule(formula=[f'LEFT($G4,{len(txt)})="{txt}"'], fill=PatternFill("solid", fgColor=col), stopIfTrue=True))
sm = wb.create_sheet("Averages", 0); title(sm, "Averages", "Pick a year. Monthly averages and morning vs evening readings update from the Log.")
sm["A3"] = "Year"; sm["B3"] = y; sm["B3"].fill = SOFT; sm["A3"].font = Font(bold=True)
header(sm, ["Month", "Readings", "Avg systolic", "Avg diastolic", "Avg pulse", "Highest systolic"], [12, 10, 12, 12, 10, 14], row=5, freeze=False)
Ld = "Log!$A$4:$A$2000"
for i, m in enumerate(MONTHS):
    r = 6 + i; sm[f"A{r}"] = m
    lo, hi = f"DATE($B$3,{i + 1},1)", f"DATE($B$3,{i + 2},1)"
    sm[f"B{r}"] = f'=COUNTIFS({Ld},">="&{lo},{Ld},"<"&{hi},Log!$C$4:$C$2000,"<>")'
    for c, src in [("C", "C"), ("D", "D"), ("E", "E")]:
        sm[f"{c}{r}"] = f'=IFERROR(AVERAGEIFS(Log!${src}$4:${src}$2000,{Ld},">="&{lo},{Ld},"<"&{hi}),"")'; sm[f"{c}{r}"].number_format = "0"
    sm[f"F{r}"] = f'=IF(B{r}=0,"",_xlfn.MAXIFS(Log!$C$4:$C$2000,{Ld},">="&{lo},{Ld},"<"&{hi}))'
header(sm, ["", "Readings", "Avg systolic", "Avg diastolic", "Avg pulse"], [12, 10, 12, 12, 10], row=19, freeze=False)
T = "Log!$B$4:$B$2000"
for r, (n, crit) in enumerate([("Morning (before 12:00)", ('"<"&TIME(12,0,0)',)), ("Evening (from 12:00)", ('">="&TIME(12,0,0)',)), ("Last 7 days", None), ("All readings", ())], 20):
    sm[f"A{r}"] = n; sm[f"A{r}"].font = Font(bold=True)
    if crit is None: cc = f',{Ld},">="&TODAY()-6'
    elif crit: cc = f",{T},{crit[0]}"
    else: cc = ""
    sm[f"B{r}"] = f'=COUNTIFS(Log!$C$4:$C$2000,"<>"{cc})'
    for c, src in [("C", "C"), ("D", "D"), ("E", "E")]:
        sm[f"{c}{r}"] = f'=IFERROR(AVERAGEIFS(Log!${src}$4:${src}$2000,Log!$C$4:$C$2000,"<>"{cc}),"")'; sm[f"{c}{r}"].number_format = "0"
sm.column_dimensions["A"].width = 24
sm["A25"] = "Categories follow common adult guidelines (normal under 120/80, high from 130/80). They are a guide only. Always follow the advice of your doctor or nurse."; sm["A25"].font = Font(italic=True, color="777777")
lc = LineChart(); lc.title = "Readings"; lc.height = 8; lc.width = 22
lc.add_data(Reference(lg, min_col=3, max_col=4, min_row=3, max_row=63), titles_from_data=True); lc.set_categories(Reference(lg, min_col=1, min_row=4, max_row=63)); sm.add_chart(lc, "H3")
howto(wb, C, ["1. Log: enter each reading with the date, time, top number (systolic), bottom number (diastolic) and pulse. The category fills in and is colour-coded.",
              "2. Take readings at the same times each day, sitting quietly for 5 minutes first, and note which arm you used. Many people take two readings a minute apart and log both.",
              "3. Averages shows monthly averages, highest reading, morning vs evening and the last 7 days. It's handy to print or share with your doctor.", "4. Weight and medication columns are optional. Delete the sample readings first.",
              "5. This log is not medical advice. If a reading is very high or you feel unwell, contact a doctor or emergency services."])
wb.save(OUT / "Blood-Pressure-Health-Log.xlsx")

# 5. Decision matrix & comparison
C = "E67700"; title, header = kit(C); wb = Workbook(); dm = wb.active; dm.title = "Decision matrix"
title(dm, "Decision Matrix", "Weight what matters, score each option from 1 to 10, and let the totals pick the winner.")
dm["A3"] = "Decision"; dm["B3"] = "Which laptop should I buy?"; dm["A3"].font = Font(bold=True); dm["B3"].fill = SOFT
opts = ["Option A", "Option B", "Option C", "Option D", "Option E", "Option F"]; names = ["Laptop Air", "Laptop Pro", "Budget Book", "", "", ""]
header(dm, ["Criterion", "Weight (1-5)"] + opts, [26, 12] + [13] * 6, row=5, freeze=False)
for i, n in enumerate(names):
    x = dm.cell(6, 3 + i, n); x.fill = SOFT; x.font = Font(bold=True); x.alignment = Alignment(horizontal="center")
dm["A6"] = "Option name →"; dm["A6"].font = Font(italic=True, color="777777")
crit = [("Price", 5, [6, 3, 9]), ("Battery life", 4, [8, 9, 5]), ("Performance", 3, [7, 10, 4]), ("Weight / portability", 3, [9, 6, 6]), ("Screen", 2, [7, 9, 5]), ("Build quality", 2, [8, 9, 5])]
for r, (n, w, sc) in enumerate(crit, 7):
    dm[f"A{r}"] = n; dm[f"B{r}"] = w
    for i, s in enumerate(sc): dm.cell(r, 3 + i, s)
dv(dm, '"1,2,3,4,5"', "B7:B16")
v = DataValidation(type="whole", operator="between", formula1="0", formula2="10", allow_blank=True); dm.add_data_validation(v); v.add("C7:H16")
for r in range(7, 17):
    for c in range(3, 9): dm.cell(r, c).alignment = Alignment(horizontal="center")
dm.conditional_formatting.add("C7:H16", __import__("openpyxl").formatting.rule.ColorScaleRule(start_type="num", start_value=1, start_color="FFC9C9", mid_type="num", mid_value=5, mid_color="FFF3BF", end_type="num", end_value=10, end_color="B2F2BB"))
for r, lab in [(18, "Weighted score"), (19, "Score out of 100"), (20, "Rank")]:
    dm[f"A{r}"] = lab; dm[f"A{r}"].font = Font(bold=True)
for i in range(6):
    cl = L(3 + i)
    dm[f"{cl}18"] = f'=IF({cl}6="","",SUMPRODUCT($B$7:$B$16,{cl}7:{cl}16))'
    dm[f"{cl}19"] = f'=IF({cl}6="","",IFERROR({cl}18/(SUM($B$7:$B$16)*10)*100,0))'; dm[f"{cl}19"].number_format = "0"
    dm[f"{cl}20"] = f'=IF({cl}6="","",RANK({cl}18,$C$18:$H$18))'
    for rr in (18, 19, 20): dm[f"{cl}{rr}"].alignment = Alignment(horizontal="center"); dm[f"{cl}{rr}"].font = Font(bold=True)
dm.conditional_formatting.add("C20:H20", CellIsRule(operator="equal", formula=["1"], fill=PatternFill("solid", fgColor="FFD43B")))
dm["A22"] = "Winner"; dm["A22"].font = Font(bold=True, size=14, color=C)
dm["B22"] = '=IFERROR(INDEX(C6:H6,MATCH(MAX(C18:H18),C18:H18,0)),"")'; dm["B22"].font = Font(bold=True, size=14)
dm["A23"] = "Runner-up"; dm["A23"].font = Font(bold=True)
dm["B23"] = '=IFERROR(INDEX(C6:H6,MATCH(LARGE(C18:H18,2),C18:H18,0)),"")'
dm["A24"] = "Margin"; dm["B24"] = '=IFERROR(MAX(C19:H19)-LARGE(C19:H19,2),"")'; dm["B24"].number_format = '0" points"'
bc = BarChart(); bc.title = "Score out of 100"; bc.height = 7; bc.width = 14; bc.legend = None
bc.add_data(Reference(dm, min_col=3, max_col=5, min_row=19, max_row=19), from_rows=True); bc.set_categories(Reference(dm, min_col=3, max_col=5, min_row=6, max_row=6)); dm.add_chart(bc, "J5")
tc = wb.create_sheet("Cost comparison"); title(tc, "Total cost of ownership", "The cheapest price is not always the cheapest choice. Add running costs and resale value.")
header(tc, ["", "Option A", "Option B", "Option C", "Option D"], [30, 14, 14, 14, 14], freeze=False)
lines_ = [("Name", "Laptop Air", "Laptop Pro", "Budget Book", ""), ("Purchase price", 1100, 1800, 550, None), ("Running cost per year", 40, 40, 90, None), ("Years you'll keep it", 5, 6, 3, None), ("Expected resale value", 300, 500, 50, None)]
for r, row in enumerate(lines_, 4):
    for c, val in enumerate(row, 1): tc.cell(r, c, val)
for c in "BCDE":
    tc[f"{c}9"] = f'=IF({c}4="","",{c}5+{c}6*{c}7-{c}8)'; tc[f"{c}10"] = f'=IF(OR({c}4="",N({c}7)=0),"",{c}9/{c}7)'
    for r in (5, 6, 8, 9, 10): tc[f"{c}{r}"].number_format = M
    tc[f"{c}4"].font = Font(bold=True)
tc["A9"] = "Total cost of ownership"; tc["A10"] = "Cost per year"; tc["A9"].font = tc["A10"].font = Font(bold=True)
tc["A12"] = "Cheapest per year"; tc["A12"].font = Font(bold=True, color=C); tc["B12"] = '=IFERROR(INDEX(B4:E4,MATCH(MIN(B10:E10),B10:E10,0)),"")'
tc.conditional_formatting.add("B10:E10", FormulaRule(formula=['AND(B10<>"",B10=MIN($B$10:$E$10))'], fill=PatternFill("solid", fgColor="B2F2BB")))
pc_ = wb.create_sheet("Pros & cons"); title(pc_, "Pros & cons", "For decisions that are hard to score. Rate how much each point matters (1-5).")
for i, (cl, h) in enumerate([("A", "Pros"), ("B", "Weight"), ("D", "Cons"), ("E", "Weight")]):
    x = pc_[f"{cl}4"]; x.value = h; x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor="2B8A3E" if cl in "AB" else "C92A2A")
pc_.column_dimensions["A"].width = pc_.column_dimensions["D"].width = 36; pc_.column_dimensions["B"].width = pc_.column_dimensions["E"].width = 9
for r, (p, w, cn, w2) in enumerate([("Lasts longer", 4, "Costs more up front", 5), ("Faster for video editing", 3, "Heavier to carry", 2), ("Better resale value", 2, "", None)], 5):
    pc_[f"A{r}"], pc_[f"B{r}"], pc_[f"D{r}"], pc_[f"E{r}"] = p, w, cn, w2
dv(pc_, '"1,2,3,4,5"', "B5:B24"); dv(pc_, '"1,2,3,4,5"', "E5:E24")
pc_["A26"] = "Pros total"; pc_["B26"] = "=SUM(B5:B24)"; pc_["D26"] = "Cons total"; pc_["E26"] = "=SUM(E5:E24)"
pc_["A28"] = "Verdict"; pc_["B28"] = '=IF(B26>E26,"Go for it",IF(B26<E26,"Probably not","Too close to call: sleep on it"))'
for c in ("A26", "D26", "A28", "B28"): pc_[c].font = Font(bold=True)
howto(wb, C, ["1. Decision matrix: name your options in the yellow row, list what matters to you as criteria and give each a weight from 1 (nice to have) to 5 (essential).",
              "2. Score every option from 1 to 10 on each criterion. The weighted totals, a score out of 100, the ranking and the winner are worked out for you.",
              "3. Cost comparison adds running costs and resale value, so you can see the real cost per year. Pros & cons is a quick check for yes/no decisions.",
              "4. Works for anything: a car, a flat, a job offer, a supplier, a university or a holiday. Replace the sample laptop example with your own."])
wb.save(OUT / "Decision-Matrix-Comparison.xlsx")
print("built 5")
