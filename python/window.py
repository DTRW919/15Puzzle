import tkinter as tk
import puzzle
import moveTimer

class Tile:
    def __init__(self, ID, value = 0, color = "gray", row = 0, col = 0):
        self.ID = ID
        self.color = color
        self.value = value

        self.row = row
        self.col = col

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
canvas.grid(row = 1, column = 0, sticky = "nsew")
root.bind("<KeyPress>", keyChecker)

root.grid_columnconfigure(0, weight = 1)
root.grid_rowconfigure(1, weight = 1)

# root.grid_rowconfigure(1, weight = 1)
# root.grid_columnconfigure(1, weight = 1)

canvas.focus_set()

movePerSecondLabel = tk.Label(root, text = "")
movePerSecondLabel.grid(row = 0, column = 0, sticky = "ne")

moveTotalLabel = tk.Label(root, text = "")
moveTotalLabel.grid(row = 0, column = 0, sticky = "nw")

solved = False

def onListEnter():
    moveList = puzzle.checkListValidity()
    print("The move list contains:", moveList)
    for move in list(moveList):
        puzzle.moveTile(moveConverter(move))
        moveTimer.addMove(move)
    updateBoard()

def onKeyPress(key):
    global solved

    if not solved:
        if key == "Up" or key == "w":
            moveTimer.addMove(puzzle.moveTile("up"))

        if key == "Down" or key == "s":
            moveTimer.addMove(puzzle.moveTile("down"))

        if key == "Left" or key == "a":
            moveTimer.addMove(puzzle.moveTile("left"))

        if key == "Right" or key == "d":
            moveTimer.addMove(puzzle.moveTile("right"))

    updateBoard()

def onMouseEnter(event, object): # TODO: Advanced mousemovement (doesnt need to be adjacent to zero)
    global solved

    if not solved:
        currentMove = moveConverter(puzzle.getMove(object.getVal()))

        if currentMove != None:
            moveTimer.addMove(currentMove)

        puzzle.moveTile(puzzle.getMove(object.getVal()))

    updateBoard()

def resetBoard():
        moveTimer.restartTime()
        puzzle.scramblePuzzle()
        puzzle.displayPuzzle()
        updateBoard()

boxWidth = 50
boxSpacing = 1
puzzleWidth = boxWidth * 4

def updateBoard():
    global solved

    solved = True

    for i in range(4):
        for j in range(4):
            tileObj = spaceList[i][j]
            tileObj.value = puzzle.getVal(i, j)

            xPos = ((canvas.winfo_width() - (puzzleWidth + (3 * boxSpacing))) / 2) + (boxWidth * (tileObj.col) + boxSpacing)
            yPos = ((canvas.winfo_height() - (puzzleWidth + (3 * boxSpacing))) / 2) + (boxWidth * (tileObj.row) + boxSpacing)

            canvas.coords(tileObj.canvas_id, xPos, yPos, xPos + boxWidth, yPos + boxWidth)
            canvas.coords(tileObj.text_id, xPos + boxWidth / 2, yPos + boxWidth / 2)

            displayValue = int(tileObj.value, 16)

            if tileObj.value == "0": # its an int now not a string
                canvas.itemconfigure(tileObj.canvas_id, fill = "black")
                canvas.itemconfigure(tileObj.text_id, text = "")
            else:
                if tileObj.ID == displayValue:
                    canvas.itemconfigure(tileObj.canvas_id, fill = "orange", outline = "white")
                else:
                    solved = False
                    canvas.itemconfigure(tileObj.canvas_id, fill = "blue", outline = "white")

                canvas.itemconfigure(tileObj.text_id, text = displayValue)
                # canvas.itemconfigure(tileObj.text_id, text = tileObj.ID) # Show something instead of Value

spaceList = [
    [],
    [],
    [],
    []
]

for i in range(4): # TODO: change to be flexible between puzzle sizes
    for j in range(4):
        spaceList[i].append(Tile((i * 4) + j + 1, row = i, col = j))

        tileObj = spaceList[i][j]

        tileObj.x = j * (boxSpacing + boxWidth)
        tileObj.y = i * (boxSpacing + boxWidth)

        # tileObj.canvas_id = canvas.create_rectangle(
        #     tileObj.x, tileObj.y,
        #     tileObj.x + boxWidth,
        #     tileObj.y + boxWidth,
        #     fill = "blue"
        # )

        xPos = ((root.winfo_width() - (puzzleWidth + (3 * boxSpacing))) / 2) + (boxWidth * (tileObj.col) + boxSpacing)
        yPos = ((root.winfo_height() - (puzzleWidth + (3 * boxSpacing))) / 2) + (boxWidth * (tileObj.row) + boxSpacing)

        tileObj.canvas_id = canvas.create_rectangle(
            xPos, tileObj.y,
            xPos + boxWidth, tileObj.y + boxWidth,
            fill = "blue"
        )

        tileObj.text_id = canvas.create_text(
            xPos + boxWidth / 2,
            tileObj.y + boxWidth / 2,
            text = tileObj.getVal()
        )

        canvas.tag_bind(tileObj.canvas_id, "<Enter>", lambda e, o = tileObj: onMouseEnter(e, o))



def updateMPS():
    movesPerSecond = moveTimer.getMPS()
    movesTotal = moveTimer.getMoves()

    movePerSecondLabel.config(text = f"MPS: {movesPerSecond}")
    moveTotalLabel.config(text = f"Moves: {movesTotal}")
    updateBoard()

    root.after(100, updateMPS)  # Call as often as possible (every ~1ms)

# Initial setup
resetBoard()
updateBoard()
updateMPS()

root.mainloop()
