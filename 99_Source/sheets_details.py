"""A-501 / A-502: typical construction details. Schematic, in inches, to show intent to the professionals."""
from sheetlib import *

CONC = colors.HexColor("#B5B5B5")
AAC = colors.HexColor("#E9E3D3")
SOIL = colors.HexColor("#CDBFA6")
FILL = colors.HexColor("#E6DDC8")
TILEC = colors.HexColor("#D9CBB8")
STONE = colors.HexColor("#A9A39A")
WATERP = colors.HexColor("#2D6FB0")
WOOD = colors.HexColor("#8E6B4E")


class D:
    """Detail canvas in inches inside a box on the sheet."""
    def __init__(self, s, x0, y0, w, h, title, num, bounds, notes_h=34):
        self.s, self.c = s, s.c
        bx1, bx2, by1, by2 = bounds
        aw, ah = w - 16 * mm, h - (notes_h + 16) * mm   # drawing area between the notes and the title
        self.k = min(aw / (bx2 - bx1), ah / (by2 - by1))  # paper length per inch
        self.ox = x0 + 8 * mm + (aw - (bx2 - bx1) * self.k) / 2 - bx1 * self.k
        self.oy = y0 + (notes_h + 2) * mm + (ah - (by2 - by1) * self.k) / 2 - by1 * self.k
        self.notes = []
        self.box = (x0, y0, w, h)
        s.c.setStrokeColor(LIGHT); s.c.setLineWidth(0.4); s.c.rect(x0, y0, w, h)
        s.c.setFillColor(ACC); s.c.circle(x0 + 6 * mm, y0 + h - 6 * mm, 3.5 * mm, stroke=0, fill=1)
        s.note(str(num), x0 + 6 * mm, y0 + h - 7.2 * mm, 9, WHITE, "Helvetica-Bold", "c")
        s.note(title, x0 + 12 * mm, y0 + h - 7.4 * mm, 8.5, INK, "Helvetica-Bold")

    def p(self, x, y):
        return self.ox + x * self.k, self.oy + y * self.k

    def r(self, x1, x2, y1, y2, fill=None, lw=0.5, stroke=INK, dash=None):
        a, b = self.p(x1, y1), self.p(x2, y2); c = self.c
        if stroke is not None: c.setStrokeColor(stroke)
        c.setLineWidth(lw); c.setDash(list(dash), 0) if dash else c.setDash()
        if fill is not None: c.setFillColor(fill)
        c.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=1 if stroke is not None else 0, fill=1 if fill is not None else 0); c.setDash()

    def l(self, pts, lw=0.5, color=INK, dash=None, fill=None, close=False):
        c = self.c; c.setStrokeColor(color); c.setLineWidth(lw); c.setDash(list(dash), 0) if dash else c.setDash()
        path = c.beginPath(); path.moveTo(*self.p(*pts[0]))
        for q in pts[1:]: path.lineTo(*self.p(*q))
        if close: path.close()
        if fill is not None: c.setFillColor(fill)
        c.drawPath(path, stroke=1, fill=1 if fill is not None else 0); c.setDash()

    def t(self, s, x, y, size=5.5, color=INK, anchor="l", font="Helvetica"):
        px, py = self.p(x, y); self.s.note(s, px, py, size, color, font, anchor)

    def call(self, x, y, note):
        """Numbered callout at (x, y) with the note listed under the drawing."""
        n = len(self.notes) + 1
        self.notes.append(note)
        px, py = self.p(x, y); c = self.c
        c.setFillColor(WHITE); c.setStrokeColor(RED); c.setLineWidth(0.5); c.circle(px, py, 1.9 * mm, stroke=1, fill=1)
        self.s.note(str(n), px, py - 0.9 * mm, 5.5, RED, "Helvetica-Bold", "c")

    def finish(self):
        x0, y0, w, h = self.box
        y = y0 + 30 * mm
        st = ParagraphStyle("n", fontName="Helvetica", fontSize=5.6, leading=6.6)
        col_w = (w - 10 * mm) / 2
        half = (len(self.notes) + 1) // 2
        for ci, chunk in enumerate((self.notes[:half], self.notes[half:])):
            yy = y
            for i, n in enumerate(chunk):
                num = i + 1 + ci * half
                p = Paragraph(f"<font color='#B4442E'><b>{num}</b></font>  {n}", st)
                pw, ph = p.wrap(col_w, 30 * mm); p.drawOn(self.c, x0 + 4 * mm + ci * (col_w + 3 * mm), yy - ph); yy -= ph + 0.6 * mm


