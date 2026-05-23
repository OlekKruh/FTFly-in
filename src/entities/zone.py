from dataclasses import dataclass, field
from typing import List
from .links import Link
from .menu_drone import Drone


@dataclass
class Zone:
    name: str
    zone_x: int
    zone_y: int
    zone: str = "normal"
    color: str = None
    max_drones: int = 1
    current_drones: List[Drone] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)

    def add_dron_to_zone(self, drone: Drone):
        self.current_drones.append(drone)

    def rm_drone_from_zone(self):
        if self.current_drones:
            first_drone = self.current_drones.pop(0)
            return first_drone
        else:
            print("No drones detected")
            return None
