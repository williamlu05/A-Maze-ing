
from mazegen import MazeGenerator
from .parser import Configuration
from typing import Optional


class OutputError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def determine_solution(solution: list[tuple[int, int]]) -> str:
    i = 1
    (y, x) = solution[0]
    path = ""
    while i < len(solution):
        (ny, nx) = solution[i]
        if nx == x + 1 and ny == y:
            path += "S"
        elif nx == x - 1 and ny == y:
            path += "N"
        elif ny == y + 1 and nx == x:
            path += "E"
        elif ny == y - 1 and nx == x:
            path += "W"
        else:
            raise OutputError("Incoherent solution: "
                              "two coordinates not adjacent")
        (y, x) = (ny, nx)
        i += 1
    return path


def output(maze: MazeGenerator, config: Configuration,
           output_file: Optional[str] = None) -> None:
    file_path = config.get_output_file() if not output_file else output_file
    with open(file_path, "w") as file:
        matrix = maze.get_maze()
        for line in matrix:
            for cell in line:
                file.write(f"{cell:x}")
            file.write("\n")
        file.write("\n")
        entry_pos = config.get_entry()
        exit_pos = config.get_exit()

        file.write(f"{entry_pos[0]},{entry_pos[1]}\t # entry (x, y)\n")
        file.write(f"{exit_pos[0]},{exit_pos[1]}\t # exit (x, y)\n")
        solution = determine_solution(maze.get_solution())
        file.write(f"{solution}")
