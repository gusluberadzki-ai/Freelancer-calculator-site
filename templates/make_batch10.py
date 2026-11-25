"""Round 15 spreadsheet products into products/. Run: python3 make_batch10.py (reuses helpers from make_batch2.py)"""
import pathlib, random
_src = (pathlib.Path(__file__).parent / "make_batch2.py").read_text()
exec(_src[:_src.index("# 1. Small business bookkeeping")])
today = dt.date.today(); y = today.year
random.seed(15)
def kpis(ws, rows, start=4, wa=28, wb_=14):
    for r, (a, f, nf_) in enumerate(rows, start):
        ws[f"A{r}"] = a; ws[f"B{r}"] = f; ws[f"B{r}"].number_format = nf_; ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
    ws.column_dimensions["A"].width = wa; ws.column_dimensions["B"].width = wb_
def settings(ws, rows, start=4, fmt=None):
    for r, (n, v, f) in enumerate(rows, start):
        ws[f"A{r}"] = n; ws[f"B{r}"] = v; ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
        if f: ws[f"B{r}"].number_format = f

# 1. Handmade shop fee & profit calculator
C = "D9480F"; title, header = kit(C); wb = Workbook(); st = wb.active; st.title = "Fees"
title(st, "Marketplace fees", "Set these to your marketplace's current fees. Defaults are examples only; check them before relying on the numbers.")
settings(st, [("Transaction fee (% of item + shipping)", 0.065, "0.0%"), ("Payment processing (%)", 0.04, "0.0%"), ("Payment processing (fixed per order)", 0.30, M),
              ("Listing fee per sale", 0.20, M), ("Offsite ads fee (% when an order comes from ads)", 0.15, "0%"), ("Your hourly rate", 15, M), ("Target profit margin", 0.30, "0%")])
st.column_dimensions["A"].width = 46; st.column_dimensions["B"].width = 12
pr = wb.create_sheet("Products", 0); title(pr, "Product costs & pricing", "Cost each product once. Profit per sale and a suggested price for your target margin are worked out.")
header(pr, ["Product", "Materials", "Packaging", "Make time (mins)", "Labour", "Unit cost", "Your price", "Shipping charged", "Postage cost", "Fees per sale", "Profit per sale", "Margin", "Suggested price"],
       [24, 11, 11, 11, 10, 10, 11, 11, 11, 11, 12, 9, 12])
items = [("Beaded bracelet", 3.20, 0.60, 25, 18, 3.5, 3.2), ("Scented candle", 4.10, 1.20, 20, 22, 4.5, 4.9), ("Linocut print A4", 1.80, 0.90, 15, 16, 2.5, 2.1), ("Knitted beanie", 6.50, 0.80, 120, 38, 4, 3.6),
         ("Ceramic mug", 5.00, 1.50, 45, 30, 5.5, 6.2), ("Greeting card", 0.45, 0.20, 5, 4.5, 1.5, 1.1)]
for r, (n, m, pk, mins, p, sh, po) in enumerate(items, 4):
    pr[f"A{r}"], pr[f"B{r}"], pr[f"C{r}"], pr[f"D{r}"], pr[f"G{r}"], pr[f"H{r}"], pr[f"I{r}"] = n, m, pk, mins, p, sh, po
for r in range(4, 204):
    pr[f"E{r}"] = f'=IF(A{r}="","",N(D{r})/60*Fees!$B$9)'
    pr[f"F{r}"] = f'=IF(A{r}="","",N(B{r})+N(C{r})+E{r})'
    pr[f"J{r}"] = f'=IF(A{r}="","",(N(G{r})+N(H{r}))*(Fees!$B$4+Fees!$B$5)+Fees!$B$6+Fees!$B$7)'
    pr[f"K{r}"] = f'=IF(A{r}="","",N(G{r})+N(H{r})-J{r}-F{r}-N(I{r}))'
    pr[f"L{r}"] = f'=IF(OR(A{r}="",N(G{r})=0),"",K{r}/G{r})'
    pr[f"M{r}"] = f'=IF(A{r}="","",IFERROR(MAX(0,(F{r}+N(I{r})-N(H{r})*(1-Fees!$B$4-Fees!$B$5)+Fees!$B$6+Fees!$B$7)/(1-Fees!$B$4-Fees!$B$5-Fees!$B$10)),""))'
    for c in "BCEFGHIJKM": pr[f"{c}{r}"].number_format = M
    pr[f"L{r}"].number_format = "0%"
pr.conditional_formatting.add("K4:K203", CellIsRule(operator="lessThan", formula=["0"], font=Font(bold=True, color="C0392B")))
pr.conditional_formatting.add("L4:L203", FormulaRule(formula=['AND(ISNUMBER(L4),L4<Fees!$B$10)'], fill=PatternFill("solid", fgColor="FFE8CC")))
od = wb.create_sheet("Orders", 1); title(od, "Orders", "One row per order line. Pick the product and the fees, costs and profit fill in.")
header(od, ["Date", "Product", "Qty", "Price each", "Shipping charged", "Postage paid", "From offsite ad?", "Revenue", "Fees", "Product cost", "Profit"], [11, 24, 6, 11, 11, 11, 11, 11, 10, 11, 11])
d = dt.date(y, 1, 4); r = 4
while d < dt.date(y, 12, 15):
    it = random.choice(items); q = random.choice([1, 1, 1, 2, 3])
    od[f"A{r}"] = d; od[f"B{r}"] = it[0]; od[f"C{r}"] = q; od[f"D{r}"] = it[4]; od[f"E{r}"] = it[5]; od[f"F{r}"] = it[6]; od[f"G{r}"] = "Yes" if random.random() < 0.12 else "No"
    d += dt.timedelta(days=random.choice([1, 2, 3, 4, 6])) if d.month not in (11, 12) else dt.timedelta(days=1); r += 1
