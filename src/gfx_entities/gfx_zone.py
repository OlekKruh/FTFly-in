import pygame as pg
from .gfx_text import TextLabel


class GfxZone:
    def __init__(self, zone_data):
        self.zone_data = zone_data
        # self.color = pg.Color(self.zone_data.color)
        self.base_radius = 20
        try:
            self.color = pg.Color(self.zone_data.color)
        except ValueError:
            print(f"Zone: '{self.zone_data.name}'. Unknown color: '{self.zone_data.color}'"
                  f"Setting color 'magenta'")
            self.color = pg.Color("magenta")

    def draw(self, screen, camera):
        # 1. Трансформация координат из мира на экран
        center_pos = camera.world_to_screen(self.zone_data.zone_x,
                                            self.zone_data.zone_y)

        # 2. Масштабируем радиус круга
        current_radius = self.base_radius  # int(self.base_radius * camera.scale)
        # Защита: чтобы круг не исчез совсем при сильном отдалении
        if current_radius < 5:
            current_radius = 5

        # Рисуем сам хаб
        pg.draw.circle(screen, self.color, center_pos, current_radius)

        # 3. Название зоны (рисуем сверху над кругом)
        name_cord = (center_pos[0], center_pos[1] - current_radius - 15)
        name_label = TextLabel(
            text=self.zone_data.name,
            size=20,
            cord=name_cord,
            color="white",
            centered=True
        )
        name_label.draw(screen)

        # 4. Счетчик дронов (рисуем снизу под кругом)
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
