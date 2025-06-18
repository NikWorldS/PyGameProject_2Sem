import pygame as pg

from settings import WHITE, HEIGHT, GRAY, DARKGREY


class InventoryRenderer:
    def __init__(self, screen, inventory, asset_mng):
        self.screen = screen
        self.inventory = inventory
        self.asset_mng = asset_mng

        self.font = pg.font.SysFont(None, 24)

    def render_inventory(self, mouse_pos):
        if self.inventory.is_inventory_open:
            self.__draw_inventory()
            self.__draw_hovered_item_label(mouse_pos)

    def __draw_inventory(self):
        """Рисует инвентарь (слоты)"""
        inv_capacity = self.inventory.capacity
        slot_side = 60
        slot_offset = 10
        inv_height = ((slot_side + slot_offset) * (inv_capacity - 1) + slot_side)
        y_start = HEIGHT/2 - inv_height/2

        for i, slot in enumerate(self.inventory.slots):
            x = 25
            y = y_start + i * (slot_side + slot_offset)

            if i == self.inventory.active_slot:
                slot_image = self.asset_mng.get('active_slot')
            else:
                slot_image = self.asset_mng.get('slot')

            self.screen.blit(slot_image, (x, y))

            item_in_slot = self.__get_item_image(slot)
            if item_in_slot:
                image = item_in_slot
                image_offset = 15
                self.screen.blit(image, (x + image_offset, y + image_offset))

    def __draw_hovered_item_label(self, mouse_pos):
        """Рисует название предмета при наведении на него"""
        current_slot = self.get_hovered_slot(mouse_pos)
        if current_slot and not current_slot.is_empty():
            self.__render_text(str(current_slot.item.name), mouse_pos)

    def __render_text(self, text, mouse_pos):
        """Готовит и рисует подпись предмета"""
        bg_offset = pg.Vector2(5, 5)
        label_offset = pg.Vector2(2, 2)
        mouse_offset = pg.Vector2(15, -2)

        label = self.font.render(text, True, WHITE)
        label_width, label_height = label.get_size()
        label_bg = pg.Surface((label_width + bg_offset.x, label_height + bg_offset.y))
        label_bg.fill(DARKGREY)
        label_bg.blit(label, (label_offset))
        self.screen.blit(label_bg, (mouse_pos[0] + mouse_offset.x, mouse_pos[1] + mouse_offset.y))

    def get_hovered_slot(self, mouse_pos):
        """Возвращает слот при наведении на него"""
        for slot in self.inventory.slots:
            if slot.rect.collidepoint(mouse_pos):
                hovered_slot = slot
                return hovered_slot

        return None

    def __get_item_image(self, slot):
        """Возвращает иконку предмета"""
        if not slot.is_empty():
            item_in_slot = self.asset_mng.get(slot.item.icon_id)
            return item_in_slot

