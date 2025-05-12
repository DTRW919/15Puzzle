import time

movesHistory = []
movesPerSecond = 0.0
startTime = time.time()

class Move:
    def __init__(self, direction):
        self.timestamp = time.time()
        self.direction = direction

def restartTime():
    global startTime
    startTime = time.time()

def checkMPSe():
    return "e"

def checkMoveHistory():
    global movesHistory

    movesHistory = [entry for entry in movesHistory if entry.direction != ""]

def addMove(direction):
    global movesHistory

    movesHistory.append(Move(direction))

def getMoves():
    global movesHistory

    return len(movesHistory)

def getMPS():
    global movesHistory

    checkMoveHistory()

    currentTime = time.time()
    lastSecond = [entry for entry in movesHistory if currentTime - entry.timestamp <= 1]

    temp = [move.direction for move in movesHistory]
    print(temp)

    return len(lastSecond)
