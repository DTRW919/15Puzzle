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
        self.advanced = self.constants.getConstant("tiles.advanced")

        self.scramblePuzzle()

    def updateAdvanced(self):
        self.advanced = self.constants.getConstant("tiles.advanced")

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

    def getMove(self, targetY, targetX, limited = False):
        self.zeroY, self.zeroX = self.findTarget("0")

        if limited:
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

    def moveUp(self, target = 0):
        self.setTarget(self.zeroY + target, self.zeroX, self.getPosVal(self.zeroY + target + 1, self.zeroX))
        return "w"

    def moveDown(self, target = 0):
        self.setTarget(self.zeroY - target, self.zeroX, self.getPosVal(self.zeroY - target - 1, self.zeroX))
        return "s"

    def moveLeft(self, target = 0):
        self.setTarget(self.zeroY, self.zeroX + target, self.getPosVal(self.zeroY, self.zeroX + target + 1))
        return "a"

    def moveRight(self, target = 0):
        self.setTarget(self.zeroY, self.zeroX - target, self.getPosVal(self.zeroY, self.zeroX - target - 1))
        return "d"

    def moveTarget(self, move, targetY = -1, targetX = -1, limited = False):
        self.zeroY, self.zeroX = self.findTarget() # Find location of empty tile

        returnString = ""

        if not limited:
            if move == "up":
                for i in range(targetY - self.zeroY):
                    returnString += self.moveUp(i)
                self.setTarget(targetY, targetX) # Set empty tile

            if move == "down":
                for i in range(self.zeroY - targetY):
                    returnString += self.moveDown(i)
                self.setTarget(targetY, targetX) # Set empty tile

            if move == "left":
                for i in range(targetX - self.zeroX):
                    returnString += self.moveLeft(i)
                self.setTarget(targetY, targetX) # Set empty tile

            if move == "right":
                for i in range(self.zeroX - targetX):
                    returnString += self.moveRight(i)
                self.setTarget(targetY, targetX) # Set empty tile
        else:
            returnString += self.moveTargetLimited(move)

        if returnString != "" and not self.startedSolve:
            self.startedSolve = True
            self.getStarted()

        self.checkFinished()

        return returnString

    def moveTargetLimited(self, move):
        self.zeroY, self.zeroX = self.findTarget() # Find location of empty tile

        returnString = ""

        if move == "up" and self.zeroY != len(self.puzzle) - 1: # Check if target is at edge
            returnString += self.moveUp()
            self.setTarget(self.zeroY + 1, self.zeroX)

        if move == "down" and self.zeroY != 0: # Check if target is at edge
            returnString += self.moveDown()
            self.setTarget(self.zeroY - 1, self.zeroX)

        if move == "left" and self.zeroX != len(self.puzzle[0]) - 1: # Check if target is at edge
            returnString += self.moveLeft()
            self.setTarget(self.zeroY, self.zeroX + 1)

        if move == "right" and self.zeroX != 0: # Check if target is at edge
            returnString += self.moveRight()
            self.setTarget(self.zeroY, self.zeroX - 1)

        return returnString

    def checkFinished(self):
        self.solved = True

        for i in range(4):
            for j in range(4):
                if i == 3 and j == 3:
                    if self.puzzle[3][3] == "0": # Solved
                        self.startedSolve = False
                        break
                if int(self.puzzle[i][j], 16) != (4 * i) + j + 1: # Not solved
                    self.solved = False
                    break

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
