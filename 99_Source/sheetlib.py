"""Shared drawing toolkit for the PDF set: sheet frame, plan and elevation mappers, tables."""
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from geom import *
from geom import _edge_t

PW, PH = landscape(A3)
INK = colors.HexColor("#1E1E1E")
GREY = colors.HexColor("#8A8A8A")
LIGHT = colors.HexColor("#D9D9D9")
ACC = colors.HexColor("#2F6B4F")
BLUE = colors.HexColor("#2D6FB0")
RED = colors.HexColor("#B4442E")
BROWN = colors.HexColor("#7A5230")
WHITE = colors.white
WALL_FILL = {"EXT": INK, "WET": colors.HexColor("#4A4A4A"), "INT": colors.HexColor("#8C8C8C")}
DRAW_W = PW - 95 * mm  # usable width left of the title block
PLAN_OX, PLAN_OY = 17.4 * mm, 47 * mm   # the house plans at 1:75: the compact house x 15-57 with the thinnai and its steps to x 64, y 4-46, clear of the legend


class Sheet:
    def __init__(self, c, num, title, scale):
        self.c, self.num, self.title, self.scale = c, num, title, scale
        self.frame()

    def frame(self):
        c = self.c
        c.setStrokeColor(INK); c.setLineWidth(0.8)
        c.rect(10 * mm, 10 * mm, PW - 20 * mm, PH - 20 * mm)
        x0 = PW - 85 * mm
        c.line(x0, 10 * mm, x0, PH - 10 * mm)
        y = PH - 22 * mm
        size = 13
        while c.stringWidth(PROJECT["name"], "Helvetica-Bold", size) > 68 * mm and size > 8:
            size -= 0.25
        c.setFillColor(INK); c.setFont("Helvetica-Bold", size)
        c.drawString(x0 + 5 * mm, y, PROJECT["name"])
        c.setFont("Helvetica", 8.5); c.setFillColor(GREY)
        for k, line in enumerate(PROJECT["title_lines"]):
            c.drawString(x0 + 5 * mm, y - (6 + 5 * k) * mm, line)
        rows = [("Stage", PROJECT["stage"]), ("Drawing", self.title), ("Sheet", self.num), ("Scale", self.scale + (" at A3" if ":" in self.scale else "")),
                ("Revision", PROJECT["rev"]), ("Date", PROJECT["date"]), ("Units", "Feet-inches; levels from finished ground")]
        yy = 60 * mm
        for k, v in rows:
            c.setFillColor(GREY); c.setFont("Helvetica", 7.5); c.drawString(x0 + 5 * mm, yy, k)
            font = "Helvetica-Bold" if k in ("Drawing", "Sheet") else "Helvetica"
            size = 14 if k == "Sheet" else 9
            while k != "Sheet" and c.stringWidth(v, font, size) > 47 * mm and size > 5.5:
                size -= 0.25
            c.setFillColor(INK); c.setFont(font, size)
            c.drawString(x0 + 25 * mm, yy, v)
            yy -= 6.5 * mm if k != "Sheet" else 8 * mm
            c.setStrokeColor(LIGHT); c.setLineWidth(0.3); c.line(x0 + 5 * mm, yy + 4 * mm, PW - 15 * mm, yy + 4 * mm)
        notes = ["Pre-construction draft for review by the",
                 "architect, structural engineer, MEP and",
                 "Vastu consultant. Not for construction",
                 "or approval until checked and signed.",
                 "Verify all dimensions and levels on site.",
                 "Prepared with AI assistance (Claude)."]
        c.setFillColor(GREY); c.setFont("Helvetica", 7.5)
        ny = 112 * mm
        for n in notes:
            c.drawString(x0 + 5 * mm, ny, n); ny -= 4 * mm
        c.setFillColor(INK)

    def note(self, text, x, y, size=8, color=INK, font="Helvetica", anchor="l"):
        c = self.c; c.setFillColor(color); c.setFont(font, size)
        {"l": c.drawString, "c": c.drawCentredString, "r": c.drawRightString}[anchor](x, y, text)

    def para(self, html, x, ytop, width, size=7.5, leading=None):
        st = ParagraphStyle("p", fontName="Helvetica", fontSize=size, leading=leading or size * 1.3)
        p = Paragraph(html, st); w, h = p.wrap(width, 400 * mm); p.drawOn(self.c, x, ytop - h); return h

    def bullets(self, items, x, ytop, width, size=7.2, title=None):
        y = ytop
        if title:
            self.note(title, x, y - 3 * mm, 9, INK, "Helvetica-Bold"); y -= 6 * mm
        for it in items:
            y -= self.para("&bull; " + it, x, y, width, size) + 1 * mm
        return ytop - y

    def table(self, data, widths, x, ytop, title=None, size=6.5):
        st = ParagraphStyle("t", fontName="Helvetica", fontSize=size, leading=size * 1.17)
        sb = ParagraphStyle("b", fontName="Helvetica-Bold", fontSize=size, leading=size * 1.17)
        if title:
            self.note(title, x, ytop + 2 * mm, 9, INK, "Helvetica-Bold")
        rows = [[Paragraph(str(v), sb if i == 0 else st) for v in r] for i, r in enumerate(data)]
        t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
        t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.2, LIGHT),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2)]))
        w, h = t.wrap(0, 0); t.drawOn(self.c, x, ytop - h); return h

    def legend(self, items, x, y, size=6.5):
        """items: list of (draw_fn(x, y), label)."""
        for fn, label in items:
            fn(x, y + 1 * mm); self.note(label, x + 8 * mm, y, size); y -= 4.5 * mm
        return y


def window_tag_xy(rec, axis, cc, a, b):
    """Where a window's tag sits on plan: outside an outer wall, on the room side of an inner one."""
    if axis == "X":
        return (a + b) / 2, cc + (1.25 if cc >= CY else -1.25) * (1 + PLANTER_GRILLES.get(rec[0], 0) / 1.25 * 0.9)
    outer = min(abs(cc - HX1), abs(cc - HX2)) < 0.5
    sg = 1 if (cc >= CX) == outer else -1
    bay = next((j for j in (JHAROKHAS if FLOOR[0] == "F1" else []) if j[0] - 0.1 <= cc + sg * 0.5 <= j[1] + 0.1 and j[2] <= (a + b) / 2 <= j[3]), None)
    if bay:   # the jharokha bay covers the usual spot: tag past its outer face
        return (bay[1] + 1.0 if sg > 0 else bay[0] - 1.0), (a + b) / 2
    return cc + sg * 1.5, (a + b) / 2


