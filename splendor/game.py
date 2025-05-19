from .exception import *
from .player import *
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
        for player in self.players:
            player.update_game_status(self.game_status)
        
            
    def set_display(self):
        self.show = True
        self.display = Display(self.game_status)
    
    def play(self):
        while True:
            for turn_player in self.game_status.get_players():
                if self.show:
                    self.display.show_all() 
                turn_player.turn()
                input()
            if self.game_status.is_over():
                break


    def show_display(self):
        self.display.show_all()