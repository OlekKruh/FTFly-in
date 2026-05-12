from dataclasses import dataclass, field
from typing import Dict, List
from .zone import Zone
from .drone import Drone
from src.parser.parser import error_exit


@dataclass
class World:
    drones_quantity: int = 0
    drone_list: List[Drone] = field(default_factory=list)
    start_hub: Zone = None
    end_hub: Zone = None
    zones_map: Dict[str, Zone] = field(default_factory=dict)

    def _safe_int(self, value: str, field_name: str) -> int:
        try:
            return int(value)
        except ValueError:
            error_exit("World Map (_safe_int):\n"
                       f"'{field_name}' must be an integer, got '{value}'")

    def _parse_meta(self, hub_name: str, meta_data: List[str]) -> Dict:
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
                            error_exit(f"World Map (_parse_meta):\n"
                                       f"Invalid zone type '{value}'"
                                       f" for '{hub_name}'")
                    case "color":
                        if value.strip().isalpha():
                            meta_dict[key] = value
                        else:
                            error_exit(f"World Map (_parse_meta):\n"
                                       f"Invalid color for '{hub_name}'")
                    case "max_drones":
                        meta_dict[key] = (
                            self._safe_int(value,
                                           f"max_drones for '{hub_name}'"))
                    case _:
                        error_exit(f"World Map (_parse_meta):\n"
                                   f"Invalid key '{key}' in meta data for"
                                   f" '{hub_name}'")
            except ValueError:
                error_exit("World Map (_parse_meta):\n"
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

        meta_dict = self._parse_meta(name, meta_data)
        for key, value in meta_dict.items():
            setattr(new_zone, key, value)

        self.zones_map[name] = new_zone

        if head == "start_hub":
            self.start_hub = new_zone
        elif head == "end_hub":
            self.end_hub = new_zone

    def add_relation_to_map(self, main_data: List, meta_data: List):
        ...
