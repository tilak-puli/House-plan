"""Kerala home, Phase 1 (courtyard concept): single data model used for every drawing and schedule.
Plan coordinates in feet: x from the west (back) boundary, y from the south boundary. The plot is a 50 x 130 ft rectangle
(x 0-130 west to the east road, y 0-50), about 6,500 sq ft. The house is a compact Tamil courtyard house, 42 x 42 ft, at x 15-57,
y 4-46: a ring of 12.5 ft rooms round a 3.5 ft walkway and a 10 x 10 ft open courtyard at the centre (36, 25); the thinnai
(x 57-62) and its steps lie east of it on the main-door axis, with a reserved 1:12 ramp. Two floors: ground (G) and first (F1, a west wing). Lists for the floor
being drawn are swapped in by set_floor() at the end. NOTE (compact plan): the ground floor's rooms and walls are re-cut (Task C2); its doors, windows and furniture are in (Tasks C3, C4), and the first floor is re-cut in Task C5; the services of both floors (electrical, plumbing, pipes) are in from Task C6, the roof
from Task C8, and the prose (finishes, specification, open issues, decisions, phasing) is rewritten for the compact house in Task C7.
Site: Guntur, Andhra Pradesh. Hot-dry summers (42-45 C), ~850-1000 mm rain (Jun-Oct, cyclonic bursts Oct-Nov),
likely expansive black cotton soil, hard / high-fluoride groundwater, seismic zone III, high cyclone wind speeds.
"""
from contextlib import contextmanager

PROJECT = {
    "name": "Kerala Home, Courtyard Concept",
    "stage": "Draft for professional review",
    "title_lines": [],   # the title block's description lines: set below, from the grid and the plot
    "plot": "",          # set below the rooms, from the plot, the house and the thinnai
    "location": "Guntur, Andhra Pradesh (agricultural land: conversion to be confirmed)",
    "road": "East",
    "rev": "E-compact (concept study)",
    "date": "25 Nov 2026",
}

# Grid of the courtyard house (feet). The house is a ring of rooms round a walkway and an open courtyard.
HX1, HX2, HY1, HY2 = 15.0, 57.0, 4.0, 46.0   # house outer wall centre lines (42 x 42)
BAND, WALK, COURT = 12.5, 3.5, 10.0           # room band depth, walkway width, open courtyard side
CX, CY = (HX1 + HX2) / 2, (HY1 + HY2) / 2     # 36.0, 25.0: house centre = brahmasthan = courtyard centre
CT = (CX - COURT / 2, CX + COURT / 2, CY - COURT / 2, CY + COURT / 2)        # (31, 41, 20, 30) courtyard
RING = (CT[0] - WALK, CT[1] + WALK, CT[2] - WALK, CT[3] + WALK)              # (27.5, 44.5, 16.5, 33.5) walkway outer edge

SITE = {"w": 50, "l": 100, "strip": 0, "trial": 0}  # frame of the house sheets (the plot runs on to the road); "trial" = the plot's back (west) boundary
# The whole plot: 130 ft deep (west to the east road) and 50 ft wide, a plain rectangle. About 6,500 sq ft.
PLOT = [(0, 0), (130, 0), (130, 50), (0, 50)]
PROJECT["title_lines"] = [f"Compact Tamil courtyard house, {HX2 - HX1:.0f} x {HY2 - HY1:.0f} ft:", "a ring of rooms round an open courtyard,",
                          "plus a west upper wing; Guntur, AP", f"Plot {max(p[1] for p in PLOT):.0f} x {max(p[0] for p in PLOT):.0f} ft, road on east"]
PLOT_X1, PLOT_X2 = 0.0, 130.0
# Vastu: the gate and the way for cars on the north side, in the north-east, as you face the house from the road.
# The shops make the road frontage in the south-east; the road wall closes the frontage between them and the gate.
SHOP_WALL = [(130.0, 25.0), (130.0, 33.0)]
DRIVE = {"x1": 102.0, "x2": 130.0, "off": (34.0, 44.0)}  # 10 ft drive 6 ft off the north boundary, from the gate to the car porch; "off" = its south and north edge (y)


def plot_north(x):
    """y of the north boundary at x (a straight rectangle plot)."""
    return 50.0


# Vegetable beds (raised, 4 ft wide) in the vegetable garden
GARDEN_BEDS = [(float(x), x + 5.0, 25.8, 29.6) for x in range(99, 124, 6)] + [(float(x), x + 5.0, 45.0, 49.0) for x in range(74, 98, 6)]  # five beds in the vegetable strip south of the drive and four on the north strip, 5 x 4 ft


def drive_poly():
    """Outline of the drive: x 102-130, y 34-44."""
    a, b = DRIVE["off"]
    return [(DRIVE["x1"], a), (DRIVE["x2"], a), (DRIVE["x2"], b), (DRIVE["x1"], b)]

T = 0.75  # outer wall thickness, ft (9 in finished)

# ---------- ground floor: a ring of rooms round the walkway and the open courtyard (Task C2, compact 42 x 42) ----------
# Blocks: SW master x 15-27.5 y 4-20.24; W middle (stair, lobby, linen/DB walk-in, low store) x 15-27.5 y 20.24-33.5;
# NW den bath x 15-22 y 39.3-46 with the den alcove south of it, den x 22-33.5 y 33.5-46 (door off the north walkway);
# N living x 33.5-51 y 33.5-46; NE console nook x 51-57 y 33.5-40 and pooja x 51-57 y 40-46; E foyer x 51-57 y 25-33.5,
# oonjal link x 44.5-51 y 25-33.5, dining end x 44.5-57 y 16.5-25 (living, nook, link and dining end are one family room R16
# with no walls between them); S master bath, powder room, utility and pantry x 27.5-44.5 y 4-16.5; SE kitchen x 44.5-57 y 4-16.5;
# centre: walkway (thazhvaram) round the courtyard (mutram); thinnai x 57-62 y 24-34.
COURTYARD = CT
# Ground-floor stair (Task C2): dog-leg against the west wall, flights and landing 3'-6" clear between wall faces. The stair
# column runs x 15-23.085 (its 5 in east wall face at 22.875); the half landing is against the den-side wall (face 33.29) over the
# low store R46; the flights run y 23.957-29.79; the 3'-6" foot lobby runs from the master's north wall face (20.45) to the first
# riser. Upstairs the arrival is at y 23.957, facing south toward the Bedroom 2 suite over the master.
_GSE = 23.085                                 # stair column to the linen walk-in / lobby (wall centre line)
_GLAND = round(RING[3] - 0.21 - 3.5, 3)       # 29.79: top of both flights; the half landing runs on to the wall face 33.29
_GFOOT = round(_GLAND - 7 * 10 / 12, 3)       # 23.957: first riser of flight 1 (7 treads of 10 in); upstairs arrival edge
_GMN = 20.24                                  # master bedroom's north wall (the lobby is 3'-6" clear from its face to the first riser)
_DB = 38.3                                    # den bath's south wall (the den's wardrobe and desk niche south of it)
_DX = 22.0                                    # den bath / den alcove to the den
_DE = 33.5                                    # den to the living: 9 in, a wing wall can stand on it
_OX, _FY, _NY = 50.8, 25.0, 40.0              # foyer / nook / pooja west line (foyer 5'-7" clear inside its jali screen); dining end to the foyer; nook to the pooja
_KY = 15.5                                    # kitchen to the dining end (the dining end is 9 ft clear deep)
_CORE = 19.125                                # centre line of the 6 in core between the flights
_BX, _PX, _QX, _UY = 34.5, 39.6, 44.5, 9.5    # master bath east; powder / pantry; utility & pantry to the kitchen; utility north
ROOMS = [  # id, name, x1, x2, y1, y2, zone
    ("R01", "Master bedroom", HX1, RING[0], HY1, _GMN, "Master suite"),             # SW corner, bed head to the south wall
    ("R40", "Master bath", RING[0], _BX, HY1, RING[2], "Master suite"),             # door from the bedroom on x 27.5
    ("R08", "Powder room", _BX, _PX, _UY, RING[2], "Service"),                      # door off the south walkway
    ("R60", "Pantry", _PX, _QX, _UY, RING[2], "Service"),                           # walk-in, door from the kitchen
    ("R13", "Utility", _BX, _QX, HY1, _UY, "Service"),                              # door from the kitchen, service door on the south wall
    ("R15", "Kitchen", _QX, HX2, HY1, _KY, "Service"),                              # SE corner
    ("R09", "Stair lobby", HX1, RING[0], _GMN, _GFOOT, "Circulation"),              # the 3'-6" foot lobby, running on 4'-5" east to the west walkway
    ("R06", "Stair", HX1, _CORE, _GFOOT, _GLAND, "Circulation"),                    # flight 1 at ground (flight 2 rises over the cupboard R48)
    ("R48", "DB and linen", _CORE, _GSE, _GFOOT, _GLAND, "Service"),               # cupboard under flight 2, door off the foot lobby (full height at its front)
    ("R47", "Den walk-in", _GSE, RING[0], _GFOOT, RING[3], "Private"),              # the den's walk-in wardrobe, door from the den on y 33.5; hatch to the low store
    ("R46", "Low store", HX1, _GSE, _GLAND, RING[3], "Service"),                    # low hatch store under the half landing
    ("R58", "Den niche", HX1, _DX, RING[3], _DB, "Private"),                        # the den's wardrobe and desk niche, open to the den
    ("R07", "Den bath", HX1, _DX, _DB, HY2, "Private"),                             # NW corner, west and north outer walls; the upper toilet stacks over it
    ("R42", "Den", _DX, _DE, RING[3], HY2, "Private"),                              # door straight off the north walkway (x 27.5-33.5)
    ("R16", "Family room (living)", _DE, _OX, RING[3], HY2, "Living"),             # folding doors to the north walkway
    ("R16N", "Console nook", _OX, HX2, RING[3], _NY, "Living"),       # open to the living
    ("R11", "Pooja", _OX, HX2, _NY, HY2, "Living"),                                 # NE corner, opens west into the living
    ("R16S", "Oonjal link", RING[1], _OX, _FY, RING[3], "Living"),   # links the living and the dining end; open to the foyer
    ("R18", "Foyer", _OX, HX2, _FY, RING[3], "Entry"),                              # main door on x 57 (north half); open west to the oonjal link
    ("R16D", "Dining end", RING[1], HX2, _KY, _FY, "Living"),    # next to the kitchen
    ("R50", "Courtyard (mutram)", CT[0], CT[1], CT[2], CT[3], "Courtyard"),
    ("R51", "Walkway (south)", RING[0], RING[1], RING[2], CT[2], "Courtyard"),
    ("R61", "Walkway (north)", RING[0], RING[1], CT[3], RING[3], "Courtyard"),
    ("R62", "Walkway (west)", RING[0], CT[0], CT[2], CT[3], "Courtyard"),
    ("R63", "Walkway (east)", CT[1], RING[1], CT[2], CT[3], "Courtyard"),
    ("R17", "Thinnai", HX2, 62.0, 24.0, 34.0, "Entry"),                             # one platform; the door gap y 27-31 is open floor; ramp opening x 58-62 on y 24
]
_TX2 = next(r[3] for r in ROOMS if r[0] == "R17")
PROJECT["plot"] = (f"{max(p[1] for p in PLOT):.0f} ft wide (north-south) x {PLOT_X2 - PLOT_X1:.0f} ft deep (west to the east road); "
                   f"{HX1 - PLOT_X1:.0f} ft of back garden behind the house, {PLOT_X2 - HX2:.0f} ft from the house wall to the road ({PLOT_X2 - _TX2:.0f} ft beyond the thinnai)")
FAMILY_ROOM = ("R16", "R16N", "R16S", "R16D")   # one L-shaped family room drawn as four rects with no walls between them

# Walls: (axis, coordinate, start, end). axis "X" = runs along x at y=c; "Y" = runs along y at x=c.
# No wall: the courtyard edge (walkway pillars); the stair to its lobby (y 23.96, x 15-19.1); the den niche to the den
# (x 22, y 33.5-38.3); inside the family room (living to nook x 51 y 33.5-40, living to oonjal link y 33.5 x 44.5-51, link to
# dining end y 25 x 44.5-51). The foyer opens to the oonjal link through a 4 ft opening (x 50.8, y 27-31) in its jali screen.
# Folding-door walls (Task C3): the living to the north walkway (y 33.5, x 33.5-44.5) and the oonjal link and dining end to the
# east walkway (x 44.5, y 16.5-33.5).
WALLS = [
    ("X", HY1, HX1, HX2), ("X", HY2, HX1, HX2), ("Y", HX1, HY1, HY2), ("Y", HX2, HY1, HY2),   # outer walls
    # walls round the walkway (9 in, they carry the walkway roof)
    ("X", RING[2], RING[0], RING[1]), ("X", RING[3], RING[0], RING[1]), ("Y", RING[0], RING[2], RING[3]), ("Y", RING[1], RING[2], RING[3]),
    # south-west and south: master, master bath, powder, pantry, utility, kitchen
    ("X", _GMN, HX1, RING[0]),                      # master to the stair and its lobby
    ("Y", RING[0], HY1, RING[2]),                   # master to its bath (wet)
    ("Y", _BX, HY1, RING[2]),                       # master bath to the utility and powder room (wet)
    ("X", _UY, _BX, _QX),                           # utility to the powder room and pantry (wet)
    ("Y", _PX, _UY, RING[2]),                       # powder room to the pantry (wet)
    ("Y", _QX, HY1, _UY), ("Y", _QX, _UY, RING[2]), # utility (wet) and pantry to the kitchen
    ("X", _KY, _QX, HX2),                           # kitchen to the dining end
    # west: stair, lobby, linen walk-in, low store
    ("Y", _GSE, _GFOOT, RING[3]),                   # stair column (cupboard, low store) to the den walk-in
    ("X", _GFOOT, _CORE, RING[0]),                  # foot lobby to the cupboard under flight 2 and the den walk-in
    ("X", _GLAND, HX1, _GSE),                       # under the landing edge: the low store's south wall
    ("X", RING[3], HX1, RING[0]),                   # west block to the den alcove and the den
    # north-west: den bath
    ("X", _DB, HX1, _DX), ("Y", _DX, _DB, HY2),     # den bath (wet)
    ("Y", _DE, RING[3], HY2),                       # den to the living (9 in: the upper wing's wall stands on it)
    # east: foyer, nook, pooja
    ("X", _FY, _OX, HX2),                           # dining end to the foyer (shoe bench)
    ("Y", _OX, _FY, 27.0), ("Y", _OX, 31.0, RING[3]),   # foyer's jali screen walls to the oonjal link: a 4 ft opening y 27-31 on the main-door axis
    ("X", RING[3], _OX, HX2),                       # foyer to the console nook (uruli niche)
    ("X", _NY, _OX, HX2), ("Y", _OX, _NY, HY2),     # pooja
]
BELOW_STAIR_WALLS = {("X", _GLAND, HX1, _GSE)}   # the low store's wall under the landing edge: drawn dashed on the plan ("below the landing")
# 9 in: the outer walls (whole lines), plus the walls round the walkway and the den-to-living wall (exact segments)
EXTERIOR = {("X", HY1), ("X", HY2), ("Y", HX1), ("Y", HX2)}
# Wall types (finished thickness, ft). AAC blocks in an RCC frame; walls carrying concealed plumbing are thicker
# so pipe chases do not cut a 4 in block in half.
WALL_TYPES = {
    "EXT": (0.75, "200 mm AAC + 20 mm external plaster + 12 mm internal plaster (~9 in)"),
    "WET": (0.58, "150 mm AAC + plaster both faces (~7 in): concealed plumbing walls"),
    "INT": (0.42, "100 mm AAC + plaster both faces (~5 in)"),
}
EXTRA_EXT_WALLS = {("Y", RING[0], HY1, RING[2]),          # master to its bath: the upper wing's east wall stands on it
                   ("X", RING[2], RING[0], RING[1]), ("X", RING[3], RING[0], RING[1]), ("Y", RING[0], RING[2], RING[3]),
                   ("Y", RING[1], RING[2], RING[3]), ("Y", _DE, RING[3], HY2)}
WET_WALLS = {("Y", _BX, HY1, RING[2]),                                # master bath (its west wall is 9 in)
             ("X", _UY, _BX, _QX),                                     # utility, powder room
             ("Y", _QX, HY1, _UY),                                     # utility to the kitchen
             ("X", _DB, HX1, _DX), ("Y", _DX, _DB, HY2)}               # den bath

# Levels and heights, ft. 0 = finished ground level (FGL) around the house.
LEVELS = {
    "FGL": 0.0,
    "FFL": 2.0,          # plinth: ground floor finished level
    "poomukham": 1.5,    # thinnai platforms 1'-6" above the forecourt (the key keeps its duplex name: the drawing code reads it)
    "wet_area": 1.96,    # utility 1/2 in below the house, falls to its trap (no step)
    "bath_drop": 0.04,   # bathrooms 1/2 in (12 mm) below adjoining floor, no raised threshold
    "door_head": 7.0,    # above floor level; continuous RCC lintel band at this level
    "wall_top": 10.0,    # above FFL: ground-floor ring beam / first-floor slab level
    "upper_ffl": 10.0,   # first floor finished level above FFL (floor to floor, 16 risers of 7.5 in)
    "upper_wall_top": 10.0,  # above the first floor: ring beam, roof trusses bolted to it
    "slab": 0.5,         # RCC slab + screed + finish at the first floor
    "false_ceiling": 9.5,
    "bath_ceiling": 8.5,
    "riser": 0.5,        # entrance steps: 6 in risers, 12 in treads
}
LEVELS["courtyard"] = LEVELS["FFL"] - 0.5   # sunken stone court, 6 in below the house
LEVELS["walkway"] = LEVELS["FFL"] - 0.08    # walkway 1 in below the rooms (rain), one step above the court
LEVELS["thinnai"] = LEVELS["FFL"] - 0.5     # thinnai platform, one step below the house
_ATH, _RED, _CER, _GRA, _VIT = ("Athangudi handmade tile", "Red oxide / Kota stone", "Anti-skid ceramic, waterproofed",
                                "Rough-dressed granite", "Matt vitrified 2x2")
FLOOR_FINISH = {  # room: floor finish key
    **{r: _ATH for r in FAMILY_ROOM},
    **{r: _RED for r in ("R01", "R42", "R58", "R47", "R48", "R06", "R09", "R11", "R17")},
    **{r: _CER for r in ("R40", "R07", "R08", "R13")},
    **{r: _GRA for r in ("R50", "R51", "R61", "R62", "R63", "R18")},
    **{r: _VIT for r in ("R15", "R60", "R46")},
    # first floor (the west wing and the roof terrace)
    **{r: _VIT for r in ("R31", "R45", "R36", "R36A")},
    **{r: _CER for r in ("R33", "R39")},
    **{r: _RED for r in ("R34", "R41")},
    "R37": "Terracotta anti-skid tile, waterproofed",
}
ROOM_LABEL_AT = {"R06": (16.2, 27.0), "R48": (21.1, 27.3), "R46": (19.0, 31.6), "R17": (59.0, 29.6), "R50": (CX, 27.4), "R09": (23.5, 22.1),
                 "R47": (25.3, 28.7), "R16S": (47.65, 29.0), "R16N": (53.9, 36.8),
                 "R31": (21.25, 12.3), "R41": (17.2, 22.1), "R36": (27.4, 37.6), "R36A": (20.0, 34.4), "R37": (40.5, 38.6), "R45": (24.0, 18.4)}  # label points for rooms whose centre is crowded
ROOM_FLOOR = {"R08": -0.04, "R07": -0.04, "R40": -0.04, "R13": -0.04, "R11": 0.25, "R18": LEVELS["thinnai"] - LEVELS["FFL"],   # foyer at the thinnai level: no lip at the main door, one 6 in step up at its 4 ft opening
              "R50": LEVELS["courtyard"] - LEVELS["FFL"], "R17": LEVELS["thinnai"] - LEVELS["FFL"],
              **{r: LEVELS["walkway"] - LEVELS["FFL"] for r in ("R51", "R61", "R62", "R63")},
              "R39": -0.04, "R33": -0.04, "R37": -0.08}  # offset from the floor level
# ceiling: ("flat", height above the room's floor level), ("sloped", note) or ("open", note) = no ceiling (skip it)
CEILINGS = {
    "R48": ("sloped", "soffit of flight 2"),
    **{r: ("flat", 9.5) for r in ("R01", "R47", "R09", "R42", "R58", "R18", "R15", "R13", "R60", "R16N", "R16S", "R16D")},
    **{r: ("flat", 8.5) for r in ("R40", "R07", "R08")},
    "R16": ("flat", 9.0),                         # the terrace slab's plastered soffit at +11'-0" (no false ceiling): slab, 1:80 falls, membrane and tile fit under the +11'-11" terrace
    "R11": ("flat", 9.0),
    "R06": ("sloped", "open to the roof (stair)"),
    "R46": ("flat", 4.5),                         # the half landing's soffit
    **{r: ("sloped", "lean-to, tiled") for r in ("R51", "R61", "R62", "R63")},
    "R50": ("open", "sky"),
    "R17": ("sloped", "exposed rafters"),
    # first floor (the west wing and the roof terrace)
    **{r: ("flat", 9.5) for r in ("R31", "R45", "R34", "R36", "R36A")},
    **{r: ("flat", 8.5) for r in ("R33", "R39")},
    "R41": ("sloped", "follows the roof (the stair chimney)"),
    "R37": ("sloped", "light tiled canopy on steel posts, open sides"),
}
SLAB_CEILINGS = {"R16"}                            # flat ceilings that are a slab's plastered soffit, not a false ceiling
_OH = 2.0                                         # roof overhang beyond the wall centre lines, all eaves
_WING = [(HX1, RING[0], HY1, HY2), (HX1, _DE, RING[3], HY2)]   # the upper wing's walls, an L: the west band, plus the family room over the den (x 27.5-33.5, y 33.5-46)
ROOF = {
    "pitch": 25,                                  # degrees: tiles need 22+; lower keeps the outer walls modest
    "overhang": _OH,                              # beyond the outer wall centre lines
    "ring": (HX1 - _OH, HX2 + _OH, HY1 - _OH, HY2 + _OH),   # outer eave outline of the single-storey ring (the ring roof stops at the wing's walls and the terrace)
    "court_eave": (CT[0] + 0.5, CT[1] - 0.5, CT[2] + 0.5, CT[3] - 0.5),  # inner eave: 6 in past the walkway edge, over the court
    # Upper wing: an L-shaped hipped roof, drawn as two hipped rectangles of the same 16.5 ft span (the roof is the higher of the two:
    # one valley at the re-entrant corner over the north walkway), 2 ft eaves all round; the east and south eaves shelter the jharokhas
    "wing_walls": _WING,
    "wing": (_WING[0][0] - _OH, _WING[0][1] + _OH, _WING[0][2] - _OH, _WING[0][3] + _OH),       # west band: x 13-29.5, y 2-48
    "wing_ext": (_WING[1][0] - _OH, _WING[1][1] + _OH, _WING[1][2] - _OH, _WING[1][3] + _OH),   # north arm over the family room: x 13-35.5, y 31.5-48 (its east eave over the terrace)
    "terrace": (_DE, _OX, RING[3], HY2),          # flat slab over the family living (no tiles), with its canopy: exactly R37
    "canopy": 7.6,                                # terrace canopy height above the terrace floor: its deck slips under the wing's east eave gutter (over x 33.5-35.5) with 2 in+ to spare
    "gutter_depth": 0.5,                          # 150 mm half-round eave gutters hang about 6 in below the eave's underside
    "grille_z": None,                             # set in geom: the court grille sits at the inner eave height
    # corners SW and NW (the wing's), the south side, the east side south of the thinnai, NE, the wing's north-east (x 33.2, 0.3 ft clear of the terrace chajja's west edge), then the terrace's;
    # each sits 0.7 ft outside the wall, under the eave (keep the DP points in PLUMBING in step)
    "downpipes": [(14.3, 3.3), (49.0, 3.3), (57.7, 15.5), (57.7, 46.7), (33.2, 46.7), (14.3, 46.7), (49.5, 46.7)],  # last: the terrace downpipe on the north wall below the parapet (no tiled eave there: the outlet pipe runs through a sleeved scupper in the parapet straight into its head)
    "upstand": 1.75,                              # RCC upstand on the terrace's SOUTH edge (parapet base under the 4 ft railing): at least 1'-9", and 6 in over the ring roof wherever the roof stands higher (geom.verge_south_h)
    "verge_south": (RING[3], RING[1], _OX, 0.5),  # SOUTH edge east of the walkway (y, x1, x2, rise): the east band's ring roof rises to its ridge here, so the upstand becomes a raking verge wall 6 in above the roof line
    "verge_east": (_OX, RING[3], HY2, 0.5),       # EAST edge: a verge wall (x, y1, y2, rise above the roof line) that follows the ring roof's profile over the console nook and the pooja, 6 in above it; see geom.verge_east_h / verge_east_max
    # South-east corner of the terrace: where the east band's ridge runs into the terrace edge, a LEVEL solid guard wall (height above the slab)
    # replaces the raking verge: on the south edge from where the raw rake first rises past the upstand (about x 45) to x 50.8, and up the east
    # edge to where the ring's north-east hip crosses it (about y 39.8); see geom.corner_guard_runs. West of it the upstand and railing, north of
    # it the raking verge and railing. The ring roof abuts it with step flashing and lead counter-flashing in a chase; the ridge end is capped into
    # the chase. Over x 44.5-50.8 (y 33.5) and y 33.5-40 (x 50.8) there is no wall below: RCC edge beams carry it.
    "corner_guard": 4.0,
    "terrace_outlet": (49.5, 45.75),              # side-entry outlet through the north parapet's foot (plumbing FT in R37): the slab falls to it; its downpipe is the last of the downpipes
    # 2 ft RCC chajja off the terrace's north edge beam at slab level (x1, x2, y1, y2): the eave of the living's north windows W75/W76; the
    # terrace downpipe drops through it in a sleeve
    "terrace_chajja": (_DE, _OX, HY2, HY2 + _OH),
    # short downpipes from the wing's courtyard-side eave gutters, discharging onto the ring roof through spreaders, clear of the jharokha bays:
    # the west band's east gutter falls south from the re-entrant corner to two, the north arm's south gutter falls east to one
    "wing_spreaders": [(RING[0] + _OH, 10.0), (RING[0] + _OH, 22.0), (_DE + 1.5, RING[3] - _OH)],
    # The wing's re-entrant corner (29.5, 31.5): a soldered internal box gutter (x, y, length, width, depth in mm, overflow spout point): the
    # wing valley's tray laps into it; it is the high point of both courtyard-side gutters, which fall 1:200 away from it to the spreaders;
    # a 50 mm overflow spout drops onto the ring's north-west valley; no downpipe at the corner
    "wing_box_gutter": (RING[0] + _OH, RING[3] - _OH, 300, 300, 150, (30.3, 30.7)),
    # the wing's courtyard-side and terrace-side gutter runs, (high end, low end): each low end is a spreader or a downpipe (the terrace-side gutter
    # falls north, turns west along the north eave and drops to the downpipe at (33.2, 46.7) on a swan-neck)
    "wing_gutter_runs": [((RING[0] + _OH, RING[3] - _OH), (RING[0] + _OH, 22.0)), ((RING[0] + _OH, 16.0), (RING[0] + _OH, 22.0)),
                         ((RING[0] + _OH, 16.0), (RING[0] + _OH, 10.0)), ((RING[0] + _OH, HY1 - _OH), (RING[0] + _OH, 10.0)),
                         ((RING[0] + _OH, RING[3] - _OH), (_DE + 1.5, RING[3] - _OH)),
                         ((_DE + _OH, RING[3] - _OH), (_DE + _OH, HY2 + _OH)), ((_DE + _OH, HY2 + _OH), (33.2, HY2 + _OH))],
    # the ring's south gutter (x 29.5-59, east of the wing) drains to its one downpipe at x 49 (the other south downpipe, at x 14.3, is the wing's
    # south-west corner); a second one near x 31-34 would cross four soil and grey runs and their chambers in the south pipe strip (y 1.2-2.8),
    # so there is none: the gutter is the standard 150 mm, and the engineer checks the run (or upsizes it to 200 mm)
    "ring_south_gutter_mm": 150,
    # Thinnai lean-to: the ring's east slope carried on over the thinnai at the same pitch from the east wall to its own eave 1'-6" past the pillars
    # (x 61.25), 9 in past the platform edge; y one ft past the platform each end; its eave gutter feeds the two rain chains (F125, F126)
    "thinnai": (HX2, 62.75, 23.0, 35.0),
    "thinnai_build_up": 0.35,                     # tiles, battens and exposed rafters: clear headroom is measured under it
    "jharokha_kerb": 0.5,                         # each jharokha bay stands on a 6 in flashed kerb over the walkway roof (back-gutter and saddle up-slope, apron down-slope)
    # the bays have no roofs of their own: each teak frame is carried up to the wing's eave soffit and closed with a timber soffit board sealed
    # to the fascia (the 2 ft eave is the bay's roof); the gutter hangs outboard on fascia brackets, its bottom 2 in+ above the casement heads
    "jharokha_to_soffit": True,
    "jharokha_head": 7.5,                         # casement head above the first floor
    # Valley saddles (crickets): bay 2 (the family room's, facing south) sits on the ring roof's north-west inner valley. The pocket between the
    # wing's east wall and the bay's west kerb is a lead-lined pocket gutter, up to the kerb top, falling south past J2's south-west kerb corner
    # to the valley at (29.5, 31.5).
    # (bay index, x1, x2, y1, y2, height above the roof at the kerb)
    "saddles": [(1, RING[0], 29.5, RING[3] - 2.0, RING[3], 0.5)],
}

