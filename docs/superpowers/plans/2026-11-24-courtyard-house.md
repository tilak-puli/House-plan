# Courtyard House Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the approved courtyard concept into the same full output set as the duplex. That means the drawing set PDF, the DXF, the schedules XLSX, the room detailing guide and the walkable 3D model, all generated from `99_Source/model.py`.

**Architecture:** One data file, `model.py`, describes the house, and every output is generated from it by `build.py`. This plan:

1. Rewrites `model.py` for the courtyard plan, from a small set of grid constants.
2. Replaces the duplex-specific roof geometry in `geom.py` with a ring roof round the courtyard plus a hipped west wing.
3. Adapts the sheet modules and the hand-written 3D builders where they assume the duplex's shape (poomukham, front gable, kitchen wing, chaipu roofs, the house box).

A new pytest suite guards the model's geometry and the build at every step.

**Tech Stack:**
- Python 3 in `99_Source/.venv`: reportlab 4.5.1, ezdxf 1.4.2, openpyxl 3.1.5, plus pytest (added in Task 1).
- three.js inside `04_3D/KH-P1_3D_Model.html`.
- The in-app browser for 3D walk tests.

**Spec:** `01_Brief/Courtyard_Concept_Spec.md` (read it first; it is the source of every size and decision below).

## Global Constraints

- **Branch:** work only on `feature/courtyard`. Never touch `feature/duplex` or `main`.
- **Commits and pushes:** commit and push only when the owner says so. Commits are anonymous:

  ```bash
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null git -c user.name="House plan" -c user.email="" commit -q -m "<message>

  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
  ```

- **Never** put the owner's real site coordinates in files or URLs.
- **Never** use the `gh` CLI.
- **Coordinates:** feet; x runs from the back (west) boundary, y from the south boundary.
- **Walls:** `(axis, c, s, e)`. `"X"` runs along x at y = c; `"Y"` runs along y at x = c.
- **Doors:** `(id, axis, c, s, e, swing, note, material)`. Swing +1 opens toward +y/+x, -1 toward -y/-x, 0 is sliding.
- **Furniture:** `(id, room, note, x1, x2, y1, y2, qty, material, shape)`.
- **Spec sizes, copied from the spec:**
  - Plot: 70 ft wide × 160 ft deep, road on the east.
  - House: x 18–72, y 8–62 (54 × 54).
  - Room bands: 16 ft deep.
  - Walkway: 4 ft wide.
  - Courtyard: 14 × 14, open to the sky.
  - Thinnai: x 72–79, two platforms 7 × 8.
- **Stair:**
  - 16 risers of 7.5 in, 10 in treads, 3'-6" flights, rising clockwise.
  - Handrails on both sides.
  - Guards 4'-0" high, with gaps of 100 mm or less.
- **Vastu:**

  | Element | Placement |
  |---|---|
  | Main door | East, on the axis y = 35 |
  | Courtyard | On the brahmasthan (the house centre) |
  | Pooja | North-east |
  | Kitchen | South-east |
  | Master bedroom | South-west, bed head south |
  | Den | North-west |
  | Stair | West |
  | Upper mass | West and south-west only |
  | Toilets | None in the north-east |

- **Bathrooms:** the basin and mirror sit straight opposite each bathroom door. The WC is never in line with the door and never in a mirror's view.
- **Carry-overs:** every carried-over duplex feature listed in spec section 10 must appear in the model.
- **The project 3D file:** `04_3D/KH-P1_3D_Model.html` must contain 0 `__walk`. The walk hooks go only into the scratchpad test copy.
- **3D artifact:** publish the courtyard 3D model as a new artifact. Never publish it to the duplex artifact `4gUCb98XDmcoBHPQFHVAVc`.

---

## File structure

| File | Responsibility | Change |
|---|---|---|
| `99_Source/requirements.txt` | Python dependencies | Add `pytest==8.3.3` |
| `99_Source/tests/conftest.py` | Puts `99_Source` on `sys.path` | Create |
| `99_Source/tests/test_model_invariants.py` | Geometry rules that hold for any house: rooms do not overlap; doors and windows sit on walls; furniture inside its room | Create (Task 1) |
| `99_Source/tests/test_build.py` | `build.py` runs and every output exists; one `@MODEL` block; no `__walk` | Create (Task 1) |
| `99_Source/tests/test_courtyard.py` | Courtyard-specific rules: plot, grid, vastu zones, reachability, bath layout, upper wing, stair well | Create (Tasks 2–7) |
| `99_Source/tests/test_roof.py` | Ring roof heights | Create (Task 9) |
| `99_Source/planlib.py` | Pure helpers used by the tests and by `model.py`: rect maths, shared edges, reachability graph | Create (Task 1) |
| `99_Source/model.py` | The courtyard house data | Rewrite section by section (Tasks 2–8) |
| `99_Source/geom.py` | Roof heights and areas | Replace the duplex roof functions (Task 9) |
| `99_Source/sheets_arch.py` | Site, plans, roof plan, schedules | `sheet_roof` rewritten; `sheet_site` and `sheet_phasing` checked (Tasks 9–10) |
| `99_Source/sheets_elev.py` | Elevations and sections | Roof profile drawn from `geom.roof_z` instead of the gable, wing and chaipu helpers (Task 10) |
| `99_Source/make_3d.py` | Model data for the 3D page | New keys for the courtyard, walkway, pillars, thinnai, jharokhas, roof and terrace canopy (Task 11) |
| `04_3D/KH-P1_3D_Model.html` | Hand-written three.js builders | Ring roof, courtyard floor and grille, thinnai, jharokha builder; poomukham-specific code removed; `KIND` map updated (Task 11) |
| `01_Brief/Courtyard_Concept_Spec.md` | The approved spec | Kept in step with any layout change agreed at the Task 3 and Task 6 checkpoints |

---

### Task 1: Test harness and generic invariants

**Files:**
- Modify: `99_Source/requirements.txt`
- Create: `99_Source/planlib.py`
- Create: `99_Source/tests/conftest.py`
- Create: `99_Source/tests/test_model_invariants.py`
- Create: `99_Source/tests/test_build.py`
- Modify: `99_Source/model.py` (add `OUTDOOR_FURNITURE`)

**Interfaces:**
- **Produces:** `planlib.overlap(a, b) -> float`, the overlap area of two rects `(x1, x2, y1, y2)`.
- **Produces:** `planlib.inside(pt, r, tol=0.01) -> bool`.
- **Produces:** `planlib.on_wall(axis, c, s, e, walls, tol=0.01) -> bool`. True when a door or window span lies within one wall segment on the same axis and line.
- **Produces:** `planlib.graph(rooms, walls, doors, min_open=2.0) -> dict[str, set[str]]`. Rooms are linked by a door, or by a shared edge where no wall covers at least `min_open` ft.
- **Produces:** `planlib.reachable(g, start) -> set[str]`.
- **Produces:** `model.OUTDOOR_FURNITURE: set[str]`, the furniture ids placed outside the house on purpose.

- [ ] **Step 1: Add pytest and make the venv current**

Append `pytest==8.3.3` to `99_Source/requirements.txt`, then run:

```bash
cd 99_Source && .venv/bin/pip install -q -r requirements.txt && .venv/bin/python -m pytest --version
```

Expected: `pytest 8.3.3`

- [ ] **Step 2: Write `planlib.py`**

