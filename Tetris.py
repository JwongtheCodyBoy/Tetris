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
tetromino, next_tetromino = deepcopy(choice(tetrominos)), deepcopy(choice(tetrominos))

feild = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

title_font = pygame.font.Font('HANGTHEDJ.ttf', 65)
font = pygame.font.Font('HANGTHEDJ.ttf', 45)
gameOverFont = pygame.font.Font('HANGTHEDJ.ttf', 100)

title_tetris = title_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_HIGH = font.render('High', True, pygame.Color('purple'))
title_RECORD = font.render('Score:', True, pygame.Color('purple'))

GameOverTxt = gameOverFont.render('GAME OVER', True, pygame.Color('firebrick1'))

bg = pygame.image.load('img/bg.jpg').convert()
game_bg = pygame.image.load('img/bg2.jpg').convert()

score, lines = 0, 0
scores = {0:0, 1:100, 2:300, 3:700, 4:1500}


def check_borders():
    if tetromino[i].x < 0 or tetromino[i].x > WIDTH-1:
        return False
    elif tetromino[i].y > HEIGHT -1 or feild[tetromino[i].y][tetromino[i].x]:           # if tetromino is touching bottom OR touching another tetromino that is touching bottom (including the ones bellow that one by chainging the binding feild 2D array ) return false
        return False
    return True

def get_record():
    try:
        with open('record.txt') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record.txt', 'w') as f:
            f.write('0')

def set_record(record, score):
    rec = max(int(record), score)
    with open('record.txt', 'w') as f:
        f.write(str(rec))

death_flag = False
while True:
    record = get_record()
    dir_x = 0
    rotate = False

    sc.blit(bg, (0,0))
    sc.blit(screen, (20,20))
    screen.blit(game_bg, (0,0))

    # Delay for full lines
    for i in range(lines):
        pygame.time.wait(200)

    # Controls
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
    
    if death_flag: continue

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
                tetromino = next_tetromino
                next_tetromino = deepcopy(choice(tetrominos))
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

    # Checking Lines 
    line, lines = HEIGHT - 1, 0
    for row in range(HEIGHT - 1, -1, -1):
        count = 0
        for i in range(WIDTH):
            if feild[row][i]:
                count += 1
            feild[line][i] = feild[row][i]
        if count < WIDTH:
            line -= 1
        else: 
            anim_speed += 3
            lines += 1
    # Compute Score
    score += scores[lines]
     

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

    # Draw next figure
    for i in range(4):
        tetromino_rect.x = next_tetromino[i].x * TILE + 375
        tetromino_rect.y = next_tetromino[i].y * TILE + 185
        pygame.draw.rect(sc, next_tetromino[4], tetromino_rect)

    # Draw Titles
    sc.blit(title_tetris, (475, 20))
    sc.blit(title_score, (535, 780))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 840))
    sc.blit(title_HIGH, (525, 600))
    sc.blit(title_RECORD, (525, 650))

    record = record if int(record) > score else score
    sc.blit(font.render(str(record), True, pygame.Color('gold')), (550, 710))

    # Game Over
    for i in range(WIDTH):
        if feild[0][i]:
            set_record(record,score)
            death_flag = True
            sc.blit(GameOverTxt, (WIDTH * TILE/8, HEIGHT * TILE/2))

    pygame.display.update()
    CLOCK.tick(60)