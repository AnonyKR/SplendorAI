from .game_status import GameStatus

class Player:
    MAX_TOKEN = 10
    MAX_HOLD = 3

    def __init__(self):
        self.game_status = None

    def __str__(self):
        return "test"

    def update_game_status(self, game_status : GameStatus):
        self.game_status = game_status