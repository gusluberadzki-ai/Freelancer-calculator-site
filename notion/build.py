"""Build Notion template assets: spec JSON (for creating them with the Notion connector),
Markdown+CSV import ZIPs, cover/preview images and listing copy.
Usage: python3 build.py OUT_DIR && node ../etsy/render.js OUT_DIR/jobs.json"""
import sys, os, json, csv, io, zipfile, html
from templates import T, BUNDLE

OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
jobs = []
E = html.escape
BASE = "margin:0;width:2000px;height:1600px;font-family:Inter,system-ui,sans-serif;box-sizing:border-box;overflow:hidden;"
def job(out, body): jobs.append(dict(out=out, html=f"<html><body style='{BASE}'>{body}</body></html>", w=2000, h=1600))

def prop_label(p):
    return {"title": "Aa", "rich_text": "≡", "number": "#", "select": "⌄", "multi_select": "☰", "status": "◉", "date": "📅",
            "checkbox": "☑", "url": "🔗", "email": "@", "formula": "Σ", "relation": "↗", "rollup": "🔍", "phone_number": "☏"}[p[1]]

def cell(v, p):
    if p[1] == "checkbox": return "☑" if v == "Yes" else "☐"
    if p[1] in ("select", "status", "multi_select") and v:
        return "".join(f'<span style="background:#f1f1ef;border-radius:6px;padding:3px 10px;margin-right:6px">{E(x.strip())}</span>' for x in v.split(","))
    return E(v)

def table(d, maxcols=6, fs=26):
    props = d["props"][:maxcols]
    th = "".join(f'<th style="text-align:left;font-weight:500;color:#787774;padding:12px 16px;border-bottom:1px solid #e9e9e7;border-right:1px solid #e9e9e7;white-space:nowrap">{prop_label(p)} {E(p[0])}</th>' for p in props)
    trs = "".join("<tr>" + "".join(f'<td style="padding:12px 16px;border-bottom:1px solid #e9e9e7;border-right:1px solid #e9e9e7;white-space:nowrap;{"font-weight:600" if i == 0 else ""}">{cell(r[i] if i < len(r) else "", p)}</td>' for i, p in enumerate(props)) + "</tr>" for r in d["rows"])
    return f'<div style="font-size:{fs+6}px;font-weight:700;margin:26px 0 10px">{d["icon"]} {E(d["name"])} <span style="font-size:{fs-4}px;color:#9b9a97;font-weight:400;margin-left:14px">{" · ".join(d["views"][:3])}</span></div><table style="border-collapse:collapse;font-size:{fs}px;color:#37352f">{th and "<tr>"+th+"</tr>"}{trs}</table>'

def notion_page(t, content, banner=True):
    return f"""<div style="width:100%;height:100%;background:linear-gradient(135deg,{t['accent']},#111);padding:80px;box-sizing:border-box">
<div style="background:#fff;border-radius:24px;height:100%;overflow:hidden;box-shadow:0 40px 100px rgba(0,0,0,.4)">
<div style="height:52px;background:#f7f7f5;border-bottom:1px solid #e9e9e7;display:flex;align-items:center;padding-left:24px;gap:12px;font-size:22px;color:#9b9a97"><span>●</span><span>●</span><span>●</span><span style="margin-left:20px">{t['icon']} {E(t['name'])}</span></div>
{'<div style="height:150px;background:linear-gradient(90deg,'+t['accent']+'33,'+t['accent']+'88)"></div>' if banner else ''}
<div style="padding:0 90px;overflow:hidden">{content}</div></div></div>"""

def cover(t, out):
    d = t["dbs"][0]
    content = f"""<div style="font-size:110px;margin-top:-62px">{t['icon']}</div><div style="font-size:72px;font-weight:800;color:#37352f">{E(t['name'])}</div>
<div style="font-size:32px;color:#787774;margin:10px 0 0">{E(t['tagline'])}</div>{table(d, 6, 34)}"""
    body = notion_page(t, content) + f"""<div style="position:absolute;right:120px;bottom:120px;background:{t['accent']};color:#fff;font-size:44px;font-weight:800;padding:22px 44px;border-radius:60px;box-shadow:0 10px 30px rgba(0,0,0,.3)">Notion template</div>"""
    job(out, f'<div style="position:relative;width:100%;height:100%">{body}</div>')

def preview(t, out):
    content = f'<div style="font-size:48px;font-weight:800;color:#37352f;margin-top:40px">{t["icon"]} {E(t["name"])}: databases</div>' + "".join(table(d, 5, 29) for d in t["dbs"][1:4] or t["dbs"])
    job(out, notion_page(t, content, banner=False))

def features(t, out, title, lines):
    li = "".join(f'<li style="margin:0 0 30px;padding-left:70px;position:relative"><span style="position:absolute;left:0;top:4px;width:44px;height:44px;border-radius:50%;background:{t["accent"]};color:#fff;font-size:30px;display:flex;align-items:center;justify-content:center">✓</span>{E(l)}</li>' for l in lines)
    job(out, f"""<div style="width:100%;height:100%;background:#fff;padding:0 150px;display:flex;flex-direction:column;justify-content:center;box-sizing:border-box">
<div style="font-size:40px;letter-spacing:6px;color:{t['accent']};font-weight:700">WHAT'S INCLUDED</div>
<div style="font-size:84px;font-weight:800;color:#1b1b1b;margin:20px 0 60px">{E(title)}</div>
<ul style="list-style:none;margin:0;padding:0;font-size:{56 if len(lines) <= 7 else 44}px;color:#333;line-height:1.25">{li}</ul></div>""")