# The utility's service steps (Group B): a level landing 3 ft deep outside the south service door D18 (it opens inward), one riser below the
# utility floor (outside 3-6 in lower: rain stays out), then the other risers down along the wall to the east, on 10 in+ treads, with a grab
# rail on the wall. The flight sits over the south strip's buried lanes (sleeved there); the kitchen line's chamber IC-22 stands east of it.
SERVICE_STEPS = {
    "door": "D18",
    "landing": (39.75, 43.0, HY1 - T / 2 - 3.0, HY1 - T / 2),   # x 39.75-43.0 along the wall (the 2'-6" door and a foot past its latch), 3'-0" deep
    "risers": 4,                                  # from the utility floor (wet_area) to the ground: about 5.9 in each
    "tread": 0.9,                                 # 10.8 in going
    "rail_z": 2.75,                               # SS grab rail on the wall, 2'-9" above the nosings, 1 ft past the bottom riser
}
_SS = SERVICE_STEPS
_SS["x_end"] = round(_SS["landing"][1] + (_SS["risers"] - 2) * _SS["tread"], 3)   # the bottom riser: the landing takes one riser, the flight the rest
_SS_R = LEVELS["wet_area"] / _SS["risers"] * 12

# Site features: id, label, kind ("rect"/"circle"), geometry (x1, x2, y1, y2) or (x, y, r)
SITE_FEATURES = [
    ("SPARE", "Back garden, 15 ft behind the house: herb and kitchen beds, the rotary airer, the den's engawa deck under the pergola", "rect", (0.3, 12.0, 0.3, 49.7)),
    ("OTTA", "Engawa: a raised teak deck 2'-7\" wide and 1'-6\" high under the creeper pergola, along the den niche's and den bath's west wall outside the garden door (one 6 in step down from the den); sit on its edge, feet on the grass, over the herb beds at sunset; slatted, on laterite piers", "rect", (12.0, 14.6, 33.5, 44.0)),
    ("GSTEP", "Two stone steps from the north end of the engawa down to the garden (the deck's south end is the level landing under the garden door's outward swing)", "rect", (12.0, 14.6, 44.0, 46.0)),
    ("PERGOLA", "Creeper pergola over the engawa along the den's west wall (no big trees near walls)", "rect", (12.2, 14.4, 36.0, 44.0)),
    ("PARIJAT", "Parijat (night-flowering jasmine) at the forecourt's north edge: white flowers on the stone at dawn", "circle", (74.0, 42.0, 1.2)),
    ("JASMINE", "Jasmine (mulla) planted 2'-6\" off the thinnai's north-east pillar, beside the platform's north edge, and trained up the pillar and along its beam: scent on the thinnai at dusk", "circle", (61.25, 34.5, 0.4)),
    ("TULSI", "Tulsi thara on the door axis in the forecourt", "circle", (70.0, 29.0, 0.6)),
    ("PATH", "Stone-paved forecourt in front of the thinnai and its steps, round the tulsi thara", "rect", (64.0, 82.0, 26.0, 40.0)),
    ("CARPORT", "Car porch 18 x 10 ft at the end of the drive on the north side, under a steel pergola grown with vegetable creepers (bottle, ridge and bitter gourd, flat beans) for shade and food (two-wheelers alongside)", "rect", (84.0, 102.0, 34.0, 44.0)),
    ("PATH2", "Stone path from the forecourt's north-east corner to the car porch", "rect", (82.0, 84.0, 35.0, 40.0)),
    ("DRIVE", "Drive 10 ft wide, 6 ft off the north boundary, from the road gate in the north-east to the car porch (vastu: the way in on the right as you face the house), gravel with paver wheel strips", "poly", (102.0, 130.0)),
    ("GATE", "Sliding gate 12 ft at the north-east of the road front with a 3 ft wicket for people", "rect", (129.5, 130.0, 33.0, 46.0)),
    ("SEPTIC", "Septic tank, 2 chambers, sealed RCC, 6 x 4 ft, south-east of the forecourt behind a hedge (never in the north-east quadrant); the tanker stops at the drive's west end beside the car porch and its hose runs about 18 ft south-west, between the car porch and the vegetable strip and past the hedge's east end, to the tank: keep that line free of beds and trees", "rect", (83.0, 89.0, 17.0, 21.0)),
    ("SOAK", "Lined soak pit for septic effluent and bath grey water (the kitchen's grey water goes to the banana circle), on the south side about 19 ft from the house wall and 60 ft+ from the borewell", "circle", (78.0, 4.0, 1.6)),
    ("HEDGE1", "Hedge screening the septic tank from the forecourt", "rect", (82.5, 89.5, 21.2, 22.0)),
    ("RECHARGE", "Rainwater recharge pit (roof run-off), between the workshop and the shops", "rect", (110.5, 115.5, 12.0, 17.0)),
    ("HERBS", "Kitchen garden (permaculture zone 1) south of the forecourt, a few steps from the kitchen: daily greens (gongura, thotakura, palak, methi) in a mulched bed round a herb spiral", "rect", (62.0, 74.0, 1.0, 17.0)),
    ("SPIRAL", "Herb spiral, 5 ft across and 3 ft high, laterite rubble and soil: curry leaf, mint, coriander, tulsi, lemongrass, chilli (dry-loving herbs at the top, mint at the wet foot)", "circle", (68.0, 9.0, 2.2)),
    ("BANANA", "Banana circle on the kitchen's grey water (a grease trap, then a pipe to a 3 ft mulch pit filled with straw and leaves): banana, papaya and colocasia round it; no septic effluent", "circle", (86.5, 4.0, 2.8)),
    ("GUILD", "Fruit guilds (permaculture zone 2) east of the septic tank and the workshop: guava, sapota, lemon, pomegranate, custard apple and a drumstick tree, each ringed with pigeon pea, chilli and brinjal, sweet potato or pumpkin as ground cover and turmeric and ginger in the shade; mulched and on drip; no big-rooted trees (mango, jamun) near the house or the septic tank", "rect", (104.0, 115.5, 18.0, 25.0)),
    ("VEG", "Vegetable garden (permaculture zone 2) on the sunny south side: raised beds 4 ft wide on 6 ft centres with 2 ft paths, built up with compost, red soil and sand over the black cotton soil (never dug in), a thick straw mulch and drip lines fed from the sump; crops rotated (tomato, okra, beans, onion, greens); a 35-50% shade net on GI hoops over the beds in April-May; a row of fruit trees along the drive to the north (canopies kept off the beds and the drive); more beds on the north strip east of the sump", "rect", (98.0, 128.0, 25.6, 29.6)),
    ("COMPOST", "Two compost pits, beside the banana circle and the soak pit, south of the septic tank: kitchen scraps, leaves and the living-fence cuttings go back to the beds", "rect", (80.0, 83.0, 6.0, 9.5)),
    ("WORM", "Worm bin (vermicompost), shaded, beside the compost pits", "rect", (80.5, 83.0, 10.0, 12.5)),
    ("FENCE", "Living fence along the south boundary inside the compound wall: gliricidia and pigeon pea, cut back three or four times a year and the cuttings dropped on the beds as mulch and nitrogen; shelters the beds from the hot west wind", "rect", (62.0, 126.0, 0.2, 0.9)),
    ("WORKSHOP", "Carpentry workshop 16 x 12 ft, built cheap and demountable: bolted steel frame (galvanised SHS posts on pad footings with anchor bolts), precast RCC post-and-panel walls (the compound-wall system: panels lift out), an insulated metal sandwich roof screwed to steel purlins, a PCC floor on compacted fill; every part unbolts or lifts out for reuse; 3-phase power on a surface-run sub-board, 8 ft double doors on the steel frame, dust extraction, a lockable timber store at the west end", "rect", (93.0, 109.0, 1.0, 13.0)),
    ("WVERANDAH", "Covered work verandah 16 x 4 ft on the north side, for unloading and working timber; the roof sheet carried on to extra steel posts, a paver floor (lifts out)", "rect", (93.0, 109.0, 13.0, 17.0)),
    ("SUMP", "Sump in the north-east quadrant on the north strip beside the forecourt (2 ft+ from the boundary): it takes the roof and courtyard rain through the first-flush filter and is topped up from the road main by a buried pipe; it feeds the house tanks (by pump) and the drip lines of the beds", "rect", (66.0, 72.0, 44.5, 48.0)),
    ("BORE", "Borewell (if any), north-east corner beyond the drive (vastu), about 64 ft from the soak pit and about 47 ft from the septic tank's nearest edge (51 ft centre to centre: a little under the usual 15 m, to confirm with the engineer)", "circle", (127.5, 48.0, 0.5)),
    ("SHOPS", "Two small rental shops on the road front in the south-east, built cheap and demountable (bolted steel frame, precast post-and-panel walls, an insulated sheet roof); they face the road directly and their rear doors open to the yard they share with the workshop; own meters; the toilet is shared with the workshop", "rect", (116.0, 130.0, 1.0, 25.0)),
    ("SHOP1", "Rental shop 1, 14 x 12 ft, a rolling shutter bolted to the steel frame under a 1'-6\" sheet canopy, a rear door to the work yard", "rect", (116.0, 130.0, 1.0, 13.0)),
    ("SHOP2", "Rental shop 2, 14 x 12 ft, a rolling shutter bolted to the steel frame under a 1'-6\" sheet canopy, a rear door to the work yard", "rect", (116.0, 130.0, 13.0, 25.0)),
    ("SITEWC", "Shared toilet for the workshop and the shops: a ready-made FRP cabin (WC and basin) in the yard between them, door to the north (the drive side); a sealed pipe to the main septic tank; it lifts out for reuse", "rect", (110.5, 115.0, 6.0, 11.0)),
    ("STEPS", "Entrance steps (3 risers) down from the thinnai on the door axis, SS handrails on both sides (F148, F149)", "rect", (62.0, 64.0, 27.0, 31.0)),
    ("RAMP", "Reserved ramp to the thinnai for a walker or wheelchair later: 1:12, 4 ft wide, about 18 ft long for a 1'-6\" rise, with a 4 x 4 ft level landing at the thinnai's south edge; keep it and the 4 ft opening in the thinnai's south edge clear: no thinnai pillar, planting or building there; the steps stay as they are", "rect", (58.0, 80.0, 20.0, 24.0)),
    ("FEET", "Foot-wash tap + drain", "circle", (65.8, 32.4, 0.35)),
    ("WSTEP", f"Service landing 3'-0\" deep outside the utility's south door D18, one {_SS_R:.1f} in riser below the utility floor, then {_SS['risers'] - 1} more risers of {_SS_R:.1f} in on {_SS['tread'] * 12:.1f} in treads down along the wall to the east ({_SS['risers']} risers in all), with an SS grab rail on the wall 2'-9\" above the nosings (Group B); laterite, granite treads", "rect", (_SS["landing"][0], _SS["x_end"], _SS["landing"][2], _SS["landing"][3])),
    ("APRON", "Plinth protection apron 3 ft, sloped away", "apron", (HX1 - 3, HX2 + 3, HY1 - 3, HY2 + 3)),
]
# Fruit guild trees and bananas (x, y, canopy radius, kind), kept 25 ft+ from the house and 9 ft+ from the septic tank
FOOD_TREES = [(106.5, 20.3, 2.0, "guava"), (112.8, 22.2, 2.4, "sapota"), (110.0, 19.3, 1.5, "lemon"), (109.0, 24.0, 1.3, "pomegranate"),
              (106.0, 23.7, 1.6, "custard apple"), (114.2, 18.8, 1.3, "drumstick")] + [(round(86.5 + 2.8 * c, 2), round(4.0 + 2.8 * s, 2), 1.1, k) for c, s, k in
              ((1, 0, "banana"), (0, 1, "banana"), (-1, 0, "papaya"), (0.6, -0.8, "banana"), (-0.6, 0.8, "banana"))]
TREES = [(float(x), 31.8, 1.9) for x in (108, 114, 120, 126)] + [(80.5, 41.5, 3.2), (100.0, 47.5, 1.8), (121.0, 47.5, 1.8)]  # a fruit-tree row south of the drive (canopies clear of the drive and the beds); a neem at the forecourt's north-east corner (15 ft+ from the house); two coconut palms in the north strip beyond the car porch, 25 ft+ from the house and 9 ft+ from the septic tank
JALI_SCREENS = []  # free-standing timber jali screens (none on the courtyard house's ground floor)
FUTURE_WALLS = []

# Doors: id, axis, c, s, e, swing (+1 toward +y/+x, -1 toward -y/-x, 0 = sliding), name, type
DOORS = [
    # main entrance and the foyer's neighbours
    ("D01", "Y", HX2, 27.0, 31.0, -1, "Main entrance, 4 ft, on the east wall in its north half (thinnai, door, foyer and the family room on one line; the step and grab post sit at the foyer's 4 ft opening)", "Teak panelled, double leaf, carved and brass-studded, jali panel above: the widest and tallest threshold in the house"),
    ("D11", "Y", _OX, 41.5, 44.5, 1, "Pooja (north-east corner; opens inward from the family room, so you stand facing east, towards the idols)", "Carved teak, double leaf (opens inward, clear of the family room; faces west, the family faces east)"),
    # master suite: the bedroom door is off the west walkway, the bath opens outward into the bedroom
    ("D04", "Y", RING[0], 17.0, 19.9, -1, "Master bedroom (from the west walkway, opens inward, 2'-10\"), the walkway is only 3'-1\" clear so the leaf never swings out", "Flush, teak veneer"),
    ("D42", "Y", RING[0], 11.0, 13.75, -1, "Master bath (from the bedroom, 2'-9\", opens outward into the bedroom so a fall behind it never blocks it; the basin and mirror face you across the room on the east wall, the WC is round the corner on the north wall)", "Flush, waterproof (WPC/FRP), lift-off hinges, emergency-release lock"),
    # stair lobby, DB and linen cupboard, low store
    ("D09", "Y", RING[0], 20.75, 23.55, 0, "Stair lobby door off the west walkway (surface-mounted, sliding on the walkway face and parking north over the den walk-in's wall): the stair and the upstairs stay one closable AC zone", "Teak frame with a carved teak jali sliding leaf and a glazed sliding sash behind it on a concealed top track; key lock from the walkway side, thumb-turn (no key) from the lobby side so nobody is ever locked in"),
    ("D48", "X", _GFOOT, 19.95, 22.3, 1, "DB and linen cupboard (from the stair lobby, opens inward into the cupboard, hinged at its west jamb; the full-height front of the cupboard under flight 2)", "Flush, teak veneer, louvred top; lockable (the distribution board is behind it)"),
    ("D46", "X", _GLAND, 20.0, 22.0, -1, "Low store hatch (from the DB and linen cupboard into the store under the half landing, a 3'-6\" high hatch, bend to enter; opens into the cupboard)", "Plywood hatch leaf, ventilated, 2'-0\" wide x 3'-6\" high, brass bolt"),
    # den, its walk-in, bath and garden door
    ("D02", "X", RING[3], 29.0, 32.0, 1, "Den / guest room (from the north walkway, opens inward), 3 ft", "Flush, teak veneer"),
    ("D47", "X", RING[3], 23.5, 26.0, -1, "Den walk-in wardrobe (from the den, opens inward into the walk-in, hinged at its east jamb)", "Flush, teak veneer, louvred top"),
    ("D07", "Y", _DX, 41.3, 44.3, 1, "Den bath (from the den, 3'-0\", opens outward into the den on lift-off hinges; the basin and mirror face you across the room on the west wall, the WC and the shower are off the door line)", "Flush, waterproof (WPC/FRP), lift-off hinges, emergency-release lock"),
    ("D45", "Y", HX1, 34.0, 36.5, -1, "Garden door from the den niche onto the engawa deck on the west (glazed, hinged, opens outward onto the deck so it never sweeps the desk; the fixed side light W72 beside it; one 6 in step down outside)", "Teak frame, glazed hinged leaf opening outward on lift-off hinges with a hold-open stay, a pleated mosquito mesh in the frame, multipoint lock"),
    # powder room, kitchen, utility, pantry
    ("D08", "X", RING[2], 35.05, 37.8, 0, "Powder room (from the south walkway, 2'-9\" clear, sliding on the walkway face and parking west, so no leaf swings into the walkway or the WC zone; the first view is the basin and mirror on the south wall, the WC is off the door line)", "Flush, waterproof (WPC/FRP) sliding leaf on a surface track, soft-close, privacy lock"),
    ("D17", "X", _KY, 46.0, 49.0, 0, "Kitchen entry from the dining end (sliding on the dining face, parking east), 3 ft", "Teak frame, reeded-glass sliding door (closes off cooking smoke; guests see no kitchen mess)"),
    ("D12", "Y", _QX, 5.6, 8.1, 1, "Kitchen to utility (opens into the kitchen, hinged at its south jamb, clear of the service door's swing)", "Steel or WPC, hinged, lockable"),
    ("D64", "Y", _QX, 10.5, 13.0, 0, "Pantry (from the kitchen, sliding on the pantry face and parking north: the kitchen face has only 2'-3\" of wall before the corner), 2'-6\"", "Teak frame, reeded-glass sliding door"),
    ("D18", "X", HY1, 40.25, 42.75, 1, "Utility service door on the south wall (opens inward, onto the landing and steps)", "Steel, lockable, louvred top"),
]
# Teak-and-glass folding doors on the courtyard-side walls of the family room: the living to the north walkway (y 33.5) and
# the dining end and oonjal link to the east walkway (x 44.5). Each set sits inside one room-to-walkway edge, with short wall
# piers between. Swing 0 = they fold and stack clear of the opening.
_FOLD = "Teak frame, toughened glass, folding (bi-fold) panels on a top track and a flush floor channel: stack open to the pier in the day, bolt shut at night"
for _id, _axis, _c, _where, _spans in (
        ("D60", "X", RING[3], "Family living to the north walkway", [(34.4, 39.0), (39.6, 44.0)]),
        ("D62", "Y", RING[1], "Dining end and oonjal link to the east walkway", [(17.0, 19.9), (20.3, 24.7), (25.3, 29.7), (30.3, 33.0)])):
    for _i, (_a, _b) in enumerate(_spans):
        DOORS.append((_id if _i == 0 else _id + "bcd"[_i - 1], _axis, _c, _a, _b, 0,
                      f"{_where}: folding teak-and-glass doors, set {_i + 1} of {len(_spans)} (borrowed light for the room, air from the courtyard)", _FOLD))
DOOR_HEIGHTS = {"D46": 3.5}   # doors lower than the 7'-0" lintel band: the low store's hatch
# Vents above inner doors (7'-6" to 9'-0", above the lintel band): air moves between rooms with doors shut
TRANSOM_TYPES = {
    "jali": "Teak jali vent in a frame: air passes freely (rooms with no sound-privacy need)",
    "jali_closable": "Teak jali with a sliding timber shutter on the room side: open for air, shut for sound privacy",
    "louvre": "Fixed louvres angled down: air for the exhaust fan, no view in",
    "glazed": "Top-hung glazed vent with seals: open for air, closed for calls",
}
TRANSOMS = {"D11": "jali", "D01": "jali", "D02": "jali_closable", "D42": "louvre", "D04": "jali_closable", "D07": "louvre", "D08": "louvre",
            "D47": "louvre", "D48": "louvre", "D12": "jali",
            "D51": "jali_closable", "D36": "jali_closable", "D39": "louvre"}  # first floor: rooms breathe into the stair head and gallery with doors shut
HINGE_AT_END = {"D47"}  # doors hinged at their far (e) jamb
TRANSOM_LABELS = {"jali": "Open jali", "jali_closable": "Closable jali", "louvre": "Louvres", "glazed": "Sealed glazed flap"}
TRANSOM_Z = (7.5, 9.0)  # sill and head above the floor

# Windows: id, axis, c, s, e, sill, head, room, type (sill and head above the floor the window serves)
WINDOWS = [
    # south wall y 4: small, deep sills and jali against the sun
    ("W60", "X", HY1, 15.7, 17.2, 3, 6.5, "Master bedroom", "Small timber jali + glazed shutters west of the bed head, 9 in deep sill (south: small against the sun); inner jamb clear of the bedside shelf"),
    ("W61", "X", HY1, 25.3, 26.8, 3, 6.5, "Master bedroom", "Small timber jali + glazed shutters east of the bed head, 9 in deep sill; inner jamb clear of the bedside shelf"),
    ("W62", "X", HY1, 29.3, 31.3, 5, 7, "Master bath", "Frosted casement, top-hung (2 ft bath window) over the shower end; its upper pane takes the exhaust fan (outer wall)"),
    ("W64", "X", HY1, 35.5, 37.5, 3.5, 7, "Utility", "Jali vent over the utility sink (2 ft vent window); the exhaust fan fits in its upper pane (outer wall)"),
    ("W82", "X", HY1, 50.2, 54.0, 3.5, 7, "Kitchen", "Timber jali + glazed shutters (3'-10\") over the prep sink, the sink centred under it, herbs on the sill; the kitchen's prep window on its south outer wall, clear of the south downpipe"),
    # west wall x 15: small, jali or frosted
    ("W66", "Y", HX1, 8.0, 10.0, 3, 6.5, "Master bedroom", "Small timber jali + glazed shutters, deep sill (west: small against the evening sun; the back garden shades it)"),
    ("W67", "Y", HX1, 14.5, 16.5, 3, 6.5, "Master bedroom", "Small timber jali + glazed shutters beside the reading chair, deep sill"),
    ("W88", "Y", HX1, 21.3, 23.3, 3, 6.5, "Stair lobby", "Small timber jali + glazed shutters, deep sill (west: small against the evening sun): daylight for the stair foot"),
    ("W69", "Y", HX1, 24.3, 26.8, 5.5, 7.5, "Stair", "Deep-sill teak casement with a jali leaf over the first flight, small and high against the west sun (3 ft or more above the treads at its widest)"),
    ("W70", "Y", HX1, 30.0, 32.0, 8.0, 9.5, "Stair", "Glazed clerestory over the half landing (the landing is 5'-0\" up, so the sill is 3'-0\" above it and nobody can fall through), top-hung, with a deep sill for a lamp: the hot-air outlet of the stair"),
    ("W71", "Y", HX1, 32.3, 33.1, 1.5, 2.5, "Low store", "Fixed louvre vent, low (air for the store under the landing)"),
    ("W72", "Y", HX1, 36.75, 37.75, 1.0, 7, "Den niche", "Fixed glazed side light (1 ft) beside the garden door, a teak jali in its lower part: daylight on the desk"),
    ("W68", "X", HY2, 19.45, 21.45, 5, 7, "Den bath", "Frosted casement, top-hung (2 ft), on the north outer wall over the WC; its upper pane takes the exhaust fan"),
    # north wall y 46: the cool side, larger
    ("W73", "X", HY2, 23.0, 25.0, 3, 7, "Den", "Teak casement, glazed (2 ft), jali lower leaf: north light"),
    ("W74", "X", HY2, 26.5, 31.0, 3, 7, "Den", "Teak casement, glazed (4'-6\"), jali lower leaf: north light for the den's reading corner"),
    ("W75", "X", HY2, 35.5, 40.5, 2.5, 7, "Family living", "Teak casement, glazed (5 ft), jali lower leaf; the diwan sits under it"),
    ("W76", "X", HY2, 43.0, 48.0, 2.5, 7, "Family living", "Teak casement, glazed (5 ft), jali lower leaf; the diwan sits under it"),
    ("W84", "X", HY2, 53.0, 55.0, 3, 6.5, "Pooja", "Small timber jali + glazed flap (2 ft) on the north wall: soft light on the idols"),
    # east wall x 57
    ("W63", "Y", HX2, 16.9, 19.9, 2.5, 7, "Dining end", "Timber jali + glazed shutters (3 ft) over the dining bench, jali lower leaf: the forecourt in the morning light"),
    ("W65", "Y", HX2, 20.9, 23.9, 2.5, 7, "Dining end", "Timber jali + glazed shutters (3 ft) over the dining bench, jali lower leaf"),
    ("W80", "Y", HX2, 25.65, 26.8, 3, 6.5, "Foyer", "Tall fixed jali slit (1'-2\") south of the main door, onto the thinnai, over the shoe bench"),
    ("W81", "Y", HX2, 31.2, 32.85, 3, 6.5, "Foyer", "Fixed jali + glazed shutter (1'-8\") north of the main door, onto the thinnai: a view of who is outside"),
    ("W78", "Y", HX2, 35.2, 38.2, 3, 6.5, "Console nook", "Timber jali + glazed shutters (3 ft): the forecourt seen from the oonjal or the console"),
    ("W79", "Y", HX2, 42.0, 44.0, 7.5, 8.75, "Pooja", "High vent above the mandapam (lamp smoke out at the ceiling), jali + glazed flap"),
    ("W83", "Y", HX2, 9.0, 11.5, 6.5, 8.5, "Kitchen", "High ventilator, jali + louvres above the hob (smoke and hot air out; the hob wall below stays solid); the cooker-hood duct and fan go through it"),
    # on the south walkway wall (the 9 in wall under the walkway roof, open to the courtyard's sky): high vents for the two inner rooms
    ("W86", "X", RING[2], 38.3, 39.2, 7.0, 8.0, "Powder room", "High louvre vent onto the open walkway (the walkway is open to the courtyard and the sky): the powder room's exhaust position (it has no outer wall; the duct could instead run through the utility to the south wall)"),
    ("W87", "X", RING[2], 41.0, 42.5, 6.5, 8.0, "Pantry", "High ventilator, jali + louvres (the pantry stays dark and cool)"),
]
OTHER_OPENINGS = []  # cased openings are plain gaps in WALLS (see the ground-floor wall notes)
# Teak or stone pillars: round the courtyard (corners and mid-points of its edges) and along the thinnai's front edge
PILLAR_R = 0.375   # walkway pillars: 9 in round teak on stone bases, set into the court by their radius so the walkway stays its full clear width
_PI = (CT[0] + PILLAR_R, CT[1] - PILLAR_R, CT[2] + PILLAR_R, CT[3] - PILLAR_R)
WALKWAY_PILLARS = [(_PI[0], _PI[2]), (CX, _PI[2]), (_PI[1], _PI[2]), (_PI[0], CY), (_PI[1], CY), (_PI[0], _PI[3]), (CX, _PI[3]), (_PI[1], _PI[3])]
THINNAI_PILLARS = [(61.25, 26.0), (61.25, 32.0)]   # turned teak, 9 in in from the platform edge, 1 ft either side of the 4 ft steps (y 27-31), symmetric about the door axis y 29; the ramp opening x 58-62 on y 24 stays clear
PILLARS = WALKWAY_PILLARS + THINNAI_PILLARS