def det_plinth(d):
    d.r(-6, 60, -30, 0, fill=SOIL, stroke=None)
    d.r(10, 30, -30, -24, fill=CONC, dash=(2, 1)); d.r(15, 24, -24, 12, fill=CONC)               # footing + plinth beam
    d.r(24, 54, -2, 20, fill=FILL, stroke=None)                                                   # plinth fill
    d.r(24, 54, 20, 24, fill=CONC); d.r(24, 54, 24, 25, fill=TILEC)                               # PCC + floor
    d.r(15, 24, 12, 13, fill=WATERP, stroke=None)                                                 # DPC
    d.r(16, 23, 13, 60, fill=AAC)                                                                 # wall above
    d.r(23, 23.6, 25, 60, fill=colors.HexColor("#F2EEE6"), lw=0.3); d.r(23, 23.6, 25, 29, fill=TILEC, lw=0.3)  # plaster, flush skirting
    d.r(14, 15, 0, 13, fill=STONE)                                                                 # plinth cladding
    d.l([(14, 2), (-6, 0.5), (-6, -2), (14, -2)], fill=CONC, close=True)                          # apron sloped away
    d.l([(-6, 0), (-6, -0.2)])
    d.t("OUTSIDE", -5, 4, 5.5, GREY); d.t("INSIDE", 40, 30, 5.5, GREY)
    d.call(20, -27, "Footing by engineer after soil test; on black cotton soil often 1.5-2.5 m deep or under-reamed piles.")
    d.call(19.5, 6, "RCC plinth beam ties all columns; 75 mm sand cushion under it on expansive soil.")
    d.call(19.5, 12.5, "DPC 40 mm with waterproof compound at plinth top, under the first AAC course.")
    d.call(40, 9, "Moorum / gravel fill compacted in 150 mm layers; anti-termite treatment at each layer.")
    d.call(40, 22, "PCC bed 100 mm with polythene sheet, then screed and tile.")
    d.call(23.3, 27, "Skirting 4 in, flush with plaster face (plaster stops in a groove): no dust ledge.")
    d.call(14.5, 7, "Stone cladding on the plinth face to 2 ft: rain splash zone stays clean.")
    d.call(3, 1.2, "3 ft PCC apron sloping 1:30 away; polysulphide joint at the wall so water never reaches the foundation.")


def det_skirting(d):
    d.r(0, 6, 0, 40, fill=AAC)
    d.r(6, 7, 6, 40, fill=colors.HexColor("#F2EEE6"), lw=0.4)
    d.l([(6, 6), (7, 6), (7, 6.6), (6, 6.6)], lw=0.4, close=True)  # groove
    d.r(6, 7, 1.5, 5.6, fill=TILEC, lw=0.5)
    d.r(6, 40, -2, 1.0, fill=colors.HexColor("#CFCFCF"))
    d.r(7.25, 40, 1.0, 1.5, fill=TILEC, lw=0.4)
    d.r(6.95, 7.25, 1.0, 1.5, fill=colors.HexColor("#444444"), stroke=None)
    d.t("WALL", 1, 30, 5.5, GREY); d.t("ROOM", 25, 15, 5.5, GREY)
    d.call(6.5, 22, "Plaster stops 1/4 in above skirting in a clean groove.")
    d.call(6.6, 3.6, "Skirting tile 4 in high set in the plaster line, face flush with the wall.")
    d.call(7.1, 0.3, "5 mm gap filled with silicone / PU sealant: allows movement, no cracked tiles.")
    d.call(22, 2.5, "In wet rooms use a cove tile or wall tile down to the floor with epoxy grout instead.")


