"""Write upload-ready listing files for the POD designs and stock assets.

Run: python3 pod-designs/listings.py DEST_DIR
"""
import csv
import json
import os
import sys

DEST = sys.argv[1]

# slug: (title, main tag, tags, description, best garment colours)
POD = {
    "coffee-and-deadlines": ("Powered by Coffee and Deadlines Retro Sunset", "freelancer", "coffee lover, deadline, work from home, retro sunset, vintage, coffee mug, office humor, remote work, entrepreneur, self employed, caffeine, workaholic, small business, coworker gift, funny work", "A retro striped sunset and a steaming mug for anyone who runs on caffeine and due dates. Great gift for freelancers, remote workers and small business owners."),
    "out-of-office-mentally": ("Out of Office (Mentally) Funny Work Humor", "out of office", "work humor, office humor, vacation mode, funny quote, coworker gift, sarcastic, retro, typography, burnout, weekend, remote work, introvert, monday, boss gift, corporate humor", "Bold retro type for the days your body is at work but your mind is on a beach. A funny gift for coworkers and anyone counting down to the weekend."),
    "invoice-sent-vibes-pending": ("Invoice Sent Vibes Pending Freelancer Humor", "freelancer", "invoice, self employed, small business, entrepreneur, side hustle, graphic designer, freelance life, accountant, work humor, funny business, get paid, solopreneur, creative, gift for freelancer, retro", "For every freelancer who has hit send on an invoice and then waited. Clean retro typography with a little paper invoice and a gold star."),
    "professional-overthinker": ("Professional Overthinker Retro Rings", "overthinker", "overthinking, anxiety humor, introvert, funny quote, retro, 70s, mental health, sarcastic, psychology, self care, typography, vintage, gift for her, gift for him, mood", "Colourful 70s rings spiral into the bullseye of every thought you have had today. For the professional overthinkers among us."),
    "houseplant-collector": ("Houseplant Collector Plant Lover Gift", "houseplant", "plant lover, plants, monstera, gardening, crazy plant person, botanical, plant parent, indoor plants, succulent, greenery, nature, gift for gardener, urban jungle, plant addict, leaves", "A terracotta pot overflowing with leaves for the person whose windowsill is already full and is still buying more plants."),
    "propagate-positivity": ("Propagate Positivity Plant Cutting in Jar", "plant lover", "propagation, houseplant, positive vibes, good vibes, plants, botanical, plant parent, gardening, pothos, optimism, inspirational, cute plant, nature lover, indoor garden, plant pun", "A plant cutting rooting in a glass jar with a hopeful pun. Perfect for plant parents and positive people."),
    "knead-more-sleep": ("Knead More Sleep Bread Baking Pun", "baking", "sourdough, bread, baker, baking pun, food pun, sleepy, nap, homemade bread, kitchen, chef, funny food, cook, bakery, carbs, foodie", "A cosy loaf of bread snoozing under a few z's. For sourdough bakers and anyone who needs more rest."),
    "cat-naps-lifestyle": ("Cat Naps Are a Lifestyle Sleepy Cat", "cat", "cat lover, cat nap, sleepy cat, cute cat, nap queen, lazy, cat mom, cat dad, kitty, cat lady, pet lover, introvert, cozy, funny cat, orange cat", "A sleepy orange cat who has mastered the art of the nap. A cute gift for cat lovers and professional nappers."),
    "just-one-more-chapter-lies": ("Just One More Chapter (Lies) Book Lover", "book lover", "reading, bookworm, books, reader, library, librarian, book club, bibliophile, book nerd, english teacher, bookish, read more, book stack, literature, gift for reader", "A colourful stack of books and an honest confession. For readers who always stay up past bedtime."),
    "running-on-spreadsheets": ("Running on Spreadsheets Accountant Humor", "spreadsheet", "excel, accountant, accounting, data analyst, finance, office humor, cpa, bookkeeper, spreadsheet nerd, tax season, numbers, data, budget, work humor, nerd", "A cheerful grid and bar chart with a formula only office people will get. For accountants, analysts and spreadsheet lovers."),
    "ctrl-alt-relax": ("Ctrl Alt Relax Keyboard Keys", "programmer", "coder, developer, computer, keyboard, relax, chill, it support, tech humor, software engineer, nerd, geek, gamer, work from home, retro, funny computer", "Three chunky keyboard keys for the most important shortcut of all. For developers, IT folks and anyone who needs a break."),
    "weekend-forecast-hiking": ("Weekend Forecast 100% Hiking Retro Mountains", "hiking", "hiker, mountains, outdoors, camping, adventure, nature, retro sunset, trail, backpacking, explore, national park, weekend, wanderlust, outdoor lover, vintage", "A retro sunset over snowy peaks with a weekend forecast every hiker wants. For trail lovers and outdoor adventurers."),
    "good-things-take-thyme": ("Good Things Take Thyme Herb Garden Pun", "gardening", "gardener, herb garden, thyme, garden pun, plant pun, patience, cooking, chef, botanical, plants, kitchen garden, food pun, gift for gardener, nature, positive", "A sprig of thyme and a gentle reminder to be patient. For gardeners, cooks and pun lovers."),
    "dog-hair-happiness": ("Covered in Dog Hair and Happiness", "dog lover", "dog, dog mom, dog dad, paw print, pet lover, puppy, dog owner, rescue dog, fur baby, dog hair, funny dog, pet parent, dog walker, k9, gift for dog owner", "A sunny paw print for dog people whose clothes are never lint-free and who would not change a thing."),
    "fueled-by-tacos": ("Fueled by Tacos Food Lover", "tacos", "taco tuesday, mexican food, foodie, food lover, funny food, taco lover, burrito, fiesta, hungry, snack, chef, cinco de mayo, spicy, retro, food humor", "A bright taco with all the toppings. For anyone powered by tortillas."),
    "cozy-season": ("Cozy Season Hot Cocoa Mug", "cozy", "autumn, fall, winter, hot chocolate, coffee, cozy vibes, hygge, sweater weather, christmas, holiday, warm drink, cute, retro, stars, homebody", "A steaming pink mug under little stars in chunky retro lettering. Perfect for fall and winter."),
    "grumpy-before-coffee": ("Grumpy Before Coffee Funny Face", "coffee", "coffee lover, morning person, not a morning person, grumpy, caffeine, funny face, sarcastic, mood, office humor, barista, espresso, latte, monday, cranky, coffee addict", "A grumpy yellow face that will not talk to you until the first coffee. For the not-a-morning-person crowd."),
    "debugging-my-life": ("Debugging My Life Programmer Humor", "programmer", "coder, developer, software engineer, coding, debugging, computer science, tech humor, terminal, geek, nerd, web developer, it, devops, hacker, funny code", "A terminal window running a quick diagnostic on life: coffee OK, sleep not found. For developers everywhere."),
    "paddle-up-stress-down": ("Paddle Up Stress Down Paddle Sport", "pickleball", "paddle, paddle sports, racket, sport, player, retirement, coach, team, tournament, court, game, gift for player, active, fitness, hobby", "Two crossed paddles and a ball with a calm-down motto. For pickleball and paddle sport fans."),
    "retro-sunset-mountains": ("Retro Sunset Mountains Badge", "mountains", "retro sunset, vintage, landscape, nature, outdoors, hiking, camping, adventure, minimalist, 70s, 80s, travel, wanderlust, lake, scenic", "A minimalist round badge with a striped sun, purple peaks and a dark lake. Works on shirts, stickers, mugs and posters."),
    "ocean-waves-badge": ("Salt Water State of Mind Retro Waves", "beach", "ocean, waves, surf, surfing, summer, sunset, vacation, sea, coastal, beach life, island, salt water, vintage, retro, travel", "Layered waves under a pink striped sun. For beach lovers, surfers and anyone who would rather be by the sea."),
    "night-owl-club": ("Night Owl Club Cute Owl", "owl", "night owl, night person, insomnia, stars, bird lover, cute owl, sleepy, introvert, gamer, student, midnight, nocturnal, retro, purple, animals", "A wide-eyed purple owl under the stars for people who do their best work after midnight."),
    "plant-more-worry-less": ("Plant More Worry Less Gardening", "gardening", "plants, gardener, plant lover, positive vibes, mindfulness, self care, nature, botanical, leaves, garden, mental health, calm, growth, inspirational, houseplant", "A fan of leaves and a calming motto for gardeners and plant lovers."),
    "self-employed-self-motivated": ("Self Employed Self Motivated Badge", "entrepreneur", "self employed, small business owner, freelancer, boss, hustle, side hustle, motivation, work from home, ceo, startup, laptop, business owner, solopreneur, remote work, gift for boss", "A round badge with a laptop and a star for people who are their own boss."),
}

