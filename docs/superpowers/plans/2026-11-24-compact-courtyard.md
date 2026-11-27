# Compact Courtyard House Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** shrink the courtyard house from 54 × 54 ft (about 4,200 sq ft over two floors) to a 42 × 42 ft ring (about 2,000 sq ft). The plot becomes about 50 × 130 ft. All outputs (PDF set, DXF, XLSX, guide, 3D) keep generating from `99_Source/model.py`.

**Architecture:** the same generator built in the first courtyard plan (`docs/superpowers/plans/2026-11-24-courtyard-house.md`). This plan:

1. Changes the grid constants and the plot.
2. Re-cuts every room, door, window, fixture and point for the smaller ring.
3. Updates the tests' numbers.
4. Checks that the parametric parts (ring roof, elevations, sections, 3D roof) follow the new grid.

The walkway round the courtyard becomes the only hallway on the ground floor.

**Tech Stack:** unchanged. Python 3 in `99_Source/.venv` (reportlab, ezdxf, openpyxl, pymupdf, pytest); three.js in `04_3D/KH-P1_3D_Model.html`.

**Spec:** `01_Brief/Courtyard_Concept_Spec.md`. Where it conflicts with this plan, this plan's sizes win. The spec is rewritten in Task C7.

## Global Constraints

- **Git and publishing rules** are unchanged:
  - Work on `feature/courtyard` only.
  - No git commits: the controller snapshots the work.
  - No artifact publishing except the new courtyard artifact, in Task C11.
  - No `gh`.
  - Never put the owner's real site coordinates anywhere.
- **Project 3D file:** `04_3D/KH-P1_3D_Model.html` must contain 0 `__walk`.
- **Coordinates:** in feet; x from the west boundary, y from the south boundary.
- **Grid constants** (model.py):
  - `HX1, HX2, HY1, HY2 = 15.0, 57.0, 4.0, 46.0` (42 × 42)
  - `BAND, WALK, COURT = 12.5, 3.5, 10.0`
  - `CX, CY = 36.0, 25.0`
  - `CT = (31, 41, 20, 30)`
  - `RING = (27.5, 44.5, 16.5, 33.5)`
- **Plot:** 50 ft wide (north–south) × 130 ft deep (east–west), with the road on the east.
  - Back garden x 0–15.
  - Thinnai x 57–62.
  - Front land x 62–130: forecourt, car porch and drive on the north side with the gate in the north-east, food garden, workshop, the two rental shops on the road front, sump in the north-east, septic tank, soak pit, recharge pit.
  - Anything that cannot fit must be reported, not silently dropped.
- **Owner decisions (2026-11-24, binding):**
  - Tight ring 42 × 42 ft.
  - Genkan and entry hall merged into one small foyer.
  - The oonjal moves out of its own hall to a corner open to the family room.
  - Living and dining become one room.
  - Upstairs reading room and theatre become one family room.
  - Earlier decisions still hold: tulsi in the courtyard; thinnai floor red oxide with turned teak pillars; a swing on the terrace and the oonjal indoors; the hotel-style Bedroom 2 suite; each basin opposite its bathroom door; vastu placements.
- **Group B (elderly parent and access), owner-approved, built in as the rooms are made:**
  - Grab rails beside every WC and in the master and den showers.
  - Fold-down shower seats in the master and den baths.
  - Pull-cord alarms in the master and den baths, with sounders in the kitchen and den.
  - Low 1'-0" motion footlights on the master's bed-to-bath route.
  - Bath doors of at least 2'-8" for the den bath and the powder room.
  - Handrails on both sides of the entrance steps, and a grab post at the foyer step.
  - A reserved 1:12 ramp to the thinnai.
  - A deeper dining bench (16 in) plus an armchair.
  - A reading chair in the master.
  - Jharokha seat at 2'-0" with a grab rail at its step.
- **Vastu:**

  | Element | Placement |
  |---|---|
  | Main door | East wall, in its north half |
  | Courtyard | On the centre (36, 25) |
  | Pooja | North-east corner |
  | Kitchen | South-east |
  | Master bedroom | South-west, bed head south |
  | Den | North-west |
  | Stair | West band |
  | Upper mass | West band only |
  | Toilets | None in the north-east |

- **Standards carried over:**
  - Stair: 16 risers of 7.5 in, 10 in treads; flights and landing 3'-6" clear between wall faces; arrival facing south toward Bedroom 2.
  - Guards: 4 ft high, gaps of 100 mm or less.
  - Bathrooms: WC 15 in side clearance and 21 in in front; showers at least 3 × 3 ft.
  - Circulation: 2 ft clear from each door to every other door of a room.
