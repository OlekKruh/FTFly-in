from dataclasses import dataclass, field
from typing import Dict, List
from .zone import Zone
from .drone import Drone
from .links import Link
from src.parser.parser import error_exit


@dataclass
class World:
    drones_quantity: int = 0
    drone_list: List[Drone] = field(default_factory=list)
    start_hub: Zone = None
    end_hub: Zone = None
    zones_map: Dict[str, Zone] = field(default_factory=dict)

    @staticmethod
    def _safe_int(value: str, field_name: str):
        try:
            return int(value)
        except ValueError:
            error_exit("World Map (_safe_int):\n"
                       f"'{field_name}' must be an integer, got '{value}'")

    def _parse_hub_meta(self, hub_name: str, meta_data: List[str]) -> Dict:
        meta_dict = {}
        for item in meta_data:
            try:
                key, value = item.split("=", 1)
                match key:
                    case "zone":
                        if value in ["normal", "blocked",
                                     "restricted", "priority"]:
                            meta_dict[key] = value
                        else:
                            error_exit(f"World Map (_parse_hub_meta):\n"
                                       f"Invalid zone type '{value}'"
                                       f" for '{hub_name}'")
                    case "color":
                        if value.strip().isalpha():
                            meta_dict[key] = value
                        else:
                            error_exit(f"World Map (_parse_hub_meta):\n"
                                       f"Invalid color for '{hub_name}'")
                    case "max_drones":
                        meta_dict[key] = (
                            self._safe_int(value,
                                           f"max_drones for '{hub_name}'"))
                    case "max_link_capacity":
                        meta_dict[key] = (
                            self._safe_int(value,
                                           f"max_link_capacity '{hub_name}'"))
                    case _:
                        error_exit(f"World Map (_parse_hub_meta):\n"
                                   f"Invalid key '{key}' in meta data for"
                                   f" '{hub_name}'")
            except ValueError:
                error_exit("World Map (_parse_hub_meta):\n"
                           f"Invalid metadata format '{item}'."
                           f" Expected 'key=value'")
        return meta_dict

    def set_drone_quantity(self, drone_quant: List):
        if len(drone_quant) != 1:
            error_exit("World Map (set_drone_quantity):\n"
                       f"'nb_drones' expects 1 value, got {len(drone_quant)}")
        self.drones_quantity = self._safe_int(drone_quant[0], "nb_drones")

    def add_zone_to_map(self, head: str, main_data: List, meta_data: List):
        if len(main_data) != 3:
            error_exit("World Map (add_zone_to_map):\n"
                       f"Zone expects [name, x, y], got {main_data}")

        name, x_str, y_str = main_data
        x = self._safe_int(x_str, f"X coord for zone '{name}'")
        y = self._safe_int(y_str, f"Y coord for zone '{name}'")

        new_zone = Zone(name, x, y)

        meta_dict = self._parse_hub_meta(name, meta_data)
        for key, value in meta_dict.items():
            setattr(new_zone, key, value)

        self.zones_map[name] = new_zone

        if head == "start_hub":
            self.start_hub = new_zone
        elif head == "end_hub":
            self.end_hub = new_zone

    def add_relation_to_map(self, main_data: List, meta_data: List):
        """
        main_data: [start-gate1] must be one arg in list!
        meta_data: [max_link_capacity=1] must be onli
        max_link_capacity and one arg in list = only to int

        main_data break on "-" find names add opposite elem like Link object
        Zone.links -> Link.target, Zone.links -> Link.max_capacity
        connection one bidirectional

        """
        if len(main_data) != 1:
            error_exit("World Map (add_relation_to_map):\n"
                       f"Link Expects main_data len 1\n"
                       f"Example 'name-name', got {main_data}")
        try:
            name1, name2 = main_data[0].split("-")
            zone1 = self.zones_map.get(name1)
            zone2 = self.zones_map.get(name2)
            if not zone1 or not zone2:
                error_exit("World Map (add_relation_to_map):\n"
                           "Invalid zone name. No such zone in world map.\n"
                           f"Expected zones with name = {name1} and name = {name2}\n"
                           f"Zone 1: {zone1}\n"
                           f"Zone 2: {zone2}\n")

            capacity = 1
            if meta_data:
                meta_dict = self._parse_hub_meta(main_data[0], meta_data)
                capacity = meta_dict.get("max_link_capacity", 1)

            zone1.links.append(Link(name2, capacity))
            zone2.links.append(Link(name1, capacity))
        except ValueError as e:
            error_exit("World Map (add_relation_to_map):\n"
                       "Invalid main_data format Expected 'name-name'\n"
                       f"got {e}")

    def init_drones(self):
        if not self.start_hub:
            error_exit("World Map (init_drones):\n"
                       "No start_hub defined in map!")
        for drone_id in range(1, self.drones_quantity + 1):
            drone_name = f"D{drone_id}"
            new_drone = Drone(drone_id=drone_name)
            self.drone_list.append(new_drone)
            self.start_hub.add_dron_to_zone(new_drone)
