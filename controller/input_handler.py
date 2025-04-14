import pygame as pg

from settings import PLAYER_SPEED
vec = pg.Vector2

class InputHandler:
    def __init__(self):
        pass


    def move_handler(self, player, dt):
        keys = pg.key.get_pressed()
        velocity = vec(0, 0)

        if keys[pg.K_w]:
            velocity += vec(0, -1)
        if keys[pg.K_s]:
            velocity += vec(0, 1)
        if keys[pg.K_a]:
            velocity += vec(-1, 0)
        if keys[pg.K_d]:
            velocity += vec(1, 0)

        if velocity.length() != 0:
            velocity = velocity.normalize()

        player.move(velocity)



    def inventory_handler(self):
        pass
