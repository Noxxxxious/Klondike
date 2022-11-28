import pygame
from utils.helpers import number_to_rank


class Card:
    def __init__(self, number, suit):
        self.number = number
        self.rank = number_to_rank(number)
        self.suit = suit
        self.name = self.rank + "_of_" + suit
        self.face = pygame.transform.scale(pygame.image.load(f"images/{self.name}.png"), (100, 140))
        self.cover = pygame.transform.scale(pygame.image.load("images/cover.png"), (100, 140))
        self.image = self.face
        self.rect = self.image.get_rect()
        self.isRevealed = True
        self.isDocked = False
        self.dock = None
        self.isColumn = False
        self.column = None

    def flip(self):
        if self.isRevealed:
            self.image = self.cover
            self.isRevealed = False
        else:
            self.image = self.face
            self.isRevealed = True

    def set_dock(self, dock):
        self.isDocked = True
        self.dock = dock

    def undock(self):
        self.isDocked = False
        self.dock = None

    def set_column(self, column):
        self.isColumn = True
        self.column = column

    def reset_column(self):
        self.isColumn = False
        self.column = None
