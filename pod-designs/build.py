"""Generate original print-on-demand designs (shirts, stickers, mugs, posters).

Output: transparent 4500x5400 PNGs (Teepublic/Redbubble apparel size) in two inks:
  light-shirts/  dark ink for white, cream, pastel garments
  dark-shirts/   cream ink for black, navy, charcoal garments
Plus a preview contact sheet.

Fonts are SIL Open Font License (Google Fonts), which allows commercial use in artwork.
Run: python3 pod-designs/build.py OUT_DIR FONT_DIR
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
FONTS = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/fonts")
W, H = 4500, 5400

NAVY = (31, 42, 68)
CREAM = (246, 234, 214)
MUSTARD = (234, 165, 61)
ORANGE = (226, 96, 58)
RUST = (177, 68, 46)
TEAL = (42, 127, 122)
PINK = (229, 143, 160)
SAGE = (134, 166, 120)
SKY = (120, 176, 206)
PLUM = (110, 63, 104)


def F(name, size):
    paths = {
        "anton": "Anton-Regular.ttf", "bebas": "BebasNeue-Regular.ttf",
        "pacifico": "Pacifico-Regular.ttf", "abril": "AbrilFatface-Regular.ttf",
        "lobster": "Lobster-Regular.ttf", "righteous": "Righteous-Regular.ttf",
        "caveat": "Caveat.ttf", "archivo": "ArchivoBlack-Regular.ttf",
        "bungee": "Bungee-Regular.ttf", "monoton": "Monoton-Regular.ttf",
        "shrikhand": "Shrikhand-Regular.ttf",
    }
    if name == "mono":
        return ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-ExtraBold.ttf", size) \
            if os.path.exists("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-ExtraBold.ttf") \
            else ImageFont.truetype(_find("JetBrainsMono-ExtraBold"), size)
    return ImageFont.truetype(os.path.join(FONTS, paths[name]), size)


def _find(stem):
    for root, _, files in os.walk("/usr/share/fonts"):
        for f in files:
            if f.startswith(stem):
                return os.path.join(root, f)
    raise FileNotFoundError(stem)


def canvas():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def fit(name, text, max_w, max_size=1400):
    size = max_size
    while size > 20:
        f = F(name, size)
        l, t, r, b = f.getbbox(text)
        if r - l <= max_w:
            return f
        size = int(size * 0.95)
    return F(name, size)


def text_c(d, cx, y, text, font, fill, anchor="mt"):
    d.text((cx, y), text, font=font, fill=fill, anchor=anchor)
    l, t, r, b = d.textbbox((cx, y), text, font=font, anchor=anchor)
    return b


def shadow_text(d, cx, y, text, font, fill, shade, depth=40, step=4, anchor="mt"):
    for i in range(depth, 0, -step):
        d.text((cx + i, y + i), text, font=font, fill=shade, anchor=anchor)
    return text_c(d, cx, y, text, font, fill, anchor) + depth


def stack(d, lines, cx, y, max_w, gap=40):
    """lines: list of (text, fontname, fill[, shade]). Each line fitted to max_w."""
    for item in lines:
        text, fname, fill = item[:3]
        f = fit(fname, text, max_w)
        if len(item) > 3:
            y = shadow_text(d, cx, y, text, f, fill, item[3])
        else:
            y = text_c(d, cx, y, text, f, fill)
        y += gap
    return y


def sunset(img, cx, cy, r, colors, gaps=5):
    """Retro striped sun: colour bands top to bottom, with transparent slits in the lower half."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    n = len(colors)
    band = 2 * r / n
    for i, c in enumerate(colors):
        d.rectangle([cx - r, cy - r + i * band, cx + r, cy - r + (i + 1) * band + 2], fill=c)
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    for g in range(gaps):
        gy = cy + r * (0.1 + g * 0.19)
        h = r * (0.025 + g * 0.012)
        md.rectangle([cx - r, gy, cx + r, gy + h], fill=0)
    img.alpha_composite(Image.composite(layer, Image.new("RGBA", img.size, (0, 0, 0, 0)), mask))


