import pygame as pg
from .roads import BaseRoad, EnemySpawn, EnemyDestination
from .towers import BaseTower


class Board:
    def __init__(self, board_list, settings):
        screen_width, screen_height = settings.screen_size
        screen_size = screen_width, screen_height * settings.map_height
        self.screen_size = screen_size
        self.settings = settings
        self.board = board_list
        self.rows = len(board_list)
        self.cols = len(board_list[0]) if board_list else 0
        self.cell_x_size = int(self.screen_size[0] / (self.cols + 2))
        self.cell_y_size = int(self.screen_size[1] / (self.rows + 2))
        self.enemy_start_cell = None
        self.enemy_destination_cell = None
        self._init_roads()

    def render(self, screen: pg.Surface, draw_occupied=False):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.get_object_in_cell(i, j) and draw_occupied:
                    color = pg.Color('Red')
                else:
                    color = pg.Color('White')
                pg.draw.rect(screen, color, [*self.get_cell_top_left_coordinates(i, j),
                                             self.cell_x_size, self.cell_y_size], 1)

    def update(self, events, screen, placing_tower=None):
        self.render(screen, draw_occupied=bool(placing_tower))

        if self.settings.wave_start:
            if self.settings.current_wave:
                self.spawn_enemy()
            else:
                self.settings.wave_start = False

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                cell_pos = self.get_cell_by_position(event.pos)
                if cell_pos:
                    if placing_tower == 'sell':
                        self.sell_tower(*cell_pos)
                    elif placing_tower == 'upgrade':
                        self.upgrade_tower(*cell_pos)
                    elif placing_tower:
                        self.add_tower_to_cell(placing_tower, *cell_pos)
                    else:
                        self.mouse_click(cell_pos)

    def mouse_click(self, cell_pos):
        obj = self.get_object_in_cell(*cell_pos)
        if obj:
            try:
                obj.clicked()
            except AttributeError:
                print(f'{obj} ({obj.__class__.__name__}) cannot be clicked')

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

    def add_tower_to_cell(self, tower, row, col):
        if self.board[row][col]:
            print('cell occupied')
            return
        object_top_left = self.get_cell_top_left_coordinates(row, col)
        self.board[row][col] = tower(self.settings, object_top_left, (self.cell_x_size, self.cell_y_size))
        self.settings.selected_tower = None
        self.settings.money -= self.settings.tower_cost[tower.__name__]

    def sell_tower(self, row, col):
        tower = self.board[row][col]
        try:
            if issubclass(tower.__class__, BaseTower):
                self.settings.money += self.settings.tower_cost[tower.__class__.__name__] // 2
                tower.kill()
                self.board[row][col] = None
                self.settings.selected_tower = None
        except TypeError:
            pass

    def upgrade_tower(self, row, col):
        tower = self.board[row][col]
        try:
            if issubclass(tower.__class__, BaseTower):
                tower.upgrade()
                self.settings.selected_tower = None
        except TypeError:
            pass

    def spawn_enemy(self):
        spawn_cell_rect = pg.Rect(self.get_cell_top_left_coordinates(*self.enemy_start_cell),
                                  (self.cell_x_size, self.cell_y_size))
        for enemy in self.settings.enemy_sprites:
            if spawn_cell_rect.collidepoint(enemy.rect.center):
                return
        new_enemy = self.settings.current_wave.pop(0)
        new_enemy(self.settings, self)

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
