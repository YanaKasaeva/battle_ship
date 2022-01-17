import pygame
import sys
import os

SPACE_PRESS_COUNT = 0


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

    def on_click(self, cell_coords, n, side):
        if side == '':  # если сторона не указана, значит эта функция была вызвана не для построения корабля,
            # а для его выбора, поэтому строю как обычно
            self.board[cell_coords[1]][cell_coords[0]] = 1 - self.board[cell_coords[1]][cell_coords[0]]
        elif side == 'right':  # проверка на то, в какую сторону строится корабль.
            # в данном случае был выбран горизонтальный корабль, поэтому строиться он будет направо
            for i in range(n):  # запуская цикл, который идет от кол-ва палуб
                self.board[cell_coords[1]][cell_coords[0] + i] = 1  # закрашиваю клетку.
                # переменная i здесь для закрашивания соседних клеток,
                # то есть сначала, допустим, закрасится клетка 5, потом 5 + 1, потом 5 + 2 и тд
        elif side == 'down':  # абсолютно аналогично, только тут я не дописала. разве что изменяться будет y, а не x
            for i in range(n):
                self.board[cell_coords[1]][cell_coords[0]] = 1

    def get_click(self, mouse_pos, n, side):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell, n, side)  # передаю в on_click позицию клика на самом поле, количество палуб и сторону


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill((0, 0, 0))
    font_1 = pygame.font.Font(None, 50)
    font_2 = pygame.font.Font(None, 32)
    rules = ['Морской бой', 'Нажмите "пробел", чтобы начать игру',
             'Игра рассчитана на двух человек, играющих на одном устройстве', 'Первым расставляет корабли PLAYER 1',
             'Чтобы это сделать, нужно нажать на корабль,', 'а затем на клетки поля, куда вы хотите его поместить',
             'Чтобы зафиксировать местоположение корабля, нажмите "W"', 'После расстановки кораблей, нажмите "пробел"',
             'Первым ходит PLAYER 1',
             'Чтобы сделать ход, нажмите на клетку, куда вы хотите выстрелить', 'После победы нажмите "пробел",',
             'чтобы увидеть результаты игры']
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
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 46)
    letters = 'абвгдежзик'  # 'АБВГДЕЖЗИК'
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

    board1 = Board(10, 10)
    board1.set_view(45, 85, 35)
    board2 = Board(10, 10)
    board2.set_view(440, 85, 35)
    board3 = Board(4, 1)
    board3.set_view(140, 495, 35)
    board4 = Board(4, 1)
    board4.set_view(460, 495, 35)

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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] >= 495:  # первая проверка того, на что мы нажали,
                # конкретно тут нажатие на поля с выборами корабликов
                if event.pos[0] <= 400: # проверка того, что мы нажали на поле с выбором горизонтальных корабликов
                    board3.get_click(event.pos, 1, side)  # вызываю функцию get_click,
                    # параметры в данном случае не имеют смысла
                    kol = board3.get_cell(event.pos)[0] + 1  # благодаря функции get_cell получаю длину палубы
                    # так как все кораблики идут слева направо в порядке увеличения размера
                    side = 'right'  # получаю сторону, в которую будет строится кораблик (вниз или направо)
                elif event.pos[0] >= 460:  # здесь все аналогично, только для второго поля,
                    # в котором корабли горизонтальные
                    board4.get_click(event.pos, 1, side)
                    kol = board4.get_cell(event.pos)[0] + 1
                    side = 'down'
                n = 1  # указываю для того, чтоб на поля основные (куда ставим кораблики) можно было
                # нажать только после выбора самого корабля
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] <= 470 and n == 1:  # смотрю, на какое поле
                # нажал пользователь ( в данном случае на поля для, где и будут стоять сами корабли)
                if event.pos[0] <= 430:  # проверяю, что пользователь нажал на левое поле
                    board1.get_click(event.pos, kol, side)  # разрешаю нажатие на клетку, передаю позицию клика мышки,
                    # количество палуб у кораблика и сторону, в которую будут рисоваться палубы
                elif event.pos[0] >= 431:  # проверяю, что пользователь нажал на правое поле
                    board2.get_click(event.pos, kol, side)  # аналогично
                kol = 1  # обнуляю
                side = ''  # обнуляю
                n = 0  # обнуляю
                # далее см. функцию get_click
        board1.render(screen)
        board2.render(screen)
        board3.render(screen)
        board4.render(screen)
        all_sprite.draw(screen)
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
                SPACE_PRESS_COUNT += 1
                main_screen()
        pygame.display.flip()

pygame.quit()