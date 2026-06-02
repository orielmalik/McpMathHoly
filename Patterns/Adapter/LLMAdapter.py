from Models.models import ActionRequest,  JsonRpcResponse
from Patterns.Builder import AsyncPipeline,AsyncURIBuilder
from Patterns.Factory import CommandFactory
from Patterns.Singelton import LoggerSingelton
from Patterns.Template.ErrorTemplate import AppErrors
from Utils import consts, helpers
import json
from groq import GroqError, APIStatusError, RateLimitError

from Utils.Errors import GroqErrorHandler
import asyncio
from groq import AsyncGroq

from Utils.consts import BASE_PROMPT, ACTION_PROMPT


class GroqService:
    _instances = {}

    def __new__(cls, api_keyy: str):
        if api_keyy not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[api_keyy] = instance
        return cls._instances[api_keyy]

    def __init__(self, api_keyy: str):
        if getattr(self, "_initialized", False):
            return

        self.api_key = api_keyy
        self.client = AsyncGroq(api_key=api_keyy)

        self._initialized = True

    async def safe_groq_call(self, messag, retries=3):

        for attempt in range(retries):
            try:
                return await self.client.chat.completions.create(
                    model=consts.model,
                    messages=messag
                )

            except RateLimitError:
                if attempt == retries - 1:
                    raise AppErrors.rate_limit()

                await asyncio.sleep(2 ** attempt)  # exponential backoff

            except APIStatusError as e:
                raise GroqErrorHandler.handle(e)

            except GroqError:
                raise AppErrors.internal(" server err AI")

class GroqLLMAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.groq = GroqService(api_keyy=api_key)

    async def ask(self, full_prompt) -> JsonRpcResponse:
        messages = [
            {"role": "system", "content": BASE_PROMPT + ACTION_PROMPT},
            {"role": "user",   "content": str(full_prompt)}
        ]

        llm_response = await self.groq.safe_groq_call(messages)
        llm_text = llm_response.choices[0].message.content

        LoggerSingelton.printer("INFO", f"Router response: {llm_text}")

        clean = llm_text.strip().strip("```json").strip("```").strip()

        try:
            parsed = json.loads(clean)
        except json.JSONDecodeError:
            parsed = {"tool": None, "operation": None, "message": ""}

        return JsonRpcResponse(
            jsonrpc="2.0",
            result=parsed,
            id=hash(full_prompt) % 100000
        )
    async def solve(self, full_prompt) -> JsonRpcResponse:
        messages = [
            {"role": "system", "content": "You are a math solver. Solve the problem and return only the answer as JSON: {\"result\": ...}"},
            {"role": "user",   "content": str(full_prompt)}
        ]

        llm_response = await self.groq.safe_groq_call(messages)
        llm_text = llm_response.choices[0].message.content

        LoggerSingelton.printer("INFO", f"Solver response: {llm_text}")

        clean = llm_text.strip().strip("```json").strip("```").strip()

        try:
            parsed = json.loads(clean)
        except json.JSONDecodeError:
            parsed = {"result": llm_text}

        return JsonRpcResponse(
            jsonrpc="2.0",
            result=parsed,
            id=hash(full_prompt) % 100000
        )
