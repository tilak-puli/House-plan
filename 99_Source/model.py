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
SITE = {"w": 27, "l": 70, "strip": 10}  # plot width (N-S), length (E-W), owned north strip, ft
T = 0.75  # outer wall thickness, ft (9 in finished)

ROOMS = [  # id, name, x1, x2, y1, y2, zone
    ("R01", "Office 2", 5, 14, 3, 11, "Master suite"),
    ("R02", "Walk-in wardrobe", 14, 21, 3, 11, "Master suite"),
    ("R03", "Dressing alcove", 5, 11.5, 11, 17, "Master suite"),
    ("R04", "Ensuite", 5, 11.5, 17, 25, "Master suite"),
    ("R05", "Master bedroom", 11.5, 21, 11, 25, "Master suite"),
    ("R07", "Bath 2 (common)", 33, 42, 19, 25, "Service"),
    ("R08", "Hall", 21, 33, 11, 15.5, "Circulation"),
    ("R09", "Bedroom 2", 21, 33, 15.5, 25, "Private"),
    ("R10", "Dining", 33, 42, 11, 19, "Living"),
    ("R11", "Pooja", 21, 30, 3, 11, "Living"),
    ("R12", "Store", 30, 42, 3, 11, "Service"),
    ("R13", "Wet area (semi-open)", 42, 50, 3, 9, "Service"),
    ("R14", "Wash link", 42, 50, 9, 13, "Circulation"),
    ("R15", "Kitchen", 50, 60, 3, 13, "Service"),
    ("R16", "Living", 42, 54, 13, 25, "Living"),
    ("R17", "Poomukham (verandah)", 54, 60, 13, 25, "Entry"),
]

# Walls: (axis, coordinate, start, end). axis "X" = runs along x at y=c; "Y" = runs along y at x=c.
WALLS = [
    ("X", 3, 5, 60), ("Y", 5, 3, 25), ("X", 25, 5, 54), ("Y", 60, 3, 13), ("Y", 54, 13, 25),
    ("Y", 14, 3, 11), ("X", 11, 5, 21), ("X", 17, 5, 11.5), ("Y", 11.5, 17, 25), ("Y", 21, 3, 25),
    ("X", 11, 21, 30), ("X", 11, 30, 42), ("Y", 30, 3, 11), ("X", 15.5, 21, 33), ("Y", 33, 15.5, 25),
    ("X", 19, 33, 42), ("Y", 42, 19, 25), ("Y", 42, 3, 11), ("X", 9, 42, 50), ("Y", 50, 3, 9),
    ("X", 13, 50, 60), ("X", 13, 44, 48),
]
EXTERIOR = {("X", 3), ("Y", 5), ("X", 25), ("Y", 60), ("Y", 54)}
# Wall types (finished thickness, ft). AAC blocks in an RCC frame; walls carrying concealed plumbing are thicker
# so pipe chases do not cut a 4 in block in half.
WALL_TYPES = {
    "EXT": (0.75, "200 mm AAC + 20 mm external plaster + 12 mm internal plaster (~9 in)"),
    "WET": (0.58, "150 mm AAC + plaster both faces (~7 in): concealed plumbing walls"),
    "INT": (0.42, "100 mm AAC + plaster both faces (~5 in)"),
}
EXTRA_EXT_WALLS = {("X", 13, 50, 60)}  # kitchen north wall faces the open poomukham
WET_WALLS = {("X", 17, 5, 11.5), ("X", 19, 33, 42), ("Y", 42, 19, 25)}  # ensuite basin wall; Bath 2 basin and shower walls

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
    "R08": "Red oxide / Kota stone", "R10": "Red oxide / Kota stone", "R16": "Red oxide / Kota stone",
    "R01": "Matt vitrified 2x2", "R02": "Matt vitrified 2x2", "R03": "Matt vitrified 2x2", "R05": "Matt vitrified 2x2",
    "R09": "Matt vitrified 2x2", "R12": "Matt vitrified 2x2",
    "R11": "Marble / teak (pooja)", "R15": "Anti-skid matt vitrified", "R04": "Anti-skid ceramic, waterproofed",
    "R07": "Anti-skid ceramic, waterproofed", "R13": "Rough Cuddapah / Kota, falls", "R14": "Rough Cuddapah / Kota, falls",
    "R17": "Flamed granite",
}
ROOM_FLOOR = {"R04": -0.04, "R07": -0.04, "R13": -0.25, "R17": -0.5}  # offset from FFL
# ceiling: ("flat", height above FFL) or ("sloped", note)
CEILINGS = {
    "R01": ("flat", 9.5), "R02": ("flat", 9.5), "R03": ("flat", 9.5), "R04": ("flat", 8.5), "R05": ("flat", 9.5),
    "R07": ("flat", 8.5), "R08": ("flat", 9.5), "R09": ("flat", 9.5),
    "R10": ("sloped", "open to ventilator"), "R11": ("flat", 9.5), "R12": ("flat", 9.5), "R13": ("sloped", "open truss"),
    "R14": ("sloped", "open truss"), "R15": ("flat", 9.5), "R16": ("sloped", "follows roof"), "R17": ("sloped", "exposed rafters"),
}
ROOF = {
    "pitch": 30,          # degrees
    "overhang": 2.5,      # eaves beyond the outer wall centreline
    "hip": (2.5, 62.5, 0.5, 27.5),     # eaves outline x1, x2, y1, y2
    "gable": (52, 62.5, 11.5, 26.5),   # front mukhappu gable outline over the poomukham, ridge E-W
    "gable_lift": 0.24,   # gable eaves sit just above the hip eaves
    "skylight": (35, 40, 12, 17),      # dining ventilator footprint (no glass)
    "vent_sill": 0.75,    # ventilator sill (top of upstand) above the ridge: 9 in minimum
    "vent_louvre": 2.0,   # louvre band height, all four sides (about 20 sq ft free vent area)
    "vent_overhang": 1.5, # hipped cap overhang beyond the louvres
    "downpipes": [(2.5, 0.5), (22, 0.5), (42, 0.5), (62.5, 0.5), (2.5, 27.5), (22, 27.5), (42, 27.5), (62.5, 27.5)],
}