class Plan:
    """Maps plan feet to page coordinates, north up."""
    def __init__(self, sheet, scale_den, ox, oy):
        self.s = sheet; self.c = sheet.c
        self.k = 304.8 / scale_den * mm
        self.ox, self.oy = ox, oy

    def p(self, x, y):
        return self.ox + x * self.k, self.oy + y * self.k

    def rect(self, x1, x2, y1, y2, stroke=INK, fill=None, lw=0.4, dash=None):
        c = self.c; a = self.p(x1, y1); b = self.p(x2, y2)
        if stroke is not None: c.setStrokeColor(stroke)
        c.setLineWidth(lw)
        c.setDash(list(dash), 0) if dash else c.setDash()
        if fill is not None: c.setFillColor(fill)
        c.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=1 if stroke else 0, fill=1 if fill is not None else 0)
        c.setDash()

    def line(self, x1, y1, x2, y2, lw=0.3, color=INK, dash=None):
        c = self.c; c.setStrokeColor(color); c.setLineWidth(lw)
        c.setDash(list(dash), 0) if dash else c.setDash()
        a = self.p(x1, y1); b = self.p(x2, y2); c.line(a[0], a[1], b[0], b[1]); c.setDash()

    def poly(self, pts, lw=0.4, color=INK, dash=None, close=False, fill=None):
        c = self.c; c.setStrokeColor(color); c.setLineWidth(lw)
        c.setDash(list(dash), 0) if dash else c.setDash()
        path = c.beginPath(); path.moveTo(*self.p(*pts[0]))
        for q in pts[1:]: path.lineTo(*self.p(*q))
        if close: path.close()
        if fill is not None: c.setFillColor(fill)
        c.drawPath(path, stroke=1, fill=1 if fill is not None else 0); c.setDash()

    def circle(self, x, y, r, lw=0.4, color=INK, fill=None, dash=None):
        c = self.c; c.setStrokeColor(color); c.setLineWidth(lw)
        c.setDash(list(dash), 0) if dash else c.setDash()
        a = self.p(x, y)
        if fill is not None: c.setFillColor(fill)
        c.circle(a[0], a[1], r * self.k, stroke=1, fill=1 if fill is not None else 0); c.setDash()

    def text(self, s, x, y, size=7, font="Helvetica", color=INK, anchor="c"):
        a = self.p(x, y); self.s.note(s, a[0], a[1] - size * 0.35, size, color, font, anchor)

    def walls(self, fill=None, typed=True):
        for (x1, x2, y1, y2), wt in wall_rects(with_type=True):
            self.rect(x1, x2, y1, y2, stroke=None, fill=fill or (WALL_FILL[wt] if typed else INK))
        for w in BELOW_STAIR_WALLS:  # walls under the landing, below the cut: dashed outline
            if w in WALLS:
                x1, x2, y1, y2 = seg_rect(w[0], w[1], w[2], w[3], wall_t(w))
                self.rect(x1, x2, y1, y2, stroke=None, fill=WHITE)
                self.rect(x1, x2, y1, y2, stroke=GREY, lw=0.4, dash=(1.5, 1))
        for axis, c, s, e in JALI_SCREENS:
            x1, x2, y1, y2 = seg_rect(axis, c, s, e)
            self.rect(x1, x2, y1 + 0.15, y2 - 0.15, stroke=INK, lw=0.4, dash=(1, 1))
        for axis, c, s, e in FUTURE_WALLS:  # possible later wall, drawn dashed
            x1, x2, y1, y2 = seg_rect(axis, c, s, e, WALL_TYPES["INT"][0])
            self.rect(x1, x2, y1, y2, stroke=GREY, lw=0.5, dash=(2, 1.5))
        for x, y in PILLARS:
            self.circle(x, y, 0.36, lw=0.6, fill=WHITE)

    def openings(self, tags=True):
        c = self.c
        for (x1, x2, y1, y2), kind, rec, axis, cc, a, b in opening_rects():
            if kind == "window":
                if rec[0] == "W06":
                    self.rect(x1, x2, y1, y2, lw=0.4)
                    n = int((b - a) / 0.5)
                    for i in range(n):
                        self.line(a + i * 0.5, y1, a + i * 0.5 + 0.5, y2, lw=0.25)
                else:
                    self.rect(x1, x2, y1, y2, lw=0.4)
                    if axis == "X": self.line(a, cc, b, cc, lw=0.3)
                    else: self.line(cc, a, cc, b, lw=0.3)
                    dp = PLANTER_GRILLES.get(rec[0])
                    if dp and axis == "X":  # planter box grille outside the window
                        sg = 1 if cc >= 25 else -1
                        y0 = cc + sg * 0.375
                        self.rect(a - 0.15, b + 0.15, min(y0, y0 + sg * dp), max(y0, y0 + sg * dp), lw=0.35, fill=colors.HexColor("#E3EDD6"))
                        self.line(a - 0.15, y0 + sg * dp * 0.5, b + 0.15, y0 + sg * dp * 0.5, lw=0.2, color=GREY)
                if tags:
                    self.text(rec[0], *window_tag_xy(rec, axis, cc, a, b), 5.5, color=ACC)
            else:
                did, _, _, s0, e0, sw, *_ = rec
                w = e0 - s0
                if sw == 0:
                    if axis == "X":
                        self.line(s0, cc - 0.13, s0 + w * 0.55, cc - 0.13, lw=0.6)
                        self.line(e0 - w * 0.55, cc + 0.13, e0, cc + 0.13, lw=0.6)
                        if tags: self.text(did, (s0 + e0) / 2, cc - 0.9, 5.5, color=ACC)
                    else:
                        self.line(cc - 0.13, s0, cc - 0.13, s0 + w * 0.55, lw=0.6)
                        self.line(cc + 0.13, e0 - w * 0.55, cc + 0.13, e0, lw=0.6)
                        if tags: self.text(did, cc - 1.1, (s0 + e0) / 2, 5.5, color=ACC)
                    continue
                c.setStrokeColor(INK); c.setLineWidth(0.25)
                if "double" in rec[7].lower():   # two leaves, each half the opening, hinged at both jambs
                    hw = w / 2
                    for h, st0 in ((s0, None), (e0, None)):
                        if axis == "X":
                            self.line(h, cc, h, cc + sw * hw, lw=0.5)
                            st = (0 if sw > 0 else 270) if h == s0 else (90 if sw > 0 else 180)
                            hx, hy = self.p(h, cc)
                        else:
                            self.line(cc, h, cc + sw * hw, h, lw=0.5)
                            st = (0 if sw > 0 else 90) if h == s0 else (270 if sw > 0 else 180)
                            hx, hy = self.p(cc, h)
                        r = hw * self.k
                        c.setStrokeColor(INK); c.setLineWidth(0.25)
                        c.setDash(1.5, 1); c.arc(hx - r, hy - r, hx + r, hy + r, st, 90); c.setDash()
                    if tags:
                        tx, ty = ((s0 + e0) / 2, cc - sw * 0.9) if axis == "X" else (cc - sw * 1.1, (s0 + e0) / 2)   # on the side away from the leaves
                        self.text(did, tx, ty, 5.5, color=ACC)
                    continue
                h = e0 if did in HINGE_AT_END else s0
                if axis == "X":
                    hx, hy = self.p(h, cc)
                    self.line(h, cc, h, cc + sw * w, lw=0.5)
                    st = (90 if sw > 0 else 180) if h == e0 else (0 if sw > 0 else 270)
                    tx, ty = (s0 + e0) / 2, cc + sw * w * 0.4
                else:
                    hx, hy = self.p(cc, h)
                    self.line(cc, h, cc + sw * w, h, lw=0.5)
                    st = (270 if sw > 0 else 180) if h == e0 else (0 if sw > 0 else 90)
                    tx, ty = cc + sw * w * 0.4, (s0 + e0) / 2
                r = w * self.k
                c.setDash(1.5, 1); c.arc(hx - r, hy - r, hx + r, hy + r, st, 90); c.setDash()
                if tags: self.text(did, tx, ty, 5.5, color=ACC)   # a low hatch (under the 7 ft band) is named in its room and on A-401

    def door_boxes(self):
        """Plan boxes (x1, x2, y1, y2) a room label must keep clear of: each door's swing and its tag, and each window's tag."""
        out = []
        for (x1, x2, y1, y2), kind, rec, axis, cc, a, b in opening_rects():
            if kind == "window":
                tx, ty = window_tag_xy(rec, axis, cc, a, b)
                out.append((tx - 1.0, tx + 1.0, ty - 0.45, ty + 0.45))
        for d in DOORS:
            did, axis, cc, s0, e0, sw = d[:6]
            w = e0 - s0
            if sw == 0:
                tx, ty = ((s0 + e0) / 2, cc - 0.9) if axis == "X" else (cc - 1.1, (s0 + e0) / 2)
                out.append((tx - 1.0, tx + 1.0, ty - 0.45, ty + 0.45))
                continue
            dep = w / 2 if "double" in d[7].lower() else w
            if "double" in d[7].lower():   # its tag sits on the other side of the wall
                tx, ty = ((s0 + e0) / 2, cc - sw * 0.9) if axis == "X" else (cc - sw * 1.1, (s0 + e0) / 2)
                out.append((tx - 1.0, tx + 1.0, ty - 0.45, ty + 0.45))
            if axis == "X":
                out.append((s0, e0, min(cc, cc + sw * dep), max(cc, cc + sw * dep)))
            else:
                out.append((min(cc, cc + sw * dep), max(cc, cc + sw * dep), s0, e0))
        return out

    def label_spot(self, r, w_ft, h_up, h_dn, start=None, strict=False):
        """A point in room r for a label w_ft wide reaching h_up above and h_dn below it, clear of doors where possible."""
        rid, _, x1, x2, y1, y2, _ = r
        cx, cy = start or ROOM_LABEL_AT.get(rid, ((x1 + x2) / 2, (y1 + y2) / 2))
        boxes = self.door_boxes()
        f1, f2 = x1 + max(_edge_t("Y", x1, y1, y2), 0.15), x2 - max(_edge_t("Y", x2, y1, y2), 0.15)   # the room's wall faces
        g1, g2 = y1 + max(_edge_t("X", y1, x1, x2), 0.15), y2 - max(_edge_t("X", y2, x1, x2), 0.15)
        def clear(px, py):
            a1, a2, b1, b2 = px - w_ft / 2, px + w_ft / 2, py - h_dn, py + h_up
            if a1 < f1 + 0.15 or a2 > f2 - 0.15 or b1 < g1 + 0.15 or b2 > g2 - 0.15:
                return False
            return not any(a1 < q2 and a2 > q1 and b1 < q4 and b2 > q3 for q1, q2, q3, q4 in boxes)
        steps = [0]
        for k in range(1, 9):
            steps += [k * 0.6, -k * 0.6]
        for dy in steps:
            for dx in (0, 1.0, -1.0, 2.0, -2.0, 3.0, -3.0, 3.5, -3.5, 4.5, -4.5, 6.0, -6.0):
                if clear(cx + dx, cy + dy):
                    return cx + dx, cy + dy
        return None if strict else (cx, cy)

    def fit(self, text, font, size, width_ft, smallest=3.6):
        """Font size at or below size that fits text in width_ft."""
        while size > smallest and self.c.stringWidth(text, font, size) > width_ft * self.k - 1.2 * mm:
            size -= 0.2
        return size

    def halo_text(self, s, x, y, size, font="Helvetica", color=INK):
        """Centred text on a white ground, so tread lines and hatching do not run through it."""
        a = self.p(x, y); w = self.c.stringWidth(s, font, size)
        self.c.setFillColor(WHITE); self.c.rect(a[0] - w / 2 - 0.4 * mm, a[1] - size * 0.42, w + 0.8 * mm, size * 0.95, stroke=0, fill=1)
        self.text(s, x, y, size, font, color)

    def vtext(self, s, x, y, size, font="Helvetica-Bold", color=INK, halo=True):
        """Text turned to read up the page (along a north-south flight), centred on (x, y), on a white ground."""
        px, py = self.p(x, y); c = self.c; w = c.stringWidth(s, font, size)
        c.saveState(); c.translate(px, py); c.rotate(90)
        if halo:
            c.setFillColor(WHITE); c.rect(-w / 2 - 0.4 * mm, -size * 0.42, w + 0.8 * mm, size * 0.95, stroke=0, fill=1)
        c.setFillColor(color); c.setFont(font, size); c.drawCentredString(0, -size * 0.35, s); c.restoreState()

    def stair_label(self, sub=None, sub_color=GREY):
        """The stair's name (and size) turned along flight 1, west of its UP arrow: never on the arrow."""
        x1, x2 = STAIR["flight1"][0], STAIR["flight1"][1]
        mx = (x1 + x2) / 2; cy = (STAIR["flight1"][2] + STAIR["flight1"][3]) / 2 + 0.6
        self.vtext("STAIR", x1 + (mx - x1) * (0.62 if sub else 0.5), cy, 5.5)
        if sub:
            self.vtext(sub, x1 + (mx - x1) * 0.25, cy, 4.2, "Helvetica", sub_color)

    def room_names(self, size=5.5, color=GREY, corner=False, sub=None, avoid=(), skip=(), halo=False, drop_blocked=False, min_size=0):
        for r in ROOMS:
            rid, name, x1, x2, y1, y2, _ = r
            if rid in skip: continue
            nm = short_name(name)
            if corner:
                if x2 - x1 < 3: continue  # a strip (the storage wall): its furniture tags say what it is
                lx, ly = x1 + 0.4, y2 - 0.7
                for o in ROOMS:  # a smaller room in the same corner (Bath 2 in Bedroom 2): label past it
                    if o is not r and o[2] <= lx <= o[3] and o[4] <= ly <= o[5] and (o[3] - o[2]) * (o[5] - o[4]) < (x2 - x1) * (y2 - y1):
                        lx = o[3] + 0.4
                def spots_for(sz):
                    wf = self.c.stringWidth(nm, "Helvetica", sz) / self.k
                    mx = (x1 + x2 - wf) / 2
                    return wf, ((lx, ly), (lx, y1 + 0.6), (x2 - 0.4 - wf, ly), (x2 - 0.4 - wf, y1 + 0.6),    # a free corner: clear of furniture tags
                                (mx, ly), (mx, y1 + 0.6), (lx, (y1 + y2) / 2), (x2 - 0.4 - wf, (y1 + y2) / 2),   # else the middle of a side
                                (lx, ly - 0.8), (x2 - 0.4 - wf, ly - 0.8), (lx, y1 + 1.4), (x2 - 0.4 - wf, y1 + 1.4),
                                (x1 + 0.3, (y1 + y2) / 2))   # last: tight to the wall, mid-side
                def free(av, wf, spots, hh):
                    return next(((px, py) for px, py in spots
                                 if not any(px < q2 and px + wf > q1 and py - hh < q4 and py + hh > q3 for q1, q2, q3, q4 in av)), None)
                sz = max(min_size, self.fit(nm, "Helvetica", size, x2 - lx - 0.2))
                wf, spots = spots_for(sz)
                hh = max(0.35, sz * 0.45 / self.k)   # half the text's height, in ft at this scale
                spot, doors = free(list(avoid), wf, spots, hh), self.door_boxes()
                if spot is None or any(spot[0] < q2 and spot[0] + wf > q1 and spot[1] - hh < q4 and spot[1] + hh > q3 for q1, q2, q3, q4 in doors):
                    # a door swing's square would take the name there: clear of the swings too if a spot allows (the name a size or two
                    # smaller if need be); else keep the spot clear of the tags, or (none at all, as under the stair's treads on A-104) the first
                    # spot clear of the swings
                    alt = None
                    for k in (1.0, 0.85):
                        if sz * k < min_size - 1e-9:
                            continue
                        wk, sk = spots_for(sz * k)
                        alt = free(list(avoid) + doors, wk, sk, max(0.35, sz * k * 0.45 / self.k))
                        if alt:
                            sz, wf = sz * k, wk; break
                    spot = alt or spot or (None if drop_blocked else free(doors, wf, spots, hh))
                if spot:
                    lx, ly = spot
                else:
                    if drop_blocked:   # no free spot (a small room full of symbols): its symbols and the key say what it is
                        continue
                self.text(nm, lx, ly, sz, color=color, anchor="l")
                continue
            if (x2 - x1) < 5 and (y2 - y1) > 2.5 * (x2 - x1):  # a narrow strip (the side walkways): label along its length
                sz = min(size - 0.6, self.fit(nm.upper(), "Helvetica-Bold", size - 0.6, y2 - y1 - 1.0))
                wf = self.c.stringWidth(nm.upper(), "Helvetica-Bold", sz) / self.k + 0.4
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                boxes = self.door_boxes()
                for dy in [0] + [s_ * k * 0.5 for k in range(1, 20) for s_ in (1, -1)]:
                    a1, a2 = cy + dy - wf / 2, cy + dy + wf / 2
                    if a1 > y1 + 0.3 and a2 < y2 - 0.3 and not any(q1 < x2 and q2 > x1 and a1 < q4 and a2 > q3 for q1, q2, q3, q4 in boxes):
                        cy += dy; break
                px, py = self.p(cx, cy); c = self.c; c.saveState(); c.translate(px, py); c.rotate(90)
                c.setFillColor(color); c.setFont("Helvetica-Bold", sz); c.drawCentredString(0, -sz * 0.3, nm.upper()); c.restoreState()
                continue
            sz = self.fit(nm.upper(), "Helvetica-Bold", size, x2 - x1 - 0.4)
            subt = sub(r) if sub else None
            ssz = self.fit(subt, "Helvetica", size - 0.7, x2 - x1 - 0.4) if subt else 0
            if subt and self.c.stringWidth(subt, "Helvetica", ssz) > (x2 - x1 - 0.4) * self.k:   # too narrow for its size: the working plan has it
                subt, ssz = None, 0
            wf = max(self.c.stringWidth(nm.upper(), "Helvetica-Bold", sz), self.c.stringWidth(subt, "Helvetica", ssz) if subt else 0) / self.k + 0.3
            cx, cy = self.label_spot(r, wf, 0.55 + sz / self.k * 0.7, (0.45 + ssz / self.k * 0.5) if subt else 0.0)
            put = self.halo_text if halo else self.text
            put(nm.upper(), cx, cy + 0.55, sz, "Helvetica-Bold", color)
            if subt: put(subt, cx, cy - 0.45, ssz, color=GREY)

    def rails(self):
        """First-floor railings: two thin lines; jali parapets drawn solid."""
        for axis, c0, a, b in RAILS:
            if (axis, c0) in JALI_RAILS:
                r = (a, b, c0 - 0.17, c0 + 0.17) if axis == "X" else (c0 - 0.17, c0 + 0.17, a, b)
                self.rect(*r, stroke=INK, lw=0.5, fill=colors.HexColor("#C8A97E"))
            elif axis == "X":
                self.line(a, c0 - 0.12, b, c0 - 0.12, lw=0.5); self.line(a, c0 + 0.12, b, c0 + 0.12, lw=0.5)
            else:
                self.line(c0 - 0.12, a, c0 - 0.12, b, lw=0.5); self.line(c0 + 0.12, a, c0 + 0.12, b, lw=0.5)

    def stair(self):
        """Dog-leg stair: treads of both flights, the half landing, the core wall and an UP / DN arrow."""
        st = STAIR
        d = st.get("dir", 1)
        x1, x2, y1, y2, n1 = st["flight1"]
        h1, e1 = (y1, y2) if d > 0 else (y2, y1)  # stair-hall end, landing end
        ground = FLOOR[0] == "G"
        above = dict(lw=0.3, color=GREY, dash=(1.5, 1))   # on the ground floor: above the cut line, dashed
        for i in range(n1):
            yy = h1 + d * i * st["tread"]
            if min(y1, y2) - 1e-6 <= yy <= max(y1, y2) + 1e-6:
                self.line(x1, yy, x2, yy, **(above if ground and d * (yy - h1) > 3.6 else dict(lw=0.3)))
        u1, u2, v1, v2, n2 = st["flight2"]
        h2, e2 = (v1, v2) if d > 0 else (v2, v1)
        for i in range(n2):
            yy = e2 - d * i * st["tread"]
            if min(v1, v2) - 1e-6 <= yy <= max(v1, v2) + 1e-6: self.line(u1, yy, u2, yy, **(above if ground else dict(lw=0.3)))
        lx1, lx2, ly1, ly2 = st["landing"]
        if ground: self.rect(lx1, lx2, ly1, ly2, stroke=GREY, lw=0.3, dash=(1.5, 1))
        else: self.rect(lx1, lx2, ly1, ly2, lw=0.3)
        cx1, cx2, cy1, cy2 = st["core"]
        self.rect(cx1, cx2, cy1, cy2, stroke=None, fill=WALL_FILL["INT"])
        mx = (x1 + x2) / 2
        if ground:  # flight 1 from the lobby, cut line part way up
            self.poly([(mx, h1 + d * 0.3), (mx, e1 - d * 0.6)], lw=0.5)
            self.poly([(mx - 0.3, e1 - d * 1.0), (mx, e1 - d * 0.6), (mx + 0.3, e1 - d * 1.0)], lw=0.5)
            self.text("UP", mx + 0.3, h1 + d * 0.9 - (0.35 if d < 0 else 0), 4.6, "Helvetica-Bold", anchor="l")   # beside its arrow
            self.line(min(u1, x1), h1 + d * 3.2, max(u2, x2), h1 + d * 4.4, lw=0.5, dash=(3, 1.5))
        else:
            ux = (u1 + u2) / 2   # flight 2 arrives at the stair head (its hall end h2); going down runs back toward the landing (e2)
            self.poly([(ux, h2 + d * 0.3), (ux, e2 - d * 0.6)], lw=0.5)
            self.poly([(ux - 0.3, e2 - d * 1.0), (ux, e2 - d * 0.6), (ux + 0.3, e2 - d * 1.0)], lw=0.5)
            self.text("DN", ux + 0.3, h2 + d * 0.9 - (0.35 if d < 0 else 0), 4.6, "Helvetica-Bold", anchor="l")

    def void(self, x1, x2, y1, y2, label=None, size=5):
        """Open to below: light cross and a label."""
        self.line(x1, y1, x2, y2, lw=0.3, color=GREY, dash=(2, 2)); self.line(x1, y2, x2, y1, lw=0.3, color=GREY, dash=(2, 2))
        if label: self.text(label, (x1 + x2) / 2, (y1 + y2) / 2 + 1.0, size, "Helvetica-Bold", GREY)

    def floor_extras(self):
        """Stair everywhere; on the ground floor the open courtyard (hatched), its walkway pillars and the thinnai with its
        steps; on the first floor the railings, the terrace posts, the jharokhas and the roofs below."""
        self.stair()
        if FLOOR[0] == "G":
            x1, x2, y1, y2 = COURTYARD
            c = self.c; a, b = self.p(x1, y1), self.p(x2, y2)
            c.saveState(); clip = c.beginPath(); clip.rect(a[0], a[1], b[0] - a[0], b[1] - a[1]); c.clipPath(clip, stroke=0, fill=0)
            c.setStrokeColor(colors.HexColor("#9DBBD6")); c.setLineWidth(0.3)
            k = x1 - (y2 - y1)
            while k < x2:
                pa, pb = self.p(k, y1), self.p(k + (y2 - y1), y2); c.line(pa[0], pa[1], pb[0], pb[1]); k += 1.5
            c.restoreState()
            self.rect(x1, x2, y1, y2, stroke=INK, lw=0.5)   # the step down from the walkway into the sunken court
            for x, y in WALKWAY_PILLARS:
                self.circle(x, y, 0.36, lw=0.6, fill=WHITE)
            t = next((r for r in ROOMS if r[0] == "R17"), None)
            if t:   # thinnai platform edge
                self.rect(t[2], t[3], t[4], t[5], stroke=INK, lw=0.5)
            stp = next((f[3] for f in SITE_FEATURES if f[0] == "STEPS"), None)
            if stp:
                n = int(round(LEVELS["thinnai"] / LEVELS["riser"]))
                for i in range(1, n):
                    xx = stp[0] + i * (stp[1] - stp[0]) / n
                    self.line(xx, stp[2], xx, stp[3], lw=0.3)
                self.rect(stp[0], stp[1], stp[2], stp[3], stroke=INK, lw=0.4)
            ss = SERVICE_STEPS   # the utility's service landing and steps outside D18, the grab rail on the wall face
            self.rect(ss["landing"][0], ss["x_end"], ss["landing"][2], ss["landing"][3], stroke=INK, lw=0.4)
            for k in range(ss["risers"] - 1):
                xx = ss["landing"][1] + k * ss["tread"]
                self.line(xx, ss["landing"][2], xx, ss["landing"][3], lw=0.3)
            self.line(ss["landing"][1] - 0.6, ss["landing"][3] - 0.15, ss["x_end"] + 1.0, ss["landing"][3] - 0.15, lw=0.6, color=GREY)
        if LIGHT_WELL:
            lx1, lx2, ly1, ly2 = LIGHT_WELL
        if LIGHT_WELL and FLOOR[0] == "F1":
            self.line(lx1, ly1, lx2, ly2, lw=0.3, color=GREY); self.line(lx1, ly2, lx2, ly1, lw=0.3, color=GREY)
            self.text("LIGHT WELL", (lx1 + lx2) / 2, (ly1 + ly2) / 2 + 0.9, 4.4, "Helvetica-Bold", GREY)
            self.text("jali grating, glazed lid", (lx1 + lx2) / 2, (ly1 + ly2) / 2 - 1.1, 4.0, color=GREY)
        elif LIGHT_WELL:
            self.rect(lx1, lx2, ly1, ly2, stroke=GREY, lw=0.4, dash=(3, 2))
            self.text("LIGHT WELL ABOVE", (lx1 + lx2) / 2, ly2 - 0.6, 4.0, color=GREY)
        if FLOOR[0] == "F1":
            self.rails()
            if BALCONY:
                bx1, bx2, by1, by2 = BALCONY
                px, py = self.p((bx1 + bx2) / 2 + 0.2, (by1 + by2) / 2); c = self.c; c.saveState(); c.translate(px, py); c.rotate(90)
                c.setFillColor(INK); c.setFont("Helvetica-Bold", 4.6); c.drawCentredString(0, 0, "BALCONY"); c.restoreState()
            for x, y in TERRACE_POSTS:
                self.rect(x - 0.17, x + 0.17, y - 0.17, y + 0.17, stroke=INK, fill=INK, lw=0.3)
            for x1, x2, y1, y2, _ in JHAROKHAS:  # teak bays projecting over the walkway roof
                self.rect(x1, x2, y1, y2, stroke=INK, lw=0.5, fill=colors.HexColor("#E8DCC8"))
            # the single-storey ring below, the open courtyard and the walkway roofs
            t_ = ROOF["terrace"]   # outline of the ring below, where it is not under the wing or the terrace
            self.poly([(RING[0], HY1), (HX2, HY1), (HX2, HY2), (t_[1], HY2)], lw=0.4, color=GREY, dash=(3, 2))
            self.rect(*COURTYARD, stroke=GREY, lw=0.4, dash=(3, 2))
            ccx, ccy = (COURTYARD[0] + COURTYARD[1]) / 2, (COURTYARD[2] + COURTYARD[3]) / 2
            csz = self.fit("(OPEN TO THE SKY)", "Helvetica", 4.6, COURTYARD[1] - COURTYARD[0] - 0.6)
            self.text("COURTYARD", ccx, ccy + 0.5, csz, color=GREY); self.text("(OPEN TO THE SKY)", ccx, ccy - 0.6, csz, color=GREY)
            rsz = self.fit("GROUND-FLOOR ROOFS BELOW", "Helvetica", 4.6, HX2 - RING[1] - 0.6)
            self.text("GROUND-FLOOR ROOFS BELOW", (RING[1] + HX2) / 2, (HY1 + RING[2]) / 2, rsz, color=GREY)

    def auto_dims(self, size=5.5):
        """Dimension chains from the wall grid: below the plan (x) and to its right (y)."""
        xs = sorted({round(w[1], 3) for w in WALLS if w[0] == "Y"})
        ys = sorted({round(w[1], 3) for w in WALLS if w[0] == "X"})
        lo_x, hi_x, lo_y, hi_y = xs[0], xs[-1], ys[0], ys[-1]
        # the chain runs along the south wall: end it where that wall ends (upstairs the wing's south wall is only the west band)
        sw = [w for w in WALLS if w[0] == "X" and abs(w[1] - lo_y) < 1e-6]
        s_lo, s_hi = min(min(w[2], w[3]) for w in sw), max(max(w[2], w[3]) for w in sw)
        clipped = s_lo > lo_x + 1e-6 or s_hi < hi_x - 1e-6
        xs = [v for v in xs if s_lo - 1e-6 <= v <= s_hi + 1e-6]
        for a, b in zip(xs, xs[1:]): self.hdim(a, b, lo_y - 2.6, size=size)   # below the south window tags
        self.hdim(xs[0], xs[-1], lo_y - 5.0, f"{fmt_ft(xs[-1] - xs[0])} OVERALL" + (" (SOUTH WALL)" if clipped else ""))
        xr = lo_x - 4.2   # west of the house: the thinnai and its steps take the east side
        for a, b in zip(ys, ys[1:]): self.vdim(a, b, xr, size=size)
        self.vdim(lo_y, hi_y, xr - 2.7, f"{fmt_ft(hi_y - lo_y)} OVERALL")

    def north(self, x, y):
        c = self.c
        c.setStrokeColor(INK); c.setFillColor(INK); c.setLineWidth(0.6)
        c.circle(x, y, 7 * mm, stroke=1, fill=0)
        p = c.beginPath(); p.moveTo(x, y + 6 * mm); p.lineTo(x - 2.5 * mm, y - 4 * mm); p.lineTo(x, y - 2 * mm); p.close()
        c.drawPath(p, stroke=1, fill=1)
        c.setFont("Helvetica-Bold", 9); c.drawCentredString(x, y + 8.5 * mm, "N")

    def scalebar(self, x, y, steps=(0, 5, 10, 20)):
        c = self.c
        steps = list(steps)
        for a, b in zip(steps, steps[1:]):
            c.setFillColor(INK if steps.index(a) % 2 == 0 else WHITE)
            c.setStrokeColor(INK); c.setLineWidth(0.4)
            c.rect(x + a * self.k, y, (b - a) * self.k, 1.6 * mm, stroke=1, fill=1)
        c.setFillColor(INK); c.setFont("Helvetica", 6.5)
        for s in steps:
            c.drawCentredString(x + s * self.k, y - 3.5 * mm, f"{s}'")
        c.drawString(x + (steps[-1] + 1) * self.k, y, "feet")

    def hdim(self, a, b, y, label=None, size=6):
        self.line(a, y, b, y, lw=0.3)
        for v in (a, b):
            self.line(v - 0.25, y - 0.25, v + 0.25, y + 0.25, lw=0.6)
            self.line(v, y - 0.5, v, y + 0.5, lw=0.25)
        self.text(label or fmt_ft(b - a), (a + b) / 2, y + 0.55, size)

    def vdim(self, a, b, x, label=None, size=6):
        self.line(x, a, x, b, lw=0.3)
        for v in (a, b):
            self.line(x - 0.25, v - 0.25, x + 0.25, v + 0.25, lw=0.6)
            self.line(x - 0.5, v, x + 0.5, v, lw=0.25)
        c = self.c; px, py = self.p(x - 0.55, (a + b) / 2)
        c.saveState(); c.translate(px, py); c.rotate(90); c.setFillColor(INK); c.setFont("Helvetica", size)
        c.drawCentredString(0, 0, label or fmt_ft(b - a)); c.restoreState()

    def level(self, x, y, v, size=5.5, color=INK):
        """Level tag: small triangle plus level text."""
        c = self.c; px, py = self.p(x, y)
        c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(0.4)
        p = c.beginPath(); p.moveTo(px, py); p.lineTo(px - 1.2 * mm, py + 1.6 * mm); p.lineTo(px + 1.2 * mm, py + 1.6 * mm); p.close()
        c.drawPath(p, stroke=1, fill=0)
        self.s.note(fmt_lvl(v), px + 1.8 * mm, py + 0.3 * mm, size, color)


