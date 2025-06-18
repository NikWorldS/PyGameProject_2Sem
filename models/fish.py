from pygame import Vector2
import random

vec2 = Vector2

class Fish:
    def __init__(self, species, weight, position, velocity):
        self.species = species  # Исходные данные
        self.weight = weight  # Исходные данные
        self.position = position
        self.velocity = velocity

        self.force = self.__calculate_force()  # сила - зависит от массы и какого-то коэффициента
        self.aggression = self.__get_aggression_by_species()  # додумать
        self.fatigue = 0.0  # додумать
        self.max_fatigue = self.__calculate_max_fatigue()
        self.fatigue_rate = 0.0  # додумать

        self.depth = 0.0
        self.target_depth = 0.0
        self.target_position = vec2(0, 0)
        self.speed = 30

        self.is_hooked = True
        self.state = "aggressive"

    def __calculate_force(self):
        """Возвращает силу рыбы на основе массы с небольшой вариативностью"""
        base_force = self.weight * 0.01
        variation = random.uniform(0.9, 1.1)
        return base_force * variation

    def __get_aggression_by_species(self):
        """Возвращает коэффициент агрессии по виду рыбы"""
        aggression_map = {
            "карп": 0.4,
            "карась": 0.3,
            "плотва": 0.3,
            "линь": 0.5,
        }
        return aggression_map.get(self.species.lower(), 0.5)

    def __calculate_max_fatigue(self):
        """Возвращает предел усталости рыбы"""
        return self.weight * 0.05

    def __get_depth_speed(self):
        """Возвращает скорость движения по вертикали"""
        if self.state == "tired":
            return 0.2
        return 0.5 + self.aggression * 0.5  # агрессивные двигаются быстрее

    def __calculate_fatigue_increase(self, tension):
        """Возвращает увеличение усталости зависит от натяжения лески и агрессии"""
        base_rate = tension * (1 - self.aggression)
        return base_rate

    def __maybe_change_target_depth(self, dt):
        """Периодически меняет цель глубины (если рыба в агрессивном состоянии)"""
        if self.state == "aggressive" and random.random() < 0.01 * dt:
            self.target_depth = random.uniform(0.5, 2.5)

    def __update_position(self, dt):
        """Обновляет позицию рыбы с течением времени"""
        self.position += self.velocity * dt

    def update(self, tension, dt):
        # движение к целевой глубине
        if abs(self.depth - self.target_depth) > 0.1:
            direction = 1 if self.target_depth > self.depth else -1
            self.depth += direction * self.__get_depth_speed() * dt

        # утомление при натяжении
        if self.is_hooked and tension > 0:
            fatigue_increase = self.__calculate_fatigue_increase(tension)
            self.fatigue += fatigue_increase * dt
            self.fatigue = min(self.fatigue, self.max_fatigue)

        # переход в усталое состояние
        if self.fatigue >= self.max_fatigue:
            self.state = "tired"

        # изменение целевой глубины
        self.__maybe_change_target_depth(dt)

