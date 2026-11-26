# Round 16 printables. exec()'d by build_round.py, so lines/chks are in scope.
WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
def tbl(heads, widths, n, h=22):
    return ('<table><tr>' + "".join(f"<th style='width:{w}'>{x}</th>" if w else f"<th>{x}</th>" for x, w in zip(heads, widths)) + '</tr>'
            + (f"<tr style='height:{h}pt'>" + "<td></td>" * len(heads) + "</tr>") * n + '</table>')
def box(t, body, flex=1, extra=""): return f'<div class="box" style="flex:{flex};margin-bottom:5pt;{extra}"><b>{t}</b>{body}</div>'
def items(xs): return "".join(f'<div class="chk"><i></i>{x}</div>' for x in xs)
def lab(t, n): return f'<div class="lbl">{t}</div>' + lines(n)
def two(a, b): return f'<div class="cols"><div>{a}</div><div>{b}</div></div>'
def row(*bs): return '<div class="cols">' + "".join(bs) + '</div>'
def scale(lo, hi, n=5): return '<div style="display:flex;align-items:center;gap:6pt;margin-top:3pt;font-size:8pt"><span>' + lo + '</span>' + '<span style="width:14pt;height:14pt;border:1.2pt solid #bbb;border-radius:50%"></span>' * n + '<span>' + hi + '</span></div>'

def birds():
    sight = ('<div class="pg"><div class="sub"><h1>Birding Outing</h1><span>Date: ______________</span></div>' + row(box("Location", lines(1), 2), box("Habitat", lines(1)), box("Time", lines(1)))
             + row(box("Weather", lines(1)), box("Temperature", lines(1)), box("Wind", lines(1)), box("Birded with", lines(1)))
             + '<div class="lbl">Species seen</div>' + tbl(["Species", "Count", "Male / female / young", "Behaviour", "Heard / seen", "New ✓"], ["26%", "8%", "16%", "", "12%", "8%"], 16, 22)
             + two(lab("Highlight of the day", 3), lab("Notes for next time", 3)) + '</div>')
    sketch = ('<div class="pg"><div class="sub"><h1>Field Sketch</h1><span>Date: ______________</span></div><div class="box" style="height:330pt;margin-bottom:6pt"><b>Sketch</b></div>'
              + row(box("Size", '<div class="small" style="margin-top:3pt">☐ sparrow ☐ robin ☐ blackbird ☐ pigeon ☐ crow ☐ larger</div>', 2), box("Bill shape", lines(1)))
              + two(box("Colours & markings", lines(4)), box("Call / song", lines(4))) + row(box("Where", lines(1)), box("What it was doing", lines(1))) + lab("I think it was", 1) + '</div>')
    life = ('<div class="pg"><div class="sub"><h1>Life List</h1><span>Every species, the first time you see it</span></div>' + tbl(["No.", "Species", "Date first seen", "Where", "Notes"], ["7%", "28%", "14%", "22%", ""], 30, 22) + '</div>')
    garden = ('<div class="pg"><div class="sub"><h1>Garden Bird Count</h1><span>Month: ______________</span></div><div class="small">Watch your garden or window for an hour each week and note the most of each species seen at once.</div>'
              + '<table><tr><th style="width:28%">Species</th>' + "".join(f"<th style='text-align:center'>Week {i}</th>" for i in range(1, 6)) + '</tr>'
              + "".join(f"<tr style='height:24pt'><td>{s}</td>" + "<td></td>" * 5 + "</tr>" for s in ["Robin", "Blackbird", "Blue tit", "Great tit", "House sparrow", "Starling", "Goldfinch", "Wood pigeon", "Magpie", "Chaffinch", "Wren", "Dunnock", "", "", "", ""])
              + '</table>' + two(box("Feeders out", items(["Seeds", "Fat balls", "Nyjer", "Mealworms", "Water"])), box("Notes", lines(5))) + '</div>')
    wish = ('<div class="pg"><div class="sub"><h1>Birds I Want to See</h1><span></span></div>' + tbl(["Species", "Where to look", "Best season", "Seen ✓"], ["", "30%", "16%", "10%"], 14, 26)
            + '<div class="lbl">Places to go birding</div>' + tbl(["Place", "What's there", "Visited"], ["30%", "", "12%"], 8, 24) + '</div>')
    return [life, sight, sight, sight, sketch, sketch, garden, wish]