# Site features: id, label, kind ("rect"/"circle"), geometry (x1, x2, y1, y2) or (x, y, r)
SITE_FEATURES = [
    ("TANK", "Overhead tank on 18 ft stand (SW), ladder to roof", "rect", (0.4, 3.0, 6, 9)),
    ("SEPTIC", "Septic tank, 2 chambers (NW, in north strip)", "rect", (0.8, 4.2, 29, 35)),
    ("SOAK", "Soak pit, grey water (6 ft+ from house)", "circle", (10, 32, 2.0)),
    ("SUMP", "Sump (NE)", "rect", (66, 69.5, 23.5, 26.5)),
    ("BORE", "Borewell (if any), NE", "circle", (63, 25.6, 0.5)),
    ("RWH", "Rainwater recharge pit (sump overflow)", "circle", (66.5, 32, 1.5)),
    ("PERGOLA", "Creeper pergola for west shade (no big trees near walls)", "rect", (0.3, 4.2, 10.5, 24)),
    ("TULSI", "Tulsi thara", "circle", (64.5, 14, 0.6)),
    ("BAY", "Two-wheeler bay", "rect", (61, 69, 3, 11)),
    ("GATE", "Gate", "rect", (70, 70.5, 15, 22)),
    ("STEPS", "Entrance steps (3 risers)", "rect", (60.375, 62.0, 19, 23)),
    ("FEET", "Foot-wash tap + drain", "circle", (62.8, 18.2, 0.35)),
    ("APRON", "Plinth protection apron 3 ft, sloped away", "apron", (2, 63, 0, 28)),
]
TREES = [(40, 33.5, 3), (54, 34.5, 2), (22, 34, 2.5), (30, 34.5, 2)]  # kept 8 ft+ from walls: roots dry out black cotton soil
JALI_SCREENS = [("X", 13, 42, 44), ("X", 13, 48, 50)]  # free-standing timber jali, living / link

