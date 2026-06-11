import pygame as pg
from .gfx_text import TextLabel


class GfxZone:
    def __init__(self, zone_data):
        self.zone_data = zone_data
        self.base_radius = 20
        try:
            self.color = pg.Color(self.zone_data.color)
        except ValueError:
            print(f"Zone: '{self.zone_data.name}'."
                  f" Unknown color: '{self.zone_data.color}'"
                  f"Setting color 'magenta'")
            self.color = pg.Color("magenta")

    def draw(self, screen, camera, heatmap=None):
        center_pos = camera.world_to_screen(self.zone_data.zone_x,
                                            self.zone_data.zone_y)

        # 2. Circle min scale
        current_radius = self.base_radius
        if current_radius < 5:
            current_radius = 5

        # Рисуем сам хаб
        pg.draw.circle(screen, self.color, center_pos, current_radius)

        # 3. Zone naming
        name_cord = (center_pos[0], center_pos[1] - current_radius - 15)
        name_label = TextLabel(
            text=self.zone_data.name,
            size=20,
            cord=name_cord,
            color="yellow",
            centered=True
        )
        name_label.draw(screen)

        # 4. Drone counter
        drones_count = len(self.zone_data.current_drones)
        status_text = f"{drones_count}/{self.zone_data.max_drones}"

        status_cord = (center_pos[0], center_pos[1] + current_radius + 15)
        status_label = TextLabel(
            text=status_text,
            size=18,
            cord=status_cord,
            color="yellow",
            centered=True
        )
        status_label.draw(screen)

        # 5. Heatmap value
        if heatmap is not None:
            dist = heatmap.get(self.zone_data.name, float('inf'))
            if dist == float('inf'):
                dist_str = "INF"
            else:
                dist_str = f"{dist:.1f}"

            heat_cord = (center_pos[0], center_pos[1] + current_radius + 35)
            heat_label = TextLabel(
                text=dist_str,
                size=16,
                cord=heat_cord,
                color="orange",
                centered=True
            )
            heat_label.draw(screen)
