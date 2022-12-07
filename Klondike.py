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

    def generate_new_deck(self):
        suits = ["hearts", "diamonds", "spades", "clubs"]
        for suit in suits:
            for number in range(1, 14):
                self.deck.append(Card(number, suit))
        # random.shuffle(self.deck)

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
                card_to_dock.set_dock(dock)
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
            if column.front_rect.collidepoint(pos):
                if card_to_column.isDocked:
                    card_to_column.dock.lift()
                    card_to_column.undock()
                if card_to_column.isColumn:
                    card_to_column.column.lift()
                    card_to_column.reset_column()
                card_to_column.set_column(column)
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

    def float_card(self, card):
        self.deck.append(card)
        self.deck.remove(card)
