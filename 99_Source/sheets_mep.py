"""E-101 lighting and ceilings, E-102 power / AC / data, P-101 water supply and drainage."""
from collections import Counter
from sheetlib import *

LIGHTING = {"L", "WL", "F", "EF", "S", "BELL", "CAM", "GL"}
POWER = {"P", "PC", "P16", "U", "D", "TV", "AC", "ODU", "G", "DB", "INV", "MTR", "EP", "CH"}
ECOL = {"L": colors.HexColor("#C28A00"), "WL": colors.HexColor("#C28A00"), "F": ACC, "EF": ACC, "S": INK, "BELL": INK,
        "CAM": INK, "GL": colors.HexColor("#C28A00"), "P": BLUE, "PC": BLUE, "P16": RED, "U": colors.HexColor("#7B3FA0"),
        "D": colors.HexColor("#7B3FA0"), "TV": colors.HexColor("#7B3FA0"), "AC": RED, "ODU": RED, "G": RED, "DB": INK,
        "INV": colors.HexColor("#7B3FA0"), "MTR": INK, "EP": INK, "CH": RED}
CEILING_ITEMS = {"L", "F"}


def _sym(pl, code, x, y, col):
    c = pl.c; px, py = pl.p(x, y)
    c.setStrokeColor(col); c.setFillColor(WHITE); c.setLineWidth(0.6)
    if code in CEILING_ITEMS:
        c.circle(px, py, 2.0 * mm, stroke=1, fill=1)
        if code == "L":
            d = 1.4 * mm; c.line(px - d, py - d, px + d, py + d); c.line(px - d, py + d, px + d, py - d)
            return
    else:
        c.rect(px - 2.2 * mm, py - 1.6 * mm, 4.4 * mm, 3.2 * mm, stroke=1, fill=1)
    pl.s.note(code, px, py - 0.9 * mm, 4.3 if len(code) > 2 else 5, col, "Helvetica-Bold", "c")


def _base(pl, ceilings=False):
    pl.rect(0, SITE["l"], 0, SITE["w"], stroke=LIGHT, lw=0.5)
    if ceilings:
        for r in ROOMS:
            kind, v = CEILINGS[r[0]]
            pl.rect(r[2], r[3], r[4], r[5], stroke=None, fill=colors.HexColor("#EEF2F6") if kind == "flat" else colors.HexColor("#FBF5EA"))
            label = f"FC {fmt_ft(v)}" if kind == "flat" else "sloped"
            pl.text(label, r[2] + 0.3, r[4] + 0.5, 4.3, color=BLUE if kind == "flat" else BROWN, anchor="l")
    pl.walls(fill=colors.HexColor("#7A7A7A"))
    pl.openings(tags=False)
    pl.room_names(4.6, GREY, corner=True)


def _counts_table(s, codes, x, ytop, types, title):
    cnt = Counter(e[0] for e in ELECTRICAL if e[0] in codes)
    rows = [["Code", "Item", "Height", "No."]] + [[k, types[k][0], types[k][1], cnt[k]] for k in sorted(codes, key=lambda k: list(types).index(k)) if cnt[k]]
    return s.table(rows, [11, 46, 17, 8], x, ytop, title, 6)


def sheet_lighting(c):
    s = Sheet(c, "E-101", "Lighting, fans and ceilings", "1:75")
    pl = Plan(s, 75, 16 * mm, 104 * mm)
    _base(pl, ceilings=True)
    sx1, sx2, sy1, sy2 = ROOF["skylight"]
    pl.rect(sx1, sx2, sy1, sy2, stroke=GREY, lw=0.4, dash=(2, 2))
    for code, x, y, rid, note in ELECTRICAL:
        if code in LIGHTING: _sym(pl, code, x, y, ECOL[code])
    _counts_table(s, LIGHTING, 24 * mm, 66 * mm, ELEC_TYPES, "Lighting schedule")
    tips = [
        "Switchboards on the latch side of every door at 4 ft; 2-way switches at both bedroom beds and both ends of the hall.",
        "Bathroom switches outside the door; geyser switch with indicator lamp outside too.",
        "Fans at least 7 ft clear of the floor; long downrods in sloped ceilings; fan hooks cast or bolted, never in false ceiling board.",
        "Warm 2700-3000 K light in living and bedrooms, 4000 K in kitchen and offices; no downlights directly over the bed head.",
        "False ceilings (blue) with 50 mm insulation above; access panel near every light cluster and near AC pipe runs.",
        "Lights, fans, office sockets and router on the inverter circuit; outdoor lights on a timer or photocell.",
    ]
    s.bullets(tips, 120 * mm, 66 * mm, 205 * mm, 6.6, title="Lighting and ceiling notes")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    c.showPage()


