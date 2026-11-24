from __future__ import annotations
from typing import Iterator, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from .generator import MazeGenerator


def dfs(g: MazeGenerator) -> Iterator[None]:
    stack = [g.entry]
    seen = [g.entry]
    is_solved = False
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
        if g.exit == (nx, ny) and not is_solved:
            is_solved = True
            g.solution = stack.copy()
        yield


ALG = {"dfs": dfs}