dv(od, "=Products!$A$4:$A$203", "B4:B3000"); dv(od, '"Yes,No"', "G4:G3000")
for r in range(4, 3001):
    od[f"A{r}"].number_format = "dd mmm yy"
    od[f"H{r}"] = f'=IF(B{r}="","",N(C{r})*N(D{r})+N(E{r}))'
    od[f"I{r}"] = f'=IF(B{r}="","",H{r}*(Fees!$B$4+Fees!$B$5+IF(G{r}="Yes",Fees!$B$8,0))+Fees!$B$6+Fees!$B$7*MAX(1,N(C{r})))'
    od[f"J{r}"] = f'=IF(B{r}="","",N(C{r})*IFERROR(VLOOKUP(B{r},Products!$A$4:$F$203,6,FALSE),0))'
    od[f"K{r}"] = f'=IF(B{r}="","",H{r}-I{r}-J{r}-N(F{r}))'
    for c in "DEFHIJK": od[f"{c}{r}"].number_format = M
od.conditional_formatting.add("K4:K3000", CellIsRule(operator="lessThan", formula=["0"], font=Font(bold=True, color="C0392B")))
db = wb.create_sheet("Dashboard", 0); title(db, "Shop Dashboard", "Pick a year. Everything below updates from the Orders tab.")
db["A3"] = "Year"; db["B3"] = y; db["B3"].fill = SOFT; db["A3"].font = Font(bold=True)
Y = 'Orders!$A$4:$A$3000,">="&DATE($B$3,1,1),Orders!$A$4:$A$3000,"<"&DATE($B$3+1,1,1)'
kpis(db, [("Orders", f"=COUNTIFS({Y})", "0"), ("Items sold", f"=SUMIFS(Orders!$C$4:$C$3000,{Y})", "0"), ("Revenue", f"=SUMIFS(Orders!$H$4:$H$3000,{Y})", M), ("Fees paid", f"=SUMIFS(Orders!$I$4:$I$3000,{Y})", M),
          ("Product costs", f"=SUMIFS(Orders!$J$4:$J$3000,{Y})", M), ("Postage", f"=SUMIFS(Orders!$F$4:$F$3000,{Y})", M), ("Profit", f"=SUMIFS(Orders!$K$4:$K$3000,{Y})", M),
          ("Profit margin", "=IFERROR(B10/B6,0)", "0%"), ("Fees as % of revenue", "=IFERROR(B7/B6,0)", "0%"), ("Average order value", "=IFERROR(B6/B4,0)", M)], start=4)
db["B10"].font = Font(bold=True, size=13, color=C)
header(db, ["Month", "Revenue", "Fees", "Profit"], [28, 14, 11, 12], row=16, freeze=False)
for i, m in enumerate(MONTHS):
    r = 17 + i; db[f"A{r}"] = m
    cond = f'Orders!$A$4:$A$3000,">="&DATE($B$3,{i + 1},1),Orders!$A$4:$A$3000,"<"&DATE($B$3,{i + 2},1)'
    for c, src in (("B", "H"), ("C", "I"), ("D", "K")): db[f"{c}{r}"] = f"=SUMIFS(Orders!${src}$4:${src}$3000,{cond})"; db[f"{c}{r}"].number_format = M
header(db, ["Best sellers", "Sold", "Profit"], [28, 14, 11], row=31, freeze=False)
for i in range(6):
    r = 32 + i; db[f"A{r}"] = f'=IF(Products!A{4 + i}="","",Products!A{4 + i})'
    db[f"B{r}"] = f'=IF(A{r}="","",SUMIFS(Orders!$C$4:$C$3000,Orders!$B$4:$B$3000,A{r},{Y}))'; db[f"C{r}"] = f'=IF(A{r}="","",SUMIFS(Orders!$K$4:$K$3000,Orders!$B$4:$B$3000,A{r},{Y}))'; db[f"C{r}"].number_format = M
bc = BarChart(); bc.title = "Revenue & profit by month"; bc.height = 8; bc.width = 18
bc.add_data(Reference(db, min_col=2, min_row=16, max_row=28), titles_from_data=True); bc.add_data(Reference(db, min_col=4, min_row=16, max_row=28), titles_from_data=True)
bc.set_categories(Reference(db, min_col=1, min_row=17, max_row=28)); db.add_chart(bc, "F3")
howto(wb, C, ["1. Fees: enter your marketplace's current fees (transaction %, payment processing % and fixed fee, listing fee, offsite ads %), your hourly rate and the profit margin you aim for.",
              "2. Products: enter materials, packaging, minutes to make, your price, the shipping you charge and the postage you pay. Unit cost, fees, profit, margin and a suggested price for your target margin are worked out. Orange margin = below target.",
              "3. Orders: one row per order. Pick the product, enter quantity and prices, and say if it came from an offsite ad. Fees, product cost and profit fill in.",
              "4. Dashboard: revenue, fees, costs, profit and margin for the year, month by month, plus best sellers.", "5. Works for any handmade or craft marketplace. Fees change, so check them. Delete the sample data first."])
wb.save(OUT / "Handmade-Shop-Profit-Calculator.xlsx")

