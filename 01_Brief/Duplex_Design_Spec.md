# Duplex option: design spec

> **Revised 1 Nov 2026: no double height.** A slab now covers the whole two-storey block. The living, dining and kitchen have flat ceilings at about 9'-5", and the front half of the first floor is a 16 x 22 ft covered terrace. The terrace opens off the landing, has railings on three sides, and sits under the main roof carried on galvanised steel posts and trusses. The landing jali window, the clerestories and the high space over the kitchen are gone. The sections below are updated to match.

Branch `feature/duplex`. A trial to see how much plot length a two-level house actually needs. Main keeps the single-storey design for comparison.

## Brief

- Same plot and road (east), but the house and its yards use only the front **55 ft** (x 20–75). The back 20 ft (x 0–20) stays spare land (kitchen garden, utility, future).
- 3 bedrooms:
  - **Ground floor:** a master bedroom with an attached bath, and a small bedroom that uses the common bath.
  - **First floor:** a second master suite with its own bath, dressing room and a sitting and study zone, plus the covered terrace.
- **Ground floor:** living, dining, kitchen, pooja, store and wet area at the front; bedrooms, baths, lobby and stair at the back. All have normal-height flat ceilings.
- **First floor:** rooms over the back half, and a covered terrace over the front half.

## Footprint and setbacks

| | Value |
|---|---|
| House | 44 × 22 ft (x 23–67, y 3–25) |
| Front yard (east) | 8 ft, unchanged: porch steps, forecourt, two-wheeler bay |
| Rear gap (west, inside the 55 ft) | 3 ft |
| Side walkways | 3 ft south, 2 ft north (as now) |
| Ground floor | 968 sq ft |
| First floor, enclosed | about 445 sq ft (master suite with sitting zone, bath, dressing, landing, stair) |
| First floor, covered terrace | 16 x 22 ft, about 350 sq ft |

## Ground floor

Plan sketch, not to scale. West is on the left, the road (east) on the right, north at the top.

```
x: 23          35     40.5  45                 55     61      67
   ┌───────────┬────────────┬──────────────────────────┬───────┐ y 25
   │ Small bed │   Stair    │   LIVING                  │       │
   │           │  dog-leg   │                    ┌─────┤ POOM- │
   ├───────────┤ ↑ ·pass·   │                    │Pooja│ UKHAM │◄ main door
   │           ├────────────┤                    └─────┤       │
   │  Master   │   Lobby    ═ (wide opening)           ├───────┤ y 12.5
   │           ├──────┬─────┤   DINING      ┌──────────┴───────┤
   │           │M.bath│C.bth├──────┬────────┤  KITCHEN         │
   │           │      │     │Store │  Wet   │  (loft above)    │
   └───────────┴──────┴─────┴──────┴────────┴──────────────────┘ y 3
```

| Room | Extent (x × y) | Size | Height |
|---|---|---|---|
| Poomukham (porch) | 61–67 × 12.5–25 | 6 × 12.5 | single, under the front gable; main door on the x 61 wall |
| Living | 45–61 × 12.5–25, less the pooja | about 184 sq ft | slab soffit, 9'-5" |
| Pooja | 57–61 × 12.5–16.5 | 4 × 4 | single |
| Dining | 45–55 × 7.5–12.5, open to living | about 50 sq ft + spill into the living | slab soffit, 9'-5" |
| Kitchen | 55–67 × 3–12.5 | 12 × 9.5 | flat ceiling at 9 ft 5 in |
| Wet area | 49–55 × 3–7.5 | 6 × 4.5 | single; side door to the south walkway |
| Store | 45–49 × 3–7.5 | 4 × 4.5 | single, opens off the dining |
| Lobby | 35–45 × 10–13.5 | 10 × 3.5 | single; wide opening to the living |
| Master bedroom | 23–35 × 3–15.5 | 12 × 12.5 | single |
| Master bath | 35–40.5 × 3–10 | 5.5 × 7 | single |
| Common bath | 40.5–45 × 3–10 | 4.5 × 7 | single, door from the lobby |
| Small bedroom | 23–35 × 15.5–25 | 12 × 9.5 | single; reached from the lobby through the open space under the upper flight (7 ft+ headroom), then a 2'-6" passage |
| Stair | 37.5–45 × 13.5–25 | dog-leg | the stair's side wall to the living is a timber jali |

