from reportlab.pdfgen import canvas
from sheetlib import PW, PH, PROJECT
from sheets_arch import (sheet_cover, sheet_basis, sheet_site, sheet_plan, sheet_furniture, sheet_working,
                         sheet_finishes, sheet_roof, sheet_schedules)
from sheets_elev import sheet_elev_long, sheet_elev_short, sheet_sections
from sheets_dw import sheet_doors_windows
from sheets_details import sheet_details_1, sheet_details_2, sheet_details_3
from sheets_mep import sheet_lighting, sheet_power, sheet_plumbing

SHEETS = [  # number, title, scale, function
    ("A-001", "Design basis and general notes", "-", sheet_basis),
    ("A-101", "Site plan and services", "1:100", sheet_site),
    ("A-102", "Ground floor plan", "1:75", sheet_plan),
    ("A-103", "Furniture layout", "1:75", sheet_furniture),
    ("A-104", "Working plan: clear sizes and sections", "1:75", sheet_working),
    ("A-105", "Floor finishes and levels", "1:75", sheet_finishes),
    ("A-106", "Roof plan", "1:75", sheet_roof),
    ("A-201", "North and south elevations", "1:75", sheet_elev_long),
    ("A-202", "East and west elevations", "1:75", sheet_elev_short),
    ("A-301", "Sections A-A and B-B", "1:75", sheet_sections),
    ("A-401", "Door and window details", "1:60", sheet_doors_windows),
    ("A-501", "Typical details 1: plinth, floor, window, eaves", "NTS", sheet_details_1),
    ("A-502", "Typical details 2: bath, kitchen, basin, AAC", "NTS", sheet_details_2),
    ("A-503", "Typical details 3: dining ventilator", "NTS", sheet_details_3),
    ("A-601", "Schedules", "-", sheet_schedules),
    ("E-101", "Lighting, fans and ceilings", "1:75", sheet_lighting),
    ("E-102", "Power, AC and data", "1:75", sheet_power),
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
