import pygame as pg
from exceptions import CellOccupied
from .roads import BaseRoad, EnemySpawn, EnemyDestination
from .towers import BaseTower
from functions import load_image
from random import choice


class Board:
    def __init__(self, board_list, screen_size, settings):
        self.screen_size = screen_size
        self.settings = settings
        self.board = board_list
        self.rows = len(board_list)
        self.cols = len(board_list[0]) if board_list else 0
        self.cell_x_size = int(self.screen_size[0] / (self.cols + 2))
        self.cell_y_size = int(self.screen_size[1] / (self.rows + 2))

    def render(self, screen: pg.Surface):
        for i in range(self.rows):
            for j in range(self.cols):
                pg.draw.rect(screen, pg.Color('White'), [*self.get_cell_top_left_coordinates(i, j),
                                                        self.cell_x_size, self.cell_y_size], 1)

    def mouse_click(self, event):
        pos = self.get_cell_by_position(event.pos)
        if pos:
            obj = self.get_object_in_cell(*pos)
            if obj:
                try:
                    obj.clicked()
                except AttributeError:
                    print(f'{obj} ({obj.__class__.__name__}) cannot be clicked')
            elif self.settings.selected_tower:
                self.add_object_to_cell(self.settings.selected_tower, *pos)
                print(f'added tower {self.settings.selected_tower.__name__} to cell {pos}')
                self.settings.selected_tower = None

    def get_object_in_cell(self, row, col):
        return self.board[row][col]

    def get_cell_by_position(self, pos):
        x, y = pos
        row = int((y - self.cell_y_size) // self.cell_y_size)
        col = int((x - self.cell_x_size) // self.cell_x_size)
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return row, col

    def get_cell_top_left_coordinates(self, row: int, col: int) -> (int, int):
        return self.cell_x_size * (col + 1), self.cell_y_size * (row + 1)

    def add_object_to_cell(self, obj, row, col, replace=False):
        if not replace and self.board[row][col]:
            raise CellOccupied
        object_top_left = self.get_cell_top_left_coordinates(row, col)
        self.board[row][col] = obj(self.settings, object_top_left, (self.cell_x_size, self.cell_y_size))


class MapBoard(Board):
    def __init__(self, board_list, settings):
        screen_width, screen_height = settings.screen_size
        screen_size = screen_width, screen_height * settings.map_height
        super(MapBoard, self).__init__(board_list, screen_size, settings)

        self.enemy_start_cell = None
        self.enemy_destination_cell = None
        self._init_roads()

    def _init_roads(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if isinstance(self.board[i][j], BaseRoad):
                    top_left = self.get_cell_top_left_coordinates(i, j)
                    self.board[i][j].init_image(top_left, self.cell_x_size, self.cell_y_size)
                    if isinstance(self.board[i][j], EnemySpawn):
                        self.enemy_start_cell = i, j
                    elif isinstance(self.board[i][j], EnemyDestination):
                        self.enemy_destination_cell = i, j


class BuyMenuBoard(Board):
    def __init__(self, board_list, settings):
        screen_width, screen_height = settings.screen_size
        screen_size = screen_width, screen_height * settings.buy_menu_height
        super(BuyMenuBoard, self).__init__(board_list, screen_size, settings)
        self.board_offset_x, self.board_offset_y = 0, screen_height * settings.map_height
        self.selected_tower = None

    def get_cell_top_left_coordinates(self, row, col):
        return self.board_offset_x + self.cell_x_size * (col + 1), self.board_offset_y + self.cell_y_size * (row + 1)

    def get_cell_by_position(self, pos):
        x, y = pos
        row = int((y - self.cell_y_size - self.board_offset_y) // self.cell_y_size)
        col = int((x - self.cell_x_size - self.board_offset_x) // self.cell_x_size)
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return row, col

    def mouse_click(self, event):
        pos = self.get_cell_by_position(event.pos)
        if pos:
            obj = self.get_object_in_cell(*pos)
            if issubclass(obj, BaseTower):
                self.settings.selected_tower = obj if self.settings.selected_tower != obj else None
