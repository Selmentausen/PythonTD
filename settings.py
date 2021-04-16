import pygame as pg


class Settings:
    def __init__(self):
        self.screen_size = self.screen_width, self.screen_height = (0, 0)
        self.map_height = 0.75
        self.buy_menu_height = 0.25
        self.fps = 30

        # Game logic
        self.wave_start = False
        self.selected_tower = None
        self.money = 150

        # Sprite groups
        self.all_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.tower_sprites = pg.sprite.Group()
        self.bullet_sprites = pg.sprite.Group()
        self.road_sprites = pg.sprite.Group()
        self.button_sprites = pg.sprite.Group()

        # Enemy settings
        self.kill_reward = 5
        self.enemy_hp_multiplier = {'RhombusEnemy': 1, 'SquareEnemy': 1.5, 'CircleEnemy': 0.5}
        self.enemy_speed_multiplier = {'RhombusEnemy': 1, 'SquareEnemy': 0.5, 'CircleEnemy': 1.5}
        self.jiggle_intensity = 0.3

        # Tower settings
        self.tower_range = {'BaseTower': 0, 'NormalTower': 200, 'FastTower': 150, 'SplitTower': 100}
        self.tower_attack_speed = {'BaseTower': 0, 'NormalTower': 1, 'FastTower': 0.4, 'SplitTower': 1.5}
        self.tower_damage = {'BaseTower': 0, 'NormalTower': 10, 'FastTower': 5, 'SplitTower': 3}
        self.tower_cost = {'BaseTower': 0, 'NormalTower': 50, 'FastTower': 70, 'SplitTower': 80}
        self.split_tower_targets = 3
        self.bullet_speed = 200

    def set_screen_sizes(self, screen_size):
        self.screen_size = screen_size
