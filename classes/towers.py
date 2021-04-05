from functions import load_image
import pygame as pg
from math import hypot

TOWER_IMAGES = {
    'ArrowTower': load_image('towers/ArrowTower.png')
}


class BaseTower(pg.sprite.Sprite):
    def __init__(self, settings, top_left, size, parent_groups=()):
        super(BaseTower, self).__init__(*parent_groups)
        self.image = pg.transform.scale(TOWER_IMAGES['ArrowTower'], size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left
        self.settings = settings

        self.x, self.y = top_left
        self.tower_range = 0

    def clicked(self):
        print('clicked A Tower')


class ArrowTower(BaseTower):
    def __init__(self, settings, top_left, size, parent_groups=()):
        super(ArrowTower, self).__init__(settings, top_left, size, parent_groups)
        image = TOWER_IMAGES['ArrowTower']
        self.image = pg.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left

        self.range = settings.arrow_tower_range
        self.damage = settings.arrow_tower_damage

    def update(self, *args, **kwargs) -> None:
        self.get_objects_in_range(args[0])

    def get_objects_in_range(self, group):
        for obj in group:
            distance = abs(hypot(self.x, self.y) - hypot(obj.x, obj.y))
            if distance <= self.range:
                print(f'hit enemy {obj.__class__.__name__}')

    def clicked(self):
        print('clicked Arrow tower')
