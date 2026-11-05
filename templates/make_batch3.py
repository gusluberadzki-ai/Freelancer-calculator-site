"""Round 7 spreadsheet products into products/. Run: python3 make_batch3.py (reuses helpers from make_batch2.py)"""
import pathlib
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
today = dt.date.today(); y = today.year

# 1. Etsy seller profit calculator
C = "D35400"; title, header = kit(C); wb = Workbook(); st = wb.active; st.title = "Fee settings"
title(st, "Etsy fee settings", "Check these against Etsy's current fees for your country and update if needed.")
fees = [("Listing fee (per sale)", 0.20, M), ("Transaction fee", 0.065, "0.0%"), ("Payment processing %", 0.03, "0.0%"), ("Payment processing fixed", 0.25, M), ("Offsite Ads fee (if the order came from an ad)", 0.15, "0.0%"), ("Sales tax / VAT on fees", 0, "0.0%")]
for r, (n, v, f) in enumerate(fees, 4):
    st[f"A{r}"] = n; st[f"B{r}"] = v; st[f"B{r}"].number_format = f; st[f"B{r}"].fill = SOFT; st[f"A{r}"].font = Font(bold=True)
st.column_dimensions["A"].width = 44; st.column_dimensions["B"].width = 12
pc = wb.create_sheet("Product calculator", 0); title(pc, "Etsy profit calculator", "Enter each product's price and costs to see your real profit per sale.")
header(pc, ["Product", "Sale price", "Shipping charged", "Material cost", "Packaging", "Shipping cost", "Offsite ad? (Y/N)", "Etsy fees", "Profit", "Margin", "Price for 30% margin"], [24, 11, 11, 11, 11, 11, 10, 11, 11, 9, 14])
prod = [("Soy candle", 22, 4.5, 4.2, 1.1, 4.2, "N"), ("Personalised mug", 18, 5, 5.5, 1.5, 5.0, "N"), ("Digital planner", 9, 0, 0, 0, 0, "Y")]
for r, p in enumerate(prod, 4):
    for c, x in enumerate(p, 1): pc.cell(r, c, x)
dv(pc, '"Y,N"', "G4:G200")
for r in range(4, 201):
    rev = f"(B{r}+C{r})"
    pc[f"H{r}"] = (f'=IF(A{r}="","",\'Fee settings\'!$B$4+{rev}*\'Fee settings\'!$B$5+{rev}*\'Fee settings\'!$B$6+\'Fee settings\'!$B$7'
                   f'+IF(UPPER(G{r})="Y",{rev}*\'Fee settings\'!$B$8,0))*(1+\'Fee settings\'!$B$9)')
    pc[f"H{r}"] = f'=IF(A{r}="","",(\'Fee settings\'!$B$4+{rev}*(\'Fee settings\'!$B$5+\'Fee settings\'!$B$6)+\'Fee settings\'!$B$7+IF(UPPER(G{r})="Y",{rev}*\'Fee settings\'!$B$8,0))*(1+\'Fee settings\'!$B$9))'
    pc[f"I{r}"] = f'=IF(A{r}="","",{rev}-D{r}-E{r}-F{r}-H{r})'
    pc[f"J{r}"] = f'=IF(OR(A{r}="",{rev}=0),"",I{r}/{rev})'
    # price p so that p+C - costs - fees(p+C) = 0.3(p+C); fees linear: a + b*(p+C), a=(listing+fixed)*(1+tax), b=(tx+proc+ad)*(1+tax)
    pc[f"K{r}"] = (f'=IF(A{r}="","",(D{r}+E{r}+F{r}+(\'Fee settings\'!$B$4+\'Fee settings\'!$B$7)*(1+\'Fee settings\'!$B$9))'
                   f'/(1-0.3-(\'Fee settings\'!$B$5+\'Fee settings\'!$B$6+IF(UPPER(G{r})="Y",\'Fee settings\'!$B$8,0))*(1+\'Fee settings\'!$B$9))-C{r})')
    for c in "BCDEFHIK": pc[f"{c}{r}"].number_format = M
    pc[f"J{r}"].number_format = "0%"
