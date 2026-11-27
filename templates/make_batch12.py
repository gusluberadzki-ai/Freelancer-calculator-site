"""Round 17 spreadsheet products into products/. Run: python3 make_batch12.py (reuses helpers from make_batch2.py)"""
import pathlib, random
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
from openpyxl.chart import PieChart
today = dt.date.today(); y = today.year
random.seed(17)
def kpis(ws, rows, start=4, wa=28, wb_=14):
    for r, (a, f, nf_) in enumerate(rows, start):
        ws[f"A{r}"] = a; ws[f"B{r}"] = f; ws[f"B{r}"].number_format = nf_; ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
    ws.column_dimensions["A"].width = wa; ws.column_dimensions["B"].width = wb_
def inputs(ws, rows, start=4, color="DBE4FF"):
    for r, (n, v, f) in enumerate(rows, start):
        ws[f"A{r}"] = n; ws[f"A{r}"].font = Font(bold=True)
        if v is not None: ws[f"B{r}"] = v; ws[f"B{r}"].fill = PatternFill("solid", fgColor=color)
        if f: ws[f"B{r}"].number_format = f

# 1. Secret Santa organiser
C = "C92A2A"; title, header = kit(C); wb = Workbook(); pp = wb.active; pp.title = "Draw"
title(pp, "Secret Santa Draw", "Add names, then change the draw number until it says 'All good'. Nobody gets themselves, and people in the same household are kept apart.")
pp["A3"] = "Draw number (change to reshuffle)"; pp["A3"].font = Font(bold=True); pp["D3"] = 7; pp["D3"].fill = PatternFill("solid", fgColor="FFE3E3"); pp["D3"].font = Font(bold=True, size=13)
pp["F3"] = '=IF(COUNTA(A6:A105)<3,"Add at least 3 people",IF(COUNTIF(H6:H105,"Clash")>0,"Same household paired: change the draw number","All good ✓"))'; pp["F3"].font = Font(bold=True, size=12, color=C)
header(pp, ["Name", "Household / couple (optional)", "Wish list / ideas", "Shuffle key", "Order", "Buys a gift for", "Their wish list", "Check"], [18, 22, 32, 11, 8, 18, 32, 9], row=5)
people = [("Anna", "Home 1", "Books, cosy socks"), ("Tom", "Home 1", "Coffee, board games"), ("Priya", "Home 2", "Candles, plants"), ("Luca", "Home 2", "Football stuff"), ("Maya", "", "Art supplies"),
          ("Sam", "Home 3", "Puzzles"), ("Jo", "Home 3", "Gin, chocolate"), ("Ben", "", "Gadgets"), ("Ella", "", "Jewellery, bath bombs"), ("Kofi", "", "Music, vinyl")]
for r, (n, h, w) in enumerate(people, 6): pp[f"A{r}"], pp[f"B{r}"], pp[f"C{r}"] = n, h or None, w
N = "COUNTA($A$6:$A$105)"
for r in range(6, 106):
    pp[f"D{r}"] = f'=IF(A{r}="","",MOD($D$3*7919+ROW()*ROW()*104729+ROW()*$D$3*31,100003)+ROW()/1000)'
    pp[f"E{r}"] = f'=IF(A{r}="","",COUNTIF($D$6:$D$105,"<"&D{r})+1)'
    pp[f"F{r}"] = f'=IF(A{r}="","",INDEX($A$6:$A$105,MATCH(IF(E{r}={N},1,E{r}+1),$E$6:$E$105,0)))'
    pp[f"G{r}"] = f'=IF(F{r}="","",INDEX($C$6:$C$105,MATCH(F{r},$A$6:$A$105,0))&"")'
    pp[f"H{r}"] = f'=IF(OR(F{r}="",B{r}=""),IF(F{r}="","","OK"),IF(INDEX($B$6:$B$105,MATCH(F{r},$A$6:$A$105,0))=B{r},"Clash","OK"))'
pp.column_dimensions["D"].hidden = False
pp.conditional_formatting.add("H6:H105", CellIsRule(operator="equal", formula=['"Clash"'], fill=PatternFill("solid", fgColor="FFC9C9"), font=Font(bold=True, color="C0392B")))
pp.conditional_formatting.add("H6:H105", CellIsRule(operator="equal", formula=['"OK"'], font=Font(color="2B8A3E")))
pp.conditional_formatting.add("F3", FormulaRule(formula=['ISNUMBER(SEARCH("All good",F3))'], fill=PatternFill("solid", fgColor="D3F9D8")))
for c in "DE": pp[f"{c}5"].font = Font(bold=True, color="FFFFFF")
st = wb.create_sheet("Details", 1); title(st, "Exchange details", "Shown on every card.")
inputs(st, [("Event", "Family Christmas", None), ("Exchange date", dt.date(y, 12, 20), "dddd dd mmmm yyyy"), ("Spending limit", 25, M), ("Where", "Grandma's house", None), ("Organiser", "Anna", None)], color="FFE3E3")
st.column_dimensions["A"].width = 18; st.column_dimensions["B"].width = 30
cd = wb.create_sheet("Cards", 2); cd["A1"] = "Secret Santa cards"; cd["A1"].font = Font(bold=True, size=18, color=C)
cd["A2"] = "Print this sheet, cut along the rows and fold each card so only the name on the left shows. Hand them out and keep the Draw tab hidden!"; cd["A2"].font = Font(italic=True, color="777777")
cd.column_dimensions["A"].width = 22; cd.column_dimensions["B"].width = 70
for i in range(40):
    r = 4 + i * 2; src = 6 + i
    cd[f"A{r}"] = f'=IF(Draw!A{src}="","","For "&Draw!A{src})'; cd[f"A{r}"].font = Font(bold=True, size=12, color=C)
    cd[f"B{r}"] = f'=IF(Draw!A{src}="","","You are buying for "&UPPER(Draw!F{src})&" · Limit "&TEXT(Details!$B$6,"0.00")&" · "&TEXT(Details!$B$5,"dd mmm")&" at "&Details!$B$7&IF(Draw!G{src}<>"","  ·  Ideas: "&Draw!G{src},""))'
    cd.row_dimensions[r].height = 30
    for c in "AB": cd[f"{c}{r}"].alignment = Alignment(vertical="center", wrap_text=True); cd[f"{c}{r}"].border = __import__("openpyxl").styles.Border(bottom=__import__("openpyxl").styles.Side(style="dashed", color="BBBBBB"))
