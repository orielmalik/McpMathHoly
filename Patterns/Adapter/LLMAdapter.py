from Patterns.Builder import AsyncURIBuilder, AsyncPipeline
from Patterns.Singelton import LoggerSingelton


class FreeLLMAdapter:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.builder = AsyncURIBuilder(api_url)
        self.pipeline = AsyncPipeline(self.builder)
        self.pipeline.add_step(self._send_request)

    async def _send_request(self, builder: AsyncURIBuilder, prompt: str):
        response = await builder.request(
            method="POST",
            endpoint="",
            json_body={"prompt": prompt},
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        if "text" not in response:
            raise Exception(f"LLM returned invalid response: {response}")
        return response["text"]

    async def ask(self, prompt: str) -> str:
        result = await self.pipeline.run(prompt)
        return result
