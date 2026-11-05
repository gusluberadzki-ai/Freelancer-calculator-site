"""Build Canva-ready template packs as PPTX (Canva imports PPTX as fully editable designs;
they also open in PowerPoint, Keynote and Google Slides). Fonts used: Montserrat and Playfair Display
(both free Google Fonts that Canva includes).
Usage: python3 build.py OUT_DIR"""
import sys, os, subprocess, glob
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
PX = 9525
SANS, SERIF = "Montserrat", "Playfair Display"

class Deck:
    def __init__(s, w, h):
        s.p = Presentation(); s.p.slide_width = Emu(w * PX); s.p.slide_height = Emu(h * PX); s.w, s.h = w, h
    def slide(s, bg):
        sl = s.p.slides.add_slide(s.p.slide_layouts[6]); s.s = sl
        f = sl.background.fill; f.solid(); f.fore_color.rgb = RGBColor.from_string(bg.strip("#")); return sl
    def rect(s, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE, line=None):
        sh = s.s.shapes.add_shape(shape, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
        if color: sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor.from_string(color.strip("#"))
        else: sh.fill.background()
        if line: sh.line.color.rgb = RGBColor.from_string(line.strip("#")); sh.line.width = Emu(3 * PX)
        else: sh.line.fill.background()
        sh.shadow.inherit = False
        return sh
    def oval(s, x, y, w, h, color, line=None): return s.rect(x, y, w, h, color, MSO_SHAPE.OVAL, line)
    def text(s, x, y, w, h, t, size, color="#1e1e1e", font=SANS, bold=False, align="l", anchor="t", italic=False, spacing=None):
        tb = s.s.shapes.add_textbox(Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
        tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        for i, line in enumerate(t.split("\n")):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
            if spacing: para.line_spacing = spacing
            r = para.add_run(); r.text = line
            r.font.size = Pt(size * 0.75); r.font.name = font; r.font.bold = bold; r.font.italic = italic
            r.font.color.rgb = RGBColor.from_string(color.strip("#"))
        return tb
    def photo(s, x, y, w, h, tint="#d9cfc3", shape=MSO_SHAPE.RECTANGLE, label="Drop your photo here"):
        if not isinstance(tint, str): shape, tint = tint, "#d9cfc3"
        s.rect(x, y, w, h, tint, shape)
        s.text(x, y + h / 2 - 20, w, 40, label, max(14, min(28, w / 16)), "#7a6e62", align="c")
    def save(s, path): s.p.save(path)

# ---------------------------------------------------------------- Instagram: small business
def instagram(path):
    C = dict(cream="#f6f1ea", ink="#1f1d1b", terra="#c4663f", sage="#8a9a7b", sand="#e7d8c6", white="#ffffff")
    d = Deck(1080, 1350); W, H = 1080, 1350
    def handle(col=C["ink"]): d.text(60, H - 90, W - 120, 40, "@yourbusiness", 26, col, align="c")
    # 1 announcement
    d.slide(C["terra"]); d.text(80, 380, W - 160, 120, "BIG NEWS", 40, C["cream"], bold=True, align="c")
    d.text(80, 470, W - 160, 400, "We're opening\na new shop", 110, C["cream"], SERIF, True, "c", spacing=0.95)
    d.rect(440, 930, 200, 6, C["cream"]); d.text(80, 980, W - 160, 60, "Saturday 12 March · 10am", 34, C["cream"], align="c"); handle(C["cream"])
    # 2 quote
    d.slide(C["cream"]); d.text(80, 260, W - 160, 200, "“", 300, C["terra"], SERIF, True, "c")
    d.text(110, 520, W - 220, 400, "Small steps every day add up to big results.", 72, C["ink"], SERIF, False, "c", italic=True)
    d.text(80, 1000, W - 160, 50, "— YOUR NAME", 30, C["terra"], bold=True, align="c"); handle()
    # 3 sale
    d.slide(C["ink"]); d.text(80, 250, W - 160, 80, "WEEKEND SALE", 46, C["sand"], bold=True, align="c")
    d.text(80, 360, W - 160, 420, "30%\nOFF", 230, C["terra"], SERIF, True, "c", spacing=0.85)
    d.rect(290, 930, 500, 100, C["sand"], MSO_SHAPE.ROUNDED_RECTANGLE); d.text(290, 955, 500, 60, "Use code SAVE30", 36, C["ink"], bold=True, align="c"); handle(C["sand"])
    # 4 product spotlight
    d.slide(C["sand"]); d.photo(90, 90, 900, 820, "#d8c6b0"); d.text(90, 960, 900, 90, "Product name", 76, C["ink"], SERIF, True)
    d.text(90, 1060, 700, 100, "Short description of what makes it special.", 32, C["ink"]); d.text(800, 1060, 190, 60, "$39", 54, C["terra"], bold=True, align="r"); handle()
    # 5 tip
    d.slide(C["sage"]); d.text(90, 140, 400, 60, "TIP #01", 38, C["cream"], bold=True)
    d.text(90, 230, 900, 500, "How to keep your plants alive in winter", 92, C["white"], SERIF, True, spacing=0.95)
    for i, t in enumerate(["Water less often", "Move them nearer the light", "Wipe dust off the leaves"]):
        d.oval(90, 800 + i * 120, 70, 70, C["cream"]); d.text(90, 812 + i * 120, 70, 50, str(i + 1), 34, C["sage"], bold=True, align="c")
        d.text(190, 812 + i * 120, 800, 60, t, 40, C["white"])
    handle(C["cream"])
    # 6 testimonial
    d.slide(C["cream"]); d.oval(440, 170, 200, 200, "#d8c6b0"); d.text(80, 420, W - 160, 60, "★★★★★", 60, C["terra"], align="c")
    d.text(110, 530, W - 220, 380, "“Absolutely love it. Fast delivery and the quality is even better than the photos.”", 56, C["ink"], SERIF, False, "c", italic=True)
    d.text(80, 960, W - 160, 50, "SARAH M. · VERIFIED CUSTOMER", 28, C["ink"], bold=True, align="c"); handle()
    # 7 new arrival
    d.slide(C["white"]); d.photo(0, 0, W, 900, "#e4dbd0"); d.rect(0, 900, W, 450, C["ink"])
    d.text(80, 960, 700, 60, "NEW ARRIVAL", 34, C["sand"], bold=True); d.text(80, 1030, 920, 140, "The Autumn Collection", 80, C["cream"], SERIF, True)
    d.text(80, 1180, 920, 60, "Shop now · link in bio", 32, C["sand"])
    # 8 behind the scenes
    d.slide(C["cream"]); d.photo(80, 80, 450, 600, "#d8c6b0"); d.photo(550, 80, 450, 600, "#cbbba7")
    d.text(80, 740, 920, 80, "BEHIND THE SCENES", 36, C["terra"], bold=True); d.text(80, 810, 920, 300, "A day in the studio: packing your orders with love", 70, C["ink"], SERIF, True); handle()
    # 9 FAQ
    d.slide(C["sand"]); d.text(90, 120, 900, 80, "FAQ", 54, C["terra"], bold=True)
    for i, (q, a) in enumerate([("Do you ship worldwide?", "Yes, to over 40 countries."), ("How long does delivery take?", "3 to 5 working days in the US."), ("Can I return my order?", "Of course, within 30 days.")]):
        d.text(90, 260 + i * 300, 900, 70, q, 46, C["ink"], SERIF, True); d.text(90, 340 + i * 300, 900, 80, a, 34, C["ink"])
    handle()
    # 10 carousel cover
    d.slide(C["terra"]); d.text(90, 200, 900, 80, "SAVE THIS POST", 36, C["cream"], bold=True)
    d.text(90, 300, 900, 600, "5 mistakes new small business owners make", 104, C["cream"], SERIF, True, spacing=0.95)
    d.text(90, 1100, 900, 60, "Swipe →", 44, C["cream"], bold=True, align="r")
    # 11 carousel slide
    d.slide(C["cream"]); d.text(90, 120, 300, 200, "01", 180, C["terra"], SERIF, True)
    d.text(90, 400, 900, 200, "Not tracking your numbers", 80, C["ink"], SERIF, True)
    d.text(90, 640, 900, 400, "If you don't know your profit per order, you can't price properly. Spend 10 minutes a week updating your books.", 40, C["ink"], spacing=1.2)
    d.text(90, 1180, 900, 60, "→", 60, C["terra"], bold=True, align="r")
    # 12 giveaway
    d.slide(C["sage"]); d.text(80, 160, W - 160, 200, "GIVEAWAY", 130, C["cream"], SERIF, True, "c")
    d.photo(240, 400, 600, 450, "#a9b59c", MSO_SHAPE.ROUNDED_RECTANGLE)
    for i, t in enumerate(["1. Follow @yourbusiness", "2. Like this post", "3. Tag 2 friends"]): d.text(80, 900 + i * 70, W - 160, 60, t, 40, C["white"], bold=True, align="c")
    d.text(80, 1170, W - 160, 50, "Winner announced Friday", 30, C["cream"], align="c")
    # 13 thank you
    d.slide(C["ink"]); d.text(80, 470, W - 160, 300, "Thank you", 150, C["cream"], SERIF, False, "c", italic=True)
    d.text(80, 720, W - 160, 120, "for 10,000 followers", 54, C["sand"], align="c"); d.rect(440, 870, 200, 6, C["terra"]); handle(C["sand"])
    # 14 event / workshop
    d.slide(C["cream"]); d.rect(0, 0, W, 520, C["terra"]); d.text(90, 140, 900, 80, "FREE WORKSHOP", 40, C["cream"], bold=True)
    d.text(90, 220, 900, 280, "Branding basics for beginners", 86, C["cream"], SERIF, True)
    for i, (k, v) in enumerate([("DATE", "Thursday 18 May"), ("TIME", "6pm - 7:30pm"), ("WHERE", "Online · Zoom")]):
        d.text(90, 620 + i * 160, 300, 50, k, 30, C["terra"], bold=True); d.text(90, 670 + i * 160, 900, 70, v, 52, C["ink"], SERIF)
    d.rect(90, 1120, 420, 100, C["ink"], MSO_SHAPE.ROUNDED_RECTANGLE); d.text(90, 1147, 420, 60, "Book your seat", 34, C["cream"], bold=True, align="c")
    # 15 CTA / link in bio
    d.slide(C["sand"]); d.oval(240, 150, 600, 600, C["terra"]); d.text(240, 330, 600, 260, "Shop\nnow", 120, C["cream"], SERIF, True, "c", spacing=0.9)
    d.text(80, 830, W - 160, 200, "New pieces every Friday. Free shipping over $50.", 50, C["ink"], SERIF, False, "c")
    d.text(80, 1080, W - 160, 60, "LINK IN BIO", 38, C["ink"], bold=True, align="c"); handle()
    d.save(path)

# ---------------------------------------------------------------- Pinterest pins
def pinterest(path):
    pal = [("#1d3557", "#f1faee", "#e63946"), ("#fefae0", "#283618", "#bc6c25"), ("#2a2a2a", "#ffffff", "#ffb703"), ("#f8edeb", "#3d405b", "#e07a5f"), ("#e9f5db", "#1b4332", "#52b788")]
    d = Deck(1000, 1500); W, H = 1000, 1500
    def site(fg): d.text(60, H - 90, W - 120, 40, "yourwebsite.com", 28, fg, bold=True, align="c")
    for i in range(10):
        bg, fg, ac = pal[i % 5]; d.slide(bg)
        k = i
        if k == 0:
            d.photo(0, 0, W, 700); d.rect(60, 620, W - 120, 560, bg); d.text(110, 680, W - 220, 70, "THE ULTIMATE GUIDE TO", 36, ac, bold=True, align="c")
            d.text(110, 760, W - 220, 360, "Starting a side hustle", 96, fg, SERIF, True, "c"); site(fg)
        elif k == 1:
            d.text(80, 120, W - 160, 300, "10", 280, ac, SERIF, True, "c"); d.text(80, 460, W - 160, 300, "easy ways to save money every month", 80, fg, SERIF, True, "c")
            d.photo(80, 830, W - 160, 500, label="Drop your photo"); site(fg)
        elif k == 2:
            d.text(80, 100, W - 160, 200, "Morning routine checklist", 84, fg, SERIF, True, "c")
            for j, t in enumerate(["Drink a glass of water", "Make your bed", "10 minutes of stretching", "Plan your top 3 tasks", "Healthy breakfast", "No phone for 30 minutes"]):
                d.rect(120, 400 + j * 150, 60, 60, None, line=ac); d.text(220, 405 + j * 150, 700, 60, t, 44, fg)
            site(fg)
        elif k == 3:
            d.photo(0, 0, W / 2 - 5, 900, label="Before"); d.photo(W / 2 + 5, 0, W / 2 - 5, 900, "#cbbba7", label="After")
            d.text(80, 960, W - 160, 300, "Small bedroom makeover on a budget", 80, fg, SERIF, True, "c"); site(fg)
        elif k == 4:
            d.text(100, 380, W - 200, 600, "“Done is better than perfect.”", 110, fg, SERIF, False, "c", italic=True); d.rect(400, 1080, 200, 8, ac); site(fg)
        elif k == 5:
            d.photo(100, 100, W - 200, 800, MSO_SHAPE.ROUNDED_RECTANGLE); d.text(80, 960, W - 160, 90, "NEW IN THE SHOP", 40, ac, bold=True, align="c")
            d.text(80, 1040, W - 160, 200, "Linen tote bag", 92, fg, SERIF, True, "c"); site(fg)
        elif k == 6:
            d.photo(0, 0, W, 760); d.text(80, 810, W - 160, 200, "15-minute creamy tomato pasta", 78, fg, SERIF, True, "c")
            for j, (a, b) in enumerate([("15", "MIN"), ("4", "SERVES"), ("$", "BUDGET")]):
                d.text(100 + j * 280, 1120, 240, 90, a, 70, ac, SERIF, True, "c"); d.text(100 + j * 280, 1210, 240, 50, b, 26, fg, bold=True, align="c")
            site(fg)
        elif k == 7:
            d.text(80, 110, W - 160, 220, "Best books to read this year", 84, fg, SERIF, True, "c")
            for j in range(5):
                d.text(120, 420 + j * 170, 100, 100, f"{j + 1}", 80, ac, SERIF, True); d.text(250, 440 + j * 170, 650, 60, "Book title by Author", 44, fg)
            site(fg)
        elif k == 8:
            d.text(80, 100, W - 160, 200, "How to start a blog in 4 steps", 82, fg, SERIF, True, "c")
            for j, t in enumerate(["Pick your niche", "Choose a platform", "Write 5 posts", "Share on Pinterest"]):
                y = 400 + j * 240; d.oval(110, y, 140, 140, ac); d.text(110, y + 35, 140, 80, str(j + 1), 60, bg, SERIF, True, "c"); d.text(290, y + 40, 620, 80, t, 50, fg, bold=True)
            site(fg)
        else:
            d.rect(80, 120, W - 160, 1200, None, line=ac); d.text(120, 220, W - 240, 80, "FREE DOWNLOAD", 44, ac, bold=True, align="c")
            d.text(120, 330, W - 240, 320, "Printable weekly meal planner", 96, fg, SERIF, True, "c"); d.photo(220, 720, W - 440, 420, MSO_SHAPE.ROUNDED_RECTANGLE, label="Product mockup")
            d.rect(270, 1190, 460, 90, ac, MSO_SHAPE.ROUNDED_RECTANGLE); d.text(270, 1213, 460, 50, "Get it now", 36, bg, bold=True, align="c")
    d.save(path)

# ---------------------------------------------------------------- Resumes (US Letter)
def resumes(path):
    d = Deck(816, 1056); W, H = 816, 1056
    jobs = [("Senior Marketing Manager", "Brightline Co.", "2022 - Present", ["Grew organic traffic 140% in 18 months", "Led a team of 5 across content and paid social", "Cut cost per lead by 32%"]),
            ("Marketing Specialist", "Northwind Studio", "2019 - 2022", ["Launched 3 product campaigns", "Built the email programme from 0 to 40k subscribers"])]
    skills = ["SEO & content", "Paid social", "Email marketing", "Google Analytics", "Team leadership", "Copywriting"]
    # A: classic serif
    d.slide("#ffffff"); d.text(60, 60, W - 120, 70, "ALEX MORGAN", 46, "#1e1e1e", SERIF, True, "c")
    d.text(60, 130, W - 120, 30, "Marketing Manager · alex@email.com · (555) 123-4567 · New York, NY", 13, "#555555", align="c"); d.rect(60, 175, W - 120, 2, "#1e1e1e")
    y = 200
    for head, body in [("PROFILE", "Marketing manager with 7 years' experience growing brands through content, SEO and paid social. I turn data into campaigns that sell.")]:
        d.text(60, y, 200, 24, head, 14, "#1e1e1e", bold=True); d.text(60, y + 28, W - 120, 60, body, 13, "#333333", spacing=1.2); y += 110
    d.text(60, y, 200, 24, "EXPERIENCE", 14, "#1e1e1e", bold=True); y += 34
    for t, c, dt, bl in jobs:
        d.text(60, y, 450, 24, f"{t}, {c}", 14, "#1e1e1e", SERIF, True); d.text(W - 260, y, 200, 24, dt, 12, "#555555", align="r"); y += 28
        d.text(76, y, W - 140, 22 * len(bl), "\n".join("• " + b for b in bl), 12.5, "#333333", spacing=1.25); y += 24 * len(bl) + 18
    d.text(60, y, 200, 24, "EDUCATION", 14, "#1e1e1e", bold=True); d.text(60, y + 28, W - 120, 24, "BA Communications, State University · 2019", 13, "#333333"); y += 80
    d.text(60, y, 200, 24, "SKILLS", 14, "#1e1e1e", bold=True); d.text(60, y + 28, W - 120, 24, " · ".join(skills), 13, "#333333")
    # B: modern sidebar
    d.slide("#ffffff"); d.rect(0, 0, 270, H, "#1f3a5f"); d.oval(60, 50, 150, 150, "#c9d6e3"); d.text(60, 113, 150, 24, "Photo", 13, "#1f3a5f", align="c")
    d.text(30, 230, 210, 40, "CONTACT", 14, "#c9d6e3", bold=True); d.text(30, 262, 220, 110, "alex@email.com\n(555) 123-4567\nNew York, NY\nlinkedin.com/in/alex", 12, "#ffffff", spacing=1.35)
    d.text(30, 400, 210, 30, "SKILLS", 14, "#c9d6e3", bold=True); d.text(30, 432, 220, 200, "\n".join(skills), 12, "#ffffff", spacing=1.5)
    d.text(30, 650, 210, 30, "EDUCATION", 14, "#c9d6e3", bold=True); d.text(30, 682, 220, 80, "BA Communications\nState University, 2019", 12, "#ffffff", spacing=1.35)
    d.text(310, 60, 460, 60, "Alex Morgan", 44, "#1f3a5f", SANS, True); d.text(310, 120, 460, 30, "MARKETING MANAGER", 15, "#4f6d8f", bold=True)
    d.text(310, 175, 470, 80, "Marketing manager with 7 years' experience growing brands through content, SEO and paid social.", 13, "#333333", spacing=1.25)
    y = 270; d.text(310, y, 300, 30, "EXPERIENCE", 15, "#1f3a5f", bold=True); d.rect(310, y + 28, 460, 2, "#1f3a5f"); y += 46
    for t, c, dt, bl in jobs:
        d.text(310, y, 460, 24, t, 15, "#1e1e1e", bold=True); y += 24; d.text(310, y, 460, 22, f"{c} · {dt}", 12, "#4f6d8f"); y += 26
        d.text(322, y, 450, 22 * len(bl), "\n".join("• " + b for b in bl), 12.5, "#333333", spacing=1.25); y += 24 * len(bl) + 24
    # C: minimal accent
    d.slide("#fbfaf7"); d.rect(60, 60, 12, 110, "#c4663f"); d.text(95, 55, 600, 70, "Alex Morgan", 52, "#1e1e1e", SERIF, False)
    d.text(95, 130, 650, 30, "Marketing Manager  |  alex@email.com  |  (555) 123-4567", 13, "#666666")
    y = 220
    for head in ["About", "Experience", "Skills"]:
        d.text(60, y, 160, 30, head, 18, "#c4663f", SERIF, True)
        if head == "About": d.text(230, y + 2, 520, 70, "I build marketing programmes that grow revenue. 7 years across content, SEO, paid social and email.", 13, "#333333", spacing=1.25); y += 100
        elif head == "Experience":
            for t, c, dt, bl in jobs:
                d.text(230, y + 2, 520, 22, f"{t} · {c}", 14, "#1e1e1e", bold=True); d.text(230, y + 26, 520, 20, dt, 12, "#888888")
                d.text(230, y + 50, 520, 22 * len(bl), "\n".join("— " + b for b in bl), 12.5, "#333333", spacing=1.25); y += 70 + 24 * len(bl) + 10
            y += 10
        else: d.text(230, y + 2, 520, 60, " / ".join(skills), 13, "#333333", spacing=1.3)
    # D: cover letter matching B
    d.slide("#ffffff"); d.rect(0, 0, W, 130, "#1f3a5f"); d.text(60, 35, 500, 50, "Alex Morgan", 36, "#ffffff", bold=True); d.text(60, 85, 600, 24, "alex@email.com · (555) 123-4567 · New York, NY", 12, "#c9d6e3")
    d.text(60, 180, W - 120, 700, "12 March 2027\n\nDear Hiring Manager,\n\nI'm excited to apply for the Senior Marketing Manager role at Company. In my current role at Brightline Co. I grew organic traffic by 140% and cut cost per lead by a third, and I'd love to bring that same focus on results to your team.\n\n[Paragraph 2: one or two achievements that match the job.]\n\n[Paragraph 3: why this company, and a friendly close.]\n\nThank you for your time and consideration.\n\nKind regards,\nAlex Morgan", 14, "#333333", spacing=1.35)
    d.save(path)

# ---------------------------------------------------------------- Etsy shop branding kit (one PPTX per size)
def etsy_kit(folder):
    os.makedirs(folder, exist_ok=True)
    themes = [("#f6f1ea", "#1f1d1b", "#c4663f"), ("#1d3557", "#f1faee", "#e9c46a")]
    d = Deck(3360, 840)
    for bg, fg, ac in themes:
        d.slide(bg); d.text(0, 230, 3360, 240, "Your Shop Name", 200, fg, SERIF, True, "c"); d.rect(1530, 500, 300, 8, ac)
        d.text(0, 550, 3360, 80, "HANDMADE GIFTS · DIGITAL PRINTABLES · FREE SHIPPING OVER $35", 54, fg, align="c")
    d.save(os.path.join(folder, "1-shop-banner-3360x840.pptx"))
    d = Deck(500, 500)
    for bg, fg, ac in themes:
        d.slide(bg); d.oval(40, 40, 420, 420, None, line=ac); d.text(0, 150, 500, 160, "YS", 150, fg, SERIF, True, "c"); d.text(0, 330, 500, 40, "YOUR SHOP", 26, ac, bold=True, align="c")
    d.save(os.path.join(folder, "2-shop-icon-500x500.pptx"))
    d = Deck(2000, 1600)
    for bg, fg, ac in themes + [("#e9f5db", "#1b4332", "#52b788")]:
        d.slide(bg); d.photo(1000, 120, 880, 1360, MSO_SHAPE.ROUNDED_RECTANGLE, label="Product mockup")
        d.text(120, 380, 820, 480, "Product\nName Here", 150, fg, SERIF, True, spacing=0.95)
        d.text(120, 900, 820, 100, "Printable PDF · A4 & US Letter", 52, fg)
        d.rect(120, 1080, 520, 120, ac, MSO_SHAPE.ROUNDED_RECTANGLE); d.text(120, 1110, 520, 70, "Instant download", 46, bg, bold=True, align="c")
    d.save(os.path.join(folder, "3-listing-thumbnail-2000x1600.pptx"))
    d = Deck(1200, 1800)
    for bg, fg, ac in themes:
        d.slide(bg); d.text(80, 420, 1040, 300, "Thank you", 200, fg, SERIF, False, "c", italic=True); d.rect(500, 760, 200, 8, ac)
        d.text(120, 820, 960, 400, "for supporting my small shop. I hope you love your order as much as I loved making it.", 60, fg, align="c", spacing=1.25)
        d.text(80, 1300, 1040, 70, "Leave a review and get 15% off with code THANKYOU15", 40, ac, bold=True, align="c"); d.text(80, 1600, 1040, 60, "yourshop.etsy.com", 40, fg, align="c")
    d.save(os.path.join(folder, "4-thank-you-card-4x6in.pptx"))

def to_png(pptx, outdir, res=40):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", outdir, pptx], capture_output=True, timeout=300)
    pdf = os.path.join(outdir, os.path.basename(pptx).replace(".pptx", ".pdf"))
    stem = os.path.join(outdir, os.path.basename(pptx).replace(".pptx", ""))
    subprocess.run(["pdftoppm", "-r", str(res), "-png", pdf, stem], check=True); os.remove(pdf)

packs = os.path.join(OUT, "packs"); prev = os.path.join(OUT, "previews"); os.makedirs(packs, exist_ok=True); os.makedirs(prev, exist_ok=True)
instagram(os.path.join(packs, "Instagram-Post-Templates-Small-Business.pptx"))
pinterest(os.path.join(packs, "Pinterest-Pin-Templates.pptx"))
resumes(os.path.join(packs, "Resume-Templates.pptx"))
etsy_kit(os.path.join(packs, "Etsy-Shop-Branding-Kit"))
for f in glob.glob(os.path.join(packs, "*.pptx")) + glob.glob(os.path.join(packs, "*/*.pptx")):
    to_png(f, prev, 60)
print("ok")
