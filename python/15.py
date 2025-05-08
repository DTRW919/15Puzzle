puzzle = [
    ["1", "2", "3", "4"],
    ["5", "6", "7", "8"],
    ["9", "A", "B", "C"],
    ["D", "E", "F", "0"]
]
# 0 is the empty tile

def findTile(x):
    for row, col in enumerate(puzzle):
        if x in col:
            print(f"x at row {row + 1}, column {col.index(x) + 1}")
            return row, col.index(x)
    return -1, -1
    
def setTile(x, y, val = 0):
    puzzle[x][y] = 

# findTile(input(": ").strip().upper(), "row") # test

def moveTile(move):
    locX, locY = findTile(0)

    if move == "up" and locY != len(puzzle[0]):
        .


def checkValidity(validOptions, prompt = ""):
    userInput = None
    while userInput not in validOptions:
        userInput = input(prompt + ": ")

    return userInput