def wine():
    note = ('<div class="pg"><div class="sub"><h1>Tasting Notes</h1><span>Date: ______________</span></div>' + row(box("Wine", lines(1), 2), box("Vintage", lines(1)))
            + row(box("Producer", lines(1)), box("Region / country", lines(1)), box("Grape(s)", lines(1)))
            + row(box("Type", '<div class="small" style="margin-top:3pt">☐ red ☐ white ☐ rosé ☐ sparkling ☐ dessert</div>', 2), box("Price", lines(1)), box("Bought at", lines(1)))
            + '<div class="cols"><div class="box"><b>Look</b><div class="small" style="margin-top:3pt">Colour & clarity</div>' + lines(2) + '</div><div class="box"><b>Smell</b><div class="small" style="margin-top:3pt">Fruit, flowers, spice, oak, earth</div>' + lines(2) + '</div></div>'
            + '<div class="box" style="margin-bottom:5pt"><b>Taste</b><div class="cols"><div>' + "".join(f'<div class="small" style="margin-top:4pt">{t}</div>' + scale(a, b) for t, a, b in [("Sweetness", "dry", "sweet"), ("Acidity", "soft", "crisp"), ("Tannin", "smooth", "grippy")])
            + '</div><div>' + "".join(f'<div class="small" style="margin-top:4pt">{t}</div>' + scale(a, b) for t, a, b in [("Body", "light", "full"), ("Finish", "short", "long"), ("Alcohol", "low", "high")]) + '</div></div>' + lines(2) + '</div>'
            + two(box("Food pairing", lines(3)), box("Would I buy it again?", '<div class="small" style="margin-top:3pt">☐ yes ☐ maybe ☐ no</div>' + lines(2))) + '<div class="box" style="height:90pt"><b>Overall</b>  ☆ ☆ ☆ ☆ ☆<div class="small" style="margin-top:6pt">Stick the label here</div></div></div>')
    flight = ('<div class="pg"><div class="sub"><h1>Tasting Flight</h1><span>Event / date: ______________</span></div>' + tbl(["#", "Wine & vintage", "Look", "Smell", "Taste", "Score / 10"], ["5%", "26%", "14%", "", "20%", "10%"], 8, 52)
              + two(lab("Favourite of the night", 2), lab("Notes", 2)) + '</div>')
    cellar = ('<div class="pg"><div class="sub"><h1>Cellar List</h1><span></span></div>' + tbl(["Wine", "Vintage", "Qty", "Bought", "Price", "Drink from", "Drink by", "Opened"], ["", "9%", "6%", "11%", "9%", "11%", "11%", "10%"], 28, 22) + '</div>')
    wheel = ('<div class="pg"><div class="sub"><h1>Aroma Words</h1><span>A cheat sheet for tasting notes</span></div><div class="cols" style="flex:1"><div class="grow">'
             + box("Red & black fruit", '<div class="small" style="line-height:1.8;margin-top:4pt">strawberry · raspberry · cherry · plum · blackberry · blackcurrant · blueberry · fig</div>')
             + box("Citrus, orchard & tropical", '<div class="small" style="line-height:1.8;margin-top:4pt">lemon · lime · grapefruit · apple · pear · peach · apricot · pineapple · mango · passion fruit</div>')
             + box("Floral & herbal", '<div class="small" style="line-height:1.8;margin-top:4pt">rose · violet · elderflower · cut grass · mint · eucalyptus · green pepper · tomato leaf</div>') + '</div><div class="grow">'
             + box("Spice & oak", '<div class="small" style="line-height:1.8;margin-top:4pt">vanilla · clove · cinnamon · black pepper · toast · smoke · coconut · cedar</div>')
             + box("Earth & savoury", '<div class="small" style="line-height:1.8;margin-top:4pt">mushroom · forest floor · leather · tobacco · wet stone · flint · olive</div>')
             + box("Sweet & aged", '<div class="small" style="line-height:1.8;margin-top:4pt">honey · caramel · toffee · dried fruit · nuts · brioche · chocolate · coffee</div>') + '</div></div>'
             + lab("My own words", 4) + '<div class="small" style="margin-top:6pt">Please drink responsibly.</div></div>')
    wish = ('<div class="pg"><div class="sub"><h1>Wines to Try</h1><span></span></div>' + tbl(["Wine / grape / region", "Recommended by", "Where to buy", "Price", "Tried ✓"], ["", "20%", "20%", "10%", "9%"], 18, 24)
            + '<div class="lbl">Wineries & places to visit</div>' + tbl(["Place", "Notes", "Visited"], ["30%", "", "12%"], 7, 24) + '</div>')
    return [wheel, note, note, note, note, flight, cellar, wish]

