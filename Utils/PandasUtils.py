import pandas as pd
import chardet
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
from datetime import datetime


def merge_files(*file_paths):
    dfs = [pd.read_csv(f) for f in file_paths]
    return pd.concat(dfs, ignore_index=True)


def select_columns(df, columns):
    valid = [c for c in columns if c in df.columns]
    return df[valid]


class PandasHelper:

    def __init__(self, file_path=None, data=None, columns=None):
        self.file_path = file_path
        if isinstance(file_path, pd.DataFrame):
            self.df = file_path
        elif data is not None:
            self.df = pd.DataFrame(data, columns=columns)
        else:
            self.df = None

    def detect_encoding(self):
        with open(self.file_path, 'rb') as f:
            return chardet.detect(f.read())['encoding']

    def read_file(self):
        if self.file_path.endswith(".csv"):
            enc = self.detect_encoding()
            self.df = pd.read_csv(self.file_path, encoding=enc)
        elif self.file_path.endswith(".xlsx"):
            self.df = pd.read_excel(self.file_path)
        elif self.file_path.endswith(".json"):
            self.df = pd.read_json(self.file_path)
        return self

    def sqlSelect(self, query, dfs=None):
        from pandasql import PandaSQL
        sql = PandaSQL()
        if dfs is None:
            dfs = [self.df]
        env = {f"t{i + 1}": df for i, df in enumerate(dfs)}
        return sql(query, env=env)

    def create_chart(self, data, chart_type, title, labels=None):
        plt.figure(figsize=(8, 6))

        if chart_type == "histogram":
            plt.hist(data, bins=10)

        elif chart_type == "pie":
            if isinstance(data, dict):
                labels = list(data.keys())
                data = list(data.values())
            plt.pie(data, labels=labels, autopct='%1.1f%%')

        elif chart_type == "plot":
            plt.plot(data)

        plt.title(title)
        filename = f"chart_{datetime.now().timestamp()}.png"
        plt.savefig(filename)
        plt.close()
        return filename
