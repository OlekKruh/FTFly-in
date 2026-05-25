import pygame as pg

class GfxLink:
    def __init__(self, source_zone, target_zone, link_data):
        """
        Link(source='start', target='junction', max_capacity=1)
        """
        self.source_zone = source_zone
        self.target_zone = target_zone
        self.link_data = link_data
        self.link_color = "white"
        self.link_thickness = self.link_data.max_capacity * 5

    def draw(self, screen, camera):
        start_pos = camera.world_to_screen(self.source_zone.zone_x,
                                           self.source_zone.zone_y)
        end_pos = camera.world_to_screen(self.target_zone.zone_x,
                                         self.target_zone.zone_y)
        pg.draw.line(screen, self.link_color,
                     start_pos, end_pos,
                     self.link_thickness)
