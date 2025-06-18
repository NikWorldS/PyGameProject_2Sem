import pygame as pg

from settings import HEIGHT
from models.item import Item

class Slot:
    def __init__(self, index):
        self.index = index
        self.item = None

        side = 60
        x = 25
        y_offset = 10
        start_y = HEIGHT//2 - 170  # 170 =  ((side + offset) * (capacity - 1) + side)/2
        y = start_y + index * (side + y_offset)

        self.rect = pg.Rect(x, y, side, side)

    def is_empty(self):
        return self.item is None

    def add_item(self, item):
        if self.is_empty():
            self.item = item
            return True
        return False


class Inventory:
    def __init__(self, push_alert = None):
        self.capacity = 5
        self.slots =  [Slot(i) for i in range(self.capacity)]
        self.is_inventory_open = False
        self.push_alert = push_alert
        self.active_slot = None

    def add_item(self, item, slot_index: int = None):
        if all(not slot.is_empty() for slot in self.slots):
            print(f'[INVENTORY] - Инвентарь полон!')
            if self.push_alert:
                self.push_alert('Inventory', 'Инвентарь полон!')
            return

        if slot_index is not None:
            if 0 <= slot_index < self.capacity:
                if self.slots[slot_index].add_item(item):
                    print(f'[INVENTORY] - Добавлен предмет "{item}" в слот "{slot_index}"')
                else:
                    print(f'[INVENTORY] - Слот занят!')
                    if self.push_alert:
                        self.push_alert('Inventory', 'Слот занят!')
                return
            else:
                if self.push_alert:
                    self.push_alert('Inventory', 'Index is out of range!')


        for slot in self.slots:
            if slot.add_item(item):
                print(f'[INVENTORY] - Добавлен предмет "{item}" в слот "{slot.index}"')
                return

    def remove_item(self, slot_index: int):
        if 0 <= slot_index < self.capacity:
            slot = self.slots[slot_index]
            if not slot.is_empty():
                print(f'[INVENTORY] - Удалён предмет "{slot.item}" из слота "{slot_index}"')
                slot.item = None
            elif slot.is_empty():
                print(f'[INVENTORY] - Слот "{slot_index}" пуст')
            else:
                print(f'[INVENTORY] Unknown error with "{slot_index}" index')
        else:
            print('Некорректный индекс слота')

    def set_active_slot(self, index):
        if 0 <= index < self.capacity:
            if self.active_slot == index:
                self.active_slot = None
                print(f'[INVENTORY] - Активный слот {index} снят')
            else:
                self.active_slot = index
                print(f'[INVENTORY] - Выбран активный слот {index}')

    def get_active_item(self):
        if self.active_slot is not None and not self.slots[self.active_slot].is_empty():
            item = self.slots[self.active_slot].item
            return item

    def get_item(self, index):
        if 0 <= index < self.capacity:
            slot = self.slots[index]
            if not slot.is_empty():
                return slot.item
            else:
                return None

    def list_items(self):
        return [slot.item.name if slot.item else None for slot in self.slots]

    def _test_add_item(self):
        self.add_item(Item('картошка', 'poatato', 1))