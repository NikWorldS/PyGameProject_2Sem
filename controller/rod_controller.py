from abc import ABC, abstractmethod
import pygame as pg

class RodController(ABC):
    def __init__(self, rod_logic):
        self.rod_logic = rod_logic
        self.charge_power = 0
        self.charge_start_time = 0
        self.is_charging = False
        self.power_limit = 1
        self.max_power = 1250  # in ms

    @abstractmethod
    def cast_rod(self, final_power, player_rect, camera):
        ...

    @abstractmethod
    def uncast_rod(self):
        ...

    def handle_event(self, event, player_rect, camera):
        if not self.rod_logic.is_cast:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.is_charging = True
                self.rod_logic.start_throwing()
                self.charge_start_time = pg.time.get_ticks()

            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.is_charging:
                self.is_charging = False
                final_power = min(self.charge_power, self.power_limit)
                self.cast_rod(final_power, player_rect, camera)
                self.charge_power = 0
        else:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.rod_logic.start_reeling()
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.rod_logic.stop_reeling()
                

    def get_direction_vector(self, player_rect, camera):
        mouse_pos = pg.mouse.get_pos()

        scr_player_pos = player_rect.move(camera.offset.x, camera.offset.y).center
        direction_vector = pg.Vector2(mouse_pos) - pg.Vector2(scr_player_pos)

        if direction_vector.length() != 0:
            direction_vector = direction_vector.normalize()

        return direction_vector

    def update(self):
        if self.is_charging:
            now = pg.time.get_ticks()
            elapsed = now - self.charge_start_time

            self.charge_power = min(elapsed / self.max_power, self.power_limit)
            self.rod_logic.charge = self.charge_power
