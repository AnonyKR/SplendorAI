from splendor.game import Game
from splendor.player import *

game = Game(HumanPlayer(), HumanPlayer())
game.set_display()
game.play()
