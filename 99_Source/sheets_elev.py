"""Elevations (A-201, A-202) and sections (A-301) for the duplex, all derived from model levels and roof geometry."""
from sheetlib import *
from sheets_arch import SECTIONS

F = LEVELS["FFL"]
H = LEVELS["wall_top"]
U = floor_base("F1")          # first floor, above finished ground
UT = upper_wall_top_z()       # first-floor ring beam
TILE = colors.HexColor("#C98B6B")
GABLE = colors.HexColor("#F1E9DA")
WALLC = colors.HexColor("#F7F4EE")
BACKC = colors.HexColor("#E9E4DA")   # walls set back behind the verandah
LAT = colors.HexColor("#B9785A")     # laterite kitchen front
DARK = colors.HexColor("#5A5048")
TEAK = colors.HexColor("#6B4A2E")
HATCH = colors.HexColor("#BDBDBD")
PLINTH = colors.HexColor("#B8B2A8")
PILLAR_TOP = F + 9.3
FLOORS = (("G", F), ("F1", U))

# faces: wall line, u mapping (u grows left to right as seen), title
FACES = {
    "S": dict(line=("X", 3), u=lambda x, y: x, title="South elevation"),
    "N": dict(line=("X", 25), u=lambda x, y: SITE["l"] - x, title="North elevation"),
    "E": dict(line=("Y", 67), u=lambda x, y: y, title="East elevation (road side)"),
    "W": dict(line=("Y", 23), u=lambda x, y: SITE["w"] - y, title="West elevation"),
}


def _poly(e, pts, fill, stroke=INK, lw=0.6):
    e.poly(pts, lw=lw, color=stroke, close=True, fill=fill)


def _window(e, u1, u2, w, base, shade=True):
    sill, head = base + w[5], base + w[6]
    jali = "jali" in w[8].lower()
    e.rect(u1, u2, sill, head, lw=0.5, fill=colors.HexColor("#8E6B4E") if jali else colors.HexColor("#B9CCD3"))
    if jali:
        n = max(2, int((u2 - u1) / 0.6))
        for i in range(1, n): e.line(u1 + i * (u2 - u1) / n, sill, u1 + i * (u2 - u1) / n, head, lw=0.2, color=WHITE)
    else:
        e.line((u1 + u2) / 2, sill, (u1 + u2) / 2, head, lw=0.3)
    if shade:
        e.rect(u1 - 0.5, u2 + 0.5, head + 0.2, head + 0.45, lw=0.4, fill=WALLC)
    e.text(w[0], (u1 + u2) / 2, sill - 0.9, 4.2, color=ACC)


def _openings_on(face, u, along_x, shade=True):
    """Windows and doors of both floors on a face line."""
    axis, c0 = FACES[face]["line"]
    for fl, base in FLOORS:
        with on_floor(fl):
            for w in WINDOWS:
                if (w[1], w[2]) == (axis, c0):
                    a, b = sorted((u(w[3], 0), u(w[4], 0)) if along_x else (u(0, w[3]), u(0, w[4])))
                    _window(e_cur[0], a, b, w, base, shade and not (face == "N"))
            for d in DOORS:
                if (d[1], d[2]) == (axis, c0):
                    a, b = sorted((u(d[3], 0), u(d[4], 0)) if along_x else (u(0, d[3]), u(0, d[4])))
                    e_cur[0].rect(a, b, base - (F - LEVELS["wet_area"] if fl == "G" else 0), base + 7, lw=0.5, fill=TEAK)
                    e_cur[0].text(d[0], (a + b) / 2, base + 7.7, 4.2, color=ACC)


e_cur = [None]


def _wall_span(fl, axis, c0):
    """Extent of a floor's walls on a line (for the wall face rectangle)."""
    with on_floor(fl):
        segs = [(w[2], w[3]) for w in WALLS if (w[0], w[1]) == (axis, c0)]
    return (min(s for s, _ in segs), max(e for _, e in segs)) if segs else None


def _rail_band(e, a, b, base, top):
    """Open side of the terrace: dark opening above a railing."""
    e.rect(a, b, base, top, lw=0.4, fill=DARK)
    e.rect(a, b, base, base + 3.5, lw=0.5, fill=WALLC)
    n = max(2, int((b - a) / 0.5))
    for i in range(1, n): e.line(a + i * (b - a) / n, base + 0.3, a + i * (b - a) / n, base + 3.2, lw=0.25, color=TEAK)
    e.line(a, base + 3.5, b, base + 3.5, lw=1.0, color=TEAK)


