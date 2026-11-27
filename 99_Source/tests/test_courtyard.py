import model as M


def test_plot_is_50_by_130_road_east():
    xs = [p[0] for p in M.PLOT]; ys = [p[1] for p in M.PLOT]
    assert (min(xs), max(xs), min(ys), max(ys)) == (0, 130, 0, 50)


def test_grid_adds_up():
    assert (M.HX1, M.HX2, M.HY1, M.HY2) == (15.0, 57.0, 4.0, 46.0)
    assert M.HX2 - M.HX1 == 42 and M.HY2 - M.HY1 == 42
    assert (M.BAND, M.WALK, M.COURT) == (12.5, 3.5, 10.0)
    assert M.BAND + M.WALK + M.COURT + M.WALK + M.BAND == 42
    assert (M.CX, M.CY) == (36.0, 25.0)
    assert M.CT == (31.0, 41.0, 20.0, 30.0) and M.RING == (27.5, 44.5, 16.5, 33.5)
    assert M.PLOT_X1 == 0 and M.PLOT_X2 == 130 and M.plot_north(10) == 50


def test_site_features_inside_plot():
    for fid, _, kind, g in M.SITE_FEATURES:
        if kind == "rect":
            assert 0 <= g[0] < g[1] <= 130 and 0 <= g[2] < g[3] <= 50, fid
        elif kind == "circle":
            assert 0 <= g[0] - g[2] and g[0] + g[2] <= 130 and 0 <= g[1] - g[2] and g[1] + g[2] <= 50, fid


def test_services_spacing():
    f = {s[0]: s[3] for s in M.SITE_FEATURES}
    sx, sy = f["SOAK"][0], f["SOAK"][1]
    bx, by = f["BORE"][0], f["BORE"][1]
    assert ((sx - bx) ** 2 + (sy - by) ** 2) ** 0.5 >= 60          # soak pit 60 ft+ from the borewell
    assert f["SOAK"][0] - M.HX2 >= 20                              # soak pit about 20 ft+ from the house
    assert f["SUMP"][0] > 65 and f["SUMP"][2] > 25                 # sump in the north-east quadrant
    assert 50 - f["SUMP"][3] >= 2 and f["SUMP"][1] <= M.DRIVE["x1"] - 2   # sump 2 ft+ from the boundary and from the drive
    zx, zy = f["BORE"][:2]
    assert ((f["SEPTIC"][0] + f["SEPTIC"][1]) / 2 - zx) ** 2 + ((f["SEPTIC"][2] + f["SEPTIC"][3]) / 2 - zy) ** 2 >= 50 ** 2   # septic 50 ft+ from the borewell
    assert zy - 0.5 - M.DRIVE["off"][1] >= 3 and 50 - zy >= 1.5     # borewell 3 ft+ off the drive edge
    sx1, sx2, sy1, sy2 = f["SEPTIC"]
    assert not ((sx1 + sx2) / 2 > 65 and (sy1 + sy2) / 2 > 25)     # septic not in the plot's north-east quadrant
    assert sy2 <= 25 and sx1 > M.HX2 + 20                          # on the south side of the forecourt, 20 ft+ from the house
    for fid in ("SOAK", "SEPTIC"):                                 # tank and pit clear of the reserved ramp
        g = f[fid]; b = (g[0] - g[2], g[0] + g[2], g[1] - g[2], g[1] + g[2]) if len(g) == 3 else g
        assert b[0] >= f["RAMP"][1] or b[3] <= f["RAMP"][2] or b[2] >= f["RAMP"][3], fid


def test_ramp_reserve_one_in_twelve_four_ft_wide_to_the_thinnai():
    r = {s[0]: s[3] for s in M.SITE_FEATURES}["RAMP"]
    assert r[3] - r[2] == 4.0                                      # 4 ft wide
    assert r[1] - r[0] >= 22.0                                     # 18 ft of 1:12 (1'-6" rise) plus a 4 ft landing
    assert r[0] < M.HX2 + 5.0 and r[1] > M.HX2 + 5.0               # lands at the thinnai (x 57-62), runs out into the forecourt
    assert r[2] >= 20.0 and r[3] <= 24.0                           # the thinnai's south edge is y 24


def _gap_to_house(x, y, r):
    dx = max(M.HX1 - x, 0, x - M.HX2); dy = max(M.HY1 - y, 0, y - M.HY2)
    return (dx ** 2 + dy ** 2) ** 0.5 - r


def test_trees_clear_of_house_and_septic():
    sx1, sx2, sy1, sy2 = {s[0]: s[3] for s in M.SITE_FEATURES}["SEPTIC"]
    close = []
    for t in list(M.TREES) + list(M.FOOD_TREES):
        x, y, r = t[:3]
        g = _gap_to_house(x, y, r)
        if g < 25:
            close.append((t, g))
        dx = max(sx1 - x, 0, x - sx2); dy = max(sy1 - y, 0, y - sy2)
        assert (dx ** 2 + dy ** 2) ** 0.5 - r >= 9, t
    # only the one forecourt neem (canopy radius 3.2, east of the thinnai) may be nearer, and then 15 ft+
    assert len(close) <= 1, close
    for t, g in close:
        assert t[2] == 3.2 and t[0] > 62 and g >= 15, (t, g)


# pairs meant to touch or nest
_NEST = {frozenset(p) for p in [
    ("CARPORT", "PATH2"), ("SHOPS", "SHOP1"), ("SHOPS", "SHOP2"), ("WORKSHOP", "WVERANDAH"), ("HERBS", "SPIRAL"),
    ("OTTA", "PERGOLA"), ("OTTA", "GSTEP"), ("PATH", "STEPS"), ("PATH", "TULSI"), ("PATH", "FEET"), ("PATH", "PARIJAT"),
    ("PATH2", "HEDGE1"), ("DRIVE", "CARPORT"), ("DRIVE", "GATE"), ("SHOPS", "GATE"),
]}
_NEST_ONE = {"APRON", "SPARE"}        # the apron hugs the house; the back garden holds its engawa and pergola


def _box(kind, g):
    if kind == "rect":
        return g
    if kind == "circle":
        return (g[0] - g[2], g[0] + g[2], g[1] - g[2], g[1] + g[2])
    return None


def test_site_features_do_not_overlap():
    items = []
    for fid, _, kind, g in M.SITE_FEATURES:
        b = _box(kind, g)
        if b: items.append((fid, b))
    bad = []
    for i, (a, ba) in enumerate(items):
        for c, bc in items[i + 1:]:
            if frozenset((a, c)) in _NEST or a in _NEST_ONE or c in _NEST_ONE:
                continue
            w = min(ba[1], bc[1]) - max(ba[0], bc[0]); h = min(ba[3], bc[3]) - max(ba[2], bc[2])
            if w > 0 and h > 0 and w * h > 0.5:
                bad.append((a, c, round(w * h, 2)))
    assert not bad, bad


from planlib import inside, overlap

ROOM = lambda rid: next(r for r in M._FLOOR_DATA["G"]["ROOMS"] if r[0] == rid)


def CLEAR(rid):
    import geom
    with M.on_floor("G"):
        return geom.clear_dims(ROOM(rid))


def _q(rid):
    r = ROOM(rid)
    return ("N" if (r[4] + r[5]) / 2 > M.CY else "S") + ("E" if (r[2] + r[3]) / 2 > M.CX else "W")


def test_courtyard_on_the_brahmasthan():
    r = ROOM("R50")
    assert (r[2], r[3], r[4], r[5]) == M.CT
    assert ((r[2] + r[3]) / 2, (r[4] + r[5]) / 2) == (M.CX, M.CY)


def test_vastu_zones():
    assert _q("R11") == "NE" and _q("R15") == "SE" and _q("R01") == "SW" and _q("R42") == "NW"
    assert ROOM("R06")[3] <= M.RING[0] + 0.01                        # stair in the west band
    for rid in ("R07", "R08", "R40"):                               # no toilet in the north-east
        assert _q(rid) != "NE", rid
    k = ROOM("R15")
    assert k[3] == M.HX2 and k[4] == M.HY1                          # kitchen in the south-east corner
    m = ROOM("R01")
    assert m[2] == M.HX1 and m[4] == M.HY1                          # master in the south-west corner
    f = ROOM("R18")                                                 # foyer on the east wall, room for the main door in its north half
    assert f[3] == M.HX2 and f[4] >= M.CY - 0.01 and f[4] <= 27 and f[5] >= 31


def test_minimum_clear_sizes():
    need = {"R01": (11.5, 11.5), "R42": (11, 10), "R15": (11, 9), "R40": (6, 6.3), "R07": (6, 6.3), "R08": (4.5, 6), "R18": (5.5, 8), "R16D": (11, 9)}
    for rid, (a, b) in need.items():
        w, d = sorted(CLEAR(rid), reverse=True)
        assert w >= max(a, b) - 0.01 and d >= min(a, b) - 0.01, (rid, CLEAR(rid))


def test_family_room_is_one_open_l_of_300_sq_ft():
    parts = M.FAMILY_ROOM
    assert parts[0] == "R16"
    area = sum(CLEAR(r)[0] * CLEAR(r)[1] for r in parts)
    assert area >= 300, area
    with M.on_floor("G"):
        rooms = [(r[0], r[2], r[3], r[4], r[5]) for r in M.ROOMS]
        g = graph(rooms, M.WALLS, [])                                 # open edges only (no doors)
    assert reachable_from(g, "R16", parts) >= set(parts)
    assert "R16S" in g["R18"]                                         # the foyer opens into the family room
    d = ROOM("R16D")
    assert d[2] == M.RING[1] and d[3] == M.HX2 and d[4] == ROOM("R15")[5]   # the dining end beside the kitchen
    with M.on_floor("G"):                                             # the foyer opens through a 4 ft gap on the main-door axis only
        f = ROOM("R18")
        screen = [w for w in M.WALLS if w[0] == "Y" and w[1] == f[2] and w[2] < f[5] and w[3] > f[4]]
        gaps = [(a[3], b[2]) for a, b in zip(sorted(screen, key=lambda w: w[2]), sorted(screen, key=lambda w: w[2])[1:])]
        assert len(screen) == 2 and gaps == [(27.0, 31.0)], screen
    assert M.ROOM_FLOOR["R18"] == M.LEVELS["thinnai"] - M.LEVELS["FFL"]    # no lip at the main door
    assert ROOM("R16")[5] == M.HY2 and ROOM("R16")[4] == M.RING[3]          # the living in the north band


def reachable_from(g, start, allowed):
    seen, todo = {start}, [start]
    while todo:
        for n in g[todo.pop()]:
            if n in allowed and n not in seen:
                seen.add(n); todo.append(n)
    return seen


def test_pooja_in_the_ne_corner():
    r = ROOM("R11")
    assert r[3] == M.HX2 and r[5] == M.HY2 and r[3] - r[2] >= 6 and r[5] - r[4] >= 6


def test_pillars_ring_the_courtyard():
    r = M.PILLAR_R
    inset = (M.CT[0] + r, M.CT[1] - r, M.CT[2] + r, M.CT[3] - r)
    assert len(M.WALKWAY_PILLARS) == 8 and len(set(M.WALKWAY_PILLARS)) == 8
    assert all(p[0] in (inset[0], M.CX, inset[1]) and p[1] in (inset[2], M.CY, inset[3]) for p in M.WALKWAY_PILLARS)
    for px, py in M.WALKWAY_PILLARS:                                # inside the court: the walkway keeps its full clear width
        assert M.CT[0] <= px - r and px + r <= M.CT[1] and M.CT[2] <= py - r and py + r <= M.CT[3]


def test_thinnai_pillars_clear_of_the_ramp_and_the_steps_and_under_the_eave():
    t = ROOM("R17")
    steps = next(f[3] for f in M.SITE_FEATURES if f[0] == "STEPS")
    ramp = next(f[3] for f in M.SITE_FEATURES if f[0] == "RAMP")
    eave = M.ROOF["thinnai"]
    assert len(M.THINNAI_PILLARS) == 2
    ys = sorted(py for _, py in M.THINNAI_PILLARS)
    assert abs((ys[0] + ys[1]) / 2 - (steps[2] + steps[3]) / 2) < 0.01  # symmetric about the steps (the door axis)
    for px, py in M.THINNAI_PILLARS:
        assert t[2] + 2 <= px <= t[3] - 0.5 and t[4] + 1.5 <= py <= t[5] - 1.5, (px, py)       # on the platform, 6 in+ from its front edge
        assert not (steps[2] - 0.5 < py < steps[3] + 0.5), (px, py)                          # the steps' width stays clear
        assert py - M.PILLAR_R - ramp[3] >= 1.5, (px, py)                                    # clear of the ramp's opening on y 24
        assert eave[1] - px >= 1.0 and eave[2] < py < eave[3]                                # the eave runs 1 ft+ past the pillars
    assert eave[1] >= t[3] + 0.5 and eave[2] <= t[4] - 0.5 and eave[3] >= t[5] + 0.5         # and past the platform edge


def test_ground_rooms_tile_the_house_without_overlap():
    rooms = [r for r in M._FLOOR_DATA["G"]["ROOMS"] if r[0] != "R17"]
    for r in rooms:
        assert M.HX1 <= r[2] < r[3] <= M.HX2 and M.HY1 <= r[4] < r[5] <= M.HY2, r[0]
    assert not [(a[0], b[0]) for i, a in enumerate(rooms) for b in rooms[i + 1:] if overlap(a[2:6], b[2:6]) > 0.01]
    assert abs(sum((r[3] - r[2]) * (r[5] - r[4]) for r in rooms) - (M.HX2 - M.HX1) * (M.HY2 - M.HY1)) < 0.01
    ids = [r[0] for r in M._FLOOR_DATA["G"]["ROOMS"]]
    assert len(ids) == len(set(ids))
    assert not set(ids) & {"R54", "R52", "R57", "R53", "R10"}        # dropped with the 54 x 54 plan
    for rid in ids:
        assert rid in M.FLOOR_FINISH and rid in M.CEILINGS, rid


def test_walkway_is_the_hallway():
    circ = [r for r in M._FLOOR_DATA["G"]["ROOMS"] if r[6] == "Circulation"]
    assert {r[0] for r in circ} == {"R06", "R09"}                     # the stair and its foot lobby only
    lob = ROOM("R09")                                                # the foot lobby, run on to the walkway: one strip under 4 ft deep
    assert lob[2] == M.HX1 and lob[3] == M.RING[0] and lob[5] - lob[4] <= 4.0 and lob[5] == M.STAIR["flight1"][2]
    walk = {"R51", "R61", "R62", "R63"}
    assert {r[0] for r in M._FLOOR_DATA["G"]["ROOMS"] if r[6] == "Courtyard"} == walk | {"R50"}
    d = ROOM("R42")                                                  # the den opens straight off the north walkway
    assert d[4] == M.RING[3] and d[2] < M.RING[1] and d[3] > M.RING[0]


def test_den_bath_on_the_west_wall_and_the_den_wall_carries_the_wing():
    import geom
    b, d = ROOM("R07"), ROOM("R42")
    assert b[2] == M.HX1 and b[3] <= M.RING[0] and b[5] == M.HY2 and _q("R07") == "NW"
    assert abs(b[3] - d[2]) < 0.01 and b[4] < d[5] and b[5] > d[4]  # shares an edge with the den (en-suite)
    with M.on_floor("G"):
        w = next(w for w in M.WALLS if w[0] == "Y" and w[1] == d[3])
        assert geom.wall_type(w) == "EXT" and w[2] <= d[4] and w[3] >= d[5]   # 9 in wall on x 33.5: an upper wing wall can stand on it
        assert overlap(b[2:6], ROOM("R06")[2:6]) == 0
        types = {w: geom.wall_type(w) for w in M.WALLS}
        assert types[("Y", M.RING[0], M.HY1, M.RING[2])] == "EXT"           # master to its bath: the wing's east wall above
        assert all(t == "INT" for w, t in types.items() if w[0] == "Y" and w[1] == ROOM("R60")[2])   # powder to pantry: no plumbing
    k = ROOM("R47")                                                  # the den's walk-in wardrobe, entered from the den
    assert k[5] == d[4] and d[2] < k[2] < k[3] <= d[3]
    c, f2 = ROOM("R48"), M.STAIR["flight2"]                           # the DB and linen cupboard under flight 2, off the foot lobby
    assert c[2] <= f2[0] and f2[1] <= c[3] and c[4] == f2[2] and c[5] == f2[3] and c[4] == ROOM("R09")[5]


# ---------- Task 4: ground floor doors, windows and transoms ----------
from planlib import graph, reachable


def _g(key):
    return M._FLOOR_DATA["G"][key]


def test_every_ground_room_reachable_from_the_foyer():
    with M.on_floor("G"):
        rooms = [(r[0], r[2], r[3], r[4], r[5]) for r in M.ROOMS]
        g = graph(rooms, M.WALLS, M.DOORS)
    lost = {r[0] for r in rooms} - reachable(g, "R18")
    assert not lost, f"rooms with no way in: {sorted(lost)}"


def test_main_door_on_the_east_axis():
    d = next(d for d in M._FLOOR_DATA["G"]["DOORS"] if d[0] == "D01")
    f = ROOM("R18")
    assert d[1] == "Y" and d[2] == M.HX2 and (d[3] + d[4]) / 2 > M.CY and f[4] <= d[3] and d[4] <= f[5] and abs(d[4] - d[3]) >= 4   # north half, into the foyer


def test_door_ids_unique_and_named():
    ids = [d[0] for d in _g("DOORS")]
    assert len(ids) == len(set(ids))
    for need in ("D01", "D04", "D42", "D02", "D07", "D45", "D08", "D11", "D12", "D17", "D18", "D60", "D62", "D09", "D46", "D47", "D48", "D64"):
        assert need in ids, need
    assert not set(ids) & {d[0] for d in M.DOORS_F1}, "ground door ids clash with first-floor ids"
    assert not {w[0] for w in _g("WINDOWS")} & {w[0] for w in M.WINDOWS_F1}


