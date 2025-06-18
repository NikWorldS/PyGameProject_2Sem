from models.item_rod import ItemRod


class RodManager:
    def __init__(self):
        self.current_rod_controller = None

    def update(self, player, dt):
        item = player.inventory.get_active_item()
        if isinstance(item, ItemRod):
            item.rod_logic.calculate_tip_pos(player.hand_pos)
            if self.current_rod_controller is None or self.current_rod_controller.rod_logic != item.rod_logic:
                self.current_rod_controller = item.controller_class(item.rod_logic)

                item.rod_logic.in_hand = True

                self.current_rod_controller.update(dt, player.rect.center)
            elif self.current_rod_controller.rod_logic.is_cast:
                pass

        else:
            self.current_rod_controller = None

        if self.current_rod_controller:
            self.current_rod_controller.update(dt, player.rect.center)

    def handle_event(self, event, player_rect, camera):
        if self.current_rod_controller:
            self.current_rod_controller.handle_event(event, player_rect, camera)

    def get_hook_pos(self):
        if self.current_rod_controller and self.current_rod_controller.rod_logic.is_cast:
            return self.current_rod_controller.bobber.pos

    def get_line_points(self):
        if self.current_rod_controller and self.current_rod_controller.rod_logic.is_cast:
            return self.current_rod_controller.line.get_line_points()
