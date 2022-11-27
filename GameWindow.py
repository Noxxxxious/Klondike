import pygame


class GameWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Klondike")
        self.screen.fill((20, 20, 20))
        pygame.display.flip()
