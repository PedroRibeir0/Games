import random
import sys
import pygame
from pygame.locals import *

# Game Settings
pygame.init()
width = 700
height = 300
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
speed_increase = 1
# Floor
Floor = (screen, (150, 75, 0), (0, height - 10, width, 10))
Floor_pos = 250
fall = 1
jump = 2
# Dino
DinoX = 200
DinoY = 230
Dino = [screen, (0, 200, 0), [DinoX, DinoY, 20, 40]]
Dino_speed = 20
Dino_Dir = fall
# Enemies
Enemies = [
    [screen, (255, 255, 255), [680, 270, 20, 20]],
    [screen, (255, 255, 255), [680, 240, 20, 20]]
]
enemy1_chose = random.choice(Enemies)
enemy_speed = 20
enemy_respawn = 680
enemy_death = 0
# Scoreboard
scoreboard_font = pygame.font.SysFont('arial', 20, True)
score = 0
score_reset = 0

while True:

    pygame.display.update()
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Dino_Dir = jump
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                Dino[2] = [DinoX, Floor_pos, 20, 40]

    if pygame.key.get_pressed()[K_DOWN]:
        Dino[2] = [Dino[2][0], Dino[2][0] + 70, 20, 20]
    if Dino[2][1] <= 150:
        Dino_Dir = fall

    floor_rect = pygame.draw.rect(Floor[0], Floor[1], Floor[2])
    dino_rect = pygame.draw.rect(Dino[0], Dino[1], Dino[2])
    enemy1_rect = pygame.draw.rect(enemy1_chose[0], enemy1_chose[1], enemy1_chose[2])

    if dino_rect.colliderect(enemy1_rect):
        pygame.quit()
        sys.exit()

    if enemy1_chose[2][0] <= 0:
        enemy1_chose = random.choice(Enemies)
        enemy1_chose[2][0] = enemy_respawn
        score += 1
        score_reset += 1

    if Dino_Dir == fall:
        Dino[2][1] += Dino_speed
    if Dino_Dir == jump:
        Dino[2][1] -= Dino_speed
    if Dino[2][1] == Floor_pos:
        Dino_Dir = None

    enemy1_chose[2][0] -= enemy_speed

    scoreboard_msg = f'Score: {score}'
    f_scoreboard = scoreboard_font.render(scoreboard_msg, True, (255, 255, 255))
    screen.blit(f_scoreboard, (590, 20))
    if score_reset == 5:
        enemy_speed += speed_increase
        score_reset = 0
    if enemy_speed == 40:
        speed_increase = 0
    clock.tick(20)