# Doors: id, axis, c, s, e, swing (+1 toward +y/+x, -1 toward -y/-x, 0 = sliding), name, type
DOORS = [
    ("D01", "Y", 54, 19.5, 22.5, -1, "Main entrance", "Teak panelled, double leaf"),
    ("D02", "X", 3, 42.5, 44.5, +1, "Service door, wet area", "Steel frame + grille, insect mesh"),
    ("D03", "X", 11, 8, 14, 0, "Office 2 to master", "Sliding, laminated glass + brush seals"),
    ("D04", "X", 11, 17, 19.5, -1, "Walk-in wardrobe", "Flush, teak veneer"),
    ("D05", "Y", 11.5, 19, 21.5, -1, "Ensuite", "Flush, waterproof (WPC/FRP)"),
    ("D06", "Y", 21, 11.5, 14.5, -1, "Master bedroom", "Flush, teak veneer"),
    ("D08", "X", 19, 33.5, 36, +1, "Bath 2 (common)", "Flush, waterproof (WPC/FRP)"),
    ("D09", "X", 11, 38, 40.5, -1, "Store", "Flush, teak veneer"),
    ("D10", "X", 15.5, 28.5, 31.5, +1, "Bedroom 2", "Flush, teak veneer"),
    ("D11", "X", 11, 24.5, 27.5, -1, "Pooja", "Carved teak, double leaf"),
    ("D12", "Y", 50, 5.5, 8, -1, "Kitchen to wet area", "Flush, waterproof (WPC/FRP)"),
]
# Vents above inner doors (7'-6" to 9'-0", above the lintel band): air moves between rooms with doors shut
TRANSOM_TYPES = {
    "jali": "Teak jali vent in a frame: air passes freely (rooms with no sound-privacy need)",
    "jali_closable": "Teak jali with a sliding timber shutter on the room side: open for air, shut for sound privacy",
    "louvre": "Fixed louvres angled down: air for the exhaust fan, no view in",
    "glazed": "Top-hung glazed vent with seals: open for air, closed for calls",
}
TRANSOMS = {"D03": "glazed", "D04": "jali", "D09": "jali", "D11": "jali", "D12": "louvre"}
# None at bedrooms (big north windows, shallow rooms; master also ventilates through Office 2) or bathrooms (door bottom louvre feeds the fan)
TRANSOM_LABELS = {"jali": "Open jali", "jali_closable": "Closable jali", "louvre": "Louvres", "glazed": "Sealed glazed flap"}
TRANSOM_Z = (7.5, 9.0)  # sill and head above FFL

# Windows: id, axis, c, s, e, sill, head, room, type
WINDOWS = [
    ("W01", "X", 3, 7, 12, 3, 7, "Office 2", "Timber jali + glazed shutters"),
    ("W02", "X", 3, 16, 19, 5, 7, "Walk-in wardrobe", "High vent, jali"),
    ("W03", "X", 3, 23, 28, 3, 7, "Pooja", "Timber jali + glazed shutters"),
    ("W04", "X", 3, 33.5, 35.5, 5, 7, "Store", "High vent, jali + mesh"),
    ("W05", "X", 3, 37.5, 40.5, 5, 7, "Store", "High vent, jali + mesh"),
    ("W06", "X", 3, 44.5, 49.6, 0.4, 8, "Wet area", "Terracotta jali wall + insect mesh + MS grille"),
    ("W07", "X", 3, 52, 57, 3.5, 7, "Kitchen", "Timber jali + glazed shutters"),
    ("W08", "Y", 60, 5, 11, 3.5, 7, "Kitchen", "Timber jali + glazed shutters"),
    ("W09", "X", 25, 6, 9, 5, 7, "Ensuite", "Frosted casement"),
    ("W10", "Y", 5, 19, 23, 5, 7, "Ensuite", "High jali vent"),
    ("W11", "X", 25, 13, 19, 3, 7, "Master bedroom", "Teak casement, glazed"),
    ("W12", "X", 25, 24, 30, 3, 7, "Bedroom 2", "Teak casement, glazed"),
    ("W13", "X", 25, 35, 38, 5, 7, "Bath 2 (common)", "Frosted casement, top-hung vent"),
    ("W14", "X", 25, 43, 51, 2, 8, "Living", "Teak casement, tall, glazed"),
    ("W15", "Y", 54, 14, 18, 3, 7, "Living", "Teak casement onto poomukham (morning light)"),
]
OTHER_OPENINGS = [
    ("SK1", "Ventilator over dining, 5 x 5 ft, no glass: hipped tiled cap at 30 deg with 1'-6\" overhang; 2 ft band of 45 deg louvres on all four sides; SS insect mesh behind; sealed inner shutters on a winding opener; 9 in upstand; lined shaft to the dining ceiling (see A-503)"),
    ("GV1-3", "Three glazed/jali vents in front gable (mukhappu), morning light into living"),
]
PILLARS = [(59.4, 13.6), (59.4, 18.4), (59.4, 23.6), (56.5, 24.4), (54.6, 24.4)]

