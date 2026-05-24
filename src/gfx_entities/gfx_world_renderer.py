from src.data_entities.world_map import World
from src.gfx_entities.gfx_link import GfxLink
from src.gfx_entities.gfx_zone import GfxZone


class GfxWorldRenderer:
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera
        self.gfx_zones = []
        self.gfx_links = []

    def build_scene(self, world_data: World):
        self.camera.auto_fit(world_data.zones_map)
        for zone in world_data.zones_map.values():
            self.gfx_zones.append(GfxZone(zone))
            for link in zone.links:
                source_node = world_data.zones_map[link.source]
                target_node = world_data.zones_map[link.target]

                gfx_link = GfxLink(source_node, target_node, link)
                self.gfx_links.append(gfx_link)

    def render_frame(self):
        self.screen.fill((20, 20, 30))

        # Сначала рисуем все связи (нижний слой)
        for link in self.gfx_links:
            link.draw(self.screen, self.camera)

        # Затем рисуем зоны (верхний слой, перекроет концы линий)
        for zone in self.gfx_zones:
            zone.draw(self.screen, self.camera)
