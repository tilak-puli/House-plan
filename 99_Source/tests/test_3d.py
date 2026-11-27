"""The 3D page (04_3D/KH-P1_3D_Model.html) against the model: what make_3d exports, the page's roof-height ports and its furniture map."""
import json
import pathlib
import re
import shutil
import subprocess

import pytest

import geom as G
import make_3d
import model as M

ROOT = pathlib.Path(__file__).resolve().parents[2]
HTML = ROOT / "04_3D/KH-P1_3D_Model.html"
NODE = shutil.which("node")


@pytest.fixture(scope="module")
def data():
    return make_3d.model_data()


@pytest.fixture(scope="module")
def page():
    return HTML.read_text(encoding="utf-8")


def _script(page):
    return re.search(r"<script>\n(\(function\(\)\{.*?\}\)\(\);)\n</script>", page, re.S).group(1)


def test_project_page_has_no_walk_hook_and_one_model_block(page):
    assert "__walk" not in page and "__bl" not in page and "__fa" not in page
    assert len(re.findall(r"/\*@MODEL\*/", page)) == 1 and page.count("/*@ROOFZ*/") == 1


def test_roof_exports_come_from_geom(data):
    rr, rw, tr = data["roofRing"], data["roofWing"], data["terrace"]
    assert rr["holes"] == [list(h) for h in G.ring_holes()]
    assert rw["rects"] == [list(w) for w in G.wing_rects()]
    assert rr["eaveZ"] == G.eave_z() and rw["eaveZ"] == G.wing_eave_z() and rr["tan"] == G.TAN
    assert tr["guardRuns"] == [list(g) for g in G.corner_guard_runs()]
    for x, h in tr["south"]:
        assert abs(h - G.verge_south_h(x)) < 1e-3, x
    for y, h in tr["east"]:
        assert abs(h - G.verge_east_h(y)) < 1e-3, y
    assert max(h for _, h in tr["south"]) == M.ROOF["corner_guard"] and min(h for _, h in tr["south"]) == M.ROOF["upstand"]
    assert tr["chajja"] == list(M.ROOF["terrace_chajja"]) and len(tr["tanks"]) == 2
    # each tank and its square stand (x +- r, y +- r) inside the terrace less the wing wall's half-thickness on the west and the
    # parapet / upstand's on the other edges (the jali parapet's teak cap is 0.24 ft), clear of every canopy post (0.6 ft square)
    t, half_w, half_p = M.ROOF["terrace"], M.T / 2, 0.125
    assert [[p[1], p[2]] for p in M.PLUMBING_F1 if p[0] == "TK"] == [k[:2] for k in tr["tanks"]]
    for x, y, r in tr["tanks"]:
        assert x - r >= t[0] + half_w and x + r <= t[1] - half_p and y - r >= t[2] + half_p and y + r <= t[3] - half_p, (x, y)
        for px, py in M.TERRACE_POSTS:
            assert x - r >= px + 0.3 or x + r <= px - 0.3 or y - r >= py + 0.3 or y + r <= py - 0.3, (x, y, px, py)
        for fid in ("F30", "F32"):                                             # 1 in clear of the washer cabinet and the laundry sink in plan
            f = next(f for f in M._FLOOR_DATA["F1"]["FURNITURE"] if f[0] == fid)
            assert x - r >= f[4] + 0.08 or x + r <= f[3] - 0.08 or y - r >= f[6] + 0.08 or y + r <= f[5] - 0.08, (x, y, fid)
    assert all(j["toSoffit"] for j in data["jharokhas"]) and [j["face"] for j in data["jharokhas"]] == M.JHAROKHA_FACE


def test_ring_eaves_skip_the_holes_and_the_thinnai(data):
    th = M.ROOF["thinnai"]
    for x1, y1, x2, y2, k in data["roofRing"]["eaveRuns"]:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        sg = 1 if k == "out" else -1                                          # the roof lies toward the centre of an outer eave, away from it at the court
        dx, dy = (0, sg * (1 if my < M.CY else -1)) if abs(y1 - y2) < 1e-9 else (sg * (1 if mx < M.CX else -1), 0)
        assert G.ring_z(mx + dx * 0.05, my + dy * 0.05) is not None, (x1, y1, x2, y2)
        if k == "out" and abs(x1 - x2) < 1e-9 and x1 > M.CX:
            assert my < th[2] or my > th[3]                                    # no ring fascia where the lean-to carries on


def test_wing_eave_outline_is_the_L(data):
    runs = data["roofWing"]["eaveRuns"]
    assert len(runs) == 6                                                     # an L has six sides
    per = sum(abs(x2 - x1) + abs(y2 - y1) for x1, y1, x2, y2 in runs)
    w, e = M.ROOF["wing"], M.ROOF["wing_ext"]
    assert abs(per - 2 * ((e[1] - w[0]) + (w[3] - w[2]))) < 1e-6


