"""Output locations for the generated package, relative to the project root."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REV = "RevB"
PDF = ROOT / "02_Drawings" / "PDF" / f"KH-P1_Drawing_Set_{REV}.pdf"
DXF = ROOT / "02_Drawings" / "CAD" / f"KH-P1_A-102_Ground_Floor_Plan_{REV}.dxf"
XLSX = ROOT / "03_Schedules" / f"KH-P1_Schedules_{REV}.xlsx"
HTML_3D = ROOT / "04_3D" / "KH-P1_3D_Model.html"
GUIDE_MD = ROOT / "01_Brief" / "Room_Detailing_Guide.md"
