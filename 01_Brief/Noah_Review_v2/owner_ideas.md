# Noah on the owner's two ideas

Checked against `99_Source/model.py` on `feature/duplex` (HEAD `525a62a`). Plan pages A-102 to A-105 were rendered (PDF pages 4–7). Coordinates are in feet: x runs from the west, y from the south. Rule codes refer to `01_Brief/Noah_Daniel_Principles.md`.

> **A model defect to fix first, whatever you decide.** In `model.py` line 44, three walls ended up inside a comment: `("Y", 36, 3, 11.5)`, `("X", 11.5, 36, 42)` and `("Y", 42, 3, 11.5)`. As a result, sheets A-102 and A-104 draw the master bath, the common bath, the wet area and the stair hall as one open space. The D08 door hangs in a wall that isn't drawn. Restore the three walls. Separately, the notes on `F98` and on the R39 `WC` in `PLUMBING_F1` still say "over the master bath WC". It's over the guest bath R07 now.

---

## Noah's take

"OK friends, I love that you're questioning things. Most constraints in a new build are self-imposed [FP2], and you're right that two things nag on this plan. The dining is a strip, and five bathrooms in about 1,700 sq ft is a lot of tile. But both ideas solve those problems by deleting the rooms that make the house work. The wet area is what lets you keep the kitchen closed in an Indian home. The common bath is what keeps guests out of the bedroom wing. The stair sits on the hinge between public and private, and it doubles as the cooling chimney. So my honest answer to both ideas is no, with one smaller move I'd happily steal from Idea 1. And please don't do both: together they leave the ground floor with one bathroom, and it's inside your parents' bedroom."

---

## IDEA 1: remove the wet area (R13) and the common bath (R08); R07 becomes the common bath

### Verdict: **No, and here's why.** You've found a real problem, but this is the wrong fix. I'd take a small piece of it (version 1N below).

### What he sees

- R08 is 36–42 × 3–11.5 (6 × 8.5). R13 is 42–53 × 3–7.5 (11 × 4.5). Together that's about 100 sq ft.
- Delete both and you get one room of about 36–53 × 3–12.5, roughly 17 × 9.5. That's a real dining room, against today's 11 × 5 strip (R10 is 42–53 × 7.5–12.5).
- **The dining is not as small as it looks.** Its north edge (y 12.5) is open to the living. The table F24 is 44.5–50 × 9–11.5. North-side chairs would reach y 13, and the nearest living furniture, armchair F45, starts at y 17.8. That leaves about 4'-9" of clear path for chairs on both sides. The table already seats 7 today, and 8 with the extension.

### Why it bothers him

1. **The closed kitchen depends on the wet area.** Indian cooking works with a closed kitchen *plus* a work area (section 6). Today the vessels go one step through D12 (x 53) to a sink with a low bucket tap, a floor trap and a drying rack (F29, F62, and the TAP at 49.8, 3.4). Without R13:
   - the big kadai and pressure-cooker scrubbing moves into the kitchen, onto a dry floor, on a prep sink F65 that is a single bowl;
   - or it moves outside to the 3 ft south walkway, where whoever washes the vessels blocks the only service path to the back garden.

   Chaining the service rooms is one of his rules [FP6, FP1], and here you'd be breaking the chain.
