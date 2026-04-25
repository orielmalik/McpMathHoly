import asyncio
import datetime

from Analytics.engine import PandasSDK, run_action, analytics_buffer
from Models.models import ActionRequest
from Patterns.Singelton import LoggerSingelton
from fappsetting.appDependency import get_llm_adapter
from mcpclientmock import MCPClientMock
from Utils import helpers


async def main():

    llm = get_llm_adapter()
    mcp = MCPClientMock()

    test_actions = helpers.load_actions_from_json("payloads.json")

    analytics_batch = []

    for acti in test_actions:

        actio = ActionRequest(**acti)

        route = await llm.ask(
            full_prompt=helpers.action_to_prompt(actio),
        )

        parsed = helpers.normalize_router_output(route.result)

        operation = parsed.get("operation")
        message = parsed.get("message")

        if not operation or not message:
            continue

        start_time = datetime.datetime.now()

        if operation == "solve":
            result = await llm.solve(
                full_prompt=f"Solve directly: {message}"
            )
            output = result.result

        else:
            result = await mcp.call_tool(
                operation,
                ActionRequest(
                    type=operation,
                    message=message,
                    timestamp=actio.timestamp
                )
            )
            output = result.result if hasattr(result, "result") else result

        run_action("solve", "2*x + 1 = 10", "x=4.5")
        run_action("expression", "2*x + 3*x", "5*x")
        run_action("matrix_det", "1 2; 3 4", "-2")
        run_action("motion", "0,10,5", "distance=62.5")

        sdk = PandasSDK.from_records(analytics_buffer)

        report = sdk.generate_report()
        errors = sdk.generate_error_analysis()

        sdk.plot_flow()

        print(report)
        print(errors)


if __name__ == "__main__":
    asyncio.run(main())