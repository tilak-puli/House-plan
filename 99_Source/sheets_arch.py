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
    carpet = sum(clear_dims(r)[0] * clear_dims(r)[1] for r in ROOMS)
    data = [("Site", "Guntur, Andhra Pradesh; agricultural land (conversion to confirm)"),
            ("Plot", f"{SITE['w']}' x {SITE['l']}' = {SITE['w'] * SITE['l']:,} sq ft, + {SITE['strip']}' north strip owned (Phase 2)"),
            ("Built footprint", "60' x 22' = 1,320 sq ft (wall centrelines)"),
            ("Carpet area", f"{carpet:,.0f} sq ft clear, incl. poomukham and open wet area"),
            ("Construction", "RCC frame, AAC walls, steel-truss roof with clay tiles"),
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
              ["Wall top / ring beam", fmt_lvl(LEVELS["FFL"] + LEVELS["wall_top"])],
              ["Roof eaves (tile edge)", fmt_lvl(eave_z())], ["Main ridge", fmt_lvl(ridge_z())],
              ["Front gable ridge", fmt_lvl(gable_ridge_z())]]
    h = s.table(levels, [50, 45], x2, top - 4 * mm, "Levels and heights")
    walls = [["Type", "Build-up", "Where"]] + [[k, v[1], {"EXT": "Outer walls, kitchen north wall", "WET": "Walls with concealed plumbing", "INT": "Other inner walls"}[k]] for k, v in WALL_TYPES.items()]
    s.table(walls, [12, 50, 33], x2, top - h - 16 * mm, "Wall types")
    gen = [
        "Dimensions are to wall centrelines unless marked 'clear'. Clear room sizes are on A-104.",
        "Concrete, steel, foundations and member sizes are by the structural engineer. Column positions are not shown and must be coordinated with the furniture layout.",
        "AAC: 150 mm galvanised mesh over every block-concrete joint; chases cut by machine; no hammering.",
        "All external sills, sunshades and copings get drip grooves; every external opening gets mosquito mesh.",
        "Wet rooms: waterproofing on floors, 12 in up the walls and 7 ft in showers; 48 h flood test before tiling.",
        "Skirting is flush with the plaster (no dust ledge). Grout in wet areas is epoxy.",
        "Pipes and conduits are laid before plaster and photographed with a tape measure in view, for future drilling.",
        "Keep 3 ft paved apron around the house, sloped away. No gardens, soak pits or big trees within 6-8 ft of walls.",
    ]
    s.bullets(gen, x3, top, w, title="General notes")
    rows = [["Stage", "Check before it is covered up", "Who"]] + [list(h) for h in HOLD_POINTS]
    s.table(rows, [40, 190, 50], x1, 128 * mm, "Hold points (stop and inspect)", 7)
    c.showPage()


def sheet_site(c):
    s = Sheet(c, "A-101", "Site plan and services", "1:100")
    pl = Plan(s, 100, 45 * mm, 128 * mm)
    site_context(pl)
    W = SITE["w"]
    x1, x2, y1, y2 = ROOF["hip"]
    pl.rect(x1 - 0.5, x2 + 0.5, -0, y2 + 0.5, stroke=GREY, lw=0.3, dash=(1, 1))  # apron edge (approx.)
    pl.rect(5, 65, 3, 25, stroke=INK, fill=colors.HexColor("#CFCFCF"), lw=0.8)
    pl.rect(x1, x2, y1, y2, stroke=INK, lw=0.4, dash=(3, 2))
    site_features(pl)
    pl.text("SINGLE-STOREY HOUSE, 60' x 22'", 35, 15.5, 8, "Helvetica-Bold")
    pl.text(f"FFL {fmt_lvl(LEVELS['FFL'])}  (dashed: roof eaves; dotted: 3 ft apron)", 35, 12.3, 6.5, color=GREY)
    pl.text(f"NORTH STRIP, {SITE['strip']}' (OPEN NOW, PHASE 2 SITE)", 35, W + 1.6, 6.5, color=GREY)
    pl.text("3' SERVICE WALKWAY", 35, 1.5, 6, color=GREY)
    pl.text("FRONT YARD", 71.5, 12.3, 6, color=GREY)
    pl.level(69.5, 17.6, 0)
    pl.hdim(0, 5, -3); pl.hdim(5, 65, -3); pl.hdim(65, 75, -3); pl.hdim(0, 75, -6.5, f"{SITE['l']}'-0\" PLOT")
    pl.vdim(0, 3, -3); pl.vdim(3, 25, -3); pl.vdim(25, W, -3); pl.vdim(0, W, -6.5, f"{W}'-0\" PLOT"); pl.vdim(W, W + SITE["strip"], -6.5)
    pl.north(PW - 105 * mm, PH - 40 * mm)
    pl.scalebar(250 * mm, 75 * mm)
    notes = [f"{f[0]}: {f[1]}" for f in SITE_FEATURES]
    s.bullets(notes[:7], 45 * mm, 62 * mm, 120 * mm, 6.3)
    s.bullets(notes[7:] + ["Site drains: finished ground falls 1:100 away from the house to the road side."], 175 * mm, 62 * mm, 150 * mm, 6.3)
    c.showPage()


