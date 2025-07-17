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
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

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
game_over = False
score = 0
high_score = 0
Lives = 3
font_big = pygame.font.SysFont(None, 72)
font_small = pygame.font.SysFont(None, 36)

def get_fall_speed(score):
    return 2 + (score // 5) * 0.3

def reset_game():
    global blocks, frame_count, shake_timer, offset_x, offset_y, game_over, player_pos, score
    blocks = []
    frame_count = 0
    shake_timer = 0
    offset_x = 0
    offset_y = 0
    game_over = False
    player_pos = pygame.Vector2(WIDTH / 2, HEIGHT - 100)
    score = 0

running = True
while running:
    dt = clock.tick(60) / 1000
    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    if not game_over:          
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
    FALL_SPEED = get_fall_speed(score)

    for b in blocks:
        if not b[1]:
            b[0].y += FALL_SPEED
            if b[0].y + BLOCK_SIZE >= HEIGHT:
                b[0].y = HEIGHT - BLOCK_SIZE
                b[1] = True
                shake_timer = 10
            score += 1
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




    for b in blocks:
        b[0].x += offset_x
        b[0].y += offset_y
        b[0].x -= offset_x
        b[0].y -= offset_y
        dist = ((b[0].x - player.x)**2 + (b[0].y - player.y)**2)**0.5
        if dist < PLAYER_RADIUS + BLOCK_SIZE / 2:
            game_over = True
            if score > high_score:
                high_score = score
            break
    screen.fill(BLACK)

    
    if game_over:
        text1 = font_big.render("Game Over", True, WHITE)
        text2 = font_small.render("R to restart", True, WHITE)
        text3 = font_small.render(f"Score: {score}", True, WHITE)
        text4 = font_small.render(f"High score: {high_score}", True, WHITE)
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2 + 20))
        screen.blit(text4, (WIDTH // 2 - text4.get_width() // 2, HEIGHT // 2 + 60))
    else:
        for b in blocks:
            pygame.draw.rect(screen, RED, b[0])
        pygame.draw.rect(screen,RED,player)
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()