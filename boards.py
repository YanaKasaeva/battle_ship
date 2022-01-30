import pygame
from screen import screen


def boards():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 46)
    letters = 'абвгдежзик'
    letters_x_1 = 12
    letters_x_2 = 408
    letters_y = 88
    for elem in letters:
        text = font.render(elem, True, (255, 255, 255))
        screen.blit(text, (letters_x_1, letters_y))
        screen.blit(text, (letters_x_2, letters_y))
        letters_y += 35
    text = font.render("1  2  3  4  5  6  7  8  9 10", True, (255, 255, 255))
    screen.blit(text, (55, 55))
    screen.blit(text, (450, 55))
    font_names = pygame.font.SysFont('arial', 45)
    name_1 = font_names.render("PLAYER 1", True, (0, 255, 255))
    name_2 = font_names.render("PLAYER 2", True, (0, 255, 255))
    screen.blit(name_1, (55, 5))
    screen.blit(name_2, (450, 5))
