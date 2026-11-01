"""Kerala home, Phase 1: single data model used for every drawing and schedule.
Plan coordinates in feet: x = from west boundary (0-70), y = from south boundary (0-27 plot).
Site: Guntur, Andhra Pradesh. Hot-dry summers (42-45 C), ~850-1000 mm rain (Jun-Oct, cyclonic bursts Oct-Nov),
likely expansive black cotton soil, hard / high-fluoride groundwater, seismic zone III, high cyclone wind speeds.
"""
PROJECT = {
    "name": "Kerala Home, Phase 1",
    "stage": "Draft for professional review",
    "plot": "27 ft x 75 ft (planned on this plot alone; more land may come later)",
    "location": "Guntur, Andhra Pradesh (agricultural land: conversion to be confirmed)",
    "road": "East",
    "rev": "B (pre-construction draft)",
    "date": "30 Oct 2026",
}
SITE = {"w": 27, "l": 75, "strip": 0}  # plot width (N-S), length (E-W), north strip (none for now), ft
T = 0.75  # outer wall thickness, ft (9 in finished)

ROOMS = [  # id, name, x1, x2, y1, y2, zone
    ("R01", "Workstation (open, walls optional later)", 5, 14, 3, 11, "Master suite"),
    ("R02", "Master bay (old store, open to the bedroom)", 14, 21, 3, 11, "Master suite"),
    ("R03", "Dressing alcove", 5, 11.5, 11, 17, "Master suite"),
    ("R04", "Ensuite", 5, 11.5, 17, 25, "Master suite"),
    ("R05", "Master bedroom", 11.5, 21, 11, 25, "Master suite"),
    ("R08", "Bath 2 (attached to Bedroom 2)", 21, 28, 18, 25, "Private"),
    ("R07", "Common bath", 41.5, 48, 3, 9, "Service"),
    ("R09", "Bedroom 2", 21, 38, 10.5, 25, "Private"),
    ("R10", "Dining", 38, 49, 11, 19, "Living"),
    ("R19", "Dining bay (north window)", 38, 49, 19, 25, "Living"),
    ("R13", "Wet area (open to the walkway)", 48, 53, 3, 9, "Service"),
    ("R14", "Sitting and serving area (open)", 21, 41.5, 3, 10.5, "Living"),
    ("R15", "Kitchen", 53, 67, 3, 13, "Service"),
    ("R16", "Living", 49, 61, 13, 25, "Living"),
    ("R11", "Pooja", 57, 61, 13, 17, "Living"),
    ("R17", "Poomukham (verandah)", 61, 67, 13, 25, "Entry"),
]

# Walls: (axis, coordinate, start, end). axis "X" = runs along x at y=c; "Y" = runs along y at x=c.
WALLS = [
    ("X", 3, 5, 48), ("X", 3, 53, 67), ("Y", 5, 3, 25), ("X", 25, 5, 61), ("Y", 67, 3, 13), ("Y", 61, 13, 25),
    ("X", 17, 5, 11.5), ("Y", 11.5, 17, 25), ("Y", 21, 3, 10.5), ("Y", 21, 10.5, 25),
    ("X", 10.5, 21, 37), ("Y", 37, 10.5, 12), ("X", 12, 37, 38), ("Y", 38, 12, 25),  # 1 x 1'-6" corner notch widens the way into the sitting area
    ("X", 18, 21, 28), ("Y", 28, 18, 25),
    ("Y", 41.5, 3, 9), ("X", 9, 41.5, 48), ("Y", 48, 3, 9), ("X", 9, 48, 53), ("Y", 53, 3, 13),
    ("X", 13, 53, 67), ("Y", 57, 13, 17), ("X", 17, 57, 61),
]
EXTERIOR = {("X", 3), ("Y", 5), ("X", 25), ("Y", 67), ("Y", 61)}
# Wall types (finished thickness, ft). AAC blocks in an RCC frame; walls carrying concealed plumbing are thicker
# so pipe chases do not cut a 4 in block in half.
WALL_TYPES = {
    "EXT": (0.75, "200 mm AAC + 20 mm external plaster + 12 mm internal plaster (~9 in)"),
    "WET": (0.58, "150 mm AAC + plaster both faces (~7 in): concealed plumbing walls"),
    "INT": (0.42, "100 mm AAC + plaster both faces (~5 in)"),
}
EXTRA_EXT_WALLS = {("X", 13, 53, 67)}  # kitchen north wall faces the living, the pooja and the open poomukham
WET_WALLS = {("X", 17, 5, 11.5), ("Y", 48, 3, 9), ("X", 9, 48, 53), ("Y", 28, 18, 25), ("X", 18, 21, 28)}  # ensuite basin; common bath WC and basin (shared with the wet area); washing machine; Bath 2 basin and shower

# Levels and heights, ft. 0 = finished ground level (FGL) around the house.
LEVELS = {
    "FGL": 0.0,
    "FFL": 2.0,          # plinth: ground floor finished level
    "poomukham": 1.5,    # verandah one step (6 in) below the house
    "wet_area": 1.75,    # semi-open wet area 3 in below the house
    "bath_drop": 0.04,   # bathrooms 1/2 in (12 mm) below adjoining floor, no raised threshold
    "door_head": 7.0,    # above FFL; continuous RCC lintel band at this level
    "wall_top": 10.0,    # above FFL; RCC roof (ring) beam, trusses bolted to it
    "false_ceiling": 9.5,
    "bath_ceiling": 8.5,
    "riser": 0.5,        # 6 in steps, 12 in treads
    "tank_stand": 18.0,  # top of stand above FGL: ~9 ft head over the shower roses (~0.3 bar); pressure pump for showers
}
FLOOR_FINISH = {  # room: floor finish key
    "R10": "Red oxide / Kota stone", "R16": "Red oxide / Kota stone",
    "R01": "Matt vitrified 2x2", "R02": "Matt vitrified 2x2", "R03": "Matt vitrified 2x2", "R05": "Matt vitrified 2x2",
    "R09": "Matt vitrified 2x2", "R19": "Red oxide / Kota stone",
    "R11": "Red oxide / Kota stone", "R15": "Anti-skid ceramic, waterproofed", "R04": "Anti-skid ceramic, waterproofed",
    "R07": "Anti-skid ceramic, waterproofed", "R08": "Anti-skid ceramic, waterproofed", "R13": "Anti-skid ceramic, waterproofed", "R14": "Red oxide / Kota stone",
    "R17": "Flamed granite",
}
ROOM_LABEL_AT = {"R09": (33.5, 16.8), "R11": (59.7, 14.5), "R16": (53.5, 21.8), "R17": (64, 22.6)}  # label points for rooms whose centre is crowded (the pooja sits in the living rectangle)
ROOM_FLOOR = {"R04": -0.04, "R07": -0.04, "R08": -0.04, "R11": 0.25, "R13": -0.25, "R17": -0.5}  # offset from FFL
# ceiling: ("flat", height above FFL) or ("sloped", note)
CEILINGS = {
    "R01": ("flat", 9.5), "R02": ("flat", 9.5), "R03": ("flat", 9.5), "R04": ("flat", 8.5), "R05": ("flat", 9.5),
    "R07": ("flat", 8.5), "R08": ("flat", 8.5), "R09": ("flat", 9.5), "R19": ("sloped", "follows roof"),
    "R10": ("sloped", "open to ventilator"), "R11": ("flat", 9.5), "R13": ("sloped", "open truss"),
    "R14": ("flat", 9.5), "R15": ("flat", 9.5), "R16": ("sloped", "follows roof"), "R17": ("sloped", "exposed rafters"),
}
ROOF = {
    "pitch": 30,          # degrees
    "overhang": 2.0,      # eaves beyond the outer wall centreline (2 ft keeps the north eave inside the 27 ft plot)
    "hip": (3.0, 69.0, 1.0, 27.0),     # eaves outline x1, x2, y1, y2
    "gable": (59, 69.0, 11.5, 26.5),   # front mukhappu gable outline over the poomukham, ridge E-W
    "gable_lift": 0.24,   # gable eaves sit just above the hip eaves
    "skylight": (42, 47, 12, 17),      # dining ventilator footprint (no glass)
    "vent_sill": 0.75,    # ventilator sill (top of upstand) above the ridge: 9 in minimum
    "vent_louvre": 2.0,   # louvre band height, all four sides (about 20 sq ft free vent area)
    "vent_overhang": 1.5, # hipped cap overhang beyond the louvres
    "downpipes": [(3.0, 1.0), (27, 1.0), (49, 1.0), (69.0, 1.0), (3.0, 26.9), (27, 26.9), (49, 26.9), (69.0, 26.9)],
}

