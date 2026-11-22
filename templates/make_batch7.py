"""Round 12 spreadsheet products into products/. Run: python3 make_batch7.py (reuses helpers from make_batch2.py)"""
import pathlib, random
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
today = dt.date.today(); y = today.year
mon = today - dt.timedelta(days=today.weekday())
random.seed(12)
def lab(ws, cell, text, size=None, color=None):
    ws[cell] = text; ws[cell].font = Font(bold=True, size=size, color=color)

# 1. Pocket money tracker
C = "1098AD"; title, header = kit(C); wb = Workbook(); kd = wb.active; kd.title = "Kids"
title(kd, "Kids & goals", "One row per child. Set their weekly pocket money and what they're saving for.")
header(kd, ["Name", "Weekly pocket money", "Saving for", "Goal amount"], [14, 18, 24, 13])
for r, k in enumerate([("Mia", 5, "Lego set", 60), ("Leo", 3, "Football boots", 45), ("", None, "", None)], 4):
    for c, v in enumerate(k, 1): kd.cell(r, c, v)
for r in range(4, 14): kd[f"B{r}"].number_format = kd[f"D{r}"].number_format = M
ch = wb.create_sheet("Chores"); title(ch, "Paid jobs", "Extra jobs kids can do to earn more.")
header(ch, ["Job", "Pays"], [26, 10])
for r, (j, p) in enumerate([("Wash the car", 2), ("Hoover the stairs", 1), ("Empty the dishwasher", 0.5), ("Weed the garden (30 min)", 2), ("Fold the laundry", 1), ("Walk the dog", 1)], 4):
    ch[f"A{r}"], ch[f"B{r}"] = j, p; ch[f"B{r}"].number_format = M
lg = wb.create_sheet("Money log"); title(lg, "Money log", "Every coin in and out. Spending is taken off automatically.")
header(lg, ["Date", "Child", "Type", "What for", "Amount", "+/-"], [12, 12, 14, 28, 10, 10])
types = ["Pocket money", "Paid job", "Gift", "Spent", "Bonus"]
rows = []
for w in range(6):
    d = mon - dt.timedelta(weeks=5 - w)
    rows += [(d, "Mia", "Pocket money", "Weekly", 5), (d, "Leo", "Pocket money", "Weekly", 3)]
rows += [(mon - dt.timedelta(days=30), "Mia", "Paid job", "Wash the car", 2), (mon - dt.timedelta(days=24), "Leo", "Spent", "Sweets", 1.5), (mon - dt.timedelta(days=20), "Mia", "Gift", "Grandma", 10),
         (mon - dt.timedelta(days=12), "Leo", "Paid job", "Walk the dog", 1), (mon - dt.timedelta(days=9), "Mia", "Spent", "Comic", 3.5), (mon - dt.timedelta(days=3), "Leo", "Spent", "Stickers", 2)]
rows.sort()
for r, row in enumerate(rows, 4):
    for c, v in enumerate(row, 1): lg.cell(r, c, v)
dv(lg, "=Kids!$A$4:$A$13", "B4:B1000"); dv(lg, '"' + ",".join(types) + '"', "C4:C1000")
for r in range(4, 1001):
    lg[f"A{r}"].number_format = "dd mmm yyyy"; lg[f"E{r}"].number_format = lg[f"F{r}"].number_format = M
    lg[f"F{r}"] = f'=IF(E{r}="","",IF(C{r}="Spent",-E{r},E{r}))'
