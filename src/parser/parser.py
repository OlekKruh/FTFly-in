from pathlib import Path
from typing import List
from src.utils_func.exit_func import error_exit


class FileParser:
    def __init__(self, file_path: str, world_obj):
        self.path = Path(file_path)
        self.world = world_obj


    def line_to_list(self, raw_line: str) -> List:
        res = []
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
                error_exit("Line_to_list func Error\n"
                           f"Invalid head '{head.strip()}'.\n"
                           f"Expected one of {valid_heads}")
            res.append(head)

            body = body.strip()
            if "[" in body:
                name_x_y, rest = body.split("[", 1)
                meta, trash = rest.split("]", 1)
                if trash:
                    error_exit("Line_to_list func Error\n"
                               "Trailing characters found after metadata "
                               f"'{trash.strip()}'")
                res.append(name_x_y.split())
                res.append(meta.split())
            else:
                res.append(body.split())
        except ValueError as e:
            error_exit(f"Line_to_list func Error\n"
                       f"Map format error: {e}")
        return res

    def dispatch(self, line_list: List):
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
                error_exit("Dispatch func Error.\n"
                           f"Unknown head '{head}'")

    def pars_map(self):
        """
        read by line & coll dispatch
        """
        try:
            with self.path.open(encoding="utf-8") as file:
                for line in file:
                    data_list: List = self.line_to_list(line)
                    if data_list:
                        self.dispatch(data_list)
        except FileNotFoundError:
            error_exit(f"Pars_map func Error:\n"
                       f"The file '{self.path}' was not found.")
        except PermissionError:
            error_exit(f"Pars_map func Error:\n"
                       f"No permission to read '{self.path}'.")
        except UnicodeDecodeError:
            error_exit(f"Pars_map func Error:\n"
                       f"Encoding issue. Use UTF-8 for '{self.path}'.")
        except Exception as e:
            error_exit(f"Pars_map func Error:\n"
                       f"Unexpected error during parsing: {e}")
