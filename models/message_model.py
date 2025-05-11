class MessageModel:
    def __init__(self, title, text, duration=2):
        self.title = title
        self.text = text
        self.duration = duration
        self.timer = duration
        self.alpha = 0
        self.fade_speed = 300
        self.state = 1  # 1 - fade in, 0 - display, -1 - fade out
        self.visible = True

    def update(self, dt):
        if self.state == 1:  # fade in
            self.alpha += 2 * self.fade_speed * dt
            if self.alpha >= 255:
                self.alpha = 255
                self.state = 0

        elif self.state == 0:  # visible
            self.timer -= dt
            if self.timer <= 0:
                self.state = -1

        elif self.state == -1:  # fade out
            self.alpha -= self.fade_speed * dt
            if self.alpha <= 0:
                self.alpha = 0
                self.visible = False
                self.state = 0