STOCK = {
    "icons": {
        "name": "Freelance & Remote Work Line Icons (48 SVG, PNG, EPS)",
        "price_usd": 9, "zip": "Freelance-Remote-Work-Icons.zip", "cover": "icons-cover.png",
        "summary": "48 matching line icons for freelancers, remote teams and small business sites.",
        "tags": ["icons", "line-icons", "svg-icons", "icon-set", "web-design", "ui-kit"],
        "description": "<p>48 hand-drawn-on-a-grid line icons that match perfectly: laptop, coffee, invoice, wallet, calendar, video call, kanban, rocket, chart and more.</p><ul><li>SVG with editable stroke (uses currentColor, so CSS can recolor them)</li><li>PNG at 64, 256 and 512 px in navy, white and teal</li><li>EPS for Illustrator and print</li><li>SVG sprite for websites</li></ul><p>Commercial license included. Instant download (.zip).</p>",
        "keywords": "icons, line icons, icon set, freelance, remote work, office, business, outline, web icons, ui, vector, symbol, laptop, coffee, invoice, wallet, calendar, video call, chat, email, briefcase, home office, chart, target, rocket, lightbulb, team, user, settings, search, minimal, stroke, flat, pictogram, collection, simple, modern, interface, app, website, sign, set, editable, isolated, navy, graphic, illustration, pack, symbols",
    },
    "patterns": {
        "name": "12 Retro Seamless Patterns (SVG, EPS, PNG, JPG)",
        "price_usd": 9, "zip": "Retro-Seamless-Patterns.zip", "cover": "patterns-cover.png",
        "summary": "Warm 70s-style repeat patterns for packaging, fabric, stationery and the web.",
        "tags": ["seamless-pattern", "retro", "surface-pattern", "digital-paper", "svg", "canva"],
        "description": "<p>12 seamless patterns in warm retro palettes: terrazzo, waves, mid-century arches, rainbows, leaves, polka dots, soft checker, stars, squiggles, stripes, plus grid and geometric triangles.</p><ul><li>Vector SVG tiles and EPS swatches</li><li>1000 px PNG tiles</li><li>3600 x 3600 px JPG digital papers</li></ul><p>Use for print-on-demand, packaging, scrapbooking, wrapping paper, fabric, phone cases and websites. Commercial license included. Instant download (.zip).</p>",
        "keywords": "seamless pattern, pattern, retro, vintage, 70s, background, texture, repeat, wallpaper, fabric, textile, wrapping paper, digital paper, terrazzo, waves, arches, rainbow, leaves, polka dots, checker, stars, squiggles, stripes, geometric, triangles, mid century, boho, vector, illustration, design, decorative, surface, print, packaging, scrapbook, colorful, pastel, abstract, modern, minimal, trendy, cute, ornament, tile, endless, backdrop, cover, stationery, graphic",
    },
    "backgrounds": {
        "name": "12 Grainy Gradient Backgrounds (6000 x 4000 JPG)",
        "price_usd": 7, "zip": "Grainy-Gradient-Backgrounds.zip", "cover": "backgrounds-cover.png",
        "summary": "Soft grainy gradients for social posts, slides, website heroes and wallpapers.",
        "tags": ["backgrounds", "gradient", "grainy-texture", "wallpaper", "social-media", "canva"],
        "description": "<p>12 trendy grainy gradient backgrounds at 6000 x 4000 px (24 MP): sunset glow, ocean mist, sage morning, berry dusk, peach cream, midnight aurora, lavender haze, citrus pop, deep forest, cotton candy, desert dunes and electric blue.</p><p>Drop them behind text in Canva, Figma, Keynote or Photoshop for instant polish. Crop to any size, from Instagram squares to 4K wallpapers. Commercial license included. Instant download (.zip).</p>",
        "keywords": "gradient, background, abstract, grain, grainy, noise, texture, blur, blurred, soft, color, colorful, pastel, wallpaper, backdrop, modern, trendy, aesthetic, mesh gradient, holographic, aura, glow, light, smooth, vibrant, banner, cover, social media, presentation, website, hero, design, template, minimal, dreamy, sunset, ocean, pink, blue, purple, orange, green, teal, warm, cool, digital, art, creative, header",
    },
}

