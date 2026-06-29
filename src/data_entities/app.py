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
    """
    Main application controller managing the Pygame lifecycle
        and simulation states.

    Orchestrates the display initialization, handles the transition between
    the main menu and the active simulation world, and processes all user
    inputs (keyboard events) for camera panning and turn execution.

    Attributes:
        scr_width (int): Calculated screen width (80% of monitor resolution).
        scr_height (int): Calculated screen height (80% of monitor resolution).
        screen (pygame.Surface): The main Pygame display surface.
        camera (Camera): The viewport controller for rendering offsets.
        world (World | None): The simulation environment data structure.
        current_map_path (str | None): The file path of the currently
            selected map.
        clock (pygame.time.Clock): Frame rate controller.
        menu_running (bool): Flag indicating if the main menu loop is active.
        menu_index (int): The currently highlighted index in the map
            selection menu.
    """
    def __init__(self) -> None:
        pg.init()
        monitor_info = pg.display.Info()
        self.scr_width = int(monitor_info.current_w * 0.8)
        self.scr_height = int(monitor_info.current_h * 0.8)
        self.screen = pg.display.set_mode((self.scr_width, self.scr_height))
        self.camera = Camera(self.scr_width, self.scr_height)
        self.world: World | None = None
        self.current_map_path: str | None = None
        self.clock = pg.time.Clock()
        self.menu_running = True
        self.menu_index = 0

    def _load_and_pars(self, file_path: str) -> None:
        """
        Internal helper to initialize a new World and parse the selected
            map file.

        Args:
            file_path (str): The string path to the map configuration file.
        """
        self.world = World()
        parser = FileParser(file_path, self.world)
        parser.pars_map()
        self.world.init_drones()

    def safe_quit(self) -> None:
        """
        Safely terminates the Pygame engine and exits the system process.
        """
        self.menu_running = False
        pg.quit()
        sys.exit()

    def open_menu(self) -> None:
        """
        Executes the interactive graphical main menu loop.

        Scans the './maps' directory for available levels and handles keyboard
        navigation (UP/DOWN to select, ENTER to confirm, ESC to quit).
        Transitions to the world view once a map is chosen.
        """
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

    def show_world(self, map_path: str | None = None) -> None:
        """
        Executes the main simulation loop and renders the interactive world.

        Initializes the pathfinding heatmap, maps logical drones to graphical
        entities, and enters the main event loop. Handles camera panning via
        arrow keys and triggers simulation turns step-by-step when the Spacebar
        is pressed.

        Args:
            map_path (str, optional): A direct path to a map file.
                If not provided, uses the path selected from the
                main menu (`self.current_map_path`).
        """
        if map_path:
            self._load_and_pars(map_path)
        elif self.current_map_path is not None:
            self._load_and_pars(self.current_map_path)

        if self.world is None:
            return

        world_renderer = GfxWorldRenderer(self.screen, self.camera)
        world_renderer.build_scene(self.world)

        if self.world.start_hub is None or self.world.end_hub is None:
            return
        navigator = Navigator(start_hub=self.world.start_hub,
                              end_hub=self.world.end_hub,
                              zones=self.world.zones_map)
        navigator.build_heatmap()
        world_renderer.heatmap = navigator.distances

        simulator = Simulator(world=self.world, navigator=navigator)

        # === 1. СОЗДАЕМ ГРАФИЧЕСКИХ ДРОНОВ ===
        gfx_drones_map = {}

        for logical_drone in self.world.drone_list:
            if logical_drone.current_zone is None:
                continue
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
                            if logical_drone.current_zone is None:
                                continue
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
