from Models.models import ActionRequest
from Patterns.Command.Commands import OperationCommand, MathCommand
from Patterns.Strategy import MathStrategy
from Patterns.Strategy.MathStrategy import ExpressionStrategy, SolveEquationStrategy, MatrixDeterminantStrategy, \
    MatrixDiagonalizeStrategy, MotionProblemStrategy


class CommandFactory:

    @staticmethod
    def invoke(action_type: str,req:ActionRequest) -> OperationCommand:
        if action_type == "math":
            return MathCommand().invoke(req)
        else:
            return None
