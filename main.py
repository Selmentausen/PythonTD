from classes.board import Board
import pygame as pg
import sys
from characters import BaseTower, ArrowTower
from settings import Settings

pg.init()

FPS = 60
SCREEN_SIZE = (800, 600)


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
    board = Board(10, 10, SCREEN_SIZE, settings)
    board.add_tower_to_cell(ArrowTower, 0, 0)
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
        settings.all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    settings = Settings()

    start_screen(screen)
    main_loop()
