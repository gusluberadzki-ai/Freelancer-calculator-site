"""Original seamless patterns (SVG tiles) and grainy gradient backgrounds.

patterns/: tile SVG, 3600x3600 JPG swatch, EPS swatch per pattern
backgrounds/: 6000x4000 JPG abstract gradient backgrounds (24 MP)
Run: python3 stock-assets/patterns.py OUT_DIR
"""
import math
import os
import random
import subprocess
import sys

import cairosvg
import numpy as np
from PIL import Image, ImageFilter

OUT = sys.argv[1]
T = 200  # tile size in svg units

PALETTES = {
    "retro": ["#F6EAD6", "#EAA53D", "#E2603A", "#2A7F7A", "#1F2A44"],
    "sage": ["#EEF0E5", "#86A678", "#2A7F7A", "#D9B98C", "#3E4A3D"],
    "blush": ["#FBEDEA", "#E58FA0", "#F2C6B4", "#B5442E", "#6E3F68"],
    "ocean": ["#EAF3F6", "#78B0CE", "#2A7F7A", "#1F2A44", "#F6EAD6"],
}


def rnd(seed):
    r = random.Random(seed)
    return r


def p_terrazzo(c, r):
    out = []
    for i in range(36):
        x, y = r.uniform(0, T), r.uniform(0, T)
        col = c[1 + i % 4]
        pts = []
        n = r.randint(4, 7)
        s = r.uniform(5, 14)
        for k in range(n):
            a = 2 * math.pi * k / n + r.uniform(-.3, .3)
            pts.append((s * r.uniform(.6, 1.2) * math.cos(a), s * r.uniform(.6, 1.2) * math.sin(a)))
        for dx in (-T, 0, T):
            for dy in (-T, 0, T):
                pp = " ".join(f"{x + dx + px:.1f},{y + dy + py:.1f}" for px, py in pts)
                out.append(f'<polygon points="{pp}" fill="{col}"/>')
    return out


def p_waves(c, r):
    out = []
    for i in range(5):
        y = i * T / 5 + 20
        d = f"M-10 {y} " + " ".join(f"Q {x + 25} {y - 14} {x + 50} {y} T {x + 100} {y}" for x in range(-10, T + 10, 100))
        out.append(f'<path d="{d}" fill="none" stroke="{c[1 + i % 4]}" stroke-width="9" stroke-linecap="round"/>')
    return out


def p_arches(c, r):
    out = []
    for gx in range(2):
        for gy in range(2):
            cx, cy = gx * 100 + 50, gy * 100 + 85
            for k, col in enumerate(c[1:4]):
                rad = 40 - k * 12
                out.append(f'<path d="M{cx - rad} {cy} A{rad} {rad} 0 0 1 {cx + rad} {cy}" fill="none" stroke="{col}" stroke-width="9"/>')
    return out


def p_dots(c, r):
    out = []
    for gx in range(5):
        for gy in range(5):
            off = 20 if gy % 2 else 0
            for dx in (-T, 0, T):
                out.append(f'<circle cx="{gx * 40 + off + 20 + dx}" cy="{gy * 40 + 20}" r="9" fill="{c[1 + (gx + gy) % 4]}"/>')
    return out



def p_leaves(c, r):
    out = []
    for gx in range(2):
        for gy in range(2):
            cx, cy = gx * 100 + 50 + (gy % 2) * 50, gy * 100 + 50
            ang = 35 if (gx + gy) % 2 else -35
            col = c[1 + (gx * 2 + gy) % 3]
            for dx in (-T, 0, T):
                out.append(f'<g transform="translate({cx + dx},{cy}) rotate({ang})"><path d="M0 -38 C 26 -18 26 18 0 38 C -26 18 -26 -18 0 -38z" fill="{col}"/>'
                           f'<path d="M0 -34 V 34" stroke="{c[0]}" stroke-width="3"/></g>')
    return out



def p_checker_wave(c, r):
    out = []
    n = 4
    s = T / n
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                out.append(f'<rect x="{i * s + 4}" y="{j * s + 4}" width="{s - 8}" height="{s - 8}" rx="12" fill="{c[2 if (i // 2 + j // 2) % 2 else 1]}"/>')
    return out



def p_stars(c, r):
    out = []
    for i in range(14):
        x, y = r.uniform(0, T), r.uniform(0, T)
        s = r.uniform(5, 11)
        pts = []
        for k in range(10):
            rr = s if k % 2 == 0 else s * .45
            a = math.radians(-90 + k * 36)
            pts.append((rr * math.cos(a), rr * math.sin(a)))
        for dx in (-T, 0, T):
            for dy in (-T, 0, T):
                out.append('<polygon points="' + " ".join(f"{x + dx + px:.1f},{y + dy + py:.1f}" for px, py in pts) + f'" fill="{c[1 + i % 3]}"/>')
    return out


