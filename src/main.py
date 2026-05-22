# import sys
# from entities.app import App
# from typing import Final
# from parser.map_parser import FileParser
from parser.map_searcher import MapSearcher
# from entities.world_map import World
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

    # PARSING OF ALL PATHS IN DIR MAPS
    searcher = MapSearcher('./maps')
    found_maps = searcher.scan_maps()
    for key, path in found_maps.items():
        print(f"[{key}] - {path}")

    # PARSING OF SPECIFIC MAP ON PATH
    # print("Start")
    #
    # world = World()
    # x = FileParser("./maps/hard/02_capacity_hell.txt", world)
    # x.pars_map()
    # world.init_drones()
    #
    # for key, value in world.zones_map.items():
    #     print(f"{key}: {value}")
    #
    # print("Fin")


if __name__ == "__main__":
    main()
