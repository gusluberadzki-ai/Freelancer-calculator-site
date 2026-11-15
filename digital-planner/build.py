"""Hyperlinked 2027 digital planner for GoodNotes / Notability / any PDF app.
python3 build.py [year] [out.pdf]  -> landscape iPad-ratio PDF with tabs on every page."""
import sys, calendar, datetime as dt
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

YEAR = int(sys.argv[1]) if len(sys.argv) > 1 else 2027
OUT = sys.argv[2] if len(sys.argv) > 2 else f'Digital-Planner-{YEAR}.pdf'
W, H = 1024, 768
INK, MUTED, LINE, ACC, SOFT, BG = (HexColor(x) for x in ('#1d1d1f', '#6b6b6b', '#d9d6cf', '#0b6e4f', '#e3f2ec', '#faf8f4'))
TABW = 64
M = 40
MON = [calendar.month_abbr[i].upper() for i in range(1, 13)]
c = canvas.Canvas(OUT, pagesize=(W, H))
c.setTitle(f'{YEAR} Digital Planner'); c.setAuthor('RateKit')
calendar.setfirstweekday(calendar.MONDAY)
days = [dt.date(YEAR, 1, 1) + dt.timedelta(n) for n in range((dt.date(YEAR + 1, 1, 1) - dt.date(YEAR, 1, 1)).days)]
first_monday = dt.date(YEAR, 1, 1) - dt.timedelta(dt.date(YEAR, 1, 1).weekday())
weeks = []
d = first_monday
while d.year <= YEAR and not (d.year == YEAR + 1):
    weeks.append(d); d += dt.timedelta(7)
    if d > dt.date(YEAR, 12, 31): break

def wk_of(day): return (day - first_monday).days // 7
def link(name, x, y, w, h): c.linkRect('', name, (x, y, x + w, y + h), relative=0, thickness=0)

def frame(name, current=None):
    c.bookmarkPage(name)
    c.setFillColor(BG); c.rect(0, 0, W, H, stroke=0, fill=1)
    # right-hand tabs
    x = W - TABW
    c.setFillColor(HexColor('#f0ede6')); c.rect(x, 0, TABW, H, stroke=0, fill=1)
    tabs = [('YEAR', 'year')] + [(MON[i], f'm{i+1}') for i in range(12)] + [('GOALS', 'goals'), ('HABIT', 'habits'), ('NOTES', 'notes1')]
    th = (H - 20) / len(tabs)
    for i, (lab, dest) in enumerate(tabs):
        y = H - 10 - (i + 1) * th
        if dest == current:
            c.setFillColor(ACC); c.roundRect(x + 6, y + 2, TABW - 10, th - 4, 6, stroke=0, fill=1); c.setFillColor(HexColor('#ffffff'))
        else: c.setFillColor(MUTED)
        c.setFont('Helvetica-Bold', 11); c.drawCentredString(x + TABW / 2, y + th / 2 - 4, lab)
        link(dest, x, y, TABW, th)

def title(t, sub=None, back=None):
    c.setFillColor(INK); c.setFont('Helvetica-Bold', 30); c.drawString(M, H - 64, t)
    if sub: c.setFillColor(MUTED); c.setFont('Helvetica', 13); c.drawString(M, H - 86, sub)
    if back:
        lab, dest = back; c.setFont('Helvetica-Bold', 12); c.setFillColor(ACC)
        tw = c.stringWidth(lab, 'Helvetica-Bold', 12); bx = W - TABW - M - tw
        c.drawString(bx, H - 60, lab); link(dest, bx - 6, H - 68, tw + 12, 24)

def lines(x, y0, y1, w, step=28):
    c.setStrokeColor(LINE); c.setLineWidth(.7); y = y0
    while y > y1: c.line(x, y, x + w, y); y -= step

def dots(x, y0, y1, w, step=24):
    c.setFillColor(LINE); y = y0
    while y > y1:
        xx = x
        while xx < x + w: c.circle(xx, y, .9, stroke=0, fill=1); xx += step
        y -= step

