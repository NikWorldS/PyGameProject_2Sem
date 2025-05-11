from models.message_model import MessageModel
from view.message_view import MessageView
from collections import deque

class MessageManager:
    def __init__(self):
        self.queue = deque()
        self.active = []
        self.max_visible = 3

    def add_message(self, title, text, duration=2):
        for model, _ in self.active:
            if model.title == title and model.text == text:
                model.timer = duration
                if model.state == -1:
                    model.state = 1
                return

        for i, (t, txt, dur) in enumerate(self.queue):
            if t == title and txt == text:
                self.queue[i] = (t, txt, duration)
                return

        self.queue.append((title, text, duration))
        self._try_push()

    def _try_push(self):
        while len(self.active) < self.max_visible and self.queue:
            title, text, duration = self.queue.popleft()
            model = MessageModel(title, text, duration)
            view = MessageView(model)
            self.active.append((model, view))

    def update(self, dt):
        for model, view in self.active[:]:
            model.update(dt)
            if not model.visible:
                self.active.remove((model, view))
        self._try_push()

    def draw(self, screen):
        y_offset = 10
        for model, view in self.active:
            view.draw(screen, y_offset)
            y_offset += view.box_height + 10
