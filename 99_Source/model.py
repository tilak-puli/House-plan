"""Kerala home, Phase 1: single data model used for every drawing and schedule.
Plan coordinates in feet: x = from west boundary (0-70), y = from south boundary (0-27 plot, 27-37 north strip).
Site: Guntur, Andhra Pradesh. Hot-dry summers (42-45 C), ~850-1000 mm rain (Jun-Oct, cyclonic bursts Oct-Nov),
likely expansive black cotton soil, hard / high-fluoride groundwater, seismic zone III, high cyclone wind speeds.
"""
PROJECT = {
    "name": "Kerala Home, Phase 1",
    "stage": "Draft for professional review",
    "plot": "27 ft x 70 ft (+10 ft north strip owned, Phase 2)",
    "location": "Guntur, Andhra Pradesh (agricultural land: conversion to be confirmed)",
    "road": "East",
    "rev": "B (pre-construction draft)",
    "date": "30 Oct 2026",
}
SITE = {"w": 27, "l": 75, "strip": 10}  # plot width (N-S), length (E-W), owned north strip, ft
T = 0.75  # outer wall thickness, ft (9 in finished)

ROOMS = [  # id, name, x1, x2, y1, y2, zone
    ("R01", "Workstation (open, walls optional later)", 5, 14, 3, 11, "Master suite"),
    ("R02", "Master bay (old store, open to the bedroom)", 14, 23, 3, 11, "Master suite"),
    ("R03", "Dressing alcove", 5, 11.5, 11, 17, "Master suite"),
    ("R04", "Ensuite", 5, 11.5, 17, 25, "Master suite"),
    ("R05", "Master bedroom", 11.5, 23, 11, 25, "Master suite"),
    ("R07", "Bath 2 (attached to Bedroom 2)", 23, 28.5, 19, 25, "Private"),
    ("R09", "Bedroom 2", 23, 38, 9, 25, "Private"),
    ("R10", "Dining", 38, 47, 11, 19, "Living"),
    ("R19", "Dining bay (north window)", 38, 47, 19, 25, "Living"),
    ("R11", "Pooja", 41, 45, 3, 9, "Living"),
    ("R13", "Wet area (open to the walkway)", 45, 51, 3, 9, "Service"),
    ("R14", "Sitting and serving area (open)", 23, 41, 3, 9, "Living"),
    ("R15", "Kitchen", 51, 65, 3, 13, "Service"),
    ("R16", "Living", 47, 59, 13, 25, "Living"),
    ("R17", "Poomukham (verandah)", 59, 65, 13, 25, "Entry"),
]

# Walls: (axis, coordinate, start, end). axis "X" = runs along x at y=c; "Y" = runs along y at x=c.
WALLS = [
    ("X", 3, 5, 45), ("X", 3, 51, 65), ("Y", 5, 3, 25), ("X", 25, 5, 59), ("Y", 65, 3, 13), ("Y", 59, 13, 25),
    ("X", 17, 5, 11.5), ("Y", 11.5, 17, 25), ("Y", 23, 3, 9), ("Y", 23, 9, 25),
    ("Y", 41, 3, 9), ("X", 9, 41, 45), ("X", 9, 23, 38), ("Y", 38, 9, 25), ("X", 19, 23, 28.5), ("Y", 28.5, 19, 25),
    ("Y", 45, 3, 9), ("X", 9, 45, 51), ("Y", 51, 3, 13),
    ("X", 13, 51, 65),
]
EXTERIOR = {("X", 3), ("Y", 5), ("X", 25), ("Y", 65), ("Y", 59)}
# Wall types (finished thickness, ft). AAC blocks in an RCC frame; walls carrying concealed plumbing are thicker
# so pipe chases do not cut a 4 in block in half.
WALL_TYPES = {
    "EXT": (0.75, "200 mm AAC + 20 mm external plaster + 12 mm internal plaster (~9 in)"),
    "WET": (0.58, "150 mm AAC + plaster both faces (~7 in): concealed plumbing walls"),
    "INT": (0.42, "100 mm AAC + plaster both faces (~5 in)"),
}
EXTRA_EXT_WALLS = {("X", 13, 51, 65)}  # kitchen north wall faces the living and the open poomukham
WET_WALLS = {("X", 17, 5, 11.5), ("Y", 28.5, 19, 25), ("X", 9, 45, 51)}  # ensuite basin; Bath 2 basin and shower wall; washing machine. The pooja / wet-area wall stays dry

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
    "R11": "Marble / teak (pooja)", "R15": "Anti-skid matt vitrified", "R04": "Anti-skid ceramic, waterproofed",
    "R07": "Anti-skid ceramic, waterproofed", "R13": "Rough Cuddapah / Kota, falls", "R14": "Red oxide / Kota stone",
    "R17": "Flamed granite",
}
ROOM_FLOOR = {"R04": -0.04, "R07": -0.04, "R11": 0.25, "R13": -0.25, "R17": -0.5}  # offset from FFL
# ceiling: ("flat", height above FFL) or ("sloped", note)
CEILINGS = {
    "R01": ("flat", 9.5), "R02": ("flat", 9.5), "R03": ("flat", 9.5), "R04": ("flat", 8.5), "R05": ("flat", 9.5),
    "R07": ("flat", 8.5), "R09": ("flat", 9.5), "R19": ("sloped", "follows roof"),
    "R10": ("sloped", "open to ventilator"), "R11": ("flat", 9.5), "R13": ("sloped", "open truss"),
    "R14": ("flat", 9.5), "R15": ("flat", 9.5), "R16": ("sloped", "follows roof"), "R17": ("sloped", "exposed rafters"),
}
ROOF = {
    "pitch": 30,          # degrees
    "overhang": 2.5,      # eaves beyond the outer wall centreline
    "hip": (2.5, 67.5, 0.5, 27.5),     # eaves outline x1, x2, y1, y2
    "gable": (57, 67.5, 11.5, 26.5),   # front mukhappu gable outline over the poomukham, ridge E-W
    "gable_lift": 0.24,   # gable eaves sit just above the hip eaves
    "skylight": (40, 45, 12, 17),      # dining ventilator footprint (no glass)
    "vent_sill": 0.75,    # ventilator sill (top of upstand) above the ridge: 9 in minimum
    "vent_louvre": 2.0,   # louvre band height, all four sides (about 20 sq ft free vent area)
    "vent_overhang": 1.5, # hipped cap overhang beyond the louvres
    "downpipes": [(2.5, 0.5), (27, 0.5), (47, 0.5), (67.5, 0.5), (2.5, 27.5), (27, 27.5), (47, 27.5), (67.5, 27.5)],
}