def test_folding_doors_fill_the_four_courtyard_edges():
    folding = [d for d in _g("DOORS") if "folding" in d[6].lower()]
    assert all(d[5] == 0 and abs(d[4] - d[3]) <= 8 for d in folding)
    for axis, c, lo, hi in (("X", M.RING[3], ROOM("R16")[2], M.RING[1]), ("Y", M.RING[1], M.RING[2], M.RING[3])):   # living; oonjal link and dining end
        on = [d for d in folding if d[1] == axis and d[2] == c]
        assert on and sum(d[4] - d[3] for d in on) >= 0.8 * (hi - lo), (axis, c)
        assert min(d[3] for d in on) > lo and max(d[4] for d in on) < hi
    assert {"D60", "D62"} <= {d[0] for d in folding}


def test_pooja_opens_west_inward_carved():
    d = next(d for d in _g("DOORS") if d[0] == "D11")
    assert d[1] == "Y" and d[2] == ROOM("R11")[2] and d[5] == 1 and "carved" in d[7].lower()   # on the pooja's west wall, opening inward (east)


def test_master_bath_door_opens_outward_into_the_bedroom():
    d = next(d for d in _g("DOORS") if d[0] == "D42")
    assert d[1] == "Y" and d[2] == M.RING[0] and d[5] == -1 and abs((d[4] - d[3]) - 2.75) < 0.01 and "lift-off" in d[7].lower()


def test_every_outer_room_has_a_window():
    wins = _g("WINDOWS")
    bad = []
    for r in _g("ROOMS"):
        if r[0] in {"R17", "R50"}:
            continue
        x1, x2, y1, y2 = r[2:6]
        edges = [("X", M.HY1, x1, x2) for _ in [0] if y1 == M.HY1] + [("X", M.HY2, x1, x2) for _ in [0] if y2 == M.HY2] \
            + [("Y", M.HX1, y1, y2) for _ in [0] if x1 == M.HX1] + [("Y", M.HX2, y1, y2) for _ in [0] if x2 == M.HX2]
        if edges and not any(w[1] == ax and w[2] == c and lo <= w[3] and w[4] <= hi for ax, c, lo, hi in edges for w in wins):
            bad.append(r[0])
    assert not bad, f"outer-wall rooms without a window: {bad}"


def test_genkan_two_jali_windows_and_pooja_high_vent():
    wins = _g("WINDOWS")
    assert sum(1 for w in wins if w[7].startswith("Foyer") and w[1] == "Y" and w[2] == M.HX2 and "jali" in w[8].lower()) >= 1
    assert any(w[7] == "Pooja" and w[5] >= 7 for w in wins)


def test_master_bedroom_two_south_windows_either_side_of_the_bed_head():
    ws = [w for w in _g("WINDOWS") if w[7] == "Master bedroom" and w[1] == "X" and w[2] == M.HY1]
    mx = (ROOM("R01")[2] + ROOM("R01")[3]) / 2
    f = _furn("F10"); bx = (f[3] + f[4]) / 2                         # the bed head's centre, between the two windows
    assert len(ws) == 2 and (ws[0][4] <= bx <= ws[1][3] or ws[1][4] <= bx <= ws[0][3]) and abs(bx - mx) <= 2.5


def test_south_and_west_windows_are_small():
    for w in _g("WINDOWS"):
        if (w[1] == "X" and w[2] == M.HY1) or (w[1] == "Y" and w[2] == M.HX1):
            assert w[4] - w[3] <= 4.0, w[0]


def _room_at(pt):
    hits = [r for r in _g("ROOMS") if r[2] - 1e-6 <= pt[0] <= r[3] + 1e-6 and r[4] - 1e-6 <= pt[1] <= r[5] + 1e-6]
    return min(hits, key=lambda r: (r[3] - r[2]) * (r[5] - r[4]))[0] if hits else None


def _door_sides(d, off=0.7):
    """(room on the -side, room on the +side) of a door, probed 0.7 ft off the wall at its centre."""
    m = (d[3] + d[4]) / 2
    pts = ((d[2] - off, m), (d[2] + off, m)) if d[1] == "Y" else ((m, d[2] - off), (m, d[2] + off))
    return _room_at(pts[0]), _room_at(pts[1])


def test_hinged_walkway_doors_open_into_their_rooms():
    walkway = {"R51", "R61", "R62", "R63"}
    seen = 0
    for d in _g("DOORS"):
        neg, pos = _door_sides(d)
        if not (walkway & {neg, pos}) or d[5] == 0:
            continue                                   # not on the walkway, or sliding / folding
        seen += 1
        into = pos if d[5] == 1 else neg
        assert into and into not in walkway, f"{d[0]} swings out into the walkway"
    assert seen >= 2                                   # at least the master (D04) and the den (D02)


def test_bath_doors_wide_enough_and_clear_of_the_wc_zone():
    for did, room, outward in (("D07", "R07", True), ("D08", "R08", None), ("D42", "R40", True)):
        d = next(d for d in _g("DOORS") if d[0] == did)
        assert d[4] - d[3] >= 2 + 8 / 12 - 1e-6, did                    # at least 2'-8" clear for the den bath and the powder room
        if outward:
            into = _door_sides(d)[1] if d[5] == 1 else _door_sides(d)[0]
            assert into != room, f"{did} swings into its own bath"
        else:
            assert d[5] == 0, f"{did} must slide so nothing swings into the walkway or the WC zone"
        # the basin wall straight opposite the door is solid for at least 2'-6" about the door's centre line
        r = _g("ROOMS")[[x[0] for x in _g("ROOMS")].index(room)]
        mid = (d[3] + d[4]) / 2
        if d[1] == "Y":
            opp = r[3] if abs(d[2] - r[2]) < 0.01 else r[2]
            ok = planlib_on_wall("Y", opp, mid - 1.25, mid + 1.25)
        else:
            opp = r[5] if abs(d[2] - r[4]) < 0.01 else r[4]
            ok = planlib_on_wall("X", opp, mid - 1.25, mid + 1.25)
        assert ok, f"{did}: no solid wall opposite for the basin"
    assert abs(next(d for d in _g("DOORS") if d[0] == "D42")[4] - next(d for d in _g("DOORS") if d[0] == "D42")[3] - 2.75) < 0.01


def planlib_on_wall(axis, c, a, b):
    from planlib import on_wall
    return on_wall(axis, c, a, b, M._FLOOR_DATA["G"]["WALLS"])


def test_stair_landing_window_sill_three_feet_above_the_landing():
    landing_z = M.STAIR["flight1"][4] * (M.STAIR["risers"] and 7.5 / 12)   # 8 risers of 7.5 in = 5'-0" above the ground floor
    y1, y2 = M.STAIR["landing"][2], M.STAIR["landing"][3]
    ws = [w for w in _g("WINDOWS") if w[1] == "Y" and w[2] == M.HX1 and w[7] == "Stair" and w[3] < y2 and w[4] > y1]
    assert ws, "no window over the half landing"
    assert all(w[5] >= landing_z + 3.0 - 1e-6 for w in ws), [(w[0], w[5]) for w in ws]


def test_low_store_hatch_is_four_feet_high_at_most():
    d = next(d for d in _g("DOORS") if d[0] == "D46")
    assert M.DOOR_HEIGHTS["D46"] <= 4.0
    assert "R46" in _door_sides(d) and all(M.DOOR_HEIGHTS.get(x[0], 7.0) == 7.0 for x in _g("DOORS") if x[0] != "D46")


def test_wet_rooms_and_the_kitchen_keep_an_outer_wall_opening_for_exhaust():
    outer = lambda w: (w[1] == "X" and w[2] in (M.HY1, M.HY2)) or (w[1] == "Y" and w[2] in (M.HX1, M.HX2))
    for rid, name in (("R40", "Master bath"), ("R07", "Den bath"), ("R13", "Utility"), ("R15", "Kitchen")):
        assert any(w[7] == name and outer(w) for w in _g("WINDOWS")), f"{rid}: no outer-wall window or vent for a fan"
    assert not any(w[7] in ("Powder room", "Pantry") and outer(w) for w in _g("WINDOWS"))   # inner rooms: vents on the walkway wall, reported


def test_main_door_and_pooja_door_facing():
    d01 = next(d for d in _g("DOORS") if d[0] == "D01")
    assert d01[2] == M.HX2 and 27.0 <= d01[3] and d01[4] <= 31.0 and "double" in d01[7].lower() and "carved" in d01[7].lower()
    assert _door_sides(d01)[1] in (None, "R17") and d01[5] == -1               # opens into the foyer
    d11 = next(d for d in _g("DOORS") if d[0] == "D11")
    assert _door_sides(d11) == ("R16", "R11") and d11[5] == 1                   # the family faces east to the idols


def test_ground_door_and_window_ids_clear_of_the_first_floor():
    ids = [d[0] for d in _g("DOORS")] + [w[0] for w in _g("WINDOWS")]
    assert len(ids) == len(set(ids))
    f1 = {d[0] for d in M.DOORS_F1} | {w[0] for w in M.WINDOWS_F1}
    assert not set(ids) & f1


def test_thinnai_is_red_oxide():
    assert "red oxide" in M.FLOOR_FINISH["R17"].lower()


# ---------- Task C4: ground floor furniture and fittings (with the Group B access items) ----------
import pytest

BATHS = {"R40": ("D42", "F14", "F12"), "R07": ("D07", "F49", "F48"), "R08": ("D08", "F17", "F16")}
ALL_BATHS = ["R40", "R07", "R08", "R33", "R39"]          # the ground baths, then the first-floor ones (added below, Task C5)
M_TO_FT = 1 / 0.3048


def _door(did):
    return next(d for fl in ("G", "F1") for d in M._FLOOR_DATA[fl]["DOORS"] if d[0] == did)


def _furn(fid):
    return next(f for fl in ("G", "F1") for f in M._FLOOR_DATA[fl]["FURNITURE"] if f[0] == fid)


def _room(rid):
    return next(r for fl in ("G", "F1") for r in M._FLOOR_DATA[fl]["ROOMS"] if r[0] == rid)


def _faces(rid):
    """Clear wall faces (x1, x2, y1, y2) of a room."""
    import geom
    fl = "F1" if rid in M.F1_ROOM_IDS else "G"
    r = _room(rid)
    with M.on_floor(fl):
        return (r[2] + geom._edge_t("Y", r[2], r[4], r[5]), r[3] - geom._edge_t("Y", r[3], r[4], r[5]),
                r[4] + geom._edge_t("X", r[4], r[2], r[3]), r[5] - geom._edge_t("X", r[5], r[2], r[3]))


def _gap(a, b):
    """Edge-to-edge distance between two rects (0 if they touch or overlap)."""
    dx = max(a[0] - b[1], b[0] - a[1], 0); dy = max(a[2] - b[3], b[2] - a[3], 0)
    return (dx * dx + dy * dy) ** 0.5


def _pt_gap(p, r):
    dx = max(r[0] - p[0], 0, p[0] - r[1]); dy = max(r[2] - p[1], 0, p[1] - r[3])
    return (dx * dx + dy * dy) ** 0.5


def _in_room(f, rid):
    r = _room(rid)
    return inside(((f[3] + f[4]) / 2, (f[5] + f[6]) / 2), r[2:6])


@pytest.mark.parametrize("rid", ALL_BATHS)
def test_basin_opposite_the_door_and_wc_out_of_line(rid):
    did, basin, wc = BATHS[rid]
    r, d, b, w = _room(rid), _door(did), _furn(basin), _furn(wc)
    if d[1] == "Y":
        far = r[3] if abs(d[2] - r[2]) < 0.01 else r[2]
        assert abs((b[3] if far < d[2] else b[4]) - far) <= 1.0, (rid, "basin not on the wall opposite the door")
        lo, hi = min(d[3], d[4]), max(d[3], d[4])
        assert not (lo < (w[5] + w[6]) / 2 < hi and abs((w[3] + w[4]) / 2 - far) < 2.5), (rid, "WC in line with the door")
    else:
        far = r[5] if abs(d[2] - r[4]) < 0.01 else r[4]
        assert abs((b[5] if far < d[2] else b[6]) - far) <= 1.0, (rid, "basin not on the wall opposite the door")
        lo, hi = min(d[3], d[4]), max(d[3], d[4])
        assert not (lo < (w[3] + w[4]) / 2 < hi and abs((w[5] + w[6]) / 2 - far) < 2.5), (rid, "WC in line with the door")


@pytest.mark.parametrize("rid", ALL_BATHS)
def test_basin_centred_on_the_door(rid):
    did, basin, _ = BATHS[rid]
    d, b = _door(did), _furn(basin)
    dc = (d[3] + d[4]) / 2
    bc = (b[5] + b[6]) / 2 if d[1] == "Y" else (b[3] + b[4]) / 2
    assert abs(bc - dc) <= 0.5, (rid, bc, dc)


def test_carry_overs_present():
    ids = {f[0] for fl in ("G", "F1") for f in M._FLOOR_DATA[fl]["FURNITURE"]}
    need = {"F10", "F06", "F14", "F17", "F49", "F24", "F27", "F116", "F28", "F34", "F35", "F38", "F114", "F26", "F41", "F52",
            "F120", "F121", "F122", "F123", "F124", "F125", "F126", "F128"}
    assert not need - ids, sorted(need - ids)


def test_every_listed_id_is_on_the_ground_floor():
    ids = {f[0] for f in M._FLOOR_DATA["G"]["FURNITURE"]}
    need = {"F10", "F11", "F06", "F19", "F138", "F12", "F13", "F14", "F140", "F141", "F142", "F20", "F23", "F66", "F67", "F117",
            "F132", "F133", "F48", "F49", "F50", "F143", "F144", "F145", "F16", "F17", "F146",
            "F24", "F25", "F27", "F116", "F28", "F21", "F44", "F33", "F34", "F35", "F36", "F37", "F115", "F65", "F68", "F29", "F62",
            "F61", "F113", "F38", "F39", "F45", "F46", "F114", "F53", "F26", "F41", "F52", "F120", "F131", "F147", "F121", "F122",
            "F42", "F69", "F69b", "F125", "F126", "F148", "F149", "F123", "F124", "F31", "F112", "F128"}
    assert not need - ids, sorted(need - ids)
    assert {f[0] for f in M._FLOOR_DATA["G"]["FURNITURE"] if f[0] in M.OUTDOOR_FURNITURE} == M.OUTDOOR_FURNITURE


def test_outdoor_furniture_is_exactly_the_items_outside_the_rooms():
    rooms = [r[2:6] for r in M._FLOOR_DATA["G"]["ROOMS"]]
    outside = {f[0] for f in M._FLOOR_DATA["G"]["FURNITURE"] if not any(inside(((f[3] + f[4]) / 2, (f[5] + f[6]) / 2), r) for r in rooms)}
    assert outside == M.OUTDOOR_FURNITURE, (sorted(outside - M.OUTDOOR_FURNITURE), sorted(M.OUTDOOR_FURNITURE - outside))


@pytest.mark.parametrize("fl", ["G", "F1"])
def test_no_furniture_collides(fl):
    fs = [f for f in M._FLOOR_DATA[fl]["FURNITURE"] if f[9] not in ("glass",) and f[0] not in M.OUTDOOR_FURNITURE]
    fs += [(e[0] + "+",) + (None, None) + tuple(e[1:5]) + (None, None, "rect") for e in M._FLOOR_DATA[fl]["EXTRA_DRAW"]]
    bad = [(a[0], b[0]) for i, a in enumerate(fs) for b in fs[i + 1:] if overlap(a[3:7], b[3:7]) > 0.1]
    assert not bad, (fl, bad)


def test_ground_furniture_inside_the_clear_wall_faces():
    bad = []
    for f in M._FLOOR_DATA["G"]["FURNITURE"]:
        if f[0] in M.OUTDOOR_FURNITURE:
            continue
        rid = next(r[0] for r in M._FLOOR_DATA["G"]["ROOMS"] if _in_room(f, r[0]))
        x1, x2, y1, y2 = _faces(rid)
        if f[3] < x1 - 0.02 or f[4] > x2 + 0.02 or f[5] < y1 - 0.02 or f[6] > y2 + 0.02:
            bad.append((f[0], rid))
    assert not bad, bad


def test_furniture_ids_unique():
    ids = [f[0] for fl in ("G", "F1") for f in M._FLOOR_DATA[fl]["FURNITURE"]]
    assert len(ids) == len(set(ids))


def test_courtyard_bed_is_a_round_4ft_bed_on_the_centre():
    f = _furn("F128")
    assert f[9] == "circle" and abs((f[4] - f[3]) - 4) < 1e-6 and abs((f[6] - f[5]) - 4) < 1e-6
    assert ((f[3] + f[4]) / 2, (f[5] + f[6]) / 2) == (M.CX, M.CY)
    assert "tulsi" in f[2].lower()


def test_master_bed_head_south_between_the_windows():
    f = _furn("F10")
    r = _room("R01")
    assert r[2] + 2 <= f[3] and f[4] <= r[3] - 2 and f[5] - r[4] < 1.0
    w60, w61 = (next(w for w in M._FLOOR_DATA["G"]["WINDOWS"] if w[0] == i) for i in ("W60", "W61"))
    assert w60[4] <= f[3] and f[4] <= w61[3]
    assert _furn("F06")[1] == "Master bedroom"                  # the wardrobe (no dressing room in the compact plan)


def test_master_bed_two_feet_clear_both_sides_and_the_foot():
    b = _furn("F10")
    x1, x2, y1, y2 = _faces("R01")
    strips = [(b[3] - 2, b[3], b[5], b[6]), (b[4], b[4] + 2, b[5], b[6]), (b[3], b[4], b[6], b[6] + 2)]   # west, east, foot
    others = [f[3:7] for f in M._FLOOR_DATA["G"]["FURNITURE"] if f[1] == "Master bedroom" and f[0] not in ("F10", "F11")]   # F11: wall-hung at the head
    for s in strips:
        assert x1 - 0.01 <= s[0] and s[1] <= x2 + 0.01 and y1 - 0.01 <= s[2] and s[3] <= y2 + 0.01, s
        assert all(overlap(s, o) == 0 for o in others), s