class Elev:
    """Maps (u, z) feet to page coordinates for elevations and sections."""
    def __init__(self, sheet, scale_den, ox, oy):
        self.s = sheet; self.c = sheet.c
        self.k = 304.8 / scale_den * mm
        self.ox, self.oy = ox, oy
        self.plan = Plan(sheet, scale_den, ox, oy)  # same maths, (u, z) in place of (x, y)

    def __getattr__(self, name):
        return getattr(self.plan, name)

    def zdim(self, z1, z2, u, label=None, size=5.5):
        self.plan.vdim(z1, z2, u, label, size)

    def lvl(self, u, z, label, size=5.5, right=False):
        c = self.c; px, py = self.plan.p(u, z)
        c.setStrokeColor(INK); c.setFillColor(INK); c.setLineWidth(0.4)
        p = c.beginPath(); p.moveTo(px, py); p.lineTo(px - 1.3 * mm, py + 1.8 * mm); p.lineTo(px + 1.3 * mm, py + 1.8 * mm); p.close()
        c.drawPath(p, stroke=1, fill=1)
        c.setLineWidth(0.3); c.line(px - (0 if right else 18 * mm), py, px + (18 * mm if right else 0), py)
        self.s.note(label, px + (2 * mm if right else -2 * mm), py + 0.8 * mm, size, INK, "Helvetica", "l" if right else "r")


