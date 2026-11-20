"""Round 10 spreadsheet products into products/. Run: python3 make_batch5.py (reuses helpers from make_batch2.py)"""
import pathlib
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
today = dt.date.today(); y = today.year
mon = today - dt.timedelta(days=today.weekday())

# 1. Gantt project planner
C = "1864AB"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Gantt"
title(ws, "Project Planner & Gantt Chart", "Enter tasks with a start date and length. The timeline colours itself.")
ws["A3"] = "Project start"; ws["B3"] = mon; ws["B3"].number_format = "yyyy-mm-dd"; ws["B3"].fill = SOFT; ws["A3"].font = Font(bold=True)
ws["D3"] = "Today"; ws["E3"] = "=TODAY()"; ws["E3"].number_format = "yyyy-mm-dd"
heads = ["Task", "Owner", "Start", "Days", "End", "% done", "Status"]
widths = [30, 12, 11, 7, 11, 8, 12]
hf = PatternFill("solid", fgColor=C); hfont = Font(bold=True, color="FFFFFF")
for i, (h, w) in enumerate(zip(heads, widths), 1):
    x = ws.cell(5, i, h); x.fill = hf; x.font = hfont; x.alignment = Alignment(horizontal="center", wrap_text=True); ws.column_dimensions[L(i)].width = w
NW = 84  # 12 weeks of days
for d in range(NW):
    col = 8 + d; ws.column_dimensions[L(col)].width = 2.6
    x = ws.cell(5, col, f"=$B$3+{d}"); x.number_format = "d"; x.font = Font(size=7, bold=True, color="FFFFFF"); x.fill = hf; x.alignment = Alignment(horizontal="center")
    if d % 7 == 0:
        w = ws.cell(4, col, f'=TEXT($B$3+{d},"d mmm")'); w.font = Font(size=8, bold=True, color=C)
tasks = [("Kick-off meeting", "Sam", 0, 1, 1), ("Research & requirements", "Alex", 1, 6, 1), ("Design mock-ups", "Riley", 3, 10, 0.3), ("Client review", "Sam", 15, 3, 0),
         ("Build", "Alex", 18, 21, 0), ("Testing", "Jordan", 36, 7, 0), ("Launch", "Sam", 44, 1, 0), ("Wrap-up report", "Riley", 46, 4, 0)]
for r, (t, o, s, n, p) in enumerate(tasks, 6):
    ws[f"A{r}"], ws[f"B{r}"], ws[f"C{r}"], ws[f"D{r}"], ws[f"F{r}"] = t, o, mon + dt.timedelta(days=s), n, p
last = 6 + 59
for r in range(6, last + 1):
    ws[f"C{r}"].number_format = ws[f"E{r}"].number_format = "dd mmm"
    ws[f"E{r}"] = f'=IF(OR(C{r}="",D{r}=""),"",C{r}+D{r}-1)'; ws[f"F{r}"].number_format = "0%"
    ws[f"G{r}"] = f'=IF(A{r}="","",IF(N(F{r})>=1,"Done",IF(AND(E{r}<TODAY(),N(F{r})<1),"Late",IF(C{r}<=TODAY(),"In progress","Not started"))))'
