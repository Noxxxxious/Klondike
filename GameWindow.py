import pygame


class GameWindow:
    def __init__(self):
        self.w = 1200
        self.h = 800
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Klondike")
        self.screen.fill((20, 20, 20))
        pygame.display.flip()
