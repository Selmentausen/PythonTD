import pygame as pg
import sys
import os

pg.init()
screen = pg.display.set_mode((1024, 768))
clock = pg.time.Clock()

from classes import towers
from classes.board import Board
from settings import Settings
from functions import load_level
from game_functions import create_background_surface, generate_map_board_list, add_buttons
from game_functions import generate_enemy_waves, add_text_info


def terminate():
    pg.quit()
    sys.exit()


def start_screen(surface):
    running = True
    w, h = surface.get_size()
    background_surface = create_background_surface((w, h))
    title = pg.font.Font(None, 150).render('Python TD', True, pg.Color('White'))
    info_line = pg.font.Font(None, 80).render('Press any key to START', True, pg.Color('White'))
    background_surface.blit(title, (w // 2 - title.get_width() // 2, h * 0.2))
    background_surface.blit(info_line, (w // 2 - info_line.get_width() // 2, h * 0.6))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                running = False
        surface.fill(pg.Color('Black'))
        screen.blit(background_surface, (0, 0))
        pg.display.flip()
        clock.tick()


def menu(surface):
    running = True
    w, h = surface.get_size()
    background_surface = create_background_surface((w, h))
    instructions = ["Press 'ESCAPE' to RETURN", "Press 'R' to RESTART", "Press 'Q' to QUIT"]
    font = pg.font.Font(None, 70)
    for i, line in enumerate(instructions):
        line_surface = font.render(line, True, pg.Color('White'))
        background_surface.blit(line_surface, (w // 2 - line_surface.get_width() // 2, h * (0.3 + 0.1 * i)))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_q:
                    terminate()
                elif event.key == pg.K_r:
                    return 'restart'
        surface.fill(pg.Color('Black'))
        screen.blit(background_surface, (0, 0))
        pg.display.flip()
        clock.tick()


def game_over(surface):
    running = True
    w, h = surface.get_size()
    background_surface = create_background_surface((w, h))
    title = pg.font.Font(None, 150).render('GAME OVER', True, pg.Color('Red'))
    background_surface.blit(title, (w // 2 - title.get_width() // 2, h * 0.2))
    instructions = ["Press 'R' to RESTART", "Press 'Q' to QUIT"]
    font = pg.font.Font(None, 70)
    for i, line in enumerate(instructions):
        line_surface = font.render(line, True, pg.Color('White'))
        background_surface.blit(line_surface, (w // 2 - line_surface.get_width() // 2, h * (0.5 + 0.1 * i)))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    terminate()
                elif event.key == pg.K_r:
                    return 'restart'
        surface.fill(pg.Color('Black'))
        screen.blit(background_surface, (0, 0))
        pg.display.flip()
        clock.tick()


def game_win(surface):
    running = True
    w, h = surface.get_size()
    background_surface = create_background_surface((w, h))
    title = pg.font.Font(None, 150).render('YOU WIN!!!', True, pg.Color('green'))
    background_surface.blit(title, (w // 2 - title.get_width() // 2, h * 0.2))
    instructions = ["Press ANY KEY to QUITE"]
    font = pg.font.Font(None, 70)
    for i, line in enumerate(instructions):
        line_surface = font.render(line, True, pg.Color('White'))
        background_surface.blit(line_surface, (w // 2 - line_surface.get_width() // 2, h * (0.5 + 0.1 * i)))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    terminate()
                elif event.key == pg.K_r:
                    return 'restart'
        surface.fill(pg.Color('Black'))
        screen.blit(background_surface, (0, 0))
        pg.display.flip()
        clock.tick()


def main_loop(level):
    settings = Settings()
    settings.set_screen_sizes(screen.get_size())

    delta_time = clock.tick() / 1000
    board_list = generate_map_board_list(load_level(level), settings)
    map_board = Board(board_list, settings)

    settings.enemy_waves = generate_enemy_waves(load_level(level))

    add_buttons(screen, settings, [towers.NormalTower, towers.FastTower, towers.SplitTower])
    background_surface = create_background_surface(screen.get_size())

    while True:
        events = pg.event.get()
        for event in events.copy():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if menu(screen):
                        return 'restart'
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    settings.selected_tower = None

        if settings.lives <= 0:
            return game_over(screen)
        # if no more waves left and no enemies alive change to next level
        if not settings.enemy_waves and not settings.enemy_sprites.sprites():
            return 'next_level'

        screen.fill(pg.Color('black'))
        screen.blit(background_surface, (0, 0))
        add_text_info(screen, settings)

        map_board.update(events.copy(), screen, placing_tower=settings.selected_tower)
        settings.all_sprites.draw(screen)
        settings.all_sprites.update(delta_time=delta_time, screen=screen, mouse_pos=pg.mouse.get_pos())

        pg.display.flip()
        delta_time = clock.tick(60) / 1000


if __name__ == '__main__':
    start_screen(screen)
    levels = [lvl for lvl in os.listdir('data/maps') if lvl.split('.')[-1] == 'txt']
    current_level = levels.pop(0)
    while True:
        result = main_loop(current_level)
        if result == 'next_level':
            if levels:
                current_level = levels.pop(0)
                continue
            else:
                game_win(screen)
        elif result == 'restart':
            continue
        break
    terminate()
