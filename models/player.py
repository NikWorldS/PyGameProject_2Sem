from models.inventory import Inventory
from settings import PLAYER_SPEED
import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.pos = pg.Vector2(x, y)
        self.rect = pg.Rect(self.pos.x, self.pos.y, 32, 32)
        self.delta_pos = pg.Vector2(0, 0)
        self.image = pg.image.load
        self.inventory = Inventory(self.game.assets, push_alert=self.game.msg_manager.add_message)


    def move(self, delta_pos):
        self.delta_pos = delta_pos
        self.pos.x += self.delta_pos.x * PLAYER_SPEED * self.game.dt
        self.rect.topleft = self.pos
        self.collide_with_obstacle('x')

        self.pos.y += self.delta_pos.y * PLAYER_SPEED * self.game.dt
        self.rect.topleft = self.pos
        self.collide_with_obstacle('y')

        self.rect.topleft = self.pos


    def collide_with_obstacle(self, direction):
        hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
        if hits:
            if direction == 'x':
                if self.delta_pos.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.delta_pos.x < 0:
                    self.pos.x = hits[0].rect.right
                self.delta_pos.x = 0
            elif direction == 'y':
                if self.delta_pos.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.delta_pos.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.delta_pos.y = 0

        self.rect.topleft = self.pos


    def update(self):
        pass
    #     self.inventory.update(self.game.screen)