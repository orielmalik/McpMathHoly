import json
import pandas as pd

class ReportExporter:

    def to_json(self, data, path):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def to_csv(self, df: pd.DataFrame, path):
        df.to_csv(path, index=False)