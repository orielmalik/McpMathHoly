import os

from fastapi import Request
from Patterns.Adapter.LLMAdapter import FreeLLMAdapter
from dotenv import load_dotenv

load_dotenv(dotenv_path="K.ENV")


def get_llm_adapter() -> FreeLLMAdapter:
    return FreeLLMAdapter(api_key=os.environ.get("API_KEY"), api_url=os.environ.get("API_URL"))


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