def det_sill(d):
    d.r(0, 9, 0, 30, fill=AAC)
    d.r(0, 9, 30, 36, fill=CONC)                                     # sill band / concrete sill
    d.l([(-3, 34.5), (9.5, 36), (9.5, 37), (-3, 35.5)], fill=STONE, close=True)  # external sill sloped
    d.r(9, 13, 36, 37, fill=STONE)                                   # internal sill
    d.r(3, 6, 37, 70, fill=WOOD)                                     # frame
    d.r(6.2, 6.6, 38, 69, fill=colors.HexColor("#C9DCE3"), lw=0.3)
    d.r(2.2, 2.6, 38, 69, fill=None, lw=0.3, dash=(0.6, 0.6))         # mesh
    d.r(0, 9, 70, 76, fill=CONC)                                     # lintel band
    d.l([(-22, 74.5), (0, 76), (0, 78), (-22, 76.5)], fill=CONC, close=True)  # chajja sloped
    d.l([(-20.5, 74.7), (-20.5, 74.2)], lw=1.2, color=WHITE)
    d.l([(-1.6, 34.6), (-1.6, 34.1)], lw=1.2, color=WHITE)
    d.t("OUT", -16, 20, 5.5, GREY); d.t("IN", 14, 20, 5.5, GREY)
    d.call(-9, 34.0, "External sill slopes out 1:10 and projects 2 in past the plaster with a drip groove underneath.")
    d.call(11, 37.8, "Internal sill in stone, 1/2 in higher than the outer sill (water cannot run inward).")
    d.call(4.5, 52, "Frame on a bed of sealant; gap to wall filled with PU foam and sealed both sides.")
    d.call(2.4, 62, "Insect mesh on a separate openable frame.")
    d.call(4.5, 73, "RCC lintel band continuous around the house at door-head level.")
    d.call(-12, 77, "Sunshade 1'-6\" to 2'-0\", top sloped out, drip groove under the front edge (no black streaks on walls).")


def det_eaves(d):
    d.r(30, 39, 0, 40, fill=AAC)
    d.r(29.5, 39.5, 40, 49, fill=CONC)                                  # ring beam
    d.r(31, 38, 49, 50, fill=colors.HexColor("#555555"))                # base plate
    d.l([(34.5, 44), (34.5, 51.5)], lw=1.2, color=colors.HexColor("#333333"))
    s30 = 0.577
    roof = lambda x: 50 + (x - 34.5) * s30
    d.l([(0, roof(0)), (62, roof(62))], lw=2, color=BROWN)              # rafter / top chord
    d.l([(0, roof(0) + 1.5), (62, roof(62) + 1.5), (62, roof(62) + 4.5), (0, roof(0) + 4.5)], fill=colors.HexColor("#E7E2D5"), close=True)  # deck + insulation
    d.l([(0, roof(0) + 4.5), (62, roof(62) + 4.5)], lw=0.8, color=WATERP)  # membrane
    for x in range(2, 62, 9):
        d.r(x, x + 1.5, roof(x) + 4.5, roof(x) + 6, fill=WOOD, lw=0.3)
    d.l([(-1, roof(-1) + 6), (62, roof(62) + 6), (62, roof(62) + 8), (-1, roof(-1) + 8)], fill=colors.HexColor("#C98B6B"), close=True)
    d.r(-2, -0.5, roof(0) - 3, roof(0) + 6, fill=WOOD)                  # fascia
    d.l([(-8, roof(0) - 2), (-8, roof(0) - 8), (-2, roof(0) - 8), (-2, roof(0) - 2)], lw=0.8)  # gutter
    d.l([(-8.5, roof(0) - 1.5), (-1.5, roof(0) - 1.5)], lw=0.4, dash=(0.6, 0.6))
    d.l([(-0.5, roof(0) - 3), (29.5, roof(0) - 3)], lw=0.4, dash=(1, 1))  # soffit with vent
    d.t("OUT", -6, 20, 5.5, GREY); d.t("ATTIC", 45, 51, 5.5, GREY)
    d.call(34.5, 44.5, "RCC ring beam with holding-down bolts cast in; truss shoe bolted, not just welded.")
    d.call(15, roof(15) + 3, "Cement-fibre deck + 50 mm insulation + breathable membrane under the battens.")
    d.call(10, roof(10) + 7, "Mangalore tiles; eave, verge, hip and ridge tiles clipped or screwed (cyclone wind).")
    d.call(-1.2, roof(0) + 3, "Fascia board with drip edge flashing into the gutter.")
    d.call(-5, roof(0) - 5, "150 mm gutter with leaf guard, falls 1:300 to downpipes.")
    d.call(14, roof(0) - 3, "Ventilated soffit with insect / bird mesh: hot attic air escapes at the ridge.")


