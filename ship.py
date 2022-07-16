import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_setting, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting
        '''加载飞船图像并获取其外接矩形'''
        self.image = pygame.image.load('images/pl.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        '''船在底部中间'''
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # self.center = float(self.rect.centerx)
        self.rect.centerx = float(self.rect.centerx)
        # self.rect.centery = float(self.rect.bottom)
        '''控制左右'''
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.center += self.ai_setting.ship_speed_factor
            self.rect.centerx += self.ai_setting.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            # self.center -= self.ai_setting.ship_speed_factor
            self.rect.centerx -= self.ai_setting.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            # self.center -= self.ai_setting.ship_speed_factor
            self.rect.centery -= self.ai_setting.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.height:
            self.rect.centery += self.ai_setting.ship_speed_factor
        self.rect.centerx = self.rect.centerx
        self.rect.centery = self.rect.centery

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    # 飞船居中
    def center_ship(self):
        # print(self.screen_rect.centerx)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
