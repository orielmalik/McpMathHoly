from typing import Optional

import httpx


class AsyncClientSingleton:
    _client: Optional[httpx.AsyncClient] = None

    @classmethod
    def get_client(cls, base_url: str) -> httpx.AsyncClient:
        if cls._client is None:
            cls._client = httpx.AsyncClient(base_url=base_url)
        return cls._client

    @classmethod
    async def close_client(cls):
        if cls._client:
            await cls._client.aclose()
            cls._client = None
