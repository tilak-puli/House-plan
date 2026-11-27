import re
"""Architectural plan sheets: cover, design basis, site, plans, finishes, roof, schedules."""
from sheetlib import *


def decision_summary(d, n=150):
    """One decision in short: its heading in bold, then its first sentence cut to about n characters."""
    head, rest = (d.split(": ", 1) + [""])[:2] if ": " in d[:90] else ("", d)
    if head.startswith("Carried over from the duplex") and ": " in rest[:90]:
        h2, rest = rest.split(": ", 1)
        head = "Carried: " + h2
    head = re.sub(r" \(\d+ \w+ 20\d\d(, owner)?\)", "", head)
    rest = rest.split(". ")[0]
    if len(rest) > n:  # a complete phrase: up to the last clause break (never cut mid-phrase, no "..."); else the whole sentence, wrapped
        cut = rest[:n]
        i = max(cut.rfind("; "), cut.rfind(": "), cut.rfind(", "))
        if i > n * 0.4:
            rest = cut[:i].rstrip(",;:")
        if rest.count("(") > rest.count(")"):   # never leave a bracket open
            rest = rest[:rest.rfind("(")].rstrip(" ,;:")
    return (f"<b>{head}:</b> " if head else "") + rest


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
    ar = floor_areas()
    gf = ar["ground"] + ar["walkway"]
    t_ = ROOF["terrace"]
    data = [("Site", PROJECT["location"]),
            ("Plot", f"{PROJECT['plot']}; about {plot_area():,.0f} sq ft"),
            ("Built footprint", f"{fmt_ft(HX2 - HX1)} x {fmt_ft(HY2 - HY1)} ground floor round a {COURT:.0f} x {COURT:.0f} ft open courtyard: about {gf:,.0f} sq ft (rooms and walkway); "
                                f"upper wing over the west band and the den about {ar['upper']:,.0f} sq ft (stair well included); roof terrace {(t_[1] - t_[0]) * (t_[3] - t_[2]):,.0f} sq ft over the family living; thinnai in front"),
            ("Carpet area", f"{carpet:,.0f} sq ft clear, both floors, incl. the walkway, courtyard, thinnai and roof terrace"),
            ("Construction", "Single-storey ring round the courtyard plus a two-storey west wing: RCC frame, AAC walls, first-floor slab over the wing and the terrace, clay Mangalore tile roofs"),
            ("Plinth", f"FFL {fmt_lvl(LEVELS['FFL'])} above finished ground; courtyard {fmt_lvl(LEVELS['courtyard'])}")]
    for k, v in data:
        s.note(k, 20 * mm, y, 8.5, GREY); y -= s.para(v, 52 * mm, y + 3 * mm, 112 * mm, 8.0) + 1.6 * mm
    x2 = 175 * mm; y = PH - 72 * mm
    s.note("Key design decisions", x2, y, 12, INK, "Helvetica-Bold")
    s.note("In short; the full wording is in the schedules workbook (Decisions tab).", x2 + 52 * mm, y, 7, GREY)
    y -= 4 * mm
    items = [decision_summary(d) for d in DECISIONS]
    half = (len(items) + 1) // 2
    for col, xx in ((items[:half], x2), (items[half:], x2 + 76 * mm)):
        assert y - s.bullets(col, xx, y, 72 * mm, 5.6) >= 12 * mm, "the decisions run off the cover"
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
    lv = [("Finished ground (FGL)", LEVELS["FGL"], ""), ("Thinnai and foyer", LEVELS["thinnai"], ""),
          ("Courtyard (sunken stone floor)", LEVELS["courtyard"], ""), ("Walkway", LEVELS["walkway"], ""),
          ("Wet area floor", LEVELS["wet_area"], ""), ("House floor (FFL)", LEVELS["FFL"], ""),
          ("Bathroom floors", LEVELS["FFL"] - LEVELS["bath_drop"], " (12 mm drop)"),
          ("Door head / lintel band", LEVELS["FFL"] + LEVELS["door_head"], ""),
          ("False ceilings (rooms)", LEVELS["FFL"] + LEVELS["false_ceiling"], ""),
          ("False ceilings (baths)", LEVELS["FFL"] + LEVELS["bath_ceiling"], ""),
          ("Living ceiling (terrace slab soffit)", floor_level("R16") + CEILINGS["R16"][1], ""),
          ("Ground-floor ring beam (top of the ground walls)", LEVELS["FFL"] + LEVELS["wall_top"], ""),
          ("First floor (finished)", floor_base("F1"), ""), ("Roof terrace slab (finished)", terrace_slab_z(), ""),
          ("Terrace canopy", terrace_slab_z() + ROOF["canopy"], ""),
          ("First-floor ring beam", upper_wall_top_z(), ""),
          ("Ring roof eaves (outer and inner), court grille", eave_z(), ""), ("Ring roof ridge", ridge_z(), ""),
          ("West wing eaves", wing_eave_z(), ""), ("West wing ridge", wing_ridge_z(), "")]
    levels = [["Level", "Above finished ground"]] + [[n, fmt_lvl(z) + t] for n, z, t in sorted(lv, key=lambda r: r[1])]  # low to high
    h = s.table(levels, [50, 45], x2, top - 4 * mm, "Levels and heights")
    walls = [["Type", "Build-up", "Where"]] + [[k, v[1], {"EXT": "Outer walls and the walls round the walkway", "WET": "Walls with concealed plumbing", "INT": "Other inner walls"}[k]] for k, v in WALL_TYPES.items()]
    s.table(walls, [12, 50, 33], x2, top - h - 16 * mm, "Wall types")
    gen = [
        "Dimensions are to wall centrelines unless marked 'clear'. Clear room sizes are on A-106 (ground) and A-107 (first floor).",
        "Concrete, steel, foundations and member sizes are by the structural engineer. Column positions are not shown and must be coordinated with the furniture layout.",
        "AAC: 150 mm galvanised mesh over every block-concrete joint; chases cut by machine; no hammering.",
        "Lintel band: the continuous RCC band at 7'-0\" steps up over the windows whose heads are above it (" + ", ".join(lintel_step_windows()) + ") with vertical legs either side of each opening, and stays continuous round the building (IS 4326); windows wholly above 7'-0\" sit on the band.",
        "All external sills, sunshades and copings get drip grooves; every external opening gets mosquito mesh.",
        "Wet rooms: waterproofing on floors, 12 in up the walls and 7 ft in showers; 48 h flood test before tiling.",
        "Skirting is flush with the plaster (no dust ledge). Grout in wet areas is epoxy.",
        "Pipes and conduits are laid before plaster and photographed with a tape measure in view, for future drilling.",
        "Keep 3 ft paved apron around the house, sloped away. No gardens, soak pits or big trees within 6-8 ft of walls.",
        "West wing on two storeys: its columns, footings, the first-floor slab and the stair are designed by the engineer for two floors; RCC column stubs at the roof terrace's edge take the steel canopy posts.",
    ]
    s.bullets(gen, x3, top, w, title="General notes")
    rows = [["Stage", "Check before it is covered up", "Who"]] + [list(h) for h in HOLD_POINTS]
    s.table(rows, [40, 190, 50], x1, 128 * mm, "Hold points (stop and inspect)", 7)
    c.showPage()


