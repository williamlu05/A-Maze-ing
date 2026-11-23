
from mazegen import MazeGenerator
from app import Configuration


class OutputError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__()


def output(maze: MazeGenerator, config: Configuration) -> None:
    file_path = config.get_output_file()
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
