class Camera:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.scale = 1.5
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.padding = 10

        self.world_min_x = 0
        self.world_max_x = 0
        self.world_min_y = 0
        self.world_max_y = 0

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
        self.world_min_x = min(zone.zone_x for zone in zones_map.values())
        self.world_max_x = max(zone.zone_x for zone in zones_map.values())
        self.world_min_y = min(zone.zone_y for zone in zones_map.values())
        self.world_max_y = max(zone.zone_y for zone in zones_map.values())

        # 2. Вычисляем физический размер карты
        world_w = self.world_max_x - self.world_min_x
        world_h = self.world_max_y - self.world_min_y

        # Защита от деления на ноль (если на карте всего одна зона)
        if world_w == 0:
            world_w = 1
        if world_h == 0:
            world_h = 1

        # 3. Считаем доступное место на экране с учетом отступов
        available_w = self.screen_width - (self.padding * 2)
        available_h = self.screen_height - (self.padding * 2)

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
        center_world_x = self.world_min_x + (world_w / 2)
        center_world_y = self.world_min_y + (world_h / 2)

        # Смещение = центр экрана минус (масштабированный центр мира)
        self.offset_x = center_screen_x - (center_world_x * self.scale)
        self.offset_y = center_screen_y - (center_world_y * self.scale)

    def apply_bounds(self):
        # Отдельные настройки отступов
        margin_x = 200
        margin_y = 200

        # Физические размеры карты в пикселях при текущем зуме
        map_w = (self.world_max_x - self.world_min_x) * self.scale
        map_h = (self.world_max_y - self.world_min_y) * self.scale

        # Текущие позиции крайних точек на экране
        screen_min_x = (self.world_min_x * self.scale) + self.offset_x
        screen_max_x = (self.world_max_x * self.scale) + self.offset_x
        screen_min_y = (self.world_min_y * self.scale) + self.offset_y
        screen_max_y = (self.world_max_y * self.scale) + self.offset_y

        # --- Горизонталь (X) ---
        if map_w < self.screen_width - (margin_x * 2):
            # Карта меньше доступной зоны: не даем краям выехать за margin
            if screen_min_x < margin_x:
                self.offset_x += margin_x - screen_min_x
            elif screen_max_x > self.screen_width - margin_x:
                self.offset_x -= screen_max_x - (self.screen_width - margin_x)
        else:
            # Карта больше экрана: цепляем края за margin
            if screen_max_x < self.screen_width - margin_x:
                self.offset_x += (self.screen_width - margin_x) - screen_max_x
            elif screen_min_x > margin_x:
                self.offset_x -= screen_min_x - margin_x

        # --- Вертикаль (Y) ---
        if map_h < self.screen_height - (margin_y * 2):
            # Карта меньше доступной зоны по высоте
            if screen_min_y < margin_y:
                self.offset_y += margin_y - screen_min_y
            elif screen_max_y > self.screen_height - margin_y:
                self.offset_y -= screen_max_y - (self.screen_height - margin_y)
        else:
            # Карта больше экрана по высоте
            if screen_max_y < self.screen_height - margin_y:
                self.offset_y += (self.screen_height - margin_y) - screen_max_y
            elif screen_min_y > margin_y:
                self.offset_y -= screen_min_y - margin_y