# Site features: id, label, kind ("rect"/"circle"), geometry (x1, x2, y1, y2) or (x, y, r)
SITE_FEATURES = [
    ("TANK", "Overhead tank on 18 ft stand (SW), ladder to roof", "rect", (0.4, 3.0, 6, 9)),
    ("SEPTIC", "Septic tank, 2 chambers (NW, in north strip)", "rect", (0.8, 4.2, 29, 35)),
    ("SOAK", "Soak pit, grey water (6 ft+ from house)", "circle", (10, 32, 2.0)),
    ("SUMP", "Sump (NE)", "rect", (71, 74.5, 23.5, 26.5)),
    ("BORE", "Borewell (if any), NE", "circle", (68, 25.6, 0.5)),
    ("RWH", "Rainwater recharge pit (sump overflow)", "circle", (71.5, 32, 1.5)),
    ("PERGOLA", "Creeper pergola for west shade (no big trees near walls)", "rect", (0.3, 4.2, 10.5, 24)),
    ("TULSI", "Tulsi thara", "circle", (70.5, 20.5, 0.6)),
    ("BAY", "Two-wheeler bay", "rect", (66, 74, 3, 11)),
    ("GATE", "Gate", "rect", (75, 75.5, 15, 22)),
    ("STEPS", "Entrance steps (3 risers), between the pillars", "rect", (65.375, 67.0, 14.1, 17.9)),
    ("FEET", "Foot-wash tap + drain", "circle", (67.6, 13.6, 0.35)),
    ("WSTEP", "Steps from the open wet area down to the walkway (4 risers of about 5 in, along the wall)", "rect", (45.6, 50.4, 0.5, 2.5)),
    ("APRON", "Plinth protection apron 3 ft, sloped away", "apron", (2, 68, 0, 28)),
]
TREES = [(45, 33.5, 3), (59, 34.5, 2), (27, 34, 2.5), (35, 34.5, 2)]  # kept 8 ft+ from walls: roots dry out black cotton soil
JALI_SCREENS = []  # free-standing timber jali screens (none: living opens to the dining)
FUTURE_WALLS = [("X", 11, 5, 14), ("Y", 14, 3, 11)]  # workstation walls: left out for now, can be built later

