"""Builds printable PDF products in A4 and US Letter. Run: python3 build.py"""
import pathlib, subprocess, zipfile
OUT = pathlib.Path(__file__).parent / "out"; OUT.mkdir(exist_ok=True)
CSS = """@page{margin:12mm}*{box-sizing:border-box}body{margin:0;font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:#222;font-size:10pt}
.pg{height:calc(var(--h) - 24mm);page-break-after:always;display:flex;flex-direction:column;overflow:hidden}
h1{font-size:24pt;margin:0;color:var(--c);letter-spacing:-.01em}.sub{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2pt solid var(--c);padding-bottom:4pt;margin-bottom:8pt}
.lbl{font-size:7.5pt;text-transform:uppercase;letter-spacing:.12em;color:#777;margin:8pt 0 3pt;font-weight:600}
.line{border-bottom:.7pt solid #c8c8c8;height:20pt}.box{border:.8pt solid #c8c8c8;border-radius:5pt;padding:6pt 8pt}
.cols{display:flex;gap:12pt}.cols>*{flex:1;min-width:0}.grow{flex:1;display:flex;flex-direction:column}
.chk{display:flex;align-items:center;gap:6pt;border-bottom:.7pt solid #c8c8c8;height:20pt}.chk i{width:9pt;height:9pt;border:.8pt solid #888;border-radius:2pt;flex:none}
table{width:100%;border-collapse:collapse}td,th{border:.7pt solid #c8c8c8;height:19pt;padding:0 4pt;font-size:8.5pt;text-align:left}th{background:var(--s);font-weight:600}
.hr td{height:33pt}.dots td{text-align:center}.small{font-size:8pt;color:#777}"""
def lines(n): return '<div class="line"></div>' * n
def chks(n): return '<div class="chk"><i></i></div>' * n

def daily():
    hours = "".join(f'<tr class="hr"><td style="width:15%">{h}</td><td></td></tr>' for h in ["6 am","7","8","9","10","11","12 pm","1","2","3","4","5","6","7","8","9"])
    return ['<div class="pg"><div class="sub"><h1>Daily Planner</h1><span>Date: ______________  M T W T F S S</span></div>'
            '<div class="cols" style="flex:1"><div><div class="lbl">Schedule</div><table>' + hours + '</table></div>'
            '<div class="grow"><div class="lbl">Top 3 priorities</div>' + chks(3) + '<div class="lbl">To do</div>' + chks(9) +
            '<div class="lbl">Water</div><div style="display:flex;gap:6pt">' + '<i style="width:16pt;height:20pt;border:.8pt solid #888;border-radius:3pt;display:inline-block"></i>' * 8 + '</div>'
            '<div class="lbl">Notes</div>' + lines(5) + '<div class="lbl">Grateful for</div>' + lines(2) + '</div></div></div>']
def weekly():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return ['<div class="pg"><div class="sub"><h1>Weekly Planner</h1><span>Week of: ______________</span></div><div class="cols" style="flex:1">'
            '<div class="grow">' + "".join(f'<div class="box" style="margin-bottom:6pt;flex:1"><b>{d}</b>' + lines(4) + '</div>' for d in days[:4]) + '</div>'
            '<div class="grow">' + "".join(f'<div class="box" style="margin-bottom:6pt;flex:1"><b>{d}</b>' + lines(3) + '</div>' for d in days[4:]) +
            '<div class="box" style="flex:1"><b>Goals this week</b>' + chks(4) + '</div></div></div></div>']
def habit():
    head = "".join(f"<th style='width:2.6%;text-align:center;padding:0'>{d}</th>" for d in range(1, 32))
    rows = "".join("<tr style='height:27pt'><td></td>" + "<td></td>" * 31 + "</tr>" for _ in range(18))
    return ['<div class="pg"><div class="sub"><h1>Habit Tracker</h1><span>Month: ______________</span></div>'
            f'<table class="dots"><tr><th style="text-align:left">Habit</th>{head}</tr>{rows}</table>'
            '<div class="cols" style="margin-top:8pt"><div><div class="lbl">Rewards</div>' + lines(4) + '</div><div><div class="lbl">Reflection</div>' + lines(4) + '</div></div></div>']