cd.print_area = "A1:B83"
gt = wb.create_sheet("Gift tracker", 3); title(gt, "Gift tracker (organiser)", "Tick off as people confirm they've bought their gift.")
header(gt, ["Name", "Buying for", "Gift bought?", "Spent", "Notes"], [18, 18, 12, 10, 26])
for i in range(100):
    r = 4 + i; gt[f"A{r}"] = f'=IF(Draw!A{6 + i}="","",Draw!A{6 + i})'; gt[f"B{r}"] = f'=IF(Draw!F{6 + i}="","",Draw!F{6 + i})'; gt[f"D{r}"].number_format = M
dv(gt, '"Yes,No"', "C4:C103")
gt.conditional_formatting.add("D4:D103", CellIsRule(operator="greaterThan", formula=["Details!$B$6"], font=Font(bold=True, color="C0392B")))
gt["G3"] = "Bought"; gt["H3"] = '=COUNTIF(C4:C103,"Yes")&" of "&COUNTA(Draw!A6:A105)'; gt["G3"].font = Font(bold=True)
howto(wb, C, ["1. Draw: type everyone's name, and a household or couple label if two people shouldn't draw each other. Add wish lists if you like.",
              "2. The draw is made instantly. If the box at the top says 'Same household paired', type a different draw number until it says 'All good'. Nobody ever draws themselves.",
              "3. Details: event name, date, spending limit and place. Cards: print, cut and hand out. Each card tells one person who they buy for, with the limit and wish list.",
              "4. As organiser, hide the Draw tab (right-click > Hide) before sharing, so the surprise stays secret. Gift tracker helps you check everyone has bought a present.",
              "5. Works for families, offices, friends and classrooms, up to 100 people."])
wb.save(OUT / "Secret-Santa-Organiser.xlsx")

# 2. Reselling profit tracker
C = "087F5B"; title, header = kit(C); wb = Workbook(); fs = wb.active; fs.title = "Fees"
title(fs, "Selling platforms & fees", "Set each platform's selling fee. Defaults are examples; check current fees.")
header(fs, ["Platform", "Fee % of sale", "Fixed fee per sale", "Fee on postage too?"], [18, 13, 16, 18], freeze=False)
plats = [("eBay", 0.128, 0.30, "Yes"), ("Vinted", 0.0, 0.0, "No"), ("Depop", 0.10, 0.0, "Yes"), ("Facebook", 0.0, 0.0, "No"), ("Etsy", 0.095, 0.50, "Yes"), ("Local / cash", 0.0, 0.0, "No"), ("", None, None, None), ("", None, None, None)]
for r, (p, a, b, c) in enumerate(plats, 4):
    fs[f"A{r}"] = p or None; fs[f"B{r}"] = a; fs[f"C{r}"] = b; fs[f"D{r}"] = c; fs[f"B{r}"].number_format = "0.0%"; fs[f"C{r}"].number_format = M
dv(fs, '"Yes,No"', "D4:D11")
it = wb.create_sheet("Items", 0); title(it, "Stock & sales", "One row per item. Profit, return on cost and days to sell are worked out.")
header(it, ["SKU", "Item", "Category", "Bought from", "Date bought", "Cost", "Listed on", "Listed price", "Sold on", "Date sold", "Sold price", "Postage charged", "Postage paid", "Fees", "Profit", "Return on cost", "Days to sell", "Status"],
       [8, 24, 12, 14, 11, 9, 11, 10, 11, 11, 10, 11, 10, 9, 10, 11, 10, 10])
cats = ["Clothing", "Shoes", "Books", "Toys", "Electronics", "Homeware", "Collectables", "Other"]
srcs = ["Charity shop", "Car boot", "Clearance", "Online", "Own stuff"]
names = {"Clothing": ["Barbour jacket", "Vintage denim jacket", "Wool jumper", "Party dress"], "Shoes": ["Dr Martens boots", "Running trainers"], "Books": ["Signed hardback", "Cookbook bundle"], "Toys": ["LEGO set", "Board game"],
         "Electronics": ["Retro games console", "Bluetooth speaker"], "Homeware": ["Pyrex dish set", "Retro lamp"], "Collectables": ["Vinyl LP", "Football programme"], "Other": ["Camera lens"]}
