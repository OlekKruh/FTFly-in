from dataclasses import dataclass, field
from typing import Dict, List
from .zone import Zone
from .drone import Drone
from src.parser.parser import error_exit


@dataclass
class World:
    drones_quantity: int = 0
    drone_list: List[Drone] = field(default_factory=list)
    zones_map: Dict[str, Zone] = field(default_factory=dict)

    def add_zone_to_map(self, main_arg_list: List, meta_arg_list: List):
        name, zone_x, zone_y = main_arg_list
        self.zones_map[name] = Zone(name, int(zone_x), int(zone_y))

        if meta_arg_list:
            for i in meta_arg_list:
                key, value = i.split("=")
                match key:
                    case "zone":
                        if value in ["normal", "blocked",
                                     "restricted", "priority"]:
                            self.zones_map[name].zone_type = value
                        else:
                            error_exit("Invalid zone type!")
                    case "color":
                        if value.strip().isalpha():
                            self.zones_map[name].color = value
                        else:
                            error_exit("Invalid color name!"
                                       " Must be a single word.")
                    case "max_drones":
                        try:
                            self.zones_map[name].max_drones = int(value)
                        except ValueError:
                            error_exit(f"Invalid value for max_drones:"
                                       f" '{value}'. Must be an integer.")
                    case _:
                        error_exit("Invalid key in meta data!")

    def add_drone_to_map(self):
        # TODO
        ...

    def add_relation_to_map(self, link_arg: str, meta_arg: str):
        zone1, zone2 = link_arg.split("-")
        key, value = meta_arg.split("=")
        ...
