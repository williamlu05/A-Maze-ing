import sys
from time import sleep
from app import ConfigError, Configuration, parse_configuration
from app import output, OutputError
from app.display import render, animate_solution
from mazegen import MazeGenerator, MazeGenerationError
from mazegen.helper import PATTERN_42, PATTERN_43

PATTERNS = {42: PATTERN_42, 43: PATTERN_43}

OPTIONS = [
    "Re-generate a new maze",
    "Show/Hide the shortest path",
    "Animate the shortest path",
    "Rotate number pattern",
    "Change the wall colours",
    "Return to original maze",
    "Write result in another different output file",
    "Quit"
]


def pending_action(message: str) -> None:
    print("\033[H\033[2J\033[3J", end="", flush=True)
    print(f"\n{message}\n")
    sleep(1)


def create_new_maze(config: Configuration,
                    new_seed: bool = False,
                    pattern: tuple = PATTERN_42) -> MazeGenerator:
    try:
        maze = MazeGenerator(
            config.get_width(),
            config.get_height(),
            config.get_entry(),
            config.get_exit(),
            config.get_perfect(),
            config.get_seed() if not new_seed else None,
            pattern_num=pattern
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
        color_choice: int = None
        pattern_number = 42
        animate_solution(new_maze, color_choice)
        while True:
            print(render(new_maze, show_sol, color_choice))
            # animate_solution(new_maze, COLORS)
            print("=== A-Maze-ing ===")
            for number, option in enumerate(OPTIONS):
                print(f"{number + 1}. {option}")

            choice = input(f"Choice? (1 - {len(OPTIONS)}): ")
            match choice:
                case "1":
                    pending_action("Regenerating maze")
                    new_maze = create_new_maze(config, True,
                                               PATTERNS[pattern_number])
                    show_sol = True
                    animate_solution(new_maze, color_choice)
                case "2":
                    show_sol = not show_sol
                    pending_action(f"{"Show" if show_sol else "Hid"}"
                                   "ing solution path")
                case "3":
                    show_sol = True
                    animate_solution(new_maze, color_choice)
                case "4":
                    if pattern_number == 42:
                        pattern_number = 43
                    else:
                        pattern_number = 42
                    pending_action("Changing pattern number...")
                    new_maze = create_new_maze(config, True,
                                               PATTERNS[pattern_number])
                    show_sol = True
                    animate_solution(new_maze, color_choice)
                case "5":
                    colour = input("What colour would you like? "
                                   "\n1- White\n2- Blue\n3- Purple"
                                   "\n4- Simple Emojis\n")
                    pending_action("Choose colour")
                    match colour:
                        case "1":
                            color_choice = 1
                        case "2":
                            color_choice = 2
                        case "3":
                            color_choice = 3
                        case "4":
                            color_choice = 4
                        case _:
                            color_choice = 1
                    print()
                case "6":
                    pending_action("Returning to original maze")
                    new_maze = maze
                case "7":
                    output_file = input("What is the name"
                                        " of the new output file? ")
                    pending_action("Writing in another output_file")
                    try:
                        output(new_maze, config, output_file)
                    except OutputError as e:
                        print("Error writing the maze "
                              f"to the output file: {e}\n", file=sys.stderr)
                        sleep(1)
                case "8":
                    pending_action("Quitting")
                    sys.exit(0)
                case _:
                    pending_action("Invalid choice")
    except (EOFError, KeyboardInterrupt):
        print("Exiting program")
        sys.exit(0)
