import pygame as pg
from exceptions import CellOccupied


class Board:
    def __init__(self, rows, columns, screen_size, settings):
        screen_width, screen_height = screen_size
        self.settings = settings
        self.offset = 1
        self.rows = rows
        self.columns = columns
        self.cell_x_size = int(screen_width / (self.columns + self.offset * 2))
        self.cell_y_size = int(screen_height / (self.rows + self.offset * 2))
        print(self.cell_x_size, self.cell_y_size)
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

    def get_object_in_cell(self, row, col):
        return self.board[row][col]

    def get_cell_by_position(self, pos):
        x, y = pos
        row = int((x - self.cell_x_size) // self.cell_x_size)
        col = int((y - self.cell_y_size) // self.cell_y_size)
        if 0 <= col < self.columns and 0 <= row < self.rows:
            return row, col

    def add_tower_to_cell(self, tower_class, row, col, replace=False, parent_groups=()):
        if not replace and self.board[row][col]:
            raise CellOccupied
        tower_top_left = (self.cell_x_size * (col + 1), self.cell_y_size * (row + 1))
        self.board[row][col] = tower_class(tower_top_left, self.cell_x_size, self.cell_y_size, parent_groups)
