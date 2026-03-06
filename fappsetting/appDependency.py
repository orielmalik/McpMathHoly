from fastapi import Request
from Patterns.Adapter import LLMAdapter


def get_llm_adapter() -> LLMAdapter:
    return LLMAdapter()


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