# Doors: id, axis, c, s, e, swing (+1 toward +y/+x, -1 toward -y/-x, 0 = sliding), name, type
DOORS = [
    ("D01", "Y", 59, 15, 18, -1, "Main entrance", "Teak panelled, double leaf"),
    ("D05", "Y", 11.5, 19, 21.5, -1, "Ensuite", "Flush, waterproof (WPC/FRP)"),
    ("D06", "Y", 23, 6.4, 8.9, -1, "Master suite entry, from the sitting area into the master bay", "Teak panelled, single leaf"),
    ("D10", "X", 9, 23.5, 26.5, +1, "Bedroom 2 (from the sitting area)", "Flush, teak veneer"),
    ("D15", "X", 19, 24.0, 26.5, +1, "Bath 2 (attached to Bedroom 2)", "Flush, waterproof (WPC/FRP)"),
    ("D11", "Y", 41, 4.5, 7.5, +1, "Pooja", "Carved teak, double leaf (opens west; family sits facing east)"),
    ("D12", "Y", 51, 6.2, 8.7, +1, "Kitchen to wet area", "Steel or WPC, lockable (the wet area is open to outside)"),
    ("D14", "Y", 51, 9.6, 12.6, 0, "Kitchen entry from dining", "Sliding glass, 3 ft (closes off cooking smoke)"),
]
# Vents above inner doors (7'-6" to 9'-0", above the lintel band): air moves between rooms with doors shut
TRANSOM_TYPES = {
    "jali": "Teak jali vent in a frame: air passes freely (rooms with no sound-privacy need)",
    "jali_closable": "Teak jali with a sliding timber shutter on the room side: open for air, shut for sound privacy",
    "louvre": "Fixed louvres angled down: air for the exhaust fan, no view in",
    "glazed": "Top-hung glazed vent with seals: open for air, closed for calls",
}
TRANSOMS = {"D11": "jali"}
# None at bedrooms (big north windows, shallow rooms; master also ventilates through Office 2) or bathrooms (door bottom louvre feeds the fan)
TRANSOM_LABELS = {"jali": "Open jali", "jali_closable": "Closable jali", "louvre": "Louvres", "glazed": "Sealed glazed flap"}
TRANSOM_Z = (7.5, 9.0)  # sill and head above FFL

# Windows: id, axis, c, s, e, sill, head, room, type
WINDOWS = [
    ("W01", "X", 3, 7, 12, 3, 7, "Workstation", "Timber jali + glazed shutters"),
    ("W02", "X", 3, 20.6, 22.6, 3, 7, "Master bay", "Teak casement, glazed (south light, deep sunshade)"),
    ("W03", "X", 3, 28, 33, 3, 7, "Sitting and serving area", "Timber jali + glazed shutters"),
    ("W04", "X", 3, 38, 41, 3.5, 7, "Basin and crockery nook", "Timber jali + glazed shutters (over the serving counter)"),
    ("W17", "X", 3, 41.8, 43.8, 5.5, 7, "Pooja", "High vent, jali + mesh (lamp smoke out)"),
    ("W05", "X", 3, 52.5, 55.5, 3.5, 7, "Kitchen", "Timber jali + glazed shutters"),
    ("W07", "X", 3, 57, 62, 3.5, 7, "Kitchen", "Timber jali + glazed shutters"),
    ("W08", "Y", 65, 5, 11, 3.5, 7, "Kitchen", "Timber jali + glazed shutters"),
    ("W09", "X", 25, 6, 9, 5, 7, "Ensuite", "Frosted casement"),
    ("W10", "Y", 5, 19, 23, 5, 7, "Ensuite", "High jali vent"),
    ("W11", "X", 25, 14.25, 20.25, 3, 7, "Master bedroom", "Teak casement, glazed"),
    ("W12", "X", 25, 32, 37, 3, 7, "Bedroom 2", "Teak casement, glazed"),
    ("W13", "X", 25, 24.3, 26.5, 5, 7, "Bath 2", "Frosted casement, top-hung vent"),
    ("W18", "X", 25, 40, 46, 3, 7, "Dining bay", "Teak casement, glazed (north light for the dining)"),
    ("W14", "X", 25, 48, 56, 2, 8, "Living", "Teak casement, tall, glazed"),
    ("W16", "X", 3, 34, 37, 3.5, 7, "Basin and crockery nook", "Timber jali + glazed shutters (over the serving counter)"),
]
OTHER_OPENINGS = [
    ("SK1", "Ventilator over dining, 5 x 5 ft, no glass: hipped tiled cap at 30 deg with 1'-6\" overhang; 2 ft band of 45 deg louvres on all four sides; SS insect mesh behind; sealed inner shutters on a winding opener; 9 in upstand; lined shaft to the dining ceiling (see A-503)"),
    ("GV1-3", "Three glazed/jali vents in front gable (mukhappu), morning light into living"),
]
PILLARS = [(64.4, 13.6), (64.4, 18.4), (64.4, 23.6), (61.5, 24.4), (59.6, 24.4)]

