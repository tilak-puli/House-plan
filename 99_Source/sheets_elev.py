"""Elevations (A-201, A-202) and sections (A-301), all derived from model levels and roof geometry."""
from sheetlib import *
from sheets_arch import SECTIONS

F = LEVELS["FFL"]
H = LEVELS["wall_top"]
TILE = colors.HexColor("#C98B6B")
GABLE = colors.HexColor("#F1E9DA")
WALLC = colors.HexColor("#F7F4EE")
HATCH = colors.HexColor("#BDBDBD")
LANTERN_TOP = vent_top_z()
PILLAR_TOP = F + 9.3

# faces: wall line, u mapping, plan extent, title
FACES = {
    "S": dict(line=("X", 3), u=lambda x, y: x, title="South elevation"),
    "N": dict(line=("X", 25), u=lambda x, y: SITE["l"] - x, title="North elevation"),
    "E": dict(line=("Y", 65), u=lambda x, y: y, title="East elevation (road side)"),
    "W": dict(line=("Y", 5), u=lambda x, y: SITE["w"] - y, title="West elevation"),
}


def _poly(e, pts, fill, stroke=INK, lw=0.6):
    e.poly(pts, lw=lw, color=stroke, close=True, fill=fill)


def _window(e, u1, u2, w, shade=True):
    sill, head = F + w[5], F + w[6]
    jali = "jali" in w[8].lower()
    e.rect(u1, u2, sill, head, lw=0.5, fill=colors.HexColor("#8E6B4E") if jali else colors.HexColor("#B9CCD3"))
    if jali:
        n = max(2, int((u2 - u1) / 0.6))
        for i in range(1, n): e.line(u1 + i * (u2 - u1) / n, sill, u1 + i * (u2 - u1) / n, head, lw=0.2, color=WHITE)
    else:
        e.line((u1 + u2) / 2, sill, (u1 + u2) / 2, head, lw=0.3)
    if shade:
        e.rect(u1 - 0.5, u2 + 0.5, head + 0.2, head + 0.45, lw=0.4, fill=WALLC)
    e.text(w[0], (u1 + u2) / 2, sill - 0.7, 4.6, color=ACC)


def _roof_long(e, u):
    x1, x2, y1, y2 = ROOF["hip"]
    w = (y2 - y1) / 2
    ez, rz = eave_z(), ridge_z()
    _poly(e, [(u(x1, 0), ez), (u(x2, 0), ez), (u(x2 - w, 0), rz), (u(x1 + w, 0), rz)], TILE)
    (va, vb), re_ = gable_valleys()
    gx2 = ROOF["gable"][1]
    gz = eave_z() + ROOF["gable_lift"]
    _poly(e, [(u(va[0][0], 0), gz), (u(gx2, 0), gz), (u(gx2, 0), gable_ridge_z()), (u(re_[0], 0), gable_ridge_z())], TILE, lw=0.5)
    sx1, sx2, _, _ = ROOF["skylight"]
    _ventilator(e, *sorted((u(sx1, 0), u(sx2, 0))))
    e.line(u(x1, 0), ez, u(x2, 0), ez, lw=1.2, color=BROWN)  # fascia + gutter


def _ventilator(e, a, b):
    """Ventilator seen from the side: upstand, louvre band, hipped cap."""
    rz, sz = ridge_z(), vent_sill_z()
    e.rect(a, b, rz - 0.3, sz, lw=0.5, fill=GABLE)
    e.rect(a, b, sz, LANTERN_TOP, lw=0.5, fill=colors.HexColor("#8E6B4E"))
    n = 7
    for i in range(1, n): e.line(a, sz + i * (LANTERN_TOP - sz) / n, b, sz + i * (LANTERN_TOP - sz) / n, lw=0.3, color=WHITE)
    o = ROOF["vent_overhang"]
    _poly(e, [(a - o, LANTERN_TOP), (b + o, LANTERN_TOP), ((a + b) / 2, vent_apex_z())], TILE, lw=0.6)


