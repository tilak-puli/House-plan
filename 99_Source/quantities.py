"""Approximate quantities taken off the model, for budgeting and contractor pricing (not a priced BOQ)."""
from geom import *

AAC_T = {"EXT": 0.656, "WET": 0.492, "INT": 0.328}  # block thickness, ft (200 / 150 / 100 mm)
AAC_H = LEVELS["wall_top"] - 0.75 - 0.5             # floor to underside of ring beam, less lintel band depth (same on both floors)


def opening_area(w):
    area = 0
    for a, b, kind, rec in openings_for(*w):
        area += (b - a) * (7.0 if kind == "door" else rec[6] - rec[5])
    return area


def take_off():
    q = []  # (group, item, qty, unit, basis)
    walls = {"EXT": 0, "WET": 0, "INT": 0}
    plaster_in = plaster_out = 0
    wall_len = 0
    for fl in ("G", "F1"):
        with on_floor(fl):
            for w in WALLS:
                wt = wall_type(w)
                net = (w[3] - w[2]) * AAC_H - opening_area(w)
                walls[wt] += net * AAC_T[wt]
                plaster_in += net * (1 if wt == "EXT" else 2)
                if wt == "EXT":
                    plaster_out += net
                wall_len += w[3] - w[2]
    for wt, v in walls.items():
        q.append(("Walls", f"AAC blocks, {dict(EXT='200 mm outer', WET='150 mm wet', INT='100 mm inner')[wt]} walls", round(v * 0.0283, 2), "cu m", "Both floors, net of openings, floor to beam soffit"))
    q.append(("Frame", "Lintel band / ring beam (each, running length, both floors)", round(wall_len * 0.3048, 1), "m", "Along all walls; sizes by engineer"))
    slab = sum((x2 - x1) * (y2 - y1) for x1, x2, y1, y2 in SLAB_F1)
    q.append(("Frame", "First-floor RCC slab (about 5 in)", round(slab * 0.0929, 1), "sq m", "Over the west wing and the roof terrace, less the stair well"))
    q.append(("Frame", "RCC dog-leg stair", STAIR["risers"], "risers", "3'-6\" flights, half landing 7'-6\" x 3'-6\", 16 risers of 7.5 in"))
    q.append(("Frame", f"Galvanised steel posts for the terrace canopy (about 100 mm SHS, {fmt_ft(ROOF['canopy'])})", len(TERRACE_POSTS), "no.", "On RCC column stubs; the light tiled canopy on a steel frame"))
    q.append(("Frame", "Railings, teak or MS with teak cap, 4'-0\" high", round(sum(e - s for a, c, s, e in RAILS_F1 if (a, c) not in JALI_RAILS) * 0.3048, 1), "m", "Terrace south and east sides and the stair well"))
    q.append(("Frame", "Teak jali parapet panels, 4'-0\" high, on a steel core", round(sum(e - s for a, c, s, e in RAILS_F1 if (a, c) in JALI_RAILS) * 0.3048, 1), "m", "Terrace north side (towards the neighbour)"))
    q.append(("Walls", "Internal plaster", round(plaster_in * 0.0929, 1), "sq m", "Both faces of inner walls, inner face of outer walls"))
    q.append(("Walls", "External plaster (waterproof)", round((plaster_out + (HX2 - HX1 + T) * 4 * LEVELS["FFL"]) * 0.0929, 1), "sq m", "Outer walls (both floors) + plinth face; add scaffolding for the two-storey west wing"))
    finishes = {}
    skirting = 0
    for fl in ("G", "F1"):
        with on_floor(fl):
            for r in ROOMS:
                L, W = clear_dims(r)
                finishes[FLOOR_FINISH[r[0]]] = finishes.get(FLOOR_FINISH[r[0]], 0) + L * W
                if r[0] not in ("R08", "R07", "R40", "R33", "R39", "R13", "R17", "R37", "R06"):
                    skirting += 2 * (L + W)
    for k, v in finishes.items():
        q.append(("Floors", k, round(v * 0.0929, 1), "sq m", "Clear room areas; add 5-8% wastage"))
    q.append(("Floors", "Flush skirting, 4 in", round(skirting * 0.3048, 1), "m", "Room perimeters (dry rooms), doors not deducted"))
    for rid in ("R08", "R07", "R40", "R33", "R39"):
        with on_floor("F1" if rid in F1_ROOM_IDS else "G"):
            L, W = clear_dims(room_of(rid)); nm = room_of(rid)[1]
        q.append(("Wet rooms", f"Wall tiles to 7 ft, {nm}", round((2 * (L + W) * 7 - 2.5 * 7) * 0.0929, 1), "sq m", "Full height in the shower adds ~2 sq m"))
        q.append(("Wet rooms", f"Waterproofing, {nm}", round((L * W + 2 * (L + W) * 1 + 6 * 6) * 0.0929, 1), "sq m", "Floor + 12 in upturn + shower walls to 7 ft"))
    with on_floor("F1"):
        L, W = clear_dims(room_of("R37"))
    q.append(("Wet rooms", "Waterproofing, roof terrace slab", round((L * W + 2 * (L + W)) * 0.0929, 1), "sq m", "Floor + 12 in upturn; flood test 48 h"))
    q.append(("Kitchen", "Granite counter, 2 ft deep", round((11.0 + 6.5) * 0.3048, 1), "m", "South and east runs (F34, F35)"))
    q.append(("Kitchen", "Dado between counter and wall cabinets", round((11.0 + 6.5) * 2 * 0.0929, 1), "sq m", "2 ft high"))
    q.append(("Roof", "Sloped roof area (tiles, deck, insulation, membrane)", round(roof_area() * 0.0929, 1), "sq m", f"Ring roof + the upper wing's L-shaped hip, less the court and the terrace slab, / cos {ROOF['pitch']} deg; add ~8% for laps"))
    ox1, ox2, oy1, oy2 = ROOF["ring"]; wb = wing_bbox(); t_ = ROOF["terrace"]; th = ROOF["thinnai"]
    def _eave_len(pts):   # length of the ring's outer eave where the ring roof is the top roof (sampled at 0.25 ft)
        return sum(0.25 for x, y in pts if ring_z(x, y) is not None and wing_roof_z(x, y) is None)
    n = lambda a, b: [a + 0.125 + 0.25 * k for k in range(int((b - a) / 0.25))]
    ring_eave = (_eave_len([(x, oy1 + 0.05) for x in n(ox1, ox2)]) + _eave_len([(x, oy2 - 0.05) for x in n(ox1, ox2)])
                 + _eave_len([(ox2 - 0.05, y) for y in n(oy1, oy2) if not th[2] < y < th[3]]))
    q.append(("Roof", "Gutters, ring outer eaves", round(ring_eave * 0.3048, 1), "m", "Where the ring is the top roof: the south, the east (the thinnai front apart) and the north beside the pooja"))
    q.append(("Roof", "Gutters, upper wing eaves", round(2 * ((wb[1] - wb[0]) + (wb[3] - wb[2])) * 0.3048, 1), "m", f"All round the L (its east eave over the terrace included); the courtyard-side gutters' {len(ROOF['wing_spreaders'])} spreader downpipes discharge onto the ring roof"))
    (gx1, gx2), (gy1, gy2) = corner_guard_runs()
    q.append(("Roof", f"Terrace south edge: {fmt_ft(ROOF['upstand'])} RCC upstand, then the level corner guard ({fmt_ft(ROOF['corner_guard'])})", round(verge_south_area() * 0.0929, 1), "sq m", f"Face area of the {t_[1] - t_[0]:.1f} ft long edge; the guard runs x {gx1:.1f}-{gx2:.1f}; apron, step and counter-flashing"))
    q.append(("Roof", f"Terrace east edge: the corner guard, then a verge wall 6 in over the roof", round(verge_east_area() * 0.0929, 1), "sq m", f"Face area of the {t_[3] - t_[2]:.1f} ft long edge; the guard runs y {gy1:.1f}-{gy2:.1f}, the verge north of it"))
    q.append(("Roof", "RCC edge beams under the terrace's south-east corner guard (no wall below)", round(((gx2 - RING[1]) + (__import__('model')._NY - gy1)) * 0.3048, 1), "m", "The south edge east of the walkway and the east edge over the console nook, over the open family room"))
    ch = ROOF["terrace_chajja"]
    q.append(("Roof", "RCC chajja, 2 ft, off the terrace's north edge beam", round((ch[1] - ch[0]) * 0.3048, 1), "m", "Over the living's north windows W75/W76; the terrace downpipe passes in a sleeve"))
    ww = ROOF["wing_walls"]
    apron = (RING[3] - HY1) + (ww[1][1] - RING[0]) + (t_[1] - t_[0]) + (t_[3] - t_[2])
    q.append(("Roof", "Apron / step flashing at walls", round(apron * 0.3048, 1), "m", "Where the ring roof meets the wing's east and south walls and the terrace's edge walls (counter-flashed in a chase at the corner guard)"))
    q.append(("Roof", "Spreader downpipes, wing courtyard-side eaves", len(ROOF["wing_spreaders"]), "no.", "Short, onto the ring roof, clear of the jharokhas"))
    q.append(("Roof", "Thinnai lean-to roof (tiles on exposed rafters)", round(thinnai_roof_area() * 0.0929, 1), "sq m", f"The ring's east slope carried on over the pillars, past the ring eave, / cos {ROOF['pitch']} deg"))
    q.append(("Roof", "Jharokha kerbs with back-gutter and apron flashing", len(JHAROKHAS), "no.", "6 in kerb per bay where it passes through the walkway roof"))
    q.append(("Roof", "Lead-lined pocket gutter beside a jharokha kerb", len(ROOF["saddles"]), "no.", "Bay J2's west kerb on the ring's north-west valley: falls south past the kerb corner to the valley"))
    q.append(("Roof", "Soldered internal box gutter, 300 x 300 x 150 mm, with a 50 mm overflow spout", 1, "no.", "The wing's re-entrant corner: the high point of its courtyard-side gutters"))
    q.append(("Roof", "Downpipes, 100 mm", len(ROOF["downpipes"]), "no.", "The wing's three corners, the south and east sides, the north-east corner and the terrace outlet's; about 12 ft each (the wing's 22 ft)"))
    ll = roof_line_lengths()
    q.append(("Roof", "Ridge and hip tiles", round((ll["ridge"] + ll["hip"] * HIP_K) * 0.3048, 1), "m", "Measured on the roof plan, hips to their true length (x HIP_K): ring and wing ridges and hips"))
    q.append(("Roof", "Valley gutters, 12 in GI / aluminium", round(ll["valley"] * HIP_K * 0.3048, 1), "m", "The ring's inner valleys and the wing's re-entrant valley, on the slope"))
    feat_gate = next(f[3] for f in SITE_FEATURES if f[0] == "GATE")[2:]
    q.append(("Site", "Compound wall, precast RCC post and panel, 5 ft high", round((plot_perimeter() - (feat_gate[1] - feat_gate[0]) - (SHOP_WALL[0][1] - next(f[3] for f in SITE_FEATURES if f[0] == "SHOP1")[2])) * 0.3048, 1), "m", "Plot perimeter less the gate and the shop frontage; the road face in exposed brick or local stone"))
    q.append(("Site", "Plinth protection apron, 3 ft wide", round(((HX2 - HX1 + T) * 4 * 3 + 4 * 9) * 0.0929, 1), "sq m", "PCC with slope away"))
    q.append(("Openings", "Doors", len(both("DOORS")), "no.", "See Doors tab"))
    q.append(("Openings", "Windows and vents", len(both("WINDOWS")), "no.", "See Windows tab"))
    q.append(("Openings", "Window area (for mesh and grills)", round(sum((w[4] - w[3]) * (w[6] - w[5]) for w in both("WINDOWS")) * 0.0929, 1), "sq m", ""))
    return q