def test_roof_lines_cover_both_roofs(data):
    kinds = {(k, s) for k, s, *_ in data["roofLines"]}
    assert {("ridge", "wing"), ("hip", "wing"), ("valley", "wing"), ("ridge", "ring"), ("hip", "ring"), ("valley", "ring")} <= kinds
    assert sum(1 for k, s, *_ in data["roofLines"] if (k, s) == ("valley", "wing")) == 1   # one re-entrant valley
    tot = {"ridge": 0.0, "hip": 0.0, "valley": 0.0}
    for k, _, x1, y1, x2, y2 in data["roofLines"]:
        tot[k] += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    ref = G.roof_line_lengths()
    for k in tot:
        assert abs(tot[k] - ref[k]) < 0.1, (k, tot[k], ref[k])                # the joined lines are geom's lines, to 0.1 ft per kind


def test_every_downpipe_drains_a_gutter(data):
    dps = data["roofRing"]["downpipes"]
    assert [(d["x"], d["y"]) for d in dps] == [tuple(p) for p in M.ROOF["downpipes"]]
    assert sum(d["roof"] == "terrace" for d in dps) == 1
    for d in dps:
        if d["roof"] == "terrace":
            assert (d["gx"], d["gy"]) == tuple(M.ROOF["terrace_outlet"])
            continue
        ez = G.wing_eave_z() if d["roof"] == "wing" else G.eave_z()
        assert abs(d["gz"] - (ez - M.ROOF["gutter_depth"])) < 1e-3
        assert ((d["gx"] - d["x"]) ** 2 + (d["gy"] - d["y"]) ** 2) ** 0.5 < 2.0   # a short swan neck to its own eave
    assert {d["roof"] for d in dps if d["x"] < M.HX1} == {"wing"}


def test_doors_carry_their_heights(data):
    hatch = next(d for d in data["doors"] if d["id"] == "D46")
    assert hatch["h"] == M.DOOR_HEIGHTS["D46"] < 7
    assert all(d["h"] == M.LEVELS["door_head"] for d in data["doors"] + data["f1"]["doors"] if d["id"] not in M.DOOR_HEIGHTS)


def test_walk_starts_in_the_forecourt_on_the_door_axis(data):
    x, y = data["start"]
    path = next(f[3] for f in M.SITE_FEATURES if f[0] == "PATH")
    d01 = next(d for d in M._FLOOR_DATA["G"]["DOORS"] if d[0] == "D01")
    assert path[0] < x < path[1] and path[2] < y < path[3] and y == (d01[3] + d01[4]) / 2
    assert data["centre"] == [M.CX, M.CY]


def test_every_furniture_id_has_a_kind(page):
    kind = dict(re.findall(r"\b(F\d+b?):\['(\w+)'", page[page.index("const KIND={"):page.index("};", page.index("const KIND={"))]))
    ids = {f[0] for fl in ("G", "F1") for key in ("FURNITURE", "EXTRA_DRAW") for f in M._FLOOR_DATA[fl][key]}
    assert set(kind) == ids                                                   # none missing, no stale ids
    builders = set(re.findall(r"\n  (\w+):\(o", page)) | {"glass", "mirror", "line", "grab", "post", "steprail"}
    assert set(kind.values()) <= builders
    for fl in ("G", "F1"):
        for f in M._FLOOR_DATA[fl]["FURNITURE"]:
            item = f[2].lower()
            if item.startswith("wc "):
                assert kind[f[0]] == "wc", f[0]
            if item.startswith("grab rail"):
                assert kind[f[0]] == "grab", f[0]
            if "glass" in item and ("screen" in item or "panel" in item or "return" in item):
                assert kind[f[0]] == "glass", f[0]


def test_no_duplex_leftovers_on_the_page(page):
    for s in ("54 × 54", "14 × 14", "70 × 160", "plant(65.2", "START_X=90", "x-97,y-16", "porch\":", "chaipu", "gable\":"):
        assert s not in page, s


@pytest.mark.skipif(NODE is None, reason="node not installed")
def test_page_script_parses(page, tmp_path):
    js = tmp_path / "page.js"
    js.write_text(_script(page), encoding="utf-8")
    r = subprocess.run([NODE, "--check", str(js)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-2000:]


@pytest.mark.skipif(NODE is None, reason="node not installed")
def test_page_roof_heights_match_geom(page, tmp_path):
    """The page's ringZ / wingZ / thinnaiRoofZ / roofZ, run in node on a 0.5 ft grid, give geom's heights."""
    model = re.search(r"/\*@MODEL\*/(const MODEL=.*?;)/\*@END\*/", page, re.S).group(1)
    ports = re.search(r"/\*@ROOFZ\*/(.*?)/\*@ROOFZ-END\*/", page, re.S).group(1)
    pts = [(x / 2, y / 2) for x in range(20, 130) for y in range(0, 100)]
    js = tmp_path / "roof.js"
    js.write_text(model + ports + "\nconst P=" + json.dumps(pts) + ";console.log(JSON.stringify(P.map(([x,y])=>[ringZ(x,y),wingZ(x,y),thinnaiRoofZ(x,y),roofZ(x,y)])));",
                  encoding="utf-8")
    r = subprocess.run([NODE, str(js)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-2000:]
    got = json.loads(r.stdout)
    for (x, y), zs in zip(pts, got):
        for z, ref in zip(zs, (G.ring_z(x, y), G.wing_roof_z(x, y), G.thinnai_roof_z(x, y), G.roof_z(x, y))):
            assert (z is None) == (ref is None) and (z is None or abs(z - ref) < 1e-9), (x, y, z, ref)