def sheet_phasing(c):
    s = Sheet(c, "A-002", "Construction phasing (roof first, three stages)", "1:150")
    pale = colors.HexColor("#E3EFE8"); mid = colors.HexColor("#9A9A9A")
    with on_floor("F1"):
        k150 = 304.8 / 150 * mm
        pl = Plan(s, 150, 24 * mm - (HX1 - 2) * k150, 262 * mm - (HY2 + 2) * k150)
        st_ = STAIR
        well = (HX1, st_["flight2"][1] + 0.21, st_["core"][2], RING[3])   # the stair well: x1, x2, y1, y2
        def stair_wall(r):
            x1, x2, y1, y2 = r
            on_y = abs((x1 + x2) / 2 - well[1]) < 0.4 and y2 > well[2] - 4 and y1 < well[3]   # wall between the well / stair head and the reading room
            on_x = abs((y1 + y2) / 2 - well[3]) < 0.4 and x1 < well[1] and x2 > well[0]      # the well's north wall
            return on_y or on_x
        for r in ROOMS:
            if r[0] in PHASE2_ROOMS:
                pl.rect(r[2], r[3], r[4], r[5], stroke=None, fill=pale)
        for rect, wt in wall_rects(with_type=True):
            x1, x2, y1, y2 = rect
            if wt != "EXT" and stair_wall(rect):
                pl.rect(x1, x2, y1, y2, stroke=None, fill=INK)
            elif wt == "EXT":
                pl.rect(x1, x2, y1, y2, stroke=INK, fill=mid, lw=0.3)
            else:
                pl.rect(x1, x2, y1, y2, stroke=ACC, fill=WHITE, lw=0.6, dash=(1.5, 1))
        pl.openings(tags=False)
        pl.floor_extras()
        pl.room_names(3.9, INK)
        jd = next((d for d in DOORS if "jali" in d[7].lower() and d[5] == 0), None)   # a sliding teak jali door at the stair head (none in the compact wing: the stair lobby's D09 closes the stair below)
        if jd:
            pl.line(jd[2], jd[3], jd[2], jd[4], lw=1.4, color=RED)
        for axis, c0, a, b in RAILS:   # stage 1: temporary railings on every open edge (terrace, gallery guard) until the stage 2 railings go in
            if axis == "X": pl.line(a, c0, b, c0, lw=1.4, color=RED)
            else: pl.line(c0, a, c0, b, lw=1.4, color=RED)
        pl.north(180 * mm, 246 * mm)
    s.note("First floor through the stages (1:150): stair, frame, slab, roof and terrace in stage 1; outer walls (grey) in stage 2; inner walls and fit-out (green) in stage 3.", 20 * mm, 139 * mm, 6.5, GREY)
    def sw(fill, stroke=None, dash=None):
        def f(x, y):
            s.c.setFillColor(fill or WHITE); s.c.setStrokeColor(stroke or INK); s.c.setLineWidth(0.6)
            if dash: s.c.setDash(*dash)
            s.c.rect(x, y, 6 * mm, 2 * mm, stroke=1 if stroke else 0, fill=1); s.c.setDash()
        return f
    s.legend([(sw(INK), "Stage 1: walls round the stair well (frame, slab, roof, terrace also stage 1)"), (sw(mid, INK), "Stage 2: outer walls and windows"),
              (sw(WHITE, ACC, (1.5, 1)), "Stage 3: inner walls and baths"), (sw(pale), "Stage 3 fit-out area"),
              (sw(RED), "Stage 1: temporary railings on open edges (the stair lobby door D09 locks the stair off)")], 20 * mm, 133 * mm)
    rows = [["Stage", "Scope", "Rough cost"]] + [[name, "<br/>".join("&bull; " + i for i in items), cost] for name, items, cost in PHASES]
    s.table(rows, [28, 72, 20], 205 * mm, 262 * mm, "Three stages, roof first")
    s.bullets(PHASE1_PROVISIONS, 20 * mm, 108 * mm, 160 * mm, 6.4, title="Build in stage 1 so the later stages are easy")
    s.bullets(PHASE1_LIVING, 190 * mm, 112 * mm, 135 * mm, 6.6, title="Living with stage 1")
    s.note("Rates are rough 2026 village rates around Guntur; get contractor quotes on the Quantities sheet. Structure, beams and sleeves by the structural engineer.", 20 * mm, 18 * mm, 7, GREY)
    c.showPage()


def sheet_site(c):
    s = Sheet(c, "A-101", "Site plan: the whole plot", "1:150")
    pl = Plan(s, 150, 24 * mm - PLOT_X1 * 304.8 / 150 * mm, 158 * mm)
    site_context(pl, x_end=PLOT_X2)
    # the house: the ring of rooms, the walkway round the open courtyard, the two-storey west wing, the roof terrace, the thinnai
    pl.rect(HX1, HX2, HY1, HY2, stroke=INK, fill=colors.HexColor("#C9C9C9"), lw=0.8)
    pl.rect(HX1, RING[0], HY1, HY2, stroke=INK, fill=colors.HexColor("#9E9E9E"), lw=0.5)
    t_ = ROOF["terrace"]
    pl.rect(t_[0], t_[1], t_[2], t_[3], stroke=INK, fill=colors.HexColor("#E2D6C2"), lw=0.5)
    pl.rect(*RING, stroke=INK, fill=colors.HexColor("#E4E4E4"), lw=0.5)
    pl.rect(*COURTYARD, stroke=INK, fill=colors.HexColor("#DCEAF5"), lw=0.5)
    r17 = room_of("R17")
    pl.rect(r17[2], r17[3], r17[4], r17[5], stroke=INK, fill=colors.HexColor("#E8C9B8"), lw=0.5)
    stp = next(f[3] for f in SITE_FEATURES if f[0] == "STEPS")
    pl.rect(stp[0], stp[1], stp[2], stp[3], stroke=INK, lw=0.3)
    pl.rect(*ROOF["ring"], stroke=INK, lw=0.3, dash=(3, 2))
    site_features(pl, size=4.4, x_end=PLOT_X2)
    pl.text("MUTRAM", CX, CY + 0.8, 5.2, "Helvetica-Bold", BLUE)
    pl.text("(open court)", CX, CY - 1.4, 4.2, color=BLUE)
    pl.text("HOUSE", (RING[1] + HX2) / 2, 16.5, 7, "Helvetica-Bold")
    pl.text(f"FFL {fmt_lvl(LEVELS['FFL'])}", (RING[1] + HX2) / 2, 13.0, 5, color=GREY)
    pl.text("UPPER WING", (HX1 + RING[0]) / 2, 30.0, 5, "Helvetica-Bold", WHITE)
    pl.text("(2 storeys)", (HX1 + RING[0]) / 2, 27.4, 4.4, color=WHITE)
    pl.text("ROOF TERRACE", (t_[0] + t_[1]) / 2, (t_[2] + t_[3]) / 2, 4.6, "Helvetica-Bold")
    px_, py_ = pl.p((r17[2] + r17[3]) / 2, r17[4] + 3.0); c.saveState(); c.translate(px_, py_); c.rotate(90)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 4.4); c.drawString(0, -1.5, "THINNAI"); c.restoreState()
    for x, y, rr in TREES:   # the name inside the canopy: clear of the boundary, the drive and the beds
        pl.text("neem" if rr > 3 else "coconut" if rr < 2 else "fruit tree", x, y, 3.8, color=colors.HexColor("#4F6E34"))
    guild = next(f[3] for f in SITE_FEATURES if f[0] == "GUILD")
    for x, y, rr, k in FOOD_TREES:   # the guild's trees are named in its note: label only the trees outside it
        if k not in ("banana", "papaya") and not (guild[0] <= x <= guild[1] and guild[2] <= y <= guild[3]):
            pl.text(k, x, y - rr - 0.9, 3.8, color=colors.HexColor("#4F6E34"))
    yN = lambda x: plot_north(x)
    pl.hdim(PLOT_X1, HX1, -3, f"{HX1 - PLOT_X1:.0f}' BACK GARDEN", 5); pl.hdim(HX1, HX2, -3, f"{HX2 - HX1:.0f}' HOUSE", 5); pl.hdim(HX2, PLOT_X2, -3, f"{PLOT_X2 - HX2:.0f}' FRONT LAND", 5)
    pl.hdim(PLOT_X1, PLOT_X2, -7, f"{PLOT_X2 - PLOT_X1:.0f}'-0\" PLOT (WEST BOUNDARY TO THE EAST ROAD)", 5.5)
    pl.vdim(0, yN(PLOT_X1), PLOT_X1 - 3, f"{yN(PLOT_X1):.0f}' PLOT", 5); pl.vdim(0, HY1, HX1 - 1.5, f"{HY1:.0f}'", 4.6); pl.vdim(HY2, yN(HX2), HX1 - 1.5, f"{yN(HX2) - HY2:.0f}'", 4.6)
    pl.north(PW - 100 * mm, PH - 32 * mm)
    pl.scalebar(PW - 150 * mm, 140 * mm)
    notes = [f"{f[0]}: {f[1]}" for f in SITE_FEATURES if f[0] not in ("APRON", "STEPS", "GSTEP", "FEET", "WSTEP")]
    notes += [f"Plot area about {plot_area():,.0f} sq ft; compound wall about {plot_perimeter():.0f} ft, the road face in exposed brick or local stone, the rest precast post-and-panel 5 ft.",
              "Ground falls 1:100 away from the house and down the drive to the road; roof water to the recharge pit."]
    # three balanced columns between the plan's dimensions and the frame
    size, colw, top, bottom = 5.6, 99 * mm, 128 * mm, 14 * mm
    st = ParagraphStyle("sn", fontName="Helvetica", fontSize=size, leading=size * 1.3)
    hs = [Paragraph("&bull; " + n, st).wrap(colw, 400 * mm)[1] + 1 * mm for n in notes]
    total, cols, cur, acc = sum(hs), [[]], 0, 0
    for n, h in zip(notes, hs):
        if acc + h / 2 > total * len(cols) / 3 and len(cols) < 3:
            cols.append([])
        cols[-1].append(n); acc += h
    for i, col in enumerate(cols):
        used = s.bullets(col, (18 + i * 103) * mm, top, colw, size)
        assert top - used >= bottom, f"site notes column {i + 1} runs down to {(top - used) / mm:.0f} mm"
    c.showPage()