def det_bath(d):
    d.r(-4, 0, 0, 84, fill=AAC)                                         # door-side wall
    d.r(96, 103, 0, 84, fill=AAC)                                       # far wall (wet wall)
    d.l([(-14, 0), (0, 0)], lw=0.6); d.l([(-14, 0.5), (0, 0.5)], lw=0.4)  # bedroom floor
    d.l([(0, 0.5), (4, 0)], lw=0.8)                                     # sloped granite threshold
    d.l([(4, 0), (54, -0.3), (90, -0.9), (92, -1.4), (96, -0.6)], lw=0.8)   # dry zone nearly flat, wet zone falls to drain
    d.l([(0, -1.4), (96, -2.4)], lw=1.0, color=WATERP)
    d.l([(96, -2.4), (96, 84)], lw=1.0, color=WATERP)
    d.l([(0, -1.4), (0, 12)], lw=1.0, color=WATERP)
    d.r(54, 54.4, 0, 72, fill=colors.HexColor("#C9DCE3"), lw=0.3)     # glass partition
    d.r(89, 93, -2.0, -0.8, fill=colors.HexColor("#555555"))           # linear drain
    d.r(96, 99, 60, 66, fill=colors.HexColor("#555555"))               # mixer
    d.t("BEDROOM", -13, 3, 5, GREY); d.t("DRY ZONE", 18, 10, 5.5, GREY); d.t("WET ZONE (SHOWER)", 62, 10, 5.5, GREY)
    d.call(2, 4, "Bathroom 12 mm below the bedroom floor with a sloped granite threshold: no raised step to trip on.")
    d.call(30, -1.5, "Waterproof membrane across the floor and 12 in up all walls; 48 h flood test before tiling.")
    d.call(96, 40, "Shower walls waterproofed to 7 ft; tiles to ceiling in the shower, 7 ft elsewhere.")
    d.call(91, 2, "Linear drain at the far wall; only the wet zone falls (1:60). Dry zone stays dry and safe.")
    d.call(54.2, 50, "8 mm toughened glass partition, 6 in clear of the floor drain line; matt fittings hide hard-water marks.")
    d.call(97.5, 72, "Concealed diverter and pipes in the 7 in wet wall; isolation valve outside the bathroom.")
    d.call(35, 60, "Exhaust fan high on the outer wall, opposite the door, ducted outside (not into the attic).")


