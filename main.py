import pygame as pg
import sys

pg.init()
screen = pg.display.set_mode((1024, 768))
clock = pg.time.Clock()

from classes import towers
from classes.board import Board
from settings import Settings
from functions import load_level
from game_functions import create_background_surface, generate_map_board_list, add_buttons
from game_functions import generate_enemy_waves, generate_text_surface


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
    map_board = Board(board_list, settings)
    add_buttons(screen, settings, [towers.NormalTower, towers.FastTower, towers.SplitTower])

    settings.enemy_waves = generate_enemy_waves(load_level('1.txt'))

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
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    settings.selected_tower = None
            elif event.type == ENEMY_SPAWN_EVENT:
                print('Money:', settings.money)

        screen.fill(pg.Color('black'))
        screen.blit(background_surface, (0, 0))
        screen.blit(generate_text_surface(settings), (10, 10))
        map_board.update(events.copy(), screen, placing_tower=settings.selected_tower)

        settings.all_sprites.draw(screen)
        settings.all_sprites.update(delta_time=delta_time, screen=screen, mouse_pos=pg.mouse.get_pos())

        pg.display.flip()
        delta_time = clock.tick(60) / 1000


if __name__ == '__main__':
    start_screen(screen)
    while main_loop():
        pass
    terminate()