r = 4
for k in range(34):
    c = random.choice(cats); cost = random.choice([1, 2, 3, 4, 5, 8, 10, 15]); bd = today - dt.timedelta(days=random.randint(5, 200)); pl = random.choice(["eBay", "Vinted", "Depop", "eBay", "Facebook"])
    it[f"A{r}"] = f"R{k + 1:03d}"; it[f"B{r}"] = random.choice(names[c]); it[f"C{r}"] = c; it[f"D{r}"] = random.choice(srcs); it[f"E{r}"] = bd; it[f"F{r}"] = cost; it[f"G{r}"] = pl
    lp = round(cost * random.uniform(2.5, 6)) + 4; it[f"H{r}"] = lp
    if random.random() < 0.68:
        sd = bd + dt.timedelta(days=random.randint(2, 60))
        if sd < today:
            it[f"I{r}"] = pl; it[f"J{r}"] = sd; it[f"K{r}"] = round(lp * random.uniform(0.75, 1.0), 2); it[f"L{r}"] = random.choice([0, 3.5, 4]) if pl == "eBay" else 0; it[f"M{r}"] = random.choice([3.2, 3.5, 4.2]) if pl == "eBay" else 0
    r += 1
dv(it, '"' + ",".join(cats) + '"', "C4:C3000"); dv(it, '"' + ",".join(srcs) + '"', "D4:D3000"); dv(it, "=Fees!$A$4:$A$11", "G4:G3000"); dv(it, "=Fees!$A$4:$A$11", "I4:I3000")
for r in range(4, 3001):
    it[f"E{r}"].number_format = it[f"J{r}"].number_format = "dd mmm yy"
    it[f"N{r}"] = f'=IF(OR(I{r}="",K{r}=""),"",IFERROR((N(K{r})+IF(VLOOKUP(I{r},Fees!$A$4:$D$11,4,FALSE)="Yes",N(L{r}),0))*VLOOKUP(I{r},Fees!$A$4:$D$11,2,FALSE)+VLOOKUP(I{r},Fees!$A$4:$D$11,3,FALSE),0))'
    it[f"O{r}"] = f'=IF(OR(I{r}="",K{r}=""),"",N(K{r})+N(L{r})-N(M{r})-N{r}-N(F{r}))'
    it[f"P{r}"] = f'=IF(OR(O{r}="",N(F{r})=0),"",O{r}/F{r})'
    it[f"Q{r}"] = f'=IF(OR(J{r}="",E{r}=""),IF(AND(B{r}<>"",E{r}<>""),TODAY()-E{r},""),J{r}-E{r})'
    it[f"R{r}"] = f'=IF(B{r}="","",IF(K{r}<>"","Sold",IF(G{r}<>"","Listed","To list")))'
    for c in "FHKLMNO": it[f"{c}{r}"].number_format = M
    it[f"P{r}"].number_format = "0%"
for s, col in [("Sold", "D3F9D8"), ("Listed", "D0EBFF"), ("To list", "FFF3BF")]:
    it.conditional_formatting.add("R4:R3000", CellIsRule(operator="equal", formula=[f'"{s}"'], fill=PatternFill("solid", fgColor=col)))
it.conditional_formatting.add("Q4:Q3000", FormulaRule(formula=['AND(ISNUMBER(Q4),R4<>"Sold",Q4>60)'], font=Font(bold=True, color="C0392B")))
it.conditional_formatting.add("O4:O3000", CellIsRule(operator="lessThan", formula=["0"], font=Font(bold=True, color="C0392B")))
it.freeze_panes = "C4"
db = wb.create_sheet("Dashboard", 0); title(db, "Reselling Dashboard", "Pick a year. Sales count in the month they sold.")
db["A3"] = "Year"; db["B3"] = y; db["B3"].fill = SOFT; db["A3"].font = Font(bold=True)
Y = 'Items!$J$4:$J$3000,">="&DATE($B$3,1,1),Items!$J$4:$J$3000,"<"&DATE($B$3+1,1,1)'
kpis(db, [("Items sold", f"=COUNTIFS({Y})", "0"), ("Sales (incl. postage)", f"=SUMIFS(Items!$K$4:$K$3000,{Y})+SUMIFS(Items!$L$4:$L$3000,{Y})", M), ("Fees paid", f"=SUMIFS(Items!$N$4:$N$3000,{Y})", M),
          ("Profit", f"=SUMIFS(Items!$O$4:$O$3000,{Y})", M), ("Average profit per item", "=IFERROR(B7/B4,0)", M), ("Average return on cost", f'=IFERROR(B7/SUMIFS(Items!$F$4:$F$3000,{Y}),0)', "0%"),
          ("Average days to sell", f'=IFERROR(AVERAGEIFS(Items!$Q$4:$Q$3000,{Y}),"")', "0"), ("Unsold items", '=COUNTIF(Items!R4:R3000,"Listed")+COUNTIF(Items!R4:R3000,"To list")', "0"),
          ("Money tied up in stock", '=SUMIFS(Items!F4:F3000,Items!R4:R3000,"Listed")+SUMIFS(Items!F4:F3000,Items!R4:R3000,"To list")', M), ("Potential sales (listed prices)", '=SUMIFS(Items!H4:H3000,Items!R4:R3000,"Listed")', M),
          ("Stale stock (60+ days)", '=COUNTIFS(Items!R4:R3000,"<>Sold",Items!R4:R3000,"<>",Items!Q4:Q3000,">60")', "0")], start=4, wa=30)
