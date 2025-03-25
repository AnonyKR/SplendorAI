from .game_status import GameStatus
from .exception import *

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

    def show_tokens(self):
        current_tokens = self.game_status.get_tokens()
        print(f"Current tokens : White-{current_tokens[0]}, Sky-{current_tokens[1]}, Green-{current_tokens[2]}, Red-{current_tokens[3]}, Brown-{current_tokens[4]}, Gold-{current_tokens[5]}")

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
                
        