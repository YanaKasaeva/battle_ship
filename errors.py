import pygame
from screen import screen


def del_error_f():
    pygame.draw.rect(screen, (0, 0, 0), (0, 555, 800, 50), 0)


def error_place():
    del_error_f()
    font = pygame.font.Font(None, 32)
    text = font.render('Неправильная установка кораблика. Попробуйте снова', True, (255, 255, 255))
    screen.blit(text, (85, 555))


def error_choose():
    del_error_f()
    font = pygame.font.Font(None, 32)
    text = font.render('Вы не выбрали кораблик', True, (255, 255, 255))
    screen.blit(text, (240, 555))


def error_count_ships():
    del_error_f()
    font = pygame.font.Font(None, 32)
    text = font.render('Вы уже использовали все кораблики этого типа. Выберите другой', True, (255, 255, 255))
    screen.blit(text, (40, 555))


def error_wrong_pole():
    del_error_f()
    font = pygame.font.Font(None, 32)
    text = font.render('Вы ставите кораблик не на свое поле', True, (255, 255, 255))
    screen.blit(text, (230, 555))


def error_before_w():
    del_error_f()
    font = pygame.font.Font(None, 32)
    text = font.render('Вы поставили еще не все корабли', True, (255, 255, 255))
    screen.blit(text, (240, 555))


def error_queue():
    font_names = pygame.font.SysFont('arial', 45)
    error = font_names.render("Сейчас ходит другой игрок!", True, (255, 0, 0))
    screen.blit(error, (140, 440))


def del_error_game_window():
    pygame.draw.rect(screen, (0, 0, 0), (140, 440, 580, 60), 0)


def error_same_cell():
    font_names = pygame.font.SysFont('arial', 45)
    error = font_names.render("Вы уже сюда стреляли", True, (255, 0, 0))
    screen.blit(error, (160, 440))