def test_kitchen_sink_under_w82_and_two_feet_of_counter_to_the_hob():
    sink, prep, hob, ret = _furn("F65"), _furn("F34"), _furn("F35"), _furn("F115")
    x1, x2, y1, y2 = _faces("R15")
    w82 = next(w for w in M.WINDOWS if w[0] == "W82")
    w83 = next(w for w in M.WINDOWS if w[0] == "W83")
    assert w82[1] == "X" and w82[2] == M.HY1 and w82[3] <= (sink[3] + sink[4]) / 2 <= w82[4] and abs(sink[5] - y1) < 0.02
    hob_c = (w83[3] + w83[4]) / 2                                                     # the hob (2 ft) is centred under the high vent
    assert abs(prep[3] - sink[4]) < 0.01 and abs(prep[4] - x2) < 0.02 and abs(hob[5] - prep[6]) < 0.01
    run = (prep[4] - 2.0 - sink[4]) + (hob_c - 1.0 - (y1 + 2.0))                      # along the L's front edge, sink to hob
    assert run >= 2.0 and hob_c - 1.0 - hob[5] >= 2.0 - 0.01 and hob[6] - (hob_c + 1.0) >= 1.0
    assert abs(hob[4] - x2) < 0.02 and w83[1] == "Y" and w83[2] == M.HX2              # hob on the east wall: the cook faces east
    assert hob[5] <= w83[3] and w83[4] <= hob[6] and w83[5] >= 6.0                    # under the high vent, the wall below it solid
    assert abs(ret[4] - sink[3]) < 0.01
    sw = (x1, x1 + 2.5, y1, y1 + 2.5)                                                  # the utility door's corner stays free
    assert all(overlap(sw, f[3:7]) == 0 for f in M._FLOOR_DATA["G"]["FURNITURE"] if f[1] == "Kitchen")


def test_thinnai_and_door_fittings():
    d = _door("D01")
    k = _furn("F121")
    assert k[1] == "Thinnai" and k[3] >= d[2] and abs((k[5] + k[6]) / 2 - (d[3] + d[4]) / 2) < 0.01 and d[3] <= k[5] and k[6] <= d[4]
    assert abs(_furn("F122")[5] - d[4]) <= 0.5                   # beside the door's jamb
    for fid in ("F42", "F69"):
        f = _furn(fid)
        t = _room("R17")
        assert t[2] <= f[3] and f[4] <= t[3] and t[4] <= f[5] and f[6] <= t[5] and not (f[5] < d[4] and f[6] > d[3])
    ramp = next(s[3] for s in M.SITE_FEATURES if s[0] == "RAMP")
    assert _furn("F42")[4] <= ramp[0] + 1.0                       # the ramp's arrival (x 58-62) keeps 3 ft clear past the south seat


def test_rain_chain_basins_under_the_thinnai_eave_corners_clear_of_the_ramp_and_steps():
    ex, ey1, ey2 = M.ROOF["thinnai"][1], M.ROOF["thinnai"][2], M.ROOF["thinnai"][3]
    keep = [s[3] for s in M.SITE_FEATURES if s[0] in ("RAMP", "STEPS")]
    d = _door("D01")
    ys = []
    for fid in ("F125", "F126"):
        f = _furn(fid)
        cx, cy = (f[3] + f[4]) / 2, (f[5] + f[6]) / 2
        assert abs(cx - ex) <= 0.5 and ey1 <= cy <= ey2, fid
        assert all(overlap(f[3:7], k) == 0 for k in keep), fid
        ys.append(cy)
    assert ys[0] < d[3] and ys[1] > d[4]                           # one at each end of the eave


def test_entrance_steps_have_handrails_on_both_sides():
    st = next(s[3] for s in M.SITE_FEATURES if s[0] == "STEPS")
    rails = [f for f in M._FLOOR_DATA["G"]["FURNITURE"] if "handrail" in f[2].lower() and "entrance steps" in f[2].lower()]
    south = [f for f in rails if f[6] <= st[2] + 0.01 and st[2] - f[6] <= 0.3 and f[3] < st[1] and f[4] > st[0]]
    north = [f for f in rails if f[5] >= st[3] - 0.01 and f[5] - st[3] <= 0.3 and f[3] < st[1] and f[4] > st[0]]
    assert south and north
    assert "both sides" in next(s[1] for s in M.SITE_FEATURES if s[0] == "STEPS")


def test_grab_post_at_the_foyer_step():
    post = [f for f in M._FLOOR_DATA["G"]["FURNITURE"] if "grab post" in f[2].lower()]
    assert len(post) == 1 and _in_room(post[0], "R18")
    gap = next(w for w in M._FLOOR_DATA["G"]["WALLS"] if w[0] == "Y" and w[1] == M._OX and w[2] == M._FY)[3]   # the opening's south jamb
    jamb_n = 31.0
    assert _pt_gap((M._OX, jamb_n), post[0][3:7]) <= 0.5 or _pt_gap((M._OX, gap), post[0][3:7]) <= 0.5
    assert not (post[0][5] < jamb_n and post[0][6] > gap)          # it does not narrow the 4 ft opening


def test_grab_rails_beside_every_wc_and_in_the_master_and_den_showers():
    fs = M._FLOOR_DATA["G"]["FURNITURE"] + M._FLOOR_DATA["F1"]["FURNITURE"]   # every WC on both floors (Group B)
    for w in [f for f in fs if f[9] == "wc"]:
        rails = [f for f in fs if f[1] == w[1] and "grab rail" in f[2].lower() and _gap(f[3:7], w[3:7]) <= 1.0]
        assert rails, f"no grab rail beside the WC {w[0]} ({w[1]})"
        assert all("600 mm" in f[2] for f in rails)
    fs = M._FLOOR_DATA["G"]["FURNITURE"]
    for rid, name in (("R40", "Master bath"), ("R07", "Den bath")):
        zone = M.SHOWERS[rid]
        assert any(f[1] == name and "grab rail" in f[2].lower() and overlap(f[3:7], zone) > 0 for f in fs), rid
        seat = [f for f in fs if f[1] == name and "fold-down" in f[2].lower() and "seat" in f[2].lower()]
        assert seat and all(overlap(s[3:7], zone) >= (s[4] - s[3]) * (s[6] - s[5]) - 1e-6 for s in seat), rid


def _fl(rid):
    return "F1" if rid in M.F1_ROOM_IDS else "G"


def test_showers_open_away_from_the_wc_and_the_door():
    for rid in ("R40", "R07", "R33", "R39"):
        name = _room(rid)[1]
        did, _, wc = BATHS[rid]
        x1, x2, y1, y2 = _faces(rid)
        sx1, sx2, sy1, sy2 = M.SHOWERS[rid]
        glass = [f[3:7] for f in M._FLOOR_DATA[_fl(rid)]["FURNITURE"] if f[1] == name and f[9] == "glass"]
        # the open sides: zone edges that are neither on a wall face nor covered by glass; sample points just outside them
        opens = []
        for k in range(1, 20):
            t = k / 20
            for side, p in (("W", (sx1 - 0.2, sy1 + t * (sy2 - sy1))), ("E", (sx2 + 0.2, sy1 + t * (sy2 - sy1))),
                            ("S", (sx1 + t * (sx2 - sx1), sy1 - 0.2)), ("N", (sx1 + t * (sx2 - sx1), sy2 + 0.2))):
                if not (x1 <= p[0] <= x2 and y1 <= p[1] <= y2):
                    continue                                    # that side is a wall
                if any(_pt_gap(p, g) <= 0.25 for g in glass):
                    continue
                opens.append((side, p))
        assert opens, rid
        w, d = _furn(wc), _door(did)
        for side, p in opens:
            ray = {"E": (p[0], x2, p[1] - 0.01, p[1] + 0.01), "W": (x1, p[0], p[1] - 0.01, p[1] + 0.01),
                   "N": (p[0] - 0.01, p[0] + 0.01, p[1], y2), "S": (p[0] - 0.01, p[0] + 0.01, y1, p[1])}[side]
            assert overlap(ray, w[3:7]) == 0, (rid, "shower opens toward the WC")
            if d[1] == "Y":
                assert not (side in "EW" and min(d[3], d[4]) < p[1] < max(d[3], d[4])), (rid, "shower opens toward the door")
            else:
                assert not (side in "NS" and min(d[3], d[4]) < p[0] < max(d[3], d[4])), (rid, "shower opens toward the door")


def test_reading_chair_by_a_master_window():
    chair = [f for f in M._FLOOR_DATA["G"]["FURNITURE"] if f[1] == "Master bedroom" and "reading chair" in f[2].lower()]
    assert len(chair) == 1
    wins = [w for w in M._FLOOR_DATA["G"]["WINDOWS"] if w[7] == "Master bedroom"]
    line = lambda w: (w[2], w[2], w[3], w[4]) if w[1] == "Y" else (w[3], w[4], w[2], w[2])
    assert any(_gap(line(w), chair[0][3:7]) <= 1.0 for w in wins)


def test_dining_bench_16in_stools_tuck_under_and_an_armchair_at_the_end():
    t, bench, chair = _furn("F24"), _furn("F28"), _furn("F25")
    assert abs(min(bench[4] - bench[3], bench[6] - bench[5]) - 16 / 12) < 0.05
    assert _gap(bench[3:7], t[3:7]) <= 0.5
    assert "armchair" in chair[2].lower() and _gap(chair[3:7], t[3:7]) <= 0.5
    assert (chair[3] < t[4] and chair[4] > t[3]) and (chair[5] >= t[6] or chair[6] <= t[5])     # at an end of the table
    for fid in ("F27", "F116"):
        s = _furn(fid)
        assert max(s[4] - s[3], s[6] - s[5]) <= 1.4 and _gap(s[3:7], t[3:7]) <= 0.3, fid
    # the kitchen path: 3 ft clear from the kitchen door to the oonjal link
    from planlib import walkable
    d17 = _door("D17")
    r = _room("R16D")
    obs = [f[3:7] for f in M._FLOOR_DATA["G"]["FURNITURE"] if f[9] != "glass" and _in_room(f, "R16D")]
    assert walkable(r[2:6], obs, ((d17[3] + d17[4]) / 2, r[4] + 1.6), ((d17[3] + d17[4]) / 2, r[5] - 1.6), 3.0)


def test_oonjal_in_the_console_nook_swinging_east_west_clear_of_the_link():
    o = _furn("F41")
    assert _in_room(o, "R16N")
    assert (o[6] - o[5]) > (o[4] - o[3])                                     # the seat runs north-south: it swings east-west
    x1, x2, y1, y2 = _faces("R16N")
    assert x2 - o[4] >= 2.5                                                  # room behind it
    band = [f for f in M._FLOOR_DATA["G"]["FURNITURE"] if f[0] != "F41" and f[5] < o[6] and f[6] > o[5] and f[4] <= o[3] and not f[0] in M.OUTDOOR_FURNITURE]
    assert all(o[3] - f[4] >= 3.0 for f in band)                             # 3 ft+ of swing in front, into the living
    assert not [f[0] for f in M._FLOOR_DATA["G"]["FURNITURE"] if _in_room(f, "R16S")]   # the link stays a clear path


def test_lpg_cage_one_and_a_half_metres_from_every_drain_and_the_rinse_shower():
    cage = _furn("F112")[3:7]
    lim = 1.5 * M_TO_FT
    drains = [(p[1], p[2], p[0]) for p in M._FLOOR_DATA["G"]["PLUMBING"] if p[0] in ("FT", "CD", "GT", "IC")]
    drains += [(s[3][0], s[3][1], s[0]) for s in M.SITE_FEATURES if s[0] == "FEET"]
    drains += [(p[1], p[2], "DP") for p in M._FLOOR_DATA["G"]["PLUMBING"] if p[0] == "DP"] + [(x, y, "downpipe") for x, y in M.ROOF["downpipes"]]
    sink = _furn("F65")
    drains.append(((sink[3] + sink[4]) / 2, M.HY1 - M.T, "kitchen sink outlet / grease trap"))   # its grey line leaves through the south wall
    for x, y, what in drains:
        assert _pt_gap((x, y), cage) >= lim, (what, x, y)
    assert _gap(_furn("F123")[3:7], cage) >= lim                             # the rinse shower drains where it stands


def test_outdoor_items_stay_outside_the_house_walls():
    for fid in M.OUTDOOR_FURNITURE:
        f = _furn(fid)
        cx, cy = (f[3] + f[4]) / 2, (f[5] + f[6]) / 2
        assert not (M.HX1 < cx < M.HX2 and M.HY1 < cy < M.HY2), fid
    keep = [s[3] for s in M.SITE_FEATURES if s[0] in ("RAMP", "STEPS", "PATH")]
    for fid in M.OUTDOOR_FURNITURE:
        assert all(overlap(_furn(fid)[3:7], k) == 0 for k in keep), fid
    for w in M._FLOOR_DATA["G"]["WINDOWS"]:                                 # nothing stands against a window outside
        line = (w[2], w[2], w[3], w[4]) if w[1] == "Y" else (w[3], w[4], w[2], w[2])
        for fid in ("F112", "F123"):
            assert _gap(line, _furn(fid)[3:7]) > 0.25 or w[5] >= 6.0, (fid, w[0])


def test_pocket_garden_seen_from_a_dining_window():
    g = _furn("F124")
    ws = [w for w in M._FLOOR_DATA["G"]["WINDOWS"] if w[7] in ("Dining end", "Family living") and w[1] == "Y" and w[2] == M.HX2]
    assert any(g[5] < w[4] and g[6] > w[3] and 0 < g[3] - M.HX2 <= 6 for w in ws)


import re


def _standing_zone(f, rid, depth=1.5, width=2.0):
    """The 1.5 x 2 ft floor zone in front of a wall-hung fitting, on the side away from its nearest wall face."""
    x1, x2, y1, y2 = _faces(rid)
    gaps = {"W": f[3] - x1, "E": x2 - f[4], "S": f[5] - y1, "N": y2 - f[6]}
    back = min(gaps, key=gaps.get)
    if back in "WE":
        c = min(max((f[5] + f[6]) / 2, y1 + width / 2), y2 - width / 2)
        return (f[4], f[4] + depth, c - width / 2, c + width / 2) if back == "W" else (f[3] - depth, f[3], c - width / 2, c + width / 2)
    c = min(max((f[3] + f[4]) / 2, x1 + width / 2), x2 - width / 2)
    return (c - width / 2, c + width / 2, f[6], f[6] + depth) if back == "S" else (c - width / 2, c + width / 2, f[5] - depth, f[5])


@pytest.mark.parametrize("fl", ["G", "F1"])
def test_a_clear_standing_zone_in_front_of_every_basin(fl):
    fs = M._FLOOR_DATA[fl]["FURNITURE"]
    rooms = M._FLOOR_DATA[fl]["ROOMS"]
    bad = []
    for b in [f for f in fs if re.match(r"(wash|hand-wash) basin|basin counter", f[2].lower())]:
        rid = next(r[0] for r in rooms if _in_room(b, r[0]))
        z = _standing_zone(b, rid)
        x1, x2, y1, y2 = _faces(rid)
        hits = [f[0] for f in fs if f[0] != b[0] and overlap(z, f[3:7]) > 0.01]
        if hits or z[0] < x1 - 0.01 or z[1] > x2 + 0.01 or z[2] < y1 - 0.01 or z[3] > y2 + 0.01:
            bad.append((b[0], hits))
    assert not bad, bad


def test_a_lane_to_the_north_end_of_the_dining_bench():
    from planlib import walkable
    b = _furn("F28")
    x1, x2, y1, y2 = _faces("R16D")
    obs = [f[3:7] for f in M._FLOOR_DATA["G"]["FURNITURE"] if f[9] != "glass" and _in_room(f, "R16D")]
    link = _room("R16S")
    assert walkable((x1, x2, y1, y2), obs, ((link[2] + link[3]) / 2, y2 - 0.8), (min((b[3] + b[4]) / 2, x2 - 0.75), b[6] + 0.75), 1.5, step=0.05)


def test_thinnai_ramp_arrival_three_feet_clear_past_the_pillar():
    px, py = min(M.THINNAI_PILLARS, key=lambda p: p[1])          # the pillar next to the ramp's arrival
    seat = _furn("F42")
    assert seat[5] < py < seat[6] and px - M.PILLAR_R - seat[4] >= 3.0
    assert "fold-up" in seat[2].lower()
    f69, ret = _furn("F69"), _furn("F69b")
    assert abs(ret[3] - f69[4]) < 0.01 and ret[4] <= M.THINNAI_PILLARS[1][0] - M.PILLAR_R and _in_room(ret, "R17")


def test_outward_exterior_doors_open_over_a_level_landing():
    feat = {s[0]: s[3] for s in M.SITE_FEATURES}
    landings = [feat["OTTA"], feat["WSTEP"], _room("R17")[2:6]]
    avoid = [feat[k] for k in ("STEPS", "GSTEP", "RAMP")]
    seen = 0
    for d in M._FLOOR_DATA["G"]["DOORS"]:
        if d[5] == 0:
            continue
        out = {("Y", M.HX1): -1, ("Y", M.HX2): 1, ("X", M.HY1): -1, ("X", M.HY2): 1}.get((d[1], d[2]))
        if out is None or d[5] != out:
            continue
        seen += 1
        w, f = abs(d[4] - d[3]), d[2] + out * M.T / 2                     # the leaf sweeps a w x w square off the outer face
        a, b = sorted((f, f + out * w))
        sweep = (a, b, min(d[3], d[4]), max(d[3], d[4])) if d[1] == "Y" else (min(d[3], d[4]), max(d[3], d[4]), a, b)
        assert any(l[0] - 0.05 <= sweep[0] and sweep[1] <= l[1] + 0.05 and l[2] - 0.05 <= sweep[2] and sweep[3] <= l[3] + 0.05 for l in landings), d[0]
        assert all(overlap(sweep, k) == 0 for k in avoid), d[0]
    assert seen >= 1                                                       # the den's garden door D45


