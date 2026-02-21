import functools
import inspect

from Patterns.Singelton import LoggerSingelton


def auto_error_logger(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        except Exception as e:
            LoggerSingelton.printer(
                "error",
                f"Exception in {func.__name__}: {str(e)}",
                exc_info=True
            )
            raise e

    return wrapper
