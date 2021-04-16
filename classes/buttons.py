import pygame as pg
from functions import load_image


class Button(pg.sprite.Sprite):
    button_images = {'button': load_image('buttons/button.png'),
                     'button_pressed': load_image('buttons/button_pressed.png'),
                     'button_play': load_image('buttons/button_play.png'),
                     'button_sell': load_image('buttons/button_sell.png')}

    def __init__(self, left_top, size, settings):
        super(Button, self).__init__(settings.all_sprites, settings.button_sprites)
        self.settings = settings
        self.image = pg.transform.scale(self.button_images['button'], size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = left_top

    def update(self, *args, **kwargs) -> None:
        mouse_pos = kwargs.get('mouse_pos', None)
        if self.rect.collidepoint(mouse_pos) and pg.mouse.get_pressed(3)[0]:
            self.click()

    def _change_image(self, base_image, inner_image):
        self.image = pg.transform.scale(base_image, self.rect.size)
        w, h = self.image.get_size()
        tower_img = pg.transform.scale(inner_image, (int(w * 0.70), int(h * 0.70)))
        self.image.blit(tower_img, (int(w * 0.15), int(h * 0.15)))

    def click(self, *args, **kwargs):
        pass


class TowerButton(Button):
    def __init__(self, left_top, size, tower, settings):
        super(TowerButton, self).__init__(left_top, size, settings)
        self.tower = tower
        w, h = self.image.get_size()
        img = pg.transform.scale(self.tower.tower_image[0], (int(w * 0.70), int(h * 0.70)))
        self.image.blit(img, (int(w * 0.15), int(h * 0.15)))

    def update(self, *args, **kwargs) -> None:
        mouse_pos = kwargs.get('mouse_pos', None)

        if self.settings.selected_tower == self.tower:
            self._change_image(self.button_images['button_pressed'], self.tower.tower_image[0])
        else:
            self._change_image(self.button_images['button'], self.tower.tower_image[0])

        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed(3)[0]:
                self.click()

    def click(self, *args, **kwargs):
        self.settings.selected_tower = self.tower


class StartWaveButton(Button):
    def __init__(self, left_top, size, settings):
        super(StartWaveButton, self).__init__(left_top, size, settings)
        self._change_image(self.button_images['button'], self.button_images['button_play'])

    def click(self):
        self.settings.wave_start = True


class SellTowerButton(Button):
    def __init__(self, left_top, size, settings):
        super(SellTowerButton, self).__init__(left_top, size, settings)
        self._change_image(self.button_images['button'], self.button_images['button_sell'])