def test_shower_entries_at_least_2ft_6in():
    for rid in ("R40", "R07", "R33", "R39"):
        name = _room(rid)[1]
        x1, x2, y1, y2 = _faces(rid)
        sx1, sx2, sy1, sy2 = M.SHOWERS[rid]
        glass = [f[3:7] for f in M._FLOOR_DATA[_fl(rid)]["FURNITURE"] if f[1] == name and f[9] == "glass"]
        best = 0.0
        for side in "WESN":
            n = 200; run = 0.0; step = ((sy2 - sy1) if side in "WE" else (sx2 - sx1)) / n
            for k in range(n):
                t = (k + 0.5) / n
                p = {"W": (sx1 - 0.2, sy1 + t * (sy2 - sy1)), "E": (sx2 + 0.2, sy1 + t * (sy2 - sy1)),
                     "S": (sx1 + t * (sx2 - sx1), sy1 - 0.2), "N": (sx1 + t * (sx2 - sx1), sy2 + 0.2)}[side]
                free = x1 <= p[0] <= x2 and y1 <= p[1] <= y2 and not any(_pt_gap(p, g) <= 0.12 for g in glass)
                run = run + step if free else 0.0
                best = max(best, run)
        assert best >= 2.5 - 0.05, (rid, round(best, 2))


def test_den_walk_in_aisle_and_the_den_bath_window_over_the_wc():
    x1, x2, y1, y2 = _faces("R47")
    w = _furn("F117")
    assert w[3] - x1 >= 2.0 - 0.01 and abs(w[4] - x2) < 0.02
    w68, wc = next(x for x in M._FLOOR_DATA["G"]["WINDOWS"] if x[0] == "W68"), _furn("F48")
    assert w68[3] <= (wc[3] + wc[4]) / 2 <= w68[4]


def test_utility_airer_clear_of_the_door_path():
    d18, d12 = _door("D18"), _door("D12")
    path = (min(d18[3], d18[4]), d12[2], M.HY1, max(d12[3], d12[4]))
    assert overlap(_furn("F61")[3:7], path) == 0


def test_pooja_mandapam_faces_west_and_the_foyer_fittings():
    m = _furn("F26")
    assert _in_room(m, "R11") and abs(m[4] - _faces("R11")[1]) < 0.02
    x1, x2, y1, y2 = _faces("R18")
    assert abs(_furn("F52")[5] - y1) < 0.02 and abs(_furn("F120")[6] - y2) < 0.02
    d01 = _door("D01")
    for fid in ("F52", "F120", "F131"):                                    # clear of the main door's leaves (2 ft each)
        assert overlap(_furn(fid)[3:7], (d01[2] - 2.0, d01[2], d01[3], d01[4])) == 0, fid


def test_den_wardrobe_in_the_walk_in_and_desk_in_the_niche():
    assert _in_room(_furn("F117"), "R47") and _in_room(_furn("F132"), "R58") and _in_room(_furn("F133"), "R58")
    d45 = _door("D45")
    assert d45[5] == -1                                                     # hinged, opening outward onto the deck
    w72 = next(w for w in M._FLOOR_DATA["G"]["WINDOWS"] if w[0] == "W72")
    assert w72[1] == "Y" and w72[2] == M.HX1 and "fixed" in w72[8].lower() and (w72[3] >= d45[4] or w72[4] <= d45[3])
    x1, x2, y1, y2 = _faces("R58")                                          # 2 ft+ from the den to the garden door with the chair tucked in
    desk = _furn("F132")
    assert desk[5] - y1 >= 2.5


def _tv_gap(tv, seat):
    if tv[4] <= seat[3]: return seat[3] - tv[4]
    if seat[4] <= tv[3]: return tv[3] - seat[4]
    if tv[6] <= seat[5]: return seat[5] - tv[6]
    return tv[5] - seat[6]


def test_viewing_distances_and_the_tvs_not_back_to_back():
    for tv, seats in (("F23", ("F20", "F67")), ("F53", ("F38",))):
        for s in seats:
            assert _tv_gap(_furn(tv), _furn(s)) >= 5, (tv, s)
    a, b = _furn("F23"), _furn("F53")
    across = max(b[3] - a[4], a[3] - b[4]); along = min(a[6], b[6]) - max(a[5], b[5])
    assert not (0 <= across <= 1.5 and along > 0), "den and living TVs back to back"


def test_sliding_doors_have_free_wall_to_park_on():
    import geom
    from planlib import on_wall
    g = M._FLOOR_DATA["G"]
    sliders = [d for d in g["DOORS"] if d[5] == 0 and "folding" not in d[6].lower()]
    assert {d[0] for d in sliders} == set(M.SLIDERS), sorted({d[0] for d in sliders} ^ set(M.SLIDERS))
    for d in sliders:
        along, face = M.SLIDERS[d[0]]
        w = abs(d[4] - d[3])
        lo, hi = (max(d[3], d[4]), max(d[3], d[4]) + w) if along > 0 else (min(d[3], d[4]) - w, min(d[3], d[4]))
        assert on_wall(d[1], d[2], lo, hi, g["WALLS"]), (d[0], "no wall to park on")
        for o in g["DOORS"] + g["WINDOWS"]:
            if o[0] != d[0] and o[1] == d[1] and abs(o[2] - d[2]) < 0.01 and min(o[4], hi) - max(o[3], lo) > 0.01:
                assert len(o) > 7 and o[5] >= 7.0, (d[0], "parks over", o[0])       # only a vent above the door head
        with M.on_floor("G"):
            for wl in g["WALLS"]:
                if wl[0] == d[1]:
                    continue
                t = geom.wall_t(wl) / 2
                probe = d[2] + face * 0.3
                if wl[1] + t > lo + 0.01 and wl[1] - t < hi - 0.01 and min(wl[2], wl[3]) <= probe <= max(wl[2], wl[3]):
                    raise AssertionError((d[0], "a cross wall cuts the parking wall", wl))
        strip = ((d[2], d[2] + face * 0.9) if face > 0 else (d[2] - 0.9, d[2]))
        rect = (min(strip), max(strip), lo, hi) if d[1] == "Y" else (lo, hi, min(strip), max(strip))
        hits = [f[0] for f in g["FURNITURE"] if f[9] != "glass" and overlap(rect, f[3:7]) > 0]
        assert not hits, (d[0], "furniture on the parking wall", hits)


@pytest.mark.parametrize("fl", ["G", "F1"])
def test_every_door_of_a_room_reaches_every_other_with_2ft_clear(fl):
    from planlib import walkable
    bad = []
    f = M._FLOOR_DATA[fl]
    for room in f["ROOMS"]:
        obs = [x[3:7] for x in f["FURNITURE"] if x[9] != "glass" and x[0] not in M.OUTDOOR_FURNITURE
               and room[2] - 0.01 <= (x[3] + x[4]) / 2 <= room[3] + 0.01 and room[4] - 0.01 <= (x[5] + x[6]) / 2 <= room[5] + 0.01]
        if not obs:
            continue                      # rooms without furniture (walkways, stair) cannot be blocked
        pts = _door_points(room, f["DOORS"])
        for i, (da, pa) in enumerate(pts):
            for db, pb in pts[i + 1:]:
                if not walkable(room[2:6], obs, pa, pb, 2.0):
                    bad.append((fl, room[0], da, db))
    assert not bad, bad


def _door_points(room, doors):
    """(door id, point 1 ft inside the room from the door centre) for every door on the room's boundary."""
    _, _, x1, x2, y1, y2, _ = room
    pts = []
    for d in doors:
        mid = (d[3] + d[4]) / 2
        if d[1] == "Y" and y1 - 0.01 <= mid <= y2 + 0.01:
            if abs(d[2] - x1) < 0.01: pts.append((d[0], (x1 + 1, mid)))
            elif abs(d[2] - x2) < 0.01: pts.append((d[0], (x2 - 1, mid)))
        elif d[1] == "X" and x1 - 0.01 <= mid <= x2 + 0.01:
            if abs(d[2] - y1) < 0.01: pts.append((d[0], (mid, y1 + 1)))
            elif abs(d[2] - y2) < 0.01: pts.append((d[0], (mid, y2 - 1)))
    return pts


# ---------- Task C5: upper wing (west band + over the den), stair well, roof terrace and jharokhas ----------
BATHS.update({"R33": ("D33", "F78", "F77"), "R39": ("D39", "F99", "F98")})


def test_stair_well_is_clear_upstairs():
    s = M.STAIR
    well = [s["flight1"][:4], s["flight2"][:4]]
    for r in M._FLOOR_DATA["F1"]["ROOMS"]:
        if r[0] in ("R41",):
            continue
        assert all(overlap(r[2:6], w) < 0.05 for w in well), r[0]


def test_stair_head_only_over_the_arrival_strip():
    # R41 may reach the well only by less than one tread past the top riser, and never over the landing
    s = M.STAIR
    r = _room("R41")
    assert r[5] <= s["flight1"][2] + s["tread"] + 0.01, r
    for room in M._FLOOR_DATA["F1"]["ROOMS"]:
        assert overlap(room[2:6], s["landing"]) < 0.05, room[0]


def test_slab_void_covers_both_flights_and_the_landing():
    s = M.STAIR
    for part in (s["flight1"][:4], s["flight2"][:4], s["landing"], s["core"]):
        assert all(overlap(p, part) < 0.05 for p in M.SLAB_F1), part


def _bath_faces(rid):
    import geom
    fl = "F1" if rid in M.F1_ROOM_IDS else "G"
    r = _room(rid)
    with M.on_floor(fl):
        return (r[2] + geom._edge_t("Y", r[2], r[4], r[5]), r[3] - geom._edge_t("Y", r[3], r[4], r[5]),
                r[4] + geom._edge_t("X", r[4], r[2], r[3]), r[5] - geom._edge_t("X", r[5], r[2], r[3]))


def _shower_matches_glass_and_walls(rid, faces, tol=0.02):
    """The shower zone is fixed by the drawn glass and the walls: one edge flush with a glass screen, the opposite edge on
    a wall face, and along the glass one end on a wall face and the other on a wall face or the glass's own end."""
    x1, x2, y1, y2 = faces
    sx1, sx2, sy1, sy2 = M.SHOWERS[rid]
    fl = "F1" if rid in M.F1_ROOM_IDS else "G"
    name = _room(rid)[1]
    glass = [f[3:7] for f in M._FLOOR_DATA[fl]["FURNITURE"] if f[1] == name and f[9] == "glass"]
    ok = False
    for g in glass:
        if g[1] - g[0] < g[3] - g[2]:          # a screen running along y: it fixes an x edge
            if abs(g[1] - sx1) <= tol and abs(sx2 - x2) <= tol or abs(g[0] - sx2) <= tol and abs(sx1 - x1) <= tol:
                ends = [(sy1, y1, g[2]), (sy2, y2, g[3])]
            else:
                continue
        else:                                   # a screen running along x: it fixes a y edge
            if abs(g[3] - sy1) <= tol and abs(sy2 - y2) <= tol or abs(g[2] - sy2) <= tol and abs(sy1 - y1) <= tol:
                ends = [(sx1, x1, g[0]), (sx2, x2, g[1])]
            else:
                continue
        on_wall = [abs(z - w) <= tol for z, w, _ in ends]
        on_glass_end = [abs(z - e) <= 0.15 for z, _, e in ends]
        if any(on_wall) and all(a or b for a, b in zip(on_wall, on_glass_end)):
            ok = True
    assert ok, (rid, "SHOWERS zone does not follow the drawn glass and the walls", M.SHOWERS[rid], glass)


@pytest.mark.parametrize("rid", ALL_BATHS)
def test_wc_clearances_and_shower_size(rid):
    for rid, (_, _, wc) in [(rid, BATHS[rid])]:
        r, w = _room(rid), _furn(wc)
        x1, x2, y1, y2 = _bath_faces(rid)
        fl = "F1" if rid in M.F1_ROOM_IDS else "G"
        others = [f[3:7] for f in M._FLOOR_DATA[fl]["FURNITURE"] if f[0] != wc and r[1] == f[1]]
        if rid in M.SHOWERS:
            others.append(M.SHOWERS[rid])
        # the wall the WC stands on: the nearest clear face
        gaps = {"W": w[3] - x1, "E": x2 - w[4], "S": w[5] - y1, "N": y2 - w[6]}
        back = min(gaps, key=gaps.get)
        if back in "WE":       # it faces along x; its sides are in y
            c = (w[5] + w[6]) / 2
            band = [o for o in others if o[0] < w[4] and o[1] > w[3]]
            lo = max([y1] + [o[3] for o in band if o[3] <= c]); hi = min([y2] + [o[2] for o in band if o[2] >= c])
            front_band = [o for o in others if o[2] < w[6] and o[3] > w[5]]
            front = (min([x2] + [o[0] for o in front_band if o[0] >= w[4]]) - w[4]) if back == "W" else (w[3] - max([x1] + [o[1] for o in front_band if o[1] <= w[3]]))
        else:                  # it faces along y; its sides are in x
            c = (w[3] + w[4]) / 2
            band = [o for o in others if o[2] < w[6] and o[3] > w[5]]
            lo = max([x1] + [o[1] for o in band if o[1] <= c]); hi = min([x2] + [o[0] for o in band if o[0] >= c])
            front_band = [o for o in others if o[0] < w[4] and o[1] > w[3]]
            front = (min([y2] + [o[2] for o in front_band if o[2] >= w[6]]) - w[6]) if back == "S" else (w[5] - max([y1] + [o[3] for o in front_band if o[3] <= w[5]]))
        assert c - lo >= 1.25 - 0.01 and hi - c >= 1.25 - 0.01, (rid, "WC side clearance", round(c - lo, 2), round(hi - c, 2))
        assert front >= 1.75 - 0.01, (rid, "WC front clearance", round(front, 2))
        if rid in M.SHOWERS:
            sx1, sx2, sy1, sy2 = M.SHOWERS[rid]
            _shower_matches_glass_and_walls(rid, (x1, x2, y1, y2))
            assert sx2 - sx1 >= 3 - 0.01 and sy2 - sy1 >= 3 - 0.01, (rid, "shower under 3 x 3")
            assert x1 - 0.01 <= sx1 and sx2 <= x2 + 0.01 and y1 - 0.01 <= sy1 and sy2 <= y2 + 0.01, (rid, "shower outside the walls")


def test_stair_flights_and_landing_three_feet_six_clear():
    import geom
    s = M.STAIR
    assert s["risers"] == 16 and abs(s["tread"] - 10 / 12) < 1e-9 and s["dir"] == 1
    assert 16 * 7.5 / 12 == M.LEVELS["upper_ffl"]
    f1, f2, ld, core = s["flight1"], s["flight2"], s["landing"], s["core"]
    assert f1[4] + f2[4] == 16
    for f in (f1, f2):
        assert abs((f[3] - f[2]) - (f[4] - 1) * s["tread"]) < 0.01      # 7 treads of 10 in
    with M.on_floor("G"):
        def t_at(axis, c, at):
            ws = [w for w in M.WALLS if w[0] == axis and abs(w[1] - c) < 0.01 and w[2] - 0.01 <= at <= w[3] + 0.01]
            assert ws, (axis, c, at)
            return max(geom.wall_t(w) for w in ws)
        mid = (f1[2] + f1[3]) / 2
        r06 = next(r for r in M.ROOMS if r[0] == "R06")
        east_x = min(w[1] for w in M.WALLS if w[0] == "Y" and w[1] > f2[0] and w[2] <= mid <= w[3])
        assert r06[2] == M.HX1 and r06[3] <= M.RING[0] and east_x <= M.RING[0]          # against the west wall, in the west band
        west_face = M.HX1 + t_at("Y", M.HX1, mid) / 2
        east_face = east_x - t_at("Y", east_x, mid) / 2
        north_y = next(r for r in M.ROOMS if r[0] == "R46")[5]
        north_face = north_y - t_at("X", north_y, (ld[0] + ld[1]) / 2) / 2
        assert f1[0] >= west_face - 0.01 and f1[1] - west_face >= 3.5 - 0.01           # flight 1: wall face to the core
        assert f1[1] <= core[0] + 0.01 and core[1] <= f2[0] + 0.01
        assert east_face - core[1] >= 3.5 - 0.01 and f2[1] <= east_face + 0.01        # flight 2: core to wall face
        assert north_face - max(f1[3], f2[3]) >= 3.5 - 0.01                           # half landing depth
        assert ld[1] - ld[0] >= 7.0 and ld[0] >= west_face - 0.01 and ld[1] <= east_face + 0.01
        # foot lobby: from the master's wall face to the first riser, at least as deep as the flight is wide
        lobby_s = max(w[1] for w in M.WALLS if w[0] == "X" and w[2] <= M.HX1 + 0.01 and w[1] < f1[2]) + 0.21
        assert f1[2] - lobby_s >= 3.5 - 0.01
        # the low store sits under the landing
        r46 = next(r for r in M.ROOMS if r[0] == "R46")
        assert r46[2] <= ld[0] and ld[1] <= r46[3] and abs(r46[4] - ld[2]) < 0.01
    # the arrival (top of flight 2, at its south end) faces south; the master's north wall is the line Bedroom 2's wall stacks on:
    # the suite gets 16 ft+ from the south wall to it, and the stair head between it and the top riser is 3'-6" clear
    assert f2[2] == f1[2]
    stack = ROOM("R01")[5]
    assert stack - M.HY1 >= 16.0 and f2[2] - (stack + 0.21) >= 3.5 - 0.01


