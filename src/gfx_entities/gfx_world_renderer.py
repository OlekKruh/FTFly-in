from src.data_entities.world_map import World
from src.gfx_entities.camera import Camera
from src.gfx_entities.gfx_drone import GfxDrone
from src.gfx_entities.gfx_link import GfxLink
from src.gfx_entities.gfx_zone import GfxZone
import pygame as pg


class GfxWorldRenderer:
    """
    Manages the rendering pipeline for all visual components of the simulation.

    Acts as the main scene graph, holding lists of all graphical zones, links,
    and drones. It iterates through these collections every frame to call their
    respective draw methods.
    """
    def __init__(self, screen: pg.Surface, camera: Camera) -> None:
        self.screen = screen
        self.camera = camera
        self.heatmap: dict[str, float] | None = None
        self.gfx_zones: list[GfxZone] = []
        self.gfx_links: list[GfxLink] = []
        self.gfx_drones: list[GfxDrone] = []

    def add_drone(self, drone: 'GfxDrone') -> None:
        """
        Registers a new GfxDrone instance to be rendered in the scene.
        """
        self.gfx_drones.append(drone)

    def build_scene(self, world_data: World) -> None:
        """
        Populates the graphical scene based on the logical world structure.

        Automatically adjusts the camera to fit the map, generates GfxZone
        instances, and creates GfxLink connections between them.
        """
        self.camera.auto_fit(world_data.zones_map)
        for zone in world_data.zones_map.values():
            self.gfx_zones.append(GfxZone(zone))
            for link in zone.links:
                source_node = world_data.zones_map[link.source]
                target_node = world_data.zones_map[link.target]

                gfx_link = GfxLink(source_node, target_node, link)
                self.gfx_links.append(gfx_link)

    def render_frame(self) -> None:
        """
        Clears the screen and draws all registered entities in the
            correct order:
        1. Links (Background)
        2. Zones (Midground)
        3. Drones (Foreground)
        """
        self.screen.fill((20, 20, 30))

        for link in self.gfx_links:
            link.draw(self.screen, self.camera)

        for zone in self.gfx_zones:
            current_heatmap = getattr(self, 'heatmap', None)
            zone.draw(self.screen, self.camera, current_heatmap)

        for drone in self.gfx_drones:
            drone.update_cord()
            drone.draw(self.screen, self.camera)
