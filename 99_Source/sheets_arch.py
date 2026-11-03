import re
"""Architectural plan sheets: cover, design basis, site, plans, finishes, roof, schedules."""
from sheetlib import *


def sheet_cover(c, index):
    s = Sheet(c, "A-000", "Cover and sheet index", "-")
    s.note(PROJECT["name"], 20 * mm, PH - 40 * mm, 30, INK, "Helvetica-Bold")
    s.note("Pre-construction drawing set, " + PROJECT["location"], 20 * mm, PH - 52 * mm, 12, GREY)
    y = PH - 72 * mm
    s.note("Sheet index", 20 * mm, y, 12, INK, "Helvetica-Bold"); y -= 7 * mm
    for n, t, sc in index:
        s.note(n, 20 * mm, y, 9, ACC, "Helvetica-Bold"); s.note(t, 40 * mm, y, 9); s.note(sc, 128 * mm, y, 9, GREY); y -= 5.4 * mm
    y -= 5 * mm
    s.note("Project data", 20 * mm, y, 12, INK, "Helvetica-Bold"); y -= 7 * mm
    carpet = 0
    for fl in ("G", "F1"):
        with on_floor(fl):
            carpet += sum(clear_dims(r)[0] * clear_dims(r)[1] for r in ROOMS)
    data = [("Site", "Guntur, Andhra Pradesh; agricultural land (conversion to confirm)"),
            ("Plot", f"{PLOT_X2 - PLOT_X1:.0f}' deep (west to the east road), 27' wide at the back, 30' half-way, 40' at the road: about {plot_area():,.0f} sq ft; 8' kept behind the house, 109' of front land (forecourt, car porch, drive, vegetable garden, carpentry workshop)"),
            ("Built footprint", "53' x 22' = 1,166 sq ft ground floor; about 615 sq ft enclosed + 420 sq ft covered terrace on the first floor"),
            ("Carpet area", f"{carpet:,.0f} sq ft clear, both floors, incl. poomukham and terrace"),
            ("Construction", "Two-storey RCC frame, AAC walls, first-floor slab over the back half, steel-truss roofs with clay tiles"),
            ("Plinth", f"FFL {fmt_lvl(LEVELS['FFL'])} above finished ground")]
    for k, v in data:
        s.note(k, 20 * mm, y, 8.5, GREY); s.note(v, 52 * mm, y, 8.5); y -= 5.4 * mm
    x2 = 180 * mm; y = PH - 72 * mm
    s.note("Key design decisions", x2, y, 12, INK, "Helvetica-Bold"); y -= 4 * mm
    s.bullets(DECISIONS, x2, y, 140 * mm, 8)
    c.showPage()