def plan_furniture_scale(pl):
    """North arrow and a short scale bar in the free corner north-east of the house (same place on every plan sheet)."""
    pl.north(PW - 105 * mm, PH - 40 * mm)
    pl.scalebar(281 * mm, 226 * mm, steps=(0, 5, 10))


def sheet_plan(c, num="A-102", title="Ground floor plan"):
    s = Sheet(c, num, title, "1:75")
    ground = FLOOR[0] == "G"
    pl = house_plan(s)
    pl.walls()
    pl.openings()
    pl.floor_extras()
    if ground:
        stp = next(f[3] for f in SITE_FEATURES if f[0] == "STEPS")
        pl.text("UP", (stp[0] + stp[1]) / 2 + 0.2, stp[3] + 0.7, 4.5)
    pl.room_names(6, INK, sub=lambda r: "{} x {}".format(*map(fmt_ft, clear_dims(r))), halo=True, skip=("R06",))
    if ground:
        pl.stair_label()   # turned along flight 1, beside its arrow (its size is on A-106)
    pl.auto_dims()
    plan_furniture_scale(pl)
    sw = lambda fill: (lambda x, y: s.c.setFillColor(fill) or s.c.rect(x, y, 6 * mm, 2 * mm, stroke=0, fill=1))
    s.legend([(sw(WALL_FILL[k]), f"{k}: {v[1]}") for k, v in WALL_TYPES.items()], 212 * mm, 34 * mm)
    notes = ["Door swings dashed. D = door (A-401), W = window (A-402). Room sizes are clear, wall face to wall face."]
    if ground:
        notes += ["Stair treads above the cut line dashed. Section lines and clear sizes on A-106; levels on A-108.",
                  "The courtyard (hatched) is open to the sky, one step below the walkway."]
    else:
        notes += [f"First floor at {fmt_lvl(floor_base('F1'))}. Railings 4'-0\" high, vertical bars at 100 mm or less (double lines).",
                  "The roof terrace over the family living has a light tiled canopy on steel posts; the jharokhas (shaded) project over the walkway roof."]
    for i, n in enumerate(notes):
        assert c.stringWidth(n, "Helvetica", 7) < 184 * mm, n
        s.note(n, 24 * mm, (30 - 4.5 * i) * mm, 7, GREY)
    c.showPage()


def key_columns(c, rows, x0, ytop, ybot, col_w, gap=3 * mm, size=5.4, dry=False):
    """Lay key rows ([id, text]) out in columns from x0, each column filled down to ybot. Returns the right edge used
    (dry=True measures only)."""
    st = ParagraphStyle("k", fontName="Helvetica", fontSize=size, leading=size * 1.16)
    x, y = x0, ytop
    for fid, txt in rows:
        t = Table([[Paragraph(f"<b>{fid}</b>", st), Paragraph(txt, st)]], colWidths=[8.5 * mm, col_w - 8.5 * mm])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.4), ("TOPPADDING", (0, 0), (-1, -1), 0.4),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0.5), ("RIGHTPADDING", (0, 0), (-1, -1), 1.0)]))
        w, h = t.wrap(0, 0)
        if y - h < ybot:
            x, y = x + col_w + gap, ytop
        if not dry:
            t.drawOn(c, x, y - h)
        y -= h
    return x + col_w


def sheet_furniture(c, num="A-103", title="Furniture layout, ground floor"):
    s = Sheet(c, num, title, "1:75")
    pl = house_plan(s)
    pl.walls(fill=colors.HexColor("#6B6B6B"))
    pl.openings(tags=False)
    pl.floor_extras()
    shapes = {f[0]: f[9] for f in FURNITURE}
    tags = []
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
            pending.append((fid, x1, x2, y1, y2))
        tags.append((x1, x2, y1, y2))
    pending = []
    for f in FURNITURE:
        draw(f[0], f[3], f[4], f[5], f[6], True)
    for fid, x1, x2, y1, y2 in EXTRA_DRAW:
        draw(fid, x1, x2, y1, y2, False)
    # tags: inside the item when they fit, else beside it, clear of walls, other items, door swings and other tags
    walls_ = [r for r in wall_rects()]
    placed = []
    hit = lambda b, rs: any(b[0] < q[1] and b[1] > q[0] and b[2] < q[3] and b[3] > q[2] for q in rs)
    outside = []
    for fid, x1, x2, y1, y2 in pending:
        sz = 5 if (x2 - x1) * (y2 - y1) > 3 else 4
        w = c.stringWidth(fid, "Helvetica-Bold", sz) / pl.k + 0.15; h = sz * 0.75 / pl.k + 0.1
        if w <= x2 - x1 and h <= y2 - y1:
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            pl.text(fid, cx, cy, sz, "Helvetica-Bold", ACC); placed.append((cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2))
        else:
            outside.append((fid, x1, x2, y1, y2, sz, w, h))
    swings = pl.door_boxes()
    for fid, x1, x2, y1, y2, sz, w, h in outside:
        mx, my, g = (x1 + x2) / 2, (y1 + y2) / 2, 0.15
        others = [t for t in tags if t != (x1, x2, y1, y2)]
        spots = [(x2 + g + w / 2, my), (x1 - g - w / 2, my), (mx, y2 + g + h / 2), (mx, y1 - g - h / 2)]
        spots += [(x2 + g + w / 2, y2 - h / 2), (x2 + g + w / 2, y1 + h / 2), (x1 - g - w / 2, y2 - h / 2), (x1 - g - w / 2, y1 + h / 2)]
        spots += [(x2 + g + w / 2 + d, my) for d in (0.5, 1.0)] + [(x1 - g - w / 2 - d, my) for d in (0.5, 1.0)]
        best = None
        for cx, cy in spots:
            b = (cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2)
            if not hit(b, walls_) and not hit(b, others) and not hit(b, placed) and not hit(b, swings):
                best = (cx, cy, b); break
        if best is None:   # no clear spot: the first one clear of walls and tags, over a swing if need be
            for cx, cy in spots:
                b = (cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2)
                if not hit(b, walls_) and not hit(b, placed):
                    best = (cx, cy, b); break
        cx, cy, b = best or (mx, my, (mx - w / 2, mx + w / 2, my - h / 2, my + h / 2))
        pl.text(fid, cx, cy, sz, "Helvetica-Bold", ACC); placed.append(b)
    tags += placed
    st_ = STAIR
    tags += [(st_["flight1"][0], st_["flight2"][1], st_["flight1"][2], st_["landing"][3])]   # the stair's treads
    pl.room_names(5, GREY, corner=True, avoid=tags)
    def short(t):  # the item only (its first clause); full specs are in the schedules
        return re.split(r" \(|: |; |, ", t)[0]
    rows = [(f[0], short(f[2]) + (f" (x{f[7]})" if f[7] > 1 else "")) for f in FURNITURE]
    ky = PLAN_OY + (min(min(f[5] for f in FURNITURE), HY1 - T / 2) - 1.6) * pl.k   # top of the key: below the lowest item and the south wall
    s.note("Furniture key (full specs in the schedules)", 14 * mm, ky + 1 * mm, 7, INK, "Helvetica-Bold")
    limit = PW - 87 * mm                                     # stop short of the title block: smaller type when the key is long
    for size, cw in ((5.4, 59), (5.0, 54), (4.7, 50), (4.4, 46)):
        if key_columns(c, rows, 14 * mm, ky - 1 * mm, 12 * mm, cw * mm, size=size, dry=True) <= limit:
            break
    key_columns(c, rows, 14 * mm, ky - 1 * mm, 12 * mm, cw * mm, size=size)
    plan_furniture_scale(pl)
    c.showPage()


