import pygame

from CardContainer import CardContainer


class CardColumn(CardContainer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.front_rect = pygame.Rect(self.rect)

    def place(self, cards):
        for card in cards:
            card.rect.x, card.rect.y = self.front_rect.x, self.front_rect.y
            card.prev_rect = card.rect.copy()
            card.set_column(self)
            self.front_rect.y += 20
            self.cards.append(card)

    def lift(self, cards):
        for card in cards:
            self.cards.remove(card)
            card.reset_column()
            self.front_rect.y -= 20
        if self.cards and not self.cards[-1].isRevealed:
            self.cards[-1].flip()

    def get_children(self, card):
        try:
            index = self.cards.index(card)
            return self.cards[index:]
        except ValueError:
            return []

    def print(self):
        for card in self.cards:
            card.print()
