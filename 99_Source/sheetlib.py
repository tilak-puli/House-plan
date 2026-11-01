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
        c.drawString(x0 + 5 * mm, y - 6 * mm, "Kerala-style two-storey residence (duplex option)")
        c.drawString(x0 + 5 * mm, y - 11 * mm, "Guntur, Andhra Pradesh")
        c.drawString(x0 + 5 * mm, y - 16 * mm, f"Plot {SITE['w']}' x {SITE['l']}' (front 61' used), road on east")
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
                if tags:
                    if axis == "X":
                        tx, ty = (a + b) / 2, cc + (1.25 if cc >= 25 else -1.25)
                    else:
                        tx, ty = cc + (1.5 if cc >= 61 else -1.5), (a + b) / 2
                    self.text(rec[0], tx, ty, 5.5, color=ACC)
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
                if tags: self.text(did, tx, ty, 5.5, color=ACC)

    def room_names(self, size=5.5, color=GREY, corner=False, sub=None):
        for r in ROOMS:
            rid, name, x1, x2, y1, y2, _ = r
            nm = short_name(name)
            if corner:
                lx, ly = x1 + 0.4, y2 - 0.7
                for o in ROOMS:  # a smaller room in the same corner (Bath 2 in Bedroom 2): label past it
                    if o is not r and o[2] <= lx <= o[3] and o[4] <= ly <= o[5] and (o[3] - o[2]) * (o[5] - o[4]) < (x2 - x1) * (y2 - y1):
                        lx = o[3] + 0.4
                self.text(nm, lx, ly, size, color=color, anchor="l")
            else:
                cx, cy = ROOM_LABEL_AT.get(rid, ((x1 + x2) / 2, (y1 + y2) / 2))
                self.text(nm.upper(), cx, cy + 0.55, size, "Helvetica-Bold", color)
                if sub: self.text(sub(r), cx, cy - 0.45, size - 0.7, color=GREY)

    def rails(self):
        """First-floor railings: two thin lines."""
        for axis, c0, a, b in RAILS:
            if axis == "X":
                self.line(a, c0 - 0.12, b, c0 - 0.12, lw=0.5); self.line(a, c0 + 0.12, b, c0 + 0.12, lw=0.5)
            else:
                self.line(c0 - 0.12, a, c0 - 0.12, b, lw=0.5); self.line(c0 + 0.12, a, c0 + 0.12, b, lw=0.5)

    def stair(self):
        """Dog-leg stair: treads of both flights, the half landing, the core wall and an UP / DN arrow."""
        st = STAIR
        x1, x2, y1, y2, n1 = st["flight1"]
        for i in range(n1):
            yy = y1 + i * st["tread"]
            if yy <= y2 + 1e-6: self.line(x1, yy, x2, yy, lw=0.3)
        u1, u2, v1, v2, n2 = st["flight2"]
        for i in range(n2):
            yy = v2 - i * st["tread"]
            if yy >= v1 - 1e-6: self.line(u1, yy, u2, yy, lw=0.3)
        lx1, lx2, ly1, ly2 = st["landing"]
        self.rect(lx1, lx2, ly1, ly2, lw=0.3)
        cx1, cx2, cy1, cy2 = st["core"]
        self.rect(cx1, cx2, cy1, cy2, stroke=None, fill=WALL_FILL["INT"])
        ground = FLOOR[0] == "G"
        mx = (x1 + x2) / 2
        if ground:  # flight 1 from the lobby, cut line part way up
            self.poly([(mx, y1 + 0.3), (mx, y2 - 0.6)], lw=0.5)
            self.poly([(mx - 0.3, y2 - 1.0), (mx, y2 - 0.6), (mx + 0.3, y2 - 1.0)], lw=0.5)
            self.text("UP", mx, y1 + 0.9, 4.6, "Helvetica-Bold")
            self.line(u1, y1 + 3.2, x2, y1 + 4.4, lw=0.5, dash=(3, 1.5))
        else:
            ux = (u1 + u2) / 2
            self.poly([(ux, v1 + 0.6), (ux, v2 - 0.3)], lw=0.5)
            self.poly([(ux - 0.3, v1 + 1.0), (ux, v1 + 0.6), (ux + 0.3, v1 + 1.0)], lw=0.5)
            self.text("DN", ux, v1 + 1.6, 4.6, "Helvetica-Bold")

    def void(self, x1, x2, y1, y2, label=None, size=5):
        """Open to below: light cross and a label."""
        self.line(x1, y1, x2, y2, lw=0.3, color=GREY, dash=(2, 2)); self.line(x1, y2, x2, y1, lw=0.3, color=GREY, dash=(2, 2))
        if label: self.text(label, (x1 + x2) / 2, (y1 + y2) / 2 + 1.0, size, "Helvetica-Bold", GREY)

    def floor_extras(self):
        """Stair everywhere; on the first floor also the railings, the terrace posts and the roof below."""
        self.stair()
        if FLOOR[0] == "F1":
            self.rails()
            for x, y in TERRACE_POSTS:
                self.rect(x - 0.17, x + 0.17, y - 0.17, y + 0.17, stroke=INK, fill=INK, lw=0.3)
            self.text("STEEL POSTS CARRY THE ROOF OVER THE TERRACE", 53, 23.3, 4.4, color=GREY)
            gx1, gx2, ya, yb = ROOF["gable"]
            self.rect(61.4, gx2, ya, yb, stroke=GREY, lw=0.4, dash=(3, 2))
            self.text("FRONT GABLE ROOF BELOW", (61.4 + gx2) / 2, (ya + yb) / 2, 4.6, color=GREY)

    def auto_dims(self, size=5.5):
        """Dimension chains from the wall grid: below the plan (x) and to its right (y)."""
        xs = sorted({round(w[1], 3) for w in WALLS if w[0] == "Y"})
        ys = sorted({round(w[1], 3) for w in WALLS if w[0] == "X"})
        lo_x, hi_x, lo_y, hi_y = xs[0], xs[-1], ys[0], ys[-1]
        for a, b in zip(xs, xs[1:]): self.hdim(a, b, lo_y - 1.5, size=size)
        self.hdim(lo_x, hi_x, lo_y - 4.3, f"{fmt_ft(hi_x - lo_x)} OVERALL")
        xr = max(hi_x, 67) + 4.6
        for a, b in zip(ys, ys[1:]): self.vdim(a, b, xr, size=size)
        self.vdim(lo_y, hi_y, xr + 2.7, f"{fmt_ft(hi_y - lo_y)} OVERALL")

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
    for a, b in ((" (double height)", ""), (" (covered)", ""), (" (verandah)", ""), (" (semi-open)", ""), (" (skylit)", ""), ("Dressing alcove", "Dressing"), ("Walk-in wardrobe", "Walk-in"),
                 (" (open to the hall)", ""), (" (open to the walkway)", ""), ("Sitting and serving area (open)", "Sitting area"), ("Fridge corner", "Fridge"), (" (common)", ""), (" (attached to Bedroom 2)", ""), (" (open, walls optional later)", ""),  (" (old store, open to the bedroom)", ""), (" (north window)", "")):
        name = name.replace(a, b)
    return name


