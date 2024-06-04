from cmu_112_graphics import *
from foodClass import *
from ingredientClass import *

import time

# class of counters that keeps track of all the counters and whether or not 
# there is something on it; also keeps track of the location of the counter 
# in the grid and stored as row, col
class counter():
    def __init__(self, row, col, dish):
        self.row = row
        self.col = col
        self.dish = dish
    
    def getLocation(self):
        return (self.row, self.col)

# inheritance with counter being the super class
# ingredient counters at the front of the kitchen
class ingredientCounter(counter):
    def __init__(self, row, col, dish):
        super().__init__(row, col, dish)


# choppingBoard is the subclass that takes a dish and chops it up 
# returns the chopped ingredient
class choppingBoard(counter):
    def __init__(self, row, col, dish, image, app):
        super().__init__(row, col, dish)
        boardImage = scaleImage(app, image, app.dishSize)
        self.item = boardImage.transpose(Image.FLIP_LEFT_RIGHT)
        # above flip image from animations part 4 on the course link below:
        # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#flipImage
    
    # funciton to chop up the ingredient
    # called when the player is one from the chopping board 
    def chopIngredient(self):
        if self.dish != None and type(self.dish) == ingredient:
            self.dish.image = self.dish.allImages[self.dish.chopCounter]
        
# cooking counter
class cookingCounter(counter):
    def __init__(self, row, col, dish, image, app):
        super().__init__(row, col, dish)
        self.item = image
    
    def cook(self, app):
        app.cookingStarted = time.time()
        app.cookingTimeLeft = self.dish.cookingTime


# preparing counters 
class prepareCounter(counter):
    def __init__ (self, row, col, dish, image, app):
        super().__init__(row, col, dish)
        self.ingredientsList =  []
        self.item = scaleImage(app, image, app.dishSize)
        self.futureDish = None

# serving counters
class servingCounter(counter):
    def __init__(self, row, col, dish, image, app):
        super().__init__(row, col, dish)
        self.item = scaleImage(app, image, app.dishSize)

    def serve(self, app):
        if type(self.dish) == food:
            # serve the order by setting the specific order looked at to 
            # compelted and pop that order
            count = -1
            for i in range (len(app.orders)):
                if self.dish.name == app.orders[i].food.name:
                    app.orders[i].completed = True
                    self.dish = None
                    app.player.score += int(app.orders[i].getOrderScore())
                    count = i
                    break
            if count != -1:
                app.orders.pop(count)
                for i in range (count, len(app.orders)):
                    app.orders[i].orderNum -= 1
                app.numOfOrders = len(app.orders)
            return True
        return False


# returns a new scaled image given an image and the size needed
def scaleImage(app, original, size):
    originalWidth, originalHeight = original.size
    scale = size/originalWidth
    new = app.scaleImage(original, scale)
    return new