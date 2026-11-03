"""Builds a batch of spreadsheet products into products/. Run: python3 make_batch.py"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, DataBarRule, FormulaRule
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.utils import get_column_letter as L
import pathlib, datetime as dt
OUT = pathlib.Path(__file__).parent / "products"; OUT.mkdir(exist_ok=True)

def kit(color):
    hf = PatternFill("solid", fgColor=color); h = Font(bold=True, color="FFFFFF")
    def title(ws, t, s):
        ws["A1"] = t; ws["A1"].font = Font(bold=True, size=18, color=color); ws["A2"] = s; ws["A2"].font = Font(italic=True, color="777777")
    def header(ws, cols, widths, row=3, freeze=True):
        for i, (c, w) in enumerate(zip(cols, widths), 1):
            x = ws.cell(row, i, c); x.font = h; x.fill = hf; x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            ws.column_dimensions[L(i)].width = w
        if freeze: ws.freeze_panes = ws.cell(row + 1, 1)
    return title, header
def dv(ws, f, rng):
    v = DataValidation(type="list", formula1=f, allow_blank=True); ws.add_data_validation(v); v.add(rng)
def howto(wb, color, lines):
    ws = wb.create_sheet("How to use"); ws["A1"] = "How to use"; ws["A1"].font = Font(bold=True, size=18, color=color)
    for i, t in enumerate(lines, 3): ws.cell(i, 1, t)
    ws.column_dimensions["A"].width = 110
SOFT = PatternFill("solid", fgColor="EEF4F1")
M = "#,##0.00"

# 1. Debt payoff planner (avalanche / snowball)
C = "B23A48"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Debts"
title(ws, "Debt Payoff Planner", "List your debts, pick a method, and see your debt-free date.")
header(ws, ["Debt", "Balance", "Interest %", "Minimum payment", "Priority (auto)"], [24, 14, 12, 16, 14])
debts = [("Credit card", 3200, 22.9, 90), ("Car loan", 8500, 6.5, 210), ("Store card", 900, 27.0, 35), ("Personal loan", 4000, 11.0, 120)]
for r, d in enumerate(debts, 4):
    for c, x in enumerate(d, 1): ws.cell(r, c, x)
for r in range(4, 14):
    ws[f"E{r}"] = f'=IF(A{r}="","",IF(Plan!$B$4="Avalanche (highest interest first)",RANK(C{r},$C$4:$C$13,0)+COUNTIF($C$4:C{r},C{r})-1,RANK(B{r},$B$4:$B$13,1)+COUNTIF($B$4:B{r},B{r})-1))'
    ws[f"B{r}"].number_format = ws[f"D{r}"].number_format = M
ws["A15"] = "Total"; ws["B15"] = "=SUM(B4:B13)"; ws["D15"] = "=SUM(D4:D13)"; ws["A15"].font = Font(bold=True)
for c in "BD": ws[f"{c}15"].number_format = M
pl = wb.create_sheet("Plan", 0); title(pl, "Your payoff plan", "Set your method and monthly budget. The schedule updates automatically.")
pl["A4"] = "Method"; pl["B4"] = "Avalanche (highest interest first)"; dv(pl, '"Avalanche (highest interest first),Snowball (smallest balance first)"', "B4")
pl["A5"] = "Total you can pay each month"; pl["B5"] = 600; pl["B5"].number_format = M
pl["A6"] = "Minimums total"; pl["B6"] = "=Debts!D15"; pl["B6"].number_format = M
pl["A7"] = "Extra going to the priority debt"; pl["B7"] = "=MAX(0,B5-B6)"; pl["B7"].number_format = M
pl["A8"] = "Months to debt-free"; pl["B8"] = '=IFERROR(MATCH(TRUE,INDEX(Schedule!$N$5:$N$364<=0.005,0),0),"Over 30 years: increase your payment")'
pl["A9"] = "Debt-free date"; pl["B9"] = '=IFERROR(EDATE(TODAY(),B8),"")'; pl["B9"].number_format = "mmmm yyyy"
pl["A10"] = "Total interest paid"; pl["B10"] = '=IFERROR(SUM(Schedule!$O$5:INDEX(Schedule!$O$5:$O$364,B8)),"")'; pl["B10"].number_format = M
for r in range(4, 11): pl[f"A{r}"].font = Font(bold=True); pl[f"B{r}"].fill = SOFT
pl.column_dimensions["A"].width = 34; pl.column_dimensions["B"].width = 36
sc = wb.create_sheet("Schedule"); title(sc, "Month-by-month schedule", "Balances after each month's payment. Don't edit this tab.")
# columns: A month, B..K balances of debt slots 1..10 (by priority), N total, O interest that month
header(sc, ["Month"] + [f"Debt {i}" for i in range(1, 11)] + ["", "", "Total left", "Interest"], [8] + [11] * 10 + [2, 2, 13, 12], row=4)
# Slot i = debt with priority i. Helper rows on Debts: sorted name/balance/rate/min (rows 18-27)
ws["A17"] = "Sorted by priority (helper, don't edit)"; ws["A17"].font = Font(italic=True, color="999999")
for i in range(1, 11):
    r = 17 + i
    for c, col in zip("ABCD", "ABCD"):
        ws[f"{c}{r}"] = f'=IFERROR(INDEX(${col}$4:${col}$13,MATCH({i},$E$4:$E$13,0)),{"\"\"" if c == "A" else 0})'
    ws[f"B{r}"].number_format = ws[f"D{r}"].number_format = M
for i in range(10): sc.cell(4, 2 + i).value = f'=IF(Debts!A{18+i}="","—",Debts!A{18+i})'
for i in range(10): sc.cell(4, 17 + i).value = f"Pay {i+1}"
for m in range(1, 361):
    r = 4 + m; sc[f"A{r}"] = m
    P = lambda j: (f"Debts!B{18 + j}" if m == 1 else f"{L(2 + j)}{r - 1}")       # previous balance of slot j
    BAL = lambda j: f"({P(j)}*(1+Debts!C{18+j}/1200))"                            # balance after interest
    for i in range(10):
        later = "+".join(f"IF({P(j)}>0,MIN(Debts!D{18+j},{BAL(j)}),0)" for j in range(i + 1, 10)) or "0"
        paid_before = f"SUM({L(17)}{r}:{L(16 + i)}{r})" if i else "0"
        sc[f"{L(17 + i)}{r}"] = f"=IF({P(i)}<=0,0,MAX(MIN(Debts!D{18+i},{BAL(i)}),MIN({BAL(i)},Plan!$B$5-{paid_before}-({later}))))"
        sc[f"{L(2 + i)}{r}"] = f"=IF({P(i)}<=0,0,MAX(0,{BAL(i)}-{L(17 + i)}{r}))"
        sc[f"{L(2 + i)}{r}"].number_format = "#,##0"; sc[f"{L(17 + i)}{r}"].number_format = "#,##0"
    sc[f"N{r}"] = f"=SUM(B{r}:K{r})"; sc[f"N{r}"].number_format = "#,##0"
    sc[f"O{r}"] = "=" + "+".join(f"IF({P(i)}>0,{P(i)}*Debts!C{18+i}/1200,0)" for i in range(10)); sc[f"O{r}"].number_format = M
ch = LineChart(); ch.title = "Total debt over time"; ch.height = 7.5; ch.width = 17; ch.legend = None
ch.add_data(Reference(sc, min_col=14, min_row=4, max_row=124), titles_from_data=True); pl.add_chart(ch, "D4")
howto(wb, C, ["1. On Debts, list each debt with its balance, interest rate and minimum payment (up to 10).",
  "2. On Plan, choose Avalanche (saves the most interest) or Snowball (quick wins), and enter how much you can pay each month in total.",
  "3. The Plan tab shows how many months until you're debt-free, the date, and the total interest. Schedule shows every month.",
  "Tip: try raising your monthly payment by even 50 and see how many months it saves.", "Works in Google Sheets (File > Import) and Excel."])
wb.save(OUT / "Debt-Payoff-Planner.xlsx")

# 2. Habit tracker
C = "2E7D5B"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Habits"
title(ws, "Habit Tracker", "Type 1 (or x) on each day you do the habit. Pick the month in B2.")
ws["A2"] = None; ws["B2"] = dt.date(2026, 1, 1); ws["B2"].number_format = "mmmm yyyy"; ws["B2"].fill = SOFT; ws["A2"] = "Month:"; ws["A2"].font = Font(bold=True)
header(ws, ["Habit"] + [str(d) for d in range(1, 32)] + ["Done", "Goal", "%"], [22] + [3.6] * 31 + [7, 7, 7], row=4)
for d in range(1, 32): ws.cell(4, 1 + d).value = f'=IF({d}>DAY(EOMONTH($B$2,0)),"",{d})'
habits = ["Drink 2L water", "Exercise 30 min", "Read 20 pages", "No phone after 10pm", "Meditate", "Walk 8,000 steps", "Journal", "Sleep by 11pm", "", "", "", ""]
for i, hb in enumerate(habits, 5):
    ws.cell(i, 1, hb or None)
    ws[f"AF{i}"] = f'=COUNTIF(B{i}:AF{i},1)+COUNTIF(B{i}:AF{i},"x")'
for i in range(5, 17):
    ws[f"AG{i}"] = f'=IF(A{i}="","",COUNTIF(B{i}:AF{i},1)+COUNTIF(B{i}:AF{i},"x"))'; ws[f"AH{i}"] = f'=IF(A{i}="","",DAY(EOMONTH($B$2,0)))'
    ws[f"AI{i}"] = f'=IF(OR(A{i}="",AH{i}=0),"",AG{i}/AH{i})'; ws[f"AI{i}"].number_format = "0%"
    ws[f"AF{i}"] = None
ws.conditional_formatting.add("B5:AF16", FormulaRule(formula=['OR(B5=1,LOWER(B5)="x")'], fill=PatternFill("solid", fgColor="7BC8A4")))
ws.conditional_formatting.add("AI5:AI16", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="7BC8A4"))
# fix: day 31 column is AF; Done/Goal/% are AG/AH/AI
for c, t in zip(["AG", "AH", "AI"], ["Done", "Goal", "%"]): ws[f"{c}4"] = t; ws[f"{c}4"].font = Font(bold=True, color="FFFFFF"); ws[f"{c}4"].fill = PatternFill("solid", fgColor=C)
for r, row in enumerate([[1,1,1,0,1,1,1], [1,0,1,0,1,0,0], [1,1,1,1,1,1,1]], 5):
    for d, x in enumerate(row, 2):
        if x: ws.cell(r, d, 1)
ws.freeze_panes = "B5"
sm = wb.create_sheet("Year"); title(sm, "Year overview", "Copy each month's % here to see your year.")
header(sm, ["Habit"] + [dt.date(2026, m, 1).strftime("%b") for m in range(1, 13)], [22] + [7] * 12)
for i in range(12): sm.cell(4 + i, 1).value = f"=IF(Habits!A{5+i}=\"\",\"\",Habits!A{5+i})"
for r in range(4, 16):
    for c in range(2, 14): sm.cell(r, c).number_format = "0%"
sm.conditional_formatting.add("B4:M15", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="7BC8A4"))
howto(wb, C, ["1. Set the month in B2 on the Habits tab (any date in that month).", "2. Write up to 12 habits in column A.",
  "3. Each day, type 1 or x in the box for each habit you did. It turns green.", "4. Done, Goal and % update automatically.",
  "5. At the end of the month, copy the % column into the Year tab, then clear the ticks and change the month.", "Works in Google Sheets and Excel."])
wb.save(OUT / "Habit-Tracker.xlsx")

# 3. Wedding budget planner
C = "A35C7A"; title, header = kit(C); wb = Workbook(); st = wb.active; st.title = "Budget"
title(st, "Wedding Budget Planner", "Set your total budget. Each category gets a suggested share; override any estimate.")
st["A3"] = "Total budget"; st["B3"] = 25000; st["B3"].number_format = M; st["B3"].fill = SOFT; st["A3"].font = Font(bold=True)
header(st, ["Category", "Suggested %", "Estimate", "Actual", "Paid so far", "Still to pay", "Difference"], [26, 12, 13, 13, 13, 13, 13], row=5)
cats = [("Venue & catering", 45), ("Photography & video", 11), ("Attire & beauty", 8), ("Music & entertainment", 7), ("Flowers & decor", 8), ("Rings", 4), ("Stationery", 2), ("Transport", 2), ("Favours & gifts", 2), ("Officiant & licence", 1), ("Honeymoon", 6), ("Buffer", 4)]
for i, (c, p) in enumerate(cats, 6):
    st[f"A{i}"] = c; st[f"B{i}"] = p / 100; st[f"B{i}"].number_format = "0%"
    st[f"C{i}"] = f"=$B$3*B{i}"
    st[f"D{i}"] = f'=SUMIFS(Expenses!$D:$D,Expenses!$A:$A,A{i})'; st[f"E{i}"] = f'=SUMIFS(Expenses!$E:$E,Expenses!$A:$A,A{i})'
    st[f"F{i}"] = f"=D{i}-E{i}"; st[f"G{i}"] = f"=C{i}-D{i}"
    for c in "CDEFG": st[f"{c}{i}"].number_format = M
e = 5 + len(cats); st[f"A{e+1}"] = "Total"; st[f"A{e+1}"].font = Font(bold=True)
for c in "BCDEFG": st[f"{c}{e+1}"] = f"=SUM({c}6:{c}{e})"; st[f"{c}{e+1}"].number_format = "0%" if c == "B" else M; st[f"{c}{e+1}"].font = Font(bold=True)
st.conditional_formatting.add(f"G6:G{e}", CellIsRule(operator="lessThan", formula=["0"], fill=PatternFill("solid", fgColor="F8D7DA")))
pie = PieChart(); pie.title = "Estimate by category"; pie.height = 8; pie.width = 12
pie.add_data(Reference(st, min_col=3, min_row=6, max_row=e)); pie.set_categories(Reference(st, min_col=1, min_row=6, max_row=e)); st.add_chart(pie, "I5")
ex = wb.create_sheet("Expenses"); title(ex, "Expenses & vendors", "One row per vendor or purchase.")
header(ex, ["Category", "Vendor", "Contact", "Total cost", "Paid", "Due date", "Status", "Notes"], [24, 22, 22, 12, 12, 12, 12, 30])
dv(ex, f"=Budget!$A$6:$A${e}", "A4:A300"); dv(ex, '"Researching,Booked,Deposit paid,Paid in full"', "G4:G300")
for r, row in enumerate([("Venue & catering", "Rosewood Hall", "events@example.com", 11200, 3000, "2026-05-01", "Deposit paid"), ("Photography & video", "Lens & Light", "", 2600, 500, "2026-06-01", "Deposit paid")], 4):
    for c, x in enumerate(row, 1): ex.cell(r, c, dt.date.fromisoformat(x) if c == 6 else x)
for r in range(4, 301): ex[f"D{r}"].number_format = ex[f"E{r}"].number_format = M; ex[f"F{r}"].number_format = "yyyy-mm-dd"
gl = wb.create_sheet("Guests"); title(gl, "Guest list", "Track invites, RSVPs and meal choices.")
header(gl, ["Name", "Side", "Party size", "Invited", "RSVP", "Meal", "Table", "Gift", "Thank-you sent"], [24, 10, 10, 9, 10, 12, 8, 18, 14])
dv(gl, '"Bride,Groom,Both"', "B4:B400"); dv(gl, '"Yes,No"', "D4:D400"); dv(gl, '"Attending,Declined,No reply"', "E4:E400"); dv(gl, '"Meat,Fish,Vegetarian,Vegan,Child"', "F4:F400"); dv(gl, '"Yes,No"', "I4:I400")
gl["K3"] = "Summary"; gl["K3"].font = Font(bold=True, color=C)
for r, (k, f) in enumerate([("Invited (people)", '=SUMIFS(C:C,D:D,"Yes")'), ("Attending (people)", '=SUMIFS(C:C,E:E,"Attending")'), ("Declined", '=SUMIFS(C:C,E:E,"Declined")'), ("Waiting for reply", '=SUMIFS(C:C,E:E,"No reply")')], 4):
    gl[f"K{r}"] = k; gl[f"L{r}"] = f
gl.column_dimensions["K"].width = 20
howto(wb, C, ["1. Enter your total budget on the Budget tab. Suggested shares fill in an estimate per category; change the % to suit you.",
  "2. Add every vendor and purchase on Expenses. Actual, Paid and Still to pay update automatically. Over-budget categories turn red.",
  "3. Use Guests for invites, RSVPs, meals and thank-you notes.", "Works in Google Sheets and Excel."])
wb.save(OUT / "Wedding-Budget-Planner.xlsx")

# 4. Meal planner + grocery list
C = "D9822B"; title, header = kit(C); wb = Workbook(); mp = wb.active; mp.title = "Week plan"
title(mp, "Weekly Meal Planner", "Plan the week's meals. Pick from your recipes or type your own.")
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
header(mp, ["Day", "Breakfast", "Lunch", "Dinner", "Snacks", "Notes"], [12, 24, 24, 24, 18, 26])
for i, d in enumerate(days, 4): mp[f"A{i}"] = d; mp[f"A{i}"].font = Font(bold=True)
for c in "BCD": dv(mp, "=Recipes!$A$4:$A$100", f"{c}4:{c}10")
for i, row in enumerate([("Overnight oats", "Chicken salad wrap", "Spaghetti bolognese"), ("Greek yogurt & berries", "Leftover bolognese", "Veggie stir-fry")], 4):
    for c, x in zip("BCD", row): mp[f"{c}{i}"] = x
rc = wb.create_sheet("Recipes"); title(rc, "Recipe bank", "Your go-to meals and their main ingredients.")
header(rc, ["Recipe", "Meal", "Ingredients (comma separated)", "Prep time", "Rating"], [26, 12, 60, 10, 8])
for r, row in enumerate([("Overnight oats", "Breakfast", "oats, milk, chia seeds, berries", "5 min", 5), ("Greek yogurt & berries", "Breakfast", "greek yogurt, berries, honey", "2 min", 4),
    ("Chicken salad wrap", "Lunch", "tortilla wraps, chicken breast, lettuce, tomato", "10 min", 4), ("Spaghetti bolognese", "Dinner", "spaghetti, minced beef, tomato passata, onion, garlic", "35 min", 5),
    ("Veggie stir-fry", "Dinner", "noodles, peppers, broccoli, soy sauce, garlic", "20 min", 4)], 4):
    for c, x in enumerate(row, 1): rc.cell(r, c, x)
gr = wb.create_sheet("Grocery list"); title(gr, "Grocery list", "Tick items as you shop. Grouped by aisle.")
header(gr, ["✓", "Item", "Aisle", "Qty", "Est. price"], [5, 30, 16, 8, 11])
dv(gr, '"Produce,Meat & fish,Dairy,Bakery,Pantry,Frozen,Drinks,Household,Other"', "C4:C150"); dv(gr, '"✓"', "A4:A150")
for r, row in enumerate([("", "Oats", "Pantry", 1, 1.5), ("", "Berries", "Produce", 2, 3.0), ("", "Chicken breast", "Meat & fish", 1, 5.5), ("", "Minced beef", "Meat & fish", 1, 4.2)], 4):
    for c, x in enumerate(row, 1):
        if x != "": gr.cell(r, c, x)
gr["G3"] = "Estimated total"; gr["H3"] = "=SUMPRODUCT(D4:D150,E4:E150)"; gr["G4"] = "Items left"; gr["H4"] = '=COUNTA(B4:B150)-COUNTIF(A4:A150,"✓")'
gr["G3"].font = gr["G4"].font = Font(bold=True); gr["H3"].number_format = M; gr.column_dimensions["G"].width = 16
gr.conditional_formatting.add("A4:E150", FormulaRule(formula=['$A4="✓"'], font=Font(strike=True, color="999999")))
howto(wb, C, ["1. Save your favourite meals on Recipes.", "2. On Week plan, pick meals from the dropdowns (or type anything).", "3. Write what you need on Grocery list, grouped by aisle. Tick ✓ as you shop; ticked items are crossed out.", "Works in Google Sheets and Excel."])
wb.save(OUT / "Meal-Planner-Grocery-List.xlsx")

# 5. Social media content calendar
C = "3B5BDB"; title, header = kit(C); wb = Workbook(); cc = wb.active; cc.title = "Calendar"
title(cc, "Social Media Content Calendar", "Plan every post: date, platform, format, caption and status.")
header(cc, ["Date", "Day", "Platform", "Format", "Topic / hook", "Caption", "Hashtags", "Link", "Status", "Likes", "Comments", "Shares"], [12, 6, 12, 12, 28, 40, 24, 22, 12, 8, 10, 8])
dv(cc, '"Instagram,TikTok,LinkedIn,X,Facebook,YouTube,Pinterest,Threads"', "C4:C500"); dv(cc, '"Post,Reel,Story,Carousel,Video,Short,Thread,Pin"', "D4:D500"); dv(cc, '"Idea,Drafting,Scheduled,Posted"', "I4:I500")
for r in range(4, 501): cc[f"A{r}"].number_format = "yyyy-mm-dd"; cc[f"B{r}"] = f'=IF(A{r}="","",TEXT(A{r},"ddd"))'
for r, row in enumerate([("2026-01-05", "Instagram", "Carousel", "5 mistakes new freelancers make", "", "#freelance #smallbusiness", "", "Scheduled"), ("2026-01-06", "LinkedIn", "Post", "How I set my rates", "", "", "", "Drafting")], 4):
    for c, x in zip([1, 3, 4, 5, 6, 7, 8, 9], row): cc.cell(r, c, dt.date.fromisoformat(x) if c == 1 else (x or None))
for st_, col in [("Posted", "D3F9D8"), ("Scheduled", "DBE4FF"), ("Drafting", "FFF3BF")]:
    cc.conditional_formatting.add("I4:I500", CellIsRule(operator="equal", formula=[f'"{st_}"'], fill=PatternFill("solid", fgColor=col)))
db = wb.create_sheet("Dashboard", 0); title(db, "Content dashboard", "Updates from the Calendar tab.")
header(db, ["Platform", "Planned", "Posted", "Avg likes", "Avg comments"], [14, 10, 10, 11, 13])
for i, p in enumerate(["Instagram", "TikTok", "LinkedIn", "X", "Facebook", "YouTube", "Pinterest", "Threads"], 4):
    db[f"A{i}"] = p; db[f"B{i}"] = f"=COUNTIF(Calendar!C:C,A{i})"; db[f"C{i}"] = f'=COUNTIFS(Calendar!C:C,A{i},Calendar!I:I,"Posted")'
    db[f"D{i}"] = f'=IFERROR(AVERAGEIFS(Calendar!J:J,Calendar!C:C,A{i},Calendar!I:I,"Posted"),"")'; db[f"E{i}"] = f'=IFERROR(AVERAGEIFS(Calendar!K:K,Calendar!C:C,A{i},Calendar!I:I,"Posted"),"")'
    db[f"D{i}"].number_format = db[f"E{i}"].number_format = "0"
bc = BarChart(); bc.title = "Posts by platform"; bc.height = 7; bc.width = 15
bc.add_data(Reference(db, min_col=2, min_row=3, max_col=3, max_row=11), titles_from_data=True); bc.set_categories(Reference(db, min_col=1, min_row=4, max_row=11)); db.add_chart(bc, "G3")
idb = wb.create_sheet("Idea bank"); title(idb, "Idea bank", "Park post ideas here, then move them to the calendar.")
header(idb, ["Idea", "Pillar", "Best platform", "Notes"], [40, 16, 16, 40]); dv(idb, '"Educate,Inspire,Entertain,Promote,Behind the scenes"', "B4:B300")
howto(wb, C, ["1. Add each planned post on Calendar with its date, platform and format. The weekday fills in.", "2. Move Status from Idea to Drafting, Scheduled and Posted. Rows change colour.",
  "3. After posting, add likes, comments and shares. Dashboard shows what's working per platform.", "4. Keep a backlog of ideas on Idea bank.", "Works in Google Sheets and Excel."])
wb.save(OUT / "Social-Media-Content-Calendar.xlsx")

# 6. 52-week savings challenge
C = "1C7ED6"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Challenge"
title(ws, "52-Week Savings Challenge", "Save a little more each week. Tick each week when you've saved it.")
ws["A3"] = "Starting amount (week 1)"; ws["B3"] = 1; ws["A4"] = "Increase each week by"; ws["B4"] = 1; ws["A5"] = "Order"; ws["B5"] = "Smallest first"
dv(ws, '"Smallest first,Biggest first"', "B5")
for r in (3, 4, 5): ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
ws.column_dimensions["A"].width = 26; ws.column_dimensions["B"].width = 16
header(ws, ["Week", "Save this week", "Done? (type x)", "Running total", "Date saved"], [26, 16, 15, 15, 13], row=7)
for w in range(1, 53):
    r = 7 + w; ws[f"A{r}"] = w
    ws[f"B{r}"] = f'=IF($B$5="Smallest first",$B$3+(A{r}-1)*$B$4,$B$3+(52-A{r})*$B$4)'
    ws[f"D{r}"] = f'=SUMIFS($B$8:B{r},$C$8:C{r},"x")'; ws[f"B{r}"].number_format = ws[f"D{r}"].number_format = M; ws[f"E{r}"].number_format = "yyyy-mm-dd"
ws.conditional_formatting.add("A8:E59", FormulaRule(formula=['LOWER($C8)="x"'], fill=PatternFill("solid", fgColor="D0EBFF")))
ws["G7"] = "Progress"; ws["G7"].font = Font(bold=True, size=12, color=C)
for r, (k, f) in enumerate([("Goal at week 52", "=SUM(B8:B59)"), ("Saved so far", '=SUMIFS(B8:B59,C8:C59,"x")'), ("Weeks done", '=COUNTIF(C8:C59,"x")'), ("% complete", "=IFERROR(H9/H8,0)")], 8):
    ws[f"G{r}"] = k; ws[f"H{r}"] = f; ws[f"H{r}"].number_format = "0%" if r == 11 else M; ws[f"G{r}"].font = Font(bold=True)
ws.column_dimensions["G"].width = 18; ws.column_dimensions["H"].width = 14
ws.conditional_formatting.add("H11", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="74C0FC"))
for r in (8, 9, 10): ws[f"C{r}"] = "x"
howto(wb, C, ["1. Set the starting amount and weekly increase (the classic challenge is 1 and 1, which saves 1,378 in a year).",
  "2. Choose Biggest first if you'd rather start with the large amounts while motivation is high.", "3. Type x in Done each week. The row turns blue and your progress updates.", "Works in Google Sheets and Excel."])
wb.save(OUT / "52-Week-Savings-Challenge.xlsx")

# 7. Invoice template
C = "0B6E4F"; title, header = kit(C); wb = Workbook(); iv = wb.active; iv.title = "Invoice"
iv.column_dimensions["A"].width = 44; iv.column_dimensions["B"].width = 10; iv.column_dimensions["C"].width = 14; iv.column_dimensions["D"].width = 16
iv["A1"] = "INVOICE"; iv["A1"].font = Font(bold=True, size=26, color=C)
for r, (k, v) in enumerate([("Invoice #", "INV-001"), ("Date", dt.date(2026, 1, 15)), ("Due date", "=C3+14")], 2):
    iv[f"B{r}"] = k; iv[f"C{r}"] = v; iv[f"B{r}"].font = Font(bold=True, color="777777"); iv[f"C{r}"].number_format = "yyyy-mm-dd"; iv[f"C{r}"].fill = SOFT
iv["A3"] = "Your Business Name"; iv["A3"].font = Font(bold=True, size=12); iv["A4"] = "Street, City, Postcode"; iv["A5"] = "you@example.com · Tax ID 000000"
iv["A7"] = "BILL TO"; iv["A7"].font = Font(bold=True, size=9, color="888888"); iv["A8"] = "Client Name"; iv["A8"].font = Font(bold=True); iv["A9"] = "Client address"
for i, c in enumerate(["Description", "Qty", "Unit price", "Amount"], 1):
    x = iv.cell(11, i, c); x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=C)
for r in range(12, 24):
    iv[f"D{r}"] = f'=IF(B{r}="","",B{r}*C{r})'; iv[f"C{r}"].number_format = iv[f"D{r}"].number_format = M
    iv[f"A{r}"].border = iv[f"B{r}"].border = iv[f"C{r}"].border = iv[f"D{r}"].border = Border(bottom=Side(style="thin", color="E5E5E5"))
iv["A12"] = "Website design"; iv["B12"] = 1; iv["C12"] = 1800; iv["A13"] = "Hosting setup"; iv["B13"] = 2; iv["C13"] = 75
for r, (k, f) in enumerate([("Subtotal", "=SUM(D12:D23)"), ("Tax rate", 0.2), ("Tax", "=D25*D26"), ("TOTAL DUE", "=D25+D27")], 25):
    iv[f"C{r}"] = k; iv[f"D{r}"] = f; iv[f"C{r}"].font = Font(bold=True); iv[f"D{r}"].number_format = "0%" if r == 26 else M
iv["D28"].font = Font(bold=True, size=13, color=C); iv["C28"].font = Font(bold=True, size=13)
iv["A30"] = "Payment details"; iv["A30"].font = Font(bold=True); iv["A31"] = "Bank: Example Bank · IBAN: GB00 0000 0000 0000 00"; iv["A32"] = "Please pay within 14 days. Thank you!"
iv.print_area = "A1:D33"; iv.page_setup.fitToWidth = 1; iv.sheet_properties.pageSetUpPr.fitToPage = True
lg = wb.create_sheet("Invoice log"); title(lg, "Invoice log", "Record each invoice you send.")
header(lg, ["Invoice #", "Client", "Date", "Due", "Amount", "Status", "Paid on"], [12, 24, 12, 12, 12, 10, 12])
dv(lg, '"Sent,Paid,Overdue"', "F4:F500")
for r in range(4, 501): lg[f"E{r}"].number_format = M; lg[f"C{r}"].number_format = lg[f"D{r}"].number_format = lg[f"G{r}"].number_format = "yyyy-mm-dd"
lg["I3"] = "Unpaid total"; lg["J3"] = '=SUMIFS(E:E,F:F,"<>Paid")'; lg["I3"].font = Font(bold=True); lg["J3"].number_format = M; lg.column_dimensions["I"].width = 14
howto(wb, C, ["1. Replace your business details and client details at the top of the Invoice tab.", "2. Add line items (quantity and unit price). Amounts, tax and total calculate automatically.",
  "3. Change the tax rate in D26 (set 0% if you don't charge tax).", "4. Export: File > Download > PDF (Google Sheets) or File > Save as PDF (Excel). It fits on one page.",
  "5. Duplicate the Invoice tab for each new invoice and record it on Invoice log.", "Works in Google Sheets and Excel."])
wb.save(OUT / "Invoice-Template.xlsx")
print("saved 7")