def sheet_plan(c):
    s = Sheet(c, "A-102", "Ground floor plan", "1:75")
    pl = Plan(s, 75, 16 * mm, 75 * mm)
    site_context(pl)
    pl.walls()
    pl.openings()
    sx1, sx2, sy1, sy2 = ROOF["skylight"]
    pl.rect(sx1, sx2, sy1, sy2, stroke=GREY, lw=0.4, dash=(2, 2))
    pl.text("VENTILATOR ABOVE", (sx1 + sx2) / 2, sy1 + 0.6, 4.5, color=GREY)
    sx1_, sx2_, sy1_, sy2_ = next(f[3] for f in SITE_FEATURES if f[0] == "STEPS")
    pl.rect(sx1_, (sx1_ + sx2_) / 2, sy1_, sy2_, lw=0.3); pl.rect((sx1_ + sx2_) / 2, sx2_, sy1_, sy2_, lw=0.3)
    pl.text("UP", (sx1_ + sx2_) / 2, (sy1_ + sy2_) / 2, 4.5)
    pl.room_names(6, INK, sub=lambda r: "{} x {}".format(*map(fmt_ft, room_dims(r))))
    xs = [5, 14, 21, 41, 45, 51, 65]
    for a, b in zip(xs, xs[1:]): pl.hdim(a, b, -1.5)
    pl.hdim(5, 65, -4.3, "60'-0\" OVERALL")
    xn = [5, 11.5, 21, 36, 47, 59, 65]
    for a, b in zip(xn, xn[1:]): pl.hdim(a, b, 28.6)
    pl.vdim(3, 25, 72.6, "22'-0\" OVERALL")
    pl.vdim(3, 11, 69.6); pl.vdim(11, 13, 69.6); pl.vdim(13, 25, 69.6)
    pl.north(PW - 105 * mm, PH - 40 * mm)
    pl.scalebar(32 * mm, 30 * mm)
    sw = lambda fill: (lambda x, y: s.c.setFillColor(fill) or s.c.rect(x, y, 6 * mm, 2 * mm, stroke=0, fill=1))
    s.legend([(sw(WALL_FILL[k]), f"{k}: {v[1]}") for k, v in WALL_TYPES.items()], 150 * mm, 44 * mm)
    s.note("Door swings dashed. D = door, W = window (A-401).", 32 * mm, 20 * mm, 7, GREY)
    s.note("Section lines and clear sizes on A-104; levels on A-105.", 32 * mm, 16 * mm, 7, GREY)
    c.showPage()


def sheet_furniture(c):
    s = Sheet(c, "A-103", "Furniture layout", "1:75")
    pl = Plan(s, 75, 16 * mm, 75 * mm)
    site_context(pl)
    pl.walls(fill=colors.HexColor("#6B6B6B"))
    pl.openings(tags=False)
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
    rows = [[Paragraph(f"<b>{f[0]}</b>", st), Paragraph(f[2] + (f" (x{f[7]})" if f[7] > 1 else ""), st)] for f in FURNITURE]
    n = 3; per = (len(rows) + n - 1) // n
    for i in range(n):
        t = Table(rows[i * per:(i + 1) * per], colWidths=[8 * mm, 58 * mm])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5), ("TOPPADDING", (0, 0), (-1, -1), 0.5)]))
        w, h = t.wrap(0, 0); t.drawOn(c, (118 + i * 70) * mm, 66 * mm - h)
    s.note("Furniture key (full specs in schedules)", 118 * mm, 68 * mm, 7, INK, "Helvetica-Bold")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    pl.scalebar(32 * mm, 30 * mm)
    c.showPage()


SECTIONS = {"A": ("X", 44, "Cross section through the common bath, dining and dining bay"), "B": ("Y", 21, "Long section through bedrooms, living and poomukham")}


