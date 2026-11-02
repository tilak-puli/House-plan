# Noah Daniel review: alignment, grids, axes and hierarchy

Aspect: the "lines". All numbers come from `99_Source/model.py`, in feet: x runs west to east, y runs south to north. Wall faces use the model's wall types: EXT 0.75, WET 0.58, INT 0.42.

---

## 1. Noah's take

"Okay friends, I'm going to be insufferable about lines today. You know I'm obsessed with aligning things. The good news is that this house already *has* a grid hiding in it.
- The bays run x 14 / 28 / 42 / 53 / 67: that's 14, 14, 11, 14.
- The hip ridge sits exactly on y 14, which is the centreline of the house and also the upstairs bedroom/study wall.
- Upstairs, Bedroom 2 and the study put the bed, the wardrobe, the sofa-bed, the bookshelf, both north windows and the fan all on one line at x 21. Chef's kiss.

The problem is that the ground floor hasn't heard about any of it.
- The master bed is a foot off that line, and it's half backed by a wardrobe that stops in the middle of it.
- The TV is hung across a window.
- The upstairs wall hangs six inches off the wall below it.
- Four of the six steel terrace posts land on a window, a door or the middle of the kitchen.
- The front door is four inches off the gable that's supposed to announce it.

None of these are big moves on their own. Together they are the difference between 'it just feels very tidy and intentional' and 'it feels like a lot of things that are almost aligned', and 'almost aligned' is the worst kind. Does that make sense?"

---

## 2. Findings, most important first

### 1. The terrace posts don't land on anything below
**Severity: Major move**

**What he sees.** `TERRACE_POSTS` carry the main roof over the covered terrace. Checked against the ground floor:

| Post | What is directly below it at ground floor |
|---|---|
| (51, 3) | South wall, over the middle of wet-area window **W12** (x 50.1–51.8, centre 50.95). The post is 0.05 ft off the window centre. |
| (61, 3) | South wall, over the middle of kitchen window **W07** (x 58.5–64.5). The post is 0.5 ft from the window centre, over the prep sink. |
| (61, 10.3) | Inside the kitchen. There is no wall at x 61 between y 3 and 12.5 (`WALLS` has Y 61 only from 12.5 to 25). The post lands over the tall pantry **F37** (x 60.9–62.9, y 10.1–12.1). |
| (61, 17.7) | On wall x 61, over the main door **D01** (y 17.6–20.6), 1 in inside its south jamb. |
| (51, 25) | North wall, 0.5 ft east of the jamb of living window **W09** (east jamb at 50.5). A 9 in column or stub would touch the window frame. |
| (61, 25) | A wall corner. This is the only clean one. |

The bays are also uneven: x 42–51 is 9 ft and x 51–61 is 10 ft. Along x 61 the posts sit at y 3 / 10.3 / 17.7 / 25, which is even thirds of the 22 ft depth. But that rhythm belongs to nothing in the plan.

On the east elevation (A-202), the post at y 17.7 stands about 1 ft south of the gable apex (y 18.75). It shows inside the gable's back triangle as a near-miss.

**Why it bothers him.** These are column lines, and they're the most honest structure in the house: "skylights and openings follow the structure" [EC].
- Openings should sit between structure, not under it.
- The façade should express what's inside it [FP4, FP6].
- A post 1 ft off the gable's centre is a textbook "almost aligned" façade [WORST, FP1].

**His change.** Put every post on a wall corner of the x-grid:
- **x 53 line** (the kitchen/wet-area wall, already a T-junction at (53, 3)): posts at (53, 3) and (53, 25). (53, 25) is 2.5 ft clear of W09.
- **x 61 line**: posts at (61, 3), (61, 12.5) and (61, 25). (61, 12.5) is the T where the kitchen north wall meets the poomukham wall.
  - Drop the posts at y 10.3 and 17.7.
  - Along x 61 the spans become 9.5 ft and 12.5 ft.
  - The two posts at y 12.5 and 25 now **frame the poomukham bay symmetrically about the door axis y 18.75**, 6.25 ft each side. From the terrace and from the road they bracket the gable instead of nicking it.
- **Move W07** wholly west of x 61 so the post at (61, 3) sits on solid wall with a column under it. W07 stays a 6 ft window at x 54.6–60.6 (centre 57.6), the prep sink F65 re-centres under it, and the south counter F34 keeps its run.
  - From the sink to the hob corner there is then about 6 ft of clear prep. That's what he wants anyway: "prep space beats the work triangle" [KIT].
  - It also means the kitchen window sits entirely under the two-storey mass and not across the line where the slab meets the wing roof. That junction is visible on the south elevation (A-201) right above W07.

