import pygame as pg
from os import path
from sys import exit as sys_exit
from controller.camera import Camera
from controller.input_handler import InputHandler
from models.player import Player
from models.wall import Obstacle
from view.map import TiledMap
from settings import *
from view.renderer import Renderer
from view.MessageBox import MessageManager
from view.assetManager import AssetManager


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.assets = AssetManager()

        self.draw_debug = False

    def load_data(self):

        self.game_folder = path.dirname(__file__)
        self.map = TiledMap(self.game_folder + r'\assets\maps\test_2.tmx')
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()

        self.camera = Camera(self.map.width, self.map.height)
        self.input_handler = InputHandler()

        self.msg_manager = MessageManager()

        for tile_object in self.map.tmx_data.objects:
            if tile_object.name == 'player_spawnpoint':
                self.player = Player(self, tile_object.x, tile_object.y)
            elif tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.renderer = Renderer(self.screen, self.player)


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
        self.input_handler.move_handler(self.player)
        self.input_handler.inventory_handler(self.player)
        self.camera.update(self.player)
        self.msg_manager.update(self.dt)
        self.player.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_TAB:
                    self.player.inventory.is_inventory_open = not self.player.inventory.is_inventory_open
                if event.key == pg.K_F2:
                    self.player.inventory._test_add_item()

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        self.renderer.draw_player(self.camera)
        self.renderer.render_inventory()
        self.msg_manager.draw(self.screen)



        if self.draw_debug:
            pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player), 2)
            for sprite in self.all_sprites:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.rect), 1)


        pg.display.flip()


game = Game()
while True:
    game.new()
    game.run()