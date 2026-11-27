import pathlib
import re
import subprocess
import sys

SRC = pathlib.Path(__file__).resolve().parents[1]
ROOT = SRC.parent


def test_build_writes_every_output():
    r = subprocess.run([sys.executable, "build.py"], cwd=SRC, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-3000:]
    for rel in ("02_Drawings/PDF/KH-P1_Drawing_Set_RevB.pdf", "02_Drawings/CAD/KH-P1_A-102_Ground_Floor_Plan_RevB.dxf",
                "03_Schedules/KH-P1_Schedules_RevB.xlsx", "01_Brief/Room_Detailing_Guide.md", "04_3D/KH-P1_3D_Model.html"):
        assert (ROOT / rel).stat().st_size > 1000, rel


def test_3d_page_is_clean():
    html = (ROOT / "04_3D/KH-P1_3D_Model.html").read_text(encoding="utf-8")
    assert len(re.findall(r"/\*@MODEL\*/", html)) == 1
    assert "__walk" not in html


def test_pdf_has_every_sheet():
    import fitz  # PyMuPDF is in the venv used for page checks
    d = fitz.open(str(ROOT / "02_Drawings/PDF/KH-P1_Drawing_Set_RevB.pdf"))
    assert d.page_count == 26
    for i in (13, 14, 15):  # elevations and sections
        assert "COURTYARD" in d[i].get_text().upper() or "MUTRAM" in d[i].get_text().upper(), i


def test_elevations_and_sections_name_the_courtyard_in_the_drawing():
    """The brief's check is met by the title block alone ("Courtyard Concept"): look left of the title block."""
    import fitz
    d = fitz.open(str(ROOT / "02_Drawings/PDF/KH-P1_Drawing_Set_RevB.pdf"))
    for i in (13, 14, 15):
        r = d[i].rect
        t = d[i].get_text(clip=fitz.Rect(0, 0, r.width - 85 * 72 / 25.4, r.height)).upper()
        assert "COURTYARD" in t or "MUTRAM" in t, i
    assert d[15].get_text().count("MUTRAM (OPEN COURTYARD)") == 2


def test_no_duplex_leftovers_on_the_sheets():
    import fitz
    d = fitz.open(str(ROOT / "02_Drawings/PDF/KH-P1_Drawing_Set_RevB.pdf"))
    for i, p in enumerate(d):
        r = p.rect
        # the cover's decision-log column (from x 175 mm) quotes the duplex on purpose: check the rest of the cover
        t = (p.get_text(clip=fitz.Rect(0, 0, 174 * 72 / 25.4, r.height)) if i == 0 else p.get_text()).lower()
        for w in ("poomukham", "covered terrace", "front gable", "chaipu", "duplex option", "kitchen wing"):
            assert w not in t, (i, w)


def test_3d_model_has_courtyard_keys():
    import json
    html = (ROOT / "04_3D/KH-P1_3D_Model.html").read_text(encoding="utf-8")
    data = json.loads(re.search(r"/\*@MODEL\*/const MODEL=(.*?);/\*@END\*/", html, re.S).group(1))
    for k in ("court", "ring", "courtEave", "pillars", "jharokhas", "roofRing", "roofWing", "terrace"):
        assert k in data, k
    assert "porch" not in data["house"]


def test_dxf_first_floor_is_drawn_clear_of_the_ground_floor_plot():
    import ezdxf
    import make_dxf
    import model as M
    off = make_dxf.f1_offset()
    ys = [p[1] for p in M.PLOT]
    assert off > max(ys) - min(ys)                                   # the F1 plot outline starts north of the ground plot's
    d = ezdxf.readfile(str(ROOT / "02_Drawings/CAD/KH-P1_A-102_Ground_Floor_Plan_RevB.dxf"))
    plots = [e for e in d.modelspace().query("LWPOLYLINE") if e.dxf.layer in ("C-PROP", "C-PROP-SETB")]
    spans = sorted((min(p[1] for p in e.get_points()), max(p[1] for p in e.get_points())) for e in plots)
    assert len(spans) == 2 and spans[0][1] < spans[1][0], spans      # two plot outlines, one above the other, not overlapping


def _spans(page):
    import fitz
    out = []
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            horiz = abs(line["dir"][0]) > 0.5
            for sp in line["spans"]:
                t = sp["text"].strip()
                if not t:
                    continue
                r = fitz.Rect(sp["bbox"])
                if horiz:   # the glyph body only: line boxes of one paragraph overlap by their ascenders
                    h = r.height; r = fitz.Rect(r.x0 + 0.3, r.y0 + h * 0.25, r.x1 - 0.3, r.y1 - h * 0.25)
                else:
                    w = r.width; r = fitz.Rect(r.x0 + w * 0.25, r.y0 + 0.3, r.x1 - w * 0.25, r.y1 - 0.3)
                out.append((r, t))
    return out


def test_every_label_inside_the_frame_and_no_text_over_text():
    """Every sheet: all text inside the 10 mm frame, none crossing the title block's edge, no two pieces of text overlapping."""
    import fitz
    mm = 72 / 25.4
    d = fitz.open(str(ROOT / "02_Drawings/PDF/KH-P1_Drawing_Set_RevB.pdf"))
    bad = []
    for i, p in enumerate(d):
        W, H = p.rect.width, p.rect.height
        sp = _spans(p)
        for r, t in sp:
            if r.x0 < 10 * mm or r.x1 > W - 10 * mm or r.y0 < 10 * mm or r.y1 > H - 10 * mm or (r.x0 < W - 85 * mm < r.x1):
                bad.append((i + 1, "frame", t))
        for a in range(len(sp)):
            for b in range(a + 1, len(sp)):
                x = sp[a][0] & sp[b][0]
                if not x.is_empty and x.width > 0.4 and x.height > 0.4:
                    bad.append((i + 1, sp[a][1], sp[b][1]))
    assert not bad, bad[:10]