db["B7"].font = Font(bold=True, size=13, color=C)
header(db, ["Month", "Sold", "Profit"], [30, 9, 12], row=17, freeze=False)
for i, m in enumerate(MONTHS):
    r = 18 + i; db[f"A{r}"] = m; cond = f'Items!$J$4:$J$3000,">="&DATE($B$3,{i + 1},1),Items!$J$4:$J$3000,"<"&DATE($B$3,{i + 2},1)'
    db[f"B{r}"] = f"=COUNTIFS({cond})"; db[f"C{r}"] = f"=SUMIFS(Items!$O$4:$O$3000,{cond})"; db[f"C{r}"].number_format = M
header(db, ["Category", "Sold", "Profit", "Avg days"], [30, 9, 12, 10], row=31, freeze=False)
for i, c in enumerate(cats):
    r = 32 + i; db[f"A{r}"] = c; db[f"B{r}"] = f"=COUNTIFS(Items!$C$4:$C$3000,A{r},{Y})"; db[f"C{r}"] = f"=SUMIFS(Items!$O$4:$O$3000,Items!$C$4:$C$3000,A{r},{Y})"; db[f"C{r}"].number_format = M
    db[f"D{r}"] = f'=IFERROR(AVERAGEIFS(Items!$Q$4:$Q$3000,Items!$C$4:$C$3000,A{r},{Y}),"")'; db[f"D{r}"].number_format = "0"
header(db, ["Platform", "Sold", "Profit"], [30, 9, 12], row=41, freeze=False)
for i in range(6):
    r = 42 + i; db[f"A{r}"] = f'=IF(Fees!A{4 + i}="","",Fees!A{4 + i})'; db[f"B{r}"] = f'=IF(A{r}="","",COUNTIFS(Items!$I$4:$I$3000,A{r},{Y}))'
    db[f"C{r}"] = f'=IF(A{r}="","",SUMIFS(Items!$O$4:$O$3000,Items!$I$4:$I$3000,A{r},{Y}))'; db[f"C{r}"].number_format = M
bc = BarChart(); bc.title = "Profit by month"; bc.height = 7; bc.width = 16; bc.legend = None
bc.add_data(Reference(db, min_col=3, min_row=17, max_row=29), titles_from_data=True); bc.set_categories(Reference(db, min_col=1, min_row=18, max_row=29)); db.add_chart(bc, "F3")
bc2 = BarChart(); bc2.type = "bar"; bc2.title = "Profit by category"; bc2.height = 7; bc2.width = 16; bc2.legend = None
bc2.add_data(Reference(db, min_col=3, min_row=31, max_row=39), titles_from_data=True); bc2.set_categories(Reference(db, min_col=1, min_row=32, max_row=39)); db.add_chart(bc2, "F18")
howto(wb, C, ["1. Fees: set each selling platform's fee percentage, fixed fee per sale and whether the fee is also charged on postage. Check current fees.",
              "2. Items: one row per item with what you paid, where from, where it's listed and the asking price. When it sells, add the platform, date, sale price and postage. Fees, profit, return on cost and days to sell fill in.",
              "3. Status shows To list, Listed or Sold. Unsold items older than 60 days turn red so you can reprice or bundle them.",
              "4. Dashboard: items sold, sales, fees, profit, return on cost, average days to sell, money tied up in stock, and profit by month, category and platform.",
              "5. For charity-shop flippers, car-boot resellers and decluttering. Delete the sample items first."])
wb.save(OUT / "Reselling-Profit-Tracker.xlsx")

# 3. Car loan & affordability calculator
C = "364FC7"; title, header = kit(C); wb = Workbook(); ca = wb.active; ca.title = "Calculator"
title(ca, "Car Loan & Affordability", "Change the blue cells. See the monthly payment, total cost and whether it fits your budget.")
inputs(ca, [("THE CAR", None, None), ("Car price", 22000, M), ("Deposit / down payment", 3000, M), ("Trade-in value", 2500, M), ("Fees added to loan", 300, M),
            ("THE LOAN", None, None), ("Interest rate (APR)", 0.069, "0.00%"), ("Term (months)", 48, "0"),
            ("RUNNING COSTS (per month)", None, None), ("Insurance", 70, M), ("Fuel / charging", 120, M), ("Maintenance & tyres", 40, M), ("Tax, parking & other", 25, M),
            ("YOUR BUDGET", None, None), ("Monthly take-home pay", 3600, M), ("Max share of pay for all car costs", 0.15, "0%")])
