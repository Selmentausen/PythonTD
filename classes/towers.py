from functions import load_image
from game_functions import get_tower_range_surface
import pygame as pg
from math import hypot
from random import sample


class BaseTower(pg.sprite.Sprite):
    tower_image = [load_image('towers/ArrowTower.png')]

    def __init__(self, settings, top_left, size):
        super(BaseTower, self).__init__(settings.all_sprites, settings.tower_sprites)

        self.image = pg.transform.scale(self.tower_image[0], size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left
        self.settings = settings
        self.is_clicked = False

        self.x, self.y = top_left
        self.range = settings.tower_range[self.__class__.__name__]
        self.damage = settings.tower_damage[self.__class__.__name__]
        self.attack_speed = settings.tower_attack_speed[self.__class__.__name__]
        self.attack_cooldown = 0
        self.hit_order = 'first'

    def update(self, *args, **kwargs) -> None:
        delta_time, screen = kwargs['delta_time'], kwargs['screen']
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
    tower_image = [load_image('towers/normal_tower_lvl1.png'),
                   load_image('towers/normal_tower_lvl2.png'),
                   load_image('towers/normal_tower_lvl3.png')]

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
    tower_image = [load_image('towers/fast_tower_lvl1.png'),
                   load_image('towers/fast_tower_lvl2.png'),
                   load_image('towers/fast_tower_lvl3.png')]

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
    tower_image = [load_image('towers/split_tower_lvl1.png'),
                   load_image('towers/split_tower_lvl2.png'),
                   load_image('towers/split_tower_lvl3.png')]

    def __init__(self, settings, top_left, size):
        super(SplitTower, self).__init__(settings, top_left, size)
        self.targets = settings.split_tower_targets

    def shoot(self, enemies: pg.sprite.Group):
        if not self.attack_cooldown:
            for enemy in sample(enemies, k=min(len(enemies), self.targets)):
                Bullet(self.rect.center, enemy, self.damage, self.settings)
            self.attack_cooldown = self.attack_speed


class Bullet(pg.sprite.Sprite):
    bullet_image = {
        'normal_bullet': load_image('towers/normal_bullet.png'),
        'big_bullet': load_image('towers/big_bullet.png')
    }

    def __init__(self, start, enemy, damage, settings):
        super(Bullet, self).__init__(settings.all_sprites, settings.bullet_sprites)
        self.settings = settings
        self.image = self.bullet_image['big_bullet']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start
        self.speed = settings.bullet_speed
        self.damage = damage
        self.x, self.y = start
        self.enemy = enemy

    def update(self, *args, **kwargs) -> None:
        delta_time = kwargs['delta_time']
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
