# minesweeper/ui/main_app.py - UPDATED
import os
import tkinter as tk
from minesweeper.core.game import Game
from minesweeper.data.highscores import HighScoreManager
from minesweeper.analytics.analyzer import AnalyticsRunner
from minesweeper.ui.components.control_panel import ControlPanel
from minesweeper.ui.components.status_panel import StatusPanel
from minesweeper.ui.components.game_board import GameBoard
from minesweeper.ui.components.dialogs import DialogManager

DIFFICULTIES = {
    'easy': (9, 9, 10),
    'medium': (16, 16, 40), 
    'hard': (16, 30, 99)
}

class MinesweeperApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.root.configure(bg='lightgray')
        
        # Initialize managers
        self.highscores = HighScoreManager()
        self.analytics = AnalyticsRunner()
        self.dialogs = DialogManager(self.root)
        
        # Game state
        self.difficulty = 'easy'
        self.rows, self.cols, self.mines = DIFFICULTIES[self.difficulty]
        self.game = None
        
        # Setup UI with new layout structure
        self.setup_ui()
        self.setup_keyboard_bindings()
        self.start_game()
        
        # Start timer
        self.root.after(1000, self.update_timer)

    def setup_ui(self):
        """Setup the main user interface with the new layout structure"""
        # 1. TOP: ONLY Difficulty buttons
        self.control_panel = ControlPanel(
            self.root,
            on_difficulty_change=self.set_difficulty
        )  # REMOVED: other callbacks since we only need difficulty change
        
        # 2. STATUS: Mines counter, Face button, Timer
        self.status_panel = StatusPanel(
            self.root,
            on_reset_game=self.reset_game
        )
        
        # 3. CENTER: Game board
        self.game_board = GameBoard(
            self.root,
            on_cell_click=self.handle_cell_click,
            on_cell_right_click=self.handle_cell_right_click,
            on_cell_hover=self.handle_cell_hover
        )
        
        # 4. BOTTOM: Control buttons (New Game, Highscores, Analytics, How to Play)
        self.setup_bottom_controls()
        
        # 5. FOOTER: Keyboard status and help
        self.setup_footer()
        
        # Provide cell data to game board
        self.game_board.set_cell_provider(self.get_current_cell)

    def setup_bottom_controls(self):
        """Create bottom control buttons"""
        self.bottom_frame = tk.Frame(self.root, bg='lightgray')
        self.bottom_frame.pack(pady=10)
        
        buttons = [
            ('NEW GAME', self.reset_game),
            ('HIGHSCORES', self.show_highscores),
            ('ANALYTICS', self.run_analytics),
            ('HOW TO PLAY', self.show_how_to_play)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                self.bottom_frame, 
                text=text, 
                width=10, 
                command=command,
                font=('Arial', 8, 'bold'),
                bg='gray',
                relief='raised',
                bd=2
            )
            btn.pack(side='left', padx=3)

    def setup_footer(self):
        """Create footer with keyboard status and help"""
        self.footer_frame = tk.Frame(self.root, bg='lightgray')
        self.footer_frame.pack(pady=5)
        
        # Keyboard status
        self.keyboard_status = tk.Label(
            self.footer_frame,
            text='Keyboard: [OFF]',
            font=('Arial', 8, 'bold'),
            fg='darkgreen',
            bg='lightgray'
        )
        self.keyboard_status.pack(side='left', padx=10)
        
        # Help text
        self.help_label = tk.Label(
            self.footer_frame,
            text='Press F1 for keyboard controls help',
            font=('Arial', 8),
            fg='gray',
            bg='lightgray'
        )
        self.help_label.pack(side='left', padx=10)

    def update_keyboard_status(self, enabled):
        """Update keyboard status display"""
        status = 'ON' if enabled else 'OFF'
        color = 'green' if enabled else 'darkgreen'
        self.keyboard_status.config(
            text=f'Keyboard: [{status}]',
            fg=color
        )

    def toggle_keyboard_mode(self):
        """Toggle keyboard navigation mode"""
        current_mode = self.game_board.keyboard_mode
        self.game_board.set_keyboard_mode(not current_mode)
        self.status_panel.set_keyboard_mode(not current_mode)
        self.update_keyboard_status(not current_mode)

    # ... rest of your methods remain exactly the same
    def get_current_cell(self):
        """Provide current cell data to game board component"""
        if self.game and self.game.board:
            row, col = self.game_board.get_selected_cell()
            if (0 <= row < self.rows and 0 <= col < self.cols):
                return self.game.board.grid[row][col]
        return None

    def setup_keyboard_bindings(self):
        """Setup keyboard bindings"""
        # Navigation
        self.root.bind('<Up>', lambda e: self.game_board.move_selection(-1, 0))
        self.root.bind('<Down>', lambda e: self.game_board.move_selection(1, 0))
        self.root.bind('<Left>', lambda e: self.game_board.move_selection(0, -1))
        self.root.bind('<Right>', lambda e: self.game_board.move_selection(0, 1))
        
        # Actions
        self.root.bind('<space>', lambda e: self.handle_cell_click(*self.game_board.get_selected_cell()))
        self.root.bind('<Return>', lambda e: self.handle_cell_click(*self.game_board.get_selected_cell()))
        self.root.bind('f', lambda e: self.handle_cell_right_click(*self.game_board.get_selected_cell()))
        self.root.bind('F', lambda e: self.handle_cell_right_click(*self.game_board.get_selected_cell()))
        
        
        # Game control
        self.root.bind('n', lambda e: self.reset_game())
        self.root.bind('r', lambda e: self.reset_game())
        
        # Difficulty switching
        self.root.bind('e', lambda e: self.set_difficulty('easy'))
        self.root.bind('m', lambda e: self.set_difficulty('medium'))
        self.root.bind('h', lambda e: self.set_difficulty('hard'))
        self.root.bind('c', lambda e: self.set_difficulty('custom'))
        
        # Help and mode
        self.root.bind('<F1>', lambda e: self.dialogs.show_keyboard_help())
        self.root.bind('<Tab>', lambda e: self.toggle_keyboard_mode())
        self.root.bind('<Escape>', lambda e: self.game_board.set_keyboard_mode(False))
        
        self.root.focus_set()

    def set_difficulty(self, level):
        """Set game difficulty"""
        if level == 'custom':
            config = self.dialogs.get_custom_config()
            if config:
                self.rows, self.cols, self.mines = config
        else:
            self.difficulty = level
            self.rows, self.cols, self.mines = DIFFICULTIES[level]
        self.start_game()

    def start_game(self):
        """Start a new game"""
        self.game = Game(self.rows, self.cols, self.mines)
        self.game_board.create_board(self.rows, self.cols)
        self.status_panel.update_face_button('playing')
        self.update_mines_display()
        self.root.focus_set()

    def handle_cell_click(self, r, c):
        """Handle cell click"""
        if self.game.lost or self.game.won:
            return
        
        revealed_cells = self.game.click(r, c)
        self.update_display()
        self.check_game_end()

    def handle_cell_right_click(self, r, c):
        """Handle cell right click (flag)"""
        if self.game.lost or self.game.won:
            return
        self.game.mark(r, c)
        self.game_board.update_cell(r, c, self.game.board.grid[r][c])
        self.update_mines_display()

    def handle_cell_hover(self, r, c, is_enter):
        """Handle cell hover"""
        if self.game_board.keyboard_mode and (r == self.game_board.selected_row and c == self.game_board.selected_col):
            return
            
        cell = self.game.board.grid[r][c]
        if not cell.revealed and not cell.marked:
            # This will be handled by the GameBoard component
            pass

    def update_display(self):
        """Update the entire game display"""
        self.game_board.update_board(self.game.board)
        self.update_mines_display()

    def update_mines_display(self):
        """Update mines counter"""
        if self.game:
            marked = sum(cell.marked for row in self.game.board.grid for cell in row)
            remaining = max(0, self.mines - marked)
            self.status_panel.update_mines_display(remaining)

    def update_timer(self):
        """Update game timer"""
        if self.game and not self.game.first_click and not self.game.lost and not self.game.won:
            elapsed = int(self.game.get_elapsed_time())
            self.status_panel.update_timer(elapsed)
        self.root.after(1000, self.update_timer)

    def check_game_end(self):
        """Check if game has ended"""
        if self.game.lost:
            self.status_panel.update_face_button('lost')
            self.dialogs.show_game_over()
        elif self.game.won:
            self.status_panel.update_face_button('won')
            elapsed = self.game.get_elapsed_time()
            if self.highscores.is_highscore(self.rows, self.cols, self.mines, elapsed):
                name = self.dialogs.ask_player_name()
                if name:
                    self.highscores.add_score(self.rows, self.cols, self.mines, name, elapsed)
            self.dialogs.show_victory(elapsed)

    def reset_game(self):
        """Reset the current game"""
        self.status_panel.update_timer(0)
        self.start_game()

    def show_highscores(self):
        """Show highscores dialog"""
        self.dialogs.show_highscores(self.highscores, (self.rows, self.cols, self.mines))

    def run_analytics(self):
        """Run analytics and generate PDF report"""
        config = self.dialogs.get_analytics_config((self.rows, self.cols, self.mines))
        if config:
            rows, cols, mines, sample_size = config
            try:
                progress_popup = self.dialogs.show_progress_popup("Generating Analytics", "Generating analytics report...")
                
                # CHANGED: Let the analyzer handle the path automatically
                pdf_path = self.analytics.run_all(rows, cols, mines, sample_size=sample_size, generate_pdf=True)
                
                if progress_popup:
                    progress_popup.destroy()
                
                if pdf_path:
                    self.dialogs.show_analytics_complete((rows, cols, mines), sample_size, pdf_path)
                else:
                    self.dialogs.show_analytics_error("Failed to generate PDF file")
                    
            except Exception as e:
                if 'progress_popup' in locals() and progress_popup:
                    progress_popup.destroy()
                self.dialogs.show_analytics_error(str(e))

    def show_how_to_play(self):
        """Show how to play instructions"""
        self.dialogs.show_how_to_play()

    def run(self):
        """Start the application"""
        self.root.mainloop()