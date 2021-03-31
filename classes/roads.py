import pygame as pg


class BaseRoad(pg.sprite.Sprite):
    pass


class RightRoad(BaseRoad):
    pass


class UpRightRoad(BaseRoad):
    pass


class DownRightRoad(BaseRoad):
    pass


class LeftRoad(BaseRoad):
    pass


class UpLeftRoad(BaseRoad):
    pass


class DownLeftRoad(BaseRoad):
    pass


class UpRoad(BaseRoad):
    pass


class RightUpRoad(BaseRoad):
    pass


class LeftUpRoad(BaseRoad):
    pass


class DownRoad(BaseRoad):
    pass


class RightDownRoad(BaseRoad):
    pass


class LeftDownRoad(BaseRoad):
    pass


class EnemySpawn(pg.sprite.Sprite):
    pass


class EnemyDestination(pg.sprite.Sprite):
    pass


ROAD_SYMBOLS = {
    'S': EnemySpawn,
    'X': EnemyDestination,
    '>': RightRoad, 'R': UpRightRoad, 'r': DownRightRoad,
    '<': LeftRoad, 'L': UpLeftRoad, 'l': DownLeftRoad,
    '^': UpRoad, 'U': RightUpRoad, 'u': LeftUpRoad,
    '|': RightRoad, 'D': RightDownRoad, 'd': LeftDownRoad
}