- **Upper wing and terrace:** the upper wing stays within the west band x 15–27.5. The roof terrace sits over the living (north band).
- **Must-fix items from the first plan's reviews, built into the new layout:**
  - **A courtyard overflow:** a second drain at the north-west corner, a standpipe overflow 3 in above the floor, and a scupper through the walkway kerb.
  - **The stair landing window:** its sill at least 3'-0" above the landing, or a fixed guard to 3'-0".
  - **Exhaust fans:** only through outer walls.
  - **Shower glass:** no shower open toward a WC or a door.
  - **Store under the landing:** shown as a low hatch store.
  - **LPG cage:** at least 1.5 m from every drain.
  - **Inverter:** not beside a bedroom's only exit.
  - **Water tank:** on a shaded platform, not in a roof void.

## Room allocation (ground floor), the starting layout

The bands are 12.5 ft deep. The corner blocks are 12.5 × 12.5. The middle bands are 17 ft long.

| Block | Extent | Holds |
|---|---|---|
| North-west | x 15–27.5, y 33.5–46 | R42 den |
| West middle | x 15–27.5, y 16.5–33.5 | R06 stair against the west wall (3'-6" clear flights, landing over a low store R46), R07 den bath on the west outer wall (stacked under the upper toilet), R47 linen/DB cupboard if room allows; opens to the west walkway |
| South-west | x 15–27.5, y 4–16.5 | R01 master bedroom |
| South middle | x 27.5–44.5, y 4–16.5 | R40 master bath (entered from the master, basin opposite its door), R08 powder room (entered from the south walkway, near the foyer route), R13 utility (entered from the kitchen; service door on the south wall) |
| South-east | x 44.5–57, y 4–16.5 | R15 kitchen, with the pantry inside it |
| East band + north band | | One L-shaped family room R16 (living and dining) wrapping the courtyard's north-east. The dining end sits next to the kitchen in x 44.5–57, y 16.5–25. A strip x 44.5–51, y 25–33.5 with the oonjal links it to the living in the north band x 27.5–51, y 33.5–46. |
| Foyer | x 51–57, y 25–33.5 | R18: main door on the east wall at about y 27–31 (north half), shoe bench, uruli niche, opening into the family room and onto the walkway |
| North-east corner | x 51–57, y 40–46 | R11 pooja, opening west. The rest of the north-east block (x 51–57, y 33.5–40) is part of the family room (TV/console nook or the oonjal) |
| Centre | | R50 courtyard = CT. Walkway rects R51, R61, R62, R63 on the RING. Walkway pillars at the courtyard corners and mid-sides. |
| Thinnai | x 57–62, y 24–34 | R17 thinnai, with its lean-to roof |

The designer may refine the sub-division inside these blocks. Every rule above must hold, and the Task C2 owner checkpoint shows the result.

**Upper wing (west band x 15–27.5):**
- **R31 Bedroom 2:** south-west, bed head south.
- **R45 walk-in, then R33 bath:** the bath's WC on the west outer wall.
- **R41 stair head:** over the stair.
- **R39 upper toilet:** stacked over R07.
- **R36 upstairs family room:** north-west. One room with the bookshelf wall, the screen, the sofa-bed, the desk and a jharokha seat over the courtyard.
- **R37 roof terrace:** over the living (north band x 27.5–44.5), with its canopy, swing, daybed and laundry corner.
- **Jharokhas:** project east from x 27.5 over the walkway roof (one at the stair head, one in the family room). Each sits on a 6 in kerb, with the seat at 2'-0".

## Tasks

Each task: update the code and data, update and extend the tests (`.venv/bin/python -m pytest -q`, all green except `test_build.py` where the task says it may be red), render the sheets the task touches to PNGs in the scratchpad, write a report, no git commands.

### Task C1: Grid, plot and site
- Set the grid constants and PLOT above. Update `plot_north`, SITE, DRIVE and all SITE_FEATURES, TREES, FOOD_TREES and GARDEN_BEDS for the 50 × 130 plot.
- Keep every feature id the sheets and `make_3d.py` read.
- Add a RAMP reserve: 1:12, 4 ft wide with a landing, to the thinnai.
- Update `tests/test_courtyard.py`'s grid, plot, site, tree and service tests to the new numbers: soak pit 60 ft or more from the borewell and about 20 ft or more from the house, trees 25 ft or more from the house (the forecourt tree 15 ft or more), sump in the north-east, septic not in the plot's north-east quadrant.
- Report anything that cannot fit.

### Task C2: Ground-floor rooms, walls, levels, finishes, ceilings, pillars (owner checkpoint)
- Re-cut ROOMS and WALLS to the allocation above, and update EXTERIOR, WET_WALLS, LEVELS, FLOOR_FINISH, ROOM_FLOOR, CEILINGS, PILLARS, STAIR and SLAB as needed.
- Temporarily empty the ground DOORS, WINDOWS, FURNITURE, ELECTRICAL, PLUMBING and PIPES if they block the tests.
- Update the room tests: vastu zones, minimum clear sizes and the courtyard centre. Suggested minimum clear sizes:

  | Space | Minimum |
  |---|---|
  | Master bedroom | 11.5 × 11.5 |
  | Den | 11 × 10 |
  | Family room | 300 sq ft or more |
  | Kitchen | 11 × 9 |
  | Each bath | 6 × 6.3 |
  | Powder room | 4.5 × 6 |
  | Foyer | 5.5 × 8 |

- Render A-102.
- The controller shows the plan to the owner before Task C3.

### Task C3: Doors, windows, transoms
- Re-place every door and window for the new rooms: main door, folding doors onto the walkway, bath doors (at least 2'-8" where Group B says), pooja door opening west, service door.
- Windows on every outer-wall room; south and west windows small or jali.
- The stair landing window sill at least 3'-0" above the landing.
- Keep the reachability test: every ground room reachable from the foyer R18.

### Task C4: Ground furniture and fittings
- Carry over the furniture by role: master, den, family room (living and dining with the 16 in bench, the stools and an armchair), kitchen, utility, pooja mandapam, oonjal, foyer shoe bench and uruli niche, thinnai seats, kolam stone, nilavilakku, rain-chain basins under the thinnai eave corners, rinse shower at least 1.5 m from the LPG cage, pocket garden visible from the dining, tulsi planter, airer, LPG cage.
- Add the Group B grab rails, shower seats and reading chair.
- Keep the tests for basin opposite door, collisions, circulation and viewing distance. Update KIND in the 3D page for every id.

### Task C5: Upper wing, stair, terrace, jharokhas (owner checkpoint)
- Re-cut the upper floor to the allocation above, including the hotel suite, R39 over R07, the stair well clear, and the 3'-6" clear stair.
- Terrace over the living, with its canopy, railing and north jali.
- Jharokhas on kerbs.
- Update the upper tests.
- Render A-103 and A-105. The controller shows them to the owner before Task C6.

### Task C6: Electrical, plumbing, pipes
- Rebuild all points and pipes for the new layout, including:
  - the Group B alarms and footlights (ELEC_TYPES gets a low footlight code);
  - the second courtyard drain and the overflow;
  - exhaust fans only through outer walls;
  - the inverter away from any bedroom's only exit;
  - the tank on a shaded platform;
  - the LPG cage at least 1.5 m from every drain.
- Keep the pipe tests: separation, trees, reachability, inspection-chamber spacing, soil outside the house except WC stubs.

### Task C7: Text and spec
- Rewrite FINISHES, SPEC, OPEN_ISSUES, PHASES (re-priced roughly for about 2,000 sq ft), PROJECT text and COURTYARD_DECISIONS (add the compact decisions and Group B) for the compact house.
- Rewrite `01_Brief/Courtyard_Concept_Spec.md`: status "drawn", the plot and site table, the room tables with the real sizes, the area table (compact against the 54 × 54 against the duplex), and the open review items not yet approved (groups A remainder, C, D).
- Keep the no-duplex-terms test.

### Task C8: Roof
- Check the ROOF dict and geom follow the new grid: ring and court eave from the constants; wing over x 15–27.5 plus its 2 ft east overhang (x 29.5); terrace over the north band; thinnai lean-to over x 57–61.75; verge and upstand rules; downpipes clear of windows and doors.
- Make the tests derive from the constants: thinnai headroom 7.5 ft or more, jharokha kerb clearance, canopy clear of the wing gutter.
- Render A-110.

### Task C9: Drawing set
- Build everything, render all 26 pages and look at each one: tags inside the frame, no overlaps, levels quoted from geom, sections through the courtyard showing the wing beyond.
- Fix the sheet code where the smaller house exposes layout problems.

### Task C10: 3D model
- Rebuild, check the console, run walk tests on every route on both floors (empty blocked lists), fix any duplex-size assumptions, and take five screenshots: courtyard from the foyer, the family room with the oonjal, the stair-head jharokha, the terrace, and the thinnai from the forecourt.

### Task C11: Final review and publish (controller)
- One whole-house review against the spec and the owner decisions.
- Show the owner the screenshots and the plans.
- Publish the 3D model as a NEW artifact (never the duplex one).
- List every ruling made on the owner's behalf.
