import pygame
import sys

SPACE_PRESS_COUNT = 0


class Board:
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
        colors = [pygame.Color(0, 0, 0), pygame.Color(0, 255, 0)]
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, (255, 255, 255),
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

    def on_click(self, cell_coords):
        self.board[cell_coords[1]][cell_coords[0]] = 1 - self.board[cell_coords[1]][cell_coords[0]]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


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
    board1.render(screen)
    board2 = Board(10, 10)
    board2.set_view(440, 85, 35)
    board2.render(screen)


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