def _f1_graph(doors=True):
    rooms = [(r[0], r[2], r[3], r[4], r[5]) for r in M._FLOOR_DATA["F1"]["ROOMS"]]
    return rooms, graph(rooms, M._FLOOR_DATA["F1"]["WALLS"], M._FLOOR_DATA["F1"]["DOORS"] if doors else [])


def test_upper_mass_stays_west():
    # the wing keeps to the west band, and only over the den block (north band, x <= 33.5) does it reach east (C2 ruling)
    for r in M._FLOOR_DATA["F1"]["ROOMS"]:
        if r[0] == "R37":
            continue
        assert M.HX1 <= r[2] and r[3] <= M._DE + 0.01, r[0]
        assert r[3] <= M.RING[0] + 0.01 or r[4] >= M.RING[3] - 0.01, (r[0], "east of the west band outside the north band")
    t = _room("R37")                                                      # the roof terrace over the living only
    assert tuple(t[2:6]) == (M._DE, M._OX, M.RING[3], M.HY2)
    assert tuple(t[2:6]) == tuple(_room("R16")[2:6])


def test_hotel_suite_and_stack():
    _, g = _f1_graph()
    # hotel order: the stair head, the walk-in / dressing lobby, then the bedroom one way and the bath the other
    assert g["R45"] == {"R41", "R31", "R33"}
    assert g["R31"] == {"R45"} and g["R33"] == {"R45"}                              # no door from the bedroom to the bath
    up, down = _room("R39"), _room("R07")                                           # the upper toilet sits over the den bath
    assert down[2] - 0.01 <= up[2] and up[3] <= down[3] + 0.01 and down[4] - 0.01 <= up[4] and up[5] <= down[5] + 0.01
    r = _room("R31")                                                                # the bedroom in the SW corner over the master
    assert r[2] == M.HX1 and r[4] == M.HY1 and _room("R33")[5] == _room("R01")[5]
    bed = _furn("F10")                                                              # the bath is not over the master's bed
    assert overlap(_room("R33")[2:6], bed[3:7]) == 0
    wc = _furn("F77")
    assert abs(wc[3] - _faces("R33")[0]) < 0.02 and _faces("R33")[0] < M.HX1 + 0.5  # the WC on the west outer wall


def test_upper_rooms_reachable_from_the_stair_head():
    rooms, g = _f1_graph()
    assert not {r[0] for r in rooms} - reachable(g, "R41")


def test_upper_family_room_is_one_room_of_150_sq_ft():
    import geom
    parts = M.UPPER_FAMILY_ROOM
    with M.on_floor("F1"):
        area = sum(geom.clear_dims(_room(p))[0] * geom.clear_dims(_room(p))[1] for p in parts)
    assert area >= 150, area
    _, g = _f1_graph(doors=False)
    assert parts[1] in g[parts[0]]                                                  # open to each other, no door
    have = {f[0]: f for f in M._FLOOR_DATA["F1"]["FURNITURE"] if f[1] in {_room(p)[1] for p in parts}}
    assert {"F107", "F55", "F92", "F91", "F101"} <= set(have)                       # bookshelf wall, screen, sofa-bed, desk, jharokha seat
    assert "bookshelf" in have["F107"][2].lower() and "screen" in have["F55"][2].lower() and "sofa-cum-bed" in have["F92"][2].lower()
    assert 5.0 <= _tv_gap(_furn("F55"), _furn("F92")) <= 10.0                       # viewing distance
    tv, sofa = _furn("F55"), _furn("F92")
    assert sofa[5] < tv[6] and sofa[6] > tv[5]                                       # the sofa-bed faces the screen


def test_jharokhas_over_the_walkway_roof_on_kerbs():
    assert len(M.JHAROKHAS) == 2 and len(M.JHAROKHA_FACE) == 2
    homes = []
    for (x1, x2, y1, y2, sill), face in zip(M.JHAROKHAS, M.JHAROKHA_FACE):
        assert sill == 2.0 and M.ROOF["jharokha_kerb"] == 0.5
        assert sorted((x2 - x1, y2 - y1)) == [2.0, 4.0]                             # 4 ft wide, 2 ft deep
        assert (x2 - x1 == 2.0) == (face in "EW")
        # over the walkway roof: inside the ring, off the open court, off the terrace
        assert M.RING[0] - 0.01 <= x1 and x2 <= M.RING[1] + 0.01 and M.RING[2] - 0.01 <= y1 and y2 <= M.RING[3] + 0.01
        assert overlap((x1, x2, y1, y2), M.CT) == 0 and overlap((x1, x2, y1, y2), _room("R37")[2:6]) == 0
        wall = ("Y", x1) if face == "E" else ("X", y2)                               # the wing wall it projects from
        span = (y1, y2) if face == "E" else (x1, x2)
        home = [r[0] for r in M._FLOOR_DATA["F1"]["ROOMS"] if (r[3] if wall[0] == "Y" else r[4]) == wall[1]
                and (r[4] if wall[0] == "Y" else r[2]) - 0.01 <= span[0] and span[1] <= (r[5] if wall[0] == "Y" else r[3]) + 0.01]
        assert len(home) == 1, (span, home)
        homes.append(home[0])
        seat = [f for f in M._FLOOR_DATA["F1"]["FURNITURE"] if x1 - 0.01 <= f[3] and f[4] <= x2 + 0.01 and y1 - 0.01 <= f[5] and f[6] <= y2 + 0.01]
        assert len(seat) == 1 and "2'-0\"" in seat[0][2] and "6 in" in seat[0][2] and "grab rail" in seat[0][2].lower(), seat
        assert any(w[1] == wall[0] and w[2] == wall[1] and w[3] <= span[0] + 0.01 and span[1] - 0.01 <= w[4] and w[5] == sill
                   for w in M.WINDOWS_F1), "no opening for the bay"
    assert sorted(homes) == ["R34", "R36"]                                          # the stair head's gallery and the family room


def test_jharokhas_clear_the_ring_roof_by_their_kerb_follows_the_roof():
    # FOLLOWS THE ROOF: re-run after Task C8 re-cuts ROOF (geom.ring_z); the bays' undersides must clear the walkway roof by the 6 in kerb
    import geom
    for j in M.JHAROKHAS:
        assert geom.jharokha_clearance(j) >= M.ROOF["jharokha_kerb"], (j, geom.jharokha_clearance(j))


def test_stair_well_open_over_both_flights_and_the_landing_with_guards():
    s = M.STAIR
    well = (M.HX1, M._GSE, s["flight1"][2], M.RING[3])
    for part in (s["flight1"][:4], s["flight2"][:4], s["landing"], s["core"]):
        assert well[0] <= part[0] and part[1] <= well[1] + 0.01 and well[2] - 0.01 <= part[2] and part[3] <= well[3]
    for r in M._FLOOR_DATA["F1"]["ROOMS"]:
        assert overlap(r[2:6], well) < 0.05, r[0]
    rails = M._FLOOR_DATA["F1"]["RAILS"]
    assert ("X", s["flight1"][2], M.HX1, s["core"][0]) in rails                      # over the foot of flight 1
    g = next(a for a in rails if a[0] == "Y" and a[1] == M._GSE)                     # the gallery's guard over flight 2 and the landing
    assert g[2] <= s["flight2"][2] + 0.01 and g[3] >= M.RING[3] - 0.01 and g[1] - 0.21 >= s["flight2"][1] - 0.01   # it does not narrow the 3'-6" flight
    import geom
    with M.on_floor("F1"):
        assert geom.clear_dims(_room("R41"))[1] >= 3.5 - 0.01                        # the arrival strip 3'-6" clear deep
        assert geom.clear_dims(_room("R34"))[0] >= 3.5                               # the gallery


def test_roof_terrace_rails_posts_and_furniture():
    from planlib import on_wall
    r = _room("R37")
    assert M.RAIL_H == 4.0
    rails = M._FLOOR_DATA["F1"]["RAILS"]
    x1, x2, y1, y2 = r[2:6]
    for edge in (("X", y1, x1, x2), ("Y", x2, y1, y2), ("X", y2, x1, x2)):          # south, east and north edges
        assert any(a[0] == edge[0] and a[1] == edge[1] and a[2] <= edge[2] + 0.01 and edge[3] - 0.01 <= a[3] for a in rails), edge
    assert ("X", M.HY2) in M.JALI_RAILS                                              # the north jali parapet
    assert on_wall("Y", x1, y1, y2, M._FLOOR_DATA["F1"]["WALLS"])                    # the family room's wall on its west
    corners = {(x1, y1), (x2, y1), (x1, y2), (x2, y2)}
    assert corners <= set(M.TERRACE_POSTS) and len(M.TERRACE_POSTS) == 6
    g = M._FLOOR_DATA["G"]["WALLS"]
    for px, py in M.TERRACE_POSTS:                                                   # every canopy post over a ground wall
        assert any(w[0] == "X" and abs(w[1] - py) < 0.01 and w[2] - 0.01 <= px <= w[3] + 0.01 for w in g) or \
               any(w[0] == "Y" and abs(w[1] - px) < 0.01 and w[2] - 0.01 <= py <= w[3] + 0.01 for w in g), (px, py)
    terrace = {f[0]: f for f in M._FLOOR_DATA["F1"]["FURNITURE"] if f[1] == r[1]}
    assert {"F127", "F103", "F89", "F30", "F32", "F88"} <= set(terrace)
    assert "jasmine" in terrace["F89"][2].lower() and "east" in terrace["F127"][2].lower() and "swing" in terrace["F103"][2].lower()
    assert "washing machine" in terrace["F30"][2].lower() and "sink" in terrace["F32"][2].lower() and "drying" in terrace["F88"][2].lower()
    for f in terrace.values():                                                       # nothing to climb on against a railing (the low trough apart)
        if f[9] == "glass":                                                           # overhead rails, glass
            continue
        for a in rails:
            if (a[0], a[1]) == ("Y", x1):
                continue
            line = (a[2], a[3], a[1], a[1]) if a[0] == "X" else (a[1], a[1], a[2], a[3])
            assert _gap(f[3:7], line) >= 1.5 - 0.01, (f[0], a)


def test_terrace_daybed_sees_east_over_the_verge_follows_the_roof():
    # FOLLOWS THE ROOF: the ring roof east of the terrace (over the nook and the pooja) needs a verge; over the daybed's span it stays
    # under 2'-11" above the slab so a seated person sees the sunrise over it. Re-run after Task C8.
    import geom
    d = _furn("F127")
    assert d[4] - d[3] > d[6] - d[5]                                                  # lying east-west
    ex = _room("R37")[3]
    slab = geom.terrace_slab_z()
    hs = [geom.ring_z(ex + 0.001, d[5] + k * (d[6] - d[5]) / 20) for k in range(21)]
    verge = max((z - slab + M.ROOF["jharokha_kerb"]) if z is not None else 0 for z in hs)
    assert verge <= 2 + 11 / 12, round(verge, 2)


def test_terrace_swing_has_3ft_clear_in_front_and_behind():
    s = _furn("F103")
    rail_face = M.RING[3] + 0.12
    north_face = M.HY2 - 0.17
    front, back = (s[3], s[4], s[5] - 3.0, s[5]), (s[3], s[4], s[6], s[6] + 3.0)    # it faces south and swings north-south
    assert front[2] >= rail_face - 0.01 and back[3] <= north_face + 0.01
    for z in (front, back):
        hits = [f[0] for f in M._FLOOR_DATA["F1"]["FURNITURE"] if f[0] != "F103" and f[9] != "glass" and overlap(z, f[3:7]) > 0]
        assert not hits, (z, hits)                                                   # overhead drying rails (glass) are hauled up above head height


def test_terrace_door_slides_onto_free_wall():
    from planlib import on_wall
    f1 = M._FLOOR_DATA["F1"]
    sliders = [d for d in f1["DOORS"] if d[5] == 0]
    assert {d[0] for d in sliders} == set(M.SLIDERS_F1)
    for d in sliders:
        along, face = M.SLIDERS_F1[d[0]]
        w = abs(d[4] - d[3])
        lo, hi = (max(d[3], d[4]), max(d[3], d[4]) + w) if along > 0 else (min(d[3], d[4]) - w, min(d[3], d[4]))
        assert on_wall(d[1], d[2], lo, hi, f1["WALLS"]), d[0]
        assert not [o[0] for o in f1["DOORS"] + f1["WINDOWS"] if o[0] != d[0] and o[1] == d[1] and abs(o[2] - d[2]) < 0.01 and min(o[4], hi) - max(o[3], lo) > 0.01]
        with M.on_floor("F1"):                                                          # no cross wall cuts the parking span on its face
            import geom
            for wl in f1["WALLS"]:
                if wl[0] == d[1]:
                    continue
                t = geom.wall_t(wl) / 2
                probe = d[2] + face * 0.3
                assert not (wl[1] + t > lo + 0.01 and wl[1] - t < hi - 0.01 and min(wl[2], wl[3]) <= probe <= max(wl[2], wl[3])), (d[0], wl)
        strip = (d[2], d[2] + face * 0.9)
        rect = (min(strip), max(strip), lo, hi) if d[1] == "Y" else (lo, hi, min(strip), max(strip))
        assert not [f[0] for f in f1["FURNITURE"] if f[9] != "glass" and overlap(rect, f[3:7]) > 0], d[0]


def test_upper_wet_rooms_vent_through_outer_walls():
    outer = lambda w: (w[1] == "X" and w[2] in (M.HY1, M.HY2)) or (w[1] == "Y" and w[2] == M.HX1)
    for name in ("Bedroom 2 bath", "Upper toilet"):
        assert any(w[7] == name and outer(w) for w in M.WINDOWS_F1), name


def test_upper_wing_furniture_present():
    ids = {f[0] for f in M._FLOOR_DATA["F1"]["FURNITURE"]}
    need = {"F107", "F101", "F129", "F55", "F91", "F92", "F71", "F72", "F95", "F77", "F78", "F79", "F98", "F99", "F70",
            "F152", "F153", "F103", "F127", "F89", "F30", "F32", "F88"}
    assert not need - ids, sorted(need - ids)


def test_bedroom_2_bed_head_south():
    b, r = _furn("F71"), _room("R31")
    x1, x2, y1, y2 = _faces("R31")
    assert b[1] == r[1] and abs(b[5] - y1) <= 0.1 and r[4] == M.HY1 and (b[6] - b[5]) > (b[4] - b[3])   # head on the south outer wall
    assert b[3] - x1 >= 2 - 0.01 and x2 - b[4] >= 2 - 0.01 and y2 - b[6] >= 2.5 - 0.01               # clear to the wall faces
    others = [f[3:7] for f in M._FLOOR_DATA["F1"]["FURNITURE"] if f[1] == r[1] and f[0] not in ("F71", "F72")]
    for strip in ((b[3] - 2, b[3], b[5], b[6]), (b[4], b[4] + 2, b[5], b[6]), (b[3], b[4], b[6], b[6] + 2.5)):
        assert all(overlap(strip, o) == 0 for o in others), strip
    ws = [w for w in M.WINDOWS_F1 if w[7] == "Bedroom 2" and w[1] == "X" and w[2] == M.HY1]                   # a small window either side of the bed head
    assert any(w[4] <= b[3] for w in ws) and any(w[3] >= b[4] for w in ws)


def test_upper_ids_new_and_finished():
    f1 = {r[0] for r in M._FLOOR_DATA["F1"]["ROOMS"]}
    assert f1 == {"R31", "R45", "R33", "R41", "R34", "R39", "R36", "R36A", "R37"}
    assert not f1 & {r[0] for r in M._FLOOR_DATA["G"]["ROOMS"]}, "an upstairs room reuses a ground id"
    for rid in f1:
        assert rid in M.CEILINGS and rid in M.FLOOR_FINISH, rid
    ids = [d[0] for d in M.DOORS_F1] + [w[0] for w in M.WINDOWS_F1]                  # C5 keeps off the ground's id ranges
    bad = [i for i in ids if (i[0] == "D" and (1 <= int(i[1:3]) <= 18 or 60 <= int(i[1:3]) <= 64)) or (i[0] == "W" and 60 <= int(i[1:3]) <= 88)]
    assert not bad and len(ids) == len(set(ids)), bad


# ---------- Task C6: electrical, plumbing and pipes (compact 42 x 42 ring) ----------
def _fd(fl, key):
    return M._FLOOR_DATA[fl][key]


def _rect(rid):
    for fl in ("G", "F1"):
        for r in _fd(fl, "ROOMS"):
            if r[0] == rid:
                return r[2:6]
    raise KeyError(rid)


def _pts(code, room=None):
    return [e for e in M.both("ELECTRICAL") if e[0] == code and (room is None or e[3] == room)]


def _plb(code, room=None, fl=None):
    src = M.both("PLUMBING") if fl is None else _fd(fl, "PLUMBING")
    return [p for p in src if p[0] == code and (room is None or p[3] == room)]


def test_every_code_has_a_type_and_the_group_b_codes_exist():
    assert all(e[0] in M.ELEC_TYPES for e in M.both("ELECTRICAL"))
    assert all(p[0] in M.PLUMB_TYPES for p in M.both("PLUMBING"))
    assert M.ELEC_TYPES["FL"][1] == "1'-0\"" and "PA" in M.ELEC_TYPES and "SND" in M.ELEC_TYPES
    assert all(c in M.PLUMB_TYPES for c in ("CD", "OF", "SC", "PU", "TK"))
    import sheets_mep as S
    for c in ("FL", "PA", "SND"):
        assert c in S.LIGHTING and c in S.ECOL, c


