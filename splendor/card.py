def cardLoop(start, step):
    return (start + step) % 5

class Card:
    
    def __init__(self, level, token, point, white, blue, green, red, brown): 
        self.level = level
        self.token = token
        self.point = point
        self.cost = [white,blue,green,red,brown] # white, blue, green, red, brown