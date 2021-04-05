import pygame as pg
import sys
from random import randrange

pg.init()
screen = pg.display.set_mode((1024, 768))
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
enemy_sprites = pg.sprite.Group()
tower_sprites = pg.sprite.Group()

from classes.towers import ArrowTower
from classes.board import MapBoard, BuyMenuBoard
from classes.miscellaneous import Button
from classes.roads import ROAD_SYMBOLS
from classes import enemies
from settings import Settings
from functions import load_level, load_image
from random import choice

settings = Settings()
settings.set_screen_sizes(screen.get_size())
ENEMY_SPAWN_EVENT = pg.USEREVENT + 10
TEST_EVENT = pg.USEREVENT + 15

BACKGROUND_IMAGES = [load_image(f'background/bg{i}.png') for i in range(1, 8)] + [
    load_image('background/bg_blank.png')] * 50


def terminate():
    pg.quit()
    sys.exit()


def start_screen(surface):
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                running = False
        surface.fill(pg.Color('Red'))
        pg.display.flip()


def menu(surface):
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    running = False
        surface.fill(pg.Color('Blue'))
        pg.display.flip()


def generate_map_board_list(level):
    rows, cols = [int(n) for n in level[0].split(',')]
    board_list = [[None for _ in range(cols)] for _ in range(rows)]
    for y in range(1, rows + 1):
        for x in range(cols):
            symbol = level[y][x]
            road = ROAD_SYMBOLS.get(symbol, None)
            if road:
                board_list[y - 1][x] = road(all_sprites)
    return board_list


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


def generate_buy_menu_board_list():
    board_list = []
    for i in range(3):
        pass


def create_background_surface(screen_size):
    surface = pg.Surface(screen_size)
    size_x = size_y = 16
    for i in range(screen_size[0] // 16):
        for j in range(screen_size[1] // 16):
            surface.blit(choice(BACKGROUND_IMAGES), (size_x * i, size_y * j))
    return surface


def main_loop():
    delta_time = clock.tick() / 1000
    pg.time.set_timer(ENEMY_SPAWN_EVENT, 700)
    pg.time.set_timer(TEST_EVENT, 100)


    board_list = generate_map_board_list(load_level('1.txt'))
    map_board = MapBoard(board_list, settings.map_size, settings)

    all_waves = generate_enemy_waves(load_level('1.txt'))
    current_wave = all_waves.pop(0)
    wave_start = False

    background_surface = create_background_surface(screen.get_size())

    map_board.add_object_to_cell(ArrowTower, 2, 2, parent_groups=[tower_sprites])
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    terminate()
                if event.key == pg.K_m:
                    menu(screen)
                if event.key == pg.K_f:
                    pg.display.toggle_fullscreen()
                if event.key == pg.K_p:
                    wave_start = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                map_board.mouse_click_handler(event)
            elif event.type == ENEMY_SPAWN_EVENT:
                if current_wave and wave_start:
                    enemy = current_wave.pop(0)
                    enemy(30, 100, 1, settings, map_board, enemy_sprites)
                elif all_waves and not current_wave:
                    current_wave = all_waves.pop(0)
                    wave_start = False
            elif event.type == TEST_EVENT:
                tower_sprites.update(enemy_sprites)
        screen.fill(pg.Color('black'))
        screen.blit(background_surface, (0, 0))
        # map_board.render(screen)
        enemy_sprites.update(delta_time)
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)
        tower_sprites.draw(screen)
        pg.display.flip()
        delta_time = clock.tick(60) / 1000


if __name__ == '__main__':
    start_screen(screen)
    main_loop()
