from reportlab.pdfgen import canvas
from sheetlib import PW, PH, PROJECT, floor_sheet
from sheets_arch import (sheet_cover, sheet_basis, sheet_site, sheet_plan, sheet_furniture, sheet_working,
                         sheet_finishes, sheet_roof, sheet_schedules)
from sheets_elev import sheet_elev_long, sheet_elev_short, sheet_sections
from sheets_dw import sheet_doors_windows, sheet_windows_f1
from sheets_details import sheet_details_1, sheet_details_2, sheet_details_3
from sheets_mep import sheet_lighting, sheet_power, sheet_plumbing

SHEETS = [  # number, title, scale, function
    ("A-001", "Design basis and general notes", "-", sheet_basis),
    ("A-101", "Site plan and services", "1:100", sheet_site),
    ("A-102", "Ground floor plan", "1:75", floor_sheet(sheet_plan, "G", "A-102", "Ground floor plan")),
    ("A-103", "First floor plan", "1:75", floor_sheet(sheet_plan, "F1", "A-103", "First floor plan")),
    ("A-104", "Furniture layout, ground floor", "1:75", floor_sheet(sheet_furniture, "G", "A-104", "Furniture layout, ground floor")),
    ("A-105", "Furniture layout, first floor", "1:75", floor_sheet(sheet_furniture, "F1", "A-105", "Furniture layout, first floor")),
    ("A-106", "Working plan, ground floor: clear sizes and sections", "1:75", floor_sheet(sheet_working, "G", "A-106", "Working plan, ground floor: clear sizes and sections")),
    ("A-107", "Working plan, first floor: clear sizes", "1:75", floor_sheet(sheet_working, "F1", "A-107", "Working plan, first floor: clear sizes")),
    ("A-108", "Floor finishes and levels, ground floor", "1:75", floor_sheet(sheet_finishes, "G", "A-108", "Floor finishes and levels, ground floor")),
    ("A-109", "Floor finishes and levels, first floor", "1:75", floor_sheet(sheet_finishes, "F1", "A-109", "Floor finishes and levels, first floor")),
    ("A-110", "Roof plan", "1:75", sheet_roof),
    ("A-201", "North and south elevations", "1:100", sheet_elev_long),
    ("A-202", "East and west elevations", "1:100", sheet_elev_short),
    ("A-301", "Sections A-A and B-B", "1:100", sheet_sections),
    ("A-401", "Door details and ground-floor windows", "1:75", sheet_doors_windows),
    ("A-402", "Window details, first floor", "1:75", sheet_windows_f1),
    ("A-501", "Typical details 1: plinth, floor, window, eaves", "NTS", sheet_details_1),
    ("A-502", "Typical details 2: bath, kitchen, basin, AAC", "NTS", sheet_details_2),
    ("A-503", "Typical details 3: ridge ventilator", "NTS", sheet_details_3),
    ("A-601", "Schedules", "-", sheet_schedules),
    ("E-101", "Lighting, fans and ceilings, ground floor", "1:75", floor_sheet(sheet_lighting, "G", "E-101", "Lighting, fans and ceilings, ground floor")),
    ("E-102", "Lighting, fans and ceilings, first floor", "1:75", floor_sheet(sheet_lighting, "F1", "E-102", "Lighting, fans and ceilings, first floor")),
    ("E-103", "Power, AC and data, ground floor", "1:75", floor_sheet(sheet_power, "G", "E-103", "Power, AC and data, ground floor")),
    ("E-104", "Power, AC and data, first floor", "1:75", floor_sheet(sheet_power, "F1", "E-104", "Power, AC and data, first floor")),
    ("P-101", "Water supply and drainage", "1:100", sheet_plumbing),
]


def make(path):
    c = canvas.Canvas(path, pagesize=(PW, PH))
    c.setTitle(PROJECT["name"] + " - Pre-construction drawing set"); c.setAuthor("Owner, with Claude")
    index = [("A-000", "Cover and sheet index", "-")] + [(n, t, sc) for n, t, sc, _ in SHEETS]
    sheet_cover(c, index)
    for *_, fn in SHEETS:
        fn(c)
    c.save()


if __name__ == "__main__":
    from paths import PDF
    make(str(PDF))
