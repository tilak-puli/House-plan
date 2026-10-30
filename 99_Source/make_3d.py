import json
import re
from geom import *

# Short labels where the full room name will not fit in the 3D view
LABELS = {"Walk-in wardrobe": "Walk-in", "Dressing alcove": "Dressing", "Wash link": "Wash basin"}
COVERED = {("Y", 54)}  # walls under the poomukham roof: no sunshades
FULL_HEIGHT_SILL = 1.0  # windows with a lower sill are cut through the wall


def model_data():
    xs = [c for a, c in EXTERIOR if a == "Y"]
    ys = [c for a, c in EXTERIOR if a == "X"]
    rooms = []
    for _, name, x1, x2, y1, y2, _ in ROOMS:
        label = LABELS.get(name, re.sub(r"\s*\(.*\)", "", name))
        rooms.append([label, (x1 + x2) / 2, (y1 + y2) / 2])
    doors = [{"id": d[0], "axis": d[1], "c": d[2], "s": d[3], "e": d[4], "sliding": d[5] == 0,
              "exterior": (d[1], d[2]) in EXTERIOR, "transom": TRANSOMS.get(d[0])} for d in DOORS]
    windows = []
    for w in WINDOWS:
        axis, c = w[1], w[2]
        lo = min(ys) if axis == "X" else min(xs)
        windows.append({"id": w[0], "axis": axis, "c": c, "s": w[3], "e": w[4], "sill": w[5], "head": w[6],
                        "dir": -1 if c == lo else 1, "cut": w[5] < FULL_HEIGHT_SILL,
                        "shade": (axis, c) not in COVERED,
                        "mat": "win" if axis == "X" and c == max(ys) else "jali"})
    furniture = [{"id": f[0], "x1": f[3], "x2": f[4], "y1": f[5], "y2": f[6]} for f in FURNITURE]
    furniture += [{"id": e[0], "x1": e[1], "x2": e[2], "y1": e[3], "y2": e[4]} for e in EXTRA_DRAW]
    feat = {f[0]: f[3] for f in SITE_FEATURES}
    return {"walls": [list(w) + [wall_t(w)] for w in WALLS], "doors": doors, "windows": windows,
            "jali": [list(j) for j in JALI_SCREENS], "pillars": [list(p) for p in PILLARS],
            "furniture": furniture, "rooms": rooms,
            "F": LEVELS["FFL"], "PF": LEVELS["poomukham"], "H": LEVELS["wall_top"], "riser": LEVELS["riser"],
            "site": {"w": SITE["w"], "strip": SITE["strip"]}, "gate": list(feat["GATE"][2:]),
            "roof": {"hip": list(ROOF["hip"]), "gable": list(ROOF["gable"]), "eave": round(eave_z(), 3), "lift": ROOF["gable_lift"],
                     "skylight": list(ROOF["skylight"]), "lantern": round(vent_top_z(), 3), "apex": round(vent_apex_z(), 3), "ventOver": ROOF["vent_overhang"]},
            "tank": {"rect": list(feat["TANK"]), "stand": LEVELS["tank_stand"]}, "pergola": list(feat["PERGOLA"]),
            "features": {"SEPTIC": list(feat["SEPTIC"]), "SUMP": list(feat["SUMP"]), "TULSI": list(feat["TULSI"][:2])},
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
