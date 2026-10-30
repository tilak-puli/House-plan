"""Approximate quantities taken off the model, for budgeting and contractor pricing (not a priced BOQ)."""
from geom import *

AAC_T = {"EXT": 0.656, "WET": 0.492, "INT": 0.328}  # block thickness, ft (200 / 150 / 100 mm)
AAC_H = LEVELS["wall_top"] - 0.75 - 0.5             # FFL to underside of ring beam, less lintel band depth


def opening_area(w):
    area = 0
    for a, b, kind, rec in openings_for(*w):
        area += (b - a) * (7.0 if kind == "door" else rec[6] - rec[5])
    return area


def take_off():
    q = []  # (group, item, qty, unit, basis)
    walls = {"EXT": 0, "WET": 0, "INT": 0}
    plaster_in = plaster_out = 0
    for w in WALLS:
        wt = wall_type(w)
        net = (w[3] - w[2]) * AAC_H - opening_area(w)
        walls[wt] += net * AAC_T[wt]
        plaster_in += net * (1 if wt == "EXT" else 2)
        if wt == "EXT":
            plaster_out += net
    for wt, v in walls.items():
        q.append(("Walls", f"AAC blocks, {dict(EXT='200 mm outer', WET='150 mm wet', INT='100 mm inner')[wt]} walls", round(v * 0.0283, 2), "cu m", "Net of openings, FFL to beam soffit"))
    wall_len = sum(w[3] - w[2] for w in WALLS)
    q.append(("Frame", "Plinth beam / lintel band / ring beam (each, running length)", round(wall_len * 0.3048, 1), "m", "Along all walls; sizes by engineer"))
    q.append(("Walls", "Internal plaster", round(plaster_in * 0.0929, 1), "sq m", "Both faces of inner walls, inner face of outer walls"))
    q.append(("Walls", "External plaster (waterproof)", round((plaster_out + (60.75 + 22.75) * 2 * LEVELS["FFL"]) * 0.0929, 1), "sq m", "Outer walls + plinth face"))
    finishes = {}
    skirting = 0
    for r in ROOMS:
        L, W = clear_dims(r)
        finishes[FLOOR_FINISH[r[0]]] = finishes.get(FLOOR_FINISH[r[0]], 0) + L * W
        if r[0] not in ("R04", "R07", "R08", "R13", "R14", "R17"):
            skirting += 2 * (L + W)
    for k, v in finishes.items():
        q.append(("Floors", k, round(v * 0.0929, 1), "sq m", "Clear room areas; add 5-8% wastage"))
    q.append(("Floors", "Flush skirting, 4 in", round(skirting * 0.3048, 1), "m", "Room perimeters (dry rooms), doors not deducted"))
    for rid in ("R04", "R07", "R08"):
        L, W = clear_dims(room_of(rid))
        q.append(("Wet rooms", f"Wall tiles to 7 ft, {room_of(rid)[1]}", round((2 * (L + W) * 7 - 2.5 * 7) * 0.0929, 1), "sq m", "Full height in the shower adds ~2 sq m"))
        q.append(("Wet rooms", f"Waterproofing, {room_of(rid)[1]}", round((L * W + 2 * (L + W) * 1 + 6 * 6) * 0.0929, 1), "sq m", "Floor + 12 in upturn + shower walls to 7 ft"))
    q.append(("Kitchen", "Granite counter, 2 ft deep", round((10.7 + 7.0) * 0.3048, 1), "m", "South and east runs (F34, F35)"))
    q.append(("Kitchen", "Dado between counter and wall cabinets", round((10.7 + 7.0) * 2 * 0.0929, 1), "sq m", "2 ft high"))
    q.append(("Roof", "Sloped roof area (tiles, deck, insulation, membrane)", round(roof_area() * 0.0929, 1), "sq m", f"Hip outline / cos {ROOF['pitch']} deg; add ~8% for gable and laps"))
    x1, x2, y1, y2 = ROOF["hip"]
    q.append(("Roof", "Gutters", round(2 * (x2 - x1) * 0.3048, 1), "m", "Both long eaves"))
    q.append(("Roof", "Downpipes, 100 mm", len(ROOF["downpipes"]), "no.", "About 12 ft each"))
    q.append(("Roof", "Ridge and hip tiles", round(((x2 - x1) - (y2 - y1) + 4 * ((y2 - y1) / 2) * 1.414) * 0.3048, 1), "m", "Approximate"))
    q.append(("Site", "Plinth protection apron, 3 ft wide", round(((60.75 + 22.75) * 2 * 3 + 4 * 9) * 0.0929, 1), "sq m", "PCC with slope away"))
    q.append(("Openings", "Doors", len(DOORS), "no.", "See Doors tab"))
    q.append(("Openings", "Windows and vents", len(WINDOWS), "no.", "See Windows tab"))
    q.append(("Openings", "Window area (for mesh and grills)", round(sum((w[4] - w[3]) * (w[6] - w[5]) for w in WINDOWS) * 0.0929, 1), "sq m", ""))
    return q
