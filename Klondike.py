import time
import pygame
import random

from Card import Card
from GameWindow import GameWindow
from CardDock import CardDock
from CardColumn import CardColumn
from CardStack import CardStack

pygame.init()


class Klondike:
    NUM_CARDS = 52
    NUM_RANKS = 13
    NUM_COLUMNS = 7
    NUM_DOCKS = 4
    BACKGROUND_COLOR = (20, 20, 20)
    CONTAINER_OFFSET = 150
    HITBOX_MARGIN = 70
    SUITS = ["hearts", "diamonds", "spades", "clubs"]
    FPS = 60

    def __init__(self):
        self.deck = list()
        self.generate_new_deck()
        self.window = GameWindow()
        self.dragged_cards = list()
        self.docks = [CardDock(550 + i * self.CONTAINER_OFFSET, 50) for i in range(self.NUM_DOCKS)]
        self.columns = [CardColumn(100 + i * self.CONTAINER_OFFSET, 240) for i in range(self.NUM_COLUMNS)]
        self.stack = CardStack(100, 50)
        self.fps_clock = pygame.time.Clock()

    def generate_new_deck(self):
        for number in range(1, self.NUM_RANKS + 1):
            for suit in self.SUITS:
                self.deck.append(Card(number, suit))

    def deal_game(self):
        random.shuffle(self.deck)
        start = 0
        for i in range(self.NUM_COLUMNS):
            for j in range(start, start + i):
                self.columns[i].place([self.deck[j]])
                self.deck[j].flip()
            start += i
        for i in range(self.NUM_COLUMNS):
            self.columns[i].place([self.deck[start + i]])
        for i in range(start + self.NUM_COLUMNS, len(self.deck)):
            self.stack.place(self.deck[i])
            self.deck[i].flip()

    def testing_deal(self):
        self.deck.reverse()
        for _ in range(self.NUM_CARDS - 1):
            self.try_dock_card((0, 0))

    def draw(self):
        pygame.draw.rect(self.window.screen, self.stack.color, self.stack.rect)
        for dock in self.docks:
            pygame.draw.rect(self.window.screen, dock.color, dock.rect)
        for column in self.columns:
            pygame.draw.rect(self.window.screen, column.color, column.rect)
        for card in self.deck:
            self.window.screen.blit(card.image, card.rect)

    def run(self):
        self.deal_game()
        while not self.game_over():
            self.handle_game_event()
            self.window.screen.fill(self.BACKGROUND_COLOR)
            self.draw()
            pygame.display.update()
            self.fps_clock.tick()
        self.animate_game_ending()

    def handle_game_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
                if not pygame.mouse.get_pressed()[0] and self.dragged_cards:
                    self.drop_card(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEMOTION and self.dragged_cards:
                for card in self.dragged_cards:
                    card.rect.move_ip(event.rel)
    
    def game_over(self):
        for dock in self.docks:
            if len(dock.cards) != self.NUM_RANKS:
                return False
        return True
        
    def lift_card(self, pos):
        for card in self.deck:
            if card.rect.collidepoint(pos) and card.is_face_up:
                if card.isColumn:
                    self.dragged_cards = card.column.get_children(card)
                else:
                    self.dragged_cards = [card]
        self.float_cards(self.dragged_cards)

    def try_dock_card(self, pos):
        card_to_dock = None
        for card in self.deck:
            if card.rect.collidepoint(pos):
                card_to_dock = card
        if (card_to_dock is None or (card_to_dock.isDocked or not card_to_dock.is_face_up)) \
                or (card_to_dock.isColumn and card_to_dock.prev_rect != card_to_dock.column.front_rect):
            return False
        for dock in self.docks:
            if card_to_dock.number == dock.rank + 1 and (card_to_dock.suit == dock.suit or dock.suit is None):
                if card_to_dock.isColumn:
                    card_to_dock.column.lift([card_to_dock])
                if card_to_dock.isStack:
                    self.stack.remove_card(card_to_dock)
                dock.place(card_to_dock)
                self.float_cards([card_to_dock])
                return True
        return False

    def try_put_to_column(self, pos, card_to_column):
        for column in self.columns:
            if not self.mouse_rect_collision(pos, column.front_rect, self.HITBOX_MARGIN, 200):
                continue
            if (not column.cards and card_to_column.rank == "king") \
                    or (column.cards and column.cards[-1].number == card_to_column.number + 1 and column.cards[-1].color != card_to_column.color):
                if card_to_column.isDocked:
                    card_to_column.dock.lift()
                    card_to_column.undock()
                if card_to_column.isColumn:
                    card_to_column.column.lift(self.dragged_cards)
                if card_to_column.isStack:
                    self.stack.remove_card(card_to_column)
                for card in self.dragged_cards:
                    column.place([card])
                return True
        return False

    def drop_card(self, pos):
        card_transported = False
        for dock in self.docks:
            if self.mouse_rect_collision(pos, dock.rect):
                card_transported = self.try_dock_card(pos)
        card_transported = card_transported or self.try_put_to_column(pos, self.dragged_cards[0])
        if not card_transported:
            for card in self.dragged_cards:
                card.rect = card.prev_rect.copy()
        self.dragged_cards = []

    def cycle_stack(self):
        if self.stack.cards:
            top_card = self.stack.cards[-1]
            self.stack.table_cards.append(self.stack.cards.pop())
            top_card.flip()
            top_card.rect.x += 150
            top_card.prev_rect = top_card.rect.copy()
            self.float_cards([top_card])
        else:
            for card in reversed(self.stack.table_cards):
                card.flip()
                card.rect.x -= 150
                self.stack.cards.append(self.stack.table_cards.pop())
                self.float_cards([card])

    @staticmethod
    def mouse_rect_collision(pos, rect, margin_x=HITBOX_MARGIN, margin_y=HITBOX_MARGIN):
        inflated_rect = rect.copy()
        inflated_rect = inflated_rect.inflate(margin_x, margin_y)
        return True if inflated_rect.collidepoint(pos) else False

    def float_cards(self, cards):
        for card in cards:
            self.deck.append(card)
            self.deck.remove(card)

    def animate_game_ending(self):
        for i in reversed(range(self.NUM_RANKS)):
            for j, dock in enumerate(self.docks):
                g = 0.5
                vel_x = - random.randint(4, 10)
                if j in [0, 1] and random.randint(0, 2) == 2:
                    vel_x = - vel_x
                vel_y = - random.randint(4, 8)
                while 0 - dock.cards[i].rect.w < dock.cards[i].rect.x < self.window.w:
                    dock.cards[i].rect.x += vel_x
                    dock.cards[i].rect.y += vel_y
                    vel_y += g
                    if dock.cards[i].rect.y + dock.cards[i].rect.h > self.window.h:
                        dock.cards[i].rect.y = self.window.h - dock.cards[i].rect.h
                        vel_y = - vel_y * 2/3
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    self.window.screen.blit(dock.cards[i].image, dock.cards[i].rect)
                    pygame.display.update()
                    time.sleep(0.01)
                dock.cards.pop()

