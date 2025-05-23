import time
import json

class Statistics:
    def __init__(self):
        self.resetAll()

        self.defaultStructure = {
            "records": {
                "time": 0.0,
                "averageOfFive": 0.0,
                "average": 0.0
            },

            "solves": []
        }

        try:
            with open("../solves.json", "r") as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = self.defaultStructure
            with open("../solves.json", "w") as file:
                json.dump(self.data, file, indent = 4)

        if not isinstance(self.data, dict):
            self.data = self.defaultStructure

            if "records" not in self.data or "solves" not in self.data:
                self.data = self.defaultStructure

        if len(self.data["solves"]) >= 5:
            lastFiveTimes = sum(entry["time"] for entry in self.data["solves"][-5:])
            self.currentAverageOfFive = lastFiveTimes / 5
        else:
            self.currentAverageOfFive = 0.0

        if len(self.data["solves"]) > 0:
            self.currentTotalAverage = sum(entry["time"] for entry in self.data["solves"]) / len(self.data["solves"])
        else:
            self.currentTotalAverage = 0.0

    def addEntry(self, startTime, timeTaken, movesTotal, moves):
        entry = {
                "timestamp": startTime,
                "time": timeTaken,
                "total moves": movesTotal,
                "moves": moves
            }

        self.data["solves"].append(entry)

        if len(self.data["solves"]) >= 5:
            lastFiveTimes = sum(entry["time"] for entry in self.data["solves"][-5:])
            self.currentAverageOfFive = lastFiveTimes / 5
        else:
            self.currentAverageOfFive = 0.0

        totalTime = sum(entry["time"] for entry in self.data["solves"])
        self.currentTotalAverage = totalTime / len(self.data["solves"])

        if self.data["solves"][-1]["time"] < self.data["records"]["time"] or self.data["records"]["time"] == 0.0:
            self.data["records"]["time"] = self.data["solves"][-1]["time"]

        if self.currentAverageOfFive < self.data["records"]["averageOfFive"] or self.data["records"]["averageOfFive"] == 0.0:
            if self.currentAverageOfFive != 0.0:
                self.data["records"]["averageOfFive"] = self.currentAverageOfFive

        if self.currentTotalAverage < self.data["records"]["average"] or self.data["records"]["average"] == 0.0:
            if self.currentTotalAverage != 0.0:
                self.data["records"]["average"] = self.currentTotalAverage

        with open("../solves.json", "w") as file:
            json.dump(self.data, file, indent = 4)

    def getRecord(self, record):
        recordData = self.data["records"]

        if record == "time":
            if recordData["time"] == self.data["solves"][-1]["time"]:
                return recordData["time"], "green"
            else:
                return recordData["time"], "white"
        elif record == "Ao5":
            if recordData["averageOfFive"] == self.currentAverageOfFive:
                return recordData["averageOfFive"], "green"
            else:
                return recordData["averageOfFive"], "white"
        elif record == "average":
            if recordData["average"] == self.currentTotalAverage:
                return recordData["average"], "green"
            else:
                return recordData["average"], "white"

    def getStat(self, stat):
        if stat == "average":
            if self.currentTotalAverage == self.data["records"]["average"]:
                return self.currentTotalAverage, "green"
            else:
                return self.currentTotalAverage, "white"
        elif stat == "Ao5":
            if self.currentAverageOfFive == self.data["records"]["averageOfFive"]:
                return self.currentAverageOfFive, "green"
            else:
                return self.currentAverageOfFive, "white"

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
