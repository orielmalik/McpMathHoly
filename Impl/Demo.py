# execute_direct.py

from Models.models import ActionRequest
from Patterns.Factory.CommandFactory import CommandFactory
from Patterns.Template.ErrorTemplate import AppErrors
from Utils.CustomException import APIException
import json
from Models.models import ActionRequest

PAYLOADS_FILE = "payloads.json"


def execute_sync(operation: str, req: ActionRequest):
    try:
        result = CommandFactory.invoke(operation, req)
        if result is None:
            raise AppErrors.not_found(f"Operation '{operation}' not found")

        return {
            "status": "success",
            "data": result
        }

    except APIException as e:
        raise e
    except Exception as e:
        raise AppErrors.bad_request(str(e))


with open(PAYLOADS_FILE, "r", encoding="utf-8") as f:
    payloads = json.load(f)

for idx, item in enumerate(payloads, start=1):
    operation = item.get("operation", "math")
    payload_data = item.get("payload", {})

    try:
        req = ActionRequest(**payload_data)
        result = execute_sync(operation, req)
        print(f"Test {idx} Success:", result)
    except Exception as e:
        print(f"Test {idx} Failed:", e)

if __name__ == "__main__":
    req1 = ActionRequest(
        type="solve",
        message=["2*x + 2 = 10"],
        timestamp="2026-02-21T21:00:00"
    )
    try:
        res = execute_sync("math", req1)
        print("Test 1 Success:", res)
    except Exception as e:
        print("Test 1 Failed:", e)

    req2 = ActionRequest(
        type="solve",
        message=["2*x + 2 = 10"]
    )
    try:
        res = execute_sync("unknown_op", req2)
        print("Test 2 Success:", res)
    except Exception as e:
        print("Test 2 Failed:", e)