def test_every_room_has_light_and_baths_have_switches_outside():
    for fl in ("G", "F1"):
        lit = {e[3] for e in M._FLOOR_DATA[fl]["ELECTRICAL"] if e[0] in ("L", "WL")}
        rooms = {r[0] for r in M._FLOOR_DATA[fl]["ROOMS"]} - {"R50"}
        assert not rooms - lit, (fl, sorted(rooms - lit))
    assert len([p for p in M.PLUMBING if p[0] == "CD"]) == 2
    assert "CD" in M.PLUMB_TYPES and M.PLUMB_TYPES["CD"] == "Courtyard drain with first-flush filter to the sump"
    # switches OUTSIDE each bath's door: a switch in the room the door opens from, within 3 ft of the door (the upper toilet's door D39 opens from R36A)
    outside = {"R40": ("R01", "D42"), "R07": ("R42", "D07"), "R08": ("R51", "D08"), "R33": ("R45", "D33"), "R39": ("R36A", "D39")}
    doors = {d[0]: d for fl in ("G", "F1") for d in _fd(fl, "DOORS")}
    for bath, (room, did) in outside.items():
        d = doors[did]
        mid = (d[3] + d[4]) / 2
        near = [e for e in _pts("S", room) if abs((e[2] if d[1] == "Y" else e[1]) - mid) <= 3.0 and abs((e[1] if d[1] == "Y" else e[2]) - d[2]) <= 1.0]
        assert near, (bath, did)
        assert not [e for e in M.both("ELECTRICAL") if e[3] == bath and e[0] == "S"], bath      # and none inside the wet room


def test_points_sit_inside_their_room_and_clear_of_openings():
    for fl in ("G", "F1"):
        for key in ("ELECTRICAL", "PLUMBING"):
            for p in _fd(fl, key):
                code, x, y, rid = p[:4]
                if rid == "SITE" or code in ("ODU", "INV"):
                    continue
                x1, x2, y1, y2 = _rect(rid)
                assert x1 - 0.05 <= x <= x2 + 0.05 and y1 - 0.05 <= y <= y2 + 0.05, (fl, code, x, y, rid)
        for e in _fd(fl, "ELECTRICAL"):                                   # wall points are not in a door opening
            if e[0] not in ("S", "P", "PC", "AC", "TV", "D", "U", "LS", "WL", "EF", "G", "CH", "BELL"):
                continue
            for o in _fd(fl, "DOORS"):
                t_ = M.EF_OVER_DOOR
                if (e[0], e[3], o[0]) == (t_["code"], t_["rid"], t_["door"]) and abs(e[1] - t_["x"]) < 0.01:
                    continue   # the one duct terminal high over a door (checked against the lintel band and ring beam below)
                c = o[2]; along = e[1] if o[1] == "X" else e[2]; across = e[2] if o[1] == "X" else e[1]
                assert not (abs(across - c) <= 0.45 and o[3] - 0.05 <= along <= o[4] + 0.05), (fl, e[:4], o[0])


def test_fans_in_every_habitable_room():
    need = {"G": {"R01", "R42", "R16", "R16D", "R15", "R17"}, "F1": {"R31", "R36", "R37"}}
    for fl, rooms in need.items():
        have = {e[3] for e in _fd(fl, "ELECTRICAL") if e[0] == "F"}
        assert not rooms - have, (fl, sorted(rooms - have))


def test_exhaust_fans_only_through_outer_walls():
    for fl in ("G", "F1"):
        ext = _fd(fl, "EXTERIOR")
        efs = [e for e in _fd(fl, "ELECTRICAL") if e[0] == "EF"]
        for e in efs:
            near = [(a, c) for a, c in ext if abs((e[2] if a == "X" else e[1]) - c) <= 0.8]
            if near:
                continue
            # the powder room has no outer wall: its fan is ducted through the utility to a louvre terminal on the south outer wall
            assert fl == "G" and e[3] == "R08" and "duct" in e[4], e[:4]
            term = [t for t in efs if t[3] == "R13" and "terminal" in t[4] and abs(t[2] - M.HY1) <= 0.8 and ((t[1] - e[1]) ** 2 + (t[2] - e[2]) ** 2) ** 0.5 <= 15.0]
            assert term, "no terminal on the south wall for the powder room's duct"
            assert "non-return damper" in e[4] and "non-return damper" in term[0][4]
            w64 = next(w for w in _fd("G", "WINDOWS") if w[0] == "W64")
            assert min(abs(term[0][1] - w64[3]), abs(term[0][1] - w64[4])) >= 3.3 and not (w64[3] <= term[0][1] <= w64[4])   # 1 m+ from the utility window
            d18 = next(d for d in _fd("G", "DOORS") if d[0] == "D18")
            jamb = min(abs(term[0][1] - d18[3]), abs(term[0][1] - d18[4]))
            t_ = M.EF_OVER_DOOR
            over = d18[3] < term[0][1] < d18[4] and (t_["rid"], t_["door"]) == ("R13", "D18") and abs(term[0][1] - t_["x"]) < 0.01
            if over:   # between the lintel band over the door (6 in deep) and the ring beam (9 in deep under the wall top)
                assert M.LEVELS["door_head"] + 0.5 < t_["z"] - t_["cowl"] / 2 and t_["z"] + t_["cowl"] / 2 < M.LEVELS["wall_top"] - 0.75
                assert "drip lip" in term[0][4] and "away from D18" in term[0][4] and "bulkhead" in term[0][4]
            assert jamb >= 1.0 and (over or not (d18[3] <= term[0][1] <= d18[4])), jamb   # 1 ft+ clear of the service door's jambs, or high over its head
        # none of them looks onto the courtyard walkway
        court = {("X", M.RING[2]), ("X", M.RING[3]), ("Y", M.RING[0]), ("Y", M.RING[1])}
        assert not [e for e in efs if any(abs((e[2] if a == "X" else e[1]) - c) <= 0.8 and e[3] not in ("R13", "R08") for a, c in court)], fl
    ef_rooms = {e[3] for e in M.both("ELECTRICAL") if e[0] == "EF"}
    assert {"R40", "R08", "R07", "R13", "R33", "R39"} <= ef_rooms


def test_ac_and_odu_in_the_five_rooms_on_shaded_outer_walls():
    five = ["R01", "R42", "R31", "R16", "R36"]
    for rid in five:
        assert len(_pts("AC", rid)) == 1 and len(_pts("ODU", rid)) == 1, rid
        ac, odu = _pts("AC", rid)[0], _pts("ODU", rid)[0]
        x1, x2, y1, y2 = _rect(rid)
        assert x1 - 0.1 <= ac[1] <= x2 + 0.1 and y1 - 0.1 <= ac[2] <= y2 + 0.1, rid
        west = odu[1] < M.HX1 - 0.3 and M.HY1 < odu[2] < M.HY2
        south = odu[2] < M.HY1 - 0.3
        north = odu[2] > M.HY2 + 0.3 and M.HX1 < odu[1] < M.HX2
        has_w_or_s = abs(x1 - M.HX1) < 0.01 or abs(y1 - M.HY1) < 0.01
        assert (west or south) if has_w_or_s else north, (rid, odu)        # west or south where the room has such a wall, else the cool north
        assert odu[1] < M.HX2 - 10, rid                                    # never on the thinnai / east front
        assert not (M.CT[0] - 1 <= odu[1] <= M.CT[1] + 1 and M.CT[2] - 1 <= odu[2] <= M.CT[3] + 1), rid
    assert not any(e[0] in ("AC", "ODU") and e[3] not in five for e in M.both("ELECTRICAL"))
    odus = [(e[3], e[1], e[2]) for e in _fd("G", "ELECTRICAL") if e[0] == "ODU"], [(e[3], e[1], e[2]) for e in _fd("F1", "ELECTRICAL") if e[0] == "ODU"]
    for _, gx, gy in odus[0]:
        for _, fx, fy in odus[1]:
            assert ((gx - fx) ** 2 + (gy - fy) ** 2) ** 0.5 >= 2.0, (gx, gy, fx, fy)       # no unit stacked over another
    for e in M.both("ELECTRICAL"):                                   # west units wear a louvred sun-hood with 1 m clear; north units are already in the shade
        if e[0] == "ODU":
            assert e[2] > M.HY2 + 0.3 or ("hood" in e[4] and "1 m clear" in e[4]), e[:4]
    for rid, bed in (("R01", "F10"), ("R31", "F71")):                                        # never above the bed head (the head is on the south wall)
        f = _furn(bed); ac = _pts("AC", rid)[0]
        assert ac[2] >= (f[5] + f[6]) / 2, rid


def test_alarms_lamp_sockets_stair_and_garden_lights():
    assert {e[3] for e in M.both("ELECTRICAL") if e[0] == "SA"} == {"R09", "R41", "R01", "R42", "R31"}    # stair foot and head, plus the three bedrooms
    assert {e[3] for e in M.both("ELECTRICAL") if e[0] == "HA"} == {"R15"}
    for rid in ("R16", "R01", "R42", "R31", "R36"):
        assert _pts("LS", rid), rid
    assert len(_pts("FL", "R06")) >= 4 and _pts("WL", "R06")        # low stair lights on both faces of flight 1
    assert _pts("FL", "R34") and _pts("FL", "R41")                  # and at the stair head and along the well guard
    gl = [(e[1], e[2], e[3]) for e in M.both("ELECTRICAL") if e[0] == "GL"]
    assert sum(1 for *_, rid in gl if rid == "R50") >= 2           # courtyard uplights
    otta = _feature("OTTA")
    assert any(otta[0] - 2 <= x <= otta[1] + 2 and otta[2] <= y <= otta[3] for x, y, _ in gl)         # engawa
    g = _furn("F124")
    assert any(abs(x - (g[3] + g[4]) / 2) <= 2.5 and abs(y - (g[5] + g[6]) / 2) <= 2.5 for x, y, _ in gl)   # pocket garden
    assert sum(1 for *_, rid in gl if rid == "R17") >= 2           # thinnai


def test_group_b_alarms_sounders_and_footlights():
    for bath, door_wc in (("R40", "F12"), ("R07", "F48")):
        pa = _pts("PA", bath)
        assert len(pa) == 2, bath
        sx1, sx2, sy1, sy2 = M.SHOWERS[bath]
        assert sum(1 for e in pa if sx1 <= e[1] <= sx2 and sy1 <= e[2] <= sy2) == 1, bath       # one in the shower
        wc = _furn(door_wc)
        assert sum(1 for e in pa if _pt_gap((e[1], e[2]), wc[3:7]) <= 2.0) == 1, bath            # one by the WC
    assert {e[3] for e in _pts("PA")} == {"R40", "R07"}
    assert {e[3] for e in _pts("SND")} == {"R15", "R42"}                                         # sounders in the kitchen and the den
    fl = _pts("FL", "R01")
    assert len(fl) >= 3 and _pts("FL", "R40")
    d42 = next(d for d in _fd("G", "DOORS") if d[0] == "D42")
    for e in fl:                                                     # on the bed-to-bath route (bed's east side to the bath door)
        assert _dist_pt_seg((e[1], e[2]), (25.0, 6.0), (d42[2], (d42[3] + d42[4]) / 2)) <= 3.0, e[:4]
    assert not _pts("FL", "R31")


def test_db_sub_board_and_the_inverter_in_a_shielded_box_a_metre_from_every_opening():
    db = {e[3]: e for e in M.both("ELECTRICAL") if e[0] == "DB"}
    r48 = _rect("R48")
    assert r48[0] <= db["R48"][1] <= r48[1] and r48[2] <= db["R48"][2] <= r48[3]
    assert "R34" in db or "R41" in db                                # a sub-board upstairs
    inv = _pts("INV")
    assert len(inv) == 1 and "OUTSIDE" in inv[0][4] and "IP54" in inv[0][4] and "LiFePO4" in inv[0][4] and "heat-shielded" in inv[0][4]
    x, y = inv[0][1], inv[0][2]
    assert abs(y - M.HY1) <= 0.1                                      # on a south outer wall
    wstep = _feature("WSTEP")
    assert not (wstep[0] - 1 <= x <= wstep[1] + 1)                    # clear of the service landing and steps
    for o in _fd("G", "DOORS") + _fd("G", "WINDOWS"):                 # 1 m (3.3 ft) from every door and window on that wall
        if o[1] == "X" and abs(o[2] - M.HY1) < 0.01:
            assert (o[3] - x if x < o[3] else x - o[4] if x > o[4] else 0.0) >= 3.3, o[0]
    for e in _fd("G", "ELECTRICAL"):                                  # and from every fan terminal and hood duct on it
        if e[0] in ("EF", "CH") and abs(e[2] - M.HY1) <= 0.8:
            assert abs(e[1] - x) >= 3.3, e[:4]
    for d in _fd("G", "DOORS"):                                       # nowhere near a bedroom's exit
        if d[0] in ("D04", "D42", "D02", "D47", "D45", "D07"):
            c = (d[2], (d[3] + d[4]) / 2) if d[1] == "Y" else ((d[3] + d[4]) / 2, d[2])
            assert ((c[0] - x) ** 2 + (c[1] - y) ** 2) ** 0.5 >= 10.0, d[0]
    assert not [e for e in M.both("ELECTRICAL") if e[0] == "INV" and e[3] in ("R46", "R06", "R09", "R48")]


def test_geysers_out_of_the_shower_spray():
    for rid in ("R40", "R07", "R33", "R39"):
        g = _pts("G", rid)
        assert len(g) == 1, rid
        sx1, sx2, sy1, sy2 = M.SHOWERS[rid]
        dx = max(sx1 - g[0][1], 0, g[0][1] - sx2); dy = max(sy1 - g[0][2], 0, g[0][2] - sy2)
        assert (dx * dx + dy * dy) ** 0.5 >= 2.5, (rid, g[0][1:3])


def test_every_fixture_has_a_point():
    want = {"R40": "WC HF BS SH FT GY", "R07": "WC HF BS SH FT GY", "R08": "WC HF BS", "R13": "SK WM FT TAP", "R15": "SK RO", "R16D": "BS",
            "R33": "WC HF BS SH FT GY", "R39": "WC HF BS SH FT GY", "R37": "WM SK FT TAP TK TK"}
    for rid, codes in want.items():
        have = sorted(p[0] for p in M.both("PLUMBING") if p[3] == rid and not (p[0] == "IC" and p[4].startswith("RE-")))
        assert have == sorted(codes.split()), (rid, have)
    assert {p[0] for p in M.both("PLUMBING") if p[3] == "SITE"} >= {"DP", "TAP", "IC", "GT", "PU"}


def _pipe_graph(kind):
    lines = [p[1] for p in M.PIPES if p[0] == kind]
    def on(pt, line, tol=0.06):
        for a, b in zip(line, line[1:]):
            (x1, y1), (x2, y2) = a, b
            if min(x1, x2) - tol <= pt[0] <= max(x1, x2) + tol and min(y1, y2) - tol <= pt[1] <= max(y1, y2) + tol:
                if abs((x2 - x1) * (pt[1] - y1) - (y2 - y1) * (pt[0] - x1)) <= tol * max(abs(x2 - x1) + abs(y2 - y1), 1e-9):
                    return True
        return False
    n = len(lines); parent = list(range(n))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(n):
        for j in range(n):
            if i != j and any(on(pt, lines[j]) for pt in (lines[i][0], lines[i][-1])):
                parent[find(i)] = find(j)
    return lines, find, on


def _reaches(kind, start, target_rect=None, target_pt=None, tol=0.06):
    lines, find, on = _pipe_graph(kind)
    src = [i for i, l in enumerate(lines) if on(start, l)]
    assert src, ("no pipe at", kind, start)
    def hits(line):
        for q in line:
            if target_pt is not None and abs(q[0] - target_pt[0]) <= tol and abs(q[1] - target_pt[1]) <= tol:
                return True
            if target_rect is not None and target_rect[0] - tol <= q[0] <= target_rect[1] + tol and target_rect[2] - tol <= q[1] <= target_rect[3] + tol:
                return True
        return False
    roots = {find(i) for i in src}
    return any(hits(l) for i, l in enumerate(lines) if find(i) in roots)


def _feature(fid):
    g = next(f[3] for f in M.SITE_FEATURES if f[0] == fid)
    return g if len(g) == 4 else (g[0] - g[2], g[0] + g[2], g[1] - g[2], g[1] + g[2])


def _ics(kind):
    """Inspection chambers whose note reads 'IC-n <kind>:' (soil, grey, kitchen, effluent)."""
    return [p for p in M.PLUMBING if p[0] == "IC" and re.match(r"IC-\d+ " + kind, p[4])]


def _ric():
    return [p for p in M.PLUMBING if p[0] == "IC" and (p[4].startswith("RIC-") or p[4].startswith("FF"))]


def _plen(line):
    return sum(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for a, b in zip(line, line[1:]))


def _dist_pt_seg(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = dx * dx + dy * dy
    u = 0.0 if n == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / n))
    return ((p[0] - a[0] - u * dx) ** 2 + (p[1] - a[1] - u * dy) ** 2) ** 0.5


def _seg_len_inside(a, b, rect, n=400):
    x1, x2, y1, y2 = rect
    L = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
    k = sum(1 for i in range(n) if x1 <= a[0] + (b[0] - a[0]) * (i + .5) / n <= x2 and y1 <= a[1] + (b[1] - a[1]) * (i + .5) / n <= y2)
    return L * k / n


