import puzzle, window, moveTimer, constants

class FifteenPuzzle:
    def __init__(self):
        self.puzzle = puzzle.Puzzle()
        self.window = window.Window(self.puzzle)
