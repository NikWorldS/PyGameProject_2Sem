class Item:
    def __init__(self, name: str, code_name: str, count: int ):
        self.name = name
        self.code_name = code_name
        self.icon_id = f'icon_{code_name}'
        self.held_id = f'held_{code_name}'
        self.count = count