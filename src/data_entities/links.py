from dataclasses import dataclass

@dataclass
class Link:
    source: str
    target: str
    max_capacity: int = 1
