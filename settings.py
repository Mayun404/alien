import pygame


class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (193, 210, 240)
        self.caption = 'Alien Invasion'
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # 子弹
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10
        # alien设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 30
        self.fleet_direction = 1  # 右移，-1为左移
        # 加快
        self.speedup_scale = 1.1
        # 得分加大
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        # 计分
        self.alien_points = 100

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print('当前一个alien是' + str(self.alien_points) + '分')
