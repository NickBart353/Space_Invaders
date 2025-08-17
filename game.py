import pygame
import random

from data.alien import Alien
from data.bullet import Bullet

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

#player stuff
player_x = 10
player_y = 9

#bullets
bullets = []
bullet_movement_increment = 100 #milliseconds
shoot_increment = 200
last_shot_fired = -1

#aliens
last_alien_movement_update = pygame.time.get_ticks()
last_alien_spawn_update = pygame.time.get_ticks()
alien_movement_increment = 1000 #milliseconds
alien_spawn_increment = 300 #milliseconds
aliens = []

while running:
    screen.fill((0,0,0))

    now = pygame.time.get_ticks()
    if now > last_alien_spawn_update + alien_spawn_increment:
        last_alien_spawn_update = pygame.time.get_ticks()
        aliens.append(Alien("green", 5,0, "right"))

    for alien in aliens[:]:
        alien.rect = pygame.Rect(alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE, COLUMN_SIZE, ROW_SIZE)
        pygame.draw.rect(screen, (0, 50, 100),alien.rect)

        if now > last_alien_movement_update + alien_movement_increment:
            last_alien_movement_update = pygame.time.get_ticks()
            if not alien.pos_x == 14 and alien.movement_direction == "right":
                alien.pos_x += 1
            elif not alien.pos_x == 5 and alien.movement_direction == "left":
                alien.pos_x -= 1
            elif alien.pos_x == 14 and alien.movement_direction == "right":
                alien.pos_y += 1
                alien.movement_direction = "left"
            else:
                alien.pos_y += 1
                alien.movement_direction = "right"

    for bullet in bullets[:]:
        bullet.rect = pygame.Rect(bullet.pos_x * COLUMN_SIZE, bullet.pos_y * ROW_SIZE, COLUMN_SIZE, ROW_SIZE)
        pygame.draw.rect(screen, (130, 130, 230),bullet.rect)

        if now > bullet.last_bullet_movement_update + bullet_movement_increment:
            if bullet.pos_y == 0:
                bullets.remove(bullet)
            else:
                bullet.last_bullet_movement_update = pygame.time.get_ticks()
                bullet.pos_y -= 1

        for alien in aliens[:]:
            if bullet.rect.colliderect(alien.rect):
                bullets.remove(bullet)
                aliens.remove(alien)




    pygame.draw.rect(screen, (255,255,255), (player_x*COLUMN_SIZE,player_y*ROW_SIZE,COLUMN_SIZE, ROW_SIZE))

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
                    bullets.append(Bullet(player_x, player_y-1,pygame.time.get_ticks()))

    delta_time = clock.tick(60) / 1000
    pygame.display.update()

pygame.quit()

#        for i in range(COLUMNS//4, COLUMNS-COLUMNS//4):
            #for j in range(0, ROWS):