def _posts(e, uf, posts):
    """Galvanised steel posts of the terrace frame."""
    for x, y in posts:
        uu = uf(x, y)
        e.rect(uu - 0.17, uu + 0.17, U, UT - 0.75, lw=0.4, fill=colors.HexColor("#8C9196"))


def _roof_long(e, u):
    x1, x2, y1, y2 = ROOF["hip"]
    gx1, gx2, ya, yb = ROOF["gable"]
    w = (y2 - y1) / 2
    ez, rz, gz, gr = eave_z(), ridge_z(), gable_eave_z(), gable_ridge_z()
    _poly(e, [(u(gx1, 0), gz), (u(gx2, 0), gz), (u(gx2, 0), gr), (u(gx1, 0), gr)], TILE, lw=0.5)   # front gable slope, seen side-on
    for i in range(1, 6):
        zz = gz + i * (gr - gz) / 6
        e.line(u(gx1, 0), zz, u(gx2, 0), zz, lw=0.25, color=BROWN)
    e.line(u(gx1, 0), gz, u(gx2, 0), gz, lw=1.0, color=BROWN)
    _poly(e, [(u(x1, 0), ez), (u(x2, 0), ez), (u(x2 - w, 0), rz), (u(x1 + w, 0), rz)], TILE)
    e.line(u(x1, 0), ez, u(x2, 0), ez, lw=1.2, color=BROWN)  # fascia + gutter


def _roof_end(e, u, east):
    x1, x2, y1, y2 = ROOF["hip"]
    ez, rz = eave_z(), ridge_z()
    _poly(e, [(u(0, y1), ez), (u(0, y2), ez), (u(0, (y1 + y2) / 2), rz)], TILE)
    e.line(u(0, y1), ez, u(0, y2), ez, lw=1.2, color=BROWN)


def _front_gable(e, u):
    gx1, gx2, ya, yb = ROOF["gable"]
    gz, gr = gable_eave_z(), gable_ridge_z()
    _poly(e, [(u(0, ya), gz), (u(0, yb), gz), (u(0, (ya + yb) / 2), gr)], GABLE, lw=0.8)
    e.poly([(u(0, ya - 0.3), gz - 0.15), (u(0, (ya + yb) / 2), gr + 0.35), (u(0, yb + 0.3), gz - 0.15)], lw=1.4, color=BROWN)  # barge boards
    for c0 in (-1.6, 0, 1.6):
        yc = (ya + yb) / 2 + c0
        e.rect(u(0, yc - 0.55), u(0, yc + 0.55), gz + 2.0, gz + 3.4 - abs(c0) * 0.3, lw=0.4, fill=colors.HexColor("#8E6B4E"))


def _ground(e, u1, u2):
    e.line(u1, 0, u2, 0, lw=1.0)
    e.text("FINISHED GROUND", u1 + 3, -0.9, 4.4, color=GREY, anchor="l")


def _levels(e, u):
    for z, lab in ((0, "FGL +0'-0\""), (F, f"FFL {fmt_lvl(F)}"), (F + H, f"Slab / ring beam {fmt_lvl(F + H)}"), (U, f"First floor {fmt_lvl(U)}"),
                   (UT, f"Ring beam {fmt_lvl(UT)}"), (eave_z(), f"Eaves {fmt_lvl(eave_z())}"), (ridge_z(), f"Ridge {fmt_lvl(ridge_z())}")):
        if abs(z - U) < 0.01 and abs(U - (F + H)) < 0.6 and lab.startswith("Slab"):
            continue
        e.lvl(u, z, lab, 4.6)


