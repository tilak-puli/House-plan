import geom as G
import model as M


def _area(r):
    return max(0.0, r[1] - r[0]) * max(0.0, r[3] - r[2])


def _meet(a, b):
    return (max(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), min(a[3], b[3]))


def test_ring_roof_outline_follows_the_grid():
    oh = M.ROOF["overhang"]
    assert M.ROOF["ring"] == (M.HX1 - oh, M.HX2 + oh, M.HY1 - oh, M.HY2 + oh)
    assert M.ROOF["court_eave"] == (M.CT[0] + 0.5, M.CT[1] - 0.5, M.CT[2] + 0.5, M.CT[3] - 0.5)
    assert abs(G.eave_z() - (M.LEVELS["FFL"] + M.LEVELS["wall_top"] - oh * G.TAN)) < 1e-9
    assert M.ROOF["grille_z"] == G.eave_z()


def test_ring_roof_rises_from_both_eaves_to_a_ridge():
    e = G.eave_z()
    x_mid_band_s = M.CX
    y_outer, y_inner = M.ROOF["ring"][2], M.ROOF["court_eave"][2]
    assert abs(G.ring_z(x_mid_band_s, y_outer + 0.001) - e) < 0.01
    assert abs(G.ring_z(x_mid_band_s, y_inner - 0.001) - e) < 0.01
    ridge_y = (y_outer + y_inner) / 2
    assert abs(G.ring_z(x_mid_band_s, ridge_y) - G.ridge_z()) < 0.01 and G.ridge_z() > e
    band = (M.ROOF["court_eave"][0] - M.ROOF["ring"][0]) / 2
    assert abs(G.ridge_z() - (e + G.TAN * band)) < 1e-9


def test_court_is_open_and_terrace_flat():
    assert G.ring_z(M.CX, M.CY) is None
    t = M.ROOF["terrace"]
    assert t == (M._DE, M._OX, M.RING[3], M.HY2)                     # exactly the roof terrace R37
    r37 = next(r for r in M._FLOOR_DATA["F1"]["ROOMS"] if r[0] == "R37")
    assert tuple(r37[2:6]) == t
    assert G.ring_z((t[0] + t[1]) / 2, (t[2] + t[3]) / 2) is None
    assert G.ring_z((t[0] + t[1]) / 2, (M.HY2 + M.ROOF["ring"][3]) / 2) is None   # no tiled eave past the terrace's north parapet


def test_wing_roof_covers_the_whole_l_with_2ft_eaves_and_the_ring_never_runs_under_it():
    oh = M.ROOF["overhang"]
    walls = M.ROOF["wing_walls"]
    assert walls[0] == (M.HX1, M.RING[0], M.HY1, M.HY2) and walls[1] == (M.HX1, M._DE, M.RING[3], M.HY2)
    for w, r in zip(walls, G.wing_rects()):
        assert r == (w[0] - oh, w[1] + oh, w[2] - oh, w[3] + oh)
    # every room of the upper floor (bar the open terrace) sits under the wing roof
    for room in M._FLOOR_DATA["F1"]["ROOMS"]:
        if room[0] == "R37":
            continue
        x1, x2, y1, y2 = room[2:6]
        for x in (x1 + 0.1, (x1 + x2) / 2, x2 - 0.1):
            for y in (y1 + 0.1, (y1 + y2) / 2, y2 - 0.1):
                assert G.wing_roof_z(x, y) is not None, (room[0], x, y)
    # the ring roof stops at the wing's walls: no ring roof inside them, nor on the wing's outer eaves
    for w in walls:
        for k in range(1, 20):
            for m in range(1, 20):
                x, y = w[0] + (w[1] - w[0]) * k / 20, w[2] + (w[3] - w[2]) * m / 20
                assert G.ring_z(x, y) is None, (x, y)
    assert G.ring_z(M.HX1 - oh / 2, M.CY) is None and G.ring_z(M.CX - 6, M.HY1 - oh / 2) is not None
    # the L's re-entrant corner is a valley: the wing roof there is lower than either arm's ridge and rises toward both
    cx, cy = M.ROOF["wing"][1], M.ROOF["wing_ext"][2]
    assert abs(G.wing_roof_z(cx, cy) - G.wing_eave_z()) < 1e-9
    assert abs(G.wing_roof_z(cx - 1, cy + 1) - (G.wing_eave_z() + G.TAN)) < 1e-9