SECTIONS = {"A": ("X", CX, "North-south through the courtyard: utility and powder room, walkways, the open mutram, family living with the roof terrace above"),
            "B": ("Y", CY, "East-west through the courtyard: thinnai, foyer, oonjal link, walkways, the open mutram, the den walk-in, the DB cupboard and the stair, the gallery above")}


def sheet_working(c, num="A-104", title="Working plan, ground floor: clear sizes and sections"):
    s = Sheet(c, num, title, "1:75")
    pl = house_plan(s)
    pl.walls()
    pl.openings()
    pl.floor_extras()
    for r in ROOMS:
        rid, name, x1, x2, y1, y2, _ = r
        L, W = clear_dims(r)
        nm = short_name(name).upper()
        if rid == "R06":   # the stair: name and clear size turned along flight 1, beside its arrow
            pl.stair_label(f"{fmt_ft(L)} x {fmt_ft(W)}", ACC)
            continue
        if r[0] in ("R62", "R63"):   # the side walkways: along their length
            nm = "WALKWAY"
        sz = pl.fit(nm, "Helvetica-Bold", 5.8, L - 0.3)
        line2 = f"{fmt_ft(L)} x {fmt_ft(W)}"          # every size on this sheet is clear (see the note)
        s2 = pl.fit(line2, "Helvetica", 5, L - 0.3)
        two = s2 < 4.4   # too narrow for one line: split the size over two
        if two:
            s2 = pl.fit(max(f"{fmt_ft(L)} x", fmt_ft(W), key=len), "Helvetica", 4.6, L - 0.3)
        wf = max(c.stringWidth(nm, "Helvetica-Bold", sz), c.stringWidth(line2 if not two else f"{fmt_ft(L)} x", "Helvetica", s2)) / pl.k + 0.3
        cx, cy = pl.label_spot(r, wf, 0.6 + sz / pl.k * 0.7, 1.3 if two else 0.7)
        pl.halo_text(nm, cx, cy + 0.6, sz, "Helvetica-Bold")
        if two:
            pl.halo_text(f"{fmt_ft(L)} x", cx, cy - 0.3, s2, color=ACC); pl.halo_text(fmt_ft(W), cx, cy - 1.05, s2, color=ACC)
        else:
            pl.halo_text(line2, cx, cy - 0.4, s2, color=ACC)
    for name, (axis, c0, _) in (SECTIONS.items() if FLOOR[0] == "G" else ()):
        if axis == "X":
            y1, y2 = HY1 - 6.0, HY2 - 2.4   # the sheet's top edge is just past the north wall: the top bubble sits inside it
            pl.line(c0, y1, c0, y2, lw=0.7, color=RED, dash=(6, 2, 1, 2))
            for yy in (y1 - 0.8, y2 + 0.8):
                pl.circle(c0, yy, 0.8, lw=0.6, color=RED, fill=WHITE); pl.text(name, c0, yy, 6.5, "Helvetica-Bold", RED)
            pl.poly([(c0 - 0.9, y1 - 0.8), (c0 - 2.0, y1 - 0.8)], lw=0.8, color=RED)   # looking west
        else:
            x1, x2 = HX1 - 3.0, max(f[3][1] for f in SITE_FEATURES if f[0] == "STEPS") + 1.5
            pl.line(x1, c0, x2, c0, lw=0.7, color=RED, dash=(6, 2, 1, 2))
            for xx in (x1 - 0.8, x2 + 0.8):
                pl.circle(xx, c0, 0.8, lw=0.6, color=RED, fill=WHITE); pl.text(name, xx, c0, 6.5, "Helvetica-Bold", RED)
            pl.poly([(x2 + 0.8, c0 + 0.9), (x2 + 0.8, c0 + 2.0)], lw=0.8, color=RED)   # looking north
    pl.auto_dims(5)
    s.note("Room sizes (green) are clear: wall face to wall face after plaster. Grid dimensions are to wall centrelines.", 24 * mm, 30 * mm, 7, GREY)
    s.note(("Sections A-A (looking west) and B-B (looking north) on A-301. " if FLOOR[0] == "G" else "") + "Check every furniture item against the clear size before ordering.", 24 * mm, 25.5 * mm, 7, GREY)
    s.note("Column positions (by engineer) must avoid door swings, wardrobes and the TV wall.", 24 * mm, 21 * mm, 7, GREY)
    plan_furniture_scale(pl)
    c.showPage()


FLOOR_COLOURS = {"Athangudi handmade tile": "#F0DDB0", "Red oxide / Kota stone": "#E8C9B8", "Matt vitrified 2x2": "#E5E1D6", "Anti-skid ceramic, waterproofed": "#CFE0EC",
                 "Rough-dressed granite": "#D3CEC6", "Terracotta anti-skid tile, waterproofed": "#E9B98F"}
FLOOR_GROUPS = [(k, colors.HexColor(v), [r for r, f in FLOOR_FINISH.items() if f == k]) for k, v in FLOOR_COLOURS.items()]


def sheet_finishes(c, num="A-105", title="Floor finishes and levels, ground floor"):
    s = Sheet(c, num, title, "1:75")
    pl = house_plan(s)
    ids = {r[0] for r in ROOMS}
    for _, col, rooms in FLOOR_GROUPS:
        for rid in rooms:
            if rid in ids:
                r = room_of(rid); pl.rect(r[2], r[3], r[4], r[5], stroke=None, fill=col)
    pl.walls(fill=INK)
    pl.openings(tags=False)
    pl.floor_extras()
    falls = {"R07": "1:60 to drain", "R08": "1:60 to drain", "R40": "1:60 to drain", "R33": "1:60 to drain", "R39": "1:60 to drain", "R13": "1:80 to drain",
             "R37": "1:80 to its outlet", "R50": "to the court drain"}
    for r in ROOMS:
        rid, name, x1, x2, y1, y2, _ = r
        nm = short_name(name)
        if rid in ("R62", "R63"):
            nm = "Walkway"
        L = clear_dims(r)[0]
        sz = pl.fit(nm, "Helvetica-Bold", 5.2, L - 0.3)
        if rid == "R06":   # the stair: its foot is the lobby's level (A-301 has the risers); name only, beside the arrow
            pl.halo_text(nm, *pl.label_spot(r, c.stringWidth(nm, "Helvetica-Bold", sz) / pl.k + 0.3, 0.5, 0.3), sz, "Helvetica-Bold")
            continue
        wf = max(c.stringWidth(nm, "Helvetica-Bold", sz) / pl.k, 3.1) + 0.3
        cx, cy = pl.label_spot(r, wf, 0.8 + sz / pl.k * 0.7, 1.2)
        pl.halo_text(nm, cx, cy + 0.8, sz, "Helvetica-Bold")
        pl.level(cx - 1.2, cy - 0.6, floor_level(rid), 5)
        if rid in falls:   # the falls note: its own spot, clear of the door swings and of the name above
            ft = "falls " + falls[rid]
            fs = pl.fit(ft, "Helvetica", 4.4, x2 - x1 - 0.4)
            fw = c.stringWidth(ft, "Helvetica", fs) / pl.k + 0.2
            spot = (pl.label_spot((rid, name, x1, x2, y1, min(y2, cy - 0.9), None), fw, 0.25, 0.25, start=(cx, cy - 1.5), strict=True)
                    or pl.label_spot((rid, name, x1, x2, max(y1, cy + 1.6), y2, None), fw, 0.25, 0.25, start=(cx, cy + 2.0), strict=True)   # above the name
                    or (cx, cy - 1.5))
            fx, fy = spot
            pl.text(ft, fx, fy, fs, color=BLUE)
    if FLOOR[0] == "G":
        pl.level(HX2 + 2.0, HY1 - 4.0, LEVELS["FGL"], 5); pl.text("finished ground", HX2 + 2.6, HY1 - 4.9, 4.5, color=GREY, anchor="l")
    sw = lambda fill: (lambda x, y: s.c.setFillColor(fill) or s.c.setStrokeColor(GREY) or s.c.rect(x, y, 6 * mm, 3 * mm, stroke=1, fill=1))
    s.legend([(sw(col), name) for name, col, _ in FLOOR_GROUPS], 16 * mm, 52 * mm)
    tips = [
        "Skirting 4 in high, set flush with the plaster face (plaster stops in a groove above it), so no ledge collects dust.",
        "Bathrooms 12 mm below the bedroom floor with a sloped granite threshold: no raised step to trip on, water stays in.",
        "Walkway 1 in below the rooms (rain stays out) and one step above the sunken courtyard; the courtyard stone falls to its drain.",
        "First floor: the upper baths sit on sunk slabs and the roof terrace is a waterproofed slab: flood-test 48 h, then tile.",
        "Shower zone: linear drain at the far end, floor falls 1:60 only inside the wet zone; dry zone floor nearly flat.",
        "Thinnai steps, walkway and courtyard: rough-dressed or flamed stone. Polished granite is slippery when wet.",
        "Kitchen: mid-tone matt floor; white glossy tile shows every stain and is slippery with oil. Leave 5 mm expansion gaps at walls and every 15-20 ft.",
    ]
    s.bullets(tips, 105 * mm, 56 * mm, 215 * mm, 6.2, title="Floor detailing")
    plan_furniture_scale(pl)
    c.showPage()


