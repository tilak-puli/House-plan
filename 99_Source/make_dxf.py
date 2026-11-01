import math
import ezdxf
from ezdxf import units
from geom import *

MM = 304.8  # mm per ft
OFF = [0.0]  # north offset of the floor being drawn (first floor is drawn 40 ft north of the ground floor)


def P(x, y):
    return (x * MM, (y + OFF[0]) * MM)


def make(path):
    doc = ezdxf.new("R2010", setup=True)
    doc.units = units.MM
    doc.header["$INSUNITS"] = 4
    layers = {
        "C-PROP": 1, "C-PROP-SETB": 8, "A-WALL": 7, "A-WALL-PATT": 8, "A-DOOR": 3, "A-GLAZ": 4,
        "A-JALI": 30, "A-COLS": 32, "A-FURN": 140, "A-FLOR-FIXT": 150, "A-AREA-IDEN": 2,
        "A-ANNO-DIMS": 1, "A-ANNO-TEXT": 7, "A-ROOF-OTLN": 9, "L-PLNT": 94, "A-SITE": 8,
        "A-WALL-EXT": 7, "A-WALL-WET": 5, "A-WALL-INT": 8, "E-LITE": 2, "E-POWR": 1,
        "P-FIXT": 4, "P-DOMW": 5, "P-SANR": 34, "P-SANR-GREY": 94, "P-STRM": 140,
    }
    for name, col in layers.items():
        doc.layers.add(name, color=col)
    doc.layers.get("A-ROOF-OTLN").dxf.linetype = "DASHED"
    doc.layers.get("C-PROP-SETB").dxf.linetype = "DASHED"
    msp = doc.modelspace()

    def rect(x1, x2, y1, y2, layer, close=True):
        return msp.add_lwpolyline([P(x1, y1), P(x2, y1), P(x2, y2), P(x1, y2)], close=close, dxfattribs={"layer": layer})

    def text(s, x, y, h=120, layer="A-ANNO-TEXT", align="MIDDLE_CENTER"):
        t = msp.add_text(s, height=h, dxfattribs={"layer": layer, "style": "OpenSans"})
        t.set_placement(P(x, y), align=ezdxf.enums.TextEntityAlignment[align])
        return t

    # site
    W, S = SITE["w"], SITE["strip"]
    rect(0, SITE["l"], 0, W + S, "C-PROP-SETB")
    rect(0, SITE["l"], 0, W, "C-PROP")
    rect(SITE["trial"], SITE["l"], 0, W, "C-PROP-SETB")
    rect(*ROOF["hip"], "A-ROOF-OTLN")
    rect(*ROOF["gable"], "A-ROOF-OTLN")
    text(f"PLOT {W}' x {SITE['l']}'", 35, 1.2, 150, "A-ANNO-TEXT")
    if S: text(f"NORTH STRIP {S}' x {SITE['l']}' (PHASE 2 SITE)", 35, W + 1.5, 150)
    text("EAST ROAD", 81, W / 2, 200)
    for fid, label, kind, g in SITE_FEATURES:
        if kind == "rect":
            rect(*g, "A-SITE"); text(fid, (g[0] + g[1]) / 2, (g[2] + g[3]) / 2, 70)
        elif kind == "circle":
            msp.add_circle(P(g[0], g[1]), g[2] * MM, dxfattribs={"layer": "A-SITE"}); text(fid, g[0], g[1] + g[2] + 0.5, 70)
    for x, y, r in TREES:
        msp.add_circle(P(x, y), r * MM, dxfattribs={"layer": "L-PLNT"})

    for fl, dy in (("G", 0.0), ("F1", 40.0)):
        OFF[0] = dy
        with on_floor(fl):
            _floor(msp, rect, text, fl)
    OFF[0] = 0.0
    doc.saveas(path)