# 2. Wedding guest list & seating
C = "A61E4D"; title, header = kit(C); wb = Workbook(); gl = wb.active; gl.title = "Guest list"
title(gl, "Wedding Guest List", "One row per invitation (household). RSVPs, meals and tables are counted for you.")
header(gl, ["Invitation / household", "Side", "Group", "Adults", "Children", "Address", "Save the date", "Invite sent", "RSVP", "Attending", "Meal choices", "Dietary needs", "Table", "Gift", "Thank-you sent"],
       [26, 12, 14, 8, 9, 26, 10, 10, 10, 10, 18, 16, 7, 18, 10])
groups = ["Family", "Friends", "Work", "Plus-ones"]
fam = ["Smith", "Garcia", "Novak", "Chen", "Patel", "Murphy", "Rossi", "Kowalski", "Okafor", "Silva", "Müller", "Haddad", "Larsen", "Brown", "Tanaka", "Dubois", "Ivanova", "Kaur", "Evans", "Moreau", "Jansen", "Ahmed"]
for i, f in enumerate(fam):
    r = 4 + i; a = random.choice([1, 2, 2, 2]); ch = random.choice([0, 0, 0, 1, 2])
    gl[f"A{r}"] = random.choice(["The ", ""]) + f + (" family" if ch else ""); gl[f"B{r}"] = random.choice(["Partner 1", "Partner 2", "Both"]); gl[f"C{r}"] = random.choice(groups)
    gl[f"D{r}"] = a; gl[f"E{r}"] = ch; gl[f"G{r}"] = "Yes"; gl[f"H{r}"] = "Yes"
    rs = random.choice(["Yes", "Yes", "Yes", "No", "Pending"]); gl[f"I{r}"] = rs
    if rs == "Yes":
        gl[f"J{r}"] = a + ch - random.choice([0, 0, 0, 1]) if a + ch > 1 else 1; gl[f"M{r}"] = 1 + i % 6
        gl[f"K{r}"] = random.choice(["2 beef", "1 fish, 1 veg", "2 chicken", "1 beef, 1 veg", "1 chicken"]); gl[f"L{r}"] = random.choice(["", "", "", "Gluten-free", "Nut allergy", "Vegan"])
dv(gl, '"Partner 1,Partner 2,Both"', "B4:B500"); dv(gl, '"' + ",".join(groups) + ',Neighbours,Other"', "C4:C500"); dv(gl, '"Yes,No"', "G4:H500"); dv(gl, '"Yes,No"', "O4:O500"); dv(gl, '"Pending,Yes,No"', "I4:I500")
for s, col in [("Yes", "D3F9D8"), ("No", "F1F3F5"), ("Pending", "FFF3BF")]:
    gl.conditional_formatting.add("I4:I500", CellIsRule(operator="equal", formula=[f'"{s}"'], fill=PatternFill("solid", fgColor=col)))
gl.conditional_formatting.add("O4:O500", FormulaRule(formula=['AND($N4<>"",$O4<>"Yes")'], fill=PatternFill("solid", fgColor="FFE3E3")))
ts = wb.create_sheet("Seating", 1); title(ts, "Seating plan", "Set each table's capacity, then put table numbers on the Guest list.")
header(ts, ["Table", "Name / label", "Seats", "Seated", "Free seats", "Guests (write names)"], [8, 18, 8, 8, 10, 60])
for i in range(20):
    r = 4 + i; ts[f"A{r}"] = i + 1; ts[f"C{r}"] = 10 if i < 6 else None
    if i == 0: ts[f"B{r}"] = "Top table"; ts[f"C{r}"] = 8
    ts[f"D{r}"] = f"=SUMIFS('Guest list'!$J$4:$J$500,'Guest list'!$M$4:$M$500,A{r})"
    ts[f"E{r}"] = f'=IF(N(C{r})=0,"",C{r}-D{r})'
ts.conditional_formatting.add("E4:E23", CellIsRule(operator="lessThan", formula=["0"], fill=PatternFill("solid", fgColor="FFC9C9"), font=Font(bold=True, color="C0392B")))
ts["A25"] = "Attending guests without a table"; ts["A25"].font = Font(bold=True); ts["D25"] = "=SUMIFS('Guest list'!J4:J500,'Guest list'!I4:I500,\"Yes\",'Guest list'!M4:M500,\"\")"
sm = wb.create_sheet("Summary", 0); title(sm, "Guest Summary", "Updates from the Guest list.")
G = "'Guest list'!"
kpis(sm, [("Invitations", f"=COUNTA({G}A4:A500)", "0"), ("Guests invited", f"=SUM({G}D4:E500)", "0"), ("Guests attending", f"=SUM({G}J4:J500)", "0"),
          ("Invitations still pending", f'=COUNTIF({G}I4:I500,"Pending")', "0"), ("Guests on pending invitations", f'=SUMIFS({G}D4:D500,{G}I4:I500,"Pending")+SUMIFS({G}E4:E500,{G}I4:I500,"Pending")', "0"),
          ("Invitations declined", f'=COUNTIF({G}I4:I500,"No")', "0"), ("Invites not sent yet", f'=COUNTA({G}A4:A500)-COUNTIF({G}H4:H500,"Yes")', "0"),
          ("Dietary needs to tell caterer", f'=COUNTIF({G}L4:L500,"?*")', "0"), ("Thank-yous still to send", f'=COUNTIFS({G}N4:N500,"?*",{G}O4:O500,"<>Yes")', "0")], wa=32)
