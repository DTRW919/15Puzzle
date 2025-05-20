import random
import constants

class Puzzle:
    def __init__(self):
        self.puzzle = [
            ["0", "1", "2", "3"],
            ["4", "5", "6", "7"],
            ["8", "9", "A", "B"],
            ["C", "D", "E", "F"]
        ]  # Strings

        self.solved = True
        self.startedSolve = False

        self.zeroY = -1
        self.zeroX = -1

        self.constants = constants.Constants()

        self.scramblePuzzle()

    def getStarted(self):
        return self.startedSolve

    def setStarted(self, state):
        self.startedSolve = state

    def getSolved(self):
        self.checkFinished()
        return self.solved

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

        self.zeroY, self.zeroX = self.findTarget("0")

        if not advanced:
            if self.zeroX == targetX:
                if self.zeroY - targetY == 1:
                    return "down"
                if self.zeroY - targetY == -1:
                    return "up"
            if self.zeroY == targetY:
                if self.zeroX - targetX == 1:
                    return "right"
                if self.zeroX - targetX == -1:
                    return "left"
        else:
            if self.zeroX == targetX:
                if self.zeroY > targetY:
                    return "down"
                if self.zeroY < targetY:
                    return "up"
            if self.zeroY == targetY:
                if self.zeroX > targetX:
                    return "right"
                if self.zeroX < targetX:
                    return "left"

        return "invalid"

    def setTarget(self, targetY, targetX, val = "0"):
        if val == "0":
            self.zeroY = targetY
            self.zeroX = targetX

        self.puzzle[targetY][targetX] = val

    def moveUp(self, target, advanced = False):
        if not advanced:
            if self.zeroY != len(self.puzzle) - 1:
                self.setTarget(self.zeroY, self.zeroX, self.getPosVal(self.zeroY + 1, self.zeroX))
                self.setTarget(self.zeroY + 1, self.zeroX)
                return "w"
        else:
            self.setTarget(self.zeroY + target, self.zeroX, self.getPosVal(self.zeroY + target + 1, self.zeroX))
            return "w"

    def moveDown(self, target, advanced = False):
        if not advanced:
            if self.zeroY != 0:
                self.setTarget(self.zeroY, self.zeroX, self.getPosVal(self.zeroY - 1, self.zeroX))
                self.setTarget(self.zeroY - 1, self.zeroX)
                return "s"
        else:
            self.setTarget(self.zeroY - target, self.zeroX, self.getPosVal(self.zeroY - target - 1, self.zeroX))
            return "s"

    def moveLeft(self, target, advanced = False):
        if not advanced:
            if self.zeroX != len(self.puzzle[0]) - 1:
                self.setTarget(self.zeroY, self.zeroX, self.getPosVal(self.zeroY, self.zeroX + 1))
                self.setTarget(self.zeroY, self.zeroX + 1)
                return "a"
        else:
            self.setTarget(self.zeroY, self.zeroX + target, self.getPosVal(self.zeroY, self.zeroX + target + 1))
            return "a"

    def moveRight(self, target, advanced = False):
        if not advanced:
            if self.zeroX != 0:
                self.setTarget(self.zeroY, self.zeroX, self.getPosVal(self.zeroY, self.zeroX - 1))
                self.setTarget(self.zeroY, self.zeroX - 1)
                return "d"
        else:
            self.setTarget(self.zeroY, self.zeroX - target, self.getPosVal(self.zeroY, self.zeroX - target - 1))
            return "d"

    def moveTarget(self, move, targetY = -1, targetX = -1):
        self.zeroY, self.zeroX = self.findTarget() # Find location of empty tile

        advanced = self.constants.getConstant("tiles.advanced")

        returnString = ""

        if move == "up":
            for i in range(targetY - self.zeroY):
                returnString += self.moveUp(i, advanced)
            self.setTarget(targetY, targetX) # Set empty tile

        if move == "down":
            for i in range(self.zeroY - targetY):
                returnString += self.moveDown(i, advanced)
            self.setTarget(targetY, targetX) # Set empty tile

        if move == "left":
            for i in range(targetX - self.zeroX):
                returnString += self.moveLeft(i, advanced)
            self.setTarget(targetY, targetX) # Set empty tile

        if move == "right":
            for i in range(self.zeroX - targetX):
                returnString += self.moveRight(i, advanced)
            self.setTarget(targetY, targetX)


        if returnString != "" and not self.startedSolve:
            self.startedSolve = True
            self.getStarted()

        self.checkFinished()

        return returnString

    def checkFinished(self):
        for i in range(4):
            for j in range(4):
                if int(self.puzzle[i][j], 16) != (4 * i) + j:
                    self.solved = False
                    return
        self.solved = True
        self.startedSolve = False

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

        self.solved = False
        self.setStarted(False)
