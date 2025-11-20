# minesweeper/ui/themes.py
"""
UI styling and theme constants
"""
# Color schemes
CELL_COLORS = {
    'default': 'lightgray',
    'hover': '#B3B3B3', 
    'revealed': 'white',
    'selected': 'yellow',
    'mine': 'red'
}

NUMBER_COLORS = {
    1: 'blue', 2: 'green', 3: 'red', 4: 'navy',
    5: 'maroon', 6: 'turquoise', 7: 'black', 8: 'gray'
}

# Font settings
FONT_SETTINGS = {
    'cell': ('Arial', 10, 'bold'),
    'timer': ('Courier', 16),
    'button': ('Arial', 10)
}

# Layout constants
CELL_SIZE = {'width': 2, 'height': 1}
PANEL_PADDING = {'x': 10, 'y': 5}