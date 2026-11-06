"""Round 8 spreadsheet products into products/. Run: python3 make_batch4.py (reuses helpers from make_batch2.py)"""
import pathlib
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
today = dt.date.today(); y = today.year

def kv(ws, rows, start=4, w=(34, 14)):
    for r, (a, v, f) in enumerate(rows, start):
        ws[f"A{r}"] = a; ws[f"B{r}"] = v; ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
        if f: ws[f"B{r}"].number_format = f
    ws.column_dimensions["A"].width = w[0]; ws.column_dimensions["B"].width = w[1]

# 1. Holiday gift & Christmas budget
C = "B02A37"; title, header = kit(C); wb = Workbook(); sm = wb.active; sm.title = "Summary"
title(sm, "Holiday Budget", "Your whole holiday season on one page. Updates automatically.")
kv(sm, [("Total holiday budget", 1200, M), ("Spent on gifts", "=SUM(Gifts!F4:F300)", M), ("Spent on other costs", "=SUM('Other costs'!C4:C100)", M),
        ("Total spent", "=B5+B6", M), ("Left to spend", "=B4-B7", M), ("Gifts bought", '=COUNTIF(Gifts!G4:G300,"Yes")&" of "&COUNTA(Gifts!A4:A300)', None),
        ("Gifts wrapped", '=COUNTIF(Gifts!H4:H300,"Yes")&" of "&COUNTA(Gifts!A4:A300)', None)])
