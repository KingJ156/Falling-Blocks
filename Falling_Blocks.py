import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Blocks")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

player_pos = pygame.Vector2(WIDTH / 2, HEIGHT - 100)
PLAYER_RADIUS = 20
PLAYER_SPEED = 150

BLOCK_SIZE = 45
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
            player_pos.x -= PLAYER_SPEED * dt
        if keys[pygame.K_d]:
            player_pos.x += PLAYER_SPEED * dt
        player_pos.x = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, player_pos.x))

        if frame_count >= SPAWN_INTERVAL:
            x = random.randint(0, WIDTH - BLOCK_SIZE)
            y = 0
            blocks.append([x, y, False, FADE_TIME])
            frame_count = 0

        fall_speed = get_fall_speed(score)

        for b in blocks:
            if not b[2]:
                b[1] += fall_speed
                if b[1] + BLOCK_SIZE >= HEIGHT:
                    b[1] = HEIGHT - BLOCK_SIZE
                    b[2] = True
                    shake_timer = 10
                    score += 1
            else:
                b[3] -= 1

        blocks = [b for b in blocks if b[3] > 0]

        if shake_timer > 0:
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            shake_timer -= 1
        else:
            offset_x = 0
            offset_y = 0

        for b in blocks:
            bx = b[0] + BLOCK_SIZE / 2
            by = b[1] + BLOCK_SIZE / 2
            dist = ((bx - player_pos.x)**2 + (by - player_pos.y)**2)**0.5
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
            pygame.draw.rect(screen, GRAY, (b[0] + offset_x, b[1] + offset_y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.circle(screen, RED, (int(player_pos.x + offset_x), int(player_pos.y + offset_y)), PLAYER_RADIUS)
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()