def p_scales(c, r):
    out = []
    for i in range(4):
        for j in range(4):
            x, y = i * 50 + 25, j * 50 + 25
            col = c[1 + (i + 2 * j) % 4]
            out.append(f'<path d="M{x - 12} {y}h24M{x} {y - 12}v24" stroke="{col}" stroke-width="7" stroke-linecap="round"/>')
    return out



def p_squiggles(c, r):
    out = []
    for i in range(10):
        x, y = r.uniform(0, T), r.uniform(0, T)
        ang = r.uniform(0, 180)
        col = c[1 + i % 4]
        for dx in (-T, 0, T):
            for dy in (-T, 0, T):
                out.append(f'<path transform="translate({x + dx:.1f},{y + dy:.1f}) rotate({ang:.0f})" d="M-24 0 q6 -10 12 0 t12 0 t12 0 t12 0" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>')
    return out


def p_stripes(c, r):
    out = []
    for i in range(8):
        out.append(f'<rect x="0" y="{i * 25}" width="{T}" height="17" fill="{c[1 + i % 4]}"/>')
    return out



def p_rainbows(c, r):
    out = []
    for gx in range(2):
        for gy in range(2):
            cx, cy = gx * 100 + 50 + (gy % 2) * 50, gy * 100 + 62
            for k, col in enumerate([c[3], c[2], c[1]]):
                rad = 34 - k * 10
                for dx in (-T, 0, T):
                    x = cx + dx
                    out.append(f'<path d="M{x - rad} {cy} A{rad} {rad} 0 0 1 {x + rad} {cy}" fill="none" stroke="{col}" stroke-width="8" stroke-linecap="round"/>')
    return out



def p_triangles(c, r):
    out = []
    s = 50
    for i in range(4):
        for j in range(4):
            x, y = i * s, j * s
            col = c[1 + (i + j * 2) % 4]
            if (i + j) % 2:
                out.append(f'<polygon points="{x},{y} {x + s},{y} {x},{y + s}" fill="{col}"/>')
            else:
                out.append(f'<polygon points="{x + s},{y} {x + s},{y + s} {x},{y + s}" fill="{col}"/>')
    return out



PATTERNS = [
    ("terrazzo", p_terrazzo, "retro"), ("retro-waves", p_waves, "retro"), ("mid-century-arches", p_arches, "sage"),
    ("polka-dots", p_dots, "blush"), ("leafy", p_leaves, "sage"), ("soft-checker", p_checker_wave, "blush"),
    ("starry", p_stars, "ocean"), ("plus-grid", p_scales, "ocean"), ("memphis-squiggles", p_squiggles, "retro"),
    ("bold-stripes", p_stripes, "blush"), ("little-rainbows", p_rainbows, "retro"), ("geo-triangles", p_triangles, "ocean"),
]


def tile_svg(fn, pal, seed):
    c = PALETTES[pal]
    body = "".join(fn(c, rnd(seed)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{T}" height="{T}" viewBox="0 0 {T} {T}">'
            f'<defs><clipPath id="c"><rect width="{T}" height="{T}"/></clipPath></defs>'
            f'<rect width="{T}" height="{T}" fill="{c[0]}"/><g clip-path="url(#c)">{body}</g></svg>')


def swatch_svg(tile, reps):
    inner = tile.split(">", 1)[1].rsplit("</svg>", 1)[0]
    size = T * reps
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
            f'<defs><pattern id="p" width="{T}" height="{T}" patternUnits="userSpaceOnUse"><svg width="{T}" height="{T}">{inner}</svg></pattern></defs>'
            f'<rect width="{size}" height="{size}" fill="url(#p)"/></svg>')


