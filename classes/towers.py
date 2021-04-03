from functions import load_image
import pygame as pg


TOWER_IMAGES = {
    'ArrowTower': load_image('towers/ArrowTower.png')
}


class BaseTower(pg.sprite.Sprite):
    def __init__(self, top_left, width, height, groups=()):
        super(BaseTower, self).__init__(*groups)
        image = TOWER_IMAGES['ArrowTower']
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left


class ArrowTower(BaseTower):
    def __init__(self, top_left, width, height, groups=()):
        super(ArrowTower, self).__init__(top_left, width, height, groups)
        image = TOWER_IMAGES['ArrowTower']
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left

    def clicked(self):
        print('clicked Arrow tower')