2. **Using R07 as the common bath brings guests into the private wing.** R07 (28–34.5 × 18–25) opens only from the den (D07). To make it common, you would:
   - cut a door in the lobby's north wall X18 at about x 31.6–34.0, mirroring D39 upstairs;
   - remove the F56 cupboard (30.2–33.5 × 15.9–17.8), which stands right where that door would go;
   - and keep D44, the wing door you just added, open whenever there are guests.

   The lobby (6.5 × 6.5) would then have four or five doors: D02, D04, D44, the new door, and D07 if kept. He calls too many doors onto one small room a pet peeve (#13). And with D44 open, the stair hall looks straight down the y 12.4–14.9 band into the master door D04. That's the 33 ft view into the bedroom that B6 was meant to close. Public and private have to stay apart (section 5). At a festival, 20 people would queue for a toilet between your parents' bedroom door and the den.
3. **The sight lines are fine, but only that one way.** With the new door at the east end of X18, hinged on its west jamb and opening inward, the first view is the shower glass F50 (31.2–34.2 × 21.4), and the WC F48 (28.3–29.9 × 21–22.2) is hidden behind the leaf. That passes his rule (pet peeve #1). The door works; the route to it is the problem.
4. **Bath 2's plumbing stack loses the room below it.** R33 (Bath 2) sits exactly over R08.
   - Its WC soil can still drop at x 36, in a duct on the dining side of the master bath wet wall (the master bath WC F12 stack is already at 35.2, 7.8).
   - Its shower trap (39, 4.5) and basin (41.4, 7.9) have nothing below them. They would need either:
     - a bulkhead about 9 in deep over the dining's west end (36–42 × 3–11.5), or
     - a raised Bath 2 floor with a step up.

   You would also break the project rule "no bath over a living room". On top of that, the dining's new west wall becomes the master WC's wet wall. That's acceptable if it's built thick and insulated [CONTRO], but it isn't charming.
5. **Laundry and drying.** The washer would have to go to the terrace (B5-A). That's actually a good place for it in Guntur, because the drying is already up there (F88), and the terrace tap at (42.4, 4.2) exists. But in **stage 1**:
   - the upstairs is an "open covered deck… no water use until stage 3";
   - the parents live downstairs, and the house is designed for ageing in place [DREAM];
   - so every wash day would mean a climb of 16 risers, from day one.
6. **The bathroom count in stage 1.** During stage 1 the den is the house's second bedroom, because nothing upstairs is fitted out yet. Idea 1 leaves the ground floor with two baths: the master's, and one shared through the private lobby. That's livable, but it's worse than what you have.

### What it would honestly give, for the record

| | |
|---|---|
| Fixes | Dining 17 × 9.5; the dining gets the south windows W03 and W11 back; one less toilet near the centre of the house (vastu likes that: R08 touches the centre ninth at y 10.33–11.5) |
| Breaks | Vessel washing; ground-floor laundry; public/private separation; the B6 wing door; "no bath over living"; Bath 2's stack |
| Vastu | Mildly positive: no toilet beside the brahmasthan, and R07 is a toilet in the NW, which is acceptable. Vessel washing in the SE kitchen is neutral. |
| Cost | Roughly **Rs 1.0–1.5 L saved**. That's the R08 fit-out of about Rs 1.2–1.8 L, plus the utility plumbing, minus a double-bowl kitchen sink, a terrace washer point, and the Bath 2 bulkhead or duct. |
| Phasing | Stage 1 gets worse: laundry upstairs on a dry deck, and guests in the private lobby |

### His version: **1N, "give the dining the window and the basin, not the bathroom"**

Keep both wet rooms. Shorten the utility by 4 ft and give that slice to the dining as an open wash-and-water alcove.

| Element | Rectangle / position | Detail |
|---|---|---|
| Wet area R13 (shortened) | **46–53 × 3–7.5** (7 × 4.5) | Keeps the utility sink F29 (50–51.9), the rack F62, the low tap, floor trap FT (48.5, 3.6), airer F61 (46.6–52.4), D12 to the kitchen, and the D18 service door (46.8–49.3, about 6 in off the new wall). A new 5 in internal wall on x 46, y 3–7.5. |
| Dining alcove (part of R10) | **42–46 × 3–7.5**, open to the dining along y 7.5 | Hand-wash basin on the x 42 wall at about 42.3–43.0 × 5.4–6.9, back to back with the R08 basin F17. It shares R08's supply and grey line, so no new stack. A 1'-9" water / RO and crockery counter under W11 (42.3–45.8 × 3.3–5.0); W11 (42.7–45.3) is already centred on the alcove (44.0). F44 crockery moves here. |
| Dining bench F28 | 46.2–50 × 7.85–8.85 | Shortened to back onto the remaining X7.5 wall (46–53). The west chair F25 keeps 2 ft clear to the alcove. For festivals the table extends **west** into the alcove opening (to about 42.5), not east into the hatch ledge. |
| Washer | Terrace laundry corner, F1 **42.5–44.5 × 3.4–5.4** | Against Bath 2's x 42 wall. The stage-1 supply is the existing terrace tap, plus a splash-proof socket and its own floor trap, draining by an external grey pipe down the south wall to IC-5 (39, 1.0). The drying rails F88 shift to 45–52 × 3.5–6.8. **Fallback, if the parents do the laundry:** a front-loader under the utility drainboard, with D18 made a sliding door. Ask whoever actually does the washing [FP8/FP7, section 6]. |

- **What it fixes:**
  - the dining gets back its window (the B4 cost) and a proper hand-wash point (you eat with your hands; today the nearest basin is in a bathroom);
  - the festival table gains about 2 ft;
  - the alcove sits on an axis, because W11 is already centred on it.
- **What it costs:**
  - the utility loses 4 ft, and the washer leaves it (or goes under the counter);
  - about **Rs 25–40 k** for the wall, the basin and the terrace washer point.
- **Vastu:** unchanged.
- **Stacks:** unchanged.
- **Phasing:** everything is in stage 1. The terrace washer point is outdoor plumbing and doesn't conflict with "no water use in the rooms".
- **Confidence he'd push this:** medium. He'd rather give the dining its window and basin than lose a wet room.

---

## IDEA 2: move the stair west and remove the guest bath R07

### Verdict: **No, and here's why.** There is one buildable version (P2), but it's a lot of surgery for a coffee table's worth of floor. The only strong argument for it is vastu, and the vastu consultant should make that call.

### Where the stair could go (tested)

The stair is 7'-6" wide (two 3'-6" flights and a 6 in core) and 9'-4" long (7 treads of 10 in, plus a 3'-6" half landing). The only slot west of the current box is the R07 / lobby column, x 28–34.5, which is only 6.5 ft wide.

- **P1: the same N–S stair, shifted 6.5 ft west (28–35.5 × 15.67–25). Fails.**
  - Clockwise means flight 1 rises north on the west side, so its foot sits at (28–31.5, 15.67).
  - The den's only possible door wall is x 28 at y 15–25, and the stair would cover y 15.67–25 of it. That leaves 8 in for D02.
  - The lobby's x 28 wall from y 11.5 to 15.67 can't hold both the master door and the den door.
  - Flipping or rotating the flights to fix this makes it anticlockwise.
- **P2: turned E–W, in the R07 slot. Works, with one deviation.**
  - **Box 28–37.33 × 17.75–25** (9'-4" × 7'-3").
  - The 6 in AAC core becomes a **3 in open timber stringer and balustrade**. The flights stay 3'-6", and the box stays clear of the den door D02 (15.3–17.6).
  - **Flight 1:** south half, y 17.75–21.25. Its foot is at **x 37.33, facing east toward the living**, and it rises west to x 31.5.
  - **Half landing:** 28–31.5 × 17.75–25, at +5'-0".
  - **Flight 2:** north half, y 21.5–25. It rises east to arrive at x 37.33, at +10'.
  - The direction is west, turn right, then east: **clockwise ✓**.

### P2, as he'd draw it

**Ground floor**

| Element | Rectangle | Detail |
|---|---|---|
| Stair | 28–37.33 × 17.75–25 | As above. A north window on the half landing at about x 28.5–31 (it replaces W43). |
| Under the landing | 28–31.5 × 18–25 | 4'-4" headroom: a luggage and bedding store opening into the den through the old D07 wall |
| Under flight 2's high end | 34.5–37.33 × 21.5–25 | 6'-6" to 9' headroom: a bench or TV niche facing east |
| Lobby | 28–34.5 × 11.5–17.75 | D02, D04 and D44 unchanged; F56 moves 1 in south |
| Stair hall and stair foot | 34.5–42 × 11.5–17.75, plus 37.33–42 × 17.75–25 | The x 42 stair wall (15.67–25) and the jali W10 are removed, so the living reads as 37.33–57 |
| Den R42 | 14–28 × 15–25 | Unchanged in size; **no bath**; door D07 becomes the store's doors |

**First floor**

| Element | Rectangle | Detail |
|---|---|---|
| Stair void | 28–34 × 17.75–25, plus 34–37.33 × 21.5–25 | Headroom over the half landing and flight 2; the floor can run over the low end of flight 1 |
| Arrival hall | 34–42 × 15.67–25 (minus the void) | You step off at (37.33, 23) facing east |
| Terrace door D36 | x 42, **y 21.25–24.75** | On the arrival axis: the light at the top draws people up [FP6]. The diwan F84 shifts to y 15–21. |
| Landing | 28–34.5 × 11.5–17.75 | D31 (Bedroom 2) and D35 (study) unchanged; Bedroom 2's suite and the study unchanged |
| Upper toilet R39 | **Option A:** 34.5–42 × 11.5–15.67 (7'-6" × 4'-2", three bands along x), over the stair hall, its WC on the y 11.5 wall dropping into a duct in R08's north-west corner. **Option B:** none. | A puts a toilet in the **centre ninth** (31.67–49.33 × 10.33–17.67), which vastu dislikes even upstairs. The only other floor space sits over the new living, which breaks "no bath over a living room". |

### What P2 fixes

- **Vastu (the one real win).** The stair leaves the centre ninth: today the box intrudes at y 15.67–17.67, and P2 starts at y 17.75. The house centre (40.5, 14) becomes an open hall next to the light well. The stair moves into the N and NW ninths and still rises clockwise.
- **One plumbing stack instead of two.** R07 and R39 leave the north walkway line, so every wet room drains south.
- **A sculptural timber stair** with an open stringer, seen from the living. He loves a good stair [COOL, INSP1].
- About Rs 1.2–1.8 L saved on R07 under option B, or about half that under option A, where the upper toilet is rebuilt.

### What P2 costs or breaks

- **Living area.** The living gains only 37.33–42 × 15.67–25, about 44 sq ft. About 13 sq ft of that is the landing zone in front of flight 1, and the rest is the path to it. That is "a lot of path, not room" [pet peeve 3].
- **The living becomes 19'-8" × 12'-6".** Its west end turns into the route to the bedrooms upstairs.
- **The TV loses its composed wall** (F53, W10, F59), leaving only about 3'-6" of solid stair end. The lamp niche F59, on the entry axis y 18.75, would land on the stair foot, so the entry axis loses its end point [FP4].
- **The stair stops working as a chimney.** The cooling strategy (W10 jali, W05, clerestory W45) is rebuilt at the den end. The living still connects through the open stair foot, but less directly.
- **The den stops being a guest suite.** It becomes "a bed in a room" [FP1]. A visiting relative on the sofa-bed walks about 25 ft at night, out through D44, to the common bath D08. Worse, **in stage 1 the den is the second bedroom**, and it would have no bath of its own.
- **Upstairs:** either a toilet in the brahmasthan (option A) or no toilet for the study guests and terrace parties (option B).
- **Structure.** The slab voids, the beams around the stair and the stair foundations all move. It's only redrawing now, but it's a full structural redesign.

### R07 removal alone (keeping the stair)

- **Possible.** The R07 slot (6.5 × 7) would become a den bay or a house store, and R39 above it could keep its stack through a boxed duct.
- **He would not do it now.** In stage 1 the den is the second bedroom, so it needs its bath. And the M2b plan you approved made the den a guest suite on purpose. If guests are rare, revisit this before tiling, not before structure.

**His recommendation for Idea 2:** keep the stair where it is, clockwise and on the hinge, and keep R07. Draw P2 only if the vastu consultant insists the stair must leave the centre. If you do, choose option B for the upper toilet (none upstairs) rather than a toilet in the centre.

---

## Do the two ideas combine?

**No, and this is the clearest call in the review.**
- Idea 1 deletes R08 and Idea 2 deletes R07. Together they leave **one ground-floor bath, R40, reached through the master bedroom**.
- The only public place left for a new common bath is the freed stair box (37.33–42 × 15.67–25). That is exactly where the clockwise P2 stair puts its foot (37.33–41 × 17.75–21.25). The anticlockwise mirror would free that spot, but it breaks the vastu brief.
- What remains is 37.33–42 × 21.25–25 (4'-8" × 3'-9"). That's too small for a bath, and it would sit beside the TV.

So the two ideas fight over which bathroom survives, and the house loses either way.

---

## The plan he'd actually draw

Keep everything as it is except:
1. **Restore the three missing walls** (Y36, X11.5 from 36 to 42, and Y42 from 3 to 11.5).
2. **1N:**
   - the utility becomes 46–53 × 3–7.5;
   - a dining wash-and-water alcove at 42–46 × 3–7.5, open to the dining, with W11, a basin on the x 42 wet wall and a crockery / RO counter;
   - the bench becomes 46.2–50;
   - the table extends west for festivals;
   - the washer goes to the terrace laundry corner (42.5–44.5 × 3.4–5.4) with stage-1 points, or under the utility counter if the parents do the laundry.
3. **Stair, R07, R08, R39: unchanged.**

## Keep (what both ideas would have cost you)

- R08 as the **public bath**, outside the bedroom wing, stacked under Bath 2.
- R13 **next to the kitchen**, one door away. A closed Indian kitchen needs its wet partner.
- The **stair as the hinge** between public and private, with the jali W10, the lamp niche on the entry axis, and the stair chimney. It's clockwise already.
- The **den with its own bath**: the second bedroom in stage 1, and a guest suite after that.
- **D44**, the wing door that keeps the 33 ft view out of the master bedroom.
