from src.algorithm.pathfinder import Navigator
from src.data_entities.world_map import World


class Simulator:
    """
    Orchestrates the turn-based execution of the drone routing simulation.

    Connects the World state and the Navigator's pathfinding logic to
    move drones step-by-step towards their destination. It manages the
    turn counter and checks for the overall simulation completion state.

    Attributes:
        world (World): The simulation environment containing zones,
            links, and drones.
        navigator (Navigator): The pathfinding engine used to generate
            distance heatmaps.
        turn (int): The current turn number of the simulation.
        finished (bool): Flag indicating whether all drones have successfully
            reached the end_hub.
    """
    def __init__(self, world: World, navigator: Navigator):
        self.world = world
        self.navigator = navigator
        self.turn = 0
        self.finished = False

    def run_step(self) -> None:
        """
        Executes a single, complete turn of the simulation.

        The execution follows a strict pipeline to ensure
            collision-free movement:
        1. Heatmap Generation: Updates pathfinding costs based
            on current traffic.
        2. Status Check: Identifies active drones and triggers
            completion if empty.
        3. Queue Sorting: Prioritizes drones closest to the destination
            to prevent traffic jams (head-of-line blocking).
        4. Planning Phase: Iterates through sorted drones to find the optimal
            valid move temporarily reserving space in target zones and on links
        5. Execution Phase: Physically moves the drones based on the
            approved plans.
        6. Cleanup Phase: Resets all temporary turn-based reservations.

        Outputs the movement log for the current turn to the console.
        """
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
            d.current_zone.name
            if d.current_zone is not None else "", float('inf')))

        moves_to_execute = []
        moved_this_turn = []

        for drone in active_drones:
            current_zone = drone.current_zone
            if current_zone is None:
                continue
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

            if best_neighbor and best_link:
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
