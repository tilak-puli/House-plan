# Noah Daniel review: the outward look (massing, roofs, façades, arrival)

Sources checked: `99_Source/model.py` (ROOF, PILLARS, TERRACE_POSTS, RAILS_F1, JALI_RAILS, WINDOWS, WINDOWS_F1, DOORS, SITE_FEATURES, SPEC), drawing set pages 12 (roof plan A-110), 13 (N/S elevations A-201), 14 (E/W elevations A-202), 15 (sections A-301), 3 (site plan), and the 3D model's Front, Corner and North-side views (viewed only, not edited).

## 1. Noah's take

"Okay friends, I love the idea here, so let's say it first: a low, human-scale entry, a real verandah you sit in before you go inside, and a stepped Kerala roof. That's context, not a 'style', and I'm keeping all of it. But when I stand at the gate, the house reads as three things that were never introduced to each other. There's a sweet single-storey porch, then a dark two-storey void with skinny grey poles, then a huge clay roof floating on top like a carport canopy. Nothing upstairs lines up with anything downstairs: not the posts, not the gable, not the door. The long sides are a flat 53-foot plaster box, with every bit of the Kerala character spent on the road face. Most of this is fixed with a grid and one wrap-around roof line, not with a redesign. Does that make sense?"

## 2. Findings, most important first

