import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)

block = 20
clock = pygame.time.Clock()

snake = [(100,100)]
dx, dy = block, 0

def spawn_food():
    while True:
        pos = (random.randrange(0, WIDTH, block),
               random.randrange(0, HEIGHT, block))
        if pos not in snake:
            return pos

food = spawn_food()

score = 0
level = 1
speed = 10

font = pygame.font.SysFont(None, 30)

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: dx, dy = 0, -block
    if keys[pygame.K_DOWN]: dx, dy = 0, block
    if keys[pygame.K_LEFT]: dx, dy = -block, 0
    if keys[pygame.K_RIGHT]: dx, dy = block, 0

    head = (snake[0][0] + dx, snake[0][1] + dy)

    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        running = False

    if head in snake:
        running = False

    snake.insert(0, head)

    if head == food:
        score += 1
        food = spawn_food()
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, block, block))

    pygame.draw.rect(screen, RED, (*food, block, block))

    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()