def test_wing_roof_is_above_the_ring():
    for x, y in ((M.RING[0] - 1.5, M.CY), (M.RING[0] + 2.0, M.HY2 - 3.0)):
        assert G.wing_roof_z(x, y) > G.ridge_z()


def test_wing_ridge_from_the_span():
    span = M.RING[0] - M.HX1 + 2 * M.ROOF["overhang"]
    assert abs(G.wing_ridge_z() - (G.wing_eave_z() + G.TAN * span / 2)) < 1e-9
    assert abs(G.wing_eave_z() - (G.upper_wall_top_z() - M.ROOF["overhang"] * G.TAN)) < 1e-9


def test_terrace_edge_walls_clear_the_ring_roof():
    slab = G.terrace_slab_z()
    t = M.ROOF["terrace"]
    rise = 0.5
    assert M.ROOF["verge_east"] == (t[1], t[2], t[3], rise) and M.ROOF["verge_south"][0] == t[2]
    n_s = n_e = 0
    x = t[0] + 0.25
    while x < t[1]:                                   # south edge: upstand, raking where the east band's roof rises
        h = G.verge_south_h(x)
        assert h >= M.ROOF["upstand"] - 1e-9
        z = G.ring_z(x, t[2] - 0.001)
        if x < M.ROOF["verge_south"][1] and z is not None:              # over the walkway the plain upstand alone meets the rule
            assert M.ROOF["upstand"] >= (z - slab) + rise - 1e-9, x
        if z is not None and z > slab:
            assert h >= (z - slab) + rise - 1e-9, x
            n_s += 1
        x += 0.5
    y = t[2] + 0.25
    while y < t[3]:                                   # east edge: the verge wall
        z = G.ring_z(t[1] + 0.001, y)
        if z is not None and z > slab:
            assert G.verge_east_h(y) >= (z - slab) + rise - 1e-9, y
            n_e += 1
        y += 0.5
    assert n_s >= int((t[1] - t[0]) / 0.5) - 1 and n_e >= int((t[3] - t[2]) / 0.5) - 1
    # north of the corner guard the east wall follows the roof (a raking verge), not a constant
    (gx1, gx2), (gy1, gy2) = G.corner_guard_runs()
    hs = [G.verge_east_h(gy2 + 0.25 + 0.5 * k) for k in range(int((t[3] - gy2) / 0.5))]
    assert max(hs) - min(hs) > 1.0


def test_terrace_corner_guard_is_level_over_the_ridge_end():
    slab, t, g = G.terrace_slab_z(), M.ROOF["terrace"], M.ROOF["corner_guard"]
    assert g >= G.ridge_z() - slab + 0.5 - 1e-9 and g >= M.RAIL_H     # 6 in over the ridge end, and a full guard height
    (gx1, gx2), (gy1, gy2) = G.corner_guard_runs()
    rr = G.ring_ridge_rect()
    assert gx2 == t[1] and gy1 == t[2] and abs(gy2 - (rr[3] + t[1] - rr[1])) < 1e-9   # turns up the east edge to the NE hip crossing
    assert G._raw_south(gx1 - 0.05) <= M.ROOF["upstand"] + 1e-9 < G._raw_south(gx1 + 0.05)   # starts where the rake first passes the upstand
    assert gx1 < rr[1] < gx2                                           # the ring's east ridge runs into it
    hs = [G.verge_south_h(gx1 + (gx2 - gx1) * k / 20) for k in range(21)] + [G.verge_east_h(gy1 + (gy2 - gy1) * k / 20) for k in range(21)]
    assert max(hs) - min(hs) < 1e-9 and hs[0] == g                      # a constant top over the whole corner run
    assert G.verge_south_h(gx1 - 0.25) == M.ROOF["upstand"]           # west of it, the plain upstand
    d = next(f for f in M._FLOOR_DATA["F1"]["FURNITURE"] if f[0] == "F127")
    assert d[5] > gy2 and max(G.verge_east_h(d[5] + (d[6] - d[5]) * k / 20) for k in range(21)) <= 2 + 11 / 12   # the daybed still sees east


