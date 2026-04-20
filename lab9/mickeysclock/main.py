import pygame
from clock import MickeyClock

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()
mickey = MickeyClock(screen, WIDTH, HEIGHT)

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mickey.update()
    mickey.draw()

    pygame.display.flip()
    clock.tick(1) 

pygame.quit()