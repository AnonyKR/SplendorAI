class GameStatus:

    def __init__(self, *args):
        GAME_WIN_POINT = 15

        if len(args) > 0:
            self.players = args[0]
            first_element = str(self.players[0])
            print(f"First element: {first_element}")
        