def floor_sheet(fn, floor, num, title):
    """Run a plan sheet function for one floor (the model's lists are swapped while it draws)."""
    def run(c):
        with on_floor(floor):
            fn(c, num, title)
    return run


def site_context(pl, light=False):
    g = GREY
    L, W, S = SITE["l"], SITE["w"], SITE["strip"]
    pl.line(SITE["trial"], 0, SITE["trial"], W, lw=0.5, color=GREY, dash=(4, 2))
    if S: pl.rect(0, L, 0, W + S, stroke=GREY, lw=0.5, dash=(3, 2))
    pl.rect(0, L, 0, W, stroke=INK, lw=0.9)
    pl.rect(L, L + 3.5, -1, W + S + 1, stroke=None, fill=colors.HexColor("#EDEDED"))
    pl.text("ROAD", L + 1.75, W / 2, 6, color=g)
    for x, y, r in TREES:
        pl.circle(x, y, r, lw=0.3, color=colors.HexColor("#6F8E4A"))


def site_features(pl, labels=True, size=5):
    for fid, label, kind, g in SITE_FEATURES:
        if kind == "rect":
            x1, x2, y1, y2 = g
            if fid == "SPARE":
                pl.rect(x1, x2, y1, y2, stroke=None, fill=colors.HexColor("#EEF3E8"))
                if labels: pl.text("SPARE LAND (BACK 14 FT)", (x1 + x2) / 2, y2 - 2.2, size + 0.5, "Helvetica-Bold", GREY)
                continue
            pl.rect(x1, x2, y1, y2, lw=0.4, dash=(2, 1) if fid == "PERGOLA" else None)
            if labels and fid not in ("GATE", "STEPS", "HEDGE3"):
                pl.text(fid if fid != "PERGOLA" else "PERGOLA", (x1 + x2) / 2, (y1 + y2) / 2, size)
        elif kind == "circle":
            x, y, r = g
            pl.circle(x, y, r, lw=0.4)
            if labels: pl.text(fid, x, y + r + 0.6, size)
