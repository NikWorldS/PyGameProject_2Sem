import pygame as pg

from settings import PIXELS_PER_METER


class Bobber:
    def __init__(self, start_pos, target_pos):
        self.pos = pg.Vector2(start_pos)
        self.target_pos = pg.Vector2(target_pos)
        self.throw_speed = 500
        self.velocity = pg.Vector2(0, 0)

        self.landed_time = None
        self.initial_throw = False
        self.is_landed = False

    def update(self, dt, max_length, rod_tip_pos):
        if not self.initial_throw:
            self.__recalculate_target(max_length, rod_tip_pos)
            direction = self.target_pos - self.pos
            distance = direction.length()

            if distance == 0:
                self.initial_throw = True
                self.is_landed = True
                return

            self.velocity = direction.normalize() * self.throw_speed
            step = self.velocity * dt
            if step.length() >= distance:
                self.pos = self.target_pos
                self.is_landed = True
                self.initial_throw = True
                self.velocity = pg.Vector2(0, 0)
                self.landed_time = pg.time.get_ticks()
            else:
                self.pos += step

        elif self.initial_throw:
            direction = rod_tip_pos - self.pos
            distance = direction.length() / PIXELS_PER_METER

            if distance > max_length:
                pull_target = rod_tip_pos + direction.normalize() * PIXELS_PER_METER
                pull_direction = (pull_target - self.pos).normalize()

                base_speed = self.throw_speed
                coif = 0.85
                #  Квадратичная формула скорости поплавка (от расстояния)
                pull_speed = coif * base_speed + coif * (distance - max_length)**2

                self.velocity = pull_direction * pull_speed
                self.pos += self.velocity * dt
            else:
                self.velocity = pg.Vector2(0, 0)


    def __recalculate_target(self, max_distance, rod_tip_pos):
        max_distance_px = max_distance * PIXELS_PER_METER

        direction = self.target_pos - rod_tip_pos
        distance = direction.length()

        if distance > max_distance_px:
            direction.scale_to_length(max_distance_px)
            self.target_pos = rod_tip_pos + direction

