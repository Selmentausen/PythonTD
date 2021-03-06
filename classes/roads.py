import pygame as pg
from functions import load_image
from random import choice

ROAD_IMAGES = {
    'spawn': load_image('roads/start_road.png'),
    'end': load_image('roads/end_road.png'),
    'down_left': load_image('roads/down_left_road.png'),
    'down_right': load_image('roads/down_right_road.png'),
    'right_left': (load_image('roads/right_left_road.png'), load_image('roads/right_left_road_2.png'),
                   load_image('roads/right_left_road_3.png')),
    'up_down': (load_image('roads/up_down_road.png'), load_image('roads/up_down_road_2.png'),
                load_image('roads/up_down_road_3.png')),
    'up_left': load_image('roads/up_left_road.png'),
    'up_right': load_image('roads/up_right_road.png')
}


class BaseRoad(pg.sprite.Sprite):
    def __init__(self, settings):
        super(BaseRoad, self).__init__(settings.all_sprites, settings.road_sprites)

    def init_image(self, top_left, width, height):
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left


class EnemySpawn(BaseRoad):
    def __init__(self, settings):
        super(EnemySpawn, self).__init__(settings)
        self.image = ROAD_IMAGES['spawn']


class EnemyDestination(BaseRoad):
    def __init__(self, settings):
        super(EnemyDestination, self).__init__(settings)
        self.image = ROAD_IMAGES['end']


class RightRoad(BaseRoad):
    def __init__(self, settings):
        super(RightRoad, self).__init__(settings)
        self.image = choice(ROAD_IMAGES['right_left'])


class LeftRoad(BaseRoad):
    def __init__(self, settings):
        super(LeftRoad, self).__init__(settings)
        self.image = choice(ROAD_IMAGES['right_left'])


class UpRoad(BaseRoad):
    def __init__(self, settings):
        super(UpRoad, self).__init__(settings)
        self.image = choice(ROAD_IMAGES['up_down'])


class DownRoad(BaseRoad):
    def __init__(self, settings):
        super(DownRoad, self).__init__(settings)
        self.image = choice(ROAD_IMAGES['up_down'])


class DownRightRoad(BaseRoad):
    def __init__(self, settings):
        super(DownRightRoad, self).__init__(settings)
        self.image = ROAD_IMAGES['down_right']


class LeftUpRoad(BaseRoad):
    def __init__(self, settings):
        super(LeftUpRoad, self).__init__(settings)
        self.image = ROAD_IMAGES['down_right']


class DownLeftRoad(BaseRoad):
    def __init__(self, settings):
        super(DownLeftRoad, self).__init__(settings)
        self.image = ROAD_IMAGES['down_left']


class RightUpRoad(BaseRoad):
    def __init__(self, settings):
        super(RightUpRoad, self).__init__(settings)
        self.image = ROAD_IMAGES['down_left']


class UpRightRoad(BaseRoad):
    def __init__(self, settings):
        super(UpRightRoad, self).__init__(settings)
        self.image = ROAD_IMAGES['up_right']


class LeftDownRoad(BaseRoad):
    def __init__(self, settings):
        super(LeftDownRoad, self).__init__(settings)
        self.image = ROAD_IMAGES['up_right']


class UpLeftRoad(BaseRoad):
    def __init__(self, settings):
        super(UpLeftRoad, self).__init__(settings)
        self.image = ROAD_IMAGES['up_left']


class RightDownRoad(BaseRoad):
    def __init__(self, settings):
        super(RightDownRoad, self).__init__(settings)
        self.image = ROAD_IMAGES['up_left']


ROAD_SYMBOLS = {
    'S': EnemySpawn,
    'X': EnemyDestination,
    '>': RightRoad, '<': LeftRoad,
    '^': UpRoad, '|': DownRoad,
    'r': UpRightRoad, 'R': LeftDownRoad,
    '\\': UpLeftRoad, '*': RightDownRoad,
    'L': DownRightRoad, 'l': LeftUpRoad,
    '/': DownLeftRoad, '+': RightUpRoad
}
