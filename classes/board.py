import pygame as pg
from exceptions import CellOccupied
from .towers import BaseTower


class Board:
    def __init__(self, board_list, screen_size, settings):
        screen_width, screen_height = screen_size
        self.settings = settings
        self.offset = 1
        self.board = board_list
        self.rows = len(board_list)
        self.cols = len(board_list[0])
        self.cell_x_size = int(screen_width / (self.cols + self.offset * 2))
        self.cell_y_size = int(screen_height / (self.rows + self.offset * 2))

    def get_empty_board(self):
        return [[None] * self.cols for _ in range(self.rows)]

    def render(self, screen: pg.Surface):
        for i in range(self.rows):
            for j in range(self.cols):
                pg.draw.rect(screen, pg.Color('White'), [*self._get_cell_top_left_coordinates(i, j),
                                                         self.cell_x_size, self.cell_y_size], 1)

    def mouse_click_handler(self, event):
        pos = self.get_cell_by_position(event.pos)
        if pos:
            obj = self.get_object_in_cell(*pos)
            try:
                obj.clicked()
            except AttributeError:
                print(obj.__class__.__name__, 'cannot be clicked')

    def get_object_in_cell(self, row, col):
        return self.board[row][col]

    def get_cell_by_position(self, pos):
        x, y = pos
        row = int((y - self.cell_y_size) // self.cell_y_size)
        col = int((x - self.cell_x_size) // self.cell_x_size)
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return row, col

    def _get_cell_top_left_coordinates(self, row: int, col: int) -> (int, int):
        return self.cell_x_size * (col + 1), self.cell_y_size * (row + 1)

    def add_object_to_cell(self, obj, row, col, replace=False, parent_groups=()):
        if not replace and self.board[row][col]:
            raise CellOccupied
        object_top_left = self._get_cell_top_left_coordinates(row, col)
        self.board[row][col] = obj(object_top_left, self.cell_x_size, self.cell_y_size, parent_groups)


class MapBoard(Board):
    pass


class BuyMenuBoard(Board):
    def __init__(self, rows, cols, screen_size, settings, board_offset):
        super(BuyMenuBoard, self).__init__(rows, cols, screen_size, settings)
        self.board_offset_x, self.board_offset_y = board_offset

    def _get_cell_top_left_coordinates(self, row, col):
        return self.board_offset_x + self.cell_x_size * (col + 1), self.board_offset_y + self.cell_y_size * (row + 1)

    def get_cell_by_position(self, pos):
        x, y = pos
        row = int((y - self.cell_y_size - self.board_offset_y) // self.cell_y_size)
        col = int((x - self.cell_x_size - self.board_offset_x) // self.cell_x_size)
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return row, col
