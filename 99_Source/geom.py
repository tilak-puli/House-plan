import math
import re
from model import *
import model as _model

EPS = 1e-6
TAN = math.tan(math.radians(ROOF["pitch"]))
HIP_K = math.sqrt(1 + TAN * TAN / 2)   # true length / plan length of a 45-degree hip or valley between two slopes of this pitch


def wall_type(w):
    axis, c, s, e = w
    if (axis, c) in EXTERIOR or w in EXTRA_EXT_WALLS:
        return "EXT"
    return "WET" if w in WET_WALLS else "INT"


def wall_t(w):
    return WALL_TYPES[wall_type(w)][0]


def openings_for(axis, c, s, e):
    out = []
    for d in DOORS:
        if d[1] == axis and abs(d[2] - c) < EPS and d[3] >= s - EPS and d[4] <= e + EPS:
            out.append((d[3], d[4], "door", d))
    for w in WINDOWS:
        if w[1] == axis and abs(w[2] - c) < EPS and w[3] >= s - EPS and w[4] <= e + EPS:
            out.append((w[3], w[4], "window", w))
    return sorted(out, key=lambda o: o[0])


def seg_rect(axis, c, a, b, t=T):
    t = t / 2
    if axis == "X":
        return (a, b, c - t, c + t)
    return (c - t, c + t, a, b)


def wall_rects(with_type=False):
    """Solid wall pieces (x1,x2,y1,y2) after removing door/window openings."""
    rects = []
    for w in WALLS:
        axis, c, s, e = w
        t = wall_t(w)
        ops = openings_for(axis, c, s, e)
        cur = s - t / 2
        end = e + t / 2
        pieces = []
        for a, b, _, _ in ops:
            if a > cur:
                pieces.append(seg_rect(axis, c, cur, a, t))
            cur = max(cur, b)
        if end > cur:
            pieces.append(seg_rect(axis, c, cur, end, t))
        rects += [(p, wall_type(w)) for p in pieces] if with_type else pieces
    return rects


def opening_rects():
    out = []
    for w in WALLS:
        axis, c, s, e = w
        for a, b, kind, rec in openings_for(axis, c, s, e):
            out.append((seg_rect(axis, c, a, b, wall_t(w)), kind, rec, axis, c, a, b))
    return out


def fmt_ft(v):
    neg = v < 0
    v = abs(v)
    ft = int(v + 1e-6)
    inch = round((v - ft) * 24) / 2  # nearest half inch
    if inch >= 12:
        ft, inch = ft + 1, inch - 12
    inch = int(inch) if inch == int(inch) else inch
    return ("-" if neg else "") + f"{ft}'-{inch}\""


def fmt_lvl(v):
    return ("+" if v >= 0 else "") + fmt_ft(v)


def room_dims(r):
    _, _, x1, x2, y1, y2, _ = r
    return x2 - x1, y2 - y1


def _edge_t(axis, c, s, e):
    """Half-thickness of the wall along a room edge (0 if the edge is open)."""
    best = 0
    for w in WALLS:
        if w[0] == axis and abs(w[1] - c) < EPS and w[2] < e - EPS and w[3] > s + EPS:
            best = max(best, wall_t(w) / 2)
    return best


def clear_dims(r):
    """Clear (wall-face to wall-face) room size, ft."""
    _, _, x1, x2, y1, y2, _ = r
    L = x2 - x1 - _edge_t("Y", x1, y1, y2) - _edge_t("Y", x2, y1, y2)
    W = y2 - y1 - _edge_t("X", y1, x1, x2) - _edge_t("X", y2, x1, x2)
    return L, W


def room_of(rid):
    return next(r for r in ROOMS if r[0] == rid)


def plot_area():
    """Plot area (sq ft), from the boundary polygon."""
    pts = PLOT + PLOT[:1]
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:]))) / 2


def plot_perimeter():
    pts = PLOT + PLOT[:1]
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def floor_level(rid):
    return LEVELS["FFL"] + (LEVELS["upper_ffl"] if rid in F1_ROOM_IDS else 0) + ROOM_FLOOR.get(rid, 0)


def upper_wall_top_z():
    """Top of the first-floor walls (main roof ring beam) above finished ground."""
    return LEVELS["FFL"] + LEVELS["upper_ffl"] + LEVELS["upper_wall_top"]


