import pygame as pg
from .text import TextLabel


class MenuButton:
    def __init__(self, x: int, y: int, text: str):
        self.width = 200
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

    def draw_button(self, screen, is_selected: bool):
        current_color = self.selection_color if is_selected\
            else self.normal_color
        pg.draw.rect(screen, current_color, self.rect, border_radius=5)
        self.label.draw(screen)
