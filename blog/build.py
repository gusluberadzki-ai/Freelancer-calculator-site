"""Builds the RateKit blog into /blog/. Run: python3 build.py
Posts live in posts.py. Affiliate links and Gumroad products live in affiliates.json:
paste a referral link into "ref" (or set a product's "published" to true) and rebuild."""
import pathlib, json, html, re, datetime
OUT = pathlib.Path(__file__).parent
SITE = "https://gusluberadzki-ai.github.io/Freelancer-calculator-site/"
BASE = SITE + "blog/"
exec((OUT / "posts.py").read_text())
CFG = json.loads((OUT / "affiliates.json").read_text())
AFF, PROD = CFG["links"], CFG["products"]
BY_SLUG = {p["slug"]: p for p in POSTS}

def shortcodes(body, depth):
    up = "../" * depth  # path back to site root
    def aff(m):
        k, text = m.group(1), m.group(2)
        a = AFF[k]
        return f'<a href="{html.escape(a["ref"] or a["url"])}" rel="sponsored nofollow noopener" target="_blank">{text or a["name"]}</a>'
    def tool(m):
        return f'<a href="{up}{m.group(1)}">{m.group(2)}</a>'
    def post(m):
        assert m.group(1) in BY_SLUG, m.group(1)
        return f'<a href="{up}blog/{m.group(1)}/">{m.group(2)}</a>'
    def prod(m):
        p = PROD[m.group(1)]
        if not p["published"]:
            return ""
        return f'<aside class="cta"><strong>{html.escape(p["name"])}</strong><span>{html.escape(p["pitch"])}</span><a class="btn" href="{p["url"]}" target="_blank" rel="noopener">Get it on Gumroad</a></aside>'
    body = re.sub(r"\[\[aff:(\w+)(?:\|([^\]]+))?\]\]", aff, body)
    body = re.sub(r"\[\[tool:([^|\]]+)\|([^\]]+)\]\]", tool, body)
    body = re.sub(r"\[\[post:([^|\]]+)\|([^\]]+)\]\]", post, body)
    body = re.sub(r"\[\[product:(\w+)\]\]", prod, body)
    assert "[[" not in body, body[body.index("[["):][:80]
    return body

CSS = """article table{width:100%;border-collapse:collapse;margin:16px 0;font-size:.95rem;display:block;overflow-x:auto}
article th,article td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}article th{background:var(--accent-soft)}
.meta{color:var(--muted);font-size:.9rem}.disclosure{font-size:.85rem;color:var(--muted);background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px}
.cta{display:flex;flex-direction:column;gap:6px;background:var(--accent-soft);border-radius:12px;padding:16px;margin:24px 0}.cta span{color:var(--muted)}
.btn{display:inline-block;align-self:flex-start;border-radius:8px;padding:10px 16px;font-weight:600;background:var(--accent);color:#fff;text-decoration:none}
article li{margin:4px 0}.tag{display:inline-block;font-size:.78rem;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:.04em}"""

def page(title, desc, path, body, depth, extra_head=""):
    up = "../" * depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="article">
<link rel="alternate" type="application/rss+xml" title="RateKit Blog" href="{up}blog/feed.xml">
<link rel="stylesheet" href="{up}freelance-calc/style.css"><style>{CSS}</style>{extra_head}
<!-- ADSENSE: paste the AdSense <script> tag here once approved --></head><body>
<header><a class="logo" href="{up}freelance-calc/">Rate<span>Kit</span></a><nav><a href="{up}blog/">Blog</a><a href="{up}tools/">Free tools</a></nav></header><main>
{body}<p class="allaccess" style="background:var(--accent-soft);border-radius:10px;padding:12px 14px;margin-top:28px;font-size:.93rem"><strong>RateKit All-Access:</strong> Pro in every RateKit app plus 50+ spreadsheet and printable templates, CHF 6/month. <a href="{up}pro/">See what's included</a></p></main><footer>RateKit Blog: practical money and tools guides for freelancers. Some links are affiliate links; see our <a href="{up}blog/disclosure.html">disclosure</a>. Not financial or tax advice. · <a href="{up}freelance-calc/privacy.html">Privacy</a></footer></body></html>"""

