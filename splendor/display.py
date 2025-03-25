from .game_status import GameStatus
from .exception import *
from .player import *

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


class Display:

    def __init__(self, game_status : GameStatus):
        self.game_status : GameStatus = game_status
    
    def show(self):
        pass

    def show_all(self):
        self.show_nobles()
        self.show_cards()
        self.show_tokens()
        self.show_players()

    def show_tokens(self):
        current_tokens = self.game_status.get_tokens()
        print(f"Current tokens : White-{current_tokens[0]}, Sky-{current_tokens[1]}, Green-{current_tokens[2]}, Red-{current_tokens[3]}, Brown-{current_tokens[4]}, Joker-{current_tokens[5]}")

    def show_nobles(self):
        index_to_letter = ["W", "S", "G", "R", "B"]
        current_nobles = self.game_status.get_nobles()
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

    def show_cards(self):
        index_to_letter = ["W", "S", "G", "R", "B"]
        current_cards = self.game_status.get_cards()
        current_deck = self.game_status.get_decks()
        print("Cards:")
        for x in range(0,3):
            if x != 0:
                print("----+----+----+----+----")
            empty_cost = []
            cost_list = []
            for y in current_cards[x]:
                cost_list.append(y.get_cost())
                empty_cost.append(count_zeros(y.get_cost()))
            print("    |" + str(index_to_letter[current_cards[x][0].get_token()]) + "  " + str(current_cards[x][0].get_point()) + "|" + str(index_to_letter[current_cards[x][1].get_token()]) + "  " + str(current_cards[x][1].get_point()) + "|" + str(index_to_letter[current_cards[x][2].get_token()]) + "  " + str(current_cards[x][2].get_point()) + "|" + str(index_to_letter[current_cards[x][3].get_token()]) + "  " + str(current_cards[x][3].get_point()))
            for y in range(0,5):
                if y == 1:
                    print("Lv." + str(3-x),end="")
                elif y == 3:
                    if len(str(len(current_deck[x]))) == 2:
                        print(" " + str(len(current_deck[x])) + " ",end="")
                    else:
                        print(" " + str(len(current_deck[x])) + "  ",end="")
                else:
                    print("    ",end="")
                for z in range(0, 4):
                    print("|",end="")
                    to_print = nth_value(cost_list[z], y - empty_cost[z] + 1)
                    print(" ", end="")
                    if to_print[0] == -1:
                        print("   ", end="")
                    else:
                        print(index_to_letter[to_print[0]] + "-" + str(to_print[1]), end="")
                print("")      

    def show_players(self):
        for x in self.game_status.get_players():
            Display.print_player(x)
            print("")

    def print_player(player : Player):
        print(player.get_name() + ": " + str(player.get_points()) + "pts")
        index_to_letter = ["White", "Sky", "Green", "Red", "Brown","Joker"]
        t = player.get_tokens()
        tp = player.get_card_tokens()
        for x in range(0, 6):
            print(index_to_letter[x] + ": " + str(t[x]), end="")
            if x != 5:
                print("(+" + str(tp[x]) + ")")
        print("")
        index_to_letter = ["W", "S", "G", "R", "B"]
        if len(player.get_hold()) != 0:
            print("Hold:")
            cost_list = []
            empty_cost = []
            for x in player.get_hold():
                cost_list.append(x.get_cost())
                empty_cost.append(count_zeros(x.get_cost()))
            for x in range(0,5):
                for y in range(0, len(cost_list)):
                    if y != 0:
                        print("|", end="")
                    to_print = nth_value(cost_list[y], x - empty_cost[y] + 1)
                    print(" ", end="")
                    if to_print[0] == -1:
                        print("  ", end="")
                    else:
                        print(index_to_letter[to_print[0]] + "-" + str(to_print[1]), end="")
                print("")
        else:
            print("Holding no card")