**Trade-offs and knock-on effects.**
- Terrace bays become 11 ft (x 42–53) and 8 ft (x 53–61), so they're still asymmetric. But each bay now means something: the 11 ft bay sits over dining and living, the 8 ft bay over the kitchen.
- The 12.5 ft eave span on x 61 needs a deeper steel edge member or truss bearing plate. That's a modest cost; the structural engineer sizes it.
- The main-roof ridge ends at x 50 (hip run 13 ft from eave x 63). That's 3 ft from the new x 53 line, against 1 ft today. It isn't visible inside, because the terrace ceiling is trusses, so he would accept it.
- The sink moves about 4 ft west, which shortens the sink-to-hob walk slightly. The RO and PC points move with it.
- Vastu isn't affected: the cook still faces east.

**Confidence: high.** He wouldn't phrase it as "columns", but he'd catch the post through the window and the post next to the gable apex instantly.

---

### 2. Upstairs walls hang 6 in off the walls below (y 11.5 / 12 / 12.5)
**Severity: Significant**

**What he sees.** The long cross wall of the back block is drawn at three lines within 1 ft of each other.

| Floor | Wall | Line | Faces |
|---|---|---|---|
| Ground | X 12, x 26–42 (small room and common bath north wall) | y 12 | 11.79–12.21 (INT) |
| Upper | X 11.5, x 28–42 (alcove and bath north wall) | y 11.5 | 11.29–11.71 |
| Ground | Kitchen north wall, x 53–67 (also the poomukham back) | y 12.5 | |

The upper wall sits beside the wall below rather than on it, with a 1 in gap between faces. A beam at y 11.5 (`PHASE1_PROVISIONS`) would show as a roughly 4 in downstand ledge along the ceilings of the small room and the common bath.

The bath stack is also off:
- The upper bath is 36–42 × 3–11.5 (8.5 ft deep). The common bath is 36–42 × 3–12 (9 ft deep).
- The basins don't stack: F17 is at y 9.4–10.6 and F78 at y 7.4–8.6.

**Why it bothers him.**
- "Align with…", "a clean, thoughtful grid" [FP1, FP3].
- When a wall stacks on a wall, the structure reads "structurally cohesive" [FP1]. He moved a ridge to a new wall for exactly that.
- Two lines 6 in apart are worse than two lines 3 ft apart: they look like a mistake.

**His change.** Put the back block on **one line, y 11.5, on both floors.**
- Ground: walls X 12 (x 26–36 and 36–42) move to y 11.5.
- Small room 10 × 8.5 ft, about 9'-5" × 7'-11" clear.
  - The 4 × 6'-6" bed F01 (y 3.4–7.4) still fits.
  - Wardrobe F03 moves to y 8.1–11.1.
  - Door D04's swing (radius 2.5 ft) clears the bed.
- Common bath 6 × 8.5 ft, matching the upper bath exactly. Basin F17 moves to y 7.4–8.6, under F78.
- Stair hall widens from 3'-5½" clear (12.21 to 15.67) to 3'-11½" clear (11.71 to 15.67). This hall is the house's only route from the living to the master, the small room, the common bath and the stair foot, so it is the right place to gain 6 in.
- Lobby grows to 6.5 × 6.5 ft.
- Leave the kitchen line at y 12.5. The front block is a different structural bay (dining and living are open between x 42 and 53), so the 1 ft step between front and back reads as a deliberate change of bay, not a wobble.

**Alternative.** Put both floors on y 12. This keeps the small room at 9 ft, but the upper landing shrinks from 4'-2" to 3'-8" (3'-5½" clear), barely the 3'-6" flight width. That is worse for a landing with five doors on it.

**Trade-offs and knock-on effects.**
- The small room loses 6 in of depth.
- Phasing: the "beam at y 11.5" provision now sits on the stage-1 wall below, so there is one less beam, which is cheaper.
- The plumbing stack is cleaner: basins over basins.
- Vastu isn't affected.

**Confidence: high** that he'd flag it. Medium on which line he picks. He usually takes inches from a room to give a hallway breathing room only when the hallway is the main route, and here it is.

---

### 3. The front entry axis has two centres, 4 in apart
**Severity: Significant**

**What he sees.** The front gable `ROOF["gable"]` runs y 10.5–27 and is centred at **y 18.75**. So are:
- the poomukham (y 12.5–25);
- the outer pillars at y 13.1 and 24.4 (± 5.65).

Everything else on the entry sequence is centred at **y 19.1**:
- main door D01 (y 17.6–20.6);
- inner pillars at y 16.4 and 21.8 (± 2.7);
- steps (y 17.3–20.9);
- path (y 16.1–22.1);
- tulsi thara (y 19.1);
- gate (y 15.6–22.6).

