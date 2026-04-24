import os
from fastapi import Request
from Patterns.Adapter.LLMAdapter import GroqLLMAdapter
from Utils.helpers import find_and_load_env


def get_llm_adapter() -> GroqLLMAdapter:
    return GroqLLMAdapter(api_key=find_and_load_env(key_name="API_KEY",filename="k.env"))


def get_request_meta(request: Request):
    return {
        "origin": request.headers.get("origin"),
        "user_agent": request.headers.get("user-agent"),
        "ip": request.client.host
    }


def get_runtime_context(request: Request):
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    origin = request.headers.get("origin")
    return {"base_url": base_url, "origin": origin}
