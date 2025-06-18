import pygame as pg
import pytmx


class TiledMap:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

    def render(self, surface):
        ti = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile,
                                    (x * self.tmx_data.tilewidth,
                                     y * self.tmx_data.tileheight)
                                    )

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface