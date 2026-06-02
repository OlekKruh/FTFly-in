from src.data_entities.zone import Zone
from src.utils_func.exit_func import error_exit


class Navigator:
    def __init__(self, start_hub: Zone, end_hub: Zone,
                 zones: dict[str, Zone]):
        self.queue = []
        self.visited = set()
        self.came_from = {}
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.zones = zones

    def _build_path(self) -> list[str]:
        path = []
        current = self.end_hub.name

        while current is not None:
            path.append(current)
            current = self.came_from[current]

        path.reverse()
        return path

    def broad_search(self) -> list[str]:
        self.queue.append(self.start_hub)
        self.visited.add(self.start_hub.name)
        self.came_from[self.start_hub.name] = None

        while self.queue:
            current_hub = self.queue.pop(0)

            if current_hub == self.end_hub:
                return self._build_path()

            for link in current_hub.links:
                neighbor_name = link.target

                if neighbor_name not in self.visited:
                    self.visited.add(neighbor_name)
                    self.came_from[neighbor_name] = current_hub.name

                    neighbor_hub = self.zones[neighbor_name]
                    self.queue.append(neighbor_hub)
        return []