def arc_text(img, text, cx, cy, radius, font, fill, center_deg=-90, spacing=1.0, bottom=False):
    """Draw text along a circle. center_deg -90 = top. bottom=True reads left-to-right along the bottom."""
    d = ImageDraw.Draw(img)
    widths = [font.getlength(ch) * spacing for ch in text]
    total = sum(widths)
    ang_total = total / radius
    if bottom:
        a = math.radians(90) + ang_total / 2
    else:
        a = math.radians(center_deg) - ang_total / 2
    for ch, w in zip(text, widths):
        da = w / radius
        mid = a - da / 2 if bottom else a + da / 2
        x = cx + radius * math.cos(mid)
        y = cy + radius * math.sin(mid)
        size = int(font.size * 1.6)
        g = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((size / 2, size / 2), ch, font=font, fill=fill, anchor="mm")
        rot = -math.degrees(mid) - 90 if not bottom else -math.degrees(mid) + 90
        g = g.rotate(rot, resample=Image.BICUBIC)
        img.alpha_composite(g, (int(x - size / 2), int(y - size / 2)))
        a = a - da if bottom else a + da
    return d


def ring(d, cx, cy, r, w, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=w)


def star(d, cx, cy, r, fill, points=5, inner=0.45, rot=-90):
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


# ---------- icons (drawn with shapes, scalable by s) ----------

def mug(d, cx, cy, s, body, ink, steam=True):
    w, h = 900 * s, 1000 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=120 * s, fill=body, outline=ink, width=int(60 * s))
    d.ellipse([cx + w / 2 - 80 * s, cy - 260 * s, cx + w / 2 + 360 * s, cy + 220 * s], outline=ink, width=int(70 * s))
    if steam:
        for i in (-1, 0, 1):
            x = cx + i * 260 * s
            for j in range(3):
                y0 = cy - h / 2 - 140 * s - j * 170 * s
                d.arc([x - 90 * s + (j % 2) * 60 * s, y0 - 170 * s, x + 90 * s + (j % 2) * 60 * s, y0], 90 if j % 2 else 270, 270 if j % 2 else 90, fill=ink, width=int(55 * s))


def leaf(d, cx, cy, s, angle, fill, vein):
    L, Wd = 900 * s, 380 * s
    pts = []
    for i in range(41):
        t = i / 40
        x = -L / 2 + L * t
        y = Wd / 2 * math.sin(math.pi * t) ** 0.8
        pts.append((x, y))
    pts += [(x, -y) for x, y in reversed(pts)]
    a = math.radians(angle)
    rot = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    d.polygon(rot, fill=fill)
    d.line([rot[0], rot[40]], fill=vein, width=int(28 * s))


def mountains(d, x0, y0, w, h, colors, snow=None):
    peaks = [(0.0, 1.0), (0.22, 0.25), (0.42, 0.62), (0.62, 0.0), (0.82, 0.45), (1.0, 1.0)]
    back = [(x0 + w * px, y0 + h * py) for px, py in peaks]
    d.polygon(back, fill=colors[0])
    front = [(x0, y0 + h), (x0 + w * 0.3, y0 + h * 0.45), (x0 + w * 0.55, y0 + h * 0.8), (x0 + w * 0.78, y0 + h * 0.5), (x0 + w, y0 + h)]
    d.polygon(front, fill=colors[1])
    if snow:
        px, py = x0 + w * 0.62, y0
        d.polygon([(px, py), (px - w * 0.07, py + h * 0.22), (px - w * 0.02, py + h * 0.17), (px + w * 0.02, py + h * 0.24), (px + w * 0.06, py + h * 0.2)], fill=snow)


