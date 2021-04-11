import pygame as pg
from functions import load_image

BUTTON_IMAGES = {
    'test_button': load_image('buttons/test.png')
}


class Button(pg.sprite.Sprite):
    def __init__(self, left_top, size, settings):
        super(Button, self).__init__(settings.all_sprites, settings.button_sprites)
        self.settings = settings
        self.image = pg.transform.scale(BUTTON_IMAGES['test_button'], size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = left_top
        self._bound_function = None

    def update(self, *args, **kwargs) -> None:
        mouse_pos = kwargs.get('mouse_pos', None)
        if self.rect.collidepoint(mouse_pos) and pg.mouse.get_pressed(3)[0]:
            self.click()

    def click(self, *args, **kwargs):
        print('hello')
        if callable(self._bound_function):
            return self._bound_function(*args, **kwargs)

    def bind(self, func):
        self._bound_function = func