# Site features: id, label, kind ("rect"/"circle"), geometry (x1, x2, y1, y2) or (x, y, r)
SITE_FEATURES = [
    ("TANK", "Overhead tank on 18 ft stand (SW), ladder to roof", "rect", (0.4, 3.0, 6, 9)),
    ("SEPTIC", "Septic tank, 2 chambers, sealed RCC, under the two-wheeler bay (front yard, SE), heavy-duty covers", "rect", (69.5, 74.3, 3.4, 6.6)),
    ("SOAK", "Lined soak pit for septic effluent and grey water, front yard SE, as far from the house and sump as the plot allows (or treated outflow to a road drain)", "circle", (72.6, 9.6, 1.5)),
    ("SUMP", "Sump (NE)", "rect", (71, 74.5, 23.5, 26.5)),
    ("BORE", "Borewell (if any), NE", "circle", (70, 25.6, 0.5)),
    ("PERGOLA", "Creeper pergola for west shade (no big trees near walls)", "rect", (0.3, 4.2, 10.5, 24)),
    ("TULSI", "Tulsi thara at the centre of the forecourt, on the door axis", "circle", (72.4, 19.1, 0.6)),
    ("PATH", "Stone-paved forecourt 6 ft wide on the door axis, gate to steps, around the tulsi thara", "rect", (69.8, 75.0, 16.1, 22.1)),
    ("HEDGE1", "Low hedge screening the two-wheeler bay (access left open by the gate)", "rect", (68.0, 71.0, 11.2, 11.8)),
    ("HEDGE2", "Low hedge screening the sump", "rect", (70.6, 74.6, 22.8, 23.3)),
    ("BAY", "Two-wheeler bay", "rect", (68, 74, 3, 11)),
    ("GATE", "Gate 7 ft, centred on the main door", "rect", (75, 75.5, 15.6, 22.6)),
    ("STEPS", "Entrance steps (3 risers), between the pillars, SS handrail one side", "rect", (67.375, 69.0, 17.3, 20.9)),
    ("FEET", "Foot-wash tap + drain", "circle", (69.6, 13.6, 0.35)),
    ("WSTEP", "Steps from the open wet area down to the walkway (4 risers of about 5 in, along the wall)", "rect", (48.6, 52.4, 0.5, 2.5)),
    ("APRON", "Plinth protection apron 3 ft, sloped away", "apron", (2, 70, 0, 28)),
]
TREES = []  # kept 8 ft+ from walls: roots dry out black cotton soil
JALI_SCREENS = []  # free-standing timber jali screens (none: living opens to the dining)
FUTURE_WALLS = [("X", 11, 5, 14), ("Y", 14, 3, 11)]  # workstation walls: left out for now, can be built later

# Doors: id, axis, c, s, e, swing (+1 toward +y/+x, -1 toward -y/-x, 0 = sliding), name, type
DOORS = [
    ("D01", "Y", 61, 17.6, 20.6, -1, "Main entrance (centred under the front gable)", "Teak panelled, double leaf"),
    ("D05", "Y", 11.5, 19, 21.5, +1, "Ensuite (opens outward)", "Flush, waterproof (WPC/FRP)"),
    ("D06", "Y", 21, 6.4, 8.9, -1, "Master suite entry, from the sitting area into the master bay", "Teak panelled, single leaf"),
    ("D10", "X", 10.5, 33.6, 36.6, +1, "Bedroom 2 (from the sitting area, east end)", "Flush, teak veneer"),
    ("D15", "Y", 41.5, 6.2, 8.7, -1, "Common bath (from the sitting area, opens outward, hinged at the north jamb so the open leaf stays clear of the counter)", "Flush, waterproof (WPC/FRP), door closer"),
    ("D16", "Y", 28, 18.4, 20.9, +1, "Bath 2 (east wall, from Bedroom 2, opens outward)", "Flush, waterproof (WPC/FRP)"),
    ("D11", "Y", 57, 13.5, 16.5, +1, "Pooja", "Carved teak, double leaf (opens inward, clear of the living; faces west, family faces east)"),
    ("D12", "Y", 53, 6.2, 8.7, +1, "Kitchen to wet area", "Steel or WPC, lockable (the wet area is open to outside)"),
    ("D17", "Y", 53, 9.4, 12.4, +1, "Kitchen entry (west, from the dining alcove; hinged at the north jamb)", "Teak frame, glazed upper panel, 3 ft (closes off cooking smoke)"),
]
# Vents above inner doors (7'-6" to 9'-0", above the lintel band): air moves between rooms with doors shut
TRANSOM_TYPES = {
    "jali": "Teak jali vent in a frame: air passes freely (rooms with no sound-privacy need)",
    "jali_closable": "Teak jali with a sliding timber shutter on the room side: open for air, shut for sound privacy",
    "louvre": "Fixed louvres angled down: air for the exhaust fan, no view in",
    "glazed": "Top-hung glazed vent with seals: open for air, closed for calls",
}
TRANSOMS = {"D11": "jali"}
HINGE_AT_END = {"D15", "D17"}  # doors hinged at their far (e) jamb
# None at bedrooms (big north windows, shallow rooms; master also ventilates through Office 2) or bathrooms (door bottom louvre feeds the fan)
TRANSOM_LABELS = {"jali": "Open jali", "jali_closable": "Closable jali", "louvre": "Louvres", "glazed": "Sealed glazed flap"}
TRANSOM_Z = (7.5, 9.0)  # sill and head above FFL