def words(s):
    return len(re.sub("<[^>]+>", " ", s).split())

POSTS.sort(key=lambda p: p["date"], reverse=True)
for p in POSTS:
    d = OUT / p["slug"]; d.mkdir(exist_ok=True)
    body = shortcodes(p["body"], 2)
    mins = max(1, round(words(body) / 220))
    related = [q for q in POSTS if q is not p and q["tag"] == p["tag"]][:3] or [q for q in POSTS if q is not p][:3]
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"],
                     "author": {"@type": "Organization", "name": "RateKit"}, "publisher": {"@type": "Organization", "name": "RateKit"}, "mainEntityOfPage": BASE + p["slug"] + "/"})
    has_aff = "[[aff:" in p["body"]
    art = f"""<article><span class="tag">{html.escape(p['tag'])}</span><h1>{html.escape(p['title'])}</h1>
<p class="meta">{datetime.date.fromisoformat(p['date']).strftime('%-d %B %Y')} · {mins} min read</p>
{'<p class="disclosure">This article contains affiliate links. If you sign up through them we may earn a commission, at no extra cost to you. It never affects what we recommend.</p>' if has_aff else ''}
{body}
<div class="ad"><!-- ad slot --></div>
<h2>Free tools for this</h2><div class="cards">{''.join(f'<a href="../../{u}"><strong>{html.escape(n)}</strong></a>' for n, u in p['tools'])}</div>
<h2>Keep reading</h2><div class="cards">{''.join(f'<a href="../{q["slug"]}/"><strong>{html.escape(q["title"])}</strong><span>{html.escape(q["desc"][:90])}…</span></a>' for q in related)}</div></article>
<script type="application/ld+json">{ld}</script>"""
    (d / "index.html").write_text(page(p["title"] + " | RateKit", p["desc"], f"blog/{p['slug']}/", art, 2))

tags = {}
for p in POSTS: tags.setdefault(p["tag"], []).append(p)
idx = '<h1>RateKit Blog</h1><p class="lead">Practical guides on pricing, getting paid, taxes, tools and money for freelancers and the self-employed.</p>'
for t, ps in tags.items():
    idx += f"<h2>{html.escape(t)}</h2><div class='cards'>" + "".join(f'<a href="{p["slug"]}/"><strong>{html.escape(p["title"])}</strong><span>{html.escape(p["desc"][:110])}…</span></a>' for p in ps) + "</div>"
(OUT / "index.html").write_text(page("RateKit Blog: Money and Tools Guides for Freelancers", "Guides for freelancers on setting rates, invoicing, getting paid abroad, taxes, budgeting and the best tools.", "blog/", idx, 1))
(OUT / "disclosure.html").write_text(page("Affiliate Disclosure | RateKit", "How RateKit earns money from affiliate links and ads.", "blog/disclosure.html",
 "<h1>Affiliate disclosure</h1><p>RateKit's tools and articles are free. To keep them free, some links to products and services are affiliate links: if you click one and sign up or buy, we may receive a commission from the company at no extra cost to you. Pages may also show advertising.</p><p>We only recommend products we think are genuinely useful for freelancers and small businesses, and commission never decides what we include or how we rank it. Prices and features change, so always check the provider's own site before buying.</p><p>Nothing on this site is financial, legal or tax advice.</p>", 1))
now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
items = "".join(f"<item><title>{html.escape(p['title'])}</title><link>{BASE}{p['slug']}/</link><guid>{BASE}{p['slug']}/</guid><pubDate>{datetime.datetime.fromisoformat(p['date']).strftime('%a, %d %b %Y 09:00:00 +0000')}</pubDate><description>{html.escape(p['desc'])}</description></item>" for p in POSTS)
(OUT / "feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>RateKit Blog</title><link>{BASE}</link><description>Money and tools guides for freelancers</description><lastBuildDate>{now}</lastBuildDate>{items}</channel></rss>\n')
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{m}</lastmod></url>" for u, m in [("", POSTS[0]["date"]), ("disclosure.html", POSTS[0]["date"])] + [(p["slug"] + "/", p["date"]) for p in POSTS]) + "</urlset>\n")
print(len(POSTS), "posts,", sum(words(p["body"]) for p in POSTS), "words")
