"""Round 9 spreadsheet products into products/. Run: python3 make_batch4.py (reuses helpers from make_batch2.py)"""
import pathlib
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
today = dt.date.today(); y = today.year
HIDE0 = '#,##0.00;-#,##0.00;""'

def inputs(ws, rows, start=4, wa=44, wb_=14):
    for r, (n, v, f) in enumerate(rows, start):
        ws[f"A{r}"] = n; ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"] = v; ws[f"B{r}"].number_format = f; ws[f"B{r}"].fill = SOFT
    ws.column_dimensions["A"].width = wa; ws.column_dimensions["B"].width = wb_

# 1. Bill splitter for roommates, couples and trips
C = "1C7ED6"; title, header = kit(C); wb = Workbook(); pp = wb.active; pp.title = "People"
title(pp, "People", "Type up to 6 names. They appear everywhere else automatically.")
header(pp, ["Name"], [24], freeze=False)
for r, n in enumerate(["Alex", "Sam", "Jordan", "Riley"], 4): pp[f"A{r}"] = n
for r in range(4, 10): pp[f"A{r}"].fill = SOFT
ex = wb.create_sheet("Expenses", 0); title(ex, "Shared expenses", "Log who paid. Everyone shares each cost unless you type N under their name.")
cols = ["Date", "Description", "Category", "Amount", "Paid by"] + [f"P{i}" for i in range(1, 7)] + ["Share each"]
header(ex, cols, [12, 26, 14, 11, 14] + [9] * 6 + [11])
P = "FGHIJK"
for i, c in enumerate(P): ex[f"{c}3"] = f'=IF(People!A{4+i}="","",People!A{4+i})'
dv(ex, "=People!$A$4:$A$9", "E4:E500"); dv(ex, '"Groceries,Rent,Utilities,Internet,Eating out,Transport,Travel,Household,Other"', "C4:C500"); dv(ex, '"N"', "F4:K500")
sample = [(today.replace(day=1), "Rent", "Rent", 1800, "Alex", ""), (today.replace(day=2), "Big shop", "Groceries", 146.30, "Sam", ""), (today.replace(day=3), "Electricity", "Utilities", 92.40, "Jordan", ""),
          (today.replace(day=5), "Pizza night", "Eating out", 64, "Riley", "Jordan"), (today.replace(day=8), "Cleaning supplies", "Household", 23.75, "Sam", "")]
for r, (d, s, cat, a, by, skip) in enumerate(sample, 4):
    ex[f"A{r}"], ex[f"B{r}"], ex[f"C{r}"], ex[f"D{r}"], ex[f"E{r}"] = d, s, cat, a, by
    if skip: ex[f"{P[['Alex','Sam','Jordan','Riley'].index(skip)]}{r}"] = "N"
for r in range(4, 501):
    ex[f"A{r}"].number_format = "yyyy-mm-dd"; ex[f"D{r}"].number_format = M
    ex[f"L{r}"] = f'=IF(D{r}="",0,IFERROR(D{r}/(COUNTA(People!$A$4:$A$9)-COUNTIF(F{r}:K{r},"N")),0))'; ex[f"L{r}"].number_format = HIDE0
    for c in P: ex[f"{c}{r}"].alignment = Alignment(horizontal="center")
