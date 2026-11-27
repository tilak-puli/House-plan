"""E-101 lighting and ceilings, E-102 power / AC / data, P-101 water supply and drainage."""
from collections import Counter
from sheetlib import *

LIGHTING = {"L", "WL", "F", "EF", "S", "BELL", "CAM", "GL", "SA", "HA", "LS", "FL", "PA", "SND"}
POWER = {"P", "PC", "P16", "U", "D", "TV", "AC", "ODU", "G", "DB", "INV", "MTR", "EP", "CH"}
ECOL = {"L": colors.HexColor("#C28A00"), "WL": colors.HexColor("#C28A00"), "F": ACC, "EF": ACC, "S": INK, "BELL": INK,
        "CAM": INK, "GL": colors.HexColor("#C28A00"), "P": BLUE, "PC": BLUE, "P16": RED, "U": colors.HexColor("#7B3FA0"),
        "D": colors.HexColor("#7B3FA0"), "TV": colors.HexColor("#7B3FA0"), "AC": RED, "ODU": RED, "G": RED, "DB": INK,
        "INV": colors.HexColor("#7B3FA0"), "MTR": INK, "EP": INK, "CH": RED, "SA": RED, "HA": RED, "LS": colors.HexColor("#C28A00"),
        "FL": colors.HexColor("#E08A00"), "PA": RED, "SND": RED}   # FL: low motion footlights (amber); PA and SND: the Group B pull-cord alarms and their sounders
CEILING_ITEMS = {"L", "F"}


def _hits(b, boxes):
    return any(b[0] < q[1] and b[1] > q[0] and b[2] < q[3] and b[3] > q[2] for q in boxes)


def _sym_spots(codes, x_max=72):
    """Where each point's symbol goes: where two would overlap, the later one moves just clear of the others (schematic: the
    point stays where the data has it). (code, x, y, sx, sy, box) for every point drawn on this sheet."""
    placed, out = [], []
    for code, x, y, rid, note in ELECTRICAL:
        if code not in codes or x > x_max:
            continue
        hw, hh = (0.5, 0.5) if code in CEILING_ITEMS else (0.56, 0.42)
        spot = None
        for dx, dy in ((0, 0), (0, 0.9), (0, -0.9), (1.15, 0), (-1.15, 0), (1.15, 0.9), (-1.15, 0.9), (1.15, -0.9), (-1.15, -0.9), (0, 1.8), (0, -1.8)):
            b = (x + dx - hw, x + dx + hw, y + dy - hh, y + dy + hh)
            if not _hits(b, placed):
                spot = (x + dx, y + dy, b); break
        sx, sy, b = spot or (x, y, (x - hw, x + hw, y - hh, y + hh))
        out.append((code, x, y, sx, sy, b))
        placed.append(b)
    return out


def _place_syms(pl, codes, x_max=72):
    """Draw each point's symbol at its spot (_sym_spots), with a short leader back to its true position where it moved."""
    placed = []
    for code, x, y, sx, sy, b in _sym_spots(codes, x_max):
        if (sx, sy) != (x, y):
            pl.line(x, y, sx, sy, lw=0.3, color=ECOL[code])
            pl.circle(x, y, 0.08, lw=0.3, color=ECOL[code], fill=ECOL[code])
        _sym(pl, code, sx, sy, ECOL[code])
        placed.append(b)
    return placed


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


