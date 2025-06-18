class MessageModel:
    def __init__(self, title, text, duration=2):
        self.title = title
        self.text = text
        self.duration = duration
        self.timer = duration
        self.alpha = 0
        self.fade_speed = 300
        self.state = 1  # 1 - появление, 0 - видимый, -1 - растворение
        self.visible = True

    def update(self, dt):
        if self.state == 1:  # появление
            self.alpha += 2 * self.fade_speed * dt
            if self.alpha >= 255:
                self.alpha = 255  # максимальная непрозрачность
                self.state = 0

        elif self.state == 0:  # видимый
            self.timer -= dt
            if self.timer <= 0:
                self.state = -1

        elif self.state == -1:  # растворение
            self.alpha -= self.fade_speed * dt
            if self.alpha <= 0:
                self.alpha = 0
                self.visible = False
                self.state = 0
