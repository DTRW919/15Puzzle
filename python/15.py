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

def displayPuzzle():
    for row in range(len(puzzle)):
        for val in puzzle[row]:
            print(val, end = " ")
        print()

def findVal(y, x):
    return puzzle[y][x]

def findTile(target, display = False):
    for row, col in enumerate(puzzle):
        if target in col:
            if display:
                print(f"Found {target} at row {row}, column {col.index(target)}")
            return row, col.index(target)
    print("not found")
    return -1, -1

def setTile(y, x, val = "0"): # Defaults to 0
    puzzle[y][x] = val

def moveTile(move):
    locY, locX = findTile("0")

    if move == "up" and locY != len(puzzle) - 1:
        setTile(locY, locX, findVal(locY + 1, locX))
        setTile(locY + 1, locX)
        return
    if move == "down" and locY != 0:
        setTile(locY, locX, findVal(locY - 1, locX))
        setTile(locY - 1, locX)
        return

    print("NOOOO")



displayPuzzle()

moveTile("down")

print()
displayPuzzle()
