import pygame as pg


class Settings:
    def __init__(self):
        self.screen_size = self.screen_width, self.screen_height = (0, 0)
        self.buy_menu_size = (0, 0)
        self.map_size = (0, 0)
        self.fps = 60

    def set_screen_sizes(self, screen_size):
        self.screen_size = screen_size
        self.map_size = (screen_size[0], screen_size[1] * 0.75)
        self.buy_menu_size = (screen_size[0], screen_size[1] * 0.25)