def _fill_polys(d):
    """Closed outlines of a filled path (rects, quads, line/curve runs)."""
    out, cur = [], []
    def flush():
        if len(cur) > 2: out.append(list(cur))
    for it in d["items"]:
        op = it[0]
        if op == "re":
            r = it[1]; out.append([(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)])
        elif op == "qu":
            q = it[1]; out.append([(q.ul.x, q.ul.y), (q.ur.x, q.ur.y), (q.lr.x, q.lr.y), (q.ll.x, q.ll.y)])
        elif op in ("l", "c"):
            a, b = it[1], it[-1]
            if cur and abs(cur[-1][0] - a.x) < 0.01 and abs(cur[-1][1] - a.y) < 0.01:
                cur.append((b.x, b.y))
            else:
                flush(); cur[:] = [(a.x, a.y), (b.x, b.y)]
    flush()
    return out


def _inside(pt, poly):
    x, y = pt; c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def test_no_text_is_painted_over_by_later_graphics():
    """A label must not be hidden under a filled shape drawn after it (a roof over a window tag, a stair over a room name).
    Knock-out and white grounds drawn BEFORE their text are fine: only fills later in the paint order count."""
    import fitz
    d = fitz.open(str(ROOT / "02_Drawings/PDF/KH-P1_Drawing_Set_RevB.pdf"))
    bad = []
    for i, p in enumerate(d):
        fills = [(g["seqno"], fitz.Rect(g["rect"]), _fill_polys(g)) for g in p.get_drawings() if g.get("fill") is not None]
        for sp in p.get_texttrace():
            t = "".join(chr(ch[0]) for ch in sp["chars"]).strip()
            if not t:
                continue
            r = fitz.Rect(sp["bbox"])
            pts = [(r.x0 + r.width * fx, r.y0 + r.height * fy) for fx in (0.12, 0.3, 0.5, 0.7, 0.88) for fy in (0.45, 0.75)]
            for sq, fr, polys in fills:
                if sq > sp["seqno"] and any(fr.contains(fitz.Point(*q)) for q in pts) and any(_inside(q, poly) for poly in polys for q in pts):
                    bad.append((i + 1, t)); break
    assert not bad, bad[:10]


def test_no_text_is_truncated_with_an_ellipsis():
    import fitz
    d = fitz.open(str(ROOT / "02_Drawings/PDF/KH-P1_Drawing_Set_RevB.pdf"))
    for i, p in enumerate(d):
        t = p.get_text()
        assert "..." not in t and "\u2026" not in t, (i + 1, [l for l in t.splitlines() if "..." in l][:3])


def test_sheet_text_quotes_no_model_coordinates():
    """Prose on the sheets speaks in words ("the 42 ft house", "the thinnai's south edge"), never in model coordinates
    such as "x 15-57", "(y 27-31)" or "74-97 x 45-49"."""
    import fitz
    pat = re.compile(r"(?<![A-Za-z])[xy] ?\d+(?:\.\d+)?\s?[-–]\s?\d+(?:\.\d+)?|\d+(?:\.\d+)?[-–]\d+(?:\.\d+)? x \d+(?:\.\d+)?[-–]\d+")
    d = fitz.open(str(ROOT / "02_Drawings/PDF/KH-P1_Drawing_Set_RevB.pdf"))
    bad = []
    for i, p in enumerate(d):
        t = p.get_text().replace("\n", " ")
        bad += [(i + 1, t[max(0, m.start() - 30):m.end() + 10]) for m in pat.finditer(t)]
    assert not bad, bad[:10]


def test_no_door_swing_arc_strikes_a_label():
    """Extends the painted-over check to strokes: a dashed door-swing arc must not run through a label (D48's arc struck the
    DB and linen size text on A-102). An arc drawn before a label that has a knock-out ground under it is hidden, so it is fine."""
    import fitz
    def bez(p0, p1, p2, p3, n=16):
        for k in range(n + 1):
            t = k / n; u = 1 - t
            yield (u ** 3 * p0.x + 3 * u * u * t * p1.x + 3 * u * t * t * p2.x + t ** 3 * p3.x,
                   u ** 3 * p0.y + 3 * u * u * t * p1.y + 3 * u * t * t * p2.y + t ** 3 * p3.y)
    d = fitz.open(str(ROOT / "02_Drawings/PDF/KH-P1_Drawing_Set_RevB.pdf"))
    bad = set()
    for i, p in enumerate(d):
        spans = []
        for sp in p.get_texttrace():
            t = "".join(chr(ch[0]) for ch in sp["chars"]).strip()
            if t:
                r = fitz.Rect(sp["bbox"])
                spans.append((fitz.Rect(r.x0 + 0.3, r.y0 + r.height * 0.25, r.x1 - 0.3, r.y1 - r.height * 0.1), t, sp["seqno"]))
        dr = p.get_drawings()
        fills = [(g["seqno"], fitz.Rect(g["rect"])) for g in dr if g.get("fill") is not None]
        for g in dr:
            if g.get("fill") is not None or not g.get("dashes") or g["dashes"].startswith("[] "):
                continue
            for it in g["items"]:
                if it[0] != "c":
                    continue
                for x, y in bez(*it[1:5]):
                    q = fitz.Point(x, y)
                    for rr, t, sq in spans:
                        if rr.contains(q) and not (g["seqno"] < sq and any(g["seqno"] < fs < sq and fr.contains(q) for fs, fr in fills)):
                            bad.add((i + 1, t))
    assert not bad, sorted(bad)[:10]
