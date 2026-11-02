# Noah Daniel review: the layout ("wipe it clean and zoom out")

Reviewer aspect: big organisation only. All coordinates are from `99_Source/model.py` (ft; x west→east/road, y south→north). Renders used: A-104 / A-105 furniture plans (pages 6, 7).

---

## 1. Noah's take

"Okay friends, it's floor plan time, and honestly the bones of this one are really good. Public at the front, private at the back, the stair right on the hinge between them, the master on the main level, two tidy wet stacks, and that entry axis from the gate past the tulsi, through the door, to a lit lamp niche: *chef's kiss*, I'm keeping all of that. What's bugging me when I zoom out is that the plan spends its best real estate on the wrong things: a 22 ft master doing three jobs while the dining, the heart of an Indian home, is a 5 ft strip with no daylight; shoes and a shoe bench sitting in the north-east corner where the pooja wants to be; and a lovely private back garden the house literally turns its back on. Also, can you see it already? The stair turns the wrong way for the owner's own vastu brief. None of this needs a new house. It needs about four confident moves inside the same grid."

---

## 2. Findings, most important first

### 2.1 The dining is a corridor, not a room (and it's the darkest place in the house)
- **Severity:** Major move
- **What he sees:** Dining R10 is 42–53 × 7.5–12.5, i.e. **11 × 5 ft**, with a 3'-9" × 2'-6" four-seat table F24. Its only daylight is borrowed from the 4 × 4.5 nook R12 (W11, 3 ft, south) and the kitchen hatch W44. It is boxed between the wet-area wall (y 7.5) and the living path. The plan centre of gravity (where the family actually eats, every day and at festivals) has the least light and the least floor.
- **Why it bothers him:** The open plan needs a strong centre, "a central table under a pendant" [FP6, FP1]; dining should be a rectangle you centre on something [FP1, FP3, FP5]; no formal dining, but a *big table that expands* for gatherings [FP6, DREAM; section 6 says this transfers strongly to Indian hosting]; daylight from two sides [FP2].
- **His change:**
  1. **A light well over the table.** Cut a ~6 × 4'-6" void in the first-floor slab at **x 45.5–51, y 8–12.5**, centred on the table, opening onto the covered terrace R37 above (which is under the main roof, so no rain falls in). The east edge at x 51 lines up with the terrace posts at (51, 3) and (51, 25). Jali railing upstairs, 6 in upstand so terrace water can't run in. The bright terrace floor bounces light down; hot air from the dining and living rises out through the terrace's open sides (stack effect — great in Guntur). Optionally a few glass tiles in the roof, but only if they are shaded; this is the south slope.
  2. **A bigger table that grows into the living.** 4'-6" × 2'-6" table at x 46–50.5, y 8.85–11.35. The bench F28 is extended to 4'-6" along the wet-area wall; two chairs on the north side (y 11.4–12.9) and one at each end (east chair stops at x 52, clear of the serving ledge F33). That seats 6–7, leaving ~4'-8" of path north of the chairs before the armchairs at y 17.6. At festivals it slides north into the living with a leaf.
- **Trade-offs:** about 27 sq ft of terrace is lost (the terrace stays about 390 sq ft). A future living AC needs a closable lid at the void (a sliding glazed or teak-louvre panel at the soffit). Two short edge beams in the stage-1 slab; less concrete overall. **Vastu:** an opening to the sky near the centre is positive. The trial-plot centre is (43, 13.5), so this void sits just south-east of it. **Phasing:** must be cast in stage 1 (structure is never deferred); temporary railing as already planned for the deck.
- **Confidence:** high (dining as the heart + light from above are his core moves; he will mention the courtyard instinct here).

