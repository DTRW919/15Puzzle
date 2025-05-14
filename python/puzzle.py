import random
import constants

class Puzzle:
    def __init__(self):
        self.puzzle = [
            ["1", "2", "3", "4"],
            ["5", "6", "7", "8"],
            ["9", "A", "B", "C"],
            ["D", "E", "F", "0"]
        ]  # Strings

        self.solved = True
        self.startedSolve = False

        self.constants = constants.Constants()

        self.scramblePuzzle()

    def getStarted(self):
        return self.startedSolve

    def setStarted(self, state):
        self.startedSolve = state

    def inputValidity(self, options = [], prompt = ""):
        userInput = None

        while userInput not in options:
            userInput = input(prompt + ": ")

        return userInput

    def logPuzzle(self):
        for row in range(len(self.puzzle)):
            for col in self.puzzle[row]:
                print(col, end=" ")
            print()

    def findTarget(self, target = "0"): # Defaults to empty tile
        for row, col in enumerate(self.puzzle):
            if target in col:
                return row, col.index(target)

        print("Error: target not found")
        return -1, -1

    def getPosVal(self, y, x):
        value = self.puzzle[y][x]

        return value

    def getMove(self, targetY, targetX):
        advanced = self.constants.getConstant("tiles.advanced")

        zeroY, zeroX = self.findTarget("0")

        if not advanced:
            if zeroX == targetX:
                if zeroY - targetY == 1:
                    return "down"
                if zeroY - targetY == -1:
                    return "up"
            if zeroY == targetY:
                if zeroX - targetX == 1:
                    return "right"
                if zeroX - targetX == -1:
                    return "left"
        else:
            if zeroX == targetX:
                if zeroY > targetY:
                    return "down"
                if zeroY < targetY:
                    return "up"
            if zeroY == targetY:
                if zeroX > targetX:
                    return "right"
                if zeroX < targetX:
                    return "left"

        return "invalid"

    def setTarget(self, targetY, targetX, val = "0"):
        self.puzzle[targetY][targetX] = val

    def moveTarget(self, move, targetY = -1, targetX = -1):
        returnString = "" # Defaults to no valid move

        advanced = self.constants.getConstant("tiles.advanced")

        zeroY, zeroX = self.findTarget()

        if not advanced or (targetY == -1 and targetX == -1):
            if move == "up" and zeroY != len(self.puzzle) - 1:
                self.setTarget(zeroY, zeroX, self.getPosVal(zeroY + 1, zeroX))
                self.setTarget(zeroY + 1, zeroX)
                returnString = "w"

            if move == "down" and zeroY != 0:
                self.setTarget(zeroY, zeroX, self.getPosVal(zeroY - 1, zeroX))
                self.setTarget(zeroY - 1, zeroX)
                returnString = "s"

            if move == "left" and zeroX != len(self.puzzle[0]) - 1:
                self.setTarget(zeroY, zeroX, self.getPosVal(zeroY, zeroX + 1))
                self.setTarget(zeroY, zeroX + 1)
                returnString = "a"

            if move == "right" and zeroX != 0:
                self.setTarget(zeroY, zeroX, self.getPosVal(zeroY, zeroX - 1))
                self.setTarget(zeroY, zeroX - 1)
                returnString = "d"

        else:

            if move == "up":
                for i in range(targetY - zeroY):
                    self.setTarget(zeroY + i, zeroX, self.getPosVal(zeroY + i + 1, zeroX))
                    returnString += "w"
                self.setTarget(targetY, targetX)

            if move == "down":
                for i in range(zeroY - targetY):
                    self.setTarget(zeroY - i, zeroX, self.getPosVal(zeroY - i - 1, zeroX))
                    returnString += "s"
                self.setTarget(targetY, targetX)

            if move == "left":
                for i in range(targetX - zeroX):
                    self.setTarget(zeroY, zeroX + i, self.getPosVal(zeroY, zeroX + i + 1))
                    returnString += "a"
                self.setTarget(targetY, targetX)

            if move == "right":
                for i in range(zeroX - targetX):
                    self.setTarget(zeroY, zeroX - i, self.getPosVal(zeroY, zeroX - i - 1))
                    returnString += "d"
                self.setTarget(targetY, targetX)

        if not self.getStarted() and returnString != "":
            self.setStarted(True)

        return returnString

    def scramblePuzzle(self):
        print("Resetting puzzle...")

        def getInversions(flatPuzzle):
            inversions = 0

            zeroPos = flatPuzzle.index(0)
            flatPuzzle.remove(0)

            for i in range(len(flatPuzzle)):
                for j in range(i + 1, len(flatPuzzle)):
                    if flatPuzzle[i] > flatPuzzle[j]:
                        inversions += 1

            flatPuzzle.insert(zeroPos, 0)

            print(f"there are {inversions} inversions")
            print(*flatPuzzle)
            return inversions

        def shuffleFlatPuzzle(flatPuzzle):
            return random.shuffle(flatPuzzle)

        flatPuzzle = [int(item, 16) for sublist in self.puzzle for item in sublist]

        shuffleFlatPuzzle(flatPuzzle)

        inversions = getInversions(flatPuzzle)
        zeroRow = 4 - (flatPuzzle.index(0) // 4) # row number from bottom because proofs idk

        if (inversions % 2) ^ (zeroRow % 2) != 1: # TODO: Make sure this works
            print("Unsolvable. Trying again.") # TODO: Redo shuffling algorithm to manually shuffle from sovled state to guarantee
            self.scramblePuzzle()
        else:
            for row in range(4):
                for col in range(4):
                    self.puzzle[row][col] = hex(flatPuzzle[(row * 4) + col]).upper()[2 :]

        self.setStarted(False)