sm.conditional_formatting.add("B8", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
header(sm, ["Group", "Gift budget", "Spent", "Left"], [34, 14, 14, 14], row=13, freeze=False)
groups = ["Family", "Partner", "Kids", "Friends", "Work", "Teachers", "Neighbours", "Other"]
for i, g in enumerate(groups, 14):
    sm[f"A{i}"] = g; sm[f"B{i}"] = f"=SUMIF(Gifts!$B$4:$B$300,A{i},Gifts!$E$4:$E$300)"; sm[f"C{i}"] = f"=SUMIF(Gifts!$B$4:$B$300,A{i},Gifts!$F$4:$F$300)"; sm[f"D{i}"] = f"=B{i}-C{i}"
    for c in "BCD": sm[f"{c}{i}"].number_format = M
sm.conditional_formatting.add("D14:D21", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
ch = BarChart(); ch.title = "Spent by group"; ch.height = 7; ch.width = 14; ch.add_data(Reference(sm, min_col=3, min_row=13, max_row=21), titles_from_data=True)
ch.set_categories(Reference(sm, min_col=1, min_row=14, max_row=21)); sm.add_chart(ch, "F4")
gf = wb.create_sheet("Gifts"); title(gf, "Gift list", "One row per gift. Mark Bought and Wrapped as you go.")
header(gf, ["Person", "Group", "Gift idea", "Where to buy", "Budget", "Actual", "Bought?", "Wrapped?", "Notes"], [18, 12, 26, 18, 11, 11, 10, 10, 24])
dv(gf, "=Summary!$A$14:$A$21", "B4:B300"); dv(gf, '"Yes,No"', "G4:H300")
for r, g in enumerate([("Mum", "Family", "Cashmere scarf", "Online", 60, 55, "Yes", "No"), ("Dad", "Family", "Coffee grinder", "Store", 50, None, "No", "No"),
                       ("Sam", "Partner", "Weekend away", "Booking site", 250, 240, "Yes", "Yes"), ("Lily", "Kids", "Lego set", "Toy shop", 45, 42, "Yes", "No"), ("Jo", "Friends", "Candle set", "Etsy", 25, None, "No", "No")], 4):
    for c, x in enumerate(g, 1): gf.cell(r, c, x)
for r in range(4, 301): gf[f"E{r}"].number_format = gf[f"F{r}"].number_format = M
gf.conditional_formatting.add("F4:F300", FormulaRule(formula=['AND(ISNUMBER(F4),F4>E4)'], font=Font(color="C0392B", bold=True)))
gf.conditional_formatting.add("A4:I300", FormulaRule(formula=['AND($G4="Yes",$H4="Yes")'], fill=PatternFill("solid", fgColor="E6F4EA")))
oc = wb.create_sheet("Other costs"); title(oc, "Other holiday costs", "Food, decorations, travel, cards, parties.")
header(oc, ["Item", "Category", "Cost", "Paid?"], [30, 16, 12, 9])
dv(oc, '"Food & drink,Decorations,Travel,Cards & postage,Wrapping,Parties,Charity,Other"', "B4:B100"); dv(oc, '"Yes,No"', "D4:D100")
for r, o in enumerate([("Christmas dinner", "Food & drink", 140, "No"), ("Tree & lights", "Decorations", 85, "Yes"), ("Cards & stamps", "Cards & postage", 30, "Yes")], 4):
    for c, x in enumerate(o, 1): oc.cell(r, c, x)
for r in range(4, 101): oc[f"C{r}"].number_format = M
cd = wb.create_sheet("Card list"); title(cd, "Card list", "Who gets a card and whether it's sent.")
header(cd, ["Name", "Address", "Sent?", "Received from them?"], [22, 46, 9, 18]); dv(cd, '"Yes,No"', "C4:D300")
howto(wb, C, ["1. Set your total holiday budget on the Summary tab.", "2. Add every gift on the Gifts tab with a budget. Enter the actual price when you buy it. Over-budget prices turn red, and rows turn green once bought and wrapped.",
              "3. Add food, decorations and travel on Other costs.", "4. The Summary shows what's left, progress on buying and wrapping, and spending by group. Rename the groups to suit you.", "5. Delete the sample rows before you start."])
wb.save(OUT / "Holiday-Gift-Budget-Planner.xlsx")

# 2. Mileage log
C = "1C7ED6"; title, header = kit(C); wb = Workbook(); st = wb.active; st.title = "Settings"
title(st, "Mileage settings", "Set your rate per mile or km. Check your tax authority's current rate.")
kv(st, [("Unit", "miles", None), ("Rate per unit", 0.70, "0.000"), ("Vehicle", "My car", None), ("Tax year", y, "0")])
dv(st, '"miles,km"', "B4")
tr = wb.create_sheet("Trips", 0); title(tr, "Mileage log", "Log each trip. Distance comes from the odometer, or type it in directly.")
header(tr, ["Date", "From", "To", "Purpose", "Client / project", "Start odometer", "End odometer", "Distance", "Business?", "Deduction", "Month"], [12, 16, 16, 24, 18, 13, 13, 10, 10, 12, 8])
dv(tr, '"Yes,No"', "I4:I2000")
trips = [(dt.date(y, 1, 6), "Home", "Client office", "Kick-off meeting", "Acme Ltd", 12040, 12068, "Yes"), (dt.date(y, 1, 9), "Home", "Print shop", "Collect samples", "Acme Ltd", 12068, 12079, "Yes"),
         (dt.date(y, 1, 14), "Home", "Supermarket", "Personal", "", 12079, 12087, "No"), (dt.date(y, 2, 3), "Home", "Coworking", "Workshop", "Beta Co", 12210, 12241, "Yes")]
for r, t in enumerate(trips, 4):
    for c, x in zip("ABCDEFGI", t): tr[f"{c}{r}"] = x
for r in range(4, 2001):
    tr[f"A{r}"].number_format = "yyyy-mm-dd"
    tr[f"H{r}"] = f'=IF(AND(ISNUMBER(F{r}),ISNUMBER(G{r})),G{r}-F{r},"")'
    tr[f"J{r}"] = f'=IF(AND(I{r}="Yes",ISNUMBER(H{r})),H{r}*Settings!$B$5,"")'; tr[f"J{r}"].number_format = M
    tr[f"K{r}"] = f'=IF(A{r}="","",MONTH(A{r}))'
tr.conditional_formatting.add("H4:H2000", FormulaRule(formula=['AND(ISNUMBER(H4),H4<0)'], fill=PatternFill("solid", fgColor="FFE3E3")))
sm = wb.create_sheet("Summary", 0); title(sm, "Mileage summary", "Business distance and deduction by month.")
header(sm, ["Month", "Business distance", "Personal distance", "Deduction"], [12, 18, 18, 14], row=4, freeze=False)
for m in range(1, 13):
    r = 4 + m; sm[f"A{r}"] = MONTHS[m - 1]
    sm[f"B{r}"] = f'=SUMIFS(Trips!$H$4:$H$2000,Trips!$K$4:$K$2000,{m},Trips!$I$4:$I$2000,"Yes")'
    sm[f"C{r}"] = f'=SUMIFS(Trips!$H$4:$H$2000,Trips!$K$4:$K$2000,{m},Trips!$I$4:$I$2000,"No")'
    sm[f"D{r}"] = f"=SUMIF(Trips!$K$4:$K$2000,{m},Trips!$J$4:$J$2000)"; sm[f"D{r}"].number_format = M
sm["A17"] = "Year"; sm["A17"].font = Font(bold=True)
for c in "BCD": sm[f"{c}17"] = f"=SUM({c}5:{c}16)"; sm[f"{c}17"].font = Font(bold=True)
sm["D17"].number_format = M; sm["A19"] = "Business share"; sm["B19"] = '=IF(B17+C17=0,"",B17/(B17+C17))'; sm["B19"].number_format = "0%"; sm["A19"].font = Font(bold=True)
ch = BarChart(); ch.title = "Business distance by month"; ch.height = 7; ch.width = 16; ch.add_data(Reference(sm, min_col=2, min_row=4, max_row=16), titles_from_data=True)
ch.set_categories(Reference(sm, min_col=1, min_row=5, max_row=16)); sm.add_chart(ch, "F4")
howto(wb, C, ["1. On Settings, choose miles or km and enter the rate per unit you can claim (check your tax authority's current rate).", "2. Log each trip on Trips with start and end odometer readings. Mark it Business or not.",
              "3. Distance and deduction are calculated for you. The Summary totals business distance and deduction per month and for the year.", "4. Keep the file as your mileage record for your tax return. Delete the sample trips first."])
wb.save(OUT / "Mileage-Log.xlsx")

# 3. Loan & mortgage calculator
C = "343A40"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Calculator"
title(ws, "Loan & Mortgage Calculator", "Change the yellow cells. Everything else updates, including the full schedule.")
inp = [("Loan amount", 250000, M), ("Annual interest rate", 0.045, "0.00%"), ("Term (years)", 25, "0"), ("Payments per year", 12, "0"), ("First payment date", dt.date(y + 1, 1, 1), "yyyy-mm-dd"), ("Extra payment each period", 100, M)]
kv(ws, inp, w=(36, 16))
for r in range(4, 10): ws[f"B{r}"].fill = PatternFill("solid", fgColor="FFF3BF")
dv(ws, '"12,26,52,4,1"', "B7")
out = [("Regular payment", "=-PMT(B5/B7,B6*B7,B4)", M), ("Number of payments (no extra)", "=B6*B7", "0"), ("Total interest (no extra)", "=B11*B12-B4", M),
       ("Payments needed with extra", "=COUNTIF(Schedule!C4:C2603,\">0.005\")", "0"), ("Total interest with extra", "=SUM(Schedule!E4:E2603)", M),
       ("Interest saved", "=B13-B15", M), ("Time saved (years)", "=(B12-B14)/B7", "0.0"), ("Payoff date with extra", "=IFERROR(INDEX(Schedule!B4:B2603,B14),\"\")", "yyyy-mm-dd")]
for r, (a, f, nf_) in enumerate(out, 11):
    ws[f"A{r}"] = a; ws[f"B{r}"] = f; ws[f"B{r}"].number_format = nf_; ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
ws["B16"].font = Font(bold=True, color="2B8A3E")
sc = wb.create_sheet("Schedule"); title(sc, "Amortisation schedule", "One row per payment. Rows after payoff show zero.")
header(sc, ["#", "Date", "Opening balance", "Payment", "Interest", "Principal", "Extra", "Closing balance"], [7, 12, 16, 13, 13, 13, 11, 16])
for i in range(1, 2601):
    r = 3 + i; prev = "Calculator!$B$4" if i == 1 else f"H{r-1}"
    sc[f"A{r}"] = i
    sc[f"B{r}"] = f"=IF(Calculator!$B$7=12,EDATE(Calculator!$B$8,A{r}-1),Calculator!$B$8+ROUND((A{r}-1)*365/Calculator!$B$7,0))"
    sc[f"C{r}"] = f"=MAX(0,{prev})"
    sc[f"E{r}"] = f"=C{r}*Calculator!$B$5/Calculator!$B$7"
    sc[f"D{r}"] = f"=IF(C{r}<=0,0,MIN(Calculator!$B$11,C{r}+E{r}))"
    sc[f"F{r}"] = f"=D{r}-E{r}"
    sc[f"G{r}"] = f"=IF(C{r}<=0,0,MIN(Calculator!$B$9,C{r}-F{r}))"
    sc[f"H{r}"] = f"=MAX(0,C{r}-F{r}-G{r})"
    sc[f"B{r}"].number_format = "yyyy-mm-dd"
    for c in "CDEFGH": sc[f"{c}{r}"].number_format = M
ch = LineChart(); ch.title = "Balance over time"; ch.height = 8; ch.width = 18; ch.add_data(Reference(sc, min_col=8, min_row=3, max_row=3 + 600), titles_from_data=True); ch.legend = None
ws.add_chart(ch, "D4")
howto(wb, C, ["1. Enter the loan amount, interest rate, term and how often you pay (12 = monthly, 26 = fortnightly, 52 = weekly).", "2. Add any extra payment you plan to make each period, or 0 for none.",
              "3. The Calculator shows your regular payment, total interest, and how much interest and time the extra payment saves.", "4. The Schedule tab lists every payment with interest, principal and balance. Works for mortgages, car loans and personal loans.",
              "Results are estimates for planning. Your lender's figures may differ slightly because of rounding and fees."])
wb.save(OUT / "Loan-Mortgage-Calculator.xlsx")

# 4. Freelance timesheet & billable hours
C = "0CA678"; title, header = kit(C); wb = Workbook(); cl = wb.active; cl.title = "Clients"
title(cl, "Clients & rates", "List each client with your hourly rate for them.")
header(cl, ["Client", "Hourly rate", "Contact", "Notes"], [24, 12, 26, 30])
for r, c in enumerate([("Acme Ltd", 85, "ana@acme.example", ""), ("Beta Co", 70, "", "Net 30"), ("Studio Nine", 95, "", "")], 4):
    for i, x in enumerate(c, 1): cl.cell(r, i, x)
for r in range(4, 104): cl[f"B{r}"].number_format = M
ts = wb.create_sheet("Timesheet", 0); title(ts, "Timesheet", "Log time per task. Hours, rate and amount fill in for you.")
header(ts, ["Date", "Client", "Project", "Task", "Start", "End", "Break (min)", "Hours", "Billable?", "Rate", "Amount", "Invoiced?", "Month"], [12, 16, 18, 26, 8, 8, 10, 8, 10, 9, 11, 10, 8])
dv(ts, "=Clients!$A$4:$A$103", "B4:B3000"); dv(ts, '"Yes,No"', "I4:I3000"); dv(ts, '"Yes,No"', "L4:L3000")
rows = [(dt.date(y, 1, 5), "Acme Ltd", "Website", "Wireframes", dt.time(9), dt.time(12, 30), 15, "Yes", "Yes"), (dt.date(y, 1, 5), "Beta Co", "Logo", "Concepts", dt.time(13, 30), dt.time(16), 0, "Yes", "No"),
        (dt.date(y, 1, 6), "Acme Ltd", "Website", "Client call", dt.time(10), dt.time(10, 45), 0, "Yes", "Yes"), (dt.date(y, 1, 6), "Studio Nine", "Admin", "Quote prep", dt.time(14), dt.time(15), 0, "No", "No")]
for r, t in enumerate(rows, 4):
    for c, x in zip("ABCDEFGIL", t): ts[f"{c}{r}"] = x
for r in range(4, 3001):
    ts[f"A{r}"].number_format = "ddd d mmm"; ts[f"E{r}"].number_format = ts[f"F{r}"].number_format = "hh:mm"
    ts[f"H{r}"] = f'=IF(OR(E{r}="",F{r}=""),"",ROUND((MOD(F{r}-E{r},1)*24)-N(G{r})/60,2))'
    ts[f"J{r}"] = f'=IF(B{r}="","",IFERROR(INDEX(Clients!$B$4:$B$103,MATCH(B{r},Clients!$A$4:$A$103,0)),0))'
    ts[f"K{r}"] = f'=IF(OR(H{r}="",I{r}<>"Yes"),"",H{r}*J{r})'; ts[f"J{r}"].number_format = ts[f"K{r}"].number_format = M
    ts[f"M{r}"] = f'=IF(A{r}="","",MONTH(A{r}))'
ts.conditional_formatting.add("A4:M3000", FormulaRule(formula=['AND($I4="Yes",$L4<>"Yes",$A4<>"")'], fill=PatternFill("solid", fgColor="FFF3BF")))
sm = wb.create_sheet("Summary", 0); title(sm, "Hours & earnings", "Yellow rows on the Timesheet are billable but not invoiced yet.")
kv(sm, [("Total hours", "=SUM(Timesheet!H4:H3000)", "0.00"), ("Billable hours", '=SUMIF(Timesheet!I4:I3000,"Yes",Timesheet!H4:H3000)', "0.00"),
        ("Billable share", "=IF(B4=0,\"\",B5/B4)", "0%"), ("Billable amount", "=SUM(Timesheet!K4:K3000)", M), ("Not invoiced yet", '=SUMIF(Timesheet!L4:L3000,"<>Yes",Timesheet!K4:K3000)', M),
        ("Effective hourly rate (all hours)", "=IF(B4=0,\"\",B7/B4)", M)], w=(34, 14))
header(sm, ["Client", "Hours", "Billable amount", "Not invoiced"], [34, 14, 16, 14], row=12, freeze=False)
for i in range(13, 23):
    sm[f"A{i}"] = f'=IF(Clients!A{i-9}="","",Clients!A{i-9})'
    sm[f"B{i}"] = f'=IF(A{i}="","",SUMIF(Timesheet!$B$4:$B$3000,A{i},Timesheet!$H$4:$H$3000))'
    sm[f"C{i}"] = f'=IF(A{i}="","",SUMIF(Timesheet!$B$4:$B$3000,A{i},Timesheet!$K$4:$K$3000))'
    sm[f"D{i}"] = f'=IF(A{i}="","",SUMIFS(Timesheet!$K$4:$K$3000,Timesheet!$B$4:$B$3000,A{i},Timesheet!$L$4:$L$3000,"<>Yes"))'
    sm[f"C{i}"].number_format = sm[f"D{i}"].number_format = M
header(sm, ["Month", "Hours", "Billable amount"], [34, 14, 16], row=25, freeze=False)
for m in range(1, 13):
    r = 25 + m; sm[f"A{r}"] = MONTHS[m - 1]; sm[f"B{r}"] = f"=SUMIF(Timesheet!$M$4:$M$3000,{m},Timesheet!$H$4:$H$3000)"; sm[f"C{r}"] = f"=SUMIF(Timesheet!$M$4:$M$3000,{m},Timesheet!$K$4:$K$3000)"; sm[f"C{r}"].number_format = M
howto(wb, C, ["1. Add your clients and hourly rates on the Clients tab.", "2. Log each block of work on the Timesheet: date, client, task, start and end time and any break. Hours, rate and amount are calculated.",
              "3. Mark work as Billable or not, and set Invoiced to Yes once you've billed it. Billable rows not yet invoiced are highlighted yellow.", "4. The Summary shows hours, earnings, unbilled work per client and per month, and your effective hourly rate.", "5. Delete the sample rows before you start."])
wb.save(OUT / "Freelance-Timesheet-Billable-Hours.xlsx")

# 5. Car maintenance & fuel log
C = "E8590C"; title, header = kit(C); wb = Workbook(); fu = wb.active; fu.title = "Fuel"
title(fu, "Fuel log", "Fill up to full each time and log it to get accurate consumption.")
header(fu, ["Date", "Odometer", "Litres", "Total cost", "Price / litre", "Distance since last", "L/100 km", "MPG (UK)", "MPG (US)", "Month"], [12, 12, 9, 11, 11, 15, 10, 10, 10, 8])
fills = [(dt.date(y, 1, 3), 45210, 42.5, 72.25), (dt.date(y, 1, 17), 45790, 40.1, 69.37), (dt.date(y, 2, 1), 46355, 39.2, 66.64), (dt.date(y, 2, 18), 46950, 41.8, 72.31)]
for r, f in enumerate(fills, 4):
    for c, x in zip("ABCD", f): fu[f"{c}{r}"] = x
for r in range(4, 1001):
    fu[f"A{r}"].number_format = "yyyy-mm-dd"; fu[f"D{r}"].number_format = M
    fu[f"E{r}"] = f'=IF(OR(C{r}="",C{r}=0),"",D{r}/C{r})'; fu[f"E{r}"].number_format = "0.000"
    fu[f"F{r}"] = "" if r == 4 else f'=IF(OR(B{r}="",B{r-1}=""),"",B{r}-B{r-1})'
    fu[f"G{r}"] = f'=IF(OR(F{r}="",N(F{r})=0),"",C{r}/F{r}*100)'; fu[f"H{r}"] = f'=IF(G{r}="","",282.481/G{r})'; fu[f"I{r}"] = f'=IF(G{r}="","",235.215/G{r})'
    for c in "GHI": fu[f"{c}{r}"].number_format = "0.0"
    fu[f"J{r}"] = f'=IF(A{r}="","",MONTH(A{r}))'
sv = wb.create_sheet("Service"); title(sv, "Service & repairs", "Every service, repair, tyre and MOT/inspection, with when it's next due.")
header(sv, ["Date", "Odometer", "Type", "Description", "Garage", "Cost", "Next due (km)", "Next due (date)", "Km to go", "Days to go"], [12, 11, 14, 28, 16, 11, 13, 14, 10, 10])
dv(sv, '"Service,Oil change,Tyres,Brakes,Inspection / MOT,Repair,Battery,Insurance,Tax,Other"', "C4:C500")
for r, s in enumerate([(dt.date(y, 1, 10), 45500, "Service", "Annual service", "Main St Garage", 289, 60500, dt.date(y + 1, 1, 10)), (dt.date(y, 2, 5), 46400, "Tyres", "2 front tyres", "TyreFit", 180, None, None),
                       (dt.date(y, 3, 1), 47100, "Inspection / MOT", "Annual inspection", "Main St Garage", 55, None, dt.date(y + 1, 3, 1))], 4):
    for c, x in zip("ABCDEFGH", s): sv[f"{c}{r}"] = x
for r in range(4, 501):
    sv[f"A{r}"].number_format = sv[f"H{r}"].number_format = "yyyy-mm-dd"; sv[f"F{r}"].number_format = M
    sv[f"I{r}"] = f'=IF(G{r}="","",G{r}-MAX(Fuel!$B$4:$B$1000,$B$4:$B$500))'; sv[f"J{r}"] = f'=IF(H{r}="","",H{r}-TODAY())'
sv.conditional_formatting.add("I4:J500", FormulaRule(formula=['AND(ISNUMBER(I4),I4<=30)'], fill=PatternFill("solid", fgColor="FFE3E3"), font=Font(bold=True, color="C0392B")))
sm = wb.create_sheet("Summary", 0); title(sm, "Car costs", "Running costs at a glance.")
kv(sm, [("Vehicle", "Make, model, reg", None), ("Distance logged (km)", "=IFERROR(MAX(Fuel!B4:B1000)-MIN(Fuel!B4:B1000),0)", "#,##0"), ("Fuel cost", "=SUM(Fuel!D4:D1000)", M),
        ("Service & repair cost", "=SUM(Service!F4:F500)", M), ("Total cost", "=B6+B7", M), ("Cost per km", "=IF(B5=0,\"\",B8/B5)", "0.000"), ("Average L/100 km", "=IFERROR(SUM(Fuel!C5:C1000)/SUM(Fuel!F5:F1000)*100,\"\")", "0.0"),
        ("Average MPG (UK)", "=IFERROR(282.481/B10,\"\")", "0.0"), ("Items due soon", '=COUNTIFS(Service!I4:I500,"<=1000",Service!I4:I500,">-100000")+COUNTIFS(Service!J4:J500,"<=30",Service!J4:J500,">-100000")', "0")], w=(30, 18))
header(sm, ["Month", "Fuel", "Service & repairs"], [30, 18, 18], row=15, freeze=False)
for m in range(1, 13):
    r = 15 + m; sm[f"A{r}"] = MONTHS[m - 1]; sm[f"B{r}"] = f"=SUMIF(Fuel!$J$4:$J$1000,{m},Fuel!$D$4:$D$1000)"
    sm[f"C{r}"] = f'=SUMPRODUCT((Service!$A$4:$A$500<>"")*(MONTH(Service!$A$4:$A$500+0)={m}),Service!$F$4:$F$500)'
    sm[f"B{r}"].number_format = sm[f"C{r}"].number_format = M
howto(wb, C, ["1. Each time you fill up, fill the tank completely and log the date, odometer, litres and cost on the Fuel tab. Consumption is worked out from the distance since your last fill-up.",
              "2. Log services, tyres, repairs and inspections on the Service tab. Add when the next one is due (by km or date) and it turns red when it's within 1,000 km or 30 days.",
              "3. The Summary shows total running cost, cost per km, average consumption and spending per month.", "Using miles and gallons? Type miles in Odometer and gallons in Litres, and read the cost per mile; the L/100 km columns then won't apply."])
wb.save(OUT / "Car-Maintenance-Fuel-Log.xlsx")

# 6. Dividend income tracker
C = "5F3DC4"; title, header = kit(C); wb = Workbook(); hd = wb.active; hd.title = "Holdings"
title(hd, "Dividend holdings", "Your dividend stocks and ETFs with yield and expected yearly income.")
header(hd, ["Ticker", "Name", "Shares", "Price", "Value", "Annual dividend / share", "Yield", "Annual income", "Monthly average", "Pays in (months)"], [10, 24, 9, 10, 12, 14, 8, 13, 13, 18])
for r, h in enumerate([("VYM", "Vanguard High Dividend ETF", 40, 120, 3.40, "Mar Jun Sep Dec"), ("KO", "Coca-Cola", 25, 62, 1.94, "Apr Jul Oct Dec"), ("O", "Realty Income", 60, 57, 3.16, "Monthly"), ("JNJ", "Johnson & Johnson", 10, 155, 4.96, "Mar Jun Sep Dec")], 4):
    for c, x in zip("ABCDFJ", h): hd[f"{c}{r}"] = x
for r in range(4, 204):
    hd[f"E{r}"] = f'=IF(A{r}="","",C{r}*D{r})'; hd[f"G{r}"] = f'=IF(OR(A{r}="",N(D{r})=0),"",F{r}/D{r})'; hd[f"H{r}"] = f'=IF(A{r}="","",C{r}*F{r})'; hd[f"I{r}"] = f'=IF(A{r}="","",H{r}/12)'
    for c in "DEFHI": hd[f"{c}{r}"].number_format = M
    hd[f"G{r}"].number_format = "0.00%"
hd.conditional_formatting.add("G4:G203", DataBarRule(start_type="num", start_value=0, end_type="max", color="9775FA"))
lg = wb.create_sheet("Received"); title(lg, "Dividends received", "Log each payment as it lands in your account.")
header(lg, ["Date", "Ticker", "Gross", "Tax withheld", "Net", "Reinvested?", "Month", "Year"], [12, 10, 11, 12, 11, 12, 8, 8])
dv(lg, "=Holdings!$A$4:$A$203", "B4:B3000"); dv(lg, '"Yes,No"', "F4:F3000")
for r, d in enumerate([(dt.date(y, 1, 15), "O", 15.80, 2.37, "Yes"), (dt.date(y, 2, 14), "O", 15.80, 2.37, "Yes"), (dt.date(y, 3, 10), "JNJ", 12.40, 1.86, "No"), (dt.date(y, 3, 26), "VYM", 34.00, 5.10, "Yes")], 4):
    for c, x in zip("ABCDF", d): lg[f"{c}{r}"] = x
for r in range(4, 3001):
    lg[f"A{r}"].number_format = "yyyy-mm-dd"; lg[f"E{r}"] = f'=IF(C{r}="","",C{r}-N(D{r}))'
    for c in "CDE": lg[f"{c}{r}"].number_format = M
    lg[f"G{r}"] = f'=IF(A{r}="","",MONTH(A{r}))'; lg[f"H{r}"] = f'=IF(A{r}="","",YEAR(A{r}))'
sm = wb.create_sheet("Summary", 0); title(sm, "Dividend summary", "Expected vs received. Change the year in B4.")
kv(sm, [("Year", y, "0"), ("Portfolio value", "=SUM(Holdings!E4:E203)", M), ("Expected annual income", "=SUM(Holdings!H4:H203)", M), ("Portfolio yield", "=IF(B5=0,\"\",B6/B5)", "0.00%"),
        ("Received this year (net)", "=SUMIF(Received!H4:H3000,B4,Received!E4:E3000)", M), ("Of expected", "=IF(B6=0,\"\",B8/B6)", "0%"), ("Annual income goal", 3000, M), ("Progress to goal", "=IF(B10=0,\"\",B6/B10)", "0%")], w=(28, 16))
sm.conditional_formatting.add("B11", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="9775FA"))
header(sm, ["Month", "Net received"], [28, 16], row=14, freeze=False)
for m in range(1, 13):
    r = 14 + m; sm[f"A{r}"] = MONTHS[m - 1]; sm[f"B{r}"] = f"=SUMIFS(Received!$E$4:$E$3000,Received!$G$4:$G$3000,{m},Received!$H$4:$H$3000,$B$4)"; sm[f"B{r}"].number_format = M
ch = BarChart(); ch.title = "Dividends by month"; ch.height = 7; ch.width = 16; ch.add_data(Reference(sm, min_col=2, min_row=14, max_row=26), titles_from_data=True); ch.legend = None
ch.set_categories(Reference(sm, min_col=1, min_row=15, max_row=26)); sm.add_chart(ch, "D4")
howto(wb, C, ["1. List your dividend stocks and ETFs on Holdings with shares, current price and annual dividend per share. Value, yield and expected income are calculated.",
              "2. Log each dividend payment on Received, with any tax withheld.", "3. The Summary compares expected and received income, tracks progress to your income goal and charts dividends by month.",
              "4. Update prices and dividends now and then. Sample tickers are examples only, not recommendations. Delete them before you start."])
wb.save(OUT / "Dividend-Income-Tracker.xlsx")
print("built 6")
