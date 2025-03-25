from .game_status import GameStatus

class Player:
    MAX_TOKEN = 10
    MAX_HOLD = 3

    def __init__(self):
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

    def get_tokens(self):
        return self.tokens
    
    def get_hold(self):
        return self.hold
    
    def get_card_tokens(self):
        return self.card_tokens
    
    def get_name(self):
        return self.name

    def get_points(self):
        return self.points