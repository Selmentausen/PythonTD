import pygame as pg


class Settings:
    def __init__(self):
        self.screen_size = self.screen_width, self.screen_height = (800, 600)
        self.buy_menu_size = self.buy_menu_size_width, self.buy_menu_size_height = (self.screen_width, 200)
        self.map_size = self.screen_width, self.screen_height = (self.screen_width,
                                                                 (self.screen_height - self.buy_menu_size_height))
        self.fps = 60
