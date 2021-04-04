import pygame as pg
from functions import load_image
import classes.roads as roads


ENEMY_IMAGES = {
    'placeholder_enemy': load_image('enemies/enemy_placeholder.png'),
    'square_enemy': load_image('enemies/enemy_square.png'),
    'triangle_enemy': load_image('enemies/enemy_triangle.png'),
    'rhombus_enemy': load_image('enemies/enemy_rhombus.png')
}


class EnemyBase(pg.sprite.Sprite):
    def __init__(self, hp, speed, enemy_level, settings, board, *parent_groups):
        super(EnemyBase, self).__init__(*parent_groups)
        self.image = ENEMY_IMAGES['placeholder_enemy']
        self.start_cell = board.enemy_start_cell
        self.board = board
        self.settings = settings
        self.hp = hp
        self.speed = speed
        self.level = enemy_level
        self.set_start_pos()

    def set_start_pos(self):
        self.image = pg.transform.scale(self.image, (self.board.cell_x_size // 2, self.board.cell_y_size // 2))
        self.rect = self.image.get_rect()
        x, y = self.board.get_cell_top_left_coordinates(*self.board.enemy_start_cell)
        self.rect.x, self.rect.y = x + self.board.cell_x_size // 4, y + self.board.cell_y_size // 4

    def move(self):
        pass


class SquareEnemy(EnemyBase):
    def __init__(self, *args, **kwargs):
        super(SquareEnemy, self).__init__(*args, **kwargs)
        self.image = ENEMY_IMAGES['square_enemy']
        self.hp *= self.settings.square_enemy_hp_multiplier
        self.speed *= self.settings.square_enemy_speed_multiplier
        self.set_start_pos()


class TriangleEnemy(EnemyBase):
    def __init__(self, *args, **kwargs):
        super(TriangleEnemy, self).__init__(*args, **kwargs)
        self.image = ENEMY_IMAGES['triangle_enemy']
        self.hp *= self.settings.triangle_enemy_hp_multiplier
        self.speed *= self.settings.triangle_enemy_speed_multiplier
        self.set_start_pos()


class RhombusEnemy(EnemyBase):
    def __init__(self, *args, **kwargs):
        super(RhombusEnemy, self).__init__(*args, **kwargs)
        self.image = ENEMY_IMAGES['rhombus_enemy']
        self.hp *= self.settings.rhombus_enemy_hp_multiplier
        self.speed *= self.settings.rhombus_enemy_speed_multiplier
        self.set_start_pos()
