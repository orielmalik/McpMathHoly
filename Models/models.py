from pydantic import BaseModel
from typing import List, Optional, Any


class ToolCall(BaseModel):
    tool_name: str
    operation: Optional[str] = None
    args: dict = {}


class ActionRequest(BaseModel):
    type: str
    message: str
    timestamp: Optional[str] = None

class JsonRpcError(BaseModel):
    code: int
    message: str


class JsonRpcResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[ToolCall | dict | str] = None
    error: Optional[JsonRpcError] = None
    id: int | str | None = None


class JsonRpcRequest(BaseModel):
    jsonrpc: str
    method: str
    params: ActionRequest
    id: int | str

class Action(BaseModel):
    name: str
    operation: str
    payload: ActionRequest
