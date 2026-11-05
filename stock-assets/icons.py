"""Original line icon set: "Freelance & Remote Work" (48 icons, 24px grid, 1.75 stroke).

Writes SVG (editable stroke), PNG (64/256/512), EPS per icon, an SVG sprite and a preview cover.
Run: python3 stock-assets/icons.py OUT_DIR
"""
import os
import sys

import cairosvg

OUT = sys.argv[1]
S = 'fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"'

ICONS = {
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
    "monitor": '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M9 20h6M12 16v4"/>',
    "coffee": '<path d="M4 9h12v6a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4z"/><path d="M16 11h1.5a2.5 2.5 0 0 1 0 5H16"/><path d="M8 3c-.8 1 .8 2 0 3M12 3c-.8 1 .8 2 0 3"/>',
    "invoice": '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 11h7M9 14h7M9 17h4"/>',
    "wallet": '<path d="M4 7h15a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z"/><path d="M4 7l11-3v3"/><path d="M20 12h-4a1.5 1.5 0 0 0 0 3h4"/>',
    "coins": '<ellipse cx="9" cy="7" rx="5" ry="2.5"/><path d="M4 7v4c0 1.4 2.2 2.5 5 2.5s5-1.1 5-2.5V7"/><path d="M10 15.5c0 1.4 2.2 2.5 5 2.5s5-1.1 5-2.5v-4c0-1.4-2.2-2.5-5-2.5"/><path d="M10 15.5v-1"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="1.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/><path d="M8 14h2M14 14h2M8 17h2"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "timer": '<circle cx="12" cy="13.5" r="7"/><path d="M12 10v3.5l2 1.5M10 3h4M12 3v3.5M18.5 6.5l1.5-1.5"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "video-call": '<rect x="3" y="6" width="13" height="12" rx="1.5"/><path d="M16 10l5-3v10l-5-3"/>',
    "headphones": '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3.5 6l8.5 7 8.5-7"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="1.5"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M3 12.5h18M11 12.5h2v2h-2z"/>',
    "home-office": '<path d="M3 11l9-7 9 7"/><path d="M5 9.5V20h14V9.5"/><rect x="9" y="12" width="6" height="4" rx=".5"/><path d="M8 18h8"/>',
    "plant": '<path d="M8 15h8l-1 6H9z"/><path d="M12 15V9"/><path d="M12 10c0-3 2-5 5-5 0 3-2 5-5 5zM12 12c0-2.5-2-4-4.5-4 0 2.5 2 4 4.5 4z"/>',
    "lightbulb": '<path d="M9 17h6M10 20h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.4.3.5.8.5 1.3V17h6v-1.8c0-.5.1-1 .5-1.3A6 6 0 0 0 12 3z"/>',
    "rocket": '<path d="M12 3c3 2 5 5.5 4 11l-2 2h-4l-2-2C7 8.5 9 5 12 3z"/><circle cx="12" cy="9.5" r="1.5"/><path d="M8 14l-3 2 1 4 3-2M16 14l3 2-1 4-3-2M11 19l1 2 1-2"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    "chart-up": '<path d="M4 4v16h16"/><path d="M7 15l4-4 3 3 5-6"/><path d="M15 8h4v4"/>',
    "pie-chart": '<path d="M12 3.5a8.5 8.5 0 1 0 8.5 8.5H12z"/><path d="M15 3.8A8.5 8.5 0 0 1 20.2 9H15z"/>',
    "checklist": '<path d="M4 6l1.5 1.5L8 5M4 12l1.5 1.5L8 11M4 18l1.5 1.5L8 17M11 6.5h9M11 12.5h9M11 18.5h9"/>',
    "kanban": '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M9 4v16M15 4v16"/><path d="M5 8h2M11 8h2M17 8h2M5 11h2M11 11h2"/>',
    "folder": '<path d="M3 6a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/>',
    "cloud-upload": '<path d="M7 18a4.5 4.5 0 0 1-.5-9A6 6 0 0 1 18 9.5a4 4 0 0 1-.5 8.5"/><path d="M12 12v8M9 15l3-3 3 3"/>',
    "wifi": '<path d="M2.5 9a14 14 0 0 1 19 0M5.5 12.5a9.5 9.5 0 0 1 13 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19" r=".8"/>',
    "lock": '<rect x="5" y="10" width="14" height="10" rx="1.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v2"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 20a8 8 0 0 1 16 0"/>',
    "team": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M15.5 4.8a3.5 3.5 0 0 1 0 6.4M18 14a6.5 6.5 0 0 1 3.5 6"/>',
    "star": '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z"/>',
    "megaphone": '<path d="M3 10v4a1 1 0 0 0 1 1h3l9 5V4L7 9H4a1 1 0 0 0-1 1z"/><path d="M7 15l1.5 5M19 9.5a3 3 0 0 1 0 5"/>',
    "pencil": '<path d="M4 20l1-4L16 5l3 3L8 19z"/><path d="M14 7l3 3"/>',
    "palette": '<path d="M12 3.5a8.5 8.5 0 0 0 0 17c1.4 0 2-1 1.4-2.1-.7-1.2.1-2.4 1.5-2.4H17a3.5 3.5 0 0 0 3.5-3.5c0-5-3.8-9-8.5-9z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7.5" r="1"/><circle cx="14.5" cy="7.5" r="1"/>',
    "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
    "camera": '<path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.5" r="3.5"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.5 3.5 5.5 3.5 8.5s-1 6-3.5 8.5c-2.5-2.5-3.5-5.5-3.5-8.5s1-6 3.5-8.5z"/>',
    "send": '<path d="M21 3L3 10.5l7 3 3 7.5z"/><path d="M10 13.5L21 3"/>',
    "suitcase": '<rect x="4" y="7" width="16" height="13" rx="2"/><path d="M9 7V4h6v3M8 7v13M16 7v13"/>',
    "receipt": '<path d="M6 3h12v18l-2-1.5-2 1.5-2-1.5-2 1.5-2-1.5L6 21z"/><path d="M9 8h6M9 11.5h6M9 15h3"/>',
    "credit-card": '<rect x="3" y="5.5" width="18" height="13" rx="1.5"/><path d="M3 10h18M6.5 15h3"/>',
    "percent": '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
    "calculator": '<rect x="5" y="3" width="14" height="18" rx="1.5"/><rect x="8" y="6" width="8" height="3.5" rx=".5"/><path d="M8.5 13h.01M12 13h.01M15.5 13h.01M8.5 16.5h.01M12 16.5h.01M15.5 16.5h.01" stroke-width="2.2"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M5.5 18.5l1.7-1.7M16.8 7.2l1.7-1.7"/><circle cx="12" cy="12" r="6.5"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L20.5 20.5"/>',
    "bookmark": '<path d="M6 3.5h12V21l-6-4.5L6 21z"/>',
    "moon-focus": '<path d="M19.5 14.5A8 8 0 0 1 9.5 4.5a8 8 0 1 0 10 10z"/><path d="M16 4l.7 1.5L18 6l-1.3.5L16 8l-.7-1.5L14 6l1.3-.5z"/>',
}

