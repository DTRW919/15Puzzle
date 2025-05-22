import time
import json, os

class Statistics:
    def __init__(self):
        self.resetAll()

        self.bestTime = 0.0
        self.updateBestTime(start = True)

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

    def addEntry(self, startTime, timeTaken, movesTotal, moves): # To solves.json
        if os.path.exists("../solves.json"):
            with open("../solves.json", "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        entry = {
                "timestamp": startTime,
                "time": timeTaken,
                "total moves": movesTotal,
                "moves": moves
            }

        data.append(entry)

        with open("../solves.json", "w") as file:
            json.dump(data, file, indent = 2)

    def getAverage(self, num):
        if os.path.exists("../solves.json"):
            with open("../solves.json", "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        numTimes = 0
        totalTime = 0

        if len(data) == 0 or num > len(data):
            return 0

        if num == 0:
            numTimes = len(data)
        else:
            numTimes = num

        for i in range(numTimes):
            totalTime += data[-i]["time"]

        return round(totalTime / numTimes, 3)

    def updateBestTime(self, start = False):
        if os.path.exists("../solves.json"):
            with open("../solves.json", "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        if start:
            if len(data) == 0:
                return 0

            bestTime = data[0]["time"]

            for entry in data:
                if entry["time"] < bestTime:
                    bestTime = entry["time"]

            self.bestTime = bestTime
        else:
            if data[-1]["time"] < self.bestTime or self.bestTime == 0.0: # Can only be 0.0 when there are no solves
                self.bestTime = data[-1]["time"]
                return True # Returns true if best time changes, false otherwise

            return False

    def getBestTime(self, start = False):
        color = "white"

        if self.updateBestTime(start):
            color = "green"

        return self.bestTime, color # First indice is best time, second is color

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

        self.addEntry(self.startTime, self.timeTaken, len(self.movesHistory), self.getMoves())

    def getTime(self):
        if self.solving:
            self.timeTaken = round(time.time() - self.startTime, 3)

        return self.timeTaken

    def checkMoveHistory(self):
        self.movesHistory = [entry for entry in self.movesHistory if entry.direction != ""]

    def addMove(self, direction):
        for char in direction:
            self.movesHistory.append(self.Move(char))

    def getMoves(self):
        condensedMovesList = ""

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
                    condensedMovesList += str(counter)
                condensedMovesList += lastMove

            i += 1
        return condensedMovesList

    def printFinished(self):
        print(f"You completed this 15 Puzzle in {self.getTime()} seconds ", end = "")
        print(f"with a MPS of {self.getMPS()} ", end = "")
        print("following the directions: ")
        print(self.getMoves())

    def getNumMoves(self):
        return len(self.movesHistory)

    def getMovesHistory(self):
        return self.movesHistory

    def getMPS(self):
        self.checkMoveHistory()

        return round(len(self.movesHistory) / (time.time() - self.startTime), 1)