def sheet_basis(c):
    s = Sheet(c, "A-001", "Design basis and general notes", "-")
    x1, x2, x3, w = 18 * mm, 125 * mm, 232 * mm, 98 * mm
    top = PH - 22 * mm
    site = [
        "<b>Heat:</b> summer days 40-45 C (March-June). Insulated roof, ventilated attic, shaded west and south walls, AC provisions.",
        "<b>Rain:</b> about 850-1000 mm a year, mostly June-October, with short cyclonic downpours in Oct-Nov. Deep eaves, gutters, drip grooves.",
        "<b>Wind:</b> coastal cyclone belt. Trusses bolted down; every edge tile clipped; no light sheeting that can lift.",
        "<b>Soil:</b> black cotton (expansive) soil is common. A soil test decides the foundation; keep water and trees away from the walls.",
        "<b>Earthquake:</b> seismic zone III. RCC frame with lintel and ring bands.",
        "<b>Water:</b> groundwater is often hard with high fluoride. RO for drinking, softener if needed, matt fittings.",
        "<b>Termites and mosquitoes:</b> anti-termite treatment before the plinth; mesh on every opening.",
        "<b>Land:</b> agricultural land. Confirm conversion and the permission route before work starts.",
    ]
    s.bullets(site, x1, top, w, title="Site conditions (Guntur)")
    levels = [["Level", "Above finished ground"],
              ["Finished ground (FGL)", fmt_lvl(LEVELS["FGL"])], ["Poomukham floor", fmt_lvl(LEVELS["poomukham"])],
              ["Wet area floor", fmt_lvl(LEVELS["wet_area"])], ["House floor (FFL)", fmt_lvl(LEVELS["FFL"])],
              ["Bathroom floors", fmt_lvl(LEVELS["FFL"] - LEVELS["bath_drop"]) + " (12 mm drop)"],
              ["Door head / lintel band", fmt_lvl(LEVELS["FFL"] + LEVELS["door_head"])],
              ["False ceilings (rooms)", fmt_lvl(LEVELS["FFL"] + LEVELS["false_ceiling"])],
              ["False ceilings (baths)", fmt_lvl(LEVELS["FFL"] + LEVELS["bath_ceiling"])],
              ["Ground ring beam / first-floor slab", fmt_lvl(LEVELS["FFL"] + LEVELS["wall_top"])],
              ["First floor (finished)", fmt_lvl(floor_base("F1"))],
              ["First-floor ring beam", fmt_lvl(upper_wall_top_z())],
              ["Front gable eaves / ridge", fmt_lvl(gable_eave_z()) + " / " + fmt_lvl(gable_ridge_z())],
              ["Main roof eaves (tile edge)", fmt_lvl(eave_z())], ["Main ridge", fmt_lvl(ridge_z())]]
    h = s.table(levels, [50, 45], x2, top - 4 * mm, "Levels and heights")
    walls = [["Type", "Build-up", "Where"]] + [[k, v[1], {"EXT": "Outer walls, kitchen north wall", "WET": "Walls with concealed plumbing", "INT": "Other inner walls"}[k]] for k, v in WALL_TYPES.items()]
    s.table(walls, [12, 50, 33], x2, top - h - 16 * mm, "Wall types")
    gen = [
        "Dimensions are to wall centrelines unless marked 'clear'. Clear room sizes are on A-106 (ground) and A-107 (first floor).",
        "Concrete, steel, foundations and member sizes are by the structural engineer. Column positions are not shown and must be coordinated with the furniture layout.",
        "AAC: 150 mm galvanised mesh over every block-concrete joint; chases cut by machine; no hammering.",
        "All external sills, sunshades and copings get drip grooves; every external opening gets mosquito mesh.",
        "Wet rooms: waterproofing on floors, 12 in up the walls and 7 ft in showers; 48 h flood test before tiling.",
        "Skirting is flush with the plaster (no dust ledge). Grout in wet areas is epoxy.",
        "Pipes and conduits are laid before plaster and photographed with a tape measure in view, for future drilling.",
        "Keep 3 ft paved apron around the house, sloped away. No gardens, soak pits or big trees within 6-8 ft of walls.",
        "Two storeys: columns, footings, the first-floor slab and the stair are designed by the engineer for two floors; RCC column stubs at the terrace edge take the steel roof posts.",
    ]
    s.bullets(gen, x3, top, w, title="General notes")
    rows = [["Stage", "Check before it is covered up", "Who"]] + [list(h) for h in HOLD_POINTS]
    s.table(rows, [40, 190, 50], x1, 128 * mm, "Hold points (stop and inspect)", 7)
    c.showPage()


