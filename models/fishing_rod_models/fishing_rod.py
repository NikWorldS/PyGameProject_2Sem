from abc import ABC, abstractmethod
from pygame import Vector3, Vector2


class FishingRod(ABC):
    def __init__(self, name, rod_length, max_line_length, rod_tip_pos):
        self.name = name
        self.rod_length = rod_length
        self.max_line_length = max_line_length
        self.line_length = 0.0

        self.in_hand = False
        self.is_cast = False
        self.is_hooked = False
        self.fish = None

        self.player_force = 0.0
        self.tension = 0.0

        self.raise_progress = 0
        self.rod_tip_pos = rod_tip_pos
        self.hook_pos = Vector2(0, 0)

    def release_fish(self):
        self.is_hooked = False
        self.fish = None

    def reset(self):
        self.is_cast = False
        self.release_fish()
        self.hook_pos = Vector2(0, 0)
        self.line_length = 0

    def get_max_throw_distance(self):
        return self.max_line_length

    @abstractmethod
    def cast(self, position):
        """Закинуть удочку"""
        pass

    @abstractmethod
    def calculate_tension(self):
        """Расчёт натяжения лески"""
        pass

    @abstractmethod
    def update(self):
        pass
