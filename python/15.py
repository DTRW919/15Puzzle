import random

puzzle = [
    ["1", "2", "3", "4"],
    ["5", "6", "7", "8"],
    ["9", "A", "B", "C"],
    ["D", "E", "F", "0"]
]
# 0 is the empty tile

def checkValidity(validOptions, prompt = ""):
    userInput = None
    while userInput not in validOptions:
        userInput = input(prompt + ": ")

    return userInput

def checkPuzzleValidity(puzzle):
    def getInversions(puzzle):
        inversions = 0
        flatPuzzle = [int(item, 16) for sublist in puzzle for item in sublist]
        flatPuzzle.remove(0)

        for i in range(len(flatPuzzle) - 1):
            if flatPuzzle[i] > flatPuzzle[i + 1]:
                inversions += 1
        return inversions

    inversions = getInversions(puzzle) # Number of times a tile is larger than the one after it in a 1D list

    zeroRow = findTile("0")[0] # Row that the blank tile is in

    if (inversions + zeroRow) % 2 == 0: # If the number of inversions added to the numbered row zero is in is even it is solvable
        return True
    else:
        return False

def displayPuzzle(puzzle):
    for row in range(len(puzzle)):
        for val in puzzle[row]:
            print(val, end = " ")
        print()

def findVal(y, x):
    value = puzzle[y][x]

    return value

def setTile(y, x, val = "0"): # Defaults to 0
    puzzle[y][x] = val

def findTile(target, display = False):
    for row, col in enumerate(puzzle):
        if target in col:
            if display:
                print(f"Found {target} at row {row}, column {col.index(target)}")
            return row, col.index(target)

    print("not found")
    return -1, -1

def moveTile(move):
    locY, locX = findTile("0") # Location of empty tile

    if move == "up" and locY != len(puzzle) - 1:
        setTile(locY, locX, findVal(locY + 1, locX))
        setTile(locY + 1, locX)
        return

    if move == "down" and locY != 0:
        setTile(locY, locX, findVal(locY - 1, locX))
        setTile(locY - 1, locX)
        return

    if move == "left" and locX != len(puzzle[0]) - 1:
        setTile(locY, locX, findVal(locY, locX + 1))
        setTile(locY, locX + 1)
        return

    if move == "right" and locX != 0:
        setTile(locY, locX, findVal(locY, locX - 1))
        setTile(locY, locX - 1)
        return

    print("NOOOO")

def scramblePuzzle(puzzle):
    firstShuffle = True
    while not checkPuzzleValidity(puzzle) or firstShuffle:
        firstShuffle = False

        for row in puzzle:
            for col in puzzle:
                random.shuffle(col)
        random.shuffle(puzzle)



### Test ###
validMoves = ["left", "right", "up", "down", "exit"]

scramblePuzzle(puzzle)
displayPuzzle(puzzle)

userInput = ""
while True:
    userInput = checkValidity(validMoves, "Enter a valid move")
    if userInput == "exit":
        break
    moveTile(userInput)
    print()
    displayPuzzle(puzzle)
