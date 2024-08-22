import pygame
import sys
from copy import deepcopy

WIDTH, HEIGHT = 10, 18;
TILE = 45;
GAME_RES = (WIDTH * TILE, HEIGHT * TILE)

pygame.init()
screen = pygame.display.set_mode(GAME_RES)
pygame.display.set_caption("Tetris")

CLOCK = pygame.time.Clock()
GRID = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WIDTH) for y in range(HEIGHT)]       # Uses [] because we are making a list of Rect

tetrominos_pos = [[(-1,-1),(-2,-1),(0,-1),(1,-1)], # I
              [(0,-1),(-1,-1),(-1,0),(0,0)], # O
              [(0,0),(-1,-1),(0,-1),(1,0)], # Z
              [(0,0),(-1,0),(0,-1),(1,-1)], # S
              [(0,0),(-1,0),(1,0),(1,-1)], # L
              [(0,0),(-1,-1),(-1,0),(1,0)], # J
              [(0,0),(-1,0),(1,0),(0,-1)]] # T

tetrominos = [[pygame.Rect(x + WIDTH // 2, y +1, 1, 1) for x, y in block_pos] for block_pos in tetrominos_pos]
tetromino_rect = pygame.Rect(0,0, TILE -2, TILE -2)

tetromino = deepcopy(tetrominos[0])

anim_count, anim_speed, anim_limit = 0, 60, 2000

def check_borders():
    if tetromino[i].x < 0 or tetromino[i].x > WIDTH-1:
        return False
    return True

while True:
    screen.fill(pygame.Color("black"))
    dir_x = 0

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
                anim_limit = 2000



    # (40,40,40) is color (gray), i_rect is position in GRID, [] is used because we are running this line by making a list and not storing list in a var so no new element is created (could just write it normamly but python is cool like that)
    [pygame.draw.rect(screen, (40,40,40), i_rect, 1) for i_rect in GRID]

    for i in range(4):
        tetromino_rect.x = tetromino[i].x * TILE
        tetromino_rect.y = tetromino[i].y * TILE
        pygame.draw.rect(screen, pygame.Color("white"), tetromino_rect)

    pygame.display.update()
    CLOCK.tick(60)