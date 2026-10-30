"""A-401: door and window elevations, drawn from the door and window schedules."""
from sheetlib import *

DOOR_NOTES = {
    "D01": "Teak, double leaf, panelled; 4 in raised threshold outside slope; tower bolts + mortise lock",
    "D02": "MS frame + grill shutter outside, mesh door inside; 1 in weather bar",
    "D03": "Sliding laminated glass, brush seals, soft-close; frosted band at 3-5 ft",
    "D05": "WPC/FRP shutter, frame on granite base; louvre at bottom",
    "D08": "WPC/FRP shutter, frame on granite base; louvre at bottom",
    "D12": "WPC/FRP shutter, frame on granite base",
}


def _door(pl, x, d, h=7.0):
    w = d[4] - d[3]
    t = d[7].lower()
    glass = "glass" in t
    tr = TRANSOMS.get(d[0])
    if tr:  # vent above the door, over the lintel band
        z1, z2 = TRANSOM_Z
        pl.rect(x - 0.25, x + w + 0.25, h + 0.25, z1, lw=0.4, fill=LIGHT)
        pl.rect(x - 0.25, x + w + 0.25, z1, z2, lw=0.8, fill={"jali": colors.HexColor("#8E6B4E"), "jali_closable": colors.HexColor("#8E6B4E"), "louvre": colors.HexColor("#D9D9D9"), "glazed": colors.HexColor("#C9DCE3")}[tr])
        if tr.startswith("jali"):
            for i in range(1, int(w / 0.4) + 1): pl.line(x + i * 0.4, z1, x + i * 0.4, z2, lw=0.2, color=WHITE)
            pl.line(x - 0.25, (z1 + z2) / 2, x + w + 0.25, (z1 + z2) / 2, lw=0.2, color=WHITE)
            if tr == "jali_closable":  # sliding shutter, shown half open
                pl.rect(x - 0.25, x + w / 2, z1 + 0.1, z2 - 0.1, lw=0.6, fill=colors.HexColor("#C9A97F"))
                pl.line(x + w / 2 + 0.2, (z1 + z2) / 2, x + w / 2 + 0.7, (z1 + z2) / 2, lw=0.6)
        elif tr == "louvre":
            for j in range(1, 5): pl.line(x - 0.25, z1 + j * (z2 - z1) / 5, x + w + 0.25, z1 + j * (z2 - z1) / 5, lw=0.4)
        else:
            pl.line(x - 0.25, z2, x + (w + 0.5) / 2 - 0.25, z1, lw=0.25, dash=(1, 1)); pl.line(x + (w + 0.5) / 2 - 0.25, z1, x + w + 0.25, z2, lw=0.25, dash=(1, 1))
    pl.rect(x - 0.25, x + w + 0.25, 0, h + 0.25, lw=0.9, fill=colors.HexColor("#6B4A2E") if not glass else None)
    fill = colors.HexColor("#C9DCE3") if glass else (colors.HexColor("#E6D8C3") if "teak" in t or "carved" in t else colors.HexColor("#ECECEC"))
    if d[5] == 0:
        pl.rect(x, x + w * 0.55, 0, h, lw=0.5, fill=fill); pl.rect(x + w * 0.45, x + w, 0, h, lw=0.5, fill=fill)
        pl.line(x + w * 0.2, h / 2, x + w * 0.35, h / 2, lw=0.6); pl.line(x + w * 0.65, h / 2, x + w * 0.8, h / 2, lw=0.6)
    elif "double" in t:
        pl.rect(x, x + w / 2, 0, h, lw=0.5, fill=fill); pl.rect(x + w / 2, x + w, 0, h, lw=0.5, fill=fill)
        for a in (x, x + w / 2):
            pl.rect(a + 0.3, a + w / 2 - 0.3, 0.6, 3.2, lw=0.3); pl.rect(a + 0.3, a + w / 2 - 0.3, 3.8, h - 0.6, lw=0.3)
    else:
        pl.rect(x, x + w, 0, h, lw=0.5, fill=fill)
        if "panel" in t: pl.rect(x + 0.3, x + w - 0.3, 0.6, h - 0.6, lw=0.3)
        hinge_left = d[5] > 0
        pl.line(x + (w if hinge_left else 0), h * 0.5, x + (0 if hinge_left else w), 0, lw=0.25, dash=(1, 1))
        pl.line(x + (w if hinge_left else 0), h * 0.5, x + (0 if hinge_left else w), h, lw=0.25, dash=(1, 1))
        if "waterproof" in t:
            pl.rect(x - 0.25, x + w + 0.25, 0, 0.33, lw=0.4, fill=colors.HexColor("#555555"))
            for i in range(4): pl.line(x + 0.3, 0.5 + i * 0.18, x + w - 0.3, 0.5 + i * 0.18, lw=0.3)
    return w


