"""Elevations (A-201, A-202) and sections (A-301) of the courtyard house, all derived from the model's levels and the roof
geometry in geom (ring_z, wing_roof_z, eave_z, ridge_z, wing_eave_z): nothing on these sheets is a hard-coded height."""
from sheetlib import *
import math
from sheets_arch import SECTIONS

F = LEVELS["FFL"]
H = LEVELS["wall_top"]
U = floor_base("F1")          # first floor, above finished ground
UT = upper_wall_top_z()       # first-floor ring beam
SLAB = terrace_slab_z()       # finished level of the roof terrace
TILE = colors.HexColor("#C98B6B")
WALLC = colors.HexColor("#F7F4EE")
OCHRE = colors.HexColor("#EBD9B4")   # lime wash, ochre: the upper wing
JALI = colors.HexColor("#8E6B4E")
DARK = colors.HexColor("#5A5048")
TEAK = colors.HexColor("#6B4A2E")
STEEL = colors.HexColor("#8C9196")
COPPER = colors.HexColor("#B87333")
HATCH = colors.HexColor("#BDBDBD")
PLINTH = colors.HexColor("#B8B2A8")
REDOX = colors.HexColor("#B5654A")   # red oxide thinnai
STONE = colors.HexColor("#CFC8BC")
SKY = colors.HexColor("#EAF2F8")
GREEN = colors.HexColor("#6F8E4A")
TT = 0.45                     # roof build-up (tiles, battens, deck), drawn below the roof surface

THINNAI_ROOF = ROOF["thinnai"]   # the thinnai lean-to (geom.thinnai_roof_z): the ring's east slope carried on over the pillars
TB = ROOF["thinnai_build_up"]


WING_WALLS = ROOF["wing_walls"]     # the two storeys' outlines: the west band and the north arm over the den
NARM_X = max(w[1] for w in WING_WALLS)   # the north arm's east wall (x 33.5)


def ring_vis(x, y):
    """The ring roof where it is a roof: not inside the upper wing's walls (the wing rises through it there)."""
    if any(w[0] < x < w[1] and w[2] < y < w[3] for w in WING_WALLS):
        return None
    return ring_z(x, y)


def _behind_wing(face, x, y):
    """True where a point lies behind the upper wing's walls as seen from a face (hidden by them)."""
    if face == "S":
        return HX1 < x < RING[0] and y > HY1
    if face == "N":   # the north arm's north wall hides everything behind it, west of its east wall
        return HX1 < x < NARM_X and y < HY2
    if face == "W":
        return HY1 < y < HY2 and x > HX1
    return False


# faces: wall lines per floor, u mapping (u grows left to right as seen), depth samples, title
FACES = {
    "S": dict(lines={"G": ("X", HY1), "F1": ("X", HY1)}, u=lambda x, y: x, title="South elevation"),
    "N": dict(lines={"G": ("X", HY2), "F1": ("X", HY2)}, u=lambda x, y: SITE["l"] - x, title="North elevation"),
    "E": dict(lines={"G": ("Y", HX2), "F1": ("Y", RING[0])}, u=lambda x, y: y, title="East elevation (road side)"),
    "W": dict(lines={"G": ("Y", HX1), "F1": ("Y", HX1)}, u=lambda x, y: SITE["w"] - y, title="West elevation (back garden)"),
}


def _along(face):
    return face in ("S", "N")   # True: the face runs along x


def _profile(face, zfun, a, b, step=0.25, occlude=False):
    """Silhouette of a roof seen from a face: for each position along the face (a..b, plan coordinate), the highest
    z over the depth of the house. Returns [(u, z or None)]."""
    o = ROOF["ring"]
    d1, d2 = (o[2], o[3]) if _along(face) else (o[0], THINNAI_ROOF[1])
    n_d = int(round((d2 - d1) / step))
    u = FACES[face]["u"]
    out = []
    n = int(round((b - a) / step))
    for i in range(n + 1):
        p = a + i * step
        best = None
        for j in range(n_d + 1):
            d = d1 + j * step
            x, y = (p, d) if _along(face) else (d, p)
            if occlude and _behind_wing(face, x, y):
                continue
            z = zfun(x, y)
            if z is not None and (best is None or z > best):
                best = z
        out.append((u(p, 0) if _along(face) else u(0, p), best))
    return out


def _fill_profile(e, prof, base, fill=TILE, edge=BROWN):
    """Fill each run of a silhouette down to a base line (the eave)."""
    runs, cur = [], []
    for u_, z in prof:
        if z is None:
            if cur: runs.append(cur); cur = []
        else:
            cur.append((u_, z))
    if cur: runs.append(cur)
    for r in runs:
        if len(r) < 2: continue
        pts = r + [(r[-1][0], base), (r[0][0], base)]
        e.poly(pts, lw=0.5, close=True, fill=fill)
        e.line(r[0][0], base, r[-1][0], base, lw=1.0, color=edge)   # fascia with its gutter


def _roof_profile(e, face):
    """The roof as seen from a face, computed from geom: the ring roof (outer slopes to the eaves, inner slopes hidden
    behind the ridge), the hipped west wing above it and the thinnai's lean-to. Each layer is the max roof height over
    the depth of the house at 0.25 ft steps, filled in the roof colour."""
    o, w = ROOF["ring"], wing_bbox()   # the wing's L roof (geom.wing_rects)
    a, b = (o[0], THINNAI_ROOF[1]) if _along(face) else (o[2], o[3])
    tp = _profile(face, thinnai_roof_z, a, b) if face != "W" else []
    if _along(face):   # seen from the side the thinnai lean-to is a sloping band
        _roof_band(e, tp)
    else:
        _fill_profile(e, tp, thinnai_roof_z(THINNAI_ROOF[1], CY))
    _fill_profile(e, _profile(face, ring_vis, a, b, occlude=True), eave_z())
    wa, wb = (w[0], w[1]) if _along(face) else (w[2], w[3])
    _fill_profile(e, _profile(face, wing_roof_z, wa, wb), wing_eave_z())


def _window(e, u1, u2, w, base, shade=True, tag=True):
    sill, head = base + w[5], base + w[6]
    jali = "jali" in w[8].lower()
    e.rect(u1, u2, sill, head, lw=0.5, fill=JALI if jali else colors.HexColor("#B9CCD3"))
    if jali:
        n = max(2, int((u2 - u1) / 0.6))
        for i in range(1, n): e.line(u1 + i * (u2 - u1) / n, sill, u1 + i * (u2 - u1) / n, head, lw=0.2, color=WHITE)
    else:
        e.line((u1 + u2) / 2, sill, (u1 + u2) / 2, head, lw=0.3)
    if shade:
        e.rect(u1 - 0.5, u2 + 0.5, head + 0.2, head + 0.45, lw=0.4, fill=WALLC)
    if tag:
        e.text(w[0], (u1 + u2) / 2, sill - 0.9, 4.2, color=ACC)


