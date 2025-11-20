# minesweeper/data/highscores.py
import json
import os
from datetime import datetime

class HighScoreManager:
    def __init__(self, path=None):
        # Use absolute path to data folder
        if path is None:
            # Get the directory where this file is located (data folder)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.path = os.path.join(current_dir, 'highscores.json')
        else:
            self.path = path
        
        print(f"Highscores file path: {self.path}")  # Debug
        self.scores = self._load()

    def _load(self):
        print(f"Loading highscores from: {self.path}")  # Debug
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    data = json.load(f)
                    print(f"Loaded {len(data)} highscore configurations")  # Debug
                    return data
            except Exception as e:
                print(f"Error loading highscores: {e}")  # Debug
                return {}
        else:
            print(f"Highscores file not found at: {self.path}")  # Debug
            # Create empty file
            self._save()
            return {}

    def _save(self):
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, 'w') as f:
                json.dump(self.scores, f, indent=2)
            print(f"Saved highscores to: {self.path}")  # Debug
        except Exception as e:
            print(f"Error saving highscores: {e}")  # Debug

    def _key(self, rows, cols, mines):
        return f"{rows}x{cols}_{mines}"

    def is_highscore(self, rows, cols, mines, time):
        k = self._key(rows, cols, mines)
        lst = self.scores.get(k, [])
        print(f"Checking highscore for {k}: {len(lst)} existing scores, new time: {time:.2f}")  # Debug
        return len(lst) < 10 or time < max(s['time'] for s in lst)

    def add_score(self, rows, cols, mines, name, time):
        k = self._key(rows, cols, mines)
        entry = {
            'name': name,
            'time': time,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"Adding score for {k}: {entry}")  # Debug
        
        if k not in self.scores:
            self.scores[k] = []
        
        self.scores[k].append(entry)
        self.scores[k] = sorted(self.scores[k], key=lambda x: x['time'])[:10]
        self._save()
        
        # Verify it was saved
        saved_scores = self.get_top_scores(rows, cols, mines)
        print(f"Verified saved scores for {k}: {len(saved_scores)} entries")  # Debug

    def get_top_scores(self, rows, cols, mines):
        k = self._key(rows, cols, mines)
        scores = self.scores.get(k, [])
        print(f"Retrieving scores for {k}: {len(scores)} entries")  # Debug
        for i, score in enumerate(scores):
            print(f"  {i+1}. {score['name']} - {score['time']:.2f}s")  # Debug
        return scores