# ---- roof: heights above finished ground (FGL = 0) ----
def eave_z():
    """Ring roof eave (outer and inner): the ground-floor wall top less the overhang's fall."""
    return LEVELS["FFL"] + LEVELS["wall_top"] - ROOF["overhang"] * TAN


ROOF["grille_z"] = eave_z()   # the court's steel grille sits at the inner eave height


def _in(r, x, y):
    return r[0] <= x <= r[1] and r[2] <= y <= r[3]


def _inside(r, x, y):
    return r[0] < x < r[1] and r[2] < y < r[3]


def _to_outer_eave(r):
    """A plan rect carried out to the ring's outer eave on every side that sits on an outer wall (the overhang beyond that wall is the
    rect's own, not the ring roof's)."""
    o = ROOF["ring"]
    return (o[0] if r[0] <= HX1 + 1e-9 else r[0], o[1] if r[1] >= HX2 - 1e-9 else r[1],
            o[2] if r[2] <= HY1 + 1e-9 else r[2], o[3] if r[3] >= HY2 - 1e-9 else r[3])


def ring_holes():
    """Where the ring roof does not run: the upper wing (its walls and its own outer eaves) and the terrace slab (with no eave past
    its north parapet). The open court is the third hole (ROOF['court_eave'])."""
    return [_to_outer_eave(r) for r in ROOF["wing_walls"]] + [_to_outer_eave(ROOF["terrace"])]


def ring_z(x, y):
    """Ring roof height at (x, y): None outside the ring, over the open court, over the terrace slab and inside the upper wing (the ring
    roof stops against the wing's walls; under the wing's courtyard-side eaves it runs on below them)."""
    o, i = ROOF["ring"], ROOF["court_eave"]
    if not _in(o, x, y) or _inside(i, x, y) or any(_inside(h, x, y) for h in ring_holes()):
        return None
    d_out = min(x - o[0], o[1] - x, y - o[2], o[3] - y)
    d_in = max(i[0] - x, x - i[1], i[2] - y, y - i[3])
    return eave_z() + TAN * min(d_out, d_in)


def ridge_z():
    o, i = ROOF["ring"], ROOF["court_eave"]
    return eave_z() + TAN * min(i[0] - o[0], o[3] - i[3], i[2] - o[2], o[1] - i[1]) / 2


def ring_ridge_rect():
    """The ring's ridge line, a rectangle midway between the outer and the inner eave."""
    o, i = ROOF["ring"], ROOF["court_eave"]
    return ((o[0] + i[0]) / 2, (o[1] + i[1]) / 2, (o[2] + i[2]) / 2, (o[3] + i[3]) / 2)


def ring_valley_points(step=0.05):
    """Sample points (x, y) along the ring roof's four inner valleys (court-eave corners out to the ridge corners) where the roof exists."""
    i, r = ROOF["court_eave"], ring_ridge_rect()
    pts = []
    for (ax, ay), (bx, by) in (((i[0], i[2]), (r[0], r[2])), ((i[1], i[2]), (r[1], r[2])), ((i[0], i[3]), (r[0], r[3])), ((i[1], i[3]), (r[1], r[3]))):
        n = int(round(abs(bx - ax) / step))
        for k in range(n + 1):
            x, y = ax + (bx - ax) * k / n, ay + (by - ay) * k / n
            if ring_z(x, y) is not None:
                pts.append((x, y))
    return pts


def wing_rects():
    """The upper wing's roof as hipped rectangles (an L: the west band and the north arm over the family room)."""
    return [ROOF["wing"], ROOF["wing_ext"]]


def wing_bbox():
    rs = wing_rects()
    return (min(r[0] for r in rs), max(r[1] for r in rs), min(r[2] for r in rs), max(r[3] for r in rs))


def wing_eave_z():
    """Eave of the hipped roof over the upper west wing."""
    return upper_wall_top_z() - ROOF["overhang"] * TAN


def _hip_z(w, x, y):
    return wing_eave_z() + TAN * min(x - w[0], w[1] - x, y - w[2], w[3] - y)


def wing_roof_z(x, y):
    """The wing's L roof: the higher of the two hipped rectangles (same pitch and eave), which gives one valley at the re-entrant corner."""
    zs = [_hip_z(w, x, y) for w in wing_rects() if _in(w, x, y)]
    return max(zs) if zs else None


