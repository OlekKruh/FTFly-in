from dataclasses import dataclass, field
from typing import List
from .links import Link
from .drone import Drone


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
    incoming_count: int = 0
    outgoing_count: int = 0

    def add_dron_to_zone(self, drone: Drone):
        self.current_drones.append(drone)

    def rm_drone_from_zone(self):
        if self.current_drones:
            first_drone = self.current_drones.pop(0)
            return first_drone
        else:
            print("No drones detected")
            return None

    def is_free(self) -> bool:
        if self.name in ["end_hub", "goal"]:
            return True
        return (len(self.current_drones)
                - self.outgoing_count
                + self.incoming_count
                < self.max_drones)

    def book_arrival(self) -> bool:
        if self.is_free():
            self.incoming_count += 1
            return True
        return False

    def book_departure(self):
        self.outgoing_count += 1

    def clear_reservations(self):
        self.incoming_count = 0
        self.outgoing_count = 0
