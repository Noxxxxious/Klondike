from CardContainer import CardContainer


class CardDock(CardContainer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.suit = None
        self.rank = 0

    def place(self, card):
        card.rect.x, card.rect.y = self.rect.x, self.rect.y
        card.prev_rect = card.rect.copy()
        if not self.cards:
            self.suit = card.suit
        self.cards.append(card)
        self.rank += 1

    def lift(self):
        self.cards.pop()
        if not self.cards:
            self.suit = None
        self.rank -= 1

