import pygame as pg

from controller.rod_controller import RodController
from models.fishing_models.fishing_line import FishingLine
from settings import PIXELS_PER_METER
from models.fishing_models.bobber import Bobber

class FloatRodController(RodController):
    def __init__(self, rod_logic):
        super().__init__(rod_logic)
        self.bobber = None
        self.line = None

    def update(self, dt, player_pos):
        super().update()


        if self.bobber:
            self.bobber.update(dt,
                               self.rod_logic.get_max_throw_distance(),
                               self.rod_logic.rod_tip_pos,
                               )
            self.line.update(self.rod_logic.rod_tip_pos)
            self.rod_logic.hook_pos = self.bobber.pos

        self.rod_logic.update(dt, player_pos)


    def cast_rod(self, power, player_rect, camera):
        if not self.rod_logic.is_cast:
            dir_vec = self.get_direction_vector(player_rect, camera)

            bobber_pos = self.calculate_bobber_pos(power, dir_vec)

            self.rod_logic.cast(bobber_pos)
            self.bobber = Bobber(self.rod_logic.rod_tip_pos, bobber_pos)
            self.line = FishingLine(self.rod_logic, self.bobber)
            print(f"[FLOAT ROD] - Заброс с силой: {power:.2f}")
        if self.rod_logic.is_cast:
            pass

    def uncast_rod(self):
        self.rod_logic.test_uncast()
        self.bobber = None
        self.rod_logic.charge = 0

    def calculate_bobber_pos(self, power, direction_vector):
        max_throw_distance = self.rod_logic.get_max_throw_distance()
        throw_distance = power * max_throw_distance * PIXELS_PER_METER
        throw_vector = direction_vector * throw_distance
        start_pos = pg.Vector2(self.rod_logic.rod_tip_pos)
        final_pos = start_pos + throw_vector
        return final_pos

