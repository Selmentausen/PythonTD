import pygame as pg
from functions import load_image


class Button(pg.sprite.Sprite):
    def __init__(self, top_left, width, height, parent_groups=()):
        super(Button, self).__init__(parent_groups)
        self.top_left = top_left
        self.width = width
        self.height = height
        self.image = pg.transform.scale(load_image('button.jpg', colorkey=-1), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left

    def clicked(self):
        print('you clicked this button')