lg.conditional_formatting.add("F4:F1000", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B")))
sm = wb.create_sheet("Balances", 0); title(sm, "Pocket Money Balances", "Updates from the Money log.")
header(sm, ["Child", "Pocket money", "Paid jobs", "Gifts & bonus", "Spent", "Balance", "Goal", "Progress", "Still to save", "Weeks to goal"], [12, 13, 11, 13, 10, 11, 11, 10, 12, 12], freeze=False)
for i in range(10):
    r = 4 + i; k = f"Kids!A{4 + i}"
    sm[f"A{r}"] = f'=IF({k}="","",{k})'
    sf = lambda t: f"SUMIFS('Money log'!$E$4:$E$1000,'Money log'!$B$4:$B$1000,$A{r},'Money log'!$C$4:$C$1000,\"{t}\")"
    sm[f"B{r}"] = f'=IF(A{r}="","",{sf("Pocket money")})'; sm[f"C{r}"] = f'=IF(A{r}="","",{sf("Paid job")})'
    sm[f"D{r}"] = f'=IF(A{r}="","",{sf("Gift")}+{sf("Bonus")})'; sm[f"E{r}"] = f'=IF(A{r}="","",{sf("Spent")})'
    sm[f"F{r}"] = f'=IF(A{r}="","",B{r}+C{r}+D{r}-E{r})'; sm[f"G{r}"] = f'=IF(A{r}="","",N(Kids!D{4 + i}))'
    sm[f"H{r}"] = f'=IF(OR(A{r}="",N(G{r})=0),"",MIN(1,MAX(0,F{r})/G{r}))'; sm[f"I{r}"] = f'=IF(OR(A{r}="",N(G{r})=0),"",MAX(0,G{r}-F{r}))'
    sm[f"J{r}"] = f'=IF(OR(I{r}="",N(Kids!B{4 + i})=0),"",ROUNDUP(I{r}/Kids!B{4 + i},0))'
    for c in "BCDEFGI": sm[f"{c}{r}"].number_format = M
    sm[f"H{r}"].number_format = "0%"
sm.conditional_formatting.add("H4:H13", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="3BC9DB"))
sm.conditional_formatting.add("H4:H13", CellIsRule(operator="greaterThanOrEqual", formula=["1"], font=Font(bold=True, color="2B8A3E")))
sm.conditional_formatting.add("F4:F13", CellIsRule(operator="lessThan", formula=["0"], font=Font(bold=True, color="C0392B")))
bc = BarChart(); bc.title = "Balance vs goal"; bc.height = 7; bc.width = 16
bc.add_data(Reference(sm, min_col=6, max_col=7, min_row=3, max_row=5), titles_from_data=True); bc.set_categories(Reference(sm, min_col=1, min_row=4, max_row=5)); sm.add_chart(bc, "A16")
howto(wb, C, ["1. Kids: add each child with their weekly pocket money and what they're saving for (and how much it costs).", "2. Chores: list extra paid jobs and what they pay, so everyone knows the deal.",
              "3. Money log: add a row whenever money comes in (pocket money, paid job, gift, bonus) or goes out (spent). Spending is subtracted automatically.",
              "4. Balances shows what each child has, how close they are to their goal and how many weeks of pocket money it will take. A great way to teach saving.", "5. Delete the sample rows first."])
wb.save(OUT / "Pocket-Money-Tracker.xlsx")

# 2. Fundraising & donation tracker
C = "AE3EC9"; title, header = kit(C); wb = Workbook(); st = wb.active; st.title = "Settings"
title(st, "Campaign", "Name your fundraiser and set the target.")
for r, (n, v) in enumerate([("Campaign name", "School playground appeal"), ("Target", 5000), ("Start date", today - dt.timedelta(days=90)), ("End date", today + dt.timedelta(days=60)), ("Gift Aid / match rate (0 if none)", 0.25)], 4):
    st[f"A{r}"] = n; st[f"B{r}"] = v; st[f"A{r}"].font = Font(bold=True); st[f"B{r}"].fill = SOFT
st["B5"].number_format = M; st["B6"].number_format = st["B7"].number_format = "dd mmm yyyy"; st["B8"].number_format = "0%"; st.column_dimensions["A"].width = 30; st.column_dimensions["B"].width = 26
dn = wb.create_sheet("Donations"); title(dn, "Donations", "One row per gift. Tick Gift Aid / match if it applies.")
header(dn, ["Date", "Donor", "Amount", "Method", "Gift Aid / match?", "Extra claimed", "Thanked?", "Email / note"], [12, 22, 11, 13, 14, 12, 10, 26])
names = ["A. Patel", "J. Smith", "The Green family", "Local bakery", "M. Novak", "Anonymous", "R. Okafor", "PTA bake sale", "S. Müller", "K. Brown", "Rotary club", "L. Rossi"]
for r in range(4, 22):
    dn[f"A{r}"] = today - dt.timedelta(days=random.randint(0, 85)); dn[f"B{r}"] = random.choice(names); dn[f"C{r}"] = random.choice([10, 20, 25, 50, 50, 100, 250])
    dn[f"D{r}"] = random.choice(["Online", "Cash", "Bank transfer", "Cheque"]); dn[f"E{r}"] = random.choice(["Yes", "No"]); dn[f"G{r}"] = random.choice(["Yes", "Yes", "No"])
dv(dn, '"Online,Cash,Bank transfer,Cheque,Card"', "D4:D2000"); dv(dn, '"Yes,No"', "E4:E2000"); dv(dn, '"Yes,No"', "G4:G2000")
for r in range(4, 2001):
    dn[f"A{r}"].number_format = "dd mmm yyyy"; dn[f"C{r}"].number_format = dn[f"F{r}"].number_format = M
    dn[f"F{r}"] = f'=IF(AND(C{r}<>"",E{r}="Yes"),C{r}*Settings!$B$8,"")'
