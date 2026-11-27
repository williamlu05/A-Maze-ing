import time
from mazegen.helper import DIRS
from typing import Any
from mazegen import MazeGenerator


def build_canvas(g: MazeGenerator, show_sol: bool) -> list[list[str]]:
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
    if show_sol:
        draw_sol(canv, g.solution)
    canv[2 * g.entry[1] + 1][2 * g.entry[0] + 1] = "entry"
    canv[2 * g.exit[1] + 1][2 * g.exit[0] + 1] = "exit"
    return canv


def draw_sol(canvas: list[list[str]],
             cells: list[tuple[int, int]]) -> None:
    y0, x0 = cells[0]
    canvas[2*y0 + 1][2*x0 + 1] = "solution"
    for (xa, ya), (xb, yb) in zip(cells, cells[1:]):
        canvas[ya + yb + 1][xa + xb + 1] = "solution"
        canvas[2*yb + 1][2*xb + 1] = "solution"


style = dict[str, Any]


def tile(kind: str, colors: dict[str, style]) -> str:
    s = colors[kind]
    return f"\033[{s['color']}m{s['symbol']}\033[0m"


def render(g: MazeGenerator, show_sol: bool = True, choice: int = None,
           canvas: list[list[str]] = None) -> str:
    colors: dict[str, Any] = {}
    colors = {
        "wall": {"symbol": "██", "color": 0},
        "p42": {"symbol": "▒▒", "color": 0},
        "floor": {"symbol": "  ", "color": 0},
        "solution": {"symbol": "██", "color": 92},
        "entry": {"symbol": "██", "color": "1;31"},
        "exit": {"symbol": "██", "color": "1;31"},
    }
    if choice == 1:
        colors["wall"]["color"] = 0
        # colors["wall"]["color"] = 0
    elif choice == 2:
        colors["wall"]["color"] = 94
        # colors["wall"]["color"] = 94
        colors["solution"]["color"] = 97
    elif choice == 3:
        colors["wall"]["color"] = 95
        # colors["wall"]["color"] = 95
        colors["solution"]["color"] = 93
    elif choice == 4:
        colors["wall"]["color"] = 32
        colors["p42"]["color"] = 33
        colors["solution"]["color"] = 33
        colors["entry"]["symbol"] = "🐝"
        colors["exit"]["symbol"] = "🌼"

    if canvas is None:
        canvas = build_canvas(g, show_sol)
    return "\n".join("".join(tile(k, colors) for k in row)
                     for row in canvas)


# ANIMACION
def animate_solution(g: MazeGenerator, choice: int = None,
                     delay: float = 0.03) -> None:
    canvas = build_canvas(g, False)
    print("\033[H\033[2J", end="")
    print("\033[H" + render(g, False, choice, canvas), flush=True)
    time.sleep(0.5)
    for (xa, ya), (xb, yb) in zip(g.solution, g.solution[1:]):
        for cx, cy in ((xa + xb + 1, ya + yb + 1), (2 * xb + 1, 2 * yb + 1)):
            if canvas[cy][cx] == "floor":
                canvas[cy][cx] = "solution"
                print("\033[H" + render(g, False, choice, canvas), flush=True)
                time.sleep(delay)
    print("\033[H\033[2J\033[3J", end="", flush=True)
