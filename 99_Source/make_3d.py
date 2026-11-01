import json
import re
from geom import *

# Short labels where the full room name will not fit in the 3D view
LABELS = {"Stair and passage": "Stair", "Outdoor lounge (covered)": "Outdoor lounge", "Upper master bedroom": "Upper master", "Covered terrace": "Covered terrace"}
COVERED = {("Y", 61)}  # walls under the poomukham roof (and, upstairs, above the front gable): no sunshades
FULL_HEIGHT_SILL = 1.0  # windows with a lower sill are cut through the wall


def floor_data():
    """Walls, openings, rooms, fittings and furniture of the floor currently swapped in."""
    xs = [c for a, c in EXTERIOR if a == "Y"]
    ys = [c for a, c in EXTERIOR if a == "X"]
    rooms = []
    for rid, name, x1, x2, y1, y2, _ in ROOMS:
        label = LABELS.get(name, re.sub(r"\s*\(.*\)", "", name))
        rooms.append([label, *ROOM_LABEL_AT.get(rid, ((x1 + x2) / 2, (y1 + y2) / 2))])
    doors = [{"id": d[0], "axis": d[1], "c": d[2], "s": d[3], "e": d[4], "sliding": d[5] == 0, "swing": d[5], "hingeEnd": d[0] in HINGE_AT_END,
              "kind": "bath" if "waterproof" in d[7].lower() else "glazed" if "glaz" in d[7].lower() else "carved" if "carved" in d[7].lower() else "teak",
              "exterior": (d[1], d[2]) in EXTERIOR and d[0] == "D01", "transom": TRANSOMS.get(d[0])} for d in DOORS]
    windows = []
    for w in WINDOWS:
        axis, c = w[1], w[2]
        lo = min(ys) if axis == "X" else min(xs)
        ext = (axis, c) in EXTERIOR
        windows.append({"id": w[0], "axis": axis, "c": c, "s": w[3], "e": w[4], "sill": w[5], "head": w[6],
                        "dir": -1 if c == lo else 1, "cut": w[5] < FULL_HEIGHT_SILL,
                        "shade": ext and (axis, c) not in COVERED and not (axis == "X" and c == max(ys)) and "clerestory" not in w[7].lower(),
                        "mat": "win" if (axis == "X" and c == max(ys)) or "glazed clerestory" in w[8].lower() or ("glazed" in w[8].lower() and "jali" not in w[8].lower() and not ext) else "jali"})
    floor_keys = (("Red oxide", "redoxide"), ("Matt vitrified 2x2", "vitrified"), ("Marble", "marble"), ("Anti-skid matt", "antiskid"),
                  ("Anti-skid ceramic", "ceramic"), ("Cuddapah", "cuddapah"), ("Flamed granite", "granite"), ("Terracotta", "antiskid"))
    room_rects = []
    for rid, name, x1, x2, y1, y2, _ in ROOMS:
        fin = FLOOR_FINISH.get(rid, "Red oxide")
        key = next((k for t, k in floor_keys if t in fin), "redoxide")
        ceil = CEILINGS.get(rid)
        room_rects.append({"id": rid, "x1": x1, "x2": x2, "y1": y1, "y2": y2, "floor": key, "fo": ROOM_FLOOR.get(rid, 0),
                           "ceil": ceil[1] if ceil and ceil[0] == "flat" else None})
    fixtures = [[p[0], p[1], p[2]] for p in PLUMBING if p[3] != "SITE"]
    elec = [[e[0], e[1], e[2], e[3]] for e in ELECTRICAL if e[0] in ("F", "L", "WL") and e[3] != "SITE"]
    furniture = [{"id": f[0], "x1": f[3], "x2": f[4], "y1": f[5], "y2": f[6]} for f in FURNITURE]
    furniture += [{"id": e[0], "x1": e[1], "x2": e[2], "y1": e[3], "y2": e[4]} for e in EXTRA_DRAW]
    return {"walls": [list(w) + [wall_t(w)] for w in WALLS], "doors": doors, "windows": windows, "furniture": furniture, "rooms": rooms,
            "roomRects": room_rects, "exterior": [[a, c] for a, c in sorted(EXTERIOR)], "fixtures": fixtures, "elec": elec,
            "rails": [list(r) for r in RAILS], "z": floor_base() }


def model_data():
    with on_floor("G"):
        g = floor_data()
    with on_floor("F1"):
        f1 = floor_data()
    feat = {f[0]: f[3] for f in SITE_FEATURES}
    return {**g, "f1": f1, "jali": [list(j) for j in JALI_SCREENS], "pillars": [list(p) for p in PILLARS],
            "F": LEVELS["FFL"], "PF": LEVELS["poomukham"], "H": LEVELS["wall_top"], "H1": LEVELS["upper_wall_top"], "riser": LEVELS["riser"],
            "slabT": LEVELS["slab"], "slab": [list(s) for s in SLAB_F1], "stair": STAIR, "posts": [list(p) for p in TERRACE_POSTS],
            "house": {"x1": 23, "x2": 67, "y1": 3, "y2": 25, "porch": [61, 67, 12.5, 25], "block": [23, 61]},
            "site": {"w": SITE["w"], "strip": SITE["strip"], "trial": SITE["trial"]}, "gate": list(feat["GATE"][2:]),
            "roof": {"hip": list(ROOF["hip"]), "gable": list(ROOF["gable"]), "eave": round(eave_z(), 3), "geave": round(gable_eave_z(), 3),
                     "skylight": list(ROOF["skylight"]), "lantern": round(vent_top_z(), 3), "apex": round(vent_apex_z(), 3), "ventOver": ROOF["vent_overhang"]},
            "pergola": list(feat["PERGOLA"]),
            "features": {"SEPTIC": list(feat["SEPTIC"]), "SUMP": list(feat["SUMP"]), "TULSI": list(feat["TULSI"][:2]), "STEPS": list(feat["STEPS"]), "WSTEP": list(feat["WSTEP"]),
                         "SOAK": list(feat["SOAK"]), **{k: list(feat[k]) for k in ("PATH", "HEDGE1", "HEDGE2", "HEDGE3") if k in feat}},
            "trees": [list(t) for t in TREES]}


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