dn.conditional_formatting.add("G4:G2000", CellIsRule(operator="equal", formula=['"No"'], fill=PatternFill("solid", fgColor="FFE3E3")))
ev = wb.create_sheet("Events"); title(ev, "Fundraising events", "Track what each event cost and raised.")
header(ev, ["Event", "Date", "Income", "Costs", "Net raised", "Volunteers", "Notes"], [24, 12, 11, 11, 12, 11, 26])
for r, e in enumerate([("Bake sale", -60, 420, 65, 8), ("Quiz night", -30, 960, 180, 6), ("Sponsored walk", 14, None, None, 12)], 4):
    ev[f"A{r}"], ev[f"B{r}"], ev[f"C{r}"], ev[f"D{r}"], ev[f"F{r}"] = e[0], today + dt.timedelta(days=e[1]), e[2], e[3], e[4]
for r in range(4, 54):
    ev[f"B{r}"].number_format = "dd mmm"; ev[f"E{r}"] = f'=IF(A{r}="","",N(C{r})-N(D{r}))'
    for c in "CDE": ev[f"{c}{r}"].number_format = M
db = wb.create_sheet("Dashboard", 0); db["A1"] = "=Settings!B4"; db["A1"].font = Font(bold=True, size=18, color=C); db["A2"] = "Fundraising dashboard. Updates from Donations and Events."; db["A2"].font = Font(italic=True, color="777777")
kp = [("Donations", "=SUM(Donations!C4:C2000)", M), ("Gift Aid / match claimed", "=SUM(Donations!F4:F2000)", M), ("Net from events", "=SUM(Events!E4:E53)", M), ("Total raised", "=SUM(B4:B6)", M), ("Target", "=Settings!B5", M),
      ("Progress", "=IFERROR(B7/B8,0)", "0%"), ("Still to raise", "=MAX(0,B8-B7)", M), ("Days left", "=MAX(0,Settings!B7-TODAY())", "0"), ("Needed per day", "=IFERROR(B10/B11,0)", M),
      ("Number of gifts", "=COUNT(Donations!C4:C2000)", "0"), ("Average gift", "=IFERROR(B4/B13,0)", M), ("Largest gift", "=MAX(Donations!C4:C2000)", M), ("Thank-yous to send", '=COUNTIFS(Donations!C4:C2000,"<>",Donations!G4:G2000,"<>Yes")', "0")]
for r, (a, f, nf_) in enumerate(kp, 4):
    db[f"A{r}"] = a; db[f"B{r}"] = f; db[f"B{r}"].number_format = nf_; db[f"A{r}"].font = Font(bold=True); db[f"B{r}"].fill = SOFT
db["B7"].font = Font(bold=True, size=13, color=C); db.column_dimensions["A"].width = 26; db.column_dimensions["B"].width = 14
db.conditional_formatting.add("B9", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="DA77F2"))
db.conditional_formatting.add("B16", CellIsRule(operator="greaterThan", formula=["0"], font=Font(bold=True, color="C0392B")))
header(db, ["Month", "Donations"], [26, 14], row=19, freeze=False)
for i in range(6):
    r = 20 + i
    db[f"A{r}"] = f"=EDATE(DATE(YEAR(TODAY()),MONTH(TODAY()),1),{i - 5})"; db[f"A{r}"].number_format = "mmm yyyy"
    db[f"B{r}"] = f'=SUMIFS(Donations!$C$4:$C$2000,Donations!$A$4:$A$2000,">="&A{r},Donations!$A$4:$A$2000,"<"&EDATE(A{r},1))'; db[f"B{r}"].number_format = M
bc = BarChart(); bc.title = "Donations by month"; bc.height = 7; bc.width = 16; bc.legend = None
bc.add_data(Reference(db, min_col=2, min_row=19, max_row=25), titles_from_data=True); bc.set_categories(Reference(db, min_col=1, min_row=20, max_row=25)); db.add_chart(bc, "D3")
howto(wb, C, ["1. Settings: name the campaign, set the target, start and end dates, and a Gift Aid or employer match rate if you can claim one (use 0 if not).",
              "2. Donations: one row per gift. Mark Gift Aid / match and whether you've said thank you. Unthanked gifts are highlighted.",
              "3. Events: record income and costs for each event to see what it really raised.", "4. Dashboard: total raised, progress to target, how much you need per day, average and largest gift, thank-yous to send and a monthly chart.",
              "5. Great for schools, clubs, charities, church groups and personal fundraisers. Delete the sample rows first."])
wb.save(OUT / "Fundraising-Donation-Tracker.xlsx")

