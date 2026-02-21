from Patterns.Factory import StrategyFactory
from Patterns.Strategy import MathContext


def switchSDKMathOperation(operation, message):
    context = MathContext(operation)
    context.run()


