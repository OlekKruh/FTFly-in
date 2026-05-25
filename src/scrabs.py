# def dispatch(self, line_list: List):
#     if line_list[0] == "nb_drones":
#         try:
#             if len(line_list[1]) != 1:
#                 error_exit(f"Error: 'nb_drones' expects 1 value, "
#                            f"got {len(line_list[1])}")
#             self.world.drones_quantity = int(line_list[1][0])
#         except (ValueError, IndexError, TypeError) as e:
#             error_exit(f"Error nb_drones: {e}")
#
#     elif line_list[0] in ["start_hub", "hub", "end_hub"]:
#         try:
#             main_param = line_list[1]
#             meta_data = line_list[2] if len(line_list) > 2 else None
#             if len(main_param) != 3:
#                 error_exit(f"Error: {line_list[0]} expects [name, x, y],"
#                            f" got {main_param}")
#             hub_name, hub_x, hub_y = (
#                 line_list[1][0],
#                 int(line_list[1][1]),
#                 int(line_list[1][2])
#             )
#             self.world.add_zone_to_map(
#                 [hub_name, hub_x, hub_y],
#                 meta_data  # выпадаем за список нужно условие
#             )
#         except (ValueError, IndexError) as e:
#             error_exit(f"Error hub: Invalid main parameters format "
#                        f"or missing values. {e}")
#
#     elif line_list[0] == "connection":
#         try:
#             connection = line_list[1]
#             meta_data = line_list[2] if len(line_list) > 2 else None
#             if len(connection) != 1:
#                 error_exit("Invalid value. "
#                            "Onli one connection must be in line "
#                            f"got {connection}")
#             self.world.add_relation_to_map(connection[0], meta_data[0])
#         except (ValueError, IndexError) as e:
#             error_exit(f"Error: Invalid connection parameters format "
#                        f"or missing values. {e}")
#
#     def add_zone_to_map(self, main_arg_list: List, meta_arg_list: List):
#         name, zone_x, zone_y = main_arg_list
#         self.zones_map[name] = Zone(name, int(zone_x), int(zone_y))
#
#         if meta_arg_list:
#             for i in meta_arg_list:
#                 key, value = i.split("=")
#                 match key:
#                     case "zone":
#                         if value in ["normal", "blocked",
#                                      "restricted", "priority"]:
#                             self.zones_map[name].zone_type = value
#                         else:
#                             error_exit("Invalid zone type!")
#                     case "color":
#                         if value.strip().isalpha():
#                             self.zones_map[name].color = value
#                         else:
#                             error_exit("Invalid color name!"
#                                        " Must be a single word.")
#                     case "max_drones":
#                         try:
#                             self.zones_map[name].max_drones = int(value)
#                         except ValueError:
#                             error_exit(f"Invalid value for max_drones:"
#                                        f" '{value}'. Must be an integer.")
#                     case _:
#                         error_exit("Invalid key in meta data!")

# ==========================================
# if len(meta_data) != 1:
#     error_exit("World Map (add_relation_to_map):\n"
#                f"Link Expects meta_data len 1\n"
#                f"Example 'key=value', got {meta_data}")
# try:
#     meta_key, meta_value = meta_data[0].split("=")
#     if meta_key != "max_link_capacity":
#         error_exit("World Map (add_relation_to_map):\n"
#                    "Invalid meta_key Expected "
#                    "'max_link_capacity'\n"
#                    f"got {meta_key}")
#     try:
#         capacity = int(meta_value)
#     except ValueError as e:
#         error_exit("World Map (add_relation_to_map):\n"
#                    "Invalid meta_value format Expected 'int'\n"
#                    f"got {e}")
# except ValueError as e:
#     error_exit("World Map (add_relation_to_map):\n"
#                "Invalid meta_data format Expected 'key=value'\n"
#                f"got {e}")
# ==========================================
# PARSING OF ALL PATHS IN DIR MAPS
# searcher = MapSearcher('./maps')
# found_maps = searcher.scan_maps()
# for key, path in found_maps.items():
#     print(f"[{key}] - {path}")

# PARSING OF SPECIFIC MAP ON PATH
# print("Start")
#
# world = World()
# x = FileParser("./maps/hard/02_capacity_hell.txt", world)
# x.pars_map()
# world.init_drones()
#
# for key, value in world.zones_map.items():
#     print(f"{key}: {value}")
#
# print("Fin")


