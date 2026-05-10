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
                self.world.drones_quantity = int(line_list[1][0])
            except TypeError as e:
                error_exit(f"Error: {e}")
        elif line_list[0] in ["start_hub", "hub", "end_hub"]:
            try:
                self.world.add_zone_to_map(line_list[1], line_list[2])
            except IndexError as e:
                error_exit(f"Error: {e}")
        elif line_list[0] == "connection":
            # TODO
            self.world.add_relation_to_map()

    def pars_map(self):
        """
        read by line & coll dispatch
        """
        if not self.path.is_file():
            error_exit("Invalid map path!")
        with self.path.open(encoding="utf-8") as file:
            for line in file:
                data_list = self.line_to_list(line)
                if data_list:
                    self.dispatch(data_list)