def wing_ridge_z():
    return max(wing_eave_z() + TAN * min(w[1] - w[0], w[3] - w[2]) / 2 for w in wing_rects())


def roof_z(x, y):
    zs = [z for z in (ring_z(x, y), wing_roof_z(x, y)) if z is not None]
    return max(zs) if zs else None


def roof_area():
    """Sloped area of the ring and the wing (each piece of plan counted once), by sampling a 0.5 ft grid (good to about 1%)."""
    step, total = 0.5, 0.0
    o = ROOF["ring"]
    y = o[2] + step / 2
    while y < o[3]:
        x = o[0] + step / 2
        while x < o[1]:
            if roof_z(x, y) is not None:
                total += step * step
            x += step
        y += step
    return total / math.cos(math.radians(ROOF["pitch"]))


def _roof_src(x, y):
    """Which roof is on top at (x, y): 'wing', 'ring' or None."""
    if wing_roof_z(x, y) is not None:
        return "wing"
    return "ring" if ring_z(x, y) is not None else None


def roof_lines(step=0.1):
    """The roof plan's visible ridges, hips and valleys as short pieces [(kind, (x1, y1), (x2, y2))], kind 'ridge', 'hip' or 'valley'.
    Candidate lines (the ridge mid-lines and the 45-degree lines from every eave corner) are kept where the top roof surface really
    folds across them: down on both sides (ridge or hip) or up on both sides (valley)."""
    o, i, rr = ROOF["ring"], ROOF["court_eave"], ring_ridge_rect()
    bb = (o[0], o[1], o[2], o[3])
    lines = set()   # whole lines across the roof's bounding box: ("x", c) y = c; ("y", c) x = c; ("+", c) y = x + c; ("-", c) y = -x + c
    lines |= {("x", rr[2]), ("x", rr[3]), ("y", rr[0]), ("y", rr[1])}
    for w in wing_rects():
        lines |= {("x", round((w[2] + w[3]) / 2, 4)), ("y", round((w[0] + w[1]) / 2, 4))}
    for r in [o, i] + wing_rects():
        for cx in (r[0], r[1]):
            for cy in (r[2], r[3]):
                lines |= {("+", round(cy - cx, 4)), ("-", round(cy + cx, 4))}
    cands = []
    for k, c in sorted(lines):
        if k == "x":
            cands.append((bb[0], c, bb[1], c))
        elif k == "y":
            cands.append((c, bb[2], c, bb[3]))
        else:
            sg = 1 if k == "+" else -1                      # y = sg * x + c, clipped to the box
            xs = sorted(((bb[2] - c) * sg, (bb[3] - c) * sg))
            lo, hi = max(bb[0], xs[0]), min(bb[1], xs[1])
            if hi - lo > 1e-6:
                cands.append((lo, sg * lo + c, hi, sg * hi + c))
    d, tol = 0.05, TAN * 0.05 * 0.5
    out = []
    for x1, y1, x2, y2 in cands:
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        nx, ny = -uy, ux
        diag = abs(ux) > 1e-6 and abs(uy) > 1e-6
        n = max(1, int(round(L / step)))
        for k in range(n):
            px, py = x1 + (x2 - x1) * (k + 0.5) / n, y1 + (y2 - y1) * (k + 0.5) / n
            src = _roof_src(px, py)
            if src is None or _roof_src(px + nx * d, py + ny * d) != src or _roof_src(px - nx * d, py - ny * d) != src:
                continue
            if _roof_src(px + ux * d, py + uy * d) != src or _roof_src(px - ux * d, py - uy * d) != src:
                continue
            f = wing_roof_z if src == "wing" else ring_z
            sec = f(px + nx * d, py + ny * d) + f(px - nx * d, py - ny * d) - 2 * f(px, py)
            if abs(f(px + ux * d, py + uy * d) + f(px - ux * d, py - uy * d) - 2 * f(px, py)) >= tol:
                continue                                    # a crossing, not a line
            kind = None if abs(sec) < tol else ("valley" if sec > 0 else ("hip" if diag else "ridge"))
            if kind:
                out.append((kind, (x1 + (x2 - x1) * k / n, y1 + (y2 - y1) * k / n), (x1 + (x2 - x1) * (k + 1) / n, y1 + (y2 - y1) * (k + 1) / n)))
    seen, uniq = set(), []
    for k_, a, b in out:
        key = (round(a[0], 2), round(a[1], 2), round(b[0], 2), round(b[1], 2))
        if key not in seen and (key[2], key[3], key[0], key[1]) not in seen:
            seen.add(key); uniq.append((k_, a, b))
    return uniq


