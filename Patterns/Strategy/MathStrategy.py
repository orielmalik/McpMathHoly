from abc import ABC, abstractmethod
import numpy as np
from sympy import symbols, sympify, Eq, solve


class MathStrategy(ABC):
    @abstractmethod
    def exec(self, data):
        pass


class ExpressionStrategy(MathStrategy):
    def exec(self, data):
        expr = sympify(data)
        return expr


class SolveEquationStrategy(MathStrategy):
    def exec(self, data):
        equations = [sympify(eq) for eq in data['equations']]
        vars = symbols(data.get('variables', None))
        return solve(equations, vars)


class MatrixDeterminantStrategy(MathStrategy):
    def exec(self, data):
        matrix = np.array(data)
        return np.linalg.det(matrix)


class MatrixDiagonalizeStrategy(MathStrategy):
    def exec(self, data):
        matrix = np.array(data)
        return np.linalg.eig(matrix)


class MotionProblemStrategy(MathStrategy):
    def exec(self, data):
        v0 = data.get('v0', 0)
        a = data.get('a', 0)
        t = data.get('t', 0)
        return v0 + a * t



