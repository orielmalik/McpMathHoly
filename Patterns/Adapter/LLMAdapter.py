from typing import Any
from Models.models import ActionRequest, JsonRpcRequest, JsonRpcResponse
from Patterns.Builder import AsyncURIBuilder, AsyncPipeline
from Patterns.Singelton import LoggerSingelton
from Utils import consts
import json

class FreeLLMAdapter:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.builder = AsyncURIBuilder.AsyncURIBuilder(api_url)
        self.pipeline = AsyncPipeline.AsyncPipeline(self.builder)
        self.pipeline.add_step(self._send_request)

    async def _send_request(self, builder: AsyncURIBuilder, payload: dict):
        response = await builder.request(
            method="POST",
            endpoint="",
            json_body=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        if "text" not in response:
            raise Exception(f"LLM returned invalid response: {response}")
        return response["text"]

    async def ask(self, action: ActionRequest) -> JsonRpcResponse:
        user_messages = "\n".join(action.message or [])
        full_prompt = f"""
    {consts.SYSTEM_PROMPT}
    Action Type: {action.type}
    Messages:
    {user_messages}
    
    {consts.DEFAULT_PROMPT}
    """
        payload = {
            "prompt": full_prompt
        }
        LoggerSingelton.printer("DEBUG", f"Sending prompt to LLM: {payload}")
        llm_text = await self.pipeline.run(payload)

        try:
            parsed = json.loads(llm_text)
            if not isinstance(parsed, dict):
                raise ValueError("Parsed response is not a dict")
            return JsonRpcResponse(
                jsonrpc="2.0",
                result=parsed,
                id=action.timestamp or 1
            )
        except json.JSONDecodeError:
            return JsonRpcResponse(
                jsonrpc="2.0",
                error=None,
                result={"text": llm_text},
                id=action.timestamp or 1
            )