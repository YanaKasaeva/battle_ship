import pygame
import sys
import os
import random

SPACE_PRESS_COUNT = 0
W_PRESS_COUNT = 0
MOUSE_PRESS_LEFT = 0
MOUSE_PRESS_RIGHT = 0
LEFT_SHIPS = 20
RIGHT_SHIPS = 20
WINNER = ''
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


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(ALL_SPRITE)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 2

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for i in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


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

    def on_click(self, cell_coords, n, side, pole, pos):
        global P4_COUNT, P3_COUNT, P2_COUNT, P1_COUNT, UNCLICK, UP
        UNCLICK = True
        # if UP % 2 == 0:
        # error_choose()
        if CAN:
            if side == 'right':
                BOARD3.on_click('', 0, 0, 0, pos)
            elif side == 'down':
                BOARD4.on_click('', 0, 0, 0, pos)
            if n == 4:
                if P4_COUNT == 0:
                    error_count_ships()
                else:
                    self.ok_click(cell_coords, n, side, pole, pos)
            elif n == 3:
                if P3_COUNT == 0:
                    error_count_ships()
                else:
                    self.ok_click(cell_coords, n, side, pole, pos)
            elif n == 2:
                if P2_COUNT == 0:
                    error_count_ships()
                else:
                    self.ok_click(cell_coords, n, side, pole, pos)
            elif n == 1:
                if P1_COUNT == 0:
                    error_count_ships()
                else:
                    self.ok_click(cell_coords, n, side, pole, pos)
        else:
            pass

    def ok_click(self, cell_coords, n, side, pole, pos):
        global RED_FLAG, P4_COUNT, P3_COUNT, P2_COUNT, P1_COUNT, UNCLICK
        if pole == 1:
            self.matrix = matrix_1
        else:
            self.matrix = matrix_2
        if side == 'right':
            if cell_coords[0] + n <= 10:
                for i in range(n):
                    if self.matrix[cell_coords[1]][cell_coords[0] + i] == 1 \
                            or self.matrix[cell_coords[1]][cell_coords[0] + i] == 2:
                        RED_FLAG = True
                        error_place()

                if not RED_FLAG:
                    UNCLICK = True
                    BOARD3.on_click('', 0, 0, 0, pos)
                    if n == 4:
                        P4_COUNT -= 1
                    if n == 3:
                        P3_COUNT -= 1
                    if n == 2:
                        P2_COUNT -= 1
                    if n == 1:
                        P1_COUNT -= 1

                    for i in range(n):
                        self.board[cell_coords[1]][cell_coords[0] + i] = 1
                        self.matrix[cell_coords[1]][cell_coords[0] + i] = 1
                        del_error_f()

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

            else:
                error_place()

            RED_FLAG = False

        elif side == 'down':
            UNCLICK = True
            if cell_coords[1] + n <= 10:
                for i in range(n):
                    if self.matrix[cell_coords[1] + i][cell_coords[0]] == 1 \
                            or self.matrix[cell_coords[1] + i][cell_coords[0]] == 2:
                        RED_FLAG = True
                        error_place()

                if not RED_FLAG:
                    UNCLICK = True
                    BOARD4.on_click('', 0, 0, 0, pos)
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

    def get_click(self, mouse_pos, n, side, pole, pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell, n, side,
                          pole, pos)

    def fire(self, cell, pole):
        global LEFT_SHIPS, RIGHT_SHIPS, HOD
        if pole == 1:
            self.matrix = matrix_1
        elif pole == 2:
            self.matrix = matrix_2
        if self.matrix[cell[1]][cell[0]] == 4 or self.matrix[cell[1]][cell[0]] == 3:
            error_same_cell()
        elif self.matrix[cell[1]][cell[0]] == 1:
            create_particles(get_coords(cell, pole))
            self.matrix[cell[1]][cell[0]] = 4
            if pole == 1:
                LEFT_SHIPS -= 1
            elif pole == 2:
                RIGHT_SHIPS -= 1
            HOD += 1
        else:
            self.matrix[cell[1]][cell[0]] = 3

    def coor_fire(self, mouse_pos, side):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.fire(cell, side)


class Board_Choose_Ship(Board):

    def on_click(self, cell_coords, n, side, board, pos):
        global UNCLICK, UP, press_count, old, CAN
        if UNCLICK:
            self.board[pos[1]][pos[0]] = 0
            UNCLICK = False
        else:
            self.board[cell_coords[1]][cell_coords[0]] = 1 - self.board[cell_coords[1]][cell_coords[0]]
            if self.board[cell_coords[1]][cell_coords[0]] == 1 and new != old:
                press_count += 1
            if self.board[cell_coords[1]][cell_coords[0]] == 1:
                CAN = True
            else:
                CAN = False
        if press_count >= 2:
            self.board[old[1]][old[0]] = 0
            press_count -= 1


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