# Furniture: id, room, item, x1, x2, y1, y2, qty, material / spec, shape ("rect"|"circle"|"wc"|"glass")
# Group B (owner-approved): a 600 mm grab rail beside every WC and in the master and den showers, fold-down shower seats,
# a reading chair in the master, handrails both sides of the entrance steps, a grab post at the foyer step, a 16 in dining
# bench and a dining armchair. Wall-hung rails and seats are drawn as thin rects on the wall face.
_GRAB = "SS 304, 32 mm, satin, fixed to the wall with concealed flanges into solid blocking (takes 150 kg)"
_SEAT = "Teak slats on an SS frame, wall-hinged, folds up flat; seat 1'-6\" above the floor"
# the thinnai's rain-chain basins (F125, F126) on the lean-to's eave line (ROOF["thinnai"]): the north one under the eave's north-east corner, the
# south one as near its south-east corner as the reserved ramp allows (the corner itself stands over the ramp)
_BAS_X = ROOF["thinnai"][1]
_BAS_S = max(ROOF["thinnai"][2], next(f[3][3] for f in SITE_FEATURES if f[0] == "RAMP"))
FURNITURE = [
    # ---- master suite (SW): bed head south between the windows, wardrobe and dressing table in the bedroom, hotel-style bath ----
    ("F10", "Master bedroom", "King bed 6' x 6'6\" + headboard, head to the south wall between two windows (the south-west corner of the house), bed head centre on x 21.25", 18.25, 24.25, 4.375, 10.875, 1, "Teak, head to south", "rect"),
    ("F11", "Master bedroom", "Floating bedside shelf with a drawer, reading light and charging point above (against the south wall, beside each window jamb)", 17.25, 18.25, 4.375, 5.375, 2, "Teak, wall-hung", "rect"),
    ("F06", "Master bedroom", "Built-in wardrobe 8'-0\", full height with lofts, along the bedroom's north wall", 15.375, 23.4, 18.03, 20.03, 1, "Ply + laminate, sliding shutters, acoustic board at the back", "rect"),
    ("F19", "Master bedroom", "Dressing table with a mirror and drawers on the east wall, between the bath door and the bedroom door", 25.6, 27.125, 14.0, 16.8, 1, "Teak", "rect"),
    ("F138", "Master bedroom", "Reading chair beside the west window W67, its back to the west wall (daylight over the shoulder), a footstool and a reading lamp beside it", 15.375, 17.375, 13.6, 15.6, 1, "Teak frame, cane, cotton cushion", "rect"),
    ("F12", "Master bath", "WC (EWC) on the north wall in the north-west corner, round the corner from the door and out of the mirror's view (the mirror faces west on the east wall)", 28.6, 30.0, 14.3, 16.125, 1, "Wall-hung, concealed cistern", "wc"),
    ("F140", "Master bath", "Grab rail beside the WC: 600 mm L (a horizontal leg at 2'-9\" and a vertical leg), on the west wall", 27.875, 27.995, 14.15, 16.12, 1, _GRAB, "rect"),
    ("F13", "Master bath", "Glass screen of the walk-in shower across the south end (4'-0\" x 3'-6\"), open at the east end onto the dry corner (never toward the WC or the door), a linear drain along the south wall", 27.875, 31.875, 7.875, 8.0, 1, "8 mm toughened glass", "glass"),
    ("F142", "Master bath", "Fold-down shower seat 1'-4\" x 1'-2\" on the shower's west wall", 27.875, 29.125, 5.0, 6.4, 1, _SEAT, "rect"),
    ("F141", "Master bath", "Grab rail in the shower: 600 mm L on the south wall beside the seat, under the window", 29.3, 31.27, 4.375, 4.495, 1, _GRAB, "rect"),
    ("F14", "Master bath", "Wash basin on the east wall, straight opposite the door (the first thing you see), mirror cabinet recessed 4 in into the wet wall above with a light over it", 32.71, 34.21, 11.625, 13.125, 1, "Wall-hung", "rect"),
    # ---- powder room ----
    ("F16", "Powder room", "WC (EWC) on the east wall (you sit facing west), past the door line, 2 ft clear of the basin, never in the mirror's view", 37.39, 39.39, 11.25, 12.65, 1, "Wall-hung on the wet wall, concealed cistern", "wc"),
    ("F146", "Powder room", "Grab rail beside the WC: a 600 mm swing-up rail on the back wall on the WC's south side (folds up against the wall)", 37.42, 39.39, 10.53, 10.65, 1, _GRAB, "rect"),
    ("F17", "Powder room", "Wash basin on the south wall straight opposite the door, a mirror and a feature tile panel above it, a light over the mirror", 35.5, 36.9, 9.79, 11.19, 1, "Wall-hung", "rect"),
    # ---- den (guest room), its niche and walk-in ----
    ("F20", "Den (guest room)", "Sofa-cum-bed 6' x 3' against the den's east wall, facing the TV on the west wall about 7 ft away; a 4 ft path stays clear from the door to the bath door and the niche", 30.125, 33.125, 37.4, 43.4, 1, "Teak, cotton mattress and bolsters", "rect"),
    ("F67", "Den (guest room)", "Armchair facing the TV (about 8 ft from it), north of the sofa-bed", 31.2, 33.0, 43.6, 45.4, 1, "Teak frame, cane, cotton cushion", "rect"),
    ("F66", "Den (guest room)", "Coffee table 2 ft x 1 ft 6 in between the sofa-bed and the TV", 27.6, 29.1, 39.4, 41.4, 1, "Teak", "rect"),
    ("F23", "Den (guest room)", "Media wall on the den's solid west wall between the niche and the bath door (not back to back with the family living's TV; an acoustic board lining on battens behind the TV, against the bath): a 40 in TV, a floating console", 22.29, 22.9, 38.6, 41.1, 1, "Teak veneer, cable conduit to the TV point", "rect"),
    ("F117", "Den walk-in", "Guests hanging wardrobe 6 ft x 1'-9\" along the walk-in's east wall, clear of the door's swing, a 2 ft aisle in front", 25.375, 27.125, 24.4, 30.6, 1, "Ply + laminate, teak veneer shutters", "rect"),
    ("F132", "Den niche", "Writing desk 4'-6\" along the niche's north wall, lit by the garden door's side light W72, drawers to one side, a task light", 17.0, 21.5, 36.51, 38.01, 1, "Teak, leather inlay top", "rect"),
    ("F133", "Den niche", "Task chair at the writing desk, drawn parked beside the desk under the side light (2'-9\" clear to the garden door)", 15.45, 16.85, 36.55, 37.95, 1, "Teak frame, cane seat", "rect"),
    # ---- den bath ----
    ("F48", "Den bath", "WC (EWC) on the north wall in the north-east corner (you sit facing south), past the door's line and out of the mirror's view", 19.75, 21.15, 43.8, 45.625, 1, "Wall-hung, concealed cistern", "wc"),
    ("F143", "Den bath", "Grab rail beside the WC: a 600 mm swing-up rail on the back wall on the WC's west side (folds up against the wall)", 19.05, 19.17, 43.65, 45.62, 1, _GRAB, "rect"),
    ("F49", "Den bath", "Wash basin on the west wall, straight opposite the door, a mirror cabinet recessed 4 in into the wall above with a light over it", 15.375, 16.875, 42.05, 43.55, 1, "Wall-hung", "rect"),
    ("F50", "Den bath", "Fixed glass panel of the walk-in shower in the south-west corner (3'-1\" x 3'-0\", open to the east onto the blank south-east wall): keeps the spray off the basin", 15.375, 18.5, 41.6, 41.72, 1, "8 mm toughened glass", "glass"),
    ("F151", "Den bath", "Glass return on the shower's east side, so its 2'-7\" opening faces the blank wall (never the door or the WC)", 18.5, 18.62, 41.2, 41.72, 1, "8 mm toughened glass", "glass"),
    ("F145", "Den bath", "Fold-down shower seat 1'-4\" x 1'-2\" on the shower's west wall", 15.375, 16.625, 39.2, 40.6, 1, _SEAT, "rect"),
    ("F144", "Den bath", "Grab rail in the shower: 600 mm L on the south wall beside the seat", 16.75, 18.4, 38.59, 38.71, 1, _GRAB, "rect"),
    # ---- dining end of the family room ----
    ("F24", "Dining end", "Dining table 5'-6\" x 2'-6\" running north-south beside the bench, apron set back so the stools slide under (4 daily: two on the bench, two on stools on the west side, the armchair at the south end; extends to about 7'-6\" with stools for festivals, 8 seats)", 52.6, 55.1, 17.25, 22.75, 1, "Teak, extending", "rect"),
    ("F27", "Dining end", "Backless stool 1'-4\" square on the west side, slides fully under the table when not in use (drawn just clear of the table), so nothing stands in the kitchen path", 51.2, 52.53, 18.0, 19.33, 1, "Teak, woven cane seat", "rect"),
    ("F116", "Dining end", "Backless stool 1'-4\" square on the west side, slides fully under the table when not in use (drawn just clear of the table)", 51.2, 52.53, 20.6, 21.93, 1, "Teak, woven cane seat", "rect"),
    ("F28", "Dining end", "Built-in bench 16 in deep on the dining end's east wall under the windows, storage below; a 1'-6\" lane to its north end past the hand-wash basin (the table extends for festivals)", 55.29, 56.625, 16.9, 22.6, 1, "Teak, cushion", "rect"),
    ("F25", "Dining end", "Dining armchair at the table's south end (arms to push up on), clear of the kitchen path", 52.95, 54.75, 15.75, 17.25, 1, "Teak, cane seat and back", "rect"),
    ("F33", "Kitchen", "Granite serving ledge 9 in deep on the kitchen face of the dining wall, beside the sliding door: dishes go out to the dining end", 49.3, 52.0, 14.54, 15.29, 1, "Granite top on brackets", "rect"),
    ("F44", "Kitchen", "Water / RO and crockery counter 1'-9\" deep on the kitchen's north wall between the serving ledge and the fridge, glass-shuttered crockery below", 52.0, 54.375, 13.54, 15.29, 1, "Granite top, teak + glass", "rect"),
    ("F21", "Dining end", "Hand-wash basin with a mirror above, on the north wall, north-west of the table (the lane to the bench stays clear)", 51.0, 52.5, 24.29, 24.79, 1, "Wall-hung, ceramic", "rect"),
    ("F124", "Dining end", "Pocket garden (tsuboniwa) outside the dining end's east window W63: an 8 in bed of ferns and moss stones against a lime-washed screen wall, a small stone lantern and a water bowl, an uplight", 59.5, 60.25, 16.3, 19.5, 1, "Laterite edging, ferns, stone lantern", "rect"),
    # ---- kitchen: the L runs along the south wall (sink under W82) and the east wall (hob on solid wall, cook faces east) ----
    ("F115", "Kitchen", "Counter return on the south wall west of the sink: a place for the mixer and wet grinder (the south-west corner stays clear for the utility door)", 47.4, 51.2, 4.375, 6.375, 1, "Granite top on a ply base", "rect"),
    ("F65", "Kitchen", "Prep sink, one deep 24 x 18 in bowl, drainboard on its east side, centred under the south window W82 (kitchen herbs on the sill)", 51.2, 53.0, 4.375, 6.375, 1, "SS 304, under-mount", "rect"),
    ("F34", "Kitchen", "L-counter, south run and the corner (3'-7\"): with the east run's 2'-10\" south of the hob, about 6'-5\" of clear counter between the sink and the hob (2 ft at the least), deep drawers for vessels", 53.0, 56.625, 4.375, 6.375, 1, "Granite top, ply carcass", "rect"),
    ("F35", "Kitchen", "L-counter, east run (hob centred at y 10.25 under the vent W83 on solid wall, about 2'-10\" of landing south and 1'-6\" north; pull-out masala drawer beside the hob)", 54.625, 56.625, 6.375, 12.75, 1, "Granite top, cook faces east", "rect"),
    ("F36", "Kitchen", "Refrigerator on the east wall north of the hob, clear of the sliding entry", 54.375, 56.625, 12.79, 15.29, 1, "Double-door, 2'6\" wide", "rect"),
    ("F68", "Kitchen", "Full-height larder unit 1'-6\" deep on the west wall between the utility and pantry doors (pull-out larder; no blind corner), 2 ft 3 in clear in front of the counter", 44.79, 46.29, 8.65, 10.45, 1, "Ply + laminate, full height", "rect"),
    ("F112", "Kitchen", "LPG cylinder cage outside the kitchen's east wall, south of the high vent (main + spare upright, louvred, shaded, locked): a fixed copper line through the wall to the hob with an isolation valve at the counter; delivery without entering the house; 1.5 m+ from every open drain, gully and inspection chamber (the south strip's closed pipes pass 0.5-0.9 m from it, sleeved)", 57.4, 59.0, 5.0, 7.8, 1, "MS louvred cage on a raised plinth", "rect"),
    ("F123", "Kitchen", "Garden rinse shower on the kitchen's east wall, north of the LPG cage (1.5 m+ clear of it): a stone platform with a slatted teak duckboard, a hand shower and tap, hooks for towels and garden hats, a bamboo screen on its open side; wash off garden or workshop dirt before going in; its water goes to the banana circle", 57.4, 59.2, 12.9, 14.7, 1, "Granite platform, teak duckboard, bamboo screen", "rect"),
    # ---- pantry and utility ----
    ("F37", "Pantry", "Pantry shelving 1'-6\" deep along the west wall, full height, microwave inside (tall storage away from the hob)", 39.81, 41.31, 9.79, 16.125, 1, "Ply + laminate, full height, pull-outs", "rect"),
    ("F29", "Utility", "Utility sink counter on the south wall under W64, where vessels are washed (clear of both doors)", 35.0, 38.0, 4.375, 6.275, 1, "Kadappa / granite, SS sink", "rect"),
    ("F62", "Utility", "Dish-drying rack over the utility sink: steel rods, drip tray draining into the sink", 35.5, 37.5, 4.4, 5.1, 1, "SS 304", "glass"),
    ("F113", "Utility", "Space for a washing machine (inlet, drain and socket ready) beside the utility sink, clear of the service door's swing, so ground-floor laundry need not go up the stair", 38.1, 40.1, 4.375, 6.375, 1, "Splash-proof socket, floor trap", "rect"),
    ("F61", "Utility", "Ceiling clothes airer on pulleys (lower to load, raise to dry), over the sink end, clear of the path between the two doors", 35.0, 39.6, 7.0, 8.9, 1, "Aluminium rails, nylon rope, cleat on the wall", "glass"),
    ("F31", "Back garden", "Rotary clothes airer in the back garden's south-west corner (out of the service walkway)", 9.0, 13.0, 9.0, 13.0, 1, "SS wire, wall brackets", "glass"),
    # ---- family living (north band) ----
    ("F53", "Family living", "Floating TV console 5' x 1'-4\" wall-hung at 1'-3\" on the living's solid west wall (the den's TV is on another wall, not back to back; the wall gets a 12 mm acoustic board lining on battens on the den side, behind the sofa-bed) (set-top box and router inside, the floor below clear), the TV (65 in) above it centred on the sofa, on a plain matt back wall in a soft mid-tone (nothing patterned or shiny around the screen), a dim bias light behind the TV; HDMI and power in a conduit behind", 33.875, 35.2, 37.0, 42.0, 1, "Teak veneer console, matt wall", "rect"),
    ("F38", "Family living", "Sofa 5' (2-3 seats) facing west to the TV about 8 ft away, its back to the oonjal link and the path to the pooja", 43.5, 46.2, 37.0, 42.0, 1, "Teak frame, cotton cushions", "rect"),
    ("F39", "Family living", "Coffee table 2'-5\" x 2'-2\", 1 ft from the sofa", 40.0, 42.4, 38.4, 40.6, 1, "Teak", "rect"),
    ("F45", "Family living", "Armchair facing south to the sofa group (with F46, a soft edge to the seating, not a sofa back)", 40.3, 42.1, 41.6, 43.4, 1, "Teak frame, cane, cotton cushion", "rect"),
    ("F46", "Family living", "Armchair facing north to the sofa group", 40.3, 42.1, 35.6, 37.4, 1, "Teak frame, cane, cotton cushion", "rect"),
    ("F114", "Family living", "Built-in teak diwan 5 ft with storage under each north window (bolsters, floor mats for festival overflow seating)", 35.5, 40.5, 44.125, 45.625, 2, "Teak, cushions, storage below", "rect"),
    # ---- console nook (oonjal), pooja, foyer ----
    ("F41", "Console nook", "Oonjal (swing) 3'6\", hung from the ceiling beam in the console nook facing west into the family living, swinging east-west, 2'-6\" clear behind and the living open in front; the oonjal link stays a clear path", 52.6, 54.1, 35.0, 38.5, 1, "Teak, chains to beam", "rect"),
    ("F26", "Pooja", "Pooja mandapam 1'-6\" deep on the east wall (idols face west; family faces east)", 55.1, 56.625, 41.6, 44.4, 1, "Carved teak", "rect"),
    ("F120", "Foyer", "Display niche (tokonoma) against the foyer's north wall, seen through the 4 ft opening: a low teak plinth 9 in high with a brass uruli of water and floating flowers, one seasonal object, a hidden picture light above; NE of the house, so water here suits vastu", 51.5, 53.3, 31.8, 33.29, 1, "Teak plinth, brass uruli", "rect"),
    ("F52", "Foyer", "Shoe bench 3'-6\" in the foyer (sit to take shoes off), louvred shoe shelves below and a loft cupboard above the coat and umbrella hooks, beside W80; a contrasting stone band and a low step light mark the 6 in step at the 4 ft opening", 53.1, 56.625, 25.21, 26.38, 1, "Teak top, ply + laminate, 14 in deep", "rect"),
    ("F131", "Foyer", "Umbrella and bag shelf 3 ft high in the north-east corner under W81, louvred, opposite the shoe bench", 54.6, 56.625, 32.3, 33.29, 1, "Teak, louvred", "rect"),
    ("F147", "Foyer", "Grab post at the 6 in step in the 4 ft opening: a turned teak post 3 in square, 3'-0\" high, fixed to the floor and the screen wall's end at the opening's north jamb", 51.01, 51.26, 31.0, 31.25, 1, "Teak, bolted to an SS shoe", "rect"),
    # ---- thinnai ----
    ("F121", "Thinnai", "Kolam stone at the main door: a smooth flamed-granite slab set flush in the thinnai floor in front of the door, for the morning kolam", 57.6, 59.4, 27.2, 30.8, 1, "Black granite, honed, flush", "rect"),
    ("F122", "Thinnai", "Stone lamp pedestal 2'-6\" high beside the door's north jamb for the nilavilakku, lit at dusk (sandhya deepam), facing east to the road", 57.45, 58.05, 31.15, 31.75, 1, "Granite, brass nilavilakku", "rect"),
    ("F42", "Thinnai", "Thinnai: fold-up seat with a sloping lime-plastered backrest against the wall, south of the door, on the raised red oxide platform; 1'-4\" deep when down on two folding steel brackets, folded flat (5 in) and held up by a sprung barrel bolt into the backrest, so the ramp's arrival keeps 3 ft clear past the pillar", 57.375, 57.825, 24.4, 26.8, 1, "Laterite base, teak seat and backrest, red oxide floor", "rect"),
    ("F69", "Thinnai", "Thinnai: built-in seat with a sloping lime-plastered backrest against the wall, north of the door, on the raised red oxide platform", 57.375, 59.375, 31.9, 33.85, 1, "Laterite base, teak seat and backrest, red oxide floor", "rect"),
    ("F69b", "Thinnai", "Thinnai: L-return of the north seat along its north edge, toward the pillar, with a low backrest (seats three in all)", 59.375, 60.75, 32.45, 33.85, 1, "Laterite base, teak seat and backrest, red oxide floor", "rect"),
    ("F125", "Thinnai", "Rain-chain basin: a copper rain chain from the gutter's south outlet into a granite basin of pebbles on the thinnai eave line at its south-east corner, the outlet 1'-6\" in from the corner so the basin stands just north of the reserved ramp, never on it (you see and hear the rain); the basin overflows into the rain line to the sump", _BAS_X - 0.5, _BAS_X + 0.5, _BAS_S, _BAS_S + 1.0, 1, "Copper chain, granite basin", "rect"),
    ("F126", "Thinnai", "Rain-chain basin under the thinnai eave's north-east corner, the chain from the gutter's end outlet, in view from the thinnai seats; overflows into the rain line", _BAS_X - 0.5, _BAS_X + 0.5, ROOF["thinnai"][3] - 0.5, ROOF["thinnai"][3] + 0.5, 1, "Copper chain, granite basin", "rect"),
    ("F148", "Thinnai", "Handrail on the south side of the entrance steps (rails on both sides), 2'-9\" above the nosings, the full flight from the top step to the bottom step", 62.0, 64.0, 26.8, 26.95, 1, "SS 304, 40 mm, on posts", "rect"),
    ("F149", "Thinnai", "Handrail on the north side of the entrance steps (rails on both sides), 2'-9\" above the nosings, the full flight from the top step to the bottom step", 62.0, 64.0, 31.05, 31.2, 1, "SS 304, 40 mm, on posts", "rect"),
    # ---- courtyard ----
    ("F128", "Courtyard (mutram)", "Raised round bed 4 ft across at the centre of the courtyard (the brahmasthan), a granite kerb 18 in high, the tulsi planted in it (the owner's choice), the sunken stone floor round it", CX - 2, CX + 2, CY - 2, CY + 2, 1, "Granite kerb, tulsi", "circle"),
]
# Furniture placed outside the house on purpose (garden, walkway, forecourt): skipped by the "inside a room" check
OUTDOOR_FURNITURE = {"F31", "F112", "F123", "F124", "F125", "F126", "F148", "F149"}
# extra placements (same item, additional copies drawn on plan)
EXTRA_DRAW = [("F11", 24.25, 25.25, 4.375, 5.375), ("F114", 43.0, 48.0, 44.125, 45.625)]
# Sliding doors (not the folding sets): which way the leaf parks along its wall (+1 toward +x/+y) and on which face (+1 = the
# +x/+y face). The wall beside each must stay free (no opening, no furniture) for at least the leaf's width.
SLIDERS = {"D08": (-1, +1), "D09": (+1, +1), "D17": (+1, +1), "D64": (+1, -1)}

# ---------- first floor (Task C5, compact 42 x 42): the upper wing over the west band and the den, the roof terrace over the living ----------
# The wing is the west band x 15-27.5 (y 4-33.5) plus the den block x 15-33.5 in the north band (y 33.5-46): the NW upper mass the
# C2 ruling allows. South to north: the Bedroom 2 suite over the master (hotel order: the stair head, the walk-in / dressing lobby,
# then the bedroom in the south-west corner one way and the bath north of it the other, its WC on the west outer wall), the stair head over the foot lobby (arrival at y 23.957 facing
# south), the stair well open over both flights and the half landing, a gallery beside the well over the den's walk-in (with the
# stair-head jharokha over the west walkway roof), then the upstairs family room over the den with its desk nook over the den niche
# and the upper toilet over the den bath. The roof terrace (x 33.5-50.8) sits over the living and is reached from the family room.
_UW = 22.4      # Bedroom 2 bath / walk-in (the bath is 6'-9" clear wide: WC, basin and a 3 x 3 shower)
_UB = 14.0      # Bedroom 2 / the suite's bath and walk-in (the bath sits north of the bed, over the master's wardrobe end, not over its bed)
ROOMS_F1 = [
    ("R33", "Bedroom 2 bath", HX1, _UW, _UB, _GMN, "Upper suite"),                # west: WC on the west outer wall, door from the walk-in
    ("R45", "Walk-in wardrobe", _UW, RING[0], _UB, _GMN, "Upper suite"),           # the dressing lobby: from the stair head, to the bedroom and to the bath
    ("R31", "Bedroom 2", HX1, RING[0], HY1, _UB, "Upper suite"),                   # SW corner over the master, bed head to the south outer wall
    ("R41", "Stair head", HX1, RING[0], _GMN, _GFOOT, "Circulation"),             # the arrival strip over the foot lobby, 3'-6" clear deep
    ("R34", "Gallery", _GSE, RING[0], _GFOOT, RING[3], "Circulation"),            # beside the well (a 4 ft guard on x 23.085), the stair-head jharokha on its east wall
    ("R36A", "Family room desk nook", HX1, _DX, RING[3], _DB, "Family"),          # over the den niche, open to the family room
    ("R39", "Upper toilet", HX1, _DX, _DB, HY2, "Service"),                        # stacked exactly over the den bath R07
    ("R36", "Family room", _DX, _DE, RING[3], HY2, "Family"),                     # over the den: bookshelf wall, screen, sofa-bed, jharokha over the courtyard
    ("R37", "Roof terrace", _DE, _OX, RING[3], HY2, "Terrace"),                   # over the living, reached from the family room
]
UPPER_FAMILY_ROOM = ("R36", "R36A")   # one room drawn as two rects (no wall between them)
WALLS_F1 = [
    ("X", HY1, HX1, RING[0]), ("Y", HX1, HY1, HY2), ("X", HY2, HX1, _DE), ("Y", RING[0], HY1, RING[3]),   # outer walls of the wing
    ("X", RING[3], RING[0], _DE), ("Y", _DE, RING[3], HY2),                       # the wing's walls over the north walkway and to the terrace
    ("Y", _UW, _UB, _GMN),                                                         # bath to the walk-in (wet)
    ("X", _UB, HX1, _UW), ("X", _UB, _UW, RING[0]),                                # the suite's bath (wet) and walk-in to Bedroom 2 (the bed's foot end; its head is on the south wall)
    ("X", _GMN, HX1, RING[0]),                                                     # Bedroom 2 to the stair head (on the master's north wall)
    ("X", RING[3], HX1, RING[0]),                                                  # the well's north wall and the gallery's end (on the ground wall below)
    ("X", _DB, HX1, _DX), ("Y", _DX, _DB, HY2),                                    # upper toilet (wet), on the den bath's walls
]
EXTERIOR_F1 = {("X", HY1), ("X", HY2), ("Y", HX1), ("Y", RING[0]), ("Y", _DE)}
EXTRA_EXT_WALLS_F1 = {("X", RING[3], RING[0], _DE)}                                # the family room's south wall over the north walkway (9 in, outer)
WET_WALLS_F1 = {("Y", _UW, _UB, _GMN), ("X", _UB, HX1, _UW), ("X", _DB, HX1, _DX), ("Y", _DX, _DB, HY2)}
# Stair: dog-leg, 16 risers of 7.5 in (floor to floor 10 ft), 10 in treads, flights and half landing 3'-6" clear between wall faces.
# Against the west outer wall (vastu: west), rising clockwise from the 3'-6" foot lobby R09 (y 20.45-23.957): flight 1 rises north on
# the west side, turn at the half landing against the den-side wall (face y 33.29, over the low store R46), flight 2 rises south on
# the east side and arrives at y 23.957 facing south, onto the stair head and toward the suite door D31.
# Rects are wall face to wall face: west wall face x 15.375, core 6 in, east wall face x 22.875, north wall face y 33.29.
STAIR = {
    "risers": 16, "tread": 10 / 12, "dir": 1,   # dir: the way flight 1 rises (+1 north, -1 south)
    "flight1": (HX1 + T / 2, 18.875, _GFOOT, _GLAND, 8),       # x1, x2, y1, y2, risers (both flights start and end at the lobby end)
    "landing": (HX1 + T / 2, _GSE - 0.21, _GLAND, RING[3] - 0.21),
    "flight2": (19.375, _GSE - 0.21, _GFOOT, _GLAND, 8),
    "core": (18.875, 19.375, _GFOOT, _GLAND),                  # wall between the flights: see core_note
    "core_note": "The 6 in core between the flights is a full-height wall from the foot of the stair to the roof, with a handrail fixed to it on both flights; wherever it is cut lower it carries a 4'-0\" guard with gaps of 100 mm or less above flight 2.",
}
# Railings at the first floor (axis, c, s, e): open sides of the roof terrace and the edges of the stair well. 4'-0" (1.2 m) high,
# vertical bars or balusters with gaps of 100 mm or less, no horizontal footholds, bottom gap 50 mm or less; nothing to climb on placed against them.
RAIL_H = 4.0
RAILS_F1 = [("X", _GFOOT, HX1, STAIR["core"][0]),                                # the well edge over the foot of flight 1 (the core wall runs on to the roof)
            ("Y", _GSE, _GFOOT, RING[3]),                                          # the gallery's guard over the well (flight 2 and the landing below)
            ("X", RING[3], _DE, _OX), ("Y", _OX, RING[3], HY2), ("X", HY2, _DE, _OX)]   # roof terrace: south (over the walkway roof), east, north
