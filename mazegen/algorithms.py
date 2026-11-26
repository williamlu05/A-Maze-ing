from __future__ import annotations
from typing import Iterator, TYPE_CHECKING
import heapq

if TYPE_CHECKING:
    from .generator import MazeGenerator


def dfs(g: MazeGenerator) -> Iterator[None]:
    stack = [g.entry]
    seen = [g.entry]
    dead_end = False
    while stack:
        x, y = stack[-1]
        # mira los vecinos pisables y se queda con los que no hay en seen
        options = [(dir, nx, ny) for dir, nx, ny in g.free_neighbors(x, y)
                   if (nx, ny) not in seen]
        if not options:
            # Modo not perfect
            if dead_end and not g.perfect:
                walled = [(d, ox, oy) for d, ox, oy in g.free_neighbors(x, y)
                          if g.grid[y][x] & d]
                if walled:
                    d, _, _ = g.rng.choice(walled)
                    g.open_wall(x, y, d)
                    yield
            dead_end = False
            stack.pop()
            continue
        dir, nx, ny = g.rng.choice(options)
        g.open_wall(x, y, dir)
        seen.append((nx, ny))
        stack.append((nx, ny))
        dead_end = True
        yield


Cell = tuple[int, int]


def find_solution(g: MazeGenerator) -> list[Cell]:
    ex, ey = g.exit

    def h(cell: Cell) -> int:
        return abs(cell[0] - ex) + abs(cell[1] - ey)

    # (f, h, cell)
    queue: list[tuple[int, int, Cell]] = []
    heapq.heappush(queue, (h(g.entry), h(g.entry), g.entry))
    best_steps: dict[Cell, int] = {g.entry: 0}
    parent: dict[Cell, Cell] = {}
    best_len = float("inf")

    while queue:
        f, ch, cell = heapq.heappop(queue)
        steps = f - ch

        if f >= best_len or steps > best_steps[cell]:
            continue
        if cell == g.exit:
            best_len = steps
            continue

        x, y = cell
        for dir, nx, ny in g.free_neighbors(x, y):
            if g.grid[y][x] & dir:
                continue
            nxt = (nx, ny)
            new_steps = steps + 1
            if new_steps >= best_steps.get(nxt, float("inf")):
                continue
            nh = h(nxt)
            if new_steps + nh >= best_len:
                continue
            best_steps[nxt] = new_steps
            parent[nxt] = cell
            heapq.heappush(queue, (new_steps + nh, nh, nxt))

    if g.exit not in parent:
        return []

    path = [g.exit]
    while path[-1] != g.entry:
        path.append(parent[path[-1]])
    path.reverse()
    return path


ALG = {"dfs": dfs}