def elevation(e, face):
    e_cur[0] = e
    f = FACES[face]
    u = f["u"]
    axis, c0 = f["line"]
    if face in ("S", "N"):
        _ground(e, u(17, 0) if face == "S" else u(77, 0), u(77, 0) if face == "S" else u(17, 0))
        lo, hi = sorted((u(23 - 0.375, 0), u(67 + 0.375, 0)))
        e.rect(lo, hi, 0, F, lw=0.6, fill=PLINTH)
        g = _wall_span("G", axis, c0); up = _wall_span("F1", axis, c0)
        ga, gb = sorted((u(g[0] - 0.375, 0), u(g[1] + 0.375, 0)))
        e.rect(ga, gb, F, F + H, lw=0.6, fill=WALLC)
        if face == "N":  # verandah and kitchen front, set back
            a, b = sorted((u(61, 0), u(67.375, 0)))
            e.rect(a, b, F, F + H, lw=0.3, fill=BACKC)
            for px, py in PILLARS:
                if py > 24:
                    e.rect(u(px, 0) - 0.33, u(px, 0) + 0.33, LEVELS["poomukham"], PILLAR_TOP, lw=0.5, fill=TEAK)
        ua, ub = sorted((u(up[0] - 0.375, 0), u(up[1] + 0.375, 0)))
        e.rect(ua, ub, U, UT, lw=0.6, fill=WALLC)
        if face in ("S", "N"):  # back wall of the covered terrace, seen through the open front half
            a, b = sorted((u(45.375, 0), u(61, 0)))
            e.rect(a, b, U, UT - 0.75, lw=0.3, fill=DARK)
        e.line(min(ga, ua), F + H, max(gb, ub), F + H, lw=0.4, color=GREY)  # band at first-floor level
        with on_floor("F1"):
            for ax, cc, s_, e_ in RAILS:
                if (ax, cc) == (axis, c0):
                    a, b = sorted((u(s_ - (0.375 if s_ < 40 else 0), 0), u(e_ + (0.4 if e_ > 60 else 0), 0)))
                    _rail_band(e, a, b, U, UT - 0.75)
        _posts(e, lambda x, y: u(x, 0), [p for p in TERRACE_POSTS if abs(p[1] - c0) < 0.5])
        e.rect(*sorted((u(45.375, 0), u(61.4, 0))), UT - 0.75, UT, lw=0.5, fill=colors.HexColor("#7A7A7A"))  # steel edge beam
        _openings_on(face, u, True)
        _roof_long(e, u)
        _levels(e, min(u(19, 0), u(71, 0)) - 1.0)
        e.hdim(lo, hi, -2.4, "44'-9\" incl. walls", 5)
    else:
        east = face == "E"
        _ground(e, u(0, -1) if east else u(0, 28), u(0, 28) if east else u(0, -1))
        lo, hi = sorted((u(0, 3 - 0.375), u(0, 25 + 0.375)))
        e.rect(lo, hi, 0, F, lw=0.6, fill=PLINTH)
        if east:
            e.rect(lo, hi, U, UT, lw=0.4, fill=DARK)  # covered terrace, open to the east behind its railing
            _rail_band(e, *sorted((u(0, 2.6), u(0, 25.4))), U, UT - 0.75)
            _posts(e, lambda x, y: u(0, y), [p for p in TERRACE_POSTS if p[0] > 60])
            e.rect(lo, hi, UT - 0.75, UT, lw=0.5, fill=colors.HexColor("#7A7A7A"))
            a, b = sorted((u(0, 3 - 0.375), u(0, 12.5)))
            e.rect(a, b, F, F + H, lw=0.6, fill=LAT)
            a, b = sorted((u(0, 12.5), u(0, 25.375)))
            e.rect(a, b, F, F + H, lw=0.3, fill=BACKC)
            for d in DOORS:
                if d[0] == "D01":
                    e.rect(u(0, d[3]), u(0, d[4]), F, F + 7, lw=0.5, fill=TEAK); e.text("D01", u(0, (d[3] + d[4]) / 2), F + 7.7, 4.2, color=ACC)
            for w in WINDOWS:
                if w[0] in ("W08", "W17"):
                    _window(e, *sorted((u(0, w[3]), u(0, w[4]))), w, F, shade=w[0] == "W08")
            for fid in ("F42", "F69"):
                ar = next(x for x in FURNITURE if x[0] == fid)
                e.rect(u(0, ar[5]), u(0, ar[6]), LEVELS["poomukham"], LEVELS["poomukham"] + 1.5, lw=0.4, fill=PLINTH)
            for px, py in PILLARS:
                if px > 66:
                    e.rect(u(0, py) - 0.33, u(0, py) + 0.33, LEVELS["poomukham"], PILLAR_TOP, lw=0.5, fill=TEAK)
            stp = next(x[3] for x in SITE_FEATURES if x[0] == "STEPS")
            for i in range(3):
                e.rect(u(0, stp[2]), u(0, stp[3]), i * LEVELS["riser"], (i + 1) * LEVELS["riser"], lw=0.4, fill=colors.HexColor("#CFC8BC"))
            _front_gable(e, u)
        else:
            e.rect(lo, hi, F, F + H, lw=0.6, fill=WALLC)
            up = _wall_span("F1", "Y", 23)
            a, b = sorted((u(0, up[0] - 0.375), u(0, up[1] + 0.375)))
            e.rect(a, b, U, UT, lw=0.6, fill=WALLC)
            with on_floor("F1"):
                for ax, cc, s_, e_ in RAILS:
                    if (ax, cc) == ("Y", 23):
                        a, b = sorted((u(0, s_), u(0, e_ + 0.375)))
                        _rail_band(e, a, b, U, UT - 0.75)
            _openings_on(face, u, False)
            px1, px2, py1, py2 = next(x[3] for x in SITE_FEATURES if x[0] == "PERGOLA")
            a, b = sorted((u(0, py1), u(0, py2)))
            e.rect(a, b, 8.5, 9.1, stroke=colors.HexColor("#6F8E4A"), lw=0.5, dash=(2, 1))
            for yy in (py1, (py1 + py2) / 2, py2):
                e.line(u(0, yy), 0, u(0, yy), 8.5, lw=0.5, color=colors.HexColor("#6F8E4A"), dash=(2, 1))
            e.text("CREEPER PERGOLA (IN FRONT)", (a + b) / 2, 9.7, 4.2, color=colors.HexColor("#4F6E34"))
        _roof_end(e, u, east)
        _levels(e, min(u(0, 0.5), u(0, 27.5)) - 1.0)
        e.hdim(lo, hi, -2.4, "22'-9\" incl. walls", 5)


