import pygame

def transform_image(image_path):
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return pygame.transform.scale(pygame.image.load(image_path),
                           (screen.get_width() // 20, screen.get_height() // 10)).convert_alpha()

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

def weak_alien_animation():
    return [transform_image("data/animations/aliens/weak_alien1.png"),
            transform_image("data/animations/aliens/weak_alien2.png")]

def medium_green_alien_animation():
    return [transform_image("data/animations/aliens/medium_alien_green1.png"),
            transform_image("data/animations/aliens/medium_alien_green2.png")]

def medium_purp_alien_animation():
    return [transform_image("data/animations/aliens/medium_alien_purp1.png"),
            transform_image("data/animations/aliens/medium_alien_purp2.png")]

def strong_green_alien_animation():
    return [transform_image("data/animations/aliens/strong_alien_green1.png"),
            transform_image("data/animations/aliens/strong_alien_green2.png")]

def strong_purp_alien_animation():
    return [transform_image("data/animations/aliens/strong_alien_purp1.png"),
            transform_image("data/animations/aliens/strong_alien_purp2.png")]

def strong_red_alien_animation():
    return [transform_image("data/animations/aliens/strong_alien_red1.png"),
            transform_image("data/animations/aliens/strong_alien_red2.png")]

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

def logo():
    return pygame.image.load("data/background/logo.png").convert_alpha()

def buttons():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return [pygame.transform.scale(pygame.image.load("data/menu/newer_button1.png").convert_alpha(), (screen.get_width()//20*2.7, screen.get_height()//10*1)).convert_alpha(),
            pygame.transform.scale(pygame.image.load("data/menu/newer_button2.png").convert_alpha(), (screen.get_width()//20*2.7, screen.get_height()//10*1)).convert_alpha(),]

def score_border():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return pygame.transform.scale(pygame.image.load("data/menu/newer_button1.png").convert_alpha(),
                                   (screen.get_width() // 20 * 5, screen.get_height() // 10 * 0.7)).convert_alpha()

def ufo():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return [pygame.transform.scale(pygame.image.load("data/menu/ufo1.png"),(screen.get_width()//20*1.2, screen.get_height()//10*1)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("data/menu/ufo2.png"),(screen.get_width()//20*1.2, screen.get_height()//10*1)).convert_alpha()]

def help_background():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return pygame.transform.scale(pygame.image.load("data/menu/newer_button1.png").convert_alpha(), (screen.get_width()//20*22, screen.get_height()//10*10)).convert_alpha()