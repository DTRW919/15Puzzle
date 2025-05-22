import time

class Statistics:
    def __init__(self):
        self.resetAll()

    class Move:
        def __init__(self, direction):
            converter = {
                "w" : "U",
                "s" : "D",
                "a" : "L",
                "d" : "R"
            }

            self.timestamp = time.time()
            self.direction = converter[direction]

    def resetAll(self):
        self.solving = False
        self.movesHistory = []
        self.movesPerSecond = 0.0
        self.startTime = 0.0
        self.timeTaken = 0.0

    def startTracking(self):
        if not self.solving:
            self.solving = True
            self.startTime = time.time()

    def stopTracking(self): # Maybe not used
        if self.solving:
            self.solving = False

    def getTime(self):
        if self.solving:
            self.timeTaken = round(time.time() - self.startTime, 3)

        return self.timeTaken

    def checkMoveHistory(self):
        self.movesHistory = [entry for entry in self.movesHistory if entry.direction != ""]

    def addMove(self, direction):
        for char in direction:
            self.movesHistory.append(self.Move(char))

    def printMoves(self):
        lastMove = ""

        i = 0
        while i < len(self.movesHistory) - 1:
            counter = 1

            if self.movesHistory[i].direction != lastMove:
                lastMove = self.movesHistory[i].direction

                j = i + 1
                while j < len(self.movesHistory):
                    if self.movesHistory[j].direction == self.movesHistory[i].direction:
                        counter += 1
                    else:
                        break
                    j += 1

                if counter > 1:
                    print(counter, end = "")
                print(lastMove, end = "", flush = True)

            i += 1

    def printFinished(self):
        print(f"You completed this 15 Puzzle in {self.getTime()} seconds ", end = "")
        print(f"with a MPS of {self.getMPS()} ", end = "")
        print("following the directions: ")
        print(*[entry.direction for entry in self.movesHistory], sep = "")
        self.printMoves()

    def getNumMoves(self):
        return len(self.movesHistory)

    def getMovesHistory(self):
        return self.movesHistory

    def getMPS(self):
        self.checkMoveHistory()

        return round(len(self.movesHistory) / (time.time() - self.startTime), 1)
