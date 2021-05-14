from functions import load_image
import pygame as pg
from math import hypot
from random import sample


class BaseTower(pg.sprite.Sprite):
    tower_image = [load_image('towers/ArrowTower.png')]
    radius_image = load_image('towers/tower_radius.png')

    def __init__(self, settings, top_left, size):
        super(BaseTower, self).__init__(settings.all_sprites, settings.tower_sprites)

        self.image = pg.transform.scale(self.tower_image[0], size)
        self.size = size
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = top_left
        self.settings = settings
        self.is_clicked = False

        self.x, self.y = top_left
        self.range = settings.tower_range[self.__class__.__name__]
        self.damage = settings.tower_damage[self.__class__.__name__]
        self.attack_speed = settings.tower_attack_speed[self.__class__.__name__]
        self.attack_cooldown = 0
        self.level = 1
        self.hit_order = 'first'

    def update(self, *args, **kwargs) -> None:
        delta_time, screen = kwargs['delta_time'], kwargs['screen']
        self.attack_cooldown = max(self.attack_cooldown - delta_time, 0)
        if self.is_clicked:
            self.draw_tower_radius(screen)
        enemies = self.get_objects_in_range(self.settings.enemy_sprites)
        if enemies:
            self.shoot(enemies)

    def draw_tower_radius(self, screen):
        img = pg.transform.scale(self.radius_image,
                                 (self.rect.size[0] * (self.range * 2 + 1),
                                  self.rect.size[0] * (self.range * 2 + 1)))
        img.set_alpha(100)
        screen.blit(img, (self.rect.x - self.range * self.rect.size[0], self.rect.y - self.range * self.rect.size[1]))

    def get_objects_in_range(self, group):
        objects = []
        origin = self.rect
        width, height = self.rect.size
        top_left = origin[0] - width * self.range, origin[1] - height * self.range
        bottom_right = origin[0] + width * (self.range + 1), origin[1] + height * (self.range + 1)
        for obj in group:
            if top_left[0] < obj.rect.centerx < bottom_right[0] and top_left[1] < obj.rect.centery < bottom_right[1]:
                objects.append(obj)
        return objects

    def shoot(self, enemies):
        pass

    def clicked(self):
        self.is_clicked = not self.is_clicked

    def upgrade(self):
        if self.level < 3 \
                and self.settings.money >= self.settings.tower_upgrade_cost[self.__class__.__name__][self.level - 1]:
            self.level += 1
            self.image = pg.transform.scale(self.tower_image[self.level - 1], self.size)
            self.upgrade_stats()
            self.settings.money -= self.settings.tower_upgrade_cost[self.__class__.__name__][self.level - 2]

    def upgrade_stats(self):
        pass


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

    def upgrade_stats(self):
        self.damage = int(self.damage * 2)
        self.range = int(self.range * 1.3)


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

    def upgrade_stats(self):
        self.damage = int(self.damage * 1.2)
        self.attack_speed = self.attack_speed * 0.8
        self.range = int(self.range * 1.1)


class SplitTower(BaseTower):
    tower_image = [load_image('towers/split_tower_lvl1.png'),
                   load_image('towers/split_tower_lvl2.png'),
                   load_image('towers/split_tower_lvl3.png')]

    def __init__(self, settings, top_left, size):
        super(SplitTower, self).__init__(settings, top_left, size)
        self.targets = settings.split_tower_targets

    def shoot(self, enemies):
        if not self.attack_cooldown:
            for enemy in sample(enemies, k=min(len(enemies), self.targets)):
                Bullet(self.rect.center, enemy, self.damage, self.settings)
            self.attack_cooldown = self.attack_speed

    def upgrade_stats(self):
        self.targets += 1
        self.damage = int(self.damage * 1.5)
        self.range = int(self.range * 1.2)


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
