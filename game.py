import pygame
import random

from data.alien import Alien
from data.bullet import Bullet
from data.explosion import Explosion
from data.image_loader import *
from data.enemy_wave import *
from data.button import *

# <editor-fold desc="game stuff">
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
ROWS, COLUMNS = 10, 20
ROW_SIZE = screen.get_height() / ROWS
COLUMN_SIZE = screen.get_width() / COLUMNS
pygame.display.set_caption('Space Invaders')
#icon = pygame.image.load('images/icon.png').convert_alpha()
#pygame.display.set_icon(icon)
clock = pygame.time.Clock()
delta_time = 0
running = True
game_running = False
pause_menu = False
main_menu = True
options_menu = False
how_to_play = False
# </editor-fold>

# <editor-fold desc="player position">
player_x = 10
player_y = 8
# </editor-fold>

# <editor-fold desc="mouse stuff">
mouse_clicked = False
# </editor-fold>

# <editor-fold desc="menu pics">
cog_wheel_icon = cog_wheel_pic()
screen_background = background_pic()
screen_background = pygame.transform.scale(screen_background, (screen.get_width(), screen.get_height()))
# </editor-fold>

# <editor-fold desc="animations">
rocket_animation_list = rocket_animation()
rocket_animation_counter = 0

green_alien_animation_list = green_alien_animation()
last_green_alien_updated = -1
green_alien_update_increment = 500
green_alien_counter = 0

bullet_animation_list = bullet_animation()
bullet_animation_counter = 0

explosion_animation_list =explosion_animation()
explosion_list = []
explosion_animation_increment = 100
# </editor-fold>

# <editor-fold desc="bullets">
bullets = []
bullet_movement_increment = 100 #milliseconds
shoot_increment = 200
last_shot_fired = -1
# </editor-fold>

# <editor-fold desc="aliens">
last_alien_movement_update = pygame.time.get_ticks()
last_alien_spawn_update = pygame.time.get_ticks()
alien_movement_increment = 1000 #milliseconds
alien_spawn_increment = 3000 #milliseconds
aliens = []
# </editor-fold>

# <editor-fold desc="enemy waves">
enemy_waves = init_enemy_waves()
# </editor-fold>

