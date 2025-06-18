import pygame as pg

from models.item_rod import ItemRod


class InventoryController:
    def __init__(self, inventory, renderer):
        self.inventory = inventory
        self.renderer = renderer
        self.rod_casted = False

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DELETE:
                mouse_pos = pg.mouse.get_pos()
                hovered_index = self.renderer.get_hovered_slot(mouse_pos)
                if hovered_index is not None:
                    self.inventory.remove_item(hovered_index.index)

            if pg.K_1 <= event.key <= pg.K_5:
                slot_index = event.key - pg.K_1
                if self.rod_casted:
                    self.inventory.push_alert('Fishing', 'Удочка уже закинута!')
                    return
                else:
                    self.inventory.set_active_slot(slot_index)

    def update(self):
        active_item = self.inventory.get_active_item()
        if isinstance(active_item, ItemRod):
            if active_item.rod_logic.is_cast:
                self.rod_casted = True
            else:
                self.rod_casted = False
        else:
            self.rod_casted = False