sm["B6"].font = Font(bold=True, size=13, color=C)
header(sm, ["By side", "Invited", "Attending"], [32, 14, 12], row=15, freeze=False)
for i, s in enumerate(["Partner 1", "Partner 2", "Both"]):
    r = 16 + i; sm[f"A{r}"] = s; sm[f"B{r}"] = f"=SUMIFS({G}D4:D500,{G}B4:B500,A{r})+SUMIFS({G}E4:E500,{G}B4:B500,A{r})"; sm[f"C{r}"] = f"=SUMIFS({G}J4:J500,{G}B4:B500,A{r})"
header(sm, ["By group", "Invited", "Attending"], [32, 14, 12], row=20, freeze=False)
for i, s in enumerate(groups + ["Neighbours", "Other"]):
    r = 21 + i; sm[f"A{r}"] = s; sm[f"B{r}"] = f"=SUMIFS({G}D4:D500,{G}C4:C500,A{r})+SUMIFS({G}E4:E500,{G}C4:C500,A{r})"; sm[f"C{r}"] = f"=SUMIFS({G}J4:J500,{G}C4:C500,A{r})"
bc = BarChart(); bc.title = "Invited vs attending by side"; bc.height = 7; bc.width = 14
bc.add_data(Reference(sm, min_col=2, min_row=15, max_row=18), titles_from_data=True); bc.add_data(Reference(sm, min_col=3, min_row=15, max_row=18), titles_from_data=True)
bc.set_categories(Reference(sm, min_col=1, min_row=16, max_row=18)); sm.add_chart(bc, "E3")
howto(wb, C, ["1. Guest list: one row per invitation (a couple or family). Enter who's on which side, the group, how many adults and children are invited and the address.",
              "2. Tick save the dates and invites as they go out. When replies arrive, set RSVP and enter how many are attending, their meal choices and any dietary needs.",
              "3. Seating: set each table's seats, then type a table number for each household on the Guest list. Seated and free seats update, and overfull tables turn red.",
              "4. Summary: invited, attending, pending, declined, dietary needs for the caterer and thank-yous still to send. Delete the sample guests first."])
wb.save(OUT / "Wedding-Guest-List-Seating.xlsx")

# 3. Sports team manager
C = "2B8A3E"; title, header = kit(C); wb = Workbook(); pl = wb.active; pl.title = "Players"
title(pl, "Squad", "Your players, contacts and subs. Games, goals and fees owed update automatically.")
header(pl, ["Player", "Shirt no.", "Position", "Parent / contact", "Phone", "Medical notes", "Season fee", "Paid", "Owed", "Games played", "Goals", "Assists", "Player of match"], [18, 8, 11, 18, 14, 18, 10, 10, 10, 10, 8, 8, 10])
squad = [("Leo", "GK"), ("Maya", "DEF"), ("Sami", "DEF"), ("Theo", "DEF"), ("Zara", "MID"), ("Owen", "MID"), ("Aria", "MID"), ("Jude", "FWD"), ("Nia", "FWD"), ("Ravi", "MID"), ("Elsie", "DEF"), ("Kofi", "FWD")]
for i, (n, p) in enumerate(squad):
    r = 4 + i; pl[f"A{r}"] = n + " " + random.choice("ABCDEFGHKLMNPRST") + "."; pl[f"B{r}"] = i + 1; pl[f"C{r}"] = p; pl[f"G{r}"] = 120; pl[f"H{r}"] = random.choice([120, 120, 60, 0])
dv(pl, '"GK,DEF,MID,FWD"', "C4:C60")
P, F = "Match log!", None
for r in range(4, 61):
    pl[f"I{r}"] = f'=IF(A{r}="","",N(G{r})-N(H{r}))'
    pl[f"J{r}"] = f"=IF(A{r}=\"\",\"\",COUNTIFS('Match log'!$B$4:$B$3000,A{r},'Match log'!$C$4:$C$3000,\"Yes\"))"
    pl[f"K{r}"] = f"=IF(A{r}=\"\",\"\",SUMIFS('Match log'!$D$4:$D$3000,'Match log'!$B$4:$B$3000,A{r}))"
    pl[f"L{r}"] = f"=IF(A{r}=\"\",\"\",SUMIFS('Match log'!$E$4:$E$3000,'Match log'!$B$4:$B$3000,A{r}))"
    pl[f"M{r}"] = f"=IF(A{r}=\"\",\"\",COUNTIFS('Match log'!$B$4:$B$3000,A{r},'Match log'!$F$4:$F$3000,\"Yes\"))"
    for c in "GHI": pl[f"{c}{r}"].number_format = M
pl.conditional_formatting.add("I4:I60", CellIsRule(operator="greaterThan", formula=["0"], font=Font(bold=True, color="C0392B")))
fx = wb.create_sheet("Fixtures", 1); title(fx, "Fixtures & results", "Enter fixtures at the start of the season and scores after each game.")
header(fx, ["Date", "Kick-off", "Opponent", "Home / away", "Competition", "Our score", "Their score", "Result", "Points", "Notes"], [11, 9, 20, 11, 12, 9, 10, 8, 7, 24])
opp = ["Riverside FC", "Hillview Rangers", "Northgate Utd", "Parkside Juniors", "St Mary's", "Oakwood Town", "Lakeside", "Eastfield Rovers", "Meadow Park", "Westbrook"]
d = today - dt.timedelta(days=today.weekday() + 2 + 7 * 7); sc = []
for i, o in enumerate(opp):
    r = 4 + i; fx[f"A{r}"] = d + dt.timedelta(weeks=i); fx[f"B{r}"] = dt.time(10, 30); fx[f"C{r}"] = o; fx[f"D{r}"] = "Home" if i % 2 == 0 else "Away"; fx[f"E{r}"] = "League" if i != 6 else "Cup"
    if i < 7:
        a, b = random.choice([0, 1, 2, 2, 3, 4]), random.choice([0, 1, 1, 2, 3]); fx[f"F{r}"] = a; fx[f"G{r}"] = b; sc.append((fx[f"A{r}"].value, a))
