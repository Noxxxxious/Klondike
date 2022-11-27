import pygame

from Card import Card
from GameWindow import GameWindow


class Klondike:
    def __init__(self):
        self.deck = list()
        self.generate_new_deck()
        self.window = GameWindow()
        self.running = True
        self.dragging = False
        self.dragged_card = None

    def generate_new_deck(self):
        suits = ["hearts", "diamonds", "spades", "clubs"]
        for suit in suits:
            for number in range(1, 14):
                self.deck.append(Card(number, suit))

    def draw(self):
        for card in self.deck:
            self.window.screen.blit(card.image, card.rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.player_action(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not pygame.mouse.get_pressed()[0]:
                        self.dragging = False
                        self.dragged_card = None
                elif event.type == pygame.MOUSEMOTION and self.dragging and self.dragged_card is not None:
                    self.dragged_card.rect.move_ip(event.rel)
            self.window.screen.fill((20, 20, 20))
            self.draw()
            pygame.display.update()
        pygame.quit()

    def player_action(self, pos, pressed):
        if pressed[0]:
            card_to_drag = None
            for i, card in enumerate(self.deck):
                if card.rect.collidepoint(pos):
                    card_to_drag = card
            self.deck.append(card_to_drag)
            self.deck.remove(card_to_drag)
            self.dragged_card = card_to_drag
            self.dragging = True
        if pressed[2]:
            a = 1
