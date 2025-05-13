import time

movesHistory = []
movesPerSecond = 0.0
startTime = time.time()

class Move:
    def __init__(self, direction):
        self.timestamp = time.time()
        self.direction = direction

def resetAll():
    global movesHistory
    global movesPerSecond
    global startTime

    movesHistory = []
    movesPerSecond = 0.0
    startTime = time.time()

def getTime():
    global startTime

    return round(time.time() - startTime, 3)

def checkMoveHistory():
    global movesHistory

    movesHistory = [entry for entry in movesHistory if entry.direction != ""]

def addMove(direction):
    global movesHistory

    movesHistory.append(Move(direction))

def getNumMoves():
    global movesHistory

    return len(movesHistory)

def getMovesHistory():
    global movesHistory

    return movesHistory

def getMPS():
    global movesHistory

    checkMoveHistory()

    currentTime = time.time()
    lastSecond = [entry for entry in movesHistory if currentTime - entry.timestamp <= 1]

    return len(lastSecond)
