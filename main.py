import pygame
import sys
import os

SPACE_PRESS_COUNT = 0
W_PRESS_COUNT = 0

matrix_1 = [[0] * 10 for i in range(10)]
matrix_2 = [[0] * 10 for j in range(10)]
RED_FLAG = False
RED_FLAG_POLE = False
P4_COUNT = 1
P3_COUNT = 2
P2_COUNT = 3
P1_COUNT = 4


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не существует')
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for i in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        colors = [pygame.Color(0, 0, 0), pygame.Color(255, 255, 255)]
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, colors[1],
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)
                pygame.draw.rect(screen, colors[self.board[y][x]], (x * self.cell_size + self.left + 1,
                                                                    y * self.cell_size + self.top + 1,
                                                                    self.cell_size - 2, self.cell_size - 2))

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= x < self.width and 0 <= y < self.height:
            return x, y
        return None

    def on_click(self, cell_coords, n, side, pole):
        global P4_COUNT, P3_COUNT, P2_COUNT, P1_COUNT  # переменные показывающие количество возможных кораблей тех или иных палуб
        #  то есть изначально р4 = 1 а после уставноки на поле 4палубного корабля вычитаю один из переменной
        if n == 4:  # решила использовать n чтобы узнать колво палуб у нажатого корабля
            if P4_COUNT == 0:  # если переменная равна 0 то выводится сообещин на экран и кораблик не ставится
                error_count_ships()
            else:
                self.ok_click(cell_coords, n, side, pole)
        elif n == 3:
            if P3_COUNT == 0:
                error_count_ships()
            else:
                self.ok_click(cell_coords, n, side, pole)

        elif n == 2:
            if P2_COUNT == 0:
                error_count_ships()
            else:
                self.ok_click(cell_coords, n, side, pole)

        elif n == 1:
            if P1_COUNT == 0:
                error_count_ships()
            else:
                self.ok_click(cell_coords, n, side, pole)

    def ok_click(self, cell_coords, n, side, pole):
        global RED_FLAG, P4_COUNT, P3_COUNT, P2_COUNT, P1_COUNT
        if pole == 1:
            self.matrix = matrix_1
        else:
            self.matrix = matrix_2

        if side == 'right':  # здесь как раз таки проверяю,
            # на каком поле рисовать(из-за различных матриц, да)
            if cell_coords[0] + n <= 10:
                for i in range(n):
                    if self.matrix[cell_coords[1]][cell_coords[0] + i] == 1 \
                            or self.matrix[cell_coords[1]][cell_coords[0] + i] == 2:
                        RED_FLAG = True
                        error_place()

                if not RED_FLAG:
                    if n == 4:
                        P4_COUNT -= 1
                    if n == 3:
                        P3_COUNT -= 1
                    if n == 2:
                        P2_COUNT -= 1
                    if n == 1:
                        P1_COUNT -= 1

                    for i in range(n):  # строю кораблик заношу с марицу его клетки
                        self.board[cell_coords[1]][cell_coords[0] + i] = 1
                        self.matrix[cell_coords[1]][cell_coords[0] + i] = 1
                        del_error_f()  # очищаю после на случай если до этого были ошибки

                        # далее заношу в матрицу двойки
                        if cell_coords[0] + n <= 9:
                            self.matrix[cell_coords[1]][cell_coords[0] + n] = 2
                            if cell_coords[1] + 1 <= 9:
                                self.matrix[cell_coords[1] + 1][cell_coords[0] + n] = 2
                            if cell_coords[1] - 1 >= 0:
                                self.matrix[cell_coords[1] - 1][cell_coords[0] + n] = 2

                        if cell_coords[0] >= 1:
                            self.matrix[cell_coords[1]][cell_coords[0] - 1] = 2
                            if cell_coords[1] + 1 <= 9:
                                self.matrix[cell_coords[1] + 1][cell_coords[0] - 1] = 2
                            if cell_coords[1] - 1 >= 0:
                                self.matrix[cell_coords[1] - 1][cell_coords[0] - 1] = 2

                        for i in range(n):
                            if cell_coords[1] >= 1:
                                self.matrix[cell_coords[1] - 1][cell_coords[0] + i] = 2
                            if cell_coords[1] + 1 <= 9:
                                self.matrix[cell_coords[1] + 1][cell_coords[0] + i] = 2

            # убираю флаг и для удобства вывожу матрицу
            else:
                error_place()  # если ошибка есть то вывожу оповещение

            RED_FLAG = False
            for elem in matrix_1:
                print(elem)

        elif side == 'down':
            if cell_coords[1] + n <= 10:
                for i in range(n):
                    if self.matrix[cell_coords[1] + i][cell_coords[0]] == 1 \
                            or self.matrix[cell_coords[1] + i][cell_coords[0]] == 2:
                        RED_FLAG = True
                        error_place()

                if not RED_FLAG:
                    if n == 4:
                        P4_COUNT -= 1
                    if n == 3:
                        P3_COUNT -= 1
                    if n == 2:
                        P2_COUNT -= 1
                    if n == 1:
                        P1_COUNT -= 1

                    for i in range(n):
                        self.board[cell_coords[1] + i][cell_coords[0]] = 1
                        self.matrix[cell_coords[1] + i][cell_coords[0]] = 1
                        del_error_f()

                        if cell_coords[1] + n <= 9:
                            self.matrix[cell_coords[1] + n][cell_coords[0]] = 2
                            if cell_coords[0] + 1 <= 9:
                                self.matrix[cell_coords[1] + n][cell_coords[0] + 1] = 2
                            if cell_coords[0] - 1 >= 0:
                                self.matrix[cell_coords[1] + n][cell_coords[0] - 1] = 2

                        if cell_coords[1] >= 1:
                            self.matrix[cell_coords[1] - 1][cell_coords[0]] = 2
                            if cell_coords[0] + 1 <= 9:
                                self.matrix[cell_coords[1] - 1][cell_coords[0] + 1] = 2
                            if cell_coords[0] - 1 >= 0:
                                self.matrix[cell_coords[1] - 1][cell_coords[0] - 1] = 2

                        for i in range(n):
                            if cell_coords[0] >= 1:
                                self.matrix[cell_coords[1] + i][cell_coords[0] - 1] = 2
                            if cell_coords[0] + 1 <= 9:
                                self.matrix[cell_coords[1] + i][cell_coords[0] + 1] = 2

            else:
                error_place()

            RED_FLAG = False
            for elem in matrix_1:
                print(elem)

    def get_click(self, mouse_pos, n, side, pole):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell, n, side,
                          pole)