def sheet_power(c):
    s = Sheet(c, "E-102", "Power, AC and data", "1:75")
    pl = Plan(s, 75, 16 * mm, 104 * mm)
    _base(pl)
    for code, x, y, rid, note in ELECTRICAL:
        if code in POWER: _sym(pl, code, x, y, ECOL[code])
    _counts_table(s, POWER, 24 * mm, 66 * mm, ELEC_TYPES, "Power schedule")
    tips = [
        "Separate MCB circuit for each AC, geyser, kitchen power, washing machine and pump; RCCB 30 mA on all socket circuits.",
        "AC: 16 A socket at 7'-6\", 65 mm sleeve sloping out, drain pipe to a gully (not onto the wall); ODUs on shaded north / west walls on brackets.",
        "AC indoor units never above the bed head or desk chair: cold draught on the head is the common complaint.",
        "Work desks (Office 2, Bedroom 2): 2 x UPS sockets + data + 1 normal socket at desk height; Cat6 from the router to the TV and both desks.",
        "Kitchen: 5-6 counter sockets at 42 in, 16 A for the fridge, chimney and microwave / OTG; none within 2 ft of the sink.",
        "DB on the dining face of Bedroom 2's east wall (central, dry) with 25% spare ways; meter at the gate; 2 earth pits; surge protector.",
        "Empty 25 mm conduits from the roof (solar PV), gate (CCTV, bell, intercom) and sump (pump controller) to the DB.",
    ]
    s.bullets(tips, 120 * mm, 66 * mm, 205 * mm, 6.6, title="Power notes")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    c.showPage()


PIPE_STYLE = {"supply": (BLUE, None, 0.8, "Water supply (CPVC), from overhead tank"),
              "soil": (BROWN, None, 1.0, "Soil line (uPVC 110 mm) to septic tank"),
              "grey": (ACC, (3, 1.5), 0.9, "Grey water (uPVC 75 mm) to soak trench"),
              "rain": (colors.HexColor("#5AA0D8"), (1, 1.2), 0.8, "Rainwater to sump filter / recharge pit")}


def sheet_plumbing(c):
    s = Sheet(c, "P-101", "Water supply and drainage", "1:100")
    pl = Plan(s, 100, 40 * mm, 118 * mm)
    site_context(pl)
    pl.walls(fill=colors.HexColor("#7A7A7A"))
    pl.openings(tags=False)
    pl.room_names(4.2, GREY, corner=True)
    site_features(pl, size=4.5)
    for kind, pts in PIPES:
        col, dash, lw, _ = PIPE_STYLE[kind]
        pl.poly(pts, lw=lw, color=col, dash=dash)
    for dx, dy in ROOF["downpipes"]:
        pl.circle(dx, dy, 0.3, lw=0.5, color=PIPE_STYLE["rain"][0], fill=WHITE)
    for code, x, y, rid, note in PLUMBING:
        px, py = pl.p(x, y); cc = c
        col = BROWN if code in ("WC", "IC") else (ACC if code in ("FT", "GT") else BLUE)
        cc.setStrokeColor(col); cc.setFillColor(WHITE); cc.setLineWidth(0.5)
        if code in ("IC", "GT"):
            cc.rect(px - 1.8 * mm, py - 1.8 * mm, 3.6 * mm, 3.6 * mm, stroke=1, fill=1)
        else:
            cc.circle(px, py, 1.7 * mm, stroke=1, fill=1)
        s.note(code, px, py - 0.8 * mm, 3.8, col, "Helvetica-Bold", "c")
        if code == "IC": s.note(note.split()[0], px + 2.2 * mm, py + 1.2 * mm, 4, BROWN)
    def sw(kind):
        col, dash, lw, _ = PIPE_STYLE[kind]
        return lambda x, y: (c.setStrokeColor(col), c.setLineWidth(lw * 1.4), c.setDash(list(dash), 0) if dash else c.setDash(), c.line(x, y, x + 6 * mm, y), c.setDash())
    y = s.legend([(sw(k), v[3]) for k, v in PIPE_STYLE.items()], 40 * mm, 66 * mm)
    codes = sorted({p[0] for p in PLUMBING}, key=lambda k: list(PLUMB_TYPES).index(k))
    cnt = Counter(p[0] for p in PLUMBING)
    rows = [["Code", "Item", "No."]] + [[k, PLUMB_TYPES[k], cnt[k]] for k in codes]
    s.table(rows, [11, 46, 8], 120 * mm, 70 * mm, "Fixtures and points", 6)
    tips = [
        "Overhead tank feeds by gravity; isolation valve for each bathroom and the kitchen, outside the room.",
        "Supply pipes run on the outside of walls in clamps or shallow chases, never under the floor slab.",
        "Soil and grey water kept separate; inspection chamber at every bend and junction; 1:40 falls on 110 mm, 1:30 on 75 mm.",
        "Grease trap before the kitchen line joins anything; vent pipe from each WC stack above the eaves.",
        "Soak trench and septic in the north strip, 6 ft+ from walls: wet black cotton soil swells and cracks the house.",
        "Rain from both gutters to the sump through a first-flush filter; overflow to a recharge pit.",
        "Test the bore / supply water: RO for drinking, softener for bathrooms if hardness is high; matt or PVD fittings.",
    ]
    s.bullets(tips, 205 * mm, 74 * mm, 125 * mm, 6.4, title="Plumbing notes")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    c.showPage()
