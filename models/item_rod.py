from models.item import Item

class ItemRod(Item):
    def __init__(self, name, code_name, rod_logic, controller_class):
        super().__init__(name, code_name, 1)
        self.rod_logic = rod_logic
        self.controller_class = controller_class
