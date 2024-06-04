import math
import time
import random
import copy

# import different files for classes
from ingredientClass import *
from foodClass import *
from orderClass import *
from counterClass import *
from playerClass import *
from mouseClass import *

from cmu_112_graphics import *

# utilized cmu 112 graphics for multiple functions in this term project

##########################################
# helper funtions
##########################################

# round to nearest with ties going away from zero
def roundHalfUp(d):
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
# above helper function pasted from part 10 of link:
# https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html

# returns a new scaled image given an image and the size needed
def scaleImage(app, original, size):
    originalWidth, originalHeight = original.size
    scale = size/originalWidth
    new = app.scaleImage(original, scale)
    return new


# checks if the player's next movement is a legal move
def isLegalMove(app):
    app.chefFeetX, app.chefFeetY = app.chefX, app.chefY+app.charHeight/2
    rowFeet, colFeet = getCell(app, app.chefFeetX, app.chefFeetY)
    row, col = getCell(app, app.chefX, app.chefY)
    if row >= app.rows-1 or row < 0 or col >= app.cols-1 or col < 0:
        return False
    elif app.floor[row][col] != None:
        return False
    elif app.floor[0][col] != None and rowFeet == 1:
        return False
    return True

# get cell bounds for the floor
# takes in the row and the col and gets the bounds of the cell 
# similar to the function getCellBounds from the website below:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# returns a list of four points (tuples) from bottom most point clockwise
def getCellBounds(app, r, c):
    xRight = app.width-app.margin # right most point
    xLeft = app.margin # left most point
    y0 = app.height/2
    x = app.width/2
    y = 200
    xNew = x*(math.cos(math.pi/4)) - y*(math.cos(math.pi/6))
    yNew = x*(math.sin(math.pi/4)) + y*(math.sin(math.pi/6))
    # above formulas from an image from TP mentor Bonnie Guo, which is from the 
    # video in the link:
    # https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=5226ea89-b987
    # -4458-9056-acfc017c6167
    dx = xNew-x 
    dy = yNew-y
    cellScale = 1/app.rows
    dx = dx * cellScale
    dy = dy * cellScale
    
    xBottom = xRight + dx*(r+c+1)
    yBottom = y0 + dy*(r+1) - dy*c

    xLeft = xBottom + dx
    yLeft = yBottom - dy

    xTop = xBottom
    yTop = yBottom - dy*2

    xRight = xLeft - dx*2
    yRight = yLeft

    return [(xBottom, yBottom), (xLeft, yLeft), (xTop, yTop), (xRight, yRight)]

# get cell for the floor
# uses a certain location (x and y value) and return the row and the col that 
# that the location is in
def getCell(app, currX, currY):
    xRight = app.width-app.margin # right most point
    xLeft = app.margin # left most point
    y0 = app.height/2
    x = app.width/2
    y = 200
    xNew = x*(math.cos(math.pi/4)) - y*(math.cos(math.pi/6))
    yNew = x*(math.sin(math.pi/4)) + y*(math.sin(math.pi/6))
    # above formulas from an image from TP mentor Bonnie Guo, which is from the 
    # video in the link:
    # https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=5226ea89-b987
    # -4458-9056-acfc017c6167
    dx = xNew-x 
    dy = yNew-y
    xMid = xRight + dx # mid-point
    yBottom = y0 + dy # lowest point
    yMid = y0 - dy # center middle pointa and top of left and right
    yMidTop = yMid - dy # highest point
    cellScale = 1/app.rows
    dx = dx * cellScale
    dy = dy * cellScale
    
    cellSide = (dx**2 + dy**2)**0.5

    lineForRow = xRight, y0, xMid, yMid
    lineForCol = xRight, y0, xMid, yBottom
    row = distanceLinePoint(xRight, y0, xMid, yMid, currX, currY)/cellSide + 1
    col = distanceLinePoint(xRight, y0, xMid, yBottom, currX, currY)/cellSide
    row = int(row)
    col = int(col)
    # returns None if out of bound
    return row, col
    
# get the shortest distance between a line and a point
# pass in two points of a line and the point wanted
def distanceLinePoint(lineX0, lineY0, lineX1, lineY1, pointX, pointY):
    a = (lineY1-lineY0)/(lineX1-lineX0)
    b = -1
    c = lineY0-(lineY1-lineY0)/(lineX1-lineX0)*lineX0
    # below formula of distance between line and point from link:
    # https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
    distance = abs(a*pointX + b*pointY + c)/((a**2+b**2)**0.5)
    return distance

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

# get the center coordinates of a cell
def getCellCenter(app, r, c):
    points = getCellBounds(app, r, c)
    xBottom, yBottom = points[0]
    xLeft, yLeft = points[1]
    xTop, yTop = points[2]
    xRight, yRight = points[3]
    return (xLeft + xRight)/2, (yBottom + yTop)/2

# returns the distance between two points
def findDistance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**0.5

##########################################
# main app
##########################################

