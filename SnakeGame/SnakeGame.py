import pygame
from pygame.locals import *
from sys import exit
from random import randint, choice

pygame.init()
# Game settings
widht = 800
height = 600
screen = pygame.display.set_mode((widht, height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
death = False
# Snake
x_snake = int(widht / 2)
y_snake = int(height / 2)
snake_list = []
snake_speed = 20
snake_size = 3
x_control = snake_speed
y_control = 0
# Apple
x_apple = randint(0, 780) // 20 * 20
y_apple = randint(0, 580) // 20 * 20
# Scoreboard
score = 0
scoreboard_font = pygame.font.SysFont('arial', 20, bold=True, italic=True)
# Walls
walls = []
walls_rect_list = []
wallsXpositions = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560, 600, 640, 680, 720, 760]
wallsYpositions = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560]


def snakeIncreases(snake_list_):
    for pos in snake_list_:
        pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], 20, 20))


def snakeDeath():
    global death
    restart_game_font = pygame.font.SysFont('arial', 20, True, True)
    restart_game_msg = 'Game over! Press R to play again'
    f_restart_game = restart_game_font.render(restart_game_msg, True, (0, 0, 0))
    restart_game_ret = f_restart_game.get_rect()
    death = True

    while death:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    restartGame()

        restart_game_ret.center = (widht // 2, widht // 2)
        screen.blit(f_restart_game, restart_game_ret)
        pygame.display.update()


def restartGame():
    global score, snake_size, x_snake, y_snake, snake_list, snake_head, x_apple, y_apple, death
    score = 0
    snake_size = 5
    x_snake = int(widht / 2)
    y_snake = int(height / 2)
    snake_list = []
    snake_head = []
    x_apple = randint(0, 780) // 20 * 20
    y_apple = randint(0, 580) // 20 * 20
    walls.clear()
    walls_rect_list.clear()
    death = False


# Game loop
while True:
    clock.tick(20)
    screen.fill((0, 0, 0))

    scoreboard_msg = f'Score: {score}'
    f_scoreboard = scoreboard_font.render(scoreboard_msg, True, (255, 255, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_a:
                if not x_control == snake_speed:
                    x_control = -snake_speed
                    y_control = 0
            if event.key == K_d:
                if not x_control == -snake_speed:
                    x_control = snake_speed
                    y_control = 0
            if event.key == K_w:
                if not y_control == snake_speed:
                    y_control = -snake_speed
                    x_control = 0
            if event.key == K_s:
                if not y_control == -snake_speed:
                    y_control = snake_speed
                    x_control = 0

    x_snake += x_control
    y_snake += y_control

    snake = pygame.draw.rect(screen, (0, 255, 0), (x_snake, y_snake, 20, 20))
    apple = pygame.draw.rect(screen, (255, 0, 0), (x_apple, y_apple, 20, 20))
    if len(walls) > 0:
        for wall in walls:
            wall_rect = pygame.draw.rect(screen, (255, 255, 255), (wall[0], wall[1], 40, 40))
            walls_rect_list.append(wall_rect)

    if snake.colliderect(apple):
        x_apple = randint(0, 780) // 20 * 20
        y_apple = randint(0, 580) // 20 * 20
        score += 1
        snake_size += 1
        chance = randint(0, 1)
        if chance == 1:
            new_wall = (choice(wallsXpositions), choice(wallsYpositions))
            if new_wall not in walls:
                walls.append(new_wall)
    for cd in walls_rect_list:
        if apple.colliderect(cd):
            x_apple = randint(0, 780) // 20 * 20
            y_apple = randint(0, 580) // 20 * 20

        if snake.colliderect(cd):
            snakeDeath()

    snake_head = [x_snake, y_snake]
    snake_list.append(snake_head)

    if snake_list.count(snake_head) > 1:
        snakeDeath()

    if x_snake > widht:
        snakeDeath()
    if x_snake < 0:
        snakeDeath()
    if y_snake < 0:
        snakeDeath()
    if y_snake > widht:
        snakeDeath()

    if len(snake_list) > snake_size:
        del snake_list[0]

    snakeIncreases(snake_list)
    screen.blit(f_scoreboard, (670, 10))
    pygame.display.update()
