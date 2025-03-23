from .exception import *
from .card import *

import os
import random

class GameStatus:
    GAME_WIN_POINT = 15

    def __init__(self, *args):
        #check number of players and tokens used
        if len(args) > 0:
            self.players = args[0]
            match (len(self.players)):
                case 2:
                    self.tokens = [4,4,4,4,4,5]
                case 3:
                    self.tokens = [5,5,5,5,5,5]
                case 4:
                    self.tokens = [7,7,7,7,7,5]
                case _:
                    raise GameException
        else:
            raise GameException
        #set up cards to be used
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "cardPreset.txt")
        preset = open(file_path, "r")
        presetSave = preset.readlines()
        preset.close()
        cardList = []
        for x in presetSave:
            cardList.append(x.strip())
        cardObjects = []
        for x in cardList:
            cardObjects.append(Card(int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), int(x[6]), int(x[7])))
        #split cards into each deck for level 1,2,3
        self.cards = [[],[],[]] #level 3, level 2, level 1
        for x in cardObjects:
            cardLevel = x.get_level()
            match (cardLevel):
                case 1:
                    self.cards[2].append(x)
                case 2:
                    self.cards[1].append(x)
                case 3:
                    self.cards[0].append(x)
        random.shuffle(self.cards[0])
        random.shuffle(self.cards[1])
        random.shuffle(self.cards[2])
        self.opens = [[],[],[]]
        for x in range(0,4):
            self.opens[0].append(self.cards[0].pop())
            self.opens[1].append(self.cards[1].pop())
            self.opens[2].append(self.cards[2].pop())
        #set up noble tiles
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "noble.txt")
        preset = open(file_path, "r")
        presetSave = preset.readlines()
        preset.close()
        nobleList = []
        for x in presetSave:
            nobleList.append(x.strip())
        noblesObjects = []
        for x in nobleList:
            noblesObjects.append(Noble(int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4])))
        random.shuffle(noblesObjects)
        self.noble_used = []
        for x in range(0, len(self.players) + 1):
            self.noble_used.append(noblesObjects.pop())
        