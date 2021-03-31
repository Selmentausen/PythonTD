import pygame as pg
from functions import load_image


class BaseRoad(pg.sprite.Sprite):
    def __init__(self, parent_groups=()):
        super(BaseRoad, self).__init__(parent_groups)


class EnemySpawn(BaseRoad):
    pass


class EnemyDestination(BaseRoad):
    pass


class RightLeftRoad(BaseRoad):
    pass


class UpDownRoad(BaseRoad):
    pass


class DownRightRoad(BaseRoad):
    pass


class DownLeftRoad(BaseRoad):
    pass


class UpRightRoad(BaseRoad):
    pass


class UpLeftRoad(BaseRoad):
    pass


ROAD_SYMBOLS = {
    'S': EnemySpawn,
    'X': EnemyDestination,
    '-': RightLeftRoad, '|': UpDownRoad,
    'r': UpRightRoad, '\\': UpLeftRoad,
    'L': DownRightRoad, '/': DownLeftRoad
}
