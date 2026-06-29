from pathlib import Path
from typing import Any

import pygame as pg
from src.gfx_entities.gfx_button import MenuButton
from src.gfx_entities.gfx_text import TextLabel


class MenuRenderer:
    """
    Handles the dynamic construction and rendering of the main menu UI.

    Parses map file paths to categorize levels by difficulty, generates
    text headers for each category, and creates interactive buttons for
    level selection, placing them dynamically based on screen resolution.
    """
    def __init__(self, screen: pg.Screen):
        self.screen = screen
        self.menu_titles: list[Any] = []
        self.menu_buttons: list[Any] = []

    @staticmethod
    def _pars_path(fali_path: str) -> tuple[str, str]:
        """
        Extracts the level name and difficulty category from a file path.

        Args:
            fali_path (str): The string representation of the file path.

        Returns:
            tuple[str, str]: A tuple containing the level name
                (without extension) and the directory name
                representing the difficulty.
        """
        path = Path(fali_path)
        current_level_name = path.stem
        current_level_difficulty = path.parent.name
        return current_level_name, current_level_difficulty

    def build_layout(self, found_maps: dict[Any, Any]) -> None:
        """
        Constructs the graphical layout of titles and buttons.

        Iterates through the discovered maps, grouping them by difficulty.
        Calculates vertical spacing and font sizes dynamically using
        percentages of the current screen height to ensure responsive
        UI scaling.

        Args:
            found_maps (dict): A dictionary mapping string indices
                to file paths.
        """
        scr_w = self.screen.get_width()
        scr_h = self.screen.get_height()
        cord_y = scr_h * 0.00
        button_width = 300
        cord_x = (scr_w // 2) - (button_width // 2)
        current_category = ""

        for i in found_maps:
            level_name, level_difficulty = self._pars_path(found_maps[i])
            if level_difficulty != current_category:
                cord_y += scr_h * 0.03  # padding before title text
                current_category = level_difficulty
                title_font_size = int(scr_h * 0.04)
                title = TextLabel(current_category.upper(), title_font_size,
                                  (scr_w // 2, cord_y), "white", True)
                self.menu_titles.append(title)
                cord_y += scr_h * 0.02  # padding after title text
            buton = MenuButton(cord_x, cord_y, level_name)
            self.menu_buttons.append(buton)
            cord_y += scr_h * 0.08  # padding after button text

    def menu_render(self, menu_index: int) -> None:
        """
        Draws the menu background, difficulty titles, and level buttons.

        Args:
            menu_index (int): The index of the currently highlighted button,
                used to trigger the selection visual state.
        """
        self.screen.fill((30, 30, 30))

        for label in self.menu_titles:
            label.draw(self.screen)

        for index, button in enumerate(self.menu_buttons):
            is_selected = (index == menu_index)
            button.draw_button(self.screen, is_selected)