def test_terrace_outlet_has_a_downpipe_clear_of_the_eave_and_a_rain_pipe():
    t, o = M.ROOF["terrace"], M.ROOF["terrace_outlet"]
    assert t[0] < o[0] < t[1] and t[2] < o[1] < t[3]
    dp = M.ROOF["downpipes"][-1]
    assert abs(dp[0] - o[0]) < 0.1 and dp[1] > t[3]                   # outside the north parapet: no pipe through the slab or tiles
    assert G.roof_z(*dp) is None
    assert any(p[0] == "DP" and (p[1], p[2]) == dp for p in M.PLUMBING)


def test_roof_area_matches_the_plan_outline():
    # plan area of every roof piece counted once: the ring outline, less the court and the terrace (to its parapet), plus the wing's eave
    # over the terrace; then / cos(pitch)
    import math
    o, ce, t0 = M.ROOF["ring"], M.ROOF["court_eave"], M.ROOF["terrace"]
    t = (t0[0], t0[1], t0[2], o[3] if t0[3] == M.HY2 else t0[3])     # the terrace hole runs out to the outer eave line past its parapet
    w1, w2 = M.ROOF["wing"], M.ROOF["wing_ext"]
    wing_on_terrace = _area(_meet(w1, t)) + _area(_meet(w2, t)) - _area(_meet(_meet(w1, w2), t))
    plan = _area(o) - _area(ce) - _area(t) + wing_on_terrace
    expect = plan / math.cos(math.radians(M.ROOF["pitch"]))
    assert abs(G.roof_area() - expect) <= 0.01 * expect, (G.roof_area(), expect)


def test_wing_eave_is_above_the_ring_ridge():
    assert G.wing_eave_z() > G.ridge_z()


def test_thinnai_lean_to_carries_the_ring_slope_with_headroom_at_the_pillars():
    th = M.ROOF["thinnai"]
    t17 = next(r for r in M.ROOMS if r[0] == "R17")
    assert th[0] == M.HX2 and th[1] == max(px for px, _ in M.THINNAI_PILLARS) + 1.5
    assert th[2] <= t17[4] and th[3] >= t17[5]                       # covers the platform end to end
    assert abs(G.thinnai_roof_z(M.ROOF["ring"][1], M.CY) - G.eave_z()) < 1e-9          # the ring's east slope, same plane
    assert abs(G.thinnai_roof_z(M.HX2, M.CY) - G.ring_z(M.HX2 + 0.001, M.HY1 + 5)) < 0.01
    assert G.thinnai_headroom() >= 7.5
    for px, py in M.THINNAI_PILLARS:
        assert G.thinnai_roof_z(px, py) is not None and px < th[1]


def test_jharokhas_clear_the_walkway_roof_by_their_kerb():
    for j in M.JHAROKHAS:
        assert j[4] == 2.0
        assert G.jharokha_clearance(j) >= M.ROOF["jharokha_kerb"]


def test_jharokha_on_a_valley_gets_a_saddle_round_its_kerb():
    kerb = M.ROOF["jharokha_kerb"]
    valley = G.ring_valley_points()
    on_valley = set()
    for k, j in enumerate(M.JHAROKHAS):
        under = [p for p in valley if j[0] <= p[0] <= j[1] and j[2] <= p[1] <= j[3]]
        for p in under:                                                # the bay clears the valley under its kerb
            assert G.jharokha_base_z(j) - G.ring_z(*p) >= kerb - 1e-9, (k, p)
        if not under:
            continue
        on_valley.add(k)
        zlow = min(G.ring_z(*p) for p in under)
        up = [p for p in valley if j[0] - 1 <= p[0] <= j[1] + 1 and j[2] - 1 <= p[1] <= j[3] + 1 and G.ring_z(*p) >= zlow - 1e-9]
        for p in up:                                                   # the valley under and up-slope of the kerb is filled by a saddle
            s = [s for s in M.ROOF["saddles"] if s[0] == k and s[1] - 1e-9 <= p[0] <= s[2] + 1e-9 and s[3] - 1e-9 <= p[1] <= s[4] + 1e-9]
            assert s, (k, p)
            assert G.ring_z(*p) + s[0][5] <= G.jharokha_base_z(j) + 1e-9 or not (j[0] <= p[0] <= j[1] and j[2] <= p[1] <= j[3])
    assert on_valley and on_valley == {s[0] for s in M.ROOF["saddles"]}
    for s in M.ROOF["saddles"]:
        j = M.JHAROKHAS[s[0]]
        assert s[5] == kerb and _area(_meet(s[1:5], j[:4])) > 0       # it reaches the bay's kerb, up to the kerb top
        assert s[1] >= M.RING[0] - 1e-9                                # it stops against the wing's wall


