from .exception import *
from .card import *

import os
import random

def cost_vs_payment_valid(cost_list, payment_list):
    for x in payment_list:
        if x < 0:
            raise GameException()
    if sum(cost_list) != sum(payment_list):
        return False
    if len(payment_list) == 5 or payment_list[5] == 0:
        return payment_list[:5] == cost_list
    if payment_list[5] < 0:
        return False
    for x in range(0,5):
        if payment_list[x] < 0:
            return False
        if payment_list[x] > cost_list[x]:
            return False
    return True
    

class GameStatus:
    GAME_WIN_POINT = 15
    MAX_HOLD = 3

    def __init__(self, *args):
        #check number of players and tokens used
        #token is in white, blue, green, red, brown, gold order
        if len(args) > 0:
            self.players = args[0]
            match (len(self.players)):
                case 2:
                    self.tokens = [4,4,4,4,4,5]
                case 3:
                    self.tokens = [5,5,5,5,5,5]
                case 4:
                    self.tokens = [7,7,7,7,7,5]
                case _:
                    raise GameException
        else:
            raise GameException
        #set up cards to be used
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "cardPreset.txt")
        preset = open(file_path, "r")
        presetSave = preset.readlines()
        preset.close()
        cardList = [] 
        for x in presetSave:
            cardList.append(x.strip())
        cardObjects = []
        for x in cardList:
            cardObjects.append(Card(int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), int(x[6]), int(x[7])))
        #split cards into each deck for level 1,2,3
        self.cards = [[],[],[]] #level 3, level 2, level 1
        for x in cardObjects:
            cardLevel = x.get_level()
            match (cardLevel):
                case 1:
                    self.cards[2].append(x)
                case 2:
                    self.cards[1].append(x)
                case 3:
                    self.cards[0].append(x)
        random.shuffle(self.cards[0])
        random.shuffle(self.cards[1])
        random.shuffle(self.cards[2])
        self.opens = [[],[],[]]
        for x in range(0,4):
            self.opens[0].append(self.cards[0].pop())
            self.opens[1].append(self.cards[1].pop())
            self.opens[2].append(self.cards[2].pop())
        #set up noble tiles
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "noble.txt")
        preset = open(file_path, "r")
        presetSave = preset.readlines()
        preset.close()
        nobleList = []
        for x in presetSave:
            nobleList.append(x.strip())
        noblesObjects : list[Noble] = []
        for x in nobleList:
            noblesObjects.append(Noble(int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4])))
        random.shuffle(noblesObjects)
        self.noble_used = []
        for x in range(0, len(self.players) + 1):
            self.noble_used.append(noblesObjects.pop())
        
    def get_cards(self):
        return self.opens
    
    def get_decks(self):
        return self.cards
    
    def get_tokens(self):
        return self.tokens
    
    def get_nobles(self) -> list[Noble]:
        return self.noble_used
    
    def get_players(self):
        return self.players
    
    def is_over(self):
        for x in self.players:
            if x.get_points() >= 15:
                return True
        return False
    
    def take_hold(self, turn, card_choice):
        if card_choice > 14 or card_choice < 0:
            raise GameException()
        if len(turn.get_hold()) >= GameStatus.MAX_HOLD:
            raise GameException()
        if card_choice % 5 == 0:
            turn.add_hold(self.cards[card_choice // 5].pop())
        else:
            turn.add_hold(self.opens[card_choice // 5].pop(card_choice % 5 - 1))
            self.opens[card_choice // 5].insert(card_choice % 5 - 1, self.cards[card_choice // 5].pop()) # issue
        if self.tokens[5] >= 1:
            turn.add_tokens([0,0,0,0,0,1]) #check if it has it
            self.tokens[5] -= 1

    def take_token(self, token_list, hold=False):
        if hold is True:
            if self.tokens[5] >= 1:
                self.tokens[5] -= 1
                return [0,0,0,0,0,1]
            else:
                return [0,0,0,0,0,0]
        if len(token_list) != 5 and token_list[5] != 0: #could have length of 5
            raise GameException()
        two_count = 0
        two_loc = 0
        one_count = 0
        zero_count = 0
        for x in range(0,5):
            if token_list[x] == 1:
                one_count += 1
            elif token_list[x] == 2:
                two_count += 1
                two_loc = x
            elif token_list[x] == 0:
                zero_count += 1
            else:
                raise GameException()
        if two_count == 1 and zero_count == 4:
            if not (self.tokens[two_loc] >= 4):
                raise GameException()
            return self.token_subtract(token_list)
        if two_count != 0:
            raise GameException()
        empty_pile = 0
        for x in range(0,5):
            if self.tokens[x] == 0:
                empty_pile += 1
        if (empty_pile >= 3 and one_count == 5 - empty_pile) or (empty_pile <= 2 and one_count == 3):
            return self.token_subtract(token_list)
        raise GameException()
    
    def token_subtract(self, token_list):
        for x in range(0,len(token_list)):
            self.tokens[x] -= token_list[x]
        return token_list
    
    def token_add(self, token_list):
        for x in range(0,6):
            self.tokens[x] += token_list[x]

    def buy_card(self, card : Card, turn, payment_list):
        #card is card Object
        #payment only counts actual token, not permenet ones.
        if not self.players[x].subtract_poss(payment_list):
            raise GameException()
        total_pay = [0,0,0,0,0,0]
        for x in range(0,6):
            total_pay[x] += payment_list[x]
        card_token = self.players[turn].get_card_tokens()
        for x in range(0,5):
            total_pay[x] += card_token[x]
        if not cost_vs_payment_valid(card.get_cost(), total_pay):
            raise GameException()
        self.players[turn].subtract_tokens(payment_list)
        self.players[turn].add_card(card)
        self.token_add(payment_list)

    def check_noble(self, turn):
        choices = []
        cards_owned = turn.get_card_tokens()
        for x in self.noble_used:
            cost = x.get_cost()
            add = True
            for y in range(0,5):
                if cost[y] >cards_owned[y]:
                    add = False
                    break
            if add:
                choices.append(x)
        return choices

    def take_noble(self, noble):
        for x in range(0,len(self.noble_used)):
            if noble is self.noble_used[x]:
                return self.noble_used.pop(x)
        raise GameException()
            