def sheet_working(c):
    s = Sheet(c, "A-104", "Working plan: clear sizes and sections", "1:75")
    pl = Plan(s, 75, 16 * mm, 104 * mm)
    pl.rect(0, SITE["l"], 0, SITE["w"], stroke=LIGHT, lw=0.5)
    pl.walls()
    pl.openings()
    for r in ROOMS:
        rid, name, x1, x2, y1, y2, _ = r
        cx, cy = ROOM_LABEL_AT.get(rid, ((x1 + x2) / 2, (y1 + y2) / 2))
        if rid == "R10": cy = 17.3
        L, W = clear_dims(r)
        small = (x2 - x1) <= 6
        pl.text(short_name(name).upper(), cx, cy + 0.6, 5 if small else 5.8, "Helvetica-Bold")
        pl.text(f"{fmt_ft(L)} x", cx, cy - 0.3, 4.6, color=ACC) if small else None
        pl.text(f"{fmt_ft(W)}" if small else f"{fmt_ft(L)} x {fmt_ft(W)} clear", cx, cy - (1.05 if small else 0.4), 4.6 if small else 5, color=ACC)
    for name, (axis, c0, _) in SECTIONS.items():
        if axis == "X":
            pl.line(c0, -2.5, c0, 28.5, lw=0.7, color=RED, dash=(6, 2, 1, 2))
            for yy, lab in ((-3.3, name), (29.2, name)):
                pl.circle(c0, yy, 0.8, lw=0.6, color=RED, fill=WHITE); pl.text(lab, c0, yy, 6.5, "Helvetica-Bold", RED)
        else:
            pl.line(1, c0, 70, c0, lw=0.7, color=RED, dash=(6, 2, 1, 2))
            for xx in (0.2, 70.8):
                pl.circle(xx, c0, 0.8, lw=0.6, color=RED, fill=WHITE); pl.text(name, xx, c0, 6.5, "Helvetica-Bold", RED)
    xs = [5, 11.5, 14, 21, 41, 45, 47, 51, 55, 59, 65]
    for a, b in zip(xs, xs[1:]): pl.hdim(a, b, -1.3, size=5)
    yn = [3, 10.5, 13, 15.5, 17, 19, 25]
    for a, b in zip(yn, yn[1:]): pl.vdim(a, b, 68.6, size=5)
    s.note("Clear sizes are wall face to wall face after plaster (green). Grid dimensions are to wall centrelines.", 24 * mm, 32 * mm, 7, GREY)
    s.note("Section A-A and B-B on A-301. Check every furniture item against the clear size before ordering.", 24 * mm, 27 * mm, 7, GREY)
    s.note("Column positions (by engineer) must avoid door swings, wardrobes and the TV wall.", 24 * mm, 22 * mm, 7, GREY)
    pl.north(PW - 105 * mm, PH - 40 * mm)
    pl.scalebar(200 * mm, 30 * mm)
    c.showPage()


FLOOR_COLOURS = {"Red oxide / Kota stone": "#E8C9B8", "Matt vitrified 2x2": "#E5E1D6", "Marble / teak (pooja)": "#F4F1E8",
                 "Anti-skid matt vitrified": "#D8E3D4", "Anti-skid ceramic, waterproofed": "#CFE0EC",
                 "Rough Cuddapah / Kota, falls": "#D4D9DE", "Flamed granite": "#DCD2C4"}
FLOOR_GROUPS = [(k, colors.HexColor(v), [r for r, f in FLOOR_FINISH.items() if f == k]) for k, v in FLOOR_COLOURS.items()]


def sheet_finishes(c):
    s = Sheet(c, "A-105", "Floor finishes and levels", "1:75")
    pl = Plan(s, 75, 16 * mm, 104 * mm)
    pl.rect(0, SITE["l"], 0, SITE["w"], stroke=LIGHT, lw=0.5)
    for _, col, rooms in FLOOR_GROUPS:
        for rid in rooms:
            r = room_of(rid); pl.rect(r[2], r[3], r[4], r[5], stroke=None, fill=col)
    pl.walls(fill=INK)
    pl.openings(tags=False)
    for r in ROOMS:
        rid, name, x1, x2, y1, y2, _ = r
        cx, cy = ROOM_LABEL_AT.get(rid, ((x1 + x2) / 2, (y1 + y2) / 2))
        pl.text(short_name(name), cx, cy + 0.8, 5.2, "Helvetica-Bold")
        pl.level(cx - 1.2, cy - 0.6, floor_level(rid), 5)
    for rid, ang in (("R04", "1:60 to drain"), ("R07", "1:60 to drain"), ("R08", "1:60 to drain"), ("R13", "1:80 to drain")):
        r = room_of(rid); pl.text("falls " + ang, (r[2] + r[3]) / 2, r[4] + 0.8, 4.4, color=BLUE)
    pl.level(69, 9, LEVELS["FGL"], 5); pl.text("finished ground", 69, 8, 4.5, color=GREY)
    sw = lambda fill: (lambda x, y: s.c.setFillColor(fill) or s.c.setStrokeColor(GREY) or s.c.rect(x, y, 6 * mm, 3 * mm, stroke=1, fill=1))
    s.legend([(sw(col), name) for name, col, _ in FLOOR_GROUPS], 24 * mm, 64 * mm)
    tips = [
        "Skirting 4 in high, set flush with the plaster face (plaster stops in a groove above it), so no ledge collects dust.",
        "Bathrooms 12 mm below the bedroom floor with a sloped granite threshold: no raised step to trip on, water stays in.",
        "Shower zone: linear drain at the far end, floor falls 1:60 only inside the wet zone; dry zone floor nearly flat.",
        "Poomukham and steps: flamed or leather-finish stone. Polished granite is slippery when wet.",
        "Kitchen: mid-tone matt floor; white glossy tile shows every stain and is slippery with oil.",
        "Leave 5 mm expansion gaps at walls under the skirting and every 15-20 ft in large floors.",
    ]
    s.bullets(tips, 110 * mm, 66 * mm, 210 * mm, 6.8, title="Floor detailing")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    c.showPage()