def _hatch(pl, x1, x2, y1, y2, step=1.6, color=GREY, lw=0.3):
    """45-degree hatch clipped to a plan rectangle."""
    c = pl.c
    a, b = pl.p(x1, y1), pl.p(x2, y2)
    c.saveState()
    clip = c.beginPath(); clip.rect(a[0], a[1], b[0] - a[0], b[1] - a[1]); c.clipPath(clip, stroke=0, fill=0)
    c.setStrokeColor(color); c.setLineWidth(lw)
    k = x1 - (y2 - y1)
    while k < x2:
        pa, pb = pl.p(k, y1), pl.p(k + (y2 - y1), y2)
        c.line(pa[0], pa[1], pb[0], pb[1])
        k += step
    c.restoreState()


def _slope_arrow(pl, x, y, dx, dy, color=BLUE):
    """Slope arrow from (x, y) running downhill by (dx, dy), with an arrowhead."""
    pl.line(x, y, x + dx, y + dy, lw=0.5, color=color)
    n = math.hypot(dx, dy); ux, uy = dx / n, dy / n
    ex, ey = x + dx, y + dy
    pl.poly([(ex, ey), (ex - 0.8 * ux - 0.35 * uy, ey - 0.8 * uy + 0.35 * ux), (ex - 0.8 * ux + 0.35 * uy, ey - 0.8 * uy - 0.35 * ux)], lw=0.4, color=color, close=True, fill=color)


COPPER_C = colors.HexColor("#B87333")


def _runs(pieces):
    """Join the short roof-line pieces from geom.roof_lines into straight runs [(kind, a, b)]."""
    runs = []
    for k, a, b in pieces:
        if runs and runs[-1][0] == k and abs(runs[-1][2][0] - a[0]) < 1e-6 and abs(runs[-1][2][1] - a[1]) < 1e-6:
            runs[-1] = (k, runs[-1][1], b)
        else:
            runs.append((k, a, b))
    return runs


def _downhill(x, y, d=0.05):
    """Unit vector downhill on the top roof surface at (x, y)."""
    z = lambda u, v: roof_z(u, v) if roof_z(u, v) is not None else thinnai_roof_z(u, v)
    gx = (z(x + d, y) - z(x - d, y)) / (2 * d); gy = (z(x, y + d) - z(x, y - d)) / (2 * d)
    n = math.hypot(gx, gy)
    return -gx / n, -gy / n


def _ktext(pl, s_, x, y, size, font="Helvetica", color=INK, anchor="c"):
    """Plan text on a white knock-out box (legible over hatching and lines)."""
    w = pl.c.stringWidth(s_, font, size) / pl.k
    x1 = x - w / 2 if anchor == "c" else (x if anchor == "l" else x - w)
    pl.rect(x1 - 0.15, x1 + w + 0.15, y - 0.3 * size / 4, y + 0.75 * size / 4, stroke=None, fill=WHITE)
    pl.text(s_, x, y, size, font, color, anchor)