The model comment on the gable says "centred on the main door (y 18.75)". It isn't: it's 0.35 ft (4¼ in) off.

The asymmetry causes knock-ons:
- Pillar bays are 3.3 / 5.4 / 2.6 ft, so the two charupadi seats differ. F42 is 2.3 ft long (y 13.6–15.9) and F69 is 1.9 ft (y 22.15–24.05). The "symmetrical flanking seats" aren't.
- Inside, the vilakku lamp niche F59 (y 18.0–19.8, centre 18.9) is the thing the axis ends on. It's 0.2 ft off the door and 0.15 ft off the gable, so it matches neither.

**Why it bothers him.**
- One axis, punctuated at the end: "punctuate the end of this axis" [FP1, FP3, FP5, FP6].
- His professor story about the misaligned door [§1].
- The entry should read as the most important, clearest thing on the façade [FP1, FP7].

**His change.** Everything goes on **y 18.75**, the poomukham centre and gable ridge. The plot boundary fixes the gable's north eave at y 27, so the gable can't move and the door has to.

| Element | Now | New |
|---|---|---|
| Main door D01 | 17.6–20.6 | 17.25–20.25. Better, with finding 4: 4 ft wide at 16.75–20.75. |
| Inner pillars | 16.4 / 21.8 | 16.05 / 21.45, so the bays become 3.0 / 5.4 / 3.0 |
| Charupadi seats F42, F69 | unequal | both about 2.4 ft, mirrored |
| Steps | 17.3–20.9 | 16.95–20.55 |
| Path | 16.1–22.1 | 15.75–21.75 |
| Tulsi thara | (72.4, 19.1) | (72.4, 18.75) |
| Gate | 15.6–22.6 | 15.25–22.25 |
| Lamp niche F59 | 18.0–19.8 | 17.85–19.65 |
| Gable vents GV1-3 | | stay on 18.75 |

On the terrace, the diwan, coffee table and armchairs (F84–F87, now centred at y 19.0) move 0.25 ft south to y 18.75. That puts the terrace's seating group on the gable's centreline, looking at the jali that closes the gable's back triangle.

**Trade-offs and knock-on effects.**
- None structurally: these are setting-out changes.
- The 4 ft door's south jamb at y 16.75 lands flush with the pooja's north wall face (16.71). So the door's south reveal continues the pooja wall line, and the south leaf opens flat against that wall. That's a bonus alignment.
- The shoe bench F52 (y 21.2–24.4) keeps 0.45 ft clear of the north jamb.
- Vastu: the door stays on the east and moves 4 in south. Ask the consultant if a pada matters.

**Confidence: high.**

---

### 4. The main door doesn't out-rank the pooja door, or any other door
**Severity: Significant**

**What he sees.** D01, the main door, is 3'-0" wide (y 17.6–20.6), teak double leaf, so each leaf is 1'-6". D11, the pooja door, is also 3'-0" (y 13.0–16.0), *carved* teak double leaf.

The two sit 4 ft apart in x and side by side in y, on the same side of the living. From the sofa you see two near-identical 3 ft double teak doors, and the carved one is the pooja's.

Every door head is at 7'-0" (`LEVELS["door_head"]`). The interior doors come in five widths: 2'-5", 2'-6", 2'-7", 2'-10" and 3'-0".

The threshold from the living into the private wing is the 3.5 ft gap at x 42 (y 12–15.5). It has no header or casing, so it reads as a hole in the wall.

**Why it bothers him.**
- "Give the main threshold a taller header than the secondary doors" [FP2].
- Hierarchy of doors [FP1, FP7].
- Don't jam a narrow door in. He paired a 150 cm entry door with a sidelight [FP1].
- Cased openings between public and private zones [FP8].

**His change.** A three-step hierarchy:
1. **Main door.** 4'-0" (two 2'-0" leaves) at y 16.75–20.75 with an **8'-0" head**. Above it, a carved teak or jali transom in the gable wall, up to the 9'-0" transom line already used for vents (`TRANSOM_Z`). It is the only door on the house taller than 7 ft.
2. **Pooja door.** Keep it 3'-0" at 7'-0". Its carving makes it the special *inside* moment.
3. **Opening to the private wing at x 42.** A cased opening exactly the hall's width (y 11.5–15.67 after finding 2), with a 7'-0" teak-cased head matching the door heads. It is the clear public-to-private threshold.

Room doors: standardise on two widths, 2'-9" for bedrooms and the study and 2'-6" for baths and service.

