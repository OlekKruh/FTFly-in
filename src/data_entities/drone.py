from dataclasses import dataclass
from typing import Any


@dataclass
class Drone:
    """
    Represents a drone navigating through the simulation world.

    Keeps track of the drone's unique identifier and its location history.
    The location history is primarily used by the pathfinding algorithm
    to prevent the drone from making U-turns (moving back to the zone
    it just came from).

    Attributes:
        drone_id (str): The unique identifier of the drone (e.g., "D1").
        current_zone (Zone | None): The zone where the drone is currently
         located.
        previous_zone (Zone | None): The zone where the drone was in the
         previous turn.
    """
    drone_id: str
    current_zone: Any = None
    previous_zone: Any = None
