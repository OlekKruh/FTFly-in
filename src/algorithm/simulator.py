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
            print(f"Simulation completed in {self.turn} turns.")
            return

        active_drones.sort(key=lambda d: self.navigator.distances.get(
            d.current_zone.name, float('inf')))

        moves_to_execute = []
        moved_this_turn = []

        for drone in active_drones:
            current_zone = drone.current_zone
            best_neighbor = None
            best_link = None

            min_dist = self.navigator.distances.get(
                current_zone.name, float('inf'))

            for link in current_zone.links:
                neighbor_name = link.target
                if (drone.previous_zone and
                        neighbor_name == drone.previous_zone.name):
                    continue
                neighbor = self.world.zones_map.get(neighbor_name)

                if not neighbor:
                    continue

                neighbor_dist = self.navigator.distances.get(
                    neighbor_name, float('inf'))

                if neighbor_dist < min_dist:
                    if link.current_load < link.max_capacity:
                        if (len(neighbor.current_drones)
                                + neighbor.incoming_count
                                - neighbor.outgoing_count
                                < neighbor.max_drones):
                            min_dist = neighbor_dist
                            best_neighbor = neighbor
                            best_link = link

            if best_neighbor:
                best_neighbor.book_arrival()
                best_link.current_load += 1
                current_zone.book_departure()
                moves_to_execute.append((drone, current_zone, best_neighbor))

        for drone, from_zone, to_zone in moves_to_execute:
            if drone in from_zone.current_drones:
                from_zone.current_drones.remove(drone)

            to_zone.add_dron_to_zone(drone)
            drone.previous_zone = drone.current_zone
            drone.current_zone = to_zone

            moved_this_turn.append(f"{drone.drone_id}-{to_zone.name}")

        for zone in self.world.zones_map.values():
            zone.clear_reservations()

        if moved_this_turn:
            print(" ".join(moved_this_turn))

        self.turn += 1