def cat_head(d, cx, cy, s, fill, ink):
    r = 700 * s
    d.polygon([(cx - r * 0.95, cy - r * 0.2), (cx - r * 0.8, cy - r * 1.25), (cx - r * 0.2, cy - r * 0.8)], fill=fill)
    d.polygon([(cx + r * 0.95, cy - r * 0.2), (cx + r * 0.8, cy - r * 1.25), (cx + r * 0.2, cy - r * 0.8)], fill=fill)
    d.ellipse([cx - r, cy - r * 0.9, cx + r, cy + r * 0.85], fill=fill)
    # closed sleepy eyes
    for sx in (-1, 1):
        ex = cx + sx * r * 0.42
        d.arc([ex - r * 0.22, cy - r * 0.15, ex + r * 0.22, cy + r * 0.2], 20, 160, fill=ink, width=int(55 * s))
    d.polygon([(cx - r * 0.1, cy + r * 0.25), (cx + r * 0.1, cy + r * 0.25), (cx, cy + r * 0.38)], fill=ink)
    for sx in (-1, 1):
        for k in (-1, 0, 1):
            d.line([(cx + sx * r * 0.35, cy + r * 0.38 + k * r * 0.1), (cx + sx * r * 1.25, cy + r * 0.3 + k * r * 0.2)], fill=ink, width=int(26 * s))


def book(d, x, y, w, h, fill, ink):
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(h * 0.12), fill=fill, outline=ink, width=40)
    d.line([(x + w * 0.12, y + h * 0.3), (x + w * 0.88, y + h * 0.3)], fill=ink, width=36)
    d.line([(x + w * 0.12, y + h * 0.6), (x + w * 0.6, y + h * 0.6)], fill=ink, width=36)


def wave_band(d, y, amp, wl, h, fill, x0=0, x1=W, phase=0.0):
    pts = []
    for x in range(int(x0), int(x1) + 1, 20):
        pts.append((x, y + amp * math.sin(2 * math.pi * x / wl + phase)))
    pts += [(x1, y + h), (x0, y + h)]
    d.polygon(pts, fill=fill)


# ---------- designs ----------
DESIGNS = []


def design(slug):
    def deco(fn):
        DESIGNS.append((slug, fn))
        return fn
    return deco


@design("coffee-and-deadlines")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sunset(img, W / 2, 1700, 1300, [MUSTARD, ORANGE, RUST, PLUM])
    mug(d, W / 2, 1900, 1.1, CREAM, ink)
    stack(d, [("POWERED BY", "bebas", ink), ("COFFEE", "anton", ORANGE, ink), ("& DEADLINES", "anton", TEAL, ink)], W / 2, 3250, 3900, 30)


@design("out-of-office-mentally")
def _(img, ink):
    d = ImageDraw.Draw(img)
    y = stack(d, [("OUT OF", "anton", ink), ("OFFICE", "anton", ORANGE, ink)], W / 2, 900, 4100, 10)
    f = fit("pacifico", "(mentally)", 3000)
    text_c(d, W / 2, y + 40, "(mentally)", f, TEAL)
    for i, c in enumerate([MUSTARD, ORANGE, RUST]):
        d.rounded_rectangle([600, 4500 + i * 170, 3900, 4600 + i * 170], radius=50, fill=c)


@design("invoice-sent-vibes-pending")
def _(img, ink):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([700, 600, 3800, 2700], radius=120, fill=CREAM, outline=ink, width=70)
    text_c(d, W / 2, 800, "INVOICE #001", F("mono", 300), NAVY)
    for i in range(4):
        d.line([(1000, 1350 + i * 280), (3500 - (i % 2) * 700, 1350 + i * 280)], fill=SAGE, width=90)
    star(d, 3500, 2600, 380, MUSTARD)
    stack(d, [("INVOICE SENT.", "anton", ink), ("VIBES PENDING.", "anton", PINK, ink)], W / 2, 3100, 4000, 40)