def sheet_roof(c):
    s = Sheet(c, "A-106", "Roof plan", "1:75")
    pl = Plan(s, 75, 16 * mm, 104 * mm)
    pl.rect(0, SITE["l"], 0, SITE["w"], stroke=LIGHT, lw=0.5)
    pl.rect(5, 60, 3, 25, stroke=GREY, lw=0.4, dash=(2, 2))
    x1, x2, y1, y2 = ROOF["hip"]
    w = (y2 - y1) / 2; yc = (y1 + y2) / 2
    pl.rect(x1, x2, y1, y2, lw=0.9)
    pl.line(x1 + w, yc, x2 - w, yc, lw=1.0)
    for cx, cy, rx in ((x1, y1, x1 + w), (x1, y2, x1 + w), (x2, y1, x2 - w), (x2, y2, x2 - w)):
        pl.line(cx, cy, rx, yc, lw=0.7)
    gx1, gx2, ya, yb = ROOF["gable"]
    (v1, v2), ridge_end = gable_valleys()
    pl.line(ridge_end[0], ridge_end[1], gx2, (ya + yb) / 2, lw=1.0)
    for a, b in (v1, v2):
        pl.line(a[0], a[1], b[0], b[1], lw=0.6, dash=(3, 1.5))
    pl.line(gx2, ya, gx2, yb, lw=1.2)
    pl.text("FRONT GABLE (MUKHAPPU)", gx2 + 1, (ya + yb) / 2 + 1, 5, "Helvetica-Bold", anchor="l")
    sx1, sx2, sy1, sy2 = ROOF["skylight"]
    o = ROOF["vent_overhang"]
    pl.rect(sx1 - o, sx2 + o, sy1 - o, sy2 + o, lw=0.5)
    for cx, cy in ((sx1 - o, sy1 - o), (sx2 + o, sy1 - o), (sx1 - o, sy2 + o), (sx2 + o, sy2 + o)):
        pl.line(cx, cy, (sx1 + sx2) / 2, (sy1 + sy2) / 2, lw=0.4)
    pl.rect(sx1, sx2, sy1, sy2, lw=0.4, dash=(1.5, 1))  # louvre band under the cap
    pl.text("VENTILATOR (A-503)", (sx1 + sx2) / 2, sy2 + o + 0.7, 5, "Helvetica-Bold")
    # slope arrows
    for ax, ay, dx, dy in ((20, 8, 0, -4), (35, 22, 0, 4), (8.5, 14, -4, 0), (63, 6, 3, 0)):
        pl.line(ax, ay, ax + dx, ay + dy, lw=0.5, color=BLUE)
        pl.circle(ax + dx, ay + dy, 0.18, lw=0.4, color=BLUE, fill=BLUE)
    pl.text(f"{ROOF['pitch']} deg", 20.8, 7, 5, color=BLUE)
    # gutters and downpipes
    pl.rect(x1 - 0.4, x2 + 0.4, y1 - 0.4, y1, stroke=BLUE, lw=0.4); pl.rect(x1 - 0.4, x2 + 0.4, y2, y2 + 0.4, stroke=BLUE, lw=0.4)
    for i, (dx, dy) in enumerate(ROOF["downpipes"]):
        pl.circle(dx, dy - 0.2 if dy < 14 else dy + 0.2, 0.35, lw=0.5, color=BLUE, fill=WHITE)
    pl.text("GUTTER + LEAF GUARD", 12, y1 - 1.2, 5, color=BLUE); pl.text("GUTTER + LEAF GUARD", 12, y2 + 1.2, 5, color=BLUE)
    pl.text("SOLAR PV ZONE (FUTURE), SOUTH SLOPE", 30, 5.5, 5.5, "Helvetica-Bold", ACC)
    pl.rect(18, 51, 1.5, 9.5, stroke=ACC, lw=0.4, dash=(2, 2))
    pl.text(f"RIDGE {fmt_lvl(ridge_z())}", 24, yc + 0.8, 5.5, "Helvetica-Bold")
    pl.text(f"EAVES {fmt_lvl(eave_z())}", 10, y1 + 1.5, 5)
    pl.text("ridge vent with mesh", 25, yc - 0.9, 4.6, color=GREY)
    pl.text("LADDER", 1.7, 9.8, 4.6)
    pl.hdim(x1, x2, -1.5, size=5); pl.vdim(y1, y2, 64.8, size=5)
    pl.hdim(x1, 5, 29.5, "2'-6\"", 4.6)
    tips = [
        "Every tile along eaves, verges, hips and ridges clipped or screwed; every third row elsewhere. Cyclone winds lift loose tiles first at the edges.",
        "Trusses bolted to the RCC ring beam with holding-down bolts; purlins cleated, not just welded tacks.",
        "Eaves 2'-6\" beyond the wall line with a drip edge so water falls clear of the wall and windows.",
        "Gutters at both long eaves, downpipes at 8 points into the sump filter and recharge pit; none discharging onto bare soil by the walls.",
        "Ventilator: hipped tiled cap, 45 deg louvres with mesh, sealed inner shutters, 9 in upstand with flashing (detail on A-503).",
        "Valleys at the front gable: 600 mm wide GI / aluminium valley gutter under the tiles.",
        "Attic vented at the ridge and soffits with insect mesh; 50 mm insulation on the deck.",
        "Leave a 25 mm conduit from roof to DB now for future solar PV on the south slope.",
    ]
    s.bullets(tips, 24 * mm, 66 * mm, 285 * mm, 6.8, title="Roof detailing (Guntur: heat, cyclone wind, short heavy rain)")
    pl.north(PW - 105 * mm, PH - 40 * mm)
    c.showPage()