def hide_pole(pole):
    global BOARD1, BOARD2
    if pole == 1:
        BOARD1 = Board(10, 10)
        BOARD1.set_view(45, 85, 35)
    elif pole == 2:
        BOARD2 = Board(10, 10)
        BOARD2.set_view(440, 85, 35)


def error_queue():
    font_names = pygame.font.SysFont('arial', 45)
    error = font_names.render("Сейчас ходит другой игрок!", True, (255, 0, 0))
    screen.blit(error, (140, 440))


def del_error_game_window():
    pygame.draw.rect(screen, (0, 0, 0), (140, 440, 580, 60), 0)


def error_same_cell():
    font_names = pygame.font.SysFont('arial', 45)
    error = font_names.render("Вы уже сюда стреляли", True, (255, 0, 0))
    screen.blit(error, (140, 440))


def player(n):
    pygame.draw.rect(screen, (0, 0, 0), (225, 500, 270, 100), 0)
    font_names = pygame.font.SysFont('arial', 45)
    if n % 2 == 0:
        name = font_names.render("Player 1", True, (255, 255, 255))
    else:
        name = font_names.render("Player 2", True, (255, 255, 255))
    screen.blit(name, (230, 500))


BOARD1 = Board(10, 10)
BOARD1.set_view(45, 85, 35)
BOARD2 = Board(10, 10)
BOARD2.set_view(440, 85, 35)
BOARD3 = Board_Choose_Ship(4, 1)
BOARD3.set_view(140, 495, 35)
BOARD4 = Board_Choose_Ship(4, 1)
BOARD4.set_view(460, 495, 35)


def start_screen():
    screen.fill((0, 0, 0))
    font_1 = pygame.font.Font(None, 50)
    font_2 = pygame.font.Font(None, 32)
    rules = ['Морской бой',
             '- Игра рассчитана на двух человек, играющих на одном устройстве', '- Первым расставляет корабли PLAYER 1',
             '- Чтобы это сделать, нужно нажать на корабль,', 'а затем на клетку поля, откуда будет построен кораблик',
             '- Чтобы зафиксировать местоположение всех кораблей, нажмите "w"',
             '- Тогда корабли будет расставлять PLAYER 2', '- Первым ходит PLAYER 1',
             '- Чтобы сделать ход, нажмите на клетку, куда вы хотите выстрелить',
             '- Вы сразу перейдете на окно результатов,',
             'когда кто-то из игроков победит', '- Нажмите "пробел", чтобы начать игру']
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


def main_screen():
    global BOARD1, BOARD2, BOARD3, BOARD4, W_PRESS_COUNT, ALL_SPRITE, old, new
    boards()

    ship1 = pygame.sprite.Sprite()
    ship1.image = load_image('small_gor.jpg')
    ship1.rect = ship1.image.get_rect()
    ALL_SPRITE.add(ship1)
    ship2 = pygame.sprite.Sprite()
    ship2.image = load_image('mid_gor.jpg')
    ship2.rect = ship2.image.get_rect()
    ALL_SPRITE.add(ship2)
    ship3 = pygame.sprite.Sprite()
    ship3.image = load_image('mid_max_gor.jpg')
    ship3.rect = ship3.image.get_rect()
    ALL_SPRITE.add(ship3)
    ship4 = pygame.sprite.Sprite()
    ship4.image = load_image('max_gor.jpg')
    ship4.rect = ship4.image.get_rect()
    ALL_SPRITE.add(ship4)

    ship1vert = pygame.sprite.Sprite()
    ship1vert.image = load_image('small_vert.jpg')
    ship1vert.rect = ship1vert.image.get_rect()
    ALL_SPRITE.add(ship1vert)
    ship2vert = pygame.sprite.Sprite()
    ship2vert.image = load_image('mid_vert.jpg')
    ship2vert.rect = ship2vert.image.get_rect()
    ALL_SPRITE.add(ship2vert)
    ship3vert = pygame.sprite.Sprite()
    ship3vert.image = load_image('mid_max_vert.jpg')
    ship3vert.rect = ship3vert.image.get_rect()
    ALL_SPRITE.add(ship3vert)
    ship4vert = pygame.sprite.Sprite()
    ship4vert.image = load_image('max_vert.jpg')
    ship4vert.rect = ship4vert.image.get_rect()
    ALL_SPRITE.add(ship4vert)

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

    pos = ''
    n = 333
    side = ''
    kol = 1
    w_kol = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            old = new
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] >= 495:
                if 140 <= event.pos[0] <= 280 and 495 <= event.pos[1] <= 530:
                    new = BOARD3.get_cell(event.pos)
                    BOARD3.get_click(event.pos, 1, side, 0, pos)
                    cell = BOARD3.get_cell(event.pos)
                    if cell is None:
                        pass
                    else:
                        kol = cell[0] + 1
                    side = 'right'
                    pos = BOARD3.get_cell(event.pos)
                elif 460 <= event.pos[0] <= 600 and 495 <= event.pos[1] <= 530:
                    new = BOARD4.get_cell(event.pos)
                    BOARD4.get_click(event.pos, 1, side, 0, pos)
                    cell = BOARD4.get_cell(event.pos)
                    if cell is None:
                        pass
                    else:
                        kol = cell[0] + 1
                    side = 'down'
                    pos = BOARD4.get_cell(event.pos)
                n = 1
            global P4_COUNT, P3_COUNT, P2_COUNT, P1_COUNT, RED_FLAG_POLE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                if P4_COUNT == 0 and P3_COUNT == 0 and P2_COUNT == 0 and P1_COUNT == 0 and w_kol == 0:
                    P4_COUNT, P3_COUNT, P2_COUNT, P1_COUNT = 1, 2, 3, 4
                    hide_pole(1)
                    W_PRESS_COUNT = 1
                    RED_FLAG_POLE = True
                    w_kol = 1
                elif P4_COUNT == 0 and P3_COUNT == 0 and P2_COUNT == 0 and P1_COUNT == 0 and w_kol == 1:
                    del_error_f()
                    hide_pole(2)
                    W_PRESS_COUNT = 2
                    game_window()
                else:
                    error_before_w()
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] <= 470 and n == 1:
                if event.pos[0] <= 430 and not RED_FLAG_POLE:
                    BOARD1.get_click(event.pos, kol, side, 1, pos)
                elif event.pos[0] >= 431 and W_PRESS_COUNT == 1:
                    BOARD2.get_click(event.pos, kol, side, 2, pos)
                else:
                    error_wrong_pole()
                kol = 1
                side = ''
                n = 0
        BOARD1.render(screen)
        BOARD2.render(screen)
        BOARD3.render(screen)
        BOARD4.render(screen)
        ALL_SPRITE.draw(screen)
        pygame.display.flip()


