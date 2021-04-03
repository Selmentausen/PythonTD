import pygame as pg
from functions import load_image


ENEMY_IMAGES = {
    'square_enemy': load_image('enemies/enemy_square.png'),
    'triangle_enemy': load_image('enemies/enemy_triangle.png'),
    'rhombus_enemy': load_image('enemies/enemy_triangle.png')
}


class EnemyBase(pg.sprite.Sprite):
    def __init__(self, hp, speed, level, settings, *parent_groups):
        super(EnemyBase, self).__init__(*parent_groups)
        self.settings = settings
        self.hp = hp
        self.speed = speed
        self.level = level
        self.image = ENEMY_IMAGES['square_enemy']


class SquareEnemy(EnemyBase):
    def __init__(self, hp, speed, level, settings, parent_groups):
        super(SquareEnemy, self).__init__(hp, speed, level, settings, *parent_groups)
        self.image = ENEMY_IMAGES['square_enemy']
        self.hp *= settings.square_enemy_hp_multiplier
        self.speed *= settings.square_enemy_speed_multiplier


class TriangleEnemy(EnemyBase):
    def __init__(self, hp, speed, level, settings, parent_groups):
        super(TriangleEnemy, self).__init__(hp, speed, level, settings, *parent_groups)
        self.image = ENEMY_IMAGES['triangle_enemy']
        self.hp *= settings.triangle_enemy_hp_multiplier
        self.speed *= settings.triangle_enemy_speed_multiplier


class RhombusEnemy(EnemyBase):
    def __init__(self, hp, speed, level, settings, parent_groups):
        super(RhombusEnemy, self).__init__(hp, speed, level, settings, *parent_groups)
        self.image = ENEMY_IMAGES['rhombus_enemy']
        self.hp *= settings.rhombus_enemy_hp_multiplier
        self.speed *= settings.rhombus_enemy_speed_multiplier
