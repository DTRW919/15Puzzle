import tkinter as tk

# Example objects array (you can use any kind of object)
class MyObject:
    def __init__(self, id, x, y, size):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.canvas_id = None  # This will store the Canvas rectangle ID

# Sample array of objects
objects = [
    MyObject(id=1, x=50, y=50, size=40),
    MyObject(id=2, x=150, y=100, size=60),
    MyObject(id=3, x=250, y=150, size=30)
]

# Tkinter window and canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=300, bg='white')
canvas.pack()

# Draw squares on the canvas and store the canvas ID
for obj in objects:
    x1 = obj.x
    y1 = obj.y
    x2 = x1 + obj.size
    y2 = y1 + obj.size
    obj.canvas_id = canvas.create_rectangle(x1, y1, x2, y2, fill="skyblue")

# Example: move one square after 2 seconds
def move_object():
    obj = objects[0]
    canvas.move(obj.canvas_id, 50, 50)  # Move right 50px and down 50px

root.after(2000, move_object)



root.mainloop()