# 3. Recipe cost calculator
C = "D9480F"; title, header = kit(C); wb = Workbook(); ig = wb.active; ig.title = "Ingredients"
title(ig, "Ingredients", "What you pay for each ingredient. Cost per gram, ml or item is worked out for you.")
header(ig, ["Ingredient", "Pack size", "Unit", "Pack price", "Cost per unit", "Supplier"], [24, 10, 8, 11, 13, 16])
ing = [("Plain flour", 1500, "g", 1.2), ("Caster sugar", 1000, "g", 1.1), ("Butter", 250, "g", 2.4), ("Eggs", 12, "each", 3.3), ("Milk", 1000, "ml", 0.95), ("Cocoa powder", 250, "g", 3.2), ("Vanilla extract", 38, "ml", 2.6),
       ("Icing sugar", 1000, "g", 1.6), ("Baking powder", 170, "g", 1.1), ("Chocolate chips", 200, "g", 1.8), ("Cupcake cases", 100, "each", 1.5), ("Gift box", 25, "each", 9.0)]
for r, x in enumerate(ing, 4):
    for c, v in enumerate(x, 1): ig.cell(r, c, v)
dv(ig, '"g,kg,ml,l,each"', "C4:C203")
for r in range(4, 204):
    ig[f"D{r}"].number_format = M; ig[f"E{r}"] = f'=IF(OR(A{r}="",N(B{r})=0),"",D{r}/B{r})'; ig[f"E{r}"].number_format = "0.0000"
rc = wb.create_sheet("Recipe", 0); title(rc, "Recipe Cost Calculator", "Pick ingredients and amounts. The cost per batch and per portion, and a selling price, are worked out for you.")
for r, (a, v) in enumerate([("Recipe", "Chocolate cupcakes"), ("Portions per batch", 12), ("Packaging per portion", 0), ("Labour minutes per batch", 45), ("Your hourly rate", 12), ("Overheads (energy etc) per batch", 0.8)], 3):
    rc[f"A{r}"] = a; rc[f"B{r}"] = v; rc[f"A{r}"].font = Font(bold=True); rc[f"B{r}"].fill = SOFT
for c in ("B5", "B7", "B8"): rc[c].number_format = M
header(rc, ["Ingredient", "Amount used", "Unit", "Cost"], [30, 13, 8, 11], row=10, freeze=False)
for r, (n, q) in enumerate([("Plain flour", 200), ("Caster sugar", 200), ("Butter", 150), ("Eggs", 3), ("Milk", 120), ("Cocoa powder", 40), ("Vanilla extract", 5), ("Icing sugar", 250), ("Baking powder", 8), ("Cupcake cases", 12)], 11):
    rc[f"A{r}"], rc[f"B{r}"] = n, q
dv(rc, "=Ingredients!$A$4:$A$203", "A11:A35")
for r in range(11, 36):
    rc[f"C{r}"] = f'=IF(A{r}="","",IFERROR(INDEX(Ingredients!$C$4:$C$203,MATCH(A{r},Ingredients!$A$4:$A$203,0)),"?"))'
    rc[f"D{r}"] = f'=IF(A{r}="","",IFERROR(B{r}*INDEX(Ingredients!$E$4:$E$203,MATCH(A{r},Ingredients!$A$4:$A$203,0)),0))'; rc[f"D{r}"].number_format = M
lab(rc, "F3", "Cost breakdown", 12, C); rc.column_dimensions["F"].width = 30; rc.column_dimensions["G"].width = 13
rows = [("Ingredients per batch", "=SUM(D11:D35)"), ("Packaging per batch", "=B5*B4"), ("Labour per batch", "=B6/60*B7"), ("Overheads per batch", "=B8"), ("Total cost per batch", "=SUM(G4:G7)"),
        ("Cost per portion", "=IFERROR(G8/B4,0)"), ("Ingredient cost per portion", "=IFERROR(G4/B4,0)")]
for r, (a, f) in enumerate(rows, 4):
    rc[f"F{r}"] = a; rc[f"G{r}"] = f; rc[f"G{r}"].number_format = M
for c in ("F8", "G8", "F9", "G9"): rc[c].font = Font(bold=True)
lab(rc, "F13", "Suggested price per portion", 12, C)
for c, h in zip("FGHI", ["Profit margin", "Price", "Profit each", "Batch profit"]):
    rc[f"{c}14"] = h; rc[f"{c}14"].font = Font(bold=True, color="FFFFFF"); rc[f"{c}14"].fill = PatternFill("solid", fgColor=C)
rc.column_dimensions["H"].width = 12; rc.column_dimensions["I"].width = 12
for r, mg in enumerate([0.3, 0.4, 0.5, 0.6, 0.7], 15):
    rc[f"F{r}"] = mg; rc[f"F{r}"].number_format = "0%"; rc[f"G{r}"] = f"=IFERROR($G$9/(1-F{r}),0)"; rc[f"H{r}"] = f"=G{r}-$G$9"; rc[f"I{r}"] = f"=H{r}*$B$4"
    for c in "GHI": rc[f"{c}{r}"].number_format = M
