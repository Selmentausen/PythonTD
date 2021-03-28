import pygame as pg
import sys

from classes.towers import ArrowTower
from classes.board import Board
from classes.miscellaneous import Button
from settings import Settings

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
    board = Board(6, 6, settings.map_size, settings)
    board.add_tower_to_cell(ArrowTower, 0, 0, parent_groups=[all_sprites])
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    terminate()
                if event.key == pg.K_m:
                    menu(screen)
            elif event.type == pg.MOUSEBUTTONDOWN:
                coords = board.get_cell_by_position(event.pos)
                if coords:
                    print(board.get_object_in_cell(*coords))
        screen.fill(pg.Color('black'))
        board.render(screen)
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
