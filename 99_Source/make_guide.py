"""Writes the room-by-room detailing guide (Markdown) from guide.py."""
from model import PROJECT, HOLD_POINTS
from guide import GUIDE

INTRO = """# Room-by-room detailing guide

{name}, {location}. Revision {rev}, {date}.

This guide lists the mistakes people most often regret in Indian homes, room by room, and what this design does instead.
"Shown on" points to the sheet in the drawing set (A-501/3 = detail 3 on sheet A-501).
Go through it with your architect, engineer and contractor; the same list is in the Excel workbook (Checklist tab) with a status column.

Site conditions that drive many of these points (Guntur): very hot summers (40-45 C), short heavy cyclonic rain,
expansive black cotton soil, hard and often fluoride-rich groundwater, seismic zone III, termites and mosquitoes.
"""


def make(path):
    out = [INTRO.format(**PROJECT)]
    n = 0
    for area, items in GUIDE:
        out.append(f"\n## {area}\n")
        for mistake, fix, ref in items:
            n += 1
            out.append(f"{n}. **Avoid:** {mistake}  \n   **Do:** {fix}" + (f"  \n   *Shown on: {ref}*" if ref else "") + "\n")
    out.append("\n## Hold points: stop and inspect before work is covered up\n")
    out.append("| Stage | Check | Who |\n|---|---|---|\n")
    for stage, check, who in HOLD_POINTS:
        out.append(f"| {stage} | {check} | {who} |\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))


if __name__ == "__main__":
    from paths import GUIDE_MD
    make(str(GUIDE_MD))
