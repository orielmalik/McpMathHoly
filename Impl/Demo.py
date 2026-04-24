import asyncio
from Models.models import ActionRequest
from Patterns.Singelton import LoggerSingelton
from fappsetting.appDependency import get_llm_adapter
from mcpclientmock import MCPClientMock
from Utils import helpers





async def main():
    llm = get_llm_adapter()
    mcp = MCPClientMock()

    test_actions = helpers.load_actions_from_json("payloads.json")

    for acti in test_actions:
        actio = ActionRequest(**acti)

        route = await llm.ask(
            full_prompt=helpers.action_to_prompt(actio),
        )

        parsed = helpers.normalize_router_output(route.result)

        operation = parsed.get("operation")

        if parsed.get("tool") is None:
            LoggerSingelton.printer("INFO", "SKIPPED")
            continue

        message=parsed.get("message")
        if not message:
            LoggerSingelton.printer("ERROR", "Empty message")
            continue

        if operation == "solve":
            result = await llm.solve(
                full_prompt=f"Solve directly: {message}"
            )
            LoggerSingelton.printer("INFO", f"LLM RESULT: {result.result}")
            continue

        if not operation:
            LoggerSingelton.printer("ERROR", "Missing operation")
            continue

        result = await mcp.call_tool(
            operation,
            ActionRequest(
                type=operation,
                message=message,
                timestamp=actio.timestamp
            )
        )

        LoggerSingelton.printer("INFO", f"TOOL RESULT: {result}")


if __name__ == "__main__":
    asyncio.run(main())