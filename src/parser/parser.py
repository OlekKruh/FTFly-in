from pathlib import Path
from typing import List
from src.utils_func.exit_func import error_exit


class FileParser:
    def __init__(self, file_path: str, world_obj):
        self.path = Path(file_path)
        self.world = world_obj

    def line_to_list(self, raw_line):
        res = []
        valid_heads = [
            "nb_drones",
            "start_hub",
            "hub",
            "end_hub",
            "connection"
        ]
        if "#" in raw_line:
            return res
        if ":" not in raw_line:
            return res
        head, body = raw_line.split(":", 1)
        head = head.strip()
        if head not in valid_heads:
            error_exit("Invalid line head!\n"
                       "Line mast start flom one in list "
                       f"{valid_heads}")
        res.append(head)

        body = body.strip()
        if "[" in body:
            name_x_y, rest = body.split("[")
            res.append(name_x_y.split())

            meta, trash = rest.split("]")
            if trash:
                error_exit("Wrong line format in map description")
            res.append(meta.split())
        else:
            res.append(body.split())

        return res

    def dispatch(self, line_list: List):
        if line_list[0] == "nb_drones":
            try:
                if len(line_list[1]) != 1:
                    error_exit(f"Error: 'nb_drones' expects 1 value, "
                               f"got {len(line_list[1])}")
                self.world.drones_quantity = int(line_list[1][0])
            except (ValueError, IndexError, TypeError) as e:
                error_exit(f"Error: {e}")

        elif line_list[0] in ["start_hub", "hub", "end_hub"]:
            try:
                main_param = line_list[1]
                if len(main_param) != 3:
                    error_exit(f"Error: {line_list[0]} expects [name, x, y],"
                               f" got {main_param}")
                hub_name, hub_x, hub_y = (
                    line_list[1][0],
                    int(line_list[1][1]),
                    int(line_list[1][2])
                )
                self.world.add_zone_to_map(
                    [hub_name, hub_x, hub_y],
                    line_list[2] # выпадаем за список нужно условие
                )
            except (ValueError, IndexError) as e:
                error_exit(f"Error: Invalid main parameters format "
                           f"or missing values. {e}")

        elif line_list[0] == "connection":
            try:
                connection = line_list[1]
                meta_data = line_list[2] # выпадаем за список нужно условие
                if len(connection) != 1:
                    error_exit("Invalid value. "
                               "Onli one connection must be in line "
                               f"got {connection}")
                self.world.add_relation_to_map(connection[0], meta_data[0])
            except (ValueError, IndexError) as e:
                error_exit(f"Error: Invalid connection parameters format "
                           f"or missing values. {e}")


    def pars_map(self):
        """
        read by line & coll dispatch
        """
        try:
            with self.path.open(encoding="utf-8") as file:
                for line in file:
                    data_list = self.line_to_list(line)
                    if data_list:
                        self.dispatch(data_list)
        except FileNotFoundError:
            error_exit(f"Error: The file '{self.path}' was not found.")
        except PermissionError:
            error_exit(f"Error: No permission to read '{self.path}'.")
        except UnicodeDecodeError:
            error_exit(f"Error: Encoding issue. Use UTF-8 for '{self.path}'.")
        except Exception as e:
            error_exit(f"Unexpected error during parsing: {e}")