def short_name(name):
    for a, b in ((" (double height)", ""), (" (covered)", ""), (" (verandah)", ""), (" (semi-open)", ""), (" (skylit)", ""), ("Dressing alcove", "Dressing"), ("Bedroom 2 wardrobe alcove", "Alcove"), ("Bedroom 2 bath", "Bath 2"), ("Walk-in wardrobe", "Walk-in"), ("Family room desk nook", "Desk nook"), ("Low store", "Low hatch store"),
                 (" (open to the hall)", ""), (" (open to the walkway)", ""), ("Sitting and serving area (open)", "Sitting area"), ("Fridge corner", "Fridge"), ("Genkan (shoe-off foyer)", "Genkan"), (" (common)", ""), (" (attached to Bedroom 2)", ""), (" (open, walls optional later)", ""),  (" (old store, open to the bedroom)", ""), (" (north window)", "")):
        name = name.replace(a, b)
    return name


def house_plan(sheet):
    """The house at 1:75, in the same place on every plan sheet."""
    return Plan(sheet, 75, PLAN_OX, PLAN_OY)


def floor_sheet(fn, floor, num, title):
    """Run a plan sheet function for one floor (the model's lists are swapped while it draws)."""
    def run(c):
        with on_floor(floor):
            fn(c, num, title)
    return run


