def cards_to_str(cards):
    dict_card = {0:"2",1:"3",2:"4",3:"5",4:"6",5:"7",6:"8",7:"9",8:"10",9:"J",10:"Q",11:"K",12:"A"}
    save = " "
    for card in cards:
        save = save + dict_card[card] + " "
    return save

class Player:
    
    BLACKJACK = 21
    
    def __init__(self, name="Player", money= 1000):
        self.name = name
        self.money = money
        self.hand = []
        self.sum = 0
        self.aces = 0
        self.bet = 0
        self.dealer_open = []
        
    def __str__(self):
        return f"{self.name}: Bet-{self.bet}, Cards-{cards_to_str(cards=self.hand)}, Sum - {self.max_sum()}"
    
    def dealer_info(self, dealer_open):
        self.dealer_open = dealer_open
        
    def is_bust(self):
        return self.sum - self.aces * 10 > 21
        
    def is_blackjack(self):
        return self.max_sum() == 21
        
    def max_sum(self):
        if not self.is_bust():
            toReturn = self.sum
            while toReturn > 21:
                toReturn -= 10
            return toReturn
        return -1
    
    def add_hand(self, card):
        self.hand.append(card)
        if card < 9:
            self.sum += card + 2
        elif card == 12:
            self.sum += 11
            self.aces += 1
        else:
            self.sum += 10

    def hit(self):
        pass
    
    def betting(self, money):
        self.bet += money
        self.money -= money
    
    def result(self, win=False, tie=False, display=False):
        if win:
            self.money += self.bet * 2
        if tie:
            self.money += self.bet
        self.aces = 0
        self.sum = 0
        self.bet = 0
        temp = self.hand 
        self.hand = []
        if display:
            if win:
                print(f"{self.name} wins!")
            elif tie:
                print("It's a tie!") 
            else:
                print(f"{self.name} lost!")
        return temp
        
class HumanPlayer(Player):
    
    def __init__(self, sname="HumanPlayer", smoney= 1000):
        super().__init__(name=sname, money=smoney)
    
    def hit(self):
        while True:
            answer = input("Do you want to hit? (y/n) : ").lower()
            if answer == "y":
                return True
            elif answer == "n":
                return False
            else: 
                pass

class NEATPlayer(Player):

    def __init__(self, sname="HumanPlayer", smoney= 1000, net=None):
        super().__init__(name=sname, money=smoney)
        self.net = net
        self.fitness = 0.0

    def get_fitness(self):
        return self.fitness
    
    def result(self, win=False, tie=False,display=False):
        if win:
            self.fitness += 1.0
        elif tie:
            self.fitness += 0.1
        else:
            self.fitness += 0.0
        return super().result(win, tie, display)
    
    def hit(self):
        inputs = [self.max_sum()/21.0, self.aces, self.dealer_open[0]]
        if self.net.activate(inputs)[0] > 0.5:
            return True
        else:
            return False
