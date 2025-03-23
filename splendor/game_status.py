from .exception import *
from .card import Card

import os

class GameStatus:

    def __init__(self, *args):
        GAME_WIN_POINT = 15
        if len(args) > 0:
            self.players = args[0]
            first_element = str(self.players[0])
        else:
            raise GameException
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "cardPreset.txt")
        preset = open(file_path, "r")
        presetSave = preset.readlines()
        preset.close()
        cardList = []
        for x in presetSave:
            cardList.append(x.strip)
        cardObjects = []
        for x in cardObjects:
            cardObjects.append(Card(int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), int(x[6]), int(x[7])))
        
        