**Trade-offs and knock-on effects.**
- A larger teak door and a local raised lintel over the main door. That is feasible: the gable ridge runs E–W over the door, so there is height there.
- The W17 vent head stays at 7 ft and so is no longer level with the door head. That's intended.

**Confidence: high** for the main door. Medium on standardising the room doors.

---

### 5. The ground master is a foot off the house's best line, x 21
**Severity: Significant**

**What he sees.** Upstairs, everything sits on **x 21**, the centre of the 14–28 bay:
- Bedroom 2: bed F71 (18–24), wardrobe F90 (17–25), windows W31/W37 symmetric at 16.2 / 25.8, fan at x 21.
- Study: sofa-bed F92 (18–24), bookshelf F95 (18–24), north window W34 (18–24), fan at x 21.

The ground master's windows are on it too: W04 north (18–24, centre 21) and W14 south (19.5–22.5, centre 21). The furniture is not:

- **Bed F10** at x 17–23, centre **20**. It is 1 ft west of both windows, the room centre (21.08) and the bed upstairs.
- **Divider wardrobe F06** at x 14.4–20.4, centre 17.4. It is supposed to back the bed ("headboard against the back of the divider wardrobe"), but it **stops 2.6 ft short of the bed's east side**. Only 3.4 ft of the 6 ft bed has anything behind it.
- **East bedside shelf** (`EXTRA_DRAW` F11 at x 23–24, y 14.7–15.7) is specified as "floating… wall-hung", but **there is no wall behind it**: the wardrobe ends at 20.4. It is a wall-hung shelf hanging in mid-air.
- **TV cabinet F23** with the TV above (west wall, y 6.9–12.3) **overlaps window W01** (y 10–13) by 2.3 ft. The TV hangs across half the window. The AC point at (14.4, 11.6) is also in the window. The wardrobe F06 (from y 12.6) covers the window's last 0.4 ft.
- **Day bed F20** (x 16.5–23, centre 19.75) sits under W14 (centre 21), 1.25 ft off.
- **Coffee table F66** has its centre at 18.65.

The master sleeping zone's fan (24, 20) is 3 ft off the bed axis.

**Why it bothers him.**
- Centre windows on beds and bays [FP1, FP3, FP4, FP5].
- Built-ins should be full and honest, not a wardrobe that half-backs a bed [DREAM, SA1].
- A wall-hung shelf with no wall is a drafting typo he'd call out in one breath with door swings [FP1].
- The TV over a window is a cousin of his TV-placed-as-an-afterthought complaint [FP5, IHATE].
- "It might seem like I'm obsessed with aligning things, but it really does elevate a space" [§3.12].

**His change.** Make **x 21 the bedroom axis through both floors**, and stack the ground divider directly under the upstairs wall.

- **Divider wardrobe F06**: 8 ft long at x 17–25, y 12.0–14.0.
  - Its back face sits on **y 14**, the upstairs Bedroom 2/study wall, the stage-1 beam line and the ridge line.
  - It sits directly under the upstairs wardrobe F90 (x 17–25, y 12.2–13.9), so the built-ins stack.
  - Passages stay open at both ends: 2.6 ft at the west and 2.8 ft at the east.
- **Bed F10**: x 18–24 with the head on y 14.0 (y 14.0–20.8). Bedside shelves at x 17–18 and 24–25, both now on the wardrobe's back. Fan to (21, 19.5), directly under the study fan.
- **Sitting zone** on the same axis:
  - day bed under W14 at x 17.75–24.25;
  - **TV in a 3 ft niche in the centre of the divider's south face** at x 21, facing the day bed, so the wardrobe becomes a media wall ("one built-in", [FP6, KJ]);
  - the 5 ft sofa F67 and the west TV cabinet F23 are dropped;
  - a reading chair goes by the west window.
- **West wall** is now free for the window (finding 7).

