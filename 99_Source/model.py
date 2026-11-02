"""Kerala home, Phase 1 (duplex option): single data model used for every drawing and schedule.
Plan coordinates in feet: x = from west boundary (0-75), y = from south boundary (0-27 plot).
The duplex is planned in the front 64 ft of the plot (x 11-75); the back 11 ft (x 0-11) stays spare land.
Two floors: ground (G) and first (F1). Lists for the floor being drawn are swapped in by set_floor() at the end.
Site: Guntur, Andhra Pradesh. Hot-dry summers (42-45 C), ~850-1000 mm rain (Jun-Oct, cyclonic bursts Oct-Nov),
likely expansive black cotton soil, hard / high-fluoride groundwater, seismic zone III, high cyclone wind speeds.
"""
from contextlib import contextmanager

PROJECT = {
    "name": "Kerala Home, Phase 1",
    "stage": "Draft for professional review (duplex option)",
    "plot": "27 ft x 75 ft; duplex trial uses the front 64 ft, back 11 ft spare",
    "location": "Guntur, Andhra Pradesh (agricultural land: conversion to be confirmed)",
    "road": "East",
    "rev": "C-duplex (option study)",
    "date": "1 Nov 2026",
}
SITE = {"w": 27, "l": 75, "strip": 0, "trial": 11}  # plot width (N-S), length (E-W), north strip (none), x where the 64 ft trial plot starts
T = 0.75  # outer wall thickness, ft (9 in finished)

# ---------- ground floor ----------
ROOMS = [  # id, name, x1, x2, y1, y2, zone
    ("R01", "Master bedroom", 14, 28, 3, 14, "Master suite"),
    ("R40", "Master bath", 28, 36, 3, 8.75, "Master suite"),
    ("R41", "Master vestibule", 28, 36, 8.75, 11.5, "Master suite"),
    ("R42", "Guest room / den", 14, 28, 14, 25, "Private"),
    ("R08", "Common bath", 36, 42, 3, 11.5, "Service"),
    ("R05", "Lobby", 28, 34.5, 11.5, 18, "Circulation"),
    ("R07", "Guest bath", 28, 34.5, 18, 25, "Service"),
    ("R09", "Stair hall", 34.5, 42, 11.5, 15.67, "Circulation"),
    ("R06", "Stair", 34.5, 42, 15.67, 25, "Circulation"),
    ("R13", "Wet area", 42, 53, 3, 7.5, "Service"),
    ("R10", "Dining", 42, 53, 7.5, 12.5, "Living"),
    ("R15", "Kitchen", 53, 67, 3, 12.5, "Service"),
    ("R16", "Living", 42, 61, 12.5, 25, "Living"),
    ("R11", "Pooja", 57, 61, 21, 25, "Living"),
    ("R18", "Genkan (shoe-off foyer)", 57, 61, 12.5, 21, "Entry"),
    ("R17", "Poomukham (verandah)", 61, 67, 12.5, 25, "Entry"),
]

# Walls: (axis, coordinate, start, end). axis "X" = runs along x at y=c; "Y" = runs along y at x=c.
WALLS = [
    ("X", 3, 14, 67), ("Y", 14, 3, 25), ("X", 25, 14, 61), ("Y", 67, 3, 12.5), ("Y", 61, 12.5, 25),
    ("Y", 28, 3, 11.5), ("Y", 28, 11.5, 18), ("Y", 28, 18, 25), ("X", 11.5, 28, 36), ("X", 14, 14, 28), ("X", 8.75, 28, 36), ("Y", 34.5, 8.75, 11.5), ("Y", 36, 3, 11.5), ("X", 11.5, 36, 42), ("Y", 42, 3, 11.5),
    ("Y", 34.5, 11.5, 25), ("Y", 42, 15.67, 25), ("X", 18, 28, 34.5),  # cross wall on y 11.5, the same line as upstairs; stair-hall opening = the hall's width
    ("X", 7.5, 42, 53),  # one straight wall: the dining nook folded into a linear utility
    ("Y", 53, 3, 12.5), ("X", 12.5, 53, 67),  # kitchen: west wall (wet-area door, serving hatch) and north wall (living door, poomukham side)
    ("Y", 57, 21, 25), ("X", 21, 57, 61),  # pooja in the north-east corner of the living
]
EXTERIOR = {("X", 3), ("Y", 14), ("X", 25), ("Y", 67), ("Y", 61)}
# Wall types (finished thickness, ft). AAC blocks in an RCC frame; walls carrying concealed plumbing are thicker
# so pipe chases do not cut a 4 in block in half.
WALL_TYPES = {
    "EXT": (0.75, "200 mm AAC + 20 mm external plaster + 12 mm internal plaster (~9 in)"),
    "WET": (0.58, "150 mm AAC + plaster both faces (~7 in): concealed plumbing walls"),
    "INT": (0.42, "100 mm AAC + plaster both faces (~5 in)"),
}
EXTRA_EXT_WALLS = {("X", 12.5, 53, 67)}  # kitchen north wall faces the living, the pooja and the open poomukham
WET_WALLS = {("Y", 28, 3, 11.5), ("Y", 36, 3, 11.5), ("Y", 42, 3, 11.5), ("X", 7.5, 42, 53), ("Y", 28, 18, 25), ("X", 18, 28, 34.5)}  # bath WCs, basins and showers; washing machine

# Levels and heights, ft. 0 = finished ground level (FGL) around the house.
LEVELS = {
    "FGL": 0.0,
    "FFL": 2.0,          # plinth: ground floor finished level
    "poomukham": 1.5,    # verandah one step (6 in) below the house
    "wet_area": 1.75,    # wet area 3 in below the house
    "bath_drop": 0.04,   # bathrooms 1/2 in (12 mm) below adjoining floor, no raised threshold
    "door_head": 7.0,    # above floor level; continuous RCC lintel band at this level
    "wall_top": 10.0,    # above FFL: ground-floor ring beam / first-floor slab level; front gable and kitchen wing trusses bolted to it
    "upper_ffl": 10.0,   # first floor finished level above FFL (floor to floor)
    "upper_wall_top": 10.0,  # above the first floor: ring beam, main roof trusses bolted to it
    "slab": 0.5,         # RCC slab + screed + finish at the first floor
    "false_ceiling": 9.5,
    "bath_ceiling": 8.5,
    "riser": 0.5,        # entrance steps: 6 in risers, 12 in treads
}
FLOOR_FINISH = {  # room: floor finish key
    "R10": "Red oxide / Kota stone", "R16": "Red oxide / Kota stone", "R11": "Red oxide / Kota stone", "R05": "Red oxide / Kota stone",
    "R06": "Red oxide / Kota stone", "R09": "Red oxide / Kota stone", "R38": "Matt vitrified 2x2", "R39": "Anti-skid ceramic, waterproofed", "R07": "Anti-skid ceramic, waterproofed", "R34": "Red oxide / Kota stone", "R35": "Matt vitrified 2x2",
    "R01": "Matt vitrified 2x2", "R04": "Red oxide / Kota stone", "R31": "Matt vitrified 2x2", "R32": "Matt vitrified 2x2",
    "R40": "Anti-skid ceramic, waterproofed", "R41": "Matt vitrified 2x2", "R42": "Matt vitrified 2x2", "R08": "Anti-skid ceramic, waterproofed", "R33": "Anti-skid ceramic, waterproofed",
    "R13": "Anti-skid ceramic, waterproofed", "R15": "Anti-skid ceramic, waterproofed",
    "R17": "Flamed granite", "R18": "Flamed granite (shoes-on zone, one step below the living)", "R36": "Matt vitrified 2x2", "R37": "Terracotta anti-skid tile, waterproofed",
}
ROOM_LABEL_AT = {"R01": (21.0, 11.0), "R42": (21.0, 17.0), "R06": (38.3, 23.2), "R11": (59.0, 23.4), "R18": (59.0, 17.5), "R16": (50.0, 16.6), "R17": (64, 19.0), "R10": (48.0, 10.6),
                 "R34": (37.5, 13.2), "R38": (31.25, 16.8), "R31": (21, 11.0), "R37": (51, 14.0)}  # label points for rooms whose centre is crowded
ROOM_FLOOR = {"R08": -0.04, "R07": -0.04, "R40": -0.04, "R39": -0.04, "R33": -0.04, "R11": 0.25, "R18": -0.5, "R13": -0.25, "R17": -0.5, "R37": -0.25}  # offset from the floor level
# ceiling: ("flat", height above the room's floor level) or ("sloped", note)
CEILINGS = {
    "R01": ("flat", 9.4), "R04": ("flat", 9.4), "R05": ("flat", 9.4), "R40": ("flat", 8.5), "R41": ("flat", 9.4), "R42": ("flat", 9.4), "R08": ("flat", 8.5),
    "R06": ("sloped", "open to the roof (stair)"), "R09": ("flat", 9.4), "R07": ("flat", 8.5), "R38": ("flat", 9.5), "R39": ("flat", 8.5), "R13": ("flat", 9.4), "R15": ("flat", 9.4),
    "R10": ("sloped", "slab soffit at 9'-5\", open over the table to the light well"), "R18": ("flat", 9.4), "R16": ("flat", 9.4), "R11": ("flat", 9.0),
    "R17": ("sloped", "exposed rafters"),
    "R31": ("flat", 9.5), "R32": ("flat", 9.5), "R33": ("flat", 8.5), "R34": ("sloped", "follows roof"),
    "R35": ("flat", 9.5), "R36": ("flat", 9.5), "R37": ("sloped", "steel trusses, tiled roof above"),
}
ROOF = {
    "pitch": 30,          # degrees
    "overhang": 2.0,      # eaves beyond the outer wall centreline (keeps the north eave inside the 27 ft plot)
    "hip": (12.0, 63.0, 1.0, 27.0),    # main hipped roof over the two-storey block: eaves outline x1, x2, y1, y2
    "gable": (61.0, 69.0, 10.5, 27.0),  # front mukhappu gable over the poomukham only, centred on the main door (y 18.75), ridge E-W
    "wing": (61.0, 69.0, 1.0, 10.5),    # low hipped roof over the kitchen front: hips to the east, north and south; eaves level with the gable's, ridge lower, kept plain (no finial or vents)
    "gablet": 3.5,        # Kerala gablet at both hip ends of the main roof: a jali triangle this high under the ridge lets the hot roof air out
    "chaipu": [(12.0, 61.0, 1.0, 3.0, "S"), (12.0, 14.0, 1.0, 25.375, "W")],  # low lean-to roofs on the south and west walls, eaves level with the front roofs
    "gable_lift": 0.24,   # gable eaves sit just above a plain eave line at ground-floor wall top
    "downpipes": [(12.0, 1.0), (38.0, 1.0), (69.0, 1.0), (69.0, 10.5), (12.0, 26.9), (38.0, 26.9), (69.0, 26.9)],  # (69, 10.5): the valley between gable and wing
}

# Site features: id, label, kind ("rect"/"circle"), geometry (x1, x2, y1, y2) or (x, y, r)
SITE_FEATURES = [
    ("SPARE", "Spare land, back 11 ft (owner's): a walled back-garden court with kitchen-garden beds, clothes drying, the septic tank (north-west) and soak pit", "rect", (0.4, 10.4, 0.4, 26.6)),
    ("HEDGE3", "Low hedge on the 64 ft line (the trial plot starts here), open opposite the den's garden door", "rect", (10.6, 11.0, 1.0, 17.5)),
    ("HEDGE4", "Low hedge on the 64 ft line, north part", "rect", (10.6, 11.0, 21.5, 26.0)),
    ("OTTA", "Stone-paved sit-out under the creeper pergola, outside the den's garden door", "rect", (11.0, 13.6, 14.5, 24.0)),
    ("GSTEP", "Stone steps from the den's garden door down to the sit-out (4 risers along the wall)", "rect", (12.4, 13.6, 18.3, 20.8)),
    ("SEPTIC", "Septic tank, 2 chambers, sealed RCC, in the north-west corner of the back garden (the vastu position), heavy-duty covers", "rect", (1.0, 5.0, 19.5, 25.5)),
    ("SOAK", "Lined soak pit for septic effluent and grey water, in the spare land, about 9 ft from the house", "circle", (3.5, 14.0, 1.6)),
    ("SUMP", "Sump (NE)", "rect", (71, 74.5, 23.5, 26.5)),
    ("BORE", "Borewell (if any), NE", "circle", (70, 25.6, 0.5)),
    ("PERGOLA", "Creeper pergola along the west wall (shades the master window; no big trees near walls)", "rect", (11.4, 13.4, 4.5, 24.0)),
    ("TULSI", "Tulsi thara at the centre of the forecourt, on the door axis", "circle", (72.4, 18.75, 0.6)),
    ("PATH", "Stone-paved forecourt 6 ft wide on the door axis, gate to steps, around the tulsi thara", "rect", (69.8, 75.0, 15.75, 21.75)),
    ("HEDGE1", "Low hedge screening the two-wheeler bay (access left open by the gate)", "rect", (68.0, 71.0, 11.2, 11.8)),
    ("HEDGE2", "Low hedge screening the sump", "rect", (70.6, 74.6, 22.8, 23.3)),
    ("BAY", "Two-wheeler bay (front yard now free of the septic tank)", "rect", (68, 74, 3, 11)),
    ("GATE", "Gate 7 ft, centred on the main door", "rect", (75, 75.5, 15.25, 22.25)),
    ("GATE2", "Scooter gate 4 ft beside the two-wheeler bay (keeps scooters off the forecourt and the tulsi)", "rect", (75, 75.5, 4.0, 8.0)),
    ("STEPS", "Entrance steps (3 risers), between the pillars, SS handrail one side", "rect", (67.375, 69.0, 16.95, 20.55)),
    ("FEET", "Foot-wash tap + drain", "circle", (69.6, 13.6, 0.35)),
    ("WSTEP", "Landing at the wet-area service door, then 3 steps down along the wall (4 risers of about 5 in), 1'-3\" deep so a clear strip of the walkway stays beside them", "rect", (46.5, 51.7, 1.35, 2.6)),
    ("APRON", "Plinth protection apron 3 ft, sloped away", "apron", (11, 70, 0, 28)),
]
TREES = []  # kept 8 ft+ from walls: roots dry out black cotton soil
JALI_SCREENS = [("X", 24.9, 61.4, 66.0)]  # free-standing timber jali screens: the poomukham's open north side (the neighbour is 2 ft away)
FUTURE_WALLS = []