rc["F21"] = "Your actual price"; rc["G21"] = 2.5; rc["G21"].fill = SOFT; rc["G21"].number_format = M; rc["F21"].font = Font(bold=True)
rc["F22"] = "Your margin"; rc["G22"] = "=IFERROR((G21-G9)/G21,0)"; rc["G22"].number_format = "0%"
rc["F23"] = "Profit per batch"; rc["G23"] = "=(G21-G9)*B4"; rc["G23"].number_format = M
rc.conditional_formatting.add("G22", CellIsRule(operator="lessThan", formula=["0.3"], font=Font(bold=True, color="C0392B")))
rc.conditional_formatting.add("D11:D35", DataBarRule(start_type="num", start_value=0, end_type="max", color="FFA94D"))
ps = wb.create_sheet("Price list", 1); title(ps, "Price list", "Copy the cost per portion of each recipe here to compare products.")
header(ps, ["Product", "Cost per portion", "Price", "Margin", "Profit each"], [26, 15, 11, 10, 12])
for r, (n, cst, p) in enumerate([("Chocolate cupcakes", "=Recipe!G9", 2.5), ("Lemon drizzle slice", 0.62, 2.2), ("Brownie", 0.71, 2.5), ("Celebration cake (12 slices)", 9.4, 32)], 4):
    ps[f"A{r}"], ps[f"B{r}"], ps[f"C{r}"] = n, cst, p
for r in range(4, 54):
    ps[f"D{r}"] = f'=IF(OR(A{r}="",N(C{r})=0),"",(C{r}-B{r})/C{r})'; ps[f"E{r}"] = f'=IF(A{r}="","",C{r}-B{r})'
    for c in "BCE": ps[f"{c}{r}"].number_format = M
    ps[f"D{r}"].number_format = "0%"
ps.conditional_formatting.add("D4:D53", CellIsRule(operator="lessThan", formula=["0.3"], font=Font(bold=True, color="C0392B")))
howto(wb, C, ["1. Ingredients: enter each ingredient with the pack size, unit (g, ml or each) and what you paid. The cost per unit is worked out for you.",
              "2. Recipe: name the recipe, set portions, packaging, labour time, your hourly rate and overheads. Pick ingredients and amounts in the same unit as the Ingredients tab.",
              "3. You'll see the total batch cost, the cost per portion and suggested prices for different profit margins. Type your actual price to check your margin.",
              "4. For more recipes, right-click the Recipe tab and duplicate it. Copy each cost per portion into the Price list to compare products. Margins under 30% turn red.",
              "5. Great for home bakers, cafés, market stalls and caterers. Delete the sample data first."])
wb.save(OUT / "Recipe-Cost-Calculator.xlsx")

# 4. Strength training progress tracker
C = "343A40"; title, header = kit(C); wb = Workbook(); ex = wb.active; ex.title = "Exercises"
title(ex, "Exercises", "Your exercise list. Add any you like.")
header(ex, ["Exercise", "Muscle group", "Goal weight"], [24, 16, 12])
exs = [("Squat", "Legs", 120), ("Bench press", "Chest", 90), ("Deadlift", "Back", 150), ("Overhead press", "Shoulders", 60), ("Barbell row", "Back", 80), ("Pull-up (added kg)", "Back", 20), ("Romanian deadlift", "Legs", 100), ("Incline dumbbell press", "Chest", 30)]
for r, e in enumerate(exs, 4):
    for c, v in enumerate(e, 1): ex.cell(r, c, v)
lg = wb.create_sheet("Workout log"); title(lg, "Workout log", "One row per exercise per session. Estimated 1-rep max and volume are worked out for you.")
header(lg, ["Date", "Exercise", "Weight (kg)", "Reps", "Sets", "RPE (1-10)", "Est. 1RM", "Volume", "Week starting", "Notes"], [12, 22, 11, 7, 7, 10, 10, 10, 13, 22])
base = {"Squat": 80, "Bench press": 62.5, "Deadlift": 105, "Overhead press": 40, "Barbell row": 55}
r = 4
for w in range(12):
    for d, lifts in [(0, ["Squat", "Bench press", "Barbell row"]), (2, ["Deadlift", "Overhead press"]), (4, ["Squat", "Bench press"])]:
        for lft in lifts:
            lg[f"A{r}"] = mon - dt.timedelta(weeks=11 - w) + dt.timedelta(days=d); lg[f"B{r}"] = lft
            lg[f"C{r}"] = base[lft] + w * (2.5 if lft != "Overhead press" else 1.25); lg[f"D{r}"] = 5; lg[f"E{r}"] = 3 if lft != "Deadlift" else 1; lg[f"F{r}"] = 7 + (w % 3)
            r += 1