# класс для того чтобы в матрицу не заносились данные корабликов для выбора
class Board_Choose_Ship(Board):
    def on_click(self, cell_coords, n, side, board):
        self.board[cell_coords[1]][cell_coords[0]] = 1 - self.board[cell_coords[1]][cell_coords[0]]


BOARD1 = Board(10, 10)
BOARD1.set_view(45, 85, 35)
BOARD2 = Board(10, 10)
BOARD2.set_view(440, 85, 35)
BOARD3 = Board_Choose_Ship(4, 1)
BOARD3.set_view(140, 495, 35)
BOARD4 = Board_Choose_Ship(4, 1)
BOARD4.set_view(460, 495, 35)


def del_error_f():
    pygame.draw.rect(screen, (0, 0, 0), (0, 555, 800, 50), 0)


def terminate():
    pygame.quit()
    sys.exit()


def error_place():
    del_error_f()
    font = pygame.font.Font(None, 32)
    text = font.render('Неправильная установка кораблика. Попробуйте снова', True, (255, 255, 255))
    screen.blit(text, (85, 555))


def error_count_ships():
    del_error_f()
    font = pygame.font.Font(None, 32)
    text = font.render('Вы уже использовали все кораблики этого типа. Выберете другой', True, (255, 255, 255))
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


def hide_pole(pole):
    global BOARD1, BOARD2
    if pole == 1:
        BOARD1 = Board(10, 10)
        BOARD1.set_view(45, 85, 35)
    elif pole == 2:
        BOARD2 = Board(10, 10)
        BOARD2.set_view(440, 85, 35)


def start_screen():
    screen.fill((0, 0, 0))
    font_1 = pygame.font.Font(None, 50)
    font_2 = pygame.font.Font(None, 32)
    rules = ['Морской бой',
             'Игра рассчитана на двух человек, играющих на одном устройстве', 'Первым расставляет корабли PLAYER 1',
             'Чтобы это сделать, нужно нажать на корабль,', 'а затем на клетку поля, откуда будет построен кораблик',
             'Чтобы зафиксировать местоположение всех кораблей, нажмите "w"',
             'Тогда корабли будет расставлять PLAYER 2', 'Первым ходит PLAYER 1',
             'Чтобы сделать ход, нажмите на клетку, куда вы хотите выстрелить', 'После победы нажмите "пробел",',
             'чтобы увидеть результаты игры', 'Нажмите "пробел", чтобы начать игру']
    y = 15
    for elem in rules:
        if elem == 'Морской бой':
            text = font_1.render(elem, True, (0, 255, 255))
        else:
            text = font_2.render(elem, True, (255, 255, 255))
        text_x = width // 2 - text.get_width() // 2
        text_y = y
        screen.blit(text, (text_x, text_y))
        y += 50


