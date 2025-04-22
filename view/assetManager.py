import os.path
import pygame as pg

class AssetManager:
    def __init__(self):
        self.textures = {}
        self.load_assets()

    def load_image(self, path, alpha=True):
        image = pg.image.load(path)
        return image.convert_alpha() if alpha else image.convert()

    def load_assets(self):
        base_path = r'.\assets\textures'

        self.textures['slot'] = self.load_image(os.path.join(base_path, 'inventory', 'inventorySlot.png'))

    def get(self, name):
        return self.textures.get(name)