def test_wing_eaves_shelter_the_jharokhas_and_the_canopy_butts_under_the_wing_gutter():
    oh = M.ROOF["overhang"]
    t = M.ROOF["terrace"]
    over = [w for w in G.wing_rects() if w[0] < t[0] < w[1] and _area(_meet(w, t)) > 0]
    assert over and all(abs(w[1] - (t[0] + oh)) < 1e-9 for w in over)    # the wing's east eave hangs 2 ft over the terrace
    under = G.wing_eave_z() - 0.45            # the eave's underside (tiles, battens, deck)
    assert G.terrace_slab_z() + M.ROOF["canopy"] + 0.35 <= under - M.ROOF["gutter_depth"] - 2 / 12   # canopy deck clears the gutter by 2 in
    assert M.ROOF["canopy"] >= 7.5                                   # 7'-6" clear on the terrace
    gutter_bottom = under - M.ROOF["gutter_depth"]
    for j, face in zip(M.JHAROKHAS, M.JHAROKHA_FACE):
        assert any(w[0] <= j[0] and j[1] <= w[1] and w[2] <= j[2] and j[3] <= w[3] for w in G.wing_rects()), j   # under a wing eave
        head = G.floor_base("F1") + M.ROOF["jharokha_head"]
        assert gutter_bottom >= head + 2 / 12 - 1e-9                   # the outboard gutter's bottom 2 in+ above the casement heads
        if M.ROOF["jharokha_to_soffit"]:
            continue                                                   # closed up to the eave soffit: the eave is the bay's roof
        # otherwise the bay needs its own roof: a plan gap to the eave line and its top under the gutter
        edge = [w for w in G.wing_rects() if w[0] <= j[0] and j[1] <= w[1] and w[2] <= j[2] and j[3] <= w[3]][0]
        gap = (edge[1] - j[1]) if face == "E" else (j[2] - edge[2])
        assert gap >= 0.25 and head + 0.9 <= gutter_bottom - 2 / 12, j


def test_wing_gutters_fall_away_from_the_box_gutter_to_spreaders_or_downpipes():
    bx, by, *_mm, spout = M.ROOF["wing_box_gutter"]
    assert (bx, by) == (M.ROOF["wing"][1], M.ROOF["wing_ext"][2])       # at the L's re-entrant corner
    assert (bx, by) not in M.ROOF["downpipes"]
    runs = M.ROOF["wing_gutter_runs"]
    assert sum(1 for hi, lo in runs if hi == (bx, by)) == 2 and all(lo != (bx, by) for _, lo in runs)   # the box is a high point of both
    for hi, lo in runs:
        on = lambda p: any((abs(p[0] - w[0]) < 1e-9 or abs(p[0] - w[1]) < 1e-9) and w[2] - 1e-9 <= p[1] <= w[3] + 1e-9 or
                           (abs(p[1] - w[2]) < 1e-9 or abs(p[1] - w[3]) < 1e-9) and w[0] - 1e-9 <= p[0] <= w[1] + 1e-9 for w in G.wing_rects())
        assert on(hi) and on(lo), (hi, lo)                             # along a wing eave
        assert lo in M.ROOF["wing_spreaders"] or any(hi2 == lo for hi2, _ in runs) or any(abs(lo[0] - d[0]) <= 0.5 and abs(lo[1] - d[1]) <= 1.5 for d in M.ROOF["downpipes"]), lo
    # the overflow spout drops onto the ring's north-west valley
    assert min(abs(spout[0] - p[0]) + abs(spout[1] - p[1]) for p in G.ring_valley_points()) < 0.1


