import pygame as pg


class TextLabel:
    def __init__(self, text: str, size: int, cord: tuple[int, int],
                 color: str = "white", centered: bool = False):
        font = pg.font.SysFont(None, size)
        self.text_surf = font.render(text, True, pg.Color(color))

        if centered:
            self.text_rect = self.text_surf.get_rect(center=cord)
        else:
            self.text_rect = self.text_surf.get_rect(topleft=cord)

    def draw(self, screen):
        screen.blit(self.text_surf, self.text_rect)
