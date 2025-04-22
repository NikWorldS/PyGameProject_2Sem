import pygame as pg

from settings import WHITE, HEIGHT, GRAY, DARKGREY


class Renderer:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.player_image = pg.Surface((self.player.rect.width, self.player.rect.height))
        self.player_image.fill((0, 255, 0))
        self.font = pg.font.SysFont(None, 24)

    def draw_player(self, camera):
        screen_pos = self.player.rect.move(camera.offset.x, camera.offset.y)
        self.screen.blit(self.player_image, screen_pos)


    def render_inventory(self):
        if self.player.inventory.is_inventory_open:
            self.__draw_inventory()
            self.__draw_hovered_item_label()

    def __draw_inventory(self):
        for i, slot in enumerate(self.player.inventory.slots):
            x = 15 + 10
            y = HEIGHT/2 - 180 + 10 + i * 70
            self.screen.blit(self.player.inventory.slots[0].image, (x, y))
            text = self.font.render('1' if slot.item else '', True, WHITE)
            self.screen.blit(text, (x + 5, y + 15))


    def __draw_hovered_item_label(self):
        mouse_pos = pg.mouse.get_pos()
        hovered_slot = None
        for slot in self.player.inventory.slots:
            if slot.rect.collidepoint(mouse_pos):
                hovered_slot = slot
                item_label = hovered_slot.item
                if item_label is not None:
                    self.__render_text(item_label, mouse_pos)

    def __render_text(self, text, mouse_pos):
        label = self.font.render(text, True, WHITE)
        label_width, label_height = label.get_size()
        label_bg = pg.Surface((label_width+5, label_height+5))
        label_bg.fill(DARKGREY)
        label_bg.blit(label, (2, 2))
        self.screen.blit(label_bg, (mouse_pos[0] + 15, mouse_pos[1] - 2))
