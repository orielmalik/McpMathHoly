# demo.py
import asyncio
from Models.models import ActionRequest
from Patterns.Singelton import LoggerSingelton
from Patterns.Adapter.LLMAdapter import FreeLLMAdapter
from Patterns.Adapter.McpClientAdapter import MCPClientAdapter
from Utils.consts import mcptitle
from fappsetting.appDependency import get_llm_adapter


async def main():
    llm = get_llm_adapter()
    mcp_client = MCPClientAdapter(server_url="https://demo-mcp-server.com")

    test_actions = [
        ActionRequest(
            type="MATHCOMMAND",
            message=["2 + 2", "5 * 7"],
            timestamp="2026-03-08T16:00:00"
        ),
        ActionRequest(
            type="MATHCOMMAND",
            message=["sqrt(16)", "log(100)"],
            timestamp="2026-03-08T16:01:00"
        ),
        ActionRequest(
            type="MATHCOMMAND",
            message=["integrate x^2 dx from 0 to 3"],
            timestamp="2026-03-08T16:02:00"
        )
    ]

    for action in test_actions:
        LoggerSingelton.printer("INFO", f"Sending action to LLM & MCP: {action}")
        llm_response = await llm.ask(action)
        LoggerSingelton.printer("INFO", f"LLM Response: {llm_response.json()}")

        if llm_response.result and "tool_name" in llm_response.result:
            tool_name = llm_response.result["tool_name"]
            result = await mcp_client.call_tool(tool_name=tool_name, action=action)
            LoggerSingelton.printer("INFO", f"MCP Tool Result: {result}")
        else:
            LoggerSingelton.printer("INFO", f"Direct Answer from LLM: {llm_response.result}")


if __name__ == "__main__":
    asyncio.run(main())
