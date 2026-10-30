# Kerala Home, Phase 1: pre-construction design package

Revision B (pre-construction draft), 30 Oct 2026. Prepared by the owner with Claude (AI assistant).
This is a Kerala-style house sited in **Guntur, Andhra Pradesh**, on a 27 ft x 75 ft agricultural plot (length to be confirmed by survey).
The package is detailed enough for an architect, a structural engineer and MEP consultants to review, mark up and sign.
It is **not** for construction or approval until they have done so.

## Folder structure

| Folder | Contents | Format |
|---|---|---|
| 01_Brief | Design brief (Guntur climate and ground), room-by-room detailing guide (mistakes to avoid) | Markdown |
| 02_Drawings/PDF | 19-sheet A3 drawing set (see index below); earlier revisions in `Superseded` | PDF |
| 02_Drawings/CAD | Site and ground floor in millimetres with typed walls, electrical and plumbing layers | DXF |
| 03_Schedules | Rooms (clear sizes, levels, ceilings), doors, windows, furniture budget, finishes, specification, quantities with rate cells, electrical and plumbing points, checklist, hold points, open issues, decisions | Excel |
| 04_3D | Interactive 3D model (open in a browser, needs internet) plus online link | HTML |
| 05_Handover | Questions for the surveyor, architect, engineer, MEP and Vastu consultant | Markdown |
| 99_Source | Scripts that generate every drawing, schedule, the guide and the 3D model from one data model | Python |

## Drawing set (Rev B)

| Sheet | Title |
|---|---|
| A-000 / A-001 | Cover and index; design basis, levels, wall types, general notes, hold points |
| A-101 | Site plan and services (tank, septic, soak pit, sump, recharge pit, pergola, apron) |
| A-102 / A-103 | Ground floor plan with wall types; furniture layout |
| A-104 | Working plan: clear room sizes, section lines |
| A-105 | Floor finishes and levels |
| A-106 | Roof plan: ridges, valleys, gutters, downpipes, dining ventilator, solar zone |
| A-201 / A-202 | Elevations: north, south, east (road), west |
| A-301 | Sections A-A and B-B |
| A-401 | Door and window details |
| A-501 to A-503 | Dining ventilator; typical details: plinth and apron, flush skirting, window sill, eaves and gutter, bathroom, kitchen counter, hand-wash basin, AAC joints, thresholds |
| A-601 | Schedules |
| E-101 / E-102 | Lighting, fans and ceilings; power, AC and data |
| P-101 | Water supply and drainage |

## Typical next stages

1. **Land and survey:** confirm the agricultural-land conversion and permission route; level survey; soil test; water test.
2. **Professional review** of this package: architect, structural engineer, MEP, Vastu. Their mark-ups become Rev C.
3. **Statutory drawings:** permit submission under the AP Building Rules 2017 (via APDPMS or the panchayat).
4. **Good-for-construction (GFC) set:** structural drawings and bar bending schedules, final MEP, priced BOQ from the Quantities tab.
5. **Interior drawings:** joinery, lighting scenes, finishes.

## Regenerating the package

Every output comes from `99_Source/model.py` (rooms, walls, levels, roof, doors, windows, furniture, services, finishes,
specification, issues, decisions) and `99_Source/guide.py` (the room-by-room checklist). Edit them, then rebuild everything at once:

```bash
cd 99_Source
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # first time only
.venv/bin/python build.py
```

Before issuing a new revision, bump `REV` in `99_Source/paths.py` and `PROJECT["rev"]` in `model.py`, and move the old files into `Superseded`.
In the 3D model the textures, roof timbers and furniture heights are set in the HTML; everything else comes from the model.

## Units and conventions

- Feet-inches in the PDF and Excel files; millimetres in the DXF (1 ft = 304.8 mm). Levels are measured from finished ground.
- Plan dimensions are to wall centrelines; clear sizes (wall face to wall face) are on A-104 and in the Rooms tab.
- Walls: 9 in outer, 7 in plumbing walls, 5 in inner (AAC plus plaster).
- Drawings are north-up.
