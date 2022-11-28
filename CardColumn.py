import pygame

from CardContainer import CardContainer


class CardColumn(CardContainer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.front_rect = pygame.Rect(self.rect)

    def place(self, card):
        card.rect.x, card.rect.y = self.front_rect.x, self.front_rect.y
        self.cards.append(card)
        self.front_rect.y += 20

    def lift(self):
        self.cards.pop()
        self.front_rect.y -= 20