dv(fx, '"Home,Away"', "D4:D200"); dv(fx, '"League,Cup,Friendly,Tournament"', "E4:E200")
for r in range(4, 201):
    fx[f"A{r}"].number_format = "ddd dd mmm"; fx[f"B{r}"].number_format = "hh:mm"
    fx[f"H{r}"] = f'=IF(OR(F{r}="",G{r}=""),"",IF(F{r}>G{r},"W",IF(F{r}=G{r},"D","L")))'
    fx[f"I{r}"] = f'=IF(H{r}="","",IF(H{r}="W",3,IF(H{r}="D",1,0)))'
for s, col in [("W", "D3F9D8"), ("D", "FFF3BF"), ("L", "FFE3E3")]:
    fx.conditional_formatting.add("H4:H200", CellIsRule(operator="equal", formula=[f'"{s}"'], fill=PatternFill("solid", fgColor=col)))
ml = wb.create_sheet("Match log", 2); title(ml, "Match log", "One row per player per game: did they play, goals, assists, player of the match.")
header(ml, ["Match date", "Player", "Played?", "Goals", "Assists", "Player of match", "Minutes", "Notes"], [12, 18, 9, 8, 8, 13, 9, 24])
r = 4
for md, goals in sc:
    names = [pl[f"A{4 + i}"].value for i in range(len(squad))]; random.shuffle(names); pom = random.randrange(10)
    scorers = [random.choice(names[:10]) for _ in range(goals)]
    for k, n in enumerate(names):
        ml[f"A{r}"] = md; ml[f"B{r}"] = n; ml[f"C{r}"] = "Yes" if k < 10 else "No"
        if k < 10:
            g = scorers.count(n); ml[f"D{r}"] = g or None; ml[f"G{r}"] = random.choice([40, 50, 60, 60])
            if k == pom: ml[f"F{r}"] = "Yes"
            if g == 0 and goals and random.random() < 0.15: ml[f"E{r}"] = 1
        r += 1
dv(ml, "=Players!$A$4:$A$60", "B4:B3000"); dv(ml, '"Yes,No"', "C4:C3000"); dv(ml, '"Yes"', "F4:F3000")
for r in range(4, 3001): ml[f"A{r}"].number_format = "dd mmm"
db = wb.create_sheet("Season", 0); title(db, "Season Dashboard", "Results, goals and fees at a glance.")
db["A3"] = "Team"; db["B3"] = "Under-11s"; db["B3"].fill = SOFT; db["A3"].font = Font(bold=True)
kpis(db, [("Played", '=COUNT(Fixtures!F4:F200)-COUNTIFS(Fixtures!F4:F200,"<>",Fixtures!G4:G200,"")', "0"), ("Won", '=COUNTIF(Fixtures!H4:H200,"W")', "0"), ("Drawn", '=COUNTIF(Fixtures!H4:H200,"D")', "0"),
          ("Lost", '=COUNTIF(Fixtures!H4:H200,"L")', "0"), ("Goals for", '=SUMIFS(Fixtures!F4:F200,Fixtures!H4:H200,"?*")', "0"), ("Goals against", '=SUMIFS(Fixtures!G4:G200,Fixtures!H4:H200,"?*")', "0"),
          ("Goal difference", "=B8-B9", "+0;-0;0"), ("League points", '=SUMIFS(Fixtures!I4:I200,Fixtures!E4:E200,"League")', "0"), ("Win rate", "=IFERROR(B5/B4,0)", "0%"),
          ("Top scorer", '=IFERROR(IF(MAX(Players!K4:K60)=0,"",INDEX(Players!A4:A60,MATCH(MAX(Players!K4:K60),Players!K4:K60,0))&" ("&MAX(Players!K4:K60)&")"),"")', "@"),
          ("Next fixture", '=IFERROR(INDEX(Fixtures!C4:C200,MATCH(1,INDEX((Fixtures!A4:A200>=TODAY())*(Fixtures!C4:C200<>""),0),0))&" · "&TEXT(INDEX(Fixtures!A4:A200,MATCH(1,INDEX((Fixtures!A4:A200>=TODAY())*(Fixtures!C4:C200<>""),0),0)),"dd mmm"),"None scheduled")', "@"),
          ("Fees still owed", "=SUM(Players!I4:I60)", M)], start=4, wb_=26)
db["B11"].font = Font(bold=True, size=13, color=C)
header(db, ["Player", "Goals", "Games"], [28, 26, 10], row=18, freeze=False)
for i in range(12):
    r = 19 + i; db[f"A{r}"] = f'=IF(Players!A{4 + i}="","",Players!A{4 + i})'; db[f"B{r}"] = f'=IF(A{r}="","",Players!K{4 + i})'; db[f"C{r}"] = f'=IF(A{r}="","",Players!J{4 + i})'
bc = BarChart(); bc.title = "Goals by player"; bc.height = 8; bc.width = 16; bc.legend = None
bc.add_data(Reference(db, min_col=2, min_row=18, max_row=30), titles_from_data=True); bc.set_categories(Reference(db, min_col=1, min_row=19, max_row=30)); db.add_chart(bc, "E3")
howto(wb, C, ["1. Players: add your squad with shirt numbers, positions, contacts, medical notes and the season fee. Enter what each has paid and the amount owed shows in red.",
              "2. Fixtures: enter the season's games. After each game add both scores: the result (W/D/L) and points fill in.",
              "3. Match log: after each game add a row per player (pick from the list) saying whether they played, goals, assists and player of the match. Totals appear on the Players tab.",
              "4. Season: record, goals for and against, league points, win rate, top scorer, the next fixture, fees owed and a goals chart.", "5. Works for football, hockey, netball and most team sports. Delete the sample data first."])
