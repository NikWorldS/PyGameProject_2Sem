import pygame as pg

from models.item_rod import ItemRod


class PlayerRenderer:
    def __init__(self, screen, player, asset_mng):
        self.screen = screen
        self.player = player
        self.asset_mng = asset_mng
        self.font = pg.font.SysFont(None, 24)

    def draw_player(self, camera):
        player_image = self.asset_mng.get(f'player')
        player_offset_y = -player_image.get_height()/2
        screen_pos = self.player.rect.move(camera.offset.x, camera.offset.y + player_offset_y)

        self.screen.blit(player_image, screen_pos)
        self._draw_held_item(camera.offset)

    def _get_held_item_image(self):
        item = self.player.inventory.get_active_item()
        item_image = self.asset_mng.get(item.held_id)

        if not item_image:
            item_image = self.asset_mng.get('unknown_texture')

        return item_image

    def _draw_held_item(self, camera_offset):
        active_item = self.player.inventory.get_active_item()
        if self.player.inventory.active_slot is not None and active_item:
            handed_item = self._get_held_item_image()

            hand_pos = self.player.hand_pos + camera_offset

            if isinstance(active_item, ItemRod):
                pass
                # fishing_renderer.draw_fishing_rod(active_item.rod_logic, handed_item, hand_pos)
            else:
                self.screen.blit(handed_item, hand_pos)
