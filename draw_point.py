import pygame
from screen import screen
from settings import colors_point


def get_coords(cell, pole):
    if pole == 1:
        x = (cell[0] + 1) * 35 + 45 - 35 // 2
    else:
        x = (cell[0] + 1) * 35 + 440 - 35 // 2
    y = (cell[1] + 1) * 35 + 85 - 35 // 2
    return x, y


def draw_point_success(cell, pole):
    pygame.draw.circle(screen, colors_point[0], get_coords(cell, pole), 5)


def draw_point_unsuccess(cell, pole):
    pygame.draw.circle(screen, colors_point[1], get_coords(cell, pole), 5)