while running:
    screen.blit(screen_background, (0,0))

    if game_running:
        now = pygame.time.get_ticks()

        cog_rect = pygame.Rect(0,0,COLUMN_SIZE,ROW_SIZE)
        screen.blit(cog_wheel_icon, (0,0))
        cog_collision = cog_rect.collidepoint(pygame.mouse.get_pos())
        if mouse_clicked and cog_collision:
            game_running = False
            pause_menu = True

        if now > last_alien_spawn_update + alien_spawn_increment:
            last_alien_spawn_update = pygame.time.get_ticks()
            aliens.append(Alien("green", 5, 1, "right"))

        for alien in aliens[:]:
            alien.rect = pygame.Rect(alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE, COLUMN_SIZE, ROW_SIZE)
            match alien.name:
                case "green":
                    screen.blit(green_alien_animation_list[green_alien_counter],
                                (alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE))
                    if now > last_green_alien_updated + green_alien_update_increment:
                        last_green_alien_updated = pygame.time.get_ticks()
                        green_alien_counter = (green_alien_counter + 1) % len(green_alien_animation_list)

        if now > last_alien_movement_update + alien_movement_increment:
            last_alien_movement_update = pygame.time.get_ticks()
            for alien in aliens[:]:
                if alien.pos_x < 14 and alien.movement_direction == "right":
                    alien.pos_x += 1
                elif alien.pos_x > 5 and alien.movement_direction == "left":
                    alien.pos_x -= 1
                elif alien.pos_x == 14 and alien.movement_direction == "right":
                    alien.pos_y += 1
                    alien.movement_direction = "left"
                else:
                    alien.pos_y += 1
                    alien.movement_direction = "right"

        for bullet in bullets[:]:
            bullet.rect = pygame.Rect(bullet.pos_x * COLUMN_SIZE, bullet.pos_y * ROW_SIZE, COLUMN_SIZE, ROW_SIZE)
            screen.blit(bullet_animation_list[bullet.animation_counter],
                        (bullet.pos_x * COLUMN_SIZE, bullet.pos_y * ROW_SIZE))
            bullet.animation_counter = (bullet_animation_counter + 1) % len(bullet_animation_list)

            if now > bullet.last_bullet_movement_update + bullet_movement_increment:
                if bullet.pos_y == 0:
                    bullets.remove(bullet)
                else:
                    bullet.last_bullet_movement_update = pygame.time.get_ticks()
                    bullet.pos_y -= 1

            for alien in aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    explosion_list.append(Explosion(alien.pos_x, alien.pos_y))
                    if bullet in bullets: bullets.remove(bullet)
                    if alien in aliens: aliens.remove(alien)

        for explosion in explosion_list[:]:
            screen.blit(explosion_animation_list[explosion.animation_counter],
                        (explosion.pos_x * COLUMN_SIZE, explosion.pos_y * ROW_SIZE))
            if now > explosion.animation_last_update + explosion_animation_increment:
                explosion.animation_last_update = pygame.time.get_ticks()
                explosion.animation_counter += 1
                if explosion.animation_counter > 3: explosion_list.remove(explosion)

        screen.blit(rocket_animation_list[rocket_animation_counter], (player_x * COLUMN_SIZE, player_y * ROW_SIZE))
        rocket_animation_counter += 1
        if rocket_animation_counter == len(rocket_animation_list) - 1: rocket_animation_counter = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and player_x < 14:
                    player_x += 1
                if event.key == pygame.K_a and player_x > 5:
                    player_x -= 1
                if event.key == pygame.K_SPACE:
                    now = pygame.time.get_ticks()
                    if now > last_shot_fired + shoot_increment or last_shot_fired == -1:
                        last_shot_fired = pygame.time.get_ticks()
                        bullets.append(Bullet(player_x, player_y - 1, pygame.time.get_ticks()))
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                    pause_menu = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_clicked = False

        delta_time = clock.tick(60) / 1000
        pygame.display.update()

    if pause_menu:
        screen.fill((55, 50, 55))
        pauseMenuRect = pygame.Rect(4 * COLUMN_SIZE,2 * ROW_SIZE,12 * COLUMN_SIZE,6 * ROW_SIZE)

        exitGameRect = pygame.Rect(12 * COLUMN_SIZE,6 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (200, 75, 75), exitGameRect)

        continueGameRect = pygame.Rect(6 * COLUMN_SIZE,4 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (75, 200, 75), continueGameRect)

        optionsRect = pygame.Rect(6 * COLUMN_SIZE,6 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (150, 150, 150), optionsRect)

        mainMenuRect = pygame.Rect(12 * COLUMN_SIZE,4 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (220, 220, 220), mainMenuRect)

        if exitGameRect.collidepoint(pygame.mouse.get_pos()) and mouse_clicked:
            pause_menu = False
            running = False

        if continueGameRect.collidepoint(pygame.mouse.get_pos()) and mouse_clicked:
            pause_menu = False
            game_running = True

        if optionsRect.collidepoint(pygame.mouse.get_pos()) and mouse_clicked:
            pause_menu = False
            options_menu = True

        if mainMenuRect.collidepoint(pygame.mouse.get_pos()) and mouse_clicked:
            pause_menu = False
            main_menu = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_clicked = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = True
                    pause_menu = False

        delta_time = clock.tick(60) / 1000
        pygame.display.update(pauseMenuRect)

    if options_menu:
        pass

    if main_menu:

        start_game_rect = pygame.Rect(9 * COLUMN_SIZE, 4 * ROW_SIZE, 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        pygame.draw.rect(screen, (75, 200, 75), start_game_rect)

        how_to_play_rect = pygame.Rect(9 * COLUMN_SIZE, 5.5 * ROW_SIZE, 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        pygame.draw.rect(screen, (150, 75, 150), how_to_play_rect)

        optionsRect = pygame.Rect(9 * COLUMN_SIZE,7 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (150, 150, 150), optionsRect)

        exit_game_rect = pygame.Rect(9 * COLUMN_SIZE, 8.5 * ROW_SIZE, 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        pygame.draw.rect(screen, (200, 75, 75), exit_game_rect)

        if start_game_rect.collidepoint(pygame.mouse.get_pos()) and mouse_clicked:
            main_menu = False
            game_running = True

        if how_to_play_rect.collidepoint(pygame.mouse.get_pos()) and mouse_clicked:
            main_menu = False
            how_to_play = True

        if optionsRect.collidepoint(pygame.mouse.get_pos()) and mouse_clicked:
            main_menu = False
            options_menu = True

        if exit_game_rect.collidepoint(pygame.mouse.get_pos()) and mouse_clicked:
            main_menu = False
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_clicked = False

        delta_time = clock.tick(60) / 1000
        pygame.display.update()

    if how_to_play:
        pass

pygame.quit()

