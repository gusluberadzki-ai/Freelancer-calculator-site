"""Make product covers, the Adobe Stock icon sheet, and zip the stock packs.

Run: python3 stock-assets/package.py BUILD_DIR DEST_DIR FONT_DIR
BUILD_DIR holds icons/ and stock/ from icons.py and patterns.py.
"""
import os
import shutil
import subprocess
import sys
import zipfile

import cairosvg
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from icons import ICONS, S  # noqa: E402

B, DEST, FONTS = sys.argv[1], sys.argv[2], sys.argv[3]
NAVY, CREAM, ORANGE, TEAL = (31, 42, 68), (246, 234, 214), (226, 96, 58), (42, 127, 122)

LICENSE = """LICENSE (short version)

You may use these files in unlimited personal and commercial projects:
websites, apps, client work, social media, print, merchandise and products for sale.

You may not resell or give away the files themselves, alone or in a bundle,
or upload them to other stock, icon or template marketplaces.

Credit is appreciated but not required.
"""


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def cover(path, size, title, subtitle, art, bg=CREAM, ink=NAVY):
    w, h = size
    im = Image.new("RGB", size, bg)
    art = art.copy()
    art.thumbnail((int(w * 0.58), int(h * 0.86)))
    im.paste(art, (w - art.width - int(w * 0.04), (h - art.height) // 2), art if art.mode == "RGBA" else None)
    d = ImageDraw.Draw(im)
    x = int(w * 0.05)
    f1 = font("Anton-Regular.ttf", int(h * 0.12))
    y = int(h * 0.2)
    for line in title.split("\n"):
        d.text((x, y), line, font=f1, fill=ink)
        y += int(h * 0.145)
    d.rectangle([x, y + 20, x + int(w * 0.08), y + 34], fill=ORANGE)
    f2 = font("BebasNeue-Regular.ttf", int(h * 0.05))
    y += 70
    for line in subtitle.split("\n"):
        d.text((x, y), line, font=f2, fill=TEAL)
        y += int(h * 0.065)
    im.save(path, quality=92)


def icon_sheet(cols=8, cell=160, color="#1F2A44"):
    names = list(ICONS)
    rows = (len(names) + cols - 1) // cols
    parts = []
    for i, n in enumerate(names):
        x, y = (i % cols) * cell + cell * 0.2, (i // cols) * cell + cell * 0.2
        sc = cell * 0.6 / 24
        parts.append(f'<g transform="translate({x},{y}) scale({sc})" {S.replace("currentColor", color)}>{ICONS[n]}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{cols * cell}" height="{rows * cell}" viewBox="0 0 {cols * cell} {rows * cell}">'
            f'<rect width="100%" height="100%" fill="#FFFFFF"/>{"".join(parts)}</svg>')


def zipdir(src, zpath, extra=None):
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(src):
            for f in sorted(files):
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, os.path.dirname(src)))
        for name, text in (extra or {}).items():
            z.writestr(os.path.join(os.path.basename(src), name), text)


def grid(paths, cols, cell, crop=None, gap=12, bg=(255, 255, 255)):
    rows = (len(paths) + cols - 1) // cols
    cw, ch = cell
    out = Image.new("RGB", (cols * (cw + gap) - gap, rows * (ch + gap) - gap), bg)
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB")
        if crop:
            im = im.crop(crop)
        im = im.resize((cw, ch), Image.LANCZOS)
        out.paste(im, ((i % cols) * (cw + gap), (i // cols) * (ch + gap)))
    return out


def main():
    stock = os.path.join(DEST, "stock")
    os.makedirs(stock, exist_ok=True)
    adobe = os.path.join(stock, "adobe-stock-upload")
    os.makedirs(adobe, exist_ok=True)

    # icon pack
    sheet_svg = icon_sheet()
    icons_dir = os.path.join(B, "icons")
    open(os.path.join(icons_dir, "all-icons-sheet.svg"), "w").write(sheet_svg)
    cairosvg.svg2png(bytestring=sheet_svg.encode(), write_to=os.path.join(B, "sheet.png"), output_width=4800)
    pdf = os.path.join(B, "sheet.pdf")
    cairosvg.svg2pdf(bytestring=sheet_svg.encode(), write_to=pdf)
    subprocess.run(["pdftocairo", "-eps", pdf, os.path.join(adobe, "freelance-remote-work-line-icons-set.eps")], check=True)
    zipdir(icons_dir, os.path.join(stock, "Freelance-Remote-Work-Icons.zip"), {"LICENSE.txt": LICENSE,
           "README.txt": "48 line icons on a 24px grid, 1.75 stroke, round caps.\nsvg/ editable stroke (uses currentColor), png/ 64-256-512 navy, png-white/, png-teal/, eps/ per icon, sprite.svg for websites, all-icons-sheet.svg.\n"})
    sheet = Image.open(os.path.join(B, "sheet.png")).convert("RGB")
    cover(os.path.join(stock, "icons-cover.png"), (1280, 720), "48 FREELANCE &\nREMOTE WORK\nLINE ICONS", "SVG · PNG · EPS · SPRITE\nEDITABLE STROKE", sheet, bg=(255, 255, 255))
    cover(os.path.join(stock, "icons-cover-creative-market.jpg"), (1820, 1214), "48 FREELANCE &\nREMOTE WORK\nLINE ICONS", "SVG · PNG · EPS · SPRITE\nEDITABLE STROKE", sheet, bg=(255, 255, 255))

    # patterns
    pat = os.path.join(B, "stock", "patterns")
    pj = sorted(os.path.join(pat, "jpg-3600", f) for f in os.listdir(os.path.join(pat, "jpg-3600")))
    zipdir(pat, os.path.join(stock, "Retro-Seamless-Patterns.zip"), {"LICENSE.txt": LICENSE,
           "README.txt": "12 seamless patterns.\nsvg-tile/ vector tile (use as a pattern fill or repeat it), png-tile-1000/ raster tile, jpg-3600/ 3600x3600 ready-made swatches, eps/ 3x3 vector swatch.\nIn Canva / Photoshop / Procreate, repeat the tile edge to edge; it has no visible seam.\n"})
    pg = grid(pj, 4, (400, 400), crop=(0, 0, 1200, 1200))
    cover(os.path.join(stock, "patterns-cover.png"), (1280, 720), "12 RETRO\nSEAMLESS\nPATTERNS", "SVG · EPS · PNG TILE · JPG 3600PX\nFOR FABRIC, PACKAGING & WEB", pg)
    cover(os.path.join(stock, "patterns-cover-creative-market.jpg"), (1820, 1214), "12 RETRO\nSEAMLESS\nPATTERNS", "SVG · EPS · PNG TILE · JPG 3600PX\nFOR FABRIC, PACKAGING & WEB", pg)
    for f in os.listdir(os.path.join(pat, "eps")):
        shutil.copy(os.path.join(pat, "eps", f), os.path.join(adobe, "pattern-" + f))

    # backgrounds
    bgd = os.path.join(B, "stock", "backgrounds")
    bj = sorted(os.path.join(bgd, f) for f in os.listdir(bgd))
    zipdir(bgd, os.path.join(stock, "Grainy-Gradient-Backgrounds.zip"), {"LICENSE.txt": LICENSE,
           "README.txt": "12 grainy gradient backgrounds, 6000x4000 px JPG (24 MP).\nGreat for social posts, slides, website heroes, phone wallpapers and print.\n"})
    bgrid = grid(bj, 4, (450, 300))
    cover(os.path.join(stock, "backgrounds-cover.png"), (1280, 720), "12 GRAINY\nGRADIENT\nBACKGROUNDS", "6000 × 4000 PX · 24 MP JPG\nSOCIAL · SLIDES · WEB · PRINT", bgrid)
    cover(os.path.join(stock, "backgrounds-cover-creative-market.jpg"), (1820, 1214), "12 GRAINY\nGRADIENT\nBACKGROUNDS", "6000 × 4000 PX · 24 MP JPG\nSOCIAL · SLIDES · WEB · PRINT", bgrid)
    for p in bj:
        shutil.copy(p, os.path.join(adobe, "background-" + os.path.basename(p)))
    print("done")


if __name__ == "__main__":
    main()
