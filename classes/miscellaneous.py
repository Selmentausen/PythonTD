import pygame as pg
from functions import load_image
from math import hypot
import pygame as pg

BULLET_IMAGES = {
    'normal_bullet': load_image('towers/big_bullet.png')
}


class Button(pg.sprite.Sprite):
    def __init__(self, top_left, width, height, settings):
        super(Button, self).__init__(settings.all_sprites)
        self.settings = settings
        self.top_left = top_left
        self.width = width
        self.height = height
        self.image = pg.transform.scale(load_image('button.jpg', colorkey=-1), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left

    def click(self):
        pass


class StartWaveButton(Button):
    def click(self):
        self.settings.start_wave = True


class Bullet(pg.sprite.Sprite):
    def __init__(self, start, enemy, damage, settings):
        super(Bullet, self).__init__(settings.all_sprites, settings.bullet_sprites)
        self.settings = settings
        self.image = BULLET_IMAGES['normal_bullet']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start
        self.speed = settings.bullet_speed
        self.damage = damage
        self.x, self.y = start
        self.enemy = enemy

    def update(self, delta_time, screen):
        if pg.sprite.collide_rect(self, self.enemy):
            self.enemy.hit(self.damage)
            self.kill()
        self._update_unit_vector()
        self.x += self.unit_vector[0] * self.speed * delta_time
        self.y += self.unit_vector[1] * self.speed * delta_time
        self.rect.x = self.x
        self.rect.y = self.y

    def _update_unit_vector(self):
        v = self.enemy.rect.centerx - self.rect.centerx, self.enemy.rect.centery - self.rect.centery
        vm = hypot(*v)
        self.unit_vector = (v[0] / vm, v[1] / vm)