dv(lg, "=Exercises!$A$4:$A$53", "B4:B3000")
for r in range(4, 3001):
    lg[f"A{r}"].number_format = "dd mmm yy"; lg[f"C{r}"].number_format = "0.0"
    lg[f"G{r}"] = f'=IF(OR(N(C{r})=0,N(D{r})=0),"",IF(D{r}=1,C{r},C{r}*(1+D{r}/30)))'; lg[f"G{r}"].number_format = "0.0"
    lg[f"H{r}"] = f'=IF(B{r}="","",N(C{r})*N(D{r})*MAX(1,N(E{r})))'; lg[f"H{r}"].number_format = "#,##0"
    lg[f"I{r}"] = f'=IF(A{r}="","",A{r}-WEEKDAY(A{r},3))'; lg[f"I{r}"].number_format = "dd mmm"
pr = wb.create_sheet("Progress", 0); title(pr, "Strength Progress", "Personal records and progress for every exercise, from the Workout log.")
header(pr, ["Exercise", "Best est. 1RM", "Heaviest weight", "Goal", "To goal", "Sessions", "Last trained", "Total volume"], [24, 13, 14, 10, 10, 10, 13, 13], freeze=False)
W = "'Workout log'!"
for i in range(15):
    r = 4 + i; e = f"Exercises!A{4 + i}"
    pr[f"A{r}"] = f'=IF({e}="","",{e})'
    pr[f"B{r}"] = f'=IF(A{r}="","",IFERROR(1/(1/_xlfn.MAXIFS({W}$G$4:$G$3000,{W}$B$4:$B$3000,A{r})),""))'
    pr[f"C{r}"] = f'=IF(A{r}="","",IFERROR(1/(1/_xlfn.MAXIFS({W}$C$4:$C$3000,{W}$B$4:$B$3000,A{r})),""))'
    pr[f"D{r}"] = f'=IF(A{r}="","",IF(Exercises!C{4 + i}="","",Exercises!C{4 + i}))'
    pr[f"E{r}"] = f'=IF(OR(C{r}="",D{r}=""),"",MAX(0,D{r}-C{r}))'
    pr[f"F{r}"] = f'=IF(A{r}="","",COUNTIF({W}$B$4:$B$3000,A{r}))'
    pr[f"G{r}"] = f'=IF(OR(A{r}="",F{r}=0),"",_xlfn.MAXIFS({W}$A$4:$A$3000,{W}$B$4:$B$3000,A{r}))'; pr[f"G{r}"].number_format = "dd mmm yy"
    pr[f"H{r}"] = f'=IF(A{r}="","",SUMIF({W}$B$4:$B$3000,A{r},{W}$H$4:$H$3000))'; pr[f"H{r}"].number_format = "#,##0"
    for c in "BCDE": pr[f"{c}{r}"].number_format = "0.0"
pr.conditional_formatting.add("E4:E18", CellIsRule(operator="equal", formula=["0"], fill=PatternFill("solid", fgColor="B2F2BB")))
pr.conditional_formatting.add("G4:G18", FormulaRule(formula=['AND(G4<>"",TODAY()-G4>14)'], font=Font(color="C0392B")))
header(pr, ["Week starting", "Sessions", "Volume (kg)"] + [x[0] for x in exs[:4]], [24, 13, 14, 10, 10, 10, 13], row=21, freeze=False)
pr["H21"].value = None
for i in range(12):
    r = 22 + i
    pr[f"A{r}"] = f"=TODAY()-WEEKDAY(TODAY(),3)-{(11 - i) * 7}"; pr[f"A{r}"].number_format = "dd mmm"
    pr[f"B{r}"] = f'=SUMPRODUCT(({W}$I$4:$I$3000=A{r})/COUNTIFS({W}$A$4:$A$3000,{W}$A$4:$A$3000&"",{W}$I$4:$I$3000,{W}$I$4:$I$3000&""))'
    pr[f"C{r}"] = f"=SUMIF({W}$I$4:$I$3000,A{r},{W}$H$4:$H$3000)"; pr[f"C{r}"].number_format = "#,##0"
    for j in range(4):
        cl = L(4 + j)
        pr[f"{cl}{r}"] = f'=IFERROR(1/(1/_xlfn.MAXIFS({W}$G$4:$G$3000,{W}$B$4:$B$3000,{cl}$21,{W}$I$4:$I$3000,$A{r})),"")'; pr[f"{cl}{r}"].number_format = "0.0"
