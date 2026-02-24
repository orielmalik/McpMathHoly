from typing import Any
from Models.models import ActionRequest, JsonRpcRequest, JsonRpcResponse
from Patterns.Builder import AsyncURIBuilder, AsyncPipeline
from Patterns.Singelton import LoggerSingelton


class MCPClientAdapter:
    def __init__(self, server_url: str):
        self.builder = AsyncURIBuilder.AsyncURIBuilder(server_url)
        self.pipeline = AsyncPipeline.AsyncPipeline(self.builder)
        (self.pipeline.add_step(self._prepare_request).
         add_step(self._send_request).add_step(self._parse_response))

    async def _prepare_request(self, builder: AsyncURIBuilder, action: ActionRequest):
        payload = JsonRpcRequest(
            jsonrpc="2.0",
            method="call_tool",
            params=action,
            id=1
        ).dict()
        LoggerSingelton.printer("DEBUG", f"Prepared payload: {payload}")
        return payload

    async def _send_request(self, builder: AsyncURIBuilder, payload: dict):
        response = await builder.request(
            method="POST",
            endpoint="/mcp/call",
            json_body=payload
        )
        LoggerSingelton.printer("DEBUG", f"Received raw response: {response}")
        return response

    async def _parse_response(self, builder: AsyncURIBuilder, response_json: dict) -> Any:
        resp_model = JsonRpcResponse(**response_json)
        if resp_model.error:
            LoggerSingelton.printer("ERROR", f"MCP Server returned error: {resp_model.error}")
            raise Exception(f"MCP Error {resp_model.error.code}: {resp_model.error.message}")
        return resp_model.result

    # public API
    async def call_tool(self, tool_name: str, action: ActionRequest) -> Any:
        action.type = tool_name
        result = await self.pipeline.run(action)
        LoggerSingelton.printer("INFO", f"Tool '{tool_name}' executed successfully with result: {result}")
        return result
