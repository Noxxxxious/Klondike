import pygame

from CardContainer import CardContainer


class CardColumn(CardContainer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.front_rect = pygame.Rect(self.rect)

    def place(self, cards):
        for card in cards:
            if self.cards:
                self.front_rect.y += 20
            card.rect.x, card.rect.y = self.front_rect.x, self.front_rect.y
            card.prev_rect = card.rect.copy()
            card.column = self
            self.cards.append(card)

    def lift(self, cards):
        for card in cards:
            self.cards.remove(card)
            card.column = None
            if self.cards:
                self.front_rect.y -= 20
        if self.cards and not self.cards[-1].is_face_up:
            self.cards[-1].flip()
            return True
        return False

    def get_children(self, card):
        try:
            index = self.cards.index(card)
            return self.cards[index:]
        except ValueError:
            return []

    def print(self):
        for card in self.cards:
            card.print()
