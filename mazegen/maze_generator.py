import random
from .maze_helper import DIRECTIONS, MazeGenerationError
from .maze_helper import check_boundaries, define_42cells


def validate_dim(dim: int) -> int:
    if dim <= 0:
        raise MazeGenerationError("Invalid dimension")
    return dim


def validate_pos(pos: tuple[int, int], cells42: set[tuple[int, int]],
                 height: int, width: int) -> tuple[int, int]:
    # TODO check how to lay out the cells42 so that it can be empty or be checked whether it contains the position (if so then error)
    if not (0 <= pos[0] < height and 0 <= pos[1] < width):
        raise MazeGenerationError("Invalid position exceeding limits")
    if pos in cells42:
        raise MazeGenerationError("invalid position, "
                                  f"{pos} in designated 42 cells")
    return pos


class MazeGenerator():
    def __init__(self, width: int, height: int, entry_pos: tuple[int, int],
                 exit_pos: tuple[int, int], perfect: bool,
                 seed: int = 47) -> None:
        self._width = validate_dim(width)
        self._height = validate_dim(height)
        self._42cells = define_42cells(height, width)

        self._entry = validate_pos(entry_pos, self._42cells,
                                   self._height, self._width)
        self._exit = validate_pos(exit_pos, self._42cells,
                                  self._height, self._width)
        if self._entry == self._exit:
            raise MazeGenerationError("Invalid positions, entry = exit point")

        self._perfect = perfect
        random.seed(seed)

    def generate(self) -> None:
        self._maze = [[15 for _ in range(self._width)]
                      for _ in range(self._height)]
        # TODO Algoritmo dfs y bfs
        # TODO solo utilizar funciones para abrir paredes, para que así nunca se abre una puerta por un lado y no por otro

    # Solo para testear
    def print_maze(self) -> None:
        for x, line in enumerate(self._maze):
            for y, cell in enumerate(line):
                if (x, y) in self._42cells:
                    print(f"\033[31m{cell:x}\033[0m ", end="")
                elif (x, y) in (self._entry, self._exit):
                    print(f"\033[32m{cell:x}\033[0m ", end="")
                else:
                    print(f"{cell:x} ", end="")
            print()

    def get_maze(self) -> list[list[int]]:
        # Habria que crear una copia en verdad
        # Considerar meter el generate() dentro de la iniicialización, get_maze da fallo si no se ha generado antes
        return self._maze

    def open_wall(self, direction: str, x: int, y: int) -> None:
        if direction not in DIRECTIONS:
            raise MazeGenerationError("Invalid direction to open a wall")

        wall = DIRECTIONS[direction]
        check_boundaries(self._maze, x, y, wall.dx, wall.dy, self._42cells)

        self._maze[x][y] &= ~wall.current
        self._maze[x + wall.dx][y + wall.dy] &= ~wall.adjacent
