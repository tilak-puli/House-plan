"""Regenerate every drawing, schedule, the guide and the 3D model from model.py."""
import make_3d
import make_dxf
import make_guide
import make_pdf
import make_xlsx
from paths import DXF, GUIDE_MD, HTML_3D, PDF, ROOT, XLSX

for mod, out in ((make_pdf, PDF), (make_dxf, DXF), (make_xlsx, XLSX), (make_guide, GUIDE_MD), (make_3d, HTML_3D)):
    mod.make(str(out))
    print("wrote", out.relative_to(ROOT))