def sheet_roof(c):
    s = Sheet(c, "A-110", "Roof plan", "1:75")
    pl = Plan(s, 75, -28 * mm, 22 * mm)
    tile = colors.HexColor("#F6EFE6")
    o, ci, t, th = ROOF["ring"], ROOF["court_eave"], ROOF["terrace"], ROOF["thinnai"]
    w1, w2 = wing_rects()
    rr = ring_ridge_rect()
    slab = terrace_slab_z()
    # the ground-floor outer walls below, dashed
    pl.rect(HX1, HX2, HY1, HY2, stroke=GREY, lw=0.4, dash=(2, 2))
    # ring roof and the thinnai lean-to past its east eave
    pl.rect(o[1], th[1], th[2], th[3], lw=0.9, fill=tile)
    pl.rect(*o, lw=0.9, fill=tile)
    pl.rect(o[1] - 0.2, o[1] + 0.2, th[2] + 0.05, th[3] - 0.05, stroke=None, fill=tile)      # the lean-to is the ring's slope carried on: no eave line
    # the terrace (to its parapet: no tiled eave past it) and the open court are holes in the ring
    hole = ring_holes()[-1]
    pl.rect(hole[0], hole[1], hole[2], hole[3] + 0.25, stroke=None, fill=WHITE)
    ch = ROOF["terrace_chajja"]
    pl.rect(*ch, lw=0.6, fill=LIGHT)                                                              # 2 ft RCC chajja over the living's north windows
    pl.rect(*t, lw=0.9, fill=WHITE)
    _hatch(pl, *t)
    pl.rect(*ci, lw=0.9, fill=colors.HexColor("#DCEAF5"))
    pl.rect(*CT, stroke=GREY, lw=0.3, dash=(1.5, 1.5))
    # ring ridges, hips and valleys where the ring is the top roof
    runs = _runs(roof_lines())
    def draw_runs(src):
        for k, a, b in runs:
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            if (wing_roof_z(*m) is not None) != (src == "wing"):
                continue
            if k == "valley":
                pl.line(a[0], a[1], b[0], b[1], lw=0.8, color=BLUE, dash=(3, 1.5))
            else:
                pl.line(a[0], a[1], b[0], b[1], lw=1.0 if k == "ridge" else 0.7)
    draw_runs("ring")
    # gutters: the ring's outer eave (where it is the top roof, the thinnai front apart), the court's inner eave, the thinnai's front
    def gutter_along(x1, y1, x2, y2, nx, ny, ok):
        n = int(max(abs(x2 - x1), abs(y2 - y1)) / 0.25)
        on = None
        for k in range(n + 1):
            x, y = x1 + (x2 - x1) * k / n, y1 + (y2 - y1) * k / n
            good = ok(x, y)
            if good and on is None:
                on = (x, y)
            if (not good or k == n) and on is not None:
                pl.line(on[0] + nx, on[1] + ny, x + nx, y + ny, lw=0.5, color=BLUE)
                on = None
    ring_top = lambda x, y: ring_z(x - 0.3 * (x >= o[1]) + 0.3 * (x <= o[0]), y - 0.3 * (y >= o[3]) + 0.3 * (y <= o[2])) is not None and wing_roof_z(x, y) is None
    gutter_along(o[0], o[2], o[1], o[2], 0, -0.35, ring_top)
    gutter_along(o[0], o[3], o[1], o[3], 0, 0.35, ring_top)
    gutter_along(o[1], o[2], o[1], o[3], 0.35, 0, lambda x, y: ring_top(x, y) and not (th[2] < y < th[3]))
    pl.rect(ci[0] + 0.3, ci[1] - 0.3, ci[2] + 0.3, ci[3] - 0.3, stroke=BLUE, lw=0.4)
    pl.line(th[1] + 0.35, th[2], th[1] + 0.35, th[3], lw=0.5, color=BLUE)
    # terrace edge walls and parapet (the wing's east eave hides their west ends)
    vx, vy1, vy2, _ = ROOF["verge_east"]
    pl.rect(t[0], t[1], t[2] - 0.2, t[2] + 0.2, stroke=INK, fill=INK, lw=0.3)                     # south upstand / raking verge
    pl.rect(vx - 0.2, vx + 0.2, vy1, vy2, stroke=INK, fill=INK, lw=0.3)                           # east verge wall
    pl.rect(t[0], t[1], t[3] - 0.15, t[3] + 0.15, stroke=INK, lw=0.4, fill=LIGHT)                 # north jali parapet
    (gx1, gx2), (gy1, gy2) = corner_guard_runs()
    pl.rect(gx1, gx2 + 0.35, t[2] - 0.35, t[2] + 0.35, stroke=INK, fill=INK, lw=0.3)              # the level corner guard, south run
    pl.rect(vx - 0.35, vx + 0.35, gy1 - 0.35, gy2, stroke=INK, fill=INK, lw=0.3)                  # and its east run
    for px, py in TERRACE_POSTS:
        pl.rect(px - 0.25, px + 0.25, py - 0.25, py + 0.25, fill=INK, lw=0.3)
    # the upper wing: an L of two hipped rectangles, one valley at the re-entrant corner
    assert w1[0] == w2[0] and w1[3] == w2[3] and w2[1] > w1[1] and w2[2] > w1[2]
    Lpoly = [(w1[0], w1[2]), (w1[1], w1[2]), (w1[1], w2[2]), (w2[1], w2[2]), (w2[1], w2[3]), (w1[0], w1[3])]
    pl.rect(*w1, stroke=None, fill=tile); pl.rect(*w2, stroke=None, fill=tile)
    pl.poly(Lpoly, lw=1.1, close=True)
    gut = []                                                                                       # its eave gutter, 0.35 ft outside the eave
    for k_ in range(len(Lpoly)):
        (ax, ay), (bx, by), (qx, qy) = Lpoly[k_ - 1], Lpoly[k_], Lpoly[(k_ + 1) % len(Lpoly)]
        n1 = (math.copysign(1, by - ay) if by != ay else 0, -math.copysign(1, bx - ax) if bx != ax else 0)
        n2 = (math.copysign(1, qy - by) if qy != by else 0, -math.copysign(1, qx - bx) if qx != bx else 0)
        gut.append((bx + 0.35 * (n1[0] + n2[0]), by + 0.35 * (n1[1] + n2[1])))
    pl.poly(gut, lw=0.5, color=BLUE, close=True)
    draw_runs("wing")
    # the wing's walls below, dashed
    for wr in ROOF["wing_walls"]:
        pl.rect(*wr, stroke=GREY, lw=0.3, dash=(1, 1.5))
    # jharokha bays (under the wing's eaves), their kerbs and the valley saddle
    for k, j in enumerate(JHAROKHAS):
        pl.rect(j[0], j[1], j[2], j[3], stroke=BROWN, lw=0.6, dash=(2, 1))
        pl.text(f"J{k + 1}", (j[0] + j[1]) / 2, (j[2] + j[3]) / 2 - 0.5, 4.4, "Helvetica-Bold", BROWN)
    for sd in ROOF["saddles"]:
        _hatch(pl, sd[1], sd[2], sd[3], sd[4], step=0.5, color=COPPER_C, lw=0.4)
        pl.rect(sd[1], sd[2], sd[3], sd[4], stroke=COPPER_C, lw=0.6)
    j1, j2 = JHAROKHAS
    sd0 = ROOF["saddles"][0]
    # the J2 note: one wrapped block on the clear east slope of the west wing, just south-west of the pocket gutter, with a short leader
    jn = Paragraph(f"<b>J2 sits on the ring's NW valley:</b> a lead-lined pocket gutter beside its west kerb ({fmt_ft(sd0[5])}) falls south past "
                   f"the kerb corner to the valley. J1 and J2 are framed up to the wing soffit (the eave is their roof), "
                   f"{fmt_ft(min(jharokha_clearance(j) for j in JHAROKHAS))} clear of the ring roof under their kerbs.",
                   ParagraphStyle("j2", fontName="Helvetica", fontSize=3.9, leading=4.6, textColor=BROWN))
    nx1, nx2, ntop = 21.8, 27.1, 29.9                          # between the wing's ridge (x 21.25) and J1 / the wing's east wall (x 27.5)
    jw, jh = jn.wrap((nx2 - nx1) * pl.k, 40 * mm)
    jx, jy = pl.p(nx1, ntop)
    pl.rect(nx1 - 0.1, nx2 + 0.1, ntop - jh / pl.k - 0.1, ntop + 0.1, stroke=None, fill=WHITE)
    jn.drawOn(c, jx, jy - jh)
    assert ntop - jh / pl.k > 23.5, "the J2 note runs into the wing's slope arrow"
    pl.line(nx2 + 0.1, ntop - 0.3, sd0[1] + 0.3, sd0[3] + 0.3, lw=0.3, color=BROWN)   # short leader to the pocket gutter
    # the wing's gutters: the box gutter at the re-entrant corner (the high point), falls to the spreaders and the downpipe, overflow spout
    bxg, byg, *_mm, spout = ROOF["wing_box_gutter"]
    pl.rect(bxg - 0.5, bxg + 0.5, byg - 0.5, byg + 0.5, stroke=BLUE, fill=WHITE, lw=0.7)
    pl.line(bxg, byg, *spout, lw=0.6, color=BLUE, dash=(1, 0.6))
    _ktext(pl, "BOX GUTTER", bxg - 0.75, byg - 1.25, 4.2, "Helvetica-Bold", BLUE, anchor="r")   # south-west of the box, above J1, clear of the H and the fall arrows
    for (hx, hy), (lx, ly) in ROOF["wing_gutter_runs"]:
        L_ = math.hypot(lx - hx, ly - hy); ux, uy = (lx - hx) / L_, (ly - hy) / L_
        mx, my = (hx + lx) / 2, (hy + ly) / 2
        nx_, ny_ = (0.9, 0) if abs(uy) > 0.5 else (0, -0.9 if my < w2[3] - 0.1 else 0.9)
        _slope_arrow(pl, mx + nx_ - 0.8 * ux, my + ny_ - 0.8 * uy, 1.6 * ux, 1.6 * uy)
    for (hx, hy) in {r[0] for r in ROOF["wing_gutter_runs"]} - {r[1] for r in ROOF["wing_gutter_runs"]}:
        pl.text("H", hx + 1.0, hy - 1.0 if hy > w1[2] + 0.1 else hy + 0.5, 3.6, "Helvetica-Bold", BLUE)
    # the terrace: tanks on their stand (partly under the wing's eave), labels, outlet, edge-wall notes
    for p in PLUMBING_F1:
        if p[0] == "TK":
            pl.circle(p[1], p[2], 1.333, lw=0.5, color=BLUE, dash=(2, 1))
    tks = [p for p in PLUMBING_F1 if p[0] == "TK"]
    _ktext(pl, "2 TANKS ON A STAND", w2[1] + 0.8, tks[0][2] - 2.3, 3.8, color=BLUE, anchor="l")   # east of the wing's eave gutter (x 35.85)
    tx = (t[0] + t[1]) / 2 + 1.5
    _ktext(pl, "ROOF TERRACE: FLAT SLAB", tx, 40.4, 4.8, "Helvetica-Bold")
    _ktext(pl, f"slab {fmt_lvl(slab)}; tiled canopy on 6 steel posts", tx, 39.0, 4.0)
    _ktext(pl, f"at {fmt_lvl(slab + ROOF['canopy'])}, its deck under the wing gutter", tx, 37.8, 4.0)
    ox_, oy_ = ROOF["terrace_outlet"]; dpx, dpy = ROOF["downpipes"][-1]
    pl.circle(ox_, oy_, 0.45, lw=0.6, color=BLUE, fill=BLUE)
    pl.line(ox_, oy_, dpx, dpy, lw=0.8, color=BLUE)
    _ktext(pl, "SIDE-ENTRY OUTLET", ox_ - 0.8, oy_ - 1.3, 3.8, "Helvetica-Bold", BLUE, anchor="r")
    pl.text("2 FT RCC CHAJJA AT SLAB LEVEL OVER W75/W76", (ch[0] + ch[1]) / 2 + 1.0, ch[2] + 0.75, 3.6)
    vem = max(verge_east_h(gy2 + 0.05 + 0.05 * k) for k in range(int((t[3] - gy2) / 0.05)))
    _ktext(pl, f"SOUTH EDGE: {fmt_ft(ROOF['upstand'])} UPSTAND + RAILING;", tx - 1.5, t[2] + 1.9, 3.8)
    _ktext(pl, f"CORNER GUARD {fmt_ft(ROOF['corner_guard'])} LEVEL, SOLID (EDGE BEAMS BELOW)", tx - 1.5, t[2] + 0.8, 3.8, "Helvetica-Bold")
    pl.line(vx + 0.4, 42.0, o[1] + 1.2, 42.0, lw=0.3)
    for i_, t_ in enumerate(("EAST EDGE: LEVEL CORNER", f"GUARD FOR {fmt_ft(gy2 - gy1)} NORTH", "OF THE SE CORNER, THEN", "A STEPPED TRANSITION", "TO A VERGE 6 IN OVER", f"THE ROOF (UP TO {fmt_ft(vem)})")):
        pl.text(t_, o[1] + 1.4, 42.3 - i_ * 1.2, 3.8, anchor="l")
    # downpipes and the wing's spreaders
    for dx, dy in ROOF["downpipes"]:
        pl.circle(dx, dy, 0.4, lw=0.6, color=BLUE, fill=WHITE)
    for sx, sy in ROOF["wing_spreaders"]:
        pl.circle(sx, sy, 0.35, lw=0.5, color=BLUE, fill=BLUE)
        ux, uy = _downhill(sx + 0.6, sy - 0.6 if sy < t[2] else sy - 0.6)
        pl.line(sx, sy, sx + 1.6 * ux, sy + 1.6 * uy, lw=0.5, color=BLUE)
    # thinnai lean-to
    for px, py in THINNAI_PILLARS:
        pl.circle(px, py, 0.33, lw=0.4, color=GREY, dash=(1, 1))
    for f in FURNITURE:
        if f[0] in ("F125", "F126"):
            pl.circle((f[3] + f[4]) / 2, (f[5] + f[6]) / 2, 0.3, lw=0.5, color=COPPER_C, fill=COPPER_C)
    pl.text("THINNAI", (o[1] + th[1]) / 2, CY + 3.0, 3.8, "Helvetica-Bold")
    pl.text("LEAN-TO", (o[1] + th[1]) / 2, CY + 1.9, 3.8, "Helvetica-Bold")
    pl.text(f"eave {fmt_lvl(thinnai_roof_z(th[1], CY))}", (o[1] + th[1]) / 2, CY - 1.6, 3.8)
    pl.text(f"{fmt_ft(thinnai_headroom())} clear", (o[1] + th[1]) / 2, CY - 2.8, 3.8)
    # courtyard
    for i_, t_ in enumerate(("MUTRAM, OPEN", "TO THE SKY:", "STEEL GRILLE", f"AT {fmt_lvl(ROOF['grille_z'])}")):
        pl.text(t_, CX, CY + 1.9 - i_ * 1.3, 4.0, "Helvetica-Bold" if i_ < 3 else "Helvetica", BLUE)
    pl.circle(CT[1] - 1.0, CT[2] + 1.0, 0.4, lw=0.6, color=BLUE, fill=BLUE)
    pl.text("CD", CT[1] - 1.0, CT[2] + 1.6, 3.6, "Helvetica-Bold", BLUE)
    # slope arrows, downhill on the top surface
    for ax, ay in ((40, (o[2] + rr[2]) / 2), (40, (rr[2] + ci[2]) / 2), ((rr[1] + o[1]) / 2, 20), ((ci[1] + rr[1]) / 2, 25),
                   (38, (ci[3] + t[2]) / 2), (55.2, 36.5), (53.5, (rr[3] + o[3]) / 2 + 2.6), (36.5, 16.4), (60.2, 31.5),
                   ((w1[0] + w1[1]) / 2 - 3.5, 22), ((w1[0] + w1[1]) / 2 + 3.5, 22), ((w1[0] + w1[1]) / 2, 5.0), (26.0, (w2[3] + (w2[2] + w2[3]) / 2) / 2 + 0.3),
                   (w2[1] - 2.2, (w2[2] + w2[3]) / 2), (31.5, w2[2] + 2.8)):
        ux, uy = _downhill(ax, ay)
        _slope_arrow(pl, ax - 1.3 * ux, ay - 1.3 * uy, 2.6 * ux, 2.6 * uy)
    pl.text(f"{ROOF['pitch']} deg", 42.6, (o[2] + rr[2]) / 2 - 0.4, 4.2, color=BLUE)
    # levels on the plan
    pl.text(f"RING RIDGE {fmt_lvl(ridge_z())}", 39.0, rr[2] + 0.6, 4.4, "Helvetica-Bold")
    pl.text(f"RING EAVES {fmt_lvl(eave_z())}", 42.0, o[2] + 0.6, 4.2)
    wcx = (w1[0] + w1[1]) / 2
    pl.text("UPPER WING: L-SHAPED HIPPED ROOF", wcx + 0.5, 16.6, 4.4, "Helvetica-Bold", anchor="l")
    pl.text(f"ridge {fmt_lvl(wing_ridge_z())}, eaves {fmt_lvl(wing_eave_z())}", wcx + 0.5, 15.3, 4.0, anchor="l")
    pl.text("2 ft eaves all round", wcx + 0.5, 14.1, 4.0, anchor="l")
    # dimensions
    pl.hdim(o[0], o[1], o[2] - 2.2, size=5); pl.hdim(o[1], th[1], o[2] - 2.2, size=5)
    pl.vdim(o[2], o[3], o[0] - 1.6, size=5)
    pl.hdim(w1[0], w1[1], o[3] + 1.6, size=5); pl.hdim(w1[1], w2[1], o[3] + 1.6, size=5); pl.hdim(t[0], t[1], o[3] + 3.6, size=5)
    pl.north(225 * mm, 262 * mm)
    s.legend([(lambda x, y: (c.setStrokeColor(INK), c.setLineWidth(1.0), c.line(x, y, x + 6 * mm, y)), "Ridge / hip"),
              (lambda x, y: (c.setStrokeColor(BLUE), c.setLineWidth(0.8), c.setDash([3, 1.5], 0), c.line(x, y, x + 6 * mm, y), c.setDash()), "Valley"),
              (lambda x, y: (c.setStrokeColor(BLUE), c.setLineWidth(0.5), c.line(x, y, x + 6 * mm, y)), "Gutter"),
              (lambda x, y: (c.setStrokeColor(BLUE), c.setFillColor(WHITE), c.circle(x + 3 * mm, y, 1.3, stroke=1, fill=1)), f"Downpipe ({len(ROOF['downpipes'])})"),
              (lambda x, y: (c.setStrokeColor(BLUE), c.setFillColor(BLUE), c.circle(x + 3 * mm, y, 1.1, stroke=1, fill=1)), f"Spreader from the wing gutter ({len(ROOF['wing_spreaders'])})"),
              (lambda x, y: (c.setStrokeColor(BROWN), c.setDash([2, 1], 0), c.rect(x, y - 1 * mm, 6 * mm, 2 * mm), c.setDash()), "Jharokha bay below the wing eave"),
              (lambda x, y: (c.setStrokeColor(COPPER_C), c.setFillColor(COPPER_C), c.rect(x, y - 1 * mm, 6 * mm, 2 * mm, stroke=1, fill=1)), "Lead-lined pocket gutter at J2's kerb"),
              (lambda x, y: (c.setStrokeColor(INK), c.setFillColor(INK), c.rect(x, y - 0.7 * mm, 6 * mm, 1.4 * mm, stroke=1, fill=1)), "Terrace edge wall (thick: the level corner guard)"),
              (lambda x, y: (c.setFillColor(BLUE), c.setFont("Helvetica-Bold", 6), c.drawString(x + 2 * mm, y - 1 * mm, "H")), "Gutter high point (arrows: fall)")],
             20 * mm, 280 * mm, 6.0)
    lv = [["Level", "Above ground"],
          ["Ring eaves (outer, inner), court grille", fmt_lvl(eave_z())], ["Ring ridge", fmt_lvl(ridge_z())],
          ["Wing eaves / ridge", fmt_lvl(wing_eave_z()) + " / " + fmt_lvl(wing_ridge_z())],
          ["Terrace slab / canopy", fmt_lvl(slab) + " / " + fmt_lvl(slab + ROOF["canopy"])],
          ["Thinnai lean-to eave", fmt_lvl(thinnai_roof_z(th[1], CY))],
          ["Jharokha bay undersides", fmt_lvl(jharokha_base_z(j1))],
          ["Terrace corner guard (top)", fmt_lvl(slab + ROOF["corner_guard"])]]
    s.table(lv, [44, 22], 92 * mm, 282 * mm, None, 5.8)
    ll = roof_line_lengths()
    tips = [
        f"Ring roof at {ROOF['pitch']} deg: tiled slopes rise from the outer eave ({fmt_lvl(eave_z())}) and from the inner eave over the court to a ridge midway in each band ({fmt_lvl(ridge_z())}). It stops against the upper wing's walls on the west and north-west and at the terrace's edge walls; there is no ring eave past the terrace's north parapet.",
        f"Upper wing: an L of two hipped roofs of the same {fmt_ft(w1[1] - w1[0])} span (the west band and the north arm over the family room), ridge {fmt_lvl(wing_ridge_z())}, 2 ft eaves all round at {fmt_lvl(wing_eave_z())}, one valley at the re-entrant corner over the north walkway. Trusses bolted to the first-floor ring beam.",
        f"Where the ring roof meets the wing's walls: stepped apron flashing chased into the wall. The wing's re-entrant corner has a soldered internal box gutter ({ROOF['wing_box_gutter'][2]} x {ROOF['wing_box_gutter'][3]} x {ROOF['wing_box_gutter'][4]} mm) that takes the wing valley's tray: it is the high point (H) of both courtyard-side gutters, which fall 1:200 away from it to the spreaders; a 50 mm overflow spout drops onto the ring's NW valley; no downpipe at the corner. The east gutter over the terrace falls north and turns west along the north eave to the downpipe on a swan-neck.",
        f"Terrace edges: the south edge is a {fmt_ft(ROOF['upstand'])} RCC upstand (6 in over the walkway roof) under the 4 ft railing. At the south-east corner, where the east band's ridge runs into the edge, it becomes a LEVEL solid guard wall {fmt_ft(ROOF['corner_guard'])} high (6 in or more over the ridge end) along the last {fmt_ft(gx2 - gx1)} of the south edge to the south-east corner and {fmt_ft(gy2 - gy1)} up the east edge from that corner, where the ring's NE hip crosses it and the guard steps down to the verge (a stepped transition); the roof abuts it with step flashing and lead counter-flashing in a chase, the ridge end capped into the chase. RCC edge beams carry it over the open family room (about {gx2 - RING[1]:.1f} ft and {__import__('model')._NY - gy1:.1f} ft with no wall below). North of the guard the east edge is a verge wall 6 in over the roof (up to {fmt_ft(vem)}, under 2'-11\" along the daybed) with the railing on it. The roof falls away from or along every wall: no box gutter.",
        "Terrace drainage: the slab falls 1:80 to a side-entry outlet through the foot of the north parapet into the downpipe's rainwater head; a 2 ft RCC chajja off the north edge beam at slab level shades the living's north windows W75/W76, the downpipe passing through it in a sleeve.",
        f"Canopy: light tiles on a steel frame on the six posts at {fmt_lvl(slab + ROOF['canopy'])}; its deck slips under the wing's east eave gutter, which hangs 2 ft over the terrace, with 2 in to spare.",
        f"Jharokhas: each bay stands on a {fmt_ft(ROOF['jharokha_kerb'])} flashed kerb through the walkway roof (back-gutter up-slope, apron down-slope), under the wing's eave. The bays have no roofs of their own: the teak frame runs up to the wing's soffit, closed with a timber soffit board sealed to the fascia, so the 2 ft eave is the bay roof; the gutter hangs outboard on fascia brackets, its bottom 2 in or more above the casement heads. J2's west kerb sits on the ring's NW valley: a lead-lined pocket gutter beside it falls south past the kerb corner to the valley at the wing's re-entrant corner.",
        f"Thinnai lean-to: the ring's east slope carried on from the east wall at the same pitch to its eave {fmt_ft(th[1] - THINNAI_PILLARS[0][0])} past the turned pillars ({fmt_lvl(thinnai_roof_z(th[1], CY))}); {fmt_ft(thinnai_headroom())} clear over the platform at the pillars; its front gutter feeds the two copper rain chains into the granite basins.",
        f"Downpipes ({len(ROOF['downpipes'])}): 0.7 ft off the walls, 1 ft or more clear of every window and door, to the rain lines and the sump filter. The ring's south gutter is {ROOF['ring_south_gutter_mm']} mm (one downpipe: the south pipe strip is full of soil and grey runs). Valleys: 12 in GI/aluminium. Ridges {ll['ridge'] * 0.3048:.0f} m, hips {ll['hip'] * HIP_K * 0.3048:.0f} m and valleys {ll['valley'] * HIP_K * 0.3048:.0f} m on the slope.",
        "Every tile along eaves, hips, valleys and ridges clipped or screwed; every third row elsewhere (cyclone winds lift the edges first). Leave a 25 mm conduit from roof to DB for future solar PV.",
    ]
    s.bullets(tips, 240 * mm, 230 * mm, 90 * mm, 5.2, title="Roof detailing")
    c.showPage()


