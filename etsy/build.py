"""Build the Etsy upload pack: one folder per listing with listing.txt, images and files,
plus listings.csv. Usage: python3 build.py OUT_DIR   (then: node render.js OUT_DIR/jobs.json)
Source products are read from /mnt/project-files/income/."""
import sys, os, json, csv, shutil, subprocess, zipfile, glob, base64, html
from products import P, BUNDLES, by_slug, SHEET_TAIL, PRINT_TAIL

SRC = "/mnt/project-files/income/"
OUT = os.path.abspath(sys.argv[1])
os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(OUT, "_tmp"); os.makedirs(TMP, exist_ok=True)
jobs = []

def b64(path):
    ext = "jpeg" if path.endswith(".jpg") else "png"
    return f"data:image/{ext};base64," + base64.b64encode(open(path, "rb").read()).decode()

def esc(s): return html.escape(s)

BASE = "margin:0;width:2000px;height:1600px;font-family:Inter,system-ui,sans-serif;box-sizing:border-box;overflow:hidden;"

def job(out, body, w=2000, h=1600):
    jobs.append(dict(out=out, html=f"<html><body style='{BASE}'>{body}</body></html>", w=w, h=h))

def sheet_pages(p):
    """Render each sheet of the workbook (one page per sheet) and return PNG paths, skipping 'How to use'."""
    d = os.path.join(TMP, p["slug"]); os.makedirs(d, exist_ok=True)
    x = os.path.join(d, "book.xlsx"); shutil.copy(SRC + p["src"], x)
    subprocess.run(["soffice", "--headless", "--convert-to",
                    'pdf:calc_pdf_Export:{"SinglePageSheets":{"type":"boolean","value":"true"}}',
                    "--outdir", d, x], capture_output=True, timeout=180)
    import openpyxl
    names = openpyxl.load_workbook(x, read_only=True).sheetnames
    subprocess.run(["pdftoppm", "-r", "110", "-png", os.path.join(d, "book.pdf"), os.path.join(d, "pg")], check=True)
    pages = sorted(glob.glob(os.path.join(d, "pg-*.png")))
    return [(n, pg) for n, pg in zip(names, pages) if "how to" not in n.lower()]

def printable_pages(p):
    d = os.path.join(TMP, p["slug"]); os.makedirs(d, exist_ok=True)
    with zipfile.ZipFile(SRC + p["src"]) as z:
        pdf = next(n for n in z.namelist() if n.endswith("A4.pdf"))
        z.extract(pdf, d)
    subprocess.run(["pdftoppm", "-r", "70", "-png", "-l", "3", os.path.join(d, pdf), os.path.join(d, "pg")], check=True)
    return sorted(glob.glob(os.path.join(d, "pg-*.png")))

def preview_sheet(p, out, name, png, accent):
    from PIL import Image
    im = Image.open(png); w, h = im.size
    # crop to the top-left area that fits a 1700x1150 window
    ratio = 1150 / 1700
    cw, ch = (w, int(w * ratio)) if h / w > ratio else (w, h)
    crop = os.path.join(TMP, os.path.basename(out) + ".png"); im.crop((0, 0, cw, ch)).save(crop)
    body = f"""<div style="width:100%;height:100%;background:linear-gradient(135deg,{accent},#222);display:flex;flex-direction:column;align-items:center;justify-content:center">
<div style="color:#fff;font-size:64px;font-weight:700;margin-bottom:40px">{esc(name)} tab</div>
<div style="width:1700px;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 40px 100px rgba(0,0,0,.45)">
<div style="height:60px;background:#eceff1;display:flex;align-items:center;gap:16px;padding-left:28px"><i style="width:22px;height:22px;border-radius:50%;background:#ff5f57;display:block"></i><i style="width:22px;height:22px;border-radius:50%;background:#febc2e;display:block"></i><i style="width:22px;height:22px;border-radius:50%;background:#28c840;display:block"></i></div>
<img src="{b64(crop)}" style="width:1700px;height:1150px;object-fit:contain;object-position:top center;background:#fff;display:block"></div></div>"""
    job(out, body)