# Furniture: id, room, item, x1, x2, y1, y2, qty, material / spec, shape ("rect"|"circle"|"wc"|"glass")
FURNITURE = [
    ("F01", "Office 2", "Work desk 5'6\" x 2'", 12, 13.9, 4, 9.5, 1, "Teak or ply + veneer, cable tray", "rect"),
    ("F02", "Office 2", "Ergonomic task chair", 10.6, 11.8, 6.2, 7.4, 1, "Mesh back", "circle"),
    ("F03", "Office 2", "Bookshelf, full height (video backdrop)", 5.3, 6.5, 3.5, 10.5, 1, "Teak / ply, open shelves", "rect"),
    ("F04", "Walk-in wardrobe", "Wardrobe run, south wall", 14.3, 20.7, 3.3, 5.3, 1, "Ply + laminate, 2 ft deep", "rect"),
    ("F05", "Walk-in wardrobe", "Wardrobe run, east wall", 19, 20.7, 5.5, 10.7, 1, "Ply + laminate", "rect"),
    ("F06", "Dressing alcove", "Dresser with mirror", 5.3, 6.8, 12, 16, 1, "Teak", "rect"),
    ("F07", "Ensuite", "Vanity basin counter 3'-6\"", 7.2, 10.7, 17.3, 18.8, 1, "Granite top, wall-hung", "rect"),
    ("F08", "Ensuite", "WC (EWC)", 5.4, 7.2, 18.9, 20.1, 1, "Wall-hung, concealed cistern", "wc"),
    ("F09", "Ensuite", "Shower glass partition", 5.3, 9.0, 21.9, 22.1, 1, "8 mm toughened glass", "glass"),
    ("F10", "Master bedroom", "Queen bed 5' x 6'6\" + headboard", 14.2, 20.6, 16, 21, 1, "Teak, head to east", "rect"),
    ("F11", "Master bedroom", "Bedside table", 19.3, 20.3, 14.8, 15.9, 2, "Teak", "rect"),
    ("F12", "Master bedroom", "Reading chair", 12.0, 13.4, 22.6, 24.0, 1, "Cane / upholstered", "circle"),
    ("F16", "Bath 2 (common)", "WC (EWC)", 35.6, 37.0, 23.4, 24.6, 1, "Wall-hung on the north wall, concealed cistern", "wc"),
    ("F17", "Bath 2 (common)", "Wash basin", 36.6, 38.6, 19.3, 20.0, 1, "Wall-hung", "rect"),
    ("F18", "Bath 2 (common)", "Shower glass partition", 38.9, 39.1, 19.4, 22.8, 1, "8 mm toughened glass", "glass"),
    ("F20", "Bedroom 2", "Queen bed 5' x 6'6\" (or 4'6\" double)", 22, 27, 15.9, 22.4, 1, "Teak, head to south", "rect"),
    ("F21", "Bedroom 2", "Bedside table", 27.2, 28.3, 16.0, 17.1, 1, "Teak", "rect"),
    ("F22", "Bedroom 2", "Study desk 3'-4\" (beside the foot of the bed)", 27.5, 30.8, 23.2, 24.6, 1, "Teak / ply", "rect"),
    ("F23", "Bedroom 2", "Built-in wardrobe 6'", 31, 33, 19, 25, 1, "Ply + laminate, sound buffer to Bath 2", "rect"),
    ("F24", "Dining", "Dining table 5' x 3', 6-seat", 35.5, 40.5, 13.5, 16.5, 1, "Teak or rosewood", "rect"),
    ("F25", "Dining", "Dining chair", 35.8, 36.9, 12.3, 13.3, 6, "Teak + cane", "rect"),
    ("F26", "Pooja", "Pooja mandapam on the west wall (idol faces east)", 21.3, 21.9, 5.0, 9.0, 1, "Carved teak", "rect"),
    ("F27", "Pooja", "Pooja cupboard", 28.6, 29.7, 3.4, 6.4, 1, "Teak", "rect"),
    ("F28", "Store", "Shelving, L-shaped, with suitcase loft", 30.3, 41.7, 3.3, 4.8, 1, "MS or ply, 1.5 ft deep", "rect"),
    ("F29", "Wet area", "Double-bowl utility sink counter", 45, 49, 3.4, 5.3, 1, "Kadappa / granite, SS sinks", "rect"),
    ("F30", "Wet area", "Washing machine bay 2' x 2'", 42.4, 44.3, 6.5, 8.5, 1, "Splash-proof socket, floor drain", "rect"),
    ("F31", "Wet area", "Ceiling pulley clothes airer", 45.5, 49.5, 6, 8.5, 1, "Aluminium", "glass"),
    ("F32", "Wash link", "Hand-wash basin 16-20 in", 42.3, 44.3, 9.4, 10.5, 1, "Ceramic, wall-hung", "rect"),
    ("F33", "Wash link", "Crockery / serving unit, 1 ft deep", 44.6, 49.7, 9.4, 10.3, 1, "Teak + glass shutters", "rect"),
    ("F34", "Kitchen", "L-counter, south run", 50.4, 59.6, 3.4, 5.4, 1, "Granite top, ply carcass", "rect"),
    ("F35", "Kitchen", "L-counter, east run (hob)", 57.6, 59.6, 5.4, 12.4, 1, "Granite top, cook faces east", "rect"),
    ("F36", "Kitchen", "Refrigerator space", 52, 54.3, 10.6, 12.6, 1, "Double-door, 2'6\" wide", "rect"),
    ("F37", "Living", "TV unit + 50-55 in TV", 44.3, 47.7, 13.2, 14.4, 1, "Teak, on solid wall in screen", "rect"),
    ("F38", "Living", "Three-seat sofa 6'6\"", 43, 49.5, 22, 24.7, 1, "Teak frame, cotton cushions", "rect"),
    ("F39", "Living", "Coffee table 3'6\" x 2'", 44.5, 48, 18.5, 20.5, 1, "Teak", "rect"),
    ("F40", "Living", "Morning armchair by east window", 51.5, 53.5, 14.5, 16.5, 1, "Cane / teak", "circle"),
    ("F41", "Poomukham (verandah)", "Oonjal (swing) 3'6\"", 55, 58.5, 15.5, 17, 1, "Teak, chains to beam", "rect"),
    ("F42", "Poomukham (verandah)", "Arugu seats (built-in)", 58.8, 60, 13.9, 18.1, 2, "Laterite base, teak top", "rect"),
]
# extra placements (same item, additional copies drawn on plan)
EXTRA_DRAW = [
    ("F11", 19.3, 20.3, 21.1, 22.2), ("F25", 37.5, 38.6, 12.3, 13.3), ("F25", 39.2, 40.3, 12.3, 13.3),
    ("F25", 35.8, 36.9, 16.7, 17.7), ("F25", 37.5, 38.6, 16.7, 17.7), ("F25", 39.2, 40.3, 16.7, 17.7),
    ("F28", 30.3, 31.5, 5, 10.7), ("F42", 54, 58.8, 24, 25),
]

