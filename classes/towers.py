from functions import load_image
import pygame as pg


class BaseTower(pg.sprite.Sprite):
    def __init__(self, top_left, width, height, groups=()):
        super(BaseTower, self).__init__(*groups)
        image = load_image('ArrowTower.png')
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left


class ArrowTower(BaseTower):
    def __init__(self, top_left, width, height, groups=()):
        super(ArrowTower, self).__init__(top_left, width, height, groups)
        image = load_image('ArrowTower.png')
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left

    def clicked(self):
        print('clicked Arrow tower')