def _roof_end(e, u, east):
    x1, x2, y1, y2 = ROOF["hip"]
    ez, rz = eave_z(), ridge_z()
    _poly(e, [(u(0, y1), ez), (u(0, y2), ez), (u(0, (y1 + y2) / 2), rz)], TILE)
    _, _, sy1, sy2 = ROOF["skylight"]
    _ventilator(e, *sorted((u(0, sy1), u(0, sy2))))
    e.line(u(0, y1), ez, u(0, y2), ez, lw=1.2, color=BROWN)
    if east:
        gx1, gx2, ya, yb = ROOF["gable"]
        gz = ez + ROOF["gable_lift"]
        _poly(e, [(u(0, ya), gz), (u(0, yb), gz), (u(0, (ya + yb) / 2), gable_ridge_z())], GABLE, lw=0.8)
        e.poly([(u(0, ya - 0.3), gz - 0.15), (u(0, (ya + yb) / 2), gable_ridge_z() + 0.35), (u(0, yb + 0.3), gz - 0.15)], lw=1.4, color=BROWN)
        for c0 in (-1.6, 0, 1.6):
            yc = (ya + yb) / 2 + c0
            e.rect(u(0, yc - 0.55), u(0, yc + 0.55), gz + 1.1, gz + 2.3 - abs(c0) * 0.25, lw=0.4, fill=colors.HexColor("#8E6B4E"))


def _ground(e, u1, u2):
    e.line(u1, 0, u2, 0, lw=1.0)
    e.text("FINISHED GROUND", u1 + 3, -0.8, 4.6, color=GREY, anchor="l")


def _levels(e, u):
    for z, lab in ((0, "FGL +0'-0\""), (F, f"FFL {fmt_lvl(F)}"), (F + LEVELS["door_head"], f"Lintel {fmt_lvl(F + LEVELS['door_head'])}"),
                   (F + H, f"Ring beam {fmt_lvl(F + H)}"), (eave_z(), f"Eaves {fmt_lvl(eave_z())}"), (ridge_z(), f"Ridge {fmt_lvl(ridge_z())}")):
        e.lvl(u, z, lab, 5)


