import pygame
from screen import screen


def player(n):
    pygame.draw.rect(screen, (0, 0, 0), (225, 500, 270, 100), 0)
    font_names = pygame.font.SysFont('arial', 45)
    if n % 2 == 0:
        name = font_names.render("Player 1", True, (255, 255, 255))
    else:
        name = font_names.render("Player 2", True, (255, 255, 255))
    screen.blit(name, (230, 500))