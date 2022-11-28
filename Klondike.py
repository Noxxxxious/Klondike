import pygame
import random

from Card import Card
from GameWindow import GameWindow
from CardDock import CardDock


class Klondike:
    def __init__(self):
        self.deck = list()
        self.generate_new_deck()
        self.window = GameWindow()
        self.running = True
        self.dragging = False
        self.dragged_card = None
        self.docks = [CardDock(500, 50), CardDock(650, 50), CardDock(800, 50), CardDock(950, 50)]

    def generate_new_deck(self):
        suits = ["hearts", "diamonds", "spades", "clubs"]
        for suit in suits:
            for number in range(1, 14):
                self.deck.append(Card(number, suit))
        # random.shuffle(self.deck)

    def draw(self):
        for dock in self.docks:
            pygame.draw.rect(self.window.screen, (50, 50, 50), dock.rect)
        for card in self.deck:
            self.window.screen.blit(card.image, card.rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.lift_card(pygame.mouse.get_pos())
                    elif pygame.mouse.get_pressed()[2]:
                        self.try_dock_card(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not pygame.mouse.get_pressed()[0] and self.dragged_card is not None:
                        self.drop_card(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEMOTION and self.dragging and self.dragged_card is not None:
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
        if card_to_drag.isDocked:
            card_to_drag.dock.lift()
            card_to_drag.undock()
        self.deck.append(card_to_drag)
        self.deck.remove(card_to_drag)
        self.dragged_card = card_to_drag
        self.dragging = True

    def try_dock_card(self, pos):
        card_to_dock = None
        for card in self.deck:
            if card.rect.collidepoint(pos):
                card_to_dock = card
        if card_to_dock is None:
            return
        if card_to_dock.isDocked:
            return
        for dock in self.docks:
            if card_to_dock.number == dock.rank + 1 and (card_to_dock.suit == dock.suit or dock.suit is None):
                card_to_dock.rect.x, card_to_dock.rect.y = dock.rect.x, dock.rect.y
                card_to_dock.set_dock(dock)
                dock.place(card_to_dock)
                self.deck.append(card_to_dock)
                self.deck.remove(card_to_dock)
                print(dock.suit, ":")
                for card in dock.cards:
                    print(card.name, end="")
                print()
                return

    def drop_card(self, pos):
        for dock in self.docks:
            if dock.rect.collidepoint(pos):
                self.try_dock_card(pos)
        self.dragging = False
        self.dragged_card = None
