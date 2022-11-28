import pygame


class CardContainer:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 140)
        self.cards = list()
        self.color = (50, 50, 50)