# The terrace's north side faces the neighbour across the north boundary: a closed teak jali parapet 4'-0" high on a steel core
# (privacy, breeze), jali openings 100 mm or less, not open balusters. The courtyard (south) and road (east) sides stay open railings.
JALI_RAILS = {("X", HY2)}
# Galvanised steel posts carrying the terrace's light tiled canopy (open sides): its four corners and the mid-points of its north and
# south edges on x 44.5, every one over a ground-floor wall junction (spans 11 ft and 6'-4")
TERRACE_POSTS = [(_DE, RING[3]), (RING[1], RING[3]), (_OX, RING[3]), (_DE, HY2), (RING[1], HY2), (_OX, HY2)]
# First-floor slab outline (pieces): the wing and the roof terrace, less the stair well (x 15-23.085, y 23.957-33.5: both flights,
# the core and the half landing open to the roof)
SLAB_F1 = [(HX1, RING[0], HY1, _GFOOT), (_GSE, RING[0], _GFOOT, RING[3]), (HX1, _DE, RING[3], HY2), (_DE, _OX, RING[3], HY2)]
# Jharokhas: teak bays 4 ft wide and 2 ft deep projecting from the wing over the walkway roof, looking down into the courtyard:
# (x1, x2, y1, y2, seat height above the floor). The gallery's bay at the stair head projects east from x 27.5 over the west walkway
# roof; the family room's bay projects south from its south wall (y 33.5) over the north walkway roof (the family room has no east
# wall on the walkway: its east wall faces the terrace). JHAROKHA_FACE gives the way each bay faces.
JHAROKHAS = [(RING[0], RING[0] + 2.0, 26.0, 30.0, 2.0), (29.0, 33.0, RING[3] - 2.0, RING[3], 2.0)]
JHAROKHA_FACE = ["E", "S"]
JHAROKHA_DECK = 0.25   # the bay's seat deck (its floor) and bracket frame below the seat level: the bay's underside is sill - deck above the room floor
# A west balcony was tried and dropped (22 Nov 2026); kept as None so the drawing code skips it
BALCONY = None
# Shower zones (clear floor inside the walls and glass), x1, x2, y1, y2: every shower at least 3' x 3'
SHOWERS = {"R40": (27.875, 31.875, 4.375, 7.875), "R07": (15.375, 18.5, 38.59, 41.6),   # ground: master (4'-0" x 3'-6") and den bath (3'-1" x 3'-0")
           "R33": (19.11, 22.11, 17.03, 20.03), "R39": (15.375, 18.4, 38.59, 41.6)}      # first floor: Bedroom 2 bath (3' x 3'), upper toilet (3'-0" x 3'-0")
# Planter box grilles outside windows: window id -> depth in ft (none: the wing's south windows are a bath vent and a high jali strip)
PLANTER_GRILLES = {}
# Light well over the dining table (slab void): rail round it, walk-on jali grating and a closable glazed lid for AC and monsoon
LIGHT_WELL = None  # the light well over the dining was dropped (the dining has its own south window)

DOORS_F1 = [
    ("D31", "X", _GMN, 22.8, 25.2, 0, "Suite door from the stair head into the walk-in / dressing lobby (hotel-style: then the bedroom one way and the bath the other), sliding on the stair-head face and parking west (the east end of that wall meets the outer wall)", "Teak frame, flush teak-veneer sliding leaf on a top track, soft-close, privacy lock"),
    ("D51", "X", _UB, 22.8, 25.2, -1, "Bedroom 2 (from the walk-in, opens into the bedroom; the bed head is on the south wall beyond)", "Flush, teak veneer"),
    ("D33", "Y", _UW, 14.6, 17.0, 0, "Bedroom 2 bath (from the walk-in, sliding on the walk-in face and parking north, so no leaf swings into the bath or the dressing aisle; the basin and mirror face you across the bath on the west wall)", "Flush, waterproof (WPC/FRP) sliding leaf on a surface track, soft-close, privacy lock with an emergency release"),
    ("D39", "X", _DB, 18.9, 21.4, 1, "Upper toilet (from the family room's desk nook, opens inward; the first view is the basin and mirror on the north wall, the WC is off the door line)", "Flush, waterproof (WPC/FRP), emergency-release lock"),
    ("D36", "X", RING[3], 23.8, 26.55, 1, "Family room (from the gallery, opens in)", "Flush, teak veneer, a narrow glazed vision panel"),
    ("D49", "Y", _DE, 34.3, 37.8, 0, "Roof terrace (from the family room), sliding and parking north on the terrace face of the wall", "Teak-framed glazed sliding doors, two panels, a sliding mesh shutter and an MS security grille shutter; the terrace is 1 in down with a linear drain outside the track"),
]
WINDOWS_F1 = [
    ("W31", "Y", RING[0], 4.6, 6.1, 3, 7, "Bedroom 2", "Timber jali + glazed shutters (1'-6\") on the east wall (morning light), over the master bath's roof"),
    ("W37", "Y", RING[0], 6.6, 8.8, 3, 7, "Bedroom 2", "Timber jali + glazed shutters (2'-2\") on the east wall, hinged with an inside release: the upstairs escape window onto the master bath's roof if the stair is blocked by smoke; well south of the ring ridge, so its 3 ft sill stands 9 in above the tiles at its north jamb: a 6 in flashed apron upstand dressed over the tiles and a granite sub-sill above it (A-501/10)"),
    ("W38", "X", HY1, 15.8, 17.0, 3, 6.5, "Bedroom 2", "Small timber jali + glazed shutters west of the bed head, deep sill (south: small against the sun)"),
    ("W39", "X", HY1, 25.5, 26.7, 3, 6.5, "Bedroom 2", "Small timber jali + glazed shutters east of the bed head, deep sill"),
    ("W41", "Y", HX1, 18.0, 20.0, 5, 7, "Bedroom 2 bath", "Frosted casement, top-hung, on the west outer wall over the WC (steam out); its upper pane takes the exhaust fan (outer wall)"),
    ("W45", "Y", RING[0], 16.5, 19.5, 6, 7.5, "Walk-in wardrobe", "High jali strip over the hanging run on the east wall, top-hung glazed shutters worked by a rod from the floor: light and air without sun on the clothes"),
    ("W35", "Y", HX1, 21.3, 23.3, 3, 6.5, "Stair head", "Small timber jali + glazed shutters, deep sill (west: small against the evening sun): daylight at the arrival"),
    ("W43", "Y", RING[0], 20.7, 23.5, 3, 7, "Stair head", "Teak casement, glazed, jali lower leaf over the walkway roof: the courtyard seen as you arrive"),
    ("W33", "Y", HX1, 27.0, 31.0, 6, 9, "Stair", "Glazed clerestory over the stair well, top-hung, under the roof's eave: the hot-air outlet of the stair chimney"),
    ("W46", "Y", RING[0], 26.0, 30.0, 2.0, 7.5, "Gallery", "Opening of the stair-head jharokha in the gallery: the bay's seat at 2'-0\", fixed jali to 5'-0\", glazed casements above, looking down into the courtyard; off the stair, so the stair and the arrival stay clear"),
    ("W57", "Y", HX1, 35.0, 37.0, 3, 7, "Family room desk nook", "Small timber jali + glazed casement (2 ft) over the desk, west light; deep sill, external louvre"),
    ("W42", "X", HY2, 15.8, 17.8, 5, 7, "Upper toilet", "Frosted casement, top-hung (2 ft), on the north outer wall over the WC; its upper pane takes the exhaust fan"),
    ("W52", "X", HY2, 22.6, 24.6, 3.5, 7, "Family room", "Teak casement, glazed (2 ft), jali lower leaf: north light over the reading chair in the corner"),
    ("W47", "X", RING[3], 29.0, 33.0, 2.0, 7.5, "Family room", "Opening of the family room's jharokha on its south wall: the bay's seat at 2'-0\", fixed jali to 5'-0\", glazed casements above, looking south into the courtyard"),
]
FURNITURE_F1 = [
    # ---- Bedroom 2 suite (hotel style): bedroom, then the walk-in, then the bath ----
    ("F71", "Bedroom 2", "King bed 6' x 6'6\" + headboard, head to the south outer wall between the two small south windows, 2'-10\" clear to each side wall and 2'-10\" at its foot", 18.25, 24.25, 4.375, 10.875, 1, "Teak", "rect"),
    ("F72", "Bedroom 2", "Floating bedside shelf with a drawer, reading light and charging point above", 17.25, 18.25, 4.375, 5.375, 2, "Teak, wall-hung", "rect"),
    ("F77", "Bedroom 2 bath", "WC (EWC) on the west outer wall north of the basin (you sit facing east), 15 in+ from its centre to the L rail on the north wall and 1'-10\" clear in front; its soil pipe goes straight out through the wall and down to the soil line outside", 15.375, 17.125, 17.6, 19.0, 1, "Wall-hung, concealed cistern", "wc"),
    ("F152", "Bedroom 2 bath", "Grab rail beside the WC: 600 mm L (a horizontal leg at 2'-9\" and a vertical leg), on the north wall", 15.5, 17.4, 19.91, 20.03, 1, _GRAB, "rect"),
    ("F78", "Bedroom 2 bath", "Wash basin on the west wall straight opposite the door, a mirror cabinet recessed into the 9 in outer wall above with a light over it", 15.375, 16.875, 15.05, 16.55, 1, "Wall-hung", "rect"),
    ("F79", "Bedroom 2 bath", "Glass screen of the walk-in shower along its west side (north-east corner, 3' x 3'); open at its south end onto the blank middle of the room, never toward the WC", 18.99, 19.11, 17.03, 20.03, 1, "8 mm toughened glass", "glass"),
    ("F95", "Walk-in wardrobe", "Hanging run 1'-10\" deep along the east wall under the high jali: double short rails, a long-hang section for saris and kurtas, sari drawers and shoe racks below; ventilated back held 1 in off the wall; a 2'-7\" dressing aisle in front", 25.29, 27.125, 14.21, 20.03, 1, "Ply + laminate, open front, LED strip", "rect"),
    # ---- stair head and gallery ----
    ("F129", "Gallery", "Jharokha seat at the stair head: a cushioned teak seat 2'-0\" above the floor in a 4 ft teak bay over the west walkway roof, looking down into the courtyard; a 6 in teak step up and a grab rail at the step; fixed jali up to 3 ft above the seat, glazed above", 27.65, 29.35, 26.1, 29.9, 1, "Teak, cotton cushion and bolsters", "rect"),
    # ---- upper toilet (over the den bath) ----
    ("F98", "Upper toilet", "WC (EWC) on the north wall in the north-west corner (you sit facing south), off the door line and out of the mirror's view; its soil drops to the den bath's soil line below", 16.07, 17.47, 43.8, 45.625, 1, "Wall-hung, concealed cistern", "wc"),
    ("F153", "Upper toilet", "Grab rail beside the WC: 600 mm L (a horizontal leg at 2'-9\" and a vertical leg), on the west wall", 15.375, 15.495, 43.65, 45.6, 1, _GRAB, "rect"),
    ("F99", "Upper toilet", "Wash basin on the north wall straight opposite the door, a mirror cabinet recessed 4 in into the wall above with a light over it", 19.4, 20.9, 44.625, 45.625, 1, "Wall-hung", "rect"),
    ("F70", "Upper toilet", "Glass screen on the north side of the walk-in shower (south-west corner, 3' x 3'), keeping the spray off the WC; the shower opens east onto the blank floor beside the door", 15.375, 18.4, 41.6, 41.72, 1, "8 mm toughened glass", "glass"),
    ("F154", "Upper toilet", "Glass return on the shower's east side at its north end, so its 2'-7\" opening faces east (never the WC)", 18.4, 18.52, 41.3, 41.72, 1, "8 mm toughened glass", "glass"),
    # ---- family room (over the den) and its desk nook ----
    ("F107", "Family room", "Floor-to-ceiling bookshelf wall 5'-1\" on the north wall, starting clear of the window W52: closed cupboards 2 ft high at the base, open shelves 12 in deep above with LED strips under each shelf, a library ladder rail", 24.8, 29.9, 44.625, 45.625, 1, "Teak veneer, solid teak shelf edges", "rect"),
    ("F55", "Family room", "Screen wall on the west wall: a 55 in screen (or a projector screen) over a floating console, speakers either side; the wall to the upper toilet behind it gets an acoustic board lining on battens; blackout blinds", 22.29, 22.89, 39.3, 43.8, 1, "Teak veneer console, fabric acoustic panels", "rect"),
    ("F92", "Family room", "Three-seat sofa-cum-bed 6'-6\" against the east wall, facing the screen about 7 ft away (guest bed; sleep with the head to the south; the coffee table is moved aside when it is opened)", 30.125, 33.125, 38.9, 45.4, 1, "Teak frame, upholstered", "rect"),
    ("F156", "Family room", "Low coffee table 2' x 1'-9\" between the sofa-bed and the screen", 26.5, 28.3, 39.6, 41.6, 1, "Teak", "rect"),
    ("F135", "Family room", "Reading armchair in the north-west corner beside the screen, under the north window W52, facing south-east into the room", 22.4, 24.2, 43.9, 45.6, 1, "Teak frame, cane, cotton cushion", "rect"),
    ("F101", "Family room", "Jharokha seat (hyggekrog) 3'-10\" x 1'-8\" in the family room's teak bay over the north walkway roof: a teak box seat 2'-0\" above the floor with drawers, a thick cotton cushion and bolsters; a 6 in teak step up and a grab rail at the step; fixed jali up to 3 ft above the seat, glazed above; looking south into the courtyard; the bay's west kerb meets the roof's north-west valley: a lead-lined pocket gutter beside it falls south past the kerb corner to the valley", 29.1, 32.9, 31.65, 33.35, 1, "Teak, cotton cushion, drawers below", "rect"),
    ("F91", "Family room desk nook", "Work desk 3'-6\" x 2' on the nook's west wall under the window W57 (two screens, cable tray), drawers to one side", 15.375, 17.375, 34.1, 37.6, 1, "Teak / ply, cable tray", "rect"),
    ("F155", "Family room desk nook", "Task chair at the desk (drawn pulled out; 2 ft+ clear past it to the toilet door)", 17.5, 18.9, 35.15, 36.55, 1, "Teak frame, cane seat", "rect"),
    # ---- roof terrace (over the family living) ----
    ("F103", "Roof terrace", "Teak oonjal (swing) 5 ft hung on chains from a steel hanging beam bolted across the canopy's trusses over the swing (rated 200 kg), facing south over the walkway roof into the courtyard, 3 ft clear in front (to the south railing) and behind", 40.5, 45.5, 36.65, 38.65, 1, "Teak, brass chains", "rect"),
    ("F127", "Roof terrace", "Low daybed 2'-4\" x 5' in the terrace's north-east corner, lying east-west and facing east (tsukimi): morning coffee at sunrise, the moon rising over the trees on full-moon nights; here the east verge stands under 2'-9\" above the slab (the ring roof falls toward the north eave), so a seated person sees east over it; loose, 2 ft off the east railing and 1'-8\" off the north parapet, clear of the swing, the planter, the laundry corner and the terrace door path", 43.8, 48.8, 41.8, 44.13, 1, "Teak frame, cotton mattress, bolsters", "rect"),
    ("F89", "Roof terrace", "Low planter trough, 6 in high, 1'-6\" in from the east railing beside the daybed (nothing to climb on against the railing): jasmine (mulla) and lemongrass, the jasmine trained to the canopy post on a wire", 48.5, 49.3, 35.0, 40.5, 1, "Lightweight GRC trough, drained to the terrace outlet", "rect"),
    ("F30", "Roof terrace", "Slim front-loading washing machine (450 mm deep) in a closed teak cabinet 2'-0\" x 1'-8.5\" against the family room's east wall (louvred on its side, solid on the weather faces), with its supply, IP55 socket and floor trap; a roll-down monsoon blind along the laundry corner's open side", 33.875, 35.875, 41.35, 43.06, 1, "Weatherproof socket, louvred cabinet", "rect"),
    ("F32", "Roof terrace", "Laundry sink beside the washer (hand wash, soaking), 2'-11\" off the north parapet, clear of the tank stand", 36.0, 37.8, 41.5, 43.03, 1, "SS sink on a stone base", "rect"),
    ("F88", "Roof terrace", "Clothes-drying rails on pulleys over the washer and the sink (hauled up under the canopy when not in use); a bamboo chik on its open side screens the washing from the daybed", 35.9, 39.9, 41.0, 43.03, 1, "Aluminium rails on pulleys", "glass"),
]
EXTRA_DRAW_F1 = [("F72", 24.25, 25.25, 4.375, 5.375)]
SLIDERS_F1 = {"D49": (+1, +1), "D31": (-1, +1), "D33": (+1, +1)}   # terrace door parks north on the terrace face; the suite door west on the stair-head face; the bath door north on the walk-in face

# Prose below may quote numbers the geometry knows as {key} (see geom.prose_numbers: {ring_eave}, {terrace_slab}, {house}, ...) and
# room sizes as {clear:Rnn} (clear, wall face to wall face) or {size:Rnn} (centre lines), east-west x north-south. geom fills them in
# when it is imported, so every schedule and sheet quotes the drawn numbers.
PROSE_FILLED = False   # geom sets it True once it has filled the placeholders
FINISHES = [  # spaces, floor, walls (incl. skirting / dado), ceiling, notes
    ("Courtyard (mutram)", "Rough-dressed stone, sunk {court_drop} below the walkway (6 in below the rooms), falling to two corner drains: CD at the south-east (150 mm grating, to the first-flush filter and the sump) and CD-2 at the north-west on its own overflow line, with a standpipe overflow 3 in above the floor and a scupper through the west walkway kerb", "Lime plaster in warm white and ochre; the round tulsi bed 4 ft across at the centre in an 18 in granite kerb; plinth face of stone", "Open to the sky: a galvanised steel grille at the inner eave ({ring_eave}) with a track for a pull-across shade cloth", "{court}; sized for a 100 mm-per-hour downpour; rain and the night sky come into the house; the grille keeps it secure"),
    ("Walkway (thazhvaram)", "Rough-dressed stone, 1 in below the rooms (so rain stays out) and one step (5 in) above the courtyard", "Turned teak pillars on stone bases at the court's corners and mid-sides, set into the court so the walkway keeps its width; the walls behind in lime plaster; teak-and-glass folding doors on the family room's sides, stacked to the piers by day", "The ring roof's inner slope carried on over it to the court eave, rafters exposed", "{walk} wide ({walk_clear} clear); shades every wall that faces the courtyard and links every room under cover in the monsoon"),
    ("Thinnai (front platform)", "Red oxide (IPS), honed, 1'-6\" above the forecourt, falling 1:100 away from the door", "Lime-plastered sloping backrests (the south seat folds up); turned teak pillars; granite skirting", "Exposed rafters and board under the lean-to ({thinnai_clear} clear at the pillars)", "{size:R17}; kolam stone at the door, nilavilakku pedestal, copper rain chains at the front corners into pebble basins; three steps with rails both sides and a reserved 1:12 ramp to its south edge"),
    ("Family room: living, console nook, oonjal link, dining end (Athangudi floors)", "Athangudi handmade cement tile, sealed; the pattern chosen from the maker's sample board", "4 in flush skirting; lime-finish or mineral paint in warm white and ochre", "Insulated false ceiling at 9'-6\" under the tiled ring roof; the living's ceiling is the roof terrace slab's plastered soffit at 9'-0\" (+11'-0\"), so the slab, its 1:80 falls, membrane and terracotta tile fit under the +11'-11\" terrace floor", "Seal the tile before use: it stains easily; the oonjal in the console nook and the extending dining table are the character here"),
    ("Foyer", "Rough-dressed granite at the thinnai level, 6 in below the family room, with a weather bar at the main door; a contrasting stone band at the 6 in step in its 4 ft opening", "Teak shoe bench with hooks; granite skirting; timber jali screens to the oonjal link", "False ceiling at 9'-6\"", "The uruli niche (tokonoma) on its north wall; a low step light and a teak grab post at the step"),
    ("Bedrooms, den, walk-ins, stair lobby", "Red oxide (IPS) or polished Kota stone; matt vitrified 2x2 ft in Bedroom 2, its walk-in and the upstairs family room", "4 in flush skirting; putty + washable emulsion", "False ceiling at 9'-6\": on the ground floor with 50 mm insulation above (the master and the den lie under the wing's slab); on the first floor under the tiled roof, ventilated attic above", "AC points in the master, the den, Bedroom 2 and the upstairs family room (and the family room below): the doors onto the walkway close when the AC runs"),
    ("Pooja", "Red oxide, 3 in above the family room floor", "Teak panelling behind the idols; 4 in marble skirting", "Teak / board at 9'-0\"", "In the north-east corner, opening west into the family room so the family faces east; lamp niche with a heat-proof back and a high vent; no toilet in the north-east"),
    ("Kitchen, utility, pantry", "Anti-skid matt vitrified or Kota, mid-tone", "Tile / stone full height between counter and wall cabinets", "Moisture-resistant board at 9'-6\", storage loft above", "Counter granite (local Ongole / Chimakurthy), 2 ft deep; deep drawers for vessels, pull-out masala drawer by the hob, utensil rail on the wall beside it; the prep sink under the south window W82, the hob on the east wall under the high vent W83; the utility has a service door to the south side"),
    ("Master bath, den bath, powder room, Bedroom 2 bath, upper toilet", "Anti-skid ceramic (R11), falls 1:60 to drain", "Tiles to 7 ft; full height in shower; waterproofing 12 in up all walls, 7 ft in shower", "Moisture-resistant board / PVC at 8'-6\"", "Recessed tiled shower niche with a sloped sill; mirror cabinet over the basin, straight opposite the door; towel and clothes hooks at the dry end; 12 mm step down, no raised threshold; the master and den bath doors open outward on lift-off hinges, the powder room's and Bedroom 2's bath doors slide, the upper toilet's opens inward, all with emergency-release locks; SS grab rails by every WC and in the master and den showers, fold-down seats in both. Bedroom 2's bath (over the master's wardrobe end, not its bed) and the upper toilet (over the den bath) sit on a sunk slab: waterproof each with upturns and bonded pipe collars, and flood-test it for 48 h before tiling"),
    ("Stair", "Granite or Kota treads with a contrasting anti-slip nosing strip, 10 in treads, 7.5 in risers (190 mm, the NBC limit for houses: build no steeper)", "Teak handrails on both sides of both flights at 2'-10\" to 3'-0\" above the nosings, continuous round the half landing and carried 1 ft past the top and bottom steps (ready for a stair-lift later); the core wall between the flights is full height", "Open to the roof over both flights and the half landing, with a clerestory over the landing; a few clear glass Mangalore tiles (glass ottu) among the clay tiles over the stair well, so patches of sun move down the stair wall through the day without a hot skylight", "Flights and half landing 3'-6\" clear between wall faces; the landing window's sill 3'-0\" above the landing; low motion lights 1 ft above the treads; 2-way switches; the stair lobby's sliding door D09 closes the stair and the upstairs off"),
    ("Stair lobby, stair head, gallery", "Red oxide", "4 in flush skirting; washable paint; the main distribution board in a lockable teak cabinet in the DB and linen cupboard under flight 2, the sub-board on the gallery's east wall", "Lobby: false ceiling; stair head: open to the roof (the stair chimney)", "The gallery runs beside the well behind a 4 ft guard with the stair-head jharokha on its east wall"),
    ("Upstairs family room and its desk nook (first floor)", "Matt vitrified 2x2 ft", "4 in skirting; lime-finish or mineral paint; a floor-to-ceiling teak bookshelf wall on the north wall, the screen on the solid west wall, 50 mm mineral wool and board on the walls and a solid-core door with seals (the room sits over the den)", "Insulated false ceiling at 9'-6\" under the tiled roof", "One room for reading, the screen, guests (the sofa-bed) and work (the desk nook); a jharokha bay seat over the courtyard; glazed sliding doors to the roof terrace; its walls and glazing go in at stages 2 and 3 (the slab and roof are stage 1)"),
    ("Jharokhas (gallery, upstairs family room)", "Teak seat, cushioned, 2'-0\" above the floor, a 6 in step up with a grab rail", "Teak bay on a steel bracket frame on a 6 in flashed kerb, fixed jali with gaps of 100 mm or less up to 3 ft above the seat, glazed above", "No roof of its own: the frame runs up to the wing's eave soffit, which is its roof", "Each bay is 4 x 2 ft over the walkway roof, inside the house, looking down into the courtyard: the gallery's faces east, the family room's faces south"),
    ("Roof terrace (first floor)", "Terracotta anti-skid tile on a waterproofed slab at {terrace_slab} ({terrace_step} below the upstairs family room), falls 1:80 to the outlet through the north parapet", "A teak jali parapet 4'-0\" on a steel core on the north side (the neighbour is close); open railings on the south side (on a {upstand} RCC upstand over the walkway roof) and the east side; a level {corner_guard} solid guard wall at the south-east corner; glazed sliding doors to the family room (west); the laundry corner and two 500 L tanks on a stand at the north-west", "A light tiled canopy on six galvanised steel posts at {canopy}, open sides, full length", "{size:R37}; slab waterproofing and a 48 h flood test before tiling: it sits over the family living; the step at the door D49 is an open item"),
    ("Exterior", "Plinth apron: PCC 3 ft wide sloped away", "AAC + 20 mm plaster with waterproof additive; lime-wash colour in warm white and ochre", "-", "Drip grooves under every sill and sunshade"),
    ("Roof (all)", "Clay Mangalore tiles at {pitch}, every edge tile clipped / screwed; 2 ft overhangs; ring eave {ring_eave} and ridge {ring_ridge}; wing eave {wing_eave} and ridge {wing_ridge}", "Membrane + 50 mm insulation on cement-fibre deck", "Steel trusses or rafters on RCC ring beams: a ridge along the middle of each band of the single-storey ring, the inner slope running on over the walkway into the courtyard; an L-shaped hipped roof over the west wing and the upstairs family room", "Cyclone winds: tie trusses down with holding-down bolts"),
]