def sheet_elev_long(c):
    s = Sheet(c, "A-201", "North and south elevations", "1:100")
    for i, face in enumerate(("N", "S")):
        e = Elev(s, 100, 22 * mm, (166 - i * 128) * mm)
        elevation(e, face)
        s.note(FACES[face]["title"].upper(), 22 * mm, (166 - i * 128 + 106) * mm, 9, INK, "Helvetica-Bold")
    s.note("Two-tier roof: the main hipped roof over the two-storey block (on steel posts over the covered terrace), the low front gable over the verandah and kitchen front. Brown line = fascia with gutter.", 22 * mm, 20 * mm, 7, GREY)
    c.showPage()


def sheet_elev_short(c):
    s = Sheet(c, "A-202", "East (road) and west elevations", "1:100")
    for i, face in enumerate(("E", "W")):
        e = Elev(s, 100, (60 + i * 140) * mm, 112 * mm)
        elevation(e, face)
        s.note(FACES[face]["title"].upper(), (40 + i * 140) * mm, 225 * mm, 9, INK, "Helvetica-Bold")
    tips = ["Front gable (mukhappu) over the verandah and kitchen front; the covered terrace sits 6 ft back behind it, open behind a railing under the main roof on slim steel posts.",
            "Plinth face clad 2 ft in rough stone: the splash zone stays clean and does not erode.",
            "West wall: the upper master's west wall is solid (afternoon sun); the room above the small bedroom has only a small high vent on the west. The creeper pergola shades the ground floor.",
            "Entrance: 3 risers of 6 in, 12 in treads, flamed granite with a nosing; foot-wash tap beside the steps."]
    s.bullets(tips, 40 * mm, 80 * mm, 285 * mm, 7)
    c.showPage()


# ---------- sections ----------
def _cut_walls(axis_cut, c0):
    """Walls of the floor being drawn crossed by a section line. axis_cut 'X' = cut at x=c0 (walls running along X are crossed)."""
    return [(w, w[1]) for w in WALLS if w[0] == axis_cut and w[2] - 0.4 <= c0 <= w[3] + 0.4]


def _stair_z(y, flight):
    """Height above FFL of a flight's walking line at plan y (stepped)."""
    st = STAIR; rz = LEVELS["upper_ffl"] / st["risers"]
    if flight == 1:
        y1 = st["flight1"][2]
        k = min(st["flight1"][4] - 1, max(0, int((y - y1) / st["tread"])))
        return (k + 1) * rz
    y2 = st["flight2"][3]
    k = min(st["flight2"][4] - 1, max(0, int((y2 - y) / st["tread"])))
    return st["flight1"][4] * rz + (k + 1) * rz


