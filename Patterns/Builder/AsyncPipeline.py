from typing import Callable, Any

from Patterns.Builder import AsyncURIBuilder
from Patterns.Singelton import LoggerSingelton


class AsyncPipeline:
    def __init__(self, builder: AsyncURIBuilder):
        self.builder = builder
        self.steps: list[Callable[[AsyncURIBuilder, Any], Any]] = []

    def add_step(self, step: Callable[[AsyncURIBuilder, Any], Any]):
        self.steps.append(step)
        return self

    async def run(self, initial_input: Any = None) -> Any:
        current = initial_input

        for i, step in enumerate(self.steps, 1):
            try:
                current = await step(self.builder, current)
                LoggerSingelton.printer("DEBUG", f"Pipeline step {i} completed")
            except Exception as exc:
                LoggerSingelton.printer("ERROR", f"Pipeline failed at step {i}: {exc!r}")
                raise

        return current
