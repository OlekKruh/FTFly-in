import sys
import pygame as pg

from src.algorithm.pathfinder import Navigator
# from src.gfx_entities.gfx_drone import GfxDrone
from src.gfx_entities.gfx_world_renderer import GfxWorldRenderer
from src.parser.map_searcher import MapSearcher
from src.data_entities.world_map import World
from src.parser.map_parser import FileParser
from src.gfx_entities.menu_renderer import MenuRenderer
from src.gfx_entities.camera import Camera


class App:
    def __init__(self):
        pg.init()
        monitor_info = pg.display.Info()
        self.scr_width = int(monitor_info.current_w * 0.8)
        self.scr_height = int(monitor_info.current_h * 0.8)
        self.screen = pg.display.set_mode((self.scr_width, self.scr_height))
        self.camera = Camera(self.scr_width, self.scr_height)
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
        found_maps = searcher.scan_maps()
        map_paths = list(found_maps.values())

        renderer = MenuRenderer(self.screen)
        renderer.build_layout(found_maps)

        while self.menu_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.menu_running = False
                    self.show_world()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.safe_quit()
                    elif event.key == pg.K_DOWN:
                        self.menu_index = ((self.menu_index + 1)
                                           % len(map_paths))
                    elif event.key == pg.K_UP:
                        self.menu_index = ((self.menu_index - 1)
                                           % len(map_paths))
                    elif event.key == pg.K_RETURN:
                        self.current_map_path = map_paths[self.menu_index]
                        self.menu_running = False
                        self.show_world()
                        break

            renderer.menu_render(self.menu_index)
            pg.display.flip()
            self.clock.tick(60)
        self.safe_quit()

    def show_world(self, map_path: str = None):
        if map_path:
            self._load_and_pars(map_path)
        else:
            self._load_and_pars(self.current_map_path)

        world_renderer = GfxWorldRenderer(self.screen, self.camera)
        world_renderer.build_scene(self.world)

        navigator = Navigator(start_hub=self.world.start_hub,
                              end_hub=self.world.end_hub,
                              zones=self.world.zones_map)
        print(navigator.broad_search())


        # === Test ===
        # start_zone = self.world.zones_map["start"]
        # target_zone = self.world.zones_map["waypoint1"]
        #
        # test_drone = GfxDrone(drone_id="D_001", zone=start_zone)
        # test_drone.set_target(target_zone)
        # test_drone.update_speed()
        #
        # world_renderer.add_drone(test_drone)
        # ============================

        pan_speed = 20

        world_running = True
        while world_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.safe_quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.safe_quit()

            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                self.camera.shift_x += pan_speed
            if keys[pg.K_RIGHT]:
                self.camera.shift_x -= pan_speed
            self.camera.apply_horizontal_bounds()

            world_renderer.render_frame()
            pg.display.flip()
            self.clock.tick(60)
