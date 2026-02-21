
class AsyncPipeline:
    def __init__(self, builder: AsyncURIBuilder):
        self.builder = builder
        self.steps: List[Callable[[AsyncURIBuilder, Any], Any]] = []

    def add_step(self, step: Callable[[AsyncURIBuilder, Any], Any]):
        self.steps.append(step)

    async def run(self, initial_input: Any = None) -> Any:
        current_input = initial_input
        for step in self.steps:
            try:
                current_input = await step(self.builder, current_input)
            except Exception as e:
                print(f"Pipeline stopped at step {step.__name__}: {e}")
        return current_input
