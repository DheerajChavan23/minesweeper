import time
from collections import deque
from minesweeper.core.board import Board

class Game:
    def __init__(self, rows, cols, mines):
        self.board = Board(rows, cols, mines)
        self.started = False
        self.start_time = None
        self.end_time = None
        self.lost = False
        self.won = False
        self.first_click = True
        self.clicks = 0

    def click(self, r, c):
        if self.board.is_marked(r, c) or self.board.is_revealed(r, c):
            return []

        if self.first_click:
            self.board.place_mines((r, c))
            self.start_time = time.time()
            self.first_click = False
            self.started = True

        self.clicks += 1
        revealed = self.board.reveal(r, c)
        if self.board.is_mine(r, c):
            self.end_time = time.time()
            self.lost = True
            self.board.reveal_all()
        elif self.board.all_safe_cells_revealed():
            self.end_time = time.time()
            self.won = True

        return revealed

    def mark(self, r, c):
        self.board.toggle_mark(r, c)

    def get_elapsed_time(self):
        if self.start_time is None:
            return 0
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time