def preview_print(p, out, pages, accent):
    imgs = "".join(f'<img src="{b64(pg)}" style="height:1300px;background:#fff;border-radius:10px;box-shadow:0 30px 80px rgba(0,0,0,.4);transform:rotate({r}deg);margin:0 -60px">'
                   for pg, r in zip(pages, [-4, 0, 4]))
    body = f"""<div style="width:100%;height:100%;background:#f3efe8;display:flex;align-items:center;justify-content:center">{imgs}</div>"""
    job(out, body)

def preview_canva(p, out, pngs, accent):
    imgs = "".join(f'<img src="{b64(pg)}" style="max-height:1250px;max-width:560px;border-radius:12px;box-shadow:0 30px 80px rgba(0,0,0,.35);margin:0 25px">' for pg in pngs)
    job(out, f'<div style="width:100%;height:100%;background:#f3efe8;display:flex;align-items:center;justify-content:center">{imgs}</div>')

ACC = {"canva": "#c4663f", "sheet": "#1f6f50", "printable": "#7b5ea7", "html": "#1c3d5a", "bundle": "#b3541e"}

def features(p, out, lines, accent):
    li = "".join(f'<li style="margin:0 0 30px;padding-left:70px;position:relative"><span style="position:absolute;left:0;top:2px;width:44px;height:44px;border-radius:50%;background:{accent};color:#fff;font-size:30px;display:flex;align-items:center;justify-content:center">✓</span>{esc(l)}</li>' for l in lines)
    fs = 60 if len(lines) <= 6 else 50 if len(lines) <= 9 else 42
    body = f"""<div style="width:100%;height:100%;background:#fff;padding:0 150px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center">
<div style="font-size:40px;letter-spacing:6px;color:{accent};font-weight:700">WHAT'S INCLUDED</div>
<div style="font-size:84px;font-weight:800;color:#1b1b1b;margin:20px 0 70px;line-height:1.05">{esc(p.get('name') or p['title'].split('|')[0].strip())}</div>
<ul style="list-style:none;margin:0;padding:0;font-size:{fs}px;color:#333;line-height:1.25">{li}</ul></div>"""
    job(out, body)

STEPS = {
 "sheet": ["Buy and download the .xlsx file instantly from your Etsy Purchases page", "Excel: double-click to open. Google Sheets: upload to Google Drive, open it, then File > Save as Google Sheets", "Type over the sample data. Totals, charts and alerts update by themselves"],
 "printable": ["Buy and download the ZIP instantly from your Etsy Purchases page", "Open the A4 or US Letter PDF and print at home or at a print shop", "Or import the PDF into GoodNotes, Notability or any PDF app"],
 "html": ["Buy and download the ZIP instantly from your Etsy Purchases page", "Open index.html in any text editor and change the text marked EDIT:", "Drag the folder onto Netlify (free) and your site is live"],
 "canva": ["Buy and download the ZIP instantly from your Etsy Purchases page", "In Canva (free), click Upload and choose the .pptx file. It opens as an editable design", "Change the text, colours and photos, then download and post"],
 "bundle": ["Buy and download the ZIP instantly from your Etsy Purchases page", "Unzip it: every template is in its own folder", "Spreadsheets open in Excel or Google Sheets; printables print at A4 or US Letter"],
}

def how(p, out, accent):
    st = "".join(f'<div style="display:flex;gap:50px;align-items:flex-start;margin-bottom:70px"><div style="flex:none;width:120px;height:120px;border-radius:50%;background:#fff;color:{accent};font-size:64px;font-weight:800;display:flex;align-items:center;justify-content:center">{i+1}</div><div style="font-size:54px;line-height:1.25;padding-top:20px">{esc(s)}</div></div>' for i, s in enumerate(STEPS[p["kind"]]))
    body = f"""<div style="width:100%;height:100%;background:{accent};color:#fff;padding:130px 160px;box-sizing:border-box">
<div style="font-size:96px;font-weight:800;margin-bottom:90px">How it works</div>{st}
<div style="font-size:40px;opacity:.85">Instant digital download · No physical item is shipped</div></div>"""
    job(out, body)