lc = LineChart(); lc.title = "Estimated 1RM by week"; lc.height = 8; lc.width = 20
lc.add_data(Reference(pr, min_col=4, max_col=7, min_row=21, max_row=33), titles_from_data=True); lc.set_categories(Reference(pr, min_col=1, min_row=22, max_row=33)); pr.add_chart(lc, "J3")
bc = BarChart(); bc.title = "Weekly volume (kg)"; bc.height = 7; bc.width = 20; bc.legend = None
bc.add_data(Reference(pr, min_col=3, min_row=21, max_row=33), titles_from_data=True); bc.set_categories(Reference(pr, min_col=1, min_row=22, max_row=33)); pr.add_chart(bc, "J21")
howto(wb, C, ["1. Exercises: list your lifts and an optional goal weight. The first four appear in the weekly 1RM chart, so put your main lifts at the top.",
              "2. Workout log: one row per exercise per session with weight, reps and sets (all sets at that weight). Estimated 1-rep max (Epley formula) and volume are worked out for you.",
              "3. Progress: best estimated 1RM, heaviest weight, distance to goal, sessions and the last time you trained each lift (red after 14 days), plus weekly sessions, volume and charts.",
              "4. Prefer pounds? Enter lb and read kg as lb. Delete the sample workouts first."])
wb.save(OUT / "Strength-Training-Progress-Tracker.xlsx")

# 5. Exam revision planner
C = "1971C2"; title, header = kit(C); wb = Workbook(); exm = wb.active; exm.title = "Exams"
title(exm, "Exam countdown", "List every exam. Days left and your readiness update automatically.")
header(exm, ["Subject", "Paper", "Date", "Time", "Days left", "Topics", "Green topics", "Ready %"], [16, 22, 12, 8, 10, 9, 12, 10])
subs = ["Maths", "English", "Biology", "Chemistry", "History", "French"]
for r, (s, p, d, t) in enumerate([("Maths", "Paper 1 (non-calculator)", 40, "09:00"), ("Maths", "Paper 2 (calculator)", 47, "09:00"), ("English", "Literature", 42, "13:30"), ("Biology", "Paper 1", 44, "09:00"), ("Chemistry", "Paper 1", 49, "13:30"), ("History", "Paper 1", 51, "09:00"), ("French", "Speaking", 30, "10:15")], 4):
    exm[f"A{r}"], exm[f"B{r}"], exm[f"C{r}"], exm[f"D{r}"] = s, p, today + dt.timedelta(days=d), dt.time(*map(int, t.split(":")))
dv(exm, "=Subjects!$A$4:$A$23", "A4:A60")
for r in range(4, 61):
    exm[f"C{r}"].number_format = "ddd dd mmm"; exm[f"D{r}"].number_format = "hh:mm"
    exm[f"E{r}"] = f'=IF(C{r}="","",C{r}-TODAY())'
    exm[f"F{r}"] = f'=IF(A{r}="","",COUNTIF(Topics!$A$4:$A$1000,A{r}))'
    exm[f"G{r}"] = f'=IF(A{r}="","",COUNTIFS(Topics!$A$4:$A$1000,A{r},Topics!$C$4:$C$1000,"Green"))'
    exm[f"H{r}"] = f'=IF(OR(A{r}="",N(F{r})=0),"",G{r}/F{r})'; exm[f"H{r}"].number_format = "0%"
exm.conditional_formatting.add("E4:E60", CellIsRule(operator="between", formula=["0", "7"], font=Font(bold=True, color="C0392B")))
exm.conditional_formatting.add("H4:H60", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="74C0FC"))
sb = wb.create_sheet("Subjects"); title(sb, "Subjects", "Your subjects, used in the drop-downs.")
header(sb, ["Subject", "Planned hours this week", "Topics", "Red", "Amber", "Green"], [16, 20, 9, 8, 8, 8])
for i in range(20):
    r = 4 + i
    if i < len(subs): sb[f"A{r}"] = subs[i]
    sb[f"B{r}"] = f'=IF(A{r}="","",COUNTIF(Timetable!$B$5:$H$16,A{r})*Timetable!$K$4)'
    sb[f"C{r}"] = f'=IF(A{r}="","",COUNTIF(Topics!$A$4:$A$1000,A{r}))'
    for c, s in zip("DEF", ["Red", "Amber", "Green"]): sb[f"{c}{r}"] = f'=IF(A{r}="","",COUNTIFS(Topics!$A$4:$A$1000,A{r},Topics!$C$4:$C$1000,"{s}"))'