def _base(pl, ceilings=False, codes=()):
    # (no plot outline here: it falls outside the sheet at 1:75)
    if ceilings:
        for r in ROOMS:
            kind, v = CEILINGS[r[0]]
            if kind == "open":  # open to the sky: no ceiling
                continue
            pl.rect(r[2], r[3], r[4], r[5], stroke=None, fill=colors.HexColor("#EEF2F6") if kind == "flat" else colors.HexColor("#FBF5EA"))
    syms = [(x - 0.65, x + 0.65, y - 0.5, y + 0.5) for _, x, y, *_r in ELECTRICAL] + [b for *_r, b in _sym_spots(codes)]   # true points and drawn symbols
    notes = []
    if ceilings:   # the ceiling note in a free corner of each room: clear of the symbols
        for r in ROOMS:
            kind, v = CEILINGS[r[0]]
            if kind == "open":
                continue
            label = (f"SLAB {fmt_ft(v)}" if r[0] in SLAB_CEILINGS else f"FC {fmt_ft(v)}") if kind == "flat" else "sloped"
            w = pl.c.stringWidth(label, "Helvetica", 4.3) / pl.k + 0.1
            x1, x2, y1, y2 = r[2] + 0.3, r[3] - 0.3, r[4] + 0.3, r[5] - 0.3
            for lx, ly in ((x1, y1 + 0.2), (x2 - w, y1 + 0.2), (x1, y2 - 0.5), (x2 - w, y2 - 0.5), (x1, (y1 + y2) / 2), (x2 - w, (y1 + y2) / 2)):
                b = (lx, lx + w, ly - 0.15, ly + 0.45)
                if not _hits(b, syms) and not _hits(b, notes):
                    break
            else:
                lx, ly = x1, y1 + 0.2; b = (lx, lx + w, ly - 0.15, ly + 0.45)
            notes.append(b)
            pl.text(label, lx, ly + 0.15, 4.3, color=BLUE if kind == "flat" else BROWN, anchor="l")
    pl.walls(fill=colors.HexColor("#7A7A7A"))
    pl.openings(tags=False)
    pl.floor_extras()
    pl.room_names(4.6, GREY, corner=True, avoid=syms + notes)   # clear of the symbols and the ceiling notes


def _counts_table(s, codes, x, ytop, types, title):
    """Counts for the floor being drawn."""
    cnt = Counter(e[0] for e in ELECTRICAL if e[0] in codes)
    rows = [["Code", "Item", "Height", "No."]] + [[k, types[k][0], types[k][1], cnt[k]] for k in sorted(codes, key=lambda k: list(types).index(k)) if cnt[k]]
    return s.table(rows, [11, 38, 13, 8], x, ytop, title, 6)   # narrow: it sits beside the house, left of the title block


def sheet_lighting(c, num="E-101", title="Lighting, fans and ceilings"):
    s = Sheet(c, num, title, "1:75")
    pl = Plan(s, 75, -33 * mm, 74 * mm)  # the 42 x 42 ring (x 15-57), its back garden and the thinnai fit the sheet, left of the schedule
    _base(pl, ceilings=True, codes=LIGHTING)
    _place_syms(pl, LIGHTING)   # forecourt, gate and car-porch points (x > 72) fall off this sheet (still counted)
    _counts_table(s, LIGHTING, 262 * mm, 118 * mm, ELEC_TYPES, "Lighting schedule")
    tips = [
        "Switchboards on the latch side of every door at 4 ft; 2-way switches at both bedsides, both ends of the stair and the stair-foot lobby.",
        "Bathroom switches (light, fan, geyser with an indicator lamp) outside the door, in the room the door opens from; none inside a wet room.",
        "Fans at least 7 ft clear of the floor; fan hooks cast or bolted, never in false ceiling board. The terrace and thinnai fans and lights are wet-rated, hung from the canopy steelwork and rafters.",
        "Exhaust fans go through OUTER walls only (the upper pane of each bath window). The powder room has no outer wall: its fan is ducted about 13 ft through the utility's ceiling void and down a short boxed bulkhead to a hooded louvre cowl (EF, R13) on the south wall centred over the service door D18, its centre 8'-3\" above the floor between the lintel band and the ring beam, with a 50 mm drip lip, the hood turned down and away from the door's louvred top; 4 ft from the utility window; non-return damper.",
        "Layered, warm light: in the living rooms and bedrooms most evening light comes from lamps on switched lamp sockets (LS) wired to the door switch, the ceiling lights dimmable; 2700 K there, 4000 K in the kitchen; no downlights over the bed head.",
        "Group B: low 1 ft motion footlights (FL, amber) on the master's bed-to-bath route, in the bath, along the stair and at the foyer step; pull-cord alarms (PA) by the WC and in the shower of the master and den baths, with sounders (SND) in the kitchen and the den.",
        "Interlinked smoke alarms at the stair foot and stair head and in the master, the den and Bedroom 2, a heat alarm in the kitchen; false ceilings (blue) with 50 mm insulation above, an access panel near every light cluster and AC pipe run.",
        f"The living has no false ceiling: its ceiling is the roof terrace slab's plastered soffit at {fmt_lvl(floor_level('R16') + CEILINGS['R16'][1])} ({fmt_ft(CEILINGS['R16'][1])} clear), so its conduits, light boxes and fan hook are cast into the slab.",
        "Lights, fans, the study sockets and the router on the inverter circuit; outdoor lights on a timer or photocell.",
    ]
    s.bullets(tips, 24 * mm, 80 * mm, 215 * mm, 6.6, title="Lighting and ceiling notes")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    c.showPage()


