from typing import Any

from src.utils_func.exit_func import error_exit


class Camera:
    """
    Manages the viewport, coordinate translation, and panning boundaries.

    Handles the conversion between logical world coordinates and physical
    screen pixels. It automatically calculates the optimal zoom level (scale)
    to fit the map vertically and provides constraints for horizontal scrolling

    Attributes:
        screen_width (int): The physical width of the display window.
        screen_height (int): The physical height of the display window.
        shift_x (float): The current horizontal panning offset.
        shift_y (float): The current vertical panning offset.
        scale (float): The zoom multiplier applied to world coordinates.
        world_max_x (int): The maximum logical X coordinate among all zones.
        world_min_x (int): The minimum logical X coordinate among all zones.
        world_max_y (int): The maximum logical Y coordinate among all zones.
        world_min_y (int): The minimum logical Y coordinate among all zones.
        padding (int): The screen edge margin in pixels to keep entities
            visible.
    """
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.shift_x: float = 0
        self.shift_y: float = 0
        self.scale: float = 1.0

        self.world_max_x = 0
        self.world_min_x = 0
        self.world_max_y = 0
        self.world_min_y = 0

        self.padding = 100

    def world_to_screen(self, world_x: float,
                        world_y: float) -> tuple[int, int]:
        """
        Translates logical map coordinates into physical screen pixels.
        """
        screen_x = int((world_x * self.scale) + self.shift_x)
        screen_y = int((world_y * self.scale) + self.shift_y)
        return screen_x, screen_y

    def auto_fit(self, zone_map: dict[Any, Any]) -> None:
        """
        Calculates map boundaries and optimally fits the world to the screen.

        Determines the bounding box of the entire zone network and calculates
        a scale factor so that the map fits vertically within the screen height
        (minus padding). Centers the map vertically and aligns it to the left.

        Raises:
            SystemExit: If the provided zone_map is empty or None.
        """
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

        self.shift_x = int(self.padding - (self.world_min_x * self.scale))
        self.shift_y = int((self.screen_height / 2)
                           - ((self.world_max_y + self.world_min_y)
                           / 2 * self.scale))

    def apply_horizontal_bounds(self) -> None:
        """
        Constrains the horizontal camera pan to prevent scrolling off the map.

        Calculates the physical screen width of the scaled map. If the map
        is smaller than the screen, it locks it to the left edge. Otherwise,
        it prevents the camera from panning past the extreme left or right
        padding boundaries.
        """
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