def elevation(e, face):
    f = FACES[face]
    u = f["u"]
    axis, c0 = f["line"]
    if face in ("S", "N"):
        _ground(e, u(-2, 0) if face == "S" else u(77, 0), u(77, 0) if face == "S" else u(-2, 0))
        xa, xb = (5, 65)
        lo, hi = sorted((u(xa - 0.375, 0), u(xb + 0.375, 0)))
        e.rect(lo, hi, 0, F, lw=0.6, fill=colors.HexColor("#B8B2A8"))
        if face == "S":
            e.rect(lo, hi, F, F + H, lw=0.6, fill=WALLC)
            segs = sorted((w[2], w[3]) for w in WALLS if (w[0], w[1]) == ("X", 3))
            for (_, e1), (s2, _) in zip(segs, segs[1:]):  # open bays in the south wall (wet area)
                a_, b_ = sorted((u(e1 + 0.375, 0), u(s2 - 0.375, 0)))
                e.rect(a_, b_, LEVELS["wet_area"], F + 8, lw=0.5, fill=colors.HexColor("#5A5048"))
                e.text("OPEN WET AREA", (a_ + b_) / 2, F + 4, 4.4, color=WHITE)
        else:
            a, b = sorted((u(5 - 0.375, 0), u(59, 0)))
            e.rect(a, b, F, F + H, lw=0.6, fill=WALLC)
            a, b = sorted((u(59, 0), u(65.375, 0)))
            e.rect(a, b, F, F + H, lw=0.3, fill=colors.HexColor("#E9E4DA"))  # recessed kitchen / poomukham back
            for px, py in PILLARS:
                if py > 24:
                    e.rect(u(px, 0) - 0.33, u(px, 0) + 0.33, LEVELS["poomukham"], PILLAR_TOP, lw=0.5, fill=colors.HexColor("#6B4A2E"))
            e.rect(*sorted((u(59, 0), u(63.8, 0))), LEVELS["poomukham"], LEVELS["poomukham"] + 1.5, lw=0.4, fill=colors.HexColor("#B8B2A8"))
        for w in WINDOWS:
            if (w[1], w[2]) == (axis, c0):
                a, b = sorted((u(w[3], 0), u(w[4], 0)))
                _window(e, a, b, w)
        for d in DOORS:
            if (d[1], d[2]) == (axis, c0):
                a, b = sorted((u(d[3], 0), u(d[4], 0)))
                e.rect(a, b, F - LEVELS["FFL"] + LEVELS["wet_area"], F + 7, lw=0.5, fill=colors.HexColor("#6B4A2E"))
                e.text(d[0], (a + b) / 2, F + 7.9, 4.6, color=ACC)
        _roof_long(e, u)
        lo2, hi2 = sorted((u(2.5, 0), u(67.5, 0)))
        _levels(e, lo2 - 1.5)
        e.hdim(lo, hi, -2.2, "60'-9\" incl. walls", 5)
    else:
        east = face == "E"
        _ground(e, u(0, -1) if east else u(0, 28), u(0, 28) if east else u(0, -1))
        lo, hi = sorted((u(0, 3 - 0.375), u(0, 25 + 0.375)))
        e.rect(lo, hi, 0, F, lw=0.6, fill=colors.HexColor("#B8B2A8"))
        if east:
            a, b = sorted((u(0, 3 - 0.375), u(0, 13)))
            e.rect(a, b, F, F + H, lw=0.6, fill=WALLC)
            a, b = sorted((u(0, 13), u(0, 25.375)))
            e.rect(a, b, F, F + H, lw=0.3, fill=colors.HexColor("#E9E4DA"))
            for d in DOORS:
                if d[0] == "D01":
                    e.rect(u(0, d[3]), u(0, d[4]), F, F + 7, lw=0.5, fill=colors.HexColor("#6B4A2E")); e.text("D01", u(0, (d[3] + d[4]) / 2), F + 7.9, 4.6, color=ACC)
            for w in WINDOWS:
                if w[0] in ("W08", "W15"):
                    _window(e, u(0, w[3]), u(0, w[4]), w, shade=w[0] == "W08")
            ar = next(f for f in FURNITURE if f[0] == "F42")
            e.rect(u(0, ar[5]), u(0, ar[6]), LEVELS["poomukham"], LEVELS["poomukham"] + 1.5, lw=0.4, fill=colors.HexColor("#B8B2A8"))
            for px, py in PILLARS:
                if px > 64:
                    e.rect(u(0, py) - 0.33, u(0, py) + 0.33, LEVELS["poomukham"], PILLAR_TOP, lw=0.5, fill=colors.HexColor("#6B4A2E"))
            for i in range(3):
                stp = next(f[3] for f in SITE_FEATURES if f[0] == "STEPS")
                e.rect(u(0, stp[2]), u(0, stp[3]), i * LEVELS["riser"], (i + 1) * LEVELS["riser"], lw=0.4, fill=colors.HexColor("#CFC8BC"))
        else:
            e.rect(lo, hi, F, F + H, lw=0.6, fill=WALLC)
            for w in WINDOWS:
                if (w[1], w[2]) == (axis, c0):
                    a, b = sorted((u(0, w[3]), u(0, w[4])))
                    _window(e, a, b, w)
        _roof_end(e, u, east)
        if not east:  # tank on its stand stands in front of the west wall
            tx1, tx2, ty1, ty2 = next(f[3] for f in SITE_FEATURES if f[0] == "TANK")
            a, b = sorted((u(0, ty1), u(0, ty2)))
            ts = LEVELS["tank_stand"]
            e.rect(a, b, ts, ts + 4, lw=0.4, fill=colors.HexColor("#555555"))
            e.line(a, 0, a, ts, lw=0.6); e.line(b, 0, b, ts, lw=0.6); e.line(a, ts / 2, b, ts / 2, lw=0.4)
            e.text("OHT ON 18 FT STAND", (a + b) / 2, ts + 4.8, 4.6)
        lo2 = min(u(0, 0.5), u(0, 27.5))
        _levels(e, lo2 - 1.5)
        e.hdim(lo, hi, -2.2, "22'-9\" incl. walls", 5)


def sheet_elev_long(c):
    s = Sheet(c, "A-201", "North and south elevations", "1:75")
    for i, face in enumerate(("N", "S")):
        e = Elev(s, 75, 40 * mm, (178 - i * 118) * mm)
        elevation(e, face)
        s.note(FACES[face]["title"].upper(), 40 * mm, (178 - i * 118 + 92) * mm, 9, INK, "Helvetica-Bold")
    s.note("Brown line at the eaves = fascia with gutter. Every window has a sunshade (chajja) with a drip groove; sills slope out 1:10.", 40 * mm, 20 * mm, 7, GREY)
    c.showPage()


def sheet_elev_short(c):
    s = Sheet(c, "A-202", "East (road) and west elevations", "1:75")
    for i, face in enumerate(("E", "W")):
        e = Elev(s, 75, (45 + i * 145) * mm, 120 * mm)
        elevation(e, face)
        s.note(FACES[face]["title"].upper(), (45 + i * 145) * mm, 222 * mm, 9, INK, "Helvetica-Bold")
    tips = ["Front gable (mukhappu): three timber jali vents let morning light in and hot air out; insect mesh behind.",
            "Plinth face clad 2 ft in rough stone: the splash zone stays clean and does not erode.",
            "West wall: no large windows (afternoon sun). Shade with the creeper pergola, not trees, on black cotton soil.",
            "Entrance: 3 risers of 6 in, 12 in treads, flamed granite with a nosing; foot-wash tap beside the steps."]
    s.bullets(tips, 45 * mm, 92 * mm, 280 * mm, 7)
    c.showPage()


