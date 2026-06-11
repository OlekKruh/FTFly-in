from dataclasses import dataclass


@dataclass
class Link:
    source: str
    target: str
    max_capacity: int = 1
    current_load: int = 0

    def clear_reservations(self):
        self.current_load = 0
