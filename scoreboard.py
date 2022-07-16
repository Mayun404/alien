import pygame.font
from pygame.sprite import Group

from ship import Ship


class ScoreBoard:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示字体
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 32)

        self.pre_high_score()
        self.pre_level()
        self.pre_score()
        self.pre_ships()
        self.pre_last_score()

    # 当前得分
    def pre_score(self):
        rounded_score = int(round(self.stats.score, -1))
        # score_str = str(self.stats.score)
        score_str = "{:,}".format(rounded_score)
        score_str = 'current: ' + score_str
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.level_rect.right + 20
        self.score_rect.top = self.level_rect.top
        # print(rounded_score)

    # 显示分数
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.last_score_image, self.last_score_rect)
        self.ships.draw(self.screen)

    # 最高分
    def pre_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = '{:,}'.format(high_score)
        high_score_str = 'best: ' + high_score_str
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                                                 self.ai_settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 5
        self.high_score_rect.top = 5
        # print('high')

    # 当前等级
    def pre_level(self):
        self.level_image = self.font.render(str('level: ' + str(self.stats.level)), True, self.text_color,
                                            self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.screen_rect.centerx - 100
        self.level_rect.top = self.screen_rect.top + 25

    # 剩余飞船
    def pre_ships(self):
        self.ships = Group()
        for ship_num in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_num * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    # 上局得分
    def pre_last_score(self):
        last_score = int(round(self.stats.last_score, -1))
        last_score_str = '{:,}'.format(last_score)
        last_score_str = 'last score: ' + last_score_str
        self.last_score_image = self.font.render(last_score_str, True, self.text_color,
                                                 self.ai_settings.bg_color)

        self.last_score_rect = self.last_score_image.get_rect()
        self.last_score_rect.right = self.high_score_rect.right
        self.last_score_rect.top = self.high_score_rect.bottom + 5