def thoughts():
    rec = ('<div class="pg"><div class="sub"><h1>Thought Record</h1><span>Date: ______________</span></div>'
           + box("1. Situation", '<div class="small">Where were you, who with, what happened?</div>' + lines(2))
           + box("2. Feelings", '<div class="small">Name them and rate how strong each is (0-100%).</div>' + lines(2))
           + box("3. Automatic thought", '<div class="small">What went through your mind? Which thought hit hardest?</div>' + lines(3))
           + two(box("4. Evidence for the thought", lines(5)), box("5. Evidence against it", lines(5)))
           + box("6. Thinking traps?", '<div class="small" style="margin-top:3pt">☐ all-or-nothing ☐ catastrophising ☐ mind reading ☐ fortune telling ☐ should statements ☐ labelling ☐ discounting the positive ☐ emotional reasoning</div>')
           + box("7. A more balanced thought", lines(3)) + box("8. Feelings now (0-100%)", lines(1)) + '</div>')
    worry = ('<div class="pg"><div class="sub"><h1>Worry Time</h1><span>Date: ______________</span></div><div class="small">Jot worries down during the day, then look at them in a set 15-minute worry time.</div>'
             + tbl(["Worry", "Can I do something about it?", "If yes: next small step", "If no: let it go ✓"], ["32%", "16%", "", "12%"], 10, 34)
             + two(box("Worry time today", '<div class="small" style="margin-top:3pt">Time: ________  Place: ____________</div>'), box("How much I worried today", scale("a little", "a lot", 10)))
             + lab("What I noticed", 4) + '</div>')
    mood = ('<div class="pg"><div class="sub"><h1>Weekly Mood & Activity</h1><span>Week of: ______________</span></div><table><tr><th style="width:14%"></th>' + "".join(f"<th style='text-align:center'>{d}</th>" for d in WD) + '</tr>'
            + "".join(f"<tr style='height:{h}pt'><td>{t}</td>" + "<td></td>" * 7 + "</tr>" for t, h in [("Mood 0-10", 26), ("Anxiety 0-10", 26), ("Sleep (hrs)", 26), ("Moved my body", 26), ("Saw / spoke to someone", 30), ("Something I enjoyed", 52), ("Something I achieved", 52)])
            + '</table>' + two(lab("Patterns I notice", 4), lab("One thing to try next week", 4)) + '</div>')
    cope = ('<div class="pg"><div class="sub"><h1>My Coping Plan</h1><span></span></div>' + two(box("Early warning signs", lines(5)), box("Things that make it worse", lines(5)))
            + two(box("Things that help me feel calmer", items([""] * 6)), box("People I can talk to", '<div class="small">Name & number</div>' + lines(5)))
            + box("Grounding: 5-4-3-2-1", '<div class="small" style="line-height:1.8;margin-top:3pt">Name 5 things you can see · 4 you can touch · 3 you can hear · 2 you can smell · 1 you can taste</div>')
            + box("Box breathing", '<div class="small" style="margin-top:3pt">Breathe in for 4 · hold for 4 · out for 4 · hold for 4. Repeat 4 times.</div>')
            + box("If I'm in crisis", '<div class="small">Who I will contact, and my local emergency or crisis number:</div>' + lines(2))
            + '<div class="small" style="margin-top:6pt">These worksheets are a self-help tool and don\'t replace support from a doctor or therapist.</div></div>')
    wins = ('<div class="pg"><div class="sub"><h1>Wins & Kind Words</h1><span></span></div>' + tbl(["Date", "Something I did well, or something kind someone said"], ["14%", ""], 22, 26) + '</div>')
    return [rec, rec, rec, worry, worry, mood, wins, cope]