## First floor (floor level +10 ft)

| Room | Extent | Size | Notes |
|---|---|---|---|
| Upper master | 23–35 × 3–15.5 | 12 × 12.5 | west wall mostly solid (afternoon sun); windows south |
| Upper master bath | 35–40.5 × 3–10 | 5.5 × 7 | stacked over the ground-floor baths |
| Dressing / linen | 40.5–45 × 3–10 | 4.5 × 7 | off the upper master |
| Landing | 35–45 × 10–14 | 10 × 4 | glazed door out to the covered terrace |
| Sitting and study (part of the upper master) | 23–35 × 15.5–25 | 12 × 9.5 | **north side**, 6 ft north window, desk on the west wall, window diwan; a 6 ft wardrobe part-divides it from the bed (the outdoor lounge was merged in once the terrace was added) |
| Covered terrace | 45–61 × 3–25 | 16 × 22 | under the main roof on galvanised steel posts and trusses; railings on the north, south and east; diwan, chairs, drying rails, planters |

## Levels and stair

- Ground FFL +2 ft above ground (as now). Floor-to-floor height 10 ft, so the first-floor level is +12 ft above ground.
- **Stair:** dog-leg, two flights 3'-6" wide.
  - 17 risers of about 7 in, treads 10 in.
  - 9 + 8 risers, with a 3'-6" half landing at the north end.
  - The foot is at the lobby, so it is seen from the living.
- **Terrace:** waterproofed slab falling 1:80 to a drain in the south-east corner; steel posts on RCC stubs 6 in above the tiles.

## Roof

- **Main roof:** one hipped clay-tile roof over the whole two-storey block (x 21–63 at the eaves). It sits on the walls over the back rooms and on a light steel frame over the terrace.
- **Front gable:** a lower gable over the single-storey poomukham and kitchen front, facing the road, so the house reads as a two-tier Kerala roof.
- **No ridge ventilator:** with the terrace open on three sides, hot air under the roof escapes at its open edges; the attic over the upper rooms has meshed ridge and soffit vents.
- **Option:** the terrace part of the roof could use an insulated metal sheet on the same steel frame to save cost.
- **Eaves:** 2 ft overhang throughout. Rainwater goes to the sump, as now.

## Services

- **Wet rooms stack:** all four baths sit in one strip (x 35–45, south side), two over two, so there is one soil stack.
- **Septic tank and soak pit:** move to the spare rear land (x 5–18), behind the baths.
  - That keeps them far from the sump and the front door, and frees the front yard.
  - If the trial must stay strictly within 55 ft, they go back under the two-wheeler bay as now.
- **Water tank:** on the back-block roof or slab, so no tank stand is needed. It gives more head than the current stand.
- **AC:** the three bedrooms; the living can take one later (normal-height room).

## What stays from the current design

- The front elevation language: gable, pillars, charupadi seats, swing, laterite kitchen front.
- Materials, finishes and the look selector.
- The thin precast compound wall, now around the 55 ft trial plot.

## Build scope (after this spec is approved)

- **`model.py`:** add a `FLOOR` tag to rooms, walls, doors, windows and furniture (G / F1). Add a stair and slab, and per-floor heights.
- **Drawings:** ground- and first-floor plan sheets, sections through the stair and the terrace, elevations with two roof blocks, and the DXF with layers per floor.
- **Schedules and quantities:** areas per floor, slab, stair.
- **3D model:** a second storey, a walkable stair up to the terrace, and a floor toggle so you can view each level.
