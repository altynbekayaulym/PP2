import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,223,0)
BLACK = (0,0,0)

player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 100, 50, 80)
enemy = pygame.Rect(random.randint(0, WIDTH-50), -100, 50, 80)

coin = pygame.Rect(random.randint(50, WIDTH-50), -50, 20, 20)
coin_weight = random.choice([1, 2, 3])

score = 0
speed = 5
enemy_speed = 5

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

def spawn_coin():
    global coin_weight
    coin.x = random.randint(50, WIDTH-50)
    coin.y = -50
    coin_weight = random.choice([1, 2, 3])

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
        player.x += speed

    enemy.y += enemy_speed
    if enemy.y > HEIGHT:
        enemy.y = -100
        enemy.x = random.randint(0, WIDTH-50)

    coin.y += 5
    if coin.y > HEIGHT:
        spawn_coin()

    if player.colliderect(coin):
        score += coin_weight
        spawn_coin()
        if score % 5 == 0:
            enemy_speed += 1

    if player.colliderect(enemy):
        running = False

    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, RED, enemy)
    pygame.draw.circle(screen, YELLOW, coin.center, 10)

    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()