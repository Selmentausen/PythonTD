from functions import load_image
from game_functions import get_tower_range_surface
from .miscellaneous import Bullet
import pygame as pg
from math import hypot
from random import sample

TOWER_IMAGES = {
    'normal_tower': load_image('towers/ArrowTower.png')
}

BULLET_IMAGES = {
    'normal_bullet': load_image('towers/normal_bullet.png'),
    'big_bullet': load_image('towers/big_bullet.png')
}


class BaseTower(pg.sprite.Sprite):
    def __init__(self, settings, top_left, size):
        super(BaseTower, self).__init__(settings.all_sprites, settings.tower_sprites)
        self.image = pg.transform.scale(TOWER_IMAGES['normal_tower'], size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left
        self.settings = settings
        self.is_clicked = False

        self.x, self.y = top_left
        self.range = 0
        self.damage = 0
        self.attack_speed = 1
        self.attack_cooldown = 0
        self.hit_order = 'first'

    def update(self, delta_time, screen) -> None:
        self.attack_cooldown = max(self.attack_cooldown - delta_time, 0)
        self.draw_tower_radius(screen)
        enemies = self.get_enemies_in_range(self.settings.enemy_sprites)
        if enemies:
            self.shoot(enemies)

    def draw_tower_radius(self, screen):
        if self.is_clicked:
            screen.blit(get_tower_range_surface(self.range), (self.rect.centerx - self.range,
                                                              self.rect.centery - self.range))

    def get_enemies_in_range(self, group: pg.sprite.Group):
        origin = self.rect.center
        # get enemies in tower range
        return [enemy for enemy in group if
                hypot(origin[0] - enemy.rect.center[0], origin[1] - enemy.rect.center[1]) <= self.range]

    def shoot(self, enemies):
        pass

    def clicked(self):
        self.is_clicked = not self.is_clicked


class NormalTower(BaseTower):
    def __init__(self, settings, top_left, size):
        super(NormalTower, self).__init__(settings, top_left, size)
        image = TOWER_IMAGES['normal_tower']
        self.image = pg.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left

        self.range = settings.normal_tower_range
        self.attack_speed = settings.normal_tower_attack_speed
        self.damage = settings.normal_tower_damage

    def shoot(self, enemies):
        if not self.attack_cooldown:
            if self.hit_order == 'first':
                enemy = enemies[0]
            elif self.hit_order == 'last':
                enemy = enemies[-1]
            else:
                # get closest enemy to tower
                enemy = min(enemies, key=lambda obj: abs(hypot(*self.rect.center) - hypot(*enemy.rect.center)))
            Bullet(self.rect.center, enemy, self.damage, self.settings)
            self.attack_cooldown = self.attack_speed


class FastTower(BaseTower):
    def __init__(self, settings, top_left, size):
        super(FastTower, self).__init__(settings, top_left, size)
        image = TOWER_IMAGES['normal_tower']
        self.image = pg.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left

        self.range = settings.fast_tower_range
        self.attack_speed = settings.fast_tower_attack_speed
        self.damage = settings.fast_tower_damage

    def shoot(self, enemies):
        if not self.attack_cooldown:
            if self.hit_order == 'first':
                enemy = enemies[0]
            elif self.hit_order == 'last':
                enemy = enemies[-1]
            else:
                # get closest enemy to tower
                enemy = min(enemies, key=lambda obj: abs(hypot(*self.rect.center) - hypot(*enemy.rect.center)))
            Bullet(self.rect.center, enemy, self.damage, self.settings)
            self.attack_cooldown = self.attack_speed


class SplitTower(BaseTower):
    def __init__(self, settings, top_left, size):
        super(SplitTower, self).__init__(settings, top_left, size)
        image = TOWER_IMAGES['normal_tower']
        self.image = pg.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left

        self.range = settings.split_tower_range
        self.attack_speed = settings.split_tower_attack_speed
        self.damage = settings.split_tower_damage
        self.targets = settings.split_tower_targets

    def shoot(self, enemies: pg.sprite.Group):
        if not self.attack_cooldown:
            for enemy in sample(enemies, k=min(len(enemies), self.targets)):
                Bullet(self.rect.center, enemy, self.damage, self.settings)
            self.attack_cooldown = self.attack_speed