# Windows: id, axis, c, s, e, sill, head, room, type
WINDOWS = [
    ("W01", "X", 3, 6.5, 12.5, 3, 7, "Workstation", "Timber jali + glazed shutters"),
    ("W03", "X", 3, 28, 34, 3.5, 7, "Sitting and serving area", "Timber jali + glazed shutters"),
    ("W17", "Y", 61, 13.6, 16.4, 5.5, 7, "Pooja", "High vent to the poomukham, jali + mesh (lamp smoke out)"),
    ("W19", "X", 3, 42.4, 44.4, 5, 7, "Common bath", "Frosted casement, top-hung vent"),
    ("W05", "X", 3, 54.5, 57.5, 3.5, 7, "Kitchen", "Timber jali + glazed shutters"),
    ("W07", "X", 3, 58.5, 64.5, 3.5, 7, "Kitchen", "Timber jali + glazed shutters"),
    ("W08", "Y", 67, 9.5, 12.5, 3.5, 7, "Kitchen", "Timber jali + glazed shutters (3 ft, north end; hob wall kept solid)"),
    ("W09", "X", 25, 7, 9, 5, 7, "Ensuite", "Frosted casement"),
    ("W10", "Y", 5, 20, 22, 5, 7, "Ensuite", "High jali vent"),
    ("W11", "X", 25, 13, 19, 3, 7, "Master bedroom", "Teak casement, glazed"),
    ("W12", "X", 25, 30, 36, 3, 7, "Bedroom 2", "Teak casement, glazed (6 ft)"),
    ("W13", "X", 25, 22.4, 24.4, 5, 7, "Bath 2", "Frosted casement, top-hung vent"),
    ("W20", "X", 10.5, 27.4, 31.4, 7.5, 9, "Bedroom 2", "High jali vent to the sitting area, above the bed head (cross-ventilation with W12 and W03)"),
    ("W18", "X", 25, 42, 48, 3, 7, "Dining bay", "Teak casement, glazed (north light for the dining)"),
    ("W14", "X", 25, 51, 57, 3, 7, "Living", "Teak casement, glazed (6 ft)"),
    ("W16", "X", 3, 35, 41, 3.5, 7, "Serving counter and hand-wash basin", "Timber jali + glazed shutters (6 ft, over the counter)"),
]
OTHER_OPENINGS = [
    ("SK1", "Ventilator over dining, 5 x 5 ft, no glass: hipped tiled cap at 30 deg with 1'-6\" overhang; 2 ft band of 45 deg louvres on all four sides; SS insect mesh behind; sealed inner shutters on a winding opener; 9 in upstand; lined shaft to the dining ceiling (see A-503)"),
    ("GV1-3", "Three glazed/jali vents in front gable (mukhappu), morning light into living"),
]
PILLARS = [(66.4, 13.6), (66.4, 16.4), (66.4, 21.8), (66.4, 24.4), (63.5, 24.4), (61.6, 24.4)]