OPEN_ISSUES = [  # category, issue, who resolves, status
    ("Layout", "Size: the owner chose the compact house, {house} round a {court} courtyard on a {plot} plot (24 Nov 2026), in place of the 54 x 54 ft house: about {enclosed_area} sq ft enclosed ({ground_area} ground, {upper_area} upper with the stair well) plus {walkway_area} sq ft of walkway, the {thinnai_area} sq ft thinnai and the {terrace_area} sq ft roof terrace. Re-price from the area table before the tender", "Owner / quantity surveyor", "Open"),
    ("Roof terrace", "Terrace step at the door D49: the terrace slab is at {terrace_slab}, only {terrace_step} below the upstairs family room ({family_floor}). That is too little for a membrane upturn and a weather sill (about 6 in is usual). A deeper step means a lower slab, which changes every terrace edge-wall height (the {upstand} south upstand, the {corner_guard} corner guard, the east verge) and the canopy clearance under the wing's gutter. It already costs the living its false ceiling: the living's ceiling is the slab's plastered soffit at about +11'-0\" (9'-0\" clear over the +2'-0\" floor) so the slab, its 1:80 falls, the membrane and the tile fit under {terrace_slab}; a deeper step costs more headroom still, and raising the terrace a riser instead would change the 16-riser stair. Owner decision; then the architect re-derives the edge walls", "Owner / architect", "Owner to decide"),
    ("Owner review", "Two deviations from the approved first floor and roof, for the owner to see: (1) Bedroom 2's east windows: W37 (the escape window) moved south and narrowed to 2'-2\" (sill 3'-0\", 9 in above the tiles at its north jamb, over a 6 in flashed apron upstand) and W31 narrowed to 1'-6\", so both sit south of the ring's ridge and clear of the roof; (2) no second downpipe on the ring's south side: the south side has downpipes only at {south_dps} ({ring_south_dp} is the ring's south gutter's only one), because a second one would cross the soil and grey lines and chambers that fill the south pipe strip; the gutter is the same {south_gutter} as every other, so the engineer is to check that run or upsize it to 200 mm", "Owner / architect", "To show the owner"),
    ("Courtyard", "Grille and shade cloth: the galvanised steel grille at the inner eave ({ring_eave}), its track and the pull-across cloth; check the cloth against cyclone gusts (take it in when a warning is out) and the two drains, the first-flush filter and the overflow against a 100 mm-per-hour downpour", "Architect / engineer", "Open"),
    ("Roof", "Roof junctions, to detail: (1) apron and step flashing chased into the wall wherever the ring roof meets the wing's walls or the terrace's edge walls, with lead counter-flashing; (2) the soldered box gutter at the wing's re-entrant corner (its courtyard-side gutters fall 1:200 away from it to {spreaders} short spreader downpipes onto the ring roof, and a 50 mm overflow spout drops onto the ring's north-west valley); (3) 12 in GI / aluminium valley gutters in the ring's four inner valleys and the wing's valley; (4) the terrace edges: a {upstand} RCC upstand on the south side under the railing, a LEVEL {corner_guard} solid guard wall at the south-east corner (the last {guard_s} of the south edge to the corner and {guard_e} up the east edge, then a stepped transition), where the east band's ridge runs into the edge, then a verge wall 6 in over the roof on the east side; no box gutter on the terrace edges; (5) the terrace outlet through the north parapet's foot into its downpipe, and the 2 ft RCC chajja over the living's windows W75/W76 with the downpipe through it in a sleeve; (6) the jharokha kerbs (6 in, back-gutter and saddle up-slope) and the lead-lined pocket gutter beside the family room's bay on the north-west valley; (7) gutters on every outer eave, {downpipes} downpipes in all; detail the court's inner eave so rain falls clear of the walkway pillars", "Architect / contractor", "Open"),
    ("Finishes", "Athangudi tile: choose the patterns and colours from the maker's sample board, and order a few boxes extra (it cannot be matched later); the thinnai floor is red oxide with turned teak pillars (owner, 24 Nov 2026); decide the colour scheme (warm white and ochre lime wash) before ordering paint and door finishes", "Owner", "Open"),
    ("Land", "Survey the {plot} plot and confirm the setbacks for a two-storey wing: the house leaves {side_strip} on the north and south sides (the minimum side setback for two storeys under the AP rules is to be checked: it may be more), {back_garden} at the back and {front_land}", "Architect / surveyor", "Open"),
    ("Land", "Agricultural land: confirm conversion to non-agricultural use with the gram panchayat / collector (AP repealed the NALA Act in 2025; new process to be confirmed)", "Owner / surveyor", "Open"),
    ("Land", "Building permission route (panchayat vs DTCP / APCRDA via APDPMS) and setbacks under AP Building Rules 2017, including any height rule for two storeys; the jharokha bays project over the walkway roof, inside the house and not into a setback, so no bylaw check is expected for them", "Architect", "Open"),
    ("Site", "Workshop and shops as a demountable kit (bolted steel frame, precast post-and-panel walls, insulated sheet roof, a shared toilet cabin): confirm the panel supplier (the same as the compound wall), the anchor-bolt footings and the wind bracing for cyclone gusts; rough cost Rs 1.5-2 L for the workshop and Rs 3.5-5 L for both shops", "Engineer / owner", "Open"),
    ("Site", "Future rental shops on the road front: commercial setback and permission, separate meters, a shared toilet; decide whether to cast their plinth and service sleeves with the compound wall", "Architect / panchayat", "Open"),
    ("Site", "Septic tank south-east of the forecourt behind its hedge (it cannot sit in the north-east quadrant): the tanker stops at the drive's west end beside the car porch and its hose runs about 18 ft south-west between the car porch and the vegetable strip to the tank; the soak pit on the south side about 19 ft from the house wall. The borewell in the north-east corner is about 64 ft from the soak pit but only about 47 ft from the septic tank's nearest edge (51 ft centre to centre), a little under the 15 m (49 ft) usually asked; the tank is sealed RCC. The engineer to confirm, or drop the borewell and rely on the road main; the vastu consultant to confirm the septic position for the whole plot", "Engineer / vastu consultant", "Open"),
    ("Structure", "Two-storey RCC frame: columns, footings and the first-floor slab sized for the west wing, the upstairs family room over the den, the roof terrace and the two water tanks on their stand; the stair well; the courtyard's walkway pillars and the thinnai pillars on their own footings; RCC column stubs at the terrace edge for the six steel canopy posts; RCC edge beams under the terrace's south-east corner guard where no wall stands below", "Structural engineer", "Open"),
    ("Layout", "TV walls: the family living's TV console on its solid west wall (the den's east wall, behind the den's sofa-bed: see the sound item), the den's TV on its west wall, and the upstairs family room's screen on its west wall (about 7 ft from the sofa-bed); confirm screen sizes and a concealed HDMI / data conduit", "Owner", "Open"),
    ("Soil", "Soil test (bore holes to 3 m min): black cotton soil is common in Guntur. Foundation type (isolated footings below active zone, under-reamed piles, or soil replacement) depends on it; the sunk courtyard needs its own check of the footing depth round it", "Structural engineer", "Open"),
    ("Services", "Groundwater: test TDS, hardness, fluoride. Plan RO for drinking and a softener for bathrooms if hardness is high", "Plumber / owner", "Open"),
    ("Services", "Septic tank and soak pit: percolation test for the soak pit size; the kitchen's grey line passes 1.2 ft from the soak pit (sleeved: the 3.6 ft south strip allows no more); the effluent line runs 3 ft+ from the trees", "Engineer", "Open"),
    ("Services", "Water tanks: two interconnected 500 L tanks (1,000 L) on a 3 ft galvanised steel stand along the terrace's north parapet at its north-west corner, under the canopy's shade, filled from the sump by pump, with a pressure pump for the showers; the engineer to check the slab edge beam under the stand, and a teak or jali screen to hide them from the north neighbour", "Plumber / engineer", "Open"),
    ("Services", "Electrical load (ACs in five rooms: the master, the den, the family room, Bedroom 2 and the upstairs family room), service connection size, earthing, inverter / solar PV; the LiFePO4 inverter sits outside the south wall at the kitchen's south-west corner in an IP54 heat-shielded box, its cable through a 50 mm sleeve to the main DB in the cupboard R48", "Electrical engineer", "Open"),
    ("Vastu", "Placements as drawn: main door on the east wall in its north half; the open courtyard on the house centre; pooja in the north-east corner opening west (family faces east); kitchen south-east, cook faces east; master bedroom south-west with the bed head south; den north-west; stair in the west band, rising clockwise; the upper mass only over the west band and the den (north-west), the north-east and east low; sump in the north-east; no toilet in the north-east. Confirm which boundary and which centre the consultant uses", "Vastu consultant", "To confirm"),
    ("Vastu", "Courtyard planting: the owner chose a tulsi in the raised centre bed (24 Nov 2026); the consultant to confirm that a plant (not a tree) in the brahmasthan is right. The {court} court under a {ring_eave} eave gets only a few hours of direct sun, so a tulsi in a pot set in the bed (moved out to the sun when it needs to) may grow better", "Vastu consultant / owner", "To confirm"),
    ("Vastu", "Bathroom doors and mirrors: every basin and mirror stands straight opposite its bathroom door (an owner decision carried over from the duplex), but some sources dislike a mirror facing a door; the consultant to say whether the mirrors stay or move to a side wall, and to check each bath door's position", "Vastu consultant", "To confirm"),
    ("Vastu", "Roof terrace canopy kept full length over the terrace (north-east of the upper mass): a light structure on open posts, but it adds height toward the north-east; the consultant to confirm", "Vastu consultant", "To confirm"),
    ("Vastu", "Overhead tanks: the two tanks stand on their stand at the terrace's north-west corner (the north side of the house, west of its centre); vastu usually prefers overhead water in the south-west, which here is the tiled wing roof; the consultant to confirm the position", "Vastu consultant", "To confirm"),
    ("Climate", "Roof terrace canopy: decide between tiles on steel (drawn, to match the roof) and an insulated metal-sheet roof on the same frame before the roof is ordered; either way the frame and the fixings are designed for cyclone uplift on its open sides; chiks on the open sides in the hot months", "Owner / engineer", "Open"),
    ("Levels", "Survey road and field levels; plinth at 2 ft above finished ground (raise if the site floods); the sunk courtyard floor, {court_drop} below the walkway (6 in below the rooms), must still drain to the sump", "Surveyor / architect", "Open"),
    # Earlier room reviews (54 x 54 ft house), re-checked against the compact plan. The owner approved only Group B (elderly parent and
    # access: built in). Groups A, C and D below are NOT approved: each is a proposal for the owner.
    ("Review A: safety", "Thinnai and main door in driven rain: the thinnai faces the east (the cyclone side), open past its lean-to, and the foyer floor is at the thinnai level, so only the weather bar at D01 and the 1:100 fall of the platform keep driven rain out. Proposed in addition: a 3 in sill at D01, a scupper at the platform's east edge, rough-trowelled red oxide within 4 ft of the steps and the door, and bamboo chiks or louvres between the pillars in October-November", "Owner / architect", "Not approved"),
    ("Review A: safety", "Utility service steps (south door D18): the landing was 1'-3\" deep and its risers did not reach the ground from the plinth. Now drawn as proposed, for the owner to confirm: a landing 3 ft deep one riser below the utility floor, four risers of about 5.9 in in all on 10.8 in treads down along the wall, and an SS grab rail on the wall (the kitchen line's chamber IC-22 moved east, clear of the steps)", "Owner / architect", "Not approved"),
    ("Review A: safety", "Courtyard edge at night: the walkway drops 5 in to the court with no guard and the tulsi kerb is 18 in high, both in rough granite. Proposed: a contrasting nosing and a low step-light strip along the court edge", "Owner / architect", "Not approved"),
    ("Review A: safety", "Pooja: a 3 in step up into the pooja, and lamps and camphor burn with no heat alarm or extinguisher near. Proposed: a 1.5 in teak sill (or a rail on the jamb), an interlinked heat alarm and a small extinguisher in the family room by the pooja door", "Owner / architect", "Not approved"),
    ("Review A: safety", "Kitchen hood outlet: the cooker hood's duct leaves through the high vent W83 about 2'-6\" north of the LPG cage. Proposed: a cowl that throws the exhaust up and north, away from the cage and the rinse shower", "Owner / architect", "Not approved"),
    ("Review A: safety", "Escape window W37 from Bedroom 2 opens onto the master bath's tiled roof (eave {ring_eave}): a refuge only, with no way down. Proposed: a note on the drawings and a hold-fast or ladder bracket at the eave below it", "Owner / architect", "Not approved"),
    ("Review A: safety", "Main DB in the DB and linen cupboard R48: keep 1 m (3'-3\") in front of it clear of linen shelves, marked on the floor", "Owner / electrician", "Not approved"),
    ("Review A: safety", "Roof terrace canopy in a cyclone: tiles on an open-sided canopy can lift. Proposed: the engineer designs the frame and every tile's fixing for uplift, or the canopy takes an insulated metal sheet (see the canopy item)", "Owner / engineer", "Not approved"),
    ("Review C: comfort", "Family room AC: the L (living, console nook, oonjal link and dining end, about 430 sq ft) has one AC, and the foyer's 4 ft opening and the main door never close onto it. Proposed: a sliding teak-and-glass leaf in the 4 ft opening, and the MEP engineer to size the unit (about 2 ton, or two units)", "Owner / MEP engineer", "Not approved"),
    ("Review C: comfort", "Sound round the den: the family living's TV console is on the den's east wall, right behind the den's sofa-bed, and the upstairs family room with its screen is over the den. Proposed: 50 mm mineral wool and board on the den face of that wall, and a floating floor or an acoustic underlay in the upstairs family room", "Owner / architect", "Not approved"),
    ("Review C: comfort", "Master bedroom light and air: its windows are all small and on the hot south and west (W60, W61, W66, W67: about 12% of the floor). Proposed: widen the two west windows to 3 ft under the 2 ft eave", "Owner / architect", "Not approved"),
    ("Review C: comfort", "Daily routes round the open walkway: the master, the den and the stair reach the kitchen, the family room and the pooja only along the walkway, through folding doors bolted at night. Proposed: one end leaf of each folding set a hinged daily door, and insect mesh on the folds", "Owner / architect", "Not approved"),
    ("Review C: comfort", "Shade cloth and grille: a hand-pulled cloth over the court in a Guntur May. Proposed: a motorised cloth with a wind and rain trip, and 25 mm bird mesh on the grille", "Owner / architect", "Not approved"),
    ("Review C: comfort", "Laundry through the upstairs family room: wet washing goes from the gallery door D36 across the AC'd family room to the terrace door D49. Proposed: keep a 3 ft clear path between the two doors with a washable runner, and an anti-vibration pad under the washer against the family room's east wall", "Owner", "Not approved"),
    ("Review C: comfort", "Pantry: the walk-in pantry has one shelving run on its west wall. Proposed: shelves on its north and south walls too, for rice, oil tins and pickle jars", "Owner", "Not approved"),
    ("Review C: comfort", "Pocket garden F124: an 8 in bed 2'-6\" out from the dining end's east wall sits below the line of sight from the bench (2 ft plinth, 2'-6\" sill). Proposed: a raised bed or taller planting against a low screen wall further out", "Owner", "Not approved"),
    ("Review C: comfort", "Uruli in the foyer niche: open water breeds mosquitoes. Proposed: change the water daily or keep a few fish in it", "Owner", "Not approved"),
    ("Review D: site", "Arrival on foot: no paved path from the gate's wicket to the forecourt; you walk the gravel drive and past the parked car under an open pergola, uncovered in rain. Proposed: a 3-4 ft stone path beside the drive and a tiled bay over the car porch's west end", "Owner / architect", "Not approved"),
]

COURTYARD_DECISIONS = [
    "A Tamil courtyard house (24 Nov 2026, owner): the house is built round a small open courtyard (mutram) on the brahmasthan, the centre of the house, with a thinnai at the front. Every feature and decision from the duplex carries over unless this log says otherwise. The duplex design stays on its own branch, unchanged.",
    "Compact house on a {plot} plot (24 Nov 2026, owner): the plot is 50 ft wide (north-south) by 130 ft deep with the road on the east; the house is {house}, set towards the back of the plot, with a {back_garden} back garden, {side_strip} strips on the north and south, and {front_land}. It replaces the 54 x 54 ft courtyard house on a 70 x 160 ft plot: about {enclosed_area} sq ft enclosed ({ground_area} ground, {upper_area} upper) instead of about 3,300.",
    "A tight ring (24 Nov 2026, owner): rooms in {band} bands round a {walk} pillared walkway (thazhvaram) and a {court} open courtyard on the house centre; every room opens onto the walkway or the family room. Rejected earlier: a U open to the east (the court loses privacy) and a deep agraharam (the court is too small).",
    "Storeys (24 Nov 2026, owner): the ground floor runs round the court; one upper wing stands over the west band and the den, with a roof terrace over the living. All daily life stays on one level. For vastu the upper mass stays west and north-west, and the north-east and east stay low.",
    "Merged rooms (24 Nov 2026, owner): the genkan and the entry hall become one small foyer; the oonjal moves out of its own hall into the console nook, open to the family room; living and dining become one L-shaped family room; the upstairs reading room and theatre become one upstairs family room.",
    "Compact ground floor approved (24 Nov 2026, owner): the master bedroom in the south-west ({clear:R01} clear) with its bath east of it; the powder room, pantry and utility on the south band; the kitchen in the south-east ({clear:R15}); the family room L (living {clear:R16}, console nook, oonjal link and dining end {clear:R16D}); the foyer on the east wall; the pooja in the north-east corner; the den in the north-west ({clear:R42}) with its bath, desk niche and walk-in; the stair against the west wall.",
    "Compact first floor approved (25 Nov 2026, owner): the hotel-style Bedroom 2 suite over the master (the stair head, then the walk-in / dressing lobby {clear:R45}, then Bedroom 2 {clear:R31} with the bed head south one way, and its bath {clear:R33} with the WC on the west outer wall the other); a gallery beside the stair well with the first jharokha; the upstairs family room over the den ({clear:R36} plus a desk nook) with the bookshelf wall, the screen, the sofa-bed and the second jharokha; the upper toilet over the den bath, entered from the desk nook; the roof terrace off the family room.",
    "Courtyard open to the sky (24 Nov 2026, owner): a sunken stone floor {court_drop} below the walkway (6 in below the rooms) with two corner drains (CD to the first-flush filter and the sump; CD-2 on its own overflow line with a standpipe and a scupper), a steel grille at the inner eave and a pull-across shade cloth. Rain and night sky inside the house, the most cooling at night, and secure.",
    "Tulsi in the courtyard (24 Nov 2026, owner): the round raised bed at the courtyard's centre holds a tulsi, not a frangipani or a neem. The vastu consultant is still to confirm the planting.",
    "Thinnai (24 Nov 2026, owner): in place of the poomukham the house has a thinnai: one raised platform {size:R17} on the east, 1'-6\" above the forecourt, either side of the main door, with turned teak pillars, sloping lime-plastered backrests and a red oxide floor (not stone). The kolam stone sits at the door, the nilavilakku pedestal beside it, and copper rain chains hang at the front corners. Three steps lead down to the forecourt.",
    "Foyer and main door (24 Nov 2026, owner): the main door is on the east wall in its north half, carved teak with brass studs. It opens into the foyer at the thinnai level, with the shoe bench and the uruli niche; one 6 in step up through a 4 ft opening in its jali screens leads into the family room.",
    "Oonjal and pooja (24 Nov 2026, owner): the oonjal hangs from the ceiling beam in the console nook and faces west into the living (the court lies behind the walkway, so it no longer faces the court); the pooja is in the north-east corner, opening west into the family room so the family faces east. There is no toilet in the north-east.",
    "Both swings kept (24 Nov 2026, owner): the oonjal indoors in the console nook and a second swing on the roof terrace, so there is one to use in the rain and one under the sky.",
    "Family room (24 Nov 2026, owner): one L-shaped room: the living on the north with the TV console on its solid west wall and diwans under the north windows; the console nook and the oonjal link; the dining end next to the kitchen with a 16 in bench under the east windows, an extending table with tuck-under stools, an armchair, a hand-wash basin and the pocket garden outside. Teak-and-glass folding doors open it to the north and east walkways.",
    "Kitchen and utility (24 Nov 2026, owner): the kitchen in the south-east has an L-counter with the prep sink under the south window and the hob on the east wall under the high vent; the pantry and the utility lie west of it; the utility has the washer, the sink and a service door to the south side. The LPG cage stands outside the east wall, 1.5 m or more from every open drain, gully and chamber; the rinse shower is north of it.",
    "Den (24 Nov 2026, owner): in the north-west, off the north walkway: the sofa-cum-bed, an armchair and the TV on its west wall; a desk niche with the garden door onto the engawa deck; a walk-in wardrobe; its bath ({clear:R07}) in the north-west corner with the basin opposite its 3 ft door, which opens outward.",
    "Stair (24 Nov 2026, owner): a dog-leg against the west wall, rising clockwise from a 3'-6\" foot lobby: 16 risers of 7.5 in, 10 in treads, flights and half landing 3'-6\" clear between wall faces, handrails on both sides, the core wall full height, arriving facing south toward the Bedroom 2 suite. The landing window's sill is 3'-0\" above the landing; the store under the landing is a low hatch store; the DB and linen cupboard is under flight 2. The stair lobby's sliding door D09 closes the stair and the upstairs off (in place of the stair-head jali door).",
    "Jharokhas (24 Nov 2026, owner): two teak bays 4 x 2 ft over the walkway roof, looking down into the courtyard: the gallery's at the stair head faces east, the upstairs family room's faces south from its south wall. Each seat is 2'-0\" above the floor with a 6 in step and a grab rail, fixed jali with gaps of 100 mm or less up to 3 ft above the seat and glazing above; the bays have no roofs of their own (the wing's eave covers them). They sit inside the house, not in a setback.",
    "Roof terrace (25 Nov 2026, owner): {size:R37} over the living, reached from the upstairs family room through glazed sliding doors; the swing facing south into the courtyard, a daybed facing east, a jasmine trough and the laundry corner against the family room's east wall; a teak jali parapet on the north and railings on the south and east. It is in place of the duplex's covered terrace and east balcony.",
    "Terrace canopy, guard wall and tanks (25 Nov 2026): designer decisions, not owner-approved: a light tiled canopy on six steel posts at {canopy}, kept full length; a {upstand} upstand under the south railing and a level {corner_guard} guard wall at the south-east corner, where the ring's ridge meets the terrace edge; two 500 L tanks on a 3 ft stand at the terrace's north-west corner. The vastu consultant is to confirm the canopy and the tanks.",
    "Roof (25 Nov 2026): clay Mangalore tiles at {pitch}. The ring: eave {ring_eave}, ridge {ring_ridge} along the middle of each band, the inner slope over the walkway into the courtyard. The wing: an L-shaped hipped roof over the west band and the upstairs family room, eave {wing_eave}, ridge {wing_ridge}, with a soldered box gutter at its re-entrant corner and {spreaders} short spreader downpipes onto the ring. The thinnai lean-to ({thinnai_clear} clear at the pillars); the terrace slab at {terrace_slab}; a 2 ft chajja over the living's north windows W75/W76; {downpipes} downpipes. These are in place of the duplex's front gable, kitchen wing and chaipu roofs.",
    "Elderly parent and access, Group B (24 Nov 2026, owner): grab rails beside every WC and in the master and den showers; fold-down shower seats in the master and den baths; pull-cord alarms in both, sounding in the kitchen and the den; low 1 ft motion footlights on the master's bed-to-bath route; bath doors of 2'-8\" or more for the den bath and the powder room; handrails on both sides of the entrance steps and a grab post at the foyer step; a reserved 1:12 ramp to the thinnai; a 16 in dining bench and an armchair; a reading chair in the master; jharokha seats at 2'-0\" with a grab rail at the step.",
    "Safety fixes from the first reviews (24 Nov 2026): a second courtyard drain with a standpipe overflow and a scupper; the stair landing window's sill 3 ft above the landing; exhaust fans only through outer walls (the powder room's ducted to the south wall); no shower open toward a WC or a door; the store under the landing a low hatch store; the LPG cage 1.5 m from every open drain and chamber; the inverter never beside a bedroom's only exit; the water tanks on a shaded stand, not in a roof void; interlinked smoke alarms in the master, the den and Bedroom 2 as well as at the stair.",
    "Inverter outside (24 Nov 2026): the LiFePO4 inverter and battery stand outside the south outer wall at the kitchen's south-west corner pier, beside the utility, in an IP54 heat-shielded, ventilated steel box 3 ft up under the eave, 3.5 ft or more from every door, window and vent, with its cable through a 50 mm sleeve to the DB. The ruling put it on the utility's south wall; that wall has no spot 3.5 ft clear of its window, its service door and the powder room's fan terminal, so it sits just east of the utility. Never under the stair, in a cupboard or beside a bedroom's exit.",
    "Distribution board (24 Nov 2026): the main DB in a lockable teak cabinet in the DB and linen cupboard under flight 2, off the stair lobby, central and dry, with the first-floor sub-board on the gallery's east wall.",
    "Materials and character (24 Nov 2026, owner): AAC blocks with lime plaster in warm white and ochre (9 in outside, 7 in where there is plumbing, 5 in inside); Athangudi tiles in the family room; red oxide in the bedrooms, the den, the stair, the pooja and the thinnai; rough-dressed stone in the courtyard, the walkway and the foyer; anti-skid ceramic in the baths; teak for the main door, pillars, jharokhas, jali screens and internal doors; kolam stones, oil-lamp niches and brass hardware; warm layered light.",
    "Climate (24 Nov 2026, owner): the courtyard draws hot air up and out by day, the west wing shades it from the afternoon sun, and cooler air settles in it at night. AC is provided in the master, the den, the family room, Bedroom 2 and the upstairs family room, and the doors onto the walkway close when the AC runs.",
    "Services (24 Nov 2026): the sump on the north strip beside the forecourt takes the roof and courtyard rain through the first-flush filter and is topped up from the road main; it feeds the drip lines and, by pump, the two interconnected 500 L tanks on the terrace stand, with a pressure pump for the showers. Soil goes to the sealed septic tank south-east of the forecourt and its effluent to the soak pit on the south side; bath grey water goes to the soak pit; kitchen grey water through a grease trap to the banana circle; the sump overflows to the recharge pit. Stacks: Bedroom 2's bath on the west outer wall; the upper toilet's own stack in the den bath's corner chase; the den bath on the north wall.",
    "Site (24 Nov 2026, owner): the forecourt has stone paving and the tulsi thara on the door axis, with the parijat on its north edge and a neem at its north-east corner; the car porch (18 x 10 ft under a vegetable-creeper pergola) and the drive run along the north side to a gate in the north-east; the kitchen garden, the herb spiral, the banana circle, the fruit guilds, the vegetable beds, the workshop and the two rental shops lie to the south and south-east. Every tree except the neem stands 25 ft or more from the house.",
    "Vastu placements (24 Nov 2026, owner): main door on the east wall in its north half; the courtyard on the house centre; pooja in the north-east; kitchen in the south-east; master bedroom in the south-west, bed head south; den in the north-west; stair in the west band; the upper mass only in the west and north-west; no toilet in the north-east.",
    "Phasing (24 Nov 2026, owner): three stages, roof first. Stage 1 is the lived-in ground-floor ring with basic finishes, the courtyard, the full roof and the wing's structure; stage 2 is the ground-floor upgrades, the upstairs shell and the roof terrace; stage 3 is the upstairs fit-out. The costs on sheet A-002 are rough estimates for about {enclosed_area} sq ft, to be re-priced by a quantity surveyor.",
]

