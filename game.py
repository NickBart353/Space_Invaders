import pygame

from data.alien import Alien
from data.bullet import Bullet
from data.explosion import Explosion
from data.image_loader import *
from data.enemy_wave import *
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
where_did_i_access_options_from = ""
score = 0
score_border = score_border()
# </editor-fold>

# <editor-fold desc="player values">
player_x = 10
player_y = 8
player_health = 3
shooting = False
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

weak_list = weak_alien_animation()
medium_green_list = medium_green_alien_animation()
medium_purple_list = medium_purp_alien_animation()
strong_green_list = strong_green_alien_animation()
strong_purp_list = strong_purp_alien_animation()
strong_red_list = strong_red_alien_animation()

last_alien_movement_update = -1
alien_animation_increment = 500
alien_animation_counter = 0
last_alien_animation_updated = -1

bullet_animation_list = bullet_animation()
bullet_animation_counter = 0

explosion_animation_list =explosion_animation()
explosion_list = []
explosion_animation_increment = 100

ufo_animation_list = ufo()
ufo_animation_counter = 0
ufo_animation_increment = 500
ufo_animation_last_updated = -1
# </editor-fold>

# <editor-fold desc="sounds">
bullet_sound, explosion_sound = get_sounds()
explosion_sound.set_volume(0.3)
game_over_sound = get_game_over_sound()
mouse_over_sound = get_mouse_over_sound()
# </editor-fold>

# <editor-fold desc="font">
menu_button_font = get_menu_button_font()
score_text_font = get_score_text_font()
enemy_wave_font = get_enemy_wave_font()
menu_headline_font = get_menu_headline_font()
text_font = get_text_font()
# </editor-fold>

# <editor-fold desc="bullets">
bullets = []
bullet_movement_increment = 100 #milliseconds
shoot_increment = 200
last_shot_fired = -1
# </editor-fold>

# <editor-fold desc="aliens">
aliens = []
last_alien_spawn_update = -1
# </editor-fold>

# <editor-fold desc="enemy waves">
enemy_waves = init_enemy_waves()
enemy_wave_counter = 0
enemies_spawned = 0
next_wave_animation_played = False
wave_completed_animation_played = True
# </editor-fold>