for r in (4, 9, 12, 17): ca[f"A{r}"].font = Font(bold=True, color=C)
ca.column_dimensions["A"].width = 38; ca.column_dimensions["B"].width = 14
ca["A21"] = "RESULTS"; ca["A21"].font = Font(bold=True, color=C)
res = [("Loan amount", "=MAX(0,B5-B6-B7+B8)", M), ("Monthly loan payment", "=IF(B22=0,0,IF(B10=0,B22/B11,PMT(B10/12,B11,-B22)))", M), ("Total interest", "=B23*B11-B22", M),
       ("Total paid for the car", "=B6+B7+B23*B11", M), ("Running costs per month", "=SUM(B13:B16)", M), ("Total monthly cost of the car", "=B23+B26", M),
       ("Share of take-home pay", "=IFERROR(B27/B18,0)", "0%"), ("Verdict", '=IF(B28<=B19,"Fits your budget ✓",IF(B28<=B19*1.33,"Tight: consider a longer term, bigger deposit or cheaper car","Over budget"))', "@"),
       ("Most you could borrow at this payment limit", "=IF(B10=0,MAX(0,B18*B19-B26)*B11,MAX(0,PV(B10/12,B11,-(B18*B19-B26))))", M)]
for r, (n, f, nf_) in enumerate(res, 22):
    ca[f"A{r}"] = n; ca[f"A{r}"].font = Font(bold=True); ca[f"B{r}"] = f; ca[f"B{r}"].number_format = nf_; ca[f"B{r}"].fill = SOFT
ca["B23"].font = Font(bold=True, size=14, color=C); ca["B29"].font = Font(bold=True, color=C)
ca.conditional_formatting.add("B28", FormulaRule(formula=["B28>B19"], font=Font(bold=True, color="C0392B")))
ca.conditional_formatting.add("B28", FormulaRule(formula=["B28<=B19"], font=Font(bold=True, color="2B8A3E")))
header(ca, ["Term (months)", "Monthly payment", "Total interest", "Monthly car cost", "Share of pay"], [14, 15, 14, 15, 12], row=32, freeze=False)
for i, t in enumerate([24, 36, 48, 60, 72, 84]):
    r = 33 + i; ca[f"A{r}"] = t
    ca[f"B{r}"] = f"=IF($B$22=0,0,IF($B$10=0,$B$22/A{r},PMT($B$10/12,A{r},-$B$22)))"; ca[f"C{r}"] = f"=B{r}*A{r}-$B$22"; ca[f"D{r}"] = f"=B{r}+$B$26"; ca[f"E{r}"] = f"=IFERROR(D{r}/$B$18,0)"
    for c in "BCD": ca[f"{c}{r}"].number_format = M
    ca[f"E{r}"].number_format = "0%"
ca.conditional_formatting.add("E33:E38", FormulaRule(formula=["E33<=$B$19"], fill=PatternFill("solid", fgColor="D3F9D8")))
ca.conditional_formatting.add("E33:E38", FormulaRule(formula=["E33>$B$19"], fill=PatternFill("solid", fgColor="FFE3E3")))
ca["A40"] = "Estimates only. Your lender's figures, fees and balloon payments may differ. Not financial advice."; ca["A40"].font = Font(italic=True, color="777777")
sc = wb.create_sheet("Schedule"); title(sc, "Payment schedule", "Month by month from the Calculator tab.")
header(sc, ["Month", "Payment", "Interest", "Principal", "Balance left"], [9, 12, 12, 12, 14])
for i in range(84):
    r = 4 + i; sc[f"A{r}"] = i + 1
    prev = "Calculator!$B$22" if i == 0 else f"E{r - 1}"
    sc[f"B{r}"] = f'=IF(A{r}>Calculator!$B$11,"",Calculator!$B$23)'
    sc[f"C{r}"] = f'=IF(B{r}="","",{prev}*Calculator!$B$10/12)'
    sc[f"D{r}"] = f'=IF(B{r}="","",B{r}-C{r})'
    sc[f"E{r}"] = f'=IF(B{r}="","",MAX(0,{prev}-D{r}))'
    for c in "BCDE": sc[f"{c}{r}"].number_format = M
lc = LineChart(); lc.title = "Balance left"; lc.height = 8; lc.width = 16; lc.legend = None
lc.add_data(Reference(sc, min_col=5, min_row=3, max_row=87), titles_from_data=True); lc.set_categories(Reference(sc, min_col=1, min_row=4, max_row=87)); ca.add_chart(lc, "D4")
howto(wb, C, ["1. Calculator: change the blue cells: car price, deposit, trade-in, fees, interest rate (APR), loan term, monthly running costs and your take-home pay.",
              "2. See the monthly payment, total interest, total paid, full monthly cost of owning the car and what share of your pay it takes, with a simple verdict.",
              "3. The term table compares 24 to 84 months side by side (green = fits your budget). 'Most you could borrow' shows the biggest loan your budget allows.",
              "4. Schedule: month-by-month interest, principal and balance. Estimates only; check your lender's figures."])
wb.save(OUT / "Car-Loan-Affordability-Calculator.xlsx")