def game_window():
    screen.fill((0, 0, 0))
    global BOARD1, BOARD2, BOARD3, BOARD4, W_PRESS_COUNT
    boards()
    font_names = pygame.font.SysFont('arial', 45)
    hod = font_names.render("Ходит:", True, (255, 255, 255))
    screen.blit(hod, (55, 500))

    global MOUSE_PRESS_LEFT, MOUSE_PRESS_RIGHT, WINNER, HOD
    player(HOD)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            player(HOD)
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.pos[0] <= 430 and HOD % 2 != 0:
                    HOD += 1
                    MOUSE_PRESS_RIGHT += 1
                    BOARD1.coor_fire(event.pos, 1)
                    del_error_game_window()
                elif event.pos[0] <= 430 and HOD % 2 == 0:
                    error_queue()

                if event.pos[0] >= 431 and HOD % 2 == 0:
                    HOD += 1
                    MOUSE_PRESS_LEFT += 1
                    BOARD2.coor_fire(event.pos, 2)
                    del_error_game_window()
                elif event.pos[0] >= 431 and HOD % 2 != 0:
                    error_queue()

            if LEFT_SHIPS == 0:
                hod = MOUSE_PRESS_RIGHT
                WINNER = 'Player 2'
                end_window()
            elif RIGHT_SHIPS == 0:
                hod = MOUSE_PRESS_LEFT
                WINNER = 'Player 1'
                end_window()

        BOARD1.render(screen)
        for i in range(10):
            for j in range(10):
                if matrix_1[i][j] == 3:
                    draw_point_unsuccess((j, i), 1)
                elif matrix_1[i][j] == 4:
                    draw_point_success((j, i), 1)

        BOARD2.render(screen)
        for i in range(10):
            for j in range(10):
                if matrix_2[i][j] == 3:
                    draw_point_unsuccess((j, i), 2)
                if matrix_2[i][j] == 4:
                    draw_point_success((j, i), 2)

        pygame.display.flip()


def end_window():
    global WINNER, MOUSE_PRESS_LEFT, MOUSE_PRESS_RIGHT
    screen.fill((0, 0, 0))
    font_1 = pygame.font.Font(None, 50)
    font_2 = pygame.font.Font(None, 32)
    results = ['Результаты игры',
               f'Победил: {WINNER}',
               f'Всего было сделано ходов: ',
               f'- Первым игроком: {MOUSE_PRESS_RIGHT}',
               f'- Вторым игроком: {MOUSE_PRESS_LEFT}']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            y = 15
            for elem in results:
                if elem == 'Результаты игры':
                    text = font_1.render(elem, True, (0, 255, 255))
                else:
                    text = font_2.render(elem, True, (255, 255, 255))
                text_x = width // 2 - text.get_width() // 2
                text_y = y
                screen.blit(text, (text_x, text_y))
                y += 50

        pygame.display.flip()


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
                SPACE_PRESS_COUNT = 1
                main_screen()
        pygame.display.flip()

pygame.quit()