def _floor(msp, rect, text, fl):
    if fl == "F1":
        text("FIRST FLOOR PLAN (drawn 40 ft north of the ground floor)", 45, -2.5, 220)
        rect(0, SITE["l"], 0, SITE["w"], "C-PROP-SETB")
    # services (schematic points and runs)
    for code, x, y, rid, note in ELECTRICAL:
        msp.add_circle(P(x, y), 0.3 * MM, dxfattribs={"layer": "E-POWR" if code not in ("L", "WL", "F", "EF", "S", "GL") else "E-LITE"})
        text(code, x, y - 0.55, 50, "E-POWR" if code not in ("L", "WL", "F", "EF", "S", "GL") else "E-LITE")
    for code, x, y, rid, note in PLUMBING:
        msp.add_circle(P(x, y), 0.3 * MM, dxfattribs={"layer": "P-FIXT"}); text(code, x, y - 0.55, 50, "P-FIXT")
    for kind, pts in PIPES:
        msp.add_lwpolyline([P(*q) for q in pts], dxfattribs={"layer": {"supply": "P-DOMW", "soil": "P-SANR", "grey": "P-SANR-GREY", "rain": "P-STRM"}[kind]})

    # walls with solid poche
    for (x1, x2, y1, y2), wt in wall_rects(with_type=True):
        rect(x1, x2, y1, y2, f"A-WALL-{wt}")
        h = msp.add_hatch(color={"EXT": 250, "WET": 5, "INT": 8}[wt], dxfattribs={"layer": "A-WALL-PATT"})
        h.paths.add_polyline_path([P(x1, y1), P(x2, y1), P(x2, y2), P(x1, y2)], is_closed=True)
    for axis, c, s, e in JALI_SCREENS:
        x1, x2, y1, y2 = seg_rect(axis, c, s, e)
        rect(x1, x2, y1 + 0.2, y2 - 0.2, "A-JALI")
    for x, y in PILLARS:
        msp.add_circle(P(x, y), 0.36 * MM, dxfattribs={"layer": "A-COLS"})
    for axis, c, s, e in RAILS:
        rect(*seg_rect(axis, c, s, e, 0.25), "A-WALL-INT")
    st = STAIR
    for key in ("flight1", "flight2"):
        x1, x2, y1, y2, n = st[key]
        rect(x1, x2, y1, y2, "A-FLOR-FIXT")
        for i in range(1, n - 1):
            yy = y1 + i * st["tread"] if key == "flight1" else y2 - i * st["tread"]
            msp.add_line(P(x1, yy), P(x2, yy), dxfattribs={"layer": "A-FLOR-FIXT"})
    rect(*st["landing"], "A-FLOR-FIXT")

    # openings
    for (x1, x2, y1, y2), kind, rec, axis, c, a, b in opening_rects():
        if kind == "window":
            rect(x1, x2, y1, y2, "A-GLAZ")
            if axis == "X":
                msp.add_line(P(a, c), P(b, c), dxfattribs={"layer": "A-GLAZ"})
                tag_xy = (a + b) / 2, c + (1.2 if c >= 25 else -1.2)
            else:
                msp.add_line(P(c, a), P(c, b), dxfattribs={"layer": "A-GLAZ"})
                tag_xy = c + (1.4 if c >= 61 else -1.4), (a + b) / 2
            text(rec[0], *tag_xy, 90, "A-GLAZ")
        else:
            did, _, _, s0, e0, sw, *_ = rec
            w = e0 - s0
            if sw == 0:
                off = 0.12
                msp.add_line(P(s0, c - off), P(s0 + w * 0.55, c - off), dxfattribs={"layer": "A-DOOR"})
                msp.add_line(P(e0 - w * 0.55, c + off), P(e0, c + off), dxfattribs={"layer": "A-DOOR"})
                text(did, (s0 + e0) / 2, c - 1.0, 80, "A-DOOR")
                continue
            h = e0 if did in HINGE_AT_END else s0
            if axis == "X":
                hinge = (h, c)
                msp.add_line(P(*hinge), P(h, c + sw * w), dxfattribs={"layer": "A-DOOR"})
                start = (90 if sw > 0 else 180) if h == e0 else (0 if sw > 0 else 270)
                end = start + 90
                msp.add_arc(P(*hinge), w * MM, start, end, dxfattribs={"layer": "A-DOOR"})
                text(did, (s0 + e0) / 2, c + sw * (w * 0.45), 80, "A-DOOR")
            else:
                hinge = (c, h)
                msp.add_line(P(*hinge), P(c + sw * w, h), dxfattribs={"layer": "A-DOOR"})
                start = (270 if sw > 0 else 180) if h == e0 else (0 if sw > 0 else 90)
                end = start + 90
                msp.add_arc(P(*hinge), w * MM, start, end, dxfattribs={"layer": "A-DOOR"})
                text(did, c + sw * (w * 0.45), (s0 + e0) / 2, 80, "A-DOOR")

    # furniture and fixtures
    def furn(fid, x1, x2, y1, y2, shape):
        layer = "A-FLOR-FIXT" if shape in ("wc", "glass") or "basin" in fid.lower() else "A-FURN"
        if shape == "circle":
            msp.add_circle(P((x1 + x2) / 2, (y1 + y2) / 2), (x2 - x1) / 2 * MM, dxfattribs={"layer": layer})
        else:
            rect(x1, x2, y1, y2, layer)
    for f in FURNITURE:
        furn(f[0], f[3], f[4], f[5], f[6], f[9])
        if (f[4] - f[3]) * (f[6] - f[5]) > 4:
            text(f[0], (f[3] + f[4]) / 2, (f[5] + f[6]) / 2, 70, "A-FURN")
    shapes = {f[0]: f[9] for f in FURNITURE}
    for fid, x1, x2, y1, y2 in EXTRA_DRAW:
        furn(fid, x1, x2, y1, y2, shapes[fid])

    # room tags
    for r in ROOMS:
        rid, name, x1, x2, y1, y2, _ = r
        cx, cy = ROOM_LABEL_AT.get(rid, ((x1 + x2) / 2, (y1 + y2) / 2))
        text(name.upper(), cx, cy + 0.45, 110, "A-AREA-IDEN")
        L, W = clear_dims(r)
        text(f"{fmt_ft(L)} x {fmt_ft(W)} clear", cx, cy - 0.35, 80, "A-AREA-IDEN")

    # dimensions
    dim = {"layer": "A-ANNO-DIMS"}
    override = {"dimtxt": 120, "dimasz": 80, "dimexe": 40, "dimexo": 40, "dimdec": 0, "dimrnd": 5}
    def hdim(a, b, y, base):
        d = msp.add_linear_dim(base=P(a, base), p1=P(a, y), p2=P(b, y), dimstyle="EZ_MM_100_H25_CM", override=override, dxfattribs=dim)
        d.render()
    def vdim(a, b, x, base):
        d = msp.add_linear_dim(base=P(base, a), p1=P(x, a), p2=P(x, b), angle=90, dimstyle="EZ_MM_100_H25_CM", override=override, dxfattribs=dim)
        d.render()
    xs = sorted({w[1] for w in WALLS if w[0] == "Y"})
    ys = sorted({w[1] for w in WALLS if w[0] == "X"})
    hdim(xs[0], xs[-1], ys[-1], ys[-1] + 4.5)
    vdim(ys[0], ys[-1], xs[-1], xs[-1] + 5)
    for a, b in zip(xs, xs[1:]):
        hdim(a, b, ys[0], ys[0] - 2)
    if fl == "G":
        vdim(0, 3, 17, 13.5); vdim(25, SITE["w"], 17, 13.5)
        hdim(SITE["trial"], 17, 3, -5); hdim(67, 75, 3, -5)


if __name__ == "__main__":
    from paths import DXF
    make(str(DXF))
