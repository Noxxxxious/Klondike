import pygame

from CardContainer import CardContainer


class CardColumn(CardContainer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.front_rect = pygame.Rect(self.rect)

    def place(self, card):
        if self.cards:
            self.front_rect.y += 20
        card.rect.x, card.rect.y = self.front_rect.x, self.front_rect.y
        card.prev_rect = card.rect.copy()
        self.cards.append(card)

    def lift(self):
        self.cards.pop()
        if self.cards:
            self.front_rect.y -= 20