bl = wb.create_sheet("Balances", 0); title(bl, "Who owes whom", "Updates automatically. Positive = gets money back. Negative = owes money.")
header(bl, ["Person", "Paid", "Fair share", "Balance", "Status", "Settle up"], [18, 12, 12, 12, 20, 34], freeze=False)
for i in range(6):
    r = 4 + i; c = P[i]
    bl[f"A{r}"] = f'=IF(People!A{r}="","",People!A{r})'
    bl[f"B{r}"] = f'=IF(A{r}="","",SUMIF(Expenses!$E$4:$E$500,A{r},Expenses!$D$4:$D$500))'
    bl[f"C{r}"] = f'=IF(A{r}="","",SUMPRODUCT((Expenses!{c}$4:{c}$500<>"N")*Expenses!$L$4:$L$500))'
    bl[f"D{r}"] = f'=IF(A{r}="","",ROUND(B{r}-C{r},2))'
    bl[f"E{r}"] = f'=IF(A{r}="","",IF(D{r}>0,"Gets back "&TEXT(D{r},"#,##0.00"),IF(D{r}<0,"Owes "&TEXT(-D{r},"#,##0.00"),"All square")))'
    bl[f"F{r}"] = f'=IF(OR(A{r}="",D{r}=0),"",IF(D{r}<0,"Pay "&TEXT(-D{r},"#,##0.00")&" to "&$B$12,IF(A{r}=$B$12,"Collect, then pay out the others","Receive "&TEXT(D{r},"#,##0.00")&" from "&$B$12)))'
    for x in "BCD": bl[f"{x}{r}"].number_format = M
bl.conditional_formatting.add("D4:D9", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
bl.conditional_formatting.add("D4:D9", CellIsRule(operator="greaterThan", formula=["0"], font=Font(color="2B8A3E", bold=True)))
bl["A11"] = "Total spent"; bl["B11"] = "=SUM(Expenses!D4:D500)"; bl["B11"].number_format = M
bl["A12"] = "Banker (owed the most)"; bl["B12"] = '=IFERROR(INDEX(A4:A9,MATCH(MAX(D4:D9),D4:D9,0)),"")'
bold_label(bl, [11, 12])
bl["A14"] = "Settle up in the fewest steps: everyone who owes pays the banker, and the banker pays everyone else who is owed. Everyone ends up square."; bl["A14"].font = Font(italic=True, color="777777")
header(bl, ["Category", "Spent"], [18, 12], row=16, freeze=False)
for i, cat in enumerate(["Groceries", "Rent", "Utilities", "Internet", "Eating out", "Transport", "Travel", "Household", "Other"], 17):
    bl[f"A{i}"] = cat; bl[f"B{i}"] = f'=SUMIF(Expenses!$C$4:$C$500,A{i},Expenses!$D$4:$D$500)'; bl[f"B{i}"].number_format = M
ch = BarChart(); ch.title = "Spending by category"; ch.height = 7; ch.width = 16; ch.legend = None
ch.add_data(Reference(bl, min_col=2, min_row=16, max_row=25), titles_from_data=True); ch.set_categories(Reference(bl, min_col=1, min_row=17, max_row=25)); bl.add_chart(ch, "H3")
howto(wb, C, ["1. Type everyone's names on the People tab (up to 6).", "2. On Expenses, log each shared cost: what it was, how much, and who paid.",
              "3. Everyone splits every cost equally. If someone shouldn't pay for an item, type N in their column on that row (for example Jordan wasn't at pizza night).",
              "4. Balances shows what each person paid, their fair share and whether they owe or get money back, plus exactly who pays whom to settle up.",
              "5. Delete the sample rows before you start. Works for housemates, couples, holidays and group trips."])
wb.save(OUT / "Bill-Splitter-Shared-Expenses.xlsx")

# 2. FIRE / retirement calculator
C = "E8590C"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Calculator"
title(ws, "FIRE & Retirement Calculator", "Change the orange cells. Everything is in today's money (after inflation).")
inputs(ws, [("Current age", 30, "0"), ("Current savings & investments", 25000, M), ("Monthly contribution", 800, M), ("Yearly increase in contributions", 0.02, "0.0%"),
            ("Expected yearly return (before inflation)", 0.07, "0.0%"), ("Expected inflation", 0.025, "0.0%"), ("Yearly spending in retirement (today's money)", 36000, M), ("Safe withdrawal rate", 0.04, "0.0%")])
res = [("Real return (after inflation)", "=(1+B8)/(1+B9)-1", "0.00%"), ("Your FI number (savings needed)", "=B10/B11", M), ("Years until financial independence", '=IFERROR(MATCH(TRUE,INDEX(D17:D77>=B15,0),0)-1,"60+")', "0"),
       ("Age at financial independence", '=IF(ISNUMBER(B16),B4+B16,"")', "0")]
for r, (n, f, nf_) in enumerate(res, 14):
    ws[f"A{r}"] = n; ws[f"B{r}"] = f; ws[f"B{r}"].number_format = nf_; ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].font = Font(bold=True, color=C, size=13)