COLORS = {"black": "#1F2A44", "white": "#FFFFFF", "teal": "#2A7F7A"}


def svg(body, color="currentColor", size=24):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'{S.replace("currentColor", color)}>{body}</svg>')


def main():
    for sub in ("svg", "png/64", "png/256", "png/512", "eps", "png-white/512", "png-teal/512"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    sprite = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']
    for name, body in ICONS.items():
        open(os.path.join(OUT, "svg", f"{name}.svg"), "w").write(svg(body))
        dark = svg(body, COLORS["black"])
        for px in (64, 256, 512):
            cairosvg.svg2png(bytestring=dark.encode(), write_to=os.path.join(OUT, f"png/{px}/{name}.png"), output_width=px, output_height=px)
        cairosvg.svg2png(bytestring=svg(body, COLORS["white"]).encode(), write_to=os.path.join(OUT, f"png-white/512/{name}.png"), output_width=512, output_height=512)
        cairosvg.svg2png(bytestring=svg(body, COLORS["teal"]).encode(), write_to=os.path.join(OUT, f"png-teal/512/{name}.png"), output_width=512, output_height=512)
        pdf = cairosvg.svg2pdf(bytestring=svg(body, "#000000", 240).encode())
        tmp = os.path.join(OUT, "eps", f"{name}.pdf")
        open(tmp, "wb").write(pdf)
        os.system(f'pdftocairo -eps "{tmp}" "{os.path.join(OUT, "eps", name + ".eps")}" && rm "{tmp}"')
        sprite.append(f'<symbol id="i-{name}" viewBox="0 0 24 24" {S}>{body}</symbol>')
    sprite.append("</svg>")
    open(os.path.join(OUT, "sprite.svg"), "w").write("".join(sprite))
    print(len(ICONS), "icons")


if __name__ == "__main__":
    main()
