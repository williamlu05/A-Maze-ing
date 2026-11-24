from mazegen.helper import DIRS
from mazegen.generator import MazeGenerator


def build_canvas(g: MazeGenerator) -> list[list[str]]:
    canv = [["wall"] * (2 * g.width + 1) for _ in range(2 * g.height + 1)]
    for y in range(g.height):
        for x in range(g.width):
            if (x, y) in g.blocked:
                canv[2 * y + 1][2 * x + 1] = "p42"
                continue
            canv[2 * y + 1][2 * x + 1] = "floor"
            for dir, (dx, dy, _) in DIRS.items():
                if not g.grid[y][x] & dir:
                    canv[2 * y + 1 + dy][2 * x + 1 + dx] = "floor"
            if (x, y) in g.solution:
                canv[2 * y + 1][2 * x + 1] = "solution"
                continue
    canv[2 * g.entry[1] + 1][2 * g.entry[0] + 1] = "entry"
    canv[2 * g.exit[1] + 1][2 * g.exit[0] + 1] = "exit"
    print(g.exit)
    return canv


def render(g: MazeGenerator) -> str:
    chars = {"wall": "██", "p42": "▒▒", "floor": "  ",
             "solution": "🔹", "entry": "🔷", "exit": "🔶"}
    return "\n".join("".join(chars[k] for k in row)
                     for row in build_canvas(g))