# Furniture: id, room, item, x1, x2, y1, y2, qty, material / spec, shape ("rect"|"circle"|"wc"|"glass")
FURNITURE = [
    ("F01", "Workstation", "Work desk 5'6\" x 2' (free-standing, cable tray)", 12, 13.9, 4, 9.5, 1, "Teak or ply + veneer, cable tray", "rect"),
    ("F02", "Workstation", "Ergonomic task chair", 10.6, 11.8, 6.2, 7.4, 1, "Mesh back", "circle"),
    ("F03", "Workstation", "Bookshelf, full height (video backdrop)", 5.3, 6.5, 3.5, 10.5, 1, "Teak / ply, open shelves", "rect"),
    ("F04", "Master bay", "Built-in wardrobe 6'-5\", south wall, sliding doors, lofts above", 14.3, 20.7, 3.3, 5.3, 1, "Ply + laminate, 2 ft deep", "rect"),
    ("F06", "Dressing alcove", "Dresser with mirror (north wall)", 7.6, 10.6, 15.8, 16.6, 1, "Teak", "rect"),
    ("F45", "Dressing alcove", "Built-in wardrobe, west wall, sliding doors", 5.3, 7.3, 11.4, 16.6, 1, "Ply + laminate, 2 ft deep", "rect"),
    ("F07", "Ensuite", "Vanity basin counter 3'-6\" with a mirror cabinet above (toothbrushes, medicines)", 7.2, 10.7, 17.3, 18.8, 1, "Granite top, wall-hung", "rect"),
    ("F08", "Ensuite", "WC (EWC)", 5.4, 7.2, 18.9, 20.1, 1, "Wall-hung, concealed cistern", "wc"),
    ("F09", "Ensuite", "Shower glass partition", 5.3, 9.0, 21.9, 22.1, 1, "8 mm toughened glass", "glass"),
    ("F10", "Master bedroom", "Queen bed 5' x 6'6\" + headboard", 14.2, 20.6, 12.2, 17.2, 1, "Teak, head to east", "rect"),
    ("F11", "Master bedroom", "Floating bedside shelf with a drawer, reading light and charging point above (5 in walls are too thin for recessed niches)", 19.3, 20.3, 11.1, 12.1, 2, "Teak, wall-hung", "rect"),
    ("F12", "Master bedroom", "Reading chair", 12.0, 13.4, 22.6, 24.0, 1, "Cane / upholstered", "circle"),
    ("F54", "Master bedroom", "Window seat / diwan 5' x 2' under the north window, drawers below", 13.6, 18.6, 22.6, 24.6, 1, "Teak, cotton cushion", "rect"),
    ("F16", "Common bath", "WC (EWC), 17 in clear to the north wall", 46.0, 47.7, 6.75, 7.95, 1, "Wall-hung on the wet wall shared with the wet area, concealed cistern", "wc"),
    ("F17", "Common bath", "Wash basin with a mirror cabinet above", 47.0, 47.7, 4.2, 5.4, 1, "Wall-hung", "rect"),
    ("F18", "Common bath", "Shower glass partition (3 x 3 ft shower in the south-west corner)", 44.65, 44.8, 3.4, 6.0, 1, "8 mm toughened glass", "glass"),
    ("F48", "Bath 2", "WC (EWC), 15 in clear each side of its centre", 21.9, 23.1, 22.8, 24.6, 1, "Wall-hung on the north (outer) wall, concealed cistern", "wc"),
    ("F49", "Bath 2", "Wash basin (south wall, dry zone) with a mirror cabinet above", 21.6, 23.1, 18.3, 19.0, 1, "Wall-hung on the wet wall", "rect"),
    ("F63", "Ensuite", "Recessed shower niche 1' x 1'-7\" x 3 in deep, tiled, sloped sill (north wall below the window)", 6.6, 7.6, 24.4, 24.62, 1, "Tile lined, waterproofed", "glass"),
    ("F64", "Common bath", "Recessed shower niche 1' x 1'-7\" x 3 in deep, tiled, sloped sill (south wall below the window)", 42.6, 43.6, 3.38, 3.6, 1, "Tile lined, waterproofed", "glass"),
    ("F65", "Bath 2", "Recessed shower niche 1' x 1'-10\" x 3 in deep in the 7 in wet wall, tiled, sloped sill", 27.48, 27.71, 22.4, 23.4, 1, "Tile lined, waterproofed", "glass"),
    ("F50", "Bath 2", "Fixed glass splash panel at the south edge of the 3' x 3'-6\" wet zone (north-east)", 26.3, 27.8, 21.0, 21.15, 1, "8 mm toughened glass", "glass"),
    ("F20", "Bedroom 2", "Queen bed 5' x 6'6\" + headboard, head to the east wall (padded headboard: TV on the other side)", 31.4, 37.75, 14.0, 19.0, 1, "Teak", "rect"),
    ("F51", "Bedroom 2", "Floating bedside shelf with a drawer, reading light and charging point above", 36.8, 37.8, 12.85, 13.85, 2, "Teak, wall-hung", "rect"),
    ("F22", "Bedroom 2", "Work table 4' x 2' with monitor (east wall, north of the bed; north window to the side)", 35.8, 37.8, 20.4, 24.4, 1, "Teak / ply, cable tray, monitor arm", "rect"),
    ("F23", "Bedroom 2", "Built-in wardrobe 6' with a mirror door (west wall, shared with the master: also a sound buffer)", 21.3, 23.3, 11.2, 17.2, 1, "Ply + laminate", "rect"),
    ("F26", "Pooja", "Pooja mandapam on the east wall (idols face west; family faces east)", 60.0, 60.6, 13.5, 16.5, 1, "Carved teak", "rect"),
    ("F28", "Sitting and serving area", "Built-in bench with storage drawers below", 21.3, 22.8, 3.3, 6.1, 1, "Teak top, ply drawers, on legs", "rect"),
    ("F29", "Wet area", "Utility sink counter (on the kitchen wall), where vessels are washed", 51.0, 52.7, 3.4, 5.9, 1, "Kadappa / granite, SS sinks", "rect"),
    ("F62", "Wet area", "Dish-drying rack over the utility sink (Swedish diskskap idea): steel rods, drip tray draining into the sink", 51.95, 52.75, 3.6, 5.7, 1, "SS 304", "glass"),
    ("F61", "Wet area", "Ceiling clothes airer on pulleys (lower to load, raise to dry), fixed to the roof truss", 48.8, 52.6, 4.9, 6.3, 1, "Aluminium rails, nylon rope, cleat on the wall", "glass"),
    ("F30", "Wet area", "Washing machine bay 2' x 2' (covered back corner, 2 in clear of the bath wall)", 48.4, 50.3, 6.9, 8.8, 1, "Splash-proof socket, floor drain", "rect"),
    ("F31", "Wet area", "Fold-away clothesline in the south walkway", 48.5, 52.5, 0.6, 2.4, 1, "SS wire, wall brackets", "glass"),
    ("F44", "Wet area", "Tall slim utility cupboard (brooms, mops, detergents)", 50.5, 51.7, 7.6, 8.8, 1, "Ply + laminate on legs, louvred doors", "rect"),
    ("F32", "Sitting and serving area", "Hand-wash basin at the east end of the serving counter, just outside the common bath (after meals); mirror on the side wall", 39.3, 41.2, 3.3, 5.3, 1, "Ceramic basin in granite top", "rect"),
    ("F33", "Sitting and serving area", "Serving counter with crockery cabinets above, 6 ft", 33.2, 39.2, 3.3, 5.3, 1, "Granite top, teak + glass shutters", "rect"),
    ("F56", "Sitting and serving area", "Tall storage cupboard 5' x 2' (bedding, suitcases, festival vessels), loft above", 23.0, 28.0, 3.4, 5.4, 1, "Ply + laminate, full height", "rect"),
    ("F34", "Kitchen", "L-counter, south run: deep drawers for vessels instead of shutters", 53.4, 66.6, 3.4, 5.4, 1, "Granite top, ply carcass", "rect"),
    ("F60", "Kitchen", "Utensil rail with hooks beside the hob (ladles, tongs, strainers)", 64.7, 66.4, 3.4, 3.55, 1, "SS rail and S-hooks", "glass"),
    ("F35", "Kitchen", "L-counter, east run (hob centred 7'-6\" from the south wall face, on solid wall; pull-out masala drawer beside the hob)", 64.6, 66.6, 5.4, 12.4, 1, "Granite top, cook faces east", "rect"),
    ("F36", "Dining", "Refrigerator space (dining alcove beside the kitchen door, against the wet-area wall, door facing north)", 48.3, 50.8, 9.35, 11.75, 1, "Double-door, 2'6\" wide", "rect"),
    ("F38", "Dining", "Sofa 5'-6\" (2-3 seats) facing south to the TV about 8 ft away; behind it a 3 ft walk and the window-seat enclave; main door in side view", 42.0, 47.5, 16.9, 19.6, 1, "Teak frame, cotton cushions", "rect"),
    ("F39", "Dining", "Coffee table 3'6\" x 2'", 43.0, 46.5, 14.0, 16.0, 1, "Teak", "rect"),
    ("F53", "Dining", "TV unit 4'-5\" on the north face of the common-bath wall (55-65 in TV wall-mounted above)", 42.6, 47.0, 9.25, 10.5, 1, "Teak, low, open shelves", "rect"),
    ("F68", "Dining bay", "Built-in window seat 6'-5\" x 2' under the north window (charupadi-style enclave: cushions, bolsters, drawers below)", 41.6, 48.0, 22.6, 24.6, 1, "Teak, cotton cushions", "rect"),
    ("F66", "Dining bay", "Reading chair in the north-west corner of the bay", 38.7, 40.5, 22.6, 24.4, 1, "Cane / teak", "circle"),
    ("F40", "Living", "Armchair at the west end of the window diwan", 49.9, 51.7, 20.6, 22.4, 1, "Cane / teak", "circle"),
    ("F58", "Living", "Window diwan 6' x 2'-6\" under the north window, drawers below (guest seating, day bed); out of the line of the main door", 51.9, 57.9, 22.0, 24.6, 1, "Teak frame, cotton mattress and bolsters", "rect"),
    ("F52", "Living", "Shoe bench 3'-3\" (Japanese genkan idea): sit to take shoes off, louvred shoe shelves below, hooks and a keys niche above, small cabinet over", 59.4, 60.6, 21.2, 24.4, 1, "Teak top, ply + laminate, 14 in deep", "rect"),
    ("F59", "Living", "Vilakku madam: carved teak lamp niche with a light inside, on the wall facing the main door", 38.21, 38.55, 16.4, 18.2, 1, "Carved teak, brass lamp", "glass"),
    ("F41", "Poomukham (verandah)", "Oonjal (swing) 3'6\", north side of the verandah, clear of the entrance", 62.0, 65.3, 21.9, 23.4, 1, "Teak, chains to beam", "rect"),
    ("F42", "Poomukham (verandah)", "Charupadi: built-in teak seat with a sloping backrest between the pillars, south of the steps", 65.6, 66.9, 13.95, 16.05, 1, "Laterite base, teak seat and backrest", "rect"),
    ("F69", "Poomukham (verandah)", "Charupadi: built-in teak seat with a sloping backrest between the pillars, north of the steps", 65.6, 66.9, 22.15, 24.05, 1, "Laterite base, teak seat and backrest", "rect"),
]
# extra placements (same item, additional copies drawn on plan)
EXTRA_DRAW = [
    ("F11", 19.3, 20.3, 17.3, 18.3), ("F51", 36.8, 37.8, 19.15, 20.15), ("F18", 41.8, 42.95, 6.0, 6.15),
]

