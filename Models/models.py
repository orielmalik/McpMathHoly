from pydantic import BaseModel
from typing import List, Optional, Any


class ActionRequest(BaseModel):
    type: str
    message: Optional[List[str]] = None
    timestamp: Optional[str] = None


class JsonRpcRequest(BaseModel):
    jsonrpc: str
    method: str
    params: ActionRequest
    id: int | str


class JsonRpcError(BaseModel):
    code: int
    message: str


class JsonRpcResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Any | None = None
    error: JsonRpcError | None = None
    id: int | str | None = None