wb.save(OUT / "Sports-Team-Manager.xlsx")

# 4. Calorie & macro tracker
C = "E67700"; title, header = kit(C); wb = Workbook(); st = wb.active; st.title = "Targets"
title(st, "Daily targets", "Set your own targets. If unsure what's right for you, ask a doctor or dietitian.")
settings(st, [("Calories (kcal)", 2000, "0"), ("Protein (g)", 120, "0"), ("Carbs (g)", 220, "0"), ("Fat (g)", 65, "0"), ("Fibre (g)", 30, "0"), ("Water (glasses)", 8, "0")])
st.column_dimensions["A"].width = 22; st.column_dimensions["B"].width = 12
fl = wb.create_sheet("Food library"); title(fl, "Food library", "Add foods you eat often, once. Values per serving (check the label).")
header(fl, ["Food", "Serving", "kcal", "Protein g", "Carbs g", "Fat g", "Fibre g"], [26, 14, 8, 10, 9, 8, 9])
foods = [("Oats", "40 g", 150, 5, 27, 3, 4), ("Milk (semi-skimmed)", "200 ml", 92, 7, 9.5, 3.4, 0), ("Banana", "1 medium", 105, 1.3, 27, 0.4, 3), ("Eggs", "2 large", 143, 12.6, 0.7, 9.5, 0),
         ("Wholemeal bread", "1 slice", 90, 4, 15, 1.2, 2.5), ("Chicken breast", "150 g", 248, 46, 0, 5.4, 0), ("Rice (cooked)", "180 g", 234, 4.8, 51, 0.5, 0.7), ("Broccoli", "80 g", 27, 2.3, 2.2, 0.3, 2.1),
         ("Greek yoghurt", "150 g", 146, 13.5, 6, 7.5, 0), ("Apple", "1 medium", 72, 0.4, 19, 0.2, 3.3), ("Salmon fillet", "120 g", 250, 25, 0, 16, 0), ("Pasta (cooked)", "200 g", 316, 11.6, 62, 1.8, 3.6),
         ("Peanut butter", "1 tbsp", 94, 4, 3, 8, 1), ("Lentil soup", "1 bowl", 180, 11, 30, 2, 8), ("Cheddar", "30 g", 124, 7.6, 0, 10.4, 0), ("Almonds", "30 g", 174, 6.3, 2.2, 15, 3.7)]
for r, f in enumerate(foods, 4):
    for j, v in enumerate(f): fl.cell(r, j + 1, v)
lg = wb.create_sheet("Food log", 0); title(lg, "Food log", "Pick a food from your library and how many servings. Calories and macros fill in.")
header(lg, ["Date", "Meal", "Food", "Servings", "kcal", "Protein g", "Carbs g", "Fat g", "Fibre g", "Notes"], [11, 11, 26, 9, 8, 10, 9, 8, 8, 20])
meals = {"Breakfast": ["Oats", "Milk (semi-skimmed)", "Banana", "Eggs", "Wholemeal bread", "Greek yoghurt"], "Lunch": ["Lentil soup", "Wholemeal bread", "Chicken breast", "Rice (cooked)", "Cheddar"],
         "Dinner": ["Salmon fillet", "Pasta (cooked)", "Chicken breast", "Rice (cooked)", "Broccoli"], "Snack": ["Apple", "Almonds", "Peanut butter", "Greek yoghurt", "Banana"]}
r = 4
for k in range(14, 0, -1):
    dd = today - dt.timedelta(days=k)
    for meal, opts in meals.items():
        for f in random.sample(opts, 3 if meal != "Snack" else 2):
            lg[f"A{r}"] = dd; lg[f"B{r}"] = meal; lg[f"C{r}"] = f; lg[f"D{r}"] = random.choice([1, 1, 1, 1.5]); r += 1
dv(lg, '"Breakfast,Lunch,Dinner,Snack"', "B4:B5000"); dv(lg, "='Food library'!$A$4:$A$500", "C4:C5000")
for r in range(4, 5001):
    lg[f"A{r}"].number_format = "ddd dd mmm"
    for j, c in enumerate("EFGHI"):
        lg[f"{c}{r}"] = f"=IF(C{r}=\"\",\"\",N(D{r})*IFERROR(VLOOKUP(C{r},'Food library'!$A$4:$G$500,{j + 3},FALSE),0))"; lg[f"{c}{r}"].number_format = "0" if c == "E" else "0.0"