# Furniture: id, room, item, x1, x2, y1, y2, qty, material / spec, shape ("rect"|"circle"|"wc"|"glass")
FURNITURE = [
    ("F01", "Workstation", "Work desk 5'6\" x 2' (free-standing, cable tray)", 12, 13.9, 4, 9.5, 1, "Teak or ply + veneer, cable tray", "rect"),
    ("F02", "Workstation", "Ergonomic task chair", 10.6, 11.8, 6.2, 7.4, 1, "Mesh back", "circle"),
    ("F03", "Workstation", "Bookshelf, full height (video backdrop)", 5.3, 6.5, 3.5, 10.5, 1, "Teak / ply, open shelves", "rect"),
    ("F04", "Master bay", "Built-in wardrobe 6 ft, south wall, sliding doors, lofts above", 14.3, 20.3, 3.3, 5.3, 1, "Ply + laminate, 2 ft deep", "rect"),
    ("F06", "Dressing alcove", "Dresser with mirror (north wall)", 7.6, 10.6, 15.8, 16.6, 1, "Teak", "rect"),
    ("F45", "Dressing alcove", "Built-in wardrobe, west wall, sliding doors", 5.3, 7.3, 11.4, 16.6, 1, "Ply + laminate, 2 ft deep", "rect"),
    ("F07", "Ensuite", "Vanity basin counter 3'-6\"", 7.2, 10.7, 17.3, 18.8, 1, "Granite top, wall-hung", "rect"),
    ("F08", "Ensuite", "WC (EWC)", 5.4, 7.2, 18.9, 20.1, 1, "Wall-hung, concealed cistern", "wc"),
    ("F09", "Ensuite", "Shower glass partition", 5.3, 9.0, 21.9, 22.1, 1, "8 mm toughened glass", "glass"),
    ("F10", "Master bedroom", "Queen bed 5' x 6'6\" + headboard", 16.2, 22.6, 16, 21, 1, "Teak, head to east", "rect"),
    ("F11", "Master bedroom", "Bedside table", 21.3, 22.3, 14.8, 15.9, 2, "Teak", "rect"),
    ("F12", "Master bedroom", "Reading chair", 12.0, 13.4, 22.6, 24.0, 1, "Cane / upholstered", "circle"),
    ("F16", "Bath 2", "WC (EWC)", 23.4, 24.6, 22.8, 24.6, 1, "Wall-hung on the north (outer) wall, concealed cistern", "wc"),
    ("F17", "Bath 2", "Wash basin", 27.1, 27.8, 19.9, 21.5, 1, "Wall-hung", "rect"),
    ("F18", "Bath 2", "Shower glass partition (shower in the north-east corner)", 25.3, 25.45, 22.2, 24.6, 1, "8 mm toughened glass", "glass"),
    ("F20", "Bedroom 2", "Sofa-cum-bed 6'6\" (opens to a 5 ft deep bed)", 31.4, 37.8, 9.3, 12.1, 1, "Teak frame, foam mattress", "rect"),
    ("F22", "Bedroom 2", "Work table 4' x 2' with monitor (against the bath wall)", 28.7, 30.7, 19.6, 23.6, 1, "Teak / ply, cable tray, monitor arm", "rect"),
    ("F23", "Bedroom 2", "Built-in wardrobe 6' (east wall, toward the house centre)", 36.0, 37.8, 18.6, 24.6, 1, "Ply + laminate", "rect"),
    ("F24", "Dining", "Dining table 5' x 3', 6-seat", 40.5, 45.5, 13.5, 16.5, 1, "Teak or rosewood", "rect"),
    ("F25", "Dining", "Dining chair", 40.8, 41.9, 12.3, 13.3, 6, "Teak + cane", "rect"),
    ("F26", "Pooja", "Pooja mandapam on the east wall (idols face west; family faces east)", 44.1, 44.7, 4.5, 7.5, 1, "Carved teak", "rect"),
    ("F28", "Sitting and serving area", "Built-in bench with storage drawers below", 23.3, 24.8, 3.3, 6.1, 1, "Teak top, ply drawers, on legs", "rect"),
    ("F29", "Wet area", "Utility sink counter (on the kitchen wall)", 49.0, 50.7, 3.4, 5.9, 1, "Kadappa / granite, SS sinks", "rect"),
    ("F30", "Wet area", "Washing machine bay 2' x 2' (covered back corner, 2 in clear of the pooja wall)", 45.5, 47.4, 6.9, 8.8, 1, "Splash-proof socket, floor drain", "rect"),
    ("F31", "Wet area", "Fold-away clothesline in the south walkway", 45.5, 50.5, 0.6, 2.4, 1, "SS wire, wall brackets", "glass"),
    ("F44", "Wet area", "Tall slim utility cupboard (brooms, mops, detergents)", 47.6, 48.8, 7.6, 8.8, 1, "Ply + laminate on legs, louvred doors", "rect"),
    ("F32", "Sitting and serving area", "Counter-top wash basin at the west end of the serving counter, away from the pooja", 31.2, 33.1, 3.3, 5.3, 1, "Ceramic basin in granite top", "rect"),
    ("F33", "Sitting and serving area", "Serving counter with crockery cabinets above, 7 ft", 33.2, 40.5, 3.3, 5.3, 1, "Granite top, teak + glass shutters", "rect"),
    ("F34", "Kitchen", "L-counter, south run", 53.9, 64.6, 3.4, 5.4, 1, "Granite top, ply carcass", "rect"),
    ("F35", "Kitchen", "L-counter, east run (hob)", 62.6, 64.6, 5.4, 12.4, 1, "Granite top, cook faces east", "rect"),
    ("F36", "Kitchen", "Refrigerator space (west end, away from the hob)", 51.4, 53.7, 3.4, 5.8, 1, "Double-door, 2'6\" wide", "rect"),
    ("F37", "Living", "TV unit + 50-55 in TV (east wall, north of the door)", 57.4, 58.6, 19.8, 24.3, 1, "Teak; north window to the side, no glare", "rect"),
    ("F38", "Living", "Three-seat sofa 6'6\" facing the TV", 47.6, 50.3, 18.2, 24.5, 1, "Teak frame, cotton cushions", "rect"),
    ("F39", "Living", "Coffee table 3'6\" x 2'", 51.8, 53.8, 19.3, 22.6, 1, "Teak", "rect"),
    ("F40", "Living", "Armchair by the north window", 50.8, 52.8, 22.9, 24.5, 1, "Cane / teak", "circle"),
    ("F41", "Poomukham (verandah)", "Oonjal (swing) 3'6\"", 60, 63.5, 21, 22.5, 1, "Teak, chains to beam", "rect"),
    ("F42", "Poomukham (verandah)", "Arugu seats (built-in)", 63.8, 65, 18.9, 23.1, 2, "Laterite base, teak top", "rect"),
]
# extra placements (same item, additional copies drawn on plan)
EXTRA_DRAW = [
    ("F11", 21.3, 22.3, 21.1, 22.2), ("F25", 42.5, 43.6, 12.3, 13.3), ("F25", 44.2, 45.3, 12.3, 13.3),
    ("F25", 40.8, 41.9, 16.7, 17.7), ("F25", 42.5, 43.6, 16.7, 17.7), ("F25", 44.2, 45.3, 16.7, 17.7),
    ("F42", 59, 63.8, 24, 25),
]

