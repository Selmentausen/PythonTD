from functions import load_image
import pygame as pg
from math import hypot, atan2, degrees
from random import choice


class BaseTower(pg.sprite.Sprite):
    tower_image = [load_image('towers/ArrowTower.png')]
    radius_image = load_image('towers/tower_radius.png')
    tower_upgrade_sound = pg.mixer.Sound('data/sounds/tower_upgrade.WAV')

    def __init__(self, settings, top_left, size):
        super(BaseTower, self).__init__(settings.all_sprites, settings.tower_sprites)

        self.original_image = pg.transform.scale(self.tower_image[0], size)
        self.image = self.original_image
        self.size = size
        self.top_left = top_left
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
            enemies = self.select_enemy_to_shoot(enemies)
            self.shoot(enemies)

    def rotate_to_shooting_enemy(self, enemy):
        rel_x, rel_y = enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y
        rotation = degrees(atan2(rel_x, rel_y))
        rotated_image = pg.transform.rotate(self.original_image, rotation)
        self.rect = rotated_image.get_rect(center=self.image.get_rect(topleft=self.rect.topleft).center)
        self.image = rotated_image

    def select_enemy_to_shoot(self, enemies) -> object:
        if self.hit_order == 'first':
            enemy = enemies[0]
        elif self.hit_order == 'last':
            enemy = enemies[-1]
        elif self.hit_order == 'closest':
            enemy = min(enemies, key=lambda obj: abs(hypot(*self.rect.center) - hypot(*enemy.rect.center)))
        elif self.hit_order == 'farthest':
            enemy = max(enemies, key=lambda obj: abs(hypot(*self.rect.center) - hypot(*enemy.rect.center)))
        else:
            enemy = choice(enemies)
        self.rotate_to_shooting_enemy(enemy)
        return enemy

    def draw_tower_radius(self, screen):
        img = pg.transform.scale(self.radius_image,
                                 (self.size[0] * (self.range * 2 + 1),
                                  self.size[0] * (self.range * 2 + 1)))
        img.set_alpha(100)
        screen.blit(img, (self.top_left[0] - self.range * self.size[0], self.top_left[1] - self.range * self.size[1]))

    def get_objects_in_range(self, group):
        objects = []
        origin = self.top_left
        width, height = self.size
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
            self.original_image = self.image
            self.upgrade_stats()
            self.tower_upgrade_sound.play()
            self.settings.money -= self.settings.tower_upgrade_cost[self.__class__.__name__][self.level - 2]

    def upgrade_stats(self):
        pass


class NormalTower(BaseTower):
    tower_image = [load_image('towers/normal_tower_lvl1.png'),
                   load_image('towers/normal_tower_lvl2.png'),
                   load_image('towers/normal_tower_lvl3.png')]
    tower_shoot_sound = pg.mixer.Sound('data/sounds/tower_shoot.WAV')

    def shoot(self, enemy):
        if not self.attack_cooldown:
            Bullet(self.rect.center, enemy, self.damage, self.settings)
            self.attack_cooldown = self.attack_speed
            self.tower_shoot_sound.play()

    def upgrade_stats(self):
        self.damage = int(self.damage * 2)
        self.range += 1


class FastTower(BaseTower):
    tower_image = [load_image('towers/fast_tower_lvl1.png'),
                   load_image('towers/fast_tower_lvl2.png'),
                   load_image('towers/fast_tower_lvl3.png')]
    tower_shoot_sound = pg.mixer.Sound('data/sounds/tower_shoot.WAV')

    def shoot(self, enemy):
        if not self.attack_cooldown:
            Bullet(self.rect.center, enemy, self.damage, self.settings)
            self.attack_cooldown = self.attack_speed
            self.tower_shoot_sound.play()

    def upgrade_stats(self):
        self.damage = int(self.damage * 1.2)
        self.attack_speed = self.attack_speed * 0.8


class SplitTower(BaseTower):
    tower_image = [load_image('towers/split_tower_lvl1.png'),
                   load_image('towers/split_tower_lvl2.png'),
                   load_image('towers/split_tower_lvl3.png')]
    tower_shoot_sound = pg.mixer.Sound('data/sounds/split_tower_shoot.WAV')

    def __init__(self, settings, top_left, size):
        super(SplitTower, self).__init__(settings, top_left, size)
        self.targets = settings.split_tower_targets

    def select_enemy_to_shoot(self, enemies) -> object:
        new_enemies = []
        for _ in range(self.targets):
            if not enemies:
                break
            enemy = super(SplitTower, self).select_enemy_to_shoot(enemies)
            enemies.remove(enemy)
            new_enemies.append(enemy)
        self.rotate_to_shooting_enemy(new_enemies[0])
        return new_enemies

    def shoot(self, enemies):
        if not self.attack_cooldown:
            for enemy in enemies:
                Bullet(self.rect.center, enemy, self.damage, self.settings)
            self.attack_cooldown = self.attack_speed
            self.tower_shoot_sound.play()

    def upgrade_stats(self):
        self.targets += 1
        self.damage = int(self.damage * 1.5)
        if self.level == 3:
            self.range += 1


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
