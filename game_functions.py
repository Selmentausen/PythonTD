from classes.roads import ROAD_SYMBOLS
from classes import enemies
from classes.buttons import TowerButton
from functions import load_image
from random import choice
import pygame as pg

BACKGROUND_IMAGES = [load_image(f'background/bg{i}.png') for i in range(1, 8)] + [
    load_image('background/bg_blank.png')] * 50


def generate_map_board_list(level, settings):
    rows, cols = [int(n) for n in level[0].split(',')]
    board_list = [[None for _ in range(cols)] for _ in range(rows)]
    for y in range(1, rows + 1):
        for x in range(cols):
            symbol = level[y][x]
            road = ROAD_SYMBOLS.get(symbol, None)
            if road:
                board_list[y - 1][x] = road(settings)
    return board_list


def add_buttons(screen, settings, tower_list):
    w, h = screen.get_size()
    buttons_screen = 0, int(h * settings.map_height), w, h
    amount = len(tower_list) + 2
    size = [buttons_screen[2] // (amount + 2), (buttons_screen[3] - buttons_screen[1]) // 2]
    padding = size[0] // 10
    size[0] -= padding * (amount - 1) // amount

    for i, tower in enumerate(tower_list):
        left_top = size[0] * (i + 1) + padding * (i + 1), buttons_screen[1]
        TowerButton(left_top, size, tower, settings)


def generate_enemy_waves(level):
    waves = []
    for line in level:
        wave = []
        if not line.startswith('#'):
            continue
        for wave_enemies in line.split()[1:]:
            enemy, count = wave_enemies[0], int(wave_enemies[1:])
            wave += [enemies.ENEMY_SYMBOLS[enemy] for _ in range(count)]
        waves.append(wave)
    return waves


def create_background_surface(screen_size):
    surface = pg.Surface(screen_size)
    size_x = size_y = 16
    for i in range(screen_size[0] // 16):
        for j in range(screen_size[1] // 16):
            surface.blit(choice(BACKGROUND_IMAGES), (size_x * i, size_y * j))
    return surface


def get_tower_range_surface(tower_range):
    image = pg.transform.scale(load_image('towers/tower_radius.png'),
                               (tower_range * 2, tower_range * 2))
    image.set_alpha(100)
    return image
