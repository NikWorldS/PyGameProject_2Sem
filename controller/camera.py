import pygame as pg
from settings import WIDTH, HEIGHT


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.offset = pg.Vector2(0, 0)
        self.map_width = width
        self.map_height = height


    def update(self, target):
        desired_x = -target.centerx + WIDTH // 2
        desired_y = -target.centery + HEIGHT // 2

        self.offset.x += (desired_x - self.offset.x) * 0.03
        self.offset.y += (desired_y - self.offset.y) * 0.03

        self.offset.x = min(0, self.offset.x)
        self.offset.y = min(0, self.offset.y)
        self.offset.x = max(-(self.map_width - WIDTH), self.offset.x)
        self.offset.y = max(-(self.map_height - HEIGHT), self.offset.y)

        self.camera = pg.Rect(self.offset.x, self.offset.y, self.map_width, self.map_height)


    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)