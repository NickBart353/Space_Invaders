import pygame

from data.alien import Alien
from data.bullet import Bullet
from data.explosion import Explosion
from data.image_loader import *
from data.enemy_wave import *
from data.button import *
from data.sound_loader import *
from data.font_loader import *

# <editor-fold desc="game stuff">
pygame.display.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
game_over = False
# </editor-fold>

# <editor-fold desc="player values">
player_x = 10
player_y = 8
player_health = 3
# </editor-fold>

# <editor-fold desc="mouse stuff">
mouse_clicked = False
colliding_with_button = False
# </editor-fold>

# <editor-fold desc="menu pics">
cog_wheel_icon = cog_wheel_pic()
screen_background = background_pic()
screen_background = pygame.transform.scale(screen_background, (screen.get_width(), screen.get_height()))
filled_heart, empty_heart = heart_pics()
logo = logo()
logoDest = [COLUMN_SIZE*10-logo.get_width()//2, ROW_SIZE*3-logo.get_height()//2]
button_list = buttons()
#this is arbitrary and unclean but it works
button_animation_counter_list = [0,0,0,0,0]
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

# <editor-fold desc="sounds">
bullet_sound, explosion_sound = get_sounds()
explosion_sound.set_volume(0.3)
game_over_sound = get_game_over_sound()
mouse_over_sound = get_mouse_over_sound()
# </editor-fold>

# <editor-fold desc="font">
font = get_font()
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
alien_movement_increment = 100 #milliseconds
alien_spawn_increment = 300 #milliseconds
aliens = []
# </editor-fold>

# <editor-fold desc="enemy waves">
enemy_waves = init_enemy_waves()
# </editor-fold>

while running:
    screen.blit(screen_background, (0,0))

    if game_running:
        now = pygame.time.get_ticks()

        match player_health:
            case 3:
                screen.blit(filled_heart, (12 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(filled_heart, (13 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(filled_heart, (14 * COLUMN_SIZE, 0 * ROW_SIZE))
            case 2:
                screen.blit(filled_heart, (12 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(filled_heart, (13 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(empty_heart, (14 * COLUMN_SIZE, 0 * ROW_SIZE))
            case 1:
                screen.blit(filled_heart, (12 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(empty_heart, (13 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(empty_heart, (14 * COLUMN_SIZE, 0 * ROW_SIZE))
            case 0:
                screen.blit(empty_heart, (12 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(empty_heart, (13 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(empty_heart, (14 * COLUMN_SIZE, 0 * ROW_SIZE))

        cog_rect = pygame.Rect(0,0,COLUMN_SIZE,ROW_SIZE)
        screen.blit(cog_wheel_icon, (0,0))
        cog_collision = cog_rect.collidepoint(pygame.mouse.get_pos())

        if cog_collision and not colliding_with_button:
            mouse_over_sound.play()
            colliding_with_button = True
        colliding_with_button = cog_collision

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
            if alien.pos_y == player_y:
                player_health -= 1
                aliens.remove(alien)
                if player_health <= 0:
                    game_over_sound.play()
                    game_running = False
                    game_over = True

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
            bullet.rect = pygame.Rect(bullet.pos_x * COLUMN_SIZE, bullet.pos_y, COLUMN_SIZE, ROW_SIZE)
            screen.blit(bullet_animation_list[bullet.animation_counter],
                                     (bullet.pos_x * COLUMN_SIZE, bullet.pos_y))
            bullet.animation_counter += 1
            if bullet.animation_counter == len(bullet_animation_list): bullet.animation_counter = 0
            if bullet.pos_y <= -1 * ROW_SIZE:
                bullets.remove(bullet)
            bullet.pos_y -= delta_time * 600

            for alien in aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    explosion_list.append(Explosion(alien.pos_x, alien.pos_y))
                    if bullet in bullets: bullets.remove(bullet)
                    if alien in aliens: aliens.remove(alien)
                    explosion_sound.play()

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
                        bullets.append(Bullet(player_x, (player_y - 1)*ROW_SIZE, pygame.time.get_ticks()))
                        bullet_sound.play()
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
        pauseMenuRect = pygame.Rect(4 * COLUMN_SIZE,2 * ROW_SIZE,12 * COLUMN_SIZE,6 * ROW_SIZE)

        exitGameRect = pygame.Rect(12 * COLUMN_SIZE,6 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (200, 75, 75), exitGameRect)
        exit_collision = exitGameRect.collidepoint(pygame.mouse.get_pos())

        continueGameRect = pygame.Rect(6 * COLUMN_SIZE,4 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (75, 200, 75), continueGameRect)
        continue_collision = continueGameRect.collidepoint(pygame.mouse.get_pos())

        optionsRect = pygame.Rect(6 * COLUMN_SIZE,6 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (150, 150, 150), optionsRect)
        option_collision = optionsRect.collidepoint(pygame.mouse.get_pos())

        mainMenuRect = pygame.Rect(12 * COLUMN_SIZE,4 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (220, 220, 220), mainMenuRect)
        main_menu_collision = mainMenuRect.collidepoint(pygame.mouse.get_pos())

        if (exit_collision or continue_collision or option_collision or main_menu_collision) and not colliding_with_button:
            mouse_over_sound.play()
            colliding_with_button = True
        colliding_with_button = (exit_collision or continue_collision or option_collision or main_menu_collision)

        if exit_collision and mouse_clicked:
            pause_menu = False
            running = False

        if continue_collision and mouse_clicked:
            pause_menu = False
            game_running = True

        if option_collision and mouse_clicked:
            pause_menu = False
            options_menu = True

        if main_menu_collision and mouse_clicked:
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

    if game_over:
        screen.fill((55, 50, 55))
        gameOverRect = pygame.Rect(4 * COLUMN_SIZE,2 * ROW_SIZE,12 * COLUMN_SIZE,6 * ROW_SIZE)

        exitGameRect = pygame.Rect(12 * COLUMN_SIZE,6 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (200, 75, 75), exitGameRect)
        exit_collision = exitGameRect.collidepoint(pygame.mouse.get_pos())

        playAgain = pygame.Rect(6 * COLUMN_SIZE,4 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (75, 200, 75), playAgain)
        play_again_collision = playAgain.collidepoint(pygame.mouse.get_pos())

        optionsRect = pygame.Rect(6 * COLUMN_SIZE,6 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (150, 150, 150), optionsRect)
        option_collision = optionsRect.collidepoint(pygame.mouse.get_pos())

        mainMenuRect = pygame.Rect(12 * COLUMN_SIZE,4 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        pygame.draw.rect(screen, (220, 220, 220), mainMenuRect)
        main_menu_collision = mainMenuRect.collidepoint(pygame.mouse.get_pos())

        if (exit_collision or play_again_collision or option_collision or main_menu_collision) and not colliding_with_button:
            mouse_over_sound.play()
            colliding_with_button = True
        colliding_with_button = (exit_collision or play_again_collision or option_collision or main_menu_collision)

        if exit_collision and mouse_clicked:
            game_over = False
            running = False

        if play_again_collision and mouse_clicked:
            game_over = False
            game_running = True
            bullets  = []
            aliens = []
            player_x = 10
            player_health = 3

        if option_collision and mouse_clicked:
            game_over = False
            options_menu = True

        if main_menu_collision and mouse_clicked:
            game_over = False
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
        pygame.display.update(gameOverRect)

    if options_menu:
        pass

    if main_menu:

        transformed_pic = pygame.transform.rotozoom(logo,0,1)
        screen.blit(transformed_pic, (logoDest[0], logoDest[1]))

        start_game_rect = pygame.Rect(9 * COLUMN_SIZE, 4 * ROW_SIZE, 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[0]], (9 * COLUMN_SIZE, 4 * ROW_SIZE))
        start_game_collision = start_game_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(font.render("Play", False, (100,255,100)), (9.3 * COLUMN_SIZE, 4.4 * ROW_SIZE))

        how_to_play_rect = pygame.Rect(9 * COLUMN_SIZE, 5.2 * ROW_SIZE, 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[1]],(9 * COLUMN_SIZE, 5.2 * ROW_SIZE))
        how_to_play_collision = how_to_play_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(font.render("Help", False, (255,255,255)), (9.3 * COLUMN_SIZE, 5.6 * ROW_SIZE))

        optionsRect = pygame.Rect(9 * COLUMN_SIZE,6.4 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[2]],(9 * COLUMN_SIZE, 6.4 * ROW_SIZE))
        options_collision = optionsRect.collidepoint(pygame.mouse.get_pos())
        screen.blit(font.render("Options", False, (255,255,255)), (9.3 * COLUMN_SIZE, 6.8 * ROW_SIZE))

        exit_game_rect = pygame.Rect(9 * COLUMN_SIZE, 7.6 * ROW_SIZE, 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[3]],(9 * COLUMN_SIZE, 7.6 * ROW_SIZE))
        exit_collision = exit_game_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(font.render("Exit", False, (255,100,100)), (9.3 * COLUMN_SIZE, 8.0 * ROW_SIZE))

        if (exit_collision or start_game_collision or options_collision or how_to_play_collision) and not colliding_with_button:
            mouse_over_sound.play()
            colliding_with_button = True
        colliding_with_button = (exit_collision or start_game_collision or options_collision or how_to_play_collision)

        if start_game_collision: button_animation_counter_list[0] = 1
        else: button_animation_counter_list[0] = 0

        if start_game_collision and mouse_clicked:
            main_menu = False
            game_running = True

        if how_to_play_collision: button_animation_counter_list[1] = 1
        else: button_animation_counter_list[1] = 0

        if how_to_play_collision and mouse_clicked:
            main_menu = False
            how_to_play = True

        if options_collision: button_animation_counter_list[2] = 1
        else: button_animation_counter_list[2] = 0

        if options_collision and mouse_clicked:
            main_menu = False
            options_menu = True

        if exit_collision: button_animation_counter_list[3] = 1
        else: button_animation_counter_list[3] = 0

        if exit_collision and mouse_clicked:
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

