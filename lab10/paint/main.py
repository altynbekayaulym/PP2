import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

screen.fill(WHITE)

clock = pygame.time.Clock()

current_color = BLACK
tool = "brush"

drawing = False
start_pos = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: current_color = RED
            if event.key == pygame.K_2: current_color = GREEN
            if event.key == pygame.K_3: current_color = BLUE
            if event.key == pygame.K_4: current_color = BLACK

            if event.key == pygame.K_b: tool = "brush"
            if event.key == pygame.K_r: tool = "rect"
            if event.key == pygame.K_c: tool = "circle"
            if event.key == pygame.K_e: tool = "eraser"

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool == "rect":
                rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                pygame.draw.rect(screen, current_color, rect, 2)

            elif tool == "circle":
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 2)

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "brush":
                pygame.draw.circle(screen, current_color, event.pos, 5)
            elif tool == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()