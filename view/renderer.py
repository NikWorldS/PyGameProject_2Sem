import pygame as pg

from models.player import Player
from settings import WIDTH, HEIGHT


class Renderer:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.player_image = pg.Surface((self.player.rect.width, self.player.rect.height))
        self.player_image.fill((0, 255, 0))


    def draw_player(self, camera):
        screen_pos = self.player.rect.move(camera.offset.x, camera.offset.y)
        self.screen.blit(self.player_image, screen_pos)

    def draw_map(self):
        pass

    def draw_inventory(self):
        pass