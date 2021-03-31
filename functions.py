import os
import sys
import pygame


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
