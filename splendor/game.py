from .exception import *
from .player import Player
from .game_status import GameStatus
from .display import Display

class Game:
    MIN_PLAYER = 2
    MAX_PLAYER = 4

    def __init__(self, *args):
        self.show = False
        self.players = tuple(args)
        if len(self.players) > Game.MAX_PLAYER | len(self.players) < Game.MIN_PLAYER:
            raise GameException()
        for player in self.players:
            if not isinstance(player, Player):
                raise GameException()
        self.game_status = GameStatus(self.players)
            
    def set_display(self):
        self.show = True
        self.display = Display(self.game_status)
    
    def play(self):
        print() #placeholder

    def show_display(self):
        self.display.show_all()