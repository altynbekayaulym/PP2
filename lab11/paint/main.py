import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255,255,255)
BLACK = (0,0,0)

screen.fill(WHITE)
clock = pygame.time.Clock()

tool = "square"
start_pos = None
drawing = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: tool = "square"
            if event.key == pygame.K_t: tool = "triangle"
            if event.key == pygame.K_e: tool = "equilateral"
            if event.key == pygame.K_r: tool = "rhombus"

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            x1, y1 = start_pos
            x2, y2 = end_pos

            if tool == "square":
                size = max(abs(x2-x1), abs(y2-y1))
                pygame.draw.rect(screen, BLACK, (x1, y1, size, size), 2)

            elif tool == "triangle":
                points = [(x1,y1), (x2,y2), (x1,y2)]
                pygame.draw.polygon(screen, BLACK, points, 2)

            elif tool == "equilateral":
                side = abs(x2-x1)
                height = side * (math.sqrt(3)/2)
                points = [
                    (x1, y1),
                    (x1 + side, y1),
                    (x1 + side/2, y1 - height)
                ]
                pygame.draw.polygon(screen, BLACK, points, 2)

            elif tool == "rhombus":
                cx = (x1+x2)//2
                cy = (y1+y2)//2
                points = [
                    (cx, y1),
                    (x2, cy),
                    (cx, y2),
                    (x1, cy)
                ]
                pygame.draw.polygon(screen, BLACK, points, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()