def sheet_phasing(c):
    s = Sheet(c, "A-002", "Construction phasing (roof first, three stages)", "1:100")
    pale = colors.HexColor("#E3EFE8"); mid = colors.HexColor("#9A9A9A")
    with on_floor("F1"):
        pl = Plan(s, 100, 20 * mm - 11 * 0.3048 * 1000 / 100 * mm, 172 * mm)
        for r in ROOMS:
            if r[0] in PHASE2_ROOMS:
                pl.rect(r[2], r[3], r[4], r[5], stroke=None, fill=pale)
        for (x1, x2, y1, y2), wt in wall_rects(with_type=True):
            if x1 < 34.6 < x2 and x2 - x1 < 1 and y1 > 15:  # stair wall
                pl.rect(x1, x2, y1, y2, stroke=None, fill=INK)
            elif wt == "EXT":
                pl.rect(x1, x2, y1, y2, stroke=INK, fill=mid, lw=0.3)
            else:
                pl.rect(x1, x2, y1, y2, stroke=ACC, fill=WHITE, lw=0.6, dash=(1.5, 1))
        pl.openings(tags=False)
        pl.floor_extras()
        pl.room_names(5.2, INK)
        pl.text("STAGE 3 FIT-OUT (shaded)", 24, 9.0, 5, "Helvetica-Bold", ACC)
        pl.line(34.6, 15.9, 38.0, 15.9, lw=1.2, color=RED)
        pl.text("GRILLE GATE", 36.3, 14.7, 4.2, "Helvetica-Bold", RED)
        pl.north(218 * mm, 180 * mm)
    s.note("First floor through the stages: stair, frame, slab, roof and terrace in stage 1; outer walls (grey) in stage 2; inner walls and fit-out (green) in stage 3.", 20 * mm, 160 * mm, 7, GREY)
    def sw(fill, stroke=None, dash=None):
        def f(x, y):
            s.c.setFillColor(fill or WHITE); s.c.setStrokeColor(stroke or INK); s.c.setLineWidth(0.6)
            if dash: s.c.setDash(*dash)
            s.c.rect(x, y, 6 * mm, 2 * mm, stroke=1 if stroke else 0, fill=1); s.c.setDash()
        return f
    s.legend([(sw(INK), "Stage 1: stair walls (frame, slab, roof, terrace also stage 1)"), (sw(mid, INK), "Stage 2: outer walls and windows"),
              (sw(WHITE, ACC, (1.5, 1)), "Stage 3: inner walls and baths"), (sw(pale), "Stage 3 fit-out area"),
              (sw(RED), "Stage 1: grille gate at the stair head; temporary railings on open edges")], 20 * mm, 152 * mm)
    rows = [["Stage", "Scope", "Rough cost"]] + [[name, "<br/>".join("&bull; " + i for i in items), cost] for name, items, cost in PHASES]
    s.table(rows, [28, 72, 20], 205 * mm, 262 * mm, "Three stages, roof first")
    s.bullets(PHASE1_PROVISIONS, 20 * mm, 120 * mm, 150 * mm, 7, title="Build in stage 1 so the later stages are easy")
    s.bullets(PHASE1_LIVING, 180 * mm, 120 * mm, 145 * mm, 7, title="Living with stage 1")
    s.note("Rates are rough 2026 village rates around Guntur; get contractor quotes on the Quantities sheet. Structure, beams and sleeves by the structural engineer.", 20 * mm, 18 * mm, 7, GREY)
    c.showPage()


def sheet_site(c):
    s = Sheet(c, "A-101", "Site plan: the whole plot", "1:200")
    pl = Plan(s, 200, 30 * mm - PLOT_X1 * 304.8 / 200 * mm, 150 * mm)
    site_context(pl, x_end=PLOT_X2)
    x1, x2, y1, y2 = ROOF["hip"]
    pl.rect(14, 61, 3, 25, stroke=INK, fill=colors.HexColor("#BDBDBD"), lw=0.8)
    pl.rect(61, 67, 3, 25, stroke=INK, fill=colors.HexColor("#DADADA"), lw=0.6)
    pl.rect(x1, ROOF["gable"][1], y1, y2, stroke=INK, lw=0.3, dash=(3, 2))
    site_features(pl, size=4.4, x_end=PLOT_X2)
    pl.text("HOUSE", 40.5, 15.5, 7, "Helvetica-Bold")
    pl.text(f"FFL {fmt_lvl(LEVELS['FFL'])}", 40.5, 11.5, 5, color=GREY)
    for x, y, rr in TREES:
        pl.text("neem" if rr > 3 else "fruit tree", x, y - rr - 0.9, 3.8, color=colors.HexColor("#4F6E34"))
    yN = lambda x: plot_north(x)
    pl.hdim(PLOT_X1, 14, -3, "8'", 5); pl.hdim(14, 67, -3, "53' HOUSE", 5); pl.hdim(67, PLOT_X2, -3, f"{PLOT_X2 - 67:.0f}' FRONT LAND", 5)
    pl.hdim(PLOT_X1, PLOT_X2, -7, f"{PLOT_X2 - PLOT_X1:.0f}'-0\" PLOT (WEST BOUNDARY TO THE EAST ROAD)", 5.5)
    pl.vdim(0, yN(PLOT_X1), PLOT_X1 - 3, "27'", 5); pl.vdim(0, yN(91), 91, "30' (half-way)", 5); pl.vdim(0, yN(PLOT_X2), PLOT_X2 + 6, "40'", 5)
    pl.north(PW - 105 * mm, PH - 40 * mm)
    pl.scalebar(250 * mm, 118 * mm)
    notes = [f"{f[0]}: {f[1]}" for f in SITE_FEATURES if f[0] not in ("APRON", "STEPS", "GSTEP", "FEET", "WSTEP")]
    half = (len(notes) + 1) // 2
    s.bullets(notes[:half], 22 * mm, 92 * mm, 150 * mm, 6.0)
    s.bullets(notes[half:] + [f"Plot area about {plot_area():,.0f} sq ft; compound wall about {plot_perimeter():.0f} ft, the road face in exposed brick or local stone, the rest precast post-and-panel 5 ft.",
                              "Ground falls 1:100 away from the house and down the drive to the road; roof water to the recharge pit."], 178 * mm, 92 * mm, 150 * mm, 6.0)
    c.showPage()


