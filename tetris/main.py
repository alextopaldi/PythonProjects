import pygame
from copy import deepcopy
from random import choice

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
#Двумерный массив квадратов
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
#Координаты всех возможных семи фигур, по 4 квадрата каждая
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]
#Массив фигур
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
#Отрисовка частей фигуры
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
#Массив для пометки упавших фигур
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 3000

bg = pygame.image.load('venv/img/img.jpg').convert()
game_bg = pygame.image.load('venv/img/bg.jpg').convert()

main_font = pygame.font.Font('venv/Font/20832.ttf', 65)
font = pygame.font.Font('venv/Font/20832.ttf', 45)

title_tetris = main_font.render('Tetris', True, pygame.Color('white'))
title_score = font.render('score', True, pygame.Color('white'))
title_plus = font.render('+100', True, pygame.Color('Gold'))
title_record = font.render('record', True, pygame.Color('white'))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color = 'Blue'
record = 0
score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

#Проверка на выход за границы
def check_edges():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True
#Цикл самой игры
while True:
    move, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    # Действия для клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move = -1
            elif event.key == pygame.K_RIGHT:
                move = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
    # Перемещение по оси x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += move
        if not check_edges():
            figure = deepcopy(figure_old)
            break
    # Перемещение по оси y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_edges():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure = next_figure
                next_figure = deepcopy(choice(figures))
                anim_limit = 3000
                break
    # Вращение фигуры
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_edges():
                figure = deepcopy(figure_old)
                break
    # Удаление заполненных строк
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            lines += 1
    # Расчет счета
    score += scores[lines]
    # Рисовка сетки
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    #Рисовка предыдущей фигуры
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
    # Рисовка фигур на поле
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
    # Рисовка последующей фигуры
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, color, figure_rect)
    sc.blit(title_tetris, (540, 10))
    sc.blit(title_score, (480, 780))
    sc.blit(title_record, (610, 780))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (480, 840))
    sc.blit(font.render(str(record), True, pygame.Color('gold')), (610, 840))
    # Конец игры
    for i in range(W):
        if field[0][i]:
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            if score>record:
                record = score
            score = 0
            pygame.time.wait(2000)
    pygame.display.flip()
    clock.tick(FPS)