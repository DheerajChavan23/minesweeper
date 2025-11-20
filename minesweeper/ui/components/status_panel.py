# minesweeper/ui/components/status_panel.py
import tkinter as tk
from minesweeper.ui.themes import FONT_SETTINGS

class StatusPanel:
    def __init__(self, parent, on_reset_game):
        self.parent = parent
        self.on_reset_game = on_reset_game
        
        self.setup_panel()

    def setup_panel(self):
        """Create status panel with properly centered face button"""
        self.top_panel = tk.Frame(self.parent, bg='gray', bd=1, relief='sunken')
        self.top_panel.pack(pady=2, padx=10, fill='x')
        
        # Use grid for better centering control
        self.top_panel.columnconfigure(0, weight=1)  # Left - mines counter
        self.top_panel.columnconfigure(1, weight=1)  # Center - face button
        self.top_panel.columnconfigure(2, weight=1)  # Right - timer
        
        # Left: Mines counter
        mines_frame = tk.Frame(self.top_panel, bg='black', bd=1, relief='sunken')
        mines_frame.grid(row=0, column=0, padx=10, pady=2, sticky='w')
        
        self.mines_label = tk.Label(
            mines_frame, 
            text='010', 
            font=FONT_SETTINGS['timer'], 
            fg='red', 
            bg='black', 
            width=3
        )
        self.mines_label.pack(padx=2, pady=2)
        
        # Center: Face button (centered)
        self.face_button = tk.Button(
            self.top_panel, 
            text='😊', 
            font=('Arial', 16), 
            command=self.on_reset_game,
            bg='lightgray',
            relief='raised',
            bd=1
        )
        self.face_button.grid(row=0, column=1, padx=5, pady=2)
        
        # Right: Timer
        timer_frame = tk.Frame(self.top_panel, bg='black', bd=1, relief='sunken')
        timer_frame.grid(row=0, column=2, padx=10, pady=1, sticky='e')
        
        self.time_label = tk.Label(
            timer_frame, 
            text='000', 
            font=FONT_SETTINGS['timer'], 
            fg='red', 
            bg='black', 
            width=3
        )
        self.time_label.pack(padx=2, pady=1)

    def update_mines_display(self, remaining_mines):
        """Update mines counter"""
        self.mines_label.config(text=f"{remaining_mines:03d}")

    def update_timer(self, elapsed_seconds):
        """Update timer display"""
        self.time_label.config(text=f"{int(elapsed_seconds):03d}")

    def update_face_button(self, state):
        """Update face button based on game state"""
        faces = {
            'playing': '😊',
            'won': '😎', 
            'lost': '😵'
        }
        self.face_button.config(text=faces.get(state, '😊'))

    def set_keyboard_mode(self, active):
        """Update keyboard mode indicator"""
        # This is now handled in the main app footer
        pass