FINISHES = [  # spaces, floor, walls (incl. skirting / dado), ceiling, notes
    ("Living, dining, hall", "Red oxide (IPS) or polished Kota / Tandur stone", "4 in flush skirting in floor stone; lime-finish or mineral paint", "Sloped, follows roof, insulated board under deck", "Stone hides dust better than glossy white tile"),
    ("Bedrooms, offices, dressing", "Matt vitrified 2x2 ft or red oxide", "4 in flush skirting; putty + washable emulsion", "False ceiling at 9'-6\", 50 mm insulation above", "Ventilated attic above false ceiling"),
    ("Pooja", "White marble or teak", "Teak panelling behind idol; 4 in marble skirting", "Teak / board at 9'-6\"", "Idols on the east wall facing west (family faces east); lamp niche with heat-proof back"),
    ("Kitchen", "Anti-skid matt vitrified or Kota, mid-tone", "Tile / stone full height between counter and wall cabinets", "Moisture-resistant board at 9'-6\"", "Counter granite (local Ongole / Chimakurthy), 2 ft deep; deep drawers for vessels, pull-out masala drawer by the hob, utensil rail on the wall beside it"),
    ("Ensuite, Bath 2, common bath", "Anti-skid ceramic (R11), falls 1:60 to drain", "Tiles to 7 ft; full height in shower; waterproofing 12 in up all walls, 7 ft in shower", "Moisture-resistant board / PVC at 8'-6\"", "Recessed tiled shower niche with a sloped sill; mirror cabinet over the basin; towel and clothes hooks at the dry end; 12 mm step down, no raised threshold; doors open outward; SS grab bars by the WC and in the shower"),
    ("Wet area", "Rough Cuddapah / Kota stone, falls to drain", "4 ft stone or tile dado", "Open truss", "6 in kerb under jali wall stops rain blowing in"),
    ("Family store, sitting area", "Red oxide or vitrified", "4 in flush skirting; washable paint", "Board at 9'-6\"", ""),
    ("Poomukham, steps", "Flamed / leather-finish granite (not polished)", "Granite skirting; plinth face clad 2 ft (splash zone)", "Exposed rafters + board", "Polished stone is slippery when wet"),
    ("Exterior", "Plinth apron: PCC 3 ft wide sloped away", "AAC + 20 mm plaster with waterproof additive; elastomeric paint", "-", "Drip grooves under every sill and sunshade"),
    ("Roof (all)", "Mangalore clay tiles, every edge tile clipped / screwed", "Membrane + 50 mm insulation on cement-fibre deck", "Steel truss on RCC ring beam", "Cyclone winds: tie trusses down with holding-down bolts"),
]

OPEN_ISSUES = [
    ("Finishes", "Colour and material scheme to choose: five looks to compare in the 3D model (As drawn, Classic Kerala refined, Chettinad ochre, Modern tropical, Lime and green); decide before ordering floor tiles, paint and door finishes", "Owner", "Open"),
    ("Land", "Front yard is now 8 ft (house 62 ft long): confirm the front setback allowed for this plot and road width before finalising; fall back to a 60 ft house if 10 ft is required", "Architect", "Open"),
    ("Layout", "TV on the north face of the common-bath wall in the dining space, sofa facing south: confirm screen size (55-65 in at about 8 ft from the sofa) and a concealed HDMI/data conduit; the north window behind the sofa may reflect on the screen (matt screen or sheer blind)", "Owner", "Open"),
    ("Land", "Agricultural land: confirm conversion to non-agricultural use with the gram panchayat / collector (AP repealed the NALA Act in 2025; new process to be confirmed)", "Owner / surveyor", "Open"),
    ("Land", "Building permission route (panchayat vs DTCP / APCRDA via APDPMS) and setbacks under AP Building Rules 2017", "Architect", "Open"),
    ("Land", "Plot 27 ft x 75 ft (length to confirm by survey), planned without the north strip: north wall 2 ft from the plot line, eaves cut to 2 ft so they stay inside the plot (gutters both sides); septic tank and soak pit in the front yard", "Architect", "Open"),
    ("Soil", "Soil test (bore holes to 3 m min): black cotton soil is common in Guntur. Foundation type (isolated footings below active zone, under-reamed piles, or soil replacement) depends on it", "Structural engineer", "Open"),
    ("Structure", "RCC frame with AAC infill: columns, plinth beam, lintel band, ring beam; steel truss with cyclone tie-downs", "Structural engineer", "Open"),
    ("Security", "Wet area is open to the walkway: lockable steel/WPC kitchen-to-wet-area door, compound wall and gate at the back; optional MS grille shutter across the wet area opening", "Owner / architect", "Open"),
    ("Services", "Groundwater: test TDS, hardness, fluoride. Plan RO for drinking and a softener for bathrooms if hardness is high", "Plumber / owner", "Open"),
    ("Services", "Septic tank size and soak pit size (percolation test); keep soak pits and gardens as far from foundations as the plot allows in expansive soil", "Engineer", "Open"),
    ("Services", "Electrical load (with ACs), service connection size, earthing, inverter / solar PV", "Electrical engineer", "Open"),
    ("Future land", "If the 10 ft north strip is bought later: move the soak pit there (6 ft+ from the house), and plan any Phase 2 so the north windows keep their light", "Owner / architect", "Deferred by owner"),
    ("Services", "Soak pit in the front yard is only about 5 ft from the house and 13 ft from the sump in black cotton soil: prefer a sealed septic tank with treated outflow to a road or panchayat drain, or a bio-digester tank; confirm with the engineer and the panchayat", "Engineer / panchayat", "Open"),
    ("Vastu", "Bed head east (master), NW ensuite, Bedroom 2's attached bath in its north-west corner on the north wall (north-west of the plot centre), common bath south of the plot centre beside the wet area (outside the central zone), dining at the plot centre, pooja in the living's south-east corner back to back with the kitchen, opening west (devotees face east), shoe cupboard on the east wall north of the main door, DB on the dining face of Bedroom 2's east wall", "Vastu consultant", "To confirm"),
    ("Climate", "Roof heat: insulation, ventilated attic, ventilator lantern louvres and shutters; ODU positions on shaded walls", "Architect", "Open"),
    ("Levels", "Survey road and field levels; plinth at 2 ft above finished ground (raise if site floods)", "Surveyor / architect", "Open"),
]

