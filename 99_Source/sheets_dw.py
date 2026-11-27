"""A-401 (doors, by type) and A-402 (windows, both floors): elevations drawn from the door and window schedules."""
from sheetlib import *



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
    if "folding" in t:
        n = max(2, int(round(w / 1.6)))
        for i in range(n):
            pl.rect(x + i * w / n, x + (i + 1) * w / n, 0, h, lw=0.5, fill=fill)
        for i in range(n // 2):   # fold lines: the panels stack in pairs
            a = x + 2 * i * w / n
            pl.poly([(a, h * 0.5), (a + w / n, h * 0.42), (a + 2 * w / n, h * 0.5)], lw=0.25, dash=(1, 1))
    elif d[5] == 0:
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


def _rows(items, width, limit):
    """Split items into rows no wider than limit (ft at the sheet scale)."""
    rows, cur, used = [], [], 0
    for it in items:
        step = width(it)
        if used + step > limit and cur:
            rows.append(cur); cur, used = [], 0
        cur.append(it); used += step
    if cur: rows.append(cur)
    return rows


ROW_FT = 76   # usable width of a row at 1:75, ft


WIN_COLS = 7            # windows per row on A-402
WIN_SCALE = 100         # elevations at 1:100 so both floors fit one sheet
WIN_ELEV_FT = 6.4       # width kept for each elevation, ft (widest window 5 ft plus its frame)


def _window_grid(s, c, st, groups, ytop, ymin, xleft=18 * mm, xright=DRAW_W):
    """A grid of window cells: each cell holds the elevation (left) and its tag, size and wrapped note (right).

    groups: [(heading, [window records])]; every group starts on a fresh row under its heading.
    Returns the y below the last row; asserts that the grid stays above ymin and every note fits its cell."""
    k = 304.8 / WIN_SCALE * mm
    nrows = sum(-(-len(ws) // WIN_COLS) for _, ws in groups)
    head_h = 5 * mm
    cell_w = (xright - xleft) / WIN_COLS
    cell_h = (ytop - ymin - head_h * len(groups)) / nrows
    elev_ft = max(max(8.6, w[6] + 0.45) for _, ws in groups for w in ws)
    assert elev_ft * k + 3 * mm <= cell_h, f"window cells {cell_h / mm:.1f} mm tall, need {(elev_ft * k + 3 * mm) / mm:.1f} mm"
    note_x = WIN_ELEV_FT * k + 2 * mm
    note_w = cell_w - note_x - 1.5 * mm
    y = ytop
    for heading, ws in groups:
        s.note(heading, xleft, y - 3.5 * mm, 7.5, INK, "Helvetica-Bold")
        y -= head_h
        for i, w_rec in enumerate(ws):
            col, row = i % WIN_COLS, i // WIN_COLS
            cx, cy = xleft + col * cell_w, y - row * cell_h          # cell top-left
            if col == 0:
                c.setStrokeColor(LIGHT); c.setLineWidth(0.3); c.line(xleft, cy, xright, cy)
            w = w_rec[4] - w_rec[3]
            pl = Plan(s, WIN_SCALE, cx + (WIN_ELEV_FT / 2 - w / 2) * k, cy - cell_h + 2 * mm)
            _window(pl, 0, w_rec)
            tx = cx + note_x
            s.note(w_rec[0], tx, cy - 4 * mm, 7, ACC, "Helvetica-Bold")
            s.note(f"{fmt_ft(w)} wide", tx, cy - 6.8 * mm, 4.8, INK)
            s.note(f"sill {fmt_ft(w_rec[5])}, head {fmt_ft(w_rec[6])}", tx, cy - 8.8 * mm, 4.8, INK)
            assert c.stringWidth(f"sill {fmt_ft(w_rec[5])}, head {fmt_ft(w_rec[6])}", "Helvetica", 4.8) <= note_w
            t = w_rec[8].split("; ")[0]
            p = Paragraph(t, st)
            pw, ph = p.wrap(note_w, cell_h)
            assert ph <= cell_h - 12 * mm, f"{w_rec[0]} note {ph / mm:.1f} mm does not fit its cell"
            p.drawOn(c, tx, cy - 10.3 * mm - ph)
        y -= -(-len(ws) // WIN_COLS) * cell_h
    assert y >= ymin - 0.01, f"windows run down to {y / mm:.0f} mm"
    return y


def door_types():
    """Doors grouped by type: same width, same build and the same vent above draw once, with all their ids."""
    g = {}
    for d in both("DOORS"):
        g.setdefault((round(d[4] - d[3], 2), d[7], d[5] == 0, TRANSOMS.get(d[0])), []).append(d)
    return list(g.values())


def sheet_windows_f1(c):
    s = Sheet(c, "A-402", "Window details, both floors", "1:100")
    st = ParagraphStyle("d", fontName="Helvetica", fontSize=4.6, leading=5.3)
    with on_floor("G"):
        g = list(WINDOWS)
    with on_floor("F1"):
        f1 = list(WINDOWS)
    s.note("WINDOWS, BOTH FLOORS (viewed from inside; sill and head above the room's floor; full notes in the schedules)", 18 * mm, 270 * mm, 9, INK, "Helvetica-Bold")
    _window_grid(s, c, st, [(f"GROUND FLOOR ({len(g)} windows)", g), (f"FIRST FLOOR ({len(f1)} windows)", f1)], 266 * mm, 34 * mm)
    notes = [
        "All windows: insect mesh (SS or fibreglass) on a separate openable or sliding frame, so glass can be cleaned. MS safety grill inside the shutters on every ground-floor window; one escape window per bedroom with an openable grill section.",
        "Courtyard-side windows open onto the walkway under the lean-to; the outer walls' windows sit under the ring roof's 2 ft eave, with sunshades (chajjas, 1'-6\" to 2'-0\", drip groove) on the south and west. The jharokha openings (W46, W47) are glazed above a fixed jali: see the bay on A-202 and A-301.",
    ]
    s.bullets(notes, 18 * mm, 26 * mm, 300 * mm, 6.0)
    c.showPage()


def sheet_doors_windows(c):
    s = Sheet(c, "A-401", "Door details", "1:75")
    k = 304.8 / 75 * mm
    st = ParagraphStyle("d", fontName="Helvetica", fontSize=4.8, leading=5.6)
    s.note("DOORS BY TYPE (viewed from the side the door swings into; vents above inner doors, 7'-6\" to 9'-0\"; none at bedrooms or bathrooms)", 18 * mm, 270 * mm, 9, INK, "Helvetica-Bold")
    rows = _rows(door_types(), lambda g: max(g[0][4] - g[0][3], 2.8) + 1.9, ROW_FT)
    oy = 212 * mm   # each row sits 6 mm below the lowest note of the row above
    for ri, row in enumerate(rows):
        pl = Plan(s, 75, 18 * mm, oy)
        x = 0.5
        low = oy
        for grp in row:
            d = grp[0]
            w = _door(pl, x, d, DOOR_HEIGHTS.get(d[0], 7.0))
            ids = [g[0] for g in grp]
            pl.text(d[0] if len(ids) == 1 else f"{d[0]} (x{len(ids)})", x + w / 2, 9.6, 6.2, "Helvetica-Bold", ACC)
            pl.text(f"{fmt_ft(w)} x {fmt_ft(DOOR_HEIGHTS.get(d[0], 7.0))}", x + w / 2, -0.9, 5.0)
            head = "" if len(ids) == 1 else "<b>" + ", ".join(ids) + ":</b> "
            p = Paragraph(head + d[7] + (f"<br/><i>Above: {TRANSOM_LABELS[TRANSOMS[d[0]]].lower()}</i>" if d[0] in TRANSOMS else ""), st)
            pw, ph = p.wrap(max(w, 2.8) * k + 6 * mm, 30 * mm)
            p.drawOn(c, pl.p(x - 0.4, 0)[0], pl.p(0, -1.6)[1] - ph)
            low = min(low, pl.p(0, -1.6)[1] - ph)
            x += max(w, 2.8) + 1.9
        assert low >= 34 * mm, f"door row {ri + 1} runs down to {low / mm:.0f} mm, into the notes"
        oy = low - 6 * mm - 9.9 * k
    notes = [
        "Teak is costly and must be seasoned; good alternatives in Guntur: sal or hard pinkado for frames, UPVC or WPC on the wet side. Door frames 5 x 2.5 in; frames in bathrooms and wet areas stand on granite or WPC blocks, never touching the wet floor.",
        "Hardware: SS 304 hinges and screws (hard water and humidity rust MS); magnetic door stoppers on every door. Every external door gets a mosquito-mesh shutter.",
        "Folding doors to the walkway (D60, D62): teak frame and toughened glass on a top track and a flush floor channel, stacked to the pier in the day, bolted shut at night.",
    ]
    s.bullets(notes, 18 * mm, 30 * mm, 300 * mm, 6.0)
    c.showPage()
