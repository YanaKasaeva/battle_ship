import pygame


SPACE_PRESS_COUNT = 0
W_PRESS_COUNT = 0
MOUSE_PRESS_LEFT = 0
MOUSE_PRESS_RIGHT = 0
LEFT_SHIPS = 20
RIGHT_SHIPS = 20
HOD = 0
press_count = 0
old, new = 0, 0
UP = 0

matrix_1 = [[0] * 10 for i in range(10)]
matrix_2 = [[0] * 10 for j in range(10)]
colors_point = [pygame.Color(255, 0, 0), pygame.Color(255, 255, 255)]

RED_FLAG = False
RED_FLAG_POLE = False
UNCLICK = False
CAN = False

P4_COUNT = 1
P3_COUNT = 2
P2_COUNT = 3
P1_COUNT = 4

ALL_SPRITE = pygame.sprite.Group()
