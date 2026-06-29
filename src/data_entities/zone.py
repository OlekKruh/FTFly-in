from dataclasses import dataclass, field
from typing import List
from .links import Link
from .drone import Drone


@dataclass
class Zone:
    """
    Represents a physical or logical zone in the simulation world.

    A zone acts as a node in the network where drones can stay,
     arrive, or depart.
    It manages its own capacity and tracks reservations to prevent collisions
    or overcrowding during a single simulation turn.

    Attributes:
        name (str): The unique identifier of the zone.
        zone_x (int): The X-coordinate of the zone for visual rendering.
        zone_y (int): The Y-coordinate of the zone for visual rendering.
        zone (str): The type of the zone (e.g., "normal", "restricted").
        color (str, optional): The color of the zone for visualization.
        max_drones (int): The maximum number of drones allowed in the zone
         simultaneously.
        current_drones (List[Drone]): The list of drones currently residing
         in the zone.
        links (List[Link]): The outbound connections to neighboring zones.
        incoming_count (int): The number of drones that have booked an arrival
         this turn.
        outgoing_count (int): The number of drones that have booked a departure
         this turn.
    """
    name: str
    zone_x: int
    zone_y: int
    zone: str = "normal"
    color: str | None = None
    max_drones: int = 1
    current_drones: List[Drone] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)
    incoming_count: int = 0
    outgoing_count: int = 0

    def add_dron_to_zone(self, drone: Drone) -> None:
        """
        Adds a drone to the zone's current roster.

        Args:
            drone (Drone): The drone object to be added to the zone.
        """
        self.current_drones.append(drone)

    def rm_drone_from_zone(self) -> None | Drone:
        """
        Removes and returns the first drone from the zone (FIFO order).

        Returns:
            Drone: The removed drone object if the zone is not empty.
            None: If no drones are currently in the zone.
        """
        if self.current_drones:
            first_drone = self.current_drones.pop(0)
            return first_drone
        else:
            print("No drones detected")
            return None

    def is_free(self) -> bool:
        """
        Checks if the zone has available capacity for a new drone.

        Evaluates the current capacity by accounting for the drones currently
        present, those scheduled to leave, and those scheduled to arrive.
        The "end_hub" and "goal" zones are considered to have infinite
         capacity.

        Returns:
            bool: True if there is space for at least one more drone,
             False otherwise.
        """
        if self.name in ["end_hub", "goal"]:
            return True
        return (len(self.current_drones)
                - self.outgoing_count
                + self.incoming_count
                < self.max_drones)

    def book_arrival(self) -> bool:
        """
        Attempts to reserve a spot for an incoming drone.

        If the zone is free, it increments the incoming reservation counter.

        Returns:
            bool: True if the booking was successful,
             False if the zone is full.
        """
        if self.is_free():
            self.incoming_count += 1
            return True
        return False

    def book_departure(self) -> None:
        """
        Registers that a drone is planning to leave this zone
         during the current turn.

        Increments the outgoing reservation counter, which logically frees up
        space for incoming drones during the planning phase.
        """
        self.outgoing_count += 1

    def clear_reservations(self) -> None:
        """
        Resets all temporary turn-based reservation counters.

        This should be called at the end of each simulation turn to clear
        incoming/outgoing counts and reset the load on all outbound links.
        """
        self.incoming_count = 0
        self.outgoing_count = 0
        for link in self.links:
            link.current_load = 0