# Doors: id, axis, c, s, e, swing (+1 toward +y/+x, -1 toward -y/-x, 0 = sliding), name, type
DOORS = [
    ("D01", "Y", 61, 16.75, 20.75, -1, "Main entrance, 4 ft (on the entry axis y 18.75: gable, door, steps, path, tulsi and gate on one line)", "Teak panelled, double leaf, jali panel above: the widest and tallest threshold in the house"),
    ("D02", "Y", 28, 14.5, 17.0, -1, "Guest room / den (from the lobby)", "Flush, teak veneer"),
    ("D04", "X", 11.5, 29.0, 31.5, 1, "Master suite (from the lobby into its vestibule, opens out)", "Flush, teak veneer"),
    ("D44", "Y", 34.5, 12.4, 14.9, 1, "Bedroom wing (from the stair hall): shut it and the master suite, the den and the guest bath are private", "Teak panelled, jali panel above"),
    ("D45", "Y", 14, 18.25, 20.75, 1, "Garden door from the den to the back garden sit-out (opens inward)", "Teak frame, glazed upper half, steel grille shutter outside"),
    ("D41", "Y", 28, 9.0, 11.25, 0, "Master bedroom (from its vestibule, pocket door)", "Teak veneer pocket door, quality track"),
    ("D42", "X", 8.75, 31.7, 34.0, -1, "Master bath (from the vestibule, opens inward; the leaf screens the WC)", "Flush, waterproof (WPC/FRP)"),
    ("D43", "X", 14, 24.9, 27.2, -1, "Connecting door, master bedroom to the den (shut it and the den is a guest suite)", "Flush, teak veneer, acoustic seals"),
    ("D08", "X", 11.5, 39.2, 41.7, -1, "Common bath (from the stair hall, opens inward; the open leaf screens the WC and basin, the first view is the shower)", "Flush, waterproof (WPC/FRP), door closer"),
    ("D07", "Y", 28, 18.6, 20.85, 1, "Guest bath (from the den, opens inward on lift-off hinges)", "Flush, waterproof (WPC/FRP)"),
    ("D11", "Y", 57, 21.55, 24.35, 1, "Pooja (north-east corner of the living)", "Carved teak, double leaf (opens inward, clear of the living; faces west, family faces east)"),
    ("D12", "Y", 53, 4.6, 7.1, 0, "Kitchen to wet area (sliding)", "Steel or WPC sliding, lockable"),
    ("D17", "X", 12.5, 53.6, 56.1, 0, "Kitchen entry from the living (sliding)", "Teak frame, glazed sliding door, 2'-6\" (closes off cooking smoke)"),
    ("D18", "X", 3, 46.8, 49.3, 1, "Wet area service door to the south walkway (opens inward)", "Steel, lockable, louvred top"),
]
# Vents above inner doors (7'-6" to 9'-0", above the lintel band): air moves between rooms with doors shut
TRANSOM_TYPES = {
    "jali": "Teak jali vent in a frame: air passes freely (rooms with no sound-privacy need)",
    "jali_closable": "Teak jali with a sliding timber shutter on the room side: open for air, shut for sound privacy",
    "louvre": "Fixed louvres angled down: air for the exhaust fan, no view in",
    "glazed": "Top-hung glazed vent with seals: open for air, closed for calls",
}
TRANSOMS = {"D11": "jali", "D01": "jali", "D02": "jali_closable", "D42": "louvre", "D43": "jali_closable", "D44": "jali", "D04": "jali_closable", "D07": "louvre", "D08": "louvre",
            "D31": "jali_closable", "D35": "jali_closable", "D33": "louvre", "D39": "louvre", "D36": "jali"}  # rooms breathe into the stair well with doors shut
HINGE_AT_END = {"D36", "D42"}  # D36 hinged at its north jamb so its leaf clears the light-well rail  # doors hinged at their far (e) jamb
TRANSOM_LABELS = {"jali": "Open jali", "jali_closable": "Closable jali", "louvre": "Louvres", "glazed": "Sealed glazed flap"}
TRANSOM_Z = (7.5, 9.0)  # sill and head above the floor

# Windows: id, axis, c, s, e, sill, head, room, type (sill and head above the floor the window serves)
WINDOWS = [
    ("W01", "Y", 14, 7.2, 9.8, 3, 7, "Master bedroom", "Timber jali + glazed shutters (west, on the y 8.5 axis under W36; shaded by the pergola and the chaipu)"),
    ("W02", "X", 3, 31.25, 33.25, 5, 7, "Master bath", "Frosted casement, top-hung vent (2 ft bath window, centred under the alcove window above)"),
    ("W03", "X", 3, 38.05, 40.05, 5, 7, "Common bath", "Frosted casement, top-hung vent (centred on the shower band)"),
    ("W04", "X", 25, 18.0, 24.0, 3, 7, "Guest room / den", "Teak casement, glazed (6 ft), fixed jali on the lower 2 ft (privacy from the neighbour 2 ft away), hood above"),
    ("W05", "X", 25, 36.25, 40.25, 6, 9.5, "Stair", "Glazed casement at the half landing, centred on the stair (the clerestory W45 stacks above it)"),
    ("W10", "Y", 42, 15.9, 17.75, 1, 9.3, "Stair", "Timber jali screen between the stair well and the living, up to the slab (air into the stair chimney)"),
    ("W11", "X", 3, 42.7, 45.3, 3, 7, "Wet area", "Timber jali + glazed shutters (2'-7\" room window, over the crockery unit in the utility)"),
    ("W48", "X", 3, 14.9, 17.5, 3, 7, "Master bedroom", "Timber jali + glazed shutters, west of the bed head (stacked under W31)"),
    ("W49", "X", 3, 24.5, 27.1, 3, 7, "Master bedroom", "Timber jali + glazed shutters, east of the bed head (stacked under W37)"),
    ("W12", "X", 3, 49.95, 51.95, 5, 7, "Wet area", "Jali vent over the utility sink (2 ft vent window)"),
    ("W07", "X", 3, 54.6, 60.6, 3.5, 7, "Kitchen", "Timber jali + glazed shutters (clear of the terrace post over x 61; the sink centred under it)"),
    ("W08", "Y", 67, 10.4, 12.0, 6, 8, "Kitchen", "High ventilator, jali + louvres above the counter (smoke and hot air out; the hob wall below stays solid)"),
    ("W09", "X", 25, 44.5, 50.5, 3, 7, "Living", "Teak casement, glazed (6 ft), fixed jali on the lower 2 ft (privacy from the neighbour), hood above"),
    ("W43", "X", 25, 32.0, 34.0, 5, 7, "Guest bath", "Frosted casement, top-hung vent"),
    ("W44", "Y", 53, 7.9, 12.1, 3.0, 7, "Kitchen / dining", "Serving hatch over a granite counter, glazed sliding shutters (close while cooking)"),
    ("W17", "Y", 61, 21.6, 24.4, 5.5, 7, "Pooja", "High vent to the poomukham, jali + mesh (lamp smoke out)"),
    ("W50", "X", 3, 54.6, 60.6, 7.5, 9.0, "Kitchen", "High jali ventilator above the window W07 (hot air out under the ceiling)"),
    ("W46", "Y", 61, 13.2, 15.8, 4.5, 7, "Genkan", "Timber jali + glazed shutters over the shoe bench (light from the poomukham)"),
    ("W47", "X", 25, 51.0, 56.5, 7.5, 9.0, "Living", "Glazed clerestory, top-hung: sky light above the neighbour's wall, hot air out under the slab"),
]
OTHER_OPENINGS = [
    ("GV1", "Teak-boarded gable face with a 4 ft timber jali panel centred over the main door: vents the roof space over the verandah"),
]
PILLARS = [(66.4, 13.1), (66.4, 16.05), (66.4, 21.45), (66.4, 24.4)]  # on the entry axis y 18.75; the north edge spans to the wall on a teak beam (room for the swing)