def sheet_schedules(c):
    s = Sheet(c, "A-601", "Schedules", "-")
    rd = [["ID", "Room", "Centreline", "Clear", "Area sq ft (clear)"]]
    tot = 0
    for r in ROOMS:
        L, W = room_dims(r); cl, cw = clear_dims(r); tot += cl * cw
        rd.append([r[0], r[1], f"{fmt_ft(L)} x {fmt_ft(W)}", f"{fmt_ft(cl)} x {fmt_ft(cw)}", f"{cl * cw:.0f}"])
    rd.append(["", "Total (clear)", "", "", f"{tot:.0f}"])
    top = PH - 25 * mm
    h = s.table(rd, [9, 36, 22, 22, 16], 18 * mm, top, "Room schedule")
    dd = [["ID", "Location", "Width", "Type", "Vent above"]] + [[d[0], d[6], fmt_ft(d[4] - d[3]), d[7], TRANSOM_LABELS.get(TRANSOMS.get(d[0]), "-")] for d in DOORS]
    s.table(dd, [9, 30, 12, 42, 14], 18 * mm, top - h - 12 * mm, "Door schedule (heights 7'-0\"; vents 7'-6\" to 9'-0\")")
    wd = [["ID", "Room", "Wall", "Width", "Sill", "Head", "Type"]]
    face = lambda w: {("X", 3): "S", ("X", 25): "N", ("Y", 5): "W", ("Y", 65): "E", ("Y", 59): "E"}.get((w[1], w[2]), "-")
    wd += [[w[0], w[7], face(w), fmt_ft(w[4] - w[3]), fmt_ft(w[5]), fmt_ft(w[6]), w[8]] for w in WINDOWS]
    wd += [[o[0], "Roof", "-", "-", "-", "-", o[1]] for o in OTHER_OPENINGS]
    h2 = s.table(wd, [9, 24, 10, 12, 11, 11, 68], 136 * mm, top, "Window and vent schedule (sill/head above floor)")
    fd = [["Space", "Floor", "Walls / skirting", "Ceiling"]] + [[f[0], f[1], f[2], f[3]] for f in FINISHES]
    s.table(fd, [36, 40, 46, 38], 136 * mm, top - h2 - 12 * mm, "Finishes")
    c.showPage()