def sheet_power(c, num="E-103", title="Power, AC and data"):
    s = Sheet(c, num, title, "1:75")
    pl = Plan(s, 75, -33 * mm, 74 * mm)
    _base(pl, codes=POWER)
    _place_syms(pl, POWER)   # meters, workshop and shop points (x > 72) fall off this sheet (still counted)
    _counts_table(s, POWER, 262 * mm, 118 * mm, ELEC_TYPES, "Power schedule")
    tips = [
        "Separate MCB circuit for each AC, geyser, kitchen power, washing machine and pump; RCCB 30 mA on all socket circuits.",
        "AC in five rooms: the master, the den, Bedroom 2, the family room and the upstairs family room. 16 A socket at 7'-6\", 65 mm sleeve sloping out, drain pipe to a gully (not onto the wall). ODUs on west walls under a louvred sun-hood with 1 m clear in front, where the room has a west or south wall; the den, family room and upstairs family room have only north walls, so their units go on the north wall in the coolest shade; none on the courtyard side or the east front, none stacked over another.",
        "AC indoor units never above the bed head or the desk chair: cold draught on the head is the common complaint.",
        f"The inverter and its LiFePO4 battery stand in an IP54 heat-shielded, ventilated steel box on the OUTSIDE face of the kitchen's south wall ({fmt_ft(next(e[1] for e in both('ELECTRICAL') if e[0] == 'INV') - RING[1])} east of the utility / kitchen wall), under the eave, 3.5 ft or more from every door, window and fan terminal and clear of the service landing: a battery fault stays outside the house, away from every bedroom exit and the stair. Its cable runs through a 50 mm sleeve to the DB.",
        "Kitchen: 4 counter sockets at 42 in, 16 A for the fridge, chimney and microwave / OTG, none within 2 ft of the sink.",
        "Main DB in a lockable teak cabinet in the DB and linen cupboard R48 (central, dry, 25 % spare ways), with a sub-board on the upstairs gallery's east wall; meter at the gate; 2 earth pits 3 m apart in the back garden; surge protector.",
        "Empty 25 mm conduits from the roof (solar PV), gate (CCTV, bell, intercom) and sump (pump controller) to the DB.",
    ]
    s.bullets(tips, 24 * mm, 80 * mm, 215 * mm, 6.6, title="Power notes")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    c.showPage()


PIPE_STYLE = {"supply": (BLUE, None, 0.8, "Water supply (CPVC): sump pump to the terrace tank, then down"),
              "soil": (BROWN, None, 1.0, "Soil line (uPVC 110 mm) to septic tank"),
              "grey": (ACC, (3, 1.5), 0.9, "Grey water (uPVC 75 mm) to the soak pit"),
              "rain": (colors.HexColor("#5AA0D8"), (1, 1.2), 0.8, "Rainwater to the sump through the first-flush filter, overflow to the recharge pit")}


# notes quote dimensions from a named wall face or boundary, never model coordinates
_out_w = lambda x: f"{fmt_ft(HX1 - T / 2 - x)}"                                              # out from the west wall's outer face
_out_s = lambda y: f"{fmt_ft(HY1 - T / 2 - y)}"                                              # out from the south wall's outer face
_out_n = lambda y: f"{fmt_ft(y - HY2 - T / 2)}"                                              # out from the north wall's outer face
_east = lambda x: f"on a line {fmt_ft(x - HX2 - T / 2)} east of the house's east wall"
_south_b = lambda y: f"on a line {fmt_ft(y)} north of the south boundary"


