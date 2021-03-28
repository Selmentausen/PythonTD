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
                if event.key == pg.K_ESCAPE:
                    running = False
        surface.fill(pg.Color('Blue'))
        pg.display.flip()


def main_loop():
    board = Board(6, 6, settings.map_size, settings)
    print(settings.map_size)
    board.add_tower_to_cell(ArrowTower, 0, 0, parent_groups=[all_sprites])
    test_btn = Button((100, 500), 100, 50, all_sprites)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    menu(screen)
            elif event.type == pg.MOUSEBUTTONDOWN:
                coords = board.get_cell_by_position(event.pos)
                if coords:
                    print(board.get_object_in_cell(*coords))
        screen.fill((0, 0, 0))
        board.render(screen)
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(settings.fps)


if __name__ == '__main__':
    settings = Settings()
    screen = pg.display.set_mode(settings.screen_size)
    clock = pg.time.Clock()

    start_screen(screen)
    main_loop()