def appStarted(app):
    app.width = 750
    app.height = 750
    app.margin = 100
    app.chefX, app.chefY = app.width/2, app.height/2
    app.stepSize = 15
    app.direction = 'front'
    app.rows, app.cols = 8, 8
    # column one is right most and last column is leftmost
    app.floor = [([None] * (app.cols)) for i in range (app.rows)]

    app.spritestripOriginal = app.loadImage('retro character 2.png') # 614 * 800
    # link for photo above:
    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.freeimages.com%2Fve
    # ctor%2Fretro-character-sprite-sheet-5269982&psig=AOvVaw0u_2NTyr6_wTfIpCm_5
    # uy7&ust=1668983133231000&source=images&cd=vfe&ved=0CA4QjRxqFwoTCNiV1ueku_s
    # CFQAAAAAdAAAAABAE
    app.spritestrip = app.scaleImage(app.spritestripOriginal, 1/3) # 409.3 * 533
    app.imageWidth, app.imageHeight = app.spritestrip.size
    app.charWidth, app.charHeight = app.imageWidth/4, app.imageHeight/4
    app.sprites = dict()
    app.sprites['front'] = []
    app.sprites['right'] = []
    app.sprites['left'] = []
    app.sprites['back'] = []
    for c in range(4):
        # crop front animation
        sprite = app.spritestrip.crop(((c*app.charWidth), 0,
                        (c+1)*app.charWidth - 2, app.charHeight - 2))
        app.sprites['front'].append(sprite)
        # crop right animation
        sprite = app.spritestrip.crop(((c*app.charWidth), app.charHeight,
                        (c+1)*app.charWidth - 2, 2*app.charHeight))
        app.sprites['right'].append(sprite)
        # crop the left animation
        sprite = app.spritestrip.crop(((c*app.charWidth) + 2, 2*app.charHeight,
                        (c+1)*app.charWidth - 2, 3*app.charHeight))
        app.sprites['left'].append(sprite)
        # crop the back animation
        sprite = app.spritestrip.crop(((c*app.charWidth), 3*app.charHeight + 2,
                        (c+1)*app.charWidth - 2, 4*app.charHeight))
        app.sprites['back'].append(sprite)
    app.spriteCounter = 0
    app.chefFeetX, app.chefFeetY = app.chefX, app.chefY + app.charHeight/2
    app.gameStarted = False
    app.gameEnded = False
    app.dishSize = 50
    app.orders = []
    app.numOfOrders = len(app.orders)

    # declare the images of items
    app.boardImage = app.loadImage('chopping board.png')
    # link for the photo above:
    # https://cdn4.iconfinder.com/data/icons/objects-3-2/50/194-512.png

    app.plateImage = app.loadImage('plate.png')
    # link for the photo above:
    # https://banner2.cleanpng.com/20181124/apr/kisspng-plastic-dinner-plates-ta
    # bleware-plastic-dinner-pla-diva-la-opala-ivory-5bf8e6b010e817.834594521543
    # 0386400693.jpg

    app.panImage = app.loadImage('pan.png')
    # link for the photo above:
    # https://banner2.cleanpng.com/20180616/qbo/kisspng-frying-pan-royalty-free-
    # photography-clip-art-food-draw-5b24a291817502.5625270115291275695303.jpg

    # all chopped images of ingredients are created from the original imported image

    # declare the ingredients for a salad and the salad itself

    app.lettuce = ingredient(app,'lettuce', [app.loadImage('lettuce.tiff')], 
                            None)
    # link for the photo above:
    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fovercooked.fandom.com%2F
    # wiki%2FSalad&psig=AOvVaw1Sufp8brxV_xkUqKziQjpN&ust=1669045290084000&source
    # =images&cd=vfe&ved=0CA8QjRxqFwoTCLDH_q-MvfsCFQAAAAAdAAAAABAP
    app.tomato = ingredient(app, 'tomato', 
                [app.loadImage('tomato.webp'), 
                app.loadImage('tomato chopped 1.tiff'),
                app.loadImage('tomato chopped 2.tiff'), 
                app.loadImage('tomato chopped 3.tiff')], 3)
    # link for the photo above:
    # https://static.wikia.nocookie.net/overcooked/images/3/3f/Tomato_Transparen
    # t.png/revision/latest/top-crop/width/360/height/360?cb=20180805025547
    app.cucumber = ingredient(app, 'cucumber', 
                [app.loadImage('cucumber.png'), app.loadImage('cucumber chopped 1.png'),
                app.loadImage('cucumber chopped 2.png'), 
                app.loadImage('cucumber chopped 3.png')], None)
    # link for the photo above:
    # https://static.wikia.nocookie.net/overcooked/images/c/c1/Cucumber_Icon.png
    # /revision/latest?cb=20220228010157
    app.salad = food(app, 'salad', app.loadImage('salad.png'), 
                    [app.lettuce, app.tomato, app.cucumber], 60, 100)
    # link for the photo above:
    # https://static.wikia.nocookie.net/overcooked/images/7/7e/Salad.png/revisio
    # n/latest/smart/width/250/height/250?cb=20180830221157

    # declare the ingredients for the burger and the burger itself

    app.bun = ingredient(app, 'bun', [app.loadImage('bun.png')], None)
    # link for the photo above:
    # https://static.wikia.nocookie.net/overcooked/images/1/1d/Bun_Icon.png/revi
    # sion/latest?cb=20220213140343
    app.beef = ingredient(app, 'beef', 
                [app.loadImage('beef.png'), app.loadImage('beef chopped 1.png'),
                app.loadImage('beef chopped 2.png'), 
                app.loadImage('beef chopped 3.png')], 5)
    # link for the photo above:
    # https://static.wikia.nocookie.net/overcooked/images/2/2f/Meat_Icon.png/rev
    # ision/latest/top-crop/width/360/height/360?cb=20220213140142
    app.cheese = ingredient(app, 'cheese', 
                [app.loadImage('cheese.png'), app.loadImage('cheese chopped 1.png'),
                app.loadImage('cheese chopped 2.png'), 
                app.loadImage('cheese chopped 3.png')], None)
    # link for the photo above:
    # https://static.wikia.nocookie.net/overcooked/images/1/1a/Cheese_Transparen
    # t.png/revision/latest/smart/width/250/height/250?cb=20220213141328
    app.hamburger = food(app, 'hamburger', app.loadImage('hamburger.webp'),
                    [app.bun, app.beef, app.cheese], 90, 200)
    # link for the photo above:
    # https://static.wikia.nocookie.net/overcooked/images/2/2a/O2_Burger_Icon.pn
    # g/revision/latest?cb=20180830221242

    # randomly generate the first order
    app.foodChoices = [app.salad, app.hamburger]
    choice = random.randint(0, 1)
    app.orders.append(order(app.foodChoices[choice], app.numOfOrders, app))
    app.numOfOrders = len(app.orders)

    app.allIngredients = [app.lettuce, app.tomato, app.cucumber, app.bun, 
                        app.beef, app.cheese]

    # declare the locations of all the counters and the initial dishes they have
    app.counters = []
    # back right counters
    app.counters.append(choppingBoard(0, 0, None, app.boardImage, app))
    app.counters.append(cookingCounter(0, 1, None, app.panImage, app))
    app.counters.append(counter(0, 2, None))
    app.counters.append(prepareCounter(0, 3, None, app.plateImage, app))
    app.counters.append(prepareCounter(0, 4, None, app.plateImage, app))
    # front most counters
    for i in range(len(app.allIngredients)):
        app.counters.append(ingredientCounter(app.cols-1, i, 
                            app.allIngredients[i]))

    # middle counters
    app.counters.append(counter(3, 7, None))
    app.counters.append(servingCounter(3, 6, None, app.plateImage, app))
    app.counters.append(servingCounter(3, 5, None, app.plateImage, app))
    app.counters.append(servingCounter(3, 4, None, app.plateImage, app))

    # set counter in the 2d list of floor
    for counterItem in app.counters:
        r, c = counterItem.getLocation()
        app.floor[r][c] = counterItem

    app.player = player(app)
    app.duration = 0
    app.timePerOrder = 40
    
    app.cookingStarted = False
    app.cookingDuration = 0
    app.cooked = False

    app.isMouseThere = True # is mouse at the original spawned position
    app.drawMouseChar = False
    app.timePerMouse = 30
    app.mouseSpeed = 1
    app.mouseStep = 0
    app.mousePresent = True

    # randomly generate mouse location
    randomRow, randomCol = random.randint(0, 7), random.randint(0, 7)
    while isinstance(app.floor[randomRow][randomCol], counter):
        randomRow, randomCol = random.randint(0, 7), random.randint(0, 7)
    app.mouseRow, app.mouseCol = randomRow, randomCol


    # find app.mouseX and app.mouseY
    app.mouseX, app.mouseY = getCellCenter(app, app.mouseRow, app.mouseCol)
    app.mouse = mouse(app, app.loadImage('mouse.png'))
    app.mousePath = []