@design("professional-overthinker")
def _(img, ink):
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, 2200
    for i, c in enumerate([PINK, MUSTARD, TEAL, ORANGE]):
        r = 1600 - i * 330
        ring(d, cx, cy, r, 110, c)
    d.ellipse([cx - 300, cy - 300, cx + 300, cy + 300], fill=ink)
    f = fit("pacifico", "Professional", 3600)
    text_c(d, W / 2, 3800, "Professional", f, ink, anchor="mm")
    f2 = fit("anton", "OVERTHINKER", 4100)
    shadow_text(d, W / 2, 4300, "OVERTHINKER", f2, ORANGE, ink)


@design("houseplant-collector")
def _(img, ink):
    d = ImageDraw.Draw(img)
    # pot
    d.polygon([(1500, 2500), (3000, 2500), (2800, 3500), (1700, 3500)], fill=RUST)
    d.rectangle([1400, 2350, 3100, 2600], fill=ORANGE)
    for ang, x, y, c in [(-60, 1900, 1700, SAGE), (-110, 2650, 1600, TEAL), (-20, 3000, 2100, SAGE), (-160, 1500, 2100, TEAL), (-90, 2250, 1200, SAGE)]:
        leaf(d, x, y, 1.3, ang, c, ink)
    stack(d, [("HOUSEPLANT", "anton", ink), ("COLLECTOR", "bebas", TEAL)], W / 2, 3800, 3900, 20)


@design("propagate-positivity")
def _(img, ink):
    d = ImageDraw.Draw(img)
    # jar with cutting
    d.rounded_rectangle([1650, 1600, 2850, 3300], radius=200, outline=ink, width=70, fill=(*SKY, 140))
    d.line([(2250, 700), (2250, 2800)], fill=SAGE, width=60)
    for ang, x, y in [(-40, 2650, 900), (-140, 1850, 1200), (-30, 2600, 1500)]:
        leaf(d, x, y, 1.0, ang, SAGE, ink)
    for k in range(7):
        a = math.radians(200 + k * 20)
        d.line([(2250, 2800), (2250 + 380 * math.cos(a + 1.2), 2800 + 380 * abs(math.sin(a)) + 100)], fill=CREAM if ink == CREAM else (210, 190, 160), width=24)
    f = fit("lobster", "Propagate", 3600)
    shadow_text(d, W / 2, 3550, "Propagate", f, TEAL, ink, depth=30)
    f2 = fit("bebas", "POSITIVITY", 3400)
    text_c(d, W / 2, 4350, "POSITIVITY", f2, ink)


@design("knead-more-sleep")
def _(img, ink):
    d = ImageDraw.Draw(img)
    # loaf
    d.ellipse([900, 1100, 3600, 2900], fill=MUSTARD, outline=ink, width=70)
    for i in range(3):
        x = 1600 + i * 650
        d.line([(x, 1500), (x + 350, 2400)], fill=RUST, width=90)
    for i, (x, y) in enumerate([(3500, 900), (3800, 600), (4050, 300)]):
        s = 260 - i * 50
        f = F("anton", s * 2)
        text_c(d, x, y, "z", f, SKY, anchor="mm")
    stack(d, [("KNEAD", "anton", ink), ("MORE SLEEP", "anton", ORANGE, ink)], W / 2, 3200, 3900, 30)


@design("cat-naps-lifestyle")
def _(img, ink):
    d = ImageDraw.Draw(img)
    d.ellipse([850, 500, 3650, 3300], fill=SKY)
    cat_head(d, W / 2, 2000, 1.4, MUSTARD, ink)
    for i, (x, y) in enumerate([(3300, 900), (3600, 650)]):
        text_c(d, x, y, "z", F("pacifico", 420 - i * 120), ink, anchor="mm")
    f = fit("pacifico", "Cat naps are", 3300)
    text_c(d, W / 2, 3700, "Cat naps are", f, ink, anchor="mm")
    f2 = fit("anton", "A LIFESTYLE", 3900)
    shadow_text(d, W / 2, 4200, "A LIFESTYLE", f2, PINK, ink)