def howto(t, out):
    steps = ["Buy and open the PDF that comes with your download", "Click the template link and press Duplicate (top right) to copy it into your Notion", "Delete the sample entries and make it yours. Works on the free Notion plan, desktop and mobile"]
    st = "".join(f'<div style="display:flex;gap:50px;margin-bottom:70px"><div style="flex:none;width:120px;height:120px;border-radius:50%;background:#fff;color:{t["accent"]};font-size:64px;font-weight:800;display:flex;align-items:center;justify-content:center">{i+1}</div><div style="font-size:54px;line-height:1.25;padding-top:20px">{E(s)}</div></div>' for i, s in enumerate(steps))
    job(out, f'<div style="width:100%;height:100%;background:{t["accent"]};color:#fff;padding:130px 160px;box-sizing:border-box"><div style="font-size:96px;font-weight:800;margin-bottom:90px">How it works</div>{st}</div>')

def tags(t):
    base = ["notion template", "notion planner", "notion dashboard", "digital planner", "productivity"]
    extra = {"freelance-os": ["freelancer", "client tracker", "invoice tracker", "small business", "crm template", "project manager", "time tracker", "business planner"],
             "personal-finance-dashboard": ["budget planner", "finance tracker", "expense tracker", "savings goals", "money planner", "budget template", "subscription", "personal finance"],
             "habit-goal-tracker": ["habit tracker", "goal planner", "goal tracker", "daily planner", "self improvement", "routine planner", "new year goals", "life planner"],
             "content-calendar": ["content calendar", "content planner", "youtube planner", "social media", "creator planner", "influencer", "tiktok planner", "instagram"],
             "student-planner": ["student planner", "study planner", "college planner", "assignment tracker", "school planner", "grade tracker", "back to school", "academic planner"],
             "job-search-tracker": ["job tracker", "job search", "job application", "career planner", "interview prep", "job hunting", "resume tracker", "career change"],
             "reading-tracker": ["reading tracker", "book journal", "reading log", "book tracker", "tbr list", "bookish gift", "book lover", "reading goal"],
             "meal-planner-recipes": ["meal planner", "recipe book", "grocery list", "meal prep", "recipe organizer", "weekly menu", "food planner", "kitchen planner"]}[t["slug"]]
    return base + extra

def description(t, platform):
    lines = "\n".join("• " + f for f in t["features"])
    dbs = "\n".join(f"• {d['icon']} {d['name']}: {', '.join(p[0] for p in d['props'])}" for d in t["dbs"])
    deliver = ("You receive a PDF with your template link. Click it, press Duplicate, and the template is copied into your own Notion workspace."
               if platform == "etsy" else "After purchase you get the template link. Click it, press Duplicate, and it is copied into your Notion workspace.")
    return f"""{t['intro']}

WHAT'S INCLUDED
{lines}

DATABASES
{dbs}

HOW YOU GET IT
{deliver}
Works on the free Notion plan, on desktop, web and mobile. Sample entries show you how everything works; delete them when you're ready.

PLEASE NOTE
• Digital product. Nothing is shipped.
• You need a free Notion account (notion.com).
• For personal use. Please don't resell or share the template link.
• Designed by our shop with the help of AI tools.
"""

def import_zip(t, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        md = [f"# {t['icon']} {t['name']}", "", t["intro"], "", "## How to use", ""] + [f"- {f}" for f in t["features"]] + ["", "## Databases", ""]
        for d in t["dbs"]:
            md.append(f"- {d['icon']} {d['name']} (see {d['name']}.csv)")
            buf = io.StringIO(); w = csv.writer(buf); w.writerow([p[0] for p in d["props"]])
            for r in d["rows"]: w.writerow(r + [""] * (len(d["props"]) - len(r)))
            z.writestr(f"{t['name']}/{d['name']}.csv", buf.getvalue())
        z.writestr(f"{t['name']}/{t['name']}.md", "\n".join(md) + "\n")

specs = []
for t in T:
    d = os.path.join(OUT, t["slug"]); im = os.path.join(d, "images"); os.makedirs(im, exist_ok=True)
    cover(t, os.path.join(im, "01-cover.jpg")); preview(t, os.path.join(im, "02-databases.jpg"))
    features(t, os.path.join(im, "03-included.jpg"), t["name"], t["features"]); howto(t, os.path.join(im, "04-how-it-works.jpg"))
    import_zip(t, os.path.join(d, f"{t['slug']}-notion-import.zip"))
    tg = tags(t)[:13]
    assert all(len(x) <= 20 for x in tg) and len(tg) == 13, t["slug"]
    etsy_title = f"{t['name']} Notion Template | {t['tagline'].split(',')[0]} | Notion Dashboard | Digital Planner"[:140]
    open(os.path.join(d, "listing.md"), "w").write(f"""# {t['name']} (Notion template)

Price: ${t['price']} (Gumroad and Notion Marketplace), Etsy ${t['price'] - 0.01:.2f}

## Etsy
Title: {etsy_title}
Tags: {', '.join(tg)}
Category: Paper & Party Supplies > Paper > Calendars & Planners
Digital file: {t['slug']}-link.pdf (made after the template is published in Notion)

{description(t, 'etsy')}
## Gumroad / Notion Marketplace
Name: {t['name']}: Notion Template
Summary: {t['tagline']}

{description(t, 'gumroad')}""")
    specs.append(t)

json.dump(dict(templates=T, bundle=BUNDLE), open(os.path.join(OUT, "notion-specs.json"), "w"), indent=1, ensure_ascii=False)
json.dump(jobs, open(os.path.join(OUT, "jobs.json"), "w"))
print(len(T), "templates", len(jobs), "images")
