import json
import math
import re
from geom import *
from geom import _roof_src

# Short labels where the full room name will not fit in the 3D view
LABELS = {"Stair and passage": "Stair", "Master bedroom": "Master", "Covered terrace": "Covered terrace"}
ENGAWA_Z = 1.5  # the engawa deck (SITE_FEATURES "OTTA"): a teak deck 1'-6" above the garden
FULL_HEIGHT_SILL = 1.0  # windows with a lower sill are cut through the wall
GUTTER_OUT = 0.2        # half-round eave gutters hang this far outside the eave line (as the elevations draw them)
TANK_R = 4 / 3          # the two terrace tanks are 2 ft 8 in across (PLUMBING_F1 "TK"), on a 3 ft steel stand
TANK_STAND = 3.0
TANK_H = round(0.5 / (math.pi * (TANK_R * 0.3048) ** 2) / 0.3048 + 0.25, 2)   # 500 L in a 2'-8" drum, plus its domed lid
EF_HALF = 0.35          # half width of the powder room's duct cowl over D18 (as on the south elevation)


def _minus(r, hole):
    """Rectangle r less a rectangular hole inside it, as up to four pieces."""
    x1, x2, y1, y2 = r
    if not hole or hole[0] >= x2 or hole[1] <= x1 or hole[2] >= y2 or hole[3] <= y1:
        return [r]
    hx1, hx2, hy1, hy2 = max(hole[0], x1), min(hole[1], x2), max(hole[2], y1), min(hole[3], y2)
    parts = [(x1, x2, y1, hy1), (x1, x2, hy2, y2), (x1, hx1, hy1, hy2), (hx2, x2, hy1, hy2)]
    return [p for p in parts if p[1] - p[0] > 0.01 and p[3] - p[2] > 0.01]


def floor_data():
    """Walls, openings, rooms, fittings and furniture of the floor currently swapped in."""
    xs = [c for a, c in EXTERIOR if a == "Y"]
    ys = [c for a, c in EXTERIOR if a == "X"]
    rooms = []
    for rid, name, x1, x2, y1, y2, _ in ROOMS:
        label = LABELS.get(name, re.sub(r"\s*\(.*\)", "", name))
        rooms.append([label, *ROOM_LABEL_AT.get(rid, ((x1 + x2) / 2, (y1 + y2) / 2))])
    doors = [{"id": d[0], "axis": d[1], "c": d[2], "s": d[3], "e": d[4], "sliding": d[5] == 0, "swing": d[5], "hingeEnd": d[0] in HINGE_AT_END,
              "kind": "folding" if "folding" in d[7].lower() else "bath" if "waterproof" in d[7].lower() else "carved" if "carved" in d[7].lower() else "glazed" if "glaz" in d[7].lower() else "teak",
              "exterior": (d[1], d[2]) in EXTERIOR and d[0] == "D01", "transom": TRANSOMS.get(d[0]),
              "h": DOOR_HEIGHTS.get(d[0], LEVELS["door_head"])} for d in DOORS]
    windows = []
    for w in WINDOWS:
        axis, c = w[1], w[2]
        lo = min(ys) if axis == "X" else min(xs)
        ext = (axis, c) in EXTERIOR
        windows.append({"id": w[0], "axis": axis, "c": c, "s": w[3], "e": w[4], "sill": w[5], "head": w[6],
                        "dir": -1 if c == lo else 1, "cut": w[5] < FULL_HEIGHT_SILL,
                        "bay": any(axis == "Y" and abs(c - j[0]) < 1e-6 and abs(w[3] - j[2]) < 1e-6 and abs(w[4] - j[3]) < 1e-6 for j in JHAROKHAS),  # opening into a jharokha bay: the bay carries the jali and glass
                        "shade": ext and FLOOR[0] != "G" and (axis, c) == ("Y", HX1) and "clerestory" not in w[8].lower() and w[5] < 6,  # the ring's 2 ft eave covers the ground floor; upstairs only the west windows get a hood under the wing eave
                        "mat": "win" if (axis == "X" and c == max(ys)) or "glazed clerestory" in w[8].lower() or "fixed teak-framed glazing" in w[8].lower() or ("glazed" in w[8].lower() and "jali" not in w[8].lower() and not ext) else "jali"})
    floor_keys = (("Red oxide", "redoxide"), ("Matt vitrified 2x2", "vitrified"), ("Marble", "marble"), ("Anti-skid matt", "antiskid"),
                  ("Anti-skid ceramic", "ceramic"), ("Cuddapah", "cuddapah"), ("Flamed granite", "granite"), ("Terracotta", "terracotta"),
                  ("Athangudi", "athangudi"), ("Rough-dressed granite", "granite"))
    room_rects = []
    lw = LIGHT_WELL if floor_base() > LEVELS["FFL"] + 1 else None  # upstairs: the floor stops at the light well
    for rid, name, x1, x2, y1, y2, _ in ROOMS:
        fin = FLOOR_FINISH.get(rid, "Red oxide")
        key = next((k for t, k in floor_keys if t in fin), "redoxide")
        ceil = CEILINGS.get(rid)
        if ceil and ceil[0] == "open":  # open to the sky: no ceiling
            ceil = None
        for a, b, c, d in _minus((x1, x2, y1, y2), lw):
            room_rects.append({"id": rid, "x1": a, "x2": b, "y1": c, "y2": d, "floor": key, "fo": ROOM_FLOOR.get(rid, 0),
                               "ceil": ceil[1] if ceil and ceil[0] == "flat" else None})
    fixtures = [[p[0], p[1], p[2]] for p in PLUMBING if p[3] != "SITE"]
    elec = [[e[0], e[1], e[2], e[3]] for e in ELECTRICAL if e[0] in ("F", "L", "WL") and e[3] != "SITE"]
    furniture = [{"id": f[0], "x1": f[3], "x2": f[4], "y1": f[5], "y2": f[6]} for f in FURNITURE]
    furniture += [{"id": e[0], "x1": e[1], "x2": e[2], "y1": e[3], "y2": e[4]} for e in EXTRA_DRAW]
    return {"walls": [list(w) + [wall_t(w)] for w in WALLS], "doors": doors, "windows": windows, "furniture": furniture, "rooms": rooms,
            "roomRects": room_rects, "exterior": [[a, c] for a, c in sorted(EXTERIOR)], "fixtures": fixtures, "elec": elec,
            "rails": [list(r) + ([1] if (r[0], r[1]) in JALI_RAILS else []) for r in RAILS], "z": floor_base() }


