from pygame.sprite import spritecollide, spritecollideany

from settings import WIDTH, HEIGHT, PLAYER_SPEED, GREEN
import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.velocity = pg.Vector2(0, 0)
        self.pos = pg.Vector2(x, y)
        self.rect = pg.Rect(self.pos.x, self.pos.y, 32, 32)
        self.delta_pos = pg.Vector2(0, 0)
        self.image = pg.image.load


    def move(self, velocity):
        self.velocity = velocity
        self.pos.x += self.velocity.x * PLAYER_SPEED * self.game.dt
        self.rect.topleft = self.pos
        self.collide_with_obstacle('x')

        self.pos.y += self.velocity.y * PLAYER_SPEED * self.game.dt
        self.rect.topleft = self.pos
        self.collide_with_obstacle('y')

        self.rect.topleft = self.pos


    def collide_with_obstacle(self, direction):
        hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
        if hits:
            if direction == 'x':
                if self.velocity.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.velocity.x < 0:
                    self.pos.x = hits[0].rect.right
                self.velocity.x = 0
            elif direction == 'y':
                if self.velocity.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.velocity.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.velocity.y = 0

        self.rect.topleft = self.pos