from pathlib import Path
from typing import List, Any

from src.data_entities.world_map import World
from src.utils_func.exit_func import error_exit


class FileParser:
    """
    Parses a text-based map file and populates the simulation world.

    Reads the configuration file line by line, extracting the number of drones,
    zone definitions (start, normal, end), connections, and their respective
    metadata, then dispatches this information to the provided World object.

    Args:
        file_path (str): The string path to the map configuration file.
        world_obj (World): The World object instance to be populated with
            parsed data.

    Attributes:
        path (Path): The pathlib.Path object representing the file path.
        world (World): The reference to the simulation world.
    """
    def __init__(self, file_path: str, world_obj: World):
        self.path = Path(file_path)
        self.world = world_obj

    @classmethod
    def line_to_list(cls, raw_line: str) -> List[Any]:
        """
        Parses a single raw line from the map file into a structured list.

        Splits the line into a header (e.g., 'hub', 'connection'), main data
        (e.g., coordinates, names), and optional metadata enclosed in brackets.
        Ignores lines without a colon or lines containing comments ('#').

        Args:
            raw_line (str): A single line of text from the map file.

        Returns:
            List: A structured list containing the header, a list of main data
                elements, and an optional list of metadata elements. Returns an
                empty list if the line is a comment or lacks a colon.

        Raises:
            SystemExit: If the header is invalid, trailing characters exist
                after metadata, or the string format is malformed.
        """
        res: list[Any] = []
        valid_heads = [
            "nb_drones",
            "start_hub",
            "hub",
            "end_hub",
            "connection"
        ]
        if ":" not in raw_line or "#" in raw_line:
            return res
        try:
            head, body = raw_line.split(":", 1)
            head = head.strip()
            if head not in valid_heads:
                error_exit("FileParser (line_to_list):\n"
                           f"Invalid head '{head.strip()}'.\n"
                           f"Expected one of {valid_heads}")
            res.append(head)

            body = body.strip()
            if "[" in body:
                name_x_y, rest = body.split("[", 1)
                meta, trash = rest.split("]", 1)
                if trash:
                    error_exit("FileParser (line_to_list):\n"
                               "Trailing characters found after metadata "
                               f"'{trash.strip()}'")
                res.append(name_x_y.split())
                res.append(meta.split())
            else:
                res.append(body.split())
        except ValueError as e:
            error_exit(f"FileParser (line_to_list):\n"
                       f"Map format error: {e}")
        return res

    def dispatch(self, line_list: List[Any]) -> None:
        """
        Routes the parsed line data to the appropriate World object
            setup method.

        Based on the extracted header, it triggers the corresponding method
        in the world instance to configure drones, add zones, or create links.

        Args:
            line_list (List): The structured parsed data returned
                by line_to_list.

        Raises:
            SystemExit: If an unknown header is encountered during routing.
        """
        head = line_list[0] if line_list else ""
        main_data = line_list[1] if len(line_list) > 1 else []
        meta_data = line_list[2] if len(line_list) > 2 else []

        match head:
            case "nb_drones":
                self.world.set_drone_quantity(main_data)
            case "start_hub" | "hub" | "end_hub":
                self.world.add_zone_to_map(head, main_data, meta_data)
            case "connection":
                self.world.add_relation_to_map(main_data, meta_data)
            case _:
                error_exit("FileParser (dispatch):\n"
                           f"Unknown head '{head}'")

    def pars_map(self) -> None:
        """
        Executes the full parsing workflow for the designated map file.

        Opens the file, iterates through each line, parses it into a structured
        format, and dispatches the data to build the simulation environment.
        Includes robust error handling for common I/O operations.

        Raises:
            SystemExit: If the file is not found, permissions are denied,
                an encoding error occurs (must be UTF-8), or any other
                unexpected exception arises during the read process.
        """
        try:
            with self.path.open(encoding="utf-8") as file:
                for line in file:
                    data_list: List[Any] = self.line_to_list(line)
                    if data_list:
                        self.dispatch(data_list)
        except FileNotFoundError:
            error_exit(f"FileParser (pars_map):\n"
                       f"The file '{self.path}' was not found.")
        except PermissionError:
            error_exit(f"FileParser (pars_map):\n"
                       f"No permission to read '{self.path}'.")
        except UnicodeDecodeError:
            error_exit(f"FileParser (pars_map):\n"
                       f"Encoding issue. Use UTF-8 for '{self.path}'.")
        except Exception as e:
            error_exit(f"FileParser pars_map):\n"
                       f"Unexpected error during parsing: {e}")