### 2.2 The stair turns anticlockwise, against the owner's own vastu brief
- **Severity:** Significant (cheap to fix now, impossible later)
- **What he sees:** `STAIR`: flight 1 is x 38.5–42 rising **north** from y 15.67; half landing at the north end; flight 2 is x 34.5–38 rising **south**. Going up you turn **left** (north → west → south): anticlockwise. `RAILS_F1` ("X", 15.67, 38, 42) confirms flight 2 arrives on the west side. OPEN_ISSUES says "stair … rising clockwise".
- **Why it bothers him:** He'd say up front that this isn't his rule. It is the client's brief, and "most constraints in a new build are self-imposed, so question everything *early*" [FP2, FP1]. Since the brief insists on it, the drawing should honour it.
- **His change:** **Mirror the flights in the same 7'-6" × 9'-4" box.** Flight 1 becomes x 34.5–38 rising north from y 15.67; landing x 34.5–42 × 21.5–25 (unchanged); flight 2 becomes x 38.5–42 rising south and arrives at x 38.5–42, y 15.67, right beside the terrace door D36. Same 16 × 7.5 in risers, 10 in treads, 3'-6" flights. Move the well rail to x 34.5–38, the lamp shelf F80 to x 39.5–41 on the y 11.5 wall (it stays the wall you face at the top), and the under-stair cupboard F57 to x 38.5–42 × 18.6–21.3. The open, full-headroom part under the upper flight is then behind the jali W10, so W10 shows that space instead of the stair foot.
- **Trade-offs:** None in area. The foot of the stair moves 4 ft west, closer to the lobby, which actually suits a private stair [FP8]. Coming down you still face the common bath door D08 (x 37–39.5) at an angle; consider sliding D08 east by 1 ft. Vastu consultant should still sign off on the stair being this near the centre.
- **Confidence:** high that he'd flag it once spotted; medium that he'd spot it himself (vastu isn't his language).

### 2.3 The entry has no genkan; shoes sit in the north-east and the pooja is pushed against the kitchen
- **Severity:** Major move (small in cost)
- **What he sees:** The main door D01 (x 61, y 17.6–20.6) opens straight into the living. The shoe bench F52 is *inside* the living, in its **north-east corner** (59.4–60.6 × 21.2–24.4). The pooja R11 is in the living's south-east corner (57–61 × 12.5–16.5), sharing its wall with the kitchen.
- **Why it bothers him:** No blunt outside-to-living transitions; "the entry should be a room, not a hallway"; a shoes-off genkan, ideally sunken, with a different floor [FP1, FP2, DREAM]. The main threshold needs hierarchy [FP2]. The kitchen should be close to the entry [DREAM, FP8, FP2]. He'd also clock the vastu point: NE is the one corner the brief wants for the pooja, and right now it's the shoe corner.
- **His change: swap them and make a foyer between them.**
  - **Pooja → NE**, at 57–61 × 21–25. Door on its west wall (x 57, y 21.5–24.5), mandapam on the east wall, so the idols face west and the family faces east, as briefed.
  - **Old pooja box → shoe alcove**, at 57–61 × 12.5–16.5. Open its north side to the foyer and close its west side. The old pooja vent W17 now ventilates the shoes.
  - **Genkan foyer**, at **57–61 × 16.5–21** (4 × 4.5 ft), between the two masses and centred on the door axis (y 19.1). Its floor is flamed granite at the poomukham level (+1'-6"), one 6 in step up into the living through a 4'-6" framed opening on x 57: "cased opening, say it with me".
  - The kitchen sliding door D17 (x 53.6–56.1) is now two steps from the genkan, so groceries never cross the sofa group.
- **Trade-offs:** The living's usable box becomes 42–57 × 12.5–25 (15 × 12.5). That is no real loss, since the pooja and shoe bench already took that band. The pooja now abuts the poomukham swing wall (fine). **Vastu:** pooja in the NE (better), off the kitchen wall (better), and no shoes in the NE (better). **Phasing:** same wall length, moved; stage 1, cost-neutral.
- **Confidence:** high.

### 2.4 The master is a 22 ft room doing three jobs, and the bed actually sits in the north-west
- **Severity:** Major move
- **What he sees:**
  - Master R01 is 14–28 × 3–25: a sleeping zone north (bed F10 at y 14.7–21.3, with a 6 ft divider wardrobe F06) and a sitting/TV zone south (day bed F20, sofa F67, TV F23).
  - The door D02 (x 28, y 12.6–15.4) lands mid-room between the two zones.
  - Its bath R07 is in the NW. The "SW master" therefore actually sleeps in the NW, which the open-issue text admits.
  - Meanwhile the small room R03 is 10 × 9 with a bed and a 3 ft wardrobe, and has to use the common bath.
- **Why it bothers him:**
  - "When a bedroom is well over double the length of a bed, there should be a really good reason" [FP2, FP5].
  - Is the sitting zone on the wish list or legacy thinking [review step 4]? A second TV lounge beside a living 10 ft away is a duplicate.
  - The primary suite wants a **vestibule** connecting bed, bath and closet [FP2, FP4, FP8]; wardrobes on the shared wall as a buffer [FP5].
  - The office/guest room should be able to become a real bedroom [FP1, FP3, FP8], and an "away room" (den) is "so crucial" [DREAM, FP5].
- **His change (Alternative B below):** re-split the west bay at **y 14** (the line of the upstairs Bedroom 2 / study wall, so beams and walls stack).
  - **Master** in the true SW, 14–28 × 3–14: king bed head south between two windows stacked under W31 and W37, and an 8 ft sliding wardrobe on the y 14 wall stacked under F90.
  - **Guest room / den** in the NW, 14–28 × 14–25, which keeps the existing bath R07 and door D07.
  - **Master vestibule and bath** where the small room was.
- **Trade-offs:** The owner loses the private sitting zone (the den/guest room takes that job) and gains a second en-suite. One extra bath on the ground floor. The master bath moves to the south band (vastu consultant to confirm; see Alternative B).
- **Confidence:** medium-high. He always questions sitting areas in bedrooms, but the owner asked for one, and he'd present this as "here's what I'd do, and here's what you give up".

### 2.5 The house turns its back on its only private garden
- **Severity:** Significant
- **What he sees:** Behind the house there are 14 ft of the owner's own land (the 3 ft gap at x 11–14 plus the spare 11 ft at x 0–11). It is the quietest, most private outdoor space on the site, yet no door leads to it. The septic tank sits in its SW corner (x 1–5, y 1.5–7.5), right behind the master, and you reach the garden only down a 3 ft side walkway. The master's west wall has W01 (3 ft) and a high vent W13.
- **Why it bothers him:** Courtyards are his favourite feature, and he loves "Eichler privacy": walled courtyards rather than showy fronts [FP7, DREAM, SUBURB]. The primary suite should connect privately to the outdoors [FP2, FP5, FP7, DREAM]. A house should blur inside and outside with shaded edges [DREAM, FP8, FP2].
- **His change:** Make the back land a **walled garden court**: a 6 ft jali-topped wall on the west boundary and returns, with planting in the ground, not pots [FP7].
  - Move the **septic tank and soak pit to the NW of the spare land** (around x 1–5, y 19–25) and keep the SW as garden and drying yard.
  - Turn W01 into a **3 ft door with a grille shutter at x 14, y 10–13** (stacked under the upstairs W36) onto a stone *otta* (a raised sit-out) under the existing creeper pergola. This is the evening sit-out the plan doesn't have.
- **Trade-offs:**
  - West sun: the pergola and 2 ft eaves handle it, and it's used after sunset.
  - Security: a grille door.
  - **Vastu:** a door in the SW room's west wall may be queried. The fallback is to put the garden door on the NW guest/den room (x 14, y 15–18), which is vastu-fine.
  - Septic in the NW is the vastu-preferred spot; SW is the classic "no". Drain runs from the south stack get ~20 ft longer, with one more inspection chamber.
  - **Phasing:** stage 1; about Rs 20–40k plus the wall later.
- **Confidence:** high.

### 2.6 The living is the hallway for the whole house
- **Severity:** Moderate (Alternatives A/B tame it; it can't be removed in a 22 ft house)
- **What he sees:** From D01 to the stair hall R09 (x 34.5–42, y 12–15.67), every trip to the bedrooms, common bath, stair and dining runs along the living's south band, y 12.5–17.6. It also passes the kitchen door and the pooja. That's ~19 × 5 ft, about 40 % of the living, used as path.
- **Why it bothers him:** "A lot of path, not room"; a comfortable room needs at least one cul-de-sac corner [FP4, FP3].
- **His change:** Accept it, but *design* it as a gallery: a floor-material strip (Kota stone) and a beam or soffit line at y 17.6, with the armchairs as the soft edge (already there, F45/F46; "two armchairs make a softer boundary than a sofa back" [SA4]). The seating group in the NW corner of the living *is* a cul-de-sac, so praise that. The genkan (2.3) takes the shoe traffic out of the room, and the light well (2.1) makes the path a lit gallery rather than a dark edge [FP7, DREAM].
- **Confidence:** medium.

### 2.7 Front yard 8 ft vs back 14 ft: the balance is self-imposed
- **Severity:** Moderate (conditional)
- **What he sees:**
  - The front yard (x 67–75) carries the steps, forecourt, tulsi, two-wheeler bay (68–74 × 3–11), sump and gate.
  - A two-storey gable is seen from only 8 ft.
  - OPEN_ISSUES flags that a two-storey building may need a bigger front setback.
- **Why it bothers him:** "Most constraints in a new build are self-imposed" [FP2]. The 64 ft trial line is a test, not a law.
- **His change:** If the setback rule demands it, **slide the whole house 3 ft west** (x 11–64), giving an 11 ft front yard and keeping 11 ft of walled garden behind it (the spare land and the old gap combined). If the rule allows 8 ft, keep it, and put the effort into the back court (2.5), which is the private space.
- **Trade-offs:** The back garden drops from 14 to 11 ft deep, and the septic tank must stay ≥ 5 ft from the house. **Vastu:** more open space to the east is positive. **Phasing:** none.
- **Confidence:** medium.

### 2.8 Courtyard: why not a real open-to-sky nadumuttam?
- **Severity:** Moderate (his heart says yes; the roof says no)
- **What he sees:** One hipped roof covers x 12–63 with its ridge along y 14. Any court inside the 22 ft width is under the roof, and an open court would mean a hole in the tiles at or across the ridge, plus a cyclone and monsoon drainage problem. The history shows a courtyard was already tried and removed in the single-storey scheme.
- **His position:** He'd push for the *light well through the covered terrace* (2.1) as "the nadumuttam this house can afford", and for the *walled back garden* (2.5) as the real courtyard. A raised lantern over the void would also work, but it reverses the decision to drop the ridge ventilator, so he'd mention it only as an upgrade.
- **Confidence:** high that he'd raise courtyards; medium on this exact conclusion.

### 2.9 Covered terrace: keep it at the front
- **Severity:** Moderate (a decision, not a change)
- **What he sees:** R37 is 42–61 × 3–25, over the living and kitchen, under the main roof. It has jali parapets N/S, an open railing to the road, and the diwan lounge against the stair wall at the west (private) side.
- **His read:** He tested flipping it (Alternative C) and keeps it. It shades the living slab, it is vastu-correct (light and open in the NE/E, built mass in the SW), it keeps the stepped Kerala roof, and the lounge already sits on the private side away from the road [FP2, FP5 terrace zoning]. One ask: zone it explicitly as lounge north, drying south, with the light-well railing between them. That is already almost true.
- **Confidence:** medium-high.

### 2.10 Wet stacks: good; keep them
- **What he sees:** Two stacks: south (common bath R08 36–42 × 3–12 under Bedroom 2 bath R33) and north (master bath R07 28–34.5 × 18–25 under the upper toilet R39). The kitchen and wet area chain to an outside service door D18 [FP6, FP1 chain the service rooms]. No bath sits over a living room. All alternatives below keep both stacks.

---

## 3. Alternative arrangements

Room rectangles are x1–x2 × y1–y2. Clear sizes assume 9 in outer walls, 5 in inner and 7 in wet walls on centre lines.

### Alternative A: "Same bones, a real centre" (front half only)

```
x: 14            28     34.5   42     46  51  53      57   61    67
   ┌─────────────┬───────┬──────┬────────────────────┬────┬─────┐ y25
   │ Master      │M.bath │Stair │  LIVING (seating)  │POOJA│     │
   │ (as now)    │       │mirror│  sofa / armchairs  ├────┤POOM-│
   │             ├───────┤  ed  │                    │GEN-│UKHAM│◄ D01
   │             │ Lobby ├──────┤  ── gallery ──     │KAN │     │
   │             │       │S.hall│                    ├────┤     │
   │             ├───┬───┴──┬───┤ DINING  [void ]    │shoe│     │ y12.5
   │             │Sm.│C.bath│nk │ table 6 [above]    ├────┴─────┤
   │             │rm │      │   ├─────────┬──────────┤ KITCHEN  │
   └─────────────┴───┴──────┴───┴─ wet ───┴──────────┴──────────┘ y3
```

| Change | Rectangle |
|---|---|
| Pooja (NE) | 57–61 × 21–25, door on x 57 |
| Genkan foyer | 57–61 × 16.5–21, at poomukham level, step up at x 57 |
| Shoe alcove | 57–61 × 12.5–16.5 (the old pooja box) |
| Living | 42–57 × 12.5–25 (15 × 12.5, ~14'-6" × 12'-1" clear) |
| Dining | 42–53 × 7.5–12.5, plus the table zone into the living to y 12.9; 4'-6" table seats 6–7 |
| Light well | slab void 45.5–51 × 8–12.5, jali rail upstairs |
| Stair | mirrored (clockwise), same box 34.5–42 × 15.67–25 |

- **Fixes:** a genkan entry; pooja in the NE, off the kitchen wall; a dining room with top light and seats for festivals; stack ventilation; the stair direction.
- **Costs:** ~27 sq ft of terrace; a closable lid if the living gets an AC; ~Rs 40–70k (edge beams, rail, lid, extra step and frame). The master and small-room problems remain.
- **Vastu:** better on four counts (pooja NE, NE clean, stair clockwise, near-centre open). Nothing gets worse.
- **Phasing:** everything is stage 1 and in the ground floor or slab. The void must be cast with the slab, and the lid can come in stage 2.

### Alternative B: "Re-split the west bay": master SW with a vestibule, guest/den suite NW

```
x: 14                 28      34.5 36     42
   ┌──────────────────┬───────┬────────────┐ y25
   │ GUEST / DEN      │G.bath │   Stair    │
   │ bed head S       │(old   │ (mirrored) │
   │ (sofa = den)     │ R07)  │            │
   │               D07├───────┤            │
   │                  │ Lobby ├────────────┤ y15.67
   ├══ wardrobes ═════┤ (cup- │ Stair hall │
   │ y14            ▲ │ board)├────────────┤ y12
   │ MASTER          vest.    │            │
   │ bed head S     ├──┬──────┤  C.bath    │
   │ (true SW)      │  M.bath │ (as now)   │
   │ ◄ garden door  │  (WC on x36 wet wall)│
   └────────────────┴─────────┴────────────┘ y3
```

| Room | Rectangle | Size / clear | Notes |
|---|---|---|---|
| Master bedroom | 14–28 × 3–14 | 14 × 11 / ~13'-5" × 10'-5" | King bed 6 × 6'-6" head south at x 18–24 (as Bedroom 2 above); 8 ft sliding wardrobe 1'-9" deep on the y 14 wall (~2'-4" clear at the bed foot, the same as upstairs); windows on y 3 at x 15–17.5 and 24.5–27, stacked under W31/W37; garden door at x 14, y 10–13 |
| Master vestibule | 28–34.5 × 9.5–13 | 6.5 × 3.5 / ~6' × 3' | Doors: from the lobby on y 13, to the bedroom on x 28 (y 10–12.5), to the bath on y 9.5; linen niche 34.5–36 × 9.5–12 |
| Master bath | 28–36 × 3–9.5 | 8 × 6.5 / ~7'-6" × 5'-11" | WC on the x 36 wet wall, back to back with the common WC F16, so it joins the south stack; shower 3 × 3; Noah's 7'-6" full-bath length met |
| Lobby | 28–34.5 × 13–18 | 6.5 × 5 | Cupboard F56 stays on y 18 (3 ft clear in front) |
| Guest room / den | 14–28 × 14–25 | 14 × 11 / ~13'-5" × 10'-5" | Bed head south against the master wardrobe wall (buffer); north window W04 ahead; door on x 28 at y 14.5–17; bath via the existing D07 |
| Guest bath | 28–34.5 × 18–25 | as R07 now | North stack unchanged (upper toilet above) |
| Common bath, stair hall, stair | as now (stair mirrored) | | For the living and visitors |
| First floor | unchanged | | Ground walls at y 14 sit under the upstairs y 14 wall; the alcove R32 is dry over the new wet bath (acceptable) |

- **Fixes:**
  - Two square bedrooms instead of a 22 ft three-job room and a 10 × 9 box [FP2, FP5].
  - A real primary-suite vestibule [FP2, FP4, FP8].
  - A second en-suite that serves elders or guests and doubles as the den / "away room" [DREAM, FP5].
  - A wardrobe buffer between the two beds [FP5].
  - The master bed is in the true SW.
  - The master gets a private garden door [FP2, FP7].
  - Both stacks are kept, and the windows stack on the south wall [FP1, FP4].
- **Costs:**
  - One more bath on the ground floor (3 down, 2 up): ~Rs 1.2–1.8 lakh for fittings, waterproofing and tiling.
  - The master loses its sitting zone and north window.
  - Three doors in the vestibule (make the bath door a pocket door [FP1, FP7, CONTRO]).
  - **Budget variant:** drop the master-bath idea and give the old R07 a second door from the lobby (a shared guest/common bath). The master then has to cross the lobby to its bath, which is not recommended.
- **Vastu:**
  - Better: the master sleeps in the SW, head south; the NW holds a guest room (classic). The north bath is still NW.
  - Caution: the new master bath at 28–36 × 3–9.5 is south, just east of the SW zone. Most consultants accept S/W toilets but forbid the SW corner itself (x 14–28 here stays a bedroom). Get a sign-off.
- **Phasing:** All stage 1 (ground walls on plinth beams). The extra bath's fittings could slip to stage 2 if sleeves and traps are cast. No change to the stage-1 slab or beams.

### Alternative C: "Flip the upper floor": terrace at the back, rooms at the front (tested, rejected)

```
F1:  x14 ── terrace 19×22 over the master ── x33 | x33 ── Bedroom 2 / study / baths over living & kitchen ── x61
```

- **Fixes:** The terrace overlooks the private garden instead of the road, and the upstairs bedrooms get east morning light, away from the west wall.
- **Costs:**
  - The upstairs baths would sit over the kitchen or living (leak risk over the food zone, and a vastu red flag), or squeeze over the 7 × 4.5 wet area.
  - The two-storey mass lands on the road face, losing the stepped gable / wing / main-roof composition [FP1, FP6 push-and-pull].
  - The bedrooms take road noise and dust.
  - The living slab is no longer shaded by an open terrace.
  - The terrace is in the western afternoon sun.
- **Vastu:** worse. Built mass would sit in the NE/E and openness in the SW, the reverse of "SW heavy, NE light".
- **Phasing:** worse. Stage 1 would have to build first-floor walls over the occupied living, which is wet, heavy work above the family. The beams and stacks all move.
- **Verdict:** Noah would sketch it in two minutes, then say "no, the original instinct was right" and keep the front terrace.

### Fit checks (all alternatives)
- **Width:** every rectangle sits within y 3–25 (22 ft) and x 14–67. Wall lines reuse existing grid lines (x 14, 28, 34.5, 36, 42, 53, 57, 61, 67; y 3, 12, 12.5, 14, 16.5, 18, 21, 25) plus new ones at y 9.5, y 13 (Alt B) and the void edges at x 45.5 / 51.
- **Stair:** 16 risers × 7.5 in = 10 ft; 7 treads × 10 in = 5'-10" per flight (y 15.67–21.5); 3'-6" flights + 6 in core = 7'-6"; 3'-6" half landing. The mirror changes nothing dimensional; flight 1 starts at the slab-void edge y 15.67, so headroom is unchanged.
- **Room minimums:** both Alt B bedrooms are ~13'-5" × 10'-5" clear (king plus about 2'-8" sides, as the already-accepted Bedroom 2). The master bath is ≥ 7'-6" long [FP2]. Baths are ≥ 6 ft wide. The genkan is ~4 ft deep with a 1'-6"-leaf double door swinging in. The light well is 6 × 4'-6" with a ≥ 3 ft terrace walkway on every side. The dining path is ≥ 3'-6" [FP2].

---

## 4. Noah's recommended plan

**A + B together, plus the back garden. Reject C.**

1. **Front:** genkan foyer 57–61 × 16.5–21 between a **NE pooja** (57–61 × 21–25) and a shoe alcove (57–61 × 12.5–16.5); living 42–57 × 12.5–25.
2. **Centre:** a dining table for 6–7 under a **light well** (slab void 45.5–51 × 8–12.5) opening to the covered terrace; the living's south band is detailed as a lit gallery.
3. **Stair mirrored to rise clockwise**, same box.
4. **West bay re-split at y 14:**
   - master in the true SW with a vestibule (28–34.5 × 9.5–13) and its bath (28–36 × 3–9.5) on the south stack;
   - guest room / den in the NW using the existing north bath;
   - the 10 × 9 small room goes (its area becomes the master vestibule and bath).
5. **Back land becomes a walled garden court:** septic and soak pit move to the NW of the spare land; a garden door from the master (or from the den, if vastu objects) opens onto an otta under the pergola.
6. **Keep the covered terrace at the front.** Zone it: lounge north, drying south, the light-well rail between.
7. **Only if the setback requires it,** slide the house 3 ft west for an 11 ft front yard.

**Net effect:**
- **Same footprint** (53 × 22), same upstairs plan, same two soil stacks.
- **Rooms:** one more bath, one fewer box room, one more real room (the den).
- **Vastu** improves on every briefed point: kitchen SE (unchanged), master bed SW, pooja NE, main door E, stair clockwise, septic NW.
- **Cost:** about **+Rs 2–3 lakh** in stage 1 (extra bath, void edges, rail and lid, garden door and otta), partly offset by less slab. That stays inside the Rs 43–51 lakh band.
- **Phasing:** stage 2 and stage 3 scope is unchanged.

---

## 5. Keep

- **Public front, private back, the stair on the hinge.** Bedrooms on their own level/wing is what he praises most [FP5]. The stair is not in front of the door and runs off a side hall [FP8], with a landing window W05 at the half landing [FP6, FP5].
- **Master on the ground floor** for ageing in place [DREAM].
- **The entry axis:** gate (y 15.6–22.6) → tulsi thara on the axis (a detour that slows arrival) → steps between pillars → D01 centred on the gable (y 19.1) → vilakku madam F59 at x 42, y 18–19.8. It is "punctuating the end of the axis" done right [FP4, FP5, FP1].
- **Closed kitchen with a glazed sliding door and a serving hatch:** his "glass partition" answer to Indian cooking [CONTRO, section 6]. The kitchen, wet area and service door chain together [FP6, FP1]. The kitchen sits next to the entry [DREAM].
- **Seating group as a cul-de-sac** in the living's NW quarter, with armchairs as a soft edge [FP4, SA4].
- **Two tidy wet stacks,** no bath over a living room, and the upstairs walls stacked over ground walls on beams.
- **The covered terrace:** shaded, with jali parapets to the neighbours, and the lounge on the private side [WORST: no exposed balcony rails; FP2, FP5].
- **Roof-first phasing** that never defers structure, waterproofing or buried services [FP2, FP1 "find the cheap structural move"].
