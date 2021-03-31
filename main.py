import pygame as pg
import sys

from classes.towers import ArrowTower, BaseTower
from classes.board import MapBoard, BuyMenuBoard
from classes.miscellaneous import Button
from settings import Settings
from functions import load_level, generate_board_list

pg.init()
all_sprites = pg.sprite.Group()


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
    board_list = generate_board_list(load_level('1.txt'))
    map_board = MapBoard(board_list, settings.map_size, settings)
    # buy_menu_board = BuyMenuBoard(3, 10, settings.buy_menu_size, settings, (0, settings.map_size[1]))
    # map_board.add_object_to_cell(ArrowTower, 0, 0, parent_groups=[all_sprites])
    # map_board.add_object_to_cell(BaseTower, 3, 5, parent_groups=[all_sprites])
    # buy_menu_board.add_object_to_cell(Button, 0, 0, parent_groups=[all_sprites])
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                map_board.mouse_click_handler(event)
                # buy_menu_board.mouse_click_handler(event)
        screen.fill(pg.Color('black'))
        map_board.render(screen)
        # buy_menu_board.render(screen)
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(settings.fps)


if __name__ == '__main__':
    settings = Settings()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    settings.set_screen_sizes(screen.get_size())
    clock = pg.time.Clock()

    start_screen(screen)
    main_loop()
