from dataclasses import dataclass, field
from typing import Dict, List
from zone import Zone
from drone import Drone
from src.parser.parser import error_exit


@dataclass
class World:
    """
    список дронов
    список нодов
    словарь соединений зон
    """
    drones_quantity: int
    drone_list: List[Drone] = field(default_factory=list)
    zones_map: Dict[str, Zone] = field(default_factory=dict)

    def add_drone_to_map(self):
        ...

    def add_zone_to_map(self, main_arg_list: List, meta_arg_list: List):
        name, zone_x, zone_y = main_arg_list
        self.zones_map[name] = Zone(name, int(zone_x), int(zone_y))

        if meta_arg_list:
            for i in meta_arg_list:
                key, value = i.split("=")
                match key:
                    case "zone":
                        self.zones_map[name].zone_type = value
                    case "color":
                        self.zones_map[name].color = value
                    case "max_drones":
                        self.zones_map[name].max_drones = value
                    case _:
                        error_exit("Invalid key in meta data!")

    def add_relation_to_map(self):
        ...
