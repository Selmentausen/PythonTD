import pygame as pg


class Settings:
    def __init__(self):
        self.screen_size = self.screen_width, self.screen_height = (0, 0)
        self.buy_menu_size = (0, 0)
        self.map_size = (0, 0)
        self.fps = 30
        # Sprite groups
        self.all_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.tower_sprites = pg.sprite.Group()
        self.bullet_sprites = pg.sprite.Group()
        self.road_sprites = pg.sprite.Group()
        self.button_sprites = pg.sprite.Group()

        # Enemy settings
        self.square_enemy_hp_multiplier = 1.5
        self.square_enemy_speed_multiplier = 0.5
        self.circle_enemy_hp_multiplier = 0.5
        self.circle_enemy_speed_multiplier = 1.5
        self.rhombus_enemy_hp_multiplier = 1
        self.rhombus_enemy_speed_multiplier = 1
        self.jiggle_intensity = 0.3

        # Tower settings
        self.arrow_tower_range = 500
        self.arrow_tower_attack_speed = 1
        self.arrow_tower_damage = 10
        self.bullet_speed = 100

    def set_screen_sizes(self, screen_size):
        self.screen_size = screen_size
        self.map_size = (screen_size[0], screen_size[1] * 0.75)
        self.buy_menu_size = (screen_size[0], screen_size[1] * 0.25)
