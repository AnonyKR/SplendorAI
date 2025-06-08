from splendor.game import Game
#from splendor.player import *
from blackjack.blackjack import Blackjack
from blackjack.player import *
'''
game = Game(HumanPlayer(), HumanPlayer())
game.set_display()
game.play()
'''
game = Blackjack(display=True)
game.add_player(HumanPlayer())
game.playRound()