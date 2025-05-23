import tkinter
import statistics, constants, puzzle

class Window:
    def __init__(self, puzzle: puzzle.Puzzle): # Requires a puzzle to bind to
        self.root = tkinter.Tk()
        self.root.grid_rowconfigure(1, weight = 1)
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.bind("<KeyPress>", self.onKeyPress) # Track and react to key presses

        self.canvas = tkinter.Canvas(self.root, width = 800, height = 400, bg = "#000000", highlightthickness = 0)
        self.canvas.grid(row = 1, column = 0, sticky = "nsew")
        self.canvas.bind("<Configure>", self.onResize) # Track and react to resizing

        self.puzzle = puzzle # Reference in constructor

        self.stats = statistics.Statistics()
        self.constants = constants.Constants()

        self.advanced = self.constants.getConstant("tiles.advanced")

        self.tileList = [[], [], [], []]

        for i in range(4): # Initial tile set up
            for j in range(4):
                self.tileList[i].append(self.Tile(ID = ((i * 4) + j + 1), row = i, col = j, window = self))

                tileObj = self.tileList[i][j]

                if tileObj.ID == 16:
                    tileObj.ID = 0

                tileObj.canvas_id = self.canvas.create_rectangle(
                    0, 0, 0, 0,
                    fill = "blue",
                    outline = "black",
                    width = 5,
                    tags = tileObj.tag
                )

                tileObj.text_id = self.canvas.create_text(
                    0, 0,
                    text = tileObj.getAttribute(),
                    fill = "white",
                    font = ("SF Pro", 50, "bold"),
                    tags = tileObj.tag
                )

                self.canvas.tag_bind( # Bind mouse detection to each tile
                    tileObj.canvas_id,
                    "<Enter>",
                    lambda e, o = tileObj: self.onMouseEnter(e, o)
                )

                self.canvas.tag_bind(
                    tileObj.tag,
                    "<Button-1>",
                    lambda e, o = tileObj: self.onMouseClick(e, o)
                )

        self.movesTotalLabel = tkinter.Label(self.root, text = "Moves: ")
        self.movesTotalLabel.grid(row = 0, sticky = "nw")
        self.timeTakenLabel = tkinter.Label(self.root, text = "Time: ")
        self.timeTakenLabel.grid(row = 0, sticky = "n")
        self.movesPerSecondLabel = tkinter.Label(self.root, text = "MPS: ")
        self.movesPerSecondLabel.grid(row = 0, sticky = "ne")

        totalAverage = self.stats.getStat("average") # Bottom labels require initial values
        averageOfFive = self.stats.getStat("Ao5")
        bestTime = self.stats.getRecord("time")

        self.totalAverageLabel = tkinter.Label(self.root, text = f"Average Time: {round(totalAverage[0], 3)}")
        self.totalAverageLabel.grid(row = 2, sticky = "sw")
        self.averageOfFiveLabel = tkinter.Label(self.root, text = f"Ao5: {round(averageOfFive[0], 3)}")
        self.averageOfFiveLabel.grid(row = 2, sticky = "s")
        self.bestTimeLabel = tkinter.Label(self.root, text = f"Best Time: {bestTime[0]}")
        self.bestTimeLabel.grid(row = 2, sticky = "se")

        self.solving = False # Initially not solving

        self.periodic() # Initial periodic function

        self.root.mainloop() # Start window

    class Tile:
        def __init__(self, ID, value = "0", tileColor = "gray", textColor = "white", row = 0, col = 0, window = None):
            self.parent = window # Mainly for accessing constants

            self.tileColor = tileColor
            self.textColor = textColor

            self.ID = ID # Unchanging integer ID
            self.value = value # String value in hexidecimal
            self.display = int(self.value, 16) # Int value integer based on self.value

            self.row = row
            self.col = col

            self.canvas_id = None
            self.text_id = None

            self.tag = ("tile" + str(self.ID))

            self.x = 0
            self.y = 0

        def getAttribute(self, attribute = "value"): # Returns self.value by default
            if not attribute:
                return self.value
            elif attribute == "row":
                return self.row
            elif attribute == "col":
                return self.col

        def updateDisplayValue(self):
            self.display = int(self.value, 16)

        def updateColor(self):
            constantsReference = self.parent.constants

            self.parent.updateAdvanced()

            self.textColor = constantsReference.getConstant("colors.white")

            if self.display in {0}:
                self.tileColor = constantsReference.getConstant("colors.black")
                self.textColor = constantsReference.getConstant("colors.black")
                return

            if not self.parent.advanced:
                if self.display == self.ID:
                    self.tileColor = constantsReference.getConstant("colors.orange")
                else:
                    self.tileColor = constantsReference.getConstant("colors.blue")
            else:
                if self.display in {1, 2, 3, 4}:
                    self.tileColor = constantsReference.getConstant("colors.red")
                elif self.display in {5, 9, 13}:
                    self.tileColor = constantsReference.getConstant("colors.yellow")
                elif self.display in {6, 7, 8}:
                    self.tileColor = constantsReference.getConstant("colors.green")
                elif self.display in {10, 14}:
                    self.tileColor = constantsReference.getConstant("colors.blue")
                elif self.display in {11, 12}:
                    self.tileColor = constantsReference.getConstant("colors.purple")
                elif self.display in {15}:
                    self.tileColor = constantsReference.getConstant("colors.pink")

    def onResize(self, event = None):
        for i in range(4):
            for j in range(4):
                tileObj = self.tileList[i][j]

                tileWidth = self.constants.getConstant("tiles.tileWidth")
                tileSpacing = self.constants.getConstant("tiles.tileSpacing")
                puzzleWidth = (4 * tileWidth)

                xPos = ((self.root.grid_bbox(0, 0)[2] - (puzzleWidth + (3 * tileSpacing))) / 2) + (tileWidth * (tileObj.col) + tileSpacing)
                yPos = ((self.root.grid_bbox(0, 1)[3] - (puzzleWidth + (3 * tileSpacing))) / 2) + (tileWidth * (tileObj.row) + tileSpacing)

                self.canvas.coords(tileObj.canvas_id, xPos, yPos, xPos + tileWidth, yPos + tileWidth)
                self.canvas.coords(tileObj.text_id, xPos + (tileWidth / 2), yPos + (tileWidth / 2))

    def onKeyPress(self, event):
        key = event.keysym # Grab key from event

        settingKeys = [
            "space",
            "p"
        ]

        movementKeys = [
            "Up", "w", "Right", "d",
            "Down", "s", "Left", "a"
        ]

        if key in movementKeys:
            allegedKey = movementKeys[(int((movementKeys.index(key)) / 2)) * 2].lower() # Goofy logic to determine key pressed
            if not self.puzzle.getSolved():
                self.stats.addMove(self.puzzle.moveTarget(allegedKey, limited = True))

        elif key in settingKeys:
            if key == "space":
                self.puzzle.scramblePuzzle()
                self.solving = False
                self.stats.resetAll()
            elif key == "p":
                print(self.stats.getAverage(3))

    def onMouseClick(self, event, tileObj):
        self.updateAdvanced()

        if not self.advanced and not self.puzzle.getSolved():
            targetPos = self.puzzle.findTarget(tileObj.value)
            allegedMove = self.puzzle.getMove(targetPos[0], targetPos[1])

            if allegedMove != "invald":
                self.stats.addMove(self.puzzle.moveTarget(allegedMove, targetPos[0], targetPos[1]))

    def onMouseEnter(self, event, tileObj):
        self.updateAdvanced()

        if self.advanced and not self.puzzle.getSolved():
            targetPos = self.puzzle.findTarget(tileObj.value)
            allegedMove = self.puzzle.getMove(targetPos[0], targetPos[1])

            if allegedMove != "invald":
                self.stats.addMove(self.puzzle.moveTarget(allegedMove, targetPos[0], targetPos[1]))

    def isSolved(self):
        for i in range(4):
            for j in range(4):
                tileObj = self.tileList[i][j]

                if tileObj.display != tileObj.ID:
                    return False
        return True

    def updateTiles(self):
        for i in range(4):
            for j in range(4):
                tileObj = self.tileList[i][j]

                tileObj.value = self.puzzle.getPosVal(i, j) # Get values from puzzle reference
                tileObj.updateDisplayValue()
                tileObj.updateColor()

                self.canvas.itemconfigure(tileObj.canvas_id, fill = tileObj.tileColor)
                self.canvas.itemconfigure(tileObj.text_id, text = tileObj.display, fill = tileObj.textColor)

    def updateInfo(self):
        if not self.isSolved():
            movesTotal = self.stats.getNumMoves()
            timeTaken = self.stats.getTime()
            movesPerSecond = self.stats.getMPS()

            self.movesTotalLabel.config(text = f"Moves: {movesTotal}")
            self.timeTakenLabel.config(text = f"Time: {timeTaken}")
            self.movesPerSecondLabel.config(text = f"MPS: {movesPerSecond}")

    def updateAdvanced(self):
        self.advanced = self.constants.getConstant("tiles.advanced")

    def periodic(self):
        self.updateTiles()
        self.updateInfo()

        if self.puzzle.getStarted() and not self.solving: # On solve start:
            self.solving = True # Change state so this only runs once

            self.stats.startTracking()

        if self.puzzle.getSolved() and self.solving: # On solved:
            self.solving = False # Change state so this only runs once

            self.stats.stopTracking()
            self.stats.printFinished()

            totalAverage = self.stats.getStat("average")
            averageOfFive = self.stats.getStat("Ao5")
            bestTime = self.stats.getRecord("time")

            self.totalAverageLabel.config(text = f"Average Time: {round(totalAverage[0], 3)}", fg = self.constants.getConstant("colors." + totalAverage[1]))
            self.averageOfFiveLabel.config(text = f"Ao5: {round(averageOfFive[0], 3)}", fg = self.constants.getConstant("colors." + averageOfFive[1]))
            self.bestTimeLabel.config(text = f"Best Time: {bestTime[0]}", fg = self.constants.getConstant("colors." + bestTime[1]))


        self.root.after(20, self.periodic) # Recursively call every 20ms
