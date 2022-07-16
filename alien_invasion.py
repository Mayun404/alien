import sys
import pygame

import game_function as gf

from settings import Settings
from ship import Ship
from game_stats import GameStats
from pygame.sprite import Group
from button import Button
from scoreboard import ScoreBoard


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption(ai_settings.caption)
    # 创建按钮
    play_button = Button(ai_settings, screen, 'PLAY')
    # 统计游戏的实例 和 计分
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)
    '''创建飞船'''
    ship = Ship(ai_settings, screen)
    '''创建存储子弹的编组'''
    bullets = Group()
    # 创建alien
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        # screen.blit(bgp, (20, 20))
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                        bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