# ---------- sections ----------
def _cut_walls(axis_cut, c0):
    """Walls crossed by a section line. axis_cut 'X' = cut at x=c0 (walls running along X are crossed)."""
    out = []
    for w in WALLS:
        a, c, s, e = w
        if a == axis_cut and s - 0.4 <= c0 <= e + 0.4:
            out.append((w, c))
    return out


def section(e, name):
    axis, c0, _ = SECTIONS[name]
    # u = y for A-A (cut at x), u = x for B-B (cut at y)
    if axis == "X":
        rng = (-1.0, SITE["w"] + 1)
        zfun = lambda u: roof_z(c0, u)
        rooms = [r for r in ROOMS if r[2] <= c0 <= r[3]]
        span = lambda r: (r[4], r[5])
        walls = _cut_walls("X", c0)
        eaves = (ROOF["hip"][2], ROOF["hip"][3])
    else:
        rng = (-1.0, SITE["l"] - 3)
        zfun = lambda u: roof_z(u, c0)
        rooms = [r for r in ROOMS if r[4] <= c0 <= r[5]]
        span = lambda r: (r[2], r[3])
        walls = _cut_walls("Y", c0)
        eaves = (ROOF["hip"][0], ROOF["hip"][1])
    _ground(e, *rng)
    # foundations (indicative) and plinth fill
    hu1, hu2 = (3, 25) if axis == "X" else (5, 65)
    e.rect(hu1, hu2, 0, F - 0.33, stroke=None, fill=colors.HexColor("#E6DDC8"))
    e.text("compacted moorum / gravel fill (no black soil)", (hu1 + hu2) / 2, F / 2 - 0.2, 4.6, color=GREY)
    for w, c in walls:
        t = wall_t(w)
        e.rect(c - 1.25, c + 1.25, -4.5, -3.8, lw=0.4, dash=(2, 1))      # footing (engineer)
        e.rect(c - t / 2, c + t / 2, -3.8, 0, lw=0.3, dash=(2, 1))
        e.rect(c - t / 2 - 0.05, c + t / 2 + 0.05, F - 1.25, F - 0.33, lw=0.5, fill=colors.HexColor("#9A9A9A"))  # plinth beam
    # floors
    for r in rooms:
        a, b = span(r)
        fl = floor_level(r[0])
        e.rect(a, b, fl - 0.33, fl, lw=0.4, fill=colors.HexColor("#CFCFCF"))
    # walls cut, with openings
    for w, c in walls:
        t = wall_t(w)
        a0, b0 = c - t / 2, c + t / 2
        hits = [(k, rec) for (s_, e_, k, rec) in openings_for(w[0], w[1], w[2], w[3]) if s_ <= c0 <= e_]
        gaps = [(F + (0 if k == "door" else rec[5]), F + (7 if k == "door" else rec[6])) for k, rec in hits]
        for k, rec in hits:
            if k == "door" and rec[0] in TRANSOMS:  # vent above the door
                gaps.append((F + TRANSOM_Z[0], F + TRANSOM_Z[1]))
                e.rect(a0, b0, F + TRANSOM_Z[0], F + TRANSOM_Z[1], lw=0.4, fill=colors.HexColor("#8E6B4E"))
        z = F
        for g1, g2 in sorted(gaps):
            if g1 > z: e.rect(a0, b0, z, g1, lw=0.6, fill=HATCH)
            z = g2
        e.rect(a0, b0, z, F + H, lw=0.6, fill=HATCH)
        e.rect(a0, b0, F + LEVELS["door_head"], F + LEVELS["door_head"] + 0.5, lw=0.4, fill=colors.HexColor("#8A8A8A"))  # lintel band
        e.rect(a0 - 0.05, b0 + 0.05, F + H - 0.75, F + H, lw=0.5, fill=colors.HexColor("#8A8A8A"))                      # ring beam
    # roof profile, truss, ceilings
    n = 120
    us = [eaves[0] + (eaves[1] - eaves[0]) * i / n for i in range(n + 1)]
    top = [(u_, zfun(u_)) for u_ in us]
    bot = [(u_, zfun(u_) - 0.45) for u_ in reversed(us)]
    e.poly(top + bot, lw=0.6, close=True, fill=TILE)
    wa, wb = (3, 25) if axis == "X" else (5, 65)
    e.line(wa, F + H, wb, F + H, lw=0.5, color=BROWN)  # truss bottom chord
    k = 4
    while k < (wb - wa):
        uu = wa + k
        e.line(uu, F + H, uu, zfun(uu) - 0.45, lw=0.3, color=BROWN)
        k += 4
    for r in rooms:
        a, b = span(r)
        kind, v = CEILINGS[r[0]]
        if kind == "flat":
            e.line(a + 0.2, F + v, b - 0.2, F + v, lw=0.6, color=BLUE)
        else:
            pts = [(a + (b - a) * i / 20, zfun(a + (b - a) * i / 20) - 0.75) for i in range(21)]
            pts = [(p, min(z, zfun(p) - 0.75)) for p, z in pts]
            e.poly(pts, lw=0.6, color=BLUE, dash=(2, 1))
        e.text(short_name(r[1]).upper(), (a + b) / 2, floor_level(r[0]) + 4, 5, "Helvetica-Bold")
        e.text((f"ceiling {fmt_ft(v)}" if kind == "flat" else v), (a + b) / 2, floor_level(r[0]) + 3.1, 4.4, color=BLUE)
    if axis == "X":
        sx1, sx2, sy1, sy2 = ROOF["skylight"]
        if sx1 <= c0 <= sx2:
            _ventilator(e, sy1, sy2)
            ceil = lambda u_: zfun(u_) - 0.75
            e.line(sy1, ceil(sy1), sy1, vent_sill_z(), lw=0.6, color=BLUE)  # lined shaft
            e.line(sy2, ceil(sy2), sy2, vent_sill_z(), lw=0.6, color=BLUE)
            e.text("ventilator (A-503)", sy2 + 3.2, LANTERN_TOP, 4.6, anchor="l")
    else:
        stp = next(f[3] for f in SITE_FEATURES if f[0] == "STEPS")
        if stp[2] <= c0 <= stp[3]:  # steps only where the cut passes through them
            for i in range(3):
                e.rect(65.375 + i * 0.83, 67.8, i * LEVELS["riser"], (i + 1) * LEVELS["riser"], lw=0.3, fill=colors.HexColor("#CFC8BC"))
    # apron each side
    for edge, sgn in ((wa - 0.375, -1), (wb + 0.375, 1)):
        e.poly([(edge, 0.25), (edge + sgn * 3, 0.05), (edge + sgn * 3, -0.2), (edge, -0.2)], lw=0.4, close=True, fill=colors.HexColor("#CFCFCF"))
    _levels(e, rng[0] - 0.3)


