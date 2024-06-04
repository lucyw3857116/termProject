

# class of player that keeps track of the score of the player
class player():
    def __init__(self, app):
        self.carrying = None # not carrying anything
        self.score = 0

    # returns the type of item carried and the item carried
    def getCarrying(self):
        if self.carrying != None:
            return type(self.carrying), self.carrying

    # returns the score of the player for later display on ended screen
    def getPlayerScore(self):
        return self.score

    # repr function for printing out the score later
    def __repr__(self):
        return f'{self.score}'