# Furniture: id, room, item, x1, x2, y1, y2, qty, material / spec, shape ("rect"|"circle"|"wc"|"glass")
FURNITURE = [
    ("F10", "Master bedroom", "King bed 6' x 6'6\" + headboard, head to the south wall between two windows (true south-west; stacked under Bedroom 2's bed)", 18.0, 24.0, 3.4, 9.9, 1, "Teak, head to south", "rect"),
    ("F12", "Master bath", "WC (EWC) on the x 36 wet wall, back to back with the common bath WC (one stack); the open door leaf screens it", 34.4, 36.0, 7.2, 8.4, 1, "Wall-hung, concealed cistern", "wc"),
    ("F13", "Master bath", "Shower glass partition (shower 3' x 3' in the south-west corner, on the bedroom wet wall)", 31.2, 31.35, 3.4, 6.4, 1, "8 mm toughened glass", "glass"),
    ("F14", "Master bath", "Wash basin under the frosted window, mirror beside it", 32.3, 33.8, 3.4, 4.1, 1, "Wall-hung", "rect"),
    ("F15", "Master vestibule", "Linen cupboard, full height", 34.7, 35.8, 9.0, 11.25, 1, "Ply + laminate", "rect"),
    ("F11", "Master bedroom", "Floating bedside shelf with a drawer, reading light and charging point above (against the south wall)", 17.0, 18.0, 3.4, 4.4, 2, "Teak, wall-hung", "rect"),
    ("F06", "Master bedroom", "Built-in sliding wardrobe 8' on the north wall (y 14, under the upstairs wall), doors facing the bed, lofts above", 16.5, 24.5, 12.1, 13.8, 1, "Ply + laminate, sliding shutters", "rect"),
    ("F16", "Common bath", "WC (EWC) on the west wet wall, mid-room with 3'-6\" clear in front, under the upper bath WC (one stack)", 36.3, 37.9, 7.2, 8.4, 1, "Wall-hung on the wet wall, concealed cistern", "wc"),
    ("F17", "Common bath", "Wash basin with a mirror cabinet above (east wall, opposite the WC)", 41.0, 41.7, 7.3, 8.5, 1, "Wall-hung", "rect"),
    ("F18", "Common bath", "Shower glass partition: the shower runs across the whole south end (5'-6\" x 3'), entered from its east side", 36.3, 39.3, 6.4, 6.55, 1, "8 mm toughened glass", "glass"),
    ("F64", "Common bath", "Recessed shower niche 1' x 1'-7\" x 3 in deep, tiled, sloped sill (south wall)", 40.0, 41.0, 3.38, 3.6, 1, "Tile lined, waterproofed", "glass"),
    ("F20", "Guest room / den", "Sofa-cum-bed 6'-6\" x 3' under the north window W04 (guest bed), facing the TV, drawers below", 17.75, 24.25, 21.6, 24.6, 1, "Teak, cotton mattress and bolsters", "rect"),
    ("F67", "Guest room / den", "Armchair facing the TV", 14.7, 17.2, 15.6, 18.1, 1, "Teak frame, cane, cotton cushion", "rect"),
    ("F66", "Guest room / den", "Coffee table 2'-6\" x 2'", 19.75, 22.25, 18.4, 20.4, 1, "Teak", "rect"),
    ("F23", "Guest room / den", "Low TV unit on the south wall, TV above, centred on the sofa-bed and the north window", 18.5, 23.5, 14.4, 15.6, 1, "Teak / ply", "rect"),
    ("F57", "Stair and passage", "Under-stair cupboard under flight 2 where it rises above 7 ft (DB, inverter, brooms), doors facing the stair hall", 38.6, 41.7, 18.6, 21.3, 1, "Ply + laminate, ventilated", "rect"),
    ("F81", "Stair and passage", "Built-in bench with a planter under the high end of flight 2, seen from the living through the jali (a nook, not dead space)", 38.7, 41.7, 15.9, 17.3, 1, "Teak seat, cushion; planter at the north end", "rect"),
    ("F58", "Stair and passage", "Pull-out drawers under flight 1 where it rises above 2'-6\" (shoes, brooms, tools)", 34.7, 37.8, 19.0, 21.4, 1, "Ply + laminate", "rect"),
    ("F56", "Lobby", "Coat, shoe and linen cupboard 3'-4\" on the north wall, kept clear of the den door, lofts above", 30.2, 33.5, 15.9, 17.8, 1, "Ply + laminate, full height", "rect"),
    ("F48", "Guest bath", "WC (EWC) on the bedroom wall", 28.3, 29.9, 21.0, 22.2, 1, "Wall-hung, concealed cistern", "wc"),
    ("F49", "Guest bath", "Wash basin with a mirror cabinet above", 32.3, 33.8, 18.3, 19.0, 1, "Wall-hung", "rect"),
    ("F50", "Guest bath", "Shower glass partition (shower in the north-east corner, about 3' x 3')", 31.2, 34.2, 21.4, 21.55, 1, "8 mm toughened glass", "glass"),
    ("F24", "Dining", "Dining table 5'-6\" x 2'-6\" under the light well, extending to 7'-6\" for festivals (5 daily with the bench and end chairs, 8 with stools)", 44.5, 50.0, 9.0, 11.5, 1, "Teak, extending", "rect"),
    ("F25", "Dining", "Dining chair at the west end of the table (no chair backs in the living path)", 43.0, 44.4, 9.55, 10.95, 1, "Teak, cane seat", "rect"),
    ("F27", "Dining", "Dining chair at the east end of the table", 50.1, 51.5, 9.55, 10.95, 1, "Teak, cane seat", "rect"),
    ("F28", "Dining", "Built-in bench along the dining's straight south wall, storage below", 44.5, 50.0, 7.85, 8.85, 1, "Teak, cushion", "rect"),
    ("F33", "Dining", "Granite serving ledge 9 in deep under the kitchen hatch (dining side)", 52.0, 52.75, 7.9, 12.1, 1, "Granite top on brackets", "rect"),
    ("F44", "Wet area", "Crockery unit under the south window, glass shutters (in the utility, beside the vessel washing)", 42.3, 45.7, 3.3, 4.6, 1, "Teak + glass", "rect"),
    ("F29", "Wet area", "Utility sink counter on the south wall, where vessels are washed (clear of both doors)", 50.0, 51.9, 3.4, 5.3, 1, "Kadappa / granite, SS sink", "rect"),
    ("F62", "Wet area", "Dish-drying rack over the utility sink: steel rods, drip tray draining into the sink", 50.1, 51.8, 3.45, 4.2, 1, "SS 304", "glass"),
    ("F30", "Wet area", "Washing machine bay 2' x 2' against the north wall, clear of the service-door swing", 43.2, 45.1, 5.4, 7.2, 1, "Splash-proof socket, floor drain", "rect"),
    ("F61", "Wet area", "Ceiling clothes airer on pulleys (lower to load, raise to dry)", 46.6, 52.4, 5.8, 7.1, 1, "Aluminium rails, nylon rope, cleat on the wall", "glass"),
    ("F31", "Wet area", "Fold-away clothesline in the south walkway behind the master", 15.0, 25.0, 0.6, 2.4, 1, "SS wire, wall brackets", "glass"),
    ("F34", "Kitchen", "L-counter, south run: prep sink centred under the window W07, a 6 ft clear prep run from the sink to the corner unit, deep drawers for vessels (stops clear of the wet-area door)", 55.6, 64.6, 3.4, 5.4, 1, "Granite top, ply carcass", "rect"),
    ("F68", "Kitchen", "Full-height corner unit in the south-east corner (pull-out larder; no blind corner)", 64.6, 66.6, 3.4, 5.4, 1, "Ply + laminate, full height", "rect"),
    ("F60", "Kitchen", "Utensil rail with hooks beside the hob (ladles, tongs, strainers)", 66.45, 66.6, 5.6, 6.9, 1, "SS rail and S-hooks", "glass"),
    ("F35", "Kitchen", "L-counter, east run (hob centred at y 8.6 on solid wall, about 2 ft of landing each side; pull-out masala drawer beside the hob)", 64.6, 66.6, 5.4, 11.9, 1, "Granite top, cook faces east", "rect"),
    ("F65", "Kitchen", "Prep sink, single bowl + drainboard, centred under the window (washes vegetables; vessels go to the wet area)", 56.7, 58.5, 3.6, 5.2, 1, "SS 304, under-mount", "rect"),
    ("F37", "Kitchen", "Tall pantry unit 2', microwave inside, against the east run (tall storage grouped at the north end)", 62.5, 64.5, 10.1, 12.1, 1, "Ply + laminate, full height, pull-outs", "rect"),
    ("F36", "Kitchen", "Refrigerator on the north wall, grouped with the pantry, clear of the sliding entry", 60.0, 62.5, 10.1, 12.1, 1, "Double-door, 2'6\" wide", "rect"),
    ("F53", "Living", "TV unit 4'-3\" on the stair wall, 50 in TV above: one composed teak wall with the jali W10 and the lamp niche (a single teak frame and head line at 7 ft, the TV inside the frame)", 42.3, 43.6, 20.3, 24.6, 1, "Teak, low, open shelves", "rect"),
    ("F38", "Living", "Sofa 5' (2-3 seats) facing west to the TV about 6'-6\" away", 50.5, 53.2, 19.6, 24.6, 1, "Teak frame, cotton cushions", "rect"),
    ("F39", "Living", "Coffee table 3'2\" x 2', 1'-6\" from the sofa", 47.0, 49.0, 20.6, 23.8, 1, "Teak", "rect"),
    ("F45", "Living", "Armchair facing north to the sofa group (with F46, a soft edge to the seating, not a sofa back)", 44.8, 46.6, 17.8, 19.6, 1, "Teak frame, cane, cotton cushion", "rect"),
    ("F46", "Living", "Armchair facing north to the sofa group", 47.4, 49.2, 17.8, 19.6, 1, "Teak frame, cane, cotton cushion", "rect"),
    ("F59", "Living", "Vilakku madam: carved teak lamp niche with a light inside, on the wall facing the main door (on the entry axis)", 42.21, 42.55, 17.85, 19.65, 1, "Carved teak, brass lamp", "glass"),
    ("F52", "Genkan (shoe-off foyer)", "Shoe bench 3'-3\" in the genkan (sit to take shoes off), louvred shoe shelves below, hooks and a keys niche above", 59.4, 60.6, 13.0, 16.3, 1, "Teak top, ply + laminate, 14 in deep", "rect"),
    ("F26", "Pooja", "Pooja mandapam on the east wall (idols face west; family faces east)", 60.0, 60.6, 21.6, 24.4, 1, "Carved teak", "rect"),
    ("F41", "Poomukham (verandah)", "Oonjal (swing) 3'6\", north side of the verandah, hung from the gable beam, its arc clear of the entrance walk and the pillars", 62.0, 65.3, 22.2, 23.7, 1, "Teak, chains to beam", "rect"),
    ("F42", "Poomukham (verandah)", "Charupadi: built-in teak seat with a sloping backrest between the pillars, south of the steps", 65.6, 66.9, 13.5, 15.7, 1, "Laterite base, teak seat and backrest", "rect"),
    ("F69", "Poomukham (verandah)", "Charupadi: built-in teak seat with a sloping backrest between the pillars, north of the steps", 65.6, 66.9, 21.85, 24.0, 1, "Laterite base, teak seat and backrest", "rect"),
]
# extra placements (same item, additional copies drawn on plan)
EXTRA_DRAW = [("F11", 24.0, 25.0, 3.4, 4.4)]

# ---------- first floor: rooms over the back half, a covered terrace over the front half ----------
ROOMS_F1 = [
    ("R31", "Bedroom 2", 14, 28, 3, 14, "Upper suite"),
    ("R32", "Bedroom 2 wardrobe alcove", 28, 36, 3, 11.5, "Upper suite"),
    ("R33", "Bedroom 2 bath", 36, 42, 3, 11.5, "Upper suite"),
    ("R34", "Landing", 28, 42, 11.5, 15.67, "Circulation"),
    ("R38", "Toilet lobby", 28, 34.5, 15.67, 18, "Circulation"),
    ("R39", "Upper toilet", 28, 34.5, 18, 25, "Service"),
    ("R36", "Study", 14, 28, 14, 25, "Work"),
    ("R37", "Covered terrace", 42, 61, 3, 25, "Terrace"),
]
WALLS_F1 = [
    ("X", 3, 14, 42), ("X", 25, 14, 42), ("Y", 14, 3, 25), ("Y", 42, 3, 25),
    ("X", 14, 14, 28), ("Y", 28, 3, 25), ("X", 11.5, 28, 42), ("Y", 36, 3, 11.5), ("X", 18, 28, 34.5), ("Y", 34.5, 15.67, 25),
]
EXTERIOR_F1 = {("X", 3), ("Y", 14), ("X", 25), ("Y", 42)}
WET_WALLS_F1 = {("Y", 36, 3, 11.5), ("Y", 28, 18, 25), ("X", 18, 28, 34.5)}
# Railings at the first floor (axis, c, s, e): open sides of the terrace, edges of the stair well. 3'-6" high.
RAILS_F1 = [("X", 15.67, 34.5, 38),
            ("X", 3, 42, 61), ("X", 25, 42, 61), ("Y", 61, 3, 25),
            ("X", 8, 44.75, 49.75), ("X", 12.5, 44.75, 49.75), ("Y", 44.75, 8, 12.5), ("Y", 49.75, 8, 12.5)]  # last four: around the light well
# Terrace sides that face the neighbours a few feet away: closed teak jali parapets 3'-6" high (privacy, breeze), not open balusters.
# The road side stays an open railing behind the front gable.
JALI_RAILS = {("X", 3), ("X", 25)}
# Steel posts carrying the main roof over the covered terrace (galvanised SHS on RCC column stubs)
TERRACE_POSTS = [(53.0, 3.0), (61.0, 3.0), (61.0, 12.5), (61.0, 25.0), (53.0, 25.0)]  # each on a wall corner below; the 12.5 ft bay frames the poomukham
# Stair: dog-leg, 16 risers of 7.5 in (floor to floor 10 ft), 10 in treads, 3'-6" flights and a 3'-6" half landing.
# Clockwise going up: flight 1 rises north on the west side, turn right at the half landing, flight 2 rises south on the east side.
STAIR = {
    "risers": 16, "tread": 10 / 12,
    "flight1": (34.5, 38.0, 15.67, 21.5, 8),   # x1, x2, y1 (foot), y2 (top), risers
    "landing": (34.5, 42.0, 21.5, 25.0),
    "flight2": (38.5, 42.0, 15.67, 21.5, 8),   # x1, x2, y1 (top, at the first floor), y2 (foot, at the landing), risers
    "core": (38.0, 38.5, 15.67, 21.5),         # wall between the flights
}
# First-floor slab outline (pieces) and the voids it leaves
SLAB_F1 = [(14, 28, 3, 25), (28, 42, 3, 10), (28, 34.5, 10, 25), (34.5, 42, 10, 15.67), (42, 61, 3, 8), (42, 44.75, 8, 12.5), (49.75, 61, 8, 12.5), (42, 61, 12.5, 25)]
# Light well over the dining table (slab void): rail round it, walk-on jali grating and a closable glazed lid for AC and monsoon
LIGHT_WELL = (44.75, 49.75, 8, 12.5)  # 5 x 4'-6", centred on the dining table

DOORS_F1 = [
    ("D31", "X", 11.5, 29.5, 32.0, -1, "Bedroom 2 (from the landing, into its wardrobe alcove: the bed is out of sight from the door)", "Flush, teak veneer"),
    ("D33", "Y", 36, 8.7, 11.0, 1, "Bedroom 2 bath (from the vestibule, opens inward; the open leaf screens the WC)", "Flush, waterproof (WPC/FRP)"),
    ("D37", "Y", 28, 8.8, 11.2, 0, "Bedroom 2 from its vestibule (pocket door)", "Teak veneer pocket door, quality track"),
    ("D35", "Y", 28, 14.6, 17.2, -1, "Study (from the landing)", "Teak frame, glazed upper panel (frosted), acoustic seals"),
    ("D39", "X", 18, 31.6, 34.0, 1, "Upper toilet (from the toilet lobby, east end, opens inward; the leaf screens the WC: the first view is the shower, never the WC)", "Flush, waterproof (WPC/FRP)"),
    ("D36", "Y", 42, 12.0, 15.5, 1, "Covered terrace (from the landing, opens outward; the main threshold upstairs)", "Teak frame, glazed, 3'-6\", jali vent above"),
]
WINDOWS_F1 = [
    ("W31", "X", 3, 14.9, 17.5, 3, 7, "Bedroom 2", "Timber jali + glazed shutters, west of the bed head"),
    ("W37", "X", 3, 24.5, 27.1, 3, 7, "Bedroom 2", "Timber jali + glazed shutters, east of the bed head"),
    ("W36", "Y", 14, 7.2, 9.8, 5, 7, "Bedroom 2", "High window on the west wall, glazed shutters + grille (on the y 8.5 axis over W01)"),
    ("W35", "X", 3, 30.95, 33.55, 3, 7, "Bedroom 2 wardrobe alcove", "Timber jali + glazed shutters (2'-7\" room window) at the end of the closet aisle, centred over the bath window below"),
    ("W33", "X", 3, 38.05, 40.05, 5, 7, "Bedroom 2 bath", "Frosted casement, top-hung vent (centred on the shower band)"),
    ("W34", "X", 25, 18.0, 24.0, 3, 7, "Study", "Teak casement, glazed (6 ft, even north light for screens)"),
    ("W41", "Y", 14, 18.5, 20.5, 5, 7, "Study", "High jali vent on the y 19.5 axis, over the den's garden door"),
    ("W40", "Y", 42, 15.0, 24.5, 1, 8, "Stair", "Timber jali screen between the stair well and the covered terrace (light and air for the stair), glazed shutters behind it for driving rain and a steel grille inside for security"),
    ("W42", "X", 25, 32.0, 34.0, 5, 7, "Upper toilet", "Frosted casement, top-hung vent (centred on the shower)"),
    ("W45", "X", 25, 36.25, 40.25, 6, 9, "Stair", "Glazed clerestory over the stair well, top-hung: the hot-air outlet of the stair chimney"),
]
FURNITURE_F1 = [
    ("F71", "Bedroom 2", "King bed 6' x 6'6\" + headboard, head to the south wall between the two windows", 18.0, 24.0, 3.4, 9.9, 1, "Teak", "rect"),
    ("F72", "Bedroom 2", "Floating bedside shelf with a drawer, reading light and charging point above", 17.0, 18.0, 3.4, 4.4, 2, "Teak, wall-hung", "rect"),
    ("F74", "Bedroom 2 wardrobe alcove", "Chest of drawers and dresser run on the east wall, mirror above (opposite the hanging run)", 34.4, 35.7, 3.4, 8.5, 1, "Teak", "rect"),
    ("F75", "Bedroom 2 wardrobe alcove", "Hanging wardrobe run 5' (2 ft deep) on the bedroom wall, lofts above; the aisle between ends at the window", 28.25, 30.25, 3.4, 8.5, 1, "Ply + laminate", "rect"),
    ("F77", "Bedroom 2 bath", "WC (EWC) on the west wall, mid-room with 3'-6\" clear in front, over the common bath WC (one stack)", 36.3, 37.9, 7.2, 8.4, 1, "Wall-hung, concealed cistern", "wc"),
    ("F78", "Bedroom 2 bath", "Wash basin with a mirror cabinet above (east wall, the first view from the door)", 40.9, 41.6, 7.3, 8.5, 1, "Wall-hung", "rect"),
    ("F79", "Bedroom 2 bath", "Shower glass partition: the shower runs across the whole south end (5'-6\" x 3')", 36.3, 39.3, 6.4, 6.55, 1, "8 mm toughened glass", "glass"),
    ("F91", "Study", "Linear two-station desk 9' x 2' under the north window W34 (even north light, cameras face the room, not each other)", 16.5, 25.5, 22.6, 24.6, 1, "Teak / ply, cable tray", "rect"),
    ("F92", "Study", "Sofa-cum-bed 6' in front of the library wall (guest bed)", 16.5, 22.5, 15.4, 17.8, 1, "Teak frame, upholstered", "rect"),
    ("F95", "Study", "Full-height library wall on the south wall (call backdrop and sound buffer to Bedroom 2)", 14.5, 25.0, 14.2, 15.2, 1, "Teak / ply, open shelves", "rect"),
    ("F98", "Upper toilet", "WC (EWC) on the west wall, over the master bath WC", 28.3, 29.9, 21.0, 22.2, 1, "Wall-hung, concealed cistern", "wc"),
    ("F99", "Upper toilet", "Wash basin with a mirror cabinet above (south wall, beside the door)", 28.6, 30.1, 18.3, 19.0, 1, "Wall-hung", "rect"),
    ("F70", "Upper toilet", "Shower glass partition (shower in the north-east corner, about 3' x 3')", 31.2, 34.2, 21.4, 21.55, 1, "8 mm toughened glass", "glass"),
    ("F84", "Covered terrace", "Built-in diwan 6' against the stair wall (cushions, bolsters, storage below)", 42.4, 44.4, 16.0, 22.0, 1, "Teak, weatherproof cushions", "rect"),
    ("F85", "Covered terrace", "Low coffee table", 46.0, 48.5, 17.5, 20.5, 1, "Teak", "rect"),
    ("F86", "Covered terrace", "Cane armchair (north of the table, facing it)", 46.35, 48.15, 21.2, 23.0, 1, "Cane", "circle"),
    ("F87", "Covered terrace", "Cane armchair (south of the table, facing it)", 46.35, 48.15, 15.0, 16.8, 1, "Cane", "circle"),
    ("F88", "Covered terrace", "Clothes-drying rails, laundry corner in the south-west (out of sight from the road)", 43.0, 50.0, 3.5, 6.8, 1, "Aluminium rails on pulleys", "glass"),
    ("F80", "Landing", "Teak lamp shelf with a picture light, on the wall you face at the top of the stair (walls too thin for a recess)", 39.4, 41.1, 11.71, 12.1, 1, "Carved teak, brass lamp", "rect"),
    ("F89", "Covered terrace", "Planter boxes along the whole east edge", 59.4, 60.6, 3.5, 24.5, 1, "Ferrocement, drained to the terrace drain", "rect"),
]
EXTRA_DRAW_F1 = [("F72", 24.0, 25.0, 3.4, 4.4)]