def _runs(a, b, keep, step=0.05):
    """Pieces of the segment a-b (plan points) where keep(point) holds, sampled every `step` ft."""
    n = max(1, int(round(math.hypot(b[0] - a[0], b[1] - a[1]) / step)))
    pts = [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(n + 1)]
    out, st = [], None
    for k in range(n):
        m = ((pts[k][0] + pts[k + 1][0]) / 2, (pts[k][1] + pts[k + 1][1]) / 2)
        if keep(m):
            st = k if st is None else st
        elif st is not None:
            out.append((pts[st], pts[k])); st = None
    if st is not None:
        out.append((pts[st], pts[n]))
    return [[round(p[0], 3), round(p[1], 3), round(q[0], 3), round(q[1], 3)] for p, q in out]


def _rect_edges(r):
    """A rect's four edges, counter-clockwise, each with its outward normal."""
    x1, x2, y1, y2 = r
    return [((x1, y1), (x2, y1), (0, -1)), ((x2, y1), (x2, y2), (1, 0)), ((x2, y2), (x1, y2), (0, 1)), ((x1, y2), (x1, y1), (-1, 0))]


def ring_eave_runs():
    """The ring roof's fascia lines: its outer eave where the roof exists (not at the wing and terrace holes, nor where the thinnai lean-to
    carries the east slope on), and the whole inner eave round the court. [x1, y1, x2, y2, "out" | "in"]."""
    o, i, th = ROOF["ring"], ROOF["court_eave"], ROOF["thinnai"]
    out = []
    for a, b, (nx, ny) in _rect_edges(o):
        keep = lambda p, nx=nx, ny=ny: ring_z(p[0] - nx * 0.01, p[1] - ny * 0.01) is not None and not (nx == 1 and th[2] < p[1] < th[3])
        out += [r + ["out"] for r in _runs(a, b, keep)]
    out += [[a[0], a[1], b[0], b[1], "in"] for a, b, _ in _rect_edges(i)]
    return out


