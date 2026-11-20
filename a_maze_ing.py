import sys

from app.parser import ConfigError, parse_configuration


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    try:
        config = parse_configuration(sys.argv[1])
        maze = MazeGenerator(config)
    except (OSError, ValueError, KeyError, ConfigError) as e:
        print(f"Error reading the configurations of the maze: {e}",
              file=sys.stderr)
        sys.exit(1)