# timerFired inspired by part 10 in the link:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

def timerFired(app):
    if app.gameStarted == True and app.gameEnded == False:
        # count the time passed since the game has started
        app.duration = roundHalfUp(time.time() - app.time0)
        app.count = roundHalfUp(time.time()-app.time1)
        app.mouseCount = roundHalfUp(time.time()-app.time2)
        if app.duration > 300000:
            app.gameEnded = True
        elif app.count == app.timePerOrder and app.numOfOrders < 5:
            app.foodChoices = [app.salad, app.hamburger]
            choice = random.randint(0, 1)
            app.orders.append(order(app.foodChoices[choice], app.numOfOrders, 
                                    app))
            app.numOfOrders = len(app.orders)
            app.time1 = time.time()
        elif app.mouseCount == app.timePerMouse:
            app.isMouseThere = True
            app.drawMouseChar = True
            app.mouseStep = 0
            app.mousePresent = True
            app.mouse.carrying = None
            app.mousePath = []
            randomRow, randomCol = random.randint(0, 7), random.randint(0, 7)
            while isinstance(app.floor[randomRow][randomCol], counter):
                randomRow, randomCol = random.randint(0, 7), random.randint(0, 7)
            app.mouseRow, app.mouseCol = randomRow, randomCol
            app.mouseX, app.mouseY = getCellCenter(app, app.mouseRow, 
                                                    app.mouseCol)
            app.time2 = time.time()

        for orderItem in app.orders:
            if orderItem.timeStart == None:
                orderItem.timeStart = time.time()
    
        # pass in a mouse
        if app.mousePresent == True:
            app.drawMouseChar = True
            if app.isMouseThere == True:
                app.mouse.findNewPosition(app)
                app.mouseTime0 = time.time()
            else:
                app.stepDuration = roundHalfUp(time.time() - app.mouseTime0)
                if app.stepDuration == app.mouseSpeed and \
                    app.mouseStep < len(app.mousePath):
                    currRow, currCol = app.mousePath[app.mouseStep]
                    app.mouseX, app.mouseY = getCellCenter(app, currRow, 
                                                currCol)
                    app.mouseStep+=1
                    app.mouseTime0 = time.time()
                    if closestCounter(app, currRow, currCol) != None:
                        counterRow, counterCol = closestCounter(app, currRow, 
                                                currCol)
                        if type(app.floor[counterRow][counterCol]) == \
                            ingredientCounter:
                            app.mouse.carrying = app.floor[counterRow][counterCol].dish
                if app.mouseStep >= len(app.mousePath):
                    app.timeDisappear = roundHalfUp(time.time() - app.mouseTime0)
                    if app.timeDisappear == app.mouseSpeed*2:
                        app.mousePresent = False
                        app.drawMouseChar = False
                        app.mouseStep = 0
                        app.player.score -= 5

        # update timeLeft for passed in orders
        for orderItem in app.orders:
            orderItem.timePassed = roundHalfUp(time.time()-orderItem.timeStart)
            orderItem.timeLeft = orderItem.timeLimit-orderItem.timePassed
            if orderItem.timeLeft <= 0:
                orderItem.completed == False
                app.player.score += int(orderItem.getOrderScore())
                index = app.orders.index(orderItem)
                app.orders.pop(index)
                for i in range (index, len(app.orders)):
                    app.orders[i].orderNum -= 1
                app.numOfOrders = len(app.orders)

        # time for cooking
        if app.cookingStarted != False:
            app.cookingDuration = roundHalfUp(time.time() - app.cookingStarted)
            if app.cookingDuration > app.cookingTimeLeft:
                app.cooked = True
                for r in range (app.rows):
                    for c in range (app.cols):
                        if type(app.floor[r][c]) == cookingCounter and \
                            app.floor[r][c].dish != None:
                            app.floor[r][c].dish.ingredientCooked = True
                            app.cookingStarted = False
                            app.cookingDuration = 0
                            app.player.carrying = app.floor[r][c].dish
                            app.floor[r][c].dish = None

    else:
        app.time0 = time.time()
        app.time1 = time.time()
        app.time2 = time.time()


