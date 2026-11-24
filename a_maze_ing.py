import sys
from time import sleep


from app import ConfigError, Configuration, parse_configuration
from app import output, OutputError
from app import render
from mazegen import MazeGenerator, MazeGenerationError

OPTIONS = [
    "Re-generate a new maze",
    "Show/Hide the shortest path",
    "Rotate the wall colours",
    "Return to original maze",
    "Write result in another different output file",
    "Quit"
]


def pending_action(message: str) -> None:
    print("\033[H\033[2J\033[3J", end="", flush=True)
    print(f"\n{message}\n")
    sleep(1)


def create_new_maze(config: Configuration,
                    new_seed: bool = False) -> MazeGenerator:
    try:
        maze = MazeGenerator(
            config.get_width(),
            config.get_height(),
            config.get_entry(),
            config.get_exit(),
            config.get_perfect(),
            config.get_seed() if not new_seed else None
        )
        maze.generate()
        output(maze, config)
        return maze
    except MazeGenerationError as e:
        print(f"Error creating the maze: {e}", file=sys.stderr)
        sys.exit(1)
    except (OutputError, OSError) as e:
        print("Error writing the maze "
              f"to the output file: {e}", file=sys.stderr)
        sys.exit(1)


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
        maze = create_new_maze(config)
        new_maze = maze
        show_sol = True
        while True:
            print(render(new_maze, show_sol))
            print("=== A-Maze-ing ===")
            for number, option in enumerate(OPTIONS):
                print(f"{number + 1}. {option}")

            choice = input(f"Choice? (1 - {len(OPTIONS)}): ")
            match choice:
                case "1":
                    pending_action("Regenerating maze")
                    new_maze = create_new_maze(config, new_seed=True)
                case "2":
                    show_sol = not show_sol
                    pending_action(f"{"Show" if show_sol else "Hid"}"
                                   "ing solution path")
                case "3":
                    colour = input("What colour would you like? ")
                    pending_action("Choose colour")
                    print()
                case "4":
                    pending_action("Returning to original maze")
                    new_maze = maze
                case "5":
                    output_file = input("What is the name"
                                        " of the new output file? ")
                    pending_action("Writing in another output_file")
                    try:
                        output(new_maze, config, output_file)
                    except OutputError as e:
                        print("Error writing the maze "
                              f"to the output file: {e}\n", file=sys.stderr)
                        sleep(1)
                case "6":
                    pending_action("Quitting")
                    sys.exit(0)
                case _:
                    pending_action("Invalid choice")
    except (EOFError, KeyboardInterrupt):
        print("Exiting program")
        sys.exit(0)
