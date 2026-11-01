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
    q.append(("Frame", "First-floor RCC slab (about 5 in)", round(slab * 0.0929, 1), "sq m", "Over the back half, less the stair well"))
    q.append(("Frame", "RCC dog-leg stair", STAIR["risers"], "risers", "3'-6\" flights, half landing 7'-6\" x 5'-8\""))
    q.append(("Frame", "Galvanised steel posts for the terrace roof (about 100 mm SHS, 9 ft)", len(TERRACE_POSTS), "no.", "On RCC column stubs; trusses over the terrace in steel"))
    q.append(("Frame", "Railings, teak or MS with teak cap, 3'-6\" high", round(sum(e - s for _, _, s, e in RAILS_F1) * 0.3048, 1), "m", "Terrace open sides and stair well"))
    q.append(("Walls", "Internal plaster", round(plaster_in * 0.0929, 1), "sq m", "Both faces of inner walls, inner face of outer walls"))
    q.append(("Walls", "External plaster (waterproof)", round((plaster_out + (50.75 + 22.75) * 2 * LEVELS["FFL"]) * 0.0929, 1), "sq m", "Outer walls (both floors) + plinth face; add scaffolding for the 20 ft walls"))
    finishes = {}
    skirting = 0
    for fl in ("G", "F1"):
        with on_floor(fl):
            for r in ROOMS:
                L, W = clear_dims(r)
                finishes[FLOOR_FINISH[r[0]]] = finishes.get(FLOOR_FINISH[r[0]], 0) + L * W
                if r[0] not in ("R02", "R03", "R33", "R13", "R17", "R37", "R06"):
                    skirting += 2 * (L + W)
    for k, v in finishes.items():
        q.append(("Floors", k, round(v * 0.0929, 1), "sq m", "Clear room areas; add 5-8% wastage"))
    q.append(("Floors", "Flush skirting, 4 in", round(skirting * 0.3048, 1), "m", "Room perimeters (dry rooms), doors not deducted"))
    for rid in ("R02", "R03", "R33"):
        with on_floor("F1" if rid in F1_ROOM_IDS else "G"):
            L, W = clear_dims(room_of(rid)); nm = room_of(rid)[1]
        q.append(("Wet rooms", f"Wall tiles to 7 ft, {nm}", round((2 * (L + W) * 7 - 2.5 * 7) * 0.0929, 1), "sq m", "Full height in the shower adds ~2 sq m"))
        q.append(("Wet rooms", f"Waterproofing, {nm}", round((L * W + 2 * (L + W) * 1 + 6 * 6) * 0.0929, 1), "sq m", "Floor + 12 in upturn + shower walls to 7 ft"))
    with on_floor("F1"):
        L, W = clear_dims(room_of("R37"))
    q.append(("Wet rooms", "Waterproofing, covered terrace slab", round((L * W + 2 * (L + W)) * 0.0929, 1), "sq m", "Floor + 12 in upturn; flood test 48 h"))
    q.append(("Kitchen", "Granite counter, 2 ft deep", round((11.2 + 6.5) * 0.3048, 1), "m", "South and east runs (F34, F35)"))
    q.append(("Kitchen", "Dado between counter and wall cabinets", round((11.2 + 6.5) * 2 * 0.0929, 1), "sq m", "2 ft high"))
    q.append(("Roof", "Sloped roof area (tiles, deck, insulation, membrane)", round(roof_area() * 0.0929, 1), "sq m", f"Main hip + front gable / cos {ROOF['pitch']} deg; add ~8% for laps"))
    x1, x2, y1, y2 = ROOF["hip"]
    gx1, gx2, _, _ = ROOF["gable"]
    q.append(("Roof", "Gutters", round(2 * ((x2 - x1) + (gx2 - x2)) * 0.3048, 1), "m", "Both long eaves of the main roof and the front gable"))
    q.append(("Roof", "Downpipes, 100 mm", len(ROOF["downpipes"]), "no.", "About 22 ft (main roof) or 12 ft (front gable) each"))
    q.append(("Roof", "Ridge and hip tiles", round(((x2 - x1) - (y2 - y1) + 4 * ((y2 - y1) / 2) * 1.414) * 0.3048, 1), "m", "Approximate"))
    feat_gate = next(f[3] for f in SITE_FEATURES if f[0] == "GATE")[2:]
    q.append(("Site", "Compound wall, precast RCC post and panel, 5 ft high", round((2 * SITE["l"] + 2 * SITE["w"] - (feat_gate[1] - feat_gate[0])) * 0.3048, 1), "m", "Plot perimeter less the gate"))
    q.append(("Site", "Plinth protection apron, 3 ft wide", round(((50.75 + 22.75) * 2 * 3 + 4 * 9) * 0.0929, 1), "sq m", "PCC with slope away"))
    q.append(("Openings", "Doors", len(both("DOORS")), "no.", "See Doors tab"))
    q.append(("Openings", "Windows and vents", len(both("WINDOWS")), "no.", "See Windows tab"))
    q.append(("Openings", "Window area (for mesh and grills)", round(sum((w[4] - w[3]) * (w[6] - w[5]) for w in both("WINDOWS")) * 0.0929, 1), "sq m", ""))
    return q