FINISHES = [  # spaces, floor, walls (incl. skirting / dado), ceiling, notes
    ("Living, dining, hall", "Red oxide (IPS) or polished Kota / Tandur stone", "4 in flush skirting in floor stone; lime-finish or mineral paint", "Sloped, follows roof, insulated board under deck", "Stone hides dust better than glossy white tile"),
    ("Bedrooms, offices, dressing, walk-in", "Matt vitrified 2x2 ft or red oxide", "4 in flush skirting; putty + washable emulsion", "False ceiling at 9'-6\", 50 mm insulation above", "Ventilated attic above false ceiling"),
    ("Pooja", "White marble or teak", "Teak panelling behind idol; 4 in marble skirting", "Teak / board at 9'-6\"", "Idol on west wall facing east; lamp niche with heat-proof back"),
    ("Kitchen", "Anti-skid matt vitrified or Kota, mid-tone", "Tile / stone full height between counter and wall cabinets", "Moisture-resistant board at 9'-6\"", "Counter granite (local Ongole / Chimakurthy), 2 ft deep"),
    ("Ensuite, Bath 2", "Anti-skid ceramic (R11), falls 1:60 to drain", "Tiles to 7 ft; full height in shower; waterproofing 12 in up all walls, 7 ft in shower", "Moisture-resistant board / PVC at 8'-6\"", "12 mm step down, no raised threshold"),
    ("Wet area, wash link", "Rough Cuddapah / Kota stone, falls to drain", "4 ft stone or tile dado", "Open truss", "6 in kerb under jali wall stops rain blowing in"),
    ("Store, walk-in", "Red oxide or vitrified", "4 in flush skirting; washable paint", "Board at 9'-6\"", ""),
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
    ("Services", "Groundwater: test TDS, hardness, fluoride. Plan RO for drinking and a softener for bathrooms if hardness is high", "Plumber / owner", "Open"),
    ("Services", "Septic and soak pit sizes; keep soak pits and gardens 6 ft+ from foundations in expansive soil", "Engineer", "Open"),
    ("Services", "Electrical load (with ACs), service connection size, earthing, inverter / solar PV", "Electrical engineer", "Open"),
    ("Phase 2", "Phase 2 on the north strip will block north light and sits on the septic: plan the split now", "Architect", "Deferred by owner"),
    ("Vastu", "Bed head east (master), NW ensuite, common bath at north-centre (many schools avoid toilets in the north), central dining, pooja west of centre with idol facing east, DB in SE-ish living wall", "Vastu consultant", "To confirm"),
    ("Climate", "Roof heat: insulation, ventilated attic, ventilator lantern louvres and shutters; ODU positions on shaded walls", "Architect", "Open"),
    ("Levels", "Survey road and field levels; plinth at 2 ft above finished ground (raise if site floods)", "Surveyor / architect", "Open"),
]

