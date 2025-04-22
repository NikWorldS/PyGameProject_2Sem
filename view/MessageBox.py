import pygame as pg
from settings import WHITE
from collections import deque


class Message:
    def __init__(self):
        self.timer = 0
        self.alpha = 0
        self.fade_speed = 300
        self.visible = False
        self.state = 0
        self.title_font = pg.font.SysFont(None, 30)
        self.text_font = pg.font.SysFont(None, 24)

    def show(self, title, text, duration=2):
        self.state = 1
        self.visible = True
        self.title_surface = self.title_font.render(title, True, WHITE)
        self.text_surface = self.text_font.render(text, True, WHITE)
        self.timer = duration

        title_width, title_height = self.title_surface.get_size()
        text_width, text_height = self.text_surface.get_size()

        self.box_width = max(title_width, text_width) + 20
        self.box_height = title_height + text_height + 20

    def update(self, dt):
        if self.state == 1:
            self.alpha += 2 * self.fade_speed * dt
            if self.alpha >= 255:
                self.alpha = 255
                self.state = 0

        elif self.state == 0:
            self.timer -= dt
            if self.timer <= 0:
                self.state = -1

        elif self.state == -1:
            self.alpha -= self.fade_speed * dt
            if self.alpha <= 0:
                self.alpha = 0
                self.visible = False
                self.state = 0

    def draw_message(self, screen, y_offset):
        if self.visible:
            message_bg = pg.Surface((self.box_width, self.box_height), pg.SRCALPHA)
            message_bg.fill((255, 0, 0, int(self.alpha)))
            message_bg.blit(self.title_surface, (20, 5))
            message_bg.blit(self.text_surface, (5, 10 + self.title_surface.get_height()))

            self.title_surface.set_alpha(self.alpha)
            self.text_surface.set_alpha(self.alpha)

            x = screen.get_width() - self.box_width - 10
            y = screen.get_height() - self.box_height - y_offset
            screen.blit(message_bg, (x, y))

class MessageManager:
    def __init__(self):
        self.queue = deque()
        self.active_messages = []
        self.max_visible = 3

    def add_message(self, title, text, duration = 2):
        self.queue.append((title, text, duration))
        self._try_push_to_active()

    def _try_push_to_active(self):
        while len(self.active_messages) < self.max_visible and self.queue:
            title, text, duration = self.queue.popleft()
            msg = Message()
            msg.show(title, text, duration)
            self.active_messages.append(msg)

    def update(self, dt):
        for msg in self.active_messages[:]:
            msg.update(dt)
            if not msg.visible:
                self.active_messages.remove(msg)
        self._try_push_to_active()

    def draw(self, screen):
        y_offset = 10
        for msg in self.active_messages:
            msg.draw_message(screen, y_offset)
            y_offset += msg.box_height + 10