def bundle_cover(b, out, covers, kind_label):
    tiles = "".join(f'<img src="{b64(c)}" style="width:100%;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.3)">' for c in covers[:12])
    cols = 4 if len(covers) > 9 else 3
    body = f"""<div style="width:100%;height:100%;background:{b['accent']};display:flex;align-items:center;gap:70px;padding:0 100px;box-sizing:border-box;color:#fff">
<div style="flex:none;width:640px"><div style="font-size:200px;font-weight:900;line-height:.9">{len(b['items'])}</div><div style="font-size:96px;font-weight:800;line-height:1.02;margin-top:20px">{esc(b['name'])}</div>
<div style="font-size:44px;margin-top:40px;opacity:.92">{kind_label}</div>
<div style="display:inline-block;margin-top:50px;background:#fff;color:{b['accent']};font-size:44px;font-weight:800;padding:18px 40px;border-radius:60px">Save {b["save"]}%</div></div>
<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:26px;flex:1">{tiles}</div></div>"""
    job(out, body)

SHEET_HOW = """HOW IT WORKS
1. Download the .xlsx file instantly from your Etsy Purchases page (you get an email too).
2. Microsoft Excel: just open it. Google Sheets (free): upload the file to Google Drive, open it, then choose File > Save as Google Sheets.
3. Type over the sample data. Totals, charts and colour alerts update automatically."""
PRINT_HOW = """HOW IT WORKS
1. Download the ZIP instantly from your Etsy Purchases page (you get an email too).
2. Open the A4 or US Letter PDF and print at home or at a print shop, as many times as you like for personal use.
3. Or import the PDF into GoodNotes, Notability or any PDF annotation app."""
HTML_HOW = """HOW IT WORKS
1. Download the ZIP instantly from your Etsy Purchases page.
2. Open index.html in any text editor and replace the text marked EDIT: with your own.
3. Drag the folder onto Netlify, or use GitHub Pages or Cloudflare Pages. All free; the README walks you through it."""
CANVA_HOW = """HOW IT WORKS
1. Download the ZIP instantly from your Etsy Purchases page and unzip it.
2. Canva (a free account is fine): click Upload, choose the .pptx file, and Canva opens it as a fully editable design. It also opens in PowerPoint, Keynote and Google Slides.
3. Change the text, colours and photos, then download as PNG, JPG or PDF.
A HOW-TO-EDIT guide is included."""
NOTES = """PLEASE NOTE
• This is a digital download. No physical item will be shipped.
• For personal use (or use in your own business). Please do not resell or share the files.
• Numbers are plain amounts, so any currency works.
• Because this is a digital item, returns are not accepted, but if anything does not work, send me a message and I will fix it fast.
• Designed by our shop with the help of AI tools.

Thank you for visiting! Favourite the shop to see new templates first."""

def description(p):
    k = p["kind"]
    if k == "bundle":
        items = [by_slug(s) for s in p["items"]]
        total = sum(i["price"] for i in items)
        lines = "\n".join(f"• {i['title'].split('|')[0].strip()}" for i in items)
        how = """HOW IT WORKS
1. Download the ZIP instantly from your Etsy Purchases page (you get an email too) and unzip it. Every template has its own folder.
2. Spreadsheets: open in Microsoft Excel, or upload to Google Drive and choose File > Save as Google Sheets. Type over the sample data and everything updates.
3. Printables: print the A4 or US Letter PDF at home, or use it in GoodNotes / Notability."""
        extra = ("\nThe printables come as A4 and US Letter PDFs." if any(i["kind"] == "printable" for i in items) and any(i["kind"] == "sheet" for i in items) else "")
        return f"""{p['intro']}

WHAT'S INCLUDED ({len(items)} templates, worth ${total:.2f} separately)
{lines}

Spreadsheets work in Google Sheets (free), Microsoft Excel and LibreOffice.{extra}

{how}

{NOTES}"""
    tail = SHEET_TAIL if k == "sheet" else PRINT_TAIL if k == "printable" else []
    bl = "\n".join("• " + b for b in p["bullets"] + tail)
    how = {"canva": CANVA_HOW, "sheet": SHEET_HOW, "printable": PRINT_HOW, "html": HTML_HOW}[k]
    return f"""{p['intro']}

WHAT'S INCLUDED
{bl}

{how}

{NOTES}"""