DECISIONS = [
    "Site is in Guntur, Andhra Pradesh (farm land), not Kerala; Kerala style kept, construction adapted to local climate and soil.",
    "Plot 27 ft x 70 ft, road on east; house 55 ft x 22 ft kept; owner accepts local practice on side setbacks (to be checked).",
    "RCC frame with AAC block walls: 9 in outer, 5 in inner, 7 in where plumbing is concealed.",
    "Plinth 2 ft above finished ground; poomukham 6 in lower; bathrooms 12 mm lower with no raised threshold.",
    "AC provisions (points, sleeves, drain, outdoor-unit brackets) in both bedrooms, the office and living; passive cooling first.",
    "Flat insulated false ceilings in bedrooms, offices, baths and kitchen; sloped ceilings in living, dining and verandah.",
    "No glass skylight: the dining gets borrowed daylight from the living, wash link and hall; a louvred ventilator lantern above it lets hot air out (no glass, so no greenhouse heat).",
    "Courtyard removed; the dining hall at plot centre keeps the Brahmasthan open, with the ventilator above.",
    "Single storey, no internal stair; roof access by fixed ladder; water tank on stand in SW rear garden.",
    "Service band on south (heat buffer); bedrooms and living get north light.",
    "Kitchen in SE; stove on east wall; semi-open wet area with jali; separate dry store.",
    "Bedroom doors widened to 3 ft; bathroom, office and store doors 2 ft 6 in.",
    "Office 1 removed after family review: one office (Office 2) inside the master suite; Bedroom 2 has its own work desk.",
    "Common bathroom moved to the north side (old pooja spot), entered from the dining corner next to the hall.",
    "Pooja moved west of the dining, to the old Office 1 spot off the hall, idol on the west wall facing east; store doubled to 12 x 8 ft.",
    "Hall widened to 4 ft clear (Bedroom 2 gives up 6 in); vents above the office, walk-in, store, pooja and kitchen doors; none at bedrooms or bathrooms (sound privacy).",
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
    ("Openings", "Vents above inner doors", "Office: top-hung glazed flap with seals; walk-in, store, pooja: open jali; kitchen-wet area: louvres; bedrooms and bathrooms: none. 7'-6\" to 9'-0\" above the lintel band", "Air moves with doors shut where privacy allows; bedrooms rely on their north windows, fans and AC"),
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
    ("F", 9.5, 7, "R01", ""), ("L", 9.5, 9.5, "R01", ""), ("L", 9.5, 4.5, "R01", ""), ("S", 7.4, 10.6, "R01", "by sliding door"),
    ("U", 13.6, 5, "R01", "desk"), ("D", 13.6, 6, "R01", "desk"), ("P", 13.6, 8, "R01", "desk"), ("AC", 6.5, 10.6, "R01", "throws south, not at the desk"),
    ("ODU", 4.2, 6.5, "R01", "west wall, high"),
    # Walk-in, dressing, ensuite
    ("L", 17.5, 7, "R02", ""), ("S", 19.6, 10.6, "R02", ""), ("P", 14.5, 10.6, "R02", "iron"),
    ("L", 8.25, 14, "R03", ""), ("WL", 5.4, 14, "R03", "mirror"), ("P", 5.4, 16.4, "R03", "hair dryer"),
    ("L", 8.25, 20.5, "R04", ""), ("EF", 5.4, 24, "R04", "out through west wall"), ("G", 8.3, 24.6, "R04", "over shower"),
    ("PC", 10.9, 18.6, "R04", "shaver, by basin"), ("S", 11.9, 22.0, "R05", "ensuite switches outside the door"),
    # Master bedroom
    ("F", 15.5, 18.5, "R05", ""), ("L", 13, 13.5, "R05", ""), ("L", 13, 23.5, "R05", ""), ("S", 20.6, 15.0, "R05", "at door, 2-way"),
    ("S", 20.6, 21.6, "R05", "bedside, 2-way"), ("P", 20.6, 15.4, "R05", "bedside"), ("P", 20.6, 22.2, "R05", "bedside"),
    ("AC", 15.5, 11.4, "R05", "on south wall, not over the bed head"), ("ODU", 16, 25.6, "R05", "north wall, shaded"),
    ("P", 12.2, 24.6, "R05", "reading chair"),
    # Pooja (west of the dining)
    ("F", 25.5, 7, "R11", "small fan"), ("L", 25.5, 9.3, "R11", ""), ("WL", 21.4, 7, "R11", "lamp niche above the idol"),
    ("P", 29.6, 8, "R11", ""), ("S", 28.0, 10.6, "R11", "at door"),
    # Bath 2 (common, north)
    ("L", 37.5, 21.8, "R07", ""), ("EF", 40.5, 24.6, "R07", "out through north wall"), ("G", 41.6, 23.6, "R07", "over shower"),
    ("PC", 38.9, 19.4, "R07", "by basin"), ("S", 36.4, 18.6, "R10", "Bath 2 switches outside, dining side"),
    # Hall, bedroom 2
    ("L", 24, 13.25, "R08", ""), ("L", 30, 13.25, "R08", ""), ("S", 22, 11.4, "R08", "2-way"),
    ("F", 27, 20.25, "R09", ""), ("L", 24, 18.5, "R09", ""), ("L", 30, 22.5, "R09", ""), ("S", 32.6, 15.9, "R09", "at door"),
    ("S", 27.9, 15.9, "R09", "bedside, 2-way"), ("P", 28.3, 15.9, "R09", "bedside"), ("P", 21.4, 16.6, "R09", "bedside"),
    ("P", 30.2, 24.6, "R09", "work desk"), ("D", 28.6, 24.6, "R09", "work desk"), ("U", 29.4, 24.6, "R09", "work desk"), ("AC", 21.4, 21, "R09", "west wall, not over bed head"),
    ("ODU", 22.5, 25.6, "R09", "north wall, shaded"),
    # Dining, pooja, store
    ("L", 37.5, 15, "R10", "pendant"), ("WL", 33.4, 15, "R10", ""), ("P", 33.4, 12, "R10", ""), ("P", 41.6, 12, "R10", ""), ("S", 41.6, 17.8, "R10", ""),
    ("L", 39, 7.5, "R12", ""), ("S", 40.8, 10.6, "R12", ""), ("INV", 38.5, 9.6, "R12", "ventilated, on the store's inside wall"),
    # Wet area, wash link, kitchen
    ("L", 46, 6, "R13", "weatherproof"), ("P16", 43.3, 8.6, "R13", "washing machine"), ("P", 48.6, 5.5, "R13", "utility"),
    ("L", 46, 11, "R14", ""), ("WL", 43.3, 10.8, "R14", "over basin"), ("S", 49.6, 12.6, "R14", ""),
    ("L", 55, 8, "R15", ""), ("WL", 54, 3.5, "R15", "under-cabinet"), ("WL", 59.5, 9, "R15", "under-cabinet"),
    ("CH", 59.6, 8.75, "R15", "duct out through east wall"), ("P16", 53.1, 12.6, "R15", "refrigerator"),
    ("PC", 51, 3.5, "R15", "microwave / OTG"), ("PC", 56.5, 3.5, "R15", "mixer"), ("PC", 59.6, 6, "R15", ""), ("PC", 59.6, 11.5, "R15", ""),
    ("PC", 52.3, 3.5, "R15", "RO purifier, by sink"), ("S", 50.4, 9.6, "R15", "at entry"), ("EF", 50.4, 5, "R15", "to wet area"),
    # Living, poomukham
    ("F", 48, 19, "R16", "long downrod"), ("L", 45, 22.5, "R16", ""), ("L", 51, 16, "R16", ""), ("WL", 42.4, 17, "R16", ""),
    ("TV", 46, 13.4, "R16", "TV + data + 2 sockets"), ("P", 44.2, 24.6, "R16", "sofa"), ("P", 50, 24.6, "R16", "sofa"),
    ("AC", 42.4, 21.5, "R16", "west wall"), ("ODU", 52.5, 25.6, "R16", "north wall, shaded"),
    ("S", 53.6, 23, "R16", "main switch at door"), ("DB", 52.5, 13.4, "R16", "SE of living, near entry"), ("U", 50.5, 13.4, "R16", "router"),
    ("L", 57, 16, "R17", ""), ("L", 57, 22, "R17", ""), ("BELL", 54.4, 23, "R17", ""), ("CAM", 59.5, 24.6, "R17", "covers gate and door"),
    ("P", 54.4, 14.5, "R17", "outdoor, weatherproof"), ("S", 54.4, 23.6, "R17", ""),
    # Site
    ("MTR", 69.6, 23.0, "SITE", "meter in compound wall by gate"), ("GL", 69.6, 14.5, "SITE", "gate light"),
    ("EP", 61.2, 1.5, "SITE", "earth pit 1"), ("EP", 68.5, 1.5, "SITE", "earth pit 2"), ("GL", 2.5, 8, "SITE", "rear garden"),
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
    ("WC", 36.3, 24.4, "R07", "wall-hung on the north (outer) wall"), ("HF", 35.4, 24.4, "R07", ""), ("BS", 37.6, 19.6, "R07", "on 7 in wet wall"),
    ("SH", 41.4, 22.5, "R07", "on 7 in wet wall"), ("FT", 41.2, 20.6, "R07", "linear drain along east wall"), ("FT", 37.5, 21.8, "R07", "dry zone trap"),
    ("SK", 47, 3.6, "R13", "double bowl utility sink"), ("WM", 43.3, 8.6, "R13", ""), ("FT", 46, 6.5, "R13", ""), ("TAP", 49.6, 7.5, "R13", "bucket tap, low"),
    ("BS", 43.3, 9.6, "R14", "hand-wash basin"),
    ("SK", 53.5, 3.5, "R15", "single bowl + drainboard, under window"), ("RO", 52.3, 3.5, "R15", ""), ("FT", 57, 12.5, "R15", "cleaning trap"),
    ("TAP", 62.8, 18.2, "SITE", "foot-wash tap at steps"), ("TAP", 4.4, 10, "SITE", "garden tap"), ("TAP", 64.5, 15.6, "SITE", "tulsi / garden tap"),
    ("IC", 3.6, 19.5, "SITE", "IC-1 soil"), ("IC", 36.3, 26.6, "SITE", "IC-2 soil"), ("IC", 3.6, 26.6, "SITE", "IC-3 soil"), ("IC", 20, 26.6, "SITE", "IC-4 soil"),
    ("GT", 53.5, 1.0, "SITE", "grease trap"), ("IC", 46, 1.0, "SITE", "IC-5 grey"), ("IC", 41.4, 26.0, "SITE", "IC-6 grey"),
    ("IC", 4.2, 1.0, "SITE", "IC-7 grey"), ("IC", 4.2, 26.0, "SITE", "IC-8 grey"), ("IC", 9.6, 26.0, "SITE", "IC-9 ensuite grey"),
]
# Pipe runs (schematic): kind, list of points. South walkway: grey y=1.0, soil y=1.8, supply y=2.3 (on plinth face).
PIPES = [
    ("supply", [(1.7, 7.5), (1.7, 2.3), (59, 2.3)]),
    ("supply", [(46, 2.3), (46, 3)]), ("supply", [(53.5, 2.3), (53.5, 3)]),
    ("supply", [(1.7, 7.5), (4.4, 7.5), (4.4, 21), (5, 21)]),
    ("supply", [(4.4, 21), (4.4, 25.7), (39.5, 25.7), (39.5, 25.4)]),
    ("supply", [(59, 2.3), (61, 2.3), (61, 18.2), (62.8, 18.2)]),
    ("soil", [(6.3, 19.5), (3.6, 19.5), (3.6, 27.5), (2.5, 29)]),
    ("soil", [(36.3, 24.4), (36.3, 26.6), (3.6, 26.6)]),
    ("grey", [(53.5, 3.5), (53.5, 1.0), (4.2, 1.0), (4.2, 26.0), (8.6, 30.5), (10, 32)]),
    ("grey", [(46, 6.5), (46, 1.0)]), ("grey", [(37.5, 21.8), (41.2, 20.6), (41.4, 26.0), (41.4, 29.4), (12, 29.4), (10, 32)]),
    ("grey", [(9.6, 20.2), (9.6, 26.0), (10, 32)]), ("grey", [(8.25, 24.5), (9.6, 24.5)]),
    ("rain", [(2.5, 0.5), (69.6, 0.5), (69.6, 23), (69.5, 25)]),
    ("rain", [(2.5, 27.5), (2.5, 28.2), (62.5, 28.2), (66.5, 32)]), ("rain", [(62.5, 27.5), (62.5, 28.2)]),
    ("rain", [(66, 26.5), (66.5, 30.5)]),
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
