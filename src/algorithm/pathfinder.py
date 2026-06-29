from src.data_entities.zone import Zone


class Navigator:
    """
    Calculates and maintains a dynamic distance heatmap for drone pathfinding.

    Uses a modified breadth-first search (BFS) or Dijkstra-like approach,
    starting from the destination (end_hub) and propagating backwards through
    the graph. It calculates the cost (distance) from every zone to the finish,
    dynamically adjusting weights based on zone types and current traffic
    congestion.

    Attributes:
        queue (list): A queue used to manage nodes during the graph traversal.
        visited (set): A set intended to track visited nodes.
        start_hub (Zone): The initial spawn point for drones.
        end_hub (Zone): The final destination target for all drones.
        zones (dict[str, Zone]): A mapping of all available zones in the world.
        distances (dict[str, float]): The computed heatmap mapping zone names
            to their minimum movement cost to reach the end_hub.
    """
    def __init__(self, start_hub: Zone, end_hub: Zone,
                 zones: dict[str, Zone]):
        self.queue: list[Zone] = []
        self.visited: set[str] = set()
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.zones = zones
        self.distances: dict[str, float] = {}

    def build_heatmap(self) -> None:
        """
        Generates a distance gradient from the end_hub to all other
            reachable zones.

        Traverses the graph backwards from the destination. The base
            step cost is 1. The cost increases to 2 for 'restricted' zones,
            and dynamic penalties are added if a zone is currently at
            or over its maximum drone capacity. Zones marked as 'blocked'
            are treated as impassable.

        The resulting costs are saved in the `self.distances` attribute, which
        the simulation uses during the planning phase to find the path of least
        resistance.
        """
        self.distances = {name: float('inf') for name in self.zones}
        self.distances[self.end_hub.name] = 0

        self.queue.append(self.end_hub)

        while self.queue:
            current_hub = self.queue.pop(0)

            for link in current_hub.links:
                neighbor_name = link.target if link.source == current_hub.name\
                    else link.source
                neighbor_hub = self.zones[neighbor_name]

                if neighbor_hub.zone == "blocked":
                    continue

                step_cost = 1
                if current_hub.zone == "restricted":
                    step_cost = 2
                if (len(current_hub.current_drones) >= current_hub.max_drones
                        and current_hub.name != "end_hub"):
                    step_cost += len(current_hub.current_drones)
                new_distance = self.distances[current_hub.name] + step_cost

                if new_distance < self.distances[neighbor_name]:
                    self.distances[neighbor_name] = new_distance
                    self.queue.append(neighbor_hub)