def det_kitchen(d):
    d.r(-6, 0, 0, 96, fill=AAC)
    d.r(0, 24, 4, 33.4, fill=colors.HexColor("#EFE7DA"))                # base cabinet
    d.r(2, 22, 0, 4, fill=colors.HexColor("#555555"))                   # legs / toe kick
    d.r(0, 25, 33.4, 34.2, fill=STONE)                                  # granite
    d.l([(25, 33.4), (25, 32.8)], lw=1.0)
    d.r(0, 0.6, 34.2, 58, fill=TILEC, lw=0.3)                           # backsplash
    d.r(0, 14, 58, 88, fill=colors.HexColor("#EFE7DA"))                 # wall cabinet
    d.r(0, 20, 64, 72, fill=colors.HexColor("#777777"))                 # chimney hood
    d.l([(10, 72), (10, 96)], lw=2, color=colors.HexColor("#777777"))
    d.l([(-8, 0), (40, 0)], lw=0.8)
    d.t("34 in", 30, 17, 5.5); d.l([(28, 0), (28, 34.2)], lw=0.3)
    d.t("24 in", 10, -4, 5.5, anchor="c")
    d.call(12, 20, "Counter top at 34 in (865 mm) for standing cooking; 30-31 in section for a chapati / grinding area.")
    d.call(12, 2, "Base units on 4 in legs or a granite plinth: floor can be mopped, no termites, no water damage.")
    d.call(24, 33.8, "20 mm granite (local Chimakurthy / Ongole) with a drip edge; sink under the window, hob on the east run.")
    d.call(0.3, 46, "Stone or tile between counter and wall cabinets, full height; no painted wall behind the hob.")
    d.call(10, 68, "Chimney 26-30 in above the hob, ducted straight out through the wall (no long bends).")
    d.call(7, 80, "Wall cabinets 14 in deep, starting 22-24 in above the counter; plenty of 16 A sockets at 42 in.")


def det_basin(d):
    d.r(-6, 0, 0, 84, fill=AAC)
    d.r(0, 0.5, 30, 54, fill=TILEC, lw=0.3)
    d.l([(0, 32), (20, 32), (20, 29), (16, 25), (0, 25)], fill=colors.HexColor("#F5F5F5"), close=True)  # wall-hung basin
    d.r(2, 4, 12, 25, fill=colors.HexColor("#999999"))                   # bottle trap / waste
    d.r(0, 1, 40, 72, fill=colors.HexColor("#C9DCE3"), lw=0.3)           # mirror
    d.r(0, 6, 74, 76, fill=colors.HexColor("#FFE8A3"))                   # light
    d.r(0, 4, 36, 37.2, fill=STONE)                                      # shelf / niche
    d.l([(-8, 0), (40, 0)], lw=0.8)
    d.l([(26, 0), (26, 32)], lw=0.3); d.t("32 in", 27, 15, 5.5)
    d.call(10, 30, "Wall-hung basin, rim at 32 in (810 mm); bottle trap, so the floor below can be cleaned.")
    d.call(0.3, 44, "Tiled or stone splash-back 2 ft above the basin: painted walls stain and peel here.")
    d.call(0.5, 60, "Mirror from 40 in to 72 in, light above (not behind) the mirror, socket at 42 in kept 2 ft from the tap.")
    d.call(2, 36.5, "Soap / shelf niche recessed into the wall, sloped forward so water does not pool.")
    d.call(3, 18, "Waste pipe into the wall, not across the floor; a floor trap is not needed for a dining-area basin.")
    d.call(18, 8, "Children: keep a fold-down step; tap with a long spout so water lands in the bowl, not on the counter.")


def det_aac(d):
    d.r(0, 12, 0, 60, fill=CONC)                                         # column
    d.r(12, 60, 0, 60, fill=AAC)
    for y in range(0, 60, 8): d.l([(12, y), (60, y)], lw=0.2, color=GREY)
    d.r(0, 60, 60, 66, fill=CONC)
    d.r(6, 18, 0, 60, fill=None, lw=0.6, stroke=RED, dash=(1, 0.6))
    d.r(12, 60, 54, 66, fill=None, lw=0.6, stroke=RED, dash=(1, 0.6))
    d.r(38, 39.5, 6, 46, fill=colors.HexColor("#FFFFFF"), lw=0.4)
    d.call(12, 30, "Galvanised mesh 150 mm wide, centred on every AAC-to-column and AAC-to-beam joint, before plaster.")
    d.call(36, 59, "Top course: 20 mm gap under the beam packed with PU foam / flexible filler, not rigid mortar.")
    d.call(40, 35, "Chases cut with a wall chaser, max 1/3 of block depth; refill with polymer mortar + mesh.")
    d.call(30, 10, "Thin-bed polymer mortar 3 mm, blocks laid dry; first course on the DPC in normal mortar to level.")


