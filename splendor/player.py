from .game_status import *
from .exception import *
from .card import Card
from abc import *
from typing import List

def count_zeros(list_in):
    count = 0
    for x in list_in:
        if isinstance(x, (int, float)):
            if x == 0:
                count += 1
    return count

def nth_value(list_in, occurence): #find n-th non 0 value of the list (assume list containes ints & have that value)
    if occurence <= 0:
        return (-1,-1)
    c = 0
    for x in range(0,len(list_in)):
        if list_in[x] != 0:
            c += 1
            if c == occurence:
                return (x, list_in[x])
    return (-1,-1)


def show_nobles(noble_list):
    index_to_letter = ["W", "S", "G", "R", "B"]
    current_nobles = noble_list
    empty_cost = []
    cost_list = []
    min_zero = 5
    for x in current_nobles:
        cost_list.append(x.get_cost())
        empty_cost.append(count_zeros(x.get_cost()))
        if empty_cost[-1] < min_zero:
            min_zero = empty_cost[-1]
    repeat = 5 - min_zero
    print("Nobles:")
    for x in range(0, repeat):
        for y in range(0,len(cost_list)):
            if y != 0:
                print("|",end="")
            to_print = nth_value(cost_list[y], min_zero - empty_cost[y] + x + 1)
            print(" ", end="")
            if to_print[0] == -1:
                print("   ", end="")
            else:
                print(index_to_letter[to_print[0]] + "-" + str(to_print[1]), end="")
        print("")

class Player:
    MAX_TOKEN = 10
    MAX_HOLD = GameStatus.MAX_HOLD

    def __init__(self):
        self.order = 0
        self.game_status = None
        self.name = "Default"
        self.hold : List[Card] = []
        self.tokens = [0,0,0,0,0,0]
        self.points = 0
        self.nobles = []
        self.cards = []
        self.card_tokens = [0,0,0,0,0]

    def __str__(self):
        return "test"

    def update_game_status(self, game_status : GameStatus):
        self.game_status = game_status
        player_list = self.game_status.get_players()
        for x in range(0,len(player_list)):
            if player_list[x] is self:
                self.order = x

    def get_tokens(self):
        return self.tokens
    
    def add_tokens(self, tokens):
        for x in range(0,len(tokens)):
            self.tokens[x] += tokens[x]

    def subtract_tokens(self, tokens):
        for x in range(0,len(tokens)):
            if self.tokens[x] < tokens[x]:
                raise GameException()
            self.tokens[x] -= tokens[x]

    def subtract_poss(self, tokens):
        for x in range(0,6):
            if self.tokens[x] < tokens[x]:
                return False
        return True           
    
    def get_hold(self):
        return self.hold
    
    def add_hold(self, card : Card):
        self.hold.append(card)
    
    def get_card_tokens(self):
        return self.card_tokens
    
    def get_name(self):
        return self.name

    def get_points(self):
        return self.points
    
    def add_card(self, card : Card):
        self.cards.append(card)
        self.card_tokens[card.get_token] += 1

    @abstractmethod
    def turn(self):
        pass

class HumanPlayer(Player):
    def turn(self):
        answer = 0
        while True:
            try:
                print("1. Get token")
                print("2. Get hold")
                print("3. Buy card")
                answer = int(input("What would you like to do? : "))
                if answer < 1 or answer > 3:
                    raise GameException()
                break
            except:
                print("Invalid input")
        while True:
            #try:
                if answer == 1:
                    inVal = [0,0,0,0,0]
                    toPrint = ["white", "blue", "green", "red", "brown"]
                    for x in range(0,5):
                        inVal[x] = int(input("How many " + toPrint[x] + " tokens do you want? : "))
                    print(inVal)
                    self.add_tokens(self.game_status.take_token(inVal))
                    break
                elif answer == 2:
                    answerIn = int(input("Which card do you want to add to your hold? (0-14 from top-left to right-bottom) : "))
                    self.game_status.take_hold(self, answerIn)
                    break
                elif answer == 3:
                    buy_hold = False
                    inVal = [0,0,0,0,0]
                    toPrint = ["white", "blue", "green", "red", "brown"]
                    for x in range(0,5):
                        inVal[x] = int(input("How many " + toPrint[x] + " tokens do you want to pay? : "))
                    if len(self.hold) > 0:
                        temp = input("Do you want to buy a card from hold? (y/n) : ")
                        if temp == "y":
                            buy_hold = True
                        elif temp == "n":
                            buy_hold = False
                        else:
                            raise GameException()
                        #fix using buy card method from game status
                        if buy_hold:
                            max = len(self.hold)
                        else:
                            max = 12
                        choice = int(input("Which one do you want to buy? (0 - " + str(max - 1) + ")"))
                        if choice >= max or choice < 0:
                            raise GameException()
                        inVal = [0,0,0,0,0,0]
                        toPrint = ["white", "blue", "green", "red", "brown", "joker"]
                        for x in range(0,6):
                            inVal[x] = int(input("How many " + toPrint[x] + " tokens do you want to pay? : "))
                        self.add_tokens(self.game_status.take_token(inVal))
                        if buy_hold:
                            if cost_vs_payment_valid(self.hold[choice].get_cost(), inVal):
                                pass
                            else:
                                raise GameException()
                        else:
                            if cost_vs_payment_valid(self.game_status.get_cards[choice].get_cost(), inVal):
                                pass
                            else:
                                raise GameException()
                    break #work
            #except:
                #print("Invalid answer")
        noble_poss = self.game_status.check_noble(self)
        if len(noble_poss) == 0:
            print("Your turn ends here")
        else:
            show_nobles(noble_poss)
            valid = False
            if len(noble_poss) == 1:
                while True:
                    try:
                        answer = input("Would you like to take the noble? (y/n): ")
                        if answer == "n": 
                            break
                        elif answer == "y":
                            self.nobles.append(self.game_status.take_noble(noble_poss[0]))
                            break
                        else:
                            raise GameException()
                    except:
                        print("Invalid answer")
            else:
                while not valid:
                    try:
                        answer = input("Which noble do you want? (by index starting 0 left to right): ")
                        self.nobles.append(self.game_status.take_noble(noble_poss[int(answer)]))
                        valid = True
                    except:
                        valid = False