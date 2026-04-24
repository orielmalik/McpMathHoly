import asyncio
from Models.models import ActionRequest, JsonRpcResponse
from Patterns.Factory.CommandFactory import CommandFactory
from Patterns.Singelton import LoggerSingelton


class MCPClientMock:

    def __init__(self):
        LoggerSingelton.printer("INFO", "[MOCK MCP] Initialized (local execution mode)")

    async def call_tool(self, tool_name: str, action: ActionRequest) -> JsonRpcResponse:
        LoggerSingelton.printer("INFO", f"[MOCK MCP] Running tool: {tool_name}")

        result = await asyncio.to_thread(
            CommandFactory.invoke,"math_",
            action
            )


        LoggerSingelton.printer("INFO", f"[MOCK MCP] Result: {result}")

        return JsonRpcResponse(
            jsonrpc="2.0",
            result=result,
            error=None,
            id=1
        )