def test_courtyard_has_two_drains_an_independent_overflow_and_a_scupper_above_the_walkway():
    cds = [p for p in M.PLUMBING if p[0] == "CD"]
    assert len(cds) == 2
    se = next(p for p in cds if p[1] > M.CX and p[2] < M.CY)          # diagonal corners
    nw = next(p for p in cds if p[1] < M.CX and p[2] > M.CY)
    assert abs(se[1] - (M.CT[1] - 1.5)) <= 1.0 and abs(se[2] - (M.CT[2] + 1.5)) <= 1.0
    assert abs(nw[1] - (M.CT[0] + 1.5)) <= 1.0 and abs(nw[2] - (M.CT[3] - 1.5)) <= 1.0
    of = next(p for p in M.PLUMBING if p[0] == "OF")
    assert ((of[1] - nw[1]) ** 2 + (of[2] - nw[2]) ** 2) ** 0.5 <= 2.0
    sc = next(p for p in M.PLUMBING if p[0] == "SC")
    assert sc[3] == "R62" and abs(sc[1] - M.CT[0]) <= 0.5 and M.CT[2] < sc[2] < M.CT[3]       # through the west walkway kerb
    lvl = lambda p: float(re.search(r"([\d.]+) in above the court floor", p[4]).group(1))
    walkway = (M.LEVELS["walkway"] - M.LEVELS["courtyard"]) * 12          # the walkway floor stands about 5 in above the court floor
    assert 4.5 < walkway < 5.5
    assert lvl(of) < walkway < lvl(sc)                                     # the standpipe is below the walkway level, the scupper above it
    sump = _feature("SUMP")
    gully = next(p for p in M.PLUMBING if p[0] == "FT" and p[3] == "R62")
    cd_trunk = next(l for k, l in M.PIPES if k == "rain" and l[0] == (se[1], se[2]))
    over = next(l for k, l in M.PIPES if k == "rain" and l[0] == (33.4, 28.5))
    # hydraulic independence: the overflow line shares no point and no touching with the CD trunk, and leaves by the west rain lane
    _, find, on = _pipe_graph("rain")
    assert not any(on(q, cd_trunk, 0.3) for q in over) and not any(on(q, over, 0.3) for q in cd_trunk)
    assert over[-1][0] < M.HX1 - 5 and all(q[0] < M.CX for q in over)
    for p in (nw, of, gully):                                              # CD-2, the standpipe and the gully all reach the sump by that line
        assert _reaches("rain", (p[1], p[2]), sump), p
    assert _reaches("rain", (se[1], se[2]), sump)
    # unjointed lengths of 6 m (19.7 ft) at most between access points, and an RE at the court wall
    access = sorted(p[1] for p in M.PLUMBING if p[0] == "IC" and p[2] == 28.5 and (p[4].startswith(("RE-", "RIC-11", "RIC-12"))))
    assert any(0 < M.CT[0] - a <= 1.0 for a in access) and len(access) >= 3          # one at the court wall
    pts = [over[0][0]] + sorted(access, reverse=True) + [over[-1][0]]
    assert all(a - b <= 19.7 for a, b in zip(pts, pts[1:])), pts
    re1 = [p for p in M.PLUMBING if p[0] == "IC" and p[4].startswith("RE-1 ")]
    assert re1 and "sleeved" in re1[0][4] and re1[0][3] == "R61"


def test_every_wc_reaches_the_septic_tank_through_inspection_chambers():
    septic = _feature("SEPTIC")
    wcs = [p for p in M.both("PLUMBING") if p[0] == "WC"]
    assert {p[3] for p in wcs} == {"R08", "R40", "R07", "R33", "R39"}
    for p in wcs:
        assert _reaches("soil", (p[1], p[2]), septic), p[3]
    soil_ics = _ics("soil")
    assert len(soil_ics) >= 12 and all(_reaches("soil", (p[1], p[2]), septic) for p in soil_ics)
    # Bedroom 2's WC goes straight out through the west wall into a boxed duct; the upper toilet drops behind the den bath's WC (same wet wall)
    r33 = next(p for p in M.PLUMBING_F1 if p[0] == "WC" and p[3] == "R33")
    duct = next(l for k, l in M.PIPES if k == "soil" and abs(l[0][0] - r33[1]) < 0.05 and abs(l[0][1] - r33[2]) < 0.05)
    assert duct[1][0] < M.HX1 - 0.3 and duct[1][1] == duct[0][1]
    r39 = next(p for p in M.PLUMBING_F1 if p[0] == "WC" and p[3] == "R39")
    r07 = next(p for p in M.PLUMBING if p[0] == "WC" and p[3] == "R07")
    assert abs(r39[1] - r07[1]) <= 4.5 and abs(r39[2] - r07[2]) <= 0.5        # R39 stands over R07
    stack = next(l for k, l in M.PIPES if k == "soil" and l[0] == (r39[1], r39[2]))
    assert len(stack) == 2 and stack[1][0] == stack[0][0] and stack[1][1] > M.HY2 + 0.5     # its own straight stack, out through the north wall, no horizontal run in the slab
    assert "no horizontal run" in r39[4] and _rect("R07")[0] <= stack[0][0] <= _rect("R07")[1]
    # an access point (rodding eye) at the head of every WC's soil line, within 3 ft of the pan, on the line
    for p in M.both("PLUMBING"):
        if p[0] == "WC":
            res = [q for q in M.both("PLUMBING") if q[0] == "IC" and q[3] == p[3] and q[4].startswith("RE-") and ((q[1] - p[1]) ** 2 + (q[2] - p[2]) ** 2) ** 0.5 <= 3.0]
            assert res, p[3]
            line = next(l for k, l in M.PIPES if k == "soil" and l[0] == (p[1], p[2]))
            assert any(_dist_pt_seg((q[1], q[2]), a, b) <= 0.3 for q in res for a, b in zip(line, line[1:])), p[3]


def test_grey_kitchen_grey_and_effluent_routes_stay_separate():
    soak, banana = _feature("SOAK"), _feature("BANANA")
    for rid, code in (("R40", "FT"), ("R40", "BS"), ("R07", "FT"), ("R07", "BS"), ("R08", "BS"), ("R13", "WM"), ("R13", "FT"), ("R33", "FT"), ("R33", "BS"), ("R39", "FT"), ("R37", "WM"), ("R37", "SK")):
        p = next(q for q in M.both("PLUMBING") if q[3] == rid and q[0] == code)
        assert _reaches("grey", (p[1], p[2]), soak), (rid, code)
    gt = next(p for p in M.PLUMBING if p[0] == "GT")
    for rid, code in (("R15", "SK"), ("R13", "SK"), ("R16D", "BS")):
        p = next(q for q in M.PLUMBING if q[3] == rid and q[0] == code)
        assert _reaches("grey", (p[1], p[2]), banana), (rid, code)
        assert _reaches("grey", (p[1], p[2]), target_pt=(gt[1], gt[2])), (rid, code, "grease trap")
        assert not _reaches("grey", (p[1], p[2]), soak), (rid, code, "kitchen water never reaches the soak pit")
    assert not _reaches("grey", (gt[1], gt[2]), soak)
    # the kitchen line stays 1 ft+ from the pit's lining (a 1.2 ft gap: the 3.6 ft south strip has no room for more; the line is sleeved there)
    cx, cy, r = _circle("SOAK")
    for k, line in M.PIPES:
        if k == "grey" and any(q == (52.1, 1.2) for q in line[:1]) and line[-1] == (86.5, 1.2):
            for a, b in zip(line, line[1:]):
                assert _dist_pt_seg((cx, cy), a, b) - r >= 1.0, (a, b)


def _circle(fid):
    return next(f[3] for f in M.SITE_FEATURES if f[0] == fid)


def test_septic_outlet_opposite_the_inlet_effluent_reaches_the_soak_pit():
    septic, soak, hedge = _feature("SEPTIC"), _feature("SOAK"), _feature("HEDGE1")
    inlet = next(l[-1] for k, l in M.PIPES if k == "soil" and l[-1][0] == septic[0])
    outlet = next(l[0] for k, l in M.PIPES if k == "grey" and l[0][0] == septic[1] and septic[2] <= l[0][1] <= septic[3])
    assert inlet[0] == septic[0] and outlet[0] == septic[1] and abs(inlet[1] - outlet[1]) <= 0.5     # west face in, east face out, on one line
    assert _reaches("grey", outlet, soak)
    eff = _ics("effluent")
    assert len(eff) == 3 and all(_reaches("grey", (p[1], p[2]), soak) for p in eff)
    for p in M.PLUMBING:
        if p[0] == "IC":
            assert not (hedge[0] <= p[1] <= hedge[1] and hedge[2] <= p[2] <= hedge[3]), p
    gt = next(p for p in M.PLUMBING if p[0] == "GT")
    assert not _reaches("grey", (gt[1], gt[2]), target_pt=outlet)
    # effluent never meets the banana line: they share no point
    banana_line = next(l for k, l in M.PIPES if k == "grey" and l[-1] == (86.5, 1.2) and l[0] == (52.1, 1.2))
    eff_line = next(l for k, l in M.PIPES if k == "grey" and l[0] == outlet)
    for p in eff_line:
        assert not any(_dist_pt_seg(p, c, d) < 0.06 for c, d in zip(banana_line, banana_line[1:]))


def test_rain_all_downpipes_and_both_drains_pass_the_first_flush_chamber_to_the_sump_with_an_overflow():
    sump, recharge = _feature("SUMP"), _feature("RECHARGE")
    dps = [p for p in M.PLUMBING if p[0] == "DP"]
    assert len(dps) >= len(M.ROOF["downpipes"]) + 2
    for x, y in M.ROOF["downpipes"]:                                  # every roof downpipe has its point and its run
        assert any((p[1], p[2]) == (x, y) for p in dps), (x, y)
    for p in dps:
        assert _reaches("rain", (p[1], p[2]), sump), p
    # the terrace outlet feeds the terrace downpipe
    o = M.ROOF["terrace_outlet"]
    ft = next(p for p in M.PLUMBING_F1 if p[0] == "FT" and p[3] == "R37")
    assert (ft[1], ft[2]) == o and _reaches("rain", o, sump)
    ff = next(p for p in M.PLUMBING if p[0] == "IC" and p[4].startswith("FF"))
    # the only rain line that enters the sump starts at the first-flush chamber
    into = [l for k, l in M.PIPES if k == "rain" and any(sump[0] - .05 <= q[0] <= sump[1] + .05 and sump[2] <= q[1] <= sump[3] and q != (72.0, 44.6) for q in l)]
    assert len(into) == 1 and into[0][0] == (ff[1], ff[2])
    assert _reaches("rain", (sump[1], sump[2] + 0.1), recharge)       # overflow from the sump's east face to the recharge pit
    assert len(_ric()) >= 8


def test_supply_runs_from_the_pump_to_the_tank_riser_on_a_shaded_platform():
    sump = _feature("SUMP")
    riser = (35.5, 47.2)
    assert _reaches("supply", (sump[0], 47.2), target_pt=riser)
    tk = next(p for p in M.PLUMBING_F1 if p[0] == "TK")
    t = M.ROOF["terrace"]
    assert tk[3] == "R37" and t[0] <= tk[1] <= t[1] and t[2] <= tk[2] <= t[3]
    assert "steel stand" in tk[4] and "canopy" in tk[4] and "shade" in tk[4]       # on a shaded steel platform on the terrace, not in a roof void
    assert abs(tk[1] - riser[0]) <= 1.0 and riser[1] > M.HY2 + 0.5                  # the riser duct stands beside it, outside the north wall
    assert any(p[0] == "PU" for p in M.PLUMBING)
    # supply is 3 ft+ from every parallel soil / grey / effluent line
    for k, sl in M.PIPES:
        if k != "supply":
            continue
        for a, b in zip(sl, sl[1:]):
            for k2, ol in M.PIPES:
                if k2 not in ("soil", "grey"):
                    continue
                for c, d in zip(ol, ol[1:]):
                    if a[0] == b[0] and c[0] == d[0] and max(min(a[1], b[1]), min(c[1], d[1])) < min(max(a[1], b[1]), max(c[1], d[1])):
                        assert abs(a[0] - c[0]) >= 3.0 - 1e-6, (a, b, c, d)
                    if a[1] == b[1] and c[1] == d[1] and max(min(a[0], b[0]), min(c[0], d[0])) < min(max(a[0], b[0]), max(c[0], d[0])):
                        assert abs(a[1] - c[1]) >= 3.0 - 1e-6, (a, b, c, d)


