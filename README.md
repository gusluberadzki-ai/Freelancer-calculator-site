# Passive income projects

Everything here is a static site deployed free to GitHub Pages by `.github/workflows/pages.yml` on every push to `main`.

| Folder | What it is | Live URL |
|---|---|---|
| `freelance-calc/` | RateKit, freelancer calculators (ads + affiliate) | /freelance-calc/ |
| `freelance-tools/` | Freelance Toolbox, curated tools directory (affiliate + featured listings) | /freelance-tools/ |
| `chrome-extension/` | TickBill Chrome extension + landing page and privacy policy | /chrome-extension/ |
| `templates/` | Freelance Business Tracker spreadsheet sold on Gumroad | not deployed as a page |
| `invoice-generator/` | Free invoice generator with $5 Pro unlock (Gumroad licence key) | /invoice-generator/ |
| `resume-builder/` | Free resume/CV builder with CHF 7 Pro unlock (Gumroad receipt link, code hash in app.js) | /resume-builder/ |
| `background-remover/` | In-browser AI background remover (ads) | /background-remover/ |
| `app/` | TickBill installable phone app (PWA) | /app/ |
| `kdp-planner/` | Amazon KDP planner book generator | not deployed |
| `pdf-tools/` | Merge/split/remove/rotate PDF (vendored pdf-lib, MIT) | /pdf-tools/ |
| `percentage-calculator/`, `date-calculator/`, `word-counter/` | Evergreen ad-supported tools | /<folder>/ |
| `salary/` | 302 programmatic salary pages (`python3 build.py`) | /salary/ |
| `qr-code-generator/`, `image-compressor/` | Free tools (ads) | /<folder>/ |
| `tools/` | 69 generated free tools (`python3 build.py`; tool lists in build.py, more_tools.py, round8_tools.py) | /tools/ |
| `blog/` | RateKit Blog: affiliate articles (`python3 build.py`; posts in posts.py, referral links in affiliates.json) | /blog/ |
| `portfolio-template/` | Portfolio website template sold on Gumroad | /portfolio-template/template/ (demo) |

Rebuild a generated site with `python3 build.py` inside its folder.
