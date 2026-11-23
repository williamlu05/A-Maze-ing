from typing import NamedTuple


PATTERN_42 = (
    "1.1.111",
    "1.1...1",
    "111.111",
    "..1.1..",
    "..1.111",
)
PATTERN_42_HEIGHT = len(PATTERN_42)
PATTERN_42_WIDTH = len(PATTERN_42[0])

MIN_HEIGHT_42 = PATTERN_42_HEIGHT + 2
MIN_WIDTH_42 = PATTERN_42_WIDTH + 2


class MazeGenerationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class Wall(NamedTuple):
    current: int
    adjacent: int
    dx: int
    dy: int


DIRECTIONS: dict[str, Wall] = {
    "N": Wall(NORTH, SOUTH, -1, 0),
    "E": Wall(EAST, WEST, 0, 1),
    "S": Wall(SOUTH, NORTH, 1, 0),
    "W": Wall(WEST, EAST, 0, -1)
}


def check_boundaries(maze: list[list[int]], x: int, y: int,
                     dx: int, dy: int, cells42: set[tuple[int, int]]) -> None:
    # Tambien comprobar (x, y)
    if not 0 <= (x + dx) < len(maze) or not 0 <= (y + dy) < len(maze[0]):
        raise MazeGenerationError(f"Wall opened at maze boundary: ({x}, {y})")
    if (x,y) in cells42 or (x + dx, y + dy) in cells42:
        raise MazeGenerationError("wall from 42 pattern cell opened")


def define_42cells(height: int, width: int) -> set[tuple[int, int]]:
    if width < MIN_WIDTH_42 or height < MIN_HEIGHT_42:
        return set()

    x0 = (height - PATTERN_42_HEIGHT) // 2
    y0 = width // 2 - PATTERN_42_WIDTH // 2

    return {
        (x0 + dx, y0 + dy)
        for dx, row in enumerate(PATTERN_42)
        for dy, char in enumerate(row)
        if char == "1"
    }
