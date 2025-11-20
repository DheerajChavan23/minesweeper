# minesweeper/ui/components/game_board.py
import tkinter as tk
from minesweeper.ui.themes import CELL_COLORS, NUMBER_COLORS, FONT_SETTINGS, CELL_SIZE

class GameBoard:
    def __init__(self, parent, on_cell_click, on_cell_right_click, on_cell_hover):
        self.parent = parent
        self.on_cell_click = on_cell_click
        self.on_cell_right_click = on_cell_right_click
        self.on_cell_hover = on_cell_hover
        
        self.buttons = []
        self.selected_row = 0
        self.selected_col = 0
        self.keyboard_mode = False
        
        self.setup_board_frame()

    def setup_board_frame(self):
        """Create the main board frame"""
        self.board_frame = tk.Frame(self.parent, bg='gray')
        self.board_frame.pack(pady=3)

    def create_board(self, rows, cols):
        """Create or recreate the game board with given dimensions"""
        # Clear existing board
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.buttons = []
        self.rows = rows
        self.cols = cols
        
        # Create button grid
        for r in range(rows):
            row_buttons = []
            for c in range(cols):
                btn = self.create_cell_button(r, c)
                btn.grid(row=r, column=c)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def create_cell_button(self, r, c):
        """Create an individual cell button"""
        btn = tk.Button(
            self.board_frame,
            width=CELL_SIZE['width'],
            height=CELL_SIZE['height'],
            relief='raised',
            bg=CELL_COLORS['default'],
            font=FONT_SETTINGS['cell'],
            command=lambda: self.on_cell_click(r, c)
        )
        
        # Bind right click and hover events
        btn.bind('<Button-3>', lambda e: self.on_cell_right_click(r, c))
        btn.bind("<Enter>", lambda e: self.on_cell_hover(r, c, True))
        btn.bind("<Leave>", lambda e: self.on_cell_hover(r, c, False))
        
        return btn

    def update_cell(self, r, c, cell):
        """Update the appearance of a single cell"""
        btn = self.buttons[r][c]
        
        if cell.revealed:
            btn.config(relief='sunken', bg=CELL_COLORS['revealed'])
            if cell.is_mine:
                btn.config(text="💣", bg=CELL_COLORS['mine'], fg='black')
            elif cell.value > 0:
                btn.config(text=str(cell.value), fg=NUMBER_COLORS[cell.value])
            else:
                btn.config(text="")
        elif cell.marked:
            btn.config(text="🚩", fg='red', bg=CELL_COLORS['default'])
        else:
            btn.config(text="", bg=CELL_COLORS['default'], relief='raised')
        
        # Reapply keyboard highlight if this is the selected cell
        if self.keyboard_mode and r == self.selected_row and c == self.selected_col:
            self.highlight_selected_cell()

    def update_board(self, board):
        """Update the entire board"""
        for r in range(self.rows):
            for c in range(self.cols):
                self.update_cell(r, c, board.grid[r][c])

    def highlight_selected_cell(self):
        """Highlight the currently selected cell for keyboard navigation"""
        if not self.keyboard_mode:
            return
            
        btn = self.buttons[self.selected_row][self.selected_col]
        cell = self.get_current_cell()  # This will be provided by the main app
        
        if not cell.revealed and not cell.marked:
            btn.config(bg='yellow', relief='sunken')
        elif cell.revealed:
            btn.config(bg='lightyellow')
        else:  # Marked cell
            btn.config(bg='orange')

    def clear_cell_highlight(self, r, c):
        """Remove highlight from a cell"""
        btn = self.buttons[r][c]
        cell = self.get_current_cell()  # This will be provided by the main app
        
        if cell.revealed:
            btn.config(bg=CELL_COLORS['revealed'])
        elif cell.marked:
            btn.config(bg=CELL_COLORS['default'])
        else:
            btn.config(bg=CELL_COLORS['default'], relief='raised')

    def move_selection(self, row_delta, col_delta):
        """Move keyboard selection with arrow keys"""
        if not self.keyboard_mode:
            return
            
        # Clear previous highlight
        self.clear_cell_highlight(self.selected_row, self.selected_col)
        
        # Calculate new position with wrap-around
        new_row = (self.selected_row + row_delta) % self.rows
        new_col = (self.selected_col + col_delta) % self.cols
        
        self.selected_row = new_row
        self.selected_col = new_col
        
        # Highlight new selection
        self.highlight_selected_cell()

    def set_keyboard_mode(self, enabled):
        """Enable or disable keyboard mode"""
        self.keyboard_mode = enabled
        if not enabled:
            self.clear_cell_highlight(self.selected_row, self.selected_col)

    def get_selected_cell(self):
        """Get currently selected cell coordinates"""
        return (self.selected_row, self.selected_col)

    def set_cell_provider(self, cell_provider_func):
        """Set a function to get cell data (will be provided by main app)"""
        self.get_current_cell = cell_provider_func