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

def checkMPS():
    global movesHistory

    currentTime = time.time()
    movesHistory = [entry for entry in movesHistory if currentTime - entry.timestamp <= 1]

def addMove(direction):
    global movesHistory

    movesHistory.append(Move(direction))

def getMPS():
    global movesHistory

    currentTime = time.time()
    lastSecond = [entry for entry in movesHistory if currentTime - entry.timestamp <= 1]

    temp = [move.direction for move in movesHistory]
    print(temp)

    return len(lastSecond)
