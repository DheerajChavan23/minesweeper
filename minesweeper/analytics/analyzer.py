# minesweeper/analytics/analyzer.py - CORRECTED VERSION

import matplotlib.pyplot as plt
import numpy as np
from minesweeper.core.game import Game
from minesweeper.analytics.reporter import PDFReporter
from collections import deque
import random

class AnalyticsRunner:
    def __init__(self):
        self.sample_boards = []
        self.pdf_reporter = PDFReporter()

    def generate_boards(self, rows, cols, mines, n=100):
        """Generate sample boards with proper mine placement"""
        if n <= 0:
            raise ValueError("Sample size must be positive")
        if mines >= rows * cols:
            raise ValueError(f"Too many mines: {mines} for {rows}x{cols} board")
        if mines < 1:
            raise ValueError("Must have at least 1 mine")
            
        self.sample_boards.clear()
        print(f"Generating {n} boards for analytics...")
        
        boards_generated = 0
        for i in range(n):
            try:
                # Create game and simulate first click at random position
                game = Game(rows, cols, mines)
                first_r, first_c = random.randint(0, rows-1), random.randint(0, cols-1)
                game.board.place_mines((first_r, first_c))
                
                # Simulate revealing the board to get actual white cells
                revealed_cells = game.board.reveal(first_r, first_c)
                
                self.sample_boards.append({
                    'board': game.board,
                    'revealed_cells': revealed_cells
                })
                boards_generated += 1
            except Exception as e:
                print(f"Warning: Failed to generate board {i+1} - {e}")
                continue
        
        if boards_generated == 0:
            raise RuntimeError("Failed to generate any valid boards")
            
        print(f"Successfully generated {boards_generated} boards")
        return boards_generated

    def collect_analytics_data(self, rows, cols, mines):
        """Collect all analytics data for the 4 required visualizations - CORRECTED"""
        white_counts = []
        number_freq = [0] * 9  # 0-8
        cluster_counts = []
        heatmap = np.zeros((rows, cols))

        def find_clusters(board):
            """Find mine clusters using BFS"""
            visited = set()
            clusters = 0
            
            for r in range(rows):
                for c in range(cols):
                    if board.grid[r][c].is_mine and (r, c) not in visited:
                        # Found new cluster
                        clusters += 1
                        queue = deque([(r, c)])
                        visited.add((r, c))
                        
                        while queue:
                            cr, cc = queue.popleft()
                            for nr, nc in board.neighbours(cr, cc):
                                if (board.grid[nr][nc].is_mine and 
                                    (nr, nc) not in visited):
                                    visited.add((nr, nc))
                                    queue.append((nr, nc))
            return clusters

        # Process each board
        for board_data in self.sample_boards:
            board = board_data['board']
            revealed_cells = board_data['revealed_cells']
            
            # 1. WHITE CELLS: Count revealed cells with value 0 (actual white cells in gameplay)
            white_cells_count = 0
            revealed_positions = set(revealed_cells) if revealed_cells else set()
            
            for r, c in revealed_positions:
                cell = board.grid[r][c]
                if not cell.is_mine and cell.value == 0:
                    white_cells_count += 1
            white_counts.append(white_cells_count)

            # 2. NUMBER FREQUENCY: Count revealed numbers (as they appear in gameplay)
            for r, c in revealed_positions:
                cell = board.grid[r][c]
                if not cell.is_mine and 0 <= cell.value <= 8:
                    number_freq[cell.value] += 1

            # 3. MINE CLUSTERS
            clusters = find_clusters(board)
            cluster_counts.append(clusters)

            # 4. HEATMAP: Average mines in 3x3 neighborhood for ALL cells
            for r in range(rows):
                for c in range(cols):
                    mine_count = 0
                    for nr, nc in board.neighbours(r, c):
                        if board.grid[nr][nc].is_mine:
                            mine_count += 1
                    heatmap[r][c] += mine_count

        # Normalize heatmap by number of boards
        if self.sample_boards:
            heatmap /= len(self.sample_boards)

        return {
            'white_counts': white_counts,
            'number_freq': number_freq,
            'cluster_counts': cluster_counts,
            'heatmap': heatmap
        }

    def run_all(self, rows, cols, mines, sample_size=100, generate_pdf=True, output_path=None):
        """Run analytics and generate PDF report - UPDATED"""
        try:
            self._validate_inputs(rows, cols, mines, sample_size)
            
            print(f"Starting analytics: {rows}x{cols}, {mines} mines, {sample_size} samples")
            
            boards_generated = self.generate_boards(rows, cols, mines, n=sample_size)
            analytics_data = self.collect_analytics_data(rows, cols, mines)
            analytics_data['boards_processed'] = boards_generated
            
            print(f"Analytics data collected:")
            print(f"  - White counts: {len(analytics_data['white_counts'])} samples")
            print(f"  - Number freq: {analytics_data['number_freq']}")
            print(f"  - Cluster counts: {len(analytics_data['cluster_counts'])} samples")
            print(f"  - Heatmap shape: {analytics_data['heatmap'].shape}")
            
            if generate_pdf:
                pdf_path = self.generate_pdf_report(analytics_data, (rows, cols, mines), sample_size, output_path)
                print(f"PDF report generated at: {pdf_path}")
                return pdf_path
            
            return None
            
        except Exception as e:
            print(f"Analytics error: {e}")
            import traceback
            traceback.print_exc()
            raise

    def _validate_inputs(self, rows, cols, mines, sample_size):
        """Validate all input parameters"""
        MAX_ROWS = 30
        MAX_COLS = 40  
        MIN_ROWS = 5
        MIN_COLS = 5
        MAX_SAMPLE_SIZE = 5000
        
        if not (MIN_ROWS <= rows <= MAX_ROWS):
            raise ValueError(f"Rows must be between {MIN_ROWS} and {MAX_ROWS}")
        if not (MIN_COLS <= cols <= MAX_COLS):
            raise ValueError(f"Columns must be between {MIN_COLS} and {MAX_COLS}")
        if not (1 <= mines < rows * cols):
            raise ValueError(f"Mines must be between 1 and {rows*cols - 1}")
        if not (10 <= sample_size <= MAX_SAMPLE_SIZE):
            raise ValueError(f"Sample size must be between 10 and {MAX_SAMPLE_SIZE}")

    def generate_pdf_report(self, analytics_data, config, sample_size, output_path=None):
        """Generate PDF report with all 4 required visualizations"""
        return self.pdf_reporter.generate_analytics_report(
            analytics_data, config, sample_size, output_path
        )