for r in range(4, 12): ws[f"B{r}"].fill = PatternFill("solid", fgColor="FFE8CC")
header(ws, ["Year", "Age", "Contributions this year", "Balance (today's money)", "FI number", "Progress"], [8, 8, 18, 20, 16, 11], row=19, freeze=False)
ws.row_dimensions[19].height = 30
# put table at rows 20..80 (year 0..60); D17:D77 used above is replaced below via correct refs
for n in range(61):
    r = 20 + n
    ws[f"A{r}"] = n; ws[f"B{r}"] = f"=$B$4+A{r}"
    ws[f"C{r}"] = f"=IF(A{r}=0,0,$B$6*12*(1+$B$7)^(A{r}-1))"
    ws[f"D{r}"] = "=$B$5" if n == 0 else f"=D{r-1}*(1+$B$14)+C{r}"
    ws[f"E{r}"] = "=$B$15"; ws[f"F{r}"] = f"=MIN(1,D{r}/E{r})"
    for c in "CDE": ws[f"{c}{r}"].number_format = M
    ws[f"F{r}"].number_format = "0%"
ws["B16"] = '=IFERROR(MATCH(TRUE,INDEX(D20:D80>=B15,0),0)-1,"60+")'
ws.conditional_formatting.add("A20:F80", FormulaRule(formula=["$D20>=$E20"], fill=PatternFill("solid", fgColor="E6F4EA")))
ws.conditional_formatting.add("F20:F80", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="F08C00"))
lc = LineChart(); lc.title = "Path to financial independence"; lc.height = 9; lc.width = 20; lc.y_axis.title = "Today's money"; lc.x_axis.title = "Age"
lc.add_data(Reference(ws, min_col=4, max_col=5, min_row=19, max_row=60), titles_from_data=True); lc.set_categories(Reference(ws, min_col=2, min_row=20, max_row=60)); ws.add_chart(lc, "H3")
sc = wb.create_sheet("Scenarios"); title(sc, "What if?", "How your monthly contribution changes the age you reach financial independence (same other inputs).")
header(sc, ["Monthly contribution", "Years to FI", "Age at FI"], [22, 14, 12], freeze=False)
for i, mult in enumerate([0.5, 0.75, 1, 1.25, 1.5, 2], 4):
    sc[f"A{i}"] = f"=Calculator!$B$6*{mult}"; sc[f"A{i}"].number_format = M
    # closed-form search: balance after n years with growing contributions, find first n where >= FI number (0..60)
    bal = (f"Calculator!$B$5*(1+Calculator!$B$14)^(ROW($1:$61)-1)"
           f"+A{i}*12*IF(ABS(Calculator!$B$14-Calculator!$B$7)<0.000001,(ROW($1:$61)-1)*(1+Calculator!$B$14)^(ROW($1:$61)-2),((1+Calculator!$B$14)^(ROW($1:$61)-1)-(1+Calculator!$B$7)^(ROW($1:$61)-1))/(Calculator!$B$14-Calculator!$B$7))")
    sc[f"B{i}"] = f'=IFERROR(MATCH(TRUE,INDEX(({bal})>=Calculator!$B$15,0),0)-1,"60+")'
    sc[f"C{i}"] = f'=IF(ISNUMBER(B{i}),Calculator!$B$4+B{i},"")'
howto(wb, C, ["1. Fill in the orange cells on Calculator: your age, what you've saved, what you add each month and your expected returns.", "2. Set how much you'd like to spend each year once you stop working, in today's money.",
              "3. Your FI number is that spending divided by the safe withdrawal rate (4% is a common rule of thumb). The table shows your balance each year after inflation and turns green once you reach it.",
              "4. Scenarios shows how saving more or less each month moves your financial-independence age.", "This is an educational planning tool, not financial advice. Real returns vary year to year."])