def workout():
    t = "<table><tr><th style='width:34%'>Exercise</th><th>Set 1</th><th>Set 2</th><th>Set 3</th><th>Set 4</th></tr>" + "<tr style='height:25pt'><td></td><td></td><td></td><td></td><td></td></tr>" * 14 + "</table>"
    return ['<div class="pg"><div class="sub"><h1>Workout Log</h1><span>Date: __________  Focus: __________</span></div><div class="small">Write weight × reps in each set.</div>' + t +
            '<div class="cols"><div><div class="lbl">Cardio</div><table><tr><th>Type</th><th>Time</th><th>Distance</th></tr>' + "<tr><td></td><td></td><td></td></tr>" * 3 + '</table></div>'
            '<div><div class="lbl">How I felt</div><div style="display:flex;gap:10pt;font-size:16pt">😩 😐 🙂 😄 💪</div><div class="lbl">Sleep · Water · Energy</div>' + lines(2) + '</div></div>'
            '<div class="lbl">Notes</div>' + lines(3) + '</div>']
def reading():
    log = ('<div class="pg"><div class="sub"><h1>Reading Log</h1><span>Year: ________</span></div><table><tr><th style="width:5%">#</th><th>Title</th><th>Author</th><th style="width:12%">Finished</th><th style="width:12%">Rating</th></tr>'
           + "".join(f"<tr><td>{i}</td><td></td><td></td><td></td><td>☆☆☆☆☆</td></tr>" for i in range(1, 31)) + '</table></div>')
    rev = ('<div class="pg"><div class="sub"><h1>Book Review</h1><span>☆ ☆ ☆ ☆ ☆</span></div><div class="cols"><div><div class="lbl">Title</div>' + lines(1) + '</div><div><div class="lbl">Author</div>' + lines(1) + '</div></div>'
           '<div class="cols"><div><div class="lbl">Started</div>' + lines(1) + '</div><div><div class="lbl">Finished</div>' + lines(1) + '</div><div><div class="lbl">Genre</div>' + lines(1) + '</div></div>'
           '<div class="lbl">Summary</div>' + lines(5) + '<div class="lbl">Favourite quotes</div>' + lines(4) + '<div class="lbl">What I learned / how it made me feel</div>' + lines(4) + '<div class="lbl">Would I recommend it? To whom?</div>' + lines(2) + '</div>')
    wish = '<div class="pg"><div class="sub"><h1>Books to Read</h1><span></span></div>' + chks(32) + '</div>'
    return [log, rev, rev, wish]
PRODUCTS = [("Daily-Planner", "#2b8a3e", "#e6f4ea", daily), ("Weekly-Planner", "#1864ab", "#e7f0fa", weekly), ("Habit-Tracker-Printable", "#5f3dc4", "#efeafc", habit),
            ("Workout-Log", "#c92a2a", "#fdeaea", workout), ("Reading-Journal", "#a0522d", "#f7ede6", reading)]
exec((pathlib.Path(__file__).parent / "more_printables.py").read_text())
exec((pathlib.Path(__file__).parent / "more_printables2.py").read_text())
exec((pathlib.Path(__file__).parent / "more_printables3.py").read_text())
SIZES = {"A4": ("210mm", "297mm"), "Letter": ("8.5in", "11in")}
jobs = []
for name, c, s, fn in PRODUCTS:
    pages = fn()
    for sz, (w, h) in SIZES.items():
        f = OUT / f"{name}-{sz}.html"
        f.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>@page{{size:{w} {h}}}:root{{--c:{c};--s:{s};--h:{h}}}{CSS}</style></head><body>{''.join(pages)}</body></html>")
        jobs.append(str(f))
js = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();for(const f of " + str(jobs).replace("'", '"') + "){await p.goto('file://'+f);await p.pdf({path:f.replace('.html','.pdf'),preferCSSPageSize:true,printBackground:true});}await b.close()})()"
subprocess.run(["node", "-e", js], check=True)
for name, *_ in PRODUCTS:
    with zipfile.ZipFile(OUT / f"{name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for sz in SIZES: z.write(OUT / f"{name}-{sz}.pdf", f"{name}-{sz}.pdf")
        z.writestr("README.txt", f"{name.replace('-', ' ')}\n\nPrint at home or at a print shop. Two sizes are included: A4 and US Letter.\nPrint as many copies as you like for personal use. For best results print at 100% scale (no 'fit to page').\nYou can also use the PDF on a tablet with an annotation app such as GoodNotes or Notability.\n")
print("built", len(PRODUCTS))