def sheet_plan(c, num="A-102", title="Ground floor plan"):
    s = Sheet(c, num, title, "1:75")
    pl = Plan(s, 75, 16 * mm, 75 * mm)
    site_context(pl)
    pl.walls()
    pl.openings()
    pl.floor_extras()
    ground = FLOOR[0] == "G"
    if ground:
        sx1_, sx2_, sy1_, sy2_ = next(f[3] for f in SITE_FEATURES if f[0] == "STEPS")
        pl.rect(sx1_, (sx1_ + sx2_) / 2, sy1_, sy2_, lw=0.3); pl.rect((sx1_ + sx2_) / 2, sx2_, sy1_, sy2_, lw=0.3)
        pl.text("UP", (sx1_ + sx2_) / 2, (sy1_ + sy2_) / 2, 4.5)
    pl.room_names(6, INK, sub=lambda r: "{} x {}".format(*map(fmt_ft, room_dims(r))))
    pl.auto_dims()
    pl.north(PW - 105 * mm, PH - 40 * mm)
    pl.scalebar(32 * mm, 30 * mm)
    sw = lambda fill: (lambda x, y: s.c.setFillColor(fill) or s.c.rect(x, y, 6 * mm, 2 * mm, stroke=0, fill=1))
    s.legend([(sw(WALL_FILL[k]), f"{k}: {v[1]}") for k, v in WALL_TYPES.items()], 150 * mm, 44 * mm)
    s.note("Door swings dashed. D = door, W = window (A-401).", 32 * mm, 20 * mm, 7, GREY)
    s.note(("Section lines and clear sizes on A-106; levels on A-108." if ground else
            f"First floor at {fmt_lvl(floor_base('F1'))}. Railings 3'-6\" high (double lines). The front half is a covered terrace under the main roof, on steel posts."), 32 * mm, 16 * mm, 7, GREY)
    c.showPage()


def sheet_furniture(c, num="A-103", title="Furniture layout, ground floor"):
    s = Sheet(c, num, title, "1:75")
    pl = Plan(s, 75, 16 * mm, 75 * mm)
    site_context(pl)
    pl.walls(fill=colors.HexColor("#6B6B6B"))
    pl.openings(tags=False)
    pl.floor_extras()
    shapes = {f[0]: f[9] for f in FURNITURE}
    def draw(fid, x1, x2, y1, y2, label):
        sh = shapes[fid]
        if sh == "circle":
            pl.circle((x1 + x2) / 2, (y1 + y2) / 2, (x2 - x1) / 2, lw=0.5, color=ACC)
        elif sh == "wc":
            pl.rect(x1, x2, y1, y2, stroke=ACC, lw=0.5)
            pl.circle((x1 + x2) / 2 + 0.2, (y1 + y2) / 2, 0.45, lw=0.4, color=ACC)
        elif sh == "glass":
            pl.rect(x1, x2, y1, y2, stroke=ACC, lw=0.4, dash=(1.5, 1))
        else:
            pl.rect(x1, x2, y1, y2, stroke=ACC, lw=0.5, fill=colors.HexColor("#EEF4F0"))
        if label:
            big = (x2 - x1) * (y2 - y1) > 3
            pl.text(fid, (x1 + x2) / 2, (y1 + y2) / 2, 5 if big else 4, "Helvetica-Bold", ACC)
    for f in FURNITURE:
        draw(f[0], f[3], f[4], f[5], f[6], True)
    for fid, x1, x2, y1, y2 in EXTRA_DRAW:
        draw(fid, x1, x2, y1, y2, False)
    pl.room_names(5, GREY, corner=True)
    st = ParagraphStyle("l", fontName="Helvetica", fontSize=5.6, leading=6.6)
    short = lambda t: re.split(r" \(|: |; ", t)[0]  # key shows the item only; full specs are in the schedules
    rows = [[Paragraph(f"<b>{f[0]}</b>", st), Paragraph(short(f[2]) + (f" (x{f[7]})" if f[7] > 1 else ""), st)] for f in FURNITURE]
    n = 3; per = (len(rows) + n - 1) // n
    for i in range(n):
        t = Table(rows[i * per:(i + 1) * per], colWidths=[8 * mm, 58 * mm])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5), ("TOPPADDING", (0, 0), (-1, -1), 0.5)]))
        w, h = t.wrap(0, 0); t.drawOn(c, (118 + i * 70) * mm, 66 * mm - h)
    s.note("Furniture key (full specs in schedules)", 118 * mm, 68 * mm, 7, INK, "Helvetica-Bold")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    pl.scalebar(32 * mm, 30 * mm)
    c.showPage()


