from functions import load_image
from game_functions import get_tower_range_surface
import pygame as pg
from math import hypot
from .enemies import EnemyBase

TOWER_IMAGES = {
    'ArrowTower': load_image('towers/ArrowTower.png')
}

BULLET_IMAGES = {
    'normal_bullet': load_image('towers/normal_bullet.png'),
    'big_bullet': load_image('towers/big_bullet.png')
}


class BaseTower(pg.sprite.Sprite):
    def __init__(self, settings, top_left, size, *parent_groups):
        super(BaseTower, self).__init__(*parent_groups)
        self.image = pg.transform.scale(TOWER_IMAGES['ArrowTower'], size)
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

    def update(self, delta_time, enemies, screen) -> None:
        self.attack_cooldown = max(self.attack_cooldown - delta_time, 0)
        self.hit_objects_in_range(enemies)
        self.draw_tower_radius(screen)

    def draw_tower_radius(self, screen):
        if self.is_clicked:
            screen.blit(get_tower_range_surface(self.range), (self.rect.centerx - self.range,
                                                              self.rect.centery - self.range))

    def hit_objects_in_range(self, group: pg.sprite.Group):
        origin = self.rect.center
        # get enemies in tower range
        enemies = [enemy for enemy in group if
                   hypot(origin[0] - enemy.rect.center[0], origin[1] - enemy.rect.center[1]) <= self.range]
        if enemies and not self.attack_cooldown:
            if self.hit_order == 'first':
                enemy = enemies[0]
            elif self.hit_order == 'last':
                enemy = enemies[-1]
            else:
                # get closest enemy to tower
                enemy = min(enemies, key=lambda obj: abs(hypot(*self.rect.center) - hypot(*enemy.rect.center)))
            print(f'Hit {enemy.__class__.__name__} for {self.damage}. It has {enemy.hp - self.damage} hp left')
            enemy.hit(self.damage)
            self.attack_cooldown = self.attack_speed

    def clicked(self):
        self.is_clicked = not self.is_clicked


class ArrowTower(BaseTower):
    def __init__(self, settings, top_left, size, *parent_groups):
        super(ArrowTower, self).__init__(settings, top_left, size, *parent_groups)
        image = TOWER_IMAGES['ArrowTower']
        self.image = pg.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left

        self.range = settings.arrow_tower_range
        self.attack_speed = settings.arrow_tower_attack_speed
        self.damage = settings.arrow_tower_damage