# 4. Baby budget planner
C = "1098AD"; title, header = kit(C); wb = Workbook(); oo = wb.active; oo.title = "One-off items"
title(oo, "Baby shopping list & budget", "Everything to buy before and after baby arrives. Mark what's gifted or second-hand to see the savings.")
header(oo, ["Category", "Item", "Need it?", "Budget", "Actual cost", "Source", "Bought?", "Notes"], [14, 26, 9, 10, 11, 14, 9, 24])
items = {"Nursery": [("Cot / crib", 150), ("Cot mattress", 60), ("Fitted sheets x3", 20), ("Baby monitor", 60), ("Changing mat", 15), ("Blackout blind", 20), ("Night light", 12)],
         "Travel": [("Car seat", 150), ("Pram / pushchair", 350), ("Baby carrier / sling", 50), ("Changing bag", 30)],
         "Feeding": [("Bottles & teats", 30), ("Steriliser", 40), ("Breast pump", 60), ("Muslins x10", 15), ("Bibs", 10), ("High chair (later)", 80)],
         "Clothing": [("Bodysuits x8", 25), ("Sleepsuits x8", 30), ("Hats & mittens", 8), ("Sleeping bags x2", 40), ("Snowsuit / pramsuit", 25)],
         "Bath & health": [("Baby bath", 15), ("Hooded towels", 15), ("Thermometer", 15), ("Nail clippers", 5), ("First aid kit", 15)],
         "Hospital bag": [("Nappies newborn", 8), ("Going-home outfit", 10), ("Maternity pads", 6)]}
r = 4
for cat, its in items.items():
    for n, b in its:
        oo[f"A{r}"] = cat; oo[f"B{r}"] = n; oo[f"C{r}"] = "Yes"; oo[f"D{r}"] = b
        src = random.choice(["New", "New", "New", "Gifted", "Second-hand"]); oo[f"F{r}"] = src
        if random.random() < 0.55:
            oo[f"G{r}"] = "Yes"; oo[f"E{r}"] = 0 if src == "Gifted" else round(b * (0.45 if src == "Second-hand" else random.uniform(0.85, 1.1)))
        r += 1
dv(oo, '"Nursery,Travel,Feeding,Clothing,Bath & health,Hospital bag,Toys & play,Other"', "A4:A300"); dv(oo, '"Yes,Maybe,No"', "C4:C300"); dv(oo, '"New,Second-hand,Gifted,Borrowed"', "F4:F300"); dv(oo, '"Yes,No"', "G4:G300")
for r in range(4, 301): oo[f"D{r}"].number_format = oo[f"E{r}"].number_format = M
oo.conditional_formatting.add("A4:H300", FormulaRule(formula=['$G4="Yes"'], font=Font(color="868E96")))
oo.conditional_formatting.add("F4:F300", FormulaRule(formula=['OR(F4="Gifted",F4="Borrowed")'], fill=PatternFill("solid", fgColor="D3F9D8")))
mo = wb.create_sheet("Monthly costs", 1); title(mo, "Ongoing monthly costs", "Typical costs per month in each stage. Edit to suit you.")
header(mo, ["Cost", "0-6 months", "6-12 months", "Notes"], [24, 13, 13, 30])
for r, (n, a, b) in enumerate([("Nappies & wipes", 45, 40), ("Formula / feeding", 50, 40), ("Baby food", 0, 30), ("Clothes (growing!)", 20, 20), ("Toiletries & laundry", 12, 12), ("Childcare", 0, 600), ("Activities & classes", 20, 30), ("Toys & books", 10, 15), ("Other", 15, 15)], 4):
    mo[f"A{r}"], mo[f"B{r}"], mo[f"C{r}"] = n, a, b
for r in range(4, 21): mo[f"B{r}"].number_format = mo[f"C{r}"].number_format = M
mo["A22"] = "Total per month"; mo["A22"].font = Font(bold=True); mo["B22"] = "=SUM(B4:B20)"; mo["C22"] = "=SUM(C4:C20)"
for c in "BC": mo[f"{c}22"].number_format = M; mo[f"{c}22"].font = Font(bold=True, color=C)
sv = wb.create_sheet("Summary", 0); title(sv, "Baby Budget Summary", "Your plan at a glance.")
inputs(sv, [("Due date", dt.date(y + 1, 3, 15), "dd mmm yyyy"), ("Saved so far", 900, M), ("Expected income change per month on leave", -800, M)], color="C5F6FA")
kpis(sv, [("One-off items budget (needed)", '=SUMIFS(\'One-off items\'!D4:D300,\'One-off items\'!C4:C300,"Yes")', M),
          ("Spent so far", "=SUM('One-off items'!E4:E300)", M),
          ("Still to buy (budget)", '=SUMIFS(\'One-off items\'!D4:D300,\'One-off items\'!C4:C300,"Yes",\'One-off items\'!G4:G300,"<>Yes")', M),
          ("Saved by gifts & second-hand", "=SUMPRODUCT(('One-off items'!G4:G300=\"Yes\")*('One-off items'!F4:F300<>\"New\"),'One-off items'!D4:D300-'One-off items'!E4:E300)", M),
          ("Monthly costs: first 6 months", "='Monthly costs'!B22", M), ("Monthly costs: 6-12 months", "='Monthly costs'!C22", M),
          ("Estimated first-year cost", "=B8+B10+6*B12+6*B13", M), ("Months until due date", "=MAX(0,DATEDIF(TODAY(),B4,\"m\"))", "0"),
          ("Save per month to cover items + 3 months of costs", "=IFERROR(MAX(0,(B10+3*B12-B5)/MAX(1,B15)),0)", M), ("Items still to buy", '=COUNTIFS(\'One-off items\'!C4:C300,"Yes",\'One-off items\'!G4:G300,"<>Yes")', "0")], start=8, wa=44)