@design("just-one-more-chapter-lies")
def _(img, ink):
    d = ImageDraw.Draw(img)
    colors = [TEAL, ORANGE, MUSTARD, PINK, SAGE]
    y = 2800
    for i, c in enumerate(colors):
        w = 2600 - (i % 3) * 300
        x = W / 2 - w / 2 + (i % 2) * 150 - 75
        book(d, x, y - i * 380, w, 340, c, ink)
    f = fit("bebas", "JUST ONE MORE", 3800)
    text_c(d, W / 2, 3300, "JUST ONE MORE", f, ink)
    f2 = fit("anton", "CHAPTER", 3900)
    b = shadow_text(d, W / 2, 3950, "CHAPTER", f2, ORANGE, ink)
    text_c(d, W / 2, b + 100, "(lies)", F("pacifico", 380), TEAL)


@design("running-on-spreadsheets")
def _(img, ink):
    d = ImageDraw.Draw(img)
    x0, y0, cw, ch = 900, 700, 540, 330
    for r in range(6):
        for c in range(5):
            fill = [CREAM, (*SAGE, 255), CREAM, (*MUSTARD, 255), CREAM][(r + c) % 5] if r else TEAL
            d.rectangle([x0 + c * cw, y0 + r * ch, x0 + (c + 1) * cw, y0 + (r + 1) * ch], fill=fill, outline=ink, width=28)
    # bar chart
    for i, h in enumerate([500, 800, 650, 1100]):
        d.rectangle([1200 + i * 550, 2900 - h, 1550 + i * 550, 2900], fill=ORANGE, outline=ink, width=30)
    y = stack(d, [("RUNNING ON", "bebas", ink), ("SPREADSHEETS", "anton", TEAL, ink)], W / 2, 3200, 4000, 30)
    text_c(d, W / 2, y + 60, "=SUM(COFFEE*HOURS)", F("mono", 230), ink)


@design("ctrl-alt-relax")
def _(img, ink):
    d = ImageDraw.Draw(img)
    keys = [("CTRL", ORANGE), ("ALT", MUSTARD), ("RELAX", TEAL)]
    y = 900
    for label, c in keys:
        d.rounded_rectangle([900, y + 60, 3600, y + 1060], radius=160, fill=ink)
        d.rounded_rectangle([900, y, 3600, y + 950], radius=160, fill=c, outline=ink, width=50)
        f = fit("archivo", label, 2200, 700)
        text_c(d, W / 2, y + 475, label, f, ink if c != TEAL else CREAM, anchor="mm")
        y += 1300


@design("weekend-forecast-hiking")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sunset(img, W / 2, 1800, 1300, [MUSTARD, ORANGE, RUST])
    mountains(d, 700, 1500, 3100, 1600, [TEAL, (30, 90, 86)], snow=CREAM)
    stack(d, [("WEEKEND FORECAST", "bebas", ink), ("100% HIKING", "anton", ORANGE, ink)], W / 2, 3400, 3900, 40)


@design("good-things-take-thyme")
def _(img, ink):
    d = ImageDraw.Draw(img)
    d.line([(2250, 600), (2250, 3000)], fill=SAGE, width=60)
    for i in range(9):
        y = 800 + i * 240
        side = -1 if i % 2 else 1
        leaf(d, 2250 + side * 260, y, 0.55, 180 + side * -30 if side < 0 else -30, SAGE, ink)
    f = fit("pacifico", "Good things", 3600)
    text_c(d, W / 2, 3350, "Good things", f, ink, anchor="mm")
    f2 = fit("anton", "TAKE THYME", 3900)
    shadow_text(d, W / 2, 3850, "TAKE THYME", f2, SAGE, ink)


