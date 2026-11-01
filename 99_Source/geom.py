import math
from model import *

EPS = 1e-6
TAN = math.tan(math.radians(ROOF["pitch"]))


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


def floor_level(rid):
    return LEVELS["FFL"] + (LEVELS["upper_ffl"] if rid in F1_ROOM_IDS else 0) + ROOM_FLOOR.get(rid, 0)


def upper_wall_top_z():
    """Top of the first-floor walls (main roof ring beam) above finished ground."""
    return LEVELS["FFL"] + LEVELS["upper_ffl"] + LEVELS["upper_wall_top"]


# ---- roof: heights above finished ground (FGL = 0) ----
def eave_z():
    """Main (hipped) roof eaves, over the two-storey block."""
    return upper_wall_top_z() - ROOF["overhang"] * TAN


def gable_eave_z():
    """Front gable eaves, over the single-storey front."""
    return LEVELS["FFL"] + LEVELS["wall_top"] - ROOF["overhang"] * TAN + ROOF["gable_lift"]


def hip_z(x, y):
    x1, x2, y1, y2 = ROOF["hip"]
    d = min(x - x1, x2 - x, y - y1, y2 - y)
    return eave_z() + d * TAN if d >= 0 else None


def gable_z(x, y):
    gx1, gx2, ya, yb = ROOF["gable"]
    if not (gx1 <= x <= gx2 and ya <= y <= yb):
        return None
    return gable_eave_z() + min(y - ya, yb - y) * TAN


def roof_z(x, y):
    zs = [z for z in (hip_z(x, y), gable_z(x, y)) if z is not None]
    return max(zs) if zs else None


def ridge_z():
    x1, x2, y1, y2 = ROOF["hip"]
    return eave_z() + (y2 - y1) / 2 * TAN


def gable_ridge_z():
    gx1, gx2, ya, yb = ROOF["gable"]
    return gable_eave_z() + (yb - ya) / 2 * TAN


def roof_area():
    """Sloped roof area (sq ft): plan area of the main hip and the front gable (beyond the hip) divided by cos(pitch)."""
    x1, x2, y1, y2 = ROOF["hip"]
    gx1, gx2, ya, yb = ROOF["gable"]
    return ((x2 - x1) * (y2 - y1) + (gx2 - max(gx1, x2)) * (yb - ya)) / math.cos(math.radians(ROOF["pitch"]))


# ---- dining ventilator ----
def vent_sill_z():
    return ridge_z() + ROOF["vent_sill"]


def vent_top_z():
    """Top of the louvre band = eaves of the hipped cap."""
    return vent_sill_z() + ROOF["vent_louvre"]


def vent_apex_z():
    x1, x2, y1, y2 = ROOF["skylight"]
    return vent_top_z() + ((min(x2 - x1, y2 - y1)) / 2 + ROOF["vent_overhang"]) * TAN
