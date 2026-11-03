"""Builds Client-CRM-Pipeline.xlsx and Monthly-Budget-Planner.xlsx."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Side, Border
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, DataBarRule
from openpyxl.chart import PieChart, BarChart, Reference
from openpyxl.utils import get_column_letter as L
import pathlib, datetime as d
OUT = pathlib.Path(__file__).parent / "products"
G = "0B6E4F"; SOFT = "E3F2EC"; GREY = "F3F3F1"
H = Font(bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor=G)
def title(ws, t, s):
    ws["A1"] = t; ws["A1"].font = Font(bold=True, size=18, color=G); ws["A2"] = s; ws["A2"].font = Font(italic=True, color="777777")
def header(ws, cols, widths, row=3):
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        x = ws.cell(row, i, c); x.font = H; x.fill = HF; x.alignment = Alignment(horizontal="center", wrap_text=True)
        ws.column_dimensions[L(i)].width = w
    ws.freeze_panes = ws.cell(row + 1, 1)
def dv(ws, formula, rng):
    v = DataValidation(type="list", formula1=formula, allow_blank=True); ws.add_data_validation(v); v.add(rng)
def howto(wb, lines):
    hw = wb.create_sheet("How to use"); title(hw, "How to use", "")
    for i, t in enumerate(lines, 3): hw.cell(i, 1, t)
    hw.column_dimensions["A"].width = 110

# ---------- Client CRM & pipeline ----------
wb = Workbook(); cl = wb.active; cl.title = "Clients"
title(cl, "Clients", "Everyone you work with or want to work with.")
header(cl, ["Client", "Contact name", "Email", "Phone", "Source", "Status", "Hourly rate", "Total billed", "Last contact", "Next follow-up", "Notes"], [22, 18, 26, 15, 14, 12, 12, 14, 14, 15, 34])
dv(cl, '"Referral,Website,LinkedIn,Upwork,Cold outreach,Social media,Other"', "E4:E500")
dv(cl, '"Lead,Active,Past,Lost"', "F4:F500")
for r in range(4, 501):
    cl[f"H{r}"] = f'=IF(A{r}="","",SUMIFS(Projects!$F:$F,Projects!$A:$A,A{r},Projects!$D:$D,"Paid"))'
    for c in "IJ": cl[f"{c}{r}"].number_format = "yyyy-mm-dd"
    cl[f"G{r}"].number_format = cl[f"H{r}"].number_format = "#,##0"
cl.conditional_formatting.add("J4:J500", CellIsRule(operator="lessThanOrEqual", formula=["TODAY()"], fill=PatternFill("solid", fgColor="FDE2CF")))
for r, row in enumerate([("Acme Ltd", "Sam Lee", "sam@acme.example", "", "Referral", "Active", 80, None, "2026-10-28", "2026-11-10", "Wants a site refresh in Q1"),
                         ("Northwind", "Priya Shah", "priya@northwind.example", "", "LinkedIn", "Lead", 70, None, "2026-10-30", "2026-11-04", "Sent proposal")], 4):
    for c, v in enumerate(row, 1):
        if c == 8: continue
        cl.cell(r, c, d.date.fromisoformat(v) if c in (9, 10) and v else v)
pj = wb.create_sheet("Projects")
title(pj, "Projects & pipeline", "Every quote and project, from first enquiry to paid.")
header(pj, ["Client", "Project", "Stage date", "Stage", "Probability", "Value", "Weighted value", "Deadline", "Notes"], [22, 28, 13, 14, 12, 12, 15, 13, 34])
dv(pj, "=Clients!$A$4:$A$500", "A4:A500")
dv(pj, '"Enquiry,Proposal sent,Negotiating,Won,In progress,Delivered,Paid,Lost"', "D4:D500")
for r in range(4, 501):
    pj[f"E{r}"] = f'=IFERROR(CHOOSE(MATCH(D{r},{{"Enquiry","Proposal sent","Negotiating","Won","In progress","Delivered","Paid","Lost"}},0),0.1,0.3,0.6,0.9,1,1,1,0),"")'
    pj[f"G{r}"] = f'=IF(OR(F{r}="",E{r}=""),"",F{r}*E{r})'
    pj[f"E{r}"].number_format = "0%"; pj[f"F{r}"].number_format = pj[f"G{r}"].number_format = "#,##0"
    pj[f"C{r}"].number_format = pj[f"H{r}"].number_format = "yyyy-mm-dd"
for r, row in enumerate([("Acme Ltd", "Website refresh", "2026-10-01", "Paid", None, 3200, None, "2026-10-20", ""),
                         ("Acme Ltd", "Monthly care plan", "2026-10-21", "In progress", None, 750, None, "", ""),
                         ("Northwind", "New brand site", "2026-10-30", "Proposal sent", None, 5000, None, "2026-12-15", "")], 4):
    for c, v in enumerate(row, 1):
        if c in (5, 7): continue
        pj.cell(r, c, d.date.fromisoformat(v) if c in (3, 8) and v else v)
db = wb.create_sheet("Pipeline", 0)
title(db, "Pipeline dashboard", "Updates automatically from the Projects tab.")
header(db, ["Stage", "Projects", "Total value", "Weighted value"], [18, 12, 16, 16])
stages = ["Enquiry", "Proposal sent", "Negotiating", "Won", "In progress", "Delivered", "Paid", "Lost"]
for i, s in enumerate(stages, 4):
    db[f"A{i}"] = s; db[f"B{i}"] = f'=COUNTIF(Projects!$D:$D,A{i})'
    db[f"C{i}"] = f'=SUMIFS(Projects!$F:$F,Projects!$D:$D,A{i})'; db[f"D{i}"] = f'=SUMIFS(Projects!$G:$G,Projects!$D:$D,A{i})'
    for c in "CD": db[f"{c}{i}"].number_format = "#,##0"
    if i % 2: [setattr(db[f"{c}{i}"], "fill", PatternFill("solid", fgColor=GREY)) for c in "ABCD"]
db["F4"] = "Open pipeline (weighted)"; db["G4"] = "=SUM(D4:D6)"
db["F5"] = "Won, not yet paid"; db["G5"] = "=SUM(C7:C9)"
db["F6"] = "Win rate"; db["G6"] = '=IFERROR(SUM(B7:B10)/(SUM(B7:B10)+B11),"")'; db["G6"].number_format = "0%"
db["F7"] = "Follow-ups due"; db["G7"] = '=COUNTIFS(Clients!J:J,"<="&TODAY(),Clients!J:J,"<>")'
for r in range(4, 8): db[f"F{r}"].font = Font(bold=True); db[f"G{r}"].number_format = db[f"G{r}"].number_format if r in (6, 7) else "#,##0"
db.column_dimensions["F"].width = 26; db.column_dimensions["G"].width = 14
db.conditional_formatting.add("C4:C11", DataBarRule(start_type="min", end_type="max", color="4CC29A"))
ch = BarChart(); ch.title = "Value by stage"; ch.height = 7.5; ch.width = 16; ch.legend = None
ch.add_data(Reference(db, min_col=3, min_row=3, max_row=11), titles_from_data=True); ch.set_categories(Reference(db, min_col=1, min_row=4, max_row=11)); db.add_chart(ch, "A14")
howto(wb, ["1. Add each client on the Clients tab. Set a Next follow-up date: it turns orange when it's due.",
  "2. Add every quote or project on the Projects tab and pick its Stage from the dropdown. Probability fills in automatically.",
  "3. The Pipeline tab shows how much work is in the pipeline, what's won but unpaid, your win rate and follow-ups due.",
  "4. Total billed per client on the Clients tab adds up every project marked Paid.",
  "Delete the sample rows before you start. Works in Google Sheets (File > Import) and Excel."])
wb.save(OUT / "Client-CRM-Pipeline.xlsx")

# ---------- Monthly budget planner ----------
wb = Workbook(); st = wb.active; st.title = "Setup"
title(st, "Budget setup", "Set your monthly budget for each category once. Edit the names freely.")
header(st, ["Category", "Type", "Monthly budget"], [26, 12, 16])
cats = [("Salary / income", "Income", 4000), ("Side income", "Income", 300), ("Rent / mortgage", "Fixed", 1200), ("Utilities", "Fixed", 180), ("Phone & internet", "Fixed", 60),
        ("Insurance", "Fixed", 90), ("Subscriptions", "Fixed", 40), ("Groceries", "Variable", 450), ("Eating out", "Variable", 150), ("Transport", "Variable", 160),
        ("Shopping", "Variable", 150), ("Health", "Variable", 50), ("Fun & hobbies", "Variable", 100), ("Gifts", "Variable", 40), ("Savings", "Savings", 600), ("Investing", "Savings", 200), ("Debt repayment", "Savings", 0)]
for i, (c, t, b) in enumerate(cats, 4):
    st.cell(i, 1, c); st.cell(i, 2, t); st.cell(i, 3, b).number_format = "#,##0"
dv(st, '"Income,Fixed,Variable,Savings"', "B4:B40")
st["E3"] = "Year"; st["F3"] = 2026; st["E3"].font = Font(bold=True); st["F3"].fill = PatternFill("solid", fgColor=SOFT)
tx = wb.create_sheet("Transactions")
title(tx, "Transactions", "One row per income or expense. Pick the category from the dropdown.")
header(tx, ["Date", "Description", "Category", "Amount", "Type", "Month"], [13, 32, 22, 13, 11, 9])
dv(tx, "=Setup!$A$4:$A$40", "C4:C2000")
for r in range(4, 2001):
    tx[f"A{r}"].number_format = "yyyy-mm-dd"; tx[f"D{r}"].number_format = "#,##0.00"
    tx[f"E{r}"] = f'=IF(C{r}="","",IFERROR(INDEX(Setup!$B$4:$B$40,MATCH(C{r},Setup!$A$4:$A$40,0)),""))'
    tx[f"F{r}"] = f'=IF(A{r}="","",MONTH(A{r}))'
for r, (dt, de, ca, am) in enumerate([("2026-01-01", "Salary", "Salary / income", 4000), ("2026-01-02", "Rent", "Rent / mortgage", 1200), ("2026-01-05", "Supermarket", "Groceries", 86.4), ("2026-01-09", "Train pass", "Transport", 150)], 4):
    tx.cell(r, 1, d.date.fromisoformat(dt)); tx.cell(r, 2, de); tx.cell(r, 3, ca); tx.cell(r, 4, am)
mo = wb.create_sheet("Monthly", 0)
title(mo, "Budget vs actual", "Choose a month in B3. Everything else is automatic.")
mo["A3"] = "Month (1-12)"; mo["B3"] = 1; mo["A3"].font = Font(bold=True); mo["B3"].fill = PatternFill("solid", fgColor=SOFT)
dv(mo, '"1,2,3,4,5,6,7,8,9,10,11,12"', "B3")
for i, c in enumerate(["Category", "Type", "Budget", "Actual", "Left", "% used"], 1):
    x = mo.cell(5, i, c); x.font = H; x.fill = HF; mo.column_dimensions[L(i)].width = [24, 11, 13, 13, 13, 10][i - 1]
for i in range(len(cats)):
    r = 6 + i; s = 4 + i
    mo[f"A{r}"] = f"=Setup!A{s}"; mo[f"B{r}"] = f"=Setup!B{s}"; mo[f"C{r}"] = f"=Setup!C{s}"
    mo[f"D{r}"] = f'=SUMIFS(Transactions!$D:$D,Transactions!$C:$C,A{r},Transactions!$F:$F,$B$3)'
    mo[f"E{r}"] = f"=C{r}-D{r}"; mo[f"F{r}"] = f'=IF(C{r}=0,"",D{r}/C{r})'; mo[f"F{r}"].number_format = "0%"
    for c in "CDE": mo[f"{c}{r}"].number_format = "#,##0.00"
end = 5 + len(cats)
mo.conditional_formatting.add(f"F6:F{end}", CellIsRule(operator="greaterThan", formula=["1"], fill=PatternFill("solid", fgColor="F8D7DA")))
mo.conditional_formatting.add(f"F6:F{end}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="4CC29A"))
mo["H5"] = "Summary"; mo["H5"].font = Font(bold=True, size=12, color=G)
for r, (k, f) in enumerate([("Income", f'=SUMIFS(D6:D{end},B6:B{end},"Income")'), ("Spent (fixed + variable)", f'=SUMIFS(D6:D{end},B6:B{end},"Fixed")+SUMIFS(D6:D{end},B6:B{end},"Variable")'),
                            ("Saved & invested", f'=SUMIFS(D6:D{end},B6:B{end},"Savings")'), ("Left over", "=I6-I7-I8"), ("Savings rate", '=IFERROR(I8/I6,"")')], 6):
    mo[f"H{r}"] = k; mo[f"I{r}"] = f; mo[f"H{r}"].font = Font(bold=True); mo[f"I{r}"].number_format = "0%" if r == 10 else "#,##0.00"
mo.column_dimensions["H"].width = 24; mo.column_dimensions["I"].width = 14
pie = PieChart(); pie.title = "Where the money went"; pie.height = 8; pie.width = 12
pie.add_data(Reference(mo, min_col=4, min_row=8, max_row=end), titles_from_data=False); pie.set_categories(Reference(mo, min_col=1, min_row=8, max_row=end)); mo.add_chart(pie, "H13")
yr = wb.create_sheet("Year")
title(yr, "Year overview", "Income, spending and savings by month.")
header(yr, ["Month", "Income", "Spent", "Saved", "Left over"], [10, 13, 13, 13, 13])
for m in range(1, 13):
    r = 3 + m; yr[f"A{r}"] = d.date(2026, m, 1).strftime("%b")
    def s(t): return f'SUMIFS(Transactions!$D:$D,Transactions!$E:$E,"{t}",Transactions!$F:$F,{m})'
    yr[f"B{r}"] = "=" + s("Income"); yr[f"C{r}"] = f"={s('Fixed')}+{s('Variable')}"; yr[f"D{r}"] = "=" + s("Savings"); yr[f"E{r}"] = f"=B{r}-C{r}-D{r}"
    for c in "BCDE": yr[f"{c}{r}"].number_format = "#,##0"
bc = BarChart(); bc.title = "Monthly income vs spending"; bc.height = 7.5; bc.width = 16
bc.add_data(Reference(yr, min_col=2, min_row=3, max_col=4, max_row=15), titles_from_data=True); bc.set_categories(Reference(yr, min_col=1, min_row=4, max_row=15)); yr.add_chart(bc, "G3")
howto(wb, ["1. On Setup, set a monthly budget for each category. Rename or add categories (up to row 40) as you like.",
  "2. Log every income and expense on Transactions, choosing the category from the dropdown.",
  "3. On Monthly, choose a month to see budget vs actual. Categories over budget turn red.",
  "4. Year shows income, spending and savings for every month with a chart.",
  "Delete the sample transactions before you start. Works in Google Sheets (File > Import) and Excel."])
wb.save(OUT / "Monthly-Budget-Planner.xlsx")
print("saved")