def test_wing_east_gutter_over_the_terrace_reaches_its_downpipe():
    t, runs = M.ROOF["terrace"], M.ROOF["wing_gutter_runs"]
    east = M.ROOF["wing_ext"][1]
    r = [run for run in runs if abs(run[0][0] - east) < 1e-9 and abs(run[1][0] - east) < 1e-9]
    assert r and r[0][1][1] > r[0][0][1]                               # falls north
    turn = [run for run in runs if run[0] == r[0][1]]
    assert turn and (turn[0][1][0], M.HY2 + 0.7) in M.ROOF["downpipes"]  # then west along the north eave to the downpipe


def test_upper_openings_on_walls_the_ring_abuts_stand_over_the_roof():
    walls = [("Y", M.RING[0], M.HY1, M.RING[3]), ("X", M.RING[3], M.RING[0], M._DE)]   # the wing's walls the ring roof runs against
    f1 = M._FLOOR_DATA["F1"]
    for a, c, s1, s2 in walls:
        assert not [d[0] for d in f1["DOORS"] if (d[1], d[2]) == (a, c) and s1 <= d[3] < s2], (a, c)
        for w in f1["WINDOWS"]:
            if (w[1], w[2]) != (a, c) or not (s1 <= w[3] < s2):
                continue
            pts = [w[3] + (w[4] - w[3]) * k / 20 for k in range(21)]
            zs = [G.ring_z(c + 0.001, u) if a == "Y" else G.ring_z(u, c - 0.001) for u in pts]
            top = max(z for z in zs if z is not None)
            assert G.floor_base("F1") + w[5] >= top + 0.5 - 1e-9, (w[0], round(top + 0.5 - G.floor_base("F1"), 2))
    w37 = next(w for w in f1["WINDOWS"] if w[0] == "W37")
    r31 = next(r for r in f1["ROOMS"] if r[0] == "R31")
    assert w37[5] == 3 and r31[4] <= w37[3] and w37[4] <= r31[5]           # the escape window keeps its 3 ft sill and stays in Bedroom 2


def test_living_north_windows_under_the_terrace_chajja():
    ch, t = M.ROOF["terrace_chajja"], M.ROOF["terrace"]
    assert ch == (t[0], t[1], M.HY2, M.HY2 + M.ROOF["overhang"])
    for wid in ("W75", "W76"):
        w = next(w for w in M._FLOOR_DATA["G"]["WINDOWS"] if w[0] == wid)
        assert (w[1], w[2]) == ("X", M.HY2) and ch[0] <= w[3] and w[4] <= ch[1], wid
    dp = M.ROOF["downpipes"][-1]
    assert ch[0] < dp[0] < ch[1] and ch[2] < dp[1] < ch[3]                # the terrace downpipe drops through it in a sleeve


def test_wing_spreaders_sit_on_the_wing_eave_over_the_ring_clear_of_the_bays():
    for sx, sy in M.ROOF["wing_spreaders"]:
        on_eave = any((abs(sx - w[1]) < 1e-9 and w[2] <= sy <= w[3]) or (abs(sy - w[2]) < 1e-9 and w[0] <= sx <= w[1]) for w in G.wing_rects())
        assert on_eave, (sx, sy)
        assert G.ring_z(sx + 0.01, sy - 0.01) is not None, (sx, sy)       # discharges onto the ring roof, not the terrace
        for j in M.JHAROKHAS:
            gx = max(j[0] - sx, 0, sx - j[1]); gy = max(j[2] - sy, 0, sy - j[3])
            assert (gx * gx + gy * gy) ** 0.5 >= 1.0, (sx, sy, j)


