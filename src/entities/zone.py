from dataclasses import dataclass, field
from typing import List
from .links import Link


@dataclass
class Zone:
    name: str
    zone_x: int
    zone_y: int
    zone_type: str = "normal"
    color: str = None
    max_drones: int = 1
    current_drones: List[int] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)

    def add_dron_to_zone(self):
        # TODO
        ...

    def rm_drone_from_zone(self):
        # TODO
        ...

    def add_zone_link(self):
        # TODO
        ...
