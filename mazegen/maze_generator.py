import random


HEIGHT_MIN_42 = 5
WIDTH_MIN_42 = 7

class MazeGenerationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def validate_dim(dim: int) -> int:
    if dim <= 0:
        raise MazeGenerationError("Invalid dimension")
    return dim


def validate_pos(pos: tuple[int, int], height: int, width: int) -> tuple[int, int]:
    if pos[0] > width or pos[1] > height:
        raise MazeGenerationError("Invalid position")
    return pos


class MazeGenerator():
    def __init__(self, width, height, entry_pos, exit_pos, perfect, seed: int = 47) -> None:
        self._width = validate_dim(width)
        self._height = validate_dim(width)
        self._entry = validate_pos(entry_pos)
        self._exit = validate_pos(exit_pos)
        if self._entry == self._exit:
            raise MazeGenerationError("Invalid positions, entry = exit point")
        self._perfect = perfect
        random.seed(seed)

        #TODO add type hints __init__
        #TODO block 42 cells if the maze is bit enough. Check after validating width and height
        #TODO Initialize a grix[x][y] all to 0, all walls before the algorithm.
        #TODO Have the output of the maze, outside this class