### F1. Put the upper front on the same grid as the lower front: three posts, not four, on the ground-floor walls
- **Severity:** Major move
- **What he sees:**
  - The roof over the terrace sits on `TERRACE_POSTS` at x 61, y 3 / 10.3 / 17.7 / 25. That gives three equal bays of about 7.4 ft, centred on the house's middle line (y 14).
  - Everything below follows a different axis:
    - the front gable is centred on y 18.75 (`ROOF["gable"]` = y 10.5–27);
    - the main door D01 (y 17.6–20.6) is centred on y 19.1;
    - the kitchen/poomukham wall line is at y 12.5.
  - So the post at (61, 17.7) lands about 1 ft from the gable's peak and right over the door's south jamb (17.6). In the 3D Front view, that post runs straight down into the back of the mukhappu.
  - The post at (61, 10.3) stands mid-span on the slab edge over the kitchen, where there is no wall under it.
  - The gable ridge (+15'-10") rises only 4 in above the terrace railing top (+12' + 3'-6" = +15'-6"). The peak pokes into the railing band and reads as pasted on.
- **Why it bothers him:**
  - "Align with…", "a clean, thoughtful grid" [FP1, FP3, FP4].
  - Openings and structure on the façade must relate to what's above and below. A chaotic façade is one of his "five worst" [WORST].
  - The roof pitch and structure should tie to the plan so the house "feels structurally cohesive" [FP1].
- **His change:**
  - Front posts at **y 3, 12.5 and 25** on x 61. Delete the posts at 10.3 and 17.7.
    - The 12.5 ft bay (y 12.5–25) then frames the poomukham and its gable exactly, giving a vertical "post – gable – post" composition.
    - The 9.5 ft bay (y 3–12.5) frames the kitchen wing.
  - The post at (61, 12.5) lands on the corner where walls X 12.5 and Y 61 meet, which is a natural column position.
  - Use fewer, sturdier posts: about 150 × 150 mm SHS, or paired 100 mm sections, sized by the engineer. A heavy clay roof on 100 mm sticks looks like it floats.
  - Paint the steel a deep charcoal or teak-brown so it reads with the teak pillars below. It should be painted honest steel, not wood-look cladding [FAUX].
  - Side posts: move (51, 3) and (51, 25) to **x 53**.
    - (53, 3) sits on the junction of the kitchen/wet-area wall (Y 53) and the south wall. Today (51, 3) lands right above the wet-area window W12 (x 50.1–51.8).
    - On the north, the new 42–53 bay has its centre at x 47.5, which is exactly the centre of living window W09 (x 44.5–50.5). It lines up for free.
- **Trade-offs / knock-on effects:**
  - The steel eave beams span 12.5 ft and 9.5 ft instead of 7.4 ft, which is easy in steel. The engineer must confirm the beam and the cyclone uplift.
  - The corner post (61, 3) still sits over kitchen window W07 (x 58.5–64.5). Either split W07 into two windows of about 2'-9" either side of a column at x 61, or shift W07 west. Coordinate with the kitchen reviewer, because the prep sink F65 is centred under W07.
  - It also saves two posts and their RCC stubs.
  - Phasing is unchanged (stage 1).
- **Confidence:** high.

### F2. Wrap one low roof line round all four sides at the gable's eave level (+11'-1")
- **Severity:** Major move
- **What he sees:**
  - The north and south elevations (A-201) are one uninterrupted box, 53'-9" long, with a single eave line at +20'-10" and a hip ridge at +28'-4".
  - The only Kerala tiering is on the road face: the gable and kitchen wing eaves at +11'-1" (`geave` 11.085). That line stops dead at the front corners.
  - The 3D Corner view shows the south wall dotted with eleven separate little window hoods at different widths. The west wall (A-202) is a plain 22 ft two-storey gable-less face.
- **Why it bothers him:**
  - "Push and pull of masses": a flat box designed "about as thoughtfully as a unit in a large apartment complex" is a failure [FP1, FP6].
  - No performative façades. When all the interest is on the street face and the other three sides are flat boxes, the house is "about the people out there" [SUBURB].
  - He loves deep eaves [DREAM], and he wants regional forms used for the climate reasons that made them [STYLES].
- **His change:**
  - Add a **continuous tiled lean-to (the Kerala *chaipu*) at the ground-floor ring beam**, running round the north, south and west walls.
    - Its eave sits at **+11'-1"**, the same as the gable and wing eaves, so the front tier finally continues round the house.
    - It is 2'-0" deep on the south, 1'-6" on the north (the eave line stays at y ≈ 26.9, inside the 27 ft plot like the main roof's) and 2'-0" on the west. On the west it merges with the creeper pergola's head.
    - Use real clay tiles on steel brackets and purlins (or a sloped RCC chajja tiled as a working roof), with a gutter. It is a real roof doing a real job, not a decorative band.
  - Delete the individual window hoods it covers. Every ground-floor window head is already at FFL + 7 ft = +9'-0", so the lean-to sits about 2 ft above a common head line.
- **Trade-offs / knock-on effects:**
  - The monsoon run-off and splash on the ground-floor AAC walls and windows drop sharply, and the plinth stays drier on black cotton soil.
  - At 30° the 2 ft lean-to rises about 1'-2", so it meets the wall at about +12'-3". The upper sills are at +15'-0" (FFL1 + 3 ft), so it stays clear of them.
  - The north eave at y ≈ 26.9 sits over the 2 ft walkway at 11 ft high, so the walkway stays usable.
  - Rough cost: about 125 running ft of lean-to, roughly Rs 1.5–2.5 lakh. It could slip to stage 2, but the brackets and the cast-in plates belong in the stage-1 ring beam.
  - Adds about 3 more gutter runs and downpipes.
- **Confidence:** medium-high. He hasn't used the word *chaipu*, but "lower the roof over single-storey bump-outs" and "deep eaves" are exactly his moves.

### F3. The entry axis is 4 inches out, and the pillar bays are lopsided
- **Severity:** Significant
- **What he sees:**
  - `ROOF["gable"]` is centred on **y 18.75**, but nearly everything on the arrival line is centred on **y 19.1**:
    - the main door D01 (17.6–20.6);
    - the gate (15.6–22.6);
    - the forecourt path (16.1–22.1);
    - the tulsi thara (72.4, 19.1);
    - the steps (17.3–20.9).
  - The model comments and the 25th review both claim "centred under the front gable", but they are 0.35 ft (about 4 in) apart.
  - The poomukham pillars are at y 13.1 / 16.4 / 21.8 / 24.4, giving bays of **3.3 / 5.4 / 2.6 ft**. The outer pair is centred on 18.75 and the inner pair on 19.1.
  - So the two charupadi bays differ by 8 in, right under the gable's symmetric face.
- **Why it bothers him:** this is the professor-and-the-misaligned-door story. "I've never knowingly misaligned anything since" [Principles §1, FP4]. The main threshold is "the main character" of this façade, and a symmetric gable over an off-centre door and uneven pillars undercuts it.
- **His change:** put everything on **y 18.75**:
  - D01 at 17.25–20.25, or widen it per F7;
  - steps 16.95–20.55, gate 15.25–22.25, path 15.75–21.75, tulsi at (72.4, 18.75);
  - pillars at **13.1 / 16.05 / 21.45 / 24.4**, giving bays of 2.95 / 5.4 / 2.95.
  - The charupadi F42 and F69 then fit the two equal side bays.
- **Trade-offs / knock-on effects:**
  - Inside, the door moves 4 in south, towards the pooja wall X 16.5 (the jamb stays 0.75 ft or more clear of it).
  - The axis to the lamp niche F59 (y 18.0–19.8, centre 18.9) stays essentially on line.
  - No structural or vastu effect.
- **Confidence:** high.

### F4. The laterite kitchen front is a veneer from the wrong region: build that wing honestly or let it be plaster
- **Severity:** Significant
- **What he sees:**
  - The 31st review clads the kitchen's road face (wall Y 67, y 3–12.5) in exposed laterite over AAC. The cladding stops at the corner: the same wing's south face (x 61–67 on X 3) is plaster (A-201 south elevation).
  - Laterite is a Kerala/Konkan stone and isn't local to Guntur.
  - The two-wheeler bay (x 68–74, y 3–11) parks scooters directly in front of this feature wall.
  - The panel's composition has three different centres:
    - the wing's hip peak at y 5.75 (wing y 1–10.5);
    - the wall panel at y 7.75;
    - W08 at y 11.0 (9.5–12.5), jammed against the first pillar at y 13.1.
- **Why it bothers him:**
  - "If a material pretends to be something else, the design starts from a bad place". Cladding that stops at a corner is "set design energy" [FAUX, MAT].
  - Stone cladding is only justified when it relates to an interior function [FP4, FP6].
  - Use local materials scaled to the hand [INSP1, INSP3]. Context over style [STYLES].
  - Windows "randomly punched" [FP1, WORST].
- **His change:**
  - Make the kitchen wing a **real masonry volume**. Build its two exposed walls (east y 3–12.5 and south x 61–67) as exposed **local wire-cut or hand-moulded brick** infill in the RCC frame, wrapped round the corner up to the wing eave. If the owner truly loves laterite, use solid laterite block walls rather than tiles.
  - Then the "kitchen is its own lower pavilion" story is told by the material on every face.
  - Use local rough granite (Chimakurthy or Ongole) for the plinth face and the charupadi bases, rather than another imported stone.
  - Ask what the owner loves about laterite (warm, rough, red) and find that quality locally [FAUX].
  - Move the scooter bay so the wall isn't hidden behind it (see F8).
  - On W08: if the hob must stay on the solid east wall (vastu), keep W08 at the north end but make it deliberate. Give it the same head and frame depth as the door and the pooja vent W17, so it reads as part of the poomukham's opening rhythm rather than a stray hole.
- **Trade-offs / knock-on effects:**
  - A 9 in brick wall has more thermal mass and less insulation than AAC. It faces east only, under a 2 ft eave, so the extra morning heat in the kitchen is small.
  - Brick needs a water-repellent sealer and good eaves for the monsoon.
  - The cost is about the same as laterite cladding.
- **Confidence:** high on the veneer point, medium on brick as the answer.

### F5. Close the road side of the terrace like the other two sides, and make it look finished from stage 1
- **Severity:** Significant
- **What he sees:**
  - The terrace has closed teak jali parapets on the north and south (`JALI_RAILS`), but the road side (`RAILS_F1` Y 61, 3–25) is an open baluster railing 12 ft above the forecourt, facing the street.
  - In stage 1 the whole upper floor is "an open covered deck with temporary railings". For one to two years the house reads from the road as a ground floor with a big roof on poles over it, which is the familiar "unfinished building" look.
  - The gable's back triangle above the railing is left to a site detail.
- **Why it bothers him:**
  - On a city-facing balcony, open balusters mean "people can see your ankles": use solid railings unless there's a rural view [WORST].
  - The terrace is the family's evening room. It should feel anchored, not exposed.
- **His change:**
  - A 3'-6" parapet on the road side: a **2'-0" solid plastered upstand with a 1'-6" teak jali over it, and a teak cap**, matching the side jalis. It runs the full 3–25 and meets the gable triangle's jali cleanly.
  - Seated on the diwan, your eye level is about 3'-6" above the floor, which is about +15'-6". That is just above the parapet, so the morning view of the street and sky stays open.
  - Put the permanent side and front parapets in stage 1 (they are part of the roof/terrace package anyway) so there are no "temporary railings" on the face.
  - For the morning sun on this east face, keep the spec's bamboo chiks hung from the eave beam.
- **Trade-offs / knock-on effects:**
  - It adds the cost of about 22 running ft of parapet. That moves to stage 1, offset by not building temporary railings.
  - The planter boxes F89 can sit on the upstand.
- **Confidence:** medium-high.

### F6. Side-façade windows: stack them, standardise them, and stop posts landing on openings
- **Severity:** Moderate
- **What he sees:**
  - **North:** W04/W34 (both x 18–24) and W43/W42 (both x 30–32) are stacked perfectly. Lovely.
  - **South, west half:** composed. The upper W31 (14.9–17.5) and W37 (24.5–27.1) are symmetric about the bed axis x 21, over the single W14 (19.5–22.5) centred on it.
  - **South, east half:** a scatter:
    - openings at W35 2'-5" wide, W03 2 ft, W11 3 ft, D18, W12 1'-8", W07 6 ft;
    - sills at 3, 3.5, 4.5, 5 and 5.5 ft;
    - W35 (28.6–31.0) is 7 in narrower than the W02 below it (28.3–31.3), although both are centred on x 29.8;
    - the posts at x 51 and 61 land over W12 and W07.
  - **Upper east face, seen from the road through the terrace (wall Y 42):** D36 (y 12.2–15.0) and the stair jali W40 (15.0–24.5) form one opening band off the centre line.
- **Why it bothers him:**
  - "Place windows for the interior, then make them compose on the façade" [FP1, FP3, FP4, FP5].
  - No chaotic façades [WORST].
- **His change:**
  - Make W35 3 ft (28.3–31.3) to match W02 exactly.
  - Bring the service-side windows to two widths, 2 ft for baths and vents and 3 ft for rooms, and two sill heights: 3'-6" for rooms and 5'-0" for baths, vents and the wet area. That means W12 at sill 5'-0", 2 ft wide.
  - Move the posts per F1.
  - Treat D36 + W40 on wall Y 42 as one teak-framed composition with a shared head at 8 ft. It is the "upper façade" you see from the gate.
- **Trade-offs / knock-on effects:** W12 sits over the utility sink, and a 5 ft sill is still fine over a counter. No vastu or structural effect.
- **Confidence:** medium-high.

### F7. Door hierarchy: make the main door read as the main door
- **Severity:** Moderate
- **What he sees:**
  - D01 is a teak double leaf only 3'-0" wide, with its head at 7 ft, the same as every inner door (`LEVELS["door_head"]` 7.0).
  - The poomukham ceiling is the exposed gable rafters. At the door line (x 61, y 18.75) there is about 14 ft of height under the ridge.
  - The service door D18 is on the south walkway, out of sight of the road. Good: one gateway.
- **Why it bothers him:**
  - Give the main threshold a taller header than the secondary doors [FP2].
  - Keep one clear front door, with service doors away from the front [DREAM, FP7].
- **His change:**
  - Widen D01 to **3'-6" (y 17.0–20.5, centred on 18.75)**.
  - Give it a full-height teak frame to about 8'-9" above the poomukham floor, with a carved teak jali transom above the leaves. The RCC lintel band stays behind the frame head, and the jali ventilates the living.
- **Trade-offs / knock-on effects:**
  - The south leaf opens beside the pooja's north wall (X 16.5). Check the leaf clears the pooja door D11's swing zone; the jamb stays 0.5 ft from the wall.
  - Festival crowds and furniture deliveries are easier.
- **Confidence:** medium.

### F8. Forecourt and gate: the scooter can't turn, and the road wall shouldn't be precast panels
- **Severity:** Moderate
- **What he sees:**
  - The only gate (y 15.6–22.6) leads into a 6 ft deep forecourt (x 69–75).
  - The tulsi thara (r 0.6 at x 72.4) leaves about 2 ft between its edge and the gate line, and about 2'-10" between it and the steps.
  - The two-wheeler bay (x 68–74, y 3–11) is reached across the axis, so a scooter has to turn 90° in about 2 ft.
  - The compound wall is 5 ft precast RCC post-and-panel all round, including the road face.
- **Why it bothers him:**
  - The arrival should be calm. The axis gate → tulsi → steps → door → lamp niche is a great "punctuate the end of this axis" moment [FP1, FP3], and bikes shouldn't cut across it.
  - Hardscape and boundaries should be honest, local and hand-scaled. Builder-grade panels facing the street undo the gable's craft [INSP3, DREAM].
- **His change:**
  - Add a **separate 4 ft vehicle gate at y 4–8** straight into the bay. The 7 ft main gate stays a pedestrian and festival gate on the axis.
  - On the **road face only**, build the compound wall in the same local brick or rough granite as F4, with a teak or simple MS gate. Keep the thin precast panels on the north and south runs, where width matters.
  - Size the tulsi thara at about 2 ft square and 3 ft high. It then partly screens the view from the gate through the open door into the living without blocking the axis.
- **Trade-offs / knock-on effects:**
  - The road-face wall is about 27 ft of masonry instead of panels, a small cost increase.
  - The vehicle gate needs one more pair of posts.
  - The sump hedge and meter position are unaffected.
- **Confidence:** medium.

### F9. Screen the poomukham's north side, which faces a wall 2 ft away
- **Severity:** Moderate
- **What he sees:**
  - The poomukham is open on the north between pillars at (61.6, 24.4), (63.5, 24.4) and (66.4, 24.4).
  - The swing F41 (y 21.9–23.4) hangs 1 ft from that edge.
  - Beyond is the 2 ft walkway and the neighbour's side.
- **Why it bothers him:**
  - Frame views rather than opening everything up [FP2, FP5].
  - When there's a close neighbour, give privacy and an edge, so the sitting spot "has a home" [FP1, FP8].
- **His change:**
  - Between those pillars, add a laterite-or-brick charupadi-height wall (about 1'-6") with a full-height teak jali above. It makes a backdrop for the swing, lets the breeze through, and keeps out dust and the neighbour's view.
- **Trade-offs / knock-on effects:** a little less light on the swing, and a small cost. The north side gains the same detail language as the terrace parapet above it.
- **Confidence:** medium.

### F10. The gable face should be timber and air, not plaster with three holes
- **Severity:** Moderate
- **What he sees:**
  - On A-202 the mukhappu triangle is a plastered infill with three small jali vents (`OTHER_OPENINGS` GV1-3).
  - It has carved barge boards and a kalasham finial (31st review).
- **Why it bothers him:**
  - Ornament should be real and doing a job [Principles §1, MOD].
  - The Kerala mukhappu is traditionally a timber-panelled, ventilating face.
  - A plaster triangle with stuck-on carving drifts toward "Disneyland" [FAUX].
- **His change:**
  - Make the whole gable infill above the tie beam a **teak frame with jali panels** (insect mesh behind). It is real ventilation for the hot roof space over the verandah.
  - Keep the barge boards and the finial; they are culturally authentic.
- **Trade-offs / knock-on effects:**
  - It is open to driving rain, so the poomukham ceiling board needs a drip and a membrane above it.
  - Teak cost goes up modestly.
- **Confidence:** medium.

### Big moves considered and rejected (he'd say why on camera)
- **Moving the terrace to the back (west).** No. On the east, the two-storey block shades the terrace from about 1 pm, and it gets morning use and the street life. On the west it would cook in the 45 °C afternoon sun.
  - Putting the upper rooms over the living and kitchen would also break both wet stacks (x 36–42 and x 28–34.5) and put a bath over the kitchen.
  - The road face would become a flat two-storey wall behind a tiny gable, which is a worse "box".
- **A Kerala gablet (mukhappu) on the main hip's east end.** Tempting for ventilation. But it has to sit on the ridge axis (y 14), 4'-9" off the entry gable's axis (y 18.75), and two gables offset like that would look accidental. Fix the grid (F1) instead.
- **One lean-to roof across the whole front.** At 30° over 8 ft it reaches about +15'-8" at x 61, right at the seated eye level on the terrace. It kills the terrace's outlook.
- **Splitting the main roof into a lower tier over the terrace.** The terrace needs about 7 ft clear at its eave (+19'), so the step would be only about 1'-10". That isn't enough to read, and it adds a leak line.
- **A courtyard (nadumuttam).** He'd love one, but a 22 ft wide house can't lose a bay without losing a room. The covered terrace already does the job of an outdoor room.

## 3. Keep
- **The stepped-roof concept** and the low, single-storey entry tier: human scale at the door [FP1, FP6].
- **The poomukham as an entry room**, with swing, charupadi seats, shoes off and a step down. It's a genkan with a Kerala accent [3.1].
- **The arrival axis**: gate → tulsi → steps → door → lit lamp niche F59. It punctuates the axis beautifully once it is put on one line (F3).
- **One gateway.** The service door D18 is on the south walkway, invisible from the road [DREAM, FP7].
- **The terrace on the east,** in the house's own afternoon shadow. The closed teak jali parapets on the neighbour sides are the right call [WORST].
- **The north elevation's stacking** (W04/W34 and W43/W42), the symmetric Bedroom 2 / master window group on the south, and the common 7 ft head line everywhere.
- **The west face:** small high windows stacked (W01/W36 at y 10–13, W13/W41 at y 21–23) and a creeper pergola instead of glass to the afternoon sun.
- **The roof details:** 2 ft eaves with gutters all round, clipped tiles for the cyclone, and a stone-faced plinth splash zone (functional cladding is honest).
