from src.utils_func.exit_func import error_exit


class Camera:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.shift_x = 0
        self.shift_y = 0
        self.scale = 1.0

        self.world_max_x = 0
        self.world_min_x = 0
        self.world_max_y = 0
        self.world_min_y = 0

        self.padding = 100

    def world_to_screen(self, world_x: int,
                        world_y: int) -> tuple[int, int]:
        screen_x = int((world_x * self.scale) + self.shift_x)
        screen_y = int((world_y * self.scale) + self.shift_y)
        return screen_x, screen_y

    def auto_fit(self, zone_map: dict):
        if not zone_map:
            error_exit("Camera (auto_fit)\n"
                       "Cant calculate world size."
                       "Parameter 'zone_map' not exist or empty")

        self.world_max_x = max(zone.zone_x for zone in zone_map.values())
        self.world_min_x = min(zone.zone_x for zone in zone_map.values())
        self.world_max_y = max(zone.zone_y for zone in zone_map.values())
        self.world_min_y = min(zone.zone_y for zone in zone_map.values())
        world_width = self.world_max_x - self.world_min_x
        world_height = self.world_max_y - self.world_min_y

        if world_width == 0:
            world_width = 1
        if world_height == 0:
            world_height = 1

        available_height = self.screen_height - (self.padding * 2)
        self.scale = available_height / world_height

        self.shift_x = self.padding - (self.world_min_x * self.scale)
        self.shift_y = ((self.screen_height / 2)
                        - ((self.world_max_y + self.world_min_y)
                           / 2 * self.scale))

    def apply_horizontal_bounds(self):
        world_w = self.world_max_x - self.world_min_x
        available_w = self.screen_width - (self.padding * 2)

        map_pixel_width = world_w * self.scale

        if map_pixel_width <= available_w:
            self.shift_x = self.padding - (self.world_min_x * self.scale)
            return

        screen_min_x = (self.world_min_x * self.scale) + self.shift_x
        if screen_min_x > self.padding:
            self.shift_x = self.padding - (self.world_min_x * self.scale)

        screen_max_x = (self.world_max_x * self.scale) + self.shift_x
        if screen_max_x < self.screen_width - self.padding:
            missed_pixels = (self.screen_width - self.padding) - screen_max_x
            self.shift_x += missed_pixels