first, lastc = L(8), L(8 + NW - 1)
rng = f"{first}6:{lastc}{last}"
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND($C6<>"",{first}$5>=$C6,{first}$5<=$C6+($E6-$C6+1)*$F6-1)'], fill=PatternFill("solid", fgColor="1864AB"), stopIfTrue=True))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND($C6<>"",{first}$5>=$C6,{first}$5<=$E6)'], fill=PatternFill("solid", fgColor="A5C8F0"), stopIfTrue=True))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND($A6<>"",{first}$5=TODAY())'], fill=PatternFill("solid", fgColor="FFE066")))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND($A6<>"",WEEKDAY({first}$5,2)>5)'], fill=PatternFill("solid", fgColor="F1F3F5")))
ws.conditional_formatting.add(f"G6:G{last}", FormulaRule(formula=['$G6="Late"'], font=Font(bold=True, color="C0392B")))
ws.conditional_formatting.add(f"G6:G{last}", FormulaRule(formula=['$G6="Done"'], font=Font(color="2B8A3E")))
ws.conditional_formatting.add(f"F6:F{last}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="4DABF7"))
ws.freeze_panes = "H6"
sm = wb.create_sheet("Summary"); title(sm, "Project summary", "Updates automatically.")
rows = [("Tasks", '=COUNTA(Gantt!A6:A65)', "0"), ("Done", '=COUNTIF(Gantt!G6:G65,"Done")', "0"), ("In progress", '=COUNTIF(Gantt!G6:G65,"In progress")', "0"), ("Late", '=COUNTIF(Gantt!G6:G65,"Late")', "0"),
        ("Overall progress (by days of work)", '=IFERROR(SUMPRODUCT(Gantt!D6:D65,Gantt!F6:F65)/SUM(Gantt!D6:D65),0)', "0%"), ("Project end date", '=MAX(Gantt!E6:E65)', "dd mmm yyyy"), ("Days left", '=MAX(0,B9-TODAY())', "0")]
for r, (a, f, nf_) in enumerate(rows, 4):
    sm[f"A{r}"] = a; sm[f"B{r}"] = f; sm[f"B{r}"].number_format = nf_; sm[f"A{r}"].font = Font(bold=True); sm[f"B{r}"].fill = SOFT
sm.column_dimensions["A"].width = 36; sm.column_dimensions["B"].width = 16
howto(wb, C, ["1. Set the project start date at the top of the Gantt tab. The timeline shows 12 weeks from that day.", "2. Add each task with an owner, a start date and how many days it takes. The end date and status are worked out for you.",
              "3. Update % done as you go. The bar fills dark blue for finished work and light blue for what's left. Today is yellow, weekends are grey.", "4. Late tasks turn red. Summary shows overall progress and days left. Delete the sample tasks first."])
wb.save(OUT / "Gantt-Project-Planner.xlsx")

# 2. Freelance quote builder
C = "0B7285"; title, header = kit(C); wb = Workbook(); st = wb.active; st.title = "Settings"
title(st, "Your details", "Fill these in once. They appear on every quote.")
for r, (n, v) in enumerate([("Business name", "Your Studio"), ("Your name", "Your Name"), ("Email", "you@example.com"), ("Website", "yourstudio.com"), ("Currency symbol", "$"), ("Tax rate (0 if none)", 0), ("Quote valid for (days)", 30), ("Deposit required", 0.5)], 4):
    st[f"A{r}"] = n; st[f"B{r}"] = v; st[f"A{r}"].font = Font(bold=True); st[f"B{r}"].fill = SOFT
st["B9"].number_format = "0%"; st["B11"].number_format = "0%"; st.column_dimensions["A"].width = 26; st.column_dimensions["B"].width = 30
rt = wb.create_sheet("Rate card"); title(rt, "Rate card", "Your services and prices. Pick them on the quote.")
header(rt, ["Service", "Unit", "Rate"], [34, 12, 12])
for r, s in enumerate([("Logo design", "project", 450), ("Brand guidelines", "project", 600), ("Website page design", "page", 250), ("Copywriting", "hour", 55), ("Consulting", "hour", 75), ("Social media graphics", "post", 35), ("Revisions (extra round)", "round", 90)], 4):
    for c, v in enumerate(s, 1): rt.cell(r, c, v)
for r in range(4, 61): rt[f"C{r}"].number_format = M
q = wb.create_sheet("Quote", 0)
q.column_dimensions["A"].width = 38; q.column_dimensions["B"].width = 10; q.column_dimensions["C"].width = 12; q.column_dimensions["D"].width = 10; q.column_dimensions["E"].width = 14
q["A1"] = "=Settings!B4"; q["A1"].font = Font(bold=True, size=20, color=C); q["E1"] = "QUOTE"; q["E1"].font = Font(bold=True, size=20, color="999999"); q["E1"].alignment = Alignment(horizontal="right")
q["A2"] = '=Settings!B5&"  ·  "&Settings!B6&"  ·  "&Settings!B7'; q["A2"].font = Font(color="777777")
lab = [("Quote no.", "Q-001"), ("Date", today), ("Valid until", "=E5+Settings!B10"), ("Client", "Client name"), ("Project", "Brand refresh")]
for r, (a, v) in enumerate(lab, 4):
    q[f"D{r}"] = a; q[f"E{r}"] = v; q[f"D{r}"].font = Font(bold=True); q[f"E{r}"].alignment = Alignment(horizontal="right")
q["E5"].number_format = q["E6"].number_format = "dd mmm yyyy"
hdr = ["Service", "Qty", "Rate", "Discount", "Amount"]
for i, h in enumerate(hdr, 1):
    x = q.cell(10, i, h); x.fill = PatternFill("solid", fgColor=C); x.font = Font(bold=True, color="FFFFFF")
dv(q, "='Rate card'!$A$4:$A$60", "A11:A30")
for r, (s, n, d) in enumerate([("Logo design", 1, 0), ("Brand guidelines", 1, 0.1), ("Social media graphics", 6, 0)], 11):
    q[f"A{r}"], q[f"B{r}"], q[f"D{r}"] = s, n, d
for r in range(11, 31):
    q[f"C{r}"] = f"=IF(A{r}=\"\",\"\",IFERROR(INDEX('Rate card'!$C$4:$C$60,MATCH(A{r},'Rate card'!$A$4:$A$60,0)),0))"
    q[f"E{r}"] = f'=IF(A{r}="","",B{r}*C{r}*(1-N(D{r})))'
    q[f"C{r}"].number_format = q[f"E{r}"].number_format = M; q[f"D{r}"].number_format = "0%"
tot = [("Subtotal", "=SUM(E11:E30)"), ("Tax", "=E32*Settings!B9"), ("TOTAL", "=E32+E33"), ("Deposit to start", "=E34*Settings!B11")]
for r, (a, f) in enumerate(tot, 32):
    q[f"D{r}"] = a; q[f"E{r}"] = f; q[f"E{r}"].number_format = M; q[f"D{r}"].font = Font(bold=True)
q["E34"].font = Font(bold=True, size=13, color=C)
q["A37"] = "What's included"; q["A37"].font = Font(bold=True)
q["A38"] = "2 rounds of revisions per item. Final files delivered as PNG, SVG and PDF."
q["A40"] = "Terms"; q["A40"].font = Font(bold=True)
q["A41"] = '="This quote is valid for "&Settings!B10&" days. A "&TEXT(Settings!B11,"0%")&" deposit is due before work starts; the balance is due on delivery."'
q["A43"] = "Accepted by (name, signature, date): ______________________________________"
q.print_area = "A1:E43"
lg = wb.create_sheet("Quote log"); title(lg, "Quote log", "Track every quote you send and your win rate.")
header(lg, ["Quote no.", "Date", "Client", "Project", "Amount", "Status", "Follow up on"], [11, 12, 20, 22, 12, 12, 13])
for r, s in enumerate([("Q-001", today - dt.timedelta(days=20), "Northwind", "Logo", 450, "Won"), ("Q-002", today - dt.timedelta(days=9), "Bluebird Café", "Menu design", 320, "Lost"), ("Q-003", today - dt.timedelta(days=3), "Acme Ltd", "Website", 2400, "Sent")], 4):
    for c, v in enumerate(s, 1): lg.cell(r, c, v)
dv(lg, '"Draft,Sent,Won,Lost"', "F4:F300")
for r in range(4, 301):
    lg[f"B{r}"].number_format = lg[f"G{r}"].number_format = "yyyy-mm-dd"; lg[f"E{r}"].number_format = M
    lg[f"G{r}"] = f'=IF(F{r}="Sent",B{r}+7,"")'
lg.conditional_formatting.add("G4:G300", FormulaRule(formula=['AND(ISNUMBER(G4),G4<=TODAY())'], fill=PatternFill("solid", fgColor="FFE3E3"), font=Font(bold=True, color="C0392B")))
lg["I3"] = "Win rate"; lg["J3"] = '=IFERROR(COUNTIF(F4:F300,"Won")/(COUNTIF(F4:F300,"Won")+COUNTIF(F4:F300,"Lost")),"")'; lg["J3"].number_format = "0%"
lg["I4"] = "Value won"; lg["J4"] = '=SUMIF(F4:F300,"Won",E4:E300)'; lg["I5"] = "Open quotes"; lg["J5"] = '=SUMIF(F4:F300,"Sent",E4:E300)'
lg["J4"].number_format = lg["J5"].number_format = M
for c in ("I3", "I4", "I5"): lg[c].font = Font(bold=True)
lg.column_dimensions["I"].width = 14; lg.column_dimensions["J"].width = 13
howto(wb, C, ["1. Fill in Settings once: your business details, tax rate, how long quotes stay valid and the deposit you ask for.", "2. List your services and prices on Rate card.",
              "3. On Quote, pick services from the dropdown and set quantities and any discount. Rates, totals, tax and deposit fill in. Edit 'What's included' for each job.",
              "4. Print or File > Download as PDF to send it. Log each quote on Quote log; follow-ups due turn red and you can see your win rate."])
wb.save(OUT / "Freelance-Quote-Builder.xlsx")

# 3. Grocery price book & pantry inventory
C = "5C940D"; title, header = kit(C); wb = Workbook(); pb = wb.active; pb.title = "Price book"
title(pb, "Grocery price book", "Note prices at each shop. The cheapest place for every item is found for you.")
shops = ["Shop A", "Shop B", "Shop C", "Shop D"]
header(pb, ["Item", "Unit"] + shops + ["Cheapest", "Best price", "Saving vs dearest"], [24, 10, 10, 10, 10, 10, 14, 11, 16])
items = [("Milk", "2 L", 1.65, 1.49, 1.79, None), ("Eggs", "12", 3.20, 2.95, 3.49, 3.10), ("Bread", "loaf", 1.40, 1.10, 1.75, None), ("Rice", "1 kg", 1.90, 1.60, 2.10, 1.75), ("Chicken breast", "1 kg", 7.50, 6.90, 8.20, 7.10), ("Coffee", "500 g", 6.50, 5.99, 7.20, None), ("Tinned tomatoes", "400 g", 0.85, 0.55, 0.95, 0.70), ("Olive oil", "1 L", 8.90, 9.50, 7.95, None)]
for r, it in enumerate(items, 4):
    for c, v in enumerate(it, 1):
        if v is not None: pb.cell(r, c, v)
pb["C3"] = "Shop A"
for r in range(4, 201):
    for c in "CDEF": pb[f"{c}{r}"].number_format = M
    pb[f"H{r}"] = f'=IF(COUNT(C{r}:F{r})=0,"",MIN(C{r}:F{r}))'
    pb[f"G{r}"] = f'=IF(H{r}="","",INDEX($C$3:$F$3,MATCH(H{r},C{r}:F{r},0)))'
    pb[f"I{r}"] = f'=IF(COUNT(C{r}:F{r})<2,"",MAX(C{r}:F{r})-H{r})'
    pb[f"H{r}"].number_format = pb[f"I{r}"].number_format = M
for c in "CDEF": pb.conditional_formatting.add(f"{c}4:{c}200", FormulaRule(formula=[f'AND(ISNUMBER({c}4),{c}4=$H4)'], fill=PatternFill("solid", fgColor="D3F9D8"), font=Font(bold=True, color="2B8A3E")))
pb["K3"] = "Rename Shop A–D in the header row to your own shops."; pb["K3"].font = Font(italic=True, color="777777")
pn = wb.create_sheet("Pantry"); title(pn, "Pantry, fridge & freezer", "Know what you have, what's running low and what to use first.")
header(pn, ["Item", "Where", "Category", "Have", "Keep at least", "Use by", "Days left", "Status"], [24, 10, 13, 7, 12, 12, 10, 14])
pan = [("Pasta", "Pantry", "Dry goods", 2, 2, today + dt.timedelta(days=300)), ("Tinned tomatoes", "Pantry", "Tins", 1, 4, today + dt.timedelta(days=400)), ("Frozen peas", "Freezer", "Frozen", 1, 1, today + dt.timedelta(days=120)),
       ("Yoghurt", "Fridge", "Dairy", 3, 2, today + dt.timedelta(days=2)), ("Olive oil", "Pantry", "Oils", 0, 1, today + dt.timedelta(days=200))]
for r, p in enumerate(pan, 4):
    for c, v in enumerate(p, 1): pn.cell(r, c, v)
dv(pn, '"Pantry,Fridge,Freezer,Cupboard"', "B4:B300")
for r in range(4, 301):
    pn[f"F{r}"].number_format = "yyyy-mm-dd"
    pn[f"G{r}"] = f'=IF(F{r}="","",F{r}-TODAY())'
    pn[f"H{r}"] = f'=IF(A{r}="","",IF(AND(ISNUMBER(G{r}),G{r}<0),"Expired",IF(AND(ISNUMBER(G{r}),G{r}<=3),"Use soon",IF(N(D{r})<N(E{r}),"Buy more","OK"))))'
    pn[f"J{r}"] = f'=IF(AND(A{r}<>"",N(D{r})<N(E{r})),1,0)'; pn[f"J{r}"].font = Font(color="FFFFFF")
    pn[f"I{r}"] = f'=IF(J{r}=1,SUM($J$4:J{r}),"")'; pn[f"I{r}"].font = Font(color="FFFFFF")
pn.conditional_formatting.add("H4:H300", FormulaRule(formula=['OR($H4="Expired",$H4="Use soon")'], fill=PatternFill("solid", fgColor="FFE3E3"), font=Font(bold=True, color="C0392B")))
pn.conditional_formatting.add("H4:H300", FormulaRule(formula=['$H4="Buy more"'], fill=PatternFill("solid", fgColor="FFF3BF")))
sh = wb.create_sheet("Shopping list", 0); title(sh, "Shopping list", "Items you're low on appear here automatically, with where they're cheapest.")
header(sh, ["Item", "Need", "Cheapest at", "Best price", "Got it"], [24, 8, 14, 11, 9], freeze=False)
for i in range(30):
    r = 4 + i; k = i + 1
    sh[f"A{r}"] = f'=IFERROR(INDEX(Pantry!$A$4:$A$300,MATCH({k},Pantry!$I$4:$I$300,0)),"")'
    sh[f"B{r}"] = f'=IF(A{r}="","",INDEX(Pantry!$E$4:$E$300,MATCH(A{r},Pantry!$A$4:$A$300,0))-INDEX(Pantry!$D$4:$D$300,MATCH(A{r},Pantry!$A$4:$A$300,0)))'
    sh[f"C{r}"] = f"=IF(A{r}=\"\",\"\",IFERROR(INDEX('Price book'!$G$4:$G$200,MATCH(A{r},'Price book'!$A$4:$A$200,0)),\"\"))"
    sh[f"D{r}"] = f"=IF(A{r}=\"\",\"\",IFERROR(INDEX('Price book'!$H$4:$H$200,MATCH(A{r},'Price book'!$A$4:$A$200,0)),\"\"))"; sh[f"D{r}"].number_format = M
sh["G3"] = "Extra items"; sh["G3"].font = Font(bold=True); sh.column_dimensions["G"].width = 24
for r in range(4, 20): sh[f"G{r}"].fill = SOFT
howto(wb, C, ["1. Price book: rename the shop columns, then note what each item costs at each shop. The cheapest shop is highlighted green with your saving.",
              "2. Pantry: list what you keep in the cupboard, fridge and freezer, how many you have and the minimum you like to keep. Add use-by dates for fresh food.",
              "3. Anything below your minimum shows 'Buy more' and goes onto the Shopping list with where it's cheapest. Food near its use-by date turns red so you use it first.", "4. Delete the sample items before you start."])
wb.save(OUT / "Grocery-Price-Book-Pantry.xlsx")

# 4. Party & event planner
C = "D6336C"; title, header = kit(C); wb = Workbook(); ov = wb.active; ov.title = "Overview"
title(ov, "Party & Event Planner", "Birthdays, showers, anniversaries, work events: plan it all in one file.")
for r, (n, v) in enumerate([("Event", "Mia's 30th birthday"), ("Date", today + dt.timedelta(days=35)), ("Venue", "The Garden Room"), ("Total budget", 1200)], 4):
    ov[f"A{r}"] = n; ov[f"B{r}"] = v; ov[f"A{r}"].font = Font(bold=True); ov[f"B{r}"].fill = SOFT
ov["B5"].number_format = "dd mmm yyyy"; ov["B7"].number_format = M
summ = [("Days to go", "=MAX(0,B5-TODAY())", "0"), ("Guests invited", "=COUNTA(Guests!A4:A300)", "0"), ("Guests coming (people)", '=SUMIF(Guests!D4:D300,"Yes",Guests!E4:E300)', "0"),
        ("Still to reply", '=COUNTIF(Guests!D4:D300,"Waiting")', "0"), ("Planned spend", "=SUM(Budget!C4:C100)", M), ("Spent so far", "=SUM(Budget!D4:D100)", M), ("Left in budget", "=B7-B13", M),
        ("Cost per guest", '=IFERROR(B13/B10,"")', M), ("Tasks done", '=COUNTIF(Tasks!D4:D200,"Done")&" of "&COUNTA(Tasks!A4:A200)', "@")]
for r, (n, f, nf_) in enumerate(summ, 9):
    ov[f"A{r}"] = n; ov[f"B{r}"] = f; ov[f"B{r}"].number_format = nf_; ov[f"A{r}"].font = Font(bold=True)
ov.conditional_formatting.add("B14", CellIsRule(operator="lessThan", formula=["0"], font=Font(bold=True, color="C0392B")))
ov.column_dimensions["A"].width = 26; ov.column_dimensions["B"].width = 24
gs = wb.create_sheet("Guests"); title(gs, "Guest list", "RSVPs, plus-ones and dietary needs.")
header(gs, ["Name", "Contact", "Invited?", "RSVP", "Number of people", "Dietary needs", "Notes"], [22, 22, 9, 10, 10, 18, 22])
for r, g in enumerate([("Mia", "mia@email.com", "Yes", "Yes", 1, ""), ("Tom & Ana", "tom@email.com", "Yes", "Yes", 2, "Vegetarian (Ana)"), ("Leo", "07123 456789", "Yes", "Waiting", 1, ""), ("Priya", "priya@email.com", "Yes", "No", 1, "")], 4):
    for c, v in enumerate(g, 1): gs.cell(r, c, v)
dv(gs, '"Yes,Waiting,No"', "D4:D300"); dv(gs, '"Yes,No"', "C4:C300")
gs.conditional_formatting.add("D4:D300", FormulaRule(formula=['$D4="Waiting"'], fill=PatternFill("solid", fgColor="FFF3BF")))
bd = wb.create_sheet("Budget"); title(bd, "Budget", "Plan each cost, then log what you actually spend.")
header(bd, ["Item", "Supplier", "Planned", "Actual", "Paid?", "Difference"], [24, 20, 11, 11, 8, 12])
for r, b in enumerate([("Venue hire", "The Garden Room", 400, 400, "Yes"), ("Food", "Caterer", 350, None, "No"), ("Drinks", "", 180, None, "No"), ("Cake", "Bakery", 70, 65, "Yes"), ("Decorations", "", 60, 48, "Yes"), ("Music / DJ", "", 120, None, "No"), ("Invitations", "", 15, 12, "Yes")], 4):
    for c, v in enumerate(b, 1):
        if v is not None: bd.cell(r, c, v)
dv(bd, '"Yes,No"', "E4:E100")
for r in range(4, 101):
    bd[f"F{r}"] = f'=IF(OR(C{r}="",D{r}=""),"",C{r}-D{r})'
    for c in "CDF": bd[f"{c}{r}"].number_format = M
bd.conditional_formatting.add("F4:F100", CellIsRule(operator="lessThan", formula=["0"], font=Font(bold=True, color="C0392B")))
tk = wb.create_sheet("Tasks"); title(tk, "To-do list", "Sorted by when to do it. Overdue tasks turn red.")
header(tk, ["Task", "Who", "Do by", "Status"], [32, 12, 12, 12])
evd = today + dt.timedelta(days=35)
for r, (t, w, d, s) in enumerate([("Book venue", "Me", -28, "Done"), ("Send invitations", "Me", -21, "Done"), ("Order cake", "Me", -10, ""), ("Book DJ", "Sam", -14, ""), ("Buy decorations", "Me", -5, ""), ("Confirm final numbers with caterer", "Me", -4, ""), ("Make playlist backup", "Sam", -2, "")], 4):
    tk[f"A{r}"], tk[f"B{r}"], tk[f"C{r}"], tk[f"D{r}"] = t, w, evd + dt.timedelta(days=d), s
dv(tk, '"To do,Done"', "D4:D200")
for r in range(4, 201): tk[f"C{r}"].number_format = "dd mmm"
tk.conditional_formatting.add("A4:D200", FormulaRule(formula=['$D4="Done"'], font=Font(strike=True, color="999999")))
tk.conditional_formatting.add("A4:D200", FormulaRule(formula=['AND($A4<>"",$D4<>"Done",ISNUMBER($C4),$C4<TODAY())'], fill=PatternFill("solid", fgColor="FFE3E3")))
howto(wb, C, ["1. Fill in the event, date, venue and total budget on Overview.", "2. Add guests with their RSVP and how many people each invite covers (for couples and families). Dietary needs help with catering.",
              "3. Plan costs on Budget and fill in what you actually pay. Overview shows spend, money left and cost per guest.", "4. Add tasks with a do-by date. Overdue ones turn red. Delete the sample data first."])
wb.save(OUT / "Party-Event-Planner.xlsx")

# 5. Running training log
C = "F76707"; title, header = kit(C); wb = Workbook(); lg = wb.active; lg.title = "Run log"
title(lg, "Running Log", "Log every run. Pace, weekly distance and personal bests are worked out for you.")
header(lg, ["Date", "Type", "Distance (km)", "Time (h:mm:ss)", "Pace (min/km)", "Avg HR", "Effort (1-10)", "Shoes", "Week starting", "Notes"], [12, 12, 12, 13, 13, 9, 10, 14, 13, 24])
runs = [(0, "Easy", 5.2, "0:29:40", 142, 4, "Pegasus"), (2, "Intervals", 7.0, "0:36:10", 158, 8, "Pegasus"), (4, "Easy", 6.0, "0:34:05", 145, 4, "Pegasus"), (6, "Long", 12.5, "1:12:30", 150, 6, "Trail shoes"),
        (8, "Easy", 5.0, "0:28:20", 141, 3, "Pegasus"), (10, "Tempo", 8.0, "0:40:50", 162, 7, "Pegasus"), (13, "Long", 14.0, "1:20:15", 151, 6, "Trail shoes"), (15, "Race", 5.0, "0:23:48", 172, 10, "Racers")]
start = mon - dt.timedelta(days=14)
for r, (d, t, km, tm, hr, ef, sh_) in enumerate(runs, 4):
    lg[f"A{r}"] = start + dt.timedelta(days=d); lg[f"B{r}"] = t; lg[f"C{r}"] = km; lg[f"D{r}"] = dt.time(*map(int, tm.split(":"))); lg[f"F{r}"] = hr; lg[f"G{r}"] = ef; lg[f"H{r}"] = sh_
dv(lg, '"Easy,Long,Tempo,Intervals,Hills,Race,Recovery"', "B4:B1000")
for r in range(4, 1001):
    lg[f"A{r}"].number_format = "yyyy-mm-dd"; lg[f"D{r}"].number_format = "[h]:mm:ss"; lg[f"C{r}"].number_format = "0.00"
    lg[f"E{r}"] = f'=IF(OR(N(C{r})=0,D{r}=""),"",D{r}/C{r})'; lg[f"E{r}"].number_format = "[m]:ss"
    lg[f"I{r}"] = f'=IF(A{r}="","",A{r}-WEEKDAY(A{r},3))'; lg[f"I{r}"].number_format = "dd mmm"
wk = wb.create_sheet("Weekly"); title(wk, "Weekly mileage", "12 weeks ending this week. Aim to raise weekly distance by about 10% at most.")
header(wk, ["Week starting", "Runs", "Distance (km)", "Time", "Change vs last week"], [14, 8, 14, 12, 18], freeze=False)
for i in range(12):
    r = 4 + i
    wk[f"A{r}"] = f"=TODAY()-WEEKDAY(TODAY(),3)-{(11 - i) * 7}"; wk[f"A{r}"].number_format = "dd mmm"
    wk[f"B{r}"] = f"=COUNTIF('Run log'!$I$4:$I$1000,A{r})"
    wk[f"C{r}"] = f"=SUMIF('Run log'!$I$4:$I$1000,A{r},'Run log'!$C$4:$C$1000)"; wk[f"C{r}"].number_format = "0.0"
    wk[f"D{r}"] = f"=SUMIF('Run log'!$I$4:$I$1000,A{r},'Run log'!$D$4:$D$1000)"; wk[f"D{r}"].number_format = "[h]:mm"
    wk[f"E{r}"] = "" if i == 0 else f'=IF(OR(C{r-1}=0,C{r}=0),"",C{r}/C{r-1}-1)'; wk[f"E{r}"].number_format = "+0%;-0%;0%"
wk.conditional_formatting.add("E5:E15", CellIsRule(operator="greaterThan", formula=["0.1"], font=Font(bold=True, color="C0392B")))
bc = BarChart(); bc.title = "Weekly distance (km)"; bc.height = 7; bc.width = 18; bc.legend = None
bc.add_data(Reference(wk, min_col=3, min_row=3, max_row=15), titles_from_data=True); bc.set_categories(Reference(wk, min_col=1, min_row=4, max_row=15)); wk.add_chart(bc, "G3")
pb = wb.create_sheet("PBs & shoes"); title(pb, "Personal bests", "Fastest logged time at each race distance (runs within 3% of the distance count).")
header(pb, ["Distance", "km", "Best time", "Pace"], [16, 8, 12, 10], freeze=False)
for r, (n, km) in enumerate([("5K", 5), ("10K", 10), ("Half marathon", 21.0975), ("Marathon", 42.195)], 4):
    pb[f"A{r}"] = n; pb[f"B{r}"] = km
    pb[f"C{r}"] = f"=IFERROR(1/(1/_xlfn.MINIFS('Run log'!$D$4:$D$1000,'Run log'!$C$4:$C$1000,\">=\"&B{r}*0.97,'Run log'!$C$4:$C$1000,\"<=\"&B{r}*1.03)),\"\")"
    pb[f"C{r}"].number_format = "[h]:mm:ss"; pb[f"D{r}"] = f'=IF(C{r}="","",C{r}/B{r})'; pb[f"D{r}"].number_format = "[m]:ss"
header(pb, ["Shoes", "km run", "Replace at (km)", "Left"], [16, 8, 12, 10], row=10, freeze=False)
for r, (s, lim) in enumerate([("Pegasus", 700), ("Trail shoes", 800), ("Racers", 400)], 11):
    pb[f"A{r}"] = s; pb[f"C{r}"] = lim
    pb[f"B{r}"] = f"=SUMIF('Run log'!$H$4:$H$1000,A{r},'Run log'!$C$4:$C$1000)"; pb[f"D{r}"] = f'=IF(A{r}="","",C{r}-B{r})'
    pb[f"B{r}"].number_format = pb[f"D{r}"].number_format = "0"
pb.conditional_formatting.add("D11:D20", CellIsRule(operator="lessThan", formula=["50"], font=Font(bold=True, color="C0392B")))
pb["A22"] = "Totals"; pb["A22"].font = Font(bold=True)
pb["A23"] = "Total distance (km)"; pb["B23"] = "=SUM('Run log'!C4:C1000)"; pb["A24"] = "Total runs"; pb["B24"] = "=COUNT('Run log'!C4:C1000)"; pb["A25"] = "Longest run (km)"; pb["B25"] = "=MAX('Run log'!C4:C1000)"
for c in ("B23", "B25"): pb[c].number_format = "0.0"
howto(wb, C, ["1. Log each run on Run log: date, type, distance in km and time as h:mm:ss (for example 0:29:40). Pace is worked out for you.", "2. Weekly shows your last 12 weeks of distance. A jump of more than 10% on the week before turns red, a common sign of doing too much too soon.",
              "3. PBs & shoes finds your best 5K, 10K, half and marathon times and tracks how far each pair of shoes has gone, so you know when to replace them.", "4. Prefer miles? Just enter miles and read 'km' as miles throughout (update the PB distances). Delete the sample runs first."])
wb.save(OUT / "Running-Training-Log.xlsx")
print("built 5")