SECTIONS = {"A": ("X", 44.5, "Cross section through the dining nook, dining, living and the covered terrace above"),
            "B": ("Y", 18, "Long section through the master suites on both floors, the stair, the living with the covered terrace above, and the poomukham")}


def sheet_working(c, num="A-104", title="Working plan, ground floor: clear sizes and sections"):
    s = Sheet(c, num, title, "1:75")
    pl = Plan(s, 75, 16 * mm, 104 * mm)
    plot_outline(pl, SITE["l"] + 3, color=LIGHT, lw=0.5)
    pl.walls()
    pl.openings()
    pl.floor_extras()
    for r in ROOMS:
        rid, name, x1, x2, y1, y2, _ = r
        cx, cy = ROOM_LABEL_AT.get(rid, ((x1 + x2) / 2, (y1 + y2) / 2))
        L, W = clear_dims(r)
        small = (x2 - x1) <= 6
        pl.text(short_name(name).upper(), cx, cy + 0.6, 5 if small else 5.8, "Helvetica-Bold")
        pl.text(f"{fmt_ft(L)} x", cx, cy - 0.3, 4.6, color=ACC) if small else None
        pl.text(f"{fmt_ft(W)}" if small else f"{fmt_ft(L)} x {fmt_ft(W)} clear", cx, cy - (1.05 if small else 0.4), 4.6 if small else 5, color=ACC)
    for name, (axis, c0, _) in (SECTIONS.items() if FLOOR[0] == "G" else ()):
        if axis == "X":
            pl.line(c0, -2.5, c0, 28.5, lw=0.7, color=RED, dash=(6, 2, 1, 2))
            for yy, lab in ((-3.3, name), (29.2, name)):
                pl.circle(c0, yy, 0.8, lw=0.6, color=RED, fill=WHITE); pl.text(lab, c0, yy, 6.5, "Helvetica-Bold", RED)
        else:
            pl.line(10, c0, 72, c0, lw=0.7, color=RED, dash=(6, 2, 1, 2))
            for xx in (9.2, 72.8):
                pl.circle(xx, c0, 0.8, lw=0.6, color=RED, fill=WHITE); pl.text(name, xx, c0, 6.5, "Helvetica-Bold", RED)
    pl.auto_dims(5)
    s.note("Clear sizes are wall face to wall face after plaster (green). Grid dimensions are to wall centrelines.", 24 * mm, 32 * mm, 7, GREY)
    s.note("Sections A-A and B-B on A-301 (marked on the ground floor). Check every furniture item against the clear size before ordering.", 24 * mm, 27 * mm, 7, GREY)
    s.note("Column positions (by engineer) must avoid door swings, wardrobes and the TV wall.", 24 * mm, 22 * mm, 7, GREY)
    pl.north(PW - 105 * mm, PH - 40 * mm)
    pl.scalebar(200 * mm, 30 * mm)
    c.showPage()


FLOOR_COLOURS = {"Red oxide / Kota stone": "#E8C9B8", "Matt vitrified 2x2": "#E5E1D6", "Anti-skid ceramic, waterproofed": "#CFE0EC", "Flamed granite": "#DCD2C4",
                 "Terracotta anti-skid tile, waterproofed": "#E9B98F"}
FLOOR_GROUPS = [(k, colors.HexColor(v), [r for r, f in FLOOR_FINISH.items() if f == k]) for k, v in FLOOR_COLOURS.items()]