def advent():
    acts = ["Write a letter to Santa", "Make paper snowflakes", "Watch a Christmas film with popcorn", "Bake gingerbread", "Make a bird feeder", "Go on a Christmas lights walk", "Donate a toy or tin of food",
            "Make a paper chain", "Read a Christmas story in bed", "Have hot chocolate with marshmallows", "Make a homemade card for a neighbour", "Christmas jumper day", "Build a blanket fort",
            "Make salt dough decorations", "Sing carols", "Do a Christmas jigsaw", "Make reindeer food", "Have a family games night", "Write a thank-you note to a teacher", "Decorate cookies",
            "Make a pine cone ornament", "Have a Christmas picnic indoors", "Wrap a present for someone", "Leave out treats for Santa"]
    def card(n, t): return (f'<div style="border:1.5pt dashed #c9c9c9;border-radius:8pt;padding:6pt;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center">'
                            f'<div style="font-size:24pt;font-weight:800;color:var(--c)">{n}</div><div style="font-size:9.5pt;margin-top:3pt">{t}</div></div>')
    pages = [f'<div class="pg"><div class="sub"><h1>Advent Activity Cards</h1><span>Days {k * 12 + 1}-{k * 12 + 12} · cut out</span></div><div style="display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(4,1fr);gap:8pt;flex:1">'
             + "".join(card(k * 12 + i + 1, acts[k * 12 + i]) for i in range(12)) + '</div></div>' for k in range(2)]
    blank = ('<div class="pg"><div class="sub"><h1>Make Your Own Cards</h1><span>Write your own ideas</span></div><div style="display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(4,1fr);gap:8pt;flex:1">'
             + "".join(card("__", "<br>" + "_" * 18 + "<br><br>" + "_" * 18) for _ in range(12)) + '</div></div>')
    cal = "".join(f'<div style="border:1.5pt solid #ddd;border-radius:6pt;height:78pt;padding:4pt;position:relative"><b style="color:var(--c)">{d}</b></div>' for d in range(1, 25))
    countdown = (f'<div class="pg"><div class="sub"><h1>Christmas Countdown</h1><span>Colour in or stick a sticker each day</span></div><div style="display:grid;grid-template-columns:repeat(6,1fr);gap:7pt;margin-top:4pt">{cal}</div>'
                 + row(box("Our favourite activity", lines(2)), box("Next year let's try", lines(2))) + '</div>')
    plan = ('<div class="pg"><div class="sub"><h1>Advent Planner</h1><span>For grown-ups</span></div><div class="small">Match activities to busy and free days so nothing is a stress.</div>'
            + tbl(["Day", "Date", "Activity", "Need to buy / prep", "Ready ✓"], ["7%", "10%", "", "26%", "9%"], 24, 22) + '</div>')
    shop = ('<div class="pg"><div class="sub"><h1>Supplies List</h1><span></span></div><div class="cols" style="flex:1"><div class="grow">'
            + box("Crafts", items(["Coloured paper & card", "Glue & tape", "Glitter & stickers", "Pine cones", "Ribbon & string", "Salt, flour (salt dough)", "Paint & brushes", ""]))
            + box("Baking", items(["Gingerbread ingredients", "Cookie cutters", "Icing & sprinkles", "Hot chocolate", "Marshmallows", ""])) + '</div><div class="grow">'
            + box("Treats & extras", items(["Popcorn", "Christmas film list", "Story books", "Jigsaw", "Bird seed & lard", "Envelopes & stamps", "Food bank donations", ""]))
            + box("Notes", lines(6)) + '</div></div></div>')
    return [pages[0], pages[1], blank, countdown, plan, shop]

