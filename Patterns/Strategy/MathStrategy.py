from abc import ABC, abstractmethod
from typing import List, Optional
import numpy as np
from sympy import symbols, sympify, Eq, solve, sympify as sp_sympify


class MathStrategy(ABC):
    @abstractmethod
    def exec(self, message: List[str]):
        """Executes strategy on a list of strings"""
        pass


class ExpressionStrategy(MathStrategy):
    def exec(self, message: List[str]):
        if not message or not message[0]:
            raise ValueError("Missing expression")
        expr_str = message[0]
        return {"expression": str(sp_sympify(expr_str))}


class SolveEquationStrategy(MathStrategy):
    def exec(self, message: List[str], variables: Optional[List[str]] = None):
        if not message:
            raise ValueError("Missing equations")

        equations = []
        all_symbols = set()

        for raw in message:
            raw = raw.strip()
            if "=" in raw:
                left, right = raw.split("=", 1)
                lhs = sp_sympify(left.strip())
                rhs = sp_sympify(right.strip())
                equations.append(Eq(lhs, rhs))
                all_symbols.update(lhs.free_symbols | rhs.free_symbols)
            else:
                expr = sp_sympify(raw)
                equations.append(expr)
                all_symbols.update(expr.free_symbols)

        if variables:
            vars_to_solve = symbols(variables)
        else:
            vars_to_solve = list(all_symbols) if all_symbols else None

        solutions = solve(equations, vars_to_solve, dict=True)
        return {"solutions": solutions}


class MatrixDeterminantStrategy(MathStrategy):
    def exec(self, message: List[str]):
        if not message:
            raise ValueError("Missing matrix data")
        matrix = np.array([list(map(float, row.split())) for row in message])
        det = np.linalg.det(matrix)
        return {"determinant": float(det)}


class MatrixDiagonalizeStrategy(MathStrategy):
    def exec(self, message: List[str]):
        if not message:
            raise ValueError("Missing matrix data")
        matrix = np.array([list(map(float, row.split())) for row in message])
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        return {
            "eigenvalues": eigenvalues.tolist(),
            "eigenvectors": eigenvectors.tolist()
        }


class MotionProblemStrategy(MathStrategy):
    def exec(self, message: List[str]):
        # נניח שהסדר: v0, a, t
        if not message or len(message) < 3:
            raise ValueError("Missing motion parameters (v0, a, t)")
        v0 = float(message[0])
        a  = float(message[1])
        t  = float(message[2])
        vf = v0 + a * t
        s  = v0 * t + 0.5 * a * t**2
        return {
            "final_velocity": vf,
            "distance": s
        }