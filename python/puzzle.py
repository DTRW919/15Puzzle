import random

puzzle = [
    ["1", "2", "3", "4"],
    ["5", "6", "7", "8"],
    ["9", "A", "B", "C"],
    ["D", "E", "F", "0"]
]
# 0 is the empty tile

def checkListValidity(prompt = ""):
    userInput = " "
    userList = list(userInput)

    validMoves = ["w", "s", "a", "d"]

    flag = False

    while not flag:
        flag = True
        for char in userList:
            if char not in validMoves:
                flag = False

        if not flag:
            userInput = input(prompt + ": ")
            userList = list(userInput)
            print(userList)

    return userInput

def checkValidity(validOptions = [], prompt = ""):
    userInput = None

    while userInput not in validOptions:
        userInput = input(prompt + ": ")

    return userInput

def displayPuzzle(): # TODO: Maybe remove all unecessary 'puzzle' parameters?
    for row in range(len(puzzle)):
        for val in puzzle[row]:
            print(val, end = " ")
        print()

def getVal(y, x):
    value = puzzle[y][x]

    return value

def getMove(target, advanced = False): # Checks if adjacent to empty tile
    zeroY, zeroX = findTile("0")
    targetY, targetX = findTile(target)

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

def setTile(y, x, val = "0"): # Defaults to 0
    puzzle[y][x] = val

def findTile(target, puzzle = puzzle):
    for row, col in enumerate(puzzle):
        if target in col:
            return row, col.index(target)

    print("Error: target not found")
    return -1, -1

def moveTile(move, advanced = False, tileLocX = 0, tileLocY = 0): # tileLoc is the location of the target tile
    locY, locX = findTile("0") # Location of empty tile

    if not advanced:
        if move == "up" and locY != len(puzzle) - 1:
            setTile(locY, locX, getVal(locY + 1, locX))
            setTile(locY + 1, locX)
            return "w"

        if move == "down" and locY != 0:
            setTile(locY, locX, getVal(locY - 1, locX))
            setTile(locY - 1, locX)
            return "s"

        if move == "left" and locX != len(puzzle[0]) - 1:
            setTile(locY, locX, getVal(locY, locX + 1))
            setTile(locY, locX + 1)
            return "a"

        if move == "right" and locX != 0:
            setTile(locY, locX, getVal(locY, locX - 1))
            setTile(locY, locX - 1)
            return "d"
    else:
        if move == "up":
            for i in range(tileLocY - locY):
                setTile(locY + i, locX, getVal(locY + i + 1, locX))
            setTile(tileLocY, tileLocX)

        if move == "down":
            for i in range(locY - tileLocY):
                setTile(locY - i, locX, getVal(locY - i - 1, locX))
            setTile(tileLocY, tileLocX)

        if move == "left":
            for i in range(tileLocX - locX):
                setTile(locY, locX + i, getVal(locY, locX + i + 1))
            setTile(tileLocY, tileLocX)

        if move == "right":
            for i in range(locX - tileLocX):
                setTile(locY, locX - i, getVal(locY, locX - i - 1))
            setTile(tileLocY, tileLocX)

    return ""

def scramblePuzzle():
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

    flatPuzzle = [int(item, 16) for sublist in puzzle for item in sublist]

    shuffleFlatPuzzle(flatPuzzle)

    inversions = getInversions(flatPuzzle)
    zeroRow = 4 - (flatPuzzle.index(0) // 4) # row number from bottom because proofs idk

    if (inversions % 2) ^ (zeroRow % 2) != 1: # TODO: Make sure this works
        print("Unsolvable. Trying again.") # TODO: Redo shuffling algorithm to manually shuffle from sovled state to guarantee
        scramblePuzzle()
    else:
        for row in range(4):
            for col in range(4):
                puzzle[row][col] = hex(flatPuzzle[(row * 4) + col]).upper()[2 :]

### Test ###
# checkValidity(listCheck = True)

# validMoves = ["left", "right", "up", "down", "exit"]
# userInput = ""
# while True:
#     userInput = checkValidity(validMoves, "Enter a valid move")
#     if userInput == "exit":
#         break
#     moveTile(userInput)
#     print()
#     displayPuzzle(puzzle)
