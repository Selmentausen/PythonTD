import os
import sys
import pygame
from classes.roads import ROAD_SYMBOLS


def load_image(name, colorkey=None):
    fullname = os.path.join('data/img', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(name):
    name = os.path.join('data/maps', name)
    with open(name, 'r') as f:
        level_map = [line.strip() for line in f]
    return level_map


def generate_board_list(level):
    rows, cols = len(level), len(level[0])
    board_list = [[None for _ in range(cols)] for _ in range(rows)]
    for y in range(rows):
        for x in range(cols):
            symbol = level[y][x]
            road = ROAD_SYMBOLS.get(symbol, None)
            if road:
                board_list[y][x] = road()
    return board_list
