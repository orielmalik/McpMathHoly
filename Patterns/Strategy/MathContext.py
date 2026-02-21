from Patterns.Strategy import MathStrategy


class Context:
    def __init__(self, strategy: MathStrategy):
        self._strategy = strategy

    @property
    def strategy(self) -> MathStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: MathStrategy) -> None:
        if not isinstance(strategy, MathStrategy):
            raise TypeError("Must implement MathStrategy")
        self._strategy = strategy

    def run(self, data):
        return self._strategy.exec(data)