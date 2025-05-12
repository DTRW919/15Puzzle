import tkinter as tk
import puzzle

moveTracker = ""

class Tile:
    def __init__(self, ID, value = 0, color = "gray"):
        self.ID = ID
        self.color = color
        self.value = value

        self.canvas_id = None
        self.text_id = None

        self.x = 0
        self.y = 0

    def getVal(self):
        return self.value

def moveConverter(moveOrID):
    moveToID = {
        "up" : "w",
        "down" : "s",
        "left" : "a",
        "right" : "d"
    }

    if moveOrID in moveToID:
        return moveToID[moveOrID]
    else:
        for key, value in moveToID.items():
            if value == moveOrID:
                return key

def keyChecker(event):
    key = event.keysym

    if key == "l":
        onListEnter()

    if key == "space":
        resetBoard()

    movementKeys = [
        "Up", "Down", "Left", "Right",
        "w", "s", "a", "d"
    ]

    if key in movementKeys:
        onKeyPress(key)

root = tk.Tk()
canvas = tk.Canvas(root, width = 800, height = 400, bg = "black")
canvas.pack()
root.bind("<KeyPress>", keyChecker)
canvas.focus_set()

solved = False

def onListEnter():
    global moveTracker

    moveList = puzzle.checkListValidity()
    print("The move list contains:", moveList)
    for move in list(moveList):
        moveTracker += move
        puzzle.moveTile(moveConverter(move))
    updateBoard()

def onKeyPress(key):
    global solved
    global moveTracker

    if not solved:
        if key == "Up" or key == "w":
            moveTracker += puzzle.moveTile("up")
        if key == "Down" or key == "s":
            moveTracker += puzzle.moveTile("down")
        if key == "Left" or key == "a":
            moveTracker += puzzle.moveTile("left")
        if key == "Right" or key == "d":
            moveTracker += puzzle.moveTile("right")

    updateBoard()

def onMouseEnter(event, object): # TODO: Advanced mousemovement (doesnt need to be adjacent to zero)
    global solved
    global moveTracker

    if not solved:
        currentMove = moveConverter(puzzle.getMove(object.getVal()))
        if isinstance(currentMove, str):
            moveTracker += currentMove

        puzzle.moveTile(puzzle.getMove(object.getVal()))

    updateBoard()

def resetBoard():
        puzzle.scramblePuzzle()
        puzzle.displayPuzzle()
        updateBoard()

def updateBoard():
    global solved
    global moveTracker

    solved = True

    for i in range(4):
        for j in range(4):
            tileObj = spaceList[i][j]
            tileObj.value = puzzle.getVal(i, j)
            displayValue = int(tileObj.value, 16)

            if tileObj.value == "0": # its an int now not a string
                canvas.itemconfigure(tileObj.canvas_id, fill = "black", outline = "black")
                canvas.itemconfigure(tileObj.text_id, text = "")
            else:
                if tileObj.ID == displayValue:
                    canvas.itemconfigure(tileObj.canvas_id, fill = "orange", outline = "white")
                else:
                    solved = False
                    canvas.itemconfigure(tileObj.canvas_id, fill = "blue", outline = "white")

                canvas.itemconfigure(tileObj.text_id, text = displayValue)
                # canvas.itemconfigure(tileObj.text_id, text = tileObj.ID) # Show ID instead of Value

    print(moveTracker)


length = 50
space = length + 1

spaceList = [
    [],
    [],
    [],
    []
]

for i in range(4): # TODO: change to be flexible between puzzle sizes
    for j in range(4):
        spaceList[i].append(Tile((i * 4) + j + 1))

        tileObj = spaceList[i][j]

        tileObj.x = j * space
        tileObj.y = i * space

        tileObj.canvas_id = canvas.create_rectangle(
            tileObj.x, tileObj.y,
            tileObj.x + length,
            tileObj.y + length,
            fill = "blue"
        )
        tileObj.text_id = canvas.create_text(
            tileObj.x + length / 2,
            tileObj.y + length / 2,
            text = tileObj.getVal()
        )

        canvas.tag_bind(tileObj.canvas_id, "<Enter>", lambda e, o = tileObj: onMouseEnter(e, o))


# Initial setup
resetBoard()
updateBoard()

root.mainloop()
