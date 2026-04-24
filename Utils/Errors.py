class GroqError(Exception):
    def __init__(self, message, status_code=None, original_error=None):
        super().__init__(message)
        self.status_code = status_code
        self.original_error = original_error


class GroqRateLimitError(GroqError): pass
class GroqAuthError(GroqError): pass
class GroqServerError(GroqError): pass


class GroqErrorHandler:
    @staticmethod
    def handle(e):
        status_code = getattr(e, "status_code", None) or getattr(e, "status", None)

        try:
            message = e.response.json().get("error")
        except Exception:
            message = str(e)

        if status_code == 401:
            return GroqAuthError(message, status_code, e)
        elif status_code == 429:
            return GroqRateLimitError(message, status_code, e)
        elif status_code and status_code >= 500:
            return GroqServerError(message, status_code, e)

        return GroqError(message, status_code, e)