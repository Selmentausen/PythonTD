import pygame as pg
import sys

pg.init()
screen = pg.display.set_mode((1024, 768))
clock = pg.time.Clock()

from classes import towers
from classes.board import MapBoard, BuyMenuBoard
from classes.buttons import Button
from settings import Settings
from functions import load_level
from game_functions import create_background_surface, generate_map_board_list, add_buttons
from game_functions import generate_enemy_waves


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
        clock.tick()


def menu(surface):
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_q:
                    terminate()
                elif event.key == pg.K_r:
                    return True
        surface.fill(pg.Color('Blue'))
        pg.display.flip()
        clock.tick()


def main_loop():
    settings = Settings()
    settings.set_screen_sizes(screen.get_size())
    ENEMY_SPAWN_EVENT = pg.USEREVENT + 10
    # TEST_EVENT = pg.USEREVENT + 15

    delta_time = clock.tick() / 1000
    pg.time.set_timer(ENEMY_SPAWN_EVENT, 1500)
    # pg.time.set_timer(TEST_EVENT, 10)

    board_list = generate_map_board_list(load_level('1.txt'), settings)
    map_board = MapBoard(board_list, settings)
    map_board.add_object_to_cell(towers.NormalTower, 2, 2)
    add_buttons(screen, settings)

    all_waves = generate_enemy_waves(load_level('1.txt'))
    current_wave = all_waves.pop(0)

    background_surface = create_background_surface(screen.get_size())

    while True:
        events = pg.event.get()
        for event in events.copy():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if menu(screen):
                        return True
                if event.key == pg.K_p:
                    settings.wave_start = True
            elif event.type == ENEMY_SPAWN_EVENT:
                if current_wave and settings.wave_start:
                    enemy = current_wave.pop(0)
                    enemy(30, 30, 1, settings, map_board)
                elif all_waves and not current_wave:
                    current_wave = all_waves.pop(0)
                    settings.wave_start = False

        screen.fill(pg.Color('black'))
        screen.blit(background_surface, (0, 0))
        map_board.update(events.copy(), screen)
        settings.all_sprites.draw(screen)
        settings.all_sprites.update(delta_time=delta_time, screen=screen, mouse_pos=pg.mouse.get_pos())

        pg.display.flip()
        delta_time = clock.tick(60) / 1000


if __name__ == '__main__':
    start_screen(screen)
    while main_loop():
        pass
    terminate()
