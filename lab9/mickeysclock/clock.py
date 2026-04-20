import pygame
import datetime

class MickeyClock:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.center = (width // 2, height // 2)

        self.clock_face = pygame.image.load("clock.png").convert_alpha()

        self.left_hand = pygame.image.load("hour.png").convert_alpha()
        self.right_hand = pygame.image.load("minute.png").convert_alpha()

    def get_angle(self, value, max_value):
        return (value / max_value) * 360

    def draw_hand(self, image, angle):
        rotated = pygame.transform.rotate(image, -angle)
        rect = rotated.get_rect(center=self.center)
        self.screen.blit(rotated, rect)

    def update(self):
        now = datetime.datetime.now()
        self.seconds = now.second
        self.minutes = now.minute

    def draw(self):
        rect = self.clock_face.get_rect(center=self.center)
        self.screen.blit(self.clock_face, rect)

        sec_angle = self.get_angle(self.seconds, 60)
        min_angle = self.get_angle(self.minutes, 60)

        self.draw_hand(self.left_hand, sec_angle)

        self.draw_hand(self.right_hand, min_angle)