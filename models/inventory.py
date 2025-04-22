import pygame as pg

from settings import HEIGHT


class Slot:
    def __init__(self, index, asset_mng):
        self.index = index
        self.item = None
        self.image = asset_mng.get('slot')

        side = 60
        x = 25
        start_y = HEIGHT//2 - 170
        y = start_y + index * (side + 10)

        self.rect = self.image.get_rect(topleft=(x, y))

    def is_empty(self):
        return self.item is None

    def add_item(self, item):
        if self.is_empty():
            self.item = item
            return True
        return False


class Inventory:
    def __init__(self, asset_mng, push_alert = None):
        self.capacity = 5
        self.slots =  [Slot(i, asset_mng) for i in range(self.capacity)]
        self.is_inventory_open = False
        self.push_alert = push_alert

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
            item = self.slots[slot_index]
            if item:
                self.slots.item = None
                print(f'[INVENTORY] - Удалён предмет "{item}" из слота "{slot_index}"')
            else:
                print(f'[INVENTORY] - Слот "{slot_index}" пуст')
        else:
            print('Некорректный индекс слота')

    def list_items(self):
        return [slot.item for slot in self.slots]


    def _test_add_item(self):
        self.add_item('картошка')