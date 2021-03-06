import pygame as pg
from .roads import BaseRoad, EnemySpawn, EnemyDestination
from .towers import BaseTower


class Board:
    sounds = {'tower_placed': pg.mixer.Sound('data/sounds/tower_placed.WAV'),
              'tower_sold': pg.mixer.Sound('data/sounds/tower_sold.WAV'),
              'cell_occupied': pg.mixer.Sound('data/sounds/cell_occupied.WAV')}

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

    def update(self, events, screen, action=None):
        self.render(screen, draw_occupied=bool(action))

        if self.settings.wave_start:
            if self.settings.current_wave:
                self.spawn_enemy()
            else:
                self.settings.wave_start = False

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                cell_pos = self.get_cell_by_position(event.pos)
                if cell_pos:
                    if not action:
                        self.mouse_click(cell_pos)
                    elif action == 'sell':
                        self.sell_tower(*cell_pos)
                    elif action == 'upgrade':
                        self.upgrade_tower(*cell_pos)
                    elif issubclass(action, BaseTower):
                        self.add_tower_to_cell(action, *cell_pos)
                    self.settings.action = None

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
        if self.get_object_in_cell(row, col):
            print('cell occupied')
            self.sounds['cell_occupied'].play()
            return
        object_top_left = self.get_cell_top_left_coordinates(row, col)
        self.board[row][col] = tower(self.settings, object_top_left, (self.cell_x_size, self.cell_y_size))
        self.settings.money -= self.settings.tower_cost[tower.__name__]
        self.sounds['tower_placed'].play()

    def sell_tower(self, row, col):
        tower = self.get_object_in_cell(row, col)
        try:
            if issubclass(tower.__class__, BaseTower):
                self.settings.money += self.settings.tower_cost[tower.__class__.__name__] // 2
                tower.kill()
                self.board[row][col] = None
                self.sounds['tower_sold'].play()
        except TypeError:
            return

    def upgrade_tower(self, row, col):
        tower = self.get_object_in_cell(row, col)
        try:
            if issubclass(tower.__class__, BaseTower):
                tower.upgrade()
        except TypeError:
            return

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