```python
"""Small geometry helpers shared by model checks and tests. Rects are (x1, x2, y1, y2) in feet."""


def overlap(a, b):
    w = min(a[1], b[1]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[2], b[2])
    return w * h if w > 0 and h > 0 else 0.0


def inside(pt, r, tol=0.01):
    x, y = pt
    return r[0] - tol <= x <= r[1] + tol and r[2] - tol <= y <= r[3] + tol


def on_wall(axis, c, s, e, walls, tol=0.01):
    lo, hi = min(s, e), max(s, e)
    return any(w[0] == axis and abs(w[1] - c) <= tol and min(w[2], w[3]) - tol <= lo and hi <= max(w[2], w[3]) + tol for w in walls)


def _covered(axis, c, a, b, walls, tol=0.01):
    """Length of the segment [a, b] on line (axis, c) covered by wall segments."""
    spans = sorted((max(a, min(w[2], w[3])), min(b, max(w[2], w[3]))) for w in walls if w[0] == axis and abs(w[1] - c) <= tol)
    total, cur = 0.0, a
    for s, e in spans:
        if e <= cur:
            continue
        s = max(s, cur)
        total += max(0.0, e - s)
        cur = max(cur, e)
    return total


def graph(rooms, walls, doors, min_open=2.0):
    """rooms: [(id, x1, x2, y1, y2)]. Two rooms are linked by a door on their shared edge, or by an opening at least min_open ft long."""
    g = {r[0]: set() for r in rooms}
    for i, a in enumerate(rooms):
        for b in rooms[i + 1:]:
            for axis, c, lo, hi in _shared_edges(a, b):
                door = any(d[1] == axis and abs(d[2] - c) < 0.01 and lo - 0.01 <= min(d[3], d[4]) and max(d[3], d[4]) <= hi + 0.01 for d in doors)
                gap = (hi - lo) - _covered(axis, c, lo, hi, walls)
                if door or gap >= min_open:
                    g[a[0]].add(b[0]); g[b[0]].add(a[0])
    return g


def _shared_edges(a, b, tol=0.01):
    _, ax1, ax2, ay1, ay2 = a
    _, bx1, bx2, by1, by2 = b
    out = []
    for xa in (ax1, ax2):
        for xb in (bx1, bx2):
            if abs(xa - xb) <= tol:
                lo, hi = max(ay1, by1), min(ay2, by2)
                if hi - lo > tol:
                    out.append(("Y", xa, lo, hi))
    for ya in (ay1, ay2):
        for yb in (by1, by2):
            if abs(ya - yb) <= tol:
                lo, hi = max(ax1, bx1), min(ax2, bx2)
                if hi - lo > tol:
                    out.append(("X", ya, lo, hi))
    return out


def reachable(g, start):
    seen, todo = {start}, [start]
    while todo:
        for n in g[todo.pop()]:
            if n not in seen:
                seen.add(n); todo.append(n)
    return seen
```

- [ ] **Step 3: Write `tests/conftest.py`**

```python
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
```

- [ ] **Step 4: Write `tests/test_model_invariants.py`**

```python
import pytest

import model as M
from planlib import inside, on_wall, overlap

FLOORS = ["G", "F1"]


def floor(name):
    with M.on_floor(name):
        return (list(M.ROOMS), list(M.WALLS), list(M.DOORS), list(M.WINDOWS), list(M.FURNITURE))


@pytest.mark.parametrize("fl", FLOORS)
def test_rooms_do_not_overlap(fl):
    rooms = floor(fl)[0]
    bad = [(a[0], b[0]) for i, a in enumerate(rooms) for b in rooms[i + 1:] if overlap(a[2:6], b[2:6]) > 0.05]
    assert not bad, f"overlapping rooms on {fl}: {bad}"


@pytest.mark.parametrize("fl", FLOORS)
def test_doors_sit_on_walls(fl):
    _, walls, doors, _, _ = floor(fl)
    bad = [d[0] for d in doors if not on_wall(d[1], d[2], d[3], d[4], walls)]
    assert not bad, f"doors off any wall on {fl}: {bad}"


@pytest.mark.parametrize("fl", FLOORS)
def test_windows_sit_on_walls(fl):
    _, walls, _, windows, _ = floor(fl)
    bad = [w[0] for w in windows if not on_wall(w[1], w[2], w[3], w[4], walls)]
    assert not bad, f"windows off any wall on {fl}: {bad}"


@pytest.mark.parametrize("fl", FLOORS)
def test_furniture_inside_a_room(fl):
    rooms, _, _, _, furniture = floor(fl)
    rects = [r[2:6] for r in rooms]
    bad = []
    for f in furniture:
        if f[0] in M.OUTDOOR_FURNITURE:
            continue
        centre = ((f[3] + f[4]) / 2, (f[5] + f[6]) / 2)
        if not any(inside(centre, r) for r in rects):
            bad.append(f[0])
    assert not bad, f"furniture outside every room on {fl}: {bad}"
```

- [ ] **Step 5: Write `tests/test_build.py`**

```python
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
```

- [ ] **Step 6: Run against the duplex model to calibrate**

Run:

```bash
cd 99_Source && .venv/bin/python -m pytest -q tests/test_model_invariants.py
```

Expected: `test_furniture_inside_a_room` FAILS. Every other test passes. The failure names the duplex's outdoor items: F31 airer, F123 rinse shower, F124 pocket garden, F125 and F126 rain basins. It may also list verandah items whose rooms do not cover them.

- [ ] **Step 7: Add `OUTDOOR_FURNITURE` to `model.py` and re-run**

Insert directly under the `FURNITURE = [...]` list:

```python
# Furniture placed outside the house on purpose (garden, walkway, forecourt): skipped by the "inside a room" check
OUTDOOR_FURNITURE = {"F31", "F123", "F124", "F125", "F126"}
```

Add any other id the failure listed, but only if the item really is outdoors (check its note).

Then run:

```bash
.venv/bin/python -m pytest -q
```

Expected: all pass, including `test_build.py` (the build takes about 20 s).

- [ ] **Step 8: Commit, only when the owner says so**

```bash
git add 99_Source/requirements.txt 99_Source/planlib.py 99_Source/tests 99_Source/model.py
```

Then use the anonymous commit command with the message `Courtyard: test harness and geometry invariants`.

---

### Task 2: Grid constants, plot and site

**Files:**
- Modify: `99_Source/model.py`. Replace `PROJECT`, `SITE`, `PLOT`, `SHOP_WALL`, `DRIVE`, `plot_north`, `GARDEN_BEDS`, `drive_poly`, `SITE_FEATURES`, `FOOD_TREES` and `TREES`.
- Create: `99_Source/tests/test_courtyard.py`

**Interfaces:**
- **Produces:** grid constants in `model.py`, used by every later task:

  ```python
  HX1, HX2, HY1, HY2 = 18.0, 72.0, 8.0, 62.0   # house outer wall centre lines (54 x 54)
  BAND, WALK, COURT = 16.0, 4.0, 14.0           # room band depth, walkway width, open courtyard side
  CX, CY = (HX1 + HX2) / 2, (HY1 + HY2) / 2     # 45.0, 35.0: house centre = brahmasthan = courtyard centre
  CT = (CX - COURT / 2, CX + COURT / 2, CY - COURT / 2, CY + COURT / 2)        # (38, 52, 28, 42) courtyard
  RING = (CT[0] - WALK, CT[1] + WALK, CT[2] - WALK, CT[3] + WALK)              # (34, 56, 24, 46) walkway outer edge
  ```

- **Produces:** `PLOT = [(0, 0), (160, 0), (160, 70), (0, 70)]` and `plot_north(x) -> 70.0`.

- [ ] **Step 1: Write the failing tests** in `tests/test_courtyard.py`

```python
import model as M


def test_plot_is_70_by_160_road_east():
    xs = [p[0] for p in M.PLOT]; ys = [p[1] for p in M.PLOT]
    assert (min(xs), max(xs), min(ys), max(ys)) == (0, 160, 0, 70)


def test_grid_adds_up():
    assert M.HX2 - M.HX1 == 54 and M.HY2 - M.HY1 == 54
    assert M.BAND + M.WALK + M.COURT + M.WALK + M.BAND == 54
    assert (M.CX, M.CY) == (45.0, 35.0)
    assert M.CT == (38.0, 52.0, 28.0, 42.0) and M.RING == (34.0, 56.0, 24.0, 46.0)


def test_site_features_inside_plot():
    for fid, _, kind, g in M.SITE_FEATURES:
        if kind == "rect":
            assert 0 <= g[0] < g[1] <= 160 and 0 <= g[2] < g[3] <= 70, fid
        elif kind == "circle":
            assert 0 <= g[0] - g[2] and g[0] + g[2] <= 160 and 0 <= g[1] - g[2] and g[1] + g[2] <= 70, fid


def test_services_spacing():
    f = {s[0]: s[3] for s in M.SITE_FEATURES}
    sx, sy = f["SOAK"][0], f["SOAK"][1]
    bx, by = f["BORE"][0], f["BORE"][1]
    assert ((sx - bx) ** 2 + (sy - by) ** 2) ** 0.5 >= 60          # soak pit 60 ft+ from the borewell
    assert f["SOAK"][0] - M.HX2 >= 20                              # soak pit about 23 ft from the house
    assert f["SUMP"][0] > 100 and f["SUMP"][2] > 35                # sump in the north-east quadrant
```

