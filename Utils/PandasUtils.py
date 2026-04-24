# library aimed at maintaining PANDAS code -but needed to merge before files if needed

import pandas as pd
import chardet
from pandasql import PandaSQL
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



def merge_files(*file_paths):
    # all files become 1 file
    dataframes = [pd.read_csv(file) for file in file_paths]
    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df


def select_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    valid_columns = [col for col in columns if col in df.columns]
    if not valid_columns:
        raise ValueError("no cols")

    return df[valid_columns]


class PandasHelper:
    def __init__(self, file_path=None, data=None, columns=None):
        self.file_path = file_path
        if data is not None and columns is not None:
            self.df = pd.DataFrame(data, columns=columns)
        elif isinstance(file_path, pd.DataFrame):
            self.df = file_path
        else:
            self.df = None

    def detect_encoding(self):
        with open(self.file_path, 'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

    def read_file(self):
        if self.file_path.endswith('.csv'):
            encoding = self.detect_encoding()
            self.df = pd.read_csv(self.file_path, encoding=encoding)
        elif self.file_path.endswith('.xlsx'):
            self.df = pd.read_excel(self.file_path)
        elif self.file_path.endswith('.json'):
            self.df = pd.read_json(self.file_path)
        else:
            raise ValueError("Unsupported file format")
        return self

    def create_dataframe(self, data, columns=None):
        self.df = pd.DataFrame(data, columns=columns)
        return self.df

    def create_series(self, data):
        return pd.Series(data)

    def sqlSelect(self, query, data_frames=None):
        if data_frames is None and self.df is not None:
            data_frames = [self.df]
        sql = PandaSQL()
        env = {f't{i + 1}': df for i, df in enumerate(data_frames)}
        return sql(query, env=env)  #init object and do query

    def create_chart(self,data, chart_type, title,dictt=None, labels=None, color="skyblue"):
        global xlabel
        global ylabel
        if dictt is not None and isinstance(dictt, list):
            xlabel=dictt[0]
            ylabel=dictt[1]
        try:
            plt.figure(figsize=(8, 6))  # גודל הגרף

            if chart_type == "histogram":
                plt.hist(data, bins=10, color=color, edgecolor='black')
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)

            elif chart_type == "pie":
                if isinstance(data, dict):
                    labels = list(data.keys())
                    sizes = list(data.values())
                else:
                    labels = data.index if hasattr(data, 'index') else range(len(data))
                    sizes = data.values if hasattr(data, 'values') else data

                plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=plt.cm.Paired.colors)

            elif chart_type == "plot":
                plt.plot(data, color=color, marker='o', linestyle='-')
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)

            plt.title(title)
            plt.savefig("g.png")

        except Exception as e:
            print(f"Error creating {chart_type}: {e}")