def main_screen():
    global BOARD1, BOARD2, BOARD3, BOARD4, W_PRESS_COUNT
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

    all_sprite = pygame.sprite.Group()
    ship1 = pygame.sprite.Sprite()
    ship1.image = load_image('small_gor.jpg')
    ship1.rect = ship1.image.get_rect()
    all_sprite.add(ship1)
    ship2 = pygame.sprite.Sprite()
    ship2.image = load_image('mid_gor.jpg')
    ship2.rect = ship2.image.get_rect()
    all_sprite.add(ship2)
    ship3 = pygame.sprite.Sprite()
    ship3.image = load_image('mid_max_gor.jpg')
    ship3.rect = ship3.image.get_rect()
    all_sprite.add(ship3)
    ship4 = pygame.sprite.Sprite()
    ship4.image = load_image('max_gor.jpg')
    ship4.rect = ship4.image.get_rect()
    all_sprite.add(ship4)

    ship1vert = pygame.sprite.Sprite()
    ship1vert.image = load_image('small_vert.jpg')
    ship1vert.rect = ship1vert.image.get_rect()
    all_sprite.add(ship1vert)
    ship2vert = pygame.sprite.Sprite()
    ship2vert.image = load_image('mid_vert.jpg')
    ship2vert.rect = ship2vert.image.get_rect()
    all_sprite.add(ship2vert)
    ship3vert = pygame.sprite.Sprite()
    ship3vert.image = load_image('mid_max_vert.jpg')
    ship3vert.rect = ship3vert.image.get_rect()
    all_sprite.add(ship3vert)
    ship4vert = pygame.sprite.Sprite()
    ship4vert.image = load_image('max_vert.jpg')
    ship4vert.rect = ship4vert.image.get_rect()
    all_sprite.add(ship4vert)

    ship1.rect.x = 143
    ship1.rect.y = 497
    ship2.rect.x = 177
    ship2.rect.y = 497
    ship3.rect.x = 212
    ship3.rect.y = 497
    ship4.rect.x = 247
    ship4.rect.y = 497

    ship1vert.rect.x = 463
    ship1vert.rect.y = 497
    ship2vert.rect.x = 497
    ship2vert.rect.y = 497
    ship3vert.rect.x = 532
    ship3vert.rect.y = 497
    ship4vert.rect.x = 567
    ship4vert.rect.y = 497

    n = 333
    side = ''
    kol = 1
    w_kol = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] >= 495:
                if 140 <= event.pos[0] <= 280:
                    BOARD3.get_click(event.pos, 1, side, 0)
                    kol = BOARD3.get_cell(event.pos)[0] + 1
                    side = 'right'
                elif 460 <= event.pos[0] <= 600:
                    BOARD4.get_click(event.pos, 1, side, 0)
                    kol = BOARD4.get_cell(event.pos)[0] + 1
                    side = 'down'
                n = 1
            global P4_COUNT, P3_COUNT, P2_COUNT, P1_COUNT, RED_FLAG_POLE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                if P4_COUNT == 0 and P3_COUNT == 0 and P2_COUNT == 0 and P1_COUNT == 0 and w_kol == 0:  # функция, чтоб понять, что W нажата,
                    # т.е. для переключения на второе поле
                    P4_COUNT, P3_COUNT, P2_COUNT, P1_COUNT = 1, 2, 3, 4  # возрождаю первоначальные значения для нового поля
                    hide_pole(1)
                    W_PRESS_COUNT = 1  # переменная, которая будет указателем для второго поля, что ему можно активироваться
                    RED_FLAG_POLE = True  # флаг, благодаря которому после передачи в него значения True
                    # первое поле изменять будет нельзя
                    w_kol = 1
                else:
                    error_before_w()
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] <= 470 and n == 1:
                if event.pos[0] <= 430 and not RED_FLAG_POLE:
                    BOARD1.get_click(event.pos, kol, side, 1)  # единички и двойки тут как раз-таки для определения
                    # в функции отрисовки полей (левое или правое участвует в процессе)
                elif event.pos[0] >= 431 and W_PRESS_COUNT == 1:
                    BOARD2.get_click(event.pos, kol, side, 2)
                else:
                    error_wrong_pole()
                kol = 1
                side = ''
                n = 0
        BOARD1.render(screen)
        BOARD2.render(screen)
        BOARD3.render(screen)
        BOARD4.render(screen)
        all_sprite.draw(screen)
        pygame.display.flip()


def main_screen2():
    pass


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Касаева Яна; Цыганова Виктория")
    start_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) and SPACE_PRESS_COUNT == 0:
                SPACE_PRESS_COUNT += 1
                main_screen()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_w) and W_PRESS_COUNT == 2:
                main_screen2()
        pygame.display.flip()

pygame.quit()
