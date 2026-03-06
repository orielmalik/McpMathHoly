from fastapi import APIRouter, Path, Body, Depends
from Models.models import ActionRequest
from Patterns.Adapter import LLMAdapter
from Patterns.Adapter.McpClientAdapter import MCPClientAdapter
from Patterns.Decorator.decorators import auto_error_logger
from Patterns.Template.ErrorTemplate import AppErrors
from Utils.CustomException import APIException
from fappsetting.appDependency import *


router = APIRouter()


@auto_error_logger
@router.post("/{operation}")
async def execute(
        operation: str = Path(..., description="Operation name"),
        req: ActionRequest = Body(...),
        llm: LLMAdapter = Depends(get_llm_adapter),
        meta_data=Depends(get_request_meta)
):
    try:
        # TODO: invoke command
        result = MCPClientAdapter(meta_data["origin"]).call_tool(tool_name="execute_action", action=req)
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
