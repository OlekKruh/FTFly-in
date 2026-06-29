import pygame as pg
from src.gfx_entities.gfx_text import TextLabel


class MenuButton:
    """
    A graphical button component used in the interactive main menu.

    Handles its own dimensions, color states (normal vs. selected),
    and embeds a centered TextLabel for its display text.
    """
    def __init__(self, x: int, y: int, text: str):
        """
        Initializes the button's layout, colors, and text label.

        Args:
            x (int): The X-coordinate for the top-left corner of the button.
            y (int): The Y-coordinate for the top-left corner of the button.
            text (str): The text to be displayed inside the button.
        """
        self.width = 300
        self.height = 50

        self.rect = pg.Rect(x, y, self.width, self.height)
        self.normal_color = pg.Color("lightgreen")
        self.selection_color = pg.Color("green")

        self.label = TextLabel(
            text=text,
            size=24,
            cord=self.rect.center,
            color="black",
            centered=True
        )

    def draw_button(self, screen: pg.Surface, is_selected: bool) -> None:
        """
        Draws the button rectangle and its internal text on the screen.

        The button's background color changes dynamically depending on whether
        it is currently highlighted in the menu.

        Args:
            screen (pygame.Surface): The Pygame display surface to draw on.
            is_selected (bool): True if the user is currently hovering over
                or highlighting this button, False otherwise.
        """
        current_color = self.selection_color if is_selected\
            else self.normal_color
        pg.draw.rect(screen, current_color, self.rect, border_radius=5)
        self.label.draw(screen)
