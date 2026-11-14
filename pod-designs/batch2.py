"""Batch 2: 54 more original print-on-demand designs (same format as build.py).

Reuses the drawing helpers in build.py. Output: OUT/light-shirts, OUT/dark-shirts, previews.
Run: python3 pod-designs/batch2.py OUT_DIR FONT_DIR [slug ...]
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402
from build import (W, NAVY, CREAM, MUSTARD, ORANGE, RUST, TEAL, PINK, SAGE, SKY, PLUM,  # noqa: E402
                   F, fit, text_c, shadow_text, stack, sunset, arc_text, ring, star, mug, leaf,
                   mountains, cat_head, book, wave_band)
from PIL import Image, ImageDraw  # noqa: E402

build.DESIGNS.clear()
design = build.design
GREEN = (96, 150, 84)
LIME = (170, 196, 92)
CX = W / 2


def lw(s, base=50):
    return max(4, int(base * s))


# ---------------- icons: (d, cx, cy, s, ink) ----------------

def heart(d, cx, cy, s, fill, ink=None):
    r = 420 * s
    pts = []
    for i in range(200):
        t = 2 * math.pi * i / 200
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * r / 16, cy - y * r / 16))
    d.polygon(pts, fill=fill, outline=ink, width=lw(s) if ink else 0)


def apple(d, cx, cy, s, ink):
    r = 600 * s
    d.ellipse([cx - r, cy - r * 0.9, cx + 30 * s, cy + r], fill=RUST, outline=ink, width=lw(s))
    d.ellipse([cx - 30 * s, cy - r * 0.9, cx + r, cy + r], fill=RUST, outline=ink, width=lw(s))
    d.rectangle([cx - 60 * s, cy - r * 0.85, cx + 60 * s, cy + r * 0.9], fill=RUST)
    d.line([(cx, cy - r * 0.7), (cx + 60 * s, cy - r * 1.25)], fill=ink, width=lw(s, 70))
    leaf(d, cx + 280 * s, cy - r * 1.05, 0.55 * s, -25, SAGE, ink)
    d.arc([cx - r * 0.7, cy - r * 0.6, cx - r * 0.1, cy + r * 0.2], 190, 250, fill=CREAM, width=lw(s, 60))


def battery(d, cx, cy, s, ink, level=0.08):
    w, h = 1900 * s, 950 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=110 * s, outline=ink, width=lw(s, 80))
    d.rounded_rectangle([cx + w / 2, cy - h * 0.2, cx + w / 2 + 160 * s, cy + h * 0.2], radius=40 * s, fill=ink)
    pad = 120 * s
    d.rounded_rectangle([cx - w / 2 + pad, cy - h / 2 + pad, cx - w / 2 + pad + (w - 2 * pad) * level, cy + h / 2 - pad], radius=40 * s, fill=ORANGE)


def pizza(d, cx, cy, s, ink):
    r = 1100 * s
    tip = (cx, cy + r * 0.85)
    l, rr = (cx - r * 0.75, cy - r * 0.55), (cx + r * 0.75, cy - r * 0.55)
    d.polygon([tip, l, rr], fill=MUSTARD, outline=ink, width=lw(s))
    d.rounded_rectangle([l[0] - 60 * s, l[1] - 180 * s, rr[0] + 60 * s, l[1] + 60 * s], radius=110 * s, fill=ORANGE, outline=ink, width=lw(s))
    for px, py in [(-0.25, -0.15), (0.22, -0.2), (0.0, 0.25), (-0.05, -0.35), (0.25, 0.1)]:
        rad = 120 * s
        d.ellipse([cx + px * r - rad, cy + py * r - rad, cx + px * r + rad, cy + py * r + rad], fill=RUST)
    d.ellipse([cx - 0.3 * r - 50 * s, cy + 0.05 * r, cx - 0.3 * r + 50 * s, cy + 0.05 * r + 100 * s], fill=SAGE)


def donut(d, cx, cy, s, ink):
    r = 900 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MUSTARD, outline=ink, width=lw(s))
    pts = []
    for i in range(120):
        a = 2 * math.pi * i / 120
        rr = r * (0.82 + 0.06 * math.sin(a * 7))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=PINK)
    hr = r * 0.32
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=(0, 0, 0, 0), outline=ink, width=lw(s))
    for i in range(14):
        a = 2 * math.pi * i / 14 + 0.3
        rr = r * (0.5 + 0.22 * ((i * 7) % 3) / 2)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        dx, dy = 70 * s * math.cos(a * 3), 70 * s * math.sin(a * 3)
        d.line([(x - dx, y - dy), (x + dx, y + dy)], fill=[TEAL, CREAM, ORANGE, SKY][i % 4], width=lw(s, 45))


def donut_hole(img, cx, cy, s):
    hr = 900 * s * 0.32 - lw(s) / 2
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=255)
    img.paste((0, 0, 0, 0), (0, 0), m)


def avocado(d, cx, cy, s, ink):
    def blob(scale, fill, outline=None):
        pts = []
        for i in range(160):
            a = 2 * math.pi * i / 160
            rx = 650 * s * scale
            ry = 900 * s * scale
            k = 1 - 0.28 * (1 - math.sin(a)) / 2  # narrower at top
            pts.append((cx + rx * math.cos(a) * k, cy + ry * math.sin(a)))
        d.polygon(pts, fill=fill, outline=outline, width=lw(s) if outline else 0)
    blob(1.0, GREEN, ink)
    blob(0.82, LIME)
    r = 300 * s
    d.ellipse([cx - r, cy + 80 * s, cx + r, cy + 80 * s + 2 * r], fill=RUST, outline=ink, width=lw(s, 35))


def teacup(d, cx, cy, s, ink, body=PINK):
    w, h = 1300 * s, 800 * s
    d.chord([cx - w / 2, cy - h, cx + w / 2, cy + h], 0, 180, fill=body, outline=ink, width=lw(s))
    d.line([(cx - w / 2, cy), (cx + w / 2, cy)], fill=ink, width=lw(s))
    d.ellipse([cx + w / 2 - 120 * s, cy + 60 * s, cx + w / 2 + 300 * s, cy + 440 * s], outline=ink, width=lw(s, 60))
    d.rounded_rectangle([cx - w * 0.7, cy + h - 40 * s, cx + w * 0.7, cy + h + 90 * s], radius=60 * s, fill=CREAM, outline=ink, width=lw(s, 40))
    for i in (-1, 1):
        x = cx + i * 230 * s
        for j in range(2):
            y0 = cy - 160 * s - j * 200 * s
            d.arc([x - 90 * s + (j % 2) * 60 * s, y0 - 200 * s, x + 90 * s + (j % 2) * 60 * s, y0], 90 if j % 2 else 270, 270 if j % 2 else 90, fill=ink, width=lw(s, 55))


def wine_glass(d, cx, cy, s, ink):
    w = 1000 * s
    d.chord([cx - w / 2, cy - 1100 * s, cx + w / 2, cy + 200 * s], 0, 180, fill=RUST)
    d.arc([cx - w / 2, cy - 1100 * s, cx + w / 2, cy + 200 * s], 0, 180, fill=ink, width=lw(s))
    d.line([(cx - w / 2, cy - 450 * s), (cx - w / 2, cy - 1000 * s)], fill=ink, width=lw(s))
    d.line([(cx + w / 2, cy - 450 * s), (cx + w / 2, cy - 1000 * s)], fill=ink, width=lw(s))
    d.rectangle([cx - w / 2 + 25 * s, cy - 500 * s, cx + w / 2 - 25 * s, cy - 450 * s], fill=RUST)
    d.line([(cx, cy + 200 * s), (cx, cy + 900 * s)], fill=ink, width=lw(s, 70))
    d.rounded_rectangle([cx - 380 * s, cy + 870 * s, cx + 380 * s, cy + 970 * s], radius=50 * s, fill=ink)


def chili(d, cx, cy, s, ink):
    pts = []
    for i in range(41):
        t = i / 40
        x = cx - 900 * s + 1700 * s * t
        y = cy - 250 * s + 500 * s * math.sin(t * math.pi * 0.9)
        wdt = 330 * s * (1 - t) ** 0.6
        pts.append((x, y, wdt))
    top = [(x, y - w) for x, y, w in pts]
    bot = [(x, y + w) for x, y, w in reversed(pts)]
    d.polygon(top + bot, fill=RUST, outline=ink, width=lw(s))
    d.rounded_rectangle([cx - 1100 * s, cy - 450 * s, cx - 820 * s, cy - 50 * s], radius=60 * s, fill=GREEN, outline=ink, width=lw(s, 40))
    d.line([(cx - 960 * s, cy - 420 * s), (cx - 1000 * s, cy - 720 * s)], fill=ink, width=lw(s, 60))


def controller(d, cx, cy, s, ink):
    w, h = 2300 * s, 1150 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=h / 2, fill=PLUM, outline=ink, width=lw(s, 60))
    px, py = cx - w * 0.27, cy
    a, b = 110 * s, 330 * s
    d.rectangle([px - a, py - b, px + a, py + b], fill=CREAM)
    d.rectangle([px - b, py - a, px + b, py + a], fill=CREAM)
    for (dx, dy), c in zip([(0, -1), (1, 0), (0, 1), (-1, 0)], [MUSTARD, ORANGE, TEAL, PINK]):
        bx, by = cx + w * 0.27 + dx * 250 * s, cy + dy * 250 * s
        d.ellipse([bx - 130 * s, by - 130 * s, bx + 130 * s, by + 130 * s], fill=c)


def palette(d, cx, cy, s, ink):
    pts = []
    for i in range(160):
        a = 2 * math.pi * i / 160
        r = 1000 * s * (1 + 0.08 * math.sin(3 * a))
        pts.append((cx + r * 1.15 * math.cos(a), cy + r * 0.85 * math.sin(a)))
    d.polygon(pts, fill=CREAM, outline=ink, width=lw(s))
    hx, hy = cx + 520 * s, cy + 280 * s
    d.ellipse([hx - 170 * s, hy - 170 * s, hx + 170 * s, hy + 170 * s], fill=(0, 0, 0, 0), outline=ink, width=lw(s))
    for (dx, dy), c in zip([(-0.6, -0.1), (-0.3, -0.5), (0.15, -0.55), (0.55, -0.3), (-0.45, 0.4)], [ORANGE, MUSTARD, TEAL, PINK, PLUM]):
        x, y = cx + dx * 1000 * s, cy + dy * 1000 * s
        d.ellipse([x - 170 * s, y - 150 * s, x + 170 * s, y + 150 * s], fill=c)


def palette_hole(img, cx, cy, s):
    hx, hy = cx + 520 * s, cy + 280 * s
    r = 170 * s - lw(s) / 2
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse([hx - r, hy - r, hx + r, hy + r], fill=255)
    img.paste((0, 0, 0, 0), (0, 0), m)


def yarn(img, cx, cy, s, ink):
    d = ImageDraw.Draw(img)
    r = 900 * s
    for sx in (-1, 1):
        d.line([(cx + sx * 350 * s, cy - r * 1.5), (cx - sx * 250 * s, cy + r * 0.2)], fill=MUSTARD, width=lw(s, 70))
        d.ellipse([cx + sx * 350 * s - 90 * s, cy - r * 1.5 - 90 * s, cx + sx * 350 * s + 90 * s, cy - r * 1.5 + 90 * s], fill=MUSTARD)
    d.line([(cx + r * 0.75, cy + r * 0.6), (cx + r * 1.3, cy + r * 1.0), (cx + r * 1.0, cy + r * 1.35), (cx + r * 1.5, cy + r * 1.5)], fill=ink, width=lw(s, 45), joint="curve")
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PINK)
    for k in range(-4, 5):
        ld.arc([cx - r * 2.2 + k * 230 * s, cy - r * 1.2, cx + k * 230 * s, cy + r * 1.2], 300, 60, fill=RUST, width=lw(s, 40))
    for k in range(-3, 4):
        ld.arc([cx - r * 1.2, cy - r * 2.0 + k * 240 * s, cx + r * 1.2, cy + k * 240 * s], 30, 150, fill=CREAM, width=lw(s, 32))
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.alpha_composite(Image.composite(layer, Image.new("RGBA", img.size, (0, 0, 0, 0)), m))
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink, width=lw(s))
    for sx in (-1, 1):
        d.line([(cx - sx * 250 * s, cy + r * 0.2), (cx - sx * 330 * s, cy + r * 0.45)], fill=MUSTARD, width=lw(s, 70))


def vinyl(d, cx, cy, s, ink):
    r = 1100 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY, outline=ink, width=lw(s))
    for k in (0.85, 0.72, 0.6):
        d.arc([cx - r * k, cy - r * k, cx + r * k, cy + r * k], 200, 260, fill=SKY, width=lw(s, 22))
        d.arc([cx - r * k, cy - r * k, cx + r * k, cy + r * k], 20, 80, fill=SKY, width=lw(s, 22))
    d.ellipse([cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35], fill=ORANGE)
    d.ellipse([cx - r * 0.05, cy - r * 0.05, cx + r * 0.05, cy + r * 0.05], fill=CREAM)


def dumbbell(d, cx, cy, s, ink, angle=0):
    d.rounded_rectangle([cx - 900 * s, cy - 90 * s, cx + 900 * s, cy + 90 * s], radius=40 * s, fill=ink)
    for sx in (-1, 1):
        for k, (hh, c) in enumerate([(600, ORANGE), (450, MUSTARD)]):
            x = cx + sx * (650 + k * 230) * s
            d.rounded_rectangle([x - 110 * s, cy - hh * s, x + 110 * s, cy + hh * s], radius=60 * s, fill=c, outline=ink, width=lw(s, 40))


def bicycle(d, cx, cy, s, ink):
    r = 620 * s
    lx, rx, wy = cx - 900 * s, cx + 900 * s, cy + 300 * s
    for x in (lx, rx):
        d.ellipse([x - r, wy - r, x + r, wy + r], outline=ink, width=lw(s, 70))
        d.ellipse([x - 60 * s, wy - 60 * s, x + 60 * s, wy + 60 * s], fill=ink)
    seat = (cx - 250 * s, cy - 500 * s)
    bb = (cx, wy)
    head = (cx + 650 * s, cy - 450 * s)
    for a, b in [((lx, wy), bb), ((lx, wy), seat), (seat, bb), (bb, head), (seat, head), (head, (rx, wy))]:
        d.line([a, b], fill=TEAL, width=lw(s, 80))
    d.rounded_rectangle([seat[0] - 220 * s, seat[1] - 120 * s, seat[0] + 160 * s, seat[1] - 20 * s], radius=50 * s, fill=ink)
    d.line([head, (head[0] - 120 * s, head[1] - 250 * s), (head[0] + 150 * s, head[1] - 300 * s)], fill=ink, width=lw(s, 60))


def sun(d, cx, cy, s, fill=MUSTARD, rays=12, ink=None):
    r = 600 * s
    for i in range(rays):
        a = 2 * math.pi * i / rays
        d.line([(cx + r * 1.25 * math.cos(a), cy + r * 1.25 * math.sin(a)), (cx + r * 1.65 * math.cos(a), cy + r * 1.65 * math.sin(a))], fill=fill, width=lw(s, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=ink, width=lw(s) if ink else 0)


def cloud(d, cx, cy, s, fill, ink):
    parts = [(-500, 100, 380), (-120, -150, 520), (380, 0, 430), (650, 180, 280), (-780, 220, 240)]
    for dx, dy, r in parts:
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=ink)
    for dx, dy, r in parts:
        r2 = r - 50
        d.ellipse([cx + (dx - r2) * s, cy + (dy - r2) * s, cx + (dx + r2) * s, cy + (dy + r2) * s], fill=fill)
    d.rectangle([cx - 780 * s, cy + 200 * s, cx + 650 * s, cy + 410 * s], fill=fill)
    d.line([(cx - 780 * s, cy + 435 * s), (cx + 650 * s, cy + 435 * s)], fill=ink, width=lw(s))


def rainbow(d, cx, cy, s, ink):
    colors = [ORANGE, MUSTARD, SAGE, SKY, PLUM]
    band = 180 * s
    R = 1300 * s
    for i, c in enumerate(colors):
        r = R - i * band
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=c)
    r = R - len(colors) * band
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(0, 0, 0, 0))


def clear_semi(img, cx, cy, r):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=255)
    img.paste((0, 0, 0, 0), (0, 0), m)


def sprout(d, cx, cy, s, ink):
    d.line([(cx, cy + 500 * s), (cx, cy - 300 * s)], fill=GREEN, width=lw(s, 80))
    leaf(d, cx - 420 * s, cy - 400 * s, 0.9 * s, 200, SAGE, ink)
    leaf(d, cx + 420 * s, cy - 550 * s, 0.9 * s, -20, GREEN, ink)
    d.chord([cx - 900 * s, cy + 350 * s, cx + 900 * s, cy + 1000 * s], 180, 360, fill=RUST)


def daisy(d, cx, cy, s, ink, petal=CREAM, center=MUSTARD):
    n = 12
    for i in range(n):
        a = 2 * math.pi * i / n
        px, py = cx + 560 * s * math.cos(a), cy + 560 * s * math.sin(a)
        pts = []
        for k in range(40):
            t = 2 * math.pi * k / 40
            x, y = 380 * s * math.cos(t), 170 * s * math.sin(t)
            pts.append((px + x * math.cos(a) - y * math.sin(a), py + x * math.sin(a) + y * math.cos(a)))
        d.polygon(pts, fill=petal, outline=ink, width=lw(s, 30))
    d.ellipse([cx - 300 * s, cy - 300 * s, cx + 300 * s, cy + 300 * s], fill=center, outline=ink, width=lw(s, 40))


def mushroom(d, cx, cy, s, ink, cap=RUST):
    d.rounded_rectangle([cx - 280 * s, cy - 400 * s, cx + 280 * s, cy + 800 * s], radius=200 * s, fill=CREAM, outline=ink, width=lw(s))
    d.chord([cx - 1000 * s, cy - 900 * s, cx + 1000 * s, cy + 300 * s], 180, 360, fill=cap, outline=ink, width=lw(s))
    d.line([(cx - 1000 * s, cy - 300 * s), (cx + 1000 * s, cy - 300 * s)], fill=ink, width=lw(s))
    for dx, dy, r in [(-500, -500, 130), (-50, -720, 110), (420, -560, 150), (150, -420, 80), (-750, -360, 70), (740, -380, 70)]:
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=CREAM)


def cactus(d, cx, cy, s, ink):
    def bar(x0, y0, x1, y1):
        d.rounded_rectangle([x0, y0, x1, y1], radius=(x1 - x0) / 2, fill=GREEN, outline=ink, width=lw(s))
    bar(cx - 260 * s, cy - 1100 * s, cx + 260 * s, cy + 700 * s)
    bar(cx - 820 * s, cy - 600 * s, cx - 500 * s, cy + 50 * s)
    d.rounded_rectangle([cx - 820 * s, cy - 150 * s, cx - 200 * s, cy + 170 * s], radius=150 * s, fill=GREEN, outline=ink, width=lw(s))
    bar(cx + 500 * s, cy - 850 * s, cx + 820 * s, cy - 200 * s)
    d.rounded_rectangle([cx + 200 * s, cy - 400 * s, cx + 820 * s, cy - 80 * s], radius=150 * s, fill=GREEN, outline=ink, width=lw(s))
    bar(cx - 260 * s, cy - 1100 * s, cx + 260 * s, cy + 700 * s)
    d.line([(cx, cy - 900 * s), (cx, cy + 600 * s)], fill=SAGE, width=lw(s, 30))
    d.polygon([(cx - 650 * s, cy + 600 * s), (cx + 650 * s, cy + 600 * s), (cx + 500 * s, cy + 1300 * s), (cx - 500 * s, cy + 1300 * s)], fill=ORANGE, outline=ink, width=lw(s))
    d.rectangle([cx - 720 * s, cy + 520 * s, cx + 720 * s, cy + 760 * s], fill=RUST, outline=ink, width=lw(s))
    daisy(d, cx, cy - 1150 * s, 0.35 * s, ink, petal=PINK)


def tent(d, cx, cy, s, ink):
    w, h = 2400 * s, 1500 * s
    base = cy + h / 2
    d.polygon([(cx - w / 2, base), (cx, base - h), (cx + w / 2, base)], fill=ORANGE, outline=ink, width=lw(s, 60))
    d.polygon([(cx - 330 * s, base), (cx, base - h * 0.55), (cx + 330 * s, base)], fill=NAVY, outline=ink, width=lw(s, 40))
    d.line([(cx, base - h), (cx - 150 * s, base - h - 250 * s)], fill=ink, width=lw(s, 50))
    d.line([(cx, base - h), (cx + 150 * s, base - h - 250 * s)], fill=ink, width=lw(s, 50))
    d.line([(cx - w / 2 - 300 * s, base), (cx + w / 2 + 300 * s, base)], fill=ink, width=lw(s, 60))


def campfire(d, cx, cy, s, ink):
    base = cy + 500 * s
    for sgn in (-1, 1):
        d.line([(cx - sgn * 700 * s, base + 150 * s), (cx + sgn * 700 * s, base - 120 * s)], fill=RUST, width=lw(s, 160))
    def flame(scale, fill):
        h, w = 1500 * s * scale, 560 * s * scale
        pts = []
        for i in range(101):
            t = i / 100  # 0 bottom-right -> 1 tip
            y = base - h * t
            half = w * math.sin(math.pi * (1 - t) ** 0.9) ** 0.9 * (1 - t) ** 0.25 if t > 0 else 0
            pts.append((cx + half + 80 * s * scale * math.sin(t * 6), y))
        left = [(cx - (x - cx) + 160 * s * scale * math.sin(t * 6) * 0, y) for (x, y), t in zip(reversed(pts), [1 - i / 100 for i in range(101)])]
        d.polygon(pts + left, fill=fill)
        d.ellipse([cx - w * 0.98, base - w * 0.9, cx + w * 0.98, base + w * 0.35], fill=fill)
    flame(1.0, ORANGE)
    flame(0.66, MUSTARD)
    flame(0.33, CREAM)


def fish(d, cx, cy, s, ink, body=TEAL):
    d.ellipse([cx - 1000 * s, cy - 480 * s, cx + 700 * s, cy + 480 * s], fill=body, outline=ink, width=lw(s))
    d.polygon([(cx + 600 * s, cy), (cx + 1150 * s, cy - 500 * s), (cx + 1150 * s, cy + 500 * s)], fill=body, outline=ink, width=lw(s))
    d.ellipse([cx - 1000 * s + 3, cy - 478 * s, cx + 700 * s - 3, cy + 478 * s], fill=body)
    d.ellipse([cx - 1000 * s, cy - 480 * s, cx + 700 * s, cy + 480 * s], outline=ink, width=lw(s))
    d.arc([cx - 500 * s, cy - 450 * s, cx + 100 * s, cy + 450 * s], 290, 70, fill=ink, width=lw(s, 40))
    d.ellipse([cx - 780 * s, cy - 180 * s, cx - 620 * s, cy - 20 * s], fill=ink)
    for k in range(3):
        x = cx + (0 + k * 180) * s
        d.arc([x - 120 * s, cy - 120 * s, x + 120 * s, cy + 120 * s], 300, 60, fill=SKY, width=lw(s, 30))


def hook(d, cx, cy, s, ink):
    d.line([(cx, cy - 900 * s), (cx, cy + 200 * s)], fill=ink, width=lw(s, 70))
    d.arc([cx - 500 * s, cy - 300 * s, cx, cy + 500 * s], 0, 180, fill=ink, width=lw(s, 70))
    d.polygon([(cx - 500 * s, cy + 100 * s), (cx - 560 * s, cy - 150 * s), (cx - 380 * s, cy - 20 * s)], fill=ink)
    d.ellipse([cx - 90 * s, cy - 1050 * s, cx + 90 * s, cy - 870 * s], outline=ink, width=lw(s, 45))


def bee(d, cx, cy, s, ink):
    for sx in (-1, 1):
        d.ellipse([cx + sx * 150 * s - 380 * s + sx * 150 * s, cy - 900 * s, cx + sx * 150 * s + 380 * s + sx * 150 * s, cy - 150 * s], fill=SKY, outline=ink, width=lw(s))
    m = Image.new("L", (1, 1))  # noqa: F841 (placeholder keeps signature simple)
    d.ellipse([cx - 800 * s, cy - 520 * s, cx + 800 * s, cy + 520 * s], fill=MUSTARD, outline=ink, width=lw(s))
    for x in (-250, 150):
        d.rectangle([cx + x * s, cy - 480 * s, cx + (x + 170) * s, cy + 480 * s], fill=ink)
    d.ellipse([cx - 800 * s, cy - 520 * s, cx + 800 * s, cy + 520 * s], outline=ink, width=lw(s))
    d.polygon([(cx + 780 * s, cy - 80 * s), (cx + 1050 * s, cy), (cx + 780 * s, cy + 80 * s)], fill=ink)
    d.ellipse([cx - 600 * s, cy - 160 * s, cx - 460 * s, cy - 20 * s], fill=ink)
    d.arc([cx - 720 * s, cy - 50 * s, cx - 420 * s, cy + 200 * s], 20, 160, fill=ink, width=lw(s, 35))
    for sx in (-1, 1):
        d.line([(cx - 650 * s, cy - 450 * s), (cx - 800 * s + sx * 120 * s, cy - 850 * s)], fill=ink, width=lw(s, 35))


def chicken(d, cx, cy, s, ink):
    for k, c in enumerate([RUST, MUSTARD, ORANGE]):
        a = math.radians(-150 + k * 25)
        x, y = cx - 650 * s + 520 * s * math.cos(a), cy + 50 * s + 520 * s * math.sin(a)
        leaf(d, x, y, 0.8 * s, math.degrees(a), c, ink)
    d.ellipse([cx - 900 * s, cy - 500 * s, cx + 700 * s, cy + 800 * s], fill=CREAM, outline=ink, width=lw(s))
    d.ellipse([cx + 100 * s, cy - 1000 * s, cx + 800 * s, cy - 200 * s], fill=CREAM, outline=ink, width=lw(s))
    d.ellipse([cx - 900 * s + lw(s), cy - 500 * s + lw(s), cx + 700 * s - lw(s), cy + 800 * s - lw(s)], fill=CREAM)
    d.ellipse([cx + 100 * s + lw(s), cy - 1000 * s + lw(s), cx + 800 * s - lw(s), cy - 200 * s - lw(s)], fill=CREAM)
    for k in range(3):
        x = cx + (250 + k * 170) * s
        d.ellipse([x - 120 * s, cy - 1180 * s, x + 120 * s, cy - 920 * s], fill=RUST)
    d.polygon([(cx + 780 * s, cy - 650 * s), (cx + 1050 * s, cy - 560 * s), (cx + 780 * s, cy - 470 * s)], fill=MUSTARD, outline=ink, width=lw(s, 30))
    d.ellipse([cx + 700 * s, cy - 480 * s, cx + 860 * s, cy - 280 * s], fill=RUST)
    d.ellipse([cx + 470 * s, cy - 720 * s, cx + 590 * s, cy - 600 * s], fill=ink)
    d.arc([cx - 500 * s, cy - 100 * s, cx + 300 * s, cy + 500 * s], 20, 160, fill=ink, width=lw(s, 40))
    for x in (-250, 150):
        d.line([(cx + x * s, cy + 780 * s), (cx + x * s, cy + 1150 * s)], fill=MUSTARD, width=lw(s, 60))
        d.line([(cx + (x - 120) * s, cy + 1150 * s), (cx + (x + 120) * s, cy + 1150 * s)], fill=MUSTARD, width=lw(s, 60))


def frog(d, cx, cy, s, ink):
    for sx in (-1, 1):
        ex = cx + sx * 500 * s
        d.ellipse([ex - 380 * s, cy - 1000 * s, ex + 380 * s, cy - 250 * s], fill=GREEN, outline=ink, width=lw(s))
    d.ellipse([cx - 1100 * s, cy - 700 * s, cx + 1100 * s, cy + 700 * s], fill=GREEN, outline=ink, width=lw(s))
    for sx in (-1, 1):
        ex = cx + sx * 500 * s
        d.ellipse([ex - 380 * s + lw(s), cy - 1000 * s + lw(s), ex + 380 * s - lw(s), cy - 250 * s], fill=GREEN)
        d.ellipse([ex - 240 * s, cy - 860 * s, ex + 240 * s, cy - 380 * s], fill=CREAM)
        d.ellipse([ex - 120 * s, cy - 700 * s, ex + 120 * s, cy - 460 * s], fill=NAVY)
        d.ellipse([ex - 450 * s, cy - 100 * s, ex - 150 * s, cy + 100 * s] if sx < 0 else [ex + 150 * s, cy - 100 * s, ex + 450 * s, cy + 100 * s], fill=PINK)
    d.arc([cx - 600 * s, cy - 400 * s, cx + 600 * s, cy + 300 * s], 25, 155, fill=ink, width=lw(s))


def dog_head(d, cx, cy, s, ink, fill=MUSTARD):
    r = 800 * s
    for sx in (-1, 1):
        d.ellipse([cx + sx * r * 0.95 - 300 * s, cy - r * 0.8, cx + sx * r * 0.95 + 300 * s, cy + r * 0.6], fill=RUST, outline=ink, width=lw(s))
    d.ellipse([cx - r, cy - r, cx + r, cy + r * 0.95], fill=fill, outline=ink, width=lw(s))
    d.ellipse([cx - r * 0.5, cy + r * 0.05, cx + r * 0.5, cy + r * 0.85], fill=CREAM)
    for sx in (-1, 1):
        ex = cx + sx * r * 0.38
        d.ellipse([ex - 90 * s, cy - r * 0.35 - 90 * s, ex + 90 * s, cy - r * 0.35 + 90 * s], fill=ink)
    d.ellipse([cx - 170 * s, cy + r * 0.1, cx + 170 * s, cy + r * 0.38], fill=ink)
    d.arc([cx - 250 * s, cy + r * 0.25, cx, cy + r * 0.6], 20, 160, fill=ink, width=lw(s, 35))
    d.arc([cx, cy + r * 0.25, cx + 250 * s, cy + r * 0.6], 20, 160, fill=ink, width=lw(s, 35))
    d.chord([cx - 120 * s, cy + r * 0.45, cx + 120 * s, cy + r * 0.85], 0, 180, fill=PINK)


def paw(d, cx, cy, s, fill):
    d.ellipse([cx - 500 * s, cy - 250 * s, cx + 500 * s, cy + 550 * s], fill=fill)
    for dx, dy in [(-650, -450), (-230, -820), (230, -820), (650, -450)]:
        d.ellipse([cx + (dx - 200) * s, cy + (dy - 250) * s, cx + (dx + 200) * s, cy + (dy + 250) * s], fill=fill)


def moon(img, cx, cy, s, fill):
    r = 900 * s
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    m = Image.new("L", img.size, 255)
    ImageDraw.Draw(m).ellipse([cx - r * 0.45, cy - r * 1.15, cx + r * 1.4, cy + r * 0.75], fill=0)
    img.alpha_composite(Image.composite(layer, Image.new("RGBA", img.size, (0, 0, 0, 0)), m))


def ghost(d, cx, cy, s, ink):
    w, h = 1400 * s, 1700 * s
    top = cy - h / 2
    pts = []
    for i in range(61):
        a = math.pi + math.pi * i / 60
        pts.append((cx + w / 2 * math.cos(a), top + w / 2 + w / 2 * math.sin(a)))
    n = 4
    for i in range(n * 10 + 1):
        t = i / (n * 10)
        x = cx + w / 2 - w * t
        y = cy + h / 2 - 140 * s * abs(math.sin(math.pi * n * t))
        pts.append((x, y))
    d.polygon(pts, fill=CREAM, outline=ink, width=lw(s))
    for sx in (-1, 1):
        d.ellipse([cx + sx * 260 * s - 110 * s, cy - 300 * s, cx + sx * 260 * s + 110 * s, cy - 50 * s], fill=NAVY)
    d.ellipse([cx - 120 * s, cy + 50 * s, cx + 120 * s, cy + 300 * s], fill=NAVY)
    for sx in (-1, 1):
        d.ellipse([cx + sx * 480 * s - 110 * s, cy + 0 * s, cx + sx * 480 * s + 110 * s, cy + 140 * s], fill=PINK)


def pumpkin(d, cx, cy, s, ink):
    for dx, w in [(-520, 700), (520, 700), (-250, 760), (250, 760), (0, 800)]:
        d.ellipse([cx + (dx - w / 2) * s, cy - 650 * s, cx + (dx + w / 2) * s, cy + 650 * s], fill=ORANGE, outline=ink, width=lw(s))
    d.rounded_rectangle([cx - 90 * s, cy - 950 * s, cx + 110 * s, cy - 600 * s], radius=50 * s, fill=GREEN, outline=ink, width=lw(s, 40))
    leaf(d, cx + 380 * s, cy - 820 * s, 0.6 * s, -15, SAGE, ink)


def snowflake(d, cx, cy, s, fill):
    r = 1000 * s
    for i in range(6):
        a = math.pi / 3 * i
        ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
        d.line([(cx, cy), (ex, ey)], fill=fill, width=lw(s, 90))
        for k in (0.45, 0.72):
            bx, by = cx + r * k * math.cos(a), cy + r * k * math.sin(a)
            for sg in (-1, 1):
                b = a + sg * math.radians(45)
                L = r * (0.32 if k < 0.6 else 0.22)
                d.line([(bx, by), (bx + L * math.cos(b), by + L * math.sin(b))], fill=fill, width=lw(s, 70))
    d.ellipse([cx - 120 * s, cy - 120 * s, cx + 120 * s, cy + 120 * s], fill=fill)


def pine(d, cx, cy, s, fill, ink):
    for k, (w, y) in enumerate([(1500, 300), (1150, -250), (800, -750)]):
        d.polygon([(cx - w / 2 * s, cy + y * s + 450 * s), (cx, cy + y * s - 300 * s), (cx + w / 2 * s, cy + y * s + 450 * s)], fill=fill, outline=ink, width=lw(s, 40))
    d.rectangle([cx - 110 * s, cy + 750 * s, cx + 110 * s, cy + 1050 * s], fill=RUST, outline=ink, width=lw(s, 30))
    star(d, cx, cy - 1080 * s, 230 * s, MUSTARD)


def progress(d, cx, cy, s, ink, frac=0.7):
    w, h = 3000 * s, 520 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=h / 2, outline=ink, width=lw(s, 70))
    pad = 90 * s
    d.rounded_rectangle([cx - w / 2 + pad, cy - h / 2 + pad, cx - w / 2 + pad + (w - 2 * pad) * frac, cy + h / 2 - pad], radius=(h - 2 * pad) / 2, fill=MUSTARD)


def heartbeat(d, cx, cy, s, ink, color=ORANGE):
    pts = [(-1600, 0), (-600, 0), (-400, -300), (-200, 500), (50, -900), (300, 400), (450, 0), (1600, 0)]
    d.line([(cx + x * s, cy + y * s) for x, y in pts], fill=color, width=lw(s, 110), joint="curve")


def house_door(d, cx, cy, s, ink):
    d.polygon([(cx - 900 * s, cy - 200 * s), (cx, cy - 1000 * s), (cx + 900 * s, cy - 200 * s)], fill=RUST, outline=ink, width=lw(s))
    d.rectangle([cx - 700 * s, cy - 200 * s, cx + 700 * s, cy + 800 * s], fill=CREAM, outline=ink, width=lw(s))
    d.rectangle([cx - 200 * s, cy + 200 * s, cx + 200 * s, cy + 800 * s], fill=TEAL, outline=ink, width=lw(s, 40))
    d.rectangle([cx - 600 * s, cy, cx - 320 * s, cy + 280 * s], fill=SKY, outline=ink, width=lw(s, 35))
    d.rectangle([cx + 320 * s, cy, cx + 600 * s, cy + 280 * s], fill=SKY, outline=ink, width=lw(s, 35))


def palm(d, cx, cy, s, ink):
    d.line([(cx, cy + 1200 * s), (cx + 150 * s, cy + 400 * s), (cx + 80 * s, cy - 400 * s)], fill=RUST, width=lw(s, 150), joint="curve")
    for ang in (-160, -120, -60, -20, -90):
        a = math.radians(ang)
        leaf(d, cx + 80 * s + 520 * s * math.cos(a), cy - 400 * s + 520 * s * math.sin(a), 1.2 * s, ang, GREEN, ink)


def bars(d, y, x0=700, x1=3800, colors=(MUSTARD, ORANGE, RUST), h=100, gap=170):
    for i, c in enumerate(colors):
        d.rounded_rectangle([x0, y + i * gap, x1, y + i * gap + h], radius=h / 2, fill=c)


# ---------------- layout templates ----------------

def icon_top(img, ink, draw_icon, lines, text_y=3000, gap=30):
    d = ImageDraw.Draw(img)
    draw_icon(d)
    return stack(d, lines, CX, text_y, 3900, gap)


def badge(img, ink, top, bottom, fill, draw_icon, r=1750, cy=2600, font="anton", fsize=380):
    d = ImageDraw.Draw(img)
    ring(d, CX, cy, r, 90, ink)
    ring(d, CX, cy, r - 520, 40, ink)
    d.ellipse([CX - r + 560, cy - r + 560, CX + r - 560, cy + r - 560], fill=fill)
    draw_icon(d)
    arc_text(img, top, CX, cy, r - 270, F(font, fsize), ink, spacing=1.1)
    if bottom:
        arc_text(img, bottom, CX, cy, r - 380, F(font, fsize), ink, spacing=1.1, bottom=True)
    star(d, CX - r + 260, cy, 110, ORANGE)
    star(d, CX + r - 260, cy, 110, ORANGE)


def script_bold(img, ink, script, bold, color, script_color=None, y=900, under=True, bold_font="anton", shade=True, script_w=3400):
    d = ImageDraw.Draw(img)
    f = fit("pacifico", script, script_w)
    yb = text_c(d, CX, y, script, f, script_color or ink)
    item = (bold, bold_font, color, ink) if shade else (bold, bold_font, color)
    yb = stack(d, [item], CX, yb + 20, 4000)
    if under:
        bars(d, yb + 150)
    return yb


# ---------------- designs ----------------

@design("cat-hair-is-my-glitter")
def _(img, ink):
    d = ImageDraw.Draw(img)
    cat_head(d, CX, 1700, 1.25, MUSTARD, ink)
    for x, y, r in [(900, 900, 160), (3600, 1100, 120), (3800, 2300, 90), (700, 2200, 110)]:
        star(d, x, y, r, PINK, points=4, inner=0.3)
    stack(d, [("CAT HAIR", "anton", ink), ("IS MY GLITTER", "anton", PINK, ink)], CX, 2900, 3900, 30)


@design("dog-walks-coffee-talks")
def _(img, ink):
    d = ImageDraw.Draw(img)
    paw(d, CX - 900, 1700, 0.9, ORANGE)
    mug(d, CX + 900, 1800, 0.9, CREAM, ink)
    stack(d, [("DOG WALKS", "anton", TEAL, ink), ("& COFFEE TALKS", "bebas", ink)], CX, 2900, 3900, 30)


@design("just-here-for-the-chickens")
def _(img, ink):
    icon_top(img, ink, lambda d: chicken(d, CX, 1500, 1.1, ink),
             [("JUST HERE FOR", "bebas", ink), ("THE CHICKENS", "anton", RUST, ink)], 2900)


@design("bee-kind")
def _(img, ink):
    d = ImageDraw.Draw(img)
    bee(d, CX, 1600, 1.25, ink)
    for i in range(5):
        x = 900 + i * 280
        d.ellipse([x - 40, 2500 - 60 * math.sin(i), x + 40, 2580 - 60 * math.sin(i)], fill=ink)
    f = fit("shrikhand", "Bee Kind", 3800)
    shadow_text(d, CX, 2900, "Bee Kind", f, MUSTARD, ink)


@design("cozy-frog-club")
def _(img, ink):
    d = ImageDraw.Draw(img)
    frog(d, CX - 250, 2800, 0.95, ink)
    mushroom(d, CX + 1150, 3000, 0.45, ink)
    mushroom(d, CX - 1450, 3250, 0.3, ink, cap=MUSTARD)
    arc_text(img, "COZY FROG CLUB", CX, 2300, 1900, F("anton", 480), ink, spacing=1.1)
    for x, y in [(700, 3600), (3800, 3500)]:
        star(d, x, y, 150, MUSTARD)


@design("ruled-by-a-cat")
def _(img, ink):
    def icon(d):
        cat_head(d, CX, 2700, 0.85, ORANGE, ink)
        for i, x in enumerate((-260, 0, 260)):
            d.polygon([(CX + x - 150, 1900), (CX + x, 1650 - (60 if i == 1 else 0)), (CX + x + 150, 1900)], fill=MUSTARD)
        d.rectangle([CX - 410, 1880, CX + 410, 1990], fill=MUSTARD)
    badge(img, ink, "RULED BY A CAT", "LOYAL SUBJECT", SKY, icon)


@design("proud-rescue-parent")
def _(img, ink):
    def icon(d):
        heart(d, CX, 2600, 2.2, PINK, ink)
        paw(d, CX, 2650, 0.65, CREAM)
    badge(img, ink, "PROUD RESCUE", "PARENT", MUSTARD, icon)


@design("dog-person-forever")
def _(img, ink):
    icon_top(img, ink, lambda d: dog_head(d, CX, 1600, 1.2, ink),
             [("DOG PERSON", "anton", ORANGE, ink), ("people are optional", "pacifico", TEAL)], 2900)


@design("certified-happy-camper")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sunset(img, CX, 1700, 1300, [MUSTARD, ORANGE, RUST, PLUM])
    tent(d, CX, 2100, 0.9, ink)
    stack(d, [("CERTIFIED", "bebas", ink), ("HAPPY CAMPER", "anton", TEAL, ink)], CX, 3200, 3900, 30)


@design("campfires-and-smores")
def _(img, ink):
    d = ImageDraw.Draw(img)
    campfire(d, CX, 1800, 1.2, ink)
    for x, y in [(1100, 900), (3400, 1000), (3700, 1900)]:
        star(d, x, y, 120, MUSTARD)
    stack(d, [("CAMPFIRES", "anton", ORANGE, ink), ("& S'MORES", "anton", ink)], CX, 2700, 3900, 20)


@design("hooked-on-fishing")
def _(img, ink):
    d = ImageDraw.Draw(img)
    hook(d, CX + 1300, 1500, 1.0, ink)
    fish(d, CX - 300, 1700, 1.15, ink)
    wave_band(d, 2450, 60, 900, 80, SKY, 600, 3900)
    stack(d, [("HOOKED", "anton", TEAL, ink), ("ON FISHING", "bebas", ink)], CX, 2800, 3900, 20)


@design("lake-days-badge")
def _(img, ink):
    d = ImageDraw.Draw(img)
    cx, cy, r = CX, 2600, 1700
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([0, 0, W, 9000], fill=PINK)
    sunset(layer, cx, cy - 200, 800, [MUSTARD, ORANGE, RUST], gaps=4)
    for k in range(5):
        pine(ld, cx - 1500 + k * 280, cy + 200 - (k % 2) * 150, 0.45, TEAL, NAVY)
        pine(ld, cx + 1500 - k * 280, cy + 200 - (k % 2) * 150, 0.45, TEAL, NAVY)
    ld.rectangle([0, cy + 600, W, 9000], fill=SKY)
    for i in range(4):
        ld.line([(cx - 800 + i * 150, cy + 800 + i * 220), (cx + 800 - i * 150, cy + 800 + i * 220)], fill=CREAM, width=40)
    img.alpha_composite(Image.composite(layer, Image.new("RGBA", img.size, (0, 0, 0, 0)), mask))
    ring(d, cx, cy, r, 90, ink)
    arc_text(img, "LAKE DAYS ARE THE BEST DAYS", cx, cy, r + 300, F("bebas", 360), ink, spacing=1.12)


@design("take-a-hike")
def _(img, ink):
    d = ImageDraw.Draw(img)
    mountains(d, 600, 900, 3300, 1500, [TEAL, SAGE], snow=CREAM)
    sun(d, 3300, 1000, 0.35)
    f = fit("shrikhand", "Take a Hike", 3900)
    shadow_text(d, CX, 2650, "Take a Hike", f, ORANGE, ink)
    f2 = fit("bebas", "IT'S GOOD FOR YOU", 2600)
    text_c(d, CX, 3650, "IT'S GOOD FOR YOU", f2, ink)


@design("stay-sharp-cactus")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sunset(img, CX, 1800, 1300, [PINK, ORANGE, RUST], gaps=4)
    cactus(d, CX, 1900, 0.95, ink)
    stack(d, [("STAY", "anton", ink), ("SHARP", "anton", GREEN, ink)], CX, 3400, 3200, 10)


@design("fungi-to-be-with")
def _(img, ink):
    d = ImageDraw.Draw(img)
    mushroom(d, CX - 450, 1900, 1.0, ink)
    mushroom(d, CX + 900, 2200, 0.6, ink, cap=MUSTARD)
    for x, y in [(900, 1000), (3700, 1100)]:
        star(d, x, y, 120, SAGE, points=4, inner=0.35)
    script_bold(img, ink, "I'm a", "FUNGI TO BE WITH", RUST, y=2900, under=False, script_w=1300)


@design("professional-stargazer")
def _(img, ink):
    d = ImageDraw.Draw(img)
    moon(img, CX - 300, 1700, 1.2, MUSTARD)
    for x, y, r in [(3100, 1000, 170), (3500, 1700, 110), (2900, 2200, 90), (1000, 2500, 80), (3800, 2600, 130)]:
        star(d, x, y, r, CREAM if ink == CREAM else SKY)
    stack(d, [("PROFESSIONAL", "bebas", ink), ("STARGAZER", "anton", PLUM, ink)], CX, 3000, 3900, 20)


@design("pizza-is-my-love-language")
def _(img, ink):
    icon_top(img, ink, lambda d: pizza(d, CX, 1600, 1.2, ink),
             [("PIZZA IS MY", "bebas", ink), ("LOVE LANGUAGE", "anton", RUST, ink)], 2900)


@design("donut-worry-be-happy")
def _(img, ink):
    d = ImageDraw.Draw(img)
    donut(d, CX, 1600, 1.15, ink)
    donut_hole(img, CX, 1600, 1.15)
    d = ImageDraw.Draw(img)
    f = fit("pacifico", "Donut worry", 3600)
    y = text_c(d, CX, 2700, "Donut worry", f, ink)
    stack(d, [("BE HAPPY", "anton", PINK, ink)], CX, y + 40, 3400)


@design("holy-guacamole")
def _(img, ink):
    d = ImageDraw.Draw(img)
    avocado(d, CX, 1700, 1.15, ink)
    f = fit("shrikhand", "Holy", 2000)
    y = text_c(d, CX, 2900, "Holy", f, ink)
    stack(d, [("GUACAMOLE", "anton", GREEN, ink)], CX, y + 40, 3900)


@design("tea-time-any-time")
def _(img, ink):
    d = ImageDraw.Draw(img)
    teacup(d, CX, 1600, 1.3, ink)
    stack(d, [("TEA TIME", "anton", TEAL, ink), ("IS ANY TIME", "bebas", ink)], CX, 3000, 3900, 20)


@design("sip-happens")
def _(img, ink):
    d = ImageDraw.Draw(img)
    wine_glass(d, CX, 1700, 1.1, ink)
    for x, y in [(1200, 900), (3300, 1100)]:
        star(d, x, y, 130, MUSTARD, points=4, inner=0.3)
    f = fit("shrikhand", "Sip Happens", 3900)
    shadow_text(d, CX, 2950, "Sip Happens", f, RUST, ink)


@design("espresso-yourself")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sunset(img, CX, 1600, 1100, [PINK, ORANGE, RUST, PLUM], gaps=4)
    mug(d, CX, 1800, 0.95, CREAM, ink)
    f = fit("pacifico", "Espresso", 3800)
    y = text_c(d, CX, 2900, "Espresso", f, ORANGE)
    stack(d, [("YOURSELF", "anton", ink)], CX, y + 30, 3600)


@design("like-it-spicy")
def _(img, ink):
    d = ImageDraw.Draw(img)
    chili(d, CX + 150, 1600, 1.3, ink)
    stack(d, [("I LIKE IT", "bebas", ink), ("SPICY", "anton", RUST, ink)], CX, 2700, 3600, 10)
    for i in range(3):
        x = 3600 + i * 0
        d.arc([3500 - i * 150, 700 + i * 40, 3800 - i * 150, 1100 + i * 40], 200, 340, fill=ORANGE, width=50)


@design("teach-nap-repeat")
def _(img, ink):
    d = ImageDraw.Draw(img)
    apple(d, CX, 1500, 1.25, ink)
    y = 2700
    for word, c in [("TEACH.", ORANGE), ("NAP.", TEAL), ("REPEAT.", MUSTARD)]:
        y = stack(d, [(word, "anton", c, ink)], CX, y, 2900 if word != "NAP." else 1900, 10)


@design("caffeine-and-compassion")
def _(img, ink):
    d = ImageDraw.Draw(img)
    heart(d, CX, 1600, 2.0, PINK, ink)
    heartbeat(d, CX, 1600, 1.0, ink, color=ink)
    stack(d, [("RUNNING ON", "bebas", ink), ("CAFFEINE", "anton", TEAL, ink), ("& COMPASSION", "anton", RUST, ink)], CX, 2900, 3900, 20)


@design("it-works-on-my-machine")
def _(img, ink):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 600, 800, 3900, 2600
    d.rounded_rectangle([x0, y0, x1, y1], radius=80, fill=NAVY, outline=ink, width=60)
    for i, c in enumerate([RUST, MUSTARD, SAGE]):
        d.ellipse([x0 + 150 + i * 170, y0 + 120, x0 + 270 + i * 170, y0 + 240], fill=c)
    f = F("mono", 190)
    lines = [("$ deploy --prod", SKY), ("tests: 3 failed", RUST), ("> but it works", CREAM), ("  on my machine", MUSTARD)]
    for i, (t, c) in enumerate(lines):
        d.text((x0 + 180, y0 + 420 + i * 320), t, font=f, fill=c)
    stack(d, [("IT WORKS ON", "anton", ink), ("MY MACHINE", "anton", TEAL, ink)], CX, 2900, 3900, 20)


@design("respawning-soon")
def _(img, ink):
    d = ImageDraw.Draw(img)
    controller(d, CX, 1600, 1.4, ink)
    stack(d, [("RESPAWNING", "anton", PLUM, ink), ("SOON", "bungee", ink)], CX, 2700, 3900, 30)
    progress(d, CX, 4700, 0.8, ink, 0.65)


@design("my-commute-is-twelve-steps")
def _(img, ink):
    d = ImageDraw.Draw(img)
    for i in range(6):
        d.rectangle([800 + i * 480, 2300 - i * 260, 1280 + i * 480, 2400], fill=[MUSTARD, ORANGE, RUST, TEAL, SAGE, SKY][i])
    d.rectangle([800, 2300, 3680, 2400], fill=ink)
    mug(d, 3500, 1050, 0.55, CREAM, ink)
    stack(d, [("MY COMMUTE IS", "bebas", ink), ("12 STEPS", "anton", ORANGE, ink)], CX, 2700, 3900, 30)
    f = fit("pacifico", "and a coffee break", 2600)
    text_c(d, CX, 4700, "and a coffee break", f, TEAL)


@design("every-day-is-saturday-retired")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sun(d, CX, 1500, 1.1, MUSTARD)
    stack(d, [("OFFICIALLY RETIRED", "bebas", ink), ("EVERY DAY IS", "anton", TEAL, ink), ("SATURDAY", "anton", ORANGE, ink)], CX, 2900, 3900, 20)


@design("messy-artist-club")
def _(img, ink):
    d = ImageDraw.Draw(img)
    palette(d, CX, 2500, 1.25, ink)
    palette_hole(img, CX, 2500, 1.25)
    arc_text(img, "MESSY ARTIST CLUB", CX, 2500, 1800, F("anton", 420), ink, spacing=1.1)
    arc_text(img, "PAINT FIRST, CLEAN LATER", CX, 2500, 1700, F("bebas", 340), ink, spacing=1.1, bottom=True)


@design("just-one-more-row")
def _(img, ink):
    d = ImageDraw.Draw(img)
    yarn(img, CX, 1800, 1.1, ink)
    d = ImageDraw.Draw(img)
    stack(d, [("JUST ONE", "bebas", ink), ("MORE ROW", "anton", PINK, ink)], CX, 3200, 3700, 20)


@design("analog-soul-vinyl")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sunset(img, CX + 700, 1600, 1000, [MUSTARD, ORANGE, RUST], gaps=4)
    vinyl(d, CX - 450, 1700, 1.05, ink)
    f = fit("pacifico", "analog soul", 3600)
    y = text_c(d, CX, 2950, "analog soul", f, ORANGE)
    f2 = fit("bebas", "VINYL ALWAYS SOUNDS BETTER", 3400)
    text_c(d, CX, y + 80, "VINYL ALWAYS SOUNDS BETTER", f2, ink)


@design("talk-to-your-plants")
def _(img, ink):
    d = ImageDraw.Draw(img)
    for i in range(5):
        a = -90 + (i - 2) * 30
        r = math.radians(a)
        leaf(d, CX + 700 * math.cos(r), 1500 + 700 * math.sin(r), 1.0, a, [SAGE, GREEN][i % 2], ink)
    d.polygon([(CX - 650, 1850), (CX + 650, 1850), (CX + 480, 2700), (CX - 480, 2700)], fill=RUST, outline=ink, width=50)
    d.rectangle([CX - 720, 1780, CX + 720, 2000], fill=ORANGE, outline=ink, width=50)
    for sx in (-1, 1):
        d.ellipse([CX + sx * 220 - 50, 2200, CX + sx * 220 + 50, 2300], fill=ink)
    d.arc([CX - 150, 2250, CX + 150, 2450], 20, 160, fill=ink, width=40)
    stack(d, [("TALK TO", "bebas", ink), ("YOUR PLANTS", "anton", GREEN, ink)], CX, 3000, 3900, 20)
    f = fit("pacifico", "they're good listeners", 3000)
    text_c(d, CX, 4900, "they're good listeners", f, TEAL)


@design("lift-heavy-nap-often")
def _(img, ink):
    d = ImageDraw.Draw(img)
    dumbbell(d, CX, 1500, 1.6, ink)
    for i, z in enumerate("zzz"):
        text_c(d, 3700 + i * 180, 700 - i * 200, "Z", F("anton", 220 + i * 80), SKY)
    stack(d, [("LIFT HEAVY", "anton", ORANGE, ink), ("NAP OFTEN", "anton", ink)], CX, 2600, 3900, 30)


@design("namaste-in-bed")
def _(img, ink):
    d = ImageDraw.Draw(img)
    moon(img, CX - 600, 1500, 0.9, MUSTARD)
    cloud(d, CX + 400, 2000, 1.4, CREAM, ink)
    for x, y in [(3500, 900), (1100, 2300), (3900, 1500)]:
        star(d, x, y, 120, MUSTARD)
    f = fit("pacifico", "Namaste", 3700)
    y = text_c(d, CX, 2900, "Namaste", f, PLUM)
    stack(d, [("IN BED", "anton", ink)], CX, y + 30, 2600)


@design("slow-runners-club")
def _(img, ink):
    def icon(d):
        # snail-paced shoe: simple sneaker
        cx, cy = CX, 2600
        d.polygon([(cx - 800, cy + 250), (cx - 750, cy - 350), (cx - 250, cy - 400), (cx + 150, cy - 50), (cx + 800, cy + 50), (cx + 850, cy + 250)], fill=ORANGE, outline=ink, width=45)
        d.rounded_rectangle([cx - 850, cy + 200, cx + 900, cy + 380], radius=80, fill=CREAM, outline=ink, width=45)
        for k in range(3):
            d.line([(cx - 450 + k * 160, cy - 300 + k * 60), (cx - 250 + k * 160, cy - 200 + k * 60)], fill=CREAM, width=40)
    badge(img, ink, "SLOW RUNNERS CLUB", "STILL LAPPING THE COUCH", MUSTARD, icon, fsize=330)


@design("pedal-power")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sunset(img, CX, 1500, 1200, [MUSTARD, ORANGE, RUST], gaps=4)
    bicycle(d, CX, 1600, 1.15, ink)
    stack(d, [("PEDAL", "anton", TEAL, ink), ("POWER", "anton", ink)], CX, 2700, 3200, 10)


@design("be-kind-to-your-mind")
def _(img, ink):
    d = ImageDraw.Draw(img)
    for i, c in enumerate([PINK, ORANGE, MUSTARD]):
        heart(d, CX + (i - 1) * 900, 1500 - (300 if i == 1 else 0), 1.0 if i != 1 else 1.4, c, ink)
    f = fit("pacifico", "be kind", 3500)
    y = text_c(d, CX, 2400, "be kind", f, TEAL)
    stack(d, [("TO YOUR MIND", "anton", ink)], CX, y + 50, 3800)


@design("one-day-at-a-time")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sun(d, CX, 2200, 1.0, MUSTARD)
    d.rectangle([0, 2200, W, 4000], fill=(0, 0, 0, 0))
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rectangle([0, 2200, W, 9000], fill=255)
    img.paste((0, 0, 0, 0), (0, 0), m)
    d = ImageDraw.Draw(img)
    bars(d, 2250, 600, 3900, (ORANGE, RUST), 90, 170)
    stack(d, [("ONE DAY", "anton", ink), ("AT A TIME", "anton", ORANGE, ink)], CX, 2850, 3900, 20)


@design("small-steps-still-count")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sprout(d, CX, 1700, 1.3, ink)
    stack(d, [("SMALL STEPS", "anton", GREEN, ink), ("STILL COUNT", "anton", ink)], CX, 3000, 3900, 30)


@design("bloom-where-you-are-planted")
def _(img, ink):
    d = ImageDraw.Draw(img)
    for x, y, s, p in [(CX, 1500, 1.1, CREAM), (CX - 1300, 2000, 0.6, PINK), (CX + 1300, 2000, 0.6, MUSTARD)]:
        d.line([(x, y), (x, 2700)], fill=GREEN, width=int(60 * s))
        daisy(d, x, y, s, ink, petal=p, center=ORANGE if p == MUSTARD else MUSTARD)
    f = fit("pacifico", "Bloom where", 3600)
    y = text_c(d, CX, 2850, "Bloom where", f, ink)
    stack(d, [("YOU ARE PLANTED", "anton", PINK, ink)], CX, y + 30, 3900)


@design("introvert-battery-low")
def _(img, ink):
    d = ImageDraw.Draw(img)
    battery(d, CX, 1600, 1.4, ink)
    stack(d, [("SOCIAL BATTERY", "anton", ink), ("1% REMAINING", "anton", ORANGE, ink)], CX, 2600, 3900, 30)
    f = fit("pacifico", "please recharge me at home", 3200)
    text_c(d, CX, 4700, "please recharge me at home", f, TEAL)


@design("overstimulated-overcaffeinated")
def _(img, ink):
    d = ImageDraw.Draw(img)
    mug(d, CX, 1600, 1.05, PINK, ink)
    for i in range(8):
        a = math.radians(200 + i * 20)
        d.line([(CX + 1050 * math.cos(a), 1700 + 1050 * math.sin(a)), (CX + 1350 * math.cos(a), 1700 + 1350 * math.sin(a))], fill=MUSTARD, width=60)
    stack(d, [("OVERSTIMULATED", "anton", PLUM, ink), ("& OVERCAFFEINATED", "anton", ink)], CX, 2800, 3900, 30)


@design("low-energy-high-hopes")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sun(d, CX + 600, 1300, 0.85, MUSTARD)
    cloud(d, CX - 250, 1800, 1.3, CREAM, ink)
    stack(d, [("LOW ENERGY", "anton", ink), ("HIGH HOPES", "anton", MUSTARD, ink)], CX, 2700, 3900, 30)


@design("do-more-of-what-makes-you-happy")
def _(img, ink):
    d = ImageDraw.Draw(img)
    rainbow(d, CX, 2300, 1.15, ink)
    clear_semi(img, CX, 2300, (1300 - 5 * 180) * 1.15)
    d = ImageDraw.Draw(img)
    cloud(d, CX - 1200, 2250, 0.55, CREAM, ink)
    cloud(d, CX + 1250, 2250, 0.55, CREAM, ink)
    stack(d, [("DO MORE OF", "bebas", ink), ("WHAT MAKES", "anton", ORANGE, ink), ("YOU HAPPY", "anton", TEAL, ink)], CX, 2750, 3900, 20)


@design("dad-joke-loading")
def _(img, ink):
    d = ImageDraw.Draw(img)
    stack(d, [("DAD JOKE", "anton", ink), ("LOADING", "anton", ORANGE, ink)], CX, 900, 3900, 20)
    progress(d, CX, 3500, 1.1, ink, 0.72)
    f = fit("pacifico", "please wait", 2400)
    text_c(d, CX, 4000, "please wait", f, TEAL)


@design("mama-needs-coffee")
def _(img, ink):
    d = ImageDraw.Draw(img)
    mug(d, CX, 1600, 1.05, CREAM, ink)
    heart(d, CX - 40, 1600, 0.6, PINK)
    f = fit("pacifico", "Mama", 2800)
    y = text_c(d, CX, 2700, "Mama", f, PINK)
    stack(d, [("NEEDS COFFEE", "anton", ink)], CX, y + 40, 3900)


@design("cool-aunt-club")
def _(img, ink):
    def icon(d):
        cx, cy = CX, 2600
        for sx in (-1, 1):
            d.rounded_rectangle([cx + sx * 380 - 330, cy - 260, cx + sx * 380 + 330, cy + 220], radius=120, fill=NAVY, outline=ink, width=40)
        d.line([(cx - 60, cy - 130), (cx + 60, cy - 130)], fill=ink, width=50)
        for sx in (-1, 1):
            d.line([(cx + sx * 300 - 150, cy - 140), (cx + sx * 300, cy - 40)], fill=CREAM, width=40)
    badge(img, ink, "COOL AUNT CLUB", "MEMBER SINCE FOREVER", PINK, icon, fsize=340)


@design("home-is-where-the-snacks-are")
def _(img, ink):
    icon_top(img, ink, lambda d: house_door(d, CX, 1700, 1.2, ink),
             [("HOME IS WHERE", "bebas", ink), ("THE SNACKS ARE", "anton", ORANGE, ink)], 2900)


@design("pumpkin-spice-everything-nice")
def _(img, ink):
    d = ImageDraw.Draw(img)
    pumpkin(d, CX, 1700, 1.25, ink)
    for x, y in [(900, 1000), (3600, 1200), (3800, 2300)]:
        leaf(d, x, y, 0.5, 30, RUST, ink)
    stack(d, [("PUMPKIN SPICE", "anton", ORANGE, ink), ("& EVERYTHING NICE", "bebas", ink)], CX, 2850, 3900, 30)


@design("spooky-season")
def _(img, ink):
    d = ImageDraw.Draw(img)
    ghost(d, CX, 1600, 1.1, ink)
    for x, y in [(1000, 900), (3500, 1000), (3800, 2000)]:
        star(d, x, y, 110, MUSTARD)
    f = fit("shrikhand", "Spooky", 3600)
    y = shadow_text(d, CX, 2700, "Spooky", f, ORANGE, ink)
    stack(d, [("SEASON", "anton", ink)], CX, y + 20, 2600)


@design("snow-day-enthusiast")
def _(img, ink):
    d = ImageDraw.Draw(img)
    snowflake(d, CX, 1600, 1.1, SKY)
    for x, y, s in [(1000, 1000, 0.25), (3600, 1300, 0.3), (3700, 2400, 0.2)]:
        snowflake(d, x, y, s, SKY)
    stack(d, [("SNOW DAY", "anton", SKY, ink), ("ENTHUSIAST", "bebas", ink)], CX, 2900, 3900, 30)


@design("merry-and-bright-trees")
def _(img, ink):
    d = ImageDraw.Draw(img)
    for x, s, c in [(CX - 1100, 0.7, SAGE), (CX, 1.0, GREEN), (CX + 1100, 0.7, TEAL)]:
        pine(d, x, 1700 + (1 - s) * 900, s, c, ink)
    f = fit("pacifico", "Merry & Bright", 3800)
    shadow_text(d, CX, 2950, "Merry & Bright", f, RUST, ink, depth=30)


@design("summer-vibes-only")
def _(img, ink):
    d = ImageDraw.Draw(img)
    sunset(img, CX, 1800, 1400, [MUSTARD, ORANGE, PINK, PLUM])
    palm(d, CX - 700, 1800, 1.0, ink)
    stack(d, [("SUMMER", "anton", ORANGE, ink), ("VIBES ONLY", "bebas", ink)], CX, 3300, 3900, 30)


@design("plot-twist-i-stayed-in")
def _(img, ink):
    d = ImageDraw.Draw(img)
    for i, c in enumerate([TEAL, MUSTARD, PINK]):
        book(d, 1300 + i * 60, 1300 + i * 380, 1900 - i * 120, 330, c, ink)
    teacup(d, 3500, 1900, 0.55, ink, body=CREAM)
    stack(d, [("PLOT TWIST:", "anton", ORANGE, ink), ("I STAYED IN", "anton", ink)], CX, 2700, 3900, 30)


if __name__ == "__main__":
    build.main()
