from classes.board import Board
import pygame as pg
import sys


pg.init()

FPS = 60
SCREEN_SIZE = (800, 800)


def terminate():
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    screen = pg.display.set_mode(SCREEN_SIZE)
    board = Board(10, 10, SCREEN_SIZE)
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    terminate()
        screen.fill((0, 0, 0))
        board.render(screen)
        pg.display.flip()
        clock.tick(FPS)


