import puzzle, window, statistics, constants

class FifteenPuzzle:
    def __init__(self):
        self.puzzle = puzzle.Puzzle()
        self.window = window.Window(self.puzzle)

fifteenPuzzle = FifteenPuzzle()
