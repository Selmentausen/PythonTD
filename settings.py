class Settings:
    def __init__(self):
        self.screen_size = self.screen_width, self.screen_height = (0, 0)
        self.buy_menu_size = (0, 0)
        self.map_size = (0, 0)
        self.fps = 60

        # Enemy settings
        self.square_enemy_hp_multiplier = 1.5
        self.square_enemy_speed_multiplier = 0.5
        self.triangle_enemy_hp_multiplier = 0.5
        self.triangle_enemy_speed_multiplier = 1.5
        self.rhombus_enemy_hp_multiplier = 1
        self.rhombus_enemy_speed_multiplier = 1

    def set_screen_sizes(self, screen_size):
        self.screen_size = screen_size
        self.map_size = (screen_size[0], screen_size[1] * 0.75)
        self.buy_menu_size = (screen_size[0], screen_size[1] * 0.25)