FINISHES = [  # spaces, floor, walls (incl. skirting / dado), ceiling, notes
    ("Living, dining, hall", "Red oxide (IPS) or polished Kota / Tandur stone", "4 in flush skirting in floor stone; lime-finish or mineral paint", "Sloped, follows roof, insulated board under deck", "Stone hides dust better than glossy white tile"),
    ("Bedrooms, offices, dressing", "Matt vitrified 2x2 ft or red oxide", "4 in flush skirting; putty + washable emulsion", "False ceiling at 9'-6\", 50 mm insulation above", "Ventilated attic above false ceiling"),
    ("Pooja", "White marble or teak", "Teak panelling behind idol; 4 in marble skirting", "Teak / board at 9'-6\"", "Idol on west wall facing east; lamp niche with heat-proof back"),
    ("Kitchen", "Anti-skid matt vitrified or Kota, mid-tone", "Tile / stone full height between counter and wall cabinets", "Moisture-resistant board at 9'-6\"", "Counter granite (local Ongole / Chimakurthy), 2 ft deep"),
    ("Ensuite, Bath 2", "Anti-skid ceramic (R11), falls 1:60 to drain", "Tiles to 7 ft; full height in shower; waterproofing 12 in up all walls, 7 ft in shower", "Moisture-resistant board / PVC at 8'-6\"", "12 mm step down, no raised threshold"),
    ("Wet area", "Rough Cuddapah / Kota stone, falls to drain", "4 ft stone or tile dado", "Open truss", "6 in kerb under jali wall stops rain blowing in"),
    ("Family store, sitting area", "Red oxide or vitrified", "4 in flush skirting; washable paint", "Board at 9'-6\"", ""),
    ("Poomukham, steps", "Flamed / leather-finish granite (not polished)", "Granite skirting; plinth face clad 2 ft (splash zone)", "Exposed rafters + board", "Polished stone is slippery when wet"),
    ("Exterior", "Plinth apron: PCC 3 ft wide sloped away", "AAC + 20 mm plaster with waterproof additive; elastomeric paint", "-", "Drip grooves under every sill and sunshade"),
    ("Roof (all)", "Mangalore clay tiles, every edge tile clipped / screwed", "Membrane + 50 mm insulation on cement-fibre deck", "Steel truss on RCC ring beam", "Cyclone winds: tie trusses down with holding-down bolts"),
]