# class Camera:
#     def __init__(self, screen_width: int, screen_height: int):
#         self.screen_width = screen_width
#         self.screen_height = screen_height
#
#         self.scale = 1.5
#         self.offset_x = 0.0
#         self.offset_y = 0.0
#         self.padding = 10
#
#         self.world_min_x = 0
#         self.world_max_x = 0
#         self.world_min_y = 0
#         self.world_max_y = 0
#
#     def world_to_screen(self, world_x: float,
#                         world_y: float) -> tuple[int, int]:
#         """
#         Преобразует координаты карты в пиксели экрана.
#         """
#         screen_x = int((world_x * self.scale) + self.offset_x)
#         screen_y = int((world_y * self.scale) + self.offset_y)
#         return screen_x, screen_y
#
#     def auto_fit(self, zones_map: dict):
#         """
#         Вычисляет нужный масштаб и смещение,
#         чтобы вписать всю карту в экран.
#         """
#         if not zones_map:
#             return
#
#         # 1. Находим крайние точки мира (Bounding Box)
#         # Предполагается, что у твоих зон есть атрибуты .x и .y
#         self.world_min_x = min(zone.zone_x for zone in zones_map.values())
#         self.world_max_x = max(zone.zone_x for zone in zones_map.values())
#         self.world_min_y = min(zone.zone_y for zone in zones_map.values())
#         self.world_max_y = max(zone.zone_y for zone in zones_map.values())
#
#         # 2. Вычисляем физический размер карты
#         world_w = self.world_max_x - self.world_min_x
#         world_h = self.world_max_y - self.world_min_y
#
#         # Защита от деления на ноль (если на карте всего одна зона)
#         if world_w == 0:
#             world_w = 1
#         if world_h == 0:
#             world_h = 1
#
#         # 3. Считаем доступное место на экране с учетом отступов
#         available_w = self.screen_width - (self.padding * 2)
#         available_h = self.screen_height - (self.padding * 2)
#
#         # 4. Вычисляем масштаб
#         scale_x = available_w / world_w
#         scale_y = available_h / world_h
#
#         # Берем минимальный масштаб, чтобы карта влезла
#         # целиком и не исказились пропорции
#         self.scale = min(scale_x, scale_y)
#
#         # 5. Вычисляем смещение для центрирования
#         # Находим центр экрана
#         center_screen_x = self.screen_width / 2
#         center_screen_y = self.screen_height / 2
#
#         # Находим геометрический центр карты
#         center_world_x = self.world_min_x + (world_w / 2)
#         center_world_y = self.world_min_y + (world_h / 2)
#
#         # Смещение = центр экрана минус (масштабированный центр мира)
#         self.offset_x = center_screen_x - (center_world_x * self.scale)
#         self.offset_y = center_screen_y - (center_world_y * self.scale)
#
#     def apply_bounds(self):
#         # Отдельные настройки отступов
#         margin_x = 200
#         margin_y = 200
#
#         # Физические размеры карты в пикселях при текущем зуме
#         map_w = (self.world_max_x - self.world_min_x) * self.scale
#         map_h = (self.world_max_y - self.world_min_y) * self.scale
#
#         # Текущие позиции крайних точек на экране
#         screen_min_x = (self.world_min_x * self.scale) + self.offset_x
#         screen_max_x = (self.world_max_x * self.scale) + self.offset_x
#         screen_min_y = (self.world_min_y * self.scale) + self.offset_y
#         screen_max_y = (self.world_max_y * self.scale) + self.offset_y
#
#         # --- Горизонталь (X) ---
#         if map_w < self.screen_width - (margin_x * 2):
#             # Карта меньше доступной зоны: не даем краям выехать за margin
#             if screen_min_x < margin_x:
#                 self.offset_x += margin_x - screen_min_x
#             elif screen_max_x > self.screen_width - margin_x:
#                 self.offset_x -= screen_max_x - (self.screen_width - margin_x)
#         else:
#             # Карта больше экрана: цепляем края за margin
#             if screen_max_x < self.screen_width - margin_x:
#                 self.offset_x += (self.screen_width - margin_x) - screen_max_x
#             elif screen_min_x > margin_x:
#                 self.offset_x -= screen_min_x - margin_x
#
#         # --- Вертикаль (Y) ---
#         if map_h < self.screen_height - (margin_y * 2):
#             # Карта меньше доступной зоны по высоте
#             if screen_min_y < margin_y:
#                 self.offset_y += margin_y - screen_min_y
#             elif screen_max_y > self.screen_height - margin_y:
#                 self.offset_y -= screen_max_y - (self.screen_height - margin_y)
#         else:
#             # Карта больше экрана по высоте
#             if screen_max_y < self.screen_height - margin_y:
#                 self.offset_y += (self.screen_height - margin_y) - screen_max_y
#             elif screen_min_y > margin_y:
#                 self.offset_y -= screen_min_y - margin_y