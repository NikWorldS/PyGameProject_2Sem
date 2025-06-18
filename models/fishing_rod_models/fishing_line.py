import pygame as pg
import math

from settings import PIXELS_PER_METER


class FishingLine:
    def __init__(self, rod_logic, bobber):
        self.rod_logic = rod_logic
        self.bobber = bobber

        self.line_points = []

    def update(self):
        self.calculate_line_points()

    def calculate_line_points(self):
        """Рассчитывает точки сегментов лески"""
        rod_tip_pos = self.rod_logic.rod_tip_pos
        bobber_pos = self.bobber.pos

        direction_vec = bobber_pos - rod_tip_pos
        distance = direction_vec.length()
        max_line_length = self.rod_logic.max_line_length * PIXELS_PER_METER
        max_sag = 30
        segments = 12

        if distance == 0:
            self.line_points = [rod_tip_pos.copy()]
            return

        if distance >= max_line_length:
            self.line_points = [rod_tip_pos.copy(), bobber_pos.copy()]
            return

        slack = max_line_length - distance
        slack_ratio = slack / max_line_length


        sag_amount = max_sag * slack_ratio

        mid_pos = (rod_tip_pos + bobber_pos) * 0.5

        sag_direction = pg.Vector2(0, 1)
        control = mid_pos + sag_direction * sag_amount

        points = []

        # квадратичная кривая Безье
        # B(t) = (1−t)^2 P0 + 2(1−t)t P1 + t^2 P2
        for i in range(segments + 1):
            t = i / segments
            p0 = rod_tip_pos * ((1 - t) ** 2)
            p1 = control * (2 * (1 - t) * t)
            p2 = bobber_pos * (t ** 2)
            point = p0 + p1 + p2
            points.append(point)

        self.line_points = points
        return

    def get_line_points(self):
        """Возвращает лист точек сегментов лески"""
        return self.line_points