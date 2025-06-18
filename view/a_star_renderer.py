import pygame as pg

from settings import TILESIZE, RED


class AStarRenderer:
    def __init__(self, screen):
        self.screen = screen

    def draw_path(self, path, camera_offset):
        for tile_x, tile_y in path:
            screen_x = tile_x * TILESIZE + camera_offset.x
            screen_y = tile_y * TILESIZE + camera_offset.y
            rect = pg.Rect(screen_x, screen_y, TILESIZE, TILESIZE)
            pg.draw.rect(self.screen, RED, rect, 2)