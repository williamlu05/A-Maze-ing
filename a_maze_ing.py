import sys

from app import ConfigError, parse_configuration
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
        maze.print_maze()
    except MazeGenerationError as e:
        print(f"Error creating the maze: {e}", file=sys.stderr)
        sys.exit(1)
