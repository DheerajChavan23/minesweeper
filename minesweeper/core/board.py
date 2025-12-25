class Cell:
    """
    Represents a single cell of the Minesweeper game board.
    """
    def __init__(self):
        self.is_mine = False     # True if this cell contains a mine
        self.value = 0           # Number of adjacent mines (0-8)
        self.revealed = False    # True if player has clicked on this cell
        self.marked = False      # True if player has placed a flag on this cell

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbours(self, r, c):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.in_bounds(nr, nc):
                    yield nr, nc

    def place_mines(self, first_click):
        import random
        safe_zone = {(first_click[0] + dr, first_click[1] + dc)
                     for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                     if self.in_bounds(first_click[0] + dr, first_click[1] + dc)}
        candidates = [(r, c) for r in range(self.rows) for c in range(self.cols)
                      if (r, c) not in safe_zone]
        self.mine_positions = set(random.sample(candidates, self.mines))
        for r, c in self.mine_positions:
            self.grid[r][c].is_mine = True

        for r, c in self.mine_positions:
            for nr, nc in self.neighbours(r, c):
                self.grid[nr][nc].value += 1

    def reveal(self, r, c):
        if not self.in_bounds(r, c) or self.grid[r][c].revealed:
            return []

        queue = [(r, c)]
        revealed = []

        while queue:
            cr, cc = queue.pop()
            cell = self.grid[cr][cc]
            if cell.revealed or cell.marked:
                continue
            cell.revealed = True
            revealed.append((cr, cc))
            if cell.value == 0 and not cell.is_mine:
                for nr, nc in self.neighbours(cr, cc):
                    if not self.grid[nr][nc].revealed:
                        queue.append((nr, nc))

        return revealed

    def toggle_mark(self, r, c):
        if self.in_bounds(r, c) and not self.grid[r][c].revealed:
            self.grid[r][c].marked = not self.grid[r][c].marked

    def is_mine(self, r, c):
        return self.grid[r][c].is_mine

    def is_revealed(self, r, c):
        return self.grid[r][c].revealed

    def is_marked(self, r, c):
        return self.grid[r][c].marked

    def get_value(self, r, c):
        return self.grid[r][c].value

    def all_safe_cells_revealed(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if not cell.is_mine and not cell.revealed:
                    return False
        return True

    def reveal_all(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c].revealed = True
