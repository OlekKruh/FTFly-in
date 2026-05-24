class Camera:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.scale = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.padding = 10

    def world_to_screen(self, world_x: float,
                        world_y: float) -> tuple[int, int]:
        """
        Преобразует координаты карты в пиксели экрана.
        """
        screen_x = int((world_x * self.scale) + self.offset_x)
        screen_y = int((world_y * self.scale) + self.offset_y)
        return screen_x, screen_y

    def auto_fit(self, zones_map: dict):
        """
        Вычисляет нужный масштаб и смещение,
        чтобы вписать всю карту в экран.
        """
        if not zones_map:
            return

        # 1. Находим крайние точки мира (Bounding Box)
        # Предполагается, что у твоих зон есть атрибуты .x и .y
        min_x = min(zone.x for zone in zones_map.values())
        max_x = max(zone.x for zone in zones_map.values())
        min_y = min(zone.y for zone in zones_map.values())
        max_y = max(zone.y for zone in zones_map.values())

        # 2. Вычисляем физический размер карты
        world_w = max_x - min_x
        world_h = max_y - min_y

        # Защита от деления на ноль (если на карте всего одна зона)
        if world_w == 0:
            world_w = 1
        if world_h == 0:
            world_h = 1

        # 3. Считаем доступное место на экране с учетом отступов
        available_w = self.screen_width - self.padding
        available_h = self.screen_height - self.padding

        # 4. Вычисляем масштаб
        scale_x = available_w / world_w
        scale_y = available_h / world_h

        # Берем минимальный масштаб, чтобы карта влезла
        # целиком и не исказились пропорции
        self.scale = min(scale_x, scale_y)

        # 5. Вычисляем смещение для центрирования
        # Находим центр экрана
        center_screen_x = self.screen_width / 2
        center_screen_y = self.screen_height / 2

        # Находим геометрический центр карты
        center_world_x = min_x + (world_w / 2)
        center_world_y = min_y + (world_h / 2)

        # Смещение = центр экрана минус (масштабированный центр мира)
        self.offset_x = center_screen_x - (center_world_x * self.scale)
        self.offset_y = center_screen_y - (center_world_y * self.scale)
