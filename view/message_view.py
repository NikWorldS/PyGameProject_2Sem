import pygame as pg

from settings import WHITE

class MessageView:
    def __init__(self, message_model):
        self.model = message_model
        self.title_font = pg.font.SysFont(None, 30)
        self.text_font = pg.font.SysFont(None, 24)

        self.title_surface = self.title_font.render(self.model.title, True, WHITE)
        self.text_surface = self.text_font.render(self.model.text, True, WHITE)

        title_w, title_h = self.title_surface.get_size()
        text_w, text_h = self.text_surface.get_size()

        box_offset = 20

        self.box_width = max(title_w, text_w) + box_offset
        self.box_height = title_h + text_h + box_offset

    def draw(self, screen, y_offset):
        alpha = int(self.model.alpha)
        self.title_surface.set_alpha(alpha)
        self.text_surface.set_alpha(alpha)

        message_bg = pg.Surface((self.box_width, self.box_height), pg.SRCALPHA)
        message_bg.fill((255, 0, 0, alpha))

        title_dest = pg.Vector2(20, 5)
        text_dest = pg.Vector2(5, 10)
        message_bg.blit(self.title_surface, title_dest)
        message_bg.blit(self.text_surface, (text_dest.x, text_dest.y + self.title_surface.get_height()))

        x_offset = -10
        x = screen.get_width() - self.box_width + x_offset
        y = screen.get_height() - self.box_height - y_offset
        screen.blit(message_bg, (x, y))
