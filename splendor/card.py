class Card:
    
    def __init__(self, level, token, point, white, blue, green, red, brown): 
        self.level = level
        self.token = token
        self.point = point
        self.cost = [white,blue,green,red,brown] # white, blue, green, red, brown
    
    def get_level(self):
        return self.level

class Noble:

    def __init__(self, white, blue, green,red,brown):
        self.cost = [white,blue,green,red,brown]