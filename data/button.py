import pygame

def display_and_get_exit_button(column_size, row_size, screen):
    exit_game_rect = pygame.Rect(12 * column_size,6 * row_size,2 * column_size,1 * row_size)
    pygame.draw.rect(screen, (200, 75, 75), exit_game_rect)
    return exit_game_rect