- [ ] **Step 2: Run them to see them fail**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_courtyard.py
```

Expected: FAIL with `AttributeError: module 'model' has no attribute 'HX1'`.

- [ ] **Step 3: Write the constants and the site**

Put the grid block from **Interfaces** right after `PROJECT`.

Set `PROJECT["name"]` to `"Kerala Home, Courtyard Concept"`, and its subtitle to a Tamil courtyard house, 54 × 54 ft, on a 70 × 160 ft plot.

Set `SITE = {"w": 70, "l": 100, "strip": 0, "trial": 0}`. The house sheets then frame x 0–100.

Set `PLOT` as in **Interfaces**, and replace `plot_north` with:

```python
def plot_north(x):
    return 70.0
```

Rewrite `SITE_FEATURES` to the spec section 2 table, keeping each id the 3D and sheet code reads:

| Id | Feature |
|---|---|
| `SPARE` | Back garden, x 0–18 |
| `OTTA` | Engawa, x 14.6–17.2 along the den's west wall |
| `GSTEP` | Steps down from the engawa |
| `PERGOLA` | Pergola over the engawa |
| `TULSI` | Tulsi thara on the door axis, (86, 35) |
| `PATH` | Forecourt, x 80–95, y 20–50 |
| `PATH2` | Path to the car porch |
| `CARPORT` | Car porch, x 96–114, y 56–66 |
| `DRIVE` | Drive along the north boundary to a gate at x 160, y 56–68 |
| `GATE` | Gate at x 160, y 56–68 |
| `SEPTIC` | Septic tank, x 98–104, y 44–50, behind `HEDGE1` |
| `SOAK` | Soak pit, circle (95, 6, 1.6) |
| `HERBS` | Herb beds, x 80–94, y 1–18 |
| `SPIRAL` | Herb spiral |
| `BANANA` | Banana circle |
| `GUILD` | Fruit guilds |
| `VEG` | Vegetable beds |
| `COMPOST` | Compost pits |
| `WORM` | Worm bin |
| `FENCE` | Living fence |
| `WORKSHOP` | Workshop, x 118–134, y 2–14 |
| `WVERANDAH` | Workshop verandah |
| `SHOPS` | Rental shops |
| `SHOP1` | Shop 1, x 146–160, y 2–14 |
| `SHOP2` | Shop 2, x 146–160, y 14–26 |
| `SITEWC` | Site toilet |
| `SUMP` | Sump, x 140–145, y 46–51 |
| `BORE` | Borewell, circle (150, 44, 0.5) |
| `RECHARGE` | Recharge pit |
| `STEPS` | Steps, x 79–81, y 33–37 |
| `FEET` | Foot-wash tap |
| `WSTEP` | Kitchen service door step, on the kitchen's south door |
| `APRON` | Apron, (HX1 - 3, HX2 + 3, HY1 - 3, HY2 + 3) |
| `PARIJAT` | Parijat |
| `JASMINE` | Jasmine |

Move `TREES`, `FOOD_TREES` and `GARDEN_BEDS` into their new zones, at least 25 ft from the house and 9 ft from the septic tank. `DRIVE` becomes `{"x1": 114.0, "x2": 160.0, "off": (56.0, 66.0)}`. `drive_poly()` returns the rectangle x 114–160, y 56–66.

- [ ] **Step 4: Run the tests until they pass**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_courtyard.py
```

Expected: 4 passed. The build is expected to break until Task 3; do not run `test_build.py` yet.

- [ ] **Step 5: Commit, only when the owner says so**

Use the message `Courtyard: grid, plot and site`.

---

### Task 3: Ground floor rooms, walls and courtyard

**Files:**
- Modify: `99_Source/model.py`. Replace `ROOMS`, `WALLS`, `EXTERIOR`, `EXTRA_EXT_WALLS`, `WET_WALLS`, `LEVELS`, `FLOOR_FINISH`, `ROOM_LABEL_AT`, `ROOM_FLOOR`, `CEILINGS`, `PILLARS` and `JALI_SCREENS`.
- Modify: `99_Source/tests/test_courtyard.py`

**Interfaces:**
- **Consumes:** the grid constants from Task 2.
- **Produces:** these room ids, which later tasks rely on.

  | Id | Room | Id | Room |
  |---|---|---|---|
  | R01 | master bedroom | R40 | master bath |
  | R53 | master dressing | R47 | master walk-in |
  | R06 | stair | R09 | stair hall |
  | R08 | powder room | R46 | store |
  | R42 | den | R07 | den bath |
  | R58 | den alcove | R16 | family living |
  | R52 | oonjal hall | R11 | pooja |
  | R57 | oonjal alcove | R54 | entry hall |
  | R18 | genkan | R17 | thinnai |
  | R10 | dining | R15 | kitchen |
  | R13 | utility | R60 | pantry |
  | R50 | courtyard | R51, R61, R62, R63 | walkway (south, north, west, east) |

- **Produces:** `COURTYARD = CT` and `WALKWAY_PILLARS: list[tuple[float, float]]`.
- **Produces:** `LEVELS["courtyard"] = LEVELS["FFL"] - 0.5`, `LEVELS["walkway"] = LEVELS["FFL"] - 0.08`, `LEVELS["thinnai"] = LEVELS["FFL"] - 0.5`.

