from pathlib import Path
from .button import MenuButton
from .text import TextLabel


class MenuRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.menu_elements = []

    @staticmethod
    def _pars_path(fali_path: str):
        """
        fali_path = maps/hard/03_ultimate_challenge.txt
        """
        path = Path(fali_path)
        current_level_name = path.stem
        current_level_difficulty = path.parent.name
        return current_level_name, current_level_difficulty

    def build_layout(self, found_maps: dict):
        """
        found_maps = {
        '1' = 'maps/easy/01_linear_path.txt'
        '2' = 'maps/easy/02_simple_fork.txt'
        ...
        }
        """
        cord_y = 50
        cord_x = self.screen.width / 2
        current_category = ""

        for i in found_maps:
            level_name, level_difficulty = self._pars_path(found_maps[i])
            if level_difficulty != current_category:
                current_category = level_difficulty
                title = TextLabel(current_category, 24,
                                  (cord_y, cord_x), "black", True)
                self.menu_elements.append(title)
                cord_y += 60
            buton = MenuButton(cord_x, cord_y, level_name)
            self.menu_elements.append(buton)
            cord_y += 60

    def menu_render(self, menu_index: int):
        ...