def _window(pl, x, w_rec):
    w = w_rec[4] - w_rec[3]; sill, head = w_rec[5], w_rec[6]
    t = w_rec[8].lower()
    pl.rect(x - 0.6, x + w + 0.6, 0, 8.6, stroke=LIGHT, lw=0.3)
    pl.line(x - 0.6, 0, x + w + 0.6, 0, lw=0.6)
    jali = "jali" in t
    pl.rect(x, x + w, sill, head, lw=0.8, fill=colors.HexColor("#8E6B4E") if jali else colors.HexColor("#C9DCE3"))
    if jali:
        n = max(2, int(w / 0.5)); m = max(2, int((head - sill) / 0.5))
        for i in range(1, n): pl.line(x + i * w / n, sill, x + i * w / n, head, lw=0.2, color=WHITE)
        for j in range(1, m): pl.line(x, sill + j * (head - sill) / m, x + w, sill + j * (head - sill) / m, lw=0.2, color=WHITE)
    else:
        leaves = 1 if w <= 3 else (2 if w <= 5 else 3)
        for i in range(1, leaves): pl.line(x + i * w / leaves, sill, x + i * w / leaves, head, lw=0.4)
        if "louvre" in t:
            for j in range(1, 6): pl.line(x, sill + j * (head - sill) / 6, x + w, sill + j * (head - sill) / 6, lw=0.3)
    pl.rect(x - 0.5, x + w + 0.5, head + 0.2, head + 0.45, lw=0.4, fill=LIGHT)  # sunshade
    pl.rect(x - 0.15, x + w + 0.15, sill - 0.15, sill, lw=0.4, fill=LIGHT)      # sill
    return w


def sheet_doors_windows(c):
    s = Sheet(c, "A-401", "Door and window details", "1:60")
    k = 304.8 / 60 * mm
    st = ParagraphStyle("d", fontName="Helvetica", fontSize=5.2, leading=6)
    # doors
    pl = Plan(s, 60, 18 * mm, 206 * mm)
    s.note("DOORS (viewed from the side the door swings into; vents above inner doors, 7'-6\" to 9'-0\"; none at bedrooms or bathrooms)", 18 * mm, 266 * mm, 9, INK, "Helvetica-Bold")
    x = 0.5
    for d in DOORS:
        w = _door(pl, x, d)
        pl.text(d[0], x + w / 2, 9.6, 6.5, "Helvetica-Bold", ACC)
        pl.text(f"{fmt_ft(w)} x 7'-0\"", x + w / 2, -0.9, 5.2)
        p = Paragraph(DOOR_NOTES.get(d[0], d[7]) + (f"<br/><i>Above: {TRANSOM_LABELS[TRANSOMS[d[0]]].lower()}</i>" if d[0] in TRANSOMS else ("<br/><i>No vent above</i>" if (d[1], d[2]) not in EXTERIOR else "")), st); pw, ph = p.wrap(max(w, 2.8) * k + 5 * mm, 30 * mm)
        p.drawOn(c, pl.p(x - 0.4, 0)[0], pl.p(0, -1.6)[1] - ph)
        x += max(w, 2.8) + 1.7
    # windows
    rows = [WINDOWS[:8], WINDOWS[8:]]
    for ri, row in enumerate(rows):
        oy = (126 - ri * 66) * mm
        pl = Plan(s, 60, 18 * mm, oy)
        if ri == 0:
            s.note("WINDOWS (viewed from inside; sill and head heights above floor)", 18 * mm, oy + 52 * mm, 9, INK, "Helvetica-Bold")
        x = 1.0
        for w_rec in row:
            w = _window(pl, x, w_rec)
            pl.text(w_rec[0], x + w / 2, 9.3, 6.5, "Helvetica-Bold", ACC)
            pl.text(f"{fmt_ft(w)} wide, sill {fmt_ft(w_rec[5])}, head {fmt_ft(w_rec[6])}", x + w / 2, -0.9, 5)
            p = Paragraph(w_rec[8], st); pw, ph = p.wrap(max(w, 3) * k + 5 * mm, 30 * mm)
            p.drawOn(c, pl.p(x - 0.5, 0)[0], pl.p(0, -1.6)[1] - ph)
            x += max(w, 3) + 2.6
    notes = [
        "All windows: insect mesh (SS or fibreglass) on a separate openable or sliding frame, so glass can be cleaned.",
        "MS safety grill inside the shutters on every ground-floor window; one escape window per bedroom with an openable grill section.",
        "Teak is costly and must be seasoned; good alternatives in Guntur: sal or hard pinkado for frames, UPVC for wet-side windows.",
        "Door frames 5 x 2.5 in; frames in bathrooms and wet areas stand on granite or WPC blocks, never touching the wet floor.",
        "Hardware: SS 304 hinges and screws (hard water and humidity rust MS); magnetic door stoppers on every door.",
        "Sunshade (chajja) over every window projects 1'-6\" to 2'-0\" with a drip groove under the front edge.",
    ]
    s.bullets(notes, 18 * mm, 37 * mm, 300 * mm, 6.0)
    c.showPage()
