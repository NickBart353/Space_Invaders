import pygame

def get_sounds():
    return pygame.mixer.Sound("data/sounds/bullet.wav"),pygame.mixer.Sound("data/sounds/explosion2.mp3")

def get_game_over_sound():
    return pygame.mixer.Sound("data/sounds/game_over.wav")

def get_mouse_over_sound():
    return pygame.mixer.Sound("data/sounds/menu_button_hover.wav")