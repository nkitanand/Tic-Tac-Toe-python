import random
import copy

# Convert input to location
def input(key):
    if (key == '1'):
        return [0,0]
    if (key == '2'):
        return [0,1]
    if (key == '3'):
        return [0,2]
    if (key == '4'):
        return [1,0]
    if (key == '5'):
        return [1,1]
    if (key == '6'):
        return [1,2]
    if (key == '7'):
        return [2,0]
    if (key == '8'):
        return [2,1]
    if (key == '9'):
        return [2,2]

# print board on console
def printBoard(board, w, h):
    displayBoard = ''

    for i_h in range(h):        # iterate row
        for i_w in range(w):    # iterate columns
            displayBoard += str(board[i_h][i_w])
            displayBoard += '\t'
        displayBoard += '\n'

    print displayBoard

# get all location of players input - 0/1
# 1 = Human player
# 0 = Computer bot
def getLocation(player, board, w, h):
    locs = []

    for i_h in range(h):
        for i_w in range(w):
            if board[i_h][i_w] == player:
                locs += [[i_h, i_w]]

    return locs

def getLocs(locs, index):
    locList = []

    for x in range(len(locs)):
        locList.append(locs[x][index])

    return locList

# Checks the conditions of game over
# function returns 1 if the player has win else return 0
def isGameOver(player, board, w, h):
    # get all current locations of player
    locs = getLocation(player, board, w, h)

    if (len(locs) <= 2):    # only a combination of three locations can end the game
        return 0

    else:
        x_locs = getLocs(locs, 0)   # get all row co-ordinates
        y_locs = getLocs(locs, 1)   # get all column co-ordinates

        x_locs.sort()
        y_locs.sort()

        # check if player has any combination in same row/column
        for x in range(3):
            x_count = x_locs.count(x)
            if (x_count >= 3):
                return 1

            y_count = y_locs.count(x)
            if y_count >= 3:
                return 1

        # check for diagonal combination (left-top to right-bottom)
        if [0,0] in locs and [1,1] in locs and [2,2] in locs:
            return 1

        # check for diagonal combination (left-bottom to right-top)
        if [0,2] in locs and [1,1] in locs and [2,0] in locs:
            return 1

        return 0

# Recurse to check for the optimal move
def check(player, choices, board, w, h):
    if isGameOver(0, board, w, h):
        return 10
    elif isGameOver(1, board, w, h):
        return -10
    elif len(choices) == 0:
        return 0

    (WIN, LOSE, DRAW) = (-1, -1, -1)
    if (player == 0):   # For BOT
        (WIN, LOSE, DRAW) = (10, -10, 0)
    if (player == 1):   # For HUMAN
        (WIN, LOSE, DRAW) = (-10, 10, 0)

    # Check if opponent's next move finish the game
    nextPlayer = -1
    bufferChoices = list(choices)
    bufferBoard = copy.deepcopy(board)
    for step in choices:
        loc = input(step)
        if (player == 1):
            nextPlayer = 0
        elif (player == 0):
            nextPlayer = 1
        bufferBoard[loc[0]][loc[1]] = nextPlayer
        if isGameOver(player, bufferBoard, w, h):
            return WIN
        elif isGameOver(nextPlayer, bufferBoard, w, h):
            return LOSE
        bufferBoard[loc[0]][loc[1]] = '-'
    
    nextPlayer = -1
    loseFlag = False
    bufferChoices = list(choices)
    bufferBoard = copy.deepcopy(board)
    resultList = []
    for step in choices:
        loc = input(step)
        stepIndex = bufferChoices.index(step)
        bufferChoices.remove(step)
        if (player == 1):
            nextPlayer = 0
        elif (player == 0):
            nextPlayer = 1
        bufferBoard[loc[0]][loc[1]] = nextPlayer
        result = check(nextPlayer, bufferChoices, bufferBoard, w, h)
        resultList.append([step, result])
        bufferChoices.insert(stepIndex, step)
        bufferBoard[loc[0]][loc[1]] = '-'

    # look for win
    (winStep, drawStep, loseStep) = ('', '', '')
    for x in resultList:
        if x[1] == WIN:
            winStep = x[0]
        elif x[1] == DRAW:
            drawStep = x[0]
        elif x[1] == LOSE:
            loseStep = x[0]

    if (winStep != ''):
        return WIN
    elif (drawStep != ''):
        return DRAW
    elif (loseStep != ''):
        return LOSE
    return LOSE

def playBot(player, choices, board, w, h):
    
    (WIN, LOSE, DRAW) = (-1, -1, -1)
    if (player == 0):   # For BOT
        (WIN, LOSE, DRAW) = (10, -10, 0)
    if (player == 1):   # For HUMAN
        (WIN, LOSE, DRAW) = (-10, 10, 0)
        
    winStep  = -1;
    loseStep = -1;
    drawStep = -1;
    bufferChoices = list(choices)
    bufferBoard = copy.deepcopy(board)
    for step in choices:
        loc = input(step)
        stepIndex = bufferChoices.index(step)
        bufferChoices.remove(step)
        bufferBoard[loc[0]][loc[1]] = player
        result = check(player, bufferChoices, bufferBoard, w, h)
        bufferChoices.insert(stepIndex, step)
        bufferBoard[loc[0]][loc[1]] = '-'
        if (result == WIN):
            winStep = step
            return winStep
        elif (result == DRAW):
            drawStep = step
        elif (result == LOSE):
            loseStep = step

    if (drawStep != -1):
        return drawStep
    
    return loseStep

def main():
    (w,h) = (3,3)
    board = [['-','-','-'],['-','-','-'],['-','-','-']]
    filled = []
    choices = ['1','2','3','4','5','6','7','8','9']
    printBoard(board, w, h)

    while not len(choices) == 0:
        if not len(choices) == 0:
            print 'Your turn:'
            key = raw_input()
            if key not in choices:
                print "Invalid move"
                continue
            choices.remove(key)
            loc = input(key)
            board[loc[0]][loc[1]] = 1
        
            printBoard(board, w, h)
            if isGameOver(1, board, w, h):
                print "Congratulations! You won."
                break

        if not len(choices) == 0:
            print 'Computer turn:'
            #key = random.choice(choices)
            key = playBot(0, choices, board, w, h)
            choices.remove(key)
            print key
            loc = input(key)
            board[loc[0]][loc[1]] = 0
        
            printBoard(board, w, h)
            if isGameOver(0, board, w, h):
                print "Oops! Computer defeated you."
                break

    print "Draw. Game over!"

if __name__ == "__main__":
    main()