def test_south_strip_chambers_are_two_feet_apart_and_the_trench_is_flagged_for_the_engineer():
    ch = [p for p in M.PLUMBING if p[3] == "SITE" and p[0] in ("IC", "GT")]
    for i, a in enumerate(ch):
        for b in ch[i + 1:]:
            assert ((a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5 >= 2.0 - 1e-6, (a[4][:12], b[4][:12])      # no two chambers (the grease trap included) within 2 ft
    ic18 = next(p for p in ch if p[4].startswith("IC-18 "))
    assert "concrete-encased" in ic18[4] and "structural engineer" in ic18[4]
    assert any("0.5 to 0.9 m" in p[4] and "LPG" in p[4] for p in ch)     # closed pipes pass the cage, sleeved


def _my_crossings():
    cls = M.pipe_class
    segs = [(cls(k, l), a, b) for k, l in M.PIPES for a, b in zip(l, l[1:])]
    pts = []
    for i, (c1, a, b) in enumerate(segs):
        for c2, c, d in segs[i + 1:]:
            if c1 == c2:
                continue
            # axis-aligned pipes only: one vertical, one horizontal
            for (p, q, r, t) in ((a, b, c, d), (c, d, a, b)):
                if p[0] == q[0] and r[1] == t[1] and min(r[0], t[0]) + 0.06 < p[0] < max(r[0], t[0]) - 0.06 and min(p[1], q[1]) + 0.06 < r[1] < max(p[1], q[1]) - 0.06:
                    pts.append((p[0], r[1], c1, c2))
    return pts


def test_every_pipe_crossing_is_listed_with_the_deeper_pipe_below_and_soil_lowest():
    mine = _my_crossings()
    assert len(M.PIPE_CROSSINGS) >= 20
    for x, y, c1, c2 in mine:                                          # each geometric crossing appears in the list
        lo, up = sorted((c1, c2), key=lambda c: M._CLASS_RANK[c])
        assert any(abs(x - e[0]) < 0.4 and abs(y - e[1]) < 0.4 and e[2] == lo and e[3] == up for e in M.PIPE_CROSSINGS), (x, y, c1, c2)
    for x, y, lo, up, note in M.PIPE_CROSSINGS:
        assert M._CLASS_RANK[lo] < M._CLASS_RANK[up] and "150 mm" in note
        if "soil" in (lo, up):
            assert lo == "soil", (x, y)                                # soil is the lowest at every crossing it is in
    # the utility's two wastes (sink and washer) join east of the powder room's soil stack and cross it once, inside the utility
    pw = [c for c in M.PIPE_CROSSINGS if c[2] == "soil" and abs(c[0] - 38.4) < 0.05 and M.HY1 < c[1] < M.RING[2]]
    assert len(pw) == 1 and pw[0][3] == "bath grey", pw
    washer = next(l for k, l in M.PIPES if k == "grey" and l[0] == (39.5, 7.5))
    assert washer[-1] == (39.1, 6.4) and all(x > 38.4 for x, _ in washer)


def test_big_rain_runs_are_150_mm():
    assert M.PIPE_MM
    for (kind, start), mm in M.PIPE_MM.items():
        assert mm == 150 and any(k == kind and l[0] == start for k, l in M.PIPES), start
    assert ("rain", (39.5, 48.6)) in M.PIPE_MM and ("rain", (72.0, 44.6)) in M.PIPE_MM       # RIC-8 to FF, and the sump overflow
    n = next(l for k, l in M.PIPES if k == "rain" and l[0] == (39.5, 48.6))
    assert n[-1] == (64.5, 45.2)


def test_recharge_rodding_eyes_stay_off_the_workshop_verandah_and_the_dining_eye_is_flush():
    ver = _feature("WVERANDAH")
    over = next(l for k, l in M.PIPES if k == "rain" and l[0] == (72.0, 44.6))
    assert over[-1][1] == 14.5
    for p in M.PLUMBING:
        if p[0] == "IC" and p[3] == "SITE" and abs(p[2] - 14.5) < 0.05 and p[1] > 90:
            assert not (ver[0] <= p[1] <= ver[1] and ver[2] <= p[2] <= ver[3]), p
    xs = sorted(p[1] for p in M.PLUMBING if p[0] == "IC" and abs(p[2] - 14.5) < 0.05 and p[1] > 90)
    assert xs[0] == 92.0 and 109.0 < xs[-1] < 110.5                                  # an access point at each end of the verandah, none under it
    red = next(p for p in M.PLUMBING if p[0] == "IC" and p[4].startswith("RE-D"))
    assert red[3] == "R16D" and "flush" in red[4] and abs(red[2] - 15.5) <= 0.5 and abs(red[1] - 52.1) < 0.05


def test_tank_is_two_interconnected_500_litre_tanks_with_an_overflow_and_its_own_riser():
    tks = [p for p in M.PLUMBING_F1 if p[0] == "TK"]
    assert len(tks) == 2 and all("500 L" in p[4] for p in tks) and "1,000 L" in tks[0][4] and "interconnected" in tks[0][4]
    t = M.ROOF["terrace"]
    assert all(t[0] <= p[1] <= t[1] and t[2] <= p[2] <= t[3] for p in tks)
    o = M.ROOF["terrace_outlet"]
    ov = next(l for k, l in M.PIPES if k == "rain" and l[-1][0] == o[0] and abs(l[0][1] - l[-1][1]) < 0.01 and l[0][0] == max(p[1] for p in tks))
    assert _reaches("rain", ov[0], _feature("SUMP"))                    # overflow and washout reach the sump through the terrace outlet
    riser = next(l[-1] for k, l in M.PIPES if k == "supply")
    grey = next(l for k, l in M.PIPES if k == "grey" and l[0] == (36.9, 42.4))                       # the laundry grey duct
    duct_x = grey[1][0]
    assert abs(riser[0] - duct_x) >= 0.5                                # the supply has its own duct, 0.5 ft+ from the laundry grey



def test_soil_is_outside_the_house_except_short_wc_stubs():
    house = (M.HX1 - 0.375, M.HX2 + 0.375, M.HY1 - 0.375, M.HY2 + 0.375)
    wcs = {(p[1], p[2]): p for p in M.both("PLUMBING") if p[0] == "WC"}
    for p in M.PLUMBING:                                              # no inspection chamber inside the house footprint
        if p[0] == "IC" and p[3] == "SITE":
            assert not (house[0] < p[1] < house[1] and house[2] < p[2] < house[3]), p
    for k, line in M.PIPES:
        if k != "soil":
            continue
        inside = sum(_seg_len_inside(a, b, house) for a, b in zip(line, line[1:]))
        if inside < 0.01:
            continue
        wx, wy = line[0]
        assert (wx, wy) in wcs, line[0]
        wc = wcs[(wx, wy)]
        nearest = min(wx - M.HX1, M.HX2 - wx, wy - M.HY1, M.HY2 - wy)
        if wc[3] == "R39":
            assert inside <= 5.0                                      # the upper toilet's run to the stack behind the den bath's WC
        elif "no joints under the slab" in wc[4]:
            assert inside <= 12.5 and inside <= nearest + 1.5, (wc[3], inside)   # master 11.6 ft, powder 8.3 ft: one unjointed length each
        else:
            assert inside <= nearest + 1.5 and inside <= 6.0, (wc[3], inside)


def test_soil_inspection_chambers_every_40_ft_and_lanes_clear_of_the_soak_pit():
    soil = [l for k, l in M.PIPES if k == "soil"]
    ics = [(p[1], p[2]) for p in _ics("soil")]
    def pos(line, pt):
        d = 0.0
        for a, b in zip(line, line[1:]):
            if min(a[0], b[0]) - .05 <= pt[0] <= max(a[0], b[0]) + .05 and min(a[1], b[1]) - .05 <= pt[1] <= max(a[1], b[1]) + .05:
                return d + ((pt[0] - a[0]) ** 2 + (pt[1] - a[1]) ** 2) ** 0.5
            d += ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        return None
    for line in soil:
        ps = sorted(q for q in (pos(line, pt) for pt in ics) if q is not None)
        marks = ps + [_plen(line)]
        assert all(b - a <= 40.5 for a, b in zip(marks, marks[1:])), (line[0], marks)
    # every bend of the long soil lane has a chamber
    lane = next(l for l in soil if l[-1] == (83.0, 18.6))
    for q in lane[1:-1]:
        if abs(q[0] - 14.2) < 0.01:
            continue                                                  # the boxed duct's own corner
        assert any(abs(q[0] - i[0]) < 0.05 and abs(q[1] - i[1]) < 0.05 for i in ics), q
    cx, cy, r = _circle("SOAK")
    for l in soil:
        for p, q in zip(l, l[1:]):
            assert _dist_pt_seg((cx, cy), p, q) - r >= 1.9, (p, q)    # the soil lane clears the pit by about 2 ft


def test_west_mains_stay_clear_of_the_engawa_deck_and_the_airer():
    deck = _feature("OTTA"); gstep = _feature("GSTEP"); airer = _furn("F31")
    for k, line in M.PIPES:
        for a, b in zip(line, line[1:]):
            if a[0] == b[0] and a[0] < M.HX1 - 1 and abs(a[1] - b[1]) > 12 and k in ("soil", "grey", "rain"):
                lo, hi = sorted((a[1], b[1]))
                if lo < deck[3] and hi > deck[2]:
                    assert a[0] < deck[0] - 0.9, (k, a)                # a main beside the deck stays west of it
                if lo < airer[6] and hi > airer[5]:
                    assert not (airer[3] - 0.5 <= a[0] <= airer[4] + 0.5), (k, a)
    for k, line in M.PIPES:                                            # only short grey branches cross under the deck
        for a, b in zip(line, line[1:]):
            if a[1] == b[1] and min(a[0], b[0]) < deck[0] and max(a[0], b[0]) > deck[1] and deck[2] <= a[1] <= deck[3]:
                assert k == "grey" and abs(a[1] - 42.8) < .01, (k, a)
            if a[1] == b[1] and min(a[0], b[0]) < gstep[0] and max(a[0], b[0]) > gstep[1] and gstep[2] <= a[1] <= gstep[3]:
                raise AssertionError((k, a))


def test_every_pipe_is_3ft_from_every_tree_trunk():
    bx, by = next(f[3] for f in M.SITE_FEATURES if f[0] == "BANANA")[:2]
    trees = [(x, y) for x, y, r in M.TREES] + [(x, y) for x, y, r, k in M.FOOD_TREES if ((x - bx) ** 2 + (y - by) ** 2) ** 0.5 > 3.0]   # the banana ring is what the kitchen line feeds
    for k, line in M.PIPES:
        for a, b in zip(line, line[1:]):
            for t in trees:
                assert _dist_pt_seg(t, a, b) >= 3.0 - 1e-6, (k, a, b, t)


def test_pipes_and_chambers_stay_inside_the_plot_and_off_the_ramp_landing_and_steps():
    for k, line in M.PIPES:
        for q in line:
            assert 0.5 <= q[0] <= 130 and 0.5 <= q[1] <= 49.5, (k, q)
    steps = _feature("STEPS")
    for p in M.PLUMBING:
        if p[3] == "SITE" and p[0] in ("IC", "GT"):
            assert not (steps[0] - 0.3 <= p[1] <= steps[1] + 0.3 and steps[2] - 0.3 <= p[2] <= steps[3] + 0.3), p


def test_words_mention_the_courtyard_and_no_duplex_rooms():
    import guide, make_xlsx  # noqa: F401  (import must not fail)
    text = " ".join(map(str, M.FINISHES)) + " ".join(M.DECISIONS[:5])
    assert "courtyard" in text.lower() and "thinnai" in text.lower()
    assert "poomukham" not in " ".join(map(str, M.FINISHES)).lower()


def test_no_duplex_terms_and_phasing_shape():
    banned = ("poomukham", "mukhappu", "chaipu", "kitchen wing", "covered terrace", "east balcony", "27 ft", "27' ")  # "27'-5\"" is a real room length, so only a bare 27' counts
    def flat(x):
        if isinstance(x, (list, tuple)):
            for i in x:
                yield from flat(i)
        else:
            yield str(x)
    for name in ("FINISHES", "SPEC", "OPEN_ISSUES", "PHASES", "PHASE1_PROVISIONS", "PHASE1_LIVING", "HOLD_POINTS", "DECISIONS"):
        for s in flat(getattr(M, name)):
            low = s.lower()
            for b in banned:
                assert b not in low or "in place of" in low, (name, b, s[:80])
    assert all(d.startswith("Carried over from the duplex: ") for d in M.DUPLEX_DECISIONS_CARRIED)
    assert len(M.PHASES) == 3


def _prose(names=("FINISHES", "SPEC", "OPEN_ISSUES", "PHASES", "PHASE1_PROVISIONS", "PHASE1_LIVING", "HOLD_POINTS", "DECISIONS")):
    def flat(x):
        if isinstance(x, (list, tuple)):
            for i in x:
                yield from flat(i)
        else:
            yield str(x)
    return [s for n in names for s in flat(getattr(M, n))]


def test_prose_quotes_the_drawn_numbers():
    import geom as G
    assert not any("{" in s for s in _prose()), "an unfilled {placeholder} in the prose"
    roof = next(d for d in M.COURTYARD_DECISIONS if d.startswith("Roof ("))
    for z in (G.eave_z(), G.ridge_z(), G.wing_eave_z(), G.wing_ridge_z(), G.terrace_slab_z()):
        assert G.fmt_lvl(z) in roof, G.fmt_lvl(z)
    assert f"{len(M.ROOF['downpipes'])} downpipes" in roof
    # the areas quoted are the drawn ones: the ring less the walkway and court, and the wing's L (stair well included)
    ar = G.floor_areas()
    side = M.RING[1] - M.RING[0]
    assert abs(ar["ground"] - ((M.HX2 - M.HX1) * (M.HY2 - M.HY1) - side * side)) < 1e-6
    assert abs(ar["upper"] - sum((w[1] - w[0]) * (w[3] - w[2]) for w in M.ROOF["wing_walls"])
               + (M.ROOF["wing_walls"][0][1] - M.ROOF["wing_walls"][1][0]) * (M.ROOF["wing_walls"][1][3] - M.ROOF["wing_walls"][1][2])) < 1e-6
    size = next(d for d in M.COURTYARD_DECISIONS if d.startswith("Compact house"))
    assert f"{ar['enclosed']:,.0f} sq ft enclosed" in size and "42 x 42 ft" in size and "50 x 130 ft" in size
    with M.on_floor("F1"):
        b2 = G.clear_dims(next(r for r in M.ROOMS if r[0] == "R31"))
    assert f"Bedroom 2 {G.fmt_ft(b2[0])} x {G.fmt_ft(b2[1])}" in " ".join(M.COURTYARD_DECISIONS)


def test_no_placeholder_or_stray_brace_anywhere_in_the_model_after_geom():
    import geom  # noqa: F401
    import re
    assert M.PROSE_FILLED
    key = re.compile(r"\{(clear|size):R\w+\}|\{\w+\}")
    seen = set()
    def walk(x, path):
        if isinstance(x, str):
            assert not key.search(x) and "{" not in x and "}" not in x, (path, x[:90])
        elif isinstance(x, (list, tuple, set, frozenset)):
            if id(x) in seen:
                return
            seen.add(id(x))
            for v in x:
                walk(v, path)
        elif isinstance(x, dict):
            if id(x) in seen:
                return
            seen.add(id(x))
            for k, v in x.items():
                walk(k, path); walk(v, path)
    for name, v in vars(M).items():
        if not name.startswith("__"):
            walk(v, name)


def test_writers_see_the_filled_prose():
    import make_guide, make_xlsx  # noqa: F401
    assert M.PROSE_FILLED
    assert "{" not in " ".join(_prose())


def test_spec_quotes_the_drawn_roof_levels_and_areas():
    import pathlib
    import geom as G
    spec = (pathlib.Path(__file__).resolve().parents[2] / "01_Brief" / "Courtyard_Concept_Spec.md").read_text(encoding="utf-8")
    n = G.prose_numbers()
    for k in ("ring_eave", "ring_ridge", "wing_eave", "wing_ridge", "terrace_slab", "family_floor", "canopy", "thinnai_eave", "thinnai_clear",
              "jharokha_under", "corner_guard", "upstand", "ground_area", "walkway_area", "court_area", "thinnai_area", "upper_area",
              "terrace_area", "enclosed_area"):
        assert n[k] in spec, (k, n[k])
    assert f"{n['downpipes']} downpipes" in spec and n["court_drop"] in spec


def test_south_downpipes_quoted_from_the_roof_data():
    import geom  # noqa: F401  (fills the prose)
    sxs = sorted(x for x, y in M.ROOF["downpipes"] if y < M.HY1)
    gut = next(r for r in M.SPEC if r[1] == "Gutters and downpipes")[2]
    dev = next(o for o in M.OPEN_ISSUES if o[0] == "Owner review")[1]
    for t in (gut, dev):
        assert " and ".join(f"x {x:g}" for x in sxs) in t and "200 mm" in t and "south-east corner" not in t
    assert "upsized" not in dev and "upgrade" not in dev


def test_decisions_record_the_compact_house_and_the_owner_choices():
    import geom  # noqa: F401  (fills the prose)
    text = " ".join(M.DECISIONS)
    for head in ("Compact house on a 50 x 130 ft plot", "A tight ring", "Merged rooms", "Compact ground floor approved",
                 "Compact first floor approved", "Elderly parent and access, Group B", "Tulsi in the courtyard", "Thinnai",
                 "Both swings kept", "Vastu placements", "Carried over from the duplex: hotel-style Bedroom 2 suite",
                 "Carried over from the duplex: bathrooms planned round the door"):
        assert any(d.startswith(head) for d in M.DECISIONS), head
    merged = next(d for d in M.DECISIONS if d.startswith("Merged rooms"))
    for w in ("foyer", "console nook", "one L-shaped family room", "one upstairs family room"):
        assert w in merged, w
    group_b = next(d for d in M.DECISIONS if d.startswith("Elderly parent"))
    for w in ("grab rails", "fold-down shower seats", "pull-cord alarms", "footlights", "2'-8\"", "both sides", "1:12 ramp", "16 in", "reading chair", "2'-0\""):
        assert w in group_b, w
    assert "red oxide" in text and "turned teak pillars" in text
    terrace = next(d for d in M.DECISIONS if d.startswith("Roof terrace ("))
    assert "canopy" not in terrace and "guard wall" not in terrace and "tanks" not in terrace
    designer = next(d for d in M.DECISIONS if d.startswith("Terrace canopy, guard wall and tanks"))
    assert "owner" not in designer.split(":")[0]
    inv = next(d for d in M.DECISIONS if d.startswith("Inverter"))
    assert "outside the south outer wall" in inv and "utility" in inv


def test_open_issues_hold_the_unapproved_reviews_and_the_owner_and_vastu_items():
    import geom as G
    cats = [o[0] for o in M.OPEN_ISSUES]
    for g in ("Review A: safety", "Review C: comfort", "Review D: site"):
        assert g in cats, g
    assert all(o[3] == "Not approved" for o in M.OPEN_ISSUES if o[0].startswith("Review "))
    step = next(o for o in M.OPEN_ISSUES if "D49" in o[1])
    assert G.fmt_lvl(G.terrace_slab_z()) in step[1] and G.fmt_lvl(G.floor_level("R36")) in step[1] and step[3] == "Owner to decide"
    dev = next(o for o in M.OPEN_ISSUES if o[0] == "Owner review")
    assert "W37" in dev[1] and "W31" in dev[1] and "downpipe" in dev[1]
    vastu = " ".join(o[1] for o in M.OPEN_ISSUES if o[0] == "Vastu")
    for w in ("canopy kept full length", "two tanks", "mirror"):
        assert w in vastu, w


def test_no_old_room_names_in_the_prose_or_the_guide():
    import guide
    stale = ("stair hall", "reading room", "oonjal hall", "entry hall", "upper passage", "upper store", "loft tank", "roof space", "dressing room")
    texts = _prose() + [str(i) for _, items in guide.GUIDE for i in items]
    for s in texts:
        low = s.lower()
        for w in stale:
            assert w not in low or " become" in low, (w, s[:90])


def test_trees_and_beds_clear_of_drive_beds_and_borewell():
    f = {s[0]: s[3] for s in M.SITE_FEATURES}
    d0, d1 = M.DRIVE["off"]
    for t in list(M.TREES) + list(M.FOOD_TREES):
        x, y, r = t[:3]
        if x + r > M.DRIVE["x1"]:
            assert y - r >= d1 + 0 or y + r <= d0, t                  # canopy off the drive
        for b in M.GARDEN_BEDS:
            if t in M.TREES:
                dx = max(b[0] - x, 0, x - b[1]); dy = max(b[2] - y, 0, y - b[3])
                assert (dx ** 2 + dy ** 2) ** 0.5 >= r, (t, b)         # canopy off the beds
        bx, by = f["BORE"][:2]
        assert ((x - bx) ** 2 + (y - by) ** 2) ** 0.5 - r - 0.5 >= 3, t
    for b in M.GARDEN_BEDS:
        for fid in ("SUMP", "PATH", "RAMP", "SEPTIC", "CARPORT", "DRIVE", "GUILD", "SHOPS"):
            g = f.get(fid) if fid != "DRIVE" else (M.DRIVE["x1"], M.DRIVE["x2"], d0, d1)
            assert min(b[1], g[1]) - max(b[0], g[0]) <= 0 or min(b[3], g[3]) - max(b[2], g[2]) <= 0, (b, fid)


def test_terrace_drying_rails_clear_the_tank_stand_and_stay_over_the_washer_and_sink():
    rails = _furn("F88")
    for p in M.PLUMBING_F1:
        if p[0] == "TK":
            assert _pt_gap((p[1], p[2]), rails[3:7]) >= 1.33 - 1e-6, p[:3]      # the 2 ft 8 in tank (radius 1.33 ft) stands clear of the rails
    sink = _furn("F32")
    assert rails[3] <= sink[3] and rails[4] >= sink[4] and rails[5] <= sink[5] and rails[6] >= sink[6]    # still over the sink
    assert rails[4] - 0.0 > _furn("F30")[4] and rails[5] <= _furn("F30")[6]
    assert rails[3] >= 35.9 and rails[5] >= 41.0 - 1e-9 and rails[4] <= 39.9                     # only shortened on the north side: nothing moves toward the swing


def test_no_window_is_hidden_behind_tall_furniture():
    """A floor-to-ceiling or full-height unit never stands in front of a window (W52 was 0.2 ft behind the bookshelf)."""
    for fl in ("G", "F1"):
        for f in M._FLOOR_DATA[fl]["FURNITURE"]:
            t = f[2].lower()
            if not ("floor-to-ceiling" in t or "full-height" in t or "bookshelf" in t):
                continue
            for w in M._FLOOR_DATA[fl]["WINDOWS"]:
                if w[1] == "X" and min(abs(f[5] - w[2]), abs(f[6] - w[2])) <= 1.0:
                    assert not (f[3] < w[4] and f[4] > w[3]), (fl, f[0], w[0])
                if w[1] == "Y" and min(abs(f[3] - w[2]), abs(f[4] - w[2])) <= 1.0:
                    assert not (f[5] < w[4] and f[6] > w[3]), (fl, f[0], w[0])


# ---------- C11 final fix round ----------
def test_no_window_on_an_outer_wall_reads_inside():
    import make_xlsx
    outer = {("X", M.HY1), ("X", M.HY2), ("Y", M.HX1), ("Y", M.HX2)}
    upper = {w[0] for w in M.WINDOWS_F1}
    for w in list(M.WINDOWS) + list(M.WINDOWS_F1):
        f = make_xlsx.window_face(w, w[0] in upper)
        if (w[1], w[2]) in outer:
            assert f in ("South", "North", "West", "East"), (w[0], f)
        assert f != "Inside", (w[0], f)
    assert make_xlsx.window_face(next(w for w in M.WINDOWS if w[0] == "W60")) == "South"
    assert make_xlsx.window_face(next(w for w in M.WINDOWS_F1 if w[0] == "W37"), True) == "East (over ring roof)"