OPEN_ISSUES = [
    ("Land", "Agricultural land: confirm conversion to non-agricultural use with the gram panchayat / collector (AP repealed the NALA Act in 2025; new process to be confirmed)", "Owner / surveyor", "Open"),
    ("Land", "Building permission route (panchayat vs DTCP / APCRDA via APDPMS) and setbacks under AP Building Rules 2017", "Architect", "Open"),
    ("Land", "Plot 27 ft x 70 ft: north wall is 2 ft from the plot line and eaves overhang the owned north strip; septic and soak pit sit in the strip", "Architect", "Open"),
    ("Soil", "Soil test (bore holes to 3 m min): black cotton soil is common in Guntur. Foundation type (isolated footings below active zone, under-reamed piles, or soil replacement) depends on it", "Structural engineer", "Open"),
    ("Structure", "RCC frame with AAC infill: columns, plinth beam, lintel band, ring beam; steel truss with cyclone tie-downs", "Structural engineer", "Open"),
    ("Security", "Wet area is open to the walkway: lockable steel/WPC kitchen-to-wet-area door, compound wall and gate at the back; optional MS grille shutter across the wet area opening", "Owner / architect", "Open"),
    ("Services", "Groundwater: test TDS, hardness, fluoride. Plan RO for drinking and a softener for bathrooms if hardness is high", "Plumber / owner", "Open"),
    ("Services", "Septic and soak pit sizes; keep soak pits and gardens 6 ft+ from foundations in expansive soil", "Engineer", "Open"),
    ("Services", "Electrical load (with ACs), service connection size, earthing, inverter / solar PV", "Electrical engineer", "Open"),
    ("Phase 2", "Phase 2 on the north strip will block north light and sits on the septic: plan the split now", "Architect", "Deferred by owner"),
    ("Vastu", "Bed head east (master), NW ensuite, Bedroom 2's attached bath north-west of centre on the outer wall (no common toilet), central dining, pooja south of centre opening west (devotees face east), beside the open wet area with a dry shared wall, DB in SE-ish living wall", "Vastu consultant", "To confirm"),
    ("Climate", "Roof heat: insulation, ventilated attic, ventilator lantern louvres and shutters; ODU positions on shaded walls", "Architect", "Open"),
    ("Levels", "Survey road and field levels; plinth at 2 ft above finished ground (raise if site floods)", "Surveyor / architect", "Open"),
]