def roof_line_lengths():
    """Total PLAN length (ft) of the visible ridges, hips and valleys. Ridges are level (true length = plan); for the true length of a hip or
    valley multiply its plan length by HIP_K."""
    tot = {"ridge": 0.0, "hip": 0.0, "valley": 0.0}
    for k, a, b in roof_lines():
        tot[k] += math.hypot(b[0] - a[0], b[1] - a[1])
    return tot


def terrace_slab_z():
    """Finished level of the roof terrace's slab."""
    return floor_level("R37")


def _raw_south(x):
    """The south edge wall the rules alone would need at x: the upstand, or the ring roof + 6 in where it stands higher."""
    y, x1, x2, rise = ROOF["verge_south"]
    z = ring_z(x, y - 0.001)
    return ROOF["upstand"] if z is None else max(ROOF["upstand"], z - terrace_slab_z() + rise)


def corner_guard_runs(step=0.01):
    """The terrace's south-east corner guard: (x from, x to) on the south edge and (y from, y to) on the east edge. It starts on the south edge
    where the raw rake first rises past the upstand and turns up the east edge to where the ring's north-east hip crosses it."""
    t, rr = ROOF["terrace"], ring_ridge_rect()
    x = t[0]
    while x < t[1] and _raw_south(x) <= ROOF["upstand"] + 1e-9:
        x += step
    return (round(x, 2), t[1]), (t[2], rr[3] + (t[1] - rr[1]))


def verge_east_h(y):
    """Height above the slab of the terrace's east edge wall at y: the level corner guard over its run, then a verge wall that follows the
    ring roof's profile, 6 in above it."""
    x, y1, y2, rise = ROOF["verge_east"]
    if y <= corner_guard_runs()[1][1] + 1e-9:
        return ROOF["corner_guard"]
    z = ring_z(x + 0.001, y)
    return None if z is None else z - terrace_slab_z() + rise


def verge_east_max(step=0.05):
    """Highest point of the east edge wall above the terrace slab (ft), and that less the 6 in rise."""
    x, y1, y2, rise = ROOF["verge_east"]
    n = int(round((y2 - y1) / step))
    h = max(verge_east_h(y1 + k * step) for k in range(n + 1))
    return h, h - rise


def verge_east_area():
    """Face area (sq ft) of the east verge wall, by sampling at 0.25 ft."""
    x, y1, y2, rise = ROOF["verge_east"]
    n = int(round((y2 - y1) / 0.25))
    return sum(verge_east_h(y1 + (k + 0.5) * 0.25) * 0.25 for k in range(n))


def verge_south_h(x):
    """Height above the slab of the terrace's south edge wall at x: the 1'-9" upstand (6 in over the walkway roof) and, at the south-east
    corner where the east band's roof rises to its ridge, the level corner guard."""
    if x >= corner_guard_runs()[0][0] - 1e-9:
        return ROOF["corner_guard"]
    return _raw_south(x)


def verge_south_max(step=0.05):
    t = ROOF["terrace"]
    n = int(round((t[1] - t[0]) / step))
    return max(verge_south_h(t[0] + k * step) for k in range(n + 1))


def verge_south_area():
    """Face area (sq ft) of the south edge wall above the slab (upstand plus raking verge), by sampling at 0.25 ft."""
    t = ROOF["terrace"]
    n = int(round((t[1] - t[0]) / 0.25))
    return sum(verge_south_h(t[0] + (k + 0.5) * 0.25) * 0.25 for k in range(n))


def thinnai_roof_z(x, y):
    """The thinnai's lean-to: the ring roof's east slope (same plane) carried on from the east wall to its own eave."""
    x1, x2, y1, y2 = ROOF["thinnai"]
    if not (x1 <= x <= x2 and y1 <= y <= y2):
        return None
    return eave_z() - TAN * (x - ROOF["ring"][1])


