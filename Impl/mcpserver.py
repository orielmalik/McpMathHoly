from fastmcp import FastMCP
from fastmcp.dependencies import CurrentContext
from fastmcp.server.context import Context
from typing import Any, Dict

from Models.models import JsonRpcRequest, ActionRequest
from Patterns.Singelton import LoggerSingelton, Fappmcp
from Patterns.Factory import CommandFactory

@Fappmcp.tool
async def execute_action(action: JsonRpcRequest, ctx: Context = CurrentContext()) -> Dict[str, Any]:
    action_type = action.params.type
    message = action.params.message
    timestamp = action.params.timestamp

    await ctx.info(f"Executing action: {action_type} at {timestamp}")

    result = CommandFactory.invoke(action_type, message, timestamp)

    LoggerSingelton.printer("INFO", f"Action: {action_type} at {timestamp} completed")

    if result is None:
        await ctx.error(f"Unknown action type: {action_type}")
        return {"status": "error", "message": f"Unknown action type: {action_type}"}

    return {"status": "success", "result": result}
