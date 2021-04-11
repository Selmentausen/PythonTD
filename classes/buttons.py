import pygame as pg
from functions import load_image

BUTTON_IMAGES = {
    'test_button': load_image('buttons/test.png'),
    'button': load_image('buttons/button.png')
}


class Button(pg.sprite.Sprite):
    def __init__(self, left_top, size, settings):
        super(Button, self).__init__(settings.all_sprites, settings.button_sprites)
        self.settings = settings
        self.image = pg.transform.scale(BUTTON_IMAGES['button'], size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = left_top

    def update(self, *args, **kwargs) -> None:
        mouse_pos = kwargs.get('mouse_pos', None)
        if self.rect.collidepoint(mouse_pos) and pg.mouse.get_pressed(3)[0]:
            self.click()

    def click(self, *args, **kwargs):
        print('hello')


class TowerButton(Button):
    def __init__(self, left_top, size, tower, settings):
        super(TowerButton, self).__init__(left_top, size, settings)
        self.tower = tower
        w, h = self.image.get_size()
        img = pg.transform.scale(self.tower.tower_image[0], (int(w * 0.70), int(h * 0.70)))
        self.image.blit(img, (int(w * 0.15), int(h * 0.15)))

    def click(self, *args, **kwargs):
        self.settings.selected_tower = self.tower


class StartWaveButton(Button):
    def click(self):
        pass