DUPLEX_DECISIONS_CARRIED = [
    "Carried over from the duplex: the soul of the house (23 Nov 2026, owner): a window seat (now the two jharokhas); a tokonoma niche with a brass uruli of flowers in the foyer, seen as you step up into the family room; a kolam stone at the main door and a stone pedestal for the nilavilakku lit at dusk; layered warm light (switched lamp sockets on the door switch, dimmable ceiling lights, low stair lights); a teak engawa deck outside the den's garden door; copper rain chains into pebble basins at the thinnai's front corners; a few clear glass Mangalore tiles in the roof over the stair; the stair-head jharokha in place of the landing sill; a pocket garden outside the dining end's east window; a garden rinse shower outside the kitchen; jasmine on the thinnai pillar and the terrace and a parijat in the forecourt; a low daybed facing east on the terrace.",
    "Carried over from the duplex: bathrooms planned round the door (23 Nov 2026, owner): every basin and mirror stands straight opposite its bathroom door, the WC is never in line with the door and never in a mirror's view; vastu prefers mirrors on north or east walls and WC seats facing north or south. Some vastu sources also dislike a mirror facing a door: to confirm with the vastu consultant.",
    "Carried over from the duplex: dining stools (23 Nov 2026, owner): the dining end has a bench and an extending table with backless teak stools that slide fully under it, so between meals nothing stands in the way.",
    "Carried over from the duplex: a bookshelf wall upstairs (23 Nov 2026, owner): the upstairs family room's north wall takes a floor-to-ceiling teak bookshelf with closed cupboards at the base and lit open shelves above, held off any wet wall, with the reading armchair and a floor lamp in its corner. Since the merge (24 Nov 2026) the same room also holds the screen.",
    "Carried over from the duplex: hotel-style Bedroom 2 suite (22 Nov 2026, owner): the bath is reached through the walk-in (bedroom, then walk-in, then bath, so you bathe, dress and come out ready), with a drop seal and no louvre on the bath door; a full-length mirror in the walk-in; the bath fan on a run-on timer and a high jali window over the hanging run to keep steam off the clothes; a motion footlight and 2-way switching for night use. Guests use the upper toilet off the family room's desk nook.",
    "Carried over from the duplex: master suite doors (22 Nov 2026, owner): the master bath door is 2'-9\" opening outward on lift-off hinges; the bedroom door is 2'-10\" (the walkway allows no more than that, not 3 ft); night footlights and pull-cord alarms (Group B).",
    "Carried over from the duplex: the stair standard (2-22 Nov 2026, owner): 16 risers of 7.5 in, 10 in treads, 3'-6\" flights, teak handrails on both sides, contrasting anti-slip nosings, and guards 4'-0\" high with gaps of 100 mm or less and nothing to climb on beside them. 17 risers would only crowd the foot of the stair.",
    "Carried over from the duplex: fire and safety (22 Nov 2026, owner): interlinked smoke alarms at the stair foot and head and in the master, the den and Bedroom 2, a heat alarm in the kitchen, every geyser and bath socket outside the shower zones and on an RCD, and an LPG cylinder cage outside the kitchen's east wall with a fixed line.",
    "Carried over from the duplex: a quiet screen room (22 Nov 2026, owner): the theatre's sound insulation (50 mm mineral wool and board on its walls, a solid-core door with seals) goes into the upstairs family room, which now holds the screen and sits over the den.",
    "Carried over from the duplex: laundry waste (22 Nov 2026, owner): the washer and laundry sink on the terrace drain down a boxed duct on the north wall to the grey line, never to the terrace outlet or the rain line that feeds the sump.",
    "Carried over from the duplex: the permaculture food system on the front land (3 Nov 2026, owner): a kitchen garden and herb spiral near the kitchen with a banana circle fed by the kitchen's grey water; fruit guilds (guava, sapota, lemon, pomegranate, custard apple, drumstick, each with pigeon pea, vegetables, ground cover and turmeric under it) with the compost pits and a worm bin; raised beds, mulched, on drip and under a shade net in April-May; vegetable creepers on the car porch pergola; a gliricidia and pigeon-pea living fence on the south boundary; the drip lines run from the sump, which takes the roof rain through a first-flush filter and is topped up from the road main.",
    "Carried over from the duplex: vastu for the plot (3 Nov 2026): the way for cars on the right (north) as you face the house from the road, the gate in the north-east of the road front with a 10 ft drive along the north side to a car porch beside the forecourt; the shops on the road front in the south-east; the workshop and vegetable beds on the sunny south side; the soak pit on the south side; the sump and the borewell in the north-east.",
    "Carried over from the duplex: workshop and shops are demountable and cheap (3 Nov 2026): a bolted galvanised steel frame on anchor-bolt pad footings, precast RCC post-and-panel walls (the compound-wall system, so panels lift out), insulated metal sandwich roofs on steel purlins, PCC or paver floors, rolling shutters, and a ready-made toilet cabin shared by the workshop and the shops, so nothing is wasted if they move or come down.",
    "Carried over from the duplex: compound wall (2 Nov 2026): precast RCC post-and-panel (2 in panels in 4 in posts) set just inside the plot line.",
    "Carried over from the duplex: kitchen details (2 Nov 2026): drawers first, a pull-out masala drawer by the hob with a utensil rail, a tall pantry, a counter return by the sink and a chimney ducted straight out.",
    "Carried over from the duplex: Guntur, not Kerala (earlier): the site is farm land in Guntur, Andhra Pradesh; the Kerala style is kept, with construction adapted to the local climate and soil.",
    "Carried over from the duplex: structure and levels: an RCC frame with AAC block walls, 9 in outer, 5 in inner and 7 in where plumbing is concealed; the plinth 2 ft above finished ground; the thinnai and the foyer one step (6 in) below the house floor; bathrooms 12 mm lower than the room beside them, with no raised threshold.",
    "Carried over from the duplex: AC provisions (points, sleeves, drain and outdoor-unit brackets under sun-hoods) in the master, the den, the family room, Bedroom 2 and the upstairs family room, with passive cooling first; inverter circuits for lights, fans and the routers.",
    "Carried over from the duplex: the roof is Mangalore clay tile on a steel or timber frame over insulated cement-fibre deck, every edge tile mechanically fixed against cyclone winds.",
    "Carried over from the duplex: roof-first phasing (2 Nov 2026): the structure, roof, waterproofing and every buried pipe and conduit are never deferred; the stages are the courtyard house's own (see PHASES).",
]
DECISIONS = COURTYARD_DECISIONS + DUPLEX_DECISIONS_CARRIED

# Specification: category, element, specification, reason (Guntur-specific where relevant)
SPEC = [
    ("Substructure", "Soil investigation", "Min. 2 bore holes to 3 m or refusal; swell test, SBC", "Black cotton soil swells when wet and shrinks when dry"),
    ("Substructure", "Foundations", "As per engineer: footings below the active zone (often 1.5-2.5 m) or under-reamed piles; 300 mm sand/moorum cushion; the courtyard's edge beam and the walkway pillars on their own footings", "Prevents seasonal heave cracking"),
    ("Site", "Compound wall", "Precast RCC post-and-panel wall, 5 ft high: 4 in square posts at about 7 ft centres on small pad footings, 2 in slotted panels, set just inside the plot line; panels lift out", "Thinnest practical wall: keeps the 4 ft side strips usable; cheap, quick and reusable"),
    ("Substructure", "Plinth beam + DPC", "RCC plinth beam all round; 40 mm DPC with waterproofing compound at plinth top", "Stops rising damp into AAC"),
    ("Substructure", "Plinth fill", "Non-expansive moorum / gravel in 150 mm layers, compacted; no black soil fill", "Black soil under the floor will heave the slab"),
    ("Substructure", "Anti-termite", "Pre-construction chemical treatment (IS 6313) at foundation, plinth fill and around walls", "High termite risk; cannot be redone easily later"),
    ("Substructure", "Plinth protection", "3 ft PCC apron with slope away, joint sealed to wall", "Keeps rain off expansive soil next to foundations"),
    ("Frame", "Columns, beams, bands", "RCC frame; lintel band at door head, ring beam at wall top; seismic zone III detailing (IS 13920 as engineer decides)", "AAC infill is not load-bearing for truss + cyclone loads"),
    ("Frame", "First-floor slab and stair", "RCC slab over the west wing, the den block and the roof terrace (about 5 in, by engineer) with drop beams at the stair well and edge beams round the terrace (also under its south-east corner guard, where no wall stands below); dog-leg RCC stair, 16 risers of 7.5 in, 10 in treads, 3'-6\" flights, waist slab by engineer; columns under the wing run full height for two floors", "Two storeys in the wing: the slab carries the Bedroom 2 suite, the upstairs family room, the terrace and the two water tanks"),
    ("Frame", "Courtyard walkway and thinnai", "Turned teak pillars on stone bases and pad footings round the court and on the thinnai; the courtyard slab sunk {court_drop} below the walkway (6 in below the rooms) with two corner drains (150 mm), a standpipe overflow and a scupper; a galvanised steel grille at the inner eave with a track for the shade cloth", "The walkway and the thinnai carry only the ring roof's edges; the sunk court must drain in a 100 mm-per-hour downpour even with one drain choked"),
    ("Frame", "Roof terrace canopy frame", "Six hot-dip galvanised steel posts (about 100 x 100 mm SHS) on RCC column stubs at the slab edge, bolted base plates with grout; steel trusses and purlins carry the canopy roof at {canopy}, with a steel hanging beam across the trusses over the swing (rated 200 kg); designed for uplift on its open sides; all steel primed and painted, bolted connections", "A light frame instead of walls keeps the terrace open; galvanising resists the humid air"),
    ("Walls", "AAC blocks", "IS 2185-3, 200 mm outer / 150 mm wet walls / 100 mm inner; thin-bed polymer mortar", "Better insulation than brick; lighter frame"),
    ("Walls", "AAC to RCC joints", "Galvanised mesh strip 150 mm wide over every block-concrete joint before plaster", "The most common AAC crack; cheap to prevent"),
    ("Walls", "Chasing", "Cut chases with a groover, never hammer; fill with polymer mortar + mesh", "Hammering cracks AAC blocks"),
    ("Walls", "External plaster", "20 mm lime-finish plaster, two coats, waterproof admixture, cured 7 days; lime-wash in warm white and ochre", "Wind-driven cyclone rain"),
    ("Walls", "Sound", "50 mm mineral wool and board on the upstairs family room's walls; a solid-core door with seals to the gallery", "The screen room sits over the den, where guests sleep"),
    ("Roof", "Structure", "Steel truss or rafters (hot-dip galvanised or epoxy primed; timber rafters where the owner chooses them), {pitch} pitch, bolted to the ring beam with holding-down bolts; the ring's ridge along the middle of each band ({ring_ridge}, eave {ring_eave}); an L-shaped hipped roof over the wing (eave {wing_eave}, ridge {wing_ridge})", "Uplift in cyclone winds"),
    ("Roof", "Deck and insulation", "Cement-fibre board deck + 50 mm PIR/XPS or reflective insulation + membrane, then battens and Mangalore tiles; 2 ft overhangs on the outer walls", "Cuts attic heat in 45 C summers"),
    ("Roof", "Tile fixing", "Clip or screw every tile at eaves, verges, ridges and hips, and every 3rd row elsewhere; ridges bedded and pointed", "Loose tiles fly in cyclones"),
    ("Roof", "Ventilation", "Ridge vents with bird and insect mesh; soffit vents at eaves", "Flushes hot air from the attic"),
    ("Roof", "Gutters and downpipes", "150 mm half-round gutters with leaf guard on every outer eave of the ring and the wing; {downpipes} downpipes of 100 mm (on the south side only at {south_dps}: the ring's south gutter drains to the one at {ring_south_dp}, with no second pipe because the south pipe strip is full of drain lines; the engineer to check that run or upsize it to 200 mm); the wing's courtyard-side gutters fall from the soldered box gutter at its re-entrant corner to {spreaders} short spreader downpipes onto the ring roof; the terrace outlet through the north parapet into its downpipe; the thinnai's rain chains; the two courtyard drains; all to the first-flush filter and the sump, overflow to the recharge pit", "Short heavy bursts; protects the plinth"),
    ("Roof", "Terrace edges", "A {upstand} RCC upstand on the south side under the railing, a level {corner_guard} solid guard wall at the south-east corner, a verge wall 6 in over the ring roof on the east side; apron and step flashing with lead counter-flashing in a chase; the slab at {terrace_slab}", "Every edge is 6 in or more over the roof beside it, and the guard meets the 4 ft rule"),
    ("Openings", "Windows", "Hardwood or UPVC frames; mosquito mesh on every opening; MS grill for security", "Mosquitoes; ground-floor security"),
    ("Openings", "Courtyard doors", "Teak frames with toughened glass, folding (bi-fold) panels on a top track and a flush floor channel, on the family room's sides to the north and east walkways; stacked to the piers by day, bolted at night", "Every room opens onto the walkway; the doors close when the AC runs"),
    ("Openings", "Sills and sunshades", "External sills sloped 1:10 with drip groove; 2 ft sunshades with drip groove", "Stops staining and water entry"),
    ("Openings", "Vents above inner doors", "Pooja and main door: open jali; bedrooms, the den and the upstairs family room: closable jali; bathrooms and cupboards: louvres; all in the door transom, 7'-6\" to 9'-0\" above the lintel band", "Air moves with doors shut where privacy allows"),
    ("Openings", "Bathroom doors", "WPC / FRP shutters on WPC or granite frame base; no wooden frame touching the wet floor", "Wood frames rot at the bottom"),
    ("Joinery", "Jharokhas", "Teak bay 4 x 2 ft on a steel bracket frame and a 6 in flashed kerb over the walkway roof, carried up to the wing's eave soffit (no roof of its own), cushioned seat 2'-0\" above the floor with a 6 in step and a grab rail, fixed jali with gaps of 100 mm or less up to 3 ft above the seat, glazed above", "A window seat looking down into the courtyard, safe for children"),
    ("Floors", "General", "4 in skirting flush with the wall plaster (groove in plaster); 3 mm epoxy grout in wet areas", "No dust ledge, no black grout lines"),
    ("Floors", "Athangudi tile", "Handmade cement tile in the family room (living, console nook, oonjal link, dining end); sealed before use, laid on a cement bed with thin joints; a few boxes extra for later repairs", "Stains easily when unsealed; patterns cannot be matched later"),
    ("Floors", "Wet rooms", "Waterproofing (polymer cementitious) floor + 12 in up walls + 7 ft in shower; flood test 48 h before tiling", "Leak into neighbouring rooms is the top complaint"),
    ("Plumbing", "Supply", "CPVC hot/cold; supply runs along external walls in clamps or shallow chases; isolation valve per bathroom and kitchen", "Easy repair without breaking tiles"),
    ("Plumbing", "Drainage", "uPVC SWR 110 mm soil, 75 mm waste; inspection chamber at every bend and junction, no two within 2 ft; separate soil and grey-water lines; at every crossing soil runs lowest, the upper pipe sleeved", "Easy rodding"),
    ("Plumbing", "Water treatment", "RO for drinking at kitchen; whole-house softener if hardness > 300 mg/l; matt fittings", "Guntur groundwater is often hard with high fluoride"),
    ("Plumbing", "Storage", "Two interconnected 500 L tanks on a 3 ft galvanised steel stand at the terrace's north-west corner, under the canopy, overflow to the terrace outlet; a pressure pump for the showers", "Shade keeps the water cool; no tank in a hot roof void"),
    ("Electrical", "Wiring", "FR-LSH copper; 1.5 sq mm lights, 2.5 sq mm sockets, 4 sq mm AC / geyser; separate circuits per AC", "AC loads"),
    ("Electrical", "Protection", "RCCB 30 mA + MCBs; 2 earth pits; surge protection device; the main DB in a lockable teak cabinet in the cupboard under flight 2, the sub-board on the gallery's east wall", "Shock and lightning safety"),
    ("Electrical", "Backup", "Inverter circuit to lights, fans and the routers; the LiFePO4 inverter in an IP54 heat-shielded, ventilated steel box outside the south wall at the kitchen's south-west corner, 3.5 ft or more from every opening; conduit from roof to DB for future solar PV", "Power cuts during work-from-home; a battery fault stays outside the house"),
    ("Electrical", "AC provisions", "16 A socket at 7 ft, 65 mm sleeve through wall, drain pipe to outside, ODU brackets on shaded walls under louvred sun-hoods", "Retrofitting later means breaking walls"),
]