def sheet_plumbing(c):
    s = Sheet(c, "P-101", "Water supply and drainage", "1:150")
    pl = Plan(s, 150, 12 * mm, 160 * mm)  # 1:150: the whole 130 ft plot fits, so the sump, the septic tank, the soak pit and the recharge pit show beside the house
    site_context(pl, x_end=PLOT_X2)
    pl.walls(fill=colors.HexColor("#7A7A7A"))
    pl.openings(tags=False)
    k150 = pl.k
    pts = PLUMBING + PLUMBING_F1
    pboxes = [(x - 0.95, x + 0.95, y - 0.95, y + 0.95) for _, x, y, *_r in pts]          # the fixture symbols (1.7-1.8 mm) at 1:150
    pboxes += [(x + 1.05, x + 1.05 + c.stringWidth(n.split()[0], "Helvetica", 4.3) / k150, y + 0.5, y + 1.3) for code, x, y, _r, n in pts if code == "IC"]   # chamber names
    pl.stair()
    site_features(pl, size=4.5, x_end=PLOT_X2 + 1, skip=("JASMINE", "FEET", "TULSI", "PARIJAT", "PATH", "SPIRAL", "BANANA", "HERBS", "VEG", "GUILD", "WORKSHOP", "WVERANDAH", "SHOPS", "SHOP1", "SHOP2", "SITEWC", "COMPOST", "WORM", "FENCE", "CARPORT", "PATH2", "DRIVE", "GATE", "BORE", "HEDGE1"))   # small garden labels would sit on the pipe symbols
    pl.text("First-floor fixtures shown over the rooms below", 15, -2.6, 4.4, color=GREY)
    for kind, pts in PIPES:
        col, dash, lw, _ = PIPE_STYLE[kind]
        pl.poly(pts, lw=lw * (1.8 if PIPE_MM.get((kind, pts[0])) == 150 else 1), color=col, dash=dash)
    xlabels = []
    for n, (cx, cy, lo, up, _n) in enumerate(PIPE_CROSSINGS, 1):      # every plan crossing: the deeper pipe (soil lowest) runs below, 150 mm clear
        pl.line(cx - 0.6, cy - 0.6, cx + 0.6, cy + 0.6, lw=0.6, color=RED); pl.line(cx - 0.6, cy + 0.6, cx + 0.6, cy - 0.6, lw=0.6, color=RED)
        w = c.stringWidth(f"X{n}", "Helvetica", 4.3) / k150
        for dx, dy in ((0.8, 0.5), (-0.8 - w, 0.5), (0.8, -1.1), (-0.8 - w, -1.1), (0.8, 1.4), (-0.8 - w, 1.4), (1.8, 0.5), (-1.8 - w, 0.5), (0.8, -2.0), (-0.8 - w, -2.0)):
            b = (cx + dx, cx + dx + w, cy + dy - 0.3, cy + dy + 0.75)
            if not any(b[0] < q[1] and b[1] > q[0] and b[2] < q[3] and b[3] > q[2] for q in pboxes + xlabels):
                break
        else:
            dx, dy = 0.8, 0.5; b = (cx + dx, cx + dx + w, cy + dy - 0.3, cy + dy + 0.75)
        xlabels.append(b)
        pl.text(f"X{n}", cx + dx, cy + dy, 4.3, color=RED, anchor="l")   # 1.5 mm+ (it was 1.13 mm)
    # supply equipment (the pump and tank have symbols below; these labels name them and the riser foot)
    pl.text("PUMP", 70.0, 52.0, 4.6, "Helvetica-Bold", BLUE, "l")
    pl.text("TANKS 2 x 500 L on the terrace NW (R37), riser duct on the north wall", 36.0, 52.0, 4.3, "Helvetica-Bold", BLUE, "l")
    pl.circle(35.5, 47.2, 0.5, lw=0.6, color=BLUE, fill=WHITE)
    pl.text("ISOLATION VALVE + RISER FOOT", 34.5, 50.8, 4.3, "Helvetica-Bold", BLUE, "r")
    placed = list(xlabels)
    for code, x, y, rid, note in PLUMBING + PLUMBING_F1:
        sx, sy = x, y   # a symbol that would sit on another moves just clear, with a leader to its true point
        for dx, dy in [(0, 0)] + [(r * ux, r * uy) for r in (1.9, 3.0, 3.8) for ux, uy in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1))]:
            b = (x + dx - 0.9, x + dx + 0.9, y + dy - 0.9, y + dy + 0.9)
            if not _hits(b, placed):
                sx, sy = x + dx, y + dy; break
        placed.append((sx - 0.9, sx + 0.9, sy - 0.9, sy + 0.9))
        if (sx, sy) != (x, y):
            pl.line(x, y, sx, sy, lw=0.3, color=GREY)
        px, py = pl.p(sx, sy); cc = c
        col = BROWN if code in ("WC",) or (code == "IC" and note.startswith("IC-") and " soil" in note[:12]) else (ACC if code in ("FT", "GT") or (code == "IC" and note.startswith("IC-")) else BLUE)
        cc.setStrokeColor(col); cc.setFillColor(WHITE); cc.setLineWidth(0.5)
        if code in ("IC", "GT"):
            cc.rect(px - 1.8 * mm, py - 1.8 * mm, 3.6 * mm, 3.6 * mm, stroke=1, fill=1)
        else:
            cc.circle(px, py, 1.7 * mm, stroke=1, fill=1)
        s.note(code, px, py - 0.85 * mm, 4.3, col, "Helvetica-Bold", "c")
        if code == "IC":   # the chamber's name beside it, on a free side
            nm = note.split()[0]; w = c.stringWidth(nm, "Helvetica", 4.3) / k150
            for dx, dy in ((1.05, 0.55), (-1.05 - w, 0.55), (1.05, -1.2), (-1.05 - w, -1.2), (-w / 2, 1.1), (-w / 2, -1.7), (1.05, 1.5), (-1.05 - w, 1.5), (1.05, -2.2), (-1.05 - w, -2.2)):
                b = (sx + dx, sx + dx + w, sy + dy, sy + dy + 0.75)
                if not _hits(b, placed):
                    break
            placed.append(b)
            s.note(nm, pl.p(sx + dx, 0)[0], pl.p(0, sy + dy)[1] + 0.3 * mm, 4.3, col)
    # room names last, clear of every symbol, chamber name and crossing tag where they finally sit (the walkways: the court label says it)
    pl.room_names(4.3, GREY, corner=True, skip=("R51", "R61", "R62", "R63"), avoid=placed, drop_blocked=True, min_size=4.3)
    def sw(kind):
        col, dash, lw, _ = PIPE_STYLE[kind]
        return lambda x, y: (c.setStrokeColor(col), c.setLineWidth(lw * 1.4), c.setDash(list(dash), 0) if dash else c.setDash(), c.line(x, y, x + 6 * mm, y), c.setDash())
    y = s.legend([(sw(k), v[3]) for k, v in PIPE_STYLE.items()], 24 * mm, 146 * mm)
    codes = sorted({p[0] for p in PLUMBING + PLUMBING_F1}, key=lambda k: list(PLUMB_TYPES).index(k))
    cnt = Counter(p[0] for p in PLUMBING + PLUMBING_F1)
    rows = [["Code", "Item", "No."]] + [[k, PLUMB_TYPES[k], cnt[k]] for k in codes]
    s.table(rows, [11, 46, 8], 120 * mm, 148 * mm, "Fixtures and points", 6)
    tips = [
        f"Supply: the sump pump (north of the forecourt, 2 ft off the boundary) lifts to two interconnected 500 L tanks on a 3 ft galvanised steel stand along the terrace's north parapet at its north-west corner, under the canopy's shade and behind the north jali parapet (not in a roof void); the rising main runs along the north strip ({_out_n(47.2)} outside the north wall) to a riser duct on the north wall; a pressure pump takes the showers; downfeed branches run in the wall chases (not drawn), an isolation valve for each bathroom and the kitchen, outside the room. Supply never runs under the floor slab.",
        f"Crossings (red X1 to X{len(PIPE_CROSSINGS)} on the plan): at every one the deeper pipe runs below with 150 mm clear (soil lowest, then septic effluent, bath grey, kitchen grey, rain, supply on top) and the upper pipe is sleeved across. The supply stays 3 ft+ from any soil or grey line it runs alongside; every pipe stays 3 ft+ from every tree trunk.",
        f"Soil and grey water kept separate; inspection chambers at every bend and junction, no two within 2 ft, at most 40 ft apart. West strip lanes, measured out from the west wall's outer face: rain {_out_w(5.6)}, grey {_out_w(7.6)}, soil {_out_w(13.6)} ({_out_w(11.0)} beside the engawa deck), clear of the airer. South strip (3.6 ft wide), out from the south wall's outer face: kitchen grey {_out_s(1.2)}, soil {_out_s(2.0)}, bath grey {_out_s(2.8)}, that run concrete-encased past the footings: the structural engineer approves the trench-to-footing distance. Closed pipes of this strip pass 0.5 to 0.9 m from the LPG cage (sleeved); no chamber is within 1.5 m of it. 1:40 falls on 110 mm, 1:30 on 75 mm.",
        f"Every WC has a rodding eye at its head and leaves through the nearest outer wall: Bedroom 2's WC straight out of the west wall into a boxed duct; the den bath's WC out of the north wall; the upper toilet has its OWN stack, straight down the boxed chase in the den bath's north-west corner and out through the north wall (no horizontal run in the sunk slab); the master (11.6 ft) and powder room (8.3 ft) WCs each in one unjointed length under the slab to the south wall. The soil runs west and south round the house and east along the south strip, then north {_east(74.4)} and east {_south_b(18.6)} to the septic inlet (west face).",
        f"Septic effluent leaves the tank's EAST face, opposite the inlet, and runs south {_east(90.0)}, west {_south_b(13.4)}, then south {_east(78.0)} to the soak pit's top, 3 ft+ from every tree. The pit also takes the bath and powder-room grey water and the washing machine. Kitchen sink, utility sink and the dining hand basin (flush rodding eye at the kitchen / dining wall) pass the grease trap ({_out_s(1.2)} out from the kitchen's south wall, below its sink) and run along the strip's outer lane (1.2 ft below the pit, sleeved there: the south strip allows no more) to the banana circle. Kitchen and effluent lines never join.",
        f"Rain: seven roof downpipes, the thinnai's two rain chains, the terrace outlet and the CD drain run to the first-flush chamber FF and the sump; the trunk from RIC-8 to FF and the sump overflow are 150 mm. Overflow from the sump goes south {_east(92.0)} and east {_south_b(14.5)} to the recharge pit (rodding eyes at each end of the workshop's paver verandah, none under it). The CD trunk is sleeved in concrete under the north walkway and the family living, with a rodding eye (RE-1) in the north walkway.",
        f"Courtyard overflow, independent of the CD trunk: CD-2 (north-west), the standpipe 3 in above the court floor (below the walkway level) and the walkway gully run on their OWN line west, {fmt_ft(CT[3] - 28.5)} south of the courtyard's north edge, under the den walk-in and the stair to the west rain lane (rodding eyes at the court wall and in the den walk-in, unjointed lengths under 6 m). The scupper through the west walkway kerb is 5.5 in above the court floor, above the walkway level, and spills across the walkway to the gully.",
        "Tank: two interconnected 500 L tanks (1,000 L) on a 3 ft steel stand along the terrace's north parapet at the north-west corner, under the canopy's shade; overflow and washout run to the terrace outlet; the supply rises in its own duct on the north wall, 0.5 ft+ from the laundry grey duct. The upstairs washer and laundry sink drain down a boxed duct on the north wall to the west grey lane: never into the terrace outlet or a rain drain. The rinse shower and the foot-wash tap drain to gravel soakaways where they stand.",
        "Septic tank (sealed) south-east of the forecourt behind its hedge and a lined soak pit on the south side, 60 ft+ from the borewell (the borewell is about 47 ft from the tank's nearest edge: engineer to confirm); a vent pipe from each WC stack above the eaves. The roof downpipe positions follow the roof drawings (A-110).",
        "Test the bore / supply water: RO for drinking, softener for bathrooms if hardness is high; matt or PVD fittings.",
    ]
    used = s.bullets(tips, 205 * mm, 148 * mm, 126 * mm, 6.0, title="Plumbing notes")
    assert 148 * mm - used >= 12 * mm, "the plumbing notes run off the sheet"
    pl.north(PW - 105 * mm, 225 * mm)
    c.showPage()
