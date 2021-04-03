import pygame as pg
from functions import load_image

ROAD_IMAGES = {
    'spawn': load_image('roads/start_road.png'),
    'end': load_image('roads/end_road.png'),
    'down_left': load_image('roads/down_left_road.png'),
    'down_right': load_image('roads/down_right_road.png'),
    'right_left': load_image('roads/right_left_road.png'),
    'up_down': load_image('roads/up_down_road.png'),
    'up_left': load_image('roads/up_left_road.png'),
    'up_right': load_image('roads/up_right_road.png')
}


class BaseRoad(pg.sprite.Sprite):
    def __init__(self, parent_groups):
        super(BaseRoad, self).__init__(parent_groups)

    def init_image(self, top_left, width, height):
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left


class EnemySpawn(BaseRoad):
    def __init__(self, parent_groups):
        super(EnemySpawn, self).__init__(parent_groups)
        self.image = ROAD_IMAGES['spawn']


class EnemyDestination(BaseRoad):
    def __init__(self, parent_groups):
        super(EnemyDestination, self).__init__(parent_groups)
        self.image = ROAD_IMAGES['end']


class RightLeftRoad(BaseRoad):
    def __init__(self, parent_groups):
        super(RightLeftRoad, self).__init__(parent_groups)
        self.image = ROAD_IMAGES['right_left']


class UpDownRoad(BaseRoad):
    def __init__(self, parent_groups=()):
        super(UpDownRoad, self).__init__(parent_groups)
        self.image = ROAD_IMAGES['up_down']


class DownRightRoad(BaseRoad):
    def __init__(self, parent_groups=()):
        super(DownRightRoad, self).__init__(parent_groups)
        self.image = ROAD_IMAGES['down_right']


class DownLeftRoad(BaseRoad):
    def __init__(self, parent_groups=()):
        super(DownLeftRoad, self).__init__(parent_groups)
        self.image = ROAD_IMAGES['down_left']


class UpRightRoad(BaseRoad):
    def __init__(self, parent_groups=()):
        super(UpRightRoad, self).__init__(parent_groups)
        self.image = ROAD_IMAGES['up_right']


class UpLeftRoad(BaseRoad):
    def __init__(self, parent_groups=()):
        super(UpLeftRoad, self).__init__(parent_groups)
        self.image = ROAD_IMAGES['up_left']


ROAD_SYMBOLS = {
    'S': EnemySpawn,
    'X': EnemyDestination,
    '-': RightLeftRoad, '|': UpDownRoad,
    'r': UpRightRoad, '\\': UpLeftRoad,
    'L': DownRightRoad, '/': DownLeftRoad
}
