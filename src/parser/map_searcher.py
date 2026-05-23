from pathlib import Path
from typing import Dict
from src.parser.map_parser import error_exit


class MapSearcher:
    def __init__(self, base_dir: str = "./maps"):
        self.base_dir = Path(base_dir)

    @staticmethod
    def get_priority(path: Path) -> int:
        parts = [p.lower() for p in path.parts]

        if "easy" in parts:
            return 1
        elif "medium" in parts:
            return 2
        elif "hard" in parts:
            return 3
        else:
            return 4

    def scan_maps(self) -> Dict[str, str]:
        """
        Search all *.txt map files in dirs & sub dirs
        Return Dict shape {'1': 'maps/easy/map1.txt ...'}
        """
        map_dict = {}
        if not self.base_dir.exists() or not self.base_dir.is_dir():
            error_exit(f"Directory Error: Folder '{self.base_dir}' not found.")

        all_files = list(self.base_dir.rglob("*.txt"))
        all_files.sort(key=lambda p: (self.get_priority(p), p.name))

        index = 1
        for file_path in all_files:
            if file_path.is_file():
                map_dict[str(index)] = str(file_path)
                index += 1

        return map_dict