sv["B14"].font = Font(bold=True, size=13, color=C); sv["B16"].font = Font(bold=True, size=13, color=C)
header(sv, ["Category", "Budget", "Spent"], [44, 14, 12], row=20, freeze=False)
for i, c in enumerate(items):
    r = 21 + i; sv[f"A{r}"] = c; sv[f"B{r}"] = f'=SUMIFS(\'One-off items\'!$D$4:$D$300,\'One-off items\'!$A$4:$A$300,A{r},\'One-off items\'!$C$4:$C$300,"Yes")'
    sv[f"C{r}"] = f"=SUMIFS('One-off items'!$E$4:$E$300,'One-off items'!$A$4:$A$300,A{r})"
    for x in "BC": sv[f"{x}{r}"].number_format = M
bc = BarChart(); bc.title = "Budget vs spent by category"; bc.height = 8; bc.width = 16
bc.add_data(Reference(sv, min_col=2, min_row=20, max_row=26), titles_from_data=True); bc.add_data(Reference(sv, min_col=3, min_row=20, max_row=26), titles_from_data=True)
bc.set_categories(Reference(sv, min_col=1, min_row=21, max_row=26)); sv.add_chart(bc, "E3")
howto(wb, C, ["1. Summary: enter the due date, what you've saved and any drop in income while on leave.",
              "2. One-off items: the shopping list is ready-made with typical budgets. Mark whether you need each item, where it's coming from (new, second-hand, gifted, borrowed) and tick it off with the actual cost.",
              "3. Monthly costs: edit the typical costs for the first six months and six to twelve months, including childcare.",
              "4. Summary then shows what's left to buy, how much gifts and second-hand saved, the estimated first-year cost and how much to save each month before baby arrives.",
              "5. Prices are examples; change them to match your shops and currency."])
wb.save(OUT / "Baby-Budget-Planner.xlsx")

# 5. Credit card tracker
C = "E03131"; title, header = kit(C); wb = Workbook(); cc = wb.active; cc.title = "Cards"
title(cc, "My credit cards", "Balances, limits, rates and due dates in one place. Payment dates and interest update automatically.")
header(cc, ["Card", "Credit limit", "Balance", "Utilisation", "APR", "0% offer ends", "Days of 0% left", "Min payment %", "Min payment (fixed)", "Minimum due", "Est. interest / month", "Due day of month", "Next due date", "Days to pay"],
       [18, 11, 11, 11, 8, 12, 12, 12, 13, 12, 14, 12, 12, 10])
cards = [("Everyday Visa", 4000, 1250, 0.229, None, 0.03, 25, 15), ("Balance transfer", 6000, 3800, 0.249, today + dt.timedelta(days=210), 0.01, 25, 3), ("Store card", 1200, 480, 0.299, None, 0.03, 15, 22), ("Travel Mastercard", 3000, 0, 0.199, None, 0.025, 25, 28)]
for r, (n, l, b, a, z, mp, mf, dd) in enumerate(cards, 4):
    cc[f"A{r}"], cc[f"B{r}"], cc[f"C{r}"], cc[f"E{r}"], cc[f"F{r}"], cc[f"H{r}"], cc[f"I{r}"], cc[f"L{r}"] = n, l, b, a, z, mp, mf, dd
for r in range(4, 21):
    cc[f"D{r}"] = f'=IF(OR(A{r}="",N(B{r})=0),"",C{r}/B{r})'
    cc[f"G{r}"] = f'=IF(F{r}="","",MAX(0,F{r}-TODAY()))'
    cc[f"J{r}"] = f'=IF(A{r}="","",IF(N(C{r})<=0,0,MIN(C{r},MAX(N(I{r}),C{r}*N(H{r})))))'
    cc[f"K{r}"] = f'=IF(A{r}="","",IF(AND(F{r}<>"",F{r}>TODAY()),0,N(C{r})*N(E{r})/12))'
    cc[f"M{r}"] = f'=IF(OR(A{r}="",L{r}=""),"",IF(DAY(TODAY())<=L{r},DATE(YEAR(TODAY()),MONTH(TODAY()),L{r}),DATE(YEAR(TODAY()),MONTH(TODAY())+1,L{r})))'
    cc[f"N{r}"] = f'=IF(M{r}="","",M{r}-TODAY())'
    for c in "BCIJK": cc[f"{c}{r}"].number_format = M
    cc[f"D{r}"].number_format = "0%"; cc[f"E{r}"].number_format = "0.0%"; cc[f"H{r}"].number_format = "0.0%"; cc[f"F{r}"].number_format = cc[f"M{r}"].number_format = "dd mmm yy"
