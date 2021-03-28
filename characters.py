import pygame as pg
import os


class GameObject(pg.sprite.Sprite):
    def __init__(self):
        super(GameObject, self).__init__()
        self.rect = pg.Rect([0, 0, 10, 10])

    def is_clicked(self, pos):
        self.rect.collidepoint(*pos)


class BaseTower(pg.sprite.Sprite):
    def __init__(self, top_left, width, height):
        super(BaseTower, self).__init__()
        self.rect = pg.Rect(top_left, (width, height))



