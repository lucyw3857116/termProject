import time

# food class where it takes in the name of the food, an image for the food as a 
# string of the name of the file, a list of ingredients needed, the time limit 
# for completing the food, and the score that the food will give the player if
# it is succesfully cooked
class food():
    def __init__(self, app, name, image, ingredients, time, score):
        self.name = name
        self.image = scaleImage(app, image, app.dishSize)
        self.ingredients = ingredients
        self.time = time
        self.score = score

# returns a new scaled image given an image and the size needed
def scaleImage(app, original, size):
    originalWidth, originalHeight = original.size
    scale = size/originalWidth
    new = app.scaleImage(original, scale)
    return new