from sys import exit as sys_exit
from os import path
import pygame as pg

from controller.a_star_showcase import AStarShowcase
from controller.rod_manager import RodManager
from models.message_manager import MessageManager
from models.path_finder import PathFinder
from models.player import Player
from models.wall import Obstacle
from utils.map_utils import get_collision_grid
from view.a_star_renderer import AStarRenderer
from view.fishing_renderer import FishingRenderer
from view.inventory_renderer import InventoryRenderer
from view.player_renderer import PlayerRenderer
from view.asset_manager import AssetManager
from view.map import TiledMap
from controller.inventory_controller import InventoryController
from controller.player_controller import PlayerController
from controller.camera import Camera
from settings import *

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.load_data()
        self.assets = AssetManager()

        self.draw_debug = False

    def load_data(self):
        self.game_folder_path = path.dirname(__file__)
        self.map = TiledMap(self.game_folder_path + r'\assets\maps\test_2.tmx')
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()

    def new(self):
        self.msg_manager = MessageManager()
        self.rod_manager = RodManager()

        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()

        for tile_object in self.map.tmx_data.objects:
            if tile_object.name == 'player_spawnpoint':
                self.player = Player(self, tile_object.x, tile_object.y)
            elif tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        self.player_renderer = PlayerRenderer(self.screen, self.player, self.assets)
        self.inventory_renderer = InventoryRenderer(self.screen, self.player.inventory, self.assets)
        self.fishing_renderer = FishingRenderer(self.screen, self.assets)
        self.a_star_renderer = AStarRenderer(self.screen)

        self.camera = Camera(self.map.width, self.map.height)
        self.a_star_showcase = AStarShowcase()

        self.player_controller = PlayerController()
        self.inventory_controller = InventoryController(self.player.inventory, self.inventory_renderer)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys_exit()

    def update(self):
        self.player_controller.move_handler(self.player)
        self.camera.update(self.player)
        self.msg_manager.update(self.dt)
        self.player.update()
        self.rod_manager.update(self.player, self.dt)
        self.inventory_controller.update()
        self.a_star_showcase.update(self.map.get_tmx_data(), self.player.rect.center)

    def events(self):
        for event in pg.event.get():
            self.inventory_controller.handle_event(event)
            self.rod_manager.handle_event(event, self.player.rect, self.camera)
            self.a_star_showcase.handle_event(event)
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.draw_debug = not self.draw_debug

    def draw(self):
        mouse_pos = pg.mouse.get_pos()

        self.screen.fill(BLACK)
        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        self.inventory_renderer.render_inventory(mouse_pos)
        self.fishing_renderer.draw(self.player, self.camera.offset, self.rod_manager.get_hook_pos(), self.rod_manager.get_line_points())
        self.player_renderer.draw_player(self.camera)
        self.msg_manager.draw(self.screen)

        self.a_star_renderer.draw_path(self.a_star_showcase.get_path(), self.camera.offset)

        if self.draw_debug:
            pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player), 2)
            for sprite in self.all_sprites:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.rect), 1)

        pg.display.flip()



game = Game()
while True:
    game.new()
    game.run()