@design("dog-hair-happiness")
def _(img, ink):
    d = ImageDraw.Draw(img)
    # paw
    d.ellipse([1550, 1500, 2950, 2800], fill=ORANGE)
    for x, y in [(1350, 1000), (1900, 650), (2600, 650), (3150, 1000)]:
        d.ellipse([x - 300, y - 360, x + 300, y + 360], fill=ORANGE)
    for _ in range(0, 360, 30):
        a = math.radians(_)
        d.line([(2250 + 1700 * math.cos(a), 1600 + 1700 * math.sin(a)), (2250 + 1900 * math.cos(a), 1600 + 1900 * math.sin(a))], fill=MUSTARD, width=60)
    stack(d, [("COVERED IN", "bebas", ink), ("DOG HAIR", "anton", TEAL, ink), ("& HAPPINESS", "bebas", ink)], W / 2, 3300, 3700, 20)


@design("fueled-by-tacos")
def _(img, ink):
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, 2300
    d.pieslice([cx - 1500, cy - 1300, cx + 1500, cy + 1700], 180, 360, fill=MUSTARD, outline=ink, width=70)
    for i, c in enumerate([SAGE, RUST, PINK, SAGE, RUST]):
        d.ellipse([cx - 1200 + i * 520, cy - 1000 + abs(2 - i) * 150, cx - 800 + i * 520, cy - 600 + abs(2 - i) * 150], fill=c)
    d.pieslice([cx - 1500, cy - 1300, cx + 1500, cy + 1700], 180, 360, outline=ink, width=70)
    d.line([(cx - 1500, cy + 200), (cx + 1500, cy + 200)], fill=ink, width=70)
    stack(d, [("FUELED BY", "bebas", ink), ("TACOS", "shrikhand", ORANGE, ink)], W / 2, 2900, 3800, 20)


@design("cozy-season")
def _(img, ink):
    d = ImageDraw.Draw(img)
    mug(d, W / 2, 1700, 1.4, PINK, ink)
    d.ellipse([1960, 1550, 2540, 2050], fill=CREAM if ink == NAVY else RUST)
    star(d, 900, 900, 220, MUSTARD)
    star(d, 3700, 1300, 160, MUSTARD)
    star(d, 3500, 600, 120, MUSTARD)
    f = fit("shrikhand", "Cozy", 3200)
    shadow_text(d, W / 2, 3000, "Cozy", f, ORANGE, ink)
    f2 = fit("bebas", "SEASON", 2600)
    text_c(d, W / 2, 4400, "SEASON", f2, ink)


@design("grumpy-before-coffee")
def _(img, ink):
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, 1700
    d.ellipse([cx - 1100, cy - 1100, cx + 1100, cy + 1100], fill=MUSTARD, outline=ink, width=70)
    for sx in (-1, 1):
        d.line([(cx + sx * 650, cy - 450), (cx + sx * 250, cy - 300)], fill=ink, width=80)
        d.ellipse([cx + sx * 450 - 110, cy - 200, cx + sx * 450 + 110, cy + 20], fill=ink)
    d.arc([cx - 450, cy + 350, cx + 450, cy + 900], 200, 340, fill=ink, width=80)
    stack(d, [("GRUMPY", "anton", ink), ("BEFORE COFFEE", "bebas", ORANGE)], W / 2, 3100, 3900, 20)


@design("debugging-my-life")
def _(img, ink):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([600, 700, 3900, 3000], radius=80, fill=NAVY if ink == CREAM else (40, 44, 52), outline=ink, width=60)
    for i, c in enumerate([ORANGE, MUSTARD, SAGE]):
        d.ellipse([800 + i * 220, 850, 950 + i * 220, 1000], fill=c)
    code = ["> debug(life)", "  coffee: OK", "  sleep: NOT FOUND", "  vibes: loading..."]
    for i, line in enumerate(code):
        c = [SAGE, CREAM, ORANGE, MUSTARD][i]
        d.text((850, 1250 + i * 400), line, font=F("mono", 250), fill=c)
    stack(d, [("DEBUGGING", "anton", ink), ("MY LIFE", "anton", TEAL, ink)], W / 2, 3300, 3700, 20)