wb.save(OUT / "FIRE-Retirement-Calculator.xlsx")

# 3. Break-even & pricing calculator
C = "087F5B"; title, header = kit(C); wb = Workbook(); fx = wb.active; fx.title = "Fixed costs"
title(fx, "Monthly fixed costs", "Costs you pay every month whether you sell anything or not.")
header(fx, ["Cost", "Per month"], [32, 14])
for r, (n, v) in enumerate([("Rent / studio", 600), ("Software & subscriptions", 85), ("Website & hosting", 25), ("Insurance", 40), ("Phone & internet", 55), ("Your own salary (optional)", 0)], 4):
    fx[f"A{r}"] = n; fx[f"B{r}"] = v
for r in range(4, 31): fx[f"B{r}"].number_format = M
fx["A32"] = "TOTAL FIXED COSTS"; fx["B32"] = "=SUM(B4:B31)"; fx["B32"].number_format = M; fx["A32"].font = fx["B32"].font = Font(bold=True)
pr = wb.create_sheet("Products", 0); title(pr, "Break-even & pricing", "Enter each product's price, cost per unit and how many you expect to sell a month.")
header(pr, ["Product", "Price", "Cost per unit", "Profit per unit", "Margin", "Expected sales / month", "Contribution / month", "Price for target margin"], [24, 11, 12, 13, 9, 14, 15, 15])
pr["J3"] = "Target margin"; pr["K3"] = 0.4; pr["K3"].number_format = "0%"; pr["K3"].fill = SOFT; pr["J3"].font = Font(bold=True); pr.column_dimensions["J"].width = 26
for r, p in enumerate([("Candle", 24, 7.5, 60), ("Gift set", 45, 16, 20), ("Wax melts", 9, 2.2, 90)], 4):
    for c, v in enumerate(p, 1): pr.cell(r, c if c < 4 else 6, v)
for r in range(4, 54):
    pr[f"D{r}"] = f'=IF(A{r}="","",B{r}-C{r})'; pr[f"E{r}"] = f'=IF(OR(A{r}="",B{r}=0),"",D{r}/B{r})'
    pr[f"G{r}"] = f'=IF(A{r}="","",D{r}*F{r})'; pr[f"H{r}"] = f'=IF(A{r}="","",C{r}/(1-$K$3))'
    for c in "BCDGH": pr[f"{c}{r}"].number_format = M
    pr[f"E{r}"].number_format = "0%"
pr.conditional_formatting.add("D4:D53", CellIsRule(operator="lessThanOrEqual", formula=["0"], font=Font(color="C0392B", bold=True)))
sm = wb.create_sheet("Break-even", 1); title(sm, "Your break-even point", "Updates automatically from the other tabs.")
rows = [("Fixed costs per month", "='Fixed costs'!B32", M), ("Expected revenue per month", "=SUMPRODUCT(Products!B4:B53,Products!F4:F53)", M), ("Contribution per month", "=SUM(Products!G4:G53)", M),
        ("Expected profit per month", "=B6-B4", M), ("Average contribution margin", "=IFERROR(B6/B5,0)", "0.0%"), ("Break-even revenue per month", '=IFERROR(B4/B8,"")', M),
        ("Break-even as % of expected sales", '=IFERROR(B9/B5,"")', "0%"), ("Safety margin (how far sales can fall)", '=IFERROR(1-B10,"")', "0%")]