DECISIONS = [
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
SPEC = [
    ("Substructure", "Soil investigation", "Min. 2 bore holes to 3 m or refusal; swell test, SBC", "Black cotton soil swells when wet and shrinks when dry"),
    ("Substructure", "Foundations", "As per engineer: footings below the active zone (often 1.5-2.5 m) or under-reamed piles; 300 mm sand/moorum cushion", "Prevents seasonal heave cracking"),
    ("Site", "Compound wall", "Precast RCC post-and-panel wall, 5 ft high: 4 in square posts at about 7 ft centres on small pad footings, 2 in slotted panels, set just inside the plot line; panels lift out, so the north run can be moved if the north strip is bought", "Thinnest practical wall: keeps the 2 ft north gap and 3 ft south walkway usable; cheap, quick and reusable"),
    ("Substructure", "Plinth beam + DPC", "RCC plinth beam all round; 40 mm DPC with waterproofing compound at plinth top", "Stops rising damp into AAC"),
    ("Substructure", "Plinth fill", "Non-expansive moorum / gravel in 150 mm layers, compacted; no black soil fill", "Black soil under the floor will heave the slab"),
    ("Substructure", "Anti-termite", "Pre-construction chemical treatment (IS 6313) at foundation, plinth fill and around walls", "High termite risk; cannot be redone easily later"),
    ("Substructure", "Plinth protection", "3 ft PCC apron with slope away, joint sealed to wall", "Keeps rain off expansive soil next to foundations"),
    ("Frame", "Columns, beams, bands", "RCC frame; lintel band at door head, ring beam at wall top; seismic zone III detailing (IS 13920 as engineer decides)", "AAC infill is not load-bearing for truss + cyclone loads"),
    ("Walls", "AAC blocks", "IS 2185-3, 200 mm outer / 150 mm wet walls / 100 mm inner; thin-bed polymer mortar", "Better insulation than brick; lighter frame"),
    ("Walls", "AAC to RCC joints", "Galvanised mesh strip 150 mm wide over every block-concrete joint before plaster", "The most common AAC crack; cheap to prevent"),
    ("Walls", "Chasing", "Cut chases with a groover, never hammer; fill with polymer mortar + mesh", "Hammering cracks AAC blocks"),
    ("Walls", "External plaster", "20 mm, two coats, waterproof admixture, cured 7 days; elastomeric paint", "Wind-driven cyclone rain"),
    ("Roof", "Structure", "Steel truss (hot-dip galvanised or epoxy primed), 30 deg pitch, bolted to ring beam with holding-down bolts", "Uplift in cyclone winds"),
    ("Roof", "Deck and insulation", "Cement-fibre board deck + 50 mm PIR/XPS or reflective insulation + membrane, then battens and Mangalore tiles", "Cuts attic heat in 45 C summers"),
    ("Roof", "Tile fixing", "Clip or screw every tile at eaves, verges, ridges and hips, and every 3rd row elsewhere; ridges bedded and pointed", "Loose tiles fly in cyclones"),
    ("Roof", "Ventilation", "Ridge / gable vents with bird and insect mesh; soffit vents at eaves", "Flushes hot air from the attic"),
    ("Roof", "Dining ventilator", "Steel frame bolted to the truss; hipped tiled cap at 30 deg, 1'-6\" overhang; 45 deg timber or aluminium louvres with 4 in lap; SS 304 mesh about 1.2 mm (18 x 16) in a sealed continuous frame; inner shutters with EPDM seals and a winding opener at 5 ft; 9 in upstand with flashing; fibre-cement lined, insulated shaft", "Lets hot air out, keeps out rain, mosquitoes and attic dust, and closes for AC"),
    ("Roof", "Gutters and downpipes", "150 mm half-round gutters with leaf guard, 100 mm downpipes at 8 points, to the sump filter, overflow to the road drain", "Short heavy bursts; protects the plinth"),
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
    ("Electrical", "Backup", "Inverter circuit to lights, fans, office sockets and router; conduit from roof to DB for future solar PV", "Power cuts during work-from-home"),
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
    # Office 2
    ("F", 9.5, 7, "R01", ""), ("L", 9.5, 9.5, "R01", ""), ("L", 9.5, 4.5, "R01", ""), ("S", 5.4, 10.4, "R01", ""),
    ("U", 13.0, 5, "R01", "floor box under the desk"), ("D", 13.0, 6, "R01", "floor box under the desk"), ("P", 13.0, 8, "R01", "floor box under the desk"), ("AC", 5.6, 7, "R01", "west wall, above the bookshelf"),
    ("ODU", 4.2, 6.5, "R01", "west wall, high"),
    # Family store, dressing, ensuite
    ("L", 17.5, 7.5, "R02", ""), ("P", 14.5, 8.6, "R02", ""), ("P", 20.6, 8.6, "R02", ""),
    ("L", 8.25, 14, "R03", ""), ("WL", 5.4, 14, "R03", "mirror"), ("P", 5.4, 16.4, "R03", "hair dryer"),
    ("L", 8.25, 20.5, "R04", ""), ("EF", 5.4, 24, "R04", "out through west wall"), ("G", 8.3, 24.6, "R04", "over shower"),
    ("PC", 10.9, 18.6, "R04", "shaver, by basin"), ("S", 11.9, 22.0, "R05", "ensuite switches outside the door"),
    # Master bedroom
    ("F", 17.4, 14.7, "R05", "over the bed"), ("L", 18, 23.5, "R05", ""), ("L", 13, 13.5, "R05", ""), ("L", 13, 23.5, "R05", ""), ("S", 20.6, 9.4, "R02", "at the suite door, 2-way"),
    ("S", 20.6, 18.0, "R05", "bedside, 2-way"), ("P", 20.6, 11.6, "R05", "bedside"), ("P", 20.6, 17.6, "R05", "bedside"),
    ("AC", 11.9, 18.0, "R05", "west wall, throws along the bed, not on the head"), ("ODU", 16, 25.6, "R05", "north wall, shaded"),
    # Bath 2 (attached to Bedroom 2, in its north-west corner)
    ("L", 24.5, 21.2, "R08", ""), ("EF", 25.6, 24.6, "R08", "out through the north wall"), ("G", 27.6, 23.6, "R08", "over shower, east wall"),
    ("PC", 23.4, 18.4, "R08", "by basin"), ("S", 28.4, 21.3, "R09", "Bath 2 switches outside the bath door"),
    ("P", 12.2, 24.6, "R05", "reading chair"),
    # Pooja (living SE corner, back to back with the kitchen)
    ("L", 59, 15, "R11", ""), ("WL", 60.4, 15, "R11", "lamp niche above the idols"), ("P", 57.4, 16.6, "R11", ""),
    ("S", 56.6, 16.9, "R16", "pooja switches outside, living side"),
    ("L", 39, 6.5, "R14", ""), ("PC", 34.5, 3.4, "R14", "serving counter, on the pier between the windows"),
    # Common bath (south, beside the wet area)
    ("L", 44.7, 6.2, "R07", ""), ("EF", 46.9, 3.4, "R07", "out through the south wall"), ("G", 41.8, 4.5, "R07", "over shower, west wall (clear of the window)"),
    ("PC", 47.6, 6.0, "R07", "by basin"), ("S", 41.1, 9.2, "R14", "common bath switches outside the door"),
    # Hall, bedroom 2
    ("F", 34.6, 16.5, "R09", "over the bed"), ("WL", 37.6, 16.5, "R09", "reading light over the bed head"), ("L", 24, 14, "R09", ""), ("L", 34, 14, "R09", ""), ("L", 33, 20.5, "R09", ""),
    ("S", 36.8, 11.4, "R09", "at the door (latch side, on the corner return), 2-way"), ("S", 37.6, 13.0, "R09", "bedside, 2-way"), ("P", 37.6, 13.5, "R09", "bedside"), ("P", 37.6, 19.5, "R09", "bedside"), ("S", 37.6, 19.9, "R09", "bedside, 2-way"),
    ("P", 37.6, 20.8, "R09", "work table"), ("U", 37.6, 21.6, "R09", "work table, monitor"), ("D", 37.6, 22.4, "R09", "work table"), ("U", 37.6, 23.2, "R09", "work table"), ("AC", 28.4, 24.0, "R09", "high on the bath's east wall near the north corner, throws east toward the bed foot"),
    ("WL", 41.1, 4.4, "R14", "over basin, on the common bath wall"),
    ("ODU", 29.5, 25.6, "R09", "north wall, shaded"),
    ("L", 41.5, 21.5, "R19", ""), ("F", 45, 21.5, "R19", "long downrod, over the seating"), ("P", 48.6, 24.6, "R19", ""),
    ("TV", 44.8, 9.4, "R10", "TV wall (common-bath wall, dry face): 2 sockets + data + HDMI conduit to the unit"), ("P", 43.2, 9.4, "R10", "TV unit"),
    ("AC", 38.4, 20.0, "R19", "Bedroom 2's east wall, throws east across the hall and the TV seating"), ("ODU", 40.0, 25.6, "R19", "north wall, shaded"),
    # Dining, pooja, sitting area
    ("L", 44.5, 15, "R10", "pendant"), ("WL", 38.4, 17.3, "R10", "inside the lamp niche"), ("P", 38.4, 16.2, "R10", ""), ("S", 38.4, 13.7, "R10", "dining and bay, at the passage"),
    ("L", 30.5, 6.75, "R14", ""), ("S", 21.4, 6.0, "R14", ""), ("INV", 22, 5.0, "R14", "lithium inverter in a ventilated cabinet under the bench"),
    # Wet area, wash link, kitchen
    ("L", 50, 5.5, "R13", "weatherproof"), ("P16", 48.5, 8.7, "R13", "washing machine"), ("P", 52.6, 6.0, "R13", "utility, weatherproof"),
    ("L", 62, 8, "R15", ""), ("WL", 61, 3.5, "R15", "under-cabinet"), ("WL", 66.5, 9.6, "R15", "under-cabinet"),
    ("CH", 66.6, 7.5, "R15", "3 ft chimney on solid wall, duct out through the east wall"),  ("PC", 54.0, 3.5, "R15", ""),
    ("PC", 57.8, 3.5, "R15", "microwave / OTG"), ("PC", 65.3, 3.5, "R15", "mixer"), ("PC", 66.6, 5.6, "R15", ""), ("PC", 66.6, 9.6, "R15", ""),
    ("PC", 58.2, 3.5, "R15", "RO purifier, by sink"), ("S", 53.4, 9.0, "R15", "beside the entry, latch side"),
    # Living, poomukham
    ("F", 55, 19, "R16", "long downrod"), ("L", 54.9, 22.8, "R16", "over the diwan"), ("L", 55, 16, "R16", ""),
    ("P", 47.9, 18.0, "R10", "floor socket, sofa end"), ("P", 51.0, 20.3, "R16", "floor socket, armchair and diwan (lamp, charger)"),
    ("S", 60.6, 21.0, "R16", "main switch at door"), ("DB", 38.4, 12.6, "R10", "dining face of Bedroom 2's east wall, by the passage; dry wall away from the pooja and wet area"), ("P16", 49.55, 9.4, "R10", "refrigerator, behind the fridge (dining alcove)"), ("U", 38.4, 14.6, "R10", "router (central)"),
    ("L", 64, 16, "R17", ""), ("L", 64, 22, "R17", ""), ("BELL", 61.4, 21.0, "R17", ""), ("CAM", 66.5, 24.6, "R17", "covers gate and door"),
    ("P", 61.4, 24.0, "R17", "outdoor, weatherproof"), ("S", 61.4, 21.5, "R17", ""),
    # Site
    ("MTR", 74.6, 23.2, "SITE", "meter in compound wall by gate"), ("GL", 74.7, 15.3, "SITE", "gate post light"), ("GL", 74.7, 22.9, "SITE", "gate post light"),
    ("GL", 66.4, 16.4, "R17", "uplight at the pillar base"), ("GL", 66.4, 21.8, "R17", "uplight at the pillar base"), ("WL", 61.4, 17.1, "R17", "warm lantern beside the main door"),
    ("EP", 68.2, 1.5, "SITE", "earth pit 1"), ("EP", 73.5, 1.5, "SITE", "earth pit 2"), ("GL", 2.5, 8, "SITE", "rear garden"),
]

# Plumbing points: code, x, y, room, note
PLUMB_TYPES = {
    "WC": "Wall-hung WC, concealed cistern", "HF": "Health faucet", "BS": "Wash basin", "SH": "Shower mixer (hot + cold)",
    "FT": "Floor trap / linear drain", "SK": "Sink", "WM": "Washing-machine inlet + drain", "RO": "RO purifier point",
    "TAP": "Tap", "GY": "Geyser connection", "IC": "Inspection chamber", "GT": "Grease trap", "DP": "Rain downpipe",
}
PLUMBING = [
    ("WC", 6.3, 19.5, "R04", "wall-hung on west (outer) wall"), ("HF", 5.4, 20.6, "R04", ""), ("BS", 9.0, 17.8, "R04", "on 7 in wet wall"),
    ("SH", 5.4, 23.6, "R04", ""), ("FT", 8.25, 24.5, "R04", "linear drain along north wall"), ("FT", 9.6, 20.2, "R04", "dry zone trap"),
    ("WC", 47.6, 7.35, "R07", "on the wet wall"), ("HF", 47.6, 6.5, "R07", ""), ("BS", 47.6, 4.8, "R07", "on 7 in wet wall"),
    ("SH", 41.8, 3.9, "R07", "west wall, clear of the window"), ("FT", 43.2, 3.6, "R07", "shower drain"), ("FT", 46.3, 6.0, "R07", "dry zone trap"),
    ("WC", 22.5, 24.0, "R08", "on the north (outer) wall, 15 in clear each side"), ("HF", 21.4, 23.4, "R08", ""), ("BS", 22.35, 18.4, "R08", "on 7 in wet wall (south)"),
    ("SH", 27.6, 24.0, "R08", "east wall"), ("FT", 26.3, 24.3, "R08", "linear drain along the north wall"), ("FT", 24.6, 19.7, "R08", "dry zone trap"),
    ("SK", 51.85, 4.6, "R13", "utility sink"), ("WM", 49.35, 7.85, "R13", ""), ("FT", 49.8, 3.6, "R13", "floor falls out to the walkway"), ("TAP", 52.6, 3.4, "R13", "bucket tap, low"),
    ("BS", 40.2, 4.3, "R14", "hand-wash basin outside the common bath, waste straight out to the south walkway"),
    ("SK", 60.5, 3.5, "R15", "single bowl + drainboard, under window"), ("RO", 59.3, 3.5, "R15", ""), ("FT", 64, 12.5, "R15", "cleaning trap"),
    ("TAP", 69.6, 13.6, "SITE", "foot-wash tap at steps"), ("TAP", 4.4, 10, "SITE", "garden tap"), ("TAP", 74.0, 21.6, "SITE", "tulsi / garden tap"),
    ("IC", 3.6, 19.5, "SITE", "IC-1 soil"), ("IC", 46.8, 1.8, "SITE", "IC-2 soil"), ("IC", 3.6, 26.6, "SITE", "IC-3 soil"), ("IC", 12, 26.6, "SITE", "IC-4 soil"),
    ("GT", 60.5, 1.0, "SITE", "grease trap"), ("IC", 49.8, 1.0, "SITE", "IC-5 grey"), ("IC", 3.6, 1.8, "SITE", "IC-6 soil bend"), ("IC", 68.6, 1.8, "SITE", "IC-12 soil, to the septic tank"), ("IC", 73.2, 1.0, "SITE", "IC-13 grey, to the soak pit"),
    ("IC", 4.2, 1.0, "SITE", "IC-7 grey"), ("IC", 4.2, 26.0, "SITE", "IC-8 grey"), ("IC", 9.6, 26.0, "SITE", "IC-9 ensuite grey"),
    ("IC", 22.5, 26.6, "SITE", "IC-10 Bath 2 soil"), ("IC", 26.4, 26.0, "SITE", "IC-11 Bath 2 grey"),
]
# Pipe runs (schematic): kind, list of points. South walkway: grey y=1.0, soil y=1.8, supply y=2.3 (on plinth face).
PIPES = [
    ("supply", [(1.7, 7.5), (1.7, 2.3), (66, 2.3)]),
    ("supply", [(51.85, 2.3), (51.85, 3)]), ("supply", [(40.2, 2.3), (40.2, 3)]), ("supply", [(60.5, 2.3), (60.5, 3)]),
    ("supply", [(1.7, 7.5), (4.4, 7.5), (4.4, 21), (5, 21)]),
    ("supply", [(4.4, 21), (4.4, 25.7), (27.0, 25.7), (27.0, 25.4)]),
    ("supply", [(47.0, 2.3), (47.0, 3)]), ("supply", [(41.9, 2.3), (41.9, 3)]),
    ("supply", [(66, 2.3), (68, 2.3), (68, 13.6), (69.6, 13.6)]),
    ("soil", [(6.3, 19.5), (3.6, 19.5), (3.6, 1.8)]),
    ("soil", [(22.5, 24.0), (22.5, 26.6), (3.6, 26.6), (3.6, 19.5)]),
    ("soil", [(47.6, 7.35), (46.8, 7.35), (46.8, 1.8)]),
    ("soil", [(3.6, 1.8), (68.6, 1.8), (70.2, 3.4)]), ("soil", [(72.0, 6.6), (72.3, 8.1)]),
    ("grey", [(60.5, 3.5), (60.5, 1.0)]), ("grey", [(4.2, 26.0), (4.2, 1.0), (73.2, 1.0), (73.2, 8.2)]),
    ("grey", [(49.8, 3.6), (49.8, 1.0)]), ("grey", [(40.2, 4.3), (40.2, 1.0)]), ("grey", [(51.85, 4.6), (49.8, 3.6)]), ("grey", [(49.35, 7.85), (49.8, 3.6)]), ("grey", [(47.6, 4.8), (47.0, 4.8), (47.0, 1.0)]), ("grey", [(46.3, 6.0), (47.0, 4.8)]), ("grey", [(43.2, 3.6), (43.2, 1.0)]),
    ("grey", [(22.35, 18.4), (24.6, 19.7), (26.3, 24.3), (26.4, 26.0), (4.2, 26.0)]),
    ("grey", [(9.6, 20.2), (9.6, 26.0)]), ("grey", [(8.25, 24.5), (9.6, 24.5)]),
    ("rain", [(3.0, 0.5), (74.6, 0.5), (74.6, 23), (74.5, 25)]),
    ("rain", [(3.0, 26.9), (70.5, 26.9), (71.2, 26.2)]),
    ("rain", [(74.5, 24.0), (75.3, 24.0)]),
]

# Hold points: inspections before work is covered up. stage, check, who signs off
HOLD_POINTS = [
    ("Before design freeze", "Soil test report, level survey of plot and road, water quality test (TDS, hardness, fluoride)", "Owner, engineer"),
    ("Excavation", "Footing depth and bearing layer seen in the pit; no black soil left under footings", "Structural engineer"),
    ("Before each concrete pour", "Reinforcement, cover blocks, laps and column positions checked; photos taken", "Engineer / site supervisor"),
    ("Plinth", "Anti-termite treatment (certificate), fill compaction, DPC laid and cured", "Supervisor"),
    ("Before plaster", "Conduits, pipes, AC sleeves, mesh over AAC joints; photos with a tape measure in view", "Owner, supervisor"),
    ("Wet rooms", "Waterproofing coats, upturns, 48 h flood test passed before any tile is laid", "Owner, plumber"),
    ("Roof", "Truss holding-down bolts, membrane and insulation, edge tiles clipped, flashings at the ventilator and valleys", "Engineer, owner"),
    ("Before handover", "Water test on every floor slope and sill, plumbing pressure test, electrical insulation and earth test", "Owner, MEP"),
]
