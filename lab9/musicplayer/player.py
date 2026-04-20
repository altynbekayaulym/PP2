import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        self.playlist = [
            "Homecoming.mp3",
            "Flashing_Lights.mp3",
            "Runaway.mp3"
        ]

        self.current = 0
        self.is_playing = False

        self.font = pygame.font.SysFont(None, 36)

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        self.current = (self.current + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.current = (self.current - 1) % len(self.playlist)
        self.play()

    def draw(self, screen):
        text = f"Track: {os.path.basename(self.playlist[self.current])}"
        img = self.font.render(text, True, (255, 255, 255))
        screen.blit(img, (50, 150))