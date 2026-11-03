"""Builds the Freelance Toolbox directory from tools.json. Run: python3 build.py"""
import json, html, re, pathlib, datetime
BASE="https://gusluberadzki-ai.github.io/Freelancer-calculator-site/freelance-tools/"
OUT=pathlib.Path(__file__).parent
data=json.loads((OUT/"tools.json").read_text())
slug=lambda s: re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
SUBMIT="https://github.com/gusluberadzki-ai/Freelancer-calculator-site/issues/new?title=Tool+submission:+&body=Name:%0AWebsite:%0ACategory:%0AOne-line+description:"
def head(t,d,p): return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(t)} | Freelance Toolbox</title><meta name="description" content="{html.escape(d)}"><link rel="canonical" href="{BASE}{p}">
<link rel="stylesheet" href="style.css"><style>.tool{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:12px 0}}.tool h3{{margin:0 0 4px}}.tool p{{margin:0 0 8px;color:var(--muted)}}.feat{{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-soft)}}.pill{{font-size:.75rem;background:var(--accent);color:#fff;border-radius:20px;padding:2px 8px;margin-left:6px;vertical-align:middle}}</style>
<!-- ADSENSE: paste the AdSense <script> tag here once approved --></head><body>
<header><a class="logo" href="./">Freelance<span>Toolbox</span></a><nav><a href="./">Categories</a><a href="{SUBMIT}">Submit a tool</a></nav></header><main>"""
FOOT="""</main><footer>Freelance Toolbox is a hand-picked directory of software for freelancers. Some links may be affiliate links, which never change what you pay.
· Also see <a href="../freelance-calc/">free freelancer calculators</a>.</footer></body></html>"""
def card(n,u,d,feat=False):
    # AFFILIATE: swap u for an affiliate link when you join a program
    return f'<div class="tool{" feat" if feat else ""}"><h3>{html.escape(n)}{"<span class=pill>Featured</span>" if feat else ""}</h3><p>{html.escape(d)}</p><a href="{u}" rel="nofollow noopener" target="_blank">Visit {html.escape(n)} →</a></div>'
cats="".join(f'<a href="{slug(c)}.html"><strong>{c}</strong><span>{len(t)} tools: {", ".join(x[0] for x in t[:3])}…</span></a>' for c,t in data.items())
(OUT/"index.html").write_text(head("The Best Tools for Freelancers (Hand-Picked Directory)","A curated directory of the best software for freelancers: invoicing, time tracking, contracts, payments, finding clients and more.","")+
 f"""<h1>The best tools for freelancers</h1><p class="lead">A hand-picked directory of {sum(map(len,data.values()))} tools to run your freelance business, sorted by what you need to get done.</p>
<div class="cards">{cats}</div>
<h2>Make your tool stand out</h2><p>Build software for freelancers? <a href="{SUBMIT}">Submit it for free</a>, or ask about a featured spot at the top of a category.</p>"""+FOOT)
for c,t in data.items():
    s=slug(c); others="".join(f'<a href="{slug(o)}.html"><strong>{o}</strong></a>' for o in data if o!=c)
    (OUT/f"{s}.html").write_text(head(f"Best {c} Tools for Freelancers",f"The best {c.lower()} tools for freelancers, compared: "+", ".join(x[0] for x in t)+".",s+".html")+
      f'<h1>Best {c.lower()} tools for freelancers</h1><p class="lead">{len(t)} hand-picked options. Featured listings are paid placements and are clearly marked.</p>'+
      "".join(card(*x) for x in t)+f'<p><a href="{SUBMIT}">Suggest a tool for this list</a></p><h2>Other categories</h2><div class="cards">{others}</div>'+FOOT)
today=datetime.date.today().isoformat()
(OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+
  "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod></url>" for u in [""]+[slug(c)+".html" for c in data])+"</urlset>\n")
print("built",len(data),"categories")