bc = BarChart(); bc.type = "bar"; bc.grouping = "stacked"; bc.overlap = 100; bc.title = "Topics by confidence"; bc.height = 8; bc.width = 16
bc.add_data(Reference(sb, min_col=4, max_col=6, min_row=3, max_row=9), titles_from_data=True); bc.set_categories(Reference(sb, min_col=1, min_row=4, max_row=9)); sb.add_chart(bc, "H3")
tp = wb.create_sheet("Topics"); title(tp, "Topic checklist", "Rate every topic Red (don't get it), Amber (getting there) or Green (confident).")
header(tp, ["Subject", "Topic", "Confidence", "Times revised", "Last revised", "Past paper done?", "Notes"], [16, 32, 12, 13, 13, 15, 26])
topics = {"Maths": ["Algebra & equations", "Quadratics", "Trigonometry", "Probability", "Ratio & proportion", "Graphs"], "English": ["Macbeth", "A Christmas Carol", "Poetry anthology", "Unseen poetry"],
          "Biology": ["Cells", "Organisation", "Infection & response", "Bioenergetics"], "Chemistry": ["Atomic structure", "Bonding", "Quantitative chemistry", "Chemical changes"],
          "History": ["Medicine through time", "Weimar Germany", "Cold War"], "French": ["Speaking: family", "Speaking: holidays", "Vocab: school"]}
r = 4
for s, ts in topics.items():
    for t in ts:
        tp[f"A{r}"], tp[f"B{r}"], tp[f"C{r}"] = s, t, random.choice(["Red", "Amber", "Amber", "Green", "Green"])
        tp[f"D{r}"] = random.randint(0, 4); tp[f"E{r}"] = today - dt.timedelta(days=random.randint(1, 20)) if tp[f"D{r}"].value else None; tp[f"F{r}"] = random.choice(["Yes", "No"])
        r += 1
dv(tp, "=Subjects!$A$4:$A$23", "A4:A1000"); dv(tp, '"Red,Amber,Green"', "C4:C1000"); dv(tp, '"Yes,No"', "F4:F1000")
for rr in range(4, 1001): tp[f"E{rr}"].number_format = "dd mmm"
for s, col in [("Red", "FFC9C9"), ("Amber", "FFE8CC"), ("Green", "B2F2BB")]:
    tp.conditional_formatting.add("C4:C1000", CellIsRule(operator="equal", formula=[f'"{s}"'], fill=PatternFill("solid", fgColor=col)))
tt = wb.create_sheet("Timetable", 1); title(tt, "Weekly Revision Timetable", "Pick a subject for each session. Hours per subject show on the Subjects tab.")
tt["J4"] = "Hours per session"; tt["K4"] = 0.75; tt["J4"].font = Font(bold=True); tt["K4"].fill = SOFT; tt.column_dimensions["J"].width = 18
for i, h in enumerate(["Session"] + ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], 1):
    x = tt.cell(4, i, h); x.fill = PatternFill("solid", fgColor=C); x.font = Font(bold=True, color="FFFFFF"); x.alignment = Alignment(horizontal="center")
    tt.column_dimensions[L(i)].width = 13 if i > 1 else 12
slots = ["09:00", "10:00", "11:15", "12:15", "14:00", "15:00", "16:15", "17:15", "19:00", "20:00", "", ""]
plan = ["Maths", "Biology", "English", "Chemistry", "History", "French", "Maths"]
for i, s in enumerate(slots):
    r = 5 + i; tt[f"A{r}"] = s; tt[f"A{r}"].font = Font(bold=True)
    for d in range(7):
        if i < 8 and (d < 5 and i >= 4 or d >= 5 and i < 4) and (i + d) % 3 != 0: tt.cell(r, 2 + d, plan[(i + d) % 7])
        tt.cell(r, 2 + d).alignment = Alignment(horizontal="center"); tt.row_dimensions[r].height = 22
dv(tt, "=Subjects!$A$4:$A$23", "B5:H16")
pal = ["D0EBFF", "FFE8CC", "D3F9D8", "E5DBFF", "FFF3BF", "FFDEEB"]
for s, col in zip(subs, pal):
    tt.conditional_formatting.add("B5:H16", CellIsRule(operator="equal", formula=[f'"{s}"'], fill=PatternFill("solid", fgColor=col)))
tt["A18"] = "Total sessions"; tt["A18"].font = Font(bold=True)
for d in range(7): tt.cell(18, 2 + d, f"=COUNTA({L(2 + d)}5:{L(2 + d)}16)").alignment = Alignment(horizontal="center")
tt["A19"] = "Total hours this week"; tt["A19"].font = Font(bold=True); tt["B19"] = "=SUM(B18:H18)*K4"; tt["B19"].number_format = "0.0"
howto(wb, C, ["1. Subjects: list your subjects first. They feed the drop-downs everywhere else.", "2. Exams: add every paper with date and time. Days left counts down and turns red in the final week. Ready % comes from your Green topics.",
              "3. Topics: list the topics for each subject and rate them Red, Amber or Green. Update as you revise and focus on the reds first.",
              "4. Timetable: pick a subject for each study session. Set how long a session is (0.75 = 45 minutes). The Subjects tab shows planned hours and a confidence chart.",
              "5. Delete the sample exams, topics and timetable first. Good luck!"])
wb.save(OUT / "Exam-Revision-Planner.xlsx")
print("built 5")
