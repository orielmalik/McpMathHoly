from datetime import datetime
from typing import Any, Dict, Optional, Callable

from httpx import URL, Response

from Patterns.Decorator.decorators import auto_error_logger
from Patterns.Singelton import LoggerSingelton
from Patterns.Singelton.AsyncClientSingelton import AsyncClientSingleton


class AsyncURIBuilder:
    def __init__(self, base_url: str):
        self.base_url = URL(base_url.rstrip("/"))
        self.client = AsyncClientSingleton.get_client(base_url)

    @auto_error_logger
    async def request(
            self,
            method: str,
            endpoint: str,
            path_vars: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = None,
            json_body: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        if path_vars:
            for key, value in path_vars.items():
                placeholder = f"{{{key}}}"
                if placeholder in endpoint:
                    endpoint = endpoint.replace(placeholder, str(value))
                else:
                    raise ValueError(f"Path variable '{key}' not found in endpoint: {endpoint}")

        full_url = self.base_url.join(URL(endpoint.lstrip("/")))

        if query_params:
            full_url = full_url.with_query(query_params)

        response: Response = await self.client.request(
            method=method.upper(),
            url=full_url,
            json=json_body,
            headers=headers
        )

        LoggerSingelton.printer(
            "INFO",
            f"{method.upper()} {full_url} | body={json_body} | status={response.status_code}"
        )

        response.raise_for_status()

        try:
            data = response.json()
        except Exception:
            data = {"raw_content": response.text[:200] + "..."}

        return data