FINISHES = [  # spaces, floor, walls (incl. skirting / dado), ceiling, notes
    ("Living, dining", "Red oxide (IPS) or polished Kota / Tandur stone", "4 in flush skirting in floor stone; lime-finish or mineral paint", "RCC slab soffit at 9'-5\", plastered (the covered terrace above keeps it shaded)", "Stone hides dust better than glossy white tile"),
    ("Bedrooms, dressing", "Matt vitrified 2x2 ft or red oxide", "4 in flush skirting; putty + washable emulsion", "Ground floor: RCC slab soffit at 9'-5\", plastered; first floor: false ceiling at 9'-6\", 50 mm insulation above", "First-floor rooms sit under the roof: ventilated attic above the false ceiling"),
    ("Pooja", "White marble or teak", "Teak panelling behind idol; 4 in marble skirting", "Teak / board at 9'-6\"", "Idols on the east wall facing west (family faces east); lamp niche with heat-proof back"),
    ("Kitchen", "Anti-skid matt vitrified or Kota, mid-tone", "Tile / stone full height between counter and wall cabinets", "Moisture-resistant board at 9'-6\", storage loft above", "Counter granite (local Ongole / Chimakurthy), 2 ft deep; deep drawers for vessels, pull-out masala drawer by the hob, utensil rail on the wall beside it"),
    ("Master bath, common bath, upper bath", "Anti-skid ceramic (R11), falls 1:60 to drain", "Tiles to 7 ft; full height in shower; waterproofing 12 in up all walls, 7 ft in shower", "Moisture-resistant board / PVC at 8'-6\"", "Recessed tiled shower niche with a sloped sill; mirror cabinet over the basin; towel and clothes hooks at the dry end; 12 mm step down, no raised threshold; doors open outward (the common bath door opens inward so it never blocks the narrow lobby); SS grab bars by the WC and in the shower. The upper bath sits over the common bath: waterproof the slab and flood-test it before tiling"),
    ("Wet area", "Rough Cuddapah / Kota stone, falls to drain", "4 ft stone or tile dado", "Board at 9'-6\"", "Service door to the walkway with a 6 in kerb"),
    ("Stair", "Granite or Kota treads with a rounded nosing and anti-slip grooves, 10 in treads, 7 in risers", "Teak handrail at 3 ft on the open side, timber jali to the living", "Open to the roof", "Light at the half landing and at the top; 2-way switches"),
    ("Lobby, landing, passage", "Red oxide or vitrified", "4 in flush skirting; washable paint", "Slab soffit / board", ""),
    ("Covered terrace (first floor)", "Terracotta anti-skid tile on a waterproofed slab, falls 1:80 to a drain", "Teak jali parapets 3'-6\" on the north and south sides (neighbours close by); an open railing on the road side (teak cap, MS or teak balusters); bamboo chiks on the south and east", "Steel trusses and the tiled roof above, painted; galvanised steel posts at the terrace edge", "Slab waterproofing and a 48 h flood test before tiling: it sits over the living, dining and kitchen"),
    ("Poomukham, steps", "Flamed / leather-finish granite (not polished)", "Granite skirting; plinth face clad 2 ft (splash zone)", "Exposed rafters + board", "Polished stone is slippery when wet"),
    ("Exterior", "Plinth apron: PCC 3 ft wide sloped away", "AAC + 20 mm plaster with waterproof additive; elastomeric paint", "-", "Drip grooves under every sill and sunshade"),
    ("Roof (all)", "Mangalore clay tiles, every edge tile clipped / screwed", "Membrane + 50 mm insulation on cement-fibre deck", "Steel truss on RCC ring beams (first-floor walls for the main roof, ground-floor walls for the front gable and the kitchen wing)", "Cyclone winds: tie trusses down with holding-down bolts"),
]

OPEN_ISSUES = [
    ("Roof", "Front gable junction: " + 'with the gable now over the poomukham only, its ridge (+15\'-10") stands about 3\'-10" above the terrace floor (+12\'), so its back end meets the terrace\'s east edge as a low triangle just above the railing. (1) Close that triangle with a timber jali on the terrace edge beam (the railing stops against it). (2) Flash the line where the gable and the kitchen wing meet the terrace edge, over a small RCC upstand, so rain cannot run under the slab or into the kitchen ceiling. (3) Put a gutter on the main roof\'s front eave so monsoon run-off does not pour onto the front tiles. (4) Line the valley between the gable and the kitchen wing with a 12 in GI / aluminium valley gutter, draining east to its own downpipe', "Architect / contractor", "Open"),
    ("Option", "Duplex trial on the front 64 ft of the plot (house 53 ft), back 11 ft spare: decide between this and the single-storey 62 ft plan (main branch) before structural design", "Owner", "Open"),
    ("Finishes", "Colour and material scheme to choose: five looks to compare in the 3D model (As drawn, Classic Kerala refined, Chettinad ochre, Modern tropical, Lime and green); decide before ordering floor tiles, paint and door finishes", "Owner", "Open"),
    ("Land", "Front yard 8 ft: confirm the front setback allowed for this plot and road width before finalising; a two-storey house may need larger setbacks than a single storey", "Architect", "Open"),
    ("Structure", "Two-storey RCC frame: columns, footings and the first-floor slab sized for two floors; the stair well; RCC column stubs at the terrace edge for the steel posts that carry the roof over the terrace", "Structural engineer", "Open"),
    ("Layout", "TV on the stair wall of the living (west), sofa facing west about 6'-6\" away: confirm screen size (50 in) and a concealed HDMI/data conduit", "Owner", "Open"),
    ("Land", "Agricultural land: confirm conversion to non-agricultural use with the gram panchayat / collector (AP repealed the NALA Act in 2025; new process to be confirmed)", "Owner / surveyor", "Open"),
    ("Land", "Building permission route (panchayat vs DTCP / APCRDA via APDPMS) and setbacks under AP Building Rules 2017, including any height rule for two storeys", "Architect", "Open"),
    ("Soil", "Soil test (bore holes to 3 m min): black cotton soil is common in Guntur. Foundation type (isolated footings below active zone, under-reamed piles, or soil replacement) depends on it; two storeys raise the column loads", "Structural engineer", "Open"),
    ("Services", "Groundwater: test TDS, hardness, fluoride. Plan RO for drinking and a softener for bathrooms if hardness is high", "Plumber / owner", "Open"),
    ("Services", "Septic tank and soak pit in the spare rear land (percolation test for the soak pit size); if the back 11 ft is ever sold, move them or switch to a bio-digester with treated outflow", "Engineer", "Open"),
    ("Services", "Water tank: 1,000 L loft tank in the roof space over the upper bath, filled from the sump by pump, with a pressure pump for showers; confirm the truss carries it or put it on a steel platform off the slab", "Plumber / engineer", "Open"),
    ("Services", "Electrical load (with ACs), service connection size, earthing, inverter / solar PV", "Electrical engineer", "Open"),
    ("Vastu", "Master bedroom on the ground floor in the true south-west, bed head south, its new bath just east of it in the south band (x 28-36; ask the consultant), and a guest room / den in the north-west with the guest bath; Bedroom 2 above it (bed head south) and a study in the north-west (north light); kitchen in the south-east, stove on the east wall; pooja in the north-east corner of the living, opening west (family faces east); stair in the north-west quarter, now rising clockwise (mirrored); baths in the south band and the master bath north-west; main door on the east. Plot centre: on the 64 ft trial plot it falls in the living (kept free of walls and columns). Confirm which boundary the consultant uses, and whether the light well over the dining (south of the centre) is acceptable", "Vastu consultant", "To confirm"),
    ("Climate", "Covered terrace: deep shade from the main roof keeps the slab over the living cool; the first floor's west wall has only small high windows; chiks on the terrace's south and east sides", "Architect", "Open"),
    ("Roof", "Covered terrace roof: tiles on steel trusses (drawn, matches the rest of the roof) or a cheaper insulated metal-sheet roof on the same steel frame; decide before the roof is ordered", "Owner / architect", "Open"),
    ("Levels", "Survey road and field levels; plinth at 2 ft above finished ground (raise if site floods)", "Surveyor / architect", "Open"),
]