def plot_outline(pl, x_end=None, color=INK, lw=0.9):
    """The plot boundary, cut off at x_end on the house sheets (the plot runs on to the road)."""
    x_end = min(x_end or PLOT_X2, PLOT_X2)
    north = [(x, plot_north(x)) for x in (PLOT_X1, 91.0, x_end) if x <= x_end]
    if north[-1][0] < x_end:
        north.append((x_end, plot_north(x_end)))
    pl.line(PLOT_X1, 0, x_end, 0, lw=lw, color=color)
    pl.line(PLOT_X1, 0, PLOT_X1, plot_north(PLOT_X1), lw=lw, color=color)
    for (a, b), (c_, d) in zip(north, north[1:]):
        pl.line(a, b, c_, d, lw=lw, color=color)
    if x_end < PLOT_X2:
        pl.line(x_end, -0.5, x_end, plot_north(x_end) + 0.5, lw=0.4, color=GREY, dash=(1.5, 1.5))
    else:
        pl.line(PLOT_X2, 0, PLOT_X2, plot_north(PLOT_X2), lw=lw, color=color)
    return x_end


def site_context(pl, light=False, x_end=None):
    g = GREY
    x_end = plot_outline(pl, x_end or SITE["l"] + 3)
    if x_end < PLOT_X2:
        pl.text(f"PLOT RUNS ON {PLOT_X2 - x_end:.0f} FT TO THE ROAD", x_end - 1.0, plot_north(x_end) + 1.4, 5.5, color=g, anchor="r")
    else:
        pl.rect(PLOT_X2, PLOT_X2 + 4, -1, plot_north(PLOT_X2) + 1, stroke=None, fill=colors.HexColor("#EDEDED"))
        pl.text("ROAD", PLOT_X2 + 2, plot_north(PLOT_X2) / 2, 6, color=g)
    for x, y, r in TREES:
        if x - r < x_end:
            pl.circle(x, y, r, lw=0.3, color=colors.HexColor("#6F8E4A"))


