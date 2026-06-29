import pygame as pg

from src.data_entities.links import Link
from src.data_entities.zone import Zone
from src.gfx_entities.camera import Camera


class GfxLink:
    """
    Represents the graphical visualization of a link between two zones.

    Renders a line connecting the source and target zones. The thickness
    of the line dynamically reflects the maximum drone capacity of the link.
    """
    def __init__(self, source_zone: Zone, target_zone: Zone, link_data: Link):
        """
        Initializes the graphical properties of the link.

        Args:
            source_zone (Zone): The logical zone where the link starts.
            target_zone (Zone): The logical zone where the link ends.
            link_data (Link): The logical link object containing capacity data.
        """
        self.source_zone = source_zone
        self.target_zone = target_zone
        self.link_data = link_data
        self.link_color = "white"
        self.link_thickness = self.link_data.max_capacity * 5

    def draw(self, screen: pg.Surface, camera: Camera) -> None:
        """
        Draws the link on the screen relative to the current camera viewport.

        Converts the logical world coordinates of both connected zones to
        screen coordinates before drawing the scaled line.

        Args:
            screen (pygame.Surface): The Pygame display surface to draw on.
            camera (Camera): The viewport controller for coordinate
                translation.
        """
        start_pos = camera.world_to_screen(self.source_zone.zone_x,
                                           self.source_zone.zone_y)
        end_pos = camera.world_to_screen(self.target_zone.zone_x,
                                         self.target_zone.zone_y)
        pg.draw.line(screen, self.link_color,
                     start_pos, end_pos,
                     self.link_thickness)
