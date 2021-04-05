from functions import load_image
import pygame as pg
from math import hypot
from .enemies import EnemyBase

TOWER_IMAGES = {
    'ArrowTower': load_image('towers/ArrowTower.png')
}

BULLET_IMAGES = {
    'normal_bullet': load_image('towers/normal_bullet.png'),
    'big_bullet': load_image('towers/big_bullet.png')
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
        self.damage = 0
        self.hit_order = 'first'

    def update(self, enemies) -> None:
        self.hit_objects_in_range(enemies)

    def hit_objects_in_range(self, group: pg.sprite.Group):
        if group:
            if self.hit_order == 'first':
                enemy = group.sprites()[0]
            elif self.hit_order == 'last':
                enemy = group.sprites()[-1]
            else:
                enemy = min(group, key=lambda obj: abs(hypot(self.x, self.y) - hypot(obj.x, obj.y)))
            enemy.hit(self.damage)

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

    def clicked(self):
        print('clicked Arrow tower')
