from fastapi import Path, Body
from Patterns.Factory.CommandFactory import CommandFactory
from Models.models import ActionRequest
from Patterns.Decorator.decorators import auto_error_logger
from Patterns.Singelton.Fapp import app
from Patterns.Template.ErrorTemplate import AppErrors
from Utils.CustomException import APIException


@auto_error_logger
@app.post("/{operation}")
async def execute(
        operation: str = Path(..., description="Operation name"),
        req: ActionRequest = Body(...)
):
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


