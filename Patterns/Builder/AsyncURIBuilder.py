from datetime import datetime
from typing import Any, Dict, Optional, Callable, List

from httpx import URL

from Patterns.Singelton.AsyncSingelton import AsyncClientSingleton


class AsyncURIBuilder:
    def __init__(self, base_url: str):
        self.base_url = URL(base_url)
        self.client = AsyncClientSingleton.get_client(base_url)

    async def request(
        self,
        endpoint: str,
        method: str,
        path_vars: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if path_vars:
            for k, v in path_vars.items():
                placeholder = f"{{{k}}}"
                if placeholder in endpoint:
                    endpoint = endpoint.replace(placeholder, str(v))
                else:
                    raise ValueError(f"Path variable '{k}' not found in endpoint")

        url = self.base_url / endpoint

        # Query params
        if query_params:
            url = url.with_query(query_params)

        # Send request
        response = await self.client.request(method=method, url=url, json=json_body)
        response.raise_for_status()
        data = response.json()

        # Logging
        self.log_request(url, method, json_body, data)
        return data

    def log_request(self, url, method, body, response_data):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": method,
            "url": str(url),
            "body": body,
            "response": response_data
        }
        #print(json.dumps(log_entry, ensure_ascii=False))
