import pygame as pg
import os
from functions import load_image


class GameObject(pg.sprite.Sprite):
    def __init__(self):
        super(GameObject, self).__init__()
        self.rect = pg.Rect([0, 0, 10, 10])

    def is_clicked(self, pos):
        self.rect.collidepoint(*pos)


class BaseTower(pg.sprite.Sprite):
    def __init__(self, top_left, width, height, group):
        super(BaseTower, self).__init__(group)
        self.rect = pg.Rect(top_left, (width, height))


class ArrowTower(BaseTower):
    def __init__(self, top_left, width, height, group):
        super(ArrowTower, self).__init__(top_left, width, height, group)
        image = load_image('ArrowTower.png')
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left



