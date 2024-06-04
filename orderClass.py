import time

# order class where it takes in a food
class order():
    def __init__(self, food, orderNum, app):
        self.food = food
        self.completed = False
        self.timeLimit = food.time
        self.orderNum = orderNum
        if app.gameStarted == True:
            self.timeStart = time.time()
        else:
            self.timeStart = None
        self.timePassed = 0
        self.timeLeft = self.timeLimit
    
    # get the score received from the order by passing in the time left when 
    # the order was completed
    def getOrderScore(self):
        if self.completed == False: # if the order was not completed
            return -self.food.score
        else:
            timeBonus = self.timeLeft/self.timeLimit*self.food.score
            return self.food.score + timeBonus

    def addScore(self, player):
        player.score += self.getOrderScore()