from dataclasses import dataclass, field
from typing import Dict, List, Any
from .zone import Zone
from .drone import Drone
from .links import Link
from ..utils_func.exit_func import error_exit


@dataclass
class World:
    """
    Represents the simulation world containing all zones, connections,
     and drones.

    This class acts as the central data structure for the parsed map,
    handling the instantiation of zones, bidirectional links, and the
    initial placement of the drone fleet.

    Attributes:
        drones_quantity (int): Total number of drones in the simulation.
        drone_list (List[Drone]): Collection of all instantiated drone objects.
        start_hub (Zone): The designated starting zone where drones spawn.
        end_hub (Zone): The designated final destination zone for all drones.
        zones_map (Dict[str, Zone]): A mapping of zone names to their Zone
         objects.
    """
    drones_quantity: int = 0
    drone_list: List[Drone] = field(default_factory=list)
    start_hub: Zone | None = None
    end_hub: Zone | None = None
    zones_map: Dict[str, Zone] = field(default_factory=dict)

    @staticmethod
    def _safe_int(value: str, field_name: str) -> int:
        """
        Safely converts a string value to an integer.

        Args:
            value (str): The string representing the numerical value.
            field_name (str): The name of the field being processed
            (used for error logging).

        Returns:
            int: The successfully parsed integer value.

        Raises:
            SystemExit: If the value cannot be converted to an integer.
        """
        try:
            return int(value)
        except ValueError:
            error_exit("World Map (_safe_int):\n"
                       f"'{field_name}' must be an integer, got '{value}'")

    def _parse_hub_meta(self, hub_name: str,
                        meta_data: List[str]) -> Dict[Any, Any]:
        """
        Parses a list of metadata strings in 'key=value' format
        for a specific hub.

        Validates metadata keys (zone, color, max_drones, max_link_capacity)
        and their corresponding values.

        Args:
            hub_name (str): The name of the hub associated with the metadata.
            meta_data (List[str]): A list of metadata strings.

        Returns:
            Dict: A dictionary containing the parsed and validated metadata
            key-value pairs.

        Raises:
            SystemExit: If an invalid key, unsupported value, or malformed
            string is detected.
        """
        meta_dict: dict[str, Any] = {}
        for item in meta_data:
            try:
                key, value = item.split("=", 1)
                match key:
                    case "zone":
                        if value in ["normal", "blocked",
                                     "restricted", "priority"]:
                            meta_dict[key] = value
                        else:
                            error_exit(f"World Map (_parse_hub_meta):\n"
                                       f"Invalid zone type '{value}'"
                                       f" for '{hub_name}'")
                    case "color":
                        if value.strip().isalpha():
                            meta_dict[key] = value
                        else:
                            error_exit(f"World Map (_parse_hub_meta):\n"
                                       f"Invalid color for '{hub_name}'")
                    case "max_drones":
                        meta_dict[key] = (
                            self._safe_int(value,
                                           f"max_drones for '{hub_name}'"))
                    case "max_link_capacity":
                        meta_dict[key] = (
                            self._safe_int(value,
                                           f"max_link_capacity '{hub_name}'"))
                    case _:
                        error_exit(f"World Map (_parse_hub_meta):\n"
                                   f"Invalid key '{key}' in meta data for"
                                   f" '{hub_name}'")
            except ValueError:
                error_exit("World Map (_parse_hub_meta):\n"
                           f"Invalid metadata format '{item}'."
                           f" Expected 'key=value'")
        return meta_dict

    def set_drone_quantity(self, drone_quant: List[Any]) -> None:
        """
        Sets the total number of drones for the simulation.

        Args:
            drone_quant (List[str]): A list expected to contain exactly
            one string representing the total drone count.

        Raises:
            SystemExit: If the list does not contain exactly one element
            or if the value is not a valid integer.
        """
        if len(drone_quant) != 1:
            error_exit("World Map (set_drone_quantity):\n"
                       f"'nb_drones' expects 1 value, got {len(drone_quant)}")
        self.drones_quantity = self._safe_int(drone_quant[0], "nb_drones")

    def add_zone_to_map(self, head: str, main_data: List[Any],
                        meta_data: List[Any]) -> None:
        """
        Creates a Zone instance from parsed data and adds it to the world map.

        Sets up the zone's coordinates and applies any additional metadata
        (like capacity or color). It also identifies and assigns the start
        and end hubs.

        Args:
            head (str): The logical type of the hub
                (e.g., "start_hub", "end_hub", "hub").
            main_data (List[str]): A list containing exactly
                three elements: [name, x, y].
            meta_data (List[str]): Optional metadata strings to
            configure the zone.

        Raises:
            SystemExit: If main_data does not have exactly 3 elements or
            coordinates are invalid.
        """
        if len(main_data) != 3:
            error_exit("World Map (add_zone_to_map):\n"
                       f"Zone expects [name, x, y], got {main_data}")

        name, x_str, y_str = main_data
        x = self._safe_int(x_str, f"X coord for zone '{name}'")
        y = self._safe_int(y_str, f"Y coord for zone '{name}'")

        new_zone = Zone(name, x, y)

        meta_dict = self._parse_hub_meta(name, meta_data)
        for key, value in meta_dict.items():
            setattr(new_zone, key, value)

        self.zones_map[name] = new_zone

        if head == "start_hub":
            self.start_hub = new_zone
        elif head == "end_hub":
            self.end_hub = new_zone

    def add_relation_to_map(self, main_data: List[Any],
                            meta_data: List[Any]) -> None:
        """
        Creates a bidirectional link between two existing zones in
        the world map.

        Parses the relationship string, validates that both zones exist,
        and sets up the maximum link capacity if provided in the metadata.

        Args:
            main_data (List[str]): A list containing exactly one string in the
                format 'zone1-zone2'.
            meta_data (List[str]): Optional metadata specifying connection
                attributes (e.g., max_link_capacity).

        Raises:
            SystemExit: If the relation format is invalid, or if either
            zone does not exist in the zones_map.
        """
        if len(main_data) != 1:
            error_exit("World Map (add_relation_to_map):\n"
                       f"Link Expects main_data len 1\n"
                       f"Example 'name-name', got {main_data}")
        try:
            name1, name2 = main_data[0].split("-")
            zone1 = self.zones_map.get(name1)
            zone2 = self.zones_map.get(name2)
            if not zone1 or not zone2:
                error_exit("World Map (add_relation_to_map):\n"
                           "Invalid zone name. No such zone in world map.\n"
                           f"Expected zones with name = {name1} "
                           f"and name = {name2}\n"
                           f"Zone 1: {zone1}\n"
                           f"Zone 2: {zone2}\n")

            capacity = 1
            if meta_data:
                meta_dict = self._parse_hub_meta(main_data[0], meta_data)
                capacity = meta_dict.get("max_link_capacity", 1)

            zone1.links.append(Link(name1, name2, capacity))
            zone2.links.append(Link(name2, name1, capacity))
        except ValueError as e:
            error_exit("World Map (add_relation_to_map):\n"
                       "Invalid main_data format Expected 'name-name'\n"
                       f"got {e}")

    def init_drones(self) -> None:
        """
        Instantiates drone objects and places them in the starting hub.

        Iterates up to the configured drones_quantity, creating a Drone
        instance with a unique ID (e.g., 'D1') and adding it to
        the start_hub's roster.

        Raises:
            SystemExit: If the start_hub has not been defined in the
            map configuration.
        """
        if not self.start_hub:
            error_exit("World Map (init_drones):\n"
                       "No start_hub defined in map!")
        for drone_id in range(1, self.drones_quantity + 1):
            drone_name = f"D{drone_id}"
            new_drone = Drone(drone_name, self.start_hub, None)
            self.drone_list.append(new_drone)
            self.start_hub.add_dron_to_zone(new_drone)