def keyPressed(app, event):
    if app.gameStarted == True:
        xNew = app.stepSize*(math.cos(math.pi/4)) - app.stepSize*(
            math.cos(math.pi/6))
        yNew = app.stepSize*(math.sin(math.pi/4)) + app.stepSize*(
            math.sin(math.pi/6))
        dx = xNew-app.stepSize
        dy = yNew-app.stepSize
        # arrow keys to make the chef move around
        if event.key == 'Up':
            app.direction = 'back'
            app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
            app.chefX -= dx/2
            app.chefY -= dy*2
            if isLegalMove(app) == False:
                app.chefX += dx/2
                app.chefY += dy*2
        elif event.key == 'Down':
            app.direction = 'front'
            app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
            # 2.5D movement
            app.chefX += dx/2
            app.chefY += dy*2
            if isLegalMove(app) == False:
                app.chefX -= dx/2
                app.chefY -= dy*2
        elif event.key == 'Left':
            app.direction = 'left'
            app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
            # 2.5D movement
            app.chefX += dx
            app.chefY -= dy*2
            if isLegalMove(app) == False:
                app.chefX -= dx
                app.chefY += dy*2
        elif event.key == 'Right':
            app.direction = 'right'
            app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
            # 2.5D movement
            app.chefX -= dx
            app.chefY += dy*2
            if isLegalMove(app) == False:
                app.chefX += dx
                app.chefY -= dy*2
        # test game lost page which would later be activated when a certain 
        # amount of time has elapsed
        if event.key == 'l':
            app.gameEnded = True
        # click d to drop the food currently held
        if event.key == 'd':
            if app.player.carrying != None:
                # if the counter in 1 block of the player the dish is empty
                # set the counter dish to the dish the player is carrying
                currRow, currCol = getCell(app, app.chefX, app.chefY)
                if closestCounter(app, currRow, currCol) != None:
                    counterX, counterY = closestCounter(app, currRow, currCol)
                    currCounter = app.floor[counterX][counterY]
                    # player tries to drop off ingredient at serving counter, pass
                    if type(app.player.carrying) != food and \
                        type(currCounter) == servingCounter:
                        pass
                    # drops off at ingredient counter does not change what is 
                    # on the counter
                    elif type(currCounter) == ingredientCounter:
                        app.player.carrying = None
                    # drop off ingredient at prepare counter
                    elif type(currCounter) == prepareCounter and \
                        type(app.player.carrying) == ingredient:
                        # check that there are no repeating ingredients
                        if len(currCounter.ingredientsList) != 0:
                            isIn = False
                            for ingredientItem in currCounter.ingredientsList:
                                if app.player.carrying.name == ingredientItem.name:
                                    isIn = True
                            if isIn == False:
                            # check to see if the new dropped ingredient match
                            # the current ingredients to make a valid food
                                for futureDishIngredient in \
                                    currCounter.futureDish.ingredients:
                                    if app.player.carrying.name == \
                                        futureDishIngredient.name:
                                        currDish = app.player.carrying
                                        if (len(currDish.allImages) != 1 and \
                                            currDish.chopCounter != 3) or \
                                            (currDish.cookingTime != None and \
                                                currDish.ingredientCooked == False):
                                            pass
                                        else:
                                            currCounter.ingredientsList.append(app.player.carrying)
                                            app.player.carrying = None
                                            break
                        else: 
                            currDish = app.player.carrying
                            if (len(currDish.allImages) != 1 and \
                                currDish.chopCounter != 3) or \
                                (currDish.cookingTime != None and \
                                    currDish.ingredientCooked == False):
                                    pass
                            else:
                                currCounter.ingredientsList.append(app.player.carrying)
                                app.player.carrying = None
                    elif type(currCounter) == cookingCounter:
                        if app.player.carrying.cookingTime != None:
                            currCounter.dish = app.player.carrying
                            app.player.carrying = None
                            currCounter.cook(app)
                    elif type(currCounter) == choppingBoard and \
                        (len(app.player.carrying.allImages) == 1 or \
                            type(app.player.carrying) == food):
                        pass
                    # drop off at regular counter
                    else:
                        currCounter.dish = app.player.carrying
                        app.player.carrying = None
                # drop the food on the ground
                else:
                    app.player.carrying = None
                    app.player.score -= 10

        # click c to pick up a dish
        if event.key == 'c':
            currRow, currCol = getCell(app, app.chefX, app.chefY)
            if closestCounter(app, currRow, currCol) != None:
                counterX, counterY = closestCounter(app, currRow, currCol)
                currCounter = app.floor[counterX][counterY]
                if type(currCounter) == ingredientCounter:
                    app.player.carrying = copy.copy(currCounter.dish)
                # if the counter is a cooking counter and the food is not done
                elif type(currCounter) == cookingCounter and app.cooked == True:
                    app.player.carrying = currCounter.dish
                    currCounter.dish = None
                elif type(currCounter) != ingredientCounter and \
                    type(currCounter) != cookingCounter:
                    app.player.carrying = currCounter.dish
                    currCounter.dish = None
                if type(currCounter) == prepareCounter and \
                    len(currCounter.ingredientsList) == 1:
                    app.player.carrying = currCounter.ingredientsList[0]
                    currCounter.futureDish = None
                    currCounter.ingredientsList.pop()

        # click r to reset the counter to empty
        if event.key == 'r':
            currRow, currCol = getCell(app, app.chefX, app.chefY)
            if closestCounter(app, currRow, currCol) != None:
                counterX, counterY = closestCounter(app, currRow, currCol)
                currCounter = app.floor[counterX][counterY]
                if type(currCounter) != ingredientCounter:
                    currCounter.dish = None
                if (type(currCounter) == prepareCounter and \
                    len(currCounter.ingredientsList) != 0) or \
                        currCounter.dish != None:
                    currCounter.dish = None
                    currCounter.ingredientsList = []
        
        # click s to serve all the food you can serve on the serving counters
        if event.key == 's':
            for r in range(app.rows):
                for c in range(app.cols):
                    currCounter = app.floor[r][c]
                    if type(app.floor[r][c]) == servingCounter:
                        if currCounter.dish != None:
                            if currCounter.serve(app):
                                currCounter.serve(app)
        
        # click the space bar to chop ingredinets
        if event.key == 'Space':
            currRow, currCol = getCell(app, app.chefX, app.chefY)
            if closestCounter(app, currRow, currCol) != None:
                counterX, counterY = closestCounter(app, currRow, currCol)
                currCounter = app.floor[counterX][counterY]
                if type(currCounter) == choppingBoard and \
                    currCounter.dish != None and \
                        type(currCounter.dish) == ingredient:
                    if currCounter.dish.chopCounter < 3:
                        currCounter.dish.chopCounter += 1
                        currCounter.chopIngredient()


    else:
        if event.key == 'Return':
            app.gameStarted = True

