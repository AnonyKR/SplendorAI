from blackjack.player import *

import random

class Blackjack:
    BLACKJACK = 21
    DEALER_STOP = 17
    
    def __init__(self, deck_num=1, display=False):
        self.display = display
        self.num_deck = deck_num
        self.deck = []
        for _ in range(0,self.num_deck):
            for _ in range(0,4):
                for card in range(0,13):
                    self.deck.append(card)
        self.dealer_close = []
        self.dealer_open = []
        self.players = []
        self.discard = []
        self.shuffle_deck()
        
    def add_player(self, player : Player):
        self.players.append(player)
        
    def shuffle_deck(self):
        self.deck.extend(self.discard)
        self.discard = []
        random.shuffle(self.deck)
        
    def show(self):
        if self.display:
            if len(self.dealer_close) == 1:
                print("?", end=" ")
            print(cards_to_str(self.dealer_open) + " - Sum : " + str(self.sum_hand()))
            for x in self.players:
                print(x)
    
    def sum_hand(self):
        total = 0
        aces = 0
        for x in self.dealer_open:
            if x == 12:
                total += 11
                aces += 1
            elif x < 9:
                total += x + 2
            else:
                total += 10
        if total > 21 and aces > 0:
            while total > 21 and aces > 0:
                aces -= 1
                total -= 10
        return total
    
    def playRound(self):
        for player in self.players:
            player.add_hand(self.deck.pop(0))
            player.add_hand(self.deck.pop(0))
        self.dealer_close.append(self.deck.pop(0))
        self.dealer_open.append(self.deck.pop(0))
        for player in self.players:
            player.dealer_info(self.dealer_open)
        self.show()
        for player in self.players:
            while (not player.is_bust()) and player.hit():
                player.add_hand(self.deck.pop(0))
                self.show()
        self.dealer_open.append(self.dealer_close.pop(0))
        total = self.sum_hand()
        self.show()
        while self.sum_hand() < self.DEALER_STOP:
            self.dealer_open.append(self.deck.pop(0))
            self.show()
            if self.sum_hand() > 21:
                total = -1
                break
        if total != -1:
            total = self.sum_hand()
        for player in self.players:
            is_tie = (total == player.max_sum())
            win = (player.max_sum() >= total)
            self.discard.extend(player.result(win=win,tie=is_tie, display=self.display))