**Trade-offs and knock-on effects.**
- Wardrobe storage drops from 6 ft to about 5 ft (8 ft minus the 3 ft TV niche). Add the loft above to make it up.
- The TV now faces the high south window W14 (sill 5'-6"), so there is some glare risk. The jali on W14 helps, and the TV can be angled.
- The bed head still faces south, so the vastu preference is kept.
- The master door D02 (y 12.6–15.4) is centred on y 14.0, the divider's back face. You enter facing the divider's east end panel 3 ft inside (finding 6).

**Confidence: high** on the bed, the wardrobe, the floating shelf and the TV over the window. Medium on the TV-in-divider solution, which other reviewers may solve differently.

---

### 6. The house's spine at y ≈ 14 ends on a bedroom door
**Severity: Significant**

**What he sees.** There is a genuine 33 ft internal axis at roughly y 14, almost exactly the house centreline. The elements along it don't quite line up:

| Element | Extent (y) | Centre |
|---|---|---|
| Pooja door D11 | 13.0–16.0 | 14.5 (pooja clear centre 14.58) |
| Living-to-hall opening at x 42 | 12–15.5 | 13.75 |
| Stair hall | 12–15.67 | 13.835 |
| Master door D02 | 12.6–15.4 | 14.0 |

It's a 0.8 ft wobble overall. More important is what the axis *ends on*:
- From the living, and even from the pooja, you look down the hall straight at the master bedroom door.
- D02's hinge is at its south jamb (`HINGE_AT_END` is empty). When it's open, the leaf swings south-west and reveals the sleeping zone to the north.
- Today, past the door, the axis hits the end panel of wardrobe F06 at x 20.4.

Second, the stair-hall opening's north jamb (y 15.5, the start of wall Y 42) is 2 in short of the stair's first riser and the hall's north edge (15.67).

**Why it bothers him.**
- Punctuate the end of each axis with something worth seeing, never a private door [FP1, FP3, FP5, FP6].
- The first thing revealed should not be the private room [FP6, FP2].
- Private doors belong off a side hallway, with a stop for the eye at the end [FP7, FP4].
- Jambs should align with wall lines [FP1].

**His change.**
- **Rehang D02 on its north jamb** (y 15.4), so the open leaf screens the bed and the view goes to the sitting zone.
- With the divider moved to x 17–25 (finding 5), the hall axis lands on the **divider's east end panel at x 25, about 3 ft inside the door**. Make that panel the moment: a carved teak panel or a lit picture niche, like the lamp shelf at the top of the stair. It's what you see from the living down the hall.
- Set the hall opening at x 42 to **exactly the hall's width**: y 11.5–15.67 after finding 2. Start wall Y 42 at 15.67, flush with the first riser, and case it (finding 4).
- At the other end, the pooja is fixed by its walls (12.875–16.29). Accept its 7 in offset: it's a separate room and the casing on x 42 frames it.

**Confidence: medium-high.** He would love that the axis exists, then ask "what does it end on?"

---

### 7. West façade: windows chosen by furniture accidents, not a grid
**Severity: Moderate**

**What he sees.** On the west wall (A-202 west elevation) the windows are:

| Floor | Window | Extent (y) | Centre | Notes |
|---|---|---|---|---|
| Ground | W01 | 10–13 | 11.5 | |
| Ground | W13 | 21–23 | 22 | 2 ft wide |
| Upper | W36 | 10–13 | 11.5 | 3 ft, sill 5 |
| Upper | W41 | 21–23 | 22 | 2 ft wide |

They do stack, which is good: that came from the last review. But their positions relate to nothing:
- Bedroom 2's west wall is centred at 8.58; W36 is 3 ft off.
- The study's west wall is centred at 19.4; W41 is 2.6 ft off.
- The study desk F91 (y 16.4–20.4, centre 18.4) isn't under W41, and the opposite desk F93 (centre 21.2) doesn't share an axis with F91.
- On the ground floor, W01 is where the TV is (finding 5).

**Why it bothers him.**
- Windows centred on rooms and bays, then composed on the façade; not "randomly punched" [FP1, FP3, FP4, FP5, WORST].
- High windows over full-height or work walls [FP2, FP5].

**His change.** The 22 ft depth has quarter points at **y 8.5 / 14 / 19.5**, which is a 5.5 ft module. The ridge and the hip apex sit on y 14.
- Upper: W36 at y 7.0–10.0 (centre 8.5, on Bedroom 2's west wall). W41 widened to 3 ft at y 18.0–21.0 (centre 19.5, on the study's west wall).
- Ground, stacked: W01 at y 7.0–10.0 in the sitting zone. With the TV now in the divider, this wall is free. W13 at y 18.0–21.0 beside the bed. All four windows the same 3 ft width.
- Study desks: F91 and F93 both at y 17.5–21.5 (centre 19.5), facing across one axis, with F91 under W41's high sill. F93 stays clear of the D35 swing, which ends at y 17.2.
- AC points move off the window lines: Bedroom 2's to y 12, the master's to y 4.5.
- Result: two pairs symmetric about the hip apex, each window centred on the room behind it.

**Trade-offs and knock-on effects.** More west glazing on the upper floor: W41 goes from 2 ft to 3 ft. Keep the sills high and use jali (Guntur afternoon sun, [§6]). It's the rear façade behind the pergola, so it's cheap to do.

**Confidence: medium.**

---

### 8. Kitchen front on the road façade: roof, window and hob all on different lines
**Severity: Moderate**

**What he sees.** The kitchen's east wall (x 67) runs y 3–12.5, with its clear face centred at y 7.75. On it:
- **W08** at y 9.5–12.5 runs **4.5 in into the north wall** (inner face 12.125). It's a geometry error.
- W08's centre (11.0) is 3.25 ft north of the wall's centre.
- The chimney point CH is at y 7.5, 3 in off the wall centre.
- F35's text says the hob is "centred 7'-6" from the south wall face", which gives y 10.9, behind W08. That contradicts CH at 7.5. Fix the text.
- The wing roof (`ROOF["wing"]`, y 1–10.5) is centred at 5.75, **2 ft south** of the wall below it. The gable's south eave took y 10.5–12.5.
- Inside, the dining → hatch → kitchen axis is at y 10.0 (hatch W44 y 7.9–12.1, table F24 centre 10.2). It ends on the east wall 1 ft south of W08's centre.

On A-202 the laterite kitchen front reads lopsided: roof apex left of centre, window jammed against the poomukham.

**Why it bothers him.**
- Windows that relate to the room behind them [FP1, FP4].
- A cooktop with its hood centred on a wall makes a "very proper end" [KIT, FP4].
- This is the most-seen façade after the gable [WORST].

**His change.**
- Hob and hood centred at **y 7.75**, on solid wall.
- W08 at y 9.0–11.75 (2'-9", centre 10.4), 4½ in clear of the north wall face. That's within 5 in of the dining/hatch axis, so the view from the dining table through the hatch ends in daylight.
- Extend the **wing roof's north edge to y 12.5** (the wall line), tucked under the gable's south eave (see finding 9). Its apex moves to y 6.75, 1 ft off the wall centre rather than 2.

Alternatively, if the façade matters more to the owner than the interior axis, use two 2 ft windows symmetric about the hood at y 4.0–5.75 and 9.75–11.5.

**Confidence: medium.** He'd catch the window in the wall and the lopsided front. The fix is his "interior first, then compose".

---

### 9. The gable/wing valley runs over the kitchen ceiling, not over a wall
**Severity: Moderate**

**What he sees.** The gable's south eave and the wing's north edge meet at **y 10.5**. The valley gutter therefore runs 2 ft inside the kitchen, south of its north wall at y 12.5, above the fridge and pantry. The spec's own junction notes call the kitchen ceiling "the main leak risk".

**Why it bothers him.** "Tie roof pitch to the plan… so it feels structurally cohesive" [FP1]. A roof line that doesn't relate to any wall below is a leftover [FP4].

**His change.** Bring the wing to y 12.5 so the valley and its flashing sit on the y 12.5 wall and ring beam. The gable eave (from y 10.5) then oversails the wing's north slope by 2 ft, which is the classic stepped Kerala lap. The gable stays symmetric on y 18.75.

**Trade-offs and knock-on effects.** A slightly larger wing roof. The downpipe at (69, 10.5) moves to (69, 12.5). The leak risk is lower.

**Confidence: medium-low.** He's light on roof detailing but strong on "roofs relate to walls".

---

### 10. Doors jammed into corners, and jambs that relate to nothing
**Severity: Moderate**

**What he sees.** Returns (the wall between a jamb and the adjacent wall face):

| Door or opening | Return at the tight jamb | Problem |
|---|---|---|
| D07, master bath (x 28, y 18.4–20.9) | 1.3 in to the bath's south wall face (18.29) | jammed; WC F48 0.1 ft past the other jamb |
| D33, upper bath (x 36, y 8.8–11.2) | 1 in to the y 11.5 wall face (11.29) | jammed |
| D39, upper toilet (y 18, x 31.7–34.1) | 2 in to the x 34.5 wall face | jammed |
| D11, pooja (13.0–16.0 in 12.875–16.29) | 1.5 in south, 3.5 in north | unequal |
| W44, serving hatch (y 7.9–12.1) | 0.3 in north, 2.3 in south | corner to corner but not exactly |
| D04 small room and D02 master | 3.5 in and 4.7 in, both crowded into the lobby's SW corner | "a weird little room full of doors" [FP2] |
| D31, Bedroom 2 (y 11.5, x 29.5–32, centre 30.75) | | axis ends between W35 (centre 29.8) and wardrobe F76 (from 31.5) |

**Why it bothers him.**
- "Don't jam a door into a corner" [FP1].
- Doors that end on something [FP1].
- His professor story [§1].

**His change.** One rule: a jamb either has a **4½ in (0.375 ft) minimum return** for the architrave, or it sits flush with the wall face.
- **D07** → y 18.7–21.2. Move WC F48 north 0.3 ft. The upper WC F98 moves with it, so the stack is kept.
- **D33** → y 8.6–11.0.
- **D39** → x 31.4–33.8. While there, set **W42 (and W43 below) at x 31.9–33.9**, so the toilet door's axis ends on the window over the shower and not on tile.
- **D11** → y 13.08–16.08 (centred on 14.58).
- **W44** → exactly y 7.71–12.125 as a full-width cased opening, or 8.2–11.6 with equal returns. Either way, centred on the dining at 10.0.
- **x 30.0 line through both floors:**
  - D04 → x 28.75–31.25;
  - D31 → x 28.75–31.25 (6½ in return);
  - W35 → x 28.75–31.25;
  - W02 → x 28.5–31.5, sill 3 ft to match W35. Today W02 is 3 ft wide at sill 3.5 and W35 is 2.4 ft at sill 3, which is a stacked pair of different sizes.
  - The Bedroom 2 door then looks straight at its window, and the door and window stacks line up through both floors.

**Confidence: high** that he'd nitpick these. These are exactly the cheap fixes he loves.

---

### 11. Living west wall: four elements, three slivers of wall
**Severity: Moderate**

**What he sees.** Wall x 42, y 12.5–25, from south to north:

| Element | Extent (y) | Gap to the next element |
|---|---|---|
| Hall opening | 12–15.5 | 5 in pier |
| Stair jali W10 | 15.9–17.6 | 5 in pier |
| Lamp niche F59 | 18.0–19.8 | 6 in pier |
| TV unit F53 | 20.3–24.6 | 2 in to the north wall face |

Two other things are slightly off:
- The TV and sofa axes don't agree: TV centre 22.45, sofa F38 centre 22.1, coffee table F39 centre 22.2.
- The two armchairs F45/F46 (y 17.6–19.6) sit right on the door-to-niche axis.

**Why it bothers him.**
- Pick "the main character" of the wall [SA6].
- Leave resting walls between zones [SA3, SA2].
- "One built-in with the fireplace on one side and the TV on the other" [FP6, KJ]. Here the lamp niche is the hearth.

**His change.** Make the whole wall from y 15.67 to 24.79 **one teak built-in**: the stair jali, then the lit vilakku niche centred on y 18.75 in a framed panel, then a TV recess centred on y 22.3. The slivers become joinery stiles instead of leftover plaster.
- Sofa, coffee table and TV all on y 22.3.
- W09 nudged to x 44.75–50.75 (centre 47.75), the centre of the seating group.
- The armchairs are for the living reviewer. On alignment alone he'd want the door axis kept clear to the niche.

**Confidence: medium.**

---

### 12. Wet-room windows straddle the shower glass
**Severity: Moderate**

**What he sees.**
- **Common bath:** W03 (x 38.5–40.5) is split by the shower glass F18 at x 38.9–39.05, 0.4 ft from its west jamb.
- **Upper bath:** same again, with W33 and F79.
- **Master bath and upper toilet:** W43/W42 (x 30–32) sit half over the shower, which starts at x 31.5.

**Why it bothers him.** Partitions should land on mullions or wall lines, not cut through glass [FP1, FP4]. Light the shower deliberately [FP6, FP8].

**His change.**
- W03 and W33 → x 39.4–41.4, wholly over the shower, centred on it (shower centre 40.4).
- W42 and W43 → x 31.9–33.9 (finding 10).
- The upper and lower windows still stack.

**Side note for the bathroom reviewer:** WC F16/F77 projects to x 37.9, only 1 ft from the shower glass at 38.9.

**Confidence: medium.**

---

### Small tidy list (Moderate, all cheap)

**Stair**
- **W05** (stair window, x 36.5–40.5, centre 38.5) → x 36.25–40.25. That centres it on the stair, the hall and the core (38.25). This is his own anecdote: he moved one step so the windows centred on the stair [FP4].
- The stair foot axis (flight 1 descending, x 40.25) ends on the blank north wall of the common bath at y 11.5. Mirror the upstairs lamp shelf there: a small lit picture.

**Pillars and front plane**
- **Pillar line x 66.4**: the pillar faces sit about 7 in behind the kitchen front plane (outer face 67.375). Make them flush (centre at about 66.99) or clearly recessed by 1'-6" or more. As it is, it looks like an error.

**Upper landing**
- The axis from the terrace door (D36, centre 13.6, exactly the landing centre 13.585) ends on blank wall at x 28 between D31 and D35. Hang art there (x 28, y 12–14).
- D36 and the stair jali W40 already meet cleanly at y 15.0. Keep that.

**Sill heights**
- There are five today: 3, 3.5, 4.5, 5 and 5.5 ft. Cut to three (3, 3.5, 5): W14 and W17 → 5, W12 → 5.

**Pooja**
- **W17** (pooja vent, y 13.6–16.4, centre 15.0) → y 13.2–16.0. That centres it on the idol (14.58), not 5 in off behind the mandapam.

**Dining**
- **Dining table F24** (x 45.8–49.6) vs bench F28 (46.0–49.6): line the table up with the bench and the x 46 wall at x 46.0–49.8.
- Move the dining switch off the end of the table axis on the x 42 wall (42.4, 9.4). Hang art at (42, 10.0) to end the dining axis.

**Living**
- **Living fan** at (50, 18) relates to neither the room (51.5, 18.75) nor the seating group (47.75, 22.3). Move it to the group.

**Kitchen**
- **Tall kitchen storage** F36/F37 (x 58.4–62.9) stops 1'-11" past the x 61 slab and post line. With finding 1, end the pantry on x 61 (fridge at 56.5–59, pantry at 59–61). The x 61 column and edge beam then hide in its flank [FP1, FP2, KIT: tall storage aligned to an architectural line].
- Start the south counter run at x 56.1, the east jamb of the kitchen door D17. That leaves a clean 2'-10" service lane from D17 to the wet-area door.

---

## 3. The grid he would impose

**x (along the house).** Primary bays **14 | 28 | 42 | 53 | 67**: 14, 14, 11 and 14 ft.
- Secondary lines: 26 (small room), 34.5/36 (wet band), 46 (nook), 57 (pooja) and **61** (the edge of the two-storey slab, the poomukham wall, and the gable/wing line).
- Terrace posts on 53 and 61 only, each on a wall corner below (finding 1).

**y (across the house).**
- **Back block, both floors:** 3 | **11.5** | **14** | 25.
  - 11.5 is the single cross wall (finding 2).
  - 14 is the centreline: ridge, Bedroom 2/study wall, master divider back, master door centre.
- **Front block:** 3 | 7.5 | 12.5 | **18.75** | 25.
  - 18.75 is the entry axis: gate, tulsi, steps, pillars, door, lamp niche, gable ridge, terrace seating.

**Window module on the long façades.** The west and east façade quarter points are y 8.5 / 14 / 19.5. Side windows stack floor over floor at equal widths.

**Named axes**

| Axis | What sits on it |
|---|---|
| x 21 | The bedroom axis, both floors (finding 5) |
| x 30.0 | Small-room door, Bedroom 2 door, W02, W35 (finding 10) |
| x 38.25 | Stair, core, W05, common bath door D08 (already at 38.25) |
| x 44.0 | Dining nook axis |
| x 47.75 | Dining table, seating group, W09 |
| y 18.75 | Entry axis |
| y ≈ 14 | The spine |

---

## 4. Keep (what works)

**Hip roof**
- **Ridge on y 14**, which is exactly the house centreline and the upstairs Bedroom 2/study wall.
- **Hips pass over the corners**: (14, 3), (14, 25), and the terrace corner posts (61, 3) and (61, 25). The roof genuinely relates to the plan.

**Upstairs**
- **The upstairs x 21 axis.** Bed, wardrobe F90 (centred on the bed), symmetric windows W31/W37 (± 4.8 ft), sofa-bed, bookshelf, north window W34 and fans are all on one line. "It just feels very tidy and intentional."
- **The top of the stair:** flight 2's centre (x 36.25) lands exactly on the lamp shelf F80 (x 35.4–37.1, centre 36.25).
- **The terrace door D36** is centred on the landing (13.6 vs 13.585) and ends the landing axis in daylight.

**Stacks**
- **Window stacks:** W04 under W34, W43 under W42, W03 under W33, W02 under W35 (centre 29.8), W01 under W36, W13 under W41. W14 is centred between W31 and W37 on the south façade, a deliberate one-under-two rhythm.
- **Wet stacks:** both WCs (F16/F77 and F48/F98) and both shower glasses stack exactly. Walls x 28, 34.5, 36 and 42 and wall y 18 stack floor to floor.

**Small centrings that already work**
- **Dining nook:** W11, crockery unit F44 and the nook clear width are all centred on x 44.0.
- **Hatch W44** is centred on the dining zone (y 10.0).
- **Dining pendant** is centred on the table.
- **Living window W09** (centre 47.5) is centred on the dining-to-living N–S axis (table 47.7) and the seating group, not on the room. That's the right call.
- **Kitchen sink** is centred under W07. **Utility sink** is centred under W12.
- **Window heads** are all at 7'-0", a clean head line on every façade.
- **The front axis exists at all:** gate, tulsi, steps, door and lamp niche in one line. It only needs to be on the gable's line.