##########################################
# draw functions
##########################################

# draw the chef
def drawChef(app, canvas):
    sprite = app.sprites[app.direction][app.spriteCounter]
    canvas.create_image(app.chefX, app.chefY, image=ImageTk.PhotoImage(sprite))
    # pick up dishes
    chefRow, chefCol = getCell(app, app.chefX, app.chefY+app.charHeight/2)
    if app.player.getCarrying() != None:
        dishType, dish = app.player.getCarrying()
        dishX = app.chefX
        dishY = (app.chefY + app.charHeight/2 + app.chefY)/2
        if dishType == ingredient:
            drawIngredient(app, canvas, dish, dishX, dishY, 25)
        elif dishType == food:
            drawFood(app, canvas, dish, dishX, dishY, 25)

# draw the mouse
def drawMouse(app, canvas):
    canvas.create_image(app.mouseX, app.mouseY, 
                        image=ImageTk.PhotoImage(app.mouse.image))
    if app.mouse.carrying != None and type(app.mouse.carrying) == ingredient:
        dishX = app.mouseX
        dishY = app.mouseY
        drawIngredient(app, canvas, app.mouse.carrying, dishX, dishY, 25)

# draw the background of the kitchen (hardcoded)
def drawBackground(app, canvas):
    xRight = app.width-app.margin # right most point
    xLeft = app.margin # left most point
    y0 = app.height/2
    x = app.width/2
    y = 200
    xNew = x*(math.cos(math.pi/4)) - y*(math.cos(math.pi/6))
    yNew = x*(math.sin(math.pi/4)) + y*(math.sin(math.pi/6))
    # above formulas from an image from TP mentor Bonnie Guo, which is from the 
    # video in the link:
    # https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=5226ea89-b987
    # -4458-9056-acfc017c6167
    # dotSize = 10
    dx = xNew-x 
    dy = yNew-y
    xMid = xRight + dx # mid-point
    yBottom = y0 + dy # lowest point
    yMid = y0 - dy # center middle pointa and top of left and right
    yMidTop = yMid - dy # highest point

    # draw the bottom part of the kitchen
    canvas.create_line(xRight, y0, xMid, yBottom)
    canvas.create_line(xLeft, y0, xMid, yBottom)

    # draw the top part of the kitchen
    canvas.create_line(xRight, y0, xMid, yMid)
    canvas.create_line(xLeft, y0, xMid, yMid)
    canvas.create_line(xLeft, yMid, xMid, yMidTop)
    canvas.create_line(xRight, yMid, xMid, yMidTop)
    canvas.create_line(xLeft, y0, xLeft, yMid)
    canvas.create_line(xMid, yMid, xMid, yMidTop)
    canvas.create_line(xRight, y0, xRight, yMid)

    # fill in the floor
    canvas.create_polygon(xLeft, y0, xMid, yMid, xRight, y0, xMid, yBottom,
                        fill = 'purple4', outline = 'white', width = 3)
    # fill in the walls
    canvas.create_polygon(xLeft, y0, xLeft, yMid, xMid, yMidTop, xMid, yMid, 
                        fill = 'MediumPurple1', outline = 'white', width = 3)
    canvas.create_polygon(xMid, yMid, xMid, yMidTop, xRight, yMid, xRight, y0,
                        fill = 'MediumPurple1', outline = 'white', width = 3 )
