import time

# ingredient class where it takes in an image for the ingredient as a string
# of the name of the file
class ingredient():
    def __init__(self, app, name, images, cookingTime):
        image = scaleImage(app, images[0], app.dishSize)
        self.name = name
        self.image = image
        self.allImages = images
        self.cookingTime = cookingTime
        self.ingredientCooked = False
        self.chopCounter = 0


# helper function
# returns a new scaled image given an image and the size needed
def scaleImage(app, original, size):
    originalWidth, originalHeight = original.size
    scale = size/originalWidth
    new = app.scaleImage(original, scale)
    return new