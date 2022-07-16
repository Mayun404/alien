import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


# 按下按键
def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, aliens):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        # print('right_down')
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
        # print('left_down')
    elif event.key == pygame.K_UP:
        ship.moving_up = True
        # print('up_down')
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
        # print('down_down')
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        record_score(sb)
    elif event.key == pygame.K_r:
        # print('22')
        stats.game_active = False
        pygame.mouse.set_visible(True)
    elif event.key == pygame.K_RETURN:
        # print('11')
        restart_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


# 松开按键
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
        # print('right_up')
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
        # print('left_up')
    if event.key == pygame.K_UP:
        ship.moving_up = False
        # print('up_up')
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
        # print('down_up')


# 检查按钮事件
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            record_score(sb)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                              bullets, mouse_x, mouse_y)


# 更新屏幕
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)
    bgp = pygame.image.load("images/bg.jpg")
    screen.blit(bgp, (0, 0))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()
    # 显示按钮
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


# 删除子弹
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    # 删除子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


# 发射子弹
def fire_bullet(ai_settings, screen, ship, bullets):
    # 发射子弹
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


# 创建外星舰队
def create_fleet(ai_settings, screen, ship, aliens):
    # 外星舰队
    alien = Alien(ai_settings, screen)
    num_aliens_x = get_num_aliens_x(ai_settings, alien.rect.width)
    num_rows = get_num_aliens_rows(ai_settings, ship.rect.height, alien.rect
                                   .height)
    # 创建所有外星人
    for row_num in range(num_rows):
        for alien_num in range(num_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_num, row_num)


# 每行有多少alien
def get_num_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    num_aliens_x = int(available_space_x / (2 * alien_width))
    return num_aliens_x


# 创建外星人
def create_alien(ai_settings, screen, aliens, alien_num, row_num):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = int(20) + alien_width + 2 * alien_width * alien_num
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
    aliens.add(alien)


# 有多少行alien
def get_num_aliens_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    num_rows = int(available_space_y / (2 * alien_height))
    return num_rows


# alien到达边缘
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


# 改变alien方向
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


# 响应相撞
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.pre_ships()
        # 清空子弹和alien
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        # print('cu：' + str(stats.score))
        # print('high：' + str(stats.high_score))
        with open('high.txt', 'w') as f:
            f.write(str(stats.high_score))
        with open('last.txt', 'w') as f:
            f.write(str(stats.score))
        stats.game_active = False
        pygame.mouse.set_visible(True)


# 检查alien是否到底部
def check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        # print('Ship hit!!!')
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    # 检查alien是否到底部
    check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


# 子弹和alien重叠
def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.pre_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除所有子弹，加快
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.pre_level()

        create_fleet(ai_settings, screen, ship, aliens)


# 按下play按钮
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_click and not stats.game_active:
        restart_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


# 重置游戏
def restart_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    # 重置计分牌
    sb.pre_score()
    sb.pre_high_score()
    sb.pre_level()
    sb.pre_ships()
    sb.pre_last_score()

    # 清空alien和子弹
    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


# 检查最高分的诞生
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.pre_high_score()


# 记录最高分
def record_score(sb):
    # print('当前分：')
    # print('最高分：' + str())
    print('bey')
    sys.exit()