def _first(t, n=70):
    """The first clause of a long note, for a schedule cell (the full text is in the workbook)."""
    t = re.split(r" \(|; |: ", t)[0]
    return t   # the whole first clause: the cell wraps (no "..." truncation)


def sheet_schedules(c):
    s = Sheet(c, "A-601", "Schedules", "-")
    rd = [["ID", "Room", "Centreline", "Clear", "Sq ft"]]
    tot = 0
    for fl in ("G", "F1"):
        with on_floor(fl):
            rd.append(["", f"<b>{FLOOR_NAMES[fl]}</b>", "", "", ""])
            for r in ROOMS:
                L, W = room_dims(r); cl, cw = clear_dims(r); tot += cl * cw
                rd.append([r[0], short_name(r[1]), f"{fmt_ft(L)} x {fmt_ft(W)}", f"{fmt_ft(cl)} x {fmt_ft(cw)}", f"{cl * cw:.0f}"])
    rd.append(["", "Total (clear, both floors)", "", "", f"{tot:.0f}"])
    top = PH - 25 * mm
    h = s.table(rd, [11, 28, 23, 23, 10], 16 * mm, top, "Room schedule", 5.6)   # the ID column fits R16N / R36A on one line
    fits = lambda used, t: (t - used) >= 12 * mm
    dd = [["ID", "Location", "Width", "Type", "Vent"]] + [[d[0], _first(d[6], 30), fmt_ft(d[4] - d[3]), _first(d[7], 30), TRANSOM_LABELS.get(TRANSOMS.get(d[0]), "-")] for d in both("DOORS")]
    hd = s.table(dd, [9, 36, 10, 33, 16], 16 * mm, top - h - 9 * mm, "Door schedule (heights 7'-0\"; vents 7'-6\" to 9'-0\")", 5.0)
    assert fits(hd, top - h - 9 * mm), "the door schedule runs off the sheet"
    def face(fl, w):
        k = (w[1], w[2])
        if k in (("X", HY1),): return "S"
        if k in (("X", HY2),): return "N"
        if k in (("Y", HX1),): return "W"
        if k in (("Y", HX2),) or (fl == "F1" and k == ("Y", RING[0])): return "E"
        if k in (("X", RING[2]), ("X", RING[3]), ("Y", RING[0]), ("Y", RING[1])): return "Court"   # upstairs: the jharokha over the court (W47)
        return "In"
    wd = [["ID", "Room", "Wall", "Width", "Sill", "Head", "Type"]]
    for fl in ("G", "F1"):
        with on_floor(fl):
            wd += [[w[0], w[7] + (" (1st)" if fl == "F1" else ""), face(fl, w), fmt_ft(w[4] - w[3]), fmt_ft(w[5]), fmt_ft(w[6]), _first(w[8], 60)] for w in WINDOWS]
    wd += [[o[0], "Roof", "-", "-", "-", "-", o[1]] for o in OTHER_OPENINGS]
    assert fits(s.table(wd, [9, 25, 9, 10, 10, 10, 37], 126 * mm, top, "Window and vent schedule (sill/head above floor)", 5.2), top), "the window schedule runs off the sheet"
    fd = [["Space", "Floor", "Walls / skirting", "Ceiling"]] + [[_first(f[0], 40), _first(f[1], 55), _first(f[2], 55), _first(f[3], 45)] for f in FINISHES]
    assert fits(s.table(fd, [20, 24, 24, 22], 236 * mm, top, "Finishes (in short; full text in the workbook)", 5.2), top), "the finishes table runs off the sheet"
    c.showPage()
