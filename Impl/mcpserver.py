from fastmcp import FastMCP
from typing import Any, Dict

from Models.models import JsonRpcRequest,ActionRequest
from Patterns.Singelton import LoggerSingelton, Fappmcp


@Fappmcp.tool
def execute_action(action: JsonRpcRequest) -> Dict[str, Any]:
    action_type = action.params.type
    message = action.params.message
    timestamp = action.params.timestamp


    LoggerSingelton.printer("INFO", f"Action: {action_type} at {timestamp}")
    raise ValueError(f"Unknown action type: {action_type}")
