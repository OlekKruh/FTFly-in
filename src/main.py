# import sys
# from entities.app import App
# from typing import Final
from parser.parser import FileParser
from entities.world_map import World
# from utils_func.exit_func import error_exit


def main():
    """
    на вход идут вырианты
    1) src/main.py - запускаем менюху
    2) src/main.py maps/easy/map1.txt - запускаем конкретную карту
    3) больше двух аргументов выдаем ошибку аргументов
    """
    # app: Final = App()
    #
    # match len(sys.argv):
    #     case 1:
    #         app.open_menu()
    #     case 2:
    #         parser = FileParser(sys.argv[1])
    #         app.run_simulation()
    #     case _:
    #         error_exit("Too many arguments. Usage: python main.py [map_path]")
    print("Start")
    world_obj = World()
    x = FileParser("/Users/okruh/Documents/Fly-In/maps/hard/02_capacity_hell.txt", world_obj)
    x.pars_map()
    for key, value in world_obj.zones_map.items():
        print(f"{key}: {value}")
    print("Fin")

if __name__ == "__main__":
    main()
