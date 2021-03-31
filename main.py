import pygame as pg
import sys

pg.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()


from classes.towers import ArrowTower, BaseTower
from classes.board import MapBoard, BuyMenuBoard
from classes.miscellaneous import Button
from classes.roads import ROAD_SYMBOLS
from settings import Settings
from functions import load_level


settings = Settings()
settings.set_screen_sizes(screen.get_size())


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


def generate_board_list(level):
    rows, cols = len(level), len(level[0])
    board_list = [[None for _ in range(cols)] for _ in range(rows)]
    for y in range(rows):
        for x in range(cols):
            symbol = level[y][x]
            road = ROAD_SYMBOLS.get(symbol, None)
            if road:
                board_list[y][x] = road(all_sprites)
    return board_list


def main_loop():
    board_list = generate_board_list(load_level('1.txt'))
    map_board = MapBoard(board_list, settings.map_size, settings)
    print(all_sprites)
    # buy_menu_board = BuyMenuBoard(3, 10, settings.buy_menu_size, settings, (0, settings.map_size[1]))
    map_board.add_object_to_cell(ArrowTower, 0, 0, parent_groups=[all_sprites])
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
    start_screen(screen)
    main_loop()