def thinnai_headroom():
    """Least clear height under the thinnai lean-to (below its build-up) at the pillar line, above the thinnai floor."""
    return min(thinnai_roof_z(px, py) - ROOF["thinnai_build_up"] - LEVELS["thinnai"] for px, py in THINNAI_PILLARS)


def thinnai_roof_area():
    """Sloped area of the lean-to past the ring's eave (inside it, it is the ring roof's own slope)."""
    x1, x2, y1, y2 = ROOF["thinnai"]
    return (x2 - max(x1, ROOF["ring"][1])) * (y2 - y1) / math.cos(math.radians(ROOF["pitch"]))


def jharokha_base_z(j):
    """Underside of a jharokha bay above finished ground: the seat level less the deck and bracket frame."""
    return LEVELS["FFL"] + LEVELS["upper_ffl"] + j[4] - JHAROKHA_DECK


def jharokha_clearance(j, step=0.1):
    """Least height of a jharokha bay's underside above the ring roof surface across its depth and width."""
    x1, x2, y1, y2, _ = j
    nx, ny = int(round((x2 - x1) / step)), int(round((y2 - y1) / step))
    return min(jharokha_base_z(j) - ring_z(x1 + i * (x2 - x1) / nx, y1 + k * (y2 - y1) / ny)
               for i in range(nx + 1) for k in range(ny + 1) if ring_z(x1 + i * (x2 - x1) / nx, y1 + k * (y2 - y1) / ny) is not None)


def lintel_step_windows():
    """Windows whose heads rise above the 7'-0" lintel band while their sills are below it: the band steps up over them (both floors)."""
    hd = LEVELS["door_head"]
    return [w[0] for fl in ("G", "F1") for w in _model._FLOOR_DATA[fl]["WINDOWS"] if w[5] < hd - EPS and w[6] > hd + EPS]


# ---- numbers quoted in the model's prose (FINISHES, SPEC, OPEN_ISSUES, decisions, phases) ----
# The prose in model.py writes {key} for a number the geometry knows ({ring_eave}, {terrace_slab}, ...) and {clear:R31} / {size:R31}
# for a room's clear or centre-line size (east-west x north-south); geom fills them in place when it is imported, so the text always
# quotes the drawn numbers.
_OPEN_GROUND = ("R50", "R51", "R61", "R62", "R63", "R17")   # the courtyard, the walkway and the thinnai: not enclosed floor
_WALKWAY = ("R51", "R61", "R62", "R63")
_UNDER_WELL = ("R06", "R48", "R46")   # the ground rooms under the upstairs stair well (flight 1, the cupboard under flight 2, the low store)


def floor_areas():
    """Plan areas (sq ft) to the outer walls' centre lines: enclosed ground floor, walkway, courtyard, thinnai, enclosed upper floor,
    roof terrace, and the enclosed total. The upper floor counts the stair well (open to the roof over both flights), as a gross floor
    area does."""
    def a(r):
        return (r[3] - r[2]) * (r[5] - r[4])
    g, f1 = [r for r in both("ROOMS") if r[0] not in F1_ROOM_IDS], [r for r in both("ROOMS") if r[0] in F1_ROOM_IDS]
    out = {"ground": sum(a(r) for r in g if r[0] not in _OPEN_GROUND),
           "walkway": sum(a(r) for r in g if r[0] in _WALKWAY),
           "court": sum(a(r) for r in g if r[0] == "R50"),
           "thinnai": sum(a(r) for r in g if r[0] == "R17"),
           "upper": sum(a(r) for r in f1 if r[0] != "R37") + sum(a(r) for r in g if r[0] in _UNDER_WELL),
           "terrace": sum(a(r) for r in f1 if r[0] == "R37")}
    out["enclosed"] = out["ground"] + out["upper"]
    return out


def _room_size(rid, clear):
    r = next(r for r in both("ROOMS") if r[0] == rid)
    with on_floor("F1" if rid in F1_ROOM_IDS else "G"):
        L, W = clear_dims(r) if clear else room_dims(r)
    return f"{fmt_ft(L)} x {fmt_ft(W)}"