DUPLEX_DECISIONS = [
    "Noah review, small items (2 Nov 2026): the master vestibule deepened to 2'-6\" clear (bath wall on y 8.75) so its pocket door fits; the south-stack WCs set at y 7.2-8.4 (15 in from the shower glass, clear of the door jambs); door jambs moved at least 3 in off wall corners (D02, D07, D11, D33, D39, D42); south windows reduced to two families (2'-7\" room windows at a 3 ft sill, 2 ft bath and vent windows at 5 ft; the 6 ft kitchen window the one exception) and the west wall set on two axes symmetric about the hip apex (y 8.5: W01 under W36; y 19.5: the den's garden door under W41; W13 dropped), the ACs moved to solid wall beside them; the living's stair wall made one composed teak wall (jali, lamp niche and TV in one frame); under the stair a bench nook behind the jali and drawers under flight 1; the service door gets a landing and steps 1'-3\" deep along the wall so the walkway stays clear; the compound wall's road face in exposed brick or local stone.",
    "Noah review, remaining items (2 Nov 2026): a teak door with a jali panel closes the bedroom wing off the stair hall (D44); Kerala gablets with jali at both ends of the main hip let the hot roof air out; low chaipu roofs on the south and west walls (eaves +11'-1\", level with the front roofs) protect the ground-floor walls and windows, so those windows lose their hoods and the ground-floor north windows gain them; the kitchen east window becomes a high ventilator so the hob sits at y 8.6 with about 2 ft of landing each side, plus a high jali vent over the south window; the kitchen front is exposed local brick wrapped round the corner; the gable face is teak boarding with one 4 ft jali over the door; a jali screen closes the poomukham's north side; a 4 ft scooter gate by the two-wheeler bay; the back land becomes a garden court with the septic tank moved to its north-west corner (vastu) and a garden door from the den to a stone sit-out under the pergola. Laundry upstairs and closing the terrace's road side are left for the owner.",
    "Master option M2b chosen (2 Nov 2026): the west bay re-split on the y 14 line under the upstairs wall. Master bedroom 14 x 11 in the true south-west (bed head south between two windows stacked under Bedroom 2's) with its own vestibule and a new 8 x 6 bath on the south stack, back to back with the common bath; the north-west becomes a guest room / den with the old master bath as its guest bath, and a connecting door to the master, so it is the parents' sitting room most days and a guest suite when shut. The small room goes; one more bath (about Rs 1.2-1.8 lakh). The lobby cupboard shortened to 3'-4\" so the den door is clear.",
    "Seven-aspect review in the manner of Noah Daniel (2 Nov 2026, 01_Brief/Noah_Review_v2), suggested package applied with master option M1: common bath and Bedroom 2 bath re-planned in three bands (shower across the south end, WC mid-wall with 3'-6\" clear, basin opposite; doors open inward); terrace posts moved onto wall corners (x 53 / 61, y 3 / 12.5 / 25) with W07 moved clear; stair mirrored to rise clockwise; master zones swapped (bed in the true south-west under W14, 8 ft wardrobe on the y 14 line, TV / day bed zone in the north-west) and all AC units moved onto solid wall; poomukham north-edge pillars dropped so the swing clears; pooja moved to the living's north-east corner with a genkan shoe-off foyer (one step down) inside a 4 ft main door; entry axis set on y 18.75; dining nook folded into a linear utility and a 5 x 4'-6\" light well cut over the dining table; cross wall on y 11.5 on both floors; Bedroom 2 alcove made a vestibule with a linear closet and a pocket door to the bedroom; study re-furnished (one desk under the north window, library wall); terrace zoned (laundry SW, lounge NW, festival floor, planted east edge), terrace door 3'-6\"; stair-well chimney (clerestory W45, taller jali W10), living clerestory W47, genkan window W46, vents above doors; kitchen with a full-height corner unit and the fridge and pantry grouped at the north end. M2 (master suite with its own bath, NW guest room / den, no small room) was built as a separate study for comparison.",
    "Design review in the manner of Noah Daniel (2 Nov 2026, 01_Brief/Noah_Review_Duplex.md), all seven points applied: (1) upper toilet flipped: its door moved to the east end of the toilet lobby and opens inward, the basin moved to where the door was, so the WC is never the first view; (2) the front gable now spans the poomukham only and is centred on the main door, with a lower hipped wing (ridge about 2 ft lower) over the kitchen front and a valley gutter between them; (3) a prep sink under the kitchen window and a tall pantry beside the fridge, the SE counter corner a blind corner; (4) dining chairs moved to the table ends so no chair backs sit in the living path, the coffee table brought to 1'-6\" from the sofa and two armchairs added; (5) upper and lower windows stacked on the west and south walls (W36 over W01, W41 over W13, W02 under W35) and the Bedroom 2 wardrobe centred on the bed; (6) the terrace's north and south sides closed with teak jali parapets, the drying rails already on the south side away from the lounge; (7) a lit teak lamp shelf on the wall you face at the top of the stair.",
    "Duplex option (branch feature/duplex): the house is planned on the front 64 ft of the plot (the back 11 ft stays spare land) as a 53 ft x 22 ft two-level house, 1,166 sq ft on the ground floor and about 525 sq ft enclosed on the first floor plus a 19 x 22 ft covered terrace.",
    "House lengthened from 44 to 50 ft (after review: rooms felt small): 2 ft to the bedrooms (both now 14 ft wide), 3 ft to the bath strip (master, common and upper baths about 6 x 6'-5\" clear, dressing 6 ft wide, passage to the small bedroom 5'-6\"), 1 ft to the dining, living and wet area. Front yard unchanged at 8 ft; the trial plot grows from 55 to 61 ft.",
    "Then to 53 ft (rooms still felt tight on depth): the back half re-split so the master is 11'-6\" deep and the small bedroom 10'-6\" (about 13'-4\" x 10'-11\" and 13'-5\" x 9'-11\" clear); 2 ft added through the kitchen (about 13'-7\" x 9'-1\" clear, the living to 19 ft, the terrace to 19 ft); 1 ft added to the bath strip so all three baths are about 6'-5\" x 6'-4\" clear and the dressing 6'-6\". Trial plot now 64 ft, spare land 11 ft."
    "No double height (changed after review): a slab covers the whole two-storey block, so the living, dining, kitchen, pooja, store and wet area all have flat ceilings at about 9'-5\" and no dead space above the kitchen. Over the front half the first floor is a covered terrace, opening off the landing, with railings on three sides.",
    "Ground floor: master bedroom across the west bay (sleeping zone north-west next to its bath, sitting zone south-west), a small single-bed room off the lobby, the common bath beside the stair hall, dining by the kitchen hatch, living, kitchen and a dog-leg stair seen from the living through a timber jali. First floor: Bedroom 2 in the south-west with a wardrobe alcove and its bath, a closable study in the north-west, a toilet off the landing, a toilet off the landing, and the covered terrace.",
    "Roof: one hipped clay-tile roof over the two-storey block, carried on walls over the back rooms and on a light galvanised steel frame (posts and trusses) over the terrace, and a wide front gable (mukhappu) over the single-storey poomukham and kitchen front, so the house reads as a two-tier Kerala roof.",
    "No ridge ventilator (removed after review): with the terrace open on three sides, hot air under the main roof escapes at its open edges; the attic over the first-floor rooms is vented by meshed ridge and soffit vents.",
    "Review (2 Nov 2026): the store is folded into the dining as a nook with a 3 ft south window, so the dining has its own daylight (provisions go to the under-stair cupboard and a kitchen loft); a 3 ft window lights the end of the upper passage; a high south window above the ground master's bed head gives morning light and cross-breeze; the common bath door opens inward so it never blocks the lobby; the dresser is shortened clear of the upper bath door.",
    "Review (2 Nov 2026, no wasted space): the passage beside the stair becomes the small bedroom's entry with a wardrobe and an attached Bath 2 (6'-6\" x 7 ft, north window), entered straight from the lobby; the kitchen opens to the dining over a granite serving hatch with glazed sliding shutters, with its entry moved to a sliding door from the living, so the dining strip takes a 4-seat table and the nook a crockery unit.",
    "Review (2 Nov 2026, two baths on the ground floor): the north-west bedroom becomes the ground master (14 x 12'-6\", its own entry with a wardrobe and an attached bath); the south-west room becomes the second bedroom (14 x 9'-6\") and uses the common bath; the old master bath becomes its walk-in wardrobe and study alcove with a south window, entered from the lobby. Vastu: the upstairs south-west suite stays the main master; toilets now sit in the north-west and south only.",
    "Review (2 Nov 2026, dining and doors): the common bath moves west into the old walk-in alcove, so the old bath and the nook become a real dining room (11 x 7 ft with a 4 ft south window, open to the lobby and the serving side) with a 5 x 3 ft table; the second bedroom gets its own door from the lobby (bedroom split at 10'-6\" / 11'-6\"); the master bath door moves to its west wall, straight from the bedroom (beds now head south in both ground bedrooms); upstairs the bath moves over the common bath (one soil stack) and the old dressing becomes a study off the landing with a south window.",
    "Kitchen walls restored (2 Nov 2026): the kitchen's west wall (wet-area door, serving hatch) and north wall (sliding door to the living, solid on the poomukham side) had dropped out of the duplex model. With them back, the south counter now stops 2'-2\" short of the west wall and the utility sink moves west, so the wet-area door is clear on both sides.",
    "Roof-first phasing in three stages (2 Nov 2026): stage 1 (about Rs 30-34 lakh) is the ground floor with basic finishes under the full two-storey structure, roof and covered terrace, with upstairs an open, gated deck; stage 2 (Rs 7-11 lakh) adds the upstairs outer walls and windows, kitchen cabinets, wardrobes, ceilings and final finishes; stage 3 (Rs 7-10 lakh) fits out the first floor. Structure, waterproofing, the roof and buried services are never deferred (sheet A-002).",
    "Bedroom and study split (2 Nov 2026, from a fresh review): one huge room made the bedroom do three jobs and left two home workers with one corner desk. The west block now splits into Bedroom 2 in the south-west (bed head south between two 3 ft windows, an 8 ft sliding wardrobe on the north wall, entered through a wardrobe alcove so the bed is out of sight, its bath over the common bath) and a closable 14 x 11 study in the north-west (two desks 9 ft apart, sofa-cum-bed for guests, even north light, coolest room by day). The bath over the master bath becomes a toilet off the landing for the study, the terrace and guests. The terrace stays 19 x 22. Beams under the new walls at y 11.5 and y 14.",
    "Upper master opened up (2 Nov 2026): no dressing room and no inner walls. One open L-shaped room: sleeping zone north-west (king bed against the 6 ft divider wardrobe, wardrobe on the bath wall), sitting zone south-west (sofa under the south window, reading chair), a study corner in the south-east wing (desk on the east wall, window to the side, dresser by the window) and an entry zone off the top step with a 5 ft wardrobe screening the study. Only the bath and the landing toilet are walled.",
    "One room upstairs (2 Nov 2026): three bedrooms are enough (ground master, small room, one upstairs), so the first floor becomes a single upper master suite over the ground master: one 14 x 22 ft room with a sleeping zone north (king bed against a 6 ft divider wardrobe, as below) and a sitting/study zone south (desk under the south window, sofa, reading chair); a foyer straight off the top step with a linen cupboard; the bath over the master bath; the dressing with its south window. The old upstairs bath becomes a toilet off the landing for the terrace. The landing stays just the stair head (suite, toilet and terrace doors).",
    "No upstairs corridor (2 Nov 2026): the landing is just the stair head (7'-6\" x 5'-8\"). Both bedroom doors face east on its west wall: Bedroom 3's straight off the top step into its vestibule (6'-6\" x 5'), Bedroom 2's beside it into its own entry (6'-6\" x 3', open to the bedroom); the terrace door is opposite. The dressing gets a south window (wardrobes move to its north wall, dresser on the east wall), Bedroom 2 a high west window above the headboard for cross-ventilation, and the stair jali to the terrace gets glazed shutters and a grille. Bedroom 3's wardrobe moves from the vestibule to its east wall. The partition between the two doors sits on a beam over the lobby below",
    "Small room 10 x 9 (2 Nov 2026): the wall between the small room and the common bath moves 1 ft east on both floors, so the small room is 10 x 9 ft (a 4 ft bed and a 3 ft wardrobe) and the common bath 6 x 9 ft (WC and a 2'-10\" x 3'-3\" shower side by side at the south end, basin north). Upstairs the dressing grows to 10 x 7 and Bedroom 2's bath becomes 6 x 7, so the two WCs still share one stack.",
    "Bigger small room and common bath (2 Nov 2026): the space freed by the compact stair moved south: the lobby shifts 2 ft north and takes in the old dead-end vestibule (one 6'-6\" x 6' lobby with a coat and linen cupboard on its north wall), so the small room grows to 9 x 9 ft and the common bath to 7 x 9 ft (shower and WC south, basin north). The stair hall becomes a 3'-8\" passage from the dining to the lobby and stair. The first floor is unchanged (the bath stack still lines up).",
    "Compact stair (2 Nov 2026): 16 risers of 7.5 in (was 17 of about 7 in) and a 3'-6\" half landing (was 5'-8\"), keeping 3'-6\" flights: the stair shrinks from 7'-6\" x 11'-6\" to 7'-6\" x 9'-4\" and the freed 2'-2\" becomes a stair hall in front of it, open to the living; upstairs the landing gains the same strip.",
    "Suites arranged to suit the space (2 Nov 2026): the master sleeps in its north half next to its bath, with the king bed against the back of the divider wardrobe (head south) and the north window ahead; the sitting zone (day bed, sofa, TV) moves to the south half; the small room drops the desk and has its wardrobe on the east wall, with its door moved west.",
    "Small room widened (2 Nov 2026): 2 ft taken from the master's sleeping zone, so the small room is 9 x 7 ft (about 8'-5\" x 6'-5\" clear) with a single bed, a 4 ft wardrobe and a desk; the master keeps its king bed (centred, the west wardrobe dropped; the 6 ft divider wardrobe stays). Upstairs the dressing room grows to match (8'-3\" of wardrobes).",
    "Bath swap (2 Nov 2026): the common bath moves to the old dining spot beside the stair hall (7 x 7 ft); the old master bath becomes a small room with a single bed off the lobby; the north bath becomes the master bath, entered from the sitting zone; the dining goes back to the serving side by the kitchen hatch with the nook. Upstairs, Bedroom 2 gets a dressing room over the small room and its bath moves over the common bath (wet over wet); the study goes.",
    "Ground master (2 Nov 2026): the master moves downstairs and takes the full depth of the west bay, 14 x 22 ft: a sleeping zone in the south-west with its attached bath and a sitting zone in the north-west (day bed, sofa, TV), part-divided by a 6 ft wardrobe. Upstairs become Bedroom 2 (south-west, with its bath) and Bedroom 3 (north-west, with its own vestibule and bath).",
    "Clean redesign (option B, 2 Nov 2026): one bedroom downstairs (south-west, for elders or guests, with its attached bath) and a family room in the north-west behind a small vestibule with the common bath; two bedrooms upstairs (the south-west master with its bath, and Bedroom 2 in the north-west with its own vestibule and bath), the study and the 19 x 22 ft terrace kept. Walls line up on both floors and every bath sits over another (two soil stacks).",
    "All four bath fittings stack in the south band (two baths over two); the septic tank and soak pit move to the spare rear land behind the baths, freeing the front yard; the water tank goes into the roof space (no tank stand).",
]

