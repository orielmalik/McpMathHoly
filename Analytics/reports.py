class ReportEngine:

    def __init__(self, df):
        self.df = df

    def accuracy_by_operation(self):
        return self.df.groupby("operation")["success"].mean()

    def latency_by_operation(self):
        return self.df.groupby("operation")["latency"].mean()

    def stability(self):
        return self.df.groupby("input")["output"].nunique()

    def summary(self):
        return {
            "accuracy": self.accuracy_by_operation().to_dict(),
            "latency": self.latency_by_operation().to_dict(),
            "stability": self.stability().mean()
        }