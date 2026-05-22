import sys
from entities.app import App
from typing import Final
from utils_func.exit_func import error_exit


def main():
    """
    на вход идут вырианты
    1) src/main.py - запускаем менюху
    2) src/main.py maps/easy/map1.txt - запускаем конкретную карту
    3) больше двух аргументов выдаем ошибку аргументов
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
                       "Example: python3 main.py ./maps/medium/02_circular_loop.txt")


if __name__ == "__main__":
    main()