dy = wb.create_sheet("Daily totals", 1); title(dy, "Daily totals", "Type a start date. Each day's totals compare with your targets.")
dy["A3"] = "Start date"; dy["B3"] = today - dt.timedelta(days=14); dy["B3"].number_format = "dd mmm yy"; dy["B3"].fill = SOFT; dy["A3"].font = Font(bold=True)
header(dy, ["Date", "kcal", "vs target", "Protein g", "Carbs g", "Fat g", "Fibre g", "Water (glasses)", "Protein %kcal", "Carbs %kcal", "Fat %kcal"], [12, 9, 10, 10, 9, 8, 9, 13, 12, 11, 10], row=5)
for i in range(31):
    r = 6 + i; dy[f"A{r}"] = f"=$B$3+{i}"; dy[f"A{r}"].number_format = "ddd dd mmm"
    for c, src in (("B", "E"), ("D", "F"), ("E", "G"), ("F", "H"), ("G", "I")):
        dy[f"{c}{r}"] = f"=SUMIFS('Food log'!${src}$4:${src}$5000,'Food log'!$A$4:$A$5000,A{r})"; dy[f"{c}{r}"].number_format = "0"
    dy[f"C{r}"] = f'=IF(B{r}=0,"",B{r}-Targets!$B$4)'; dy[f"C{r}"].number_format = "+0;-0;0"
    dy[f"I{r}"] = f'=IF(B{r}=0,"",D{r}*4/B{r})'; dy[f"J{r}"] = f'=IF(B{r}=0,"",E{r}*4/B{r})'; dy[f"K{r}"] = f'=IF(B{r}=0,"",F{r}*9/B{r})'
    for c in "IJK": dy[f"{c}{r}"].number_format = "0%"
dy.conditional_formatting.add("C6:C36", CellIsRule(operator="greaterThan", formula=["0"], font=Font(color="C0392B")))
dy.conditional_formatting.add("C6:C36", CellIsRule(operator="lessThanOrEqual", formula=["0"], font=Font(color="2B8A3E")))
dy.conditional_formatting.add("D6:D36", FormulaRule(formula=["AND(D6>0,D6>=Targets!$B$5)"], fill=PatternFill("solid", fgColor="D3F9D8")))
sm = wb.create_sheet("Summary", 0); title(sm, "Nutrition Summary", "Averages over the days you logged, from the Daily totals tab.")
DT = "'Daily totals'!"
kpis(sm, [("Days logged", f'=COUNTIF({DT}B6:B36,">0")', "0"), ("Average kcal", f'=IFERROR(AVERAGEIF({DT}B6:B36,">0"),0)', "0"), ("Target kcal", "=Targets!B4", "0"),
          ("Average protein g", f"=IFERROR(SUMIFS({DT}D6:D36,{DT}B6:B36,\">0\")/B4,0)", "0"), ("Average carbs g", f"=IFERROR(SUMIFS({DT}E6:E36,{DT}B6:B36,\">0\")/B4,0)", "0"),
          ("Average fat g", f"=IFERROR(SUMIFS({DT}F6:F36,{DT}B6:B36,\">0\")/B4,0)", "0"), ("Average fibre g", f"=IFERROR(SUMIFS({DT}G6:G36,{DT}B6:B36,\">0\")/B4,0)", "0"),
          ("Days within calorie target", f'=COUNTIFS({DT}B6:B36,">0",{DT}C6:C36,"<=0")', "0"), ("Days hitting protein target", f'=COUNTIFS({DT}B6:B36,">0",{DT}D6:D36,">="&Targets!B5)', "0")], wa=30)
header(sm, ["Meal", "Share of kcal"], [30, 14], row=15, freeze=False)
for i, m in enumerate(meals):
    r = 16 + i; sm[f"A{r}"] = m; sm[f"B{r}"] = f"=IFERROR(SUMIFS('Food log'!$E$4:$E$5000,'Food log'!$B$4:$B$5000,A{r})/SUM('Food log'!$E$4:$E$5000),0)"; sm[f"B{r}"].number_format = "0%"
lc = LineChart(); lc.title = "Calories per day"; lc.height = 8; lc.width = 20; lc.legend = None
lc.add_data(Reference(dy, min_col=2, min_row=5, max_row=20), titles_from_data=True); lc.set_categories(Reference(dy, min_col=1, min_row=6, max_row=20)); sm.add_chart(lc, "E3")
sm["A22"] = "A personal food diary, not medical or dietary advice."; sm["A22"].font = Font(italic=True, color="777777")
howto(wb, C, ["1. Targets: set your daily calories, protein, carbs, fat, fibre and water.", "2. Food library: add the foods you eat often with their values per serving from the label. Do this once and reuse them.",
              "3. Food log: each meal, pick the food from the list and type the number of servings (1.5 for one and a half). Calories and macros fill in.",
              "4. Daily totals: type a start date to see 31 days against your targets, with the share of calories from protein, carbs and fat. Add water glasses by hand.",
              "5. Summary: averages, days within your calorie target, days hitting protein and calories by meal. Delete the sample log first."])
wb.save(OUT / "Calorie-Macro-Tracker.xlsx")

# 5. Rent vs buy calculator
C = "1971C2"; title, header = kit(C); wb = Workbook(); ip = wb.active; ip.title = "Calculator"
title(ip, "Rent vs Buy Calculator", "Change the blue cells. Compares your wealth after each year if you buy, or rent and invest the difference.")
inputs = [("BUYING", None, None), ("Home price", 350000, M), ("Deposit (%)", 0.15, "0%"), ("Mortgage interest rate (yearly)", 0.045, "0.00%"), ("Mortgage term (years)", 25, "0"),
          ("Buying costs (% of price: fees, taxes, survey)", 0.03, "0.0%"), ("Property tax / rates (% of value per year)", 0.005, "0.00%"), ("Maintenance (% of value per year)", 0.01, "0.0%"),
          ("Home insurance (per year)", 600, M), ("Home price growth (yearly)", 0.03, "0.0%"), ("Selling costs (% of value)", 0.025, "0.0%"),
          ("RENTING", None, None), ("Monthly rent", 1350, M), ("Rent increase (yearly)", 0.03, "0.0%"), ("Renter's insurance (per year)", 150, M),
          ("INVESTING", None, None), ("Investment return on savings (yearly)", 0.05, "0.0%")]
