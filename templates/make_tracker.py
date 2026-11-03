"""Builds Freelance-Business-Tracker.xlsx (works in Excel and Google Sheets)."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.chart import BarChart, Reference
import pathlib
GREEN="0B6E4F"; SOFT="E3F2EC"; GREY="F3F3F1"
H=Font(bold=True,color="FFFFFF"); HF=PatternFill("solid",fgColor=GREEN)
thin=Side(style="thin",color="DDDDDD"); B=Border(bottom=thin)
wb=Workbook()

def header(ws,cols,widths,row=3):
    for i,(c,w) in enumerate(zip(cols,widths),1):
        x=ws.cell(row,i,c); x.font=H; x.fill=HF; x.alignment=Alignment(horizontal="center")
        ws.column_dimensions[chr(64+i)].width=w
    ws.freeze_panes=ws.cell(row+1,1)
def title(ws,t,sub):
    ws["A1"]=t; ws["A1"].font=Font(bold=True,size=18,color=GREEN)
    ws["A2"]=sub; ws["A2"].font=Font(italic=True,color="777777")

# Settings
st=wb.active; st.title="Settings"
title(st,"Settings","Fill these in first. Everything else updates automatically.")
for r,(k,v) in enumerate([("Business name","Your Business"),("Year",2026),("Tax rate to set aside (%)",25),
                           ("Monthly income goal",5000),("Currency symbol","$")],4):
    st.cell(r,1,k).font=Font(bold=True); c=st.cell(r,2,v); c.fill=PatternFill("solid",fgColor=SOFT)
st.column_dimensions["A"].width=30; st.column_dimensions["B"].width=22
st["A11"]="Expense categories"; st["A11"].font=Font(bold=True)
cats=["Software","Equipment","Office","Travel","Marketing","Professional fees","Insurance","Training","Other"]
for i,c in enumerate(cats,12): st.cell(i,1,c)

# Income
inc=wb.create_sheet("Income")
title(inc,"Income & invoices","One row per invoice. Status turns red when overdue.")
header(inc,["Invoice date","Invoice #","Client","Description","Amount","Due date","Status","Paid date","Days overdue"],[14,12,22,30,14,14,12,14,13])
dv=DataValidation(type="list",formula1='"Draft,Sent,Paid,Overdue"',allow_blank=True); inc.add_data_validation(dv); dv.add("G4:G500")
for r in range(4,501):
    inc[f"I{r}"]=f'=IF(AND(G{r}<>"Paid",F{r}<>"",F{r}<TODAY()),TODAY()-F{r},"")'
    inc[f"A{r}"].number_format=inc[f"F{r}"].number_format=inc[f"H{r}"].number_format="yyyy-mm-dd"
    inc[f"E{r}"].number_format="#,##0.00"
sample=[("2026-01-08","INV-001","Acme Ltd","Website redesign",2400,"2026-01-22","Paid","2026-01-20"),
        ("2026-02-03","INV-002","Northwind","Monthly retainer",1500,"2026-02-17","Paid","2026-02-15")]
import datetime as d
for r,s in enumerate(sample,4):
    for c,v in enumerate(s,1):
        inc.cell(r,c,d.date.fromisoformat(v) if c in (1,6,8) else v)
inc.conditional_formatting.add("G4:G500",CellIsRule(operator="equal",formula=['"Overdue"'],fill=PatternFill("solid",fgColor="F8D7DA")))
inc.conditional_formatting.add("G4:G500",CellIsRule(operator="equal",formula=['"Paid"'],fill=PatternFill("solid",fgColor=SOFT)))

# Expenses
ex=wb.create_sheet("Expenses")
title(ex,"Expenses","Pick a category from the dropdown. Edit categories on the Settings tab.")
header(ex,["Date","Category","Supplier","Description","Amount","Receipt saved?"],[14,20,22,32,14,15])
dv2=DataValidation(type="list",formula1="=Settings!$A$12:$A$30",allow_blank=True); ex.add_data_validation(dv2); dv2.add("B4:B1000")
dv3=DataValidation(type="list",formula1='"Yes,No"',allow_blank=True); ex.add_data_validation(dv3); dv3.add("F4:F1000")
for r in range(4,1001): ex[f"A{r}"].number_format="yyyy-mm-dd"; ex[f"E{r}"].number_format="#,##0.00"
for r,s in enumerate([("2026-01-05","Software","Adobe","Creative Cloud",59.99,"Yes"),("2026-02-11","Equipment","Store","Monitor",249,"Yes")],4):
    for c,v in enumerate(s,1): ex.cell(r,c,d.date.fromisoformat(v) if c==1 else v)

# Dashboard
db=wb.create_sheet("Dashboard",0)
title(db,"Freelance Business Dashboard","Income counts invoices marked Paid, by paid date.")
db["A3"]="=Settings!B4&\" · \"&Settings!B5"; db["A3"].font=Font(bold=True,size=12)
header(db,["Month","Income","Expenses","Profit","Tax to set aside","Take-home","vs goal"],[14,14,14,14,17,14,12],row=5)
months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
for i,m in enumerate(months,1):
    r=5+i; db[f"A{r}"]=m
    s=f"DATE(Settings!$B$5,{i},1)"; e=f"EOMONTH(DATE(Settings!$B$5,{i},1),0)"
    db[f"B{r}"]=f'=SUMIFS(Income!$E:$E,Income!$G:$G,"Paid",Income!$H:$H,">="&{s},Income!$H:$H,"<="&{e})'
    db[f"C{r}"]=f'=SUMIFS(Expenses!$E:$E,Expenses!$A:$A,">="&{s},Expenses!$A:$A,"<="&{e})'
    db[f"D{r}"]=f"=B{r}-C{r}"; db[f"E{r}"]=f"=MAX(0,D{r})*Settings!$B$6/100"; db[f"F{r}"]=f"=D{r}-E{r}"
    db[f"G{r}"]=f'=IF(Settings!$B$7>0,B{r}/Settings!$B$7,"")'; db[f"G{r}"].number_format="0%"
    for c in "BCDEF": db[f"{c}{r}"].number_format="#,##0.00"
    if i%2==0:
        for c in "ABCDEFG": db[f"{c}{r}"].fill=PatternFill("solid",fgColor=GREY)
db["A18"]="Total"
for c in "BCDEF": db[f"{c}18"]=f"=SUM({c}6:{c}17)"; db[f"{c}18"].number_format="#,##0.00"
for c in "ABCDEFG": db[f"{c}18"].font=Font(bold=True); db[f"{c}18"].border=Border(top=Side(style="medium",color=GREEN))
db["I6"]="Unpaid invoices"; db["J6"]='=SUMIFS(Income!E:E,Income!G:G,"<>Paid")'
db["I7"]="Overdue invoices"; db["J7"]='=COUNTIF(Income!G:G,"Overdue")'
db["I8"]="Best month"; db["J8"]="=INDEX(A6:A17,MATCH(MAX(B6:B17),B6:B17,0))"
for r in (6,7,8): db[f"I{r}"].font=Font(bold=True)
db.column_dimensions["I"].width=18; db.column_dimensions["J"].width=14
ch=BarChart(); ch.title="Income vs expenses"; ch.height=7.5; ch.width=17
ch.add_data(Reference(db,min_col=2,min_row=5,max_col=3,max_row=17),titles_from_data=True)
ch.set_categories(Reference(db,min_col=1,min_row=6,max_row=17)); db.add_chart(ch,"A21")

# How to use
hw=wb.create_sheet("How to use")
title(hw,"How to use this tracker","")
for i,t in enumerate(["1. Go to Settings and enter your business name, year, tax rate and monthly goal.",
 "2. Delete the sample rows on the Income and Expenses tabs.",
 "3. Add a row on Income for every invoice you send. Set Status to Paid and fill Paid date when the money arrives.",
 "4. Add every business expense on Expenses.",
 "5. The Dashboard shows monthly profit, how much tax to set aside, and progress toward your goal.",
 "Google Sheets: File > Import > Upload this file, or open it from Google Drive."],3): hw.cell(i,1,t)
hw.column_dimensions["A"].width=110
out=pathlib.Path(__file__).parent/"products"; out.mkdir(exist_ok=True)
wb.save(out/"Freelance-Business-Tracker.xlsx"); print("saved")
