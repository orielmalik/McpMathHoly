from fastmcp import FastMCP
from typing import Any, Dict

from Patterns.Singelton import LoggerSingelton

mcp_server = FastMCP(name="MathActionsServer")


@mcp_server.tool
def execute_math_action(action: Dict[str, Any]) -> Dict[str, Any]:
    action_type = action.get("type")
    message = action.get("message")
    timestamp = action.get("timestamp")

    LoggerSingelton.printer("INFO", f"Action: {action_type} at {timestamp}")

    # -------------------------------
    # כאן תכניס את כל ה-APIs וה-SDK שלך
    # דוגמאות אפשריות:

    # if action_type == "solve":
    #     return your_sympy_solver(message)

    # if action_type == "integrate":
    #     return your_integration_sdk(message)

    # if action_type == "fetch_financial":
    #     return your_polygon_or_coingecko_api(message)

    # if action_type == "optimize":
    #     return your_pulp_or_scipy_optimizer(message)

    # if action_type == "plot":
    #     return your_matplotlib_or_plotly_generator(message)

    # -------------------------------
    raise ValueError(f"Unknown action type: {action_type}")