def test_south_downpipe_clear_of_the_kitchen_window():
    dp = [d for d in M.ROOF["downpipes"] if d[1] < M.HY1 and M.HX1 + 1 < d[0] < M.HX2 - 1]
    assert len(dp) == 1
    w82 = next(w for w in M._FLOOR_DATA["G"]["WINDOWS"] if w[0] == "W82")
    assert w82[1:3] == ("X", M.HY1)
    assert not (w82[3] - 1 <= dp[0][0] <= w82[4] + 1)


def test_downpipes_clear_of_every_window_and_door_on_their_wall():
    walls = (("X", M.HY1), ("X", M.HY2), ("Y", M.HX1), ("Y", M.HX2))
    for x, y in M.ROOF["downpipes"]:
        near = [(a, c) for a, c in walls if abs((y if a == "X" else x) - c) <= 1.0]
        assert near, (x, y)                                               # each pipe runs down an outer wall
        for fl in ("G", "F1"):
            d = M._FLOOR_DATA[fl]
            for o in list(d["WINDOWS"]) + list(d["DOORS"]):
                for a, c in near:
                    if (o[1], o[2]) == (a, c):
                        along = x if a == "X" else y
                        assert not (o[3] - 1.0 <= along <= o[4] + 1.0), ((x, y), o[0], fl)


def test_elevation_profile_tops_out_at_the_wing_ridge():
    import sheets_elev as E
    for face in ("N", "E"):
        w = M.ROOF["wing"]
        a, b = (w[0], w[1]) if face == "N" else (w[2], w[3])
        top = max(z for _, z in E._profile(face, G.wing_roof_z, a, b) if z is not None)
        assert abs(top - G.wing_ridge_z()) < 0.15, (face, top)


def test_terrace_tanks_stand_apart_and_clear_of_the_washer_and_sink():
    r = 1.333                                                          # 500 L tank, 2 ft 8 in across
    tks = sorted((p[1], p[2]) for p in M.PLUMBING_F1 if p[0] == "TK")
    assert len(tks) == 2 and tks[1][0] - tks[0][0] >= 2.75 - 1e-9 and tks[0][1] == tks[1][1]   # 2'-9" centres: a working gap between them
    furn = {f[0]: f for f in M._FLOOR_DATA["F1"]["FURNITURE"]}
    for fid in ("F30", "F32"):
        f = furn[fid]
        for x, y in tks:
            gx = max(f[3] - x, 0, x - f[4]); gy = max(f[5] - y, 0, y - f[6])
            assert (gx * gx + gy * gy) ** 0.5 - r >= 1 / 12 - 1e-9, (fid, x, y)
    assert all(y + r <= M.HY2 + M.T / 2 for _, y in tks)                # within the north wall's outer face (the parapet stands on it)


def test_wing_downpipes_stand_clear_of_the_terrace_chajja():
    """Only the terrace downpipe passes through the chajja (in a sleeve); every other downpipe is 0.25 ft or more clear of its edges."""
    x1, x2, y1, y2 = M.ROOF["terrace_chajja"]
    ox, oy = M.ROOF["terrace_outlet"]
    terrace_dp = min(M.ROOF["downpipes"], key=lambda d: (d[0] - ox) ** 2 + (d[1] - oy) ** 2)   # the one the terrace outlet feeds
    assert ((terrace_dp[0] - ox) ** 2 + (terrace_dp[1] - oy) ** 2) ** 0.5 <= 1.5
    for x, y in [d for d in M.ROOF["downpipes"] if d != terrace_dp]:
        if y1 - 0.25 <= y <= y2 + 0.25:
            assert x <= x1 - 0.25 or x >= x2 + 0.25, (x, y)
    dps = {(p[1], p[2]) for p in M.PLUMBING if p[0] == "DP"}
    assert set(M.ROOF["downpipes"]) <= dps                       # the plumbing points follow the roof's downpipes
    for x, y in M.ROOF["downpipes"]:
        on = lambda a, b: min(a[0], b[0]) - 0.01 <= x <= max(a[0], b[0]) + 0.01 and min(a[1], b[1]) - 0.01 <= y <= max(a[1], b[1]) + 0.01
        assert any(k == "rain" and any(on(a, b) for a, b in zip(l, l[1:])) for k, l in M.PIPES), (x, y)   # and its rain pipe starts there
