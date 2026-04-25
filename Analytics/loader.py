import pandas as pd

class LogLoader:
    def __init__(self, path: str):
        self.path = path

    def load(self):
        return pd.read_json(self.path, lines=True)