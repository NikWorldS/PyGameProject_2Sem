import math
import pygame as pg

from settings import PIXELS_PER_METER
from models.fishing_rod_models.fishing_rod import FishingRod


class FloatRod(FishingRod):
    def __init__(self, name, rod_length, max_line_length, rod_tip_pos):
        super().__init__(name, rod_length, max_line_length, rod_tip_pos)
        self.charge = 0
        self.current_angle = 0
        self.target_angle = 0
        self.upper_angle = 0
        self.max_angle = 70
        self.angle_speed = 120

        self.rod_strength = 0.8
        self.in_reeling = False
        self.in_throwing = False

        self.is_landing = False
        self.landing_progress = 0.0
        self.landing_speed = 0.01

    def cast(self, position):
        self.is_cast = True
        self.in_throwing = False
        self.hook_pos = position

    def calculate_tension(self):
        pass

    def start_throwing(self):
        self.in_throwing = True

    def start_reeling(self):
        self.in_reeling = True

    def stop_reeling(self):
        self.in_reeling = False

    def update(self, dt, player_pos, fish_strength = 0):
        speed_coif = 1
        landing_angle = 1

        if self.in_throwing:
            self.target_angle = self.max_angle

        elif self.is_cast:
            if self.in_reeling:
                diff = fish_strength - self.rod_strength
                speed_coif = min(1, max(abs(diff), 0.1))
                self.target_angle = 0


                if self.current_angle < landing_angle:
                    self.is_landing = True
                else:
                    self.is_landing = False


            if not self.in_reeling:
                self.target_angle = self.max_angle

        else:
            self.target_angle = 0

        if self.is_landing:
            lifting_distance = 32
            if self.hook_pos.distance_to(player_pos) < lifting_distance:
                self.test_uncast()

        current_angle_speed = self.angle_speed * speed_coif

        if self.current_angle < self.target_angle:
            self.current_angle = min(self.target_angle, self.current_angle + current_angle_speed * dt)
        elif self.current_angle > self.target_angle:
            self.current_angle = max(self.target_angle, self.current_angle - current_angle_speed * dt)

    def test_uncast(self):
        self.is_cast = False
        self.hook_pos = None
        self.is_landing = False
        self.is_hooked = False
        self.in_reeling = False
        self.landing_progress = 0
        print('rod is uncasted')

    def finish_landing(self):
        print('yay')
        self.test_uncast()

    def calculate_tip_pos(self, hand_pos: pg.Vector2):
        start_angle = -90  #  направлен вверх (pi/2)
        angle_radians = math.radians(start_angle + self.current_angle)
        dx = math.cos(angle_radians) * self.rod_length * PIXELS_PER_METER
        dy = math.sin(angle_radians) * self.rod_length * PIXELS_PER_METER
        self.rod_tip_pos = pg.Vector2(hand_pos.x + dx, hand_pos.y + dy)