def sheet_finishes(c, num="A-105", title="Floor finishes and levels, ground floor"):
    s = Sheet(c, num, title, "1:75")
    pl = Plan(s, 75, 16 * mm, 104 * mm)
    plot_outline(pl, SITE["l"] + 3, color=LIGHT, lw=0.5)
    ids = {r[0] for r in ROOMS}
    for _, col, rooms in FLOOR_GROUPS:
        for rid in rooms:
            if rid in ids:
                r = room_of(rid); pl.rect(r[2], r[3], r[4], r[5], stroke=None, fill=col)
    pl.walls(fill=INK)
    pl.openings(tags=False)
    pl.floor_extras()
    for r in ROOMS:
        rid, name, x1, x2, y1, y2, _ = r
        cx, cy = ROOM_LABEL_AT.get(rid, ((x1 + x2) / 2, (y1 + y2) / 2))
        pl.text(short_name(name), cx, cy + 0.8, 5.2, "Helvetica-Bold")
        pl.level(cx - 1.2, cy - 0.6, floor_level(rid), 5)
    for rid, ang in (("R07", "1:60 to drain"), ("R08", "1:60 to drain"), ("R33", "1:60 to drain"), ("R39", "1:60 to drain"), ("R13", "1:80 to drain"), ("R37", "1:80 to spout")):
        if rid in ids:
            r = room_of(rid); pl.text("falls " + ang, (r[2] + r[3]) / 2, r[4] + 0.8, 4.4, color=BLUE)
    if FLOOR[0] == "G":
        pl.level(71, 9, LEVELS["FGL"], 5); pl.text("finished ground", 71, 8, 4.5, color=GREY)
    sw = lambda fill: (lambda x, y: s.c.setFillColor(fill) or s.c.setStrokeColor(GREY) or s.c.rect(x, y, 6 * mm, 3 * mm, stroke=1, fill=1))
    s.legend([(sw(col), name) for name, col, _ in FLOOR_GROUPS], 24 * mm, 64 * mm)
    tips = [
        "Skirting 4 in high, set flush with the plaster face (plaster stops in a groove above it), so no ledge collects dust.",
        "Bathrooms 12 mm below the bedroom floor with a sloped granite threshold: no raised step to trip on, water stays in.",
        "First floor: the upper bath and the covered terrace sit on the slab over ground-floor rooms: waterproof, flood-test 48 h, then tile.",
        "Shower zone: linear drain at the far end, floor falls 1:60 only inside the wet zone; dry zone floor nearly flat.",
        "Poomukham and steps: flamed or leather-finish stone. Polished granite is slippery when wet.",
        "Kitchen: mid-tone matt floor; white glossy tile shows every stain and is slippery with oil.",
        "Leave 5 mm expansion gaps at walls under the skirting and every 15-20 ft in large floors.",
    ]
    s.bullets(tips, 110 * mm, 66 * mm, 210 * mm, 6.8, title="Floor detailing")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    c.showPage()


