import pygame as pg
from main import all_sprites


class Button(pg.sprite.Sprite):
    def __init__(self):
        super(Button, self).__init__(all_sprites)
        pass