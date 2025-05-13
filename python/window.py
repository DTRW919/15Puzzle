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

    def getVal(self, otherValue = None):
        if not otherValue:
            return self.value
        elif otherValue == "row":
            return self.row
        elif otherValue == "col":
            return self.col

def getColor(val):
    if val in {1, 2, 3, 4}:
        return "#f5462f"
    if val in {5, 9, 13}:
        return "#ffc917"
    if val in {6, 7, 8}:
        return "#1eb34b"
    if val in {10, 14}:
        return "#3081bf"
    if val in {11, 12}:
        return "#5f3787"
    if val in {15}:
        return "#b34db1"

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

def onResize(event):
    for i in range(4):
        for j in range(4):
            tileObj = spaceList[i][j]

            xPos = ((canvas.winfo_width() - (puzzleWidth + (3 * boxSpacing))) / 2) + (boxWidth * (tileObj.col) + boxSpacing)
            yPos = ((canvas.winfo_height() - (puzzleWidth + (3 * boxSpacing))) / 2) + (boxWidth * (tileObj.row) + boxSpacing)

            canvas.coords(tileObj.canvas_id, xPos, yPos, xPos + boxWidth, yPos + boxWidth)
            canvas.coords(tileObj.text_id, xPos + boxWidth / 2, yPos + boxWidth / 2)

def onAdvancedToggle():
    global advanced

    if advanced:
        advanced = False
    else:
        advanced = True

    print(f"Toggled Advanced Move {advanced}")

def getAdvanced():
    global advanced

    return advanced

root = tk.Tk()
canvas = tk.Canvas(root, width = 800, height = 400, bg = "black", highlightthickness = 0)
canvas.grid(row = 1, column = 0, sticky = "nsew")
canvas.bind("<Configure>", onResize)

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

timeTakenLabel = tk.Label(root, text = "")
timeTakenLabel.grid(row = 0, column = 0, sticky = "n")

# advanced = tk.BooleanVar() # Advanced boolean
advanced = False
advancedToggle = tk.Checkbutton(root, text = "Advanced Mode?", command = onAdvancedToggle)
advancedToggle.grid(row = 2, column = 0, sticky = "se")

solved = False # Check if puzzle is solved
startSolving = False # Check if puzzle has been started

stats = moveTimer.Stats()

def onListEnter():
    moveList = puzzle.checkListValidity()
    print("The move list contains:", moveList)
    for move in list(moveList):
        puzzle.moveTile(moveConverter(move), getAdvanced())
        stats.addMove(move)
    # updateBoard()

def onKeyPress(key):
    global solved

    if not solved:
        if key == "Up" or key == "w":
            stats.addMove(puzzle.moveTile("up", getAdvanced()))

        if key == "Down" or key == "s":
            stats.addMove(puzzle.moveTile("down", getAdvanced()))

        if key == "Left" or key == "a":
            stats.addMove(puzzle.moveTile("left", getAdvanced()))

        if key == "Right" or key == "d":
            stats.addMove(puzzle.moveTile("right", getAdvanced()))

    # updateBoard()

def onMouseEnter(event, object): # TODO: Advanced mousemovement (doesnt need to be adjacent to zero)
    global solved

    if not solved:
        currentMove = moveConverter(puzzle.getMove(object.getVal(), getAdvanced()))

        if currentMove != None:
            stats.addMove(currentMove)

        puzzle.moveTile(puzzle.getMove(object.getVal(), getAdvanced()), getAdvanced(), object.getVal("col"), object.getVal("row"))

    # updateBoard()

def resetBoard():
        stats.resetAll()
        puzzle.scramblePuzzle()
        puzzle.displayPuzzle()
        updateBoard(reset = True)

boxWidth = 100
boxSpacing = 1
puzzleWidth = boxWidth * 4

def updateBoard(advanced = False, reset = False):
    global solved

    if not solved or reset:
        solved = True

        for i in range(4):
            for j in range(4):
                tileObj = spaceList[i][j]
                tileObj.value = puzzle.getVal(i, j)

                displayValue = int(tileObj.value, 16)

                if not advanced:
                    if tileObj.value == "0":
                        canvas.itemconfigure(tileObj.canvas_id, fill = "black", outline = "black")
                        canvas.itemconfigure(tileObj.text_id, text = "")
                    else:
                        if tileObj.ID == displayValue:
                            canvas.itemconfigure(tileObj.canvas_id, fill = "orange", outline = "black")
                        else:
                            solved = False
                            canvas.itemconfigure(tileObj.canvas_id, fill = "blue", outline = "black")

                        canvas.itemconfigure(tileObj.text_id, text = displayValue, fill = "white")
                        # canvas.itemconfigure(tileObj.text_id, text = tileObj.ID) # Show something instead of Value
                else:
                    if tileObj.value == "0":
                        canvas.itemconfigure(tileObj.canvas_id, fill = "black", outline = "")
                        canvas.itemconfigure(tileObj.text_id, text = "")
                    else:
                        if tileObj.ID != displayValue:
                            solved = False
                        canvas.itemconfigure(tileObj.canvas_id, fill = getColor(displayValue), outline = "")
                        canvas.itemconfigure(tileObj.text_id, text = displayValue, fill = "black")
        if solved:
            stats.setSolving(False)
            allMoves = [move.direction for move in stats.getMovesHistory()]
            print(f"It took you {stats.getNumMoves()} to solve this puzzle in {stats.getTime()} seconds. The sequence you took is:")
            print(*allMoves, sep = "")

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

        xPos = ((root.winfo_width() - (puzzleWidth + (3 * boxSpacing))) / 2) + (boxWidth * (tileObj.col) + boxSpacing)
        yPos = ((root.winfo_height() - (puzzleWidth + (3 * boxSpacing))) / 2) + (boxWidth * (tileObj.row) + boxSpacing)

        tileObj.canvas_id = canvas.create_rectangle(
            xPos, tileObj.y,
            xPos + boxWidth, tileObj.y + boxWidth,
            fill = "blue",
            outline = "black",
            width = 5
        )

        tileObj.text_id = canvas.create_text(
            xPos + boxWidth / 2,
            tileObj.y + boxWidth / 2,
            text = tileObj.getVal(),
            fill = "white",
            font = ("SF Pro", 50, "bold")
        )

        canvas.tag_bind(tileObj.canvas_id, "<Enter>", lambda e, o = tileObj: onMouseEnter(e, o))

def updateInfo():
    movesPerSecond = stats.getMPS()
    movesTotal = stats.getNumMoves()
    timeTaken = stats.getTime()

    movePerSecondLabel.config(text = f"MPS: {movesPerSecond}")
    moveTotalLabel.config(text = f"Moves: {movesTotal}")
    timeTakenLabel.config(text = f"Time: {timeTaken}")

    updateBoard(advanced = getAdvanced())

    root.after(20, updateInfo)  # Call as often as possible (every ~1ms)

# Initial setup
resetBoard()
updateBoard()
updateInfo()

root.mainloop()
