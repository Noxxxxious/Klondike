import pygame
from utils.helpers import number_to_rank
from utils.helpers import suit_to_color


class Card:
    def __init__(self, number, suit):
        self.number = number
        self.rank = number_to_rank(number)
        self.suit = suit
        self.color = suit_to_color(suit)
        self.name = self.rank + "_of_" + suit
        self.face = pygame.transform.scale(pygame.image.load(f"images/{self.name}.png"), (100, 140))
        self.cover = pygame.transform.scale(pygame.image.load("images/cover.png"), (100, 140))
        self.image = self.face
        self.rect = self.image.get_rect()
        self.prev_rect = self.rect.copy()
        self.is_face_up = True
        self.dock = None
        self.column = None
        self.isStack = False

    def flip(self):
        if self.is_face_up:
            self.image = self.cover
            self.is_face_up = False
        else:
            self.image = self.face
            self.is_face_up = True

    def print(self):
        print(self.rank + self.suit[0], end=" ")
