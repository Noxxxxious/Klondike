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
        self.revealed = True

    def flip(self):
        if self.revealed:
            self.image = self.cover
            self.revealed = False
        else:
            self.image = self.face
            self.revealed = True
