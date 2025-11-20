# minesweeper/ui/components/control_panel.py
import tkinter as tk

DIFFICULTIES = {
    'easy': (9, 9, 10),
    'medium': (16, 16, 40), 
    'hard': (16, 30, 99)
}

class ControlPanel:
    def __init__(self, parent, on_difficulty_change):
        self.parent = parent
        self.on_difficulty_change = on_difficulty_change
        
        self.setup_difficulty_buttons()

    def setup_difficulty_buttons(self):
        """Create ONLY difficulty selection buttons"""
        self.mode_frame = tk.Frame(self.parent, bg='lightgray')
        self.mode_frame.pack(pady=5)
        
        for mode in list(DIFFICULTIES.keys()) + ['custom']:
            btn = tk.Button(
                self.mode_frame, 
                text=mode.capitalize(), 
                width=10,
                command=lambda m=mode: self.on_difficulty_change(m),
                font=('Arial', 8, 'bold'),
                bg='gray',
                relief='raised',
                bd=2
            )
            btn.pack(side='left', padx=3)