def _span(face, a, b):
    u = FACES[face]["u"]
    return sorted((u(a, 0), u(b, 0)) if _along(face) else (u(0, a), u(0, b)))


def _tag(e, text, u, z, anchor="c", color=ACC, font="Helvetica"):
    """Queue an opening's tag: elevation() draws the tags last, over every wall and roof."""
    e.plan.__dict__.setdefault("tags", []).append((text, u, z, anchor, color, font))


def _draw_tags(e):
    for text, u, z, anchor, color, font in e.plan.__dict__.pop("tags", []):
        e.text(text, u, z, 4.2, font, color, anchor)


def _openings_on(e, face, fl, skip=()):
    """Windows and doors of one floor on the face's wall line."""
    axis, c0 = FACES[face]["lines"][fl]
    base = floor_base(fl)
    pillars = [FACES[face]["u"](0, py) for _, py in THINNAI_PILLARS] if (face == "E" and fl == "G") else []
    mid = sum(pillars) / len(pillars) if pillars else 0
    with on_floor(fl):
        for w in WINDOWS:
            if (w[1], w[2]) == (axis, c0) and w[0] not in skip:
                ua, ub = _span(face, w[3], w[4])
                _window(e, ua, ub, w, base, shade=face in ("S", "W") or fl == "G", tag=False)
                tu, anchor = (ua + ub) / 2, "c"
                for pu in pillars:   # a thinnai pillar stands in front of the tag: put it on the pillar's outer side
                    if abs(tu - pu) < 1.0:
                        tu, anchor = (pu - 0.5, "r") if pu < mid else (pu + 0.5, "l")
                ty = base + w[6] + 0.95 if fl == "F1" else base + w[5] - 0.9   # upstairs: above the head, clear of the ring roof below
                _tag(e, w[0], tu, ty, anchor)
        for d in DOORS:
            if (d[1], d[2]) == (axis, c0):
                a, b = _span(face, d[3], d[4])
                hd = base + DOOR_HEIGHTS.get(d[0], LEVELS["door_head"])
                e.rect(a, b, base, hd, lw=0.5, fill=TEAK)
                if "double" in d[7].lower():   # two leaves, each with its panels
                    e.line((a + b) / 2, base, (a + b) / 2, hd, lw=0.6, color=colors.HexColor("#C8A97E"))
                    for l1, l2 in ((a, (a + b) / 2), ((a + b) / 2, b)):
                        e.rect(l1 + 0.3, l2 - 0.3, base + 0.6, base + 3.2, stroke=colors.HexColor("#C8A97E"), lw=0.4)
                        e.rect(l1 + 0.3, l2 - 0.3, base + 3.8, hd - 0.6, stroke=colors.HexColor("#C8A97E"), lw=0.4)
                if pillars or d[0] == EF_OVER_DOOR["door"]:   # under the thinnai's lean-to, or under the duct terminal: the tag goes on the door itself
                    _tag(e, d[0], (a + b) / 2, hd - 0.35, "c", WHITE, "Helvetica-Bold")
                else:
                    _tag(e, d[0], (a + b) / 2, hd + 0.7)


def _rail(e, a, b, base, jali=False):
    """A 4'-0\" railing seen face on (balusters at 100 mm or less), or a closed teak jali parapet."""
    top = base + RAIL_H
    e.rect(a, b, base, top, lw=0.5, fill=colors.HexColor("#C8A97E") if jali else None)
    n = max(2, int((b - a) / (0.35 if jali else 0.33)))
    for i in range(1, n): e.line(a + i * (b - a) / n, base, a + i * (b - a) / n, top, lw=0.2, color=TEAK)
    if jali:
        for k in range(1, 8): e.line(a, base + k * RAIL_H / 8, b, base + k * RAIL_H / 8, lw=0.2, color=TEAK)
    e.line(a, top, b, top, lw=1.0, color=TEAK)


def _post(e, uu, z1, z2):
    e.rect(uu - 0.17, uu + 0.17, z1, z2, lw=0.4, fill=STEEL)


def _canopy(e, a, b):
    """The roof terrace's light tiled canopy, seen face on."""
    z = SLAB + ROOF["canopy"]
    e.rect(a, b, z, z + 0.35, lw=0.5, fill=colors.HexColor("#D8A98F"))


def _jharokha(e, a, b):
    """A teak jharokha bay seen face on: bracket, jali below, glass above, its frame carried up to the wing's eave soffit (no roof of its own)."""
    seat = U + JHAROKHAS[0][4]
    e.rect(a, b, seat - JHAROKHA_DECK, seat, lw=0.5, fill=TEAK)             # seat deck and bracket frame
    e.rect(a, b, seat, seat + 3.0, lw=0.5, fill=JALI)                       # fixed jali, 3 ft above the seat
    for i in range(1, 8): e.line(a + i * (b - a) / 8, seat, a + i * (b - a) / 8, seat + 3.0, lw=0.2, color=WHITE)
    e.rect(a, b, seat + 3.0, U + 7.5, lw=0.5, fill=colors.HexColor("#B9CCD3"))  # glazed above
    e.rect(a, b, U + ROOF["jharokha_head"], wing_eave_z() - 0.45, lw=0.5, fill=TEAK)      # teak frame and soffit board up to the wing's eave


def _ground(e, u1, u2):
    e.line(u1, 0, u2, 0, lw=1.0)
    e.text("FINISHED GROUND", u1 + 0.5, -0.9, 4.4, color=GREY, anchor="l")


def _levels(e, u, extra=()):
    rows = [(0, "FGL +0'-0\""), (F, f"FFL {fmt_lvl(F)}"), (eave_z(), f"Ring eaves {fmt_lvl(eave_z())}"),
            (U, f"First floor {fmt_lvl(U)}"), (ridge_z(), f"Ring ridge {fmt_lvl(ridge_z())}"),
            (wing_eave_z(), f"Wing eaves {fmt_lvl(wing_eave_z())}"), (UT, f"Wing ring beam {fmt_lvl(UT)}"),
            (wing_ridge_z(), f"Wing ridge {fmt_lvl(wing_ridge_z())}")] + list(extra)
    rows.sort()
    last = None
    for z, lab in rows:
        right = last is not None and z - last < 1.2   # close to the one below: put this label on the other side
        e.lvl(u, z, lab, 4.4, right=False) if not right else e.lvl(u - 7.5, z, lab, 4.4)
        last = z if not right else None


