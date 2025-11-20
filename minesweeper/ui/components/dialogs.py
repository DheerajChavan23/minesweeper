# minesweeper/ui/components/dialogs.py
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class DialogManager:
    def __init__(self, parent):
        self.parent = parent

    def show_highscores(self, highscores, config):
        """Show highscores dialog"""
        rows, board_cols, mines = config  # CHANGED: renamed to board_cols
        
        win = tk.Toplevel(self.parent)
        win.title("Highscores")
        win.geometry("420x320")
        win.grab_set()

        # Get scores with debugging
        scores = highscores.get_top_scores(rows, board_cols, mines)  # CHANGED: use board_cols
        print(f"Dialog: Showing {len(scores)} scores for {rows}x{board_cols}_{mines}")  # CHANGED

        header = tk.Label(
            win,
            text=f"Top 10 - {rows}x{board_cols}, {mines} mines",  # CHANGED
            font=('Arial', 12, 'bold')
        )
        header.pack(padx=10, pady=10)

        # CHANGED: Use different variable names for Treeview columns
        tree_columns = ("rank", "name", "time")  # CHANGED: renamed to tree_columns
        tree = ttk.Treeview(win, columns=tree_columns, show="headings", height=10)  # CHANGED
        tree.heading("rank", text="Rank")
        tree.heading("name", text="Name")
        tree.heading("time", text="Time (s)")

        tree.column("rank", width=60, anchor="center")
        tree.column("name", width=220, anchor="center")
        tree.column("time", width=100, anchor="center")

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        if not scores:
            # Show empty message
            tree.insert("", "end", values=("No", "scores", "yet!"))
        else:
            for i, score in enumerate(scores, 1):
                tree.insert("", "end", values=(i, score['name'], f"{score['time']:.2f}"))

        close_btn = tk.Button(win, text="Close", command=win.destroy, width=8)
        close_btn.pack(pady=6, anchor="center")

    def get_custom_config(self):
        """Get custom board configuration from user"""
        popup = tk.Toplevel(self.parent)
        popup.title("Custom Configuration")
        popup.grab_set()

        tk.Label(popup, text="Rows (5–20):").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(popup, text="Cols (5–40):").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(popup, text="Mines:").grid(row=2, column=0, padx=10, pady=5)

        e_rows = tk.Entry(popup)
        e_cols = tk.Entry(popup)
        e_mines = tk.Entry(popup)

        e_rows.grid(row=0, column=1, padx=10, pady=5)
        e_cols.grid(row=1, column=1, padx=10, pady=5)
        e_mines.grid(row=2, column=1, padx=10, pady=5)

        result = []

        def submit():
            try:
                r = int(e_rows.get())
                c = int(e_cols.get())
                m = int(e_mines.get())
                if 5 <= r <= 20 and 5 <= c <= 40 and 1 <= m < r * c:
                    result.extend([r, c, m])
                    popup.destroy()
                else:
                    messagebox.showerror("Invalid Input", f"Rows 5–20, Cols 5–40, Mines 1–{r*c - 1}")
            except ValueError:
                messagebox.showerror("Invalid Input", "All fields must be integers.")

        tk.Button(popup, text="Start", command=submit).grid(row=3, column=0, columnspan=2, pady=10)
        popup.wait_window()
        return result if result else None

