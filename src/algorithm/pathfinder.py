from src.data_entities.zone import Zone


class Navigator:
    def __init__(self, start_hub: Zone, end_hub: Zone,
                 zones: dict[str, Zone]):
        self.queue = []
        self.visited = set()
        # self.came_from = {}
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.zones = zones
        self.distances = {}

    def build_heatmap(self):
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
