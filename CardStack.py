import pygame

from CardContainer import CardContainer


class CardStack(CardContainer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.table_cards = list()

    def place(self, card):
        card.rect.x, card.rect.y = self.rect.x, self.rect.y
        card.prev_rect = card.rect.copy()
        card.isStack = True
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        elif card in self.table_cards:
            self.table_cards.remove(card)
        card.isStack = False