def _thinnai_side(e, face):
    """Thinnai platform, seat, front pillar, steps and lean-to roof seen from the north or south."""
    u = FACES[face]["u"]
    r17 = room_of("R17") if "R17" in [r[0] for r in ROOMS] else None
    x1, x2 = HX2, r17[3] if r17 else 79.0
    a, b = sorted((u(x1, 0), u(x2, 0)))
    e.rect(a, b, 0, LEVELS["thinnai"], lw=0.5, fill=REDOX)
    stp = next(f[3] for f in SITE_FEATURES if f[0] == "STEPS")
    n = int(round(LEVELS["thinnai"] / LEVELS["riser"]))
    for i in range(n - 1):   # the top riser is the platform's own edge
        e.rect(*sorted((u(stp[0], 0), u(stp[1] - i * (stp[1] - stp[0]) / (n - 1), 0))), i * LEVELS["riser"], (i + 1) * LEVELS["riser"], lw=0.4, fill=STONE)
    for f in FURNITURE:
        if f[0] in ("F42",):
            sa, sb = sorted((u(f[3], 0), u(f[4], 0)))
            e.rect(sa, sb, LEVELS["thinnai"], LEVELS["thinnai"] + 1.5, lw=0.4, fill=colors.HexColor("#E8DCC8"))
    px = THINNAI_PILLARS[0][0]
    top = thinnai_roof_z(px, CY) - TB
    e.rect(u(px, 0) - 0.33, u(px, 0) + 0.33, LEVELS["thinnai"], top, lw=0.5, fill=TEAK)
    ex = THINNAI_ROOF[1]
    e.line(u(ex, 0), thinnai_roof_z(ex, CY), u(ex, 0), 0.3, lw=0.4, color=COPPER, dash=(1, 1))   # rain chain


def elevation(e, face):
    f = FACES[face]
    u = f["u"]
    along = _along(face)
    U_ = (lambda p: u(p, 0)) if along else (lambda p: u(0, p))
    lo, hi = sorted((U_((HX1 if along else HY1) - T / 2), U_((HX2 if along else HY2) + T / 2)))
    g1, g2 = (ROOF["ring"][0] - 3, THINNAI_ROOF[1] + 4) if along else (ROOF["ring"][2] - 3, ROOF["ring"][3] + 3)
    _ground(e, *sorted((U_(g1), U_(g2))))
    e.rect(lo, hi, 0, F, lw=0.6, fill=PLINTH)
    e.rect(lo, hi, F, F + H, lw=0.6, fill=WALLC)
    # upper wing (and, from the east, what stands behind the ring roof: wing, jharokhas, terrace canopy, verge wall)
    wa, wb = (HX1 - T / 2, (NARM_X if face == "N" else RING[0]) + T / 2) if along else (HY1 - T / 2, HY2 + T / 2)
    if face == "S":   # the north arm's south wall (y 33.5), behind the ring roof, east of the west band
        e.rect(*_span(face, RING[0], NARM_X + T / 2), U, UT, lw=0.6, fill=OCHRE)
    e.rect(*_span(face, wa, wb), U, UT, lw=0.6, fill=OCHRE)
    if face in ("S", "N", "W"):
        e.line(*_span(face, wa, wb)[:1], F + H, _span(face, wa, wb)[1], F + H, lw=0.4, color=GREY)   # band at first-floor level
    t = ROOF["terrace"]
    if face == "E":
        _openings_on(e, face, "F1", skip=[j for j in ("W46", "W47")])
        for x1, x2, y1, y2, _ in JHAROKHAS:
            _jharokha(e, *_span(face, y1, y2))
        vx, vy1, vy2, _ = ROOF["verge_east"]
        _gx, (gy1, gy2) = corner_guard_runs()
        _rail(e, *_span(face, gy2, t[3]), SLAB)   # the railing only where the edge wall is the low verge, north of the guard
        n = 64   # the level 4'-0" corner guard to y gy2, a stepped transition there, then the verge 6 in over the roof
        ys = sorted({vy1 + (vy2 - vy1) * i / n for i in range(n + 1)} | {gy2 - 0.001, gy2 + 0.001})
        vpts = [(U_(y), SLAB + verge_east_h(y)) for y in ys]
        e.poly(vpts + [(U_(vy2), SLAB), (U_(vy1), SLAB)], lw=0.5, close=True, fill=WALLC)
        e.text("level guard", (U_(vy1) + U_(gy2)) / 2, SLAB + ROOF["corner_guard"] - 0.55, 3.8, color=GREY)
        for x, y in TERRACE_POSTS:
            if abs(x - RING[1]) < 0.1:
                _post(e, U_(y), SLAB, SLAB + ROOF["canopy"])
        _canopy(e, *_span(face, t[2] - 0.5, t[3] + 0.5))
    elif face == "S":
        for x, y in TERRACE_POSTS:
            if abs(y - t[2]) < 0.1:
                _post(e, U_(x), SLAB, SLAB + ROOF["canopy"])
        _canopy(e, *_span(face, t[0] + T / 2, t[1] + 0.5))
        for x1, x2, y1, y2, _ in reversed(JHAROKHAS):   # J2 on the north arm's south wall (face on), then J1 at the stair head in front of it
            _jharokha(e, *_span(face, x1, x2))
        (gx1, gx2), _g = corner_guard_runs()   # the terrace's south edge: railing on the upstand, then the level corner guard (behind the ring roof)
        _rail(e, *_span(face, t[0] + T / 2, gx1), SLAB)
        e.rect(*_span(face, gx1, gx2 + 0.35), SLAB, SLAB + ROOF["corner_guard"], lw=0.5, fill=WALLC)
    else:
        for fl in ("G", "F1"):
            _openings_on(e, face, fl)
    if face in ("S",):
        for fl in ("G", "F1"):
            _openings_on(e, face, fl)
    if face == "E":
        _openings_on(e, face, "G")
    _roof_profile(e, face)
    if face == "N":   # the roof terrace in front of the ring roof (the jharokhas are hidden behind the north arm)
        a, b = _span(face, t[0], t[1])
        e.rect(a, b, SLAB - 0.5, SLAB, lw=0.5, fill=colors.HexColor("#9A9A9A"))
        _rail(e, a, b, SLAB, jali=True)
        for x, y in TERRACE_POSTS:
            if abs(y - t[3]) < 0.1:
                _post(e, U_(x), SLAB + RAIL_H, SLAB + ROOF["canopy"])
        _canopy(e, *_span(face, t[0] + T / 2, t[1] + 0.5))
        e.text("ROOF TERRACE: TEAK JALI PARAPET, CANOPY ON STEEL POSTS", (a + b) / 2, SLAB + ROOF["canopy"] + 1.2, 4.4, color=GREY)
    if face in ("S", "N"):
        _thinnai_side(e, face)
    if face == "E":   # thinnai in front of the house: platforms, seats, pillars, steps, rain chains
        r17 = room_of("R17")
        e.rect(*_span(face, r17[4], r17[5]), 0, LEVELS["thinnai"], lw=0.5, fill=REDOX)
        for f_ in FURNITURE:
            if f_[0] in ("F42", "F69"):
                e.rect(*_span(face, f_[5], f_[6]), LEVELS["thinnai"], LEVELS["thinnai"] + 1.5, lw=0.4, fill=colors.HexColor("#E8DCC8"))
        for px, py in THINNAI_PILLARS:
            e.rect(U_(py) - 0.33, U_(py) + 0.33, LEVELS["thinnai"], thinnai_roof_z(px, py) - TB, lw=0.5, fill=TEAK)
        stp = next(f_[3] for f_ in SITE_FEATURES if f_[0] == "STEPS")
        nst = int(round(LEVELS["thinnai"] / LEVELS["riser"]))
        for i in range(nst - 1):
            e.rect(*_span(face, stp[2], stp[3]), i * LEVELS["riser"], (i + 1) * LEVELS["riser"], lw=0.4, fill=STONE)
        tr = THINNAI_ROOF
        _fill_profile(e, [(U_(tr[2]), eave_z()), (U_(tr[3]), eave_z())], thinnai_roof_z(tr[1], CY))
        for yy in (tr[2], tr[3]):
            e.line(U_(yy), thinnai_roof_z(tr[1], yy), U_(yy), 0.3, lw=0.4, color=COPPER, dash=(1, 1))
        e.text("THINNAI", U_((r17[4] + r17[5]) / 2), -0.9, 4.4, "Helvetica-Bold")
        e.text("rain chain", U_(tr[3]) + 0.4, 3.0, 4.0, color=COPPER, anchor="l")
    if face == "W":   # the engawa deck and its creeper pergola, in front of the den's west wall
        ot = next(f_[3] for f_ in SITE_FEATURES if f_[0] == "OTTA")
        e.rect(*_span(face, ot[2], ot[3]), 0, 1.5, lw=0.4, fill=colors.HexColor("#C8A97E"))
        pg = next(f_[3] for f_ in SITE_FEATURES if f_[0] == "PERGOLA")
        a, b = _span(face, pg[2], pg[3])
        e.rect(a, b, 8.5, 9.1, stroke=GREEN, lw=0.5, dash=(2, 1))
        for yy in (pg[2], (pg[2] + pg[3]) / 2, pg[3]):
            e.line(U_(yy), 0, U_(yy), 8.5, lw=0.5, color=GREEN, dash=(2, 1))
        e.text("ENGAWA DECK + CREEPER PERGOLA (IN FRONT)", (a + b) / 2, 10.6, 4.2, color=colors.HexColor("#4F6E34"))   # over the pergola: clear of the ground label
    if face == "S":   # the powder room's hooded duct terminal, high over the utility's service door
        t_ = EF_OVER_DOOR
        zc = LEVELS["wet_area"] + t_["z"]; hw = 0.35
        e.rect(t_["x"] - hw, t_["x"] + hw, zc - t_["cowl"] / 2, zc + t_["cowl"] / 2, lw=0.5, fill=STEEL)
        e.poly([(t_["x"] - hw - 0.1, zc + t_["cowl"] / 2), (t_["x"] + hw + 0.1, zc + t_["cowl"] / 2), (t_["x"] + hw + 0.1, zc - t_["cowl"] / 2 - 0.15), (t_["x"] - hw - 0.1, zc - t_["cowl"] / 2 - 0.15)], lw=0.4, close=True)   # the hood, open below
        _tag(e, "EF", t_["x"] + hw + 0.3, zc, "l")
    # downpipes on this face
    for dx, dy in ROOF["downpipes"]:
        on = {"S": dy < HY1, "N": dy > HY2, "E": dx > HX2, "W": dx < HX1}[face]
        if on:
            uu = U_(dx if along else dy)
            e.line(uu, 0.2, uu, eave_z(), lw=0.8, color=STEEL)
    ext = [(SLAB + ROOF["canopy"], f"Terrace canopy {fmt_lvl(SLAB + ROOF['canopy'])}")] if face in ("N", "E", "S") else []
    if face == "E":
        ext.append((LEVELS["thinnai"], f"Thinnai {fmt_lvl(LEVELS['thinnai'])}"))
    _levels(e, min(U_(g1), U_(g2)) - 0.5, ext)
    e.hdim(lo, hi, -2.4, f"{fmt_ft(hi - lo)} incl. walls", 5)
    _draw_tags(e)