# -----------------------------------------------------------------------------
    # # draw the cells on the floor
    cellSize = 1/app.rows
    dx = dx * cellSize # dx is negative
    dy = dy * cellSize
    for r in range (app.rows):
        for c in range(app.cols):
            points = getCellBounds(app, r, c)
            xBottom, yBottom = points[0]
            xLeft, yLeft = points[1]
            xTop, yTop = points[2]
            xRight, yRight = points[3]
            canvas.create_polygon(xBottom, yBottom, xLeft, yLeft, 
                            xTop, yTop, xRight, yRight, 
                            fill = 'purple4', outline = 'white', width = 3)

# -----------------------------------------------------------------------------
# draw the counters
def drawCounterFronts(app, canvas):
    xRight = app.width-app.margin # right most point
    xLeft = app.margin # left most point
    y0 = app.height/2
    x = app.width/2
    y = 200
    xNew = x*(math.cos(math.pi/4)) - y*(math.cos(math.pi/6))
    yNew = x*(math.sin(math.pi/4)) + y*(math.sin(math.pi/6))
    # above formulas from an image from TP mentor Bonnie Guo, which is from the 
    # video in the link:
    # https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=5226ea89-b987
    # -4458-9056-acfc017c6167
    dx = xNew-x 
    dy = yNew-y
    cellSize = 1/app.rows
    dx = dx * cellSize # dx is negative
    dy = dy * cellSize
    for r in range(app.rows):
        for c in range(app.cols):
            if isinstance(app.floor[r][c], counter):
                # get the front bottom right corner of the counter
                # same calculation as xBottomR and yBottomR

                # set the color apart if it is a serving counter:
                if type(app.floor[r][c]) == servingCounter:
                    color = 'AntiqueWhite'
                else: 
                    color = 'thistle'

                points = getCellBounds(app, r, c)
                counterBottomRX = points[0][0]
                counterBottomRY = points[0][1]
                # calculate the other points of the counter from the above point
                counterBottomLX = points[1][0]
                counterBottomLY = points[1][1]
                counterTopRX = counterBottomRX
                counterTopRY = counterBottomRY - dy*2
                counterTopLX = counterBottomLX
                counterTopLY = counterBottomLY - dy*2
                # draw the front of the counter
                canvas.create_polygon(counterBottomRX, counterBottomRY,  
                                    counterTopRX, counterTopRY, 
                                    counterTopLX, counterTopLY, 
                                    counterBottomLX, counterBottomLY,
                                    fill = f'{color}2', outline = 'white',
                                    width = 3)