inputs(sm, rows, wa=40, wb_=16)
sm.conditional_formatting.add("B7", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
header(sm, ["Product", "Units to break even alone"], [40, 16], row=14, freeze=False)
for i in range(10):
    r = 15 + i; sm[f"A{r}"] = f'=IF(Products!A{4+i}="","",Products!A{4+i})'; sm[f"B{r}"] = f'=IF(OR(A{r}="",N(Products!D{4+i})<=0),"",ROUNDUP($B$4/Products!D{4+i},0))'
header(sm, ["Price change", "Profit per month"], [40, 16], row=27, freeze=False)
sm["C27"] = "(assumes the same number of sales)"; sm["C27"].font = Font(italic=True, color="777777")
for i, ch_ in enumerate([-0.2, -0.1, 0, 0.1, 0.2], 28):
    sm[f"A{i}"] = ch_; sm[f"A{i}"].number_format = "+0%;-0%;0%"
    sm[f"B{i}"] = f"=SUMPRODUCT(Products!B4:B53*(1+A{i})-Products!C4:C53,Products!F4:F53)-B4"; sm[f"B{i}"].number_format = M
bc = BarChart(); bc.title = "Profit at different prices"; bc.height = 7; bc.width = 14; bc.legend = None
bc.add_data(Reference(sm, min_col=2, min_row=27, max_row=32), titles_from_data=True); bc.set_categories(Reference(sm, min_col=1, min_row=28, max_row=32)); sm.add_chart(bc, "D3")
howto(wb, C, ["1. List your monthly fixed costs on Fixed costs (rent, software, insurance, even a salary for yourself).", "2. On Products, enter each product's price, what one unit costs you to make and ship, and how many you expect to sell a month.",
              "3. Break-even shows the revenue you need to cover your costs, how far sales could drop before you make a loss, and units needed per product.", "4. Use the price change table and 'Price for target margin' to test pricing. Delete the sample products first."])
wb.save(OUT / "Break-Even-Pricing-Calculator.xlsx")

# 4. 12-month cash flow forecast
C = "364FC7"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Cash flow"
title(ws, "12-Month Cash Flow Forecast", "Forecast money in and out each month so you never get caught short.")
ws["A3"] = "Opening bank balance"; ws["B3"] = 4000; ws["D3"] = "First month"; ws["E3"] = dt.date(y, today.month, 1)
for c in ("B3", "E3"): ws[c].fill = SOFT
ws["B3"].number_format = M; ws["E3"].number_format = "mmm yyyy"; ws["A3"].font = ws["D3"].font = Font(bold=True)
hdr = ["", "Total"] + [""] * 12
hf = PatternFill("solid", fgColor=C)
ws.cell(5, 1, "MONEY IN").font = Font(bold=True, color="FFFFFF"); ws.cell(5, 1).fill = hf
for m in range(12):
    x = ws.cell(5, 2 + m, f"=EDATE($E$3,{m})"); x.number_format = "mmm yy"; x.font = Font(bold=True, color="FFFFFF"); x.fill = hf; x.alignment = Alignment(horizontal="center")
    ws.column_dimensions[L(2 + m)].width = 11
x = ws.cell(5, 14, "Year"); x.font = Font(bold=True, color="FFFFFF"); x.fill = hf
ws.column_dimensions["A"].width = 30; ws.column_dimensions["N"].width = 13
cin = ["Sales / client payments", "Other income", "Loans / investment", "Tax refunds"]
cout = ["Rent", "Salaries / drawings", "Materials & stock", "Software", "Marketing", "Insurance", "Loan repayments", "Tax", "Other"]
samp_in = [5200, 300, 0, 0]; samp_out = [900, 2500, 800, 120, 250, 60, 0, 0, 150]
r = 6
for i, n in enumerate(cin):
    ws.cell(r, 1, n)
    for m in range(3): ws.cell(r, 2 + m, round(samp_in[i] * (1 + 0.05 * m))) if samp_in[i] else None
    r += 1
ti = r; ws.cell(ti, 1, "Total money in").font = Font(bold=True)
r = ti + 2; ws.cell(r - 1, 1, "MONEY OUT").font = Font(bold=True, color="FFFFFF"); ws.cell(r - 1, 1).fill = hf
o0 = r
for i, n in enumerate(cout):
    ws.cell(r, 1, n)
    for m in range(3): ws.cell(r, 2 + m, samp_out[i]) if samp_out[i] else None
    r += 1
to = r; ws.cell(to, 1, "Total money out").font = Font(bold=True)
nr, ob, cb = to + 2, to + 3, to + 4
ws.cell(nr, 1, "Net cash flow").font = Font(bold=True); ws.cell(ob, 1, "Opening balance"); ws.cell(cb, 1, "Closing balance").font = Font(bold=True, size=12)
for m in range(12):
    c = L(2 + m)
    ws[f"{c}{ti}"] = f"=SUM({c}6:{c}{ti-1})"; ws[f"{c}{to}"] = f"=SUM({c}{o0}:{c}{to-1})"; ws[f"{c}{nr}"] = f"={c}{ti}-{c}{to}"
    ws[f"{c}{ob}"] = "=$B$3" if m == 0 else f"={L(1+m)}{cb}"; ws[f"{c}{cb}"] = f"={c}{ob}+{c}{nr}"
    for rr in list(range(6, cb + 1)): ws[f"{c}{rr}"].number_format = M
    for rr in (ti, to, cb): ws[f"{c}{rr}"].font = Font(bold=True)
    ws[f"{c}{cb}"].fill = SOFT
for rr in list(range(6, ti + 1)) + list(range(o0, to + 1)) + [nr]:
    ws[f"N{rr}"] = f"=SUM(B{rr}:M{rr})"; ws[f"N{rr}"].number_format = M; ws[f"N{rr}"].font = Font(bold=True)
ws.conditional_formatting.add(f"B{nr}:M{cb}", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True), fill=PatternFill("solid", fgColor="FFE3E3")))
ws.cell(cb + 2, 1, "Lowest closing balance").font = Font(bold=True); ws.cell(cb + 2, 2, f"=MIN(B{cb}:M{cb})").number_format = M
ws.cell(cb + 3, 1, "Months with a negative balance").font = Font(bold=True); ws.cell(cb + 3, 2, f'=COUNTIF(B{cb}:M{cb},"<0")')
ws.freeze_panes = "B6"
lc = LineChart(); lc.title = "Closing bank balance"; lc.height = 7; lc.width = 22; lc.legend = None
lc.add_data(Reference(ws, min_col=1, max_col=13, min_row=cb), from_rows=True, titles_from_data=True); lc.set_categories(Reference(ws, min_col=2, max_col=13, min_row=5)); ws.add_chart(lc, f"A{cb+6}")
howto(wb, C, ["1. Type your opening bank balance and the first month you want to forecast at the top.", "2. Rename the money in and money out rows to match your business, then enter what you expect each month.",
              "3. Net cash flow and closing balance work out automatically. Any month where you'd go below zero turns red, so you can plan ahead (chase invoices, delay a purchase, arrange credit).",
              "4. Update the forecast with real numbers each month. Delete the sample numbers before you start."])