_HISTORY = [
    "Site is in Guntur, Andhra Pradesh (farm land), not Kerala; Kerala style kept, construction adapted to local climate and soil.",
    "Plot 27 ft x 75 ft (5 ft longer than first assumed; confirm by survey), road on east; house 62 ft x 22 ft (lengthened 2 ft for Bedroom 2) with an 8 ft front yard and 5 ft rear garden; owner accepts local practice on side setbacks (to be checked).",
    "RCC frame with AAC block walls: 9 in outer, 5 in inner, 7 in where plumbing is concealed.",
    "Plinth 2 ft above finished ground; poomukham 6 in lower; bathrooms 12 mm lower with no raised threshold.",
    "AC provisions (points, sleeves, drain, outdoor-unit brackets) in both bedrooms, the office and living; passive cooling first.",
    "Flat insulated false ceilings in bedrooms, offices, baths and kitchen; sloped ceilings in living, dining and verandah.",
    "No glass skylight: the dining gets borrowed daylight from the living, the nook window and the hall; a louvred ventilator lantern above it lets hot air out (no glass, so no greenhouse heat).",
    "Courtyard removed; the dining hall at plot centre keeps the Brahmasthan open, with the ventilator above.",
    "Single storey, no internal stair; roof access by fixed ladder; water tank on stand in SW rear garden.",
    "Service band on south (heat buffer); bedrooms and living get north light.",
    "Kitchen in SE; stove on east wall; open wet area onto the walkway; provisions in bench drawers, kitchen cabinets and lofts (no separate store).",
    "Bedroom doors widened to 3 ft; bathroom, office and store doors 2 ft 6 in.",
    "Thirty-second review: TV back on the west wall of the hall (Bedroom 2's east wall), sofa facing west about 7'-6\" away in the dining bay, coffee table between, the window seat shortened to 4 ft as side seating; the dining space under the ventilator is open again.",
    "Thirty-first review (front facade): gate re-centred on the main door with a 6 ft stone forecourt and the tulsi thara on the axis (gate, tulsi, steps, door, hall, lamp niche in one line); charupadi seats with sloping backrests between the verandah pillars, flanking the steps; carved teak barge boards and a brass kalasham finial on the front gable; the kitchen front clad in exposed laterite with a deep projecting teak frame to its window; carved teak main door with brass studs, a stone surround and a nameplate niche; warm uplights at the pillars, a lantern by the door and gate-post lights; low hedges screening the sump and the two-wheeler bay; a pair of potted palms beside the steps.",
    "Thirtieth review (proportion clean-up): windows standardised to three sizes (6 ft rooms, 3 ft small, 2 ft baths) with every head at 7 ft and three sill levels (3 ft rooms, 3'-6\" over counters, 5 ft baths); sunshades only on the sunny south, east and west walls (the eaves shade the north); floors cut to three families plus the verandah (red oxide in all public rooms and the pooja, vitrified in bedrooms, anti-skid ceramic in kitchen, baths and wet area, granite on the verandah); services hidden (pipes in chases, outdoor units grouped behind jali on the north wall), switchboards aligned, warm layered lighting, handle-less built-in fronts.",
    "Twenty-ninth review: compound wall made as thin as practical: precast RCC post-and-panel (2 in panels in 4 in posts) set just inside the plot line, so the side strips stay walkable and the north run can be lifted and moved if more land is bought.",
    "Twenty-eighth review: TV lounge reworked: sofa brought forward to about 8 ft from the TV, a 3 ft walk behind it, and a built-in window seat (charupadi-style enclave) under the dining-bay window, so the sofa backs onto a quiet seating nook rather than the entrance and nobody walks in front of the TV.",
    "Twenty-seventh review: TV lounge moves to the open dining space under the ventilator: TV on the north face of the common-bath wall, sofa facing south with its back to the north window, so the main door is in side view, not behind (commanding position) and the TV no longer faces the main door; the dining bay becomes a reading / dining nook with a chair by the window.",
    "Twenty-sixth review: built-in ideas borrowed and adapted (function, not style, in Kerala materials): recessed shower niches, mirror cabinets over basins, genkan-style shoe bench with hooks and a granite threshold band, vilakku madam lamp niche facing the main door, floating bedside shelves (walls too thin for recesses), drawers-first kitchen with a masala pull-out and utensil rail, dish-drying rack over the utility sink, ceiling clothes airer in the wet area.",
    "Twenty-fifth review: main door moved 3'-4\" south (y 17'-7\" to 20'-7\"), centred under the front gable and opening straight onto the 5 ft walk between the pooja and the diwan; shoe cupboard to its north on the east wall; window diwan back to 6 ft along the north window, out of the door's line; steps, middle verandah pillars and the swing realigned.",
    "Twenty-fourth review: planned on the 27 ft plot alone (north strip dropped for now): roof eaves cut from 2'-6\" to 2'-0\" so the north eave stays inside the plot line, septic tank moved under the two-wheeler bay in the front yard with a lined soak pit beside it, all drains rerouted along the south walkway to the front, rainwater to the sump with overflow to the road; north-strip trees and recharge pit removed.",
    "Twenty-third review: the fridge moves out of the kitchen into the dining alcove beside the kitchen door, against the wet-area wall; the kitchen's north wall is now free.",
    "Twenty-second review: the kitchen's tall pantry and the dining table and chairs are removed at the owner's request; the dining space under the ventilator stays open (the pendant light and points stay for a table later).",
    "Twenty-first review: the open hall becomes three zones: family TV lounge in the dining bay (5'-6\" sofa facing the TV), dining under the ventilator moved 9 in south (about 2 ft behind the chairs on both sides), and guest sitting by the main door with a 4'-6\" window diwan (shortened after the walk-through showed a 1'-6\" pinch at the shoe cupboard) and an armchair under the living's north window; a clear walk of about 4'-11\" from the main door to the dining and kitchen, pooja front kept clear.",
    "Twentieth review: Bedroom 2's bed moves to the east wall, head east, leaving an 8 x 14 ft open floor from the door to the bath and window; wardrobe to the west wall (sound buffer to the master), work table north of the bed, AC on the bath's outer wall; dresser dropped (mirror on the wardrobe).",
    "Nineteenth review: with Bedroom 2 at 17 ft, its bed turns head-south in the middle of the room (2 ft+ on both sides, under the jali); Bath 2 grows to 7' x 7' (6'-7\" x 6'-4\" clear) with a 3' x 3'-6\" wet zone, basin in the dry zone and the door on its east wall; a dresser takes the west wall; work table and wardrobe stay on the east wall.",
    "Eighteenth review: house lengthened 2 ft to 62 ft, all of it added to Bedroom 2 (now 17 ft wide; the sitting area below it also gains 2 ft); front yard 10 ft to 8 ft (check the front setback). Bedroom 2 window back to 6 ft.",
    "Seventeenth review: sitting area gets a 5 ft tall storage cupboard on the south wall between the bench and the window; the hand-wash basin moves to the east end of the serving counter, just outside the common bath, for washing up after meals.",
    "Sixteenth review (independent Indian-architect review): Bath 2 re-planned 7' x 6' so Bedroom 2's bed (head west) has 1'-6\" on both sides, work table to the east wall. Kitchen entered only from the dining-side door (hinged, 3 ft); the north sliding door is walled up so the pooja front is quiet, and a tall pantry takes the north wall. East kitchen window cut to 2 ft so the hob and chimney sit on solid wall. Septic tank moved 6 ft+ from the house and the soak pit replaced by a soak trench. Ensuite door opens outward; common bath WC side clearance 17 in, door rehung at the north jamb with a closer, geyser and shower off the window. DB moved to the dining face of Bedroom 2's east wall.",
    "Fifteenth review: TV moves to Bedroom 2's east wall facing the dining bay (the bay becomes the TV lounge; sofa faces west, living AC above the TV). Master bed moves 3'-10\" south toward the bay, freeing a 9 x 7 ft zone by the north window and ensuite door with a window seat. Bedroom 2's door moves to the east end of its south wall. Bath 2's door moves to its east wall (basin to its south wall) so Bedroom 2's bed sits in the strip between the bath and the sitting area, head west on the master wall, leaving the middle of the room open.",
    "Fourteenth review (designer review): Bath 2 moves into Bedroom 2's own north-west corner, made 5'-6\" x 7'-6\" (about 5'-0\" x 6'-11\" clear) for a 3' x 3'-6\" wet zone and a WC with 15 in each side and the master gets back its full room, bed position and 6 ft window. Bath doors open outward (common bath door moved to the sitting-area side, off the dining). Pooja moves 3'-6\" south, back to back with the kitchen, with doors opening inward; the fridge moves into the kitchen; a shoe cupboard takes the freed wall beside the main door. Second kitchen door (sliding) straight to the dining. Bedroom 2's south-east corner is notched 1' x 1'-6\" so the way from the dining into the sitting area is about 4'-2\" instead of 3'-3\"; Bedroom 2 gets a real queen bed, a 6 ft window and a high jali vent to the sitting area. Handrail at the entrance steps, grab bars in the baths.",
    "Common bath widened to 6'-6\" x 6' (about 6'-0\" x 5'-5\" clear: 3 x 3 ft shower, WC and basin on the wet wall) by taking 1'-6\" from the east end of the sitting area; serving counter now 6 ft.",
    "Twelfth review: Bath 2 becomes a common bath in the old pooja bay beside the wet area (5 x 6 ft, door from the sitting area, WC and basin on the shared wet wall, drains straight to the south walkway); Bedroom 2 is a clean room with no attached bath; wet area narrowed to 5 ft. Hall kept on the south so bedrooms keep their north windows.",
    "Eleventh review: the corner between the pooja and the kitchen becomes part of the kitchen and holds the fridge; the kitchen entrance moves from the dining side to the north (3 ft sliding glass door from the living); the old fridge spot extends the south counter.",
    "Tenth review: main door moved to the north end of the east wall and the pooja 3'-6\" north with it, freeing the living's south-east corner beside the kitchen; verandah steps, pillars and swing realigned to the door; TV taken off the east wall (new position open).",
    "Ninth review: pooja moved to the east side, in the living's south-east corner beside the main door and back to back with the kitchen (4 x 4 ft, opens west, idols face west, family faces east). Main door moved 2'-4\" north and the TV unit trimmed to suit; the old pooja bay joins the sitting area.",
    "Eighth review: plot 5 ft longer, so the house grows to 60 ft. The master stays 9'-6\" x 14' (bay 7 x 8 ft, full-width wardrobe, light from the workstation window; the bay's own south window dropped). Bedroom 2 grows to 15 ft wide, the sitting area to 20 x 7'-6\" (Bedroom 2 gives up 1'-6\" of depth, now 15 x 14'-6\") and the dining to 11 ft; the plot centre now falls in the dining, west of the ventilator (Vastu to confirm).",
    "Seventh review: Bedroom 2 enlarged to 12 x 16 ft by taking the hall strip; its door opens from the sitting area (as the master suite does); hand-wash basin back at the west end of the serving counter.",
    "Sixth review: Office 2 walls and sliding door left out for now (open workstation in the master suite, walls can be added later); Bedroom 2 becomes a study-guest room: work table with monitor beside the bath, sofa-cum-bed instead of a queen bed.",
    "Office 1 removed after family review: one office (Office 2) inside the master suite; Bedroom 2 has its own work desk.",
    "Common bathroom moved to the north side (old pooja spot), entered from the dining corner next to the hall.",
    "Second family review: store (8 x 8 ft) moved next to the bedrooms; pooja reduced to a small shrine opening onto the hall (idols face east); wet area moved west (9 x 8 ft); kitchen 14 x 10 ft with a 5 ft sliding entry from the living; dining gains a basin and crockery nook with a south window; TV moved to the living room's east wall.",
    "Pooja moved beside the wet area and opened to the west (idols face west, the family sits in the nook facing east); shared wall kept dry with no pipes, pooja floor 3 in higher; basin nook shifted west.",
    "Fifth review: Bedroom 2 made one 12 x 12 ft rectangle with a rectangular private bath (north-west corner, outer wall) and its wardrobe on the east wall; the leftover corner at the hall's west end is an open hand-wash corner; serving counter now 9 ft without a basin.",
    "Fourth review: Bath 2 made Bedroom 2's private bath (no common toilet); master suite entered through its bay from the sitting area; the old Bath 2 spot opens to the dining with a north window; family store merged back into the master bedroom as a wardrobe bay; inverter under the sitting-area bench.",
    "Earlier: walk-in wardrobe turned into a family store with a lockable door from the sitting area (inverter inside); built-in sliding wardrobes in the dressing alcove and on the master bedroom's south wall.",
    "Store wall removed: the strip from the walk-in to the pooja is one open sitting and serving area with a storage bench; hand-wash basin set into the west end of the serving counter, about 8 ft from the pooja, draining straight out to the south walkway.",
    "Wet area reduced to 6 x 6 ft and left open on its south side to the walkway (service route from the kitchen to the back of the house); kitchen door moved to face the dining (3 ft sliding glass); basin nook widened to 8 ft with a 6 ft serving counter.",
    "Main door moved to the south part of the living's east wall (still north of the house's centre line); TV on the north part of that wall; steps, swing and arugu seats rearranged on the poomukham.",
    "Third review: hall widened to about 6 ft clear (store, pooja and basin nook made 6 ft deep) so the family can sit facing the pooja; store left open to the hall for now (a wall and door can be added later); broom closet dropped, tall utility cupboard in the wet area instead.",
    "Earlier: hall widened to 4 ft clear (Bedroom 2 gives up 6 in); vents above the office, walk-in, store, pooja and kitchen doors; none at bedrooms or bathrooms (sound privacy).",
    "Ensuite widened by 1'-6\" into the master (about 6'-0\" x 7'-4\" clear); dressing widened by the same strip; master now 9'-6\" x 14'-0\".",
    "Roof: Mangalore clay tiles on steel truss over insulated cement-fibre deck; all edge tiles mechanically fixed.",
]

# Specification: category, element, specification, reason (Guntur-specific where relevant)
DECISIONS = DUPLEX_DECISIONS + [d for d in _HISTORY if not d.startswith(("Plot 27 ft", "Single storey", "Courtyard removed"))]