def site_features(pl, labels=True, size=5, x_end=None, skip=()):
    """skip: feature ids drawn without their label (where a sheet's own symbols crowd them)."""
    x_end = x_end or SITE["l"] + 3
    all_labels = labels
    shops_label = None
    for fid, label, kind, g in SITE_FEATURES:
        labels = all_labels and fid not in skip
        if kind == "rect":
            x1, x2, y1, y2 = g
            if x1 >= x_end:
                continue
            x2 = min(x2, x_end)
            if fid == "SPARE":
                pl.rect(x1, x2, y1, y2, stroke=None, fill=colors.HexColor("#EEF3E8"))
                if labels: pl.text(f"BACK GARDEN ({HX1:.0f} FT)", (x1 + x2) / 2, y2 - 4.5, pl.fit(f"BACK GARDEN ({HX1:.0f} FT)", "Helvetica-Bold", size + 0.5, x2 - x1 - 0.4), "Helvetica-Bold", GREY)
                continue
            if fid == "VEG":
                for b in GARDEN_BEDS:
                    if b[0] < x_end:
                        pl.rect(b[0], min(b[1], x_end), b[2], b[3], lw=0.3, fill=colors.HexColor("#EEF3E8"))
                if labels:   # west of the beds, clear of them
                    bx = min(b[0] for b in GARDEN_BEDS if b[2] < (y1 + y2) / 2 < b[3])
                    pl.text("VEGETABLE", bx - 0.6, (y1 + y2) / 2 + 0.7, size + 0.5, "Helvetica-Bold", colors.HexColor("#4F6E34"), anchor="r")
                    pl.text("GARDEN", bx - 0.6, (y1 + y2) / 2 - 0.9, size + 0.5, "Helvetica-Bold", colors.HexColor("#4F6E34"), anchor="r")
                continue
            fill = {"HERBS": colors.HexColor("#EEF3E8"), "GUILD": colors.HexColor("#EEF3E8"), "FENCE": colors.HexColor("#B9CF9A"), "WORM": colors.HexColor("#E4DCCB"), "DRIVE": colors.HexColor("#F1EEE8"), "CARPORT": colors.HexColor("#F1EEE8"), "WORKSHOP": colors.HexColor("#DADADA"), "SHOP1": colors.HexColor("#E4DCCB"), "SHOP2": colors.HexColor("#E4DCCB")}.get(fid)
            if fid == "SHOPS":
                pts = SHOP_WALL
                for (a, b), (c_, d) in zip(pts, pts[1:]):
                    pl.line(a, b, c_, d, lw=1.4)  # short road wall north of the shops
                if labels:   # inside the shops' footprint, above the boundary hedge: drawn last, over the shops' fill
                    shops_label = (x1, x2, y1)
                continue
            pl.rect(x1, x2, y1, y2, lw=0.4, dash=(2, 1) if fid in ("PERGOLA", "CARPORT", "WVERANDAH", "SHOPBACK", "RAINTANK") else None, fill=fill, stroke=INK)
            if fid == "WSTEP":   # the landing's edge and the risers down along the wall, and the grab rail on the wall face
                ss = SERVICE_STEPS
                for k in range(ss["risers"] - 1):
                    pl.line(ss["landing"][1] + k * ss["tread"], y1, ss["landing"][1] + k * ss["tread"], y2, lw=0.3)
                pl.line(ss["landing"][1] - 0.6, y2 - 0.15, ss["x_end"] + 1.0, y2 - 0.15, lw=0.5, color=GREY)
            if labels and fid not in ("GATE", "STEPS", "HEDGE1", "APRON") and x2 - x1 > 2.5:
                if fid == "COMPOST":   # the worm bin sits on its north side: name it to the west
                    pl.text("COMPOST", x1 - 0.4, (y1 + y2) / 2, size, anchor="r"); continue
                pl.text({"WVERANDAH": "VERANDAH", "CARPORT": "CAR PORCH", "PATH": "FORECOURT", "OTTA": "", "GSTEP": "", "WSTEP": "", "PATH2": "", "SHOP1": "SHOP 1", "SHOP2": "SHOP 2", "SITEWC": "WC", "HERBS": "", "GUILD": "", "FENCE": "", "WORM": ""}.get(fid, fid), (x1 + x2) / 2, y2 + 0.8 if fid == "COMPOST" else y2 - 2.0 if fid == "PATH" else (y1 + y2) / 2, size)
            if labels and fid == "HERBS":
                pl.text("KITCHEN GARDEN", (x1 + x2) / 2 + 1.5, y2 - 1.0, size, "Helvetica-Bold", colors.HexColor("#4F6E34"))
            if labels and fid == "GUILD":
                pl.text("FRUIT GUILDS", (x1 + x2) / 2, y2 - 0.9, size + 1, "Helvetica-Bold", colors.HexColor("#4F6E34"))
        elif kind == "poly" and fid == "DRIVE":
            pts = [(x, y) for x, y in drive_poly() if x <= x_end]
            if len(pts) > 2:
                pl.poly(pts, lw=0.4, close=True, fill=colors.HexColor("#F1EEE8"))
                if labels: pl.text("DRIVE", (g[0] + g[1]) / 2, plot_north((g[0] + g[1]) / 2) - 5.4, size)
        elif kind == "circle":
            x, y, r = g
            if x - r >= x_end:
                continue
            pl.circle(x, y, r, lw=0.4, fill=colors.HexColor("#DCE8CC") if fid == "SPIRAL" else None)
            if labels: pl.text({"SPIRAL": "HERB SPIRAL", "BANANA": "", "FEET": "foot tap", "JASMINE": "jasmine", "PARIJAT": "parijat", "TULSI": "tulsi", "SOAK": "SOAK PIT"}.get(fid, fid), x + (1.0 if fid == "SPIRAL" else 0), y - r - 1.4 if fid == "SPIRAL" else y if fid == "BANANA" else y + r + 0.6, size)
    for x, y, r, k in FOOD_TREES:
        if x - r < x_end:
            pl.circle(x, y, r, lw=0.3, color=colors.HexColor("#6F8E4A"), fill=colors.HexColor("#DCE8CC") if k in ("banana", "papaya") else None)
    bc = next((f[3] for f in SITE_FEATURES if f[0] == "BANANA"), None)
    if all_labels and "BANANA" not in skip and bc and bc[0] < x_end:
        pl.text("BANANAS", bc[0], bc[1], size)
    if shops_label:
        x1, x2, y1 = shops_label
        pl.text("2 RENTAL SHOPS", (x1 + x2) / 2, y1 + 2.4, pl.fit("2 RENTAL SHOPS", "Helvetica-Bold", size, x2 - x1 - 0.6), "Helvetica-Bold", ACC)
        pl.text("(build when wanted)", (x1 + x2) / 2, y1 + 1.2, pl.fit("(build when wanted)", "Helvetica", size, x2 - x1 - 0.6), color=ACC)
