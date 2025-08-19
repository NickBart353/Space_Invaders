import pygame
import random

from data.alien import Alien
from data.bullet import Bullet
from data.explosion import Explosion

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
print(COLUMN_SIZE,ROW_SIZE)

#player stuff
player_x = 10
player_y = 9

#animations
rocket_animation_list = [pygame.image.load("data/animations/rocket/rocket1.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/rocket2.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/rocket3.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/rocket4.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/rocket5.png").convert_alpha(),
                        pygame.image.load("data/animations/rocket/rocket6.png").convert_alpha(),
                        pygame.image.load("data/animations/rocket/rocket7.png").convert_alpha(),
                        pygame.image.load("data/animations/rocket/rocket8.png").convert_alpha()]
rocket_animation_counter = 0

green_alien_animation_list = [pygame.image.load("data/animations/aliens/green_alien1.png").convert_alpha(),
                              pygame.image.load("data/animations/aliens/green_alien2.png").convert_alpha()]
last_green_alien_updated = -1
green_alien_update_increment = 500
green_alien_counter = 0

bullet_animation_list = [pygame.image.load("data/animations/rocket/bullet1.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/bullet2.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/bullet3.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/bullet4.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/bullet5.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/bullet6.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/bullet7.png").convert_alpha(),
                         pygame.image.load("data/animations/rocket/bullet8.png").convert_alpha()]
bullet_animation_counter = 0

explosion_animation_list = [pygame.image.load("data/animations/explosion/explosion1.png").convert_alpha(),
                         pygame.image.load("data/animations/explosion/explosion2.png").convert_alpha(),
                         pygame.image.load("data/animations/explosion/explosion3.png").convert_alpha(),
                         pygame.image.load("data/animations/explosion/explosion4.png").convert_alpha()]
explosion_list = []
explosion_animation_increment = 100

#bullets
bullets = []
bullet_movement_increment = 100 #milliseconds
shoot_increment = 200
last_shot_fired = -1

#aliens
last_alien_movement_update = pygame.time.get_ticks()
last_alien_spawn_update = pygame.time.get_ticks()
alien_movement_increment = 1000 #milliseconds
alien_spawn_increment = 3000 #milliseconds
aliens = []

while running:
    screen.fill((0,0,0))

    now = pygame.time.get_ticks()
    if now > last_alien_spawn_update + alien_spawn_increment:
        last_alien_spawn_update = pygame.time.get_ticks()
        aliens.append(Alien("green", 5,0, "right"))

    for alien in aliens[:]:
        alien.rect = pygame.Rect(alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE, COLUMN_SIZE, ROW_SIZE)
        match alien.name:
            case "green":
                screen.blit(green_alien_animation_list[green_alien_counter], (alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE))
                if now > last_green_alien_updated + green_alien_update_increment:
                    last_green_alien_updated = pygame.time.get_ticks()
                    green_alien_counter = (green_alien_counter + 1) % len(green_alien_animation_list)

    if now > last_alien_movement_update + alien_movement_increment:
        last_alien_movement_update = pygame.time.get_ticks()
        for alien in aliens[:]:
            if alien.pos_x < 14 and alien.movement_direction == "right":
                alien.pos_x += 1
            elif  alien.pos_x > 5 and alien.movement_direction == "left":
                alien.pos_x -= 1
            elif alien.pos_x == 14 and alien.movement_direction == "right":
                alien.pos_y += 1
                alien.movement_direction = "left"
            else:
                alien.pos_y += 1
                alien.movement_direction = "right"

    for bullet in bullets[:]:
        bullet.rect = pygame.Rect(bullet.pos_x * COLUMN_SIZE, bullet.pos_y * ROW_SIZE, COLUMN_SIZE, ROW_SIZE)
        screen.blit(bullet_animation_list[bullet.animation_counter], (bullet.pos_x * COLUMN_SIZE, bullet.pos_y * ROW_SIZE))
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

    screen.blit(rocket_animation_list[rocket_animation_counter], (player_x*COLUMN_SIZE,player_y*ROW_SIZE))
    rocket_animation_counter += 1
    if rocket_animation_counter == len(rocket_animation_list)-1: rocket_animation_counter = 0

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