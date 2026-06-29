import sys
from typing import Final
from src.data_entities.app import App
from src.utils_func.exit_func import error_exit


def main() -> None:
    """The main entry point of the application.

    Parses command-line arguments (sys.argv) and determines the simulator's
    launch mode:
    - No arguments: Opens the main map selection menu.
    - One argument (path): Launches the simulation for the specified map.
    - More than one argument: Terminates the program with an error.

    Raises:
        SystemExit: If too many arguments are provided (called via error_exit).
    """
    app: Final = App()

    match len(sys.argv):
        case 1:
            app.open_menu()
        case 2:
            path = sys.argv[1]
            app.show_world(path)
        case _:
            error_exit("Too many arguments.\n"
                       "Example: python3 main.py"
                       " ./maps/medium/02_circular_loop.txt")


if __name__ == "__main__":
    main()
