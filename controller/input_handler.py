import pygame as pg
vec = pg.Vector2

class InputHandler:
    def __init__(self):
        pass


    def move_handler(self, player):
        keys = pg.key.get_pressed()
        delta_pos = vec(0, 0)

        if keys[pg.K_w]:
            delta_pos += vec(0, -1)
        if keys[pg.K_s]:
            delta_pos += vec(0, 1)
        if keys[pg.K_a]:
            delta_pos += vec(-1, 0)
        if keys[pg.K_d]:
            delta_pos += vec(1, 0)

        if delta_pos.length() != 0:
            delta_pos = delta_pos.normalize()

        player.move(delta_pos)


    def inventory_handler(self, player):
        pass