# Electrical points: code, x, y, room, note. Heights above FFL are set per code in ELEC_TYPES.
ELEC_TYPES = {  # code: (description, mounting height)
    "L": ("Ceiling light", "ceiling"), "WL": ("Wall light / mirror light", "6'-6\""), "F": ("Ceiling fan point", "ceiling"),
    "EF": ("Exhaust fan", "7'-0\""), "CH": ("Kitchen chimney point (16 A)", "7'-0\""), "S": ("Switchboard", "4'-0\""),
    "P": ("6 A socket", "1'-0\""), "LS": ("Switched lamp socket (6 A) on the room's door switch, for floor and table lamps", "1'-0\""), "PC": ("6 A socket at counter", "3'-6\""), "P16": ("16 A power socket", "varies"),
    "U": ("Inverter (UPS) socket", "1'-0\""), "D": ("Data point (Cat6)", "1'-0\""), "TV": ("TV + data point", "3'-6\""),
    "AC": ("AC indoor unit (16 A socket, sleeve, drain)", "7'-6\""), "ODU": ("AC outdoor unit bracket", "7'-0\" outside"),
    "G": ("Geyser (16 A)", "6'-6\""), "DB": ("Distribution board", "5'-0\" to top"), "INV": ("Inverter + battery", "floor"),
    "MTR": ("Meter at gate", "5'-0\""), "SA": ("Smoke alarm, interlinked, mains + battery", "ceiling"), "HA": ("Heat alarm, interlinked", "ceiling"), "EP": ("Earth pit", "ground"), "BELL": ("Bell push", "4'-6\""), "CAM": ("CCTV point", "8'-0\""),
    "GL": ("Outdoor / gate light", "7'-0\""),
    "FL": ("Low motion footlight (PIR, warm, switch-off after 2 minutes): the master's bed-to-bath route, stair and step lights", "1'-0\""),
    "PA": ("Pull-cord alarm (Group B: cord to 6 in above the floor, reachable from the floor), sounds at the SND points", "ceiling cord"),
    "SND": ("Sounder for the pull-cord alarms (kitchen and den), with a reset button", "7'-0\""),
}
# Ground floor. Wall switches and sockets sit on the wall face inside their room; "outside the bathroom door" means in the room the door opens from.
# The one wall point that stands over a door: the powder room's duct terminal, high over the utility's service door D18 (centre z above
# the utility floor, ft). It sits between the lintel band over the door and the ring beam, so it is not in the door opening.
EF_OVER_DOOR = {"code": "EF", "x": 41.5, "rid": "R13", "door": "D18", "z": 8.25, "cowl": 0.5}
ELECTRICAL = [  # ground-floor points (Task C6)
    # ---- master bedroom R01: lights, fan and lamp sockets on the inverter circuit; AC on the west wall; footlights on the bed-to-bath route ----
    ("L", 21.25, 14.5, "R01", "Ceiling light on a dimmer, over the walkway between bed and wardrobe, never over the bed head"),
    ("L", 19.4, 16.9, "R01", "Wardrobe light, switched at the door"),
    ("F", 21.25, 8.4, "R01", "Ceiling fan over the bed: hook cast in the slab, down-rod; 7 ft+ clear"),
    ("WL", 17.75, 4.45, "R01", "Bedside reading light (west), on its own switch"),
    ("WL", 24.85, 4.45, "R01", "Bedside reading light (east), on its own switch"),
    ("S", 17.3, 4.45, "R01", "Bedside switchboard (west): 2-way with the door switch for lights and fan"),
    ("S", 24.4, 4.45, "R01", "Bedside switchboard (east): 2-way with the door switch for lights and fan"),
    ("S", 27.1, 20.0, "R01", "Door switchboard by D04 (latch side): lights, fan, lamp sockets"),
    ("S", 27.1, 10.6, "R01", "Outside the master bath door D42: bath light, fan, geyser with indicator lamp"),
    ("P", 18.15, 4.45, "R01", "Bedside 6 A charging socket (west)"),
    ("P", 25.2, 4.45, "R01", "Bedside 6 A charging socket (east)"),
    ("P", 27.1, 15.4, "R01", "Dressing table socket (hair dryer, charger)"),
    ("LS", 15.45, 13.0, "R01", "Lamp socket beside the reading chair, on the door switch"),
    ("LS", 24.6, 20.0, "R01", "Lamp socket by the wardrobe end, on the door switch"),
    ("AC", 15.45, 11.8, "R01", "Master AC indoor unit on the west wall, 7 ft 6 in up, throwing east along the bed foot (never over the bed head); 16 A socket, 65 mm sleeve, drain to a gully"),
    ("ODU", 14.2, 11.8, "R01", "AC outdoor unit on a bracket on the west wall, 7 ft up, under a louvred sun-hood (shade from the afternoon sun) with 1 m clear in front of it"),
    ("FL", 26.95, 6.0, "R01", "Low 1 ft motion footlight on the bed-to-bath route (east wall, beside the bed)"),
    ("FL", 26.95, 8.4, "R01", "Low 1 ft motion footlight on the bed-to-bath route"),
    ("FL", 26.95, 10.0, "R01", "Low 1 ft motion footlight beside the bath door D42"),
    # ---- master bath R40 ----
    ("L", 31.2, 10.2, "R40", "Bath ceiling light (8 ft 6 in ceiling)"),
    ("WL", 34.15, 12.35, "R40", "Mirror light over the basin"),
    ("EF", 30.3, 4.4, "R40", "Exhaust fan in W62's upper pane: straight through the south outer wall"),
    ("G", 34.1, 9.6, "R40", "Geyser on the east wall, 2.8 ft from the shower zone (outside the spray); 16 A, own MCB"),
    ("P", 34.15, 13.6, "R40", "IP-rated shaver socket by the mirror (RCBO)"),
    ("PA", 29.6, 6.9, "R40", "Pull-cord alarm in the shower, over the fold-down seat (cord to 6 in above the floor); sounds in the kitchen and the den"),
    ("PA", 30.9, 15.6, "R40", "Pull-cord alarm by the WC, cord to 6 in above the floor; sounds in the kitchen and the den"),
    ("FL", 27.95, 10.3, "R40", "Low 1 ft motion footlight just inside the bath door"),
    ("FL", 31.5, 15.9, "R40", "Low 1 ft motion footlight on the way to the WC"),
    # ---- powder room R08 ----
    ("L", 37.0, 13.3, "R08", "Ceiling light (8 ft 6 in ceiling)"),
    ("WL", 36.2, 9.85, "R08", "Mirror light over the basin"),
    ("EF", 35.1, 9.8, "R08", "Exhaust fan: the powder room has no outer wall, so a 100 mm duct (about 13 ft: 11.8 ft falling 1:100 through the utility's ceiling void, then a 1'-3\" drop in a short boxed bulkhead inside the utility, with a non-return damper at the terminal) runs to the hooded terminal on the south wall over D18 (EF in R13)"),
    ("P", 34.95, 11.5, "R08", "IP-rated socket (hand dryer, shaver)"),
    # ---- utility R13 and the inverter ----
    ("L", 37.5, 7.6, "R13", "Utility ceiling light"),
    ("L", 41.5, 7.0, "R13", "Utility ceiling light"),
    ("EF", 36.5, 4.4, "R13", "Exhaust fan in W64's upper pane, through the south outer wall"),
    ("EF", 41.5, 4.4, "R13", "Hooded louvre cowl (the duct terminal) on the south outer wall for the powder room's duct (about 13 ft from the fan at R08, non-return damper), centred over the service door D18: its centre 8'-3\" above the utility floor, between the lintel band over the door and the ring beam (9'-3\" to 10'-0\"), the duct dropping to it in a short boxed bulkhead inside the utility; a 50 mm drip lip, the hood turned down and away from D18's louvred top; 4.0 ft from the utility window W64"),
    ("S", 43.9, 4.5, "R13", "Switchboard by the service door D18 (latch side)"),
    ("S", 44.1, 8.5, "R13", "Switchboard by the kitchen door D12, utility side"),
    ("P16", 39.1, 4.5, "R13", "Washing machine socket, splash-proof, own MCB"),
    ("P", 37.5, 9.25, "R13", "6 A socket (iron, vacuum), 1 ft up"),
    ("INV", 46.8, 3.95, "R15", "Inverter + LiFePO4 battery in an IP54 heat-shielded, ventilated steel box on the OUTSIDE face of the kitchen's south wall (the SW corner pier), 3 ft above the ground under the eave: 3.5 ft or more from every door, window and vent (nearest: the powder-room fan terminal over D18 at 41.5 and W82 at 50.2), clear of the service landing, every bedroom exit and the stair, so a battery fault stays outside the house; the cable runs through a 50 mm sleeve to the DB in R48"),
    ("SA", 23.5, 14.5, "R01", "Interlinked smoke alarm in the master bedroom (mains + battery), with the stair alarms"),
    ("SA", 25.5, 40.0, "R42", "Interlinked smoke alarm in the den (mains + battery), with the stair alarms"),
    # ---- pantry R60 ----
    ("L", 42.0, 12.8, "R60", "Pantry light"),
    ("S", 44.1, 10.0, "R60", "Switchboard on the pantry face, south of the sliding door D64"),
    ("P16", 39.85, 12.0, "R60", "Microwave socket inside the shelving"),
    # ---- kitchen R15 ----
    ("L", 48.0, 9.0, "R15", "Kitchen ceiling light, 4000 K"),
    ("L", 52.0, 10.5, "R15", "Kitchen ceiling light, 4000 K"),
    ("F", 50.5, 8.0, "R15", "Ceiling fan, clear of the hob's flame: a 3 ft+ shield from the hob"),
    ("CH", 56.5, 10.25, "R15", "Chimney (hood) point over the hob: its duct and fan go out through the high vent W83 in the east outer wall"),
    ("HA", 50.8, 12.3, "R15", "Interlinked heat alarm, 5 ft from the hob (no smoke alarm in a kitchen)"),
    ("SND", 44.9, 14.4, "R15", "Sounder for the pull-cord alarms in the master and den baths, 7 ft up on the west wall"),
    ("S", 45.6, 15.2, "R15", "Switchboard by the sliding door D17 (kitchen face)"),
    ("S", 44.95, 8.35, "R15", "Switchboard by the utility door D12"),
    ("PC", 47.9, 4.45, "R15", "Counter socket, 3 ft 3 in+ from the sink"),
    ("PC", 48.7, 4.45, "R15", "Counter socket, 2 ft 6 in from the sink"),
    ("PC", 56.9, 7.6, "R15", "Counter socket south of the hob (mixer, grinder)"),
    ("PC", 56.9, 8.7, "R15", "Counter socket south of the hob (kettle, toaster)"),
    ("P16", 56.9, 14.0, "R15", "Refrigerator socket, 16 A, own MCB"),
    ("P16", 53.2, 15.0, "R15", "RO purifier and OTG socket on the crockery counter"),
    # ---- family room: living end R16, console nook R16N, oonjal link R16S, dining end R16D ----
    ("L", 37.5, 38.0, "R16", "Living ceiling light, 2700 K, dimmable"),
    ("L", 45.5, 40.0, "R16", "Living ceiling light, 2700 K, dimmable"),
    ("F", 41.5, 39.5, "R16", "Ceiling fan over the sitting group"),
    ("AC", 41.75, 45.55, "R16", "Family-room AC indoor unit on the north wall between the two diwans, 7 ft 6 in up (cools the L with the folding doors shut)"),
    ("ODU", 41.75, 46.8, "R16", "AC outdoor unit on the north outer wall, the coolest shade, 7 ft up (the family room has no west or south outer wall)"),
    ("LS", 34.15, 36.0, "R16", "Lamp socket by the TV wall, on the door switch"),
    ("LS", 34.15, 43.4, "R16", "Lamp socket by the TV wall, on the door switch"),
    ("LS", 49.2, 45.7, "R16", "Lamp socket by the armchair corner, on the door switch"),
    ("S", 39.3, 33.85, "R16", "Switchboard on the pier between the two folding-door sets"),
    ("TV", 34.1, 39.5, "R16", "TV and data behind the console on the solid west wall, with a concealed HDMI conduit"),
    ("D", 34.15, 40.8, "R16", "Data point (router lead)"),
    ("U", 34.15, 42.6, "R16", "Inverter-circuit socket for the router and set-top box"),
    ("P", 34.15, 36.6, "R16", "6 A socket"),
    ("P", 48.5, 45.7, "R16", "6 A socket by the north window"),
    ("L", 54.0, 36.8, "R16N", "Light over the oonjal nook"),
    ("S", 56.6, 39.0, "R16N", "Switchboard in the nook (east wall)"),
    ("P", 56.8, 34.6, "R16N", "6 A socket"),
    ("L", 47.6, 29.0, "R16S", "Oonjal link light"),
    ("S", 44.9, 30.0, "R16S", "Switchboard on the pier between the folding-door sets"),
    ("P", 50.5, 26.2, "R16S", "6 A socket on the foyer screen wall"),
    ("L", 53.8, 20.0, "R16D", "Light over the dining table"),
    ("L", 47.5, 22.0, "R16D", "Dining-end ceiling light"),
    ("F", 49.5, 19.5, "R16D", "Ceiling fan at the dining end"),
    ("WL", 51.75, 24.5, "R16D", "Mirror light over the hand-wash basin"),
    ("S", 45.5, 15.8, "R16D", "Switchboard by the sliding door D17 (dining face)"),
    ("S", 44.9, 24.8, "R16D", "Switchboard on the folding-door pier"),
    ("P", 53.5, 24.8, "R16D", "6 A socket"),
    # ---- foyer R18, pooja R11, thinnai R17 ----
    ("L", 53.9, 29.0, "R18", "Foyer ceiling light"),
    ("WL", 52.4, 33.1, "R18", "Picture light over the uruli niche"),
    ("FL", 51.1, 26.7, "R18", "Low 1 ft step light at the 6 in step in the 4 ft opening"),
    ("S", 56.6, 31.5, "R18", "Door switchboard by D01 (north)"),
    ("S", 56.6, 26.6, "R18", "Door switchboard by D01 (south), above the shoe-bench loft"),
    ("L", 53.9, 43.0, "R11", "Pooja ceiling light, warm"),
    ("WL", 56.4, 43.0, "R11", "Mandapam light"),
    ("S", 51.2, 45.0, "R11", "Switchboard by D11"),
    ("P", 53.0, 45.6, "R11", "6 A socket (lamp, bell)"),
    ("L", 59.2, 25.8, "R17", "Thinnai light, wet-rated"),
    ("L", 59.2, 32.4, "R17", "Thinnai light, wet-rated"),
    ("F", 59.5, 29.0, "R17", "Thinnai fan on the rafters, wet-rated"),
    ("GL", 61.0, 24.5, "R17", "Garden light on the thinnai's south end"),
    ("GL", 61.0, 33.5, "R17", "Garden light on the thinnai's north end"),
    ("BELL", 57.1, 26.7, "R17", "Bell push by the main door"),
    ("S", 57.1, 31.5, "R17", "Thinnai switchboard by the main door"),
    ("CAM", 61.6, 33.7, "R17", "CCTV point on the thinnai's north-east pillar, 8 ft up, watching the forecourt"),
    # ---- den R42, its niche R58, walk-in R47, den bath R07 ----
    ("L", 26.0, 37.5, "R42", "Den ceiling light"),
    ("L", 28.5, 43.5, "R42", "Den ceiling light"),
    ("F", 27.5, 40.5, "R42", "Ceiling fan"),
    ("AC", 32.3, 45.55, "R42", "Den AC indoor unit on the north wall, 7 ft 6 in up above the armchair, clear of the sofa-bed"),
    ("ODU", 31.8, 46.8, "R42", "AC outdoor unit on the north outer wall (the den has no west or south outer wall), 7 ft up"),
    ("LS", 22.4, 45.3, "R42", "Lamp socket, on the door switch"),
    ("LS", 33.1, 36.0, "R42", "Lamp socket by the sofa-bed, on the door switch"),
    ("S", 32.3, 33.85, "R42", "Door switchboard by D02 (latch side)"),
    ("S", 26.4, 33.85, "R42", "Switchboard by the walk-in door D47, den side"),
    ("S", 22.4, 44.9, "R42", "Outside the den bath door D07: bath light, fan, geyser with indicator lamp"),
    ("TV", 22.4, 39.9, "R42", "TV and data on the den's west wall (behind the console)"),
    ("U", 22.4, 41.0, "R42", "Inverter-circuit socket for the TV box"),
    ("P", 33.2, 36.8, "R42", "Bedside socket by the sofa-bed"),
    ("P", 25.7, 45.7, "R42", "6 A socket on the north wall"),
    ("SND", 27.5, 33.85, "R42", "Sounder for the pull-cord alarms in the master and den baths, 7 ft up on the south wall"),
    ("L", 18.5, 35.5, "R58", "Niche light"),
    ("WL", 19.2, 38.15, "R58", "Desk task light"),
    ("PC", 20.6, 38.15, "R58", "Desk socket"),
    ("D", 17.5, 38.15, "R58", "Data point at the desk"),
    ("GL", 14.5, 39.0, "SITE", "Engawa light on the den's west wall, over the deck"),
    ("GL", 14.5, 34.7, "SITE", "Engawa light by the garden door D45"),
    ("L", 25.0, 28.5, "R47", "Walk-in wardrobe light"),
    ("S", 26.4, 33.15, "R47", "Switchboard by D47, walk-in side"),
    ("L", 18.5, 43.3, "R07", "Den bath ceiling light (8 ft 6 in ceiling)"),
    ("WL", 15.45, 42.8, "R07", "Mirror light over the basin on the west wall"),
    ("EF", 20.45, 45.6, "R07", "Exhaust fan in W68's upper pane, through the north outer wall"),
    ("G", 21.6, 39.2, "R07", "Geyser on the east wall, 3.1 ft from the shower zone (outside the spray); 16 A, own MCB"),
    ("P", 15.45, 44.5, "R07", "IP-rated shaver socket"),
    ("PA", 16.9, 40.2, "R07", "Pull-cord alarm in the shower, by the fold-down seat (cord to 6 in above the floor); sounds in the kitchen and the den"),
    ("PA", 21.5, 45.0, "R07", "Pull-cord alarm by the WC, cord to 6 in above the floor; sounds in the kitchen and the den"),
    # ---- stair (R06), foot lobby (R09), DB and linen (R48), low store (R46) ----
    ("WL", 15.45, 27.0, "R06", "Stair wall light on the west wall, 6 ft 6 in"),
    ("FL", 15.45, 25.0, "R06", "Low 1 ft motion stair light, west wall, flight 1"),
    ("FL", 15.45, 28.4, "R06", "Low 1 ft motion stair light, west wall, flight 1"),
    ("FL", 18.85, 25.4, "R06", "Low 1 ft motion stair light, core wall face, flight 1"),
    ("FL", 18.85, 28.2, "R06", "Low 1 ft motion stair light, core wall face, flight 1"),
    ("L", 21.5, 22.1, "R09", "Stair lobby ceiling light"),
    ("L", 17.5, 21.5, "R09", "Stair lobby ceiling light"),
    ("SA", 17.2, 22.6, "R09", "Interlinked smoke alarm at the stair foot (mains + battery), with the one at the stair head"),
    ("S", 15.45, 21.0, "R09", "Stair switchboard at the foot, 2-way with the stair head"),
    ("S", 27.1, 20.5, "R09", "Switchboard by the sliding door D09"),
    ("WL", 15.45, 22.5, "R09", "Wall light by the window W88"),
    ("L", 21.0, 26.5, "R48", "Cupboard light"),
    ("S", 22.65, 24.4, "R48", "Switchboard by D48, inside"),
    ("DB", 22.75, 25.6, "R48", "Main distribution board in a lockable teak cabinet on the cupboard's east wall, 25 % spare ways, central and dry"),
    ("U", 22.75, 27.4, "R48", "Inverter-circuit socket for the router and ONT"),
    ("D", 22.75, 28.0, "R48", "Data hub (Cat6 home runs)"),
    ("L", 19.0, 31.6, "R46", "Store bulkhead light"),
    ("S", 22.5, 30.2, "R46", "Switch by the hatch D46, inside"),
    # ---- walkways and courtyard ----
    ("L", 30.0, 18.2, "R51", "Walkway light"),
    ("L", 36.0, 18.2, "R51", "Walkway light"),
    ("L", 41.5, 18.2, "R51", "Walkway light"),
    ("S", 29.0, 16.85, "R51", "Walkway switchboard by the master bedroom door D04"),
    ("S", 38.2, 16.85, "R51", "Outside the powder room door D08 (east of the sliding leaf's park): light and fan"),
    ("L", 29.2, 25.0, "R62", "West walkway light"),
    ("S", 27.9, 20.4, "R62", "Walkway switchboard south of D09"),
    ("L", 30.0, 31.8, "R61", "North walkway light"),
    ("L", 36.0, 31.8, "R61", "North walkway light"),
    ("L", 42.0, 31.8, "R61", "North walkway light"),
    ("S", 32.5, 33.1, "R61", "Walkway switchboard by the den door D02"),
    ("S", 39.3, 33.1, "R61", "Walkway switchboard on the folding-door pier"),
    ("L", 42.75, 22.5, "R63", "East walkway light"),
    ("L", 42.75, 27.5, "R63", "East walkway light"),
    ("S", 44.1, 25.0, "R63", "Walkway switchboard on the folding-door pier"),
    ("GL", 33.2, 21.6, "R50", "Courtyard uplight on the tulsi bed, low and shielded"),
    ("GL", 38.8, 28.4, "R50", "Courtyard uplight on the tulsi bed, low and shielded"),
    # ---- site ----
    ("GL", 60.7, 17.9, "SITE", "Pocket garden uplight outside the dining window W63"),
    ("GL", 64.3, 27.0, "SITE", "Entrance steps light (bollard) on the door axis"),
    ("GL", 70.0, 30.4, "SITE", "Forecourt light at the tulsi thara"),
    ("GL", 76.0, 33.0, "SITE", "Forecourt path light"),
    ("GL", 93.0, 39.0, "SITE", "Car-porch light"),
    ("GL", 128.8, 36.0, "SITE", "Gate light"),
    ("MTR", 129.4, 32.0, "SITE", "Meter at the gate, on the road wall"),
    ("BELL", 129.4, 34.0, "SITE", "Gate bell push and intercom"),
    ("CAM", 128.6, 35.0, "SITE", "CCTV point at the gate"),
    ("EP", 3.0, 24.0, "SITE", "Earth pit 1 (back garden, west of the rain lane)"),
    ("EP", 3.0, 28.0, "SITE", "Earth pit 2, 3 m from pit 1"),
    ("P16", 66.7, 46.4, "SITE", "Sump pump control and socket (float switch, dry-run cut-out), weatherproof"),
    ("P16", 101.0, 13.2, "SITE", "Workshop feeder (its own sub-meter), weatherproof"),
    ("P16", 123.0, 13.0, "SITE", "Shops' feeder (separate meters)"),
]
ELECTRICAL_F1 = [  # first-floor points (Task C6)
    # ---- Bedroom 2 R31, its walk-in R45 and bath R33 ----
    ("L", 21.25, 12.3, "R31", "Bedroom ceiling light on a dimmer, over the foot of the bed"),
    ("F", 21.25, 8.6, "R31", "Ceiling fan over the bed, hook cast in the slab"),
    ("WL", 17.75, 4.45, "R31", "Bedside reading light (west)"),
    ("WL", 24.85, 4.45, "R31", "Bedside reading light (east)"),
    ("S", 17.3, 4.45, "R31", "Bedside switchboard (west), 2-way with the door"),
    ("S", 24.4, 4.45, "R31", "Bedside switchboard (east), 2-way with the door"),
    ("S", 25.6, 13.7, "R31", "Door switchboard by D51 (latch side)"),
    ("P", 18.15, 4.45, "R31", "Bedside charging socket (west)"),
    ("P", 25.2, 4.45, "R31", "Bedside charging socket (east)"),
    ("LS", 15.45, 9.5, "R31", "Lamp socket on the door switch"),
    ("LS", 27.1, 9.75, "R31", "Lamp socket between the east windows, on the door switch"),
    ("AC", 15.45, 11.8, "R31", "Bedroom 2 AC indoor unit on the west wall, 7 ft 6 in up, throwing east along the bed foot"),
    ("ODU", 14.2, 7.0, "R31", "AC outdoor unit on the west outer wall under a louvred sun-hood with 1 m clear in front of it, clear of the master's unit below"),
    ("SA", 23.5, 12.3, "R31", "Interlinked smoke alarm in Bedroom 2 (mains + battery), with the stair alarms"),
    ("L", 24.2, 17.1, "R45", "Walk-in ceiling light"),
    ("S", 22.55, 19.95, "R45", "Walk-in switchboard by D31, west of the sliding leaf"),
    ("S", 22.5, 14.3, "R45", "Outside the bath door D33 (walk-in side, south of the sliding leaf): bath light, fan, geyser with indicator lamp"),
    ("L", 18.5, 16.0, "R33", "Bath ceiling light (8 ft 6 in ceiling)"),
    ("WL", 15.45, 15.8, "R33", "Mirror light over the basin on the west wall"),
    ("EF", 15.4, 19.5, "R33", "Exhaust fan in W41's upper pane: straight through the west outer wall"),
    ("G", 21.0, 14.3, "R33", "Geyser on the south wall, 2.7 ft from the shower zone (outside the spray); 16 A, own MCB"),
    ("P", 15.45, 14.5, "R33", "IP-rated shaver socket"),
    # ---- stair head R41, gallery R34 ----
    ("L", 19.0, 22.1, "R41", "Stair-head ceiling light"),
    ("L", 24.5, 22.2, "R41", "Stair-head ceiling light"),
    ("SA", 21.0, 22.1, "R41", "Interlinked smoke alarm at the stair head (mains + battery), with the one at the foot"),
    ("S", 15.45, 21.0, "R41", "Stair switchboard at the head, 2-way with the foot"),
    ("S", 25.6, 20.55, "R41", "Switchboard for the suite door D31 (stair-head face, east of the sliding leaf's park)"),
    ("WL", 15.45, 22.6, "R41", "Wall light by the window W35"),
    ("FL", 15.45, 23.3, "R41", "Low 1 ft motion light at the head of the stair"),
    ("L", 25.3, 29.0, "R34", "Gallery ceiling light"),
    ("FL", 23.4, 26.0, "R34", "Low 1 ft motion light along the well guard"),
    ("FL", 23.4, 30.5, "R34", "Low 1 ft motion light along the well guard"),
    ("S", 27.0, 33.1, "R34", "Switchboard by D36, gallery side"),
    ("DB", 27.1, 24.8, "R34", "First-floor sub-board in a lockable teak cabinet on the gallery's east wall, 4 ft up, fed from the main DB in R48"),
    ("WL", 27.1, 31.5, "R34", "Wall light by the jharokha opening"),
    # ---- upstairs family room R36 / desk nook R36A, upper toilet R39 ----
    ("L", 27.0, 40.0, "R36", "Family-room ceiling light, dimmable"),
    ("L", 28.0, 44.0, "R36", "Family-room ceiling light, dimmable, over the bookshelf wall"),
    ("F", 27.5, 41.5, "R36", "Ceiling fan"),
    ("AC", 31.7, 45.55, "R36", "Family-room AC indoor unit on the north wall, 7 ft 6 in up, clear of the sofa-bed's head (the bed head is to the south)"),
    ("ODU", 29.6, 46.8, "R36", "AC outdoor unit on the north outer wall, 7 ft above the first floor, offset from the den's unit below"),
    ("LS", 22.35, 43.0, "R36", "Lamp socket by the reading armchair, on the door switch"),
    ("LS", 33.1, 38.4, "R36", "Lamp socket by the sofa-bed, on the door switch"),
    ("S", 27.0, 33.9, "R36", "Door switchboard by D36"),
    ("S", 33.1, 33.9, "R36", "Switchboard by the terrace door D49"),
    ("TV", 22.4, 41.5, "R36", "Screen and data behind the console on the west wall, with a concealed HDMI conduit"),
    ("D", 22.4, 40.0, "R36", "Data point (projector, streaming box)"),
    ("U", 22.4, 42.7, "R36", "Inverter-circuit socket for the screen box"),
    ("P", 22.4, 38.9, "R36", "6 A socket"),
    ("P", 30.6, 45.7, "R36", "6 A socket on the north wall"),
    ("L", 18.5, 35.8, "R36A", "Desk-nook ceiling light"),
    ("WL", 16.4, 38.05, "R36A", "Desk task light"),
    ("S", 21.8, 37.9, "R36A", "Outside the upper toilet door D39: toilet light, fan, geyser with indicator lamp"),
    ("PC", 15.45, 36.0, "R36A", "Desk socket"),
    ("D", 15.45, 34.6, "R36A", "Data point at the desk"),
    ("L", 18.8, 43.0, "R39", "Upper-toilet ceiling light (8 ft 6 in ceiling)"),
    ("WL", 20.15, 45.55, "R39", "Mirror light over the basin on the north wall"),
    ("EF", 16.8, 45.7, "R39", "Exhaust fan in W42's upper pane, through the north outer wall"),
    ("G", 21.6, 39.2, "R39", "Geyser on the east wall, 3.2 ft from the shower zone (outside the spray); 16 A, own MCB"),
    ("P", 15.45, 42.6, "R39", "IP-rated shaver socket"),
    # ---- roof terrace R37 ----
    ("L", 37.5, 38.5, "R37", "Terrace light, wet-rated, on the canopy steelwork"),
    ("L", 44.0, 40.5, "R37", "Terrace light, wet-rated"),
    ("L", 47.5, 44.6, "R37", "Terrace light, wet-rated, over the daybed"),
    ("F", 42.8, 37.65, "R37", "Terrace fan, wet-rated, hung from the canopy's steel beam over the swing"),
    ("S", 33.9, 34.0, "R37", "Terrace switchboard by D49, IP55"),
    ("P16", 33.9, 41.0, "R37", "Washing machine socket, IP55, own MCB"),
    ("P", 40.0, 45.6, "R37", "IP55 socket"),
]