def sheet_elev_long(c):
    s = Sheet(c, "A-201", "North and south elevations", "1:100")
    for i, face in enumerate(("N", "S")):
        e = Elev(s, 100, (22 if face == "N" else 48) * mm, (166 - i * 128) * mm)   # the south view sits right: its level tags stay inside the frame
        elevation(e, face)
        s.note(FACES[face]["title"].upper(), 22 * mm, (166 - i * 128 + 98) * mm, 9, INK, "Helvetica-Bold")
    s.note("Single-storey ring of rooms round the open courtyard (mutram), with the two-storey west wing on the left of the south view and the right of the north view.", 22 * mm, 24 * mm, 7, GREY)
    s.note("Ring roof: four tiled slopes, the outer ones to the eaves and gutters seen here, the inner ones into the courtyard behind the ridge. Brown line = fascia with gutter; grey lines = downpipes.", 22 * mm, 19.5 * mm, 7, GREY)
    s.note("North: the roof terrace over the family living, teak jali parapet to the neighbour, light canopy on steel posts. South: the canopy and the stair-head jharokha seen over the ring roof.", 22 * mm, 15 * mm, 7, GREY)
    c.showPage()


ELEV_TIPS = [
    "East (road): the thinnai's red oxide platform either side of the carved main door D01 in the north half of the east wall, two turned teak pillars, three stone steps with rails both sides, the reserved ramp to its south edge and copper rain chains at the front corners. Behind the low ring roof stand the upper wing, the roof terrace's canopy and its corner guard and east verge wall.",
    f"Thinnai roof: a lean-to continuing the ring roof's east slope at {ROOF['pitch']} deg, its eave {fmt_ft(ROOF['thinnai'][1] - THINNAI_PILLARS[0][0])} past the turned pillars; {fmt_ft(thinnai_headroom())} clear over the platform at the pillars.",
    "West (back garden): the two-storey wing on the full width, small high windows upstairs (afternoon sun), the den's garden door onto the engawa deck under its creeper pergola.",
    "Plinth face clad 2 ft in rough stone: the splash zone stays clean and does not erode.",
    "Entrance: 3 risers of 6 in, 12 in treads, flamed granite with a nosing; foot-wash tap beside the steps.",
]


def sheet_elev_short(c):
    s = Sheet(c, "A-202", "East (road) and west elevations", "1:100")
    for i, face in enumerate(("E", "W")):
        e = Elev(s, 100, 72 * mm, (160 - i * 128) * mm)   # room on the left for both columns of level tags
        elevation(e, face)
        s.note(FACES[face]["title"].upper(), 22 * mm, (160 - i * 128 + 98) * mm, 9, INK, "Helvetica-Bold")
    s.bullets(ELEV_TIPS, 248 * mm, 262 * mm, 76 * mm, 6.6, title="Notes")
    s.note("Courtyard (mutram) at the centre, hidden by the ring roof in these views: see sections A-A and B-B on A-301.", 22 * mm, 15 * mm, 7, GREY)
    c.showPage()


