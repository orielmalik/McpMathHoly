from typing import Any
from Models.models import ActionRequest, JsonRpcRequest, JsonRpcResponse
from Patterns.Builder import AsyncURIBuilder, AsyncPipeline
from Patterns.Singelton import LoggerSingelton
from Patterns.Template.ErrorTemplate import AppErrors
from Utils import consts
import json
from groq import AsyncGroq, GroqError, APIStatusError, RateLimitError
from Utils.helpers import find_and_load_env
import asyncio


class GroqService:

    async def safe_groq_call(self, prompt, retries=3):
        for attempt in range(retries):
            try:
                return await self.client.chat.completions.create(
                    model=consts.model,
                    messages=[{"role": "user", "content": prompt}]
                )

            except RateLimitError:
                if attempt == retries - 1:
                    raise AppErrors.rate_limit()

                await asyncio.sleep(2 ** attempt)  # exponential backoff

            except APIStatusError as e:
                raise GroqErrorHandler.handle(e)

            except GroqError:
                raise AppErrors.internal(" server err AI")


class FreeLLMAdapter:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.groq = GroqService(api_key=find_and_load_env(key_name=consts.api_key))
        self.builder = AsyncURIBuilder.AsyncURIBuilder(api_url)
        self.pipeline = AsyncPipeline.AsyncPipeline(self.builder)

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