def box(x, y, w, h, label=None):
    c.setStrokeColor(LINE); c.setLineWidth(1); c.setFillColor(HexColor('#ffffff')); c.roundRect(x, y, w, h, 8, stroke=1, fill=1)
    if label: c.setFillColor(ACC); c.setFont('Helvetica-Bold', 11); c.drawString(x + 12, y + h - 20, label.upper())

def mini_month(m, x, y, cw=26, ch=20, big=False):
    c.setFillColor(INK); c.setFont('Helvetica-Bold', 14 if big else 12); c.drawString(x, y, calendar.month_name[m]); link(f'm{m}', x, y - 4, cw * 7, 18)
    c.setFont('Helvetica', 9); c.setFillColor(MUTED)
    for i, dn in enumerate('MTWTFSS'): c.drawCentredString(x + i * cw + cw / 2, y - 18, dn)
    c.setFont('Helvetica', 10)
    for r, wk in enumerate(calendar.monthcalendar(YEAR, m)):
        for i, dd in enumerate(wk):
            if dd:
                cx, cy = x + i * cw + cw / 2, y - 18 - (r + 1) * ch
                c.setFillColor(INK); c.drawCentredString(cx, cy, str(dd)); link(f'd{dt.date(YEAR, m, dd).isoformat()}', cx - cw / 2, cy - 5, cw, ch)

# Cover
c.bookmarkPage('cover'); c.setFillColor(ACC); c.rect(0, 0, W, H, stroke=0, fill=1)
c.setFillColor(HexColor('#ffffff')); c.setFont('Helvetica-Bold', 120); c.drawCentredString(W / 2, H / 2 + 10, str(YEAR))
c.setFont('Helvetica', 28); c.drawCentredString(W / 2, H / 2 - 50, 'Digital Planner')
c.setFont('Helvetica', 14); c.drawCentredString(W / 2, 80, 'Tap anywhere to start  ·  every date, tab and week is a link')
link('year', 0, 0, W, H); c.showPage()