SPEC = [
    ("Substructure", "Soil investigation", "Min. 2 bore holes to 3 m or refusal; swell test, SBC", "Black cotton soil swells when wet and shrinks when dry"),
    ("Substructure", "Foundations", "As per engineer: footings below the active zone (often 1.5-2.5 m) or under-reamed piles; 300 mm sand/moorum cushion", "Prevents seasonal heave cracking"),
    ("Site", "Compound wall", "Precast RCC post-and-panel wall, 5 ft high: 4 in square posts at about 7 ft centres on small pad footings, 2 in slotted panels, set just inside the plot line; panels lift out, so the north run can be moved if the north strip is bought", "Thinnest practical wall: keeps the 2 ft north gap and 3 ft south walkway usable; cheap, quick and reusable"),
    ("Substructure", "Plinth beam + DPC", "RCC plinth beam all round; 40 mm DPC with waterproofing compound at plinth top", "Stops rising damp into AAC"),
    ("Substructure", "Plinth fill", "Non-expansive moorum / gravel in 150 mm layers, compacted; no black soil fill", "Black soil under the floor will heave the slab"),
    ("Substructure", "Anti-termite", "Pre-construction chemical treatment (IS 6313) at foundation, plinth fill and around walls", "High termite risk; cannot be redone easily later"),
    ("Substructure", "Plinth protection", "3 ft PCC apron with slope away, joint sealed to wall", "Keeps rain off expansive soil next to foundations"),
    ("Frame", "Columns, beams, bands", "RCC frame; lintel band at door head, ring beam at wall top; seismic zone III detailing (IS 13920 as engineer decides)", "AAC infill is not load-bearing for truss + cyclone loads"),
    ("Frame", "First-floor slab and stair", "RCC slab over the whole two-storey block (about 5 in, by engineer) with drop beams at the stair well and an edge beam round the terrace; dog-leg RCC stair, 16 risers of 7.5 in, 10 in treads, waist slab by engineer; columns run full height for two floors", "Two storeys: the slab carries the upper master, bath, lounge and terrace"),
    ("Frame", "Covered terrace roof frame", "Hot-dip galvanised steel posts (about 100 x 100 mm SHS) on RCC column stubs at the slab edge, bolted base plates with grout; steel trusses and purlins carry the same clay-tile roof as the rest of the house; all steel primed and painted, bolted connections", "A light frame instead of walls keeps the terrace open; galvanising resists the humid, salty coastal air"),
    ("Walls", "AAC blocks", "IS 2185-3, 200 mm outer / 150 mm wet walls / 100 mm inner; thin-bed polymer mortar", "Better insulation than brick; lighter frame"),
    ("Walls", "AAC to RCC joints", "Galvanised mesh strip 150 mm wide over every block-concrete joint before plaster", "The most common AAC crack; cheap to prevent"),
    ("Walls", "Chasing", "Cut chases with a groover, never hammer; fill with polymer mortar + mesh", "Hammering cracks AAC blocks"),
    ("Walls", "External plaster", "20 mm, two coats, waterproof admixture, cured 7 days; elastomeric paint", "Wind-driven cyclone rain"),
    ("Roof", "Structure", "Steel truss (hot-dip galvanised or epoxy primed), 30 deg pitch, bolted to ring beam with holding-down bolts", "Uplift in cyclone winds"),
    ("Roof", "Deck and insulation", "Cement-fibre board deck + 50 mm PIR/XPS or reflective insulation + membrane, then battens and Mangalore tiles", "Cuts attic heat in 45 C summers"),
    ("Roof", "Tile fixing", "Clip or screw every tile at eaves, verges, ridges and hips, and every 3rd row elsewhere; ridges bedded and pointed", "Loose tiles fly in cyclones"),
    ("Roof", "Ventilation", "Ridge / gable vents with bird and insect mesh; soffit vents at eaves", "Flushes hot air from the attic"),
    ("Roof", "Gutters and downpipes", "150 mm half-round gutters with leaf guard on the main and front roofs, 100 mm downpipes at 6 points, to the sump filter, overflow to the road drain", "Short heavy bursts; protects the plinth"),
    ("Openings", "Windows", "Hardwood or UPVC frames; mosquito mesh on every opening; MS grill for security", "Mosquitoes; ground-floor security"),
    ("Openings", "Sills and sunshades", "External sills sloped 1:10 with drip groove; 2 ft sunshades with drip groove; 18 in projecting drip under the jali wall", "Stops staining and water entry"),
    ("Openings", "Vents above inner doors", "Pooja: open jali; bedrooms and bathrooms: none (the workstation has no door for now). 7'-6\" to 9'-0\" above the lintel band", "Air moves with doors shut where privacy allows; bedrooms rely on their north windows, fans and AC"),
    ("Openings", "Bathroom doors", "WPC / FRP shutters on WPC or granite frame base; no wooden frame touching the wet floor", "Wood frames rot at the bottom"),
    ("Floors", "General", "4 in skirting flush with the wall plaster (groove in plaster); 3 mm epoxy grout in wet areas", "No dust ledge, no black grout lines"),
    ("Floors", "Wet rooms", "Waterproofing (polymer cementitious) floor + 12 in up walls + 7 ft in shower; flood test 48 h before tiling", "Leak into neighbouring rooms is the top complaint"),
    ("Plumbing", "Supply", "CPVC hot/cold; supply runs along external walls in clamps or shallow chases; isolation valve per bathroom and kitchen", "Easy repair without breaking tiles"),
    ("Plumbing", "Drainage", "uPVC SWR 110 mm soil, 75 mm waste; inspection chamber at every bend and junction; separate soil and grey-water lines", "Easy rodding"),
    ("Plumbing", "Water treatment", "RO for drinking at kitchen; whole-house softener if hardness > 300 mg/l; matt fittings", "Guntur groundwater is often hard with high fluoride"),
    ("Electrical", "Wiring", "FR-LSH copper; 1.5 sq mm lights, 2.5 sq mm sockets, 4 sq mm AC / geyser; separate circuits per AC", "AC loads"),
    ("Electrical", "Protection", "RCCB 30 mA + MCBs; 2 earth pits; surge protection device; DB in an accessible spot", "Shock and lightning safety"),
    ("Electrical", "Backup", "Inverter circuit to lights, fans, study sockets and router; conduit from roof to DB for future solar PV", "Power cuts during work-from-home"),
    ("Electrical", "AC provisions", "16 A socket at 7 ft, 65 mm sleeve through wall, drain pipe to outside, ODU brackets on shaded walls", "Retrofitting later means breaking walls"),
]

# Electrical points: code, x, y, room, note. Heights above FFL are set per code in ELEC_TYPES.
ELEC_TYPES = {  # code: (description, mounting height)
    "L": ("Ceiling light", "ceiling"), "WL": ("Wall light / mirror light", "6'-6\""), "F": ("Ceiling fan point", "ceiling"),
    "EF": ("Exhaust fan", "7'-0\""), "CH": ("Kitchen chimney point (16 A)", "7'-0\""), "S": ("Switchboard", "4'-0\""),
    "P": ("6 A socket", "1'-0\""), "PC": ("6 A socket at counter", "3'-6\""), "P16": ("16 A power socket", "varies"),
    "U": ("Inverter (UPS) socket", "1'-0\""), "D": ("Data point (Cat6)", "1'-0\""), "TV": ("TV + data point", "3'-6\""),
    "AC": ("AC indoor unit (16 A socket, sleeve, drain)", "7'-6\""), "ODU": ("AC outdoor unit bracket", "7'-0\" outside"),
    "G": ("Geyser (16 A)", "6'-6\""), "DB": ("Distribution board", "5'-0\" to top"), "INV": ("Inverter + battery", "floor"),
    "MTR": ("Meter at gate", "5'-0\""), "EP": ("Earth pit", "ground"), "BELL": ("Bell push", "4'-6\""), "CAM": ("CCTV point", "8'-0\""),
    "GL": ("Outdoor / gate light", "7'-0\""),
}
ELECTRICAL = [
    # Master bedroom (ground, south-west)
    ("F", 21.0, 7.0, "R01", ""), ("L", 16.0, 11.0, "R01", ""), ("L", 26.0, 7.5, "R01", ""),
    ("S", 27.6, 8.8, "R01", "at the vestibule door, 2-way"), ("S", 25.2, 3.4, "R01", "bedside, 2-way"), ("S", 27.4, 13.6, "R01", "by the connecting door"),
    ("P", 17.4, 3.4, "R01", "bedside"), ("P", 24.6, 3.4, "R01", "bedside"),
    ("AC", 14.4, 11.5, "R01", "west wall, on solid wall north of W01, throws east across the bed foot"), ("ODU", 13.6, 11.5, "R01", "west wall, under the eave and pergola"),
    # Master bath and vestibule
    ("L", 32.0, 6.0, "R40", ""), ("EF", 30.0, 3.4, "R40", "out through the south wall"), ("G", 28.4, 6.0, "R40", "over the shower"), ("PC", 34.0, 3.5, "R40", "by basin"),
    ("L", 31.25, 10.25, "R41", ""), ("S", 29.0, 11.1, "R41", "at the door; bath switches beside it"),
    # Master bath
    # Common bath
    ("L", 39.0, 8.5, "R08", ""), ("EF", 37.5, 3.4, "R08", "out through the south wall"), ("G", 41.6, 4.5, "R08", "over shower, east wall"),
    ("PC", 41.6, 9.1, "R08", "by basin"), ("S", 38.8, 11.8, "R09", "common bath switches outside the door"), ("L", 31.5, 14.0, "R05", ""),
    # Master bedroom (north-west)
    ("F", 21.0, 19.5, "R42", ""), ("L", 17.0, 22.0, "R42", ""), ("L", 25.5, 23.0, "R42", ""),
    ("S", 27.6, 17.3, "R42", "at the door"), ("S", 27.6, 21.3, "R42", "guest bath switches outside the door"), ("TV", 21.0, 14.4, "R42", "TV and data"),
    ("P", 19.0, 24.6, "R42", "reading light by the sofa-bed"), ("S", 25.0, 14.4, "R42", "by the connecting door"),
    ("AC", 14.4, 16.25, "R42", "west wall, on solid wall south of the garden door"), ("ODU", 13.6, 16.25, "R42", "west wall, under the eave (one stacked column with the study unit)"),
    # Lobby, stair, under-stair cupboard
    ("L", 38.5, 13.8, "R09", ""), ("S", 41.6, 13.6, "R09", "lobby and stair, 2-way with the landing"),
    ("DB", 40.0, 18.7, "R06", "in the under-stair cupboard, facing the stair hall (central, dry)"), ("U", 39.0, 18.7, "R06", "router (central)"),
    ("INV", 41.0, 19.6, "R06", "lithium inverter in the ventilated under-stair cupboard"),
    ("WL", 38.25, 24.6, "R06", "at the half landing"),
    ("L", 31.2, 21.5, "R07", ""), ("EF", 33.4, 24.7, "R07", "out through the north wall"), ("G", 34.2, 24.0, "R07", "over shower, east wall"),
    ("PC", 33.6, 18.4, "R07", "by basin"),
    # Store, wet area, dining
    ("L", 44.0, 5.0, "R13", "over the crockery unit"),
    ("L", 50.0, 5.0, "R13", ""), ("P16", 45.3, 7.2, "R13", "washing machine"), ("P", 52.4, 3.4, "R13", "utility, weatherproof"),
    ("L", 47.25, 10.2, "R10", "pendant over the table, centred on it, hung below the light well"), ("S", 42.4, 9.4, "R10", "dining and wet area"),
    # Kitchen
    ("L", 60.0, 8.0, "R15", ""), ("WL", 62.5, 3.5, "R15", "under-cabinet, on solid wall beside the window"), ("WL", 66.5, 10.6, "R15", "under-cabinet"),
    ("CH", 66.6, 8.6, "R15", "3 ft chimney on solid wall, duct out through the east wall"), ("PC", 55.9, 3.5, "R15", ""),
    ("PC", 61.0, 3.5, "R15", "OTG"), ("PC", 63.8, 3.5, "R15", "mixer"), ("PC", 66.6, 5.8, "R15", ""), ("PC", 66.6, 10.5, "R15", ""),
    ("PC", 59.2, 3.5, "R15", "RO purifier, by sink"), ("P16", 61.25, 12.1, "R15", "refrigerator"), ("P", 63.5, 12.1, "R15", "microwave inside the pantry unit"), ("S", 56.4, 12.3, "R15", "beside the sliding entry"),
    # Pooja
    ("L", 59.0, 23.0, "R11", ""), ("WL", 60.4, 23.0, "R11", "lamp niche above the idols"), ("P", 57.4, 24.6, "R11", ""),
    ("S", 56.6, 21.3, "R16", "pooja switches outside, living side"),
    ("L", 59.0, 17.0, "R18", ""), ("S", 60.6, 16.3, "R18", "main switch at the door"),
    # Living
    ("F", 50.0, 18.0, "R16", ""), ("L", 46.5, 22.0, "R16", "pendant"), ("L", 54.5, 16.0, "R16", "pendant"),
    ("WL", 42.4, 18.75, "R16", "inside the lamp niche"), ("TV", 42.4, 22.4, "R16", "TV wall: 2 sockets + data + HDMI conduit to the unit"),
    ("P", 42.4, 21.0, "R16", "TV unit"), ("P", 53.4, 19.4, "R16", "floor socket, sofa end"), ("P", 44.6, 17.6, "R16", "lamp socket by the armchairs"),
    # Poomukham
    ("L", 64, 15.0, "R17", ""), ("L", 64, 21.0, "R17", ""), ("BELL", 61.4, 21.2, "R17", ""), ("CAM", 66.5, 24.6, "R17", "covers gate and door"),
    ("P", 61.4, 24.0, "R17", "outdoor, weatherproof"), ("S", 61.4, 21.5, "R17", ""),
    ("GL", 66.4, 16.05, "R17", "uplight at the pillar base"), ("GL", 66.4, 21.45, "R17", "uplight at the pillar base"), ("WL", 61.4, 16.3, "R17", "warm lantern beside the main door"),
    # Site
    ("MTR", 74.6, 23.2, "SITE", "meter in compound wall by gate"), ("GL", 74.7, 14.95, "SITE", "gate post light"), ("GL", 74.7, 22.55, "SITE", "gate post light"),
    ("EP", 68.2, 1.5, "SITE", "earth pit 1"), ("EP", 73.5, 1.5, "SITE", "earth pit 2"), ("GL", 10.0, 8.0, "SITE", "spare land / kitchen garden"),
]
ELECTRICAL_F1 = [
    # Bedroom 2 (south-west) and its alcove
    ("F", 21.0, 8.0, "R31", ""), ("L", 16.0, 11.0, "R31", ""), ("L", 26.0, 7.5, "R31", ""),
    ("P", 17.4, 3.4, "R31", "bedside"), ("P", 24.6, 3.4, "R31", "bedside"), ("S", 25.2, 3.4, "R31", "bedside, 2-way"),
    ("S", 32.3, 11.2, "R32", "at the door, latch side, 2-way"), ("L", 31.5, 7.5, "R32", ""), ("P", 35.6, 7.0, "R32", "dresser"),
    ("AC", 14.4, 11.5, "R31", "west wall, on solid wall north of W36, throws east across the bed foot; 1 ton"), ("ODU", 13.6, 11.5, "R31", "west wall, under the eave"),
    # Bedroom 2 bath
    ("L", 39.0, 8.5, "R33", ""), ("EF", 37.5, 3.4, "R33", "out through the south wall"), ("G", 41.4, 4.5, "R33", "over shower, east wall"),
    ("PC", 41.4, 9.1, "R33", "by basin"), ("S", 35.6, 9.4, "R32", "bath switches outside the door"),
    # Study (north-west)
    ("F", 21.0, 19.5, "R36", ""), ("L", 16.5, 23.0, "R36", ""), ("L", 25.5, 16.0, "R36", ""), ("S", 27.6, 17.5, "R36", "at the door"),
    ("P", 17.5, 24.6, "R36", "desk 1"), ("U", 18.5, 24.6, "R36", "desk 1"), ("D", 19.5, 24.6, "R36", "desk 1"),
    ("P", 22.5, 24.6, "R36", "desk 2"), ("U", 23.5, 24.6, "R36", "desk 2"), ("D", 24.5, 24.6, "R36", "desk 2"), ("P", 25.8, 14.4, "R36", "sofa-cum-bed"),
    ("AC", 14.4, 16.25, "R36", "west wall, on solid wall south of W41, 1 ton"), ("ODU", 13.6, 16.25, "R36", "west wall, under the eave (stacked over the master unit)"),
    # Upper toilet and landing
    ("L", 31.2, 21.5, "R39", ""), ("EF", 33.4, 24.7, "R39", "out through the north wall"), ("G", 34.2, 24.0, "R39", "over shower, east wall"), ("PC", 30.4, 18.4, "R39", "by basin"),
    ("S", 31.4, 17.8, "R38", "toilet switches outside the door, beside it"), ("L", 31.2, 16.8, "R38", ""),
    ("L", 37.0, 13.5, "R34", ""), ("WL", 40.25, 11.8, "R34", "picture light over the lamp shelf facing the stair top"), ("S", 34.8, 11.8, "R34", "landing and stair, 2-way with the lobby"),
    ("F", 48.0, 19.0, "R37", "wet-rated, hung from the steel truss"), ("L", 53.5, 10.0, "R37", "wet-rated"), ("L", 56.0, 9.0, "R37", "wet-rated"),
    ("L", 56.0, 21.0, "R37", "wet-rated"), ("P", 42.4, 15.2, "R37", "weatherproof"), ("P", 42.4, 5.0, "R37", "weatherproof"),
    ("S", 41.6, 11.9, "R34", "terrace switches by the door, landing side"),
]