# ---------- sections ----------
def _cut_walls(axis_cut, c0):
    """Walls of the floor being drawn crossed by a section line. axis_cut 'X' = cut at x=c0 (walls running along X are crossed)."""
    return [(w, w[1]) for w in WALLS if w[0] == axis_cut and w[2] - 0.05 <= c0 <= w[3] + 0.05]


def _roof_band(e, pts, fill=TILE):
    """A roof cut by the section: the surface line and its build-up below it, one band per run."""
    runs, cur = [], []
    for u_, z in pts:
        if z is None:
            if cur: runs.append(cur); cur = []
        else:
            cur.append((u_, z))
    if cur: runs.append(cur)
    for r in runs:
        if len(r) > 1:
            e.poly(r + [(p, z - TT) for p, z in reversed(r)], lw=0.6, close=True, fill=fill)


def _stair_beyond(e):
    """B-B looks north at both flights end on: flight 1 rising away on the west, the half landing, flight 2 coming back
    to the stair head on the east, the full-height core wall between them."""
    st = STAIR
    rz = LEVELS["upper_ffl"] / st["risers"]
    f1, f2, ld, core = st["flight1"], st["flight2"], st["landing"], st["core"]
    n1 = f1[4]
    zl = F + n1 * rz
    e.rect(f1[0], f1[1], F, zl, lw=0.5, fill=STONE)
    for k in range(1, n1): e.line(f1[0], F + k * rz, f1[1], F + k * rz, lw=0.25, color=GREY)
    e.rect(ld[0], ld[1], zl - 0.5, zl, lw=0.4, dash=(2, 1))
    # flight 2 runs over the DB cupboard and the cut (y = CY) crosses it: only its cut waist shows, above the cupboard (which is cut too)
    n_up = math.ceil((f2[3] - CY) / st["tread"] - 1e-6)   # treads from the landing to the cut
    zt = zl + n_up * rz
    e.rect(f2[0], f2[1], zt - 0.5, zt, lw=0.6, fill=HATCH)
    top = (wing_roof_z((core[0] + core[1]) / 2, CY) or UT) - TT
    e.rect(core[0], core[1], F, top, lw=0.5, fill=HATCH)
    mx = (f1[0] + f1[1]) / 2
    e.text("STAIR", mx, zl + 2.6, 4.2, "Helvetica-Bold")
    e.text("BEYOND", mx, zl + 1.6, 4.2, "Helvetica-Bold")
    e.text("flight 1", mx, F + 2.5, 3.6, color=GREY)
    e.text("flight 2 (cut)", (f2[0] + f2[1]) / 2, zt + 0.5, 3.6, color=GREY)


def _knockout(e, text, u, z, size, font="Helvetica-Bold", color=BLUE):
    """A label on a white box, so lines behind it do not cross it."""
    w = e.c.stringWidth(text, font, size) / e.k + 0.4
    h = size * 1.25 / e.k
    e.rect(u - w / 2, u + w / 2, z - h / 2, z + h / 2, stroke=None, fill=WHITE)
    e.text(text, u, z, size, font, color)


LTILE = colors.HexColor("#E8CDBE")
LOCHRE = colors.HexColor("#F4EBD8")


def _beyond(e, axis, c0, rng, at, ca, cb):
    """What the section looks at beyond the cut, drawn light and clipped to where it can be seen: above the cut roofs,
    through the open court and over the terrace. A-A (looking west): the wing's east face with its windows and both
    jharokhas, its hip roof, the west walkway roof. B-B (looking north): the terrace canopy, posts and railing, the north roofs."""
    step = 0.25
    n = int(round((rng[1] - rng[0]) / step))
    lows = []
    for i in range(n + 1):
        u_ = rng[0] + i * step
        zs = [z for z in (ring_vis(*at(u_)), wing_roof_z(*at(u_)), thinnai_roof_z(*at(u_))) if z is not None]
        if zs:
            lo = max(zs)
        elif ca < u_ < cb:
            lo = LEVELS["courtyard"]
        else:
            t = ROOF["terrace"]
            on_t = (t[2] < u_ < t[3]) if axis == "X" else (t[0] < u_ < t[1] and c0 < t[2])
            lo = SLAB if on_t else 0.0
        lows.append((u_, lo))
    c = e.c
    c.saveState()
    path = c.beginPath()
    path.moveTo(*e.p(rng[0], 40))
    for u_, z in lows:
        path.lineTo(*e.p(u_, z))
    path.lineTo(*e.p(rng[1], 40)); path.close()
    c.clipPath(path, stroke=0, fill=0)
    t = ROOF["terrace"]
    if axis == "X":   # looking west
        w = wing_bbox()
        prof = []
        for k in range(int((w[3] - w[2]) / step) + 1):
            y = w[2] + k * step
            prof.append((y, max(z for z in (wing_roof_z(w[0] + j * step, y) for j in range(int((w[1] - w[0]) / step) + 1)) if z is not None)))
        e.poly(prof + [(w[3], wing_eave_z()), (w[2], wing_eave_z())], lw=0.3, color=GREY, close=True, fill=LTILE)
        e.rect(HY1 - T / 2, HY2 + T / 2, U, UT, lw=0.3, stroke=GREY, fill=LOCHRE)
        with on_floor("F1"):
            for wd in WINDOWS:
                if (wd[1], wd[2]) == ("Y", RING[0]) and wd[0] not in ("W46", "W47"):
                    e.rect(wd[3], wd[4], U + wd[5], U + wd[6], lw=0.3, stroke=GREY, fill=colors.HexColor("#DCE6EA"))
            for d in DOORS:
                if (d[1], d[2]) == ("Y", RING[0]):
                    e.rect(d[3], d[4], U, U + LEVELS["door_head"], lw=0.3, stroke=GREY, fill=colors.HexColor("#CDBBA8"))
        for x1, x2, y1, y2, _ in JHAROKHAS:
            _jharokha(e, y1, y2)
        rp = [(y, max([z for z in (ring_vis(x, y) for x in [RING[0] + (j + 0.5) * step for j in range(int((c0 - RING[0]) / step))]) if z is not None] or [None]) if True else None) for y in [ROOF["ring"][2] + k * step for k in range(int((ROOF["ring"][3] - ROOF["ring"][2]) / step) + 1)]]
        _fill_profile(e, rp, eave_z(), fill=LTILE, edge=GREY)
        e.text("WING EAST FACE AND JHAROKHAS BEYOND", (CT[2] + CT[3]) / 2, UT + 0.9, 3.8, color=GREY)
    else:             # looking north: the wing's north arm (its roof, its south wall and J2), then the terrace
        w2 = wing_rects()[1]
        prof = []
        for k in range(int((w2[1] - w2[0]) / step) + 1):
            x = w2[0] + k * step
            zs = [wing_roof_z(x, c0 + j * step) for j in range(int((w2[3] - c0) / step) + 1)]
            prof.append((x, max([z for z in zs if z is not None] or [None])))
        _fill_profile(e, prof, wing_eave_z(), fill=LTILE, edge=GREY)
        e.rect(RING[0], NARM_X + T / 2, U, UT, lw=0.3, stroke=GREY, fill=LOCHRE)
        for x1, x2, y1, y2, _ in JHAROKHAS:
            if y1 > c0:
                _jharokha(e, x1, x2)
        e.text("WING NORTH ARM AND J2 BEYOND", w2[1] + 0.6, UT + 0.6, 3.8, color=GREY, anchor="l")   # east of its hip, clear of the cut roof
        zc = SLAB + ROOF["canopy"]
        for x, y in TERRACE_POSTS:
            if y > c0:
                e.rect(x - 0.17, x + 0.17, SLAB, zc, lw=0.3, stroke=GREY, fill=colors.HexColor("#C9CDD1"))
        (gx1, gx2), _g = corner_guard_runs()   # the south edge: railing, then the level corner guard wall
        e.rect(t[0], gx1, SLAB, SLAB + RAIL_H, lw=0.3, stroke=GREY)
        for k in range(1, int((gx1 - t[0]) * 2)):
            e.line(t[0] + k * 0.5, SLAB, t[0] + k * 0.5, SLAB + RAIL_H, lw=0.15, color=GREY)
        e.rect(gx1, gx2 + 0.35, SLAB, SLAB + ROOF["corner_guard"], lw=0.3, stroke=GREY, fill=colors.HexColor("#F2EFEA"))
        e.rect(t[0] + T / 2, t[1] + 0.5, zc, zc + 0.35, lw=0.3, stroke=GREY, fill=colors.HexColor("#EBCDBF"))
        e.text(f"terrace canopy beyond {fmt_lvl(zc)}", (t[0] + t[1]) / 2, zc + 0.9, 3.8, color=GREY)
        rp = [(x, max([z for z in (ring_vis(x, c0 + j * step) for j in range(1, int((ROOF["ring"][3] - c0) / step) + 1)) if z is not None] or [None])) for x in [ROOF["ring"][0] + (k + 0.5) * step for k in range(int((ROOF["ring"][1] - ROOF["ring"][0]) / step) + 1)]]
        rp = [(x, z if not (t[0] < x < t[1] and z is not None and z < SLAB + RAIL_H and False) else z) for x, z in rp]
        _fill_profile(e, rp, eave_z(), fill=LTILE, edge=GREY)
    c.restoreState()


