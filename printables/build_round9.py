"""Round 9 printables: builds A4 + US Letter PDFs, zips and a preview PNG. Run: python3 build_round9.py (reuses CSS and helpers from build.py)"""
import pathlib, subprocess, zipfile, json
HERE = pathlib.Path(__file__).parent
_src = (HERE / "build.py").read_text()
exec(_src[:_src.index("def daily():")])
exec((HERE / "more_printables3.py").read_text())
SIZES = {"A4": ("210mm", "297mm"), "Letter": ("8.5in", "11in")}
jobs = []
for name, c, s, fn in PRODUCTS:
    pages = fn()
    for sz, (w, h) in SIZES.items():
        f = OUT / f"{name}-{sz}.html"
        f.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>@page{{size:{w} {h}}}:root{{--c:{c};--s:{s};--h:{h}}}{CSS}</style></head><body>{''.join(pages)}</body></html>")
        jobs.append(str(f))
    # preview of page 1 at A4 proportions
    pv = OUT / f"{name}-preview.html"
    pv.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>:root{{--c:{c};--s:{s};--h:297mm}}{CSS}body{{width:210mm;padding:12mm;background:#fff}}</style></head><body>{pages[0]}</body></html>")
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();for(const f of " + json.dumps(jobs) +
      "){await p.goto('file://'+f);await p.pdf({path:f.replace('.html','.pdf'),preferCSSPageSize:true,printBackground:true});}"
      "const q=await b.newPage({viewport:{width:794,height:1123},deviceScaleFactor:2});for(const n of " + json.dumps([n for n, *_ in PRODUCTS]) +
      "){await q.goto('file://" + str(OUT) + "/'+n+'-preview.html');await q.screenshot({path:'" + str(OUT) + "/'+n+'-preview.png'});}await b.close()})()")
subprocess.run(["node", "-e", js], check=True)
for name, *_ in PRODUCTS:
    with zipfile.ZipFile(OUT / f"{name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for sz in SIZES: z.write(OUT / f"{name}-{sz}.pdf", f"{name}-{sz}.pdf")
        z.writestr("README.txt", f"{name.replace('-', ' ')}\n\nPrint at home or at a print shop. Two sizes are included: A4 and US Letter.\nPrint as many copies as you like for personal use. For best results print at 100% scale (no 'fit to page').\nYou can also use the PDF on a tablet with an annotation app such as GoodNotes or Notability.\n")
print("built", len(PRODUCTS))