def sheet_roof(c):
    s = Sheet(c, "A-110", "Roof plan", "1:75")
    pl = Plan(s, 75, 16 * mm, 104 * mm)
    plot_outline(pl, SITE["l"] + 3, color=LIGHT, lw=0.5)
    pl.rect(14, 67, 3, 25, stroke=GREY, lw=0.4, dash=(2, 2))
    x1, x2, y1, y2 = ROOF["hip"]
    w = (y2 - y1) / 2; yc = (y1 + y2) / 2
    gx1, gx2, ya, yb = ROOF["gable"]
    # front gable first (the main roof's east eave overhangs it)
    pl.rect(gx1, gx2, ya, yb, lw=0.8, fill=colors.HexColor("#F6EFE6"))
    pl.line(gx1, (ya + yb) / 2, gx2, (ya + yb) / 2, lw=1.0)
    pl.line(gx2, ya, gx2, yb, lw=1.2)
    wx1, wx2, wa, wb = ROOF["wing"]
    ww = (wb - wa) / 2; wc = (wa + wb) / 2
    pl.rect(wx1, wx2, wa, wb, lw=0.8, fill=colors.HexColor("#F6EFE6"))
    pl.line(wx1, wc, wx2 - ww, wc, lw=1.0)
    for cy in (wa, wb):
        pl.line(wx2, cy, wx2 - ww, wc, lw=0.7)
    pl.line(wx1, wb, wx2, wb, lw=1.0, color=BLUE, dash=(3, 1.5))
    pl.text("valley gutter", (x2 + wx2) / 2, wb - 0.6, 4.2, color=BLUE)
    for i, t_ in enumerate(("KITCHEN WING", f"ridge {fmt_lvl(wing_ridge_z())}")):
        pl.text(t_, (x2 + wx2) / 2 + 0.6, wc + 1.8 - i * 1.0, 5 if i < 1 else 4.4, "Helvetica-Bold" if i < 1 else "Helvetica")
    for i, t_ in enumerate(("FRONT GABLE", "(MUKHAPPU)", f"ridge {fmt_lvl(gable_ridge_z())}", f"eaves {fmt_lvl(gable_eave_z())}")):
        pl.text(t_, (x2 + gx2) / 2, (ya + yb) / 2 + 4.6 - i * 1.0, 5 if i < 2 else 4.4, "Helvetica-Bold" if i < 2 else "Helvetica")
    pl.rect(x1, x2, y1, y2, lw=0.9, fill=WHITE)
    d = gablet_d()
    pl.line(x1 + d, yc, x2 - d, yc, lw=1.0)
    for cx, cy, gx, gy in ((x1, y1, x1 + d, y1 + d), (x1, y2, x1 + d, y2 - d), (x2, y1, x2 - d, y1 + d), (x2, y2, x2 - d, y2 - d)):
        pl.line(cx, cy, gx, gy, lw=0.7)
    for gx in (x1 + d, x2 - d):  # gablets: jali triangles at both hip ends
        pl.line(gx, y1 + d, gx, y2 - d, lw=1.2, color=ACC)
    pl.text("GABLET (JALI)", x1 + d - 1.6, yc + 2.2, 4.4, color=ACC); pl.text("GABLET (JALI)", x2 - d + 1.6, yc + 2.2, 4.4, color=ACC)
    pl.text("LOW CHAIPU ROOF ON THE SOUTH AND WEST WALLS, UNDER THIS EAVE", (x1 + x2) / 2 - 4, y1 + 0.55, 4.0, color=GREY)
    pl.text("MAIN HIPPED ROOF OVER THE TWO-STOREY BLOCK", (x1 + x2) / 2 - 4, yc + 4.5, 5.5, "Helvetica-Bold")
    # slope arrows
    for ax, ay, dx, dy in ((30, 8, 0, -4), (30, 20, 0, 4), (27, 14, -4, 0), (65, 6, 0, -3), (65, 22, 0, 3)):
        pl.line(ax, ay, ax + dx, ay + dy, lw=0.5, color=BLUE)
        pl.circle(ax + dx, ay + dy, 0.18, lw=0.4, color=BLUE, fill=BLUE)
    pl.text(f"{ROOF['pitch']} deg", 30.8, 7, 5, color=BLUE)
    # gutters and downpipes
    for a_, b_ in ((x1, x2), (gx1, gx2)):
        pl.rect(a_ - 0.4, b_ + 0.4, y1 - 0.4, y1, stroke=BLUE, lw=0.4); pl.rect(a_ - 0.4, b_ + 0.4, y2, y2 + 0.4, stroke=BLUE, lw=0.4)
    for dx, dy in ROOF["downpipes"]:
        pl.circle(dx, dy - 0.2 if dy < 14 else dy + 0.2, 0.35, lw=0.5, color=BLUE, fill=WHITE)
    pl.text("GUTTER + LEAF GUARD", 30, y1 - 1.2, 5, color=BLUE); pl.text("GUTTER + LEAF GUARD", 30, y2 + 1.2, 5, color=BLUE)
    pl.text("SOLAR PV ZONE (FUTURE), SOUTH SLOPE", 40, 5.0, 5.5, "Helvetica-Bold", ACC)
    pl.rect(31, 52, 1.6, 8.6, stroke=ACC, lw=0.4, dash=(2, 2))
    pl.text(f"RIDGE {fmt_lvl(ridge_z())}", 40, yc - 1.0, 5.5, "Helvetica-Bold")
    pl.text(f"EAVES {fmt_lvl(eave_z())}", 26, y1 + 1.5, 5)
    pl.text("LOFT TANK BELOW (OVER THE UPPER BATH)", 38.5, 8.8, 4.4, color=GREY)
    pl.hdim(x1, x2, -1.5, size=5); pl.hdim(gx1, gx2, -1.5, size=5); pl.vdim(y1, y2, 71.8, size=5)
    pl.hdim(x1, 14, 28.5, "2'-0\"", 4.6)
    tips = [
        "Every tile along eaves, verges, hips and ridges clipped or screwed; every third row elsewhere. Cyclone winds lift loose tiles first at the edges, and the main roof is now 20 ft up.",
        "Main roof trusses bolted to the first-floor ring beam; front gable and kitchen wing trusses to the ground-floor ring beam; purlins cleated, not just welded tacks.",
        "Where the front gable meets the east wall of the two-storey block: GI / aluminium apron flashing chased into the wall, with a counter-flashing; the main roof's east eave overhangs it by 2 ft. The valley between the gable and the kitchen wing gets a 12 in valley gutter draining east to its own downpipe.",
        "Eaves 2'-0\" beyond the wall line (kept inside the 27 ft plot on the north) with drip edges and gutters on both roofs; downpipes at 6 points into the sump filter, overflow to the road drain.",
        "Over the covered terrace the main roof sits on galvanised steel posts and steel trusses instead of walls; same tiles and fixings. No ridge ventilator: hot air under the roof escapes at the terrace's open sides.",
        "Attic over the first-floor rooms vented at the ridge and soffits with insect mesh; 50 mm insulation on the deck. Loft water tank on a steel platform over the upper bath.",
        "Leave a 25 mm conduit from roof to DB now for future solar PV on the south slope.",
    ]
    s.bullets(tips, 24 * mm, 66 * mm, 285 * mm, 6.8, title="Roof detailing (Guntur: heat, cyclone wind, short heavy rain)")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    c.showPage()


