import sys
import pygame as pg
from src.parser.map_searcher import MapSearcher
from src.entities.world_map import World
from src.parser.map_parser import FileParser
from src.visualizer.renderer import MenuRenderer


class App:
    SCR_WIDTH = 1280
    SCR_HEIGHT = 800

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((self.SCR_WIDTH, self.SCR_HEIGHT))
        self.world = None
        self.current_map_path = None
        self.clock = pg.time.Clock()
        self.menu_running = True
        self.menu_index = 0

    def _load_and_pars(self, file_path: str):
        self.world = World()
        parser = FileParser(file_path, self.world)
        parser.pars_map()
        self.world.init_drones()

    def safe_quit(self):
        self.menu_running = False
        pg.quit()
        sys.exit()

    def open_menu(self):
        searcher = MapSearcher('./maps')
        found_maps = searcher.scan_maps()  # DICT
        map_names = list(found_maps.keys())

        renderer = MenuRenderer(self.screen)

        while self.menu_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.safe_quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        self.menu_index = ((self.menu_index + 1)
                                           % len(map_names))
                    elif event.key == pg.K_UP:
                        self.menu_index = ((self.menu_index - 1)
                                           % len(map_names))
                    elif event.key == pg.K_RETURN:
                        selected_name = map_names[self.menu_index]
                        self.current_map_path = found_maps[selected_name]
                        self.menu_running = False
                        break
            renderer.menu_render(found_maps, self.menu_index)

            pg.display.flip()
            self.clock.tick(60)
        self.safe_quit()

    def show_world(self, map_path: str = None):
        if map_path:
            self._load_and_pars(map_path)
        else:
            self._load_and_pars(self.current_map_path)

        # TEMP SHOWCASE
        for key, value in self.world.zones_map.items():
            print(f"{key}: {value}")
