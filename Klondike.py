import pygame
import random

from Card import Card
from GameWindow import GameWindow
from CardDock import CardDock
from CardColumn import CardColumn
from CardStack import CardStack


class Klondike:
    def __init__(self):
        self.deck = list()
        self.generate_new_deck()
        self.window = GameWindow()
        self.running = True
        self.dragged_card = None
        self.docks = [CardDock(550, 50), CardDock(700, 50), CardDock(850, 50), CardDock(1000, 50)]
        self.columns = [CardColumn(100, 240), CardColumn(250, 240), CardColumn(400, 240), CardColumn(550, 240),
                        CardColumn(700, 240), CardColumn(850, 240), CardColumn(1000, 240)]
        self.stack = CardStack(100, 50)
        self.deal_game()

    def generate_new_deck(self):
        suits = ["hearts", "diamonds", "spades", "clubs"]
        for suit in suits:
            for number in range(1, 14):
                self.deck.append(Card(number, suit))
        random.shuffle(self.deck)

    def deal_game(self):
        start = 0
        for i in range(7):
            for j in range(start, start + i):
                self.columns[i].place(self.deck[j])
                self.deck[j].flip()
            start += i
        for i in range(7):
            self.columns[i].place(self.deck[start + i])
        for i in range(start + 7, len(self.deck)):
            self.stack.place(self.deck[i])

    def draw(self):
        pygame.draw.rect(self.window.screen, self.stack.color, self.stack.rect)
        for dock in self.docks:
            pygame.draw.rect(self.window.screen, dock.color, dock.rect)
        for column in self.columns:
            pygame.draw.rect(self.window.screen, column.color, column.rect)
        for card in self.deck:
            self.window.screen.blit(card.image, card.rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0]:
                        if self.stack.rect.collidepoint(pygame.mouse.get_pos()):
                            self.cycle_stack()
                        else:
                            self.lift_card(pos)
                    elif pygame.mouse.get_pressed()[2]:
                        self.try_dock_card(pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not pygame.mouse.get_pressed()[0] and self.dragged_card is not None:
                        self.drop_card(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEMOTION and self.dragged_card is not None:
                    self.dragged_card.rect.move_ip(event.rel)
            self.window.screen.fill((20, 20, 20))
            self.draw()
            pygame.display.update()
        pygame.quit()

    def lift_card(self, pos):
        card_to_drag = None
        for card in self.deck:
            if card.rect.collidepoint(pos):
                card_to_drag = card
        if card_to_drag is None:
            return
        self.float_card(card_to_drag)
        self.dragged_card = card_to_drag

    def try_dock_card(self, pos):
        card_to_dock = None
        for card in self.deck:
            if card.rect.collidepoint(pos):
                card_to_dock = card
        if card_to_dock is None:
            return False
        if card_to_dock.isDocked:
            return False
        for dock in self.docks:
            if card_to_dock.number == dock.rank + 1 and (card_to_dock.suit == dock.suit or dock.suit is None):
                if card_to_dock.isColumn:
                    card_to_dock.column.lift()
                    card_to_dock.reset_column()
                if card_to_dock.isStack:
                    self.stack.remove_card(card_to_dock)
                dock.place(card_to_dock)
                self.float_card(card_to_dock)
                return True
        return False

    def try_put_to_column(self, pos):
        card_to_column = None
        for card in self.deck:
            if card.rect.collidepoint(pos):
                card_to_column = card
        if card_to_column is None:
            return False
        for column in self.columns:
            if not column.front_rect.collidepoint(pos):
                continue
            if (not column.cards and card_to_column.rank == "king") \
                    or (column.cards and column.cards[-1].number == card_to_column.number + 1 and column.cards[-1].color != card_to_column.color):
                if card_to_column.isDocked:
                    card_to_column.dock.lift()
                    card_to_column.undock()
                if card_to_column.isColumn:
                    card_to_column.column.lift()
                    card_to_column.reset_column()
                if card_to_column.isStack:
                    self.stack.remove_card(card_to_column)
                column.place(card_to_column)
                return True
        return False

    def drop_card(self, pos):
        card_transported = False
        for dock in self.docks:
            if dock.rect.collidepoint(pos):
                card_transported = self.try_dock_card(pos)
        card_transported = card_transported or self.try_put_to_column(pos)
        if not card_transported:
            self.dragged_card.rect = self.dragged_card.prev_rect.copy()
        self.dragged_card = None

    def cycle_stack(self):
        if self.stack.cards:
            top_card = self.stack.cards[-1]
            self.stack.table_cards.append(self.stack.cards.pop())
            top_card.flip()
            top_card.rect.x += 150
            top_card.prev_rect = top_card.rect.copy()
            self.float_card(top_card)
        else:
            for card in reversed(self.stack.table_cards):
                card.flip()
                card.rect.x -= 150
                self.stack.cards.append(self.stack.table_cards.pop())
                self.float_card(card)

    def float_card(self, card):
        self.deck.append(card)
        self.deck.remove(card)