def familytree():
    def person(lbl, w="100%"): return (f'<div style="border:1.5pt solid #ccc;border-radius:8pt;padding:4pt 6pt;width:{w};box-sizing:border-box;background:#fff"><div class="small" style="color:var(--c);font-weight:700">{lbl}</div>'
                                       '<div style="border-bottom:1pt solid #ddd;height:14pt"></div><div class="small" style="margin-top:3pt">b. ________</div><div class="small" style="margin-top:3pt">d. ________</div></div>')
    gen = lambda labels: '<div style="display:flex;gap:6pt;justify-content:center">' + "".join(person(l) for l in labels) + '</div>'
    tree = ('<div class="pg"><div class="sub"><h1>Family Tree</h1><span>Four generations</span></div><div style="flex:1;display:flex;flex-direction:column;justify-content:space-around">'
            + gen(["Great-grandpa", "Great-grandma", "Great-grandpa", "Great-grandma", "Great-grandpa", "Great-grandma", "Great-grandpa", "Great-grandma"]).replace("width:100%", "width:12%")
            + gen(["Grandfather", "Grandmother", "Grandfather", "Grandmother"]).replace("width:100%", "width:23%")
            + gen(["Father", "Mother"]).replace("width:100%", "width:40%") + gen(["Me"]).replace("width:100%", "width:46%")
            + '</div><div class="small" style="text-align:center;margin-top:6pt">Fill in from the bottom up. Use one tree for each side of the family if you need more room.</div></div>')
    prof = ('<div class="pg"><div class="sub"><h1>Ancestor Profile</h1><span></span></div><div class="cols"><div class="box" style="flex:1;height:170pt"><b>Photo</b></div><div style="flex:1.5">'
            + lab("Full name (and maiden name)", 1) + lab("Born: date & place", 1) + lab("Died: date & place", 1) + lab("Parents", 1) + lab("Married: who, when, where", 1) + '</div></div>'
            + lab("Children", 2) + two(lab("Jobs & trades", 3), lab("Homes & places lived", 3)) + lab("Stories, character & memories", 6) + lab("Sources (records, people, documents)", 2) + '</div>')
    fam = ('<div class="pg"><div class="sub"><h1>Family Group Sheet</h1><span></span></div>' + two(box("Husband / partner", lines(5)), box("Wife / partner", lines(5)))
           + row(box("Married / together from", lines(1)), box("Where", lines(1)))
           + '<div class="lbl">Children</div>' + tbl(["Name", "Born", "Where", "Married to", "Died"], ["26%", "13%", "", "20%", "13%"], 10, 26) + lab("Notes", 4) + '</div>')
    res = ('<div class="pg"><div class="sub"><h1>Research Log</h1><span></span></div>' + tbl(["Date", "Looking for", "Where I searched", "What I found", "Next step"], ["10%", "18%", "20%", "", "20%"], 24, 26) + '</div>')
    interview = ('<div class="pg"><div class="sub"><h1>Family Interview</h1><span>Talking to: ______________ · Date: ______</span></div>'
                 + "".join(lab(q, n) for q, n in [("Where and when were you born? What was your home like?", 3), ("What do you remember about your parents and grandparents?", 3), ("What were your school days like?", 2),
                                                 ("What jobs did you and your family do?", 2), ("How did you meet your partner?", 2), ("What family traditions or recipes do you remember?", 2),
                                                 ("What was the biggest change you've seen in your life?", 2), ("Is there a story you'd like the family to remember?", 3)]) + '</div>')
    return [tree, tree, fam, fam, prof, prof, interview, res]

PRODUCTS = [("Birdwatching-Journal", "#2b8a3e", "#ebfbee", birds), ("Wine-Tasting-Journal", "#862e9c", "#f8f0fc", wine), ("Thought-Record-Worry-Journal", "#1971c2", "#e7f5ff", thoughts),
            ("Advent-Activity-Calendar", "#c92a2a", "#fff5f5", advent), ("Family-Tree-Worksheets", "#7c5e10", "#fdf8ec", familytree)]