wb.save(OUT / "Cash-Flow-Forecast-12-Months.xlsx")

# 5. Paycheck budget
C = "9C36B5"; title, header = kit(C); wb = Workbook(); bl = wb.active; bl.title = "Bills"
title(bl, "Bills & regular costs", "List every bill and choose which paycheck pays it.")
header(bl, ["Bill", "Amount", "Due day", "Paid from paycheck", "Paid this month?"], [26, 12, 10, 18, 16])
bills = [("Rent", 1100, 1, 1), ("Car payment", 260, 5, 1), ("Phone", 35, 10, 1), ("Internet", 45, 14, 2), ("Electricity", 80, 18, 2), ("Insurance", 95, 20, 2), ("Streaming", 18, 22, 2), ("Credit card", 150, 25, 2)]
for r, b in enumerate(bills, 4):
    for c, v in enumerate(b, 1): bl.cell(r, c, v)
dv(bl, '"1,2,3,4"', "D4:D100"); dv(bl, '"Yes,No"', "E4:E100")
for r in range(4, 101): bl[f"B{r}"].number_format = M
bl.conditional_formatting.add("A4:E100", FormulaRule(formula=['$E4="Yes"'], font=Font(strike=True, color="999999")))
pc = wb.create_sheet("Paycheck plan", 0); title(pc, "Paycheck budget", "Give every paycheck a job before you spend it.")
header(pc, ["", "Paycheck 1", "Paycheck 2", "Paycheck 3", "Paycheck 4", "Month"], [30, 14, 14, 14, 14, 14], freeze=False)
lab = ["Pay date", "Take-home pay", "Bills (from Bills tab)", "Savings", "Groceries", "Fuel & transport", "Debt extra payment", "Fun money", "Other", "Left to assign"]
for r, n in enumerate(lab, 4): pc[f"A{r}"] = n; pc[f"A{r}"].font = Font(bold=True)
samp = {4: [today.replace(day=1), today.replace(day=15)], 5: [1650, 1650], 7: [100, 300], 8: [125, 375], 9: [30, 90], 10: [0, 297], 11: [0, 200]}
for i, c in enumerate("BCDE"):
    pc[f"{c}4"].number_format = "dd mmm"
    for rr, vals in samp.items():
        if i < len(vals): pc[f"{c}{rr}"] = vals[i]
    pc[f"{c}6"] = f'=SUMIF(Bills!$D$4:$D$100,{i+1},Bills!$B$4:$B$100)'
    pc[f"{c}13"] = f'=IF(AND({c}5="",{c}6=0),"",N({c}5)-SUM({c}6:{c}12))'
    for rr in range(5, 14): pc[f"{c}{rr}"].number_format = M
    for rr in (4, 5, 7, 8, 9, 10, 11, 12): pc[f"{c}{rr}"].fill = SOFT