pc.conditional_formatting.add("I4:I200", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
pc.conditional_formatting.add("J4:J200", CellIsRule(operator="lessThan", formula=["0.2"], fill=PatternFill("solid", fgColor="FFF3BF")))
sl = wb.create_sheet("Sales log"); title(sl, "Sales log", "Log each order to track monthly revenue and profit.")
header(sl, ["Date", "Product", "Qty", "Revenue", "Profit (auto)", "Month"], [12, 24, 7, 12, 13, 8])
dv(sl, "='Product calculator'!$A$4:$A$200", "B4:B2000")
for r in range(4, 2001):
    sl[f"A{r}"].number_format = "yyyy-mm-dd"
    sl[f"D{r}"] = f'=IF(B{r}="","",C{r}*IFERROR(INDEX(\'Product calculator\'!$B$4:$B$200,MATCH(B{r},\'Product calculator\'!$A$4:$A$200,0))+INDEX(\'Product calculator\'!$C$4:$C$200,MATCH(B{r},\'Product calculator\'!$A$4:$A$200,0)),0))'
    sl[f"E{r}"] = f'=IF(B{r}="","",C{r}*IFERROR(INDEX(\'Product calculator\'!$I$4:$I$200,MATCH(B{r},\'Product calculator\'!$A$4:$A$200,0)),0))'
    sl[f"F{r}"] = f'=IF(A{r}="","",MONTH(A{r}))'
    sl[f"D{r}"].number_format = sl[f"E{r}"].number_format = M
for i, s in enumerate([(dt.date(y, 1, 4), "Soy candle", 2), (dt.date(y, 1, 9), "Digital planner", 5), (dt.date(y, 2, 2), "Personalised mug", 1)], 4):
    sl[f"A{i}"], sl[f"B{i}"], sl[f"C{i}"] = s
sl["H3"] = "Month"; sl["I3"] = "Revenue"; sl["J3"] = "Profit"
for c in "HIJ": sl[f"{c}3"].font = Font(bold=True)
for m in range(1, 13):
    r = 3 + m; sl[f"H{r}"] = MONTHS[m - 1]; sl[f"I{r}"] = f"=SUMIF($F$4:$F$2000,{m},$D$4:$D$2000)"; sl[f"J{r}"] = f"=SUMIF($F$4:$F$2000,{m},$E$4:$E$2000)"
    sl[f"I{r}"].number_format = sl[f"J{r}"].number_format = M
sl["H16"] = "Year"; sl["I16"] = "=SUM(I4:I15)"; sl["J16"] = "=SUM(J4:J15)"; sl["H16"].font = Font(bold=True)
sl["I16"].number_format = sl["J16"].number_format = M
howto(wb, C, ["1. Check the Fee settings tab against Etsy's current fee page for your country. Change any value that differs.", "2. On Product calculator, add each product with its price, the shipping you charge and your real costs.",
              "3. Etsy fees, profit, margin and the price you'd need for a 30% margin are calculated for you. Low margins turn yellow; losses turn red.", "4. Log orders on Sales log to see revenue and profit by month.", "Fee defaults are typical US values at the time of writing and may change."])
wb.save(OUT / "Etsy-Seller-Profit-Calculator.xlsx")

# 2. Subscription tracker
C = "6741D9"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Subscriptions"
title(ws, "Subscription Tracker", "See what every subscription really costs you per month and per year.")
header(ws, ["Service", "Category", "Price", "Billing", "Monthly cost", "Yearly cost", "Next renewal", "Days to renewal", "Keep?", "Notes"], [22, 14, 10, 11, 12, 12, 13, 12, 10, 26])
subs = [("Netflix", "Streaming", 15.49, "Monthly", today + dt.timedelta(days=9), "Keep"), ("Spotify", "Music", 11.99, "Monthly", today + dt.timedelta(days=3), "Keep"), ("Adobe CC", "Software", 659.88, "Yearly", today + dt.timedelta(days=40), "Review"),
        ("Gym", "Health", 35, "Monthly", today + dt.timedelta(days=15), "Cancel"), ("Cloud storage", "Software", 2.99, "Monthly", today + dt.timedelta(days=21), "Keep"), ("News site", "News", 39, "Quarterly", today + dt.timedelta(days=60), "Review")]
for r, s in enumerate(subs, 4):
    ws[f"A{r}"], ws[f"B{r}"], ws[f"C{r}"], ws[f"D{r}"], ws[f"G{r}"], ws[f"I{r}"] = s
dv(ws, '"Weekly,Monthly,Quarterly,Yearly"', "D4:D200"); dv(ws, '"Keep,Review,Cancel"', "I4:I200")
for r in range(4, 201):
    ws[f"E{r}"] = f'=IF(A{r}="","",C{r}*IF(D{r}="Weekly",52/12,IF(D{r}="Quarterly",1/3,IF(D{r}="Yearly",1/12,1))))'
    ws[f"F{r}"] = f'=IF(A{r}="","",E{r}*12)'; ws[f"H{r}"] = f'=IF(OR(A{r}="",G{r}=""),"",G{r}-TODAY())'
    for c in "CEF": ws[f"{c}{r}"].number_format = M
    ws[f"G{r}"].number_format = "yyyy-mm-dd"
ws.conditional_formatting.add("H4:H200", FormulaRule(formula=['AND(ISNUMBER(H4),H4<=7)'], fill=PatternFill("solid", fgColor="FFE3E3"), font=Font(bold=True, color="C0392B")))
ws.conditional_formatting.add("A4:J200", FormulaRule(formula=['$I4="Cancel"'], font=Font(strike=True, color="999999")))
sm = wb.create_sheet("Summary", 0); title(sm, "Subscription summary", "Updates automatically.")
rows = [("Active subscriptions", '=COUNTA(Subscriptions!A4:A200)', "0"), ("Total per month", "=SUM(Subscriptions!E4:E200)", M), ("Total per year", "=SUM(Subscriptions!F4:F200)", M),
        ("Saving per year if you cancel the 'Cancel' ones", '=SUMIF(Subscriptions!I4:I200,"Cancel",Subscriptions!F4:F200)', M), ("Renewing in the next 7 days", '=COUNTIFS(Subscriptions!H4:H200,">=0",Subscriptions!H4:H200,"<=7")', "0")]
for r, (a, f, nf_) in enumerate(rows, 4):
    sm[f"A{r}"] = a; sm[f"B{r}"] = f; sm[f"B{r}"].number_format = nf_; sm[f"A{r}"].font = Font(bold=True); sm[f"B{r}"].fill = SOFT
sm.column_dimensions["A"].width = 46; sm.column_dimensions["B"].width = 14
header(sm, ["Category", "Per month"], [46, 14], row=11, freeze=False)
for i, c in enumerate(["Streaming", "Music", "Software", "Health", "News", "Gaming", "Food", "Other"], 12):
    sm[f"A{i}"] = c; sm[f"B{i}"] = f'=SUMIF(Subscriptions!$B$4:$B$200,A{i},Subscriptions!$E$4:$E$200)'; sm[f"B{i}"].number_format = M
dv(ws, "=Summary!$A$12:$A$19", "B4:B200")
howto(wb, C, ["1. List every subscription: price, how often you're billed and the next renewal date.", "2. Monthly and yearly cost are worked out for you. Renewals in the next 7 days turn red.",
              "3. Mark each one Keep, Review or Cancel. The Summary shows how much you'd save by cancelling.", "4. Update the renewal date after each payment."])
wb.save(OUT / "Subscription-Tracker.xlsx")

# 3. Student assignment & grade tracker
C = "0B7285"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Assignments"
title(ws, "Assignment Tracker", "Every assignment, test and deadline in one list.")
header(ws, ["Subject", "Assignment", "Type", "Due date", "Days left", "Status", "Score", "Out of", "%", "Weight %"], [16, 30, 12, 12, 10, 13, 9, 9, 8, 10])
dv(ws, '"Homework,Essay,Project,Quiz,Test,Exam,Lab,Presentation"', "C4:C500"); dv(ws, '"Not started,In progress,Submitted,Graded"', "F4:F500")
asg = [("Maths", "Algebra worksheet", "Homework", today + dt.timedelta(days=2), "In progress", None, None, 5), ("English", "Essay: Macbeth", "Essay", today + dt.timedelta(days=9), "Not started", None, None, 20),
       ("Biology", "Cell quiz", "Quiz", today - dt.timedelta(days=5), "Graded", 17, 20, 10), ("Maths", "Unit 1 test", "Test", today - dt.timedelta(days=12), "Graded", 41, 50, 25), ("History", "WW1 project", "Project", today - dt.timedelta(days=3), "Graded", 78, 100, 30)]
for r, a in enumerate(asg, 4):
    for c, x in zip("ABCDFGHJ", a): ws[f"{c}{r}"] = x
for r in range(4, 501):
    ws[f"D{r}"].number_format = "ddd d mmm"
    ws[f"E{r}"] = f'=IF(OR(D{r}="",F{r}="Submitted",F{r}="Graded"),"",D{r}-TODAY())'
    ws[f"I{r}"] = f'=IF(OR(G{r}="",H{r}="",H{r}=0),"",G{r}/H{r})'; ws[f"I{r}"].number_format = "0%"
ws.conditional_formatting.add("E4:E500", FormulaRule(formula=['AND(ISNUMBER(E4),E4<0)'], fill=PatternFill("solid", fgColor="FFE3E3"), font=Font(bold=True, color="C0392B")))
ws.conditional_formatting.add("E4:E500", FormulaRule(formula=['AND(ISNUMBER(E4),E4>=0,E4<=3)'], fill=PatternFill("solid", fgColor="FFF3BF")))
gr = wb.create_sheet("Grades", 0); title(gr, "Grades by subject", "Weighted average of graded work. Updates automatically.")
header(gr, ["Subject", "Graded items", "Weighted average", "Letter", "Due this week"], [18, 13, 16, 9, 14], row=4, freeze=False)
for i, s in enumerate(["Maths", "English", "Biology", "Chemistry", "Physics", "History", "Geography", "Languages", "Art", "Computing"], 5):
    gr[f"A{i}"] = s; gr[f"B{i}"] = f'=COUNTIFS(Assignments!$A$4:$A$500,A{i},Assignments!$F$4:$F$500,"Graded")'
    gr[f"C{i}"] = f'=IFERROR(SUMPRODUCT((Assignments!$A$4:$A$500=A{i})*(Assignments!$F$4:$F$500="Graded")*(Assignments!$H$4:$H$500>0),Assignments!$G$4:$G$500/IF(Assignments!$H$4:$H$500=0,1,Assignments!$H$4:$H$500),Assignments!$J$4:$J$500)/SUMPRODUCT((Assignments!$A$4:$A$500=A{i})*(Assignments!$F$4:$F$500="Graded")*(Assignments!$H$4:$H$500>0),Assignments!$J$4:$J$500),"")'
    gr[f"C{i}"].number_format = "0.0%"
    gr[f"D{i}"] = f'=IF(C{i}="","",IF(C{i}>=0.9,"A",IF(C{i}>=0.8,"B",IF(C{i}>=0.7,"C",IF(C{i}>=0.6,"D","F")))))'
    gr[f"E{i}"] = f'=COUNTIFS(Assignments!$A$4:$A$500,A{i},Assignments!$E$4:$E$500,">=0",Assignments!$E$4:$E$500,"<=7")'
gr["A16"] = "Overdue"; gr["B16"] = '=COUNTIF(Assignments!E4:E500,"<0")'; gr["A16"].font = Font(bold=True, color="C0392B")
dv(ws, "=Grades!$A$5:$A$14", "A4:A500")
howto(wb, C, ["1. Rename the subjects on the Grades tab to match your classes.", "2. Add every assignment with its due date. Days left turns yellow when 3 or fewer remain and red when overdue.",
              "3. When work is graded, enter the score, what it was out of, and its weight (e.g. 25 for a test worth 25% of the grade).", "4. The Grades tab shows your weighted average and letter grade per subject."])
wb.save(OUT / "Student-Assignment-Grade-Tracker.xlsx")

# 4. Home renovation budget
C = "8F5B34"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Budget"
title(ws, "Home Renovation Budget", "Plan each room, get quotes, track spending and keep a contingency.")
ws["A4"] = "Total budget"; ws["B4"] = 30000; ws["A5"] = "Contingency %"; ws["B5"] = 0.1; ws["B5"].number_format = "0%"; ws["B4"].number_format = M
ws["A6"] = "Available for work"; ws["B6"] = "=B4*(1-B5)"; ws["B6"].number_format = M
for r in (4, 5, 6): ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
header(ws, ["Room / area", "Item", "Quote 1", "Quote 2", "Quote 3", "Budget (lowest quote)", "Actual spent", "Difference", "Status"], [18, 26, 12, 12, 12, 16, 13, 13, 13], row=8)
items = [("Kitchen", "Cabinets & worktops", 7800, 8600, 7200, 6900), ("Kitchen", "Appliances", 3200, None, None, 3350), ("Bathroom", "Full refit", 6500, 5900, None, None), ("Living room", "Flooring", 1800, 2100, 1650, 1650), ("Whole house", "Painting", 2400, 2600, None, None), ("Whole house", "Electrics", 3100, None, None, None)]
for r, it in enumerate(items, 9):
    for c, x in zip("ABCDEG", it): ws[f"{c}{r}"] = x
dv(ws, '"Planning,Quoted,Booked,In progress,Done"', "I9:I200")
for r in range(9, 201):
    ws[f"F{r}"] = f'=IF(COUNT(C{r}:E{r})=0,"",MIN(C{r}:E{r}))'; ws[f"H{r}"] = f'=IF(OR(F{r}="",G{r}=""),"",F{r}-G{r})'
    for c in "CDEFGH": ws[f"{c}{r}"].number_format = M
ws.conditional_formatting.add("H9:H200", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
ws["K8"] = "Summary"; ws["K8"].font = Font(bold=True, size=13, color=C)
summ = [("Planned (lowest quotes)", "=SUM(F9:F200)"), ("Spent so far", "=SUM(G9:G200)"), ("Left of work budget", "=B6-SUM(G9:G200)"), ("Planned vs available", "=B6-SUM(F9:F200)"), ("Contingency", "=B4*B5")]
for i, (a, f) in enumerate(summ, 9):
    ws[f"K{i}"] = a; ws[f"L{i}"] = f; ws[f"L{i}"].number_format = M; ws[f"L{i}"].fill = SOFT
ws.column_dimensions["K"].width = 24; ws.column_dimensions["L"].width = 14
ws.conditional_formatting.add("L11:L12", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
pm = wb.create_sheet("Payments"); title(pm, "Payments & contractors", "Track deposits and payments to each trade.")
header(pm, ["Date", "Contractor", "Trade", "Phone", "Item", "Amount", "Paid?"], [12, 20, 14, 14, 24, 12, 8])
for r in range(4, 300): pm[f"A{r}"].number_format = "yyyy-mm-dd"; pm[f"F{r}"].number_format = M
dv(pm, '"Yes,No"', "G4:G300")
howto(wb, C, ["1. Set your total budget and contingency (10–15% is typical) on the Budget tab.", "2. Add each job by room. Enter up to 3 quotes; the lowest becomes the budget for that line.",
              "3. Enter what you actually spend. Overspends turn red, and the summary shows what's left.", "4. Log contractor details and payments on the Payments tab."])
wb.save(OUT / "Home-Renovation-Budget.xlsx")

# 5. Content creator income tracker
C = "C2255C"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Income log"
title(ws, "Creator Income Log", "Log every payment from platforms, sponsors and products.")
header(ws, ["Date", "Source", "Type", "Brand / client", "Amount", "Paid?", "Month"], [12, 16, 16, 22, 12, 8, 8])
srcs = "YouTube,TikTok,Instagram,Twitch,Patreon,Newsletter,Blog,Own products,Other"; typs = "Ad revenue,Sponsorship,Affiliate,Product sales,Membership,Tips,Other"
dv(ws, f'"{srcs}"', "B4:B2000"); dv(ws, f'"{typs}"', "C4:C2000"); dv(ws, '"Yes,No"', "F4:F2000")
smp = [(dt.date(y, 1, 21), "YouTube", "Ad revenue", "", 412.5, "Yes"), (dt.date(y, 1, 28), "Instagram", "Sponsorship", "SkinCo", 600, "Yes"), (dt.date(y, 2, 3), "Blog", "Affiliate", "Amazon", 88.2, "Yes"),
       (dt.date(y, 2, 21), "YouTube", "Ad revenue", "", 455.1, "Yes"), (dt.date(y, 2, 25), "TikTok", "Sponsorship", "AppX", 350, "No"), (dt.date(y, 3, 2), "Patreon", "Membership", "", 240, "Yes")]
for r, s in enumerate(smp, 4):
    for c, x in enumerate(s, 1): ws.cell(r, c, x)
for r in range(4, 2001):
    ws[f"A{r}"].number_format = "yyyy-mm-dd"; ws[f"E{r}"].number_format = M; ws[f"G{r}"] = f'=IF(A{r}="","",MONTH(A{r}))'
db = wb.create_sheet("Dashboard", 0); title(db, "Creator income dashboard", "Updates automatically from the Income log.")
header(db, ["Source"] + MONTHS + ["Total"], [16] + [10] * 12 + [12], row=4, freeze=False)
for i, s in enumerate(srcs.split(","), 5):
    db[f"A{i}"] = s
    for m in range(1, 13): db.cell(i, m + 1, f"=SUMIFS('Income log'!$E:$E,'Income log'!$B:$B,$A{i},'Income log'!$G:$G,{m})").number_format = M
    db[f"N{i}"] = f"=SUM(B{i}:M{i})"; db[f"N{i}"].number_format = M
tr = 5 + len(srcs.split(",")); db[f"A{tr}"] = "Total"; db[f"A{tr}"].font = Font(bold=True)
for c in range(2, 15):
    x = db.cell(tr, c, f"=SUM({L(c)}5:{L(c)}{tr-1})"); x.number_format = M; x.font = Font(bold=True); x.fill = SOFT
db[f"A{tr+2}"] = "Unpaid invoices"; db[f"B{tr+2}"] = "=SUMIF('Income log'!F4:F2000,\"No\",'Income log'!E4:E2000)"; db[f"B{tr+2}"].number_format = M
db[f"A{tr+3}"] = "Set aside for tax"; db[f"B{tr+3}"] = 0.25; db[f"B{tr+3}"].number_format = "0%"
db[f"A{tr+4}"] = "Tax to set aside"; db[f"B{tr+4}"] = f"=N{tr}*B{tr+3}"; db[f"B{tr+4}"].number_format = M
for r in (tr + 2, tr + 3, tr + 4): db[f"A{r}"].font = Font(bold=True); db[f"B{r}"].fill = SOFT
header(db, ["Type", "Total"], [16, 10], row=tr + 6, freeze=False)
for i, t in enumerate(typs.split(","), tr + 7):
    db[f"A{i}"] = t; db[f"B{i}"] = f"=SUMIF('Income log'!$C:$C,A{i},'Income log'!$E:$E)"; db[f"B{i}"].number_format = M
ch = BarChart(); ch.title = "Income by month"; ch.height = 7; ch.width = 20; ch.add_data(Reference(db, min_col=1, max_col=13, min_row=tr), from_rows=True, titles_from_data=True); ch.set_categories(Reference(db, min_col=2, max_col=13, min_row=4)); db.add_chart(ch, "D" + str(tr + 2))
howto(wb, C, ["1. Log each payment on the Income log: date, platform, type, brand and amount. Mark sponsorships unpaid until the money arrives.", "2. The Dashboard totals income by platform and month, by income type, and shows unpaid invoices.",
              "3. Set your tax rate to see how much to put aside.", "4. Delete the sample rows before you start."])
wb.save(OUT / "Creator-Income-Tracker.xlsx")

# 6. Annual budget planner (12 months)
C = "2B8A3E"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Annual budget"
title(ws, "Annual Budget Planner", "Plan every month of the year: budget, actual and what's left.")
cats_in = ["Salary", "Side income", "Other income"]
cats_out = ["Rent / mortgage", "Utilities", "Groceries", "Transport", "Insurance", "Phone & internet", "Subscriptions", "Eating out", "Shopping", "Health", "Gifts", "Holidays", "Savings", "Debt payments", "Other"]
plan_in = [3200, 300, 0]; plan_out = [1100, 180, 420, 160, 90, 55, 40, 150, 120, 40, 50, 150, 400, 200, 50]
header(ws, ["Category", "Monthly budget"] + MONTHS + ["Year actual", "Budget to date", "Difference"], [20, 12] + [10] * 12 + [12, 12, 12], row=4)
r = 5; ws.cell(r, 1, "INCOME").font = Font(bold=True, color=C); r += 1; i0 = r
for c, p in zip(cats_in, plan_in):
    ws.cell(r, 1, c); ws.cell(r, 2, p).number_format = M
    for m in range(3): ws.cell(r, 3 + m, round(p * (1 + 0.02 * m), 2) if p else None)
    r += 1
it = r; ws.cell(r, 1, "Total income").font = Font(bold=True)
r += 2; ws.cell(r, 1, "SPENDING").font = Font(bold=True, color=C); r += 1; e0 = r
for c, p in zip(cats_out, plan_out):
    ws.cell(r, 1, c); ws.cell(r, 2, p).number_format = M
    for m in range(3): ws.cell(r, 3 + m, round(p * (0.9 + 0.08 * m), 2))
    r += 1
et = r; ws.cell(r, 1, "Total spending").font = Font(bold=True)
for rr in list(range(i0, it)) + list(range(e0, et)):
    for c in range(3, 15): ws.cell(rr, c).number_format = M
    ws.cell(rr, 15, f"=SUM(C{rr}:N{rr})").number_format = M; ws.cell(rr, 16, f"=B{rr}*$B${et+5}").number_format = M
    ws.cell(rr, 17, f"=P{rr}-O{rr}" if rr >= e0 else f"=O{rr}-P{rr}").number_format = M
for tot, a, b in ((it, i0, it), (et, e0, et)):
    for c in range(2, 18):
        x = ws.cell(tot, c, f"=SUM({L(c)}{a}:{L(c)}{b-1})"); x.number_format = M; x.font = Font(bold=True)
lr = et + 2; ws.cell(lr, 1, "LEFT OVER").font = Font(bold=True, size=13)
for c in range(2, 17):
    x = ws.cell(lr, c, f'=IF(COUNT({L(c)}{i0}:{L(c)}{it-1},{L(c)}{e0}:{L(c)}{et-1})=0,"",{L(c)}{it}-{L(c)}{et})'); x.number_format = M; x.font = Font(bold=True); x.fill = SOFT
ws.cell(lr + 3, 1, "Months entered so far").font = Font(italic=True, color="777777")
ws.cell(lr + 3, 2, "=" + "+".join(f"IF(COUNT({L(c)}{i0}:{L(c)}{it-1},{L(c)}{e0}:{L(c)}{et-1})>0,1,0)" for c in range(3, 15)))
ws.cell(lr + 1, 1, "Savings rate")
for c in range(3, 16): ws.cell(lr + 1, c, f'=IF(OR({L(c)}{it}=0,{L(c)}{it}=""),"",({L(c)}{lr}+{L(c)}{e0+cats_out.index("Savings")})/{L(c)}{it})').number_format = "0%"
ws.conditional_formatting.add(f"Q{e0}:Q{et}", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
ws.conditional_formatting.add(f"C{lr}:O{lr}", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
ch = BarChart(); ch.title = "Income vs spending"; ch.height = 7; ch.width = 22
ch.add_data(Reference(ws, min_col=1, max_col=14, min_row=it), from_rows=True, titles_from_data=True); ch.add_data(Reference(ws, min_col=1, max_col=14, min_row=et), from_rows=True, titles_from_data=True)
ch.set_categories(Reference(ws, min_col=3, max_col=14, min_row=4)); ws.add_chart(ch, f"A{lr+5}")
howto(wb, C, ["1. Put your planned monthly amount for each category in the Monthly budget column. Rename categories to suit you.", "2. At the end of each month, type the actual amounts into that month's column.",
              "3. Totals, money left over and your savings rate update automatically. Year actual vs budget to date (monthly budget × months entered) shows where you overspent (red).", "4. Delete the sample numbers in Jan–Mar before you start."])
wb.save(OUT / "Annual-Budget-Planner.xlsx")
print("built 6")