def drawCounterTopsAndSides(app, canvas):
    xRight = app.width-app.margin # right most point
    xLeft = app.margin # left most point
    y0 = app.height/2
    x = app.width/2
    y = 200
    xNew = x*(math.cos(math.pi/4)) - y*(math.cos(math.pi/6))
    yNew = x*(math.sin(math.pi/4)) + y*(math.sin(math.pi/6))
    # above formulas from an image from TP mentor Bonnie Guo, which is from the 
    # video in the link:
    # https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=5226ea89-b987
    # -4458-9056-acfc017c6167
    dx = xNew-x 
    dy = yNew-y
    cellSize = 1/app.rows
    dx = dx * cellSize # dx is negative
    dy = dy * cellSize
    
    for r in range(app.rows):
        for c in range(app.cols):
            if isinstance(app.floor[r][c], counter):
                # get the front bottom right corner of the counter
                # same calculation as xBottomR and yBottomR

                # set the color apart if it is a serving counter:
                if type(app.floor[r][c]) == servingCounter:
                    color = 'AntiqueWhite'
                else: 
                    color = 'thistle'

                points = getCellBounds(app, r, c)
                counterBottomRX = points[0][0]
                counterBottomRY = points[0][1]
                # calculate the other points of the counter from the above point
                counterBottomLX = points[1][0]
                counterBottomLY = points[1][1]
                counterTopRX = counterBottomRX
                counterTopRY = counterBottomRY - dy*2
                counterTopLX = counterBottomLX
                counterTopLY = counterBottomLY - dy*2
                # draw the top of the counter
                counterBackRX = counterTopRX - dx
                counterBackRY = counterTopLY
                counterBackLX = counterTopRX
                counterBackLY = counterTopRY - dy*2
                canvas.create_polygon(counterBackRX, counterBackRY, 
                                    counterBackLX, counterBackLY, 
                                    counterTopLX, counterTopLY, 
                                    counterTopRX, counterTopRY, 
                                    fill = f'{color}1', outline = 'white', 
                                    width = 3)
                # short circuit to check if there is another counter to the 
                # right of the current counter and decide whether or not to draw
                # the side of the counter
                if c-1 == -1 or not isinstance(app.floor[r][c-1], counter):
                    counterCornerX = counterBackRX
                    counterCornerY = counterBackRY + dy*2
                    canvas.create_polygon(counterBackRX, counterBackRY,
                                    counterTopRX, counterTopRY, 
                                    counterBottomRX, counterBottomRY,
                                    counterCornerX, counterCornerY,
                                    fill = f'{color}3', outline = 'white',
                                    width = 3)

                # draw the item of the counter subclasses
                if type(app.floor[r][c]) != counter and \
                    type(app.floor[r][c]) != ingredientCounter:
                    itemX = counterBottomRX
                    itemY = counterTopRY - dy
                    drawItem(app, canvas, app.floor[r][c].item, 
                            itemX, itemY, app.dishSize*0.8)

                # all the counters that is not a prepare counter and 
                # doesn't have a dish on it
                if app.floor[r][c].dish != None and \
                    type(app.floor[r][c]) != prepareCounter:
                    dishX = counterBottomRX
                    dishY = counterTopRY - dy
                    if type(app.floor[r][c].dish) == ingredient:
                        drawIngredient(app, canvas, app.floor[r][c].dish,
                                        dishX, dishY, app.dishSize/2)
                    elif type(app.floor[r][c].dish) == food:
                        drawFood(app, canvas, app.floor[r][c].dish,
                                        dishX, dishY, app.dishSize/2)
                # if the counter is a prepare counter and there is a dish on it
                elif type(app.floor[r][c]) == prepareCounter and \
                    app.floor[r][c].dish  != None:
                    dishX = counterBottomRX
                    dishY = counterTopRY - dy
                    drawFood(app, canvas,
                            app.floor[r][c].dish,
                            dishX, dishY, app.dishSize/2)
                # if the counter is a prepare counter and there are only 
                # ingredients on the counter
                elif type(app.floor[r][c]) == prepareCounter and \
                    len(app.floor[r][c].ingredientsList) != 0:
                    if len(app.floor[r][c].ingredientsList) == 1:
                        dishX = counterBottomRX
                        dishY = counterTopRY - dy
                        drawIngredient(app, canvas, 
                                app.floor[r][c].ingredientsList[0], 
                                dishX, dishY, app.dishSize/2)
                        isIn = False
                        for ingredientItem in app.hamburger.ingredients:
                            if app.floor[r][c].ingredientsList[0].name == \
                                ingredientItem.name:
                                isIn = True
                        if isIn == True:
                            app.floor[r][c].futureDish = app.hamburger
                        else:
                            app.floor[r][c].futureDish = app.salad
                    elif len(app.floor[r][c].ingredientsList) == 2:
                        dishSpace = (counterBackRX - counterTopLX)/3
                        dish1X = counterTopLX + dishSpace
                        dish1Y = counterTopRY - dy
                        drawIngredient(app, canvas, 
                                app.floor[r][c].ingredientsList[0], 
                                dish1X, dish1Y, app.dishSize/2.5)
                        dish2X = dish1X + dishSpace
                        dish2Y = dish1Y
                        dotSize = 10
                        drawIngredient(app, canvas,
                                app.floor[r][c].ingredientsList[1],
                                dish2X, dish2Y, app.dishSize/4)
                    elif len(app.floor[r][c].ingredientsList) == 3:
                        dishSpaceX = (counterBackRX - counterTopLX)/3
                        dishSpaceY = (counterTopRY - counterBackLY)/3
                        dish1X = counterTopLX + dishSpaceX
                        dish1Y = counterBackLY + dishSpaceY
                        drawIngredient(app, canvas,
                                app.floor[r][c].ingredientsList[0],
                                dish1X, dish1Y, app.dishSize/4)
                        dish2X = dish1X + dishSpaceX
                        dish2Y = dish1Y
                        drawIngredient(app, canvas,
                                app.floor[r][c].ingredientsList[1],
                                dish2X, dish2Y, app.dishSize/4)
                        dish3X = (dish2X + dish1X)/2
                        dish3Y = counterTopRY - dishSpaceY
                        drawIngredient(app, canvas, 
                                app.floor[r][c].ingredientsList[2],
                                dish3X, dish3Y, app.dishSize/4)
                        
                        # check if everything is cooked and chopped
                        canBeServed = True 
                        for ingredientItem in app.floor[r][c].ingredientsList:
                            if ingredientItem.cookingTime != None and \
                                ingredientItem.ingredientCooked == False:
                                canBeServed = False
                            if len(ingredientItem.allImages) != 1 and \
                                ingredientItem.chopCounter != 3:
                                canBeServed = False

                        # wait a bit
                        if canBeServed == True:
                            app.floor[r][c].dish = app.floor[r][c].futureDish
                            app.floor[r][c].ingredientsList = []


# -----------------------------------------------------------------------------

# draw a certain food by passing in the food and the x, y coordinates of the 
# position of the center of the food
def drawFood(app, canvas, food, x, y, size):
    foodImage = scaleImage(app, food.image, size)
    canvas.create_image(x, y, image=ImageTk.PhotoImage(foodImage))

# draw a certain ingredient by passing in the ingredient and the x, y 
# coordinates of the position of the center of the ingredient
def drawIngredient(app, canvas, ingredient, x, y, size):
    ingredientImage = scaleImage(app, ingredient.image, size)
    canvas.create_image(x, y, image=ImageTk.PhotoImage(ingredientImage))

# draw a certian item by passing in the image of the item and the x, y
# coordinates of the position of the center of the item
def drawItem(app, canvas, item, x, y, size):
    item = scaleImage(app, item, size)
    canvas.create_image(x, y, image=ImageTk.PhotoImage(item))