**Block allocation (fixed by the spec; sub-division inside a block is this task's design work):**

| Block | Extent | Holds |
|---|---|---|
| South-west | x 18–38, y 8–24 (takes 4 ft of the south band) | R01 master bedroom (bed head south), R40 bath (basin opposite its door, door opens outward), R53 dressing |
| West | x 18–34, y 24–46 | R06 stair, R09 stair hall (open to the west walkway), R08 powder room, R46 store, R47 master walk-in |
| North-west | x 18–34, y 46–62 | R42 den, R07 den bath on the west wall, R58 den alcove |
| North | x 34–56, y 46–62 | R16 family living, opening to the north walkway |
| North-east | x 56–72, y 46–62 | R52 oonjal hall, R11 pooja 6 × 6 in the very corner (x 66–72, y 56–62), R57 alcove |
| East | x 56–72, y 24–46 | R54 entry hall (x 56–66), R18 genkan (x 66–72) with the main door on y 33–37 |
| South | x 38–56, y 8–24 | R10 dining, with the wash basin and crockery on the south wall |
| South-east | x 56–72, y 8–24 | R15 kitchen (x 56–72, y 13–24), R13 utility (x 56–66, y 8–13), R60 pantry (x 66–72, y 8–13) |
| Centre | | R50 courtyard = `CT`; walkway rects R51 (x 34–56, y 24–28), R61 (x 34–56, y 42–46), R62 (x 34–38, y 28–42), R63 (x 52–56, y 28–42) |
| Thinnai | x 72–79, y 24–46 | R17 thinnai (one room rect; the door gap y 33–37 is open floor) |

**Rules the sub-division must meet** (all are tested in Step 1 or Task 4):

1. **Stair position:** the stair sits in the west block, rising clockwise. Its upper arrival faces south, so upstairs the stair head opens straight onto the Bedroom 2 suite and the stair well never cuts the suite off. Example that satisfies this:
   - R06 at x 26.5–34, y 36.67–46.
   - Flight 1 rises north on the west half from the stair hall.
   - A half landing at the north end.
   - Flight 2 rises south on the east half and arrives at y 36.67.
2. **Corner rooms:**
   - South-west: entered from the stair hall.
   - North-west: entered from the stair hall.
   - North-east: open to the entry hall and the family living.
   - South-east: entered from the dining.
   - Every room is reachable from the genkan (tested in Task 4).
3. **Minimum clear sizes:**

   | Space | Minimum |
   |---|---|
   | Master bedroom | 12 × 13 |
   | Den | 12 × 9.5 |
   | Family living | 20 × 14 |
   | Dining | 16 × 10 |
   | Kitchen | 12 × 9 |
   | Each bath | 6 × 6.3 |
   | Powder room | 4.5 × 6 |
   | Stair hall | 7 ft wide |

4. **Walls:**
   - Every wall the rooms share is a `WALLS` entry, except the open edges below.
   - **Open to the walkway (no wall):** the stair hall's east edge, the family living's south edge (teak-and-glass folding doors in Task 4), the entry hall's west edge and the dining's north edge (folding doors).
   - **No wall:** the oonjal hall to the entry hall, and the courtyard edge. Pillars stand there instead.
5. **Wall types:**
   - **Exterior** (9 in): the outer walls at `HX1`, `HX2`, `HY1`, `HY2`, plus every wall on the `RING` lines.
   - **Wet** (7 in): walls that carry plumbing.
6. **Pillars:** `WALKWAY_PILLARS` is the 8 points (38, 28), (45, 28), (52, 28), (38, 35), (52, 35), (38, 42), (45, 42), (52, 42). There are also 4 thinnai pillars at x 78.5, y 25, 32.5, 37.5, 45. `PILLARS` = walkway pillars + thinnai pillars.

- [ ] **Step 1: Write the failing tests** (append to `tests/test_courtyard.py`)

```python
from planlib import inside, overlap

ROOM = lambda rid: next(r for r in M._FLOOR_DATA["G"]["ROOMS"] if r[0] == rid)
CLEAR = lambda rid: (ROOM(rid)[3] - ROOM(rid)[2] - 0.6, ROOM(rid)[5] - ROOM(rid)[4] - 0.6)


def test_courtyard_on_the_brahmasthan():
    r = ROOM("R50")
    assert (r[2], r[3], r[4], r[5]) == M.CT
    assert ((r[2] + r[3]) / 2, (r[4] + r[5]) / 2) == (M.CX, M.CY)


def test_vastu_zones():
    q = lambda rid: ("N" if (ROOM(rid)[4] + ROOM(rid)[5]) / 2 > M.CY else "S") + ("E" if (ROOM(rid)[2] + ROOM(rid)[3]) / 2 > M.CX else "W")
    assert q("R11") == "NE" and q("R15") == "SE" and q("R01") == "SW" and q("R42") == "NW"
    assert (ROOM("R06")[2] + ROOM("R06")[3]) / 2 < M.CX            # stair in the west half
    for rid in ("R07", "R08", "R40"):                               # no toilet in the north-east
        assert q(rid) != "NE", rid


def test_minimum_clear_sizes():
    need = {"R01": (12, 13), "R42": (12, 9.5), "R16": (20, 14), "R10": (16, 10), "R15": (12, 9),
            "R40": (6, 6.3), "R07": (6, 6.3), "R08": (4.5, 6)}
    for rid, (a, b) in need.items():
        w, d = sorted(CLEAR(rid), reverse=True)
        assert w >= max(a, b) - 0.01 and d >= min(a, b) - 0.01, (rid, CLEAR(rid))


def test_pooja_in_the_ne_corner():
    r = ROOM("R11")
    assert r[3] == M.HX2 and r[5] == M.HY2 and r[3] - r[2] >= 6 and r[5] - r[4] >= 6


def test_pillars_ring_the_courtyard():
    assert len(M.WALKWAY_PILLARS) == 8
    assert all(p[0] in (M.CT[0], M.CX, M.CT[1]) and p[1] in (M.CT[2], M.CY, M.CT[3]) for p in M.WALKWAY_PILLARS)
```

- [ ] **Step 2: Run to see them fail**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_courtyard.py -k "brahmasthan or vastu or clear or pooja or pillars"
```

Expected: FAIL with `StopIteration` (rooms R50 and R11 not found).

- [ ] **Step 3: Write the rooms, walls, levels, finishes, ceilings and pillars**

Write them to the block table and the rules above.

**Finishes** (`FLOOR_FINISH`):

| Finish | Rooms |
|---|---|
| Athangudi tiles | R54, R16, R10, R52, R57 |
| Red oxide | R01, R42, R47, R53, R58 |
| Anti-skid ceramic | R40, R07, R08, R13 |
| Rough-dressed granite | R50, R51, R61, R62, R63, R17, R18 |
| Matt vitrified | R15, R60, R46 |

`FLOOR_FINISH` keys are matched by `make_3d.floor_keys`. Add `("Athangudi", "athangudi")` there, and an `athangudi` floor texture in Task 11.

**Ceilings:**
- Flat 9.5 ft for the ring rooms under a false ceiling.
- R16: `("flat", 9.5)` under the terrace slab.
- The walkway rects: `("sloped", "lean-to, tiled")`.
- The courtyard: `("open", "sky")`. Every consumer of `CEILINGS` must skip `"open"` (grep `CEILINGS[` and add the skip).

- [ ] **Step 4: Run the tests until they pass**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_courtyard.py tests/test_model_invariants.py::test_rooms_do_not_overlap
```

Expected: all pass.

- [ ] **Step 5: Owner checkpoint**

1. Build: `.venv/bin/python build.py`. If later-task data (doors, furniture) still names duplex rooms, temporarily empty `DOORS`, `WINDOWS`, `FURNITURE`, `ELECTRICAL`, `PLUMBING` and `PIPES` on the ground floor.
2. Render the ground floor plan, page 4 of the PDF, to a PNG in the scratchpad.
3. Send it to the owner with `SendUserFile`, with a short note of where each room landed.
4. Ask the owner the spec's open questions at the same time:
   - House size: keep 54 × 54 ft, or tighten to about 50 × 50 ft? If they choose 50 × 50, set `BAND = 14.0` and update the Task 2 test numbers.
   - Courtyard plant (F128).
   - Thinnai finish.
   - A second swing on the terrace (F103).
5. Do not continue until the owner approves the room layout. Fold any change into the spec's section 3 table.

- [ ] **Step 6: Commit, only when the owner says so**

Use the message `Courtyard: ground floor rooms round the courtyard`.

---

### Task 4: Ground floor doors, windows and transoms

**Files:**
- Modify: `99_Source/model.py`. Replace `DOORS`, `TRANSOMS`, `HINGE_AT_END`, `WINDOWS`, `OTHER_OPENINGS` and `PLANTER_GRILLES`.
- Modify: `99_Source/tests/test_courtyard.py`

**Interfaces:**
- **Consumes:** the room ids from Task 3.
- **Produces:** door ids, carried over by role:

  | Id | Door |
  |---|---|
  | D01 | Main door: east wall `HX2`, y 33–37, double teak leaves, carved and brass-studded |
  | D04 | Master bedroom, 3 ft |
  | D42 | Master bath, 2'-9", opens outward |
  | D02 | Den |
  | D07 | Den bath |
  | D45 | Den garden door to the engawa |
  | D08 | Powder room |
  | D11 | Pooja, carved teak, opens inward |
  | D12 | Kitchen to utility |
  | D17 | Kitchen to dining |
  | D18 | Utility service door, south wall |

- **Produces:** door ids D60–D63, the teak-and-glass folding doors from the family living, dining, entry hall and stair hall onto the walkway. They are sliding (swing 0) and their note includes "folding".

**Rules:**
- **Bathroom doors:** each bath's door sits on a wall whose opposite wall can hold the basin (checked in Task 5).
- **Windows:**
  - Every room on an outer wall gets at least one window.
  - The south and west outer windows are small, with deep sills or jali (heat).
  - Rooms on the courtyard side borrow light through the folding doors.
  - The dining's south window looks onto the pocket garden.
  - The master bedroom has two windows either side of the bed head on the south wall.
  - The pooja has a high vent.
  - The genkan has two jali windows onto the thinnai.

- [ ] **Step 1: Write the failing test**

```python
from planlib import graph, reachable


def test_every_ground_room_reachable_from_the_genkan():
    with M.on_floor("G"):
        rooms = [(r[0], r[2], r[3], r[4], r[5]) for r in M.ROOMS]
        g = graph(rooms, M.WALLS, M.DOORS)
    lost = {r[0] for r in rooms} - reachable(g, "R18")
    assert not lost, f"rooms with no way in: {sorted(lost)}"


def test_main_door_on_the_east_axis():
    d = next(d for d in M._FLOOR_DATA["G"]["DOORS"] if d[0] == "D01")
    assert d[1] == "Y" and d[2] == M.HX2 and (d[3] + d[4]) / 2 == M.CY and abs(d[4] - d[3]) >= 4
```

- [ ] **Step 2: Run to see them fail**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_courtyard.py -k "reachable or axis"
```

Expected: FAIL. Either D01 is not found, or rooms with no way in are listed.

- [ ] **Step 3: Write `DOORS`, `TRANSOMS`, `WINDOWS` and the rest to the rules**

Keep each carried-over door's material text from the duplex `DOORS` (same id). Add the folding doors.

- [ ] **Step 4: Run the whole suite**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_courtyard.py tests/test_model_invariants.py -k "not furniture"
```

Expected: all pass.

- [ ] **Step 5: Commit, only when the owner says so**

Use the message `Courtyard: ground floor doors and windows`.

---

### Task 5: Ground floor furniture and fittings (the carry-overs)

**Files:**
- Modify: `99_Source/model.py`. Replace `FURNITURE`, `EXTRA_DRAW` and `OUTDOOR_FURNITURE`.
- Modify: `04_3D/KH-P1_3D_Model.html`: the `KIND` entries for any new id.
- Modify: `99_Source/tests/test_courtyard.py`

**Interfaces:**
- **Consumes:** the rooms and doors from Tasks 3–4.
- **Produces:** furniture ids. Duplex ids are kept wherever the item carries over, so the 3D `KIND` map and the schedule notes keep working:

  | Ids | Items |
  |---|---|
  | F10, F11 | Master bed, bedside shelves |
  | F06 | Master wardrobe (in R47) |
  | F12, F13, F14 | Master bath: WC, shower glass, basin |
  | F20, F23, F66, F67, F117 | Den |
  | F48, F49, F50 | Den bath |
  | F16, F17 | Powder room |
  | F24, F27, F116, F28 | Dining: table, stools, bench |
  | F21, F44 | Wash basin, crockery |
  | F33 | Serving ledge |
  | F34, F35, F36, F37, F115, F65, F68 | Kitchen |
  | F29, F62, F61, F113 | Utility |
  | F38, F39, F45, F46, F114 | Family living |
  | F53 | Media wall on the living's west wall |
  | F26 | Pooja mandapam (idols face west) |
  | F41 | Oonjal, now in R52 |
  | F52 | Shoe bench, genkan |
  | F120 | Uruli tokonoma, entry hall, facing the courtyard |
  | F121 | Kolam stone at D01 |
  | F122 | Nilavilakku pedestal |
  | F42, F69 | Thinnai platforms, now built-in thinnai seats along R17 |
  | F125, F126 | Rain-chain basins at the thinnai's front corners |
  | F123 | Rinse shower on the kitchen's east wall |
  | F124 | Pocket garden outside the dining's south window |
  | F31 | Airer in the back garden |
  | F112 | LPG cage |

- **Produces:** `F128`, the courtyard planter: a raised round bed 4 ft across at (`CX`, `CY`) for the tulsi or frangipani. In 3D it is kind `"planter"` (a new builder in Task 11).

- [ ] **Step 1: Write the failing tests**

```python
from planlib import overlap

BATHS = {"R40": ("D42", "F14", "F12"), "R07": ("D07", "F49", "F48"), "R08": ("D08", "F17", "F16")}


def _door(did):
    return next(d for fl in ("G", "F1") for d in M._FLOOR_DATA[fl]["DOORS"] if d[0] == did)


def _furn(fid):
    return next(f for fl in ("G", "F1") for f in M._FLOOR_DATA[fl]["FURNITURE"] if f[0] == fid)


def _room(rid):
    return next(r for fl in ("G", "F1") for r in M._FLOOR_DATA[fl]["ROOMS"] if r[0] == rid)


def test_basin_opposite_the_door_and_wc_out_of_line():
    for rid, (did, basin, wc) in BATHS.items():
        r, d, b, w = _room(rid), _door(did), _furn(basin), _furn(wc)
        if d[1] == "Y":
            far = r[3] if abs(d[2] - r[2]) < 0.01 else r[2]
            assert abs((b[3] if far < d[2] else b[4]) - far) <= 1.0, (rid, "basin not on the wall opposite the door")
            lo, hi = min(d[3], d[4]), max(d[3], d[4])
            assert not (lo < (w[5] + w[6]) / 2 < hi and abs((w[3] + w[4]) / 2 - far) < 2.5), (rid, "WC in line with the door")
        else:
            far = r[5] if abs(d[2] - r[4]) < 0.01 else r[4]
            assert abs((b[5] if far < d[2] else b[6]) - far) <= 1.0, (rid, "basin not on the wall opposite the door")
            lo, hi = min(d[3], d[4]), max(d[3], d[4])
            assert not (lo < (w[3] + w[4]) / 2 < hi and abs((w[5] + w[6]) / 2 - far) < 2.5), (rid, "WC in line with the door")


def test_carry_overs_present():
    ids = {f[0] for fl in ("G", "F1") for f in M._FLOOR_DATA[fl]["FURNITURE"]}
    need = {"F10", "F06", "F14", "F17", "F49", "F24", "F27", "F116", "F28", "F34", "F35", "F38", "F114", "F26", "F41", "F52",
            "F120", "F121", "F122", "F123", "F124", "F125", "F126", "F128"}
    assert not need - ids, sorted(need - ids)


def test_no_furniture_collides():
    for fl in ("G", "F1"):
        fs = [f for f in M._FLOOR_DATA[fl]["FURNITURE"] if f[9] not in ("glass",) and f[0] not in M.OUTDOOR_FURNITURE]
        bad = [(a[0], b[0]) for i, a in enumerate(fs) for b in fs[i + 1:] if overlap(a[3:7], b[3:7]) > 0.1]
        assert not bad, (fl, bad)
```

- [ ] **Step 2: Run to see them fail**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_courtyard.py -k "basin or carry or collides"
```

Expected: FAIL (`StopIteration`, or the missing ids are listed).

- [ ] **Step 3: Write the furniture**

Keep each carried item's duplex note text. Edit only the location words, for example "on the poomukham" becomes "on the thinnai".

Give F41 (oonjal) 3 ft of swing clearance front and back. Keep it 2 ft clear of the walkway pillars.

- [ ] **Step 4: Run the whole suite, including the build**

Run:

```bash
.venv/bin/python -m pytest -q
```

Expected: all pass, except `test_build.py`, if the roof or 3D code still assumes the duplex. That is fixed in Tasks 9–11. If the build fails, note the traceback in the task report and carry on.

- [ ] **Step 5: Commit, only when the owner says so**

Use the message `Courtyard: ground floor furniture and fittings`.

---

### Task 6: Upper wing, stair, roof terrace and jharokhas

**Files:**
- Modify: `99_Source/model.py`. Replace `ROOMS_F1`, `WALLS_F1`, `EXTERIOR_F1`, `EXTRA_EXT_WALLS_F1`, `WET_WALLS_F1`, `RAILS_F1`, `JALI_RAILS`, `TERRACE_POSTS`, `STAIR`, `SLAB_F1`, `DOORS_F1`, `WINDOWS_F1`, `FURNITURE_F1`, `EXTRA_DRAW_F1` and `PLANTER_GRILLES`.
- Add `JHAROKHAS = [(x1, x2, y1, y2, sill_above_floor), ...]`.
- Modify: `99_Source/tests/test_courtyard.py`

**Interfaces:**
- **Consumes:** the grid constants, and the stair geometry from Task 3 (R06 rect and flight direction).
- **Produces:** these room ids on the upper floor:

  | Id | Room |
  |---|---|
  | R31 | Bedroom 2 |
  | R45 | Walk-in |
  | R33 | Bedroom 2 bath |
  | R41 | Stair head |
  | R39 | Upper toilet, stacked over R08 |
  | R46U | Upper store |
  | R44 | Reading room |
  | R36 | Theatre and work room |
  | R37 | Roof terrace, x 34–56, y 46–62 |

- **Produces:** `STAIR` with the same keys the duplex used: `"flight1"`, `"flight2"`, `"landing"`, `"risers"`, `"dir"`. `sheets_elev._stair_z`, `make_3d` and the 3D `stairZ()` read these.
- **Produces:** `JHAROKHAS`, two bays 4 ft wide and 2 ft deep, projecting east from the wing's east wall (x 34 to 36) at the stair head and the reading room, with the seat 1'-6" above the floor.

**Rules:**
- **Wing extent:** every upper room except R37 lies within x 18–34. R37 sits over R16.
- **Stair well:** no upper room overlaps the stair flights except R41 at the arrival.
- **Hotel suite:** R31 → R45 → R33 by doors, and R33's WC on the west outer wall.
- **Upper toilet:** R39 lies within R08's rect (the plumbing stack).
- **Railings:** RAIL_H stays 4.0. `RAILS_F1` covers R37's open edges and the stair well edge. `JALI_RAILS` covers R37's north edge.
- **Terrace furniture:** daybed F127 facing east, swing F103, planter F89 with jasmine, washer F30, sink F32, drying rails F88.
- **Wing furniture:** bookshelf F107 and the jharokha seats F101 and F129 in R44; theatre F55, F91, F92; Bedroom 2 F71, F72, F75, F95, F108, F77, F78, F79; upper toilet F98, F99, F70.

- [ ] **Step 1: Write the failing tests**

```python
def test_upper_mass_stays_west():
    for r in M._FLOOR_DATA["F1"]["ROOMS"]:
        if r[0] != "R37":
            assert r[3] <= M.RING[0] + 0.01, r[0]


def test_stair_well_is_clear_upstairs():
    s = M.STAIR
    well = [s["flight1"][:4], s["flight2"][:4]]
    for r in M._FLOOR_DATA["F1"]["ROOMS"]:
        if r[0] in ("R41",):
            continue
        assert all(overlap(r[2:6], w) < 0.05 for w in well), r[0]


def test_hotel_suite_and_stack():
    rooms = [(r[0], r[2], r[3], r[4], r[5]) for r in M._FLOOR_DATA["F1"]["ROOMS"]]
    g = graph(rooms, M._FLOOR_DATA["F1"]["WALLS"], M._FLOOR_DATA["F1"]["DOORS"])
    assert "R45" in g["R31"] and "R33" in g["R45"] and "R33" not in g["R31"]
    up, down = _room("R39"), _room("R08")
    assert down[2] - 0.01 <= up[2] and up[3] <= down[3] + 0.01 and down[4] - 0.01 <= up[4] and up[5] <= down[5] + 0.01


def test_upper_rooms_reachable_from_the_stair_head():
    rooms = [(r[0], r[2], r[3], r[4], r[5]) for r in M._FLOOR_DATA["F1"]["ROOMS"]]
    g = graph(rooms, M._FLOOR_DATA["F1"]["WALLS"], M._FLOOR_DATA["F1"]["DOORS"])
    assert not {r[0] for r in rooms} - reachable(g, "R41")


def test_two_jharokhas_over_the_walkway():
    assert len(M.JHAROKHAS) == 2
    for x1, x2, y1, y2, sill in M.JHAROKHAS:
        assert x1 == M.RING[0] and x2 - x1 == 2 and y2 - y1 == 4 and sill == 1.5
```

Also add `"R33": ("D33", "F78", "F77")` and `"R39": ("D39", "F99", "F98")` to `BATHS`.

- [ ] **Step 2: Run to see them fail**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_courtyard.py -k "upper or stair_well or hotel or jharokha"
```

Expected: FAIL.

- [ ] **Step 3: Write the upper floor to the rules**

- **`SLAB_F1`:** covers the wing (x 18–34, y 8–62) and R37, minus the stair well.
- **`TERRACE_POSTS`:** the 4 corners of R37 plus its mid-points on the north and east edges.
- **`LEVELS["upper_ffl"]`:** stays 10.0, the floor-to-floor height of 16 risers at 7.5 in.

- [ ] **Step 4: Run the whole suite**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_courtyard.py tests/test_model_invariants.py
```

Expected: all pass.

- [ ] **Step 5: Owner checkpoint**

Render the first-floor plan (page 5) and send it to the owner. Continue only after the owner approves it.

- [ ] **Step 6: Commit, only when the owner says so**

Use the message `Courtyard: upper west wing, stair and roof terrace`.

---

### Task 7: Electrical, plumbing and pipes

**Files:**
- Modify: `99_Source/model.py`. Replace `ELECTRICAL`, `ELECTRICAL_F1`, `PLUMBING`, `PLUMBING_F1` and `PIPES`.
- Modify: `99_Source/tests/test_courtyard.py`

**Interfaces:**
- **Consumes:** every room and fitting from Tasks 3–6.
- **Produces:** points with the same codes and `ELEC_TYPES`/`PLUMB_TYPES` as the duplex, including LS, SA and HA.
- **Produces:** a new plumbing code `"CD"` for the courtyard drain, added to `PLUMB_TYPES` as `"Courtyard drain with first-flush filter to the sump"`.

**Rules:**

| Item | Where |
|---|---|
| Light (L) or wall light (WL) | Every room |
| Fan (F) | Every habitable room |
| AC + ODU | R01, R42, R31, R16, R44, R36. ODUs on the west and south outer walls in shade. |
| Smoke alarm (SA) | R09 and R41 |
| Heat alarm (HA) | R15 |
| LS (switched lamp socket) | R16, R52, R01, R42, R31, R44 |
| Low step lights (WL) | Stair |
| Switches outside each bathroom | Geyser (G) out of the shower spray |
| Garden lights (GL) | Courtyard uplight, engawa, pocket garden, thinnai |

| Pipes | Route |
|---|---|
| Soil | Every WC to the septic tank, via inspection chambers. Upper WCs drop down the outer wall (R33) or inside the stacked wet wall (R39 over R08). |
| Grey | Baths to the soak pit. Kitchen through a grease trap to the banana circle. |
| Rain | The courtyard drain (CD at `CX + 6, CY - 6`) and every downpipe to the sump. |
| Supply | From the sump by pump to the overhead tank over R41. |

- [ ] **Step 1: Write the failing test**

```python
def test_every_room_has_light_and_baths_have_switches_outside():
    for fl in ("G", "F1"):
        lit = {e[3] for e in M._FLOOR_DATA[fl]["ELECTRICAL"] if e[0] in ("L", "WL")}
        rooms = {r[0] for r in M._FLOOR_DATA[fl]["ROOMS"]} - {"R50"}
        assert not rooms - lit, (fl, sorted(rooms - lit))
    assert any(p[0] == "CD" for p in M.PLUMBING)
```

- [ ] **Step 2: Run to see it fail.** Expected: FAIL, with the unlit rooms listed.

- [ ] **Step 3: Write the points and pipes to the rules.**

- [ ] **Step 4: Run the whole suite.** Expected: all pass, except the build, until Task 9.

- [ ] **Step 5: Commit, only when the owner says so**

Use the message `Courtyard: electrical and plumbing`.

---

### Task 8: Words: finishes, specification, decisions, phasing

**Files:**
- Modify: `99_Source/model.py`. Replace `FINISHES`, `OPEN_ISSUES`, `SPEC`, `PHASES`, `PHASE1_PROVISIONS`, `PHASE1_LIVING`, `PHASE2_ROOMS` and `HOLD_POINTS`.
- Add `COURTYARD_DECISIONS`. Set `DECISIONS = COURTYARD_DECISIONS + DUPLEX_DECISIONS_CARRIED`.
- Modify: `99_Source/guide.py` and `99_Source/make_xlsx.py`, wherever they name a duplex room (grep the duplex ids R33, R36, R37, R44, R46, R47 and the words "poomukham", "theatre", "terrace").

**Interfaces:**
- **Produces:** `COURTYARD_DECISIONS: list[str]`, one entry per spec section 1 decision plus the thinnai, oonjal hall, jharokhas and roof terrace.
- **Produces:** `DUPLEX_DECISIONS_CARRIED`: the duplex decisions that still hold, each prefixed "Carried over from the duplex: ".

**Rules:**
- **`FINISHES` rows:** courtyard, walkway, thinnai, Athangudi floors, oonjal hall, pooja, baths, stair, roof terrace. Take the wording from spec section 6.
- **`OPEN_ISSUES`:** the spec's section 12 questions, plus the vastu items.
- **`PHASES`:**
  - Stage 1: the ground floor ring, the courtyard and the full roof.
  - Stage 2: the upstairs shell and the roof terrace.
  - Stage 3: the upstairs fit-out.

  Re-price roughly from the area table in spec section 11.

- **`PHASE1_PROVISIONS`:** the wing's columns and beams, sleeves for R33 and R39, the sunk slab under R33, and the terrace slab waterproofed in stage 1.

- [ ] **Step 1: Write the failing test**

```python
def test_words_mention_the_courtyard_and_no_duplex_rooms():
    import guide, make_xlsx  # noqa: F401  (import must not fail)
    text = " ".join(map(str, M.FINISHES)) + " ".join(M.DECISIONS[:5])
    assert "courtyard" in text.lower() and "thinnai" in text.lower()
    assert "poomukham" not in " ".join(map(str, M.FINISHES)).lower()
```

- [ ] **Step 2: Run to see it fail.** Expected: FAIL.
- [ ] **Step 3: Write the text.**
- [ ] **Step 4: Run the whole suite.** Expected: all pass, except the build, until Task 9.
- [ ] **Step 5: Commit, only when the owner says so**

Use the message `Courtyard: finishes, specification and decisions`.

---

### Task 9: Ring roof geometry and the roof plan

**Files:**
- Modify: `99_Source/model.py`. Replace `ROOF` with the new schema below.
- Modify: `99_Source/geom.py`:
  - **Delete:** `gable_eave_z`, `gablet_d`, `hip_z`, `chaipu_z`, `gable_z`, `wing_eave_z`, `wing_z`, `wing_ridge_z`, `gable_ridge_z`.
  - **Add:** `ring_z`, `wing_roof_z`.
  - **Rewrite:** `roof_z`, `ridge_z`, `roof_area`.
- Modify: `99_Source/sheets_arch.py`: rewrite `sheet_roof`.
- Create: `99_Source/tests/test_roof.py`

**Interfaces:**
- **Produces:** the new `ROOF` schema:

  ```python
  ROOF = {
      "pitch": 25,                                  # degrees: tiles need 22+; lower keeps the outer walls modest
      "overhang": 2.0,                              # beyond the outer wall centre lines
      "ring": (HX1 - 2.0, HX2 + 2.0, HY1 - 2.0, HY2 + 2.0),   # outer eave outline of the single-storey ring
      "court_eave": (CT[0] + 0.5, CT[1] - 0.5, CT[2] + 0.5, CT[3] - 0.5),  # inner eave: 6 in past the walkway edge, over the court
      "wing": (HX1 - 2.0, RING[0] + 0.0, HY1 - 2.0, HY2 + 2.0),           # hipped roof over the upper west wing
      "terrace": (RING[0], RING[1], RING[3], HY2),  # flat slab over the family living (no tiles), with its canopy
      "canopy": 9.0,                                # terrace canopy height above the terrace floor
      "grille_z": None,                             # set in geom: the court grille sits at the inner eave height
      "downpipes": [(HX1 - 2.0, HY1 - 2.0), (HX2 + 2.0, HY1 - 2.0), (HX1 - 2.0, HY2 + 2.0), (HX2 + 2.0, HY2 + 2.0), (CX, HY1 - 2.0), (CX, HY2 + 2.0)],
  }
  ```

- **Produces** in `geom.py`:
  - `ring_z(x, y) -> float | None`: the ring roof height at (x, y), or None outside the ring or over the open court.
  - `wing_roof_z(x, y) -> float | None`.
  - `roof_z(x, y) -> float | None`: the higher of the two.
  - `eave_z() -> float`: the ring's outer and inner eave height.
  - `ridge_z() -> float`: the ring ridge.
  - `wing_eave_z() -> float`.
  - `roof_area() -> float`: sloped area, for the quantities.

- [ ] **Step 1: Write the failing tests** in `tests/test_roof.py`

```python
import geom as G
import model as M


def test_ring_roof_rises_from_both_eaves_to_a_ridge():
    e = G.eave_z()
    x_mid_band_s = M.CX
    y_outer, y_inner = M.ROOF["ring"][2], M.ROOF["court_eave"][2]
    assert abs(G.ring_z(x_mid_band_s, y_outer + 0.001) - e) < 0.01
    assert abs(G.ring_z(x_mid_band_s, y_inner - 0.001) - e) < 0.01
    ridge_y = (y_outer + y_inner) / 2
    assert abs(G.ring_z(x_mid_band_s, ridge_y) - G.ridge_z()) < 0.01 and G.ridge_z() > e


def test_court_is_open_and_terrace_flat():
    assert G.ring_z(M.CX, M.CY) is None
    tx = (M.ROOF["terrace"][0] + M.ROOF["terrace"][1]) / 2
    ty = (M.ROOF["terrace"][2] + M.ROOF["terrace"][3]) / 2
    assert G.ring_z(tx, ty) is None


def test_wing_roof_is_above_the_ring():
    y = M.CY
    assert G.wing_roof_z(26.0, y) > G.ridge_z()
```

- [ ] **Step 2: Run to see them fail**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_roof.py
```

Expected: FAIL with `AttributeError: module 'geom' has no attribute 'ring_z'`.

- [ ] **Step 3: Implement in `geom.py`**

```python
def eave_z():
    """Ring roof eave (outer and inner): the ground-floor wall top less the overhang's fall."""
    return LEVELS["FFL"] + LEVELS["wall_top"] - ROOF["overhang"] * TAN


def _in(r, x, y):
    return r[0] <= x <= r[1] and r[2] <= y <= r[3]


def ring_z(x, y):
    o, i, t = ROOF["ring"], ROOF["court_eave"], ROOF["terrace"]
    if not _in(o, x, y) or (i[0] < x < i[1] and i[2] < y < i[3]) or (t[0] < x < t[1] and t[2] < y < t[3]):
        return None
    d_out = min(x - o[0], o[1] - x, y - o[2], o[3] - y)
    d_in = max(i[0] - x, x - i[1], i[2] - y, y - i[3])
    return eave_z() + TAN * min(d_out, d_in)


def ridge_z():
    o, i = ROOF["ring"], ROOF["court_eave"]
    return eave_z() + TAN * min(i[0] - o[0], o[3] - i[3], i[2] - o[2], o[1] - i[1]) / 2


def wing_eave_z():
    return upper_wall_top_z() - ROOF["overhang"] * TAN


def wing_roof_z(x, y):
    w = ROOF["wing"]
    if not _in(w, x, y):
        return None
    return wing_eave_z() + TAN * min(x - w[0], w[1] - x, y - w[2], w[3] - y)


def roof_z(x, y):
    zs = [z for z in (ring_z(x, y), wing_roof_z(x, y)) if z is not None]
    return max(zs) if zs else None


def roof_area():
    """Sloped area of the ring and the wing, by sampling a 0.5 ft grid (good to about 1%)."""
    step, total = 0.5, 0.0
    o = ROOF["ring"]
    y = o[2] + step / 2
    while y < o[3]:
        x = o[0] + step / 2
        while x < o[1]:
            if roof_z(x, y) is not None:
                total += step * step
            x += step
        y += step
    return total / math.cos(math.radians(ROOF["pitch"]))
```

Keep `upper_wall_top_z` as it is. Delete the duplex-only functions listed under **Files**. Grep the repo for each deleted name and fix every caller to use `roof_z`, `eave_z`, `ridge_z` or `wing_eave_z`.

- [ ] **Step 4: Rewrite `sheet_roof` in `sheets_arch.py`**

Draw the following:

- **Outlines:** the ring outline `ROOF["ring"]` and the court eave `ROOF["court_eave"]` as rects.
- **Ring lines:**
  - The ridge as the rect halfway between the two outlines.
  - Hip lines from each outer corner to the ridge corner.
  - Valley lines from each inner corner to the ridge corner.
- **Wing:** the wing hip, drawn the way the duplex drew its main hip (ridge plus four hips).
- **Terrace:** the terrace slab as a hatched rect labelled "ROOF TERRACE (FLAT SLAB, TILED CANOPY)".
- **Courtyard:** the court as a blue-tinted rect labelled "MUTRAM, OPEN TO THE SKY: STEEL GRILLE AT EAVE LEVEL".
- **Slopes:** slope arrows on every face, pointing downhill.
- **Downpipes:** circles at `ROOF["downpipes"]`, plus the courtyard drain.
- **Levels:** the ridge and eave levels labelled with `fmt_lvl(ridge_z())`, `fmt_lvl(eave_z())` and `fmt_lvl(wing_eave_z())`.

- [ ] **Step 5: Run the roof tests.** Expected: 3 passed.

- [ ] **Step 6: Commit, only when the owner says so**

Use the message `Courtyard: ring roof geometry and roof plan`.

---

### Task 10: Elevations, sections and the rest of the drawing set

**Files:**
- Modify: `99_Source/sheets_elev.py`:
  - **Replace:** `_roof_long`, `_chaipu_long`, `_roof_end`, `_front_gable` with one `_roof_profile(e, face)`.
  - **Rewrite:** the roof and stair parts of `section(e, name)`.
- Modify: `99_Source/sheets_arch.py`. Check `sheet_site`, `sheet_phasing` and `sheet_plan` (pillars and courtyard hatch).
- Modify: `99_Source/sheetlib.py`. `Plan.floor_extras()` draws the courtyard hatch and the walkway pillars on the ground plan.
- Modify: `99_Source/quantities.py`, which reads duplex room ids.

**Interfaces:**
- **Consumes:** `geom.roof_z`, `eave_z`, `ridge_z`, `wing_eave_z`, `M.PILLARS`, `M.COURTYARD`, `M.JHAROKHAS`.
- **Produces:** `_roof_profile(e, face)`.
  - It samples `roof_z` along lines just inside the facade, at 0.25 ft steps.
  - Its silhouette is the max z over the depth of the house for each position along the face.
  - It draws that polyline filled in the duplex's roof colour.
  - Because it is computed, the ring, the wing and the terrace canopy all come out right on every face without per-face code.

- [ ] **Step 1: Write the failing test**

Add `test_pdf_has_every_sheet` to `tests/test_build.py`:

```python
def test_pdf_has_every_sheet():
    import fitz  # PyMuPDF is in the venv used for page checks
    d = fitz.open(str(ROOT / "02_Drawings/PDF/KH-P1_Drawing_Set_RevB.pdf"))
    assert d.page_count == 26
    for i in (13, 14, 15):  # elevations and sections
        assert "COURTYARD" in d[i].get_text().upper() or "MUTRAM" in d[i].get_text().upper(), i
```

If `fitz` is missing, add `pymupdf==1.24.10` to `requirements.txt` and reinstall.

- [ ] **Step 2: Run the build and the test to see the failures**

Run:

```bash
.venv/bin/python -m pytest -q tests/test_build.py
```

Expected: FAIL, either a traceback naming a deleted geom function or the missing courtyard label.

- [ ] **Step 3: Fix each failing sheet**

1. Implement `_roof_profile`.
2. Draw the court on sections A-A (north–south through `CX`) and B-B (east–west through `CY`). Show the open court, the sunken floor at `LEVELS["courtyard"]`, the grille at `eave_z()` and the walkway lean-tos.
3. Label "MUTRAM (OPEN COURTYARD)" on both sections.
4. Delete every reference to `ROOF["gable"]`, `ROOF["wing"]` as the kitchen wing, `ROOF["chaipu"]`, `ROOF["hip"]` and the poomukham.

- [ ] **Step 4: Visual check of every page**

Render each page to PNG at 110 dpi in the scratchpad and look at it. Fix any of these:

- labels overlapping
- text off the sheet
- a room with no name
- a door that isn't drawn
- an elevation without its roof
- a section cut through a wall the wrong way

- [ ] **Step 5: Run the whole suite.** Expected: all pass.

- [ ] **Step 6: Commit, only when the owner says so**

Use the message `Courtyard: elevations, sections and drawing set`.

---

### Task 11: 3D model

**Files:**
- Modify: `99_Source/make_3d.py`, the `model_data()` keys:
  - **Remove:** `house.porch` and `roof.gable/wing/geave/gabletD`.
  - **Add:** `court`, `ring`, `courtEave`, `courtZ`, `walkZ`, `pillars` (walkway + thinnai), `jharokhas`, `roofRing` (eave, ridge, pitch, ring, court eave), `roofWing` (eave, rect), `terrace` (rect, canopy height).
  - **Update:** `house = {"x1": HX1, "x2": HX2, "y1": HY1, "y2": HY2, "block": [HX1, RING[0]]}`.
- Modify: `04_3D/KH-P1_3D_Model.html` (hand-written JS outside the `@MODEL` block).

**Interfaces:**
- **Consumes:** every model key above.
- **Produces:**
  - New builders in the `B` table: `jharokha`, `planter`, `thinnai`.
  - Roof meshes from a JS port of `ring_z` and `wing_roof_z`. It must match Python: same formula, same `MODEL.roofRing` numbers.

**Work items:**

1. **Roof.** Replace the hip/gable/wing/chaipu roof code with two builders:
   - `ringRoof()`: 8 sloped planes, outer and inner per side, meeting on the ridge rect, with hips and valleys at the corners. Tiles use `mat.tile`.
   - `wingRoof()`: a hipped box over `roofWing.rect`.

   Both go in the `roof` group, so the "Lift roof" button keeps working.
2. **Courtyard:**
   - The floor: granite, sunk to `courtZ`.
   - The grille: a thin steel lattice at the court eave, which "Lift roof" also hides.
   - The planter F128 with a tulsi.
3. **Walkway:**
   - Pillars: turned teak on stone bases, reusing the poomukham pillar code.
   - Lean-to roofs: covered by `ringRoof`, because the inner slope runs to `courtEave`.
4. **Thinnai:** two raised platforms (`LEVELS["thinnai"]`), with pillars at the front edge and a lime backrest against the front wall.
5. **Jharokhas:** a teak box on brackets projecting east from the wing. It has a cushion seat at `sill`, a jali lower front, glazed upper panels and a small tiled hood.
6. **Remove** the poomukham-only code:
   - the front gable mukhappu
   - the kitchen wing roof
   - the chaipu
   - the PX1/PY1 porch slab and its plinth face

   Replace `VER()` with a check against `MODEL.thinnai`.
7. **`KIND` map:** add `F128:['planter']`, `F129:['diwan','E']`, the thinnai seats and any new ids from Tasks 5–6.
8. **Walk:**
   - `floorAt()` adds three levels: the court floor at `courtZ` within `court`, the walkway at `walkZ`, and the thinnai at its level.
   - The start position moves to the forecourt on the door axis: `START_Y = MODEL.house.y1 + (y2 - y1) / 2`, start x 90.
   - Camera presets "Front", "Corner", "From above" and "Whole plot" are re-aimed at the house centre.

- [ ] **Step 1: Write the failing check**

Add to `tests/test_build.py`:

```python
def test_3d_model_has_courtyard_keys():
    import json
    html = (ROOT / "04_3D/KH-P1_3D_Model.html").read_text(encoding="utf-8")
    data = json.loads(re.search(r"/\*@MODEL\*/const MODEL=(.*?);/\*@END\*/", html, re.S).group(1))
    for k in ("court", "ring", "courtEave", "pillars", "jharokhas", "roofRing", "roofWing", "terrace"):
        assert k in data, k
    assert "porch" not in data["house"]
```

- [ ] **Step 2: Run it to see it fail.** Expected: FAIL on the `court` key.

- [ ] **Step 3: Implement `make_3d.py` keys, then the JS work items 1–8 in order.**

After each item:
1. Run `.venv/bin/python build.py`.
2. Copy the HTML into the scratchpad web folder as `3d.html`.
3. Run the hook `sed` so the test copy exposes `__walk`, `__fa` and `__bl`. Insert `window.__walk=walk;window.__fa=floorAt;window.__bl=blocked;` after `walkBtn.addEventListener('click',()=>setWalk(!walk.on));`.
4. Serve it with `python3 -m http.server 8766` from that folder, in the background.
5. Open it in the in-app browser.
6. Check the console for errors with `read_console_messages` (`onlyErrors`).

- [ ] **Step 4: Walk tests**

Run these walks in the browser with the radius-0.8 path checker used for the duplex. Each route must come back with an empty blocked list.

- **Ground floor:**
  1. Forecourt → thinnai → main door → genkan → entry hall → east walkway → round all four walkway sides.
  2. Walkway → dining → kitchen → utility.
  3. Walkway → stair hall → master → master bath and walk-in; stair hall → den → den bath; stair hall → powder room.
  4. Entry hall → oonjal hall → pooja door; walkway → family living.
- **Upper floor:**
  1. Stair → stair head → jharokha seat front.
  2. Stair head → reading room → jharokha → terrace door → terrace: daybed, swing, laundry.
  3. Stair head → Bedroom 2 → walk-in → bath; stair head → upper toilet → theatre.

Take one screenshot of each of these and send them to the owner:
- the courtyard from the entry hall
- the oonjal hall
- the stair-head jharokha looking down into the court
- the terrace
- the thinnai from the forecourt

- [ ] **Step 5: Run the whole suite and check the project file is clean**

Run:

```bash
.venv/bin/python -m pytest -q && grep -c __walk ../04_3D/KH-P1_3D_Model.html
```

Expected: all pass, and the `grep` prints `0`.

- [ ] **Step 6: Commit, only when the owner says so**

Use the message `Courtyard: 3D model round the open courtyard`.

---

### Task 12: Review, publish and hand-over

**Files:**
- Modify: whatever the reviews find. Each finding is a small edit to `model.py` or the builders, re-tested with the full suite.
- Modify: `01_Brief/Courtyard_Concept_Spec.md`. Set **Status** to "drawn", and bring section 3/4 sizes in line with the model.

- [ ] **Step 1: Room reviews**

Run one review per room group, as was done for the duplex:

1. Thinnai, entry hall and oonjal hall.
2. Living and dining.
3. Kitchen and utility.
4. Master suite.
5. Den.
6. Stair, upstairs wing and terrace.
7. Baths.
8. A flow-and-light review of the courtyard.

Each review reads the spec, the plans (PDF pages 4–7) and the 3D screenshots, and reports concrete problems with coordinates.

Bring the findings to the owner grouped by severity. Fix only what the owner approves.

- [ ] **Step 2: Publish the 3D model**

Publish the 3D model as a **new** artifact. Copy the HTML to the scratchpad as `Courtyard_House_3D.html`, then publish without a `url`. Tell the owner the new link. The duplex artifact stays as it is.

- [ ] **Step 3: Final suite run**

Run:

```bash
.venv/bin/python -m pytest -q
```

Expected: all pass.

- [ ] **Step 4: Commit and push, only when the owner says so**

Commit with the message `Courtyard: reviews and spec brought up to date`. Then push:

```bash
git push -q -u origin feature/courtyard
```
