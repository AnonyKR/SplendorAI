from .exception import *
from .player import Player
from .game_status import GameStatus

class Game:
    MIN_PLAYER = 2
    MAX_PLAYER = 4

    def __init__(self, *args):
        self.players = tuple(args)
        if len(self.players) > Game.MAX_PLAYER | len(self.players) < Game.MIN_PLAYER:
            raise GameException()
        for player in self.players:
            if not isinstance(player, Player):
                raise GameException()
        self.game_status = GameStatus(self.players)
            
    def play(self):
        print() #placeholder