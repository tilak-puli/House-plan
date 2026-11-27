"""Small geometry helpers shared by model checks and tests. Rects are (x1, x2, y1, y2) in feet."""


def overlap(a, b):
    w = min(a[1], b[1]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[2], b[2])
    return w * h if w > 0 and h > 0 else 0.0


def inside(pt, r, tol=0.01):
    x, y = pt
    return r[0] - tol <= x <= r[1] + tol and r[2] - tol <= y <= r[3] + tol


def on_wall(axis, c, s, e, walls, tol=0.01):
    lo, hi = min(s, e), max(s, e)
    return any(w[0] == axis and abs(w[1] - c) <= tol and min(w[2], w[3]) - tol <= lo and hi <= max(w[2], w[3]) + tol for w in walls)


def _covered(axis, c, a, b, walls, tol=0.01):
    """Length of the segment [a, b] on line (axis, c) covered by wall segments."""
    spans = sorted((max(a, min(w[2], w[3])), min(b, max(w[2], w[3]))) for w in walls if w[0] == axis and abs(w[1] - c) <= tol)
    total, cur = 0.0, a
    for s, e in spans:
        if e <= cur:
            continue
        s = max(s, cur)
        total += max(0.0, e - s)
        cur = max(cur, e)
    return total


def graph(rooms, walls, doors, min_open=2.0):
    """rooms: [(id, x1, x2, y1, y2)]. Two rooms are linked by a door on their shared edge, or by an opening at least min_open ft long."""
    g = {r[0]: set() for r in rooms}
    for i, a in enumerate(rooms):
        for b in rooms[i + 1:]:
            for axis, c, lo, hi in _shared_edges(a, b):
                door = any(d[1] == axis and abs(d[2] - c) < 0.01 and lo - 0.01 <= min(d[3], d[4]) and max(d[3], d[4]) <= hi + 0.01 for d in doors)
                gap = (hi - lo) - _covered(axis, c, lo, hi, walls)
                if door or gap >= min_open:
                    g[a[0]].add(b[0]); g[b[0]].add(a[0])
    return g


def _shared_edges(a, b, tol=0.01):
    _, ax1, ax2, ay1, ay2 = a
    _, bx1, bx2, by1, by2 = b
    out = []
    for xa in (ax1, ax2):
        for xb in (bx1, bx2):
            if abs(xa - xb) <= tol:
                lo, hi = max(ay1, by1), min(ay2, by2)
                if hi - lo > tol:
                    out.append(("Y", xa, lo, hi))
    for ya in (ay1, ay2):
        for yb in (by1, by2):
            if abs(ya - yb) <= tol:
                lo, hi = max(ax1, bx1), min(ax2, bx2)
                if hi - lo > tol:
                    out.append(("X", ya, lo, hi))
    return out


def reachable(g, start):
    seen, todo = {start}, [start]
    while todo:
        for n in g[todo.pop()]:
            if n not in seen:
                seen.add(n); todo.append(n)
    return seen


def walkable(room_rect, obstacles, start, goal, width=2.0, step=0.25):
    """True if a square of side `width` can be moved from start to goal inside room_rect (x1, x2, y1, y2) without touching
    any obstacle rect (x1, x2, y1, y2). Grid breadth-first search; a cell is free if the square centred on it fits."""
    from collections import deque
    h = width / 2 - 1e-6
    x1, x2, y1, y2 = room_rect

    def free(x, y):
        if x - h < x1 - 1e-6 or x + h > x2 + 1e-6 or y - h < y1 - 1e-6 or y + h > y2 + 1e-6:
            return False
        return not any(overlap((x - h, x + h, y - h, y + h), o) > 0 for o in obstacles)

    def snap(p):  # nearest grid cell, or a free neighbour of it (the start or goal may sit within a step of a wall)
        i0, j0 = round((p[0] - x1) / step), round((p[1] - y1) / step)
        for di, dj in ((0, 0), (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            if free(x1 + (i0 + di) * step, y1 + (j0 + dj) * step):
                return (i0 + di, j0 + dj)
        return (i0, j0)

    s, g = snap(start), snap(goal)
    nx, ny = int((x2 - x1) / step) + 1, int((y2 - y1) / step) + 1
    cell = lambda i, j: (x1 + i * step, y1 + j * step)
    if not (0 <= s[0] < nx and 0 <= s[1] < ny and 0 <= g[0] < nx and 0 <= g[1] < ny):
        return False
    if not free(*cell(*s)) or not free(*cell(*g)):
        return False
    seen, q = {s}, deque([s])
    while q:
        i, j = q.popleft()
        if (i, j) == g:
            return True
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (i + di, j + dj)
            if n not in seen and 0 <= n[0] < nx and 0 <= n[1] < ny and free(*cell(*n)):
                seen.add(n); q.append(n)
    return False
