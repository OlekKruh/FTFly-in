from dataclasses import dataclass


@dataclass
class Link:
    """
    Represents a directed pathway between two zones in the simulation.

    Manages the flow of drones between zones by enforcing a maximum
    capacity. It tracks how many drones have reserved passage through
    this link during the current simulation turn.

    Attributes:
        source (str): The name of the starting zone for this link.
        target (str): The name of the destination zone for this link.
        max_capacity (int): The maximum number of drones that can travel
            through this link in a single turn. Defaults to 1.
        current_load (int): The number of drones currently scheduled to
            travel through this link this turn. Defaults to 0.
    """
    source: str
    target: str
    max_capacity: int = 1
    current_load: int = 0

    def clear_reservations(self) -> None:
        """
        Resets the current load on the link to zero.

        This method is called at the end of each simulation turn to
        free up the link's capacity for the planning phase of the next turn.
        """
        self.current_load = 0
