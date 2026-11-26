N, E, S, W = 1, 2, 4, 8
# dirección: (dx, dy, dirección opuesta)
DIRS = {N: (0, -1, S), E: (1, 0, W), S: (0, 1, N), W: (-1, 0, E)}
ALGORITHMS = ["dfs", "bfs"]

PATTERN_42 = (
    "1.1.111",
    "1.1...1",
    "111.111",
    "..1...1",
    "..1.111",
)


class MazeGenerationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