def section(e, name):
    axis, c0, _ = SECTIONS[name]
    # A-A: cut at x = c0, u = y, looking west. B-B: cut at y = c0, u = x, looking north.
    if axis == "X":
        at = lambda u_: (c0, u_)
        span = lambda r: (r[4], r[5])
        inside = lambda r: r[2] < c0 <= r[3]   # a room whose edge lies on the cut counts on its west side only
        rng = (ROOF["ring"][2] - 4, ROOF["ring"][3] + 4)
        hu1, hu2 = HY1, HY2
    else:
        at = lambda u_: (u_, c0)
        span = lambda r: (r[2], r[3])
        inside = lambda r: r[4] <= c0 < r[5]   # a room whose edge lies on the cut counts on its north side only
        rng = (ROOF["ring"][0] - 4, THINNAI_ROOF[1] + 4)
        hu1, hu2 = HX1, HX2
    _ground(e, *rng)
    labels = []   # the cut rooms' names and ceilings: drawn last, on white, over the stair beyond and the roofs
    # ground floor: fill under every floor, the floors, ceilings and room names
    with on_floor("G"):
        rooms = [r for r in ROOMS if inside(r)]
        for r in rooms:
            a, b = span(r)
            fz = floor_level(r[0])
            e.rect(a, b, 0, fz - 0.33, stroke=None, fill=colors.HexColor("#E6DDC8"))
            e.rect(a, b, fz - 0.33, fz, lw=0.4, fill=colors.HexColor("#CFCFCF"))
        big = max(rooms, key=lambda r: (span(r)[1] - span(r)[0]) if r[0] != "R50" else 0)
        e.text("compacted moorum fill (no black soil)", sum(span(big)) / 2, F / 2 - 0.4, 3.8, color=GREY)
    for fl in ("G", "F1"):
        base = floor_base(fl)
        with on_floor(fl):
            walls = _cut_walls(axis, c0)
            top = base + (H if fl == "G" else LEVELS["upper_wall_top"])
            if fl == "G":
                for w, c in walls:
                    t = wall_t(w)
                    e.rect(c - 1.4, c + 1.4, -4.5, -3.8, lw=0.4, dash=(2, 1))      # footing (engineer)
                    e.rect(c - t / 2, c + t / 2, -3.8, 0, lw=0.3, dash=(2, 1))
                    e.rect(c - t / 2 - 0.05, c + t / 2 + 0.05, F - 1.25, F - 0.33, lw=0.5, fill=colors.HexColor("#9A9A9A"))  # plinth beam
            for r in [r for r in ROOMS if inside(r)]:
                a, b = span(r)
                kind, v = CEILINGS[r[0]]
                nm = short_name(r[1]).split(" (")[0].upper()
                if r[0] == "R50" or (r[0] == "R06" and axis == "Y"):
                    continue   # the court is labelled on its own below; B-B's stair is named by the stair drawing
                ny = base + (4.6 if fl == "G" else 4.0)
                if kind == "flat":
                    e.line(a + 0.2, base + v, b - 0.2, base + v, lw=0.6, color=BLUE)
                if r[0] in ("R51", "R61", "R62", "R63"):
                    labels.append(("WALKWAY", (a + b) / 2, ny, 4.0, "Helvetica-Bold", INK))
                    continue
                if r[0] == "R37":
                    labels.append(("ROOF TERRACE", (a + b) / 2, base + 6.0, 4.6, "Helvetica-Bold", INK))
                    continue
                size = 4.6 if b - a > 7 else 3.8
                labels.append((nm, (a + b) / 2, ny, size, "Helvetica-Bold", INK))
                if kind == "flat" and b - a > 6:
                    labels.append((f"ceiling {fmt_ft(v)}", (a + b) / 2, ny - 1.1, 3.8, "Helvetica", BLUE))
            for w, c in walls:
                t = wall_t(w)
                a0, b0 = c - t / 2, c + t / 2
                hits = [(k, rec) for (s_, e_, k, rec) in openings_for(w[0], w[1], w[2], w[3]) if s_ <= c0 <= e_]
                gaps = [(base + (0 if k == "door" else rec[5]), base + (LEVELS["door_head"] if k == "door" else rec[6])) for k, rec in hits]
                z = base if fl == "F1" else F - 0.33
                for g1, g2 in sorted(gaps):
                    if g1 > z: e.rect(a0, b0, z, g1, lw=0.6, fill=HATCH)
                    z = g2
                e.rect(a0, b0, z, top, lw=0.6, fill=HATCH)
                e.rect(a0 - 0.05, b0 + 0.05, top - 0.75, top, lw=0.5, fill=colors.HexColor("#8A8A8A"))  # ring beam / band
            for ax, cc, s_, e_ in RAILS:
                if ax == axis and s_ - 0.05 <= c0 <= e_ + 0.05:
                    jali = (ax, cc) in JALI_RAILS
                    e.rect(cc - 0.15, cc + 0.15, base, SLAB + RAIL_H if fl == "F1" else base + RAIL_H, lw=0.5, fill=colors.HexColor("#C8A97E") if jali else JALI)
    # first-floor slab where the cut crosses it
    for x1, x2, y1, y2 in SLAB_F1:
        if (axis == "X" and x1 <= c0 <= x2) or (axis == "Y" and y1 <= c0 <= y2):
            a, b = (y1, y2) if axis == "X" else (x1, x2)
            e.rect(a, b, U - LEVELS["slab"], U, lw=0.5, fill=colors.HexColor("#9A9A9A"))
    # the open court: sunken stone floor, tulsi bed, grille at the eave, its pillars and the walkway lean-to
    ce = ROOF["court_eave"]
    ca, cb = (CT[2], CT[3]) if axis == "X" else (CT[0], CT[1])
    ea, eb = (ce[2], ce[3]) if axis == "X" else (ce[0], ce[1])
    e.rect(ca, cb, LEVELS["courtyard"], eave_z(), stroke=None, fill=SKY)
    _beyond(e, axis, c0, rng, at, ca, cb)
    e.rect(ca, cb, LEVELS["courtyard"] - 0.33, LEVELS["courtyard"], lw=0.5, fill=STONE)
    e.rect(ca, cb, 0, LEVELS["courtyard"] - 0.33, stroke=None, fill=colors.HexColor("#E6DDC8"))
    tb = next(f for f in FURNITURE if f[0] == "F128")
    ta, tb_ = (tb[5], tb[6]) if axis == "X" else (tb[3], tb[4])
    e.rect(ta, tb_, LEVELS["courtyard"], LEVELS["courtyard"] + 1.5, lw=0.5, fill=PLINTH)
    e.poly([((ta + tb_) / 2 - 0.9, LEVELS["courtyard"] + 1.5), ((ta + tb_) / 2, LEVELS["courtyard"] + 3.4), ((ta + tb_) / 2 + 0.9, LEVELS["courtyard"] + 1.5)], lw=0.4, color=GREEN, close=True, fill=colors.HexColor("#DCE8CC"))
    e.text("tulsi bed", tb_ + 0.4, LEVELS["courtyard"] + 0.8, 3.8, color=GREEN, anchor="l")
    gz = ROOF["grille_z"]
    e.line(ea, gz, eb, gz, lw=1.2, color=STEEL)
    k = ea
    while k < eb:
        e.line(k, gz - 0.15, k, gz + 0.15, lw=0.3, color=STEEL); k += 0.5
    with on_floor("G"):
        for px, py in WALKWAY_PILLARS:
            p, d = (py, px) if axis == "X" else (px, py)
            beyond = (d < c0 - 0.4) if axis == "X" else (d > c0 + 0.4)
            cut = abs(d - c0) <= 0.4
            if not (cut or beyond):
                continue
            ztop = ring_z(px, py) - TT
            e.rect(p - 0.36, p + 0.36, LEVELS["walkway"], ztop, lw=0.6 if cut else 0.3, fill=HATCH if cut else None, stroke=INK if cut else GREY)
            if cut:
                e.rect(p - 1.0, p + 1.0, -3.3, -2.7, lw=0.4, dash=(2, 1))
    zl = 7.4 if axis == "Y" else 5.6
    _knockout(e, "MUTRAM (OPEN COURTYARD)", (ca + cb) / 2, zl, 5.2)
    _knockout(e, f"open to the sky; sunken stone floor {fmt_lvl(LEVELS['courtyard'])}", (ca + cb) / 2, zl - 1.2, 3.9, "Helvetica")
    _knockout(e, f"steel grille + shade-cloth track at the eave {fmt_lvl(gz)}", (ca + cb) / 2, gz + 0.8, 3.9, "Helvetica", STEEL)
    # roofs cut by the section: the ring (outer slopes, inner slopes over the walkways), the wing, the thinnai lean-to
    n = 480
    us = [rng[0] + (rng[1] - rng[0]) * i / n for i in range(n + 1)]
    _roof_band(e, [(u_, ring_vis(*at(u_))) for u_ in us])
    _roof_band(e, [(u_, wing_roof_z(*at(u_))) for u_ in us])
    _roof_band(e, [(u_, thinnai_roof_z(*at(u_))) for u_ in us])
    # walkway lean-to labels (the ring's inner slope carried on over the walkway to the inner eave)
    walks = ((RING[2], CT[2]), (CT[3], RING[3])) if axis == "X" else ((RING[0], CT[0]), (CT[1], RING[1]))
    for wa, wb in walks:
        zz = ring_vis(*at((wa + wb) / 2))
        if zz is not None:
            _knockout(e, "lean-to", (wa + wb) / 2, zz - TT - 1.0, 3.8, "Helvetica", BROWN)
    # roof terrace (A-A): upstand on its south edge, canopy on steel posts
    t = ROOF["terrace"]
    if axis == "X" and t[0] <= c0 <= t[1]:
        e.rect(t[2] - 0.25, t[2] + 0.25, U, SLAB + ROOF["upstand"], lw=0.6, fill=HATCH)
        e.rect(t[2] - 0.08, t[2] + 0.08, SLAB + ROOF["upstand"], SLAB + RAIL_H, lw=0.4, fill=JALI)       # the railing on the upstand, to 4'-0"
        e.line(t[2] - 0.2, SLAB + RAIL_H, t[2] + 0.2, SLAB + RAIL_H, lw=1.0, color=TEAK)
        zc = SLAB + ROOF["canopy"]
        e.rect(t[2] - 0.5, t[3] + 0.5, zc, zc + 0.35, lw=0.5, fill=colors.HexColor("#D8A98F"))
        for x, y in TERRACE_POSTS:
            if abs(x - c0) < 0.4:
                e.rect(y - 0.17, y + 0.17, U, zc, lw=0.5, fill=STEEL)
            elif x < c0:
                e.rect(y - 0.17, y + 0.17, U, zc, lw=0.3, stroke=GREY)
        e.rect(t[3] - 0.17, t[3] + 0.17, U, SLAB + RAIL_H, lw=0.5, fill=colors.HexColor("#C8A97E"))   # north jali parapet, in front of its post
        e.text("jali parapet", t[3] - 0.5, SLAB + RAIL_H - 1.0, 3.6, color=GREY, anchor="r")
        e.text(f"canopy {fmt_lvl(zc)}, light tiles on steel", (t[2] + t[3]) / 2, zc + 0.9, 3.9, color=GREY)
        e.text(f"slab {fmt_lvl(SLAB)}; south upstand {fmt_ft(ROOF['upstand'])}, 4'-0\" railing", (t[2] + t[3]) / 2, SLAB + 1.2, 3.8, color=GREY)
    # B-B: the stair beyond, the stair-head jharokha, the thinnai and its steps
    if axis == "Y":
        _stair_beyond(e)
        for x1, x2, y1, y2, seat in JHAROKHAS:
            if y1 <= c0 <= y2:
                zb = U + seat
                base = zb - JHAROKHA_DECK
                e.poly([(x1 + 0.15, ring_z(x1 + 0.15, c0)), (x2 - 0.15, ring_z(x2 - 0.15, c0)), (x2 - 0.15, base), (x1 + 0.15, base)], lw=0.5, close=True, fill=HATCH)   # flashed kerb
                _knockout(e, f"{fmt_ft(ROOF['jharokha_kerb'])} flashed kerb", x2 + 3.0, base - 0.4, 3.6, "Helvetica", BLUE)
                e.rect(x1, x2, base, zb, lw=0.6, fill=TEAK)
                e.rect(x2 - 0.2, x2, zb, zb + 3.0, lw=0.5, fill=JALI)
                e.rect(x2 - 0.1, x2, zb + 3.0, U + 7.5, lw=0.5, fill=colors.HexColor("#B9CCD3"))
                e.poly([(x1, U + 8.0), (x2 + 0.4, U + 7.5), (x2 + 0.4, U + 7.3), (x1, U + 7.8)], lw=0.5, close=True, fill=COPPER)
                _knockout(e, "JHAROKHA", x2 + 2.4, zb + 1.8, 4.0, color=INK)
                _knockout(e, f"seat {fmt_ft(seat)} above the floor", x2 + 3.6, zb + 0.8, 3.6, "Helvetica", GREY)
        stp = next(f[3] for f in SITE_FEATURES if f[0] == "STEPS")
        if stp[2] <= c0 <= stp[3]:
            nst = int(round(LEVELS["thinnai"] / LEVELS["riser"]))
            for i in range(nst - 1):
                e.rect(stp[0], stp[1] - i * (stp[1] - stp[0]) / (nst - 1), i * LEVELS["riser"], (i + 1) * LEVELS["riser"], lw=0.3, fill=STONE)
        for px, py in THINNAI_PILLARS:
            if py > c0:
                e.rect(px - 0.33, px + 0.33, LEVELS["thinnai"], thinnai_roof_z(px, py) - TB, lw=0.3, stroke=GREY)
        e.text("glass tiles over the stair", (HX1 + _SE_()) / 2, wing_roof_z(HX1 + 4, c0) + 1.6, 3.8, color=BLUE)
    for edge, sgn in ((hu1 - T / 2, -1), ((hu2 + T / 2) if axis == "X" else THINNAI_ROOF[1] + 1.5, 1)):
        e.poly([(edge, 0.25), (edge + sgn * 3, 0.05), (edge + sgn * 3, -0.2), (edge, -0.2)], lw=0.4, close=True, fill=colors.HexColor("#CFCFCF"))
    _levels(e, rng[0] - 0.3, [(LEVELS["courtyard"], f"Courtyard {fmt_lvl(LEVELS['courtyard'])}")])
    for text, u_, z_, size, font, color in labels:
        _knockout(e, text, u_, z_, size, font, color)


