class Simulator:
    def __init__(self, world, navigator):
        self.world = world
        self.navigator = navigator
        self.turn = 0
        self.finished = False

    def run_step(self):
        self.navigator.build_heatmap()
        if self.finished:
            return

        active_drones = [d for d in self.world.drone_list
                         if d.current_zone != self.world.end_hub]

        if not active_drones:
            self.finished = True
            print(f"Симуляция завершена за {self.turn} ходов.")
            return

        active_drones.sort(key=lambda d: self.navigator.distances.get(
            d.current_zone.name, float('inf')))

        moves_to_execute = []
        moved_this_turn = []

        for drone in active_drones:
            current_zone = drone.current_zone
            best_neighbor = None
            current_dist = self.navigator.distances.get(
                current_zone.name, float('inf'))

            for link in current_zone.links:
                neighbor_name = link.target
                neighbor = self.world.zones_map.get(neighbor_name)

                if not neighbor:
                    continue

                neighbor_dist = self.navigator.distances.get(
                    neighbor_name, float('inf'))

                if neighbor_dist < current_dist:
                    if neighbor.book_arrival():
                        best_neighbor = neighbor
                        break

            if best_neighbor:
                current_zone.book_departure()
                moves_to_execute.append((drone, current_zone, best_neighbor))

        for drone, from_zone, to_zone in moves_to_execute:
            if drone in from_zone.current_drones:
                from_zone.current_drones.remove(drone)

            to_zone.add_dron_to_zone(drone)
            drone.current_zone = to_zone

            moved_this_turn.append(f"{drone.drone_id}-{to_zone.name}")

        for zone in self.world.zones_map.values():
            zone.clear_reservations()

        if moved_this_turn:
            print(" ".join(moved_this_turn))

        self.turn += 1
