from pathlib import Path
from typing import Dict

from src.utils_func.exit_func import error_exit


class MapSearcher:
    """
    Scans and catalogues available map files from a specified directory.

    Used to dynamically generate the map selection menu. It searches for
    .txt files within the base directory and its subdirectories, assigning
    a sorting priority based on difficulty levels found in the folder names.

    Attributes:
        base_dir (Path): The root directory to search for map files.
            Defaults to './maps'.
    """
    def __init__(self, base_dir: str = "./maps"):
        self.base_dir = Path(base_dir)

    @staticmethod
    def get_priority(path: Path) -> int:
        """
        Determines the sorting priority of a map file based on its
            directory path.

        Evaluates the path components to identify difficulty keywords ('easy',
        'medium', 'hard') and assigns a corresponding integer weight. Lower
        numbers indicate higher priority (appear first in the menu).

        Args:
            path (Path): The pathlib.Path object representing the
                map's file path.

        Returns:
            int: The priority level (1 for easy, 2 for medium, 3 for hard,
                4 for anything else).
        """
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
        Recursively searches for map files and builds a numbered
            menu dictionary.

        Scans the base directory for all '.txt' files, sorts them primarily by
        their assigned difficulty priority and secondarily by file name, and
        maps them to string-based numerical indices (e.g., '1', '2', '3').

        Returns:
            Dict[str, str]: A dictionary where keys are stringified
                numeric indices and values are the string paths to
                the corresponding map files.

        Raises:
            SystemExit: If the base directory does not exist or
                is not a folder.
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
