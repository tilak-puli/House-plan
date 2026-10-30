"""Shared drawing toolkit for the PDF set: sheet frame, plan and elevation mappers, tables."""
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from geom import *

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
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 13)
        c.drawString(x0 + 5 * mm, y, PROJECT["name"])
        c.setFont("Helvetica", 8.5); c.setFillColor(GREY)
        c.drawString(x0 + 5 * mm, y - 6 * mm, "Kerala-style single-storey residence")
        c.drawString(x0 + 5 * mm, y - 11 * mm, "Guntur, Andhra Pradesh")
        c.drawString(x0 + 5 * mm, y - 16 * mm, f"Plot {SITE['w']}' x {SITE['l']}', road on east")
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
        for axis, c, s, e in JALI_SCREENS:
            x1, x2, y1, y2 = seg_rect(axis, c, s, e)
            self.rect(x1, x2, y1 + 0.15, y2 - 0.15, stroke=INK, lw=0.4, dash=(1, 1))
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
                if tags:
                    if axis == "X":
                        tx, ty = (a + b) / 2, cc + (1.25 if cc >= 25 else -1.25)
                    else:
                        tx, ty = cc + (1.5 if cc >= 54 else -1.5), (a + b) / 2
                    self.text(rec[0], tx, ty, 5.5, color=ACC)
            else:
                did, _, _, s0, e0, sw, *_ = rec
                w = e0 - s0
                if sw == 0:
                    self.line(s0, cc - 0.13, s0 + w * 0.55, cc - 0.13, lw=0.6)
                    self.line(e0 - w * 0.55, cc + 0.13, e0, cc + 0.13, lw=0.6)
                    if tags: self.text(did, (s0 + e0) / 2, cc - 0.9, 5.5, color=ACC)
                    continue
                c.setStrokeColor(INK); c.setLineWidth(0.25)
                if axis == "X":
                    hx, hy = self.p(s0, cc)
                    self.line(s0, cc, s0, cc + sw * w, lw=0.5)
                    st = 0 if sw > 0 else 270
                    tx, ty = (s0 + e0) / 2, cc + sw * w * 0.4
                else:
                    hx, hy = self.p(cc, s0)
                    self.line(cc, s0, cc + sw * w, s0, lw=0.5)
                    st = 0 if sw > 0 else 90
                    tx, ty = cc + sw * w * 0.4, (s0 + e0) / 2
                r = w * self.k
                c.setDash(1.5, 1); c.arc(hx - r, hy - r, hx + r, hy + r, st, 90); c.setDash()
                if tags: self.text(did, tx, ty, 5.5, color=ACC)

    def room_names(self, size=5.5, color=GREY, corner=False, sub=None):
        for r in ROOMS:
            rid, name, x1, x2, y1, y2, _ = r
            nm = short_name(name)
            if corner:
                self.text(nm, x1 + 0.4, y2 - 0.7, size, color=color, anchor="l")
            else:
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                if rid == "R10": cy = 15.3
                self.text(nm.upper(), cx, cy + 0.55, size, "Helvetica-Bold", color)
                if sub: self.text(sub(r), cx, cy - 0.45, size - 0.7, color=GREY)

    def north(self, x, y):
        c = self.c
        c.setStrokeColor(INK); c.setFillColor(INK); c.setLineWidth(0.6)
        c.circle(x, y, 7 * mm, stroke=1, fill=0)
        p = c.beginPath(); p.moveTo(x, y + 6 * mm); p.lineTo(x - 2.5 * mm, y - 4 * mm); p.lineTo(x, y - 2 * mm); p.close()
        c.drawPath(p, stroke=1, fill=1)
        c.setFont("Helvetica-Bold", 9); c.drawCentredString(x, y + 8.5 * mm, "N")

    def scalebar(self, x, y):
        c = self.c
        steps = [0, 5, 10, 20]
        for a, b in zip(steps, steps[1:]):
            c.setFillColor(INK if steps.index(a) % 2 == 0 else WHITE)
            c.setStrokeColor(INK); c.setLineWidth(0.4)
            c.rect(x + a * self.k, y, (b - a) * self.k, 1.6 * mm, stroke=1, fill=1)
        c.setFillColor(INK); c.setFont("Helvetica", 6.5)
        for s in steps:
            c.drawCentredString(x + s * self.k, y - 3.5 * mm, f"{s}'")
        c.drawString(x + 21 * self.k, y, "feet")

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
    for a, b in ((" (verandah)", ""), (" (semi-open)", ""), (" (skylit)", ""), ("Dressing alcove", "Dressing"), ("Walk-in wardrobe", "Walk-in")):
        name = name.replace(a, b)
    return name


def site_context(pl, light=False):
    g = GREY
    L, W, S = SITE["l"], SITE["w"], SITE["strip"]
    pl.rect(0, L, 0, W + S, stroke=GREY, lw=0.5, dash=(3, 2))
    pl.rect(0, L, 0, W, stroke=INK, lw=0.9)
    pl.rect(L, L + 3.5, -1, W + S + 1, stroke=None, fill=colors.HexColor("#EDEDED"))
    pl.text("ROAD", L + 1.75, W / 2, 6, color=g)
    for x, y, r in TREES:
        pl.circle(x, y, r, lw=0.3, color=colors.HexColor("#6F8E4A"))


def site_features(pl, labels=True, size=5):
    for fid, label, kind, g in SITE_FEATURES:
        if kind == "rect":
            x1, x2, y1, y2 = g
            pl.rect(x1, x2, y1, y2, lw=0.4, dash=(2, 1) if fid == "PERGOLA" else None)
            if labels and fid not in ("GATE", "STEPS"):
                pl.text(fid if fid != "PERGOLA" else "PERGOLA", (x1 + x2) / 2, (y1 + y2) / 2, size)
        elif kind == "circle":
            x, y, r = g
            pl.circle(x, y, r, lw=0.4)
            if labels: pl.text(fid, x, y + r + 0.6, size)