for r, (n, v, f) in enumerate(inputs, 4):
    ip[f"A{r}"] = n; ip[f"A{r}"].font = Font(bold=True, color=C if v is None else "000000")
    if v is not None: ip[f"B{r}"] = v; ip[f"B{r}"].number_format = f; ip[f"B{r}"].fill = PatternFill("solid", fgColor="DBE4FF")
ip.column_dimensions["A"].width = 44; ip.column_dimensions["B"].width = 14
# names: price B5 dep B6 rate B7 term B8 buyc B9 tax B10 maint B11 ins B12 growth B13 sell B14 rent B16 rinc B17 rins B18 ret B20
ip["A22"] = "RESULTS"; ip["A22"].font = Font(bold=True, color=C)
res = [("Loan amount", "=B5*(1-B6)", M), ("Monthly mortgage payment", "=PMT(B7/12,B8*12,-B23)", M), ("Cash needed up front (deposit + buying costs)", "=B5*B6+B5*B9", M),
       ("First-year cost of owning (per month)", "=Years!C5/12", M), ("First-year cost of renting (per month)", "=Years!D5/12", M),
       ("Buying comes out ahead from year", '=IFERROR(INDEX(Years!A5:A34,MATCH(1,Years!K5:K34,0)),"Not within 30 years")', "0"),
       ("Wealth if you buy, after 10 years", "=Years!I14", M), ("Wealth if you rent, after 10 years", "=Years!J14", M), ("Difference after 10 years (buy - rent)", "=B29-B30", M)]
for r, (n, f, nf_) in enumerate(res, 23):
    ip[f"A{r}"] = n; ip[f"B{r}"] = f; ip[f"B{r}"].number_format = nf_; ip[f"B{r}"].fill = SOFT; ip[f"A{r}"].font = Font(bold=True)
ip["B28"].font = Font(bold=True, size=14, color=C); ip["B31"].font = Font(bold=True, color=C)
ip.conditional_formatting.add("B31", CellIsRule(operator="lessThan", formula=["0"], font=Font(bold=True, color="C0392B")))
ip["A34"] = "Estimates only, using constant rates. Not financial advice. Real prices, rates and taxes vary."; ip["A34"].font = Font(italic=True, color="777777")
yr = wb.create_sheet("Years"); title(yr, "Year by year", "Worked out from the Calculator tab. Each side invests any money it saves compared with the other.")
header(yr, ["Year", "Home value", "Cost of owning", "Cost of renting", "Mortgage left", "Home equity (after selling costs)", "Owner's savings pot", "Renter's savings pot", "Wealth if you buy", "Wealth if you rent", "Buy ahead?"],
       [7, 13, 13, 13, 13, 16, 13, 13, 14, 14, 9], row=4)
I = "Calculator!"
for i in range(30):
    r = 5 + i; yv = i + 1; yr[f"A{r}"] = yv
    yr[f"B{r}"] = f"={I}$B$5*(1+{I}$B$13)^A{r}"
    prev_val = f"{I}$B$5*(1+{I}$B$13)^(A{r}-1)"
    yr[f"C{r}"] = f"=IF(A{r}<={I}$B$8,12*{I}$B$24,0)+{prev_val}*({I}$B$10+{I}$B$11)+{I}$B$12"
    yr[f"D{r}"] = f"=12*{I}$B$16*(1+{I}$B$17)^(A{r}-1)+{I}$B$18"
    yr[f"E{r}"] = f"=IF(A{r}>={I}$B$8,0,-FV({I}$B$7/12,A{r}*12,-{I}$B$24,{I}$B$23))"
    yr[f"F{r}"] = f"=B{r}*(1-{I}$B$14)-E{r}"
    pg = f"G{r - 1}" if i else "0"; pr_ = f"H{r - 1}" if i else f"{I}$B$25"
    yr[f"G{r}"] = f"={pg}*(1+{I}$B$20)+MAX(0,D{r}-C{r})"
    yr[f"H{r}"] = f"={pr_}*(1+{I}$B$20)+MAX(0,C{r}-D{r})"
    yr[f"I{r}"] = f"=F{r}+G{r}"; yr[f"J{r}"] = f"=H{r}"; yr[f"K{r}"] = f"=IF(I{r}>=J{r},1,0)"
    for c in "BCDEFGHIJ": yr[f"{c}{r}"].number_format = "#,##0"
yr.conditional_formatting.add("K5:K34", CellIsRule(operator="equal", formula=["1"], fill=PatternFill("solid", fgColor="D3F9D8")))
lc = LineChart(); lc.title = "Wealth: buy vs rent"; lc.height = 9; lc.width = 18
lc.add_data(Reference(yr, min_col=9, min_row=4, max_row=34), titles_from_data=True); lc.add_data(Reference(yr, min_col=10, min_row=4, max_row=34), titles_from_data=True)
lc.set_categories(Reference(yr, min_col=1, min_row=5, max_row=34)); ip.add_chart(lc, "D4")
howto(wb, C, ["1. Calculator: change the blue cells: home price, deposit, mortgage rate and term, buying and selling costs, yearly property tax, maintenance and insurance, expected price growth, your rent and rent increases, and what your savings could earn.",
              "2. Results show the mortgage payment, cash needed up front, monthly cost of owning vs renting, the year buying pulls ahead, and wealth after 10 years either way.",
              "3. Years tab: the full 30-year comparison. The renter invests the deposit and buying costs, and whichever side is cheaper in a year invests the difference.",
              "4. Try different growth and return rates to see how sensitive the answer is. Estimates only, not financial advice."])
wb.save(OUT / "Rent-vs-Buy-Calculator.xlsx")
print("built 5")
