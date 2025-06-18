import pygame as pg
from random import randint

from models.path_finder import PathFinder
from settings import TILESIZE
from utils.map_utils import get_collision_grid


class AStarShowcase:
    def __init__(self):
        self.path_finder = PathFinder()
        self.path = []
        self.goal = []

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                self.goal = (
                    randint(1, 48),
                    randint(1, 48)
                )

    def update(self, tmx_data, player_pos):
        start = (
            int(player_pos[0] // TILESIZE),
            int(player_pos[1] // TILESIZE)
        )

        if start == self.goal:
            self.goal = []
            self.path = []

        if self.goal:
            grid = get_collision_grid(tmx_data, 'Wall')
            self.path = self.path_finder.a_star_search(grid, start, self.goal)

    def get_path(self):
        return self.path