ADOBE_CAT = 8  # Graphic Resources

PATTERN_TITLES = {
    "terrazzo": "Retro terrazzo seamless pattern with colorful stone chips",
    "retro-waves": "Retro wavy lines seamless pattern in warm 70s colors",
    "mid-century-arches": "Mid century arches seamless pattern in sage green",
    "polka-dots": "Pink and plum polka dot seamless pattern",
    "leafy": "Simple leaves seamless pattern in sage and teal",
    "soft-checker": "Soft rounded checkerboard seamless pattern in blush pink",
    "starry": "Scattered stars seamless pattern on light blue",
    "plus-grid": "Plus sign grid seamless pattern in blue and navy",
    "memphis-squiggles": "Memphis style squiggles seamless pattern",
    "bold-stripes": "Bold horizontal stripes seamless pattern in pink and rust",
    "little-rainbows": "Little retro rainbows seamless pattern",
    "geo-triangles": "Geometric triangles seamless pattern in blue and teal",
}


def main():
    pod = os.path.join(DEST, "pod")
    os.makedirs(pod, exist_ok=True)
    with open(os.path.join(pod, "listings.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "title", "main_tag", "tags", "description"])
        for slug, (title, main, tags, desc) in POD.items():
            w.writerow([f"{slug}.png", title, main, tags, desc])
    lines = ["# Print-on-demand listings (Redbubble and Teepublic)", "",
             "Each design has two files with the same name: `light-shirts/` (navy ink, for white, cream, pastel and heather products) and `dark-shirts/` (cream ink, for black, navy and dark products). Upload the light version first; on Teepublic you can add the dark version as the alternate design for dark garments.", ""]
    for i, (slug, (title, main, tags, desc)) in enumerate(POD.items(), 1):
        lines += [f"## {i}. {title}", f"- File: `{slug}.png`", f"- Title: {title}", f"- Main tag (Teepublic): {main}", f"- Tags: {main}, {tags}", f"- Description: {desc}", ""]
    open(os.path.join(pod, "LISTINGS.md"), "w").write("\n".join(lines))

    stock = os.path.join(DEST, "stock")
    os.makedirs(stock, exist_ok=True)
    rows = []
    rows.append(["freelance-remote-work-line-icons-set.eps", "Freelance and remote work line icon set, 48 outline vector icons", STOCK["icons"]["keywords"], ADOBE_CAT, ""])
    for k, t in PATTERN_TITLES.items():
        rows.append([f"pattern-{k}.eps", t + ", vector", STOCK["patterns"]["keywords"], ADOBE_CAT, ""])
    for name in ["sunset-glow", "ocean-mist", "sage-morning", "berry-dusk", "peach-cream", "midnight-aurora", "lavender-haze", "citrus-pop", "deep-forest", "cotton-candy", "desert-dunes", "electric-blue"]:
        nice = name.replace("-", " ")
        rows.append([f"background-{name}.jpg", f"Abstract grainy gradient background, {nice} colors, soft blurred texture", STOCK["backgrounds"]["keywords"], ADOBE_CAT, ""])
    with open(os.path.join(stock, "adobe-stock-upload", "adobe-stock-metadata.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Filename", "Title", "Keywords", "Category", "Releases"])
        w.writerows(rows)
    json.dump(STOCK, open(os.path.join(stock, "packs.json"), "w"), indent=1)

    md = ["# Stock asset packs", "", "Three packs, each a ready zip with a commercial license file and a cover image. The same text works on Creative Market, Gumroad and Etsy.", ""]
    for k, p in STOCK.items():
        md += [f"## {p['name']}", f"- Zip: `{p['zip']}`", f"- Cover: `{p['cover']}` (Gumroad, 1280x720) and `{k}-cover-creative-market.jpg` (Creative Market, 1820x1214)",
               f"- Suggested price: ${p['price_usd']} on Gumroad and Etsy, ${p['price_usd'] + 3} on Creative Market (it takes a bigger cut)",
               f"- Short summary: {p['summary']}", f"- Tags: {', '.join(t.replace('-', ' ') for t in p['tags'])}",
               "- Description:", "", p["description"].replace("<p>", "").replace("</p>", "\n").replace("<ul>", "").replace("</ul>", "").replace("<li>", "- ").replace("</li>", "\n"), ""]
    md += ["## Adobe Stock", "", f"`adobe-stock-upload/` holds {len(rows)} files (the icon set and 12 patterns as EPS vectors, plus 12 backgrounds as JPG; Adobe makes the vector previews itself, so no extra JPGs). Upload them all, then upload `adobe-stock-metadata.csv` on the CSV tab and every title and keyword fills in. Category is Graphic Resources. Answer \"No\" to \"Created using generative AI tools\": these were drawn with code, not an AI image model.", ""]
    open(os.path.join(stock, "LISTINGS.md"), "w").write("\n".join(md))
    print("listings written", len(POD), len(rows))


if __name__ == "__main__":
    main()