SECTION_NOTES = [
    "Clay tiles on battens, membrane, 50 mm insulation, cement-fibre deck on purlins (attic ventilated at ridge and soffit).",
    "Steel truss bolted to the RCC ring beam with holding-down bolts (cyclone uplift).",
    "RCC lintel band at door-head level runs continuously (seismic zone III).",
    "AAC walls in an RCC frame; mesh over every block-to-concrete joint before plaster.",
    "Flat false ceilings (blue) in bedrooms, offices, baths and kitchen, with insulation above. Living and dining follow the roof.",
    "Plinth beam with DPC; plinth fill of compacted moorum, never black soil; anti-termite treatment at every layer.",
    "Footings dashed and indicative only: type and depth by the engineer after the soil test.",
    "3 ft PCC apron sloped away from the wall; joint against the plinth sealed.",
]


def sheet_sections(c):
    s = Sheet(c, "A-301", "Sections A-A and B-B", "1:75")
    e = Elev(s, 75, 40 * mm, 186 * mm)
    section(e, "B")
    s.note("SECTION B-B: " + SECTIONS["B"][2].upper(), 32 * mm, 268 * mm, 8.5, INK, "Helvetica-Bold")
    e = Elev(s, 75, 40 * mm, 54 * mm)
    section(e, "A")
    s.note("SECTION A-A: " + SECTIONS["A"][2].upper(), 32 * mm, 156 * mm, 8.5, INK, "Helvetica-Bold")
    s.bullets(SECTION_NOTES, 190 * mm, 138 * mm, 135 * mm, 6.8, title="Section notes")
    c.showPage()
