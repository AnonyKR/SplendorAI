from .game_status import GameStatus
from .exception import *
from .card import Card
from abc import abstractmethod

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
        self.hold = []
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
        for x in range(0,6):
            self.tokens[x] += tokens[x]

    def subtract_tokens(self, tokens):
        for x in range(0,6):
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
            match (answer): #do this section
                case 1:
                    break #work
                case 2:
                    break #work
                case 3:
                    break #work
        noble_poss = self.game_status.check_noble()
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