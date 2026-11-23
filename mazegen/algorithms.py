from __future__ import annotations
from typing import Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from .generator import MazeGenerator


def dfs(g: MazeGenerator) -> Iterator[None]:
    stack = [g.entry]
    seen = [g.entry]
    while stack:
        x, y = stack[-1]
        # mira los vecinos pisables y se queda con los que no hay en seen
        options = [(dir, nx, ny) for dir, nx, ny in g.free_neighbors(x, y)
                   if (nx, ny) not in seen]
        if not options:
            stack.pop()
            continue
        dir, nx, ny = g.rng.choice(options)
        g.open_wall(x, y, dir)
        seen.append((nx, ny))
        stack.append((nx, ny))
        yield


ALG = {"dfs": dfs}