for rr in range(5, 14): pc[f"F{rr}"] = f"=SUM(B{rr}:E{rr})"; pc[f"F{rr}"].number_format = M; pc[f"F{rr}"].font = Font(bold=True)
pc.conditional_formatting.add("B13:F13", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True), fill=PatternFill("solid", fgColor="FFE3E3")))
pc.conditional_formatting.add("B13:F13", CellIsRule(operator="equal", formula=["0"], font=Font(color="2B8A3E", bold=True)))
pc["A15"] = "Goal: 'Left to assign' should be 0 for every paycheck (every dollar has a job). Red means you've planned more than you earn."; pc["A15"].font = Font(italic=True, color="777777")
pc["A17"] = "Month summary"; pc["A17"].font = Font(bold=True, size=13, color=C)
summ = [("Total take-home", "=F5"), ("Total bills", "=F6"), ("Total saved", "=F7"), ("Savings rate", '=IFERROR(F7/F5,"")'), ("Bills still unpaid this month", '=SUMIF(Bills!E4:E100,"<>Yes",Bills!B4:B100)')]
for r, (n, f) in enumerate(summ, 18):
    pc[f"A{r}"] = n; pc[f"B{r}"] = f; pc[f"B{r}"].number_format = "0%" if "rate" in n else M
bc = BarChart(); bc.type = "col"; bc.grouping = "stacked"; bc.overlap = 100; bc.title = "Where each paycheck goes"; bc.height = 8; bc.width = 16
bc.add_data(Reference(pc, min_col=1, max_col=5, min_row=6, max_row=12), from_rows=True, titles_from_data=True); bc.set_categories(Reference(pc, min_col=2, max_col=5, min_row=3)); pc.add_chart(bc, "H3")
howto(wb, C, ["1. On Bills, list every regular bill with its amount and due day, then choose which paycheck will pay it (1 to 4).",
              "2. On Paycheck plan, enter each pay date and take-home amount. Paid weekly? Use all 4 columns. Every two weeks or twice a month? Use 2 (or 3 in a three-paycheck month). Monthly? Use 1.",
              "3. Bills fill in automatically. Plan savings, groceries, fuel and fun money until 'Left to assign' is 0.", "4. Tick bills as paid each month and reset to No at the start of the next. Delete the sample numbers first."])
wb.save(OUT / "Paycheck-Budget-Planner.xlsx")
print("built 5")
