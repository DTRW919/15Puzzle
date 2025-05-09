import tkinter as tk
import puzzle

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




root = tk.Tk()
canvas = tk.Canvas(root, width = 800, height = 400, bg = "black")
canvas.pack()

def onMouseEnter(event, object): # TODO: Advanced mousemovement (doesnt need to be adjacent to zero)
    puzzle.moveTile(puzzle.getMove(object.getVal()))

    updateBoard()

def updateBoard():
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
                    canvas.itemconfigure(tileObj.canvas_id, fill = "blue", outline = "white")

                canvas.itemconfigure(tileObj.text_id, text = displayValue)
                # canvas.itemconfigure(tileObj.text_id, text = tileObj.ID) # Show ID instead of Value



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

tempArray = [[],[],[],[]]
for row in range(4):
    for col in range(4):
        tempArray[row].append((row * 4) + col)
print(tempArray)

updateBoard()

root.mainloop()
