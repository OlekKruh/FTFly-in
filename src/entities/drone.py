from dataclasses import dataclass
from zone import Zone


@dataclass
class Drone:
    drone_id: str
    position: Zone
