import pygame as pg
import sys

pg.init()
screen = pg.display.set_mode((1024, 768))
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
enemy_sprites = pg.sprite.Group()
tower_sprites = pg.sprite.Group()

from classes import towers
from classes.board import MapBoard, BuyMenuBoard
from settings import Settings
from functions import load_level
from game_functions import create_background_surface, generate_map_board_list
from game_functions import generate_enemy_waves

settings = Settings()
settings.set_screen_sizes(screen.get_size())
ENEMY_SPAWN_EVENT = pg.USEREVENT + 10
TEST_EVENT = pg.USEREVENT + 15


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


def main_loop():
    delta_time = clock.tick() / 1000
    pg.time.set_timer(ENEMY_SPAWN_EVENT, 700)
    pg.time.set_timer(TEST_EVENT, 10)

    board_list = generate_map_board_list(load_level('1.txt'), all_sprites)
    map_board = MapBoard(board_list, settings.map_size, settings)

    all_waves = generate_enemy_waves(load_level('1.txt'))
    current_wave = all_waves.pop(0)
    wave_start = False

    background_surface = create_background_surface(screen.get_size())

    map_board.add_object_to_cell(towers.ArrowTower, 2, 2, tower_sprites, all_sprites)
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
                    enemy(30, 30, 1, settings, map_board, enemy_sprites, all_sprites)
                elif all_waves and not current_wave:
                    current_wave = all_waves.pop(0)
                    wave_start = False

        screen.fill(pg.Color('black'))
        screen.blit(background_surface, (0, 0))
        map_board.render(screen)

        all_sprites.draw(screen)
        tower_sprites.update(delta_time, enemy_sprites, screen)
        enemy_sprites.update(delta_time)

        pg.display.flip()
        delta_time = clock.tick(60) / 1000


if __name__ == '__main__':
    start_screen(screen)
main_loop()