DECISIONS = [
    "Site is in Guntur, Andhra Pradesh (farm land), not Kerala; Kerala style kept, construction adapted to local climate and soil.",
    "Plot 27 ft x 75 ft (5 ft longer than first assumed; confirm by survey), road on east; house 60 ft x 22 ft with the same 10 ft front yard and 5 ft rear garden; owner accepts local practice on side setbacks (to be checked).",
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
    "Eighth review: plot 5 ft longer, so the house grows to 60 ft. The master suite takes 2 ft (master bedroom 11'-6\" x 14', master bay 9 x 8 ft) and Bedroom 2 takes 3 ft (15 x 16 ft); the sitting area in front of them grows to 18 ft. Everything east of Bedroom 2 moves 5 ft east; the plot centre now falls inside Bedroom 2, near its east wall, with the dining and ventilator about 5 ft east of it (Vastu to confirm).",
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
    ("Roof", "Gutters and downpipes", "150 mm half-round gutters with leaf guard, 100 mm downpipes at 8 points, to sump filter and recharge pit", "Short heavy bursts; protects the plinth"),
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
    ("L", 18.5, 7.5, "R02", ""), ("P", 17, 8.6, "R02", ""), ("P", 22.6, 8.6, "R02", ""),
    ("L", 8.25, 14, "R03", ""), ("WL", 5.4, 14, "R03", "mirror"), ("P", 5.4, 16.4, "R03", "hair dryer"),
    ("L", 8.25, 20.5, "R04", ""), ("EF", 5.4, 24, "R04", "out through west wall"), ("G", 8.3, 24.6, "R04", "over shower"),
    ("PC", 10.9, 18.6, "R04", "shaver, by basin"), ("S", 11.9, 22.0, "R05", "ensuite switches outside the door"),
    # Master bedroom
    ("F", 17.25, 18, "R05", ""), ("L", 20, 23.5, "R05", ""), ("L", 13, 13.5, "R05", ""), ("L", 13, 23.5, "R05", ""), ("S", 22.6, 9.4, "R02", "at the suite door, 2-way"),
    ("S", 22.6, 21.6, "R05", "bedside, 2-way"), ("P", 22.6, 15.4, "R05", "bedside"), ("P", 22.6, 22.2, "R05", "bedside"),
    ("AC", 11.9, 22.5, "R05", "west wall, throws toward the bed foot, not the head"), ("ODU", 18, 25.6, "R05", "north wall, shaded"),
    ("P", 12.2, 24.6, "R05", "reading chair"),
    # Pooja (west of the dining)
    ("L", 43, 6, "R11", ""), ("WL", 44.6, 6, "R11", "lamp niche above the idols"), ("P", 42, 3.4, "R11", ""),
    ("S", 40.6, 8.4, "R14", "pooja switches outside, nook side"),
    ("L", 37, 6.5, "R14", ""), ("PC", 35, 3.4, "R14", "serving counter"), ("PC", 38, 3.4, "R14", "serving counter"),
    # Bath 2 (common, north)
    ("L", 25.5, 21.5, "R07", ""), ("EF", 26.6, 24.6, "R07", "out through the north wall"), ("G", 28.1, 23.0, "R07", "over shower"),
    ("PC", 28.1, 21.6, "R07", "by basin"), ("S", 26.8, 18.8, "R09", "Bath 2 switches outside the bath door"),
    # Hall, bedroom 2
    ("F", 30.5, 16, "R09", ""), ("L", 30.5, 12.5, "R09", ""), ("L", 25.5, 15.5, "R09", ""), ("L", 33, 20, "R09", ""), ("S", 26.9, 9.4, "R09", "at door"),
    ("S", 37.4, 9.4, "R09", "bedside, 2-way"), ("P", 37.6, 9.9, "R09", "bedside"), ("P", 31.2, 9.4, "R09", "bedside"),
    ("P", 28.9, 20.0, "R09", "work table"), ("U", 28.9, 20.8, "R09", "work table, monitor"), ("D", 28.9, 21.6, "R09", "work table"), ("U", 28.9, 22.4, "R09", "work table"), ("AC", 37.6, 18.6, "R09", "east wall, not at the work table"),
    ("WL", 32.2, 3.4, "R14", "over basin"),
    ("ODU", 33, 25.6, "R09", "north wall, shaded"),
    ("L", 42.5, 22, "R19", ""), ("P", 46.6, 24.6, "R19", ""),
    # Dining, pooja, sitting area
    ("L", 42.5, 15, "R10", "pendant"), ("WL", 38.4, 17.5, "R10", ""), ("P", 38.4, 16.2, "R10", ""), ("S", 46.6, 17.8, "R10", ""),
    ("L", 28.5, 6, "R14", ""), ("S", 23.4, 6.0, "R14", ""), ("INV", 24, 5.0, "R14", "lithium inverter in a ventilated cabinet under the bench"),
    # Wet area, wash link, kitchen
    ("L", 48, 5.5, "R13", "weatherproof"), ("P16", 46.4, 8.7, "R13", "washing machine"), ("P", 50.6, 6.0, "R13", "utility, weatherproof"),
    ("L", 60, 8, "R15", ""), ("WL", 59, 3.5, "R15", "under-cabinet"), ("WL", 64.5, 9, "R15", "under-cabinet"),
    ("CH", 64.6, 8.75, "R15", "duct out through east wall"), ("P16", 51.6, 4.4, "R15", "refrigerator, behind the fridge"),
    ("PC", 56, 3.5, "R15", "microwave / OTG"), ("PC", 61.5, 3.5, "R15", "mixer"), ("PC", 64.6, 6, "R15", ""), ("PC", 64.6, 11.5, "R15", ""),
    ("PC", 57.3, 3.5, "R15", "RO purifier, by sink"), ("S", 51.6, 9.2, "R15", "beside the sliding entry"),
    # Living, poomukham
    ("F", 53, 19, "R16", "long downrod"), ("L", 50, 22.5, "R16", ""), ("L", 56, 16, "R16", ""), ("WL", 47.4, 24.2, "R16", ""),
    ("TV", 58.6, 22.0, "R16", "TV + data + 2 sockets, east wall"), ("P", 47.4, 18.0, "R16", "sofa"), ("P", 50.6, 17.8, "R16", "floor socket, sofa end"),
    ("AC", 47.4, 21.5, "R16", "west wall"), ("ODU", 57.5, 25.6, "R16", "north wall, shaded"),
    ("S", 58.6, 18.6, "R16", "main switch at door"), ("DB", 57.2, 13.4, "R16", "SE of living, near entry"), ("U", 58.4, 13.4, "R16", "router"),
    ("L", 62, 16, "R17", ""), ("L", 62, 22, "R17", ""), ("BELL", 59.4, 18.6, "R17", ""), ("CAM", 64.5, 24.6, "R17", "covers gate and door"),
    ("P", 59.4, 24.0, "R17", "outdoor, weatherproof"), ("S", 59.4, 19.2, "R17", ""),
    # Site
    ("MTR", 74.6, 23.0, "SITE", "meter in compound wall by gate"), ("GL", 74.6, 14.5, "SITE", "gate light"),
    ("EP", 66.2, 1.5, "SITE", "earth pit 1"), ("EP", 73.5, 1.5, "SITE", "earth pit 2"), ("GL", 2.5, 8, "SITE", "rear garden"),
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
    ("WC", 24.0, 24.0, "R07", "wall-hung on the north (outer) wall"), ("HF", 23.4, 22.4, "R07", ""), ("BS", 27.8, 20.3, "R07", "on 7 in wet wall"),
    ("SH", 28.1, 24.0, "R07", ""), ("FT", 27.0, 24.2, "R07", "linear drain along the north wall"), ("FT", 25.3, 20.6, "R07", "dry zone trap"),
    ("SK", 49.85, 4.6, "R13", "utility sink"), ("WM", 46.45, 7.85, "R13", ""), ("FT", 47.8, 3.6, "R13", "floor falls out to the walkway"), ("TAP", 50.6, 3.4, "R13", "bucket tap, low"),
    ("BS", 32.2, 4.3, "R14", "counter basin, waste straight out to the south walkway"),
    ("SK", 58.5, 3.5, "R15", "single bowl + drainboard, under window"), ("RO", 57.3, 3.5, "R15", ""), ("FT", 62, 12.5, "R15", "cleaning trap"),
    ("TAP", 67.6, 13.6, "SITE", "foot-wash tap at steps"), ("TAP", 4.4, 10, "SITE", "garden tap"), ("TAP", 70.5, 22.0, "SITE", "tulsi / garden tap"),
    ("IC", 3.6, 19.5, "SITE", "IC-1 soil"), ("IC", 24.0, 26.6, "SITE", "IC-2 soil"), ("IC", 3.6, 26.6, "SITE", "IC-3 soil"), ("IC", 12, 26.6, "SITE", "IC-4 soil"),
    ("GT", 58.5, 1.0, "SITE", "grease trap"), ("IC", 47.8, 1.0, "SITE", "IC-5 grey"), ("IC", 27.0, 26.0, "SITE", "IC-6 grey"),
    ("IC", 4.2, 1.0, "SITE", "IC-7 grey"), ("IC", 4.2, 26.0, "SITE", "IC-8 grey"), ("IC", 9.6, 26.0, "SITE", "IC-9 ensuite grey"),
]
# Pipe runs (schematic): kind, list of points. South walkway: grey y=1.0, soil y=1.8, supply y=2.3 (on plinth face).
PIPES = [
    ("supply", [(1.7, 7.5), (1.7, 2.3), (64, 2.3)]),
    ("supply", [(49.85, 2.3), (49.85, 3)]), ("supply", [(32.2, 2.3), (32.2, 3)]), ("supply", [(58.5, 2.3), (58.5, 3)]),
    ("supply", [(1.7, 7.5), (4.4, 7.5), (4.4, 21), (5, 21)]),
    ("supply", [(4.4, 21), (4.4, 25.7), (26.0, 25.7), (26.0, 25.4)]),
    ("supply", [(64, 2.3), (66, 2.3), (66, 13.6), (67.6, 13.6)]),
    ("soil", [(6.3, 19.5), (3.6, 19.5), (3.6, 27.5), (2.5, 29)]),
    ("soil", [(24.0, 24.0), (24.0, 26.6), (3.6, 26.6)]),
    ("grey", [(58.5, 3.5), (58.5, 1.0), (4.2, 1.0), (4.2, 26.0), (8.6, 30.5), (10, 32)]),
    ("grey", [(47.8, 3.6), (47.8, 1.0)]), ("grey", [(32.2, 4.3), (32.2, 1.0)]), ("grey", [(49.85, 4.6), (47.8, 3.6)]), ("grey", [(46.45, 7.85), (47.8, 3.6)]), ("grey", [(27.8, 20.3), (25.3, 20.6), (27.0, 24.2), (27.0, 26.0), (27.0, 29.4), (12, 29.4), (10, 32)]),
    ("grey", [(9.6, 20.2), (9.6, 26.0), (10, 32)]), ("grey", [(8.25, 24.5), (9.6, 24.5)]),
    ("rain", [(2.5, 0.5), (74.6, 0.5), (74.6, 23), (74.5, 25)]),
    ("rain", [(2.5, 27.5), (2.5, 28.2), (67.5, 28.2), (71.5, 32)]), ("rain", [(67.5, 27.5), (67.5, 28.2)]),
    ("rain", [(71, 26.5), (71.5, 30.5)]),
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
