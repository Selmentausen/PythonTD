import pygame as pg
from functions import load_image
from random import uniform
import classes.roads as roads

ENEMY_IMAGES = {
    'placeholder_enemy': load_image('enemies/enemy_placeholder.png'),
    'square_enemy': load_image('enemies/enemy_square.png'),
    'circle_enemy': load_image('enemies/enemy_circle.png'),
    'rhombus_enemy': load_image('enemies/enemy_rhombus.png')
}

ROAD_DIRECTIONS = {
    'EnemySpawn': (1, 0),
    'RightRoad': (1, 0), 'LeftRoad': (-1, 0),
    'DownRoad': (0, 1), 'UpRoad': (0, -1),
    'UpRightRoad': (1, -1), 'LeftDownRoad': (-1, 1),
    'UpLeftRoad': (-1, -1), 'RightDownRoad': (1, 1),
    'DownRightRoad': (1, 1), 'LeftUpRoad': (-1, -1),
    'DownLeftRoad': (-1, 1), 'RightUpRoad': (1, -1)
}


class EnemyBase(pg.sprite.Sprite):
    def __init__(self, settings, board):
        super(EnemyBase, self).__init__(settings.enemy_sprites, settings.all_sprites)
        self.image = ENEMY_IMAGES['placeholder_enemy']
        self.current_cell = board.enemy_start_cell
        self.board = board
        self.settings = settings

        self.x, self.y = 0, 0
        self.hp = settings.enemy_base_hp * settings.enemy_hp_multiplier[self.__class__.__name__] * (
                1 + (settings.difficulty_increment * (settings.enemy_level - 1)))
        self.speed = settings.enemy_base_speed * settings.enemy_speed_multiplier[self.__class__.__name__] * (
                1 + settings.difficulty_increment * (settings.enemy_level - 1))
        self.max_hp = self.hp
        self.level = settings.enemy_level
        self.set_start_pos()
        self.hp_bar = self.update_health_bar()

    def update(self, *args, **kwargs) -> None:
        delta_time, screen = kwargs['delta_time'], kwargs['screen']
        self.move_on_road(delta_time)
        self._update_rect()
        screen.blit(self.hp_bar, (self.rect.x, self.rect.y))

    def _update_rect(self):
        self.rect.x, self.rect.y = self.x, self.y

    def update_health_bar(self):
        w, h = self.rect.width * (self.hp / self.max_hp), self.rect.height * 0.2
        hp_bar = pg.Surface((w, h))
        hp_bar.fill((255, 0, 0))
        hp_bar.set_alpha(200)
        return hp_bar

    def set_start_pos(self):
        x, y = self.board.get_cell_top_left_coordinates(*self.board.enemy_start_cell)
        self.x, self.y = x + self.board.cell_x_size // 4, y + self.board.cell_y_size // 4
        self.image = pg.transform.scale(self.image, (self.board.cell_x_size // 2, self.board.cell_y_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def move_on_road(self, delta_time):
        i, j = self.board.get_cell_by_position((self.x, self.y))
        x, y = self.board.get_cell_top_left_coordinates(i, j)
        road = self.board.get_object_in_cell(i, j)
        cell_x_center = x + self.board.cell_x_size // 2
        cell_y_center = y + self.board.cell_y_size // 2
        if not isinstance(road, roads.BaseRoad):
            self.die()
        elif isinstance(road, roads.EnemyDestination):
            self.die(at_finish=True)
        else:
            road_name = road.__class__.__name__
            x_dir, y_dir = ROAD_DIRECTIONS[road_name]
            jiggle = uniform(-self.speed * self.settings.jiggle_intensity,
                             self.speed * self.settings.jiggle_intensity)
            if road_name in ['LeftDownRoad', 'LeftUpRoad']:
                if self.rect.center[0] > cell_x_center:
                    move = self.speed * x_dir, jiggle
                else:
                    move = jiggle, self.speed * y_dir
            elif road_name in ['RightDownRoad', 'RightUpRoad']:
                if self.rect.center[0] < cell_x_center:
                    move = self.speed * x_dir, jiggle
                else:
                    move = jiggle, self.speed * y_dir
            elif road_name in ['UpRightRoad', 'UpLeftRoad']:
                if self.rect.center[1] > cell_y_center:
                    move = jiggle, self.speed * y_dir
                else:
                    move = self.speed * x_dir, jiggle
            elif road_name in ['DownRightRoad', 'DownLeftRoad']:
                if self.rect.center[1] < cell_y_center:
                    move = jiggle, self.speed * y_dir
                else:
                    move = self.speed * x_dir, jiggle
            elif road_name in ['RightRoad', 'LeftRoad']:
                move = self.speed * x_dir, jiggle
            elif road_name in ['UpRoad', 'DownRoad']:
                move = jiggle, self.speed * y_dir
            else:
                move = self.speed * x_dir, self.speed * y_dir
            move = [c * delta_time for c in move]
            self.x += move[0]
            self.y += move[1]

    def die(self, at_finish=False):
        if at_finish:
            self.settings.lives -= 1
            self.kill()
        elif self.alive():
            self.settings.money += self.settings.kill_reward
            self.kill()

    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()
            return
        self.hp_bar = self.update_health_bar()


class SquareEnemy(EnemyBase):
    def __init__(self, *args, **kwargs):
        super(SquareEnemy, self).__init__(*args, **kwargs)
        self.image = ENEMY_IMAGES['square_enemy']
        self.image.set_alpha(210)
        self.set_start_pos()


class CircleEnemy(EnemyBase):
    def __init__(self, *args, **kwargs):
        super(CircleEnemy, self).__init__(*args, **kwargs)
        self.image = ENEMY_IMAGES['circle_enemy']
        self.image.set_alpha(180)
        self.set_start_pos()


class RhombusEnemy(EnemyBase):
    def __init__(self, *args, **kwargs):
        super(RhombusEnemy, self).__init__(*args, **kwargs)
        self.image = ENEMY_IMAGES['rhombus_enemy']
        self.image.set_alpha(180)
        self.set_start_pos()


ENEMY_SYMBOLS = {
    'R': RhombusEnemy,
    'S': SquareEnemy,
    'C': CircleEnemy
}
