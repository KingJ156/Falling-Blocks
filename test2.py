import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Blocks")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)

player_x = WIDTH /2
player_y = HEIGHT - 100
PLAYER_RADIUS = 20
PLAYER_SPEED = 150
player = pygame.Rect(player_x,player_y,PLAYER_RADIUS,PLAYER_RADIUS)
BLOCK_SIZE = 45
FALL_SPEED = 2
SPAWN_INTERVAL = 40
FADE_TIME = 60
blocks = []

frame_count = 0
shake_timer = 0
offset_x = 0
offset_y = 0

Lives = 3
running = True
while running:
    dt = clock.tick(60) / 1000
    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= PLAYER_SPEED * dt
    if keys[pygame.K_d]:
        player.x += PLAYER_SPEED * dt

    player.x = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, player.x))


    if frame_count >= SPAWN_INTERVAL:
        x = random.randint(0, WIDTH - BLOCK_SIZE)
        y = 0
        landed = False
        timer = FADE_TIME
        blocks.append([pygame.Rect(x,y,BLOCK_SIZE,BLOCK_SIZE), landed, timer])
        frame_count = 0

    for b in blocks:
        if not b[1]:
            b[0].y += FALL_SPEED
            if b[0].y + BLOCK_SIZE >= HEIGHT:
                b[0].y = HEIGHT - BLOCK_SIZE
                b[1] = True
                shake_timer = 10
        else:
            b[2] -= 1

    blocks = [b for b in blocks if b[2] > 0]


    if shake_timer > 0:
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        shake_timer -= 1
    else:
        offset_x = 0
        offset_y = 0


    screen.fill(BLACK)

    for b in blocks:
        b[0].x += offset_x
        b[0].y += offset_y
        pygame.draw.rect(screen, RED, b[0])
        b[0].x -= offset_x
        b[0].y -= offset_y   
    pygame.draw.rect(screen,RED,player)



    pygame.display.flip()

pygame.quit()
sys.exit()