def _SE_():
    return STAIR["flight2"][1]


SECTION_NOTES = [
    "Ring roof: clay Mangalore tiles on battens, membrane, 50 mm insulation, deck on rafters; its inner slope runs on over the walkway on teak or stone pillars (the walkway lean-to) and drops rain into the courtyard.",
    f"Courtyard (mutram): open to the sky, sunk {round((LEVELS['walkway'] - LEVELS['courtyard']) * 12)} in below the walkway (6 in below the rooms), stone on a falls slab to the drains (first-flush filter, overflow); a galvanised steel grille at the inner eave with a track for the pull-across shade cloth.",
    "West wing: hipped tiled roof, trusses bolted to the first-floor ring beam (cyclone uplift); a few clear glass tiles over the stair. Ring roof rafters bolted to the ground-floor ring beam; apron flashing where they meet the wing's east wall.",
    "Roof terrace over the family living: waterproofed RCC slab falling 1:80 to its outlet, 1'-9\" upstand on the south edge, 4'-0\" railing (teak jali parapet on the north), light tiled canopy on galvanised steel posts.",
    "RCC lintel band at door-head level on both floors (seismic zone III). AAC walls in an RCC frame; mesh over every block-to-concrete joint.",
    f"Ground-floor rooms: plastered ceilings at 9'-6\" (blue), baths at 8'-6\", the living {fmt_ft(CEILINGS['R16'][1])} (the terrace slab's soffit, {fmt_lvl(floor_level('R16') + CEILINGS['R16'][1])}, under the {fmt_lvl(terrace_slab_z())} terrace); the stair is open to the wing roof; the walkway shows its rafters.",
    "Dog-leg stair, 16 risers of 7.5 in, 10 in treads, handrails both sides, a full-height core wall between the flights.",
    "Plinth beam with DPC; plinth fill of compacted moorum, never black soil; anti-termite treatment at every layer.",
    "Footings dashed and indicative only: type and depth by the engineer after the soil test (walkway and thinnai pillars on their own pads).",
]


def sheet_sections(c):
    s = Sheet(c, "A-301", "Sections A-A and B-B", "1:100")
    e = Elev(s, 100, 32 * mm - (ROOF["ring"][0] - 4) * 3.048 * mm + 40 * mm, 168 * mm)   # room on the left for both columns of level tags
    section(e, "B")
    s.note("SECTION B-B: " + SECTIONS["B"][2].upper(), 22 * mm, 268 * mm, 8, INK, "Helvetica-Bold")
    e = Elev(s, 100, 32 * mm - (ROOF["ring"][2] - 4) * 3.048 * mm + 40 * mm, 40 * mm)
    section(e, "A")
    s.note("SECTION A-A: " + SECTIONS["A"][2].upper(), 22 * mm, 140 * mm, 8, INK, "Helvetica-Bold")
    s.bullets(SECTION_NOTES, 262 * mm, 136 * mm, 62 * mm, 6.0, title="Section notes")
    c.showPage()
