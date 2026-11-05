"""Zip each Canva pack with a how-to-edit guide, render covers, copy everything to
/mnt/project-files/income/canva/. Usage: python3 package.py BUILD_DIR  (BUILD_DIR from build.py)"""
import sys, os, glob, zipfile, json, base64, subprocess
B = os.path.abspath(sys.argv[1]); DST = "/mnt/project-files/income/canva/"; os.makedirs(DST, exist_ok=True)
PV = os.path.join(B, "previews"); PK = os.path.join(B, "packs")
GUIDE = """HOW TO EDIT YOUR TEMPLATES

IN CANVA (free account is fine)
1. Go to canva.com and sign in.
2. Click "Upload" (or Create a design > Import file) and choose the .pptx file.
3. Canva opens it as a normal editable design. Click any text to change it.
4. To add your photo: delete the beige "Drop your photo here" box, add a Frame
   from Elements, and drag your photo onto it. Or just drag the photo onto the page.
5. Download as PNG or JPG (Share > Download) and post.

IN POWERPOINT, KEYNOTE OR GOOGLE SLIDES
Open the .pptx file directly. Each page is one slide.

FONTS
Montserrat and Playfair Display: both free Google Fonts, built into Canva and Google Slides.
For PowerPoint/Keynote, install them free from fonts.google.com.

LICENCE
Use for your own business or personal brand, as many times as you like.
Do not resell or share the template files.
"""
P = [("instagram-post-templates", "Instagram-Post-Templates-Small-Business", ["Instagram-Post-Templates-Small-Business.pptx"], "15 Instagram Post Templates", "For small business · Edit in Canva", "#c4663f", 4, "Instagram-Post-Templates-Small-Business-*.png"),
     ("pinterest-pin-templates", "Pinterest-Pin-Templates", ["Pinterest-Pin-Templates.pptx"], "10 Pinterest Pin Templates", "For bloggers & shops · Edit in Canva", "#1d3557", 5, "Pinterest-Pin-Templates-*.png"),
     ("resume-templates", "Resume-Templates", ["Resume-Templates.pptx"], "3 Resume Templates + Cover Letter", "US Letter · Matching cover letter", "#1f3a5f", 4, "Resume-Templates-*.png"),
     ("etsy-shop-branding-kit", "Etsy-Shop-Branding-Kit", ["Etsy-Shop-Branding-Kit/" + f for f in sorted(os.listdir(os.path.join(PK, "Etsy-Shop-Branding-Kit")))], "Etsy Shop Branding Kit", "Banner · Icon · Thumbnails · Thank-you card", "#2b2b2b", 3, "[1234]-*.png")]
jobs = []
def b64(p): return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()
for slug, name, files, title, sub, acc, cols, pat in P:
    z = DST + name + ".zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files: zf.write(os.path.join(PK, f), name + "/" + os.path.basename(f))
        zf.writestr(name + "/HOW-TO-EDIT.txt", GUIDE)
    pv = sorted(glob.glob(os.path.join(PV, pat)))
    pd = DST + slug + "-previews/"; os.makedirs(pd, exist_ok=True)
    for f in pv: subprocess.run(["cp", f, pd])
    shown = pv[:cols * 2] if slug != "resume-templates" else pv[:3]
    tiles = "".join(f'<img src="{b64(f)}" style="width:100%;border-radius:10px;box-shadow:0 12px 30px rgba(0,0,0,.3);display:block">' for f in shown)
    html = f"""<html><body style="margin:0;width:2000px;height:1600px;background:{acc};font-family:Inter,sans-serif;color:#fff;overflow:hidden">
<div style="padding:90px 100px 40px"><div style="font-size:96px;font-weight:800;line-height:1">{title}</div><div style="font-size:48px;opacity:.9;margin-top:20px">{sub}</div></div>
<div style="display:grid;grid-template-columns:repeat({cols if slug!='resume-templates' else 3},1fr);gap:28px;padding:0 100px;align-items:start">{tiles}</div>
<div style="position:absolute;right:90px;bottom:70px;background:#fff;color:{acc};font-size:40px;font-weight:800;padding:18px 36px;border-radius:50px">Canva · PowerPoint · Slides</div></body></html>"""
    jobs.append(dict(out=DST + slug + "-cover.jpg", html=html, w=2000, h=1600))
json.dump(jobs, open(os.path.join(B, "jobs.json"), "w"))
