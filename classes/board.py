import pygame as pg


class Board:
    def __init__(self, rows, columns, screen_size):
        screen_width, screen_height = screen_size
        self.offset = 1
        self.rows = rows
        self.columns = columns
        self.cell_x_size = screen_width / (self.rows + self.offset * 2)
        self.cell_y_size = screen_height / (self.columns + self.offset * 2)
        self.board = self.get_empty_board()

    def get_empty_board(self):
        return [[None] * self.columns for _ in range(self.rows)]

    def render(self, screen: pg.Surface):
        for i in range(self.rows):
            for j in range(self.columns):
                pg.draw.rect(screen, pg.Color('White'),
                             (self.cell_x_size * (j + 1), self.cell_y_size * (i + 1),
                              self.cell_x_size, self.cell_y_size),
                             1)