def wing_eave_runs():
    """The wing's L-shaped eave outline: the edges of its two hipped rects that lie outside the other, joined. [x1, y1, x2, y2]."""
    rs, lines = wing_rects(), {}
    for r in rs:
        for a, b, (nx, ny) in _rect_edges(r):
            keep = lambda p, nx=nx, ny=ny: not any(q[0] < p[0] + nx * 0.01 < q[1] and q[2] < p[1] + ny * 0.01 < q[3] for q in rs)
            for x1, y1, x2, y2 in _runs(a, b, keep):
                k = ("y", y1) if abs(y2 - y1) < 1e-9 else ("x", x1)
                lo, hi = sorted((x1, x2) if k[0] == "y" else (y1, y2))
                lines.setdefault(k, []).append([lo, hi])
    out = []
    for (ax, c), iv in sorted(lines.items()):
        iv.sort()
        m = [iv[0]]
        for lo, hi in iv[1:]:
            if lo <= m[-1][1] + 1e-6:
                m[-1][1] = max(m[-1][1], hi)
            else:
                m.append([lo, hi])
        out += [[lo, c, hi, c] if ax == "y" else [c, lo, c, hi] for lo, hi in m]
    return out


def merged_roof_lines():
    """geom.roof_lines() joined into long straight pieces: [kind, roof, x1, y1, x2, y2], each a single straight 3D line (a piece stops
    where the line's rise per foot changes, so the page draws it as one beam between its end heights)."""
    out, run = [], None
    for kind, a, b in roof_lines():          # pieces come in order along each candidate line, end to end
        src = _roof_src((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        f = wing_roof_z if src == "wing" else ring_z
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        d = ((b[0] - a[0]) / L, (b[1] - a[1]) / L, (f(*b) - f(*a)) / L)
        if run and run[0] == kind and run[1] == src and math.hypot(a[0] - run[3][0], a[1] - run[3][1]) < 1e-6 \
                and all(abs(p - q) < 1e-3 for p, q in zip(d, run[4])):
            run[3] = b
        else:
            if run:
                out.append(run)
            run = [kind, src, a, b, d]
    if run:
        out.append(run)
    return [[k, s_, round(a[0], 3), round(a[1], 3), round(b[0], 3), round(b[1], 3)] for k, s_, a, b, _ in out]


def downpipe_data():
    """Each downpipe with the gutter it drains: the nearest eave of the roof it serves (the ring's or the wing's), or the terrace outlet."""
    ol, drop = ROOF["terrace_outlet"], ROOF["gutter_depth"]
    eaves = [(r[:4], "ring", eave_z()) for r in ring_eave_runs() if r[4] == "out"] + [(r, "wing", wing_eave_z()) for r in wing_eave_runs()]
    out = []
    for x, y in ROOF["downpipes"]:
        if abs(x - ol[0]) < 1e-6 and y > HY2:
            out.append({"x": x, "y": y, "roof": "terrace", "gx": ol[0], "gy": ol[1], "gz": round(terrace_slab_z(), 4)})
            continue
        best = None
        for (x1, y1, x2, y2), roof, ez in eaves:
            L2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
            t = max(0.0, min(1.0, ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / L2))
            px, py = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
            d = math.hypot(x - px, y - py)
            if best is None or d < best[0] - 1e-9:
                # the gutter hangs on the eave's outward side: away from the roof it serves (flip where the trial side is on that roof,
                # as the page's inW does for the wing)
                nx, ny = (0, 1) if abs(y2 - y1) < 1e-9 else (1, 0)
                on_roof = (lambda u, v: wing_roof_z(u, v) is not None) if roof == "wing" else (lambda u, v: ring_z(u, v) is not None)
                if on_roof(px + nx * 0.05, py + ny * 0.05):
                    nx, ny = -nx, -ny
                best = (d, {"x": x, "y": y, "roof": roof, "gx": round(px + nx * GUTTER_OUT, 3), "gy": round(py + ny * GUTTER_OUT, 3), "gz": round(ez - drop, 4)})
        out.append(best[1])
    return out


def terrace_profiles(step=0.25):
    """Heights above the terrace slab of its south and east edge walls (geom.verge_south_h / verge_east_h), sampled for the page."""
    t = ROOF["terrace"]
    n = int(round((t[1] - t[0]) / step))
    south = [[round(t[0] + k * (t[1] - t[0]) / n, 3), round(verge_south_h(t[0] + k * (t[1] - t[0]) / n), 4)] for k in range(n + 1)]
    m = int(round((t[3] - t[2]) / step))
    east = [[round(t[2] + k * (t[3] - t[2]) / m, 3), round(verge_east_h(t[2] + k * (t[3] - t[2]) / m), 4)] for k in range(m + 1)]
    (gx1, gx2), (gy1, gy2) = corner_guard_runs()
    for x in (gx1,):   # the level guard starts exactly here: add the step's two heights
        south.append([x - 1e-3, round(verge_south_h(x - 1e-3), 4)]); south.append([x, round(verge_south_h(x), 4)])
    for y in (gy2,):
        east.append([y, round(verge_east_h(y), 4)]); east.append([y + 1e-3, round(verge_east_h(y + 1e-3), 4)])
    return sorted(south), sorted(east)


def model_data():
    with on_floor("G"):
        g = floor_data()
    with on_floor("F1"):
        f1 = floor_data()
    feat = {f[0]: f[3] for f in SITE_FEATURES}
    r = lambda v: round(v, 4)
    return {**g, "f1": f1, "jali": [list(j) for j in JALI_SCREENS],
            "F": LEVELS["FFL"], "engawaZ": ENGAWA_Z, "H": LEVELS["wall_top"], "H1": LEVELS["upper_wall_top"], "riser": LEVELS["riser"],
            "slabT": LEVELS["slab"], "slab": [list(s) for s in SLAB_F1], "stair": STAIR, "posts": [list(p) for p in TERRACE_POSTS],
            "house": {"x1": HX1, "x2": HX2, "y1": HY1, "y2": HY2, "block": [HX1, RING[0]]},
            # the courtyard and the ring round it: open court (sunk), walkway (one step up), thinnai (outside the east wall)
            "court": list(CT), "ring": list(RING), "courtEave": list(ROOF["court_eave"]),
            "courtZ": LEVELS["courtyard"], "walkZ": LEVELS["walkway"], "thinnaiZ": LEVELS["thinnai"],
            "thinnai": list(room_of("R17")[2:6]),
            "pillars": {"walk": [list(p) for p in WALKWAY_PILLARS], "thinnai": [list(p) for p in THINNAI_PILLARS]},
            "jharokhas": [{"x1": j[0], "x2": j[1], "y1": j[2], "y2": j[3], "sill": j[4], "deck": JHAROKHA_DECK, "face": JHAROKHA_FACE[k],
                           "base": r(jharokha_base_z(j)), "kerb": ROOF["jharokha_kerb"], "head": ROOF["jharokha_head"],
                           "toSoffit": ROOF["jharokha_to_soffit"]} for k, j in enumerate(JHAROKHAS)],
            "saddles": [list(sd) for sd in ROOF["saddles"]],
            # roofs: heights above finished ground; the page's ringZ / wingZ / thinnaiRoofZ are ports of geom.ring_z / wing_roof_z /
            # thinnai_roof_z and read every number from here (tests/test_3d.py checks the ports against geom)
            "roofRing": {"eave": list(ROOF["ring"]), "courtEave": list(ROOF["court_eave"]), "ring": list(RING), "pitch": ROOF["pitch"],
                         "tan": TAN, "eaveZ": eave_z(), "ridgeZ": r(ridge_z()), "grilleZ": r(ROOF["grille_z"]),
                         "holes": [list(h) for h in ring_holes()], "eaveRuns": ring_eave_runs(),
                         "thinnai": list(ROOF["thinnai"]), "thinnaiBuildUp": ROOF["thinnai_build_up"],
                         "gutterDrop": ROOF["gutter_depth"], "gutterOut": GUTTER_OUT, "downpipes": downpipe_data()},
            "roofWing": {"rects": [list(w) for w in wing_rects()], "walls": [list(w) for w in ROOF["wing_walls"]],
                         "eaveZ": wing_eave_z(), "ridgeZ": r(wing_ridge_z()), "eaveRuns": wing_eave_runs(),
                         "spreaders": [list(p) for p in ROOF["wing_spreaders"]], "boxGutter": list(ROOF["wing_box_gutter"][:2])},
            "roofLines": merged_roof_lines(),
            "terrace": {"rect": list(ROOF["terrace"]), "slabZ": r(terrace_slab_z()), "canopyZ": r(terrace_slab_z() + ROOF["canopy"]),
                        # the canopy deck as the elevations draw it: from the family room wall's face to 6 in past the east and north edges
                        "canopy": [ROOF["terrace"][0] + T / 2, ROOF["terrace"][1] + 0.5, ROOF["terrace"][2] - 0.5, ROOF["terrace"][3] + 0.5],
                        "upstand": ROOF["upstand"], "cornerGuard": ROOF["corner_guard"], "guardRuns": [list(g) for g in corner_guard_runs()],
                        "south": terrace_profiles()[0], "east": terrace_profiles()[1], "outlet": list(ROOF["terrace_outlet"]),
                        "chajja": list(ROOF["terrace_chajja"]),
                        "tanks": [[p[1], p[2], TANK_R] for p in PLUMBING_F1 if p[0] == "TK"], "tankStand": TANK_STAND, "tankH": TANK_H},
            "efCowl": {"x": EF_OVER_DOOR["x"], "y": HY1, "z": r(LEVELS["wet_area"] + EF_OVER_DOOR["z"]), "h": EF_OVER_DOOR["cowl"], "hw": EF_HALF},
            "centre": [CX, CY],
            # walk in from the forecourt on the main-door axis: 4 ft inside the forecourt's east edge, facing west to the steps and the door
            "start": [feat["PATH"][1] - 4.0, next((d[3] + d[4]) / 2 for d in DOORS if d[0] == "D01")],
            "ramp": list(feat["RAMP"]),
            "wstep": {"landing": list(SERVICE_STEPS["landing"]), "xEnd": SERVICE_STEPS["x_end"], "risers": SERVICE_STEPS["risers"],
                      "tread": SERVICE_STEPS["tread"], "railZ": SERVICE_STEPS["rail_z"], "door": SERVICE_STEPS["door"]},
            "site": {"w": SITE["w"], "strip": SITE["strip"], "trial": SITE["trial"], "plot": [list(p) for p in PLOT], "x1": PLOT_X1, "x2": PLOT_X2, "shopWall": [list(p) for p in SHOP_WALL], "drive": {"x1": DRIVE["x1"], "x2": DRIVE["x2"], "off": list(DRIVE["off"])}}, "beds": [list(b) for b in GARDEN_BEDS], "gate": list(feat["GATE"][2:]),
            "pergola": list(feat["PERGOLA"]),
            "gate2": list(feat["GATE2"][2:]) if "GATE2" in feat else None,
            "features": {"SEPTIC": list(feat["SEPTIC"]), "SUMP": list(feat["SUMP"]), "TULSI": list(feat["TULSI"][:2]), "STEPS": list(feat["STEPS"]), "WSTEP": list(feat["WSTEP"]),
                         "SOAK": list(feat["SOAK"]), **{k: list(feat[k]) for k in ("PATH", "PATH2", "HEDGE1", "OTTA", "GSTEP", "CARPORT", "WORKSHOP", "WVERANDAH", "COMPOST", "RECHARGE", "BORE", "SHOP1", "SHOP2", "SITEWC", "HERBS", "SPIRAL", "BANANA", "GUILD", "WORM", "FENCE", "RAINTANK", "VEG", "PARIJAT", "JASMINE", "FEET") if k in feat}},
            "trees": [list(t) for t in TREES], "food": [list(t) for t in FOOD_TREES],
            "planters": [[w[3], w[4], w[2], 1 if w[2] >= 25 else -1, d, w[5], w[6], fl] for fl, ws in (("G", WINDOWS), ("F1", WINDOWS_F1)) for w in ws for k, d in PLANTER_GRILLES.items() if w[0] == k]}


def make(path):
    html = open(path, encoding="utf-8").read()
    data = json.dumps(model_data(), separators=(",", ":"))
    new, n = re.subn(r"/\*@MODEL\*/.*?/\*@END\*/", lambda _: f"/*@MODEL*/const MODEL={data};/*@END*/", html, flags=re.S)
    if n != 1:
        raise SystemExit(f"{path}: expected one /*@MODEL*/ block, found {n}")
    open(path, "w", encoding="utf-8").write(new)


if __name__ == "__main__":
    from paths import HTML_3D
    make(str(HTML_3D))
