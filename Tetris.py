import pygame
import sys
from copy import deepcopy
from random import choice, randrange

WIDTH, HEIGHT = 10, 20;
TILE = 45;
GAME_RES = (WIDTH * TILE, HEIGHT * TILE)
RES = 750, 940

pygame.init()
sc = pygame.display.set_mode(RES)
screen = pygame.Surface(GAME_RES)
pygame.display.set_caption("Tetris")

CLOCK = pygame.time.Clock()
GRID = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WIDTH) for y in range(HEIGHT)]       # Uses [] because we are making a list of Rect

tetrominos_pos = [[(-1,-1),(-2,-1),(0,-1),(1,-1), (0,173,238)], # I
              [(0,-1),(-1,-1),(-1,0),(0,0), (255,241,0)], # O
              [(0,0),(-1,-1),(0,-1),(1,0), (236,27,36)], # Z
              [(0,0),(-1,0),(0,-1),(1,-1), (139,197,63)], # S
              [(0,0),(-1,0),(1,0),(1,-1), (246, 146, 30)], # L
              [(0,0),(-1,-1),(-1,0),(1,0), (27, 116, 187)], # J
              [(0,0),(-1,0),(1,0),(0,-1), (101,45,144)]] # T

tetrominos = [
    [pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in block_pos[:-1]] + [block_pos[-1]]
    for block_pos in tetrominos_pos
]
tetromino_rect = pygame.Rect(0,0, TILE -2, TILE -2)
tetromino = deepcopy(choice(tetrominos))

feild = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

bg = pygame.image.load('img/bg.jpg').convert()
game_bg = pygame.image.load('img/bg2.jpg').convert()


def check_borders():
    if tetromino[i].x < 0 or tetromino[i].x > WIDTH-1:
        return False
    elif tetromino[i].y > HEIGHT -1 or feild[tetromino[i].y][tetromino[i].x]:           # if tetromino is touching bottom OR touching another tetromino that is touching bottom (including the ones bellow that one by chainging the binding feild 2D array ) return false
        return False
    return True

while True:
    dir_x = 0
    rotate = False

    sc.blit(bg, (0,0))
    sc.blit(screen, (20,20))
    screen.blit(game_bg, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dir_x = -1
            elif event.key == pygame.K_RIGHT:
                dir_x = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                anim_limit = 2000
    
    # x movement
    tetromino_old = deepcopy(tetromino)
    for i in range(4):
        tetromino[i].x += dir_x
        if not check_borders():
            tetromino = deepcopy(tetromino_old)
            break

    # y movement
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        tetromino_old = deepcopy(tetromino)
        for i in range(4):
            tetromino[i].y += 1
            if not check_borders():
                for i in range(4):
                    feild[tetromino_old[i].y][tetromino_old[i].x] = tetromino[4]
                tetromino = deepcopy(choice(tetrominos))
                break

    # Rotating
    center = tetromino[0]
    tetromino_old = deepcopy(tetromino)
    if rotate:
        for i in range(4):
            x = tetromino[i].y - center.y
            y = tetromino[i].x - center.x
            tetromino[i].x = center.x - x
            tetromino[i].y = center.y + y
            if not check_borders():
                tetromino = deepcopy(tetromino_old)
                break

    line = HEIGHT - 1
    for row in range(HEIGHT - 1, -1, -1):
        count = 0
        for i in range(WIDTH):
            if feild[row][i]:
                count += 1
            feild[line][i] = feild[row][i]
        if count < WIDTH:
            line -= 1

    # (40,40,40) is color (gray), i_rect is position in GRID, [] is used because we are running this line by making a list and not storing list in a var so no new element is created (could just write it normamly but python is cool like that)
    [pygame.draw.rect(screen, (40,40,40), i_rect, 1) for i_rect in GRID]

    # Drawing Block
    for i in range(4):
        tetromino_rect.x = tetromino[i].x * TILE
        tetromino_rect.y = tetromino[i].y * TILE
        pygame.draw.rect(screen, tetromino[4], tetromino_rect)

    # Drawing Feild (the bottom the tetrominos that is touching bottom)
    for y, row in enumerate(feild):
        for x, col in enumerate(row):
            if col:
                tetromino_rect.x, tetromino_rect.y = x * TILE, y * TILE
                pygame.draw.rect(screen, col, tetromino_rect)

    pygame.display.update()
    CLOCK.tick(60)