def section(e, name):
    axis, c0, _ = SECTIONS[name]
    # u = y for A-A (cut at x), u = x for B-B (cut at y)
    if axis == "X":
        rng = (-1.0, SITE["w"] + 1)
        zfun = lambda u_: roof_z(c0, u_)
        span = lambda r: (r[4], r[5])
        inside = lambda r: r[2] <= c0 <= r[3]
        eaves = (ROOF["hip"][2], ROOF["hip"][3])
        hu1, hu2 = 3, 25
    else:
        rng = (17.0, SITE["l"] - 3)
        zfun = lambda u_: roof_z(u_, c0)
        span = lambda r: (r[2], r[3])
        inside = lambda r: r[4] <= c0 <= r[5]
        eaves = (ROOF["hip"][0], ROOF["gable"][1])
        hu1, hu2 = 23, 67
    _ground(e, *rng)
    e.rect(hu1, hu2, 0, F - 0.33, stroke=None, fill=colors.HexColor("#E6DDC8"))
    e.text("compacted moorum / gravel fill (no black soil)", (hu1 + hu2) / 2, F / 2 - 0.2, 4.4, color=GREY)
    # first-floor slab where the cut crosses it
    for x1, x2, y1, y2 in SLAB_F1:
        if (axis == "X" and x1 <= c0 <= x2) or (axis == "Y" and y1 <= c0 <= y2):
            a, b = (y1, y2) if axis == "X" else (x1, x2)
            e.rect(a, b, U - LEVELS["slab"], U, lw=0.5, fill=colors.HexColor("#9A9A9A"))
    for fl, base in FLOORS:
        with on_floor(fl):
            walls = _cut_walls(axis, c0)
            top = base + (H if fl == "G" else LEVELS["upper_wall_top"])
            if fl == "G":
                for w, c in walls:
                    t = wall_t(w)
                    e.rect(c - 1.4, c + 1.4, -4.5, -3.8, lw=0.4, dash=(2, 1))      # footing (engineer)
                    e.rect(c - t / 2, c + t / 2, -3.8, 0, lw=0.3, dash=(2, 1))
                    e.rect(c - t / 2 - 0.05, c + t / 2 + 0.05, F - 1.25, F - 0.33, lw=0.5, fill=colors.HexColor("#9A9A9A"))  # plinth beam
            rooms = [r for r in ROOMS if inside(r)]
            for r in rooms:
                a, b = span(r)
                fl_z = floor_level(r[0])
                if fl == "G":
                    e.rect(a, b, fl_z - 0.33, fl_z, lw=0.4, fill=colors.HexColor("#CFCFCF"))
                kind, v = CEILINGS[r[0]]
                if kind == "flat":
                    e.line(a + 0.2, base + v, b - 0.2, base + v, lw=0.6, color=BLUE)
                elif r[0] not in ("R06",):
                    pts = [(a + (b - a) * i / 20, zfun(a + (b - a) * i / 20) - 0.75) for i in range(21)]
                    e.poly(pts, lw=0.6, color=BLUE, dash=(2, 1))
                e.text(short_name(r[1]).upper(), (a + b) / 2, base + 4, 4.6, "Helvetica-Bold")
                e.text((f"ceiling {fmt_ft(v)}" if kind == "flat" else v), (a + b) / 2, base + 3.1, 4.0, color=BLUE)
            for w, c in walls:
                t = wall_t(w)
                a0, b0 = c - t / 2, c + t / 2
                hits = [(k, rec) for (s_, e_, k, rec) in openings_for(w[0], w[1], w[2], w[3]) if s_ <= c0 <= e_]
                gaps = [(base + (0 if k == "door" else rec[5]), base + (7 if k == "door" else rec[6])) for k, rec in hits]
                z = base
                for g1, g2 in sorted(gaps):
                    if g1 > z: e.rect(a0, b0, z, g1, lw=0.6, fill=HATCH)
                    z = g2
                e.rect(a0, b0, z, top, lw=0.6, fill=HATCH)
                e.rect(a0 - 0.05, b0 + 0.05, top - 0.75, top, lw=0.5, fill=colors.HexColor("#8A8A8A"))  # ring beam / band
            for ax, cc, s_, e_ in RAILS:
                if ax == axis and s_ - 0.2 <= c0 <= e_ + 0.2:
                    e.rect(cc - 0.15, cc + 0.15, base, base + 3.5, lw=0.5, fill=colors.HexColor("#8E6B4E"))
    # stair (section B crosses both flights)
    st = STAIR
    if axis == "Y":
        f1, f2, ld = st["flight1"], st["flight2"], st["landing"]
        if f1[2] <= c0 <= f1[3]:
            z1 = F + _stair_z(c0, 1); e.rect(f1[0], f1[1], z1 - 0.6, z1, lw=0.5, fill=colors.HexColor("#CFC8BC"))
        if f2[2] <= c0 <= f2[3]:
            z2 = F + _stair_z(c0, 2); e.rect(f2[0], f2[1], z2 - 0.6, z2, lw=0.5, fill=colors.HexColor("#CFC8BC"))
        lz = F + st["flight1"][4] * LEVELS["upper_ffl"] / st["risers"]
        e.rect(ld[0], ld[1], lz - 0.5, lz, lw=0.4, dash=(2, 1))
        e.text("STAIR (half landing beyond)", (ld[0] + ld[1]) / 2, lz + 0.8, 4.2)
        stp = next(x[3] for x in SITE_FEATURES if x[0] == "STEPS")
        if stp[2] <= c0 <= stp[3]:
            for i in range(3):
                e.rect(67.375 + i * 0.8, 69.8, i * LEVELS["riser"], (i + 1) * LEVELS["riser"], lw=0.3, fill=colors.HexColor("#CFC8BC"))
    # roof profile and trusses
    n = 160
    us = [eaves[0] + (eaves[1] - eaves[0]) * i / n for i in range(n + 1)]
    pts = [(u_, zfun(u_)) for u_ in us if zfun(u_) is not None]
    e.poly(pts + [(p, z - 0.45) for p, z in reversed(pts)], lw=0.6, close=True, fill=TILE)
    blocks = [((3, 25) if axis == "X" else (23, 61), UT)]
    if axis == "Y":
        blocks.append(((61, 67), F + H))
    for (wa, wb), zc in blocks:
        e.line(wa, zc, wb, zc, lw=0.5, color=BROWN)  # truss bottom chord
        k = 4
        while k < (wb - wa):
            uu = wa + k
            zt = zfun(uu)
            if zt is not None and zt - 0.45 > zc:
                e.line(uu, zc, uu, zt - 0.45, lw=0.3, color=BROWN)
            k += 4
    if axis == "X":
        e.text("steel frame over the terrace", 14, UT + 1.2, 4.2, color=GREY)
    else:
        e.text("steel frame over the terrace", 53, UT + 1.2, 4.2, color=GREY)
    for edge, sgn in ((hu1 - 0.375, -1), (hu2 + 0.375, 1)):
        e.poly([(edge, 0.25), (edge + sgn * 3, 0.05), (edge + sgn * 3, -0.2), (edge, -0.2)], lw=0.4, close=True, fill=colors.HexColor("#CFCFCF"))
    _levels(e, rng[0] - 0.3)


