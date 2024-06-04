from counterClass import *

# class for the AI mouse
class mouse():
    def __init__(self, app, image):
        image = scaleImage(app, image, app.dishSize*1.5)
        self.image = image
        self.carrying = None
    
    # find new possible position
    def findNewPosition(self, app):
        if closestCounter(app, app.mouseRow, app.mouseCol) != None:
            counterRow, counterCol = closestCounter(app, app.mouseRow, app.mouseCol)
            if type(app.floor[counterRow][counterCol]) == ingredientCounter:
                if len(app.mousePath) != 0:
                    lastRow, lastCol = app.mousePath[-1]
                    while lastRow > 0 and lastCol < app.cols:
                        lastRow, lastCol = app.mousePath[-1]
                        newLastRow, newLastCol = lastRow-1, lastCol
                        if newLastRow < 0 or app.floor[newLastRow][newLastCol] != None:
                            if lastCol+1 < app.cols:
                                newLastRow, newLastCol = lastRow, lastCol+1
                            else: 
                                break
                        app.mousePath.append((newLastRow, newLastCol)) 
                        app.mouseRow, app.mouseCol = newLastRow, newLastCol
                app.isMouseThere = False
                return
        dirs = [        (-1, 0),  
                (0, -1),        (0, +1),
                        (+1, 0)         ]
        # below are the two optimal choices
        bestDirs = [(+1, 0), (0, -1)]
        currRow, currCol = app.mouseRow, app.mouseCol
        for change in bestDirs:
            drow, dcol = change
            newRow, newCol = currRow+drow, currCol+dcol
            if newRow >= 0 and newRow < app.rows and newCol >= 0 and newCol < app.cols and isinstance(app.floor[newRow][newCol], counter) == False:
                app.mousePath.append((newRow, newCol))
                app.mouseRow, app.mouseCol = newRow, newCol
                break
        if app.isMouseThere == True:
            app.mouse.findNewPosition(app)


# returns a new scaled image given an image and the size needed
def scaleImage(app, original, size):
    originalWidth, originalHeight = original.size
    scale = size/originalWidth
    new = app.scaleImage(original, scale)
    return new

# returns the location of the closest counter given a row and a col
# None if no counter is in the front, back, left, or right of the cell at 
# currRow, currCol
# references wordSearchFromCellInDirection on course website below:
# https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html#wordsearch2
def closestCounter(app, currRow, currCol):
    dirs = [        (-1, 0),  
            (0, -1),        (0, +1),
                    (+1, 0)         ]
    for change in dirs:
        drow, dcol = change
        newRow, newCol = currRow+drow, currCol+dcol
        if newRow < 0 or newRow >= app.rows or newCol < 0 or newCol >= app.cols:
            continue
        else:
            if isinstance(app.floor[newRow][newCol], counter):
                return newRow, newCol
    return None