# Plumbing points: code, x, y, room, note
PLUMB_TYPES = {
    "WC": "Wall-hung WC, concealed cistern", "HF": "Health faucet", "BS": "Wash basin", "SH": "Shower mixer (hot + cold)",
    "FT": "Floor trap / linear drain", "SK": "Sink", "WM": "Washing-machine inlet + drain", "RO": "RO purifier point",
    "TAP": "Tap", "GY": "Geyser connection", "IC": "Inspection chamber", "GT": "Grease trap", "DP": "Rain downpipe",
    "CD": "Courtyard drain with first-flush filter to the sump",
    "OF": "Courtyard overflow standpipe, 3 in above the court floor", "SC": "Scupper through the walkway kerb (last-resort court overflow)",
    "PU": "Sump pump", "TK": "Overhead water tank on its shaded steel platform",
}
PLUMBING = [  # ground-floor plumbing points (Task C6). IC notes read "IC-n <kind>: ..." (soil, grey, kitchen, effluent) or "RIC-n" (rain)
    # ---- master bath R40, powder room R08, utility R13, kitchen R15, dining R16D ----
    ("WC", 29.3, 15.2, "R40", "Master WC (wall-hung), soil straight south: one unjointed 110 mm length of 11.6 ft under the slab (no joints under the slab) to IC-7 outside the south wall, 1:40 fall"),
    ("HF", 30.6, 15.6, "R40", "Health faucet beside the WC"),
    ("IC", 29.3, 13.6, "R40", "RE-A rodding eye at the master WC head: a flush stainless cover in the floor on the soil line, 1.6 ft south of the pan"),
    ("BS", 33.5, 12.35, "R40", "Wash basin on the east wall, opposite the door"),
    ("SH", 31.6, 4.45, "R40", "Shower mixer (hot + cold) on the south wall at the shower's east end, spraying west"),
    ("FT", 29.9, 4.7, "R40", "Linear shower drain along the south wall, 1:60 fall to it"),
    ("GY", 34.1, 9.2, "R40", "Geyser hot and cold connections (supply from the north-wall chase)"),
    ("WC", 38.4, 11.95, "R08", "Powder WC on the east wall, soil south under the utility: 8.3 ft inside the house, one unjointed length (no joints under the slab), to IC-8"),
    ("HF", 38.6, 13.0, "R08", "Health faucet beside the WC"),
    ("IC", 38.4, 10.5, "R08", "RE-B rodding eye at the powder WC head: a flush stainless cover in the floor on the soil line, 1.5 ft south of the pan"),
    ("BS", 36.2, 10.6, "R08", "Wash basin on the south wall, opposite the door"),
    ("WC", 20.45, 44.7, "R07", "Den bath WC on the north wall: soil straight out through the wall (1.7 ft inside the house) to IC-1; the upper toilet's stack joins behind it in the same pre-wall chase"),
    ("HF", 19.3, 45.0, "R07", "Health faucet beside the WC"),
    ("IC", 20.45, 45.9, "R07", "RE-C rodding eye at the den bath WC head, in the pre-wall chase on the soil line"),
    ("BS", 16.1, 42.8, "R07", "Wash basin on the west wall, opposite the door"),
    ("SH", 15.45, 41.0, "R07", "Shower mixer on the west wall north of the seat"),
    ("FT", 16.9, 39.2, "R07", "Shower floor trap beside the seat"),
    ("GY", 21.6, 39.6, "R07", "Geyser hot and cold connections"),
    ("SK", 35.3, 5.3, "R13", "Utility sink (vessel washing): through the grease trap to the banana circle"),
    ("WM", 39.1, 5.3, "R13", "Washing machine inlet and standpipe: soapy water to the soak pit"),
    ("FT", 39.5, 7.5, "R13", "Utility floor trap (the floor falls to it)"),
    ("TAP", 34.9, 8.2, "R13", "Utility tap on the west wall"),
    ("SK", 52.1, 5.4, "R15", "Prep sink under W82: through the grease trap to the banana circle"),
    ("RO", 53.2, 14.6, "R15", "RO purifier on the crockery counter"),
    ("IC", 52.1, 15.8, "R16D", "RE-D flush rodding eye on the dining-basin grey line at the kitchen / dining wall, in the dining floor 0.3 ft off the wall"),
    ("BS", 51.75, 24.5, "R16D", "Hand-wash basin on the dining end's north wall: its waste runs south under the dining end and the kitchen to the kitchen grey line"),
    # ---- courtyard, its second drain, overflow and scupper ----
    ("CD", 39.5, 21.5, "R50", "Courtyard drain CD (south-east corner): 150 mm grating, first-flush filter at FF; the court floor falls to it and to CD-2"),
    ("CD", 32.5, 28.5, "R50", "Second courtyard drain CD-2 at the north-west corner, diagonal to CD, on its OWN overflow line (west under the den walk-in and the stair to the west rain lane), so a choked CD trunk never floods the court"),
    ("OF", 33.4, 29.3, "R50", "Overflow standpipe 3 in above the court floor (below the walkway level) beside CD-2, on the same independent line: it takes over when both gratings choke"),
    ("IC", 24.0, 28.5, "R47", "RE-3 rodding eye on the courtyard overflow line, under the den walk-in floor, flush cover"),
    ("SC", 30.95, 27.2, "R62", "Scupper through the west walkway kerb, 5.5 in above the court floor (0.5 in above the walkway floor, above the standpipe): the last resort spills across the walkway to its gully"),
    ("IC", 30.4, 28.5, "R62", "RE-2 rodding eye at the court wall on the overflow line, flush cover in the walkway"),
    ("FT", 29.2, 27.2, "R62", "Walkway gully taking the scupper's spill into the overflow line (not the CD trunk)"),
    ("IC", 39.5, 31.5, "R61", "RE-1 rodding eye in the north walkway on the court trunk: sleeved and concrete-encased under the floor, one unjointed length through the north wall"),
    # ---- site: soil chambers (IC-1 to IC-12 are on the soil line) ----
    ("IC", 20.45, 47.0, "SITE", "IC-1 soil: the den bath and upper-toilet stub leaves the north wall"),
    ("IC", 16.77, 47.0, "SITE", "IC-28 soil: the upper toilet's own stack leaves the north wall and joins the lane"),
    ("IC", 11.0, 47.0, "SITE", "IC-2 soil: bend, west of the engawa deck"),
    ("IC", 11.0, 31.0, "SITE", "IC-3 soil: bend south of the deck"),
    ("IC", 13.6, 31.0, "SITE", "IC-4 soil: bend onto the west lane"),
    ("IC", 13.6, 18.3, "SITE", "IC-5 soil: Bedroom 2's boxed duct joins the lane"),
    ("IC", 13.6, 2.0, "SITE", "IC-6 soil: south-west corner, bend onto the south lane"),
    ("IC", 29.3, 2.0, "SITE", "IC-7 soil: master WC branch joins"),
    ("IC", 38.4, 2.0, "SITE", "IC-8 soil: powder WC branch joins"),
    ("IC", 49.5, 2.0, "SITE", "IC-9 soil: straight run, 2.6 ft west of the grease trap and 8 ft from the LPG cage (every chamber on the south strip is at least 2 ft from the next)"),
    ("IC", 67.0, 2.0, "SITE", "IC-10 soil: straight run; the closed pipes of this strip pass 0.5 to 0.9 m from the LPG cage (sleeved); 9.5 ft from the cage"),
    ("IC", 74.4, 2.0, "SITE", "IC-11 soil: bend north, 2.0 ft from the soak pit's edge"),
    ("IC", 74.4, 18.6, "SITE", "IC-12 soil: bend east to the septic inlet"),
    # bath grey (to the soak pit)
    ("IC", 7.6, 47.7, "SITE", "IC-13 grey: start of the west grey lane (terrace laundry)"),
    ("IC", 7.6, 42.8, "SITE", "IC-14 grey: den bath and upper-toilet branch joins, under the deck's west end"),
    ("IC", 7.6, 19.85, "SITE", "IC-15 grey: Bedroom 2 bath shower branch joins"),
    ("IC", 7.6, 15.8, "SITE", "IC-16 grey: Bedroom 2 bath basin branch joins"),
    ("IC", 7.6, 2.8, "SITE", "IC-17 grey: south-west corner"),
    ("IC", 31.5, 2.8, "SITE", "IC-18 grey: master bath branch joins; the y 2.8 grey run is concrete-encased past the footings (the structural engineer approves the trench-to-footing distance on this 3.6 ft strip)"),
    ("IC", 36.2, 2.8, "SITE", "IC-19 grey: powder room and utility branch joins"),
    ("IC", 70.0, 2.8, "SITE", "IC-20 grey: straight run to the soak pit"),
    # kitchen grey (to the banana circle)
    ("IC", 34.9, 1.2, "SITE", "IC-21 kitchen: utility sink line turns east"),
    ("IC", 46.5, 1.2, "SITE", "IC-22 kitchen: straight run to the grease trap, east of the utility's service steps (its cover clear of them)"),
    ("GT", 52.1, 1.2, "SITE", "Grease trap on the kitchen grey line, below the prep sink, with no other chamber within 2 ft: it takes the utility sink, the prep sink and the dining basin; 6.5 ft from the LPG cage"),
    ("IC", 63.0, 1.2, "SITE", "IC-23 kitchen: straight run (5.5 ft from the LPG cage)"),
    ("IC", 72.5, 1.2, "SITE", "IC-24 kitchen: before the soak pit, line sleeved past it"),
    # septic effluent (to the soak pit)
    ("IC", 90.0, 18.6, "SITE", "IC-25 effluent: bend east of the septic outlet"),
    ("IC", 90.0, 13.4, "SITE", "IC-26 effluent: bend west"),
    ("IC", 78.0, 13.4, "SITE", "IC-27 effluent: bend south to the soak pit"),
    # rain chambers
    ("IC", 5.6, 3.3, "SITE", "RIC-2 rain: south-west corner of the west rain lane"),
    ("IC", 5.6, 48.6, "SITE", "RIC-3 rain: north-west corner, start of the north trunk"),
    ("IC", 64.5, 3.3, "SITE", "RIC-4 rain: south end of the east trunk (5.8 ft from the LPG cage; it cannot move to the herb-bed edge without coming within 1.5 m of the cage): inside the herb bed, with a flush cover on a stepping stone"),
    ("IC", 64.5, 15.5, "SITE", "RIC-5 rain: east gutter branch joins"),
    ("IC", 64.5, 25.5, "SITE", "RIC-6 rain: south rain-chain branch joins"),
    ("IC", 64.5, 34.1, "SITE", "RIC-7 rain: north rain-chain branch joins"),
    ("IC", 12.2, 28.5, "SITE", "RIC-11 rain: the courtyard overflow line leaves the house (3.6 ft unjointed lengths between its rodding eyes)"),
    ("IC", 5.6, 28.5, "SITE", "RIC-12 rain: the overflow line joins the west rain lane"),
    ("IC", 39.5, 48.6, "SITE", "RIC-8 rain: the court trunk joins the north trunk"),
    ("IC", 64.5, 45.2, "SITE", "FF first-flush filter chamber: every rain line passes it before the sump; the first 1 mm of each storm is diverted to the dry well"),
    ("IC", 92.0, 44.6, "SITE", "RIC-9 rain: sump overflow bend"),
    ("IC", 92.0, 14.5, "SITE", "RIC-10 rain: sump overflow bend east to the recharge pit (outside the workshop verandah)"),
    ("IC", 109.75, 14.5, "SITE", "RE-4 rodding eye at the recharge pit, between the verandah (x 109) and the pit (x 110.5): no chamber under the verandah's pavers"),
    # roof downpipes (the roof's own list in ROOF; C8 may adjust them) and rain chains
    ("DP", 14.3, 3.3, "SITE", "Downpipe, south-west corner, 100 mm"),
    ("DP", 49.0, 3.3, "SITE", "Downpipe, south side, 1.2 ft clear of the kitchen window W82"),
    ("DP", 57.7, 15.5, "SITE", "Downpipe, east side south of the dining window (7.7 ft from the LPG cage)"),
    ("DP", 57.7, 46.7, "SITE", "Downpipe, north-east corner"),
    ("DP", 33.2, 46.7, "SITE", "Downpipe, north side where the wing meets the terrace, 0.3 ft west of the terrace chajja's edge (clear of it): takes the wing's north eave gutter and, on a swan-neck, its east gutter over the terrace"),
    ("DP", 14.3, 46.7, "SITE", "Downpipe, north-west corner"),
    ("DP", 49.5, 46.7, "SITE", "Terrace downpipe on the north wall below the jali parapet (the terrace outlet's: a side-entry outlet through the parapet foot into a rainwater head), through the 2 ft chajja in a sleeve"),
    ("DP", 62.75, 25.5, "SITE", "Thinnai rain chain (south corner) into its pebble basin, which overflows to the rain line"),
    ("DP", 62.75, 34.1, "SITE", "Thinnai rain chain (north corner) into its pebble basin, which overflows to the rain line"),
    # taps
    ("TAP", 10.0, 20.0, "SITE", "Back-garden tap on the herb beds"),
    ("TAP", 58.3, 13.4, "SITE", "Rinse-shower tap on the kitchen's east wall, 5.1 ft from the LPG cage; the platform drains to a gravel soakaway where it stands"),
    ("TAP", 65.8, 32.8, "SITE", "Foot-wash tap by the steps, draining to a gravel soakaway under its stone"),
    ("TAP", 66.0, 12.0, "SITE", "Herb-bed tap"),
    ("PU", 66.6, 47.2, "SITE", "Sump pump (submersible, float and dry-run cut-out) lifting to the overhead tank on the terrace"),
]
PLUMBING_F1 = [  # first-floor plumbing points (Task C6)
    ("WC", 16.25, 18.3, "R33", "Bedroom 2 WC on the west outer wall: soil straight out through the wall into a boxed duct outside, down to IC-5"),
    ("HF", 17.4, 19.4, "R33", "Health faucet beside the WC"),
    ("IC", 15.6, 18.3, "R33", "RE-F rodding eye at the WC head (flush cover in the sunk slab, on the soil line behind the pan)"),
    ("BS", 16.1, 15.8, "R33", "Wash basin on the west wall: waste out through the wall to a boxed grey duct"),
    ("SH", 20.9, 19.95, "R33", "Shower mixer on the north wall"),
    ("FT", 20.6, 18.5, "R33", "Shower floor trap (sunk slab): waste along the slab build-up to the west wall and down a second boxed duct"),
    ("GY", 21.0, 14.4, "R33", "Geyser hot and cold connections"),
    ("WC", 16.77, 44.7, "R39", "Upper-toilet WC, stacked over the den bath R07: its own 110 mm stack runs straight down a boxed chase in R07's north-west corner (no horizontal run in the sunk slab) and out through the north wall to IC-28; a rodding eye RE-E at its foot"),
    ("HF", 17.6, 45.2, "R39", "Health faucet beside the WC"),
    ("IC", 16.77, 45.8, "R39", "RE-E rodding eye at the stack foot behind the WC (access panel in the R07 corner chase)"),
    ("BS", 20.15, 44.9, "R39", "Wash basin on the north wall: waste down the wet-wall chase behind the den bath's WC (grey, 75 mm)"),
    ("SH", 17.0, 38.65, "R39", "Shower mixer on the south wall"),
    ("FT", 16.9, 40.6, "R39", "Shower floor trap over the den bath's: waste down the boxed corner chase to the den bath's grey line"),
    ("GY", 21.6, 38.6, "R39", "Geyser hot and cold connections"),
    ("WM", 34.9, 42.4, "R37", "Terrace washing machine inlet and standpipe: drains down a boxed duct on the north wall to the west grey lane, never into the terrace outlet"),
    ("SK", 36.9, 42.4, "R37", "Laundry sink beside the washer"),
    ("FT", 49.5, 45.75, "R37", "Terrace outlet, side-entry through the foot of the north parapet: the slab falls to it; it feeds the terrace downpipe and the rain line"),
    ("TAP", 45.5, 45.5, "R37", "Terrace hose tap"),
    ("TK", 35.25, 44.49, "R37", "Overhead tank 1 of 2 (500 L each, 2 ft 8 in across, on 2'-9\" centres so the two stand 1 in apart, interconnected: 1,000 L in all) on a 3 ft galvanised steel stand along the north parapet at the terrace's north-west corner: the square stand stands inside the west wall's and the parapet's faces, 1 in+ clear of the washer and the sink and clear of the canopy post at the corner, bolted to the slab over the beams, under the canopy's shade and behind the jali parapet (not in a roof void); filled by the pump through the riser duct on the north wall; overflow and washout run to the terrace outlet; a pressure pump takes the showers"),
    ("TK", 38.0, 44.49, "R37", "Overhead tank 2 of 2 (500 L), interconnected with tank 1 at its foot, on the same steel stand: the stand leaves the drying-rail corner clear below 6 ft, and both tanks stand 1 in or more clear of the washer and the sink in plan"),
]
# Pipe runs (schematic; plan positions, depths in the drawings). West strip (the back garden): rain x 5.6, grey x 7.6, soil x 13.6 (x 11.0 beside the engawa deck, y 31-47);
# south strip (3.6 ft between the wall and the boundary): kitchen grey y 1.2, soil y 2.0, bath grey y 2.8, then soil north up x 74.4 and east along y 18.6 to the septic;
# north strip: soil y 47.0 (den bath and upper toilet only), grey y 47.7, supply y 47.2 (east of x 35), rain trunk y 48.6; the rain lines meet at the first-flush chamber
# (64.5, 45.2) before the sump, and the sump's overflow goes south down x 92.0 and east along y 14.5 to the recharge pit. Septic effluent leaves the east face and runs round to the soak pit.
PIPES = [  # ground-floor pipe runs (Task C6): (kind, [(x, y), ...]); kinds soil, grey, rain, supply
    # soil (110 mm uPVC) to the septic inlet (83, 18.6): west lane x 13.6, south lane y 2.0, east lane x 74.4, then y 18.6
    ("soil", [(20.45, 44.7), (20.45, 47.0), (11.0, 47.0), (11.0, 31.0), (13.6, 31.0), (13.6, 18.3)]),
    ("soil", [(16.77, 44.7), (16.77, 47.0)]),
    ("soil", [(16.25, 18.3), (14.2, 18.3), (13.6, 18.3), (13.6, 2.0), (74.4, 2.0), (74.4, 18.6), (83.0, 18.6)]),
    ("soil", [(29.3, 15.2), (29.3, 2.0)]),
    ("soil", [(38.4, 11.95), (38.4, 2.0)]),
    # bath grey (75 mm) to the soak pit (west face 76.4, 2.8): west lane x 7.6, south lane y 2.8
    ("grey", [(7.6, 47.7), (7.6, 2.8), (76.4, 2.8)]),
    ("grey", [(36.9, 42.4), (34.9, 42.4), (34.9, 47.7), (7.6, 47.7)]),
    ("grey", [(16.9, 39.2), (16.9, 42.8), (7.6, 42.8)]),
    ("grey", [(20.9, 45.4), (20.9, 42.8), (16.9, 42.8)]),
    ("grey", [(16.1, 15.8), (14.2, 15.8), (7.6, 15.8)]),
    ("grey", [(20.6, 18.5), (20.6, 19.85), (14.2, 19.85), (7.6, 19.85)]),
    ("grey", [(29.9, 4.7), (31.5, 4.7), (31.5, 2.8)]),
    ("grey", [(33.5, 12.35), (33.5, 4.7), (31.5, 4.7)]),
    ("grey", [(36.2, 10.6), (36.2, 2.8)]),
    ("grey", [(39.1, 5.3), (39.1, 6.4), (36.2, 6.4)]),
    ("grey", [(39.5, 7.5), (39.1, 7.5), (39.1, 6.4)]),   # the washer's waste joins the sink's branch east of the powder soil: one crossing, not two
    # kitchen grey (75 mm) through the grease trap (52.1, 1.2) to the banana circle (86.5, 1.2)
    ("grey", [(35.3, 5.3), (35.3, 4.5), (34.9, 4.5), (34.9, 1.2), (52.1, 1.2)]),
    ("grey", [(51.75, 24.5), (52.1, 24.5), (52.1, 1.2)]),
    ("grey", [(52.1, 1.2), (86.5, 1.2)]),
    # septic effluent (opposite the inlet) to the soak pit top (78, 5.6)
    ("grey", [(89.0, 18.6), (90.0, 18.6), (90.0, 13.4), (78.0, 13.4), (78.0, 5.6)]),
    # rain (110 mm) to the first-flush chamber FF (64.5, 45.2), then the sump (66, 45.2); overflow to the recharge pit
    ("rain", [(14.3, 3.3), (5.6, 3.3), (5.6, 48.6)]),
    ("rain", [(5.6, 48.6), (39.5, 48.6)]),
    ("rain", [(39.5, 48.6), (64.5, 48.6), (64.5, 45.2)]),
    ("rain", [(14.3, 46.7), (14.3, 48.6)]),
    ("rain", [(33.2, 46.7), (33.2, 48.6)]),
    ("rain", [(49.5, 45.75), (49.5, 48.6)]),
    ("rain", [(57.7, 46.7), (57.7, 48.6)]),
    ("rain", [(39.5, 21.5), (39.5, 48.6)]),
    ("rain", [(33.4, 28.5), (5.6, 28.5)]),   # the courtyard overflow line: CD-2, the standpipe and the walkway gully, on their own run west to the west rain lane (no pipe shared with the CD trunk)
    ("rain", [(33.4, 29.3), (33.4, 28.5)]),
    ("rain", [(29.2, 27.2), (29.2, 28.5)]),
    ("rain", [(38.0, 45.75), (49.5, 45.75)]),   # terrace tank overflow and washout (50 mm, over the slab) to the terrace outlet
    ("rain", [(49.0, 3.3), (64.5, 3.3)]),
    ("rain", [(64.5, 3.3), (64.5, 45.2)]),
    ("rain", [(57.7, 15.5), (64.5, 15.5)]),
    ("rain", [(62.75, 25.5), (64.5, 25.5)]),
    ("rain", [(62.75, 34.1), (64.5, 34.1)]),
    ("rain", [(64.5, 45.2), (66.0, 45.2)]),
    ("rain", [(72.0, 44.6), (92.0, 44.6), (92.0, 14.5), (110.5, 14.5)]),
    # supply (CPVC): sump pump to the riser foot under the terrace tank
    ("supply", [(66.0, 47.2), (35.5, 47.2)]),
]
PIPE_MM = {("rain", (39.5, 48.6)): 150, ("rain", (64.5, 45.2)): 150, ("rain", (72.0, 44.6)): 150}   # larger runs, by first point: the north trunk from RIC-8 to FF, FF to the sump, and the sump overflow (150 mm); all other rain runs 110 mm
_CLASS_RANK = {"soil": 0, "effluent": 1, "bath grey": 2, "kitchen grey": 3, "rain": 4, "supply": 5}   # deepest first


def pipe_class(kind, line):
    if kind == "grey":
        return "kitchen grey" if line[0] in ((35.3, 5.3), (51.75, 24.5), (52.1, 1.2)) else ("effluent" if line[0] == (89.0, 18.6) else "bath grey")
    return kind


def _pipe_crossings(pipes):
    """Plan crossings of pipes of different classes: (x, y, lower, upper, note). The deeper class goes below (soil lowest), 150 mm clear."""
    out = []
    segs = [(pipe_class(k, l), a, b) for k, l in pipes for a, b in zip(l, l[1:])]
    for i, (c1, a, b) in enumerate(segs):
        for c2, c, d in segs[i + 1:]:
            if c1 == c2:
                continue
            r = (b[0] - a[0], b[1] - a[1]); q = (d[0] - c[0], d[1] - c[1])
            den = r[0] * q[1] - r[1] * q[0]
            if abs(den) < 1e-9:
                continue
            t = ((c[0] - a[0]) * q[1] - (c[1] - a[1]) * q[0]) / den
            u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
            la, lc = (r[0] ** 2 + r[1] ** 2) ** .5, (q[0] ** 2 + q[1] ** 2) ** .5
            if not (0.06 / la < t < 1 - 0.06 / la and 0.06 / lc < u < 1 - 0.06 / lc):
                continue
            x, y = round(a[0] + t * r[0], 2), round(a[1] + t * r[1], 2)
            lo, up = (c1, c2) if _CLASS_RANK[c1] < _CLASS_RANK[c2] else (c2, c1)
            if not any(abs(x - e[0]) < 0.3 and abs(y - e[1]) < 0.3 and e[2] == lo and e[3] == up for e in out):
                out.append((x, y, lo, up, f"{lo} runs below {up}, at least 150 mm clear; the upper pipe is sleeved across"))
    return out


PIPE_CROSSINGS = _pipe_crossings(PIPES)   # every plan crossing, listed and marked X1.. on P-101: soil is always the lowest pipe

# Construction phasing: roof first, in three stages. Stage 1 is a lived-in ground floor (the ring of rooms and the courtyard) with
# basic finishes under the full roof, with the wing's slab, columns and the terrace slab cast; stage 2 is the upstairs shell and the
# roof terrace; stage 3 fits out the upstairs. Costs are rough 2026 village rates around Guntur for the compact house (its enclosed area
# from geom.floor_areas), scaled from the 54 x 54 ft house's estimate by its floor area: to be re-priced by a quantity surveyor.
PHASES = [
    ("Stage 1: move in", [
        "The whole ground-floor ring with basic finishes: vitrified tiles in place of Athangudi and red oxide, one coat of paint, granite kitchen counter with open shelves, ceilings only in the baths.",
        "The courtyard: sunk slab, both drains, the standpipe and scupper, the first-flush filter and the steel grille at the inner eave (the shade cloth follows later); the walkway pillars; the thinnai platform, pillars, steps and handrails.",
        "Footings, columns, first-floor slab and stair designed and built for the two-storey wing over the west band and the den; RCC frame and ring beam up to roof level.",
        "The full roof: the tiled ring roof, the L-shaped hipped roof over the wing with its gutters and box gutter, the thinnai lean-to, and the terrace slab waterproofed with its outlet (its steel canopy waits for stage 2); temporary railings on its open edges.",
        "Upstairs left as an open, covered deck: temporary railings on the open edges; the stair lobby's sliding door D09 is permanent from stage 1 and locks the stair off, so the ground floor is secure.",
        "Site works: sump, the two water tanks on their stand, septic tank, soak pit, drains, water and power connections; temporary fence."], "Rs 33-38 lakh (rough)"),
    ("Stage 2: ground-floor upgrades, upstairs shell and the roof terrace (1-2 years later)", [
        "Ground-floor upgrades: kitchen cabinets, built-in wardrobes, the foyer's jali screens and shoe bench; Athangudi and red oxide floors; false ceilings in the ring rooms; final paint; the courtyard's shade cloth.",
        "First-floor outer walls of the wing with window frames, grilles and shutters, and the two jharokha bays: a dry, lockable shell.",
        "The roof terrace: its tiled canopy on six steel posts, the railings, the corner guard wall and the teak jali parapet on the north side, the glazed sliding doors to the upstairs family room, then tiles over the waterproofing."], "Rs 10-14 lakh (rough)"),
    ("Stage 3: upstairs fit-out", [
        "Inner walls upstairs: Bedroom 2 with its walk-in and bath, the upper toilet, the gallery's guard over the stair well and the family room's desk nook.",
        "Doors, wet-room waterproofing and fittings, floors, inside plaster and paint, false ceilings.",
        "Wiring and lights from the sub-board, ACs, wardrobes, the bookshelf wall and the family room's sound lining."], "Rs 6-8 lakh (rough)"),
]
PHASE1_PROVISIONS = [
    "Plan approval for the full two-storey house now.",
    "The wing's columns and beams, cast in stage 1: columns under every corner and wall junction of the wing (the stair-well corners, the upper toilet, the upstairs family room), beams under every future upstairs wall (the Bedroom 2 suite walls, the stair-head wall, the gallery's end and the family room's south and east walls) and edge beams round the roof terrace slab, so no upstairs wall stands on an open span. Structural engineer to confirm sizes (seismic zone III).",
    "Sleeves for the WC soil pipes, floor traps and shower drains of Bedroom 2's bath (R33) and the upper toilet (R39), cast into the slab; Bedroom 2's WC straight out through the west wall into its boxed duct, the upper toilet's own stack down the den bath's corner chase; vent stacks run to roof level and capped.",
    "The sunk slab under Bedroom 2's bath R33 (over the master's wardrobe end) and under the upper toilet R39 (over the den bath) cast sunk 4 in (shallow traps, the WCs wall-hung), waterproofed in stage 1 with upturns and bonded collars at every pipe, flood-tested for 48 h, and given a temporary outlet through a sleeve so they never pond while the upstairs is an open deck; the ceilings below step down 4 in under them as bulkheads, with access panels.",
    "The terrace slab waterproofed in stage 1 (over the family living), with a drip edge all round, the outlet through the north parapet's foot to its downpipe and a 48 h flood test, so the family living stays dry while the canopy and tiles wait for stage 2; settle the step at its door first (see Open_Issues).",
    "Conduits for first-floor lights and fans cast into the slab; conduit from the main DB under flight 2 to the first-floor sub-board position on the gallery's east wall.",
    "Water supply branches to the upper bath and toilet, capped; the two 500 L tanks on their final stand at the terrace's north-west corner.",
    "Columns, ring beam and lintel band set so the stage-2 outer walls and windows drop in; AC sleeves marked; the jharokha bracket frames' fixings cast into the wing's east wall and the family room's south wall.",
    "Kitchen and wardrobe walls finished with the plumbing, sockets and hold-fasts for the stage-2 cabinets already in.",
]
PHASE1_LIVING = [
    "Upstairs is a shaded, covered deck behind the locked stair lobby door: storage, drying clothes, a sit-out (no water use until stage 3). The roof terrace over the family living is a bare waterproofed slab with railings until its canopy comes in stage 2.",
    "The ground floor stays cool from day one: it has the roof's shade and attic over it, not a bare slab, the courtyard draws hot air out, and the walkway shades the walls.",
    "Stages 2 and 3 are dry, light work under cover: no roofing over an occupied house; materials go up the stair and over the terrace; a dust curtain at the stair lobby.",
    "Splitting into three stages costs about Rs 3-4 lakh more overall (coming back, price rises, some repainting).",
    "Outside the estimate and unpriced: the compound wall, thinnai finishes and landscaping, done whenever the owner chooses.",
    "Never defer: structure, anti-termite treatment, plinth, waterproofing, the roof, the courtyard drains, or pipes and conduits buried in walls and slabs.",
]
PHASE2_ROOMS = ("R31", "R45", "R33", "R39", "R34", "R36", "R36A")   # the upstairs rooms whose inner walls and fit-out come in stage 3

HOLD_POINTS = [
    ("Before design freeze", "Soil test report, level survey of plot and road, water quality test (TDS, hardness, fluoride)", "Owner, engineer"),
    ("Excavation", "Footing depth and bearing layer seen in the pit, including round the sunk courtyard; no black soil left under footings", "Structural engineer"),
    ("Before each concrete pour", "Reinforcement, cover blocks, laps and column positions checked; photos taken", "Engineer / site supervisor"),
    ("Plinth", "Anti-termite treatment (certificate), fill compaction, DPC laid and cured", "Supervisor"),
    ("Before plaster", "Conduits, pipes, AC sleeves, mesh over AAC joints; photos with a tape measure in view", "Owner, supervisor"),
    ("Wet rooms", "Waterproofing coats, upturns, 48 h flood test passed before any tile is laid (the terrace slab and both sunk slabs included)", "Owner, plumber"),
    ("Courtyard", "Floor falls to both drains, the first-flush filter, the standpipe overflow and the scupper tested with a hose before the stone is laid; the steel grille and the shade-cloth track fixed and tested", "Owner, plumber"),
    ("Roof", "Truss holding-down bolts, membrane and insulation, edge tiles clipped, flashing where the ring roof meets the wing's walls and the terrace's edge walls, the box gutter at the wing's re-entrant corner, valley gutters at the inside corners, the jharokha kerbs", "Engineer, owner"),
    ("Before handover", "Water test on every floor slope and sill, plumbing pressure test, electrical insulation and earth test", "Owner, MEP"),
]

# ---------- floors: the generic names above (ROOMS, WALLS, ...) hold the floor being drawn ----------
RAILS = []
F1_ROOM_IDS = {r[0] for r in ROOMS_F1}
FLOOR_NAMES = {"G": "Ground floor", "F1": "First floor"}
_FLOOR_DATA = {
    "G": dict(ROOMS=ROOMS, WALLS=WALLS, EXTERIOR=EXTERIOR, DOORS=DOORS, WINDOWS=WINDOWS, FURNITURE=FURNITURE, EXTRA_DRAW=EXTRA_DRAW,
              ELECTRICAL=ELECTRICAL, PLUMBING=PLUMBING, PIPES=PIPES, PILLARS=PILLARS, WET_WALLS=WET_WALLS, EXTRA_EXT_WALLS=EXTRA_EXT_WALLS, RAILS=RAILS),
    "F1": dict(ROOMS=ROOMS_F1, WALLS=WALLS_F1, EXTERIOR=EXTERIOR_F1, DOORS=DOORS_F1, WINDOWS=WINDOWS_F1, FURNITURE=FURNITURE_F1, EXTRA_DRAW=EXTRA_DRAW_F1,
               ELECTRICAL=ELECTRICAL_F1, PLUMBING=PLUMBING_F1, PIPES=[], PILLARS=[], WET_WALLS=WET_WALLS_F1, EXTRA_EXT_WALLS=EXTRA_EXT_WALLS_F1, RAILS=RAILS_F1),
}
_FLOOR_DATA = {f: {k: (list(v) if isinstance(v, list) else set(v)) for k, v in d.items()} for f, d in _FLOOR_DATA.items()}
FLOOR = ["G"]


def set_floor(name):
    """Swap the floor's lists into the generic names, in place, so every module that imported them sees the change."""
    g = globals()
    for k, v in _FLOOR_DATA[name].items():
        if isinstance(g[k], list):
            g[k][:] = v
        else:
            g[k].clear(); g[k].update(v)
    FLOOR[0] = name


@contextmanager
def on_floor(name):
    prev = FLOOR[0]
    set_floor(name)
    try:
        yield
    finally:
        set_floor(prev)


def both(key):
    """A list from both floors, ground first (for schedules)."""
    return _FLOOR_DATA["G"][key] + _FLOOR_DATA["F1"][key]


def floor_base(name=None):
    """Finished floor level of a floor above finished ground."""
    return LEVELS["FFL"] + (LEVELS["upper_ffl"] if (name or FLOOR[0]) == "F1" else 0)


set_floor("G")