@design("paddle-up-stress-down")
def _(img, ink):
    d = ImageDraw.Draw(img)
    for sx, c in [(-1, TEAL), (1, ORANGE)]:
        cx = W / 2 + sx * 550
        a = math.radians(sx * 20)
        pts = [(-450, -800), (450, -800), (450, 300), (130, 650), (130, 1300), (-130, 1300), (-130, 650), (-450, 300)]
        rot = [(cx + x * math.cos(a) - y * math.sin(a), 1700 + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
        d.polygon(rot, fill=c, outline=ink, width=60)
    d.ellipse([1950, 2600, 2550, 3200], fill=MUSTARD, outline=ink, width=40)
    for x, y in [(2120, 2780), (2380, 2780), (2250, 3000), (2100, 3020), (2400, 3020)]:
        d.ellipse([x - 40, y - 40, x + 40, y + 40], fill=ink)
    stack(d, [("PADDLE UP", "anton", ink), ("STRESS DOWN", "bebas", TEAL)], W / 2, 3450, 3700, 20)


@design("retro-sunset-mountains")
def _(img, ink):
    d = ImageDraw.Draw(img)
    cx, cy, r = W / 2, 2500, 1900
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([0, 0, W, H], fill=SKY)
    sunset(layer, cx, cy - 300, 900, [MUSTARD, ORANGE, RUST], gaps=4)
    mountains(ld, cx - r, cy - 200, 2 * r, 1300, [PLUM, TEAL], snow=CREAM)
    wave_band(ld, cy + 1050, 60, 900, 900, NAVY)
    img.alpha_composite(Image.composite(layer, Image.new("RGBA", img.size, (0, 0, 0, 0)), mask))
    ring(d, cx, cy, r + 60, 70, ink)


@design("ocean-waves-badge")
def _(img, ink):
    d = ImageDraw.Draw(img)
    cx, cy, r = W / 2, 2700, 1700
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([0, 0, W, H], fill=CREAM)
    sunset(layer, cx, cy - 400, 800, [PINK, ORANGE, RUST], gaps=3)
    for i, c in enumerate([SKY, TEAL, NAVY, TEAL]):
        wave_band(ld, cy + 100 + i * 300, 90, 1100, 2000, c, phase=i * 1.3)
    img.alpha_composite(Image.composite(layer, Image.new("RGBA", img.size, (0, 0, 0, 0)), mask))
    ring(d, cx, cy, r, 90, ink)
    arc_text(img, "SALT WATER STATE OF MIND", cx, cy, r + 300, F("bebas", 380), ink, spacing=1.15)


@design("night-owl-club")
def _(img, ink):
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, 2800
    d.ellipse([cx - 1200, cy - 1300, cx + 1200, cy + 1300], fill=PLUM)
    d.polygon([(cx - 1100, cy - 900), (cx - 900, cy - 1600), (cx - 400, cy - 1150)], fill=PLUM)
    d.polygon([(cx + 1100, cy - 900), (cx + 900, cy - 1600), (cx + 400, cy - 1150)], fill=PLUM)
    for sx in (-1, 1):
        ex = cx + sx * 500
        d.ellipse([ex - 450, cy - 800, ex + 450, cy + 100], fill=CREAM, outline=ink, width=50)
        d.ellipse([ex - 200, cy - 550, ex + 200, cy - 150], fill=NAVY)
        d.ellipse([ex - 60, cy - 480, ex + 60, cy - 360], fill=CREAM)
    d.polygon([(cx - 180, cy + 50), (cx + 180, cy + 50), (cx, cy + 400)], fill=MUSTARD)
    for i in range(3):
        for j in range(4):
            x = cx - 600 + j * 400 + (i % 2) * 200
            y = cy + 550 + i * 230
            d.arc([x - 140, y - 100, x + 140, y + 100], 20, 160, fill=MUSTARD, width=50)
    for x, y, s in [(3900, 3900, 140), (600, 3800, 170)]:
        star(d, x, y, s, MUSTARD)
    arc_text(img, "NIGHT OWL CLUB", cx, cy, 2200, F("anton", 520), ink, spacing=1.1)


@design("plant-more-worry-less")
def _(img, ink):
    d = ImageDraw.Draw(img)
    for i in range(7):
        a = math.radians(-90 + (i - 3) * 22)
        x = 2250 + 1000 * math.cos(a)
        y = 2600 + 1000 * math.sin(a)
        leaf(d, x, y, 1.15, math.degrees(a), [SAGE, TEAL][i % 2], ink)
    d.ellipse([2000, 2350, 2500, 2850], fill=MUSTARD)
    f = fit("anton", "PLANT MORE", 3800)
    shadow_text(d, W / 2, 3250, "PLANT MORE", f, SAGE, ink)
    f2 = fit("pacifico", "worry less", 3000)
    text_c(d, W / 2, 4700, "worry less", f2, ink, anchor="mm")


@design("self-employed-self-motivated")
def _(img, ink):
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, 2300
    ring(d, cx, cy, 1800, 90, ink)
    ring(d, cx, cy, 1300, 40, ink)
    d.ellipse([cx - 1250, cy - 1250, cx + 1250, cy + 1250], fill=MUSTARD)
    # laptop
    d.rounded_rectangle([cx - 800, cy - 650, cx + 800, cy + 350], radius=60, fill=CREAM, outline=ink, width=60)
    d.polygon([(cx - 1050, cy + 350), (cx + 1050, cy + 350), (cx + 900, cy + 550), (cx - 900, cy + 550)], fill=ink)
    star(d, cx, cy - 150, 300, ORANGE)
    arc_text(img, "SELF-EMPLOYED", cx, cy, 1550, F("anton", 360), ink, spacing=1.1)
    arc_text(img, "SELF-MOTIVATED", cx, cy, 1430, F("anton", 360), ink, spacing=1.1, bottom=True)
    star(d, cx - 1550, cy, 120, ORANGE)
    star(d, cx + 1550, cy, 120, ORANGE)


def preview_sheet(paths, out_path, bg):
    thumb = 600
    cols = 6
    rows = math.ceil(len(paths) / cols)
    sheet = Image.new("RGB", (cols * thumb, rows * int(thumb * 1.2)), bg)
    for i, p in enumerate(paths):
        im = Image.open(p)
        im.thumbnail((thumb - 40, int(thumb * 1.2) - 40))
        x = (i % cols) * thumb + (thumb - im.width) // 2
        y = (i // cols) * int(thumb * 1.2) + 20
        sheet.paste(im, (x, y), im)
    sheet.save(out_path, optimize=True)


def main():
    only = set(sys.argv[3:])
    for variant, ink in [("light-shirts", NAVY), ("dark-shirts", CREAM)]:
        os.makedirs(os.path.join(OUT, variant), exist_ok=True)
    out_light, out_dark = [], []
    for slug, fn in DESIGNS:
        if only and slug not in only:
            continue
        for variant, ink, acc in [("light-shirts", NAVY, out_light), ("dark-shirts", CREAM, out_dark)]:
            img = Image.new("RGBA", (W, 9000), (0, 0, 0, 0))
            fn(img, ink)
            bbox = img.getbbox()
            # recentre content and keep the standard canvas
            if bbox:
                crop = img.crop(bbox)
                pad = 150
                scale = min((W - 2 * pad) / crop.width, (H - 2 * pad) / crop.height, 1.0)
                if scale < 1:
                    crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.LANCZOS)
                img = canvas()
                img.alpha_composite(crop, ((W - crop.width) // 2, pad))
            p = os.path.join(OUT, variant, f"{slug}.png")
            img.save(p, optimize=True)
            acc.append(p)
            print(p)
    preview_sheet(out_light, os.path.join(OUT, "preview-light.png"), (238, 236, 230))
    preview_sheet(out_dark, os.path.join(OUT, "preview-dark.png"), (28, 30, 36))


if __name__ == "__main__":
    main()
