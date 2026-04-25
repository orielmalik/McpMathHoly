from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import numpy as np
from sympy import symbols, Eq, solve, sympify
from typing import List, Dict, Any
import re


class MathStrategy(ABC):
    @abstractmethod
    def exec(self, message: List[str], **kwargs) -> Dict[str, Any]:
        pass


class ExpressionStrategy(MathStrategy):
    def exec(self, message: List[str], **kwargs):
        if not message or not message[0]:
            raise ValueError("Missing expression")
        expr = sympify(message[0])
        return {"expression": str(expr)}


class SolveEquationStrategy(MathStrategy):
    def exec(self, message: List[str], **kwargs):
        if not message:
            raise ValueError("Missing equations")

        variables = kwargs.get("variables")
        equations = []
        all_symbols = set()

        for raw in message:
            raw = raw.strip()
            if "=" in raw:
                left, right = raw.split("=", 1)
                lhs = sympify(left.strip())
                rhs = sympify(right.strip())
                eq = Eq(lhs, rhs)
                equations.append(eq)
                all_symbols.update(lhs.free_symbols | rhs.free_symbols)
            else:
                expr = sympify(raw)
                equations.append(expr)
                all_symbols.update(expr.free_symbols)

        if variables:
            vars_to_solve = symbols(" ".join(variables))
            solutions = solve(equations, vars_to_solve, dict=True)
        else:
            solutions = solve(equations, dict=True)

        return {"solutions": solutions}


class MatrixDeterminantStrategy(MathStrategy):
    def exec(self, message: List[str], **kwargs):
        if not message or not message[0]:
            raise ValueError("Missing matrix data")
        rows = message[0].split(";")
        matrix = np.array([list(map(float, row.split())) for row in rows])
        det = np.linalg.det(matrix)
        return {"determinant": round(float(det), 6)}


class MatrixDiagonalizeStrategy(MathStrategy):
    def exec(self, message: List[str], **kwargs):
        if not message or not message[0]:
            raise ValueError("Missing matrix data")
        rows = message[0].split(";")
        matrix = np.array([list(map(float, row.split())) for row in rows])
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        return {
            "eigenvalues": eigenvalues.tolist(),
            "eigenvectors": eigenvectors.tolist()
        }


class MotionProblemStrategy(MathStrategy):
    def exec(self, message: List[str], **kwargs):
        if not message or len(message) < 3:
            raise ValueError("Missing motion parameters")
        v0 = float(message[0])
        a = float(message[1])
        t = float(message[2])
        vf = v0 + a * t
        s = v0 * t + 0.5 * a * t ** 2
        return {
            "final_velocity": vf,
            "distance": s
        }


class StrategyFactory:
    _registry = {
        "expression": ExpressionStrategy,
        "solve": SolveEquationStrategy,
        "matrix_det": MatrixDeterminantStrategy,
        "matrix_eig": MatrixDiagonalizeStrategy,
        "motion": MotionProblemStrategy,
    }

    @staticmethod
    def create(action_type: str) -> MathStrategy:
        strategy_cls = StrategyFactory._registry.get(action_type)
        if not strategy_cls:
            raise ValueError(f"Unknown math action: {action_type}")
        return strategy_cls()