def prose_numbers():
    """The named numbers the prose may quote, formatted as they are written."""
    ar, slab = floor_areas(), terrace_slab_z()
    (gx1, gx2), (gy1, gy2) = corner_guard_runs()
    with on_floor("G"):
        walk_clear = clear_dims(next(r for r in ROOMS if r[0] == "R62"))[0]
    sxs = sorted(x for x, y in ROOF["downpipes"] if y < HY1)            # downpipes on the south side
    thx2 = next(r[3] for r in both("ROOMS") if r[0] == "R17")
    return {
        "house": f"{HX2 - HX1:.0f} x {HY2 - HY1:.0f} ft", "court": f"{COURT:.0f} x {COURT:.0f} ft", "band": fmt_ft(BAND), "walk": fmt_ft(WALK),
        "walk_clear": fmt_ft(walk_clear), "plot": f"{max(p[1] for p in PLOT) - min(p[1] for p in PLOT):.0f} x {PLOT_X2 - PLOT_X1:.0f} ft",
        "pitch": f"{ROOF['pitch']} deg", "ring_eave": fmt_lvl(eave_z()), "ring_ridge": fmt_lvl(ridge_z()),
        "wing_eave": fmt_lvl(wing_eave_z()), "wing_ridge": fmt_lvl(wing_ridge_z()),
        "terrace_slab": fmt_lvl(slab), "family_floor": fmt_lvl(floor_level("R36")),
        "terrace_step": f"{round((floor_level('R36') - slab) * 12)} in", "canopy": fmt_lvl(slab + ROOF["canopy"]),
        "upstand": fmt_ft(ROOF["upstand"]), "corner_guard": fmt_ft(ROOF["corner_guard"]), "guard_s": fmt_ft(gx2 - gx1), "guard_e": fmt_ft(gy2 - gy1),
        "thinnai_eave": fmt_lvl(thinnai_roof_z(ROOF["thinnai"][1], CY)), "thinnai_clear": fmt_ft(thinnai_headroom()),
        "jharokha_under": fmt_lvl(jharokha_base_z(JHAROKHAS[0])), "downpipes": str(len(ROOF["downpipes"])),
        "spreaders": str(len(ROOF["wing_spreaders"])), "south_gutter": f"{ROOF['ring_south_gutter_mm']} mm",
        "south_dps": " and ".join(f"x {x:g}" for x in sxs), "ring_south_dp": " and ".join(f"x {x:g}" for x in sxs if x > ROOF["wing"][1]),
        "court_drop": f"{round((LEVELS['walkway'] - LEVELS['courtyard']) * 12)} in",
        "back_garden": f"{HX1 - PLOT_X1:.0f} ft",
        "side_strip": f"{min(HY1 - min(p[1] for p in PLOT), max(p[1] for p in PLOT) - HY2):.0f} ft",
        "front_land": f"{PLOT_X2 - HX2:.0f} ft from the house wall to the road ({PLOT_X2 - thx2:.0f} beyond the thinnai)",
        **{f"{k}_area": f"{v:,.0f}" for k, v in ar.items()},
    }


_PROSE_LISTS = ("FINISHES", "SPEC", "OPEN_ISSUES", "PHASES", "PHASE1_PROVISIONS", "PHASE1_LIVING", "HOLD_POINTS",
                "COURTYARD_DECISIONS", "DUPLEX_DECISIONS_CARRIED", "DECISIONS")
_PROSE_KEY = re.compile(r"\{(clear|size):(R\w+)\}|\{(\w+)\}")


def fill_prose(s, nums=None):
    """A string with its {key}, {clear:Rnn} and {size:Rnn} placeholders filled from the geometry (unknown keys raise)."""
    nums = nums or prose_numbers()
    return _PROSE_KEY.sub(lambda m: _room_size(m.group(2), m.group(1) == "clear") if m.group(1) else nums[m.group(3)], s)


def _fill_all_prose():
    import model as _m
    nums = prose_numbers()
    def f(x):
        if isinstance(x, str):
            return fill_prose(x, nums) if "{" in x else x
        if isinstance(x, tuple):
            return tuple(f(i) for i in x)
        if isinstance(x, list):
            return [f(i) for i in x]
        return x
    for name in _PROSE_LISTS:
        lst = getattr(_m, name)
        lst[:] = f(lst)
    _m.PROSE_FILLED = True


_fill_all_prose()
