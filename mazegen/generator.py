import random
from typing import Optional
from collections.abc import Iterator
from .helper import N, E, S, W, DIRS, PATTERN_42, ALGORITHMS
from .helper import MazeGenerationError


def validate_dim(dim: int) -> int:
    if dim <= 0:
        raise MazeGenerationError("Invalid dimension")
    return dim


def validate_pos(pos: tuple[int, int], cells42: set[tuple[int, int]],
                 height: int, width: int) -> tuple[int, int]:
    if not (0 <= pos[0] < width and 0 <= pos[1] < height):
        raise MazeGenerationError("Invalid position exceeding limits")
    if pos in cells42:
        raise MazeGenerationError("invalid position, "
                                  f"{pos} in designated 42 cells")
    return pos


def validate_algorithm(algorithm: Optional[str]) -> str:
    if algorithm not in ALGORITHMS:
        raise MazeGenerationError(f"Invalid algorithm: {algorithm}")
    return algorithm


class MazeGenerator:
    """Maze generator. Grid is grid[y][x]"""

    def __init__(self, width: int, height: int,
                 entry_pos: tuple[int, int],
                 exit_pos: tuple[int, int],
                 perfect: bool,
                 seed: Optional[int] = None,
                 algorithm: Optional[str] = "dfs"
                 ) -> None:
        self.width = validate_dim(width)
        self.height = validate_dim(height)

        self.blocked = self.pattern42()
        self.entry = validate_pos(entry_pos, self.blocked, height, width)
        self.exit = validate_pos(exit_pos, self.blocked, height, width)

        self.seed = seed if seed is not None else random.randrange(2**32)
        self.rng = random.Random(self.seed)

        self.perfect = perfect
        self.algorithm = validate_algorithm(algorithm)

        self.grid = [[15] * width for _ in range(height)]
        self.solution: list[tuple[int, int]] = list()

        if self.entry == self.exit:
            raise MazeGenerationError("Entry and exit of the maze are equal")

    # Considerar devolver copias
    def get_maze(self) -> list[list[int]]:
        return self.grid

    def get_solution(self) -> list[tuple[int, int]]:
        return self.solution

    # mira si esta dentro de los boundaries
    def free(self, x: int, y: int) -> bool:
        return (0 <= x < self.width and 0 <= y < self.height
                and (x, y) not in self.blocked)

    # Abre el muro que le dices y su opuesto
    # NOT: ~ invierte los bits
    # AND: & da 1 en una posicion solo si ambos numeros son 1
    # OR: | da 1 en una posicion si al menos uno es 1
    def open_wall(self, x: int, y: int, dir: int) -> None:
        dx, dy, opp = DIRS[dir]
        self.grid[y][x] &= ~dir
        self.grid[y + dy][x + dx] &= ~opp

    def close_wall(self, x: int, y: int, dir: int) -> None:
        dx, dy, opp = DIRS[dir]
        self.grid[y][x] |= dir
        self.grid[y + dy][x + dx] |= opp

    # check si la celda vecina es pisable
    def free_neighbors(self, x: int, y: int) -> list[tuple[int, int, int]]:
        out: list[tuple[int, int, int]] = []
        for dir, (dx, dy, _) in DIRS.items():
            if self.free(x + dx, y + dy):
                out.append((dir, x + dx, y + dy))
        return out

    def pattern42(self) -> set[tuple[int, int]]:
        if self.width < 9 or self.height < 7:
            print("Error: the maze is too small, "
                  " '42' pattern could not be drawn.")
            return set()
        ox, oy = self.width // 2 - 3, (self.height - 5) // 2

        return {
            (ox + dx, oy + dy)
            for dy, row in enumerate(PATTERN_42)
            for dx, char in enumerate(row)
            if char == "1"
        }

    def generate_steps(self) -> Iterator[None]:
        from .algorithms import ALG, find_solution
        yield from ALG[self.algorithm](self)
        if not self.perfect:
            yield from self.braid()
            yield from self.add_loops()
        self.solution = find_solution(self)

    def generate(self) -> None:
        for _ in self.generate_steps():
            pass

    def braid(self) -> Iterator[None]:
        yield from ()

    def add_loops(self) -> Iterator[None]:
        yield from ()
