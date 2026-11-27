import pytest

import model as M
from planlib import inside, on_wall, overlap

FLOORS = ["G", "F1"]


def floor(name):
    with M.on_floor(name):
        return (list(M.ROOMS), list(M.WALLS), list(M.DOORS), list(M.WINDOWS), list(M.FURNITURE))


@pytest.mark.parametrize("fl", FLOORS)
def test_rooms_do_not_overlap(fl):
    rooms = floor(fl)[0]
    bad = [(a[0], b[0]) for i, a in enumerate(rooms) for b in rooms[i + 1:] if overlap(a[2:6], b[2:6]) > 0.05]
    assert not bad, f"overlapping rooms on {fl}: {bad}"


@pytest.mark.parametrize("fl", FLOORS)
def test_doors_sit_on_walls(fl):
    _, walls, doors, _, _ = floor(fl)
    bad = [d[0] for d in doors if not on_wall(d[1], d[2], d[3], d[4], walls)]
    assert not bad, f"doors off any wall on {fl}: {bad}"


@pytest.mark.parametrize("fl", FLOORS)
def test_windows_sit_on_walls(fl):
    _, walls, _, windows, _ = floor(fl)
    bad = [w[0] for w in windows if not on_wall(w[1], w[2], w[3], w[4], walls)]
    assert not bad, f"windows off any wall on {fl}: {bad}"


@pytest.mark.parametrize("fl", FLOORS)
def test_furniture_inside_a_room(fl):
    rooms, _, _, _, furniture = floor(fl)
    rects = [r[2:6] for r in rooms] + [j[:4] for j in getattr(M, "JHAROKHAS", [])]   # a jharokha seat sits in its bay, outside the wall line
    bad = []
    for f in furniture:
        if f[0] in M.OUTDOOR_FURNITURE:
            continue
        centre = ((f[3] + f[4]) / 2, (f[5] + f[6]) / 2)
        if not any(inside(centre, r) for r in rects):
            bad.append(f[0])
    assert not bad, f"furniture outside every room on {fl}: {bad}"