cc.conditional_formatting.add("D4:D20", CellIsRule(operator="greaterThan", formula=["0.5"], fill=PatternFill("solid", fgColor="FFC9C9"), font=Font(bold=True)))
cc.conditional_formatting.add("D4:D20", CellIsRule(operator="between", formula=["0.3", "0.5"], fill=PatternFill("solid", fgColor="FFF3BF")))
cc.conditional_formatting.add("D4:D20", CellIsRule(operator="lessThan", formula=["0.3"], fill=PatternFill("solid", fgColor="D3F9D8")))
cc.conditional_formatting.add("N4:N20", CellIsRule(operator="lessThanOrEqual", formula=["5"], font=Font(bold=True, color="C0392B")))
cc.conditional_formatting.add("G4:G20", CellIsRule(operator="lessThanOrEqual", formula=["60"], fill=PatternFill("solid", fgColor="FFE8CC")))
pl = wb.create_sheet("Payments", 1); title(pl, "Payment log", "Record each payment and new balance to see your progress.")
header(pl, ["Date", "Card", "Amount paid", "New balance", "On time?", "Notes"], [11, 18, 12, 12, 10, 24])
r = 4
for k in range(5, 0, -1):
    for n, l, b, *_ in cards[:3]:
        pl[f"A{r}"] = today - dt.timedelta(days=30 * k + random.randint(0, 3)); pl[f"B{r}"] = n; pl[f"C{r}"] = random.choice([100, 150, 200, 250]); pl[f"D{r}"] = b + k * random.choice([80, 120, 150]); pl[f"E{r}"] = "Yes"; r += 1
dv(pl, "=Cards!$A$4:$A$20", "B4:B2000"); dv(pl, '"Yes,No"', "E4:E2000")
for r in range(4, 2001): pl[f"A{r}"].number_format = "dd mmm yy"; pl[f"C{r}"].number_format = pl[f"D{r}"].number_format = M
sm = wb.create_sheet("Summary", 0); title(sm, "Credit Card Summary", "Keep utilisation under 30% and never miss a minimum payment.")
kpis(sm, [("Total credit limit", "=SUM(Cards!B4:B20)", M), ("Total balance", "=SUM(Cards!C4:C20)", M), ("Overall utilisation", "=IFERROR(B5/B4,0)", "0%"), ("Total minimum payments", "=SUM(Cards!J4:J20)", M),
          ("Estimated interest this month", "=SUM(Cards!K4:K20)", M), ("Estimated interest per year (if balances stay)", "=B8*12", M),
          ("Next payment due", '=IFERROR(INDEX(Cards!A4:A20,MATCH(_xlfn.MINIFS(Cards!N4:N20,Cards!C4:C20,">0"),Cards!N4:N20,0))&" in "&_xlfn.MINIFS(Cards!N4:N20,Cards!C4:C20,">0")&IF(_xlfn.MINIFS(Cards!N4:N20,Cards!C4:C20,">0")=1," day"," days"),"None")', "@"),
          ("Highest APR with a balance (pay this first)", '=IFERROR(INDEX(Cards!A4:A20,MATCH(_xlfn.MAXIFS(Cards!E4:E20,Cards!C4:C20,">0",Cards!K4:K20,">0"),Cards!E4:E20,0)),"None")', "@"),
          ("0% offer ending soonest", '=IFERROR(INDEX(Cards!A4:A20,MATCH(_xlfn.MINIFS(Cards!F4:F20,Cards!F4:F20,">"&TODAY()),Cards!F4:F20,0))&" ("&TEXT(_xlfn.MINIFS(Cards!F4:F20,Cards!F4:F20,">"&TODAY()),"dd mmm yy")&")","None")', "@"),
          ("Paid in the last 30 days", '=SUMIFS(Payments!C4:C2000,Payments!A4:A2000,">="&TODAY()-30)', M)], start=4, wa=44, wb_=28)
sm["B6"].font = Font(bold=True, size=13, color=C)
sm.conditional_formatting.add("B6", CellIsRule(operator="greaterThan", formula=["0.3"], font=Font(bold=True, size=13, color="C0392B")))
header(sm, ["Card", "Utilisation"], [44, 28], row=16, freeze=False)
for i in range(8):
    r = 17 + i; sm[f"A{r}"] = f'=IF(Cards!A{4 + i}="","",Cards!A{4 + i})'; sm[f"B{r}"] = f'=IF(A{r}="","",N(Cards!D{4 + i}))'; sm[f"B{r}"].number_format = "0%"
bc = BarChart(); bc.type = "bar"; bc.title = "Utilisation by card"; bc.height = 7; bc.width = 15; bc.legend = None
bc.add_data(Reference(sm, min_col=2, min_row=16, max_row=20), titles_from_data=True); bc.set_categories(Reference(sm, min_col=1, min_row=17, max_row=20)); bc.y_axis.scaling.min = 0; sm.add_chart(bc, "D3")
sm["A26"] = "Estimates use a simple monthly rate. Your statement shows the exact interest and minimum payment."; sm["A26"].font = Font(italic=True, color="777777")
howto(wb, C, ["1. Cards: for each card enter the limit, balance, APR, any 0% offer end date, the minimum payment rule (% of balance and fixed minimum) and the day of the month payment is due.",
              "2. Utilisation colours: green under 30%, yellow 30-50%, red over 50%. Next due date and days to pay update daily; 5 days or less turns red. 0% offers ending within 60 days turn orange.",
              "3. Payments: log each payment and the new balance.",
              "4. Summary: total limit and balance, overall utilisation, minimum payments, estimated interest, the next payment due, which card to pay off first (highest APR) and which 0% offer ends soonest.",
              "5. Update balances after each statement. Delete the sample cards first."])
wb.save(OUT / "Credit-Card-Tracker.xlsx")
print("built 5")
