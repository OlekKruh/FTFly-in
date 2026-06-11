import sys
import pygame as pg

from src.algorithm.pathfinder import Navigator
from src.algorithm.simulator import Simulator
from src.gfx_entities.gfx_drone import GfxDrone
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
                        self.show_world()

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
        navigator.build_heatmap()
        world_renderer.heatmap = navigator.distances

        simulator = Simulator(world=self.world, navigator=navigator)

        # === 1. СОЗДАЕМ ГРАФИЧЕСКИХ ДРОНОВ ===
        gfx_drones_map = {}
        for logical_drone in self.world.drone_list:
            gfx_drone = GfxDrone(drone_id=logical_drone.drone_id,
                                 zone=logical_drone.current_zone)
            gfx_drones_map[logical_drone.drone_id] = gfx_drone
            world_renderer.add_drone(gfx_drone)

        pan_speed = 20
        world_running = True

        while world_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.safe_quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        world_running = False

                    # === 2. ОБРАБОТКА ХОДА (ПРОБЕЛ) ===
                    elif event.key == pg.K_SPACE:
                        simulator.run_step()

                        for logical_drone in self.world.drone_list:
                            gfx_drone = gfx_drones_map[logical_drone.drone_id]

                            target_x = logical_drone.current_zone.zone_x
                            target_y = logical_drone.current_zone.zone_y

                            if (gfx_drone.target_x != target_x
                                    or gfx_drone.target_y != target_y):
                                gfx_drone.set_target(
                                    logical_drone.current_zone)
                                gfx_drone.update_speed()

            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                self.camera.shift_x += pan_speed
            if keys[pg.K_RIGHT]:
                self.camera.shift_x -= pan_speed
            self.camera.apply_horizontal_bounds()

            # === 3. АНИМАЦИЯ ===
            for gfx_drone in gfx_drones_map.values():
                gfx_drone.update_cord()

            world_renderer.render_frame()
            pg.display.flip()
            self.clock.tick(60)