CATEGORY = {"sheet": "Paper & Party Supplies > Paper > Calendars & Planners (search 'planner' or 'template' in the category box)",
            "printable": "Paper & Party Supplies > Paper > Calendars & Planners",
            "bundle": "Paper & Party Supplies > Paper > Calendars & Planners",
            "canva": "Paper & Party Supplies > Paper > Stationery > Design & Templates (or search 'template' in the category box)", "html": "Search 'template' in the category box and pick the closest digital templates option"}

rows = []
allp = P + BUNDLES
for n, p in enumerate(allp, 1):
    d = os.path.join(OUT, f"{n:02d}-{p['slug']}"); im = os.path.join(d, "images"); fd = os.path.join(d, "files")
    os.makedirs(im, exist_ok=True); os.makedirs(fd, exist_ok=True)
    acc = p.get("accent") or ACC[p["kind"]]
    # files
    if p["kind"] == "bundle":
        zp = os.path.join(fd, p["name"].replace(" ", "-") + ".zip")
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for s in p["items"]:
                i = by_slug(s); z.write(SRC + i["src"], i["slug"] + "/" + os.path.basename(i["src"]))
    else:
        shutil.copy(SRC + p["src"], fd)
    # images
    if p["kind"] == "bundle":
        items = [by_slug(s) for s in p["items"]]
        covers = [SRC + i["cover"] for i in items]
        p["save"] = int(100 * (1 - p["price"] / sum(i["price"] for i in items)))
        kinds = {i["kind"] for i in items}
        label = "Google Sheets & Excel + printable PDFs" if kinds == {"sheet", "printable"} else "Google Sheets & Excel" if kinds == {"sheet"} else "Printable PDF · A4 & US Letter"
        bundle_cover(p, os.path.join(im, "01-cover.jpg"), covers, label)
        features(p, os.path.join(im, "02-included.jpg"), [i["title"].split("|")[0].strip() for i in items], acc)
        how(p, os.path.join(im, "03-how-it-works.jpg"), acc)
    else:
        from PIL import Image; Image.open(SRC + p["cover"]).convert("RGB").save(os.path.join(im, "01-cover.jpg"), quality=90)
        idx = 2
        try:
            if p["kind"] == "sheet":
                for name, pg in sheet_pages(p)[:3]:
                    preview_sheet(p, os.path.join(im, f"{idx:02d}-preview.jpg"), name, pg, acc); idx += 1
            elif p["kind"] == "canva":
                pv = sorted(glob.glob(SRC + p["previews"] + "/*.png"))
                for k in range(0, min(len(pv), 9), 3):
                    preview_canva(p, os.path.join(im, f"{idx:02d}-preview.jpg"), pv[k:k + 3], acc); idx += 1
            elif p["kind"] == "printable":
                preview_print(p, os.path.join(im, f"{idx:02d}-preview.jpg"), printable_pages(p), acc); idx += 1
        except Exception as e:
            print("preview failed", p["slug"], e)
        tail = SHEET_TAIL if p["kind"] == "sheet" else PRINT_TAIL if p["kind"] == "printable" else []
        features(p, os.path.join(im, f"{idx:02d}-included.jpg"), (p["bullets"] or [p["intro"]]) + tail, acc); idx += 1
        how(p, os.path.join(im, f"{idx:02d}-how-it-works.jpg"), acc)
    desc = description(p)
    txt = f"""TITLE
{p['title']}

PRICE
${p['price']:.2f}

TAGS (13)
{', '.join(p['tags'])}

CATEGORY
{CATEGORY[p['kind']]}

ABOUT THIS LISTING
Who made it? I did · What is it? A finished product · When was it made? 2020 - 2026
Type: Digital · Quantity: 999 · Renewal: Automatic

PHOTOS
Upload every file in images/ in name order (01 is the thumbnail).

DIGITAL FILE
Upload the file in files/.

DESCRIPTION
{desc}
"""
    open(os.path.join(d, "listing.txt"), "w").write(txt)
    rows.append(dict(folder=os.path.basename(d), title=p["title"], price=f"{p['price']:.2f}", tags=",".join(p["tags"]),
                     category=CATEGORY[p["kind"]], who_made="i_did", is_supply="false", when_made="2020_2026",
                     type="download", quantity=999, description=desc))

with open(os.path.join(OUT, "listings.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(jobs, open(os.path.join(OUT, "jobs.json"), "w"))
print(len(rows), "listings,", len(jobs), "image jobs")