def build_patterns():
    d = os.path.join(OUT, "patterns")
    for sub in ("svg-tile", "jpg-3600", "eps", "png-tile-1000"):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    for i, (name, fn, pal) in enumerate(PATTERNS):
        tile = tile_svg(fn, pal, i + 7)
        open(os.path.join(d, "svg-tile", f"{name}.svg"), "w").write(tile)
        cairosvg.svg2png(bytestring=tile.encode(), write_to=os.path.join(d, "png-tile-1000", f"{name}.png"), output_width=1000, output_height=1000)
        # tile manually for the swatch (robust, no reliance on <pattern> support)
        t = Image.open(os.path.join(d, "png-tile-1000", f"{name}.png")).convert("RGB").resize((600, 600), Image.LANCZOS)
        sw = Image.new("RGB", (3600, 3600))
        for x in range(6):
            for y in range(6):
                sw.paste(t, (x * 600, y * 600))
        sw.save(os.path.join(d, "jpg-3600", f"{name}.jpg"), quality=92)
        # vector swatch: 3x3 copies of the tile in one SVG -> PDF -> EPS
        inner = tile.split(">", 1)[1].rsplit("</svg>", 1)[0]
        groups = "".join(f'<g transform="translate({x * T},{y * T})">{inner.replace("id=\"c\"", f"id=\"c{x}{y}\"").replace("url(#c)", f"url(#c{x}{y})")}</g>' for x in range(3) for y in range(3))
        big = f'<svg xmlns="http://www.w3.org/2000/svg" width="{3 * T}" height="{3 * T}" viewBox="0 0 {3 * T} {3 * T}">{groups}</svg>'
        pdf = os.path.join(d, "eps", f"{name}.pdf")
        cairosvg.svg2pdf(bytestring=big.encode(), write_to=pdf)
        subprocess.run(["pdftocairo", "-eps", pdf, os.path.join(d, "eps", f"{name}.eps")], check=True)
        os.remove(pdf)
        print("pattern", name)


BG_SETS = [
    ("sunset-glow", ["#F6EAD6", "#EAA53D", "#E2603A", "#E58FA0", "#6E3F68"]),
    ("ocean-mist", ["#EAF3F6", "#78B0CE", "#2A7F7A", "#1F2A44", "#B9E0D8"]),
    ("sage-morning", ["#EEF0E5", "#86A678", "#D9B98C", "#2A7F7A", "#F6EAD6"]),
    ("berry-dusk", ["#2B1B3D", "#6E3F68", "#E58FA0", "#B5442E", "#1F2A44"]),
    ("peach-cream", ["#FBEDEA", "#F2C6B4", "#EAA53D", "#E58FA0", "#FFF7EC"]),
    ("midnight-aurora", ["#0F1626", "#1F2A44", "#2A7F7A", "#86A678", "#6E3F68"]),
    ("lavender-haze", ["#F1EDF7", "#B9A7D9", "#E58FA0", "#78B0CE", "#FFFFFF"]),
    ("citrus-pop", ["#FFF5D6", "#EAA53D", "#F3D34A", "#E2603A", "#86A678"]),
    ("deep-forest", ["#14231E", "#2A7F7A", "#3E4A3D", "#86A678", "#D9B98C"]),
    ("cotton-candy", ["#FDF0F5", "#E58FA0", "#9CC9E8", "#F7D6E6", "#B9A7D9"]),
    ("desert-dunes", ["#F6EAD6", "#D9B98C", "#B5442E", "#EAA53D", "#8A5A44"]),
    ("electric-blue", ["#0B1430", "#2D5BFF", "#78B0CE", "#B9A7D9", "#1F2A44"]),
]


def hex2rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float32)


def build_backgrounds():
    d = os.path.join(OUT, "backgrounds")
    os.makedirs(d, exist_ok=True)
    Wb, Hb = 1500, 1000  # compute small, upscale (gradients are smooth), then add full-res grain
    yy, xx = np.mgrid[0:Hb, 0:Wb].astype(np.float32)
    for k, (name, cols) in enumerate(BG_SETS):
        r = np.random.default_rng(k + 11)
        base = hex2rgb(cols[0])
        img = np.ones((Hb, Wb, 3), np.float32) * base
        for i in range(7):
            col = hex2rgb(cols[1 + i % 4])
            cx, cy = r.uniform(-0.1, 1.1) * Wb, r.uniform(-0.1, 1.1) * Hb
            sx, sy = r.uniform(0.25, 0.55) * Wb, r.uniform(0.25, 0.55) * Hb
            a = r.uniform(0, math.pi)
            dx, dy = xx - cx, yy - cy
            u = (dx * math.cos(a) + dy * math.sin(a)) / sx
            v = (-dx * math.sin(a) + dy * math.cos(a)) / sy
            w = np.exp(-(u * u + v * v) * 1.6)[..., None] * r.uniform(0.6, 0.95)
            img = img * (1 - w) + col * w
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))
        im = im.resize((6000, 4000), Image.BICUBIC)
        arr = np.asarray(im).astype(np.int16)
        grain = np.random.default_rng(k).normal(0, 7, (4000, 6000, 1)).astype(np.int16)
        arr = np.clip(arr + grain, 0, 255).astype(np.uint8)
        Image.fromarray(arr).save(os.path.join(d, f"{name}.jpg"), quality=90)
        print("bg", name)


if __name__ == "__main__":
    build_patterns()
    build_backgrounds()
