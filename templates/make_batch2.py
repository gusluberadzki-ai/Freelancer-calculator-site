"""Round 6 spreadsheet products into products/. Run: python3 make_batch2.py"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, DataBarRule, FormulaRule
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter as L
import pathlib, datetime as dt
OUT = pathlib.Path(__file__).parent / "products"; OUT.mkdir(exist_ok=True)
M = "#,##0.00"; SOFT = PatternFill("solid", fgColor="EEF4F1")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

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
def bold_label(ws, rng):
    for r in rng: ws[f"A{r}"].font = Font(bold=True)

# 1. Small business bookkeeping
C = "2F5D8A"; title, header = kit(C); wb = Workbook()
tx = wb.active; tx.title = "Transactions"
title(tx, "Transactions", "Log every sale and expense. The Summary tab builds your profit & loss.")
header(tx, ["Date", "Description", "Type", "Category", "Amount", "Month (auto)"], [12, 34, 11, 22, 13, 12])
inc_cats = ["Sales", "Services", "Other income"]
exp_cats = ["Advertising", "Software & subscriptions", "Supplies", "Travel", "Phone & internet", "Rent", "Fees & bank charges", "Professional services", "Equipment", "Other expense"]
dv(tx, '"Income,Expense"', "C4:C1000")
cl = wb.create_sheet("Categories"); cl["A1"] = "Income categories"; cl["B1"] = "Expense categories"
for i, c in enumerate(inc_cats, 2): cl[f"A{i}"] = c
for i, c in enumerate(exp_cats, 2): cl[f"B{i}"] = c
cl.column_dimensions["A"].width = 22; cl.column_dimensions["B"].width = 28
dv(tx, "=Categories!$A$2:$B$20", "D4:D1000")
y = dt.date.today().year
sample = [(dt.date(y, 1, 5), "Logo design for client", "Income", "Services", 850), (dt.date(y, 1, 8), "Design software", "Expense", "Software & subscriptions", 54.99),
          (dt.date(y, 1, 20), "Website build", "Income", "Services", 2400), (dt.date(y, 2, 2), "Facebook ads", "Expense", "Advertising", 120),
          (dt.date(y, 2, 14), "Template sales", "Income", "Sales", 310), (dt.date(y, 2, 28), "Phone bill", "Expense", "Phone & internet", 35),
          (dt.date(y, 3, 3), "New monitor", "Expense", "Equipment", 280), (dt.date(y, 3, 21), "Consulting", "Income", "Services", 1200)]
for r, s in enumerate(sample, 4):
    for c, x in enumerate(s, 1): tx.cell(r, c, x)
for r in range(4, 1001):
    tx[f"A{r}"].number_format = "yyyy-mm-dd"; tx[f"E{r}"].number_format = M; tx[f"F{r}"] = f'=IF(A{r}="","",MONTH(A{r}))'
sm = wb.create_sheet("Summary", 0); title(sm, "Profit & loss", "Updates automatically from the Transactions tab.")
header(sm, ["Category"] + MONTHS + ["Total"], [28] + [11] * 12 + [13], row=4)
r = 5; sm.cell(r, 1, "INCOME").font = Font(bold=True, color=C); r += 1; inc_start = r
for c in inc_cats:
    sm.cell(r, 1, c)
    for m in range(1, 13): sm.cell(r, m + 1, f'=SUMIFS(Transactions!$E:$E,Transactions!$C:$C,"Income",Transactions!$D:$D,$A{r},Transactions!$F:$F,{m})').number_format = M
    sm.cell(r, 14, f"=SUM(B{r}:M{r})").number_format = M; r += 1
sm.cell(r, 1, "Total income").font = Font(bold=True); inc_tot = r
for c in range(2, 15): sm.cell(r, c, f"=SUM({L(c)}{inc_start}:{L(c)}{r-1})").number_format = M
r += 2; sm.cell(r, 1, "EXPENSES").font = Font(bold=True, color=C); r += 1; exp_start = r
for c in exp_cats:
    sm.cell(r, 1, c)
    for m in range(1, 13): sm.cell(r, m + 1, f'=SUMIFS(Transactions!$E:$E,Transactions!$C:$C,"Expense",Transactions!$D:$D,$A{r},Transactions!$F:$F,{m})').number_format = M
    sm.cell(r, 14, f"=SUM(B{r}:M{r})").number_format = M; r += 1
sm.cell(r, 1, "Total expenses").font = Font(bold=True); exp_tot = r
for c in range(2, 15): sm.cell(r, c, f"=SUM({L(c)}{exp_start}:{L(c)}{r-1})").number_format = M
r += 2; sm.cell(r, 1, "NET PROFIT").font = Font(bold=True, size=13); net = r
for c in range(2, 15):
    x = sm.cell(r, c, f"={L(c)}{inc_tot}-{L(c)}{exp_tot}"); x.number_format = M; x.font = Font(bold=True); x.fill = SOFT
r += 1; sm.cell(r, 1, "Profit margin")
for c in range(2, 15): sm.cell(r, c, f'=IF({L(c)}{inc_tot}=0,"",{L(c)}{net}/{L(c)}{inc_tot})').number_format = "0%"
r += 2; sm.cell(r, 1, "Set aside for tax"); sm.cell(r, 2, 0.25).number_format = "0%"; sm.cell(r, 2).fill = SOFT
sm.cell(r + 1, 1, "Tax to set aside (year)"); sm.cell(r + 1, 2, f"=MAX(0,N{net}*B{r})").number_format = M
sm.conditional_formatting.add(f"B{net}:N{net}", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
ch = BarChart(); ch.title = "Income vs expenses"; ch.height = 7; ch.width = 22
ch.add_data(Reference(sm, min_col=1, max_col=13, min_row=inc_tot), from_rows=True, titles_from_data=True)
ch.add_data(Reference(sm, min_col=1, max_col=13, min_row=exp_tot), from_rows=True, titles_from_data=True)
ch.set_categories(Reference(sm, min_col=2, max_col=13, min_row=4)); sm.add_chart(ch, f"A{r+4}")
howto(wb, C, ["1. Go to Transactions and delete the sample rows.", "2. Add each sale or expense: date, description, Income or Expense, and a category from the list.",
              "3. The Summary tab totals everything by month and category, and shows your net profit and margin.",
              "4. Set your tax rate on the Summary tab to see how much to put aside.", "5. Rename or add categories on the Categories tab (keep them in columns A and B)."])
wb.save(OUT / "Small-Business-Bookkeeping.xlsx")

# 2. Net worth tracker
C = "5B3FA0"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Net worth"
title(ws, "Net Worth Tracker", "Update your balances once a month and watch your net worth grow.")
header(ws, ["Account", "Type"] + MONTHS, [26, 12] + [12] * 12)
rows = [("Current account", "Asset", 2500), ("Savings", "Asset", 8000), ("Pension", "Asset", 22000), ("Investments (ISA / brokerage)", "Asset", 6500), ("Home value", "Asset", 0), ("Car value", "Asset", 7000),
        ("Mortgage", "Liability", 0), ("Car loan", "Liability", 5200), ("Credit card", "Liability", 1100), ("Student loan", "Liability", 14000)]
for r, (a, t, b) in enumerate(rows, 4):
    ws[f"A{r}"] = a; ws[f"B{r}"] = t
    for m in range(12): ws.cell(r, 3 + m, round(b * (1 + (0.01 if t == "Asset" else -0.02) * m)) if m < 3 and b else None).number_format = M
dv(ws, '"Asset,Liability"', "B4:B23")
ws["A25"] = "Total assets"; ws["A26"] = "Total liabilities"; ws["A27"] = "NET WORTH"; ws["A28"] = "Change from last month"
for m in range(12):
    c = L(3 + m)
    ws[f"{c}25"] = f'=IF(COUNT({c}4:{c}23)=0,"",SUMIF($B$4:$B$23,"Asset",{c}4:{c}23))'
    ws[f"{c}26"] = f'=IF(COUNT({c}4:{c}23)=0,"",SUMIF($B$4:$B$23,"Liability",{c}4:{c}23))'
    ws[f"{c}27"] = f'=IF({c}25="","",{c}25-{c}26)'
    ws[f"{c}28"] = "" if m == 0 else f'=IF(OR({c}27="",{L(2+m)}27=""),"",{c}27-{L(2+m)}27)'
    for rr in (25, 26, 27, 28): ws[f"{c}{rr}"].number_format = M
    ws[f"{c}27"].font = Font(bold=True); ws[f"{c}27"].fill = SOFT
bold_label(ws, range(25, 29)); ws["A27"].font = Font(bold=True, size=13)
ws.conditional_formatting.add("D28:N28", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B")))
ws.conditional_formatting.add("D28:N28", CellIsRule(operator="greaterThan", formula=["0"], font=Font(color="2E7D32")))
ch = LineChart(); ch.title = "Net worth"; ch.height = 7; ch.width = 22
ch.add_data(Reference(ws, min_col=1, max_col=14, min_row=27), from_rows=True, titles_from_data=True); ch.set_categories(Reference(ws, min_col=3, max_col=14, min_row=3)); ws.add_chart(ch, "A31")
howto(wb, C, ["1. List every account you own (assets) and every debt (liabilities). Choose the type in column B.", "2. Once a month, type each balance into that month's column. Enter debts as positive numbers.",
              "3. Net worth = total assets minus total liabilities. The chart and month-on-month change update automatically.", "4. Save a copy each year to keep a long-term record."])
wb.save(OUT / "Net-Worth-Tracker.xlsx")

# 3. Sinking funds tracker
C = "0F8B8D"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Sinking funds"
title(ws, "Sinking Funds Tracker", "Save a little each month for the big costs you know are coming.")
header(ws, ["Fund", "Goal", "Due date", "Saved so far", "Months left", "Save per month", "Left to save", "Progress"], [24, 12, 13, 13, 11, 14, 13, 12])
funds = [("Christmas", 600, dt.date(y, 12, 1), 150), ("Car insurance", 720, dt.date(y + 1, 3, 1), 200), ("Holiday", 2000, dt.date(y + 1, 7, 1), 400), ("Car repairs", 800, dt.date(y + 1, 6, 1), 100), ("Birthdays & gifts", 400, dt.date(y + 1, 1, 1), 50), ("Emergency fund", 5000, dt.date(y + 1, 12, 1), 1500)]
for r, f in enumerate(funds, 4):
    for c, x in enumerate(f, 1): ws.cell(r, c, x)
for r in range(4, 24):
    ws[f"C{r}"].number_format = "mmm yyyy"
    ws[f"E{r}"] = f'=IF(A{r}="","",MAX(1,DATEDIF(TODAY(),MAX(C{r},TODAY()),"m")))'
    ws[f"F{r}"] = f'=IF(A{r}="","",MAX(0,B{r}-D{r})/E{r})'; ws[f"G{r}"] = f'=IF(A{r}="","",MAX(0,B{r}-D{r}))'; ws[f"H{r}"] = f'=IF(OR(A{r}="",B{r}=0),"",MIN(1,D{r}/B{r}))'
    for c in "BDFG": ws[f"{c}{r}"].number_format = M
    ws[f"H{r}"].number_format = "0%"
ws["A25"] = "Total"; ws["B25"] = "=SUM(B4:B23)"; ws["D25"] = "=SUM(D4:D23)"; ws["F25"] = "=SUM(F4:F23)"; ws["G25"] = "=SUM(G4:G23)"
for c in "BDFG": ws[f"{c}25"].number_format = M; ws[f"{c}25"].font = Font(bold=True)
ws["A25"].font = Font(bold=True); ws["F25"].fill = SOFT
ws.conditional_formatting.add("H4:H23", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="0F8B8D"))
lg = wb.create_sheet("Deposits"); title(lg, "Deposits log", "Optional: record each deposit. Totals per fund appear in column F.")
header(lg, ["Date", "Fund", "Amount", "Note", "", "Total by fund"], [12, 24, 12, 30, 3, 16])
dv(lg, "='Sinking funds'!$A$4:$A$23", "B4:B500")
for r in range(4, 24): lg[f"E{r}"] = f"='Sinking funds'!A{r}"; lg[f"E{r}"].font = Font(color="999999"); lg[f"F{r}"] = f'=IF(E{r}=0,"",SUMIF($B$4:$B$500,E{r},$C$4:$C$500))'; lg[f"F{r}"].number_format = M
lg.column_dimensions["E"].width = 22
howto(wb, C, ["1. List each fund with its goal and the date you need the money by.", "2. Enter how much you've saved so far. The tracker tells you how much to save each month to hit every goal on time.",
              "3. The total in 'Save per month' is the amount to transfer to your sinking-fund account each payday.", "4. Optional: log each deposit on the Deposits tab and copy the totals back to 'Saved so far'."])
wb.save(OUT / "Sinking-Funds-Tracker.xlsx")

# 4. Job application tracker
C = "C2410C"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Applications"
title(ws, "Job Application Tracker", "Keep every application, interview and follow-up in one place.")
header(ws, ["Company", "Role", "Location / remote", "Salary", "Date applied", "Source", "Status", "Contact", "Next step", "Follow-up date", "Days since applied", "Notes"], [20, 24, 16, 12, 13, 14, 14, 18, 22, 14, 12, 30])
st = "Wishlist,Applied,Phone screen,Interview,Final round,Offer,Rejected,Withdrawn"
dv(ws, f'"{st}"', "G4:G500"); dv(ws, '"LinkedIn,Indeed,Company site,Referral,Recruiter,Other"', "F4:F500")
today = dt.date.today()
smp = [("Acme Ltd", "Product Designer", "Remote", 55000, today - dt.timedelta(days=12), "LinkedIn", "Interview", "Sam (HR)", "Portfolio review", today + dt.timedelta(days=3)),
       ("Northwind", "UX Designer", "London", 50000, today - dt.timedelta(days=20), "Company site", "Applied", "", "Follow up by email", today - dt.timedelta(days=1)),
       ("Globex", "Senior Designer", "Hybrid", 62000, today - dt.timedelta(days=30), "Referral", "Rejected", "Priya", "", None)]
for r, s in enumerate(smp, 4):
    for c, x in enumerate(s, 1): ws.cell(r, c, x)
for r in range(4, 501):
    ws[f"E{r}"].number_format = ws[f"J{r}"].number_format = "yyyy-mm-dd"; ws[f"D{r}"].number_format = "#,##0"
    ws[f"K{r}"] = f'=IF(E{r}="","",TODAY()-E{r})'
ws.conditional_formatting.add("A4:L500", FormulaRule(formula=['$G4="Offer"'], fill=PatternFill("solid", fgColor="D3F9D8")))
ws.conditional_formatting.add("A4:L500", FormulaRule(formula=['OR($G4="Rejected",$G4="Withdrawn")'], font=Font(color="999999")))
ws.conditional_formatting.add("J4:J500", FormulaRule(formula=['AND($J4<>"",$J4<=TODAY(),$G4<>"Rejected",$G4<>"Withdrawn",$G4<>"Offer")'], fill=PatternFill("solid", fgColor="FFE3E3"), font=Font(bold=True, color="C0392B")))
db = wb.create_sheet("Dashboard", 0); title(db, "Job search dashboard", "Counts update as you change each application's status.")
header(db, ["Status", "Count"], [22, 10], row=4, freeze=False)
for i, s in enumerate(st.split(","), 5):
    db[f"A{i}"] = s; db[f"B{i}"] = f'=COUNTIF(Applications!$G$4:$G$500,A{i})'
db["A14"] = "Total applications"; db["B14"] = '=COUNTA(Applications!$A$4:$A$500)'
db["A15"] = "Response rate"; db["B15"] = '=IF(B14-B5=0,"",(B14-B5-B6)/(B14-B5))'; db["B15"].number_format = "0%"
db["A16"] = "Follow-ups due"; db["B16"] = '=COUNTIFS(Applications!$J$4:$J$500,"<="&TODAY(),Applications!$G$4:$G$500,"<>Rejected",Applications!$G$4:$G$500,"<>Withdrawn",Applications!$G$4:$G$500,"<>Offer")'
bold_label(db, range(14, 17))
for r in range(14, 17): db[f"B{r}"].fill = SOFT
howto(wb, C, ["1. Add a row for each job, even ones you're only thinking about (status: Wishlist).", "2. Update the status as you hear back. Offers turn green; rejections fade out.",
              "3. Set a follow-up date. It turns red when it's due, and the Dashboard counts how many are due.", "4. The Dashboard shows how many applications are at each stage and your response rate."])
wb.save(OUT / "Job-Application-Tracker.xlsx")

# 5. Inventory tracker
C = "3D7A3A"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Inventory"
title(ws, "Inventory Tracker", "Stock levels, value and reorder alerts for a small shop.")
header(ws, ["SKU", "Item", "Category", "Supplier", "Unit cost", "Sale price", "Opening stock", "Stock in", "Stock out", "In stock", "Reorder at", "Status", "Stock value", "Margin"], [10, 24, 14, 16, 11, 11, 11, 10, 10, 10, 11, 12, 13, 10])
items = [("SKU-001", "Candle - lavender", "Candles", "WaxCo", 3.2, 12, 40), ("SKU-002", "Candle - vanilla", "Candles", "WaxCo", 3.2, 12, 25), ("SKU-003", "Soap bar - oat", "Soap", "PureSoap", 1.4, 6, 60), ("SKU-004", "Gift box", "Packaging", "BoxIt", 0.9, 4, 15)]
for r, it in enumerate(items, 4):
    for c, x in enumerate(it, 1): ws.cell(r, c, x)
    ws[f"K{r}"] = 10
mv = wb.create_sheet("Movements"); title(mv, "Stock movements", "Log stock coming in (purchases) and going out (sales). Inventory updates automatically.")
header(mv, ["Date", "SKU", "In / Out", "Quantity", "Note"], [12, 12, 10, 10, 30])
dv(mv, '"In,Out"', "C4:C2000"); dv(mv, "=Inventory!$A$4:$A$300", "B4:B2000")
mvs = [(today - dt.timedelta(days=9), "SKU-001", "Out", 18), (today - dt.timedelta(days=7), "SKU-002", "Out", 17), (today - dt.timedelta(days=5), "SKU-003", "In", 20), (today - dt.timedelta(days=2), "SKU-003", "Out", 12)]
for r, m in enumerate(mvs, 4):
    for c, x in enumerate(m, 1): mv.cell(r, c, x)
for r in range(4, 2001): mv[f"A{r}"].number_format = "yyyy-mm-dd"
for r in range(4, 301):
    ws[f"H{r}"] = f'=IF(A{r}="","",SUMIFS(Movements!$D:$D,Movements!$B:$B,A{r},Movements!$C:$C,"In"))'
    ws[f"I{r}"] = f'=IF(A{r}="","",SUMIFS(Movements!$D:$D,Movements!$B:$B,A{r},Movements!$C:$C,"Out"))'
    ws[f"J{r}"] = f'=IF(A{r}="","",G{r}+H{r}-I{r})'
    ws[f"L{r}"] = f'=IF(A{r}="","",IF(J{r}<=0,"Out of stock",IF(J{r}<=K{r},"Reorder","OK")))'
    ws[f"M{r}"] = f'=IF(A{r}="","",J{r}*E{r})'; ws[f"N{r}"] = f'=IF(OR(A{r}="",F{r}=0),"",(F{r}-E{r})/F{r})'
    for c in "EFM": ws[f"{c}{r}"].number_format = M
    ws[f"N{r}"].number_format = "0%"
ws.conditional_formatting.add("L4:L300", CellIsRule(operator="equal", formula=['"Reorder"'], fill=PatternFill("solid", fgColor="FFF3BF"), font=Font(bold=True, color="8A6D00")))
ws.conditional_formatting.add("L4:L300", CellIsRule(operator="equal", formula=['"Out of stock"'], fill=PatternFill("solid", fgColor="FFE3E3"), font=Font(bold=True, color="C0392B")))
ws["P3"] = "Total stock value"; ws["P4"] = "=SUM(M4:M300)"; ws["P4"].number_format = M; ws["P6"] = "Items to reorder"; ws["P7"] = '=COUNTIF(L4:L300,"Reorder")+COUNTIF(L4:L300,"Out of stock")'
ws.column_dimensions["P"].width = 18
for c in ("P3", "P6"): ws[c].font = Font(bold=True)
for c in ("P4", "P7"): ws[c].fill = SOFT
howto(wb, C, ["1. On Inventory, add each product with its SKU, cost, sale price, opening stock and the level at which you want to reorder.", "2. On Movements, log stock coming in and going out. Pick the SKU from the list.",
              "3. In stock, status, stock value and margin update automatically. Items to reorder turn yellow; out-of-stock items turn red.", "4. Delete the sample rows before you start."])
wb.save(OUT / "Inventory-Tracker.xlsx")

# 6. Travel planner & budget
C = "1971C2"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Budget"
title(ws, "Trip Budget", "Plan what you'll spend, then track what you actually spend.")
ws["A4"] = "Trip"; ws["B4"] = "Lisbon city break"; ws["A5"] = "Travellers"; ws["B5"] = 2; ws["A6"] = "Start date"; ws["B6"] = today + dt.timedelta(days=60); ws["A7"] = "Nights"; ws["B7"] = 4
ws["B6"].number_format = "yyyy-mm-dd"; bold_label(ws, range(4, 8))
for r in range(4, 8): ws[f"B{r}"].fill = SOFT
header(ws, ["Category", "Planned", "Actual (auto)", "Difference"], [26, 14, 14, 14], row=9, freeze=False)
cats = [("Flights / transport there", 320), ("Accommodation", 480), ("Food & drink", 360), ("Local transport", 60), ("Activities & tickets", 150), ("Shopping & souvenirs", 100), ("Insurance", 40), ("Other", 50)]
for r, (c, p) in enumerate(cats, 10):
    ws[f"A{r}"] = c; ws[f"B{r}"] = p; ws[f"C{r}"] = f"=SUMIF(Expenses!$C:$C,A{r},Expenses!$D:$D)"; ws[f"D{r}"] = f"=B{r}-C{r}"
    for x in "BCD": ws[f"{x}{r}"].number_format = M
ws["A18"] = "Total"; ws["B18"] = "=SUM(B10:B17)"; ws["C18"] = "=SUM(C10:C17)"; ws["D18"] = "=B18-C18"
ws["A19"] = "Per person"; ws["B19"] = "=B18/MAX(1,$B$5)"; ws["C19"] = "=C18/MAX(1,$B$5)"; ws["A20"] = "Per day"; ws["B20"] = "=B18/MAX(1,$B$7+1)"; ws["C20"] = "=C18/MAX(1,$B$7+1)"
for r in (18, 19, 20):
    ws[f"A{r}"].font = Font(bold=True)
    for x in "BCD": ws[f"{x}{r}"].number_format = M
ws.conditional_formatting.add("D10:D18", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
ex = wb.create_sheet("Expenses"); title(ex, "Expenses", "Log what you spend during the trip.")
header(ex, ["Date", "Description", "Category", "Amount", "Paid by"], [12, 30, 26, 12, 14]); dv(ex, "=Budget!$A$10:$A$17", "C4:C500")
for r, e in enumerate([(today + dt.timedelta(days=60), "Return flights", "Flights / transport there", 298), (today + dt.timedelta(days=60), "Dinner", "Food & drink", 64)], 4):
    for c, x in enumerate(e, 1): ex.cell(r, c, x)
for r in range(4, 501): ex[f"A{r}"].number_format = "yyyy-mm-dd"; ex[f"D{r}"].number_format = M
it = wb.create_sheet("Itinerary"); title(it, "Itinerary", "Day-by-day plan with bookings and confirmation numbers.")
header(it, ["Day", "Date", "Morning", "Afternoon", "Evening", "Bookings / confirmation"], [6, 12, 24, 24, 24, 30])
for d in range(1, 15):
    r = d + 3; it[f"A{r}"] = d; it[f"B{r}"] = f'=IF(A{r}>Budget!$B$7+1,"",Budget!$B$6+A{r}-1)'; it[f"B{r}"].number_format = "ddd d mmm"
pk = wb.create_sheet("Packing list"); title(pk, "Packing list", "Tick items off with an x as you pack.")
header(pk, ["Packed?", "Item", "Category"], [9, 30, 16])
pack = [("Passport / ID", "Documents"), ("Tickets & bookings", "Documents"), ("Travel insurance", "Documents"), ("Bank cards & cash", "Documents"), ("Phone + charger", "Tech"), ("Plug adapter", "Tech"), ("Headphones", "Tech"),
        ("Toothbrush & paste", "Toiletries"), ("Sunscreen", "Toiletries"), ("Medication", "Toiletries"), ("T-shirts", "Clothes"), ("Underwear & socks", "Clothes"), ("Jacket", "Clothes"), ("Comfortable shoes", "Clothes"), ("Swimwear", "Clothes"), ("Reusable water bottle", "Other")]
for r, (i, c) in enumerate(pack, 4): pk[f"B{r}"] = i; pk[f"C{r}"] = c
pk["E3"] = "Packed"; pk["E4"] = '=COUNTIF(A4:A100,"x")&" of "&COUNTA(B4:B100)'; pk["E3"].font = Font(bold=True)
pk.conditional_formatting.add("A4:C100", FormulaRule(formula=['LOWER($A4)="x"'], font=Font(strike=True, color="999999")))
howto(wb, C, ["1. On Budget, enter the trip details and your planned spend per category.", "2. During the trip, log each expense on Expenses. Actual spend and the difference update automatically; overspends turn red.",
              "3. Plan each day on Itinerary. Dates fill in from your start date.", "4. Use Packing list: type x in the first column when an item is packed."])
wb.save(OUT / "Travel-Planner-Budget.xlsx")

# 7. Weight loss / fitness tracker
C = "D6336C"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Tracker"
title(ws, "Weight Loss Tracker", "Log your weight and see progress, BMI and your goal date.")
ws["A4"] = "Height (cm)"; ws["B4"] = 170; ws["A5"] = "Start weight (kg)"; ws["B5"] = "=IFERROR(INDEX(Log!$B$4:$B$400,1),\"\")"; ws["A6"] = "Goal weight (kg)"; ws["B6"] = 68
ws["A7"] = "Current weight"; ws["B7"] = '=IFERROR(LOOKUP(2,1/(Log!$B$4:$B$400<>""),Log!$B$4:$B$400),"")'
ws["A8"] = "Lost so far"; ws["B8"] = '=IFERROR(B5-B7,"")'; ws["A9"] = "Left to goal"; ws["B9"] = '=IFERROR(MAX(0,B7-B6),"")'
ws["A10"] = "Progress"; ws["B10"] = '=IFERROR(MIN(1,MAX(0,(B5-B7)/(B5-B6))),"")'; ws["B10"].number_format = "0%"
ws["A11"] = "Current BMI"; ws["B11"] = '=IFERROR(B7/(B4/100)^2,"")'; ws["B11"].number_format = "0.0"
ws["A12"] = "Average loss per week"; ws["B12"] = '=IFERROR((B5-B7)/((LOOKUP(2,1/(Log!$B$4:$B$400<>""),Log!$A$4:$A$400)-Log!$A$4)/7),"")'; ws["B12"].number_format = "0.00"
ws["A13"] = "Estimated goal date"; ws["B13"] = '=IFERROR(IF(B12<=0,"Keep going!",LOOKUP(2,1/(Log!$B$4:$B$400<>""),Log!$A$4:$A$400)+B9/B12*7),"")'; ws["B13"].number_format = "d mmm yyyy"
for r in range(4, 14): ws[f"A{r}"].font = Font(bold=True); ws[f"B{r}"].fill = SOFT
for r in (5, 6, 7, 8, 9): ws[f"B{r}"].number_format = "0.0"
ws.column_dimensions["A"].width = 26; ws.column_dimensions["B"].width = 16
lg = wb.create_sheet("Log"); title(lg, "Weigh-in log", "Weigh yourself at the same time each week and add a row.")
header(lg, ["Date", "Weight (kg)", "Change", "Waist (cm)", "Steps / day", "Workouts", "Notes"], [12, 12, 10, 11, 12, 10, 30])
start = today - dt.timedelta(days=42)
for i, w in enumerate([78.0, 77.2, 76.9, 76.1, 75.8, 75.0, 74.6]):
    r = 4 + i; lg[f"A{r}"] = start + dt.timedelta(days=7 * i); lg[f"B{r}"] = w; lg[f"D{r}"] = 92 - i * 0.6
for r in range(4, 401):
    lg[f"A{r}"].number_format = "yyyy-mm-dd"; lg[f"C{r}"] = "" if r == 4 else f'=IF(OR(B{r}="",B{r-1}=""),"",B{r}-B{r-1})'; lg[f"C{r}"].number_format = "+0.0;-0.0;0.0"
lg.conditional_formatting.add("C5:C400", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="2E7D32")))
lg.conditional_formatting.add("C5:C400", CellIsRule(operator="greaterThan", formula=["0"], font=Font(color="C0392B")))
ch = LineChart(); ch.title = "Weight"; ch.height = 7; ch.width = 18; ch.add_data(Reference(lg, min_col=2, min_row=3, max_row=60), titles_from_data=True); ch.set_categories(Reference(lg, min_col=1, min_row=4, max_row=60)); ch.x_axis.number_format = "d mmm"; ws.add_chart(ch, "D4")
howto(wb, C, ["1. On Tracker, enter your height and goal weight.", "2. On Log, add a row each week with the date and your weight. Delete the sample rows first.",
              "3. Your progress, BMI, average weekly loss and estimated goal date update automatically.", "BMI is a rough guide and doesn't account for muscle. Talk to a doctor before big changes to diet or exercise."])
wb.save(OUT / "Weight-Loss-Tracker.xlsx")

# 8. Rental property tracker
C = "7A4E2D"; title, header = kit(C); wb = Workbook(); ws = wb.active; ws.title = "Properties"
title(ws, "Rental Property Tracker", "Income, expenses, cash flow and yield for each rental.")
header(ws, ["Property", "Purchase price", "Monthly rent", "Mortgage / month", "Income (year)", "Expenses (year)", "Net cash flow", "Gross yield", "Net yield", "Occupied?"], [22, 14, 13, 15, 14, 14, 14, 11, 11, 11])
props = [("12 Oak Street", 210000, 1150, 620, "Yes"), ("Flat 4, River Court", 165000, 950, 480, "Yes")]
for r, p in enumerate(props, 4):
    for c, x in enumerate(p[:4], 1): ws.cell(r, c, x)
    ws[f"J{r}"] = p[4]
dv(ws, '"Yes,No"', "J4:J23")
tr = wb.create_sheet("Transactions"); title(tr, "Transactions", "Record rent received and every expense, per property.")
header(tr, ["Date", "Property", "Type", "Category", "Amount", "Note"], [12, 22, 10, 20, 12, 28])
dv(tr, "=Properties!$A$4:$A$23", "B4:B3000"); dv(tr, '"Income,Expense"', "C4:C3000")
dv(tr, '"Rent,Deposit,Mortgage interest,Repairs,Insurance,Letting agent,Service charge,Utilities,Council tax,Legal & accounting,Other"', "D4:D3000")
tsm = []
for m in range(1, 4):
    tsm += [(dt.date(y, m, 1), "12 Oak Street", "Income", "Rent", 1150), (dt.date(y, m, 1), "Flat 4, River Court", "Income", "Rent", 950), (dt.date(y, m, 1), "12 Oak Street", "Expense", "Mortgage interest", 620), (dt.date(y, m, 1), "Flat 4, River Court", "Expense", "Mortgage interest", 480)]
tsm += [(dt.date(y, 2, 12), "12 Oak Street", "Expense", "Repairs", 240), (dt.date(y, 3, 5), "Flat 4, River Court", "Expense", "Insurance", 180)]
for r, t in enumerate(tsm, 4):
    for c, x in enumerate(t, 1): tr.cell(r, c, x)
for r in range(4, 3001): tr[f"A{r}"].number_format = "yyyy-mm-dd"; tr[f"E{r}"].number_format = M
for r in range(4, 24):
    ws[f"E{r}"] = f'=IF(A{r}="","",SUMIFS(Transactions!$E:$E,Transactions!$B:$B,A{r},Transactions!$C:$C,"Income"))'
    ws[f"F{r}"] = f'=IF(A{r}="","",SUMIFS(Transactions!$E:$E,Transactions!$B:$B,A{r},Transactions!$C:$C,"Expense"))'
    ws[f"G{r}"] = f'=IF(A{r}="","",E{r}-F{r})'; ws[f"H{r}"] = f'=IF(OR(A{r}="",B{r}=0),"",C{r}*12/B{r})'; ws[f"I{r}"] = f'=IF(OR(A{r}="",B{r}=0),"",G{r}/B{r})'
    for c in "BCDEFG": ws[f"{c}{r}"].number_format = M
    for c in "HI": ws[f"{c}{r}"].number_format = "0.0%"
ws["A25"] = "Portfolio total"; ws["A25"].font = Font(bold=True)
for c in "BCDEFG": ws[f"{c}25"] = f"=SUM({c}4:{c}23)"; ws[f"{c}25"].number_format = M; ws[f"{c}25"].font = Font(bold=True)
ws["H25"] = '=IF(B25=0,"",C25*12/B25)'; ws["I25"] = '=IF(B25=0,"",G25/B25)'; ws["H25"].number_format = ws["I25"].number_format = "0.0%"
ws.conditional_formatting.add("G4:G25", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
howto(wb, C, ["1. On Properties, add each rental with its purchase price, monthly rent and mortgage payment.", "2. On Transactions, record rent received and every expense. Pick the property and category from the lists.",
              "3. Yearly income, expenses, net cash flow and yields update automatically, per property and for the whole portfolio.", "4. Start a new copy each tax year so your records line up with your tax return. This isn't tax advice."])
wb.save(OUT / "Rental-Property-Tracker.xlsx")
print("built 8")