# minesweeper/ui/components/dialogs.py

    def get_analytics_config(self, current_config):
        """Get analytics configuration from user"""
        popup = tk.Toplevel(self.parent)
        popup.title("Analytics Configuration")
        popup.geometry("450x450")  # CHANGED: Increased window size
        popup.minsize(450, 450)   # ADDED: Set minimum size
        popup.grab_set()
        
        # Default values (use current game configuration as defaults)
        default_rows, default_cols, default_mines = current_config
        default_mines = min(default_mines, default_rows * default_cols - 1)
        default_samples = 100
        
        # Title
        title_label = tk.Label(popup, 
                            text="Generate Analytics PDF Report\nAll 4 visualizations will be included",
                            font=('Arial', 12, 'bold'),
                            pady=10)
        title_label.pack()
        
        # Configuration frame
        config_frame = tk.Frame(popup, padx=20, pady=10)
        config_frame.pack(fill='both', expand=True)
        
        # Rows input
        row_frame = tk.Frame(config_frame)
        row_frame.pack(fill='x', pady=5)
        tk.Label(row_frame, text="Rows (5-20):", width=15, anchor='w').pack(side='left')
        rows_var = tk.StringVar(value=str(default_rows))
        rows_entry = tk.Entry(row_frame, textvariable=rows_var, width=10)
        rows_entry.pack(side='left', padx=5)
        
        # Columns input
        col_frame = tk.Frame(config_frame)
        col_frame.pack(fill='x', pady=5)
        tk.Label(col_frame, text="Columns (5-40):", width=15, anchor='w').pack(side='left')
        cols_var = tk.StringVar(value=str(default_cols))
        cols_entry = tk.Entry(col_frame, textvariable=cols_var, width=10)
        cols_entry.pack(side='left', padx=5)
        
        # Mines input
        mine_frame = tk.Frame(config_frame)
        mine_frame.pack(fill='x', pady=5)
        tk.Label(mine_frame, text="Mines:", width=15, anchor='w').pack(side='left')
        mines_var = tk.StringVar(value=str(default_mines))
        mines_entry = tk.Entry(mine_frame, textvariable=mines_var, width=10)
        mines_entry.pack(side='left', padx=5)
        
        # Sample size input
        sample_frame = tk.Frame(config_frame)
        sample_frame.pack(fill='x', pady=5)
        tk.Label(sample_frame, text="Sample Size:", width=15, anchor='w').pack(side='left')
        sample_var = tk.StringVar(value=str(default_samples))
        sample_entry = tk.Entry(sample_frame, textvariable=sample_var, width=10)
        sample_entry.pack(side='left', padx=5)
        tk.Label(sample_frame, text="(10-5000 boards)", font=('Arial', 8), fg='gray').pack(side='left', padx=5)
        
        # Information text - CHANGED: Reduced height to make space for buttons
        info_text = tk.Text(config_frame, height=3, width=40, font=('Arial', 8))  # CHANGED: height from 4 to 3
        info_text.pack(pady=10, fill='x')
        info_text.insert('1.0', 
                        "This will generate a PDF report with:\n"
                        "• White cells distribution histogram\n"
                        "• Number frequency analysis\n" 
                        "• Mine clusters analysis\n"
                        "• Mine neighborhood heatmap\n\n"
                        "Larger sample sizes provide more accurate results but take longer to process.")
        info_text.config(state='disabled')
        
        result = []
        
        def submit():
            try:
                r = int(rows_var.get())
                c = int(cols_var.get())
                m = int(mines_var.get())
                s = int(sample_var.get())
                
                # Validate inputs
                if not (5 <= r <= 20):
                    messagebox.showerror("Invalid Input", "Rows must be between 5 and 20")
                    return
                    
                if not (5 <= c <= 40):
                    messagebox.showerror("Invalid Input", "Columns must be between 5 and 40")
                    return
                    
                if not (1 <= m < r * c):
                    messagebox.showerror("Invalid Input", f"Mines must be between 1 and {r*c - 1}")
                    return
                    
                if not (10 <= s <= 5000):
                    messagebox.showerror("Invalid Input", "Sample size must be between 10 and 5000")
                    return
                
                result.extend([r, c, m, s])
                popup.destroy()
                
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers in all fields")
        
        def cancel():
            popup.destroy()
        
        # Buttons frame - CHANGED: Added more padding at bottom
        button_frame = tk.Frame(popup, pady=15)  # CHANGED: Increased pady from 10 to 15
        button_frame.pack()
        
        tk.Button(button_frame, text="Generate PDF Report", command=submit, 
                bg='lightgreen', width=15).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancel", command=cancel, 
                width=10).pack(side='left', padx=10)
        
        # Set focus to first entry
        rows_entry.focus_set()
        
        popup.wait_window()
        return result if result else None

    def show_how_to_play(self):
        """Show comprehensive How to Play instructions"""
        help_window = tk.Toplevel(self.parent)
        help_window.title("How to Play Minesweeper")
        help_window.geometry("700x600")
        help_window.transient(self.parent)
        help_window.grab_set()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(help_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Basic Rules
        basics_frame = ttk.Frame(notebook)
        notebook.add(basics_frame, text="Basic Rules")
        self._create_basics_tab(basics_frame)
        
        # Tab 2: Game Controls
        controls_frame = ttk.Frame(notebook)
        notebook.add(controls_frame, text="Controls")
        self._create_controls_tab(controls_frame)
        
        # Tab 3: Strategies
        strategies_frame = ttk.Frame(notebook)
        notebook.add(strategies_frame, text="Strategies")
        self._create_strategies_tab(strategies_frame)
        
        # Tab 4: About
        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text="About")
        self._create_about_tab(about_frame)
        
        # Close button
        close_btn = tk.Button(help_window, text="Close", command=help_window.destroy, 
                             bg='lightcoral', font=('Arial', 10, 'bold'), width=15)
        close_btn.pack(pady=10)

    def _create_basics_tab(self, parent):
        """Create the Basic Rules tab content"""
        text_widget = tk.Text(parent, wrap='word', font=('Arial', 10), padx=15, pady=15)
        scrollbar = tk.Scrollbar(parent, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        basics_text = """
🎯 OBJECTIVE OF THE GAME

Minesweeper is a logic puzzle where you must reveal all safe cells on the board without triggering any mines.

🏆 HOW TO WIN
• Reveal ALL cells that don't contain mines
• Correctly flag ALL mine locations
• The game ends when only mines remain hidden

💥 HOW TO LOSE
• Click on any cell containing a mine
• The game ends immediately if you hit a mine

🔢 UNDERSTANDING THE NUMBERS

When you reveal a cell, it shows a number indicating how many mines are in the surrounding 8 cells:

    1  - One mine nearby
    2  - Two mines nearby  
    3  - Three mines nearby
    ... and so on up to 8

A blank cell (0) means no mines in the surrounding area - these often reveal large safe areas!

🚩 FLAGGING MINES

• RIGHT-CLICK or press F to place/remove a flag
• Flags mark suspected mine locations
• They prevent accidental clicks on marked cells
• Use flags to track where you think mines are

⏰ TIMER & SCORING

• Timer starts on your first click
• Faster completion times give better scores
• Top 10 times are saved for each difficulty level
• Flags don't affect scoring - only time matters

🎮 DIFFICULTY LEVELS

• EASY:    9×9 board with 10 mines
• MEDIUM: 16×16 board with 40 mines  
• HARD:   16×30 board with 99 mines
• CUSTOM: Choose your own board size and mine count
"""
        text_widget.insert('1.0', basics_text)
        text_widget.config(state='disabled')
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _create_controls_tab(self, parent):
        """Create the Controls tab content"""
        text_widget = tk.Text(parent, wrap='word', font=('Arial', 10), padx=15, pady=15)
        scrollbar = tk.Scrollbar(parent, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        controls_text = """
🖱️ MOUSE CONTROLS

LEFT CLICK:
• Reveal a cell
• First click is always safe
• Reveals numbers or blank areas

RIGHT CLICK:
• Place or remove a flag 🚩
• Mark suspected mine locations
• Prevents accidental clicks

HOVER:
• Cells highlight when mouseover
• Visual feedback for targeting

⌨️ KEYBOARD CONTROLS (Press Tab to activate)

ARROW KEYS: ↑ ↓ ← →
• Move cell selection around board

SPACE or ENTER:
• Reveal selected cell

F KEY:
• Flag/unflag selected cell

TAB:
• Toggle keyboard mode on/off

ESC:
• Exit keyboard mode

OTHER SHORTCUTS:
N or R - New Game
E - Easy difficulty
M - Medium difficulty  
H - Hard difficulty
C - Custom game
F1 - Show this help

🎛️ INTERFACE ELEMENTS

😊 FACE BUTTON:
• Click to start new game
• Shows 😎 when you win
• Shows 😵 when you lose

MINES DISPLAY (Red):
• Shows remaining mines to flag
• Calculated as: Total mines - Flags placed

TIMER (Red):
• Shows elapsed time in seconds
• Starts on first click
• Stops when game ends
"""
        text_widget.insert('1.0', controls_text)
        text_widget.config(state='disabled')
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')


    def show_keyboard_help(self):
        """Show keyboard controls help dialog"""
        help_text = """
=== MINESWEEPER KEYBOARD CONTROLS ===

NAVIGATION:
↑↓←→  - Move selection
Tab   - Toggle keyboard mode
Esc   - Exit keyboard mode

ACTIONS:
Space/Enter - Reveal selected cell
F           - Flag/unflag selected cell

GAME CONTROL:
N/R         - New game
E/M/H       - Easy/Medium/Hard difficulty
C           - Custom game

MOUSE:
Click       - Reveal cell
Right-click - Flag cell
Hover       - Visual feedback

Press any key to close...
        """
        
        help_window = tk.Toplevel(self.parent)
        help_window.title("Keyboard Controls Help")
        help_window.geometry("400x500")
        help_window.transient(self.parent)
        help_window.grab_set()
        
        text_widget = tk.Text(help_window, wrap='word', font=('Courier', 10), 
                            padx=10, pady=10, bg='lightyellow')
        text_widget.insert('1.0', help_text)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        help_window.bind('<Key>', lambda e: help_window.destroy())
        help_window.focus_set()

    def ask_player_name(self):
        """Ask for player name when highscore is achieved"""
        return simpledialog.askstring("Highscore", "Your name:")

    def show_progress_popup(self, title="Processing", message="Please wait..."):
        """Show a progress popup for long operations"""
        popup = tk.Toplevel(self.parent)
        popup.title(title)
        popup.geometry("300x100")
        popup.transient(self.parent)
        popup.grab_set()
        
        tk.Label(popup, text=message, font=('Arial', 11), pady=10).pack()
        popup.update()
        return popup

    def show_game_over(self):
        """Show game over message"""
        messagebox.showinfo("Game Over", "You hit a mine!")

    def show_victory(self, elapsed_time):
        """Show victory message"""
        messagebox.showinfo("Victory", f"You won in {elapsed_time:.1f} seconds!")

    def show_analytics_complete(self, config, sample_size, pdf_path):
        """Show analytics completion message with file location"""
        rows, cols, mines = config
        filename = os.path.basename(pdf_path)
        
        messagebox.showinfo(
            "Analytics Complete", 
            f"PDF report generated successfully!\n\n"
            f"File: {filename}\n"
            f"Location: {os.path.abspath(pdf_path)}\n\n"
            f"Configuration:\n"
            f"- Board: {rows}×{cols}\n"
            f"- Mines: {mines}\n"
            f"- Samples: {sample_size}\n\n"
            f"The report includes all 4 required visualizations."
        )
    
    def show_analytics_error(self, error_msg=None):
        """Show analytics error message"""
        if error_msg:
            messagebox.showerror("Analytics Error", f"Error generating analytics report:\n{error_msg}")
        else:
            messagebox.showerror("Analytics Error", "Failed to generate analytics report. Please check the configuration.")