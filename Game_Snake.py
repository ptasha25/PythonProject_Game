import random
import pygame
import pygame_menu
import time
from random import randrange

pygame.init()
surface = pygame.display.set_mode((800, 800))


def start_the_game():
    RES = 800
    SIZE = 50
    global high_score
    x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
    apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
    dris = {'W': True, 'S': True, 'A': True, 'D': True}
    length = 1
    snake = [(x, y)]
    score = 0
    dx, dy = 0, 0
    fps = 8

    pygame.init()
    sc = pygame.display.set_mode([RES, RES])
    clock = pygame.time.Clock()
    font_score = pygame.font.SysFont('Arial', 26, bold = True)
    font_end = pygame.font.SysFont('Arial', 70, bold = True)

    while True:
        sc.fill(pygame.Color('blue'))

        [(pygame.draw.rect(sc, pygame.Color('green'), (i, j, SIZE - 2, SIZE - 2))) for i, j in snake]
        pygame.draw.rect(sc, pygame.Color('red'), (*apple, SIZE, SIZE))
        render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
        sc.blit(render_score, (5, 5))

        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        snake = snake[-length:]

        if snake[-1] == apple:
            apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
            length += 1
            score += 1
            fps += 1

        if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
            render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
            sc.blit(render_end, (RES // 2 -200, RES // 3))
            pygame.display.flip()
            time.sleep(3)
            break

        pygame.display.flip()
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_w] and dris['W']:
            dris = {'W': True, 'S': False, 'A': True, 'D': True}
            dx, dy = 0, -1
        if key[pygame.K_s] and dris['S']:
            dx, dy = 0, 1
            dris = {'W': False, 'S': True, 'A': True, 'D': True}
        if key[pygame.K_a] and dris['A']:
            dx, dy = -1, 0
            dris = {'W': True, 'S': True, 'A': True, 'D': False}
        if key[pygame.K_d] and dris['D']:
            dx, dy = 1, 0
            dris = {'W': True, 'S': True, 'A': False, 'D': True}


menu = pygame_menu.Menu('SNAKE', 800, 800,
                       theme=pygame_menu.themes.THEME_BLUE)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
