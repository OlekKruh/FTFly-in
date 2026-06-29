import pygame as pg


class TextLabel:
    """
    A helper class for rendering text on a Pygame surface.

    Encapsulates font creation, text rendering, and positioning logic.
    Supports standard top-left positioning as well as center alignment.
    """
    def __init__(self, text: str, size: int, cord: tuple[int, int],
                 color: str = "white", centered: bool = False):
        """
        Initializes the text surface and calculates its bounding rectangle.

        Args:
            text (str): The string of text to display.
            size (int): The font size.
            cord (tuple[int, int]): The (x, y) coordinates for
                positioning the text.
            color (str, optional): The color of the text. Defaults to "white".
            centered (bool, optional): If True, positions the
                text using its center coordinate instead of the top-left
                corner.Defaults to False.
        """
        font = pg.font.SysFont(None, size)
        self.text_surf = font.render(text, True, pg.Color(color))

        if centered:
            self.text_rect = self.text_surf.get_rect(center=cord)
        else:
            self.text_rect = self.text_surf.get_rect(topleft=cord)

    def draw(self, screen: pg.Surfac) -> None:
        """
        Blits the rendered text surface onto the target screen.

        Args:
            screen (pygame.Surface): The Pygame display surface to draw on.
        """
        screen.blit(self.text_surf, self.text_rect)
