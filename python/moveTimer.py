import time

movesHistory = []
movesPerSecond = 0.0
startTime = time.time()
timeTaken = 0.0

solving = False # Not boolean; if 0.0 then not solving if not thent represents time taken to solve

class Move:
    def __init__(self, direction):
        self.timestamp = time.time()
        self.direction = direction

class Stats:
    def __init__(self):
        self.resetAll()

    def resetAll(self):
        self.movesHistory = []
        self.movesPerSecond = 0.0
        self.startTime = time.time()
        self.solving = False
        self.timeTaken = 0.0

    def setSolving(self, state):
        self.solving = state

    def getTime(self):
        if self.solving:
            self.timeTaken = round(time.time() - startTime, 3)

        return self.timeTaken

    def checkMoveHistory(self):
        self.movesHistory = [entry for entry in self.movesHistory if entry.direction != ""]

    def addMove(self, direction):
        self.movesHistory.append(Move(direction))

        if not self.solving: # Temporary check, this is dusgusting
            self.solving = True

    def getNumMoves(self):
        return len(self.movesHistory)

    def getMovesHistory(self):
        return self.movesHistory

    def getMPS(self):
        self.checkMoveHistory()

        currentTime = time.time()
        lastSecond = [entry for entry in self.movesHistory if currentTime - entry.timestamp <= 1]

        return len(lastSecond)
