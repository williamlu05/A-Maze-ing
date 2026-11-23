import sys

from app import ConfigError, parse_configuration
from app import output, OutputError
from mazegen import MazeGenerator, MazeGenerationError


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    try:
        config = parse_configuration(sys.argv[1])
    except (OSError, ValueError, KeyError, ConfigError) as e:
        print(f"Error reading the configurations of the maze: {e}",
              file=sys.stderr)
        sys.exit(1)

    try:
        maze = MazeGenerator(
            config.get_width(),
            config.get_height(),
            config.get_entry(),
            config.get_exit(),
            config.get_perfect()
        )
        maze.generate()

        maze.open_wall("N", 1, 0)
        maze.open_wall("E", 10, 8)
        maze.open_wall("W", 10, 8)
        try:
            maze.open_wall("S", len(maze.get_maze()), 0)
        except Exception as e:
            print(f"haha, {e}")
        try:
            maze.open_wall("O", 10, 10)
        except Exception as e:
            print(f"haha, {e}")
        maze.open_wall("S", 4, 5)
        maze.open_wall("N", 5, 5)

        maze.print_maze()

        output(maze, config)
    except MazeGenerationError as e:
        print(f"Error creating the maze: {e}", file=sys.stderr)
        sys.exit(1)
    except OutputError as e:
        print(f"Error writing the maze to the output file: {e}")
        sys.exit(1)
