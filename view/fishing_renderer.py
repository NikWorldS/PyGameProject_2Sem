import pygame as pg

from models.item_rod import ItemRod
from settings import LIGHTGREY


class FishingRenderer:
    def __init__(self, screen, asset_mng):
        self.screen = screen
        self.asset_mng = asset_mng
        self.bobber_image = self.asset_mng.get('fishing_float')

    def draw(self, player, camera_offset, hook_pos, line_points):
        self.draw_fishing_rod(player, camera_offset)
        if hook_pos:
            self.draw_hook(camera_offset, hook_pos)
            self.draw_line(camera_offset, line_points)

    def draw_hook(self, camera_offset, hook_pos):

        rect = self.bobber_image.get_rect(center=(camera_offset + hook_pos))
        self.screen.blit(self.bobber_image, rect.topleft)

    def draw_line(self, camera_offset, line_points):
        if len(line_points) < 2:
            return

        line_width = 2

        points = [(p.x + camera_offset.x, p.y + camera_offset.y) for p in line_points]
        pg.draw.lines(self.screen, LIGHTGREY, False, points, line_width)

    def draw_fishing_rod(self, player, camera_offset):
        active_item = player.inventory.get_active_item()
        if isinstance(active_item, ItemRod):
            rod_logic = active_item.rod_logic

            image = self.asset_mng.get(active_item.held_id)
            rect = image.get_rect()
            rect.bottomleft = player.hand_pos + camera_offset

            rotated_image = pg.transform.rotozoom(image, -rod_logic.current_angle, 1)
            rotated_rect = rotated_image.get_rect(bottomleft=rect.bottomright)

            offset = pg.Vector2(-30, 12)

            rotated_rect.x += offset.x
            rotated_rect.y += offset.y

            self.screen.blit(rotated_image, rotated_rect)