def det_threshold(d):
    d.r(-30, 0, -6, 0, fill=colors.HexColor("#CFCFCF"))
    d.r(0, 36, -6, 6, fill=colors.HexColor("#CFCFCF"))
    d.l([(-30, 0), (-2, 0.6), (0, 1.8), (6, 6)], lw=0.8)
    d.r(0, 6, 6, 7, fill=TILEC)
    d.r(6, 36, 6, 7, fill=TILEC)
    d.r(1, 5, 7, 60, fill=WOOD)
    d.r(1, 5, 7, 11, fill=colors.HexColor("#555555"))
    d.r(-24, 0, 6, 24, fill=colors.HexColor("#C9DCE3"), lw=0.3, dash=(1, 1))
    d.t("OUTSIDE / WET AREA", -29, 9, 5, GREY); d.t("INSIDE", 18, 12, 5.5, GREY)
    d.call(-14, 1.2, "Outside floor 3-6 in lower than inside and sloping away 1:50: rain never flows in.")
    d.call(2, 2.8, "Granite threshold with a 1 in upstand / weather bar under external doors.")
    d.call(3, 9, "Wet-area door frames stand on a granite or WPC block; wood never touches a wet floor.")
    d.call(-12, 18, "Open wet area: floor 3 in lower and sloping out to the walkway, so rain drains away from the kitchen door.")


BOUNDS = {det_plinth: (-8, 62, -31, 62), det_skirting: (-2, 42, -3, 42), det_sill: (-24, 16, -2, 80),
          det_eaves: (-10, 64, -2, 76), det_bath: (-16, 104, -4, 86), det_kitchen: (-10, 42, -6, 98),
          det_basin: (-8, 42, -2, 86), det_aac: (-2, 62, -2, 68), det_threshold: (-32, 38, -8, 62)}


def _place(s, fn, title, num, x, y, w, h, notes_h=34):
    d = D(s, x, y, w, h, title, num, BOUNDS[fn], notes_h)
    fn(d); d.finish()


def sheet_details_1(c):
    s = Sheet(c, "A-501", "Typical details 1: plinth, floor, window, eaves", "NTS")
    W, H = 158 * mm, 128 * mm
    _place(s, det_plinth, "Plinth, DPC, floor and apron", 1, 14 * mm, 147 * mm, W, H)
    _place(s, det_skirting, "Flush skirting at floor-wall joint", 2, 176 * mm, 147 * mm, W, H)
    _place(s, det_sill, "Window sill, frame and sunshade", 3, 14 * mm, 15 * mm, W, H)
    _place(s, det_eaves, "Eaves, gutter and roof build-up", 4, 176 * mm, 15 * mm, W, H)
    c.showPage()


def sheet_details_2(c):
    s = Sheet(c, "A-502", "Typical details 2: bath, kitchen, basin, AAC", "NTS")
    W1, H1, W2 = 158 * mm, 128 * mm, 104 * mm
    _place(s, det_bath, "Bathroom: wet and dry zones", 5, 14 * mm, 147 * mm, W1, H1)
    _place(s, det_kitchen, "Kitchen counter and chimney", 6, 176 * mm, 147 * mm, W1, H1)
    _place(s, det_basin, "Hand-wash basin (serving counter)", 7, 14 * mm, 15 * mm, W2, H1)
    _place(s, det_aac, "AAC wall joints and chases", 8, 122 * mm, 15 * mm, W2, H1)
    _place(s, det_threshold, "Door thresholds and rain kerbs", 9, 230 * mm, 15 * mm, W2, H1)
    c.showPage()