SECTION_NOTES = [
    "Clay tiles on battens, membrane, 50 mm insulation, cement-fibre deck on purlins (attic over the first-floor rooms ventilated at ridge and soffit).",
    "Main roof trusses bolted to the first-floor ring beam; front gable trusses to the ground-floor ring beam (cyclone uplift).",
    "First-floor RCC slab over the whole two-storey block; over the front half it is the covered terrace, waterproofed, under the main roof on galvanised steel posts and steel trusses.",
    "RCC lintel band at door-head level on both floors (seismic zone III). AAC walls in an RCC frame; mesh over every block-to-concrete joint.",
    "Ground-floor rooms have a plastered slab soffit at about 9'-5\" (blue); first-floor rooms have insulated false ceilings; the stair and terrace are open to the roof.",
    "Dog-leg stair, 17 risers of about 7 in; teak handrail; timber jali to the living and to the terrace.",
    "Plinth beam with DPC; plinth fill of compacted moorum, never black soil; anti-termite treatment at every layer.",
    "Footings dashed and indicative only: type and depth by the engineer after the soil test (two-storey loads).",
]


def sheet_sections(c):
    s = Sheet(c, "A-301", "Sections A-A and B-B", "1:100")
    e = Elev(s, 100, 0 * mm, 158 * mm)
    section(e, "B")
    s.note("SECTION B-B: " + SECTIONS["B"][2].upper(), 32 * mm, 272 * mm, 8, INK, "Helvetica-Bold")
    e = Elev(s, 100, 40 * mm, 36 * mm)
    section(e, "A")
    s.note("SECTION A-A: " + SECTIONS["A"][2].upper(), 32 * mm, 146 * mm, 8, INK, "Helvetica-Bold")
    s.bullets(SECTION_NOTES, 160 * mm, 140 * mm, 165 * mm, 6.8, title="Section notes")
    c.showPage()