def sheet_schedules(c):
    s = Sheet(c, "A-601", "Schedules", "-")
    rd = [["ID", "Room", "Centreline", "Clear", "Area sq ft (clear)"]]
    tot = 0
    for fl in ("G", "F1"):
        with on_floor(fl):
            rd.append(["", f"<b>{FLOOR_NAMES[fl]}</b>", "", "", ""])
            for r in ROOMS:
                L, W = room_dims(r); cl, cw = clear_dims(r); tot += cl * cw
                rd.append([r[0], r[1], f"{fmt_ft(L)} x {fmt_ft(W)}", f"{fmt_ft(cl)} x {fmt_ft(cw)}", f"{cl * cw:.0f}"])
    rd.append(["", "Total (clear, both floors)", "", "", f"{tot:.0f}"])
    top = PH - 25 * mm
    h = s.table(rd, [9, 36, 22, 22, 16], 18 * mm, top, "Room schedule")
    dd = [["ID", "Location", "Width", "Type", "Vent above"]] + [[d[0], d[6], fmt_ft(d[4] - d[3]), d[7], TRANSOM_LABELS.get(TRANSOMS.get(d[0]), "-")] for d in both("DOORS")]
    s.table(dd, [9, 30, 12, 42, 14], 18 * mm, top - h - 12 * mm, "Door schedule (heights 7'-0\"; vents 7'-6\" to 9'-0\")")
    wd = [["ID", "Room", "Wall", "Width", "Sill", "Head", "Type"]]
    face = lambda w: {("X", 3): "S", ("X", 25): "N", ("Y", 14): "W", ("Y", 67): "E", ("Y", 61): "E"}.get((w[1], w[2]), "In")
    upper = {w[0] for w in WINDOWS_F1}
    wd += [[w[0], w[7] + (" (1st)" if w[0] in upper else ""), face(w), fmt_ft(w[4] - w[3]), fmt_ft(w[5]), fmt_ft(w[6]), w[8]] for w in both("WINDOWS")]
    wd += [[o[0], "Roof", "-", "-", "-", "-", o[1]] for o in OTHER_OPENINGS]
    h2 = s.table(wd, [9, 24, 10, 12, 11, 11, 68], 136 * mm, top, "Window and vent schedule (sill/head above floor)")
    fd = [["Space", "Floor", "Walls / skirting", "Ceiling"]] + [[f[0], f[1], f[2], f[3]] for f in FINISHES]
    s.table(fd, [36, 40, 46, 38], 136 * mm, top - h2 - 12 * mm, "Finishes")
    c.showPage()
