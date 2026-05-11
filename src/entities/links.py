from dataclasses import dataclass

@dataclass
class Link:
    target: str
    max_capacity: int