# draw an order at the top right corner of the screen with the food that the 
# order is associated with and also the ingredients
# labels the order with the name of the food
def drawOrder(app, canvas, order):
    x0, y0 = app.margin/4, app.margin/4
    size = app.margin
    orderNum = order.orderNum
    x1 = x0+orderNum*size
    canvas.create_rectangle(x1, y0, 
                            x0+(orderNum+1)*size, y0+size, 
                            fill = 'beige', outline = 'thistle', width = 3)
    foodX = ((x1)+(x0+(orderNum+1)*size))/2
    foodY = ((y0)+(y0+size))/2
    canvas.create_image(foodX, foodY, 
                        image=ImageTk.PhotoImage(order.food.image))
    textY = (y0 + foodY)/5*2
    canvas.create_text(foodX, textY, text=order.food.name, 
                    font = 'Arial 15 bold', fill = 'purple')
    ingredientSizeScale = 2/5
    ingredient1X = (x1 + foodX)/2
    ingredientY = (foodY*1.25 + y0+size)/2
    ingredientImage = app.scaleImage(order.food.ingredients[0].image, 
                    ingredientSizeScale)
    canvas.create_image(ingredient1X, ingredientY, 
                    image=ImageTk.PhotoImage(ingredientImage))
    ingredient2X = foodX
    ingredientImage = app.scaleImage(order.food.ingredients[1].image, 
                    ingredientSizeScale)
    canvas.create_image(ingredient2X, ingredientY, 
                    image=ImageTk.PhotoImage(ingredientImage))
    ingredient3X = ((x1 + size) + foodX)/2
    ingredientImage = app.scaleImage(order.food.ingredients[2].image, 
                    ingredientSizeScale)
    canvas.create_image(ingredient3X, ingredientY, 
                    image=ImageTk.PhotoImage(ingredientImage))

    # draw the box underneath the order displaying the amount of time left to 
    # complete the order before it fails
    timeBoxL = ingredient1X
    timeBoxTop = y0 + size
    timeBoxR = ingredient3X
    timeBoxBottom = y0 + size*1.25
    canvas.create_rectangle(timeBoxL, timeBoxTop, timeBoxR, timeBoxBottom, 
                        fill = 'beige', outline = 'thistle', width = 3)
    timeX = foodX
    timeY = (timeBoxTop + timeBoxBottom)/2
    canvas.create_text(timeX, timeY, text = f'{order.timeLeft}',
                    font = 'Arial 15 bold', fill = 'purple')

# draws the starting page of the game
def drawStarting(app, canvas):
    lineSpacing = 25
    titleY = app.height*1/3
    instructionsY = app.height*10/16
    textX = app.width/2
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'thistle')
    canvas.create_text(textX, titleY, text = '112° Cooked',
                        font = 'Arial 100 bold', fill = 'purple')
    canvas.create_text(textX, instructionsY, 
                text = 'Press [Return] to start the game',
                font = 'Arial 20 bold', fill = 'purple')
    canvas.create_text(textX, instructionsY+lineSpacing,
                text = 'Use arrow keys to move the character around', 
                font = 'Arial 20 bold', fill = 'purple')
    canvas.create_text(textX, instructionsY+lineSpacing*2,
                text = 'Press [c] to pick up ingredients or food', 
                font = 'Arial 20 bold', fill = 'purple')
    canvas.create_text(textX, instructionsY+lineSpacing*3,
                text = 'Press [d] to drop off ingredients or food', 
                font = 'Arial 20 bold', fill = 'purple')
    canvas.create_text(textX, instructionsY+lineSpacing*4,
                text = 'Press [Space] to chop ingredients', 
                font = 'Arial 20 bold', fill = 'purple')
    canvas.create_text(textX, instructionsY+lineSpacing*5,
                text = 'Press [s] to serve food on the serving counters', 
                font = 'Arial 20 bold', fill = 'purple')

# draws the ending page of the game
def drawGameEnded(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'thistle')
    titleY = app.height/2
    textX = app.width/2
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'thistle')
    canvas.create_text(textX, titleY, text = 'Game Ended!',
                        font = 'Arial 100 bold', fill = 'purple')
    scoreY = app.height*3/4
    canvas.create_text(textX, scoreY, text = 
                    f'Your score was: {app.player.getPlayerScore()}', 
                    font = 'Arial 20 bold', fill = 'purple')

# display the time that has passed since the game has started
def drawTime(app, canvas):
    canvas.create_text(app.width/2, app.height/8*7, 
                text = f'''time: {app.duration}
                        score: {app.player.getPlayerScore()}''', 
                font = 'Arial 20 bold', fill = 'purple')

def redrawAll(app, canvas):
    if app.gameStarted == True:
        drawBackground(app, canvas)

        chefRow, chefCol = getCell(app, app.chefX, app.chefY)
        if chefRow == 1 or (chefRow == 2 and chefCol <= 3) or \
            (chefRow == 3 and chefCol == 3) or (chefRow == 4):
            if app.drawMouseChar == True:
                drawMouse(app, canvas)
            drawCounterTopsAndSides(app, canvas)
            drawCounterFronts(app, canvas)
            drawChef(app, canvas)
        else:
            drawChef(app, canvas)
            if app.drawMouseChar == True:
                drawMouse(app, canvas)
            drawCounterFronts(app, canvas)
            drawCounterTopsAndSides(app, canvas)


        for orderDrawn in app.orders:
            drawOrder(app, canvas, orderDrawn)
        drawTime(app, canvas)
    else:
        drawStarting(app, canvas)
    if app.gameEnded == True:
        drawGameEnded(app, canvas)

def runGame():
    runApp(width=750, height=750)

runGame()