while running:
    screen.blit(screen_background, (0,0))

    if game_running:
        now = pygame.time.get_ticks()

        match player_health:
            case 3:
                screen.blit(filled_heart, (11 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(filled_heart, (12 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(filled_heart, (13 * COLUMN_SIZE, 0 * ROW_SIZE))
            case 2:
                screen.blit(filled_heart, (11 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(filled_heart, (12 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(empty_heart, (13 * COLUMN_SIZE, 0 * ROW_SIZE))
            case 1:
                screen.blit(filled_heart, (11 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(empty_heart, (12 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(empty_heart, (13 * COLUMN_SIZE, 0 * ROW_SIZE))
            case 0:
                screen.blit(empty_heart, (11 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(empty_heart, (12 * COLUMN_SIZE, 0 * ROW_SIZE))
                screen.blit(empty_heart, (13 * COLUMN_SIZE, 0 * ROW_SIZE))

        screen.blit(score_border, (6 * COLUMN_SIZE, 0 * ROW_SIZE))
        screen.blit(score_text_font.render(f'{score:08}', False, (255,255,255)),(7 * COLUMN_SIZE, 0.15 * ROW_SIZE))

        screen.blit(ufo_animation_list[ufo_animation_counter], (5 * COLUMN_SIZE, 0 * ROW_SIZE))
        if now > ufo_animation_last_updated + ufo_animation_increment:
            ufo_animation_last_updated = now
            ufo_animation_counter = (ufo_animation_counter + 1) % len(ufo_animation_list)

        cog_rect = pygame.Rect(14*COLUMN_SIZE,0,COLUMN_SIZE,ROW_SIZE)
        screen.blit(cog_wheel_icon, (14*COLUMN_SIZE,0))
        cog_collision = cog_rect.collidepoint(pygame.mouse.get_pos())

        if cog_collision and not colliding_with_button:
            mouse_over_sound.play()
            colliding_with_button = True
        colliding_with_button = cog_collision

        screen.blit(rocket_animation_list[rocket_animation_counter], (player_x * COLUMN_SIZE, player_y * ROW_SIZE))
        rocket_animation_counter += 1
        if rocket_animation_counter == len(rocket_animation_list) - 1: rocket_animation_counter = 0

        if not next_wave_animation_played:
            pygame.display.update()
            start = pygame.time.get_ticks()
            second_counter_last_updated = pygame.time.get_ticks()
            animation_time = 3000
            second_counter = 3
            while True:
                screen.blit(screen_background, (0, 0))
                wave_no = enemy_waves[enemy_wave_counter].wave_number + 1
                wave_text_color = pygame.Color((255, 255, 255))
                if wave_no == 7:
                    wave_no = "HAAHAHAHAHAHAHAHAHAHAAHA"
                    wave_text_color = pygame.Color((255, 75, 100))
                screen.blit(enemy_wave_font.render("Wave {}".format(wave_no), False, wave_text_color), (9 * COLUMN_SIZE, 4 * ROW_SIZE))
                screen.blit(enemy_wave_font.render("{}".format(second_counter), False,(255, 255, 255)), (10 * COLUMN_SIZE, 5 * ROW_SIZE))
                if pygame.time.get_ticks() - second_counter_last_updated > 1000:
                    second_counter_last_updated = pygame.time.get_ticks()
                    second_counter -= 1
                pygame.display.update(9 * COLUMN_SIZE, 4 * ROW_SIZE,12 * COLUMN_SIZE, 2 * ROW_SIZE)

                if pygame.time.get_ticks() - start > animation_time:
                    break
            next_wave_animation_played = True

        if mouse_clicked and cog_collision:
            game_running = False
            pause_menu = True

        if (now > last_alien_spawn_update + enemy_waves[enemy_wave_counter].alien_spawn_speed) and enemies_spawned < enemy_waves[enemy_wave_counter].alien_amount:
            last_alien_spawn_update = pygame.time.get_ticks()
            match enemy_waves[enemy_wave_counter].alien_health:
                case 3:
                    alien_type = "strong"
                case 2:
                    alien_type = "medium"
                case 1:
                    alien_type = "weak"
                case _:
                    alien_type = "weak"
            aliens.append(Alien(alien_type, 5, 1,enemy_waves[enemy_wave_counter].alien_health, "right"))
            enemies_spawned += 1

        if now > last_alien_animation_updated + alien_animation_increment:
            last_alien_animation_updated = pygame.time.get_ticks()
            alien_animation_counter = (alien_animation_counter + 1) % 2

        for alien in aliens[:]:
            alien.rect = pygame.Rect(alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE, COLUMN_SIZE, ROW_SIZE)
            match alien.name:
                case "weak":
                    screen.blit(weak_list[alien_animation_counter],(alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE))
                case "medium":
                    match alien.health:
                        case 2:
                            screen.blit(medium_purple_list[alien_animation_counter],(alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE))
                        case 1:
                            screen.blit(medium_green_list[alien_animation_counter],(alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE))
                case "strong":
                    match alien.health:
                        case 3:
                            screen.blit(strong_red_list[alien_animation_counter],(alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE))
                        case 2:
                            screen.blit(strong_purp_list[alien_animation_counter],(alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE))
                        case 1:
                            screen.blit(strong_green_list[alien_animation_counter],(alien.pos_x * COLUMN_SIZE, alien.pos_y * ROW_SIZE))

            if alien.pos_y == player_y:
                player_health -= 1
                aliens.remove(alien)
                if player_health <= 0:
                    game_over_sound.play()
                    aliens = []
                    bullets = []
                    explosion_list = []
                    player_x = 10
                    player_health = 3
                    enemies_spawned = 0
                    next_wave_animation_played = False
                    game_running = False
                    game_over = True

        if now > last_alien_movement_update + enemy_waves[enemy_wave_counter].alien_movement_speed:
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

        if shooting:
            now = pygame.time.get_ticks()
            if now > last_shot_fired + shoot_increment or last_shot_fired == -1:
                last_shot_fired = pygame.time.get_ticks()
                bullets.append(Bullet(player_x, (player_y - 1)*ROW_SIZE, pygame.time.get_ticks()))
                bullet_sound.play()


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
                    alien.health -= 1
                    explosion_sound.play()
                    if bullet in bullets: bullets.remove(bullet)
                    if alien.health <= 0:
                        if alien in aliens: aliens.remove(alien)
                        score += 1

        for explosion in explosion_list[:]:
            screen.blit(explosion_animation_list[explosion.animation_counter],
                        (explosion.pos_x * COLUMN_SIZE, explosion.pos_y * ROW_SIZE))
            if now > explosion.animation_last_update + explosion_animation_increment:
                explosion.animation_last_update = pygame.time.get_ticks()
                explosion.animation_counter += 1
                if explosion.animation_counter > 3: explosion_list.remove(explosion)

        if (enemy_waves[enemy_wave_counter].alien_amount <= enemies_spawned) and len(aliens) == 0:
            next_wave_animation_played = False
            enemy_wave_counter += 1
            enemies_spawned = 0
            bullets = []
            explosion_list = []
            if not player_health == 3: player_health += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and player_x < 14:
                    player_x += 1
                if event.key == pygame.K_a and player_x > 5:
                    player_x -= 1
                if event.key == pygame.K_SPACE:
                    shooting = True
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                    pause_menu = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    shooting = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_clicked = False

        delta_time = clock.tick(60) / 1000
        pygame.display.update()

    if pause_menu:
        screen.blit(menu_headline_font.render("-- Game paused --", False, (100, 150 , 255)),(7.5 * COLUMN_SIZE, 2 * ROW_SIZE))

        pauseMenuRect = pygame.Rect(4 * COLUMN_SIZE,2 * ROW_SIZE,12 * COLUMN_SIZE,6 * ROW_SIZE)
        continue_pos = [7 * COLUMN_SIZE, 3 * ROW_SIZE]
        options_pos = [7 * COLUMN_SIZE, 5 * ROW_SIZE]
        home_pos = [11 * COLUMN_SIZE, 3 * ROW_SIZE]
        exit_pos = [11 * COLUMN_SIZE, 5 * ROW_SIZE]

        continue_game_rect = pygame.Rect(continue_pos[0],continue_pos[1], 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[0]], (continue_pos[0],continue_pos[1]))
        start_game_collision = continue_game_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Resume", False, (100,255,100)), (continue_pos[0]+ 0.3*COLUMN_SIZE,continue_pos[1]+0.4*ROW_SIZE))

        optionsRect = pygame.Rect(options_pos[0],options_pos[1],2 * COLUMN_SIZE,1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[2]],(options_pos[0],options_pos[1]))
        options_collision = optionsRect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Options", False, (255,255,255)), (options_pos[0]+ 0.3*COLUMN_SIZE,options_pos[1]+0.4*ROW_SIZE))

        home_rect = pygame.Rect(home_pos[0],home_pos[1], 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[1]],(home_pos[0],home_pos[1]))
        home_collision = home_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Home", False, (255,255,255)), (home_pos[0]+ 0.3*COLUMN_SIZE,home_pos[1]+0.4*ROW_SIZE))

        exit_game_rect = pygame.Rect(exit_pos[0],exit_pos[1], 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[3]],(exit_pos[0],exit_pos[1]))
        exit_collision = exit_game_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Exit", False, (255,100,100)), (exit_pos[0]+ 0.3*COLUMN_SIZE,exit_pos[1]+0.4*ROW_SIZE))

        if (exit_collision or start_game_collision or options_collision or home_collision) and not colliding_with_button:
            mouse_over_sound.play()
            colliding_with_button = True
        colliding_with_button = (exit_collision or start_game_collision or options_collision or home_collision)

        if start_game_collision: button_animation_counter_list[0] = 1
        else: button_animation_counter_list[0] = 0

        if start_game_collision and mouse_clicked:
            pause_menu = False
            game_running = True

        if home_collision: button_animation_counter_list[1] = 1
        else: button_animation_counter_list[1] = 0

        if home_collision and mouse_clicked:
            aliens = []
            bullets = []
            explosion_list = []
            player_x = 10
            player_health = 3
            enemies_spawned = 0
            next_wave_animation_played = False
            pause_menu = False
            main_menu = True

        if options_collision: button_animation_counter_list[2] = 1
        else: button_animation_counter_list[2] = 0

        if options_collision and mouse_clicked:
            where_did_i_access_options_from = "pause"
            pause_menu = False
            options_menu = True

        if exit_collision: button_animation_counter_list[3] = 1
        else: button_animation_counter_list[3] = 0

        if exit_collision and mouse_clicked:
            pause_menu = False
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = True
                    pause_menu = False

        delta_time = clock.tick(60) / 1000
        pygame.display.update(pauseMenuRect)

    if game_over:
        screen.blit(menu_headline_font.render("-- Game Over --", False, (255, 50 , 100)),(7.8 * COLUMN_SIZE, 2 * ROW_SIZE))

        gameOverRect = pygame.Rect(4 * COLUMN_SIZE,2 * ROW_SIZE,12 * COLUMN_SIZE,6 * ROW_SIZE)
        again_pos = [7 * COLUMN_SIZE, 3 * ROW_SIZE]
        options_pos = [7 * COLUMN_SIZE, 5 * ROW_SIZE]
        home_pos = [11 * COLUMN_SIZE, 3 * ROW_SIZE]
        exit_pos = [11 * COLUMN_SIZE, 5 * ROW_SIZE]

        again_game_rect = pygame.Rect(again_pos[0],again_pos[1], 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[0]], (again_pos[0],again_pos[1]))
        again_collision = again_game_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Retry", False, (100,255,100)), (again_pos[0]+ 0.3*COLUMN_SIZE,again_pos[1]+0.4*ROW_SIZE))

        optionsRect = pygame.Rect(options_pos[0],options_pos[1],2 * COLUMN_SIZE,1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[2]],(options_pos[0],options_pos[1]))
        options_collision = optionsRect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Options", False, (255,255,255)), (options_pos[0]+ 0.3*COLUMN_SIZE,options_pos[1]+0.4*ROW_SIZE))

        home_rect = pygame.Rect(home_pos[0],home_pos[1], 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[1]],(home_pos[0],home_pos[1]))
        home_collision = home_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Home", False, (255,255,255)), (home_pos[0]+ 0.3*COLUMN_SIZE,home_pos[1]+0.4*ROW_SIZE))

        exit_game_rect = pygame.Rect(exit_pos[0],exit_pos[1], 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[3]],(exit_pos[0],exit_pos[1]))
        exit_collision = exit_game_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Exit", False, (255,100,100)), (exit_pos[0]+ 0.3*COLUMN_SIZE,exit_pos[1]+0.4*ROW_SIZE))

        if (exit_collision or again_collision or options_collision or home_collision) and not colliding_with_button:
            mouse_over_sound.play()
            colliding_with_button = True
        colliding_with_button = (exit_collision or again_collision or options_collision or home_collision)

        if again_collision: button_animation_counter_list[0] = 1
        else: button_animation_counter_list[0] = 0

        if again_collision and mouse_clicked:
            game_over = False
            game_running = True

        if home_collision: button_animation_counter_list[1] = 1
        else: button_animation_counter_list[1] = 0

        if home_collision and mouse_clicked:
            game_over = False
            main_menu = True

        if options_collision: button_animation_counter_list[2] = 1
        else: button_animation_counter_list[2] = 0

        if options_collision and mouse_clicked:
            where_did_i_access_options_from = "game_over"
            game_over = False
            options_menu = True

        if exit_collision: button_animation_counter_list[3] = 1
        else: button_animation_counter_list[3] = 0

        if exit_collision and mouse_clicked:
            game_over = False
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = True
                    pause_menu = False

        delta_time = clock.tick(60) / 1000
        pygame.display.update(gameOverRect)

    if options_menu:
        transformed_pic = pygame.transform.rotozoom(logo,0,1)
        screen.blit(transformed_pic, (logoDest[0], logoDest[1]))

        back_dest = [2 * COLUMN_SIZE, 8 * ROW_SIZE]

        back_rect = pygame.Rect(back_dest[0],back_dest[1], 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[3]],(back_dest[0],back_dest[1]))
        back_collision = back_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Back", False, (255,255,255)), (back_dest[0] +0.3 * COLUMN_SIZE,back_dest[1] +0.4 * ROW_SIZE))

        #options
        #volume slider
        #fullscreen or not
        #resolution
        #keybinds???? maybe later

        if back_collision and not colliding_with_button:
            mouse_over_sound.play()
            colliding_with_button = True
        colliding_with_button = back_collision

        if back_collision: button_animation_counter_list[3] = 1
        else: button_animation_counter_list[3] = 0

        if back_collision and mouse_clicked:
            match where_did_i_access_options_from:
                case "game_over":
                    game_over = True
                case "pause":
                    pause_menu = True
                case "home":
                    main_menu = True
            options_menu = False

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

    if main_menu:

        transformed_pic = pygame.transform.rotozoom(logo,0,1)
        screen.blit(transformed_pic, (logoDest[0], logoDest[1]))

        start_game_rect = pygame.Rect(9 * COLUMN_SIZE, 4 * ROW_SIZE, 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[0]], (9 * COLUMN_SIZE, 4 * ROW_SIZE))
        start_game_collision = start_game_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Play", False, (100,255,100)), (9.3 * COLUMN_SIZE, 4.4 * ROW_SIZE))

        how_to_play_rect = pygame.Rect(9 * COLUMN_SIZE, 5.2 * ROW_SIZE, 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[1]],(9 * COLUMN_SIZE, 5.2 * ROW_SIZE))
        how_to_play_collision = how_to_play_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Help", False, (255,255,255)), (9.3 * COLUMN_SIZE, 5.6 * ROW_SIZE))

        optionsRect = pygame.Rect(9 * COLUMN_SIZE,6.4 * ROW_SIZE,2 * COLUMN_SIZE,1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[2]],(9 * COLUMN_SIZE, 6.4 * ROW_SIZE))
        options_collision = optionsRect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Options", False, (255,255,255)), (9.3 * COLUMN_SIZE, 6.8 * ROW_SIZE))

        exit_game_rect = pygame.Rect(9 * COLUMN_SIZE, 7.6 * ROW_SIZE, 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[3]],(9 * COLUMN_SIZE, 7.6 * ROW_SIZE))
        exit_collision = exit_game_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Exit", False, (255,100,100)), (9.3 * COLUMN_SIZE, 8.0 * ROW_SIZE))

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
            where_did_i_access_options_from = "home"
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
        #transformed_pic = pygame.transform.rotozoom(logo,0,1)
        #screen.blit(transformed_pic, (logoDest[0], logoDest[1]))

        back_dest = [2 * COLUMN_SIZE, 8 * ROW_SIZE]

        back_rect = pygame.Rect(back_dest[0],back_dest[1], 2 * COLUMN_SIZE, 1 * ROW_SIZE)
        screen.blit(button_list[button_animation_counter_list[3]],(back_dest[0],back_dest[1]))
        back_collision = back_rect.collidepoint(pygame.mouse.get_pos())
        screen.blit(menu_button_font.render("Back", False, (255,255,255)), (back_dest[0] +0.3 * COLUMN_SIZE,back_dest[1] +0.4 * ROW_SIZE))

        #content
        #How to play:
        #you play a rocket, trying to defend earth from aliens
        #shoot to kill aliens, complete waves, get high score
        #movement a left - d right, spacebar shoot
        #aliens have health indicated by color
        #survive as long as possible
        #if aliens reach earth 3 times you lose, represented by your hearts
        #on completing a wave you get 1 heart back, cant go above 3 hearts
        #your highscore gets tracked, good luck beating your friends!
        headline_dest = [6.3 * COLUMN_SIZE, 2 * ROW_SIZE]
        first_line_dest = [1 * COLUMN_SIZE, 3 * ROW_SIZE]
        second_line_dest = [1 * COLUMN_SIZE, 3.5 * ROW_SIZE]
        third_line_dest = [1 * COLUMN_SIZE, 4 * ROW_SIZE]
        fourth_line_dest = [1 * COLUMN_SIZE, 4.5 * ROW_SIZE]
        fifth_line_dest = [1 * COLUMN_SIZE, 5 * ROW_SIZE]
        sixth_line_dest = [1 * COLUMN_SIZE, 5.5 * ROW_SIZE]
        seventh_line_dest = [1 * COLUMN_SIZE, 6 * ROW_SIZE]

        screen.blit(menu_headline_font.render("How to play Space Invaders!", False, (255, 255, 255)),(headline_dest[0], headline_dest[1]))

        screen.blit(text_font.render("You play a rocket, trying to defend earth from aliens!", False, (255, 255, 255)),(first_line_dest[0], first_line_dest[1]))
        screen.blit(text_font.render("Shoot to kill aliens, complete waves, get a high score!", False, (255, 255, 255)),(second_line_dest[0], second_line_dest[1]))
        screen.blit(text_font.render("Movement: a to move left - d to move right, hold spacebar shoot!", False, (255, 255, 255)), (third_line_dest[0], third_line_dest[1]))
        screen.blit(text_font.render("Aliens have health indicated by color:", False, (255, 255, 255)), (fourth_line_dest[0], fourth_line_dest[1]))
        screen.blit(text_font.render("If aliens reach earth 3 times you lose", False, (255, 255, 255)), (fifth_line_dest[0], fifth_line_dest[1]))
        screen.blit(text_font.render("On completing a wave you get 1 heart back, you can't go above 3 hearts", False, (255, 255, 255)), (sixth_line_dest[0], sixth_line_dest[1]))
        screen.blit(text_font.render("Your highscore gets tracked, good luck beating your friends!", False, (255, 255, 255)), (seventh_line_dest[0], seventh_line_dest[1]))

        screen.blit(weak_list[0], (15.8 * COLUMN_SIZE, 3 * ROW_SIZE))
        screen.blit(explosion_animation_list[0], (16 * COLUMN_SIZE, 3 * ROW_SIZE))
        screen.blit(bullet_animation_list[0], (16 * COLUMN_SIZE, 4 * ROW_SIZE))
        screen.blit(bullet_animation_list[1], (16 * COLUMN_SIZE, 5 * ROW_SIZE))
        screen.blit(rocket_animation_list[0], (16 * COLUMN_SIZE, 6 * ROW_SIZE))

        screen.blit(filled_heart, (15 * COLUMN_SIZE, 7 * ROW_SIZE))
        screen.blit(filled_heart, (16 * COLUMN_SIZE, 7 * ROW_SIZE))
        screen.blit(empty_heart, (17 * COLUMN_SIZE, 7 * ROW_SIZE))

        screen.blit(strong_red_list[0], (8 * COLUMN_SIZE, 4.3 * ROW_SIZE))
        screen.blit(strong_purp_list[0], (9 * COLUMN_SIZE, 4.3 * ROW_SIZE))
        screen.blit(strong_green_list[0], (10 * COLUMN_SIZE, 4.3 * ROW_SIZE))



        if back_collision and not colliding_with_button:
            mouse_over_sound.play()
            colliding_with_button = True
        colliding_with_button = back_collision

        if back_collision: button_animation_counter_list[3] = 1
        else: button_animation_counter_list[3] = 0

        if back_collision and mouse_clicked:
            how_to_play = False
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

        delta_time = clock.tick(60) / 1000
        pygame.display.update()

pygame.quit()

