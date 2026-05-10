from dataclasses import dataclass, field
from typing import List


@dataclass
class Zone:
    name: str
    zone_x: int
    zone_y: int
    links: List[str]
    zone_type: str = "normal"
    color: str = None
    max_drones: int = 1
    current_drones: List[int] = field(default_factory=list)

    def add_dron_to_zone(self):
        ...

    def rm_drone_from_zone(self):
        ...