# Year
frame('year', 'year'); title(f'{YEAR} at a glance', 'Tap a month name or any date')
cw, ch = 24, 17; gx = (W - TABW - 2 * M) / 4
for i in range(12):
    mini_month(i + 1, M + (i % 4) * gx, H - 140 - (i // 4) * 200, cw, ch)
c.showPage()

# Goals
frame('goals', 'goals'); title(f'{YEAR} goals', back=('YEAR', 'year'))
bw = (W - TABW - 3 * M) / 2
for i, lab in enumerate(['Career & money', 'Health', 'Relationships', 'Growth & fun']):
    x = M + (i % 2) * (bw + M); y = H - 120 - (i // 2 + 1) * 300 + 20
    box(x, y, bw, 280, lab); lines(x + 12, y + 240, y + 10, bw - 24)
c.showPage()

# Months
for m in range(1, 13):
    frame(f'm{m}', f'm{m}'); title(f'{calendar.month_name[m]} {YEAR}', back=('YEAR', 'year'))
    gw = W - TABW - 2 * M - 220; cols = 7; cwm = gw / cols
    rows = calendar.monthcalendar(YEAR, m); chm = (H - 150 - M) / len(rows)
    c.setFont('Helvetica-Bold', 11); c.setFillColor(MUTED)
    for i, dn in enumerate(['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']): c.drawString(M + i * cwm + 6, H - 118, dn)
    for r, wk in enumerate(rows):
        y = H - 128 - (r + 1) * chm
        mon = next(dt.date(YEAR, m, dd) for dd in wk if dd) ; mon = mon - dt.timedelta(mon.weekday())
        c.setFont('Helvetica-Bold', 9); c.setFillColor(ACC); c.drawRightString(M - 4, y + chm - 14, f'W{wk_of(mon)+1}'); link(f'w{wk_of(mon)}', M - 30, y + chm - 20, 28, 16)
        for i, dd in enumerate(wk):
            x = M + i * cwm
            c.setStrokeColor(LINE); c.setFillColor(HexColor('#ffffff') if dd else BG); c.rect(x, y, cwm, chm, stroke=1, fill=1)
            if dd:
                c.setFillColor(INK); c.setFont('Helvetica-Bold', 13); c.drawString(x + 6, y + chm - 18, str(dd))
                link(f'd{dt.date(YEAR, m, dd).isoformat()}', x, y + chm - 26, 30, 26)
    nx = W - TABW - M - 200; box(nx, M, 200, H - 120 - M, 'Focus'); lines(nx + 12, H - 180, M + 10, 176)
    c.showPage()

# Weeks
for wi, mon in enumerate(weeks):
    sun = mon + dt.timedelta(6)
    mm = mon.month if mon.year == YEAR else 1
    frame(f'w{wi}', f'm{mm}'); title(f'Week {wi+1}', f'{mon:%d %b} – {sun:%d %b %Y}', back=(calendar.month_name[mm].upper(), f'm{mm}'))
    bw = (W - TABW - 2 * M - 30) / 4; bh = (H - 120 - M - 10) / 2
    for i in range(8):
        x = M + (i % 4) * (bw + 10); y = M + (1 - i // 4) * (bh + 10)
        if i < 7:
            day = mon + dt.timedelta(i); box(x, y, bw, bh, f'{day:%a %d}')
            if day.year == YEAR: link(f'd{day.isoformat()}', x, y + bh - 28, bw, 28)
        else: box(x, y, bw, bh, 'Priorities')
        lines(x + 10, y + bh - 44, y + 8, bw - 20, 24)
    c.showPage()

# Days
for day in days:
    frame(f'd{day.isoformat()}', f'm{day.month}')
    title(f'{day:%A}', f'{day:%d %B %Y}  ·  Week {wk_of(day)+1}', back=(f'WEEK {wk_of(day)+1}', f'w{wk_of(day)}'))
    lw = (W - TABW - 3 * M) * .55; rw = (W - TABW - 3 * M) - lw
    box(M, M, lw, H - 120 - M, 'Schedule')
    c.setFont('Helvetica', 10); c.setFillColor(MUTED)
    y = H - 170
    for hr in range(6, 23):
        c.drawString(M + 12, y + 4, f'{hr:02d}:00'); c.setStrokeColor(LINE); c.line(M + 60, y, M + lw - 12, y); y -= (H - 210 - M) / 17
    rx = M * 2 + lw
    box(rx, H - 80 - 260, rw, 240, 'Top 3'); lines(rx + 12, H - 140 - 40, H - 340, rw - 24, 50)
    box(rx, M, rw, H - 120 - 260 - M, 'Notes'); dots(rx + 16, H - 400, M + 10, rw - 30)
    c.showPage()

# Habits
for m in range(1, 13):
    frame('habits' if m == 1 else f'h{m}', 'habits'); title(f'Habit tracker · {calendar.month_name[m]}', back=('YEAR', 'year'))
    nd = calendar.monthrange(YEAR, m)[1]; gx0 = M + 180; cw = (W - TABW - M - gx0) / nd
    c.setFont('Helvetica', 8); c.setFillColor(MUTED)
    for dd in range(nd): c.drawCentredString(gx0 + dd * cw + cw / 2, H - 118, str(dd + 1))
    for r in range(18):
        y = H - 150 - r * 32
        c.setStrokeColor(LINE); c.line(M, y - 6, M + 170, y - 6)
        for dd in range(nd): c.setFillColor(HexColor('#ffffff')); c.circle(gx0 + dd * cw + cw / 2, y, min(cw, 22) / 2 - 2, stroke=1, fill=1)
    if m < 12:
        c.setFont('Helvetica-Bold', 12); c.setFillColor(ACC); c.drawRightString(W - TABW - M, M - 20 + 10, 'NEXT MONTH →'); link(f'h{m+1}', W - TABW - M - 110, M - 16, 110, 22)
    c.showPage()

# Notes
for n in range(1, 21):
    frame(f'notes{n}', 'notes1'); title(f'Notes {n}', back=('YEAR', 'year'))
    (lines if n % 2 else dots)(M, H - 120, M, W - TABW - 2 * M, 30 if n % 2 else 24)
    if n < 20:
        c.setFont('Helvetica-Bold', 12); c.setFillColor(ACC); c.drawRightString(W - TABW - M, 16, 'NEXT →'); link(f'notes{n+1}', W - TABW - M - 70, 10, 70, 22)
    c.showPage()
c.save()
print(OUT)
