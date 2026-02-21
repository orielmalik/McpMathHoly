from Patterns.Strategy import MathStrategy
from Patterns.Strategy.MathStrategy import ExpressionStrategy, SolveEquationStrategy, MatrixDeterminantStrategy, \
    MatrixDiagonalizeStrategy, MotionProblemStrategy


class StrategyFactory:
    _registry = {
        "expression": ExpressionStrategy,
        "solve": SolveEquationStrategy,
        "matrix_det": MatrixDeterminantStrategy,
        "matrix_diag": MatrixDiagonalizeStrategy,
        "motion": MotionProblemStrategy
    }

    @staticmethod
    def create(action_type: str) -> MathStrategy:
        strategy_cls = StrategyFactory._registry.get(action_type)
        if not strategy_cls:
            raise ValueError(f"Unknown action type: {action_type}")
        return strategy_cls()