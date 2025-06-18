from pydoc import plain

import pygame as pg
import os.path

class AssetManager:
    def __init__(self):
        self.textures = {}
        self.load_assets()

    def load_image(self, path, alpha=True):
        image = pg.image.load(path)
        return image.convert_alpha() if alpha else image.convert()

    def load_assets(self):
        base_path = r'.\assets\textures'
        self.textures['unknown_texture'] = self.load_image(os.path.join(base_path, 'UnknownTexture.png'))

        # gui textures
        self.textures['slot'] = self.load_image(os.path.join(base_path, 'gui', 'InventorySlot.png'))
        self.textures['active_slot'] = self.load_image(os.path.join(base_path, 'gui', 'ActiveInventorySlot.png'))

        #item's icon textures
        self.textures['icon_fishing_rod'] = self.load_image(os.path.join(base_path, 'item', 'icon', 'FishingRod.png'))

        #item's held textures
        self.textures['held_fishing_rod'] = self.load_image(os.path.join(base_path, 'item', 'held', 'test_rod.png'))

        #player's textures
        self.textures['player'] = self.load_image(os.path.join(base_path, 'player', 'right.png'))


        #some fishing things
        self.textures['fishing_float'] = self.load_image(os.path.join(base_path, 'item', 'held', 'bobber.png'))

    def get(self, name):
        if name not in self.textures:
            image = self.textures.get('unknown_texture')
        else:
            image = self.textures.get(name)
        return image