import pygame

def rocket_animation():
    rocket_animation_list = [pygame.image.load("data/animations/rocket/rocket1.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/rocket2.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/rocket3.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/rocket4.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/rocket5.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/rocket6.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/rocket7.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/rocket8.png").convert_alpha()]
    return rocket_animation_list

def green_alien_animation():
    green_alien_animation_list = [pygame.image.load("data/animations/aliens/green_alien1.png").convert_alpha(),
                                  pygame.image.load("data/animations/aliens/green_alien2.png").convert_alpha()]
    return green_alien_animation_list

def bullet_animation():
    bullet_animation_list = [pygame.image.load("data/animations/rocket/bullet1.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/bullet2.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/bullet3.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/bullet4.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/bullet5.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/bullet6.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/bullet7.png").convert_alpha(),
                             pygame.image.load("data/animations/rocket/bullet8.png").convert_alpha()]
    return bullet_animation_list

def explosion_animation():
    explosion_animation_list = [pygame.image.load("data/animations/explosion/explosion1.png").convert_alpha(),
                                pygame.image.load("data/animations/explosion/explosion2.png").convert_alpha(),
                                pygame.image.load("data/animations/explosion/explosion3.png").convert_alpha(),
                                pygame.image.load("data/animations/explosion/explosion4.png").convert_alpha()]
    return  explosion_animation_list

def cog_wheel_pic():
    return pygame.image.load("data/menu/cog_wheel.png").convert_alpha()

def background_pic():
    return pygame.image.load("data/background/star_background.png").convert_alpha()

def heart_pics():
    filled_heart = pygame.image.load("data/menu/heart8.png").convert_alpha()
    empty_heart = pygame.image.load("data/menu/heart7.png").convert_alpha()
    return filled_heart, empty_heart