# Plumbing points: code, x, y, room, note
PLUMB_TYPES = {
    "WC": "Wall-hung WC, concealed cistern", "HF": "Health faucet", "BS": "Wash basin", "SH": "Shower mixer (hot + cold)",
    "FT": "Floor trap / linear drain", "SK": "Sink", "WM": "Washing-machine inlet + drain", "RO": "RO purifier point",
    "TAP": "Tap", "GY": "Geyser connection", "IC": "Inspection chamber", "GT": "Grease trap", "DP": "Rain downpipe",
}
PLUMBING = [
    ("WC", 37.1, 7.8, "R08", "on the west wall, mid-room, under the upper WC"), ("HF", 36.4, 8.6, "R08", ""), ("BS", 41.6, 7.9, "R08", "east wall, opposite the WC"),
    ("SH", 41.6, 4.9, "R08", "east wall"), ("FT", 39.0, 4.5, "R08", "shower drain, across the south band"), ("FT", 39.5, 9.6, "R08", "dry zone trap"),
    ("WC", 35.2, 7.8, "R40", "on the x 36 wet wall, back to back with the common WC (one stack)"), ("HF", 35.8, 8.5, "R40", ""), ("BS", 33.05, 3.5, "R40", "under the window"),
    ("SH", 28.4, 4.9, "R40", "on the bedroom wet wall"), ("FT", 29.7, 4.9, "R40", "shower drain"), ("FT", 33.0, 7.0, "R40", "dry zone trap"),
    ("WC", 29.1, 21.6, "R07", "on the den wall"), ("HF", 28.4, 22.4, "R07", ""), ("BS", 33.0, 18.4, "R07", ""),
    ("SH", 34.2, 23.4, "R07", "east wall"), ("FT", 32.8, 24.4, "R07", "shower drain"), ("FT", 30.6, 19.6, "R07", "dry zone trap"),
    ("SK", 50.95, 4.3, "R13", "utility sink"), ("WM", 44.15, 6.8, "R13", ""), ("FT", 48.5, 3.6, "R13", "floor falls to the trap"), ("TAP", 49.8, 3.4, "R13", "bucket tap, low"),
    ("SK", 57.6, 3.5, "R15", "single bowl + drainboard, centred under the window"), ("RO", 59.0, 3.5, "R15", ""), ("FT", 63.0, 12.0, "R15", "cleaning trap"),
    ("TAP", 69.6, 13.6, "SITE", "foot-wash tap at steps"), ("TAP", 9.0, 10.0, "SITE", "kitchen garden tap (spare land)"), ("TAP", 74.0, 21.6, "SITE", "tulsi / garden tap"),
    ("IC", 37.1, 1.8, "SITE", "IC-1 soil, common bath and the upper WC stack"), ("IC", 12.6, 1.8, "SITE", "IC-3 soil bend at the 64 ft line"),
    ("GT", 57.6, 1.0, "SITE", "grease trap"), ("IC", 48.5, 1.0, "SITE", "IC-4 grey"), ("IC", 39.0, 1.0, "SITE", "IC-5 grey"), ("IC", 12.6, 22.5, "SITE", "IC-7 soil bend to the septic tank (north-west)"), ("IC", 12.0, 1.0, "SITE", "IC-6 grey, to the soak pit"),
]
PLUMBING_F1 = [
    ("WC", 37.1, 7.8, "R33", "on the west wall, over the common bath WC (one stack)"), ("HF", 36.4, 8.6, "R33", ""), ("BS", 41.4, 7.9, "R33", ""),
    ("SH", 41.4, 4.9, "R33", "east wall"), ("FT", 39.0, 4.5, "R33", "shower drain, across the south band"), ("FT", 39.5, 9.6, "R33", "dry zone trap"),
    ("WC", 29.1, 21.6, "R39", "over the master bath WC"), ("HF", 28.4, 22.4, "R39", ""), ("BS", 29.35, 18.4, "R39", "south wall, west of the door"),
    ("SH", 34.2, 23.4, "R39", "east wall"), ("FT", 32.8, 24.4, "R39", "shower drain"), ("FT", 30.6, 19.6, "R39", "dry zone trap"),
    ("FT", 60.4, 3.6, "R37", "terrace drain, to a downpipe at the south-east corner"), ("TAP", 42.4, 4.2, "R37", "terrace tap (plants, cleaning)"),
]
# Pipe runs (schematic): kind, list of points. South walkway: grey y=1.0, soil y=1.8, supply y=2.3 (on plinth face).
PIPES = [
    ("supply", [(71.0, 23.5), (68.2, 23.5), (68.2, 2.3), (42.3, 2.3), (42.3, 3.0)]),
    ("supply", [(68.2, 13.6), (69.6, 13.6)]), ("supply", [(57.6, 2.3), (57.6, 3.0)]), ("supply", [(51.75, 2.3), (51.75, 3.0)]),
    ("supply", [(42.3, 2.3), (38.5, 2.3), (38.5, 3.0)]), ("supply", [(38.5, 2.3), (30.0, 2.3), (30.0, 3.0)]),
    ("soil", [(37.1, 7.8), (37.1, 1.8), (12.6, 1.8), (12.6, 22.5), (5.0, 22.5)]), ("soil", [(35.2, 7.8), (35.2, 1.8)]),
    ("soil", [(29.1, 21.6), (29.1, 26.6), (12.6, 26.6), (12.6, 22.5)]), ("soil", [(3.0, 19.5), (3.5, 15.6)]),
    ("grey", [(57.6, 3.5), (57.6, 1.0), (12.0, 1.0), (12.0, 14.0), (5.1, 14.0)]),
    ("grey", [(48.5, 3.6), (48.5, 1.0)]), ("grey", [(51.75, 4.3), (48.5, 3.6)]), ("grey", [(44.15, 6.8), (48.5, 3.6)]),
    ("grey", [(39.0, 4.5), (39.0, 1.0)]), ("grey", [(29.7, 4.9), (29.7, 1.0)]),
    ("grey", [(32.8, 24.4), (32.8, 26.0), (12.0, 26.0), (12.0, 14.0)]),
    ("rain", [(12.0, 0.5), (74.6, 0.5), (74.6, 23), (74.5, 25)]),
    ("rain", [(12.0, 26.9), (70.5, 26.9), (71.2, 26.2)]),
    ("rain", [(74.5, 24.0), (75.3, 24.0)]),
]

# Construction phasing: roof first, in three stages. Stage 1 is a lived-in ground floor with basic finishes under the full
# two-storey structure and roof; stage 2 adds the upstairs shell and the upgrades; stage 3 fits out the first floor.
# Costs are rough 2026 village rates around Guntur.
PHASES = [
    ("Stage 1: move in", [
        "Whole ground floor with basic finishes: vitrified tiles, one coat of paint, granite kitchen counter with open shelves, ceilings only in the baths.",
        "Footings, columns, first-floor slab and stair designed and built for two floors; RCC frame and ring beam up to roof level.",
        "Tiled hip roof, front gable, kitchen wing and the steel-framed covered terrace with railings and side jali parapets; the whole first-floor slab waterproofed, with drains.",
        "Upstairs left as an open, covered deck: temporary railings on the open edges and a lockable grille gate at the stair head.",
        "Site works: sump, septic tank, drains, water and power connections; temporary fence."], "Rs 30-34 lakh"),
    ("Stage 2: upstairs shell and upgrades (1-2 years later)", [
        "First-floor outer walls with window frames, grilles and shutters: a dry, lockable shell.",
        "Kitchen cabinets, built-in wardrobes and the timber jali screens.",
        "False ceilings in the rooms; final paint and any floor upgrades.",
        "Compound wall, poomukham finishes and landscaping (outside the estimate)."], "Rs 7-11 lakh"),
    ("Stage 3: first-floor fit-out", [
        "Inner walls upstairs: Bedroom 2, its alcove and bath, the study and the toilet.",
        "Doors, wet-room waterproofing and fittings, floors, inside plaster and paint, false ceilings.",
        "Wiring and lights from the sub-board, ACs, wardrobes and desks."], "Rs 7-10 lakh"),
]
PHASE1_PROVISIONS = [
    "Plan approval for the full two-storey house now.",
    "Beams under the future upstairs walls (y 11.5 and y 14 over the ground master) cast with the slab.",
    "Sleeves for the WC soil pipes, floor traps and shower drains cast into the slab at the upper bath and toilet; soil and vent stacks run to roof level and capped.",
    "Conduits for first-floor lights and fans cast into the slab; conduit from the main DB to the first-floor sub-board position.",
    "Water supply branches to the upper bath and toilet, capped; overhead tank on its final stand.",
    "Whole first-floor slab waterproofed in stage 1, with a drip edge all round.",
    "Columns, ring beam and lintel band set so the stage-2 outer walls and windows drop in; AC sleeves marked.",
    "Kitchen and wardrobe walls finished with the plumbing, sockets and hold-fasts for the stage-2 cabinets already in.",
]
PHASE1_LIVING = [
    "Upstairs is a shaded, covered deck behind a grille gate: storage, drying clothes, a sit-out (no water use until stage 3).",
    "The ground floor stays cool from day one: it has the roof's shade and attic over it, not a bare slab.",
    "Stages 2 and 3 are dry, light work under cover: no roofing over an occupied house; materials up the stair and the terrace; a dust curtain at the stair hall.",
    "Splitting into three stages costs about Rs 2-4 lakh more overall (coming back, price rises, some repainting).",
    "Never defer: structure, anti-termite treatment, plinth, waterproofing, the roof, or pipes and conduits buried in walls and slabs.",
]
PHASE2_ROOMS = ("R31", "R32", "R33", "R36", "R38", "R39")

HOLD_POINTS = [
    ("Before design freeze", "Soil test report, level survey of plot and road, water quality test (TDS, hardness, fluoride)", "Owner, engineer"),
    ("Excavation", "Footing depth and bearing layer seen in the pit; no black soil left under footings", "Structural engineer"),
    ("Before each concrete pour", "Reinforcement, cover blocks, laps and column positions checked; photos taken", "Engineer / site supervisor"),
    ("Plinth", "Anti-termite treatment (certificate), fill compaction, DPC laid and cured", "Supervisor"),
    ("Before plaster", "Conduits, pipes, AC sleeves, mesh over AAC joints; photos with a tape measure in view", "Owner, supervisor"),
    ("Wet rooms", "Waterproofing coats, upturns, 48 h flood test passed before any tile is laid", "Owner, plumber"),
    ("Roof", "Truss holding-down bolts, membrane and insulation, edge tiles clipped, flashing where the front gable and the kitchen wing meet the two-storey wall, valley gutter between them", "Engineer, owner"),
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
               ELECTRICAL=ELECTRICAL_F1, PLUMBING=PLUMBING_F1, PIPES=[], PILLARS=[], WET_WALLS=WET_WALLS_F1, EXTRA_EXT_WALLS=set(), RAILS=RAILS_F1),
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
