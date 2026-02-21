from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class APIException(Exception):
    def __init__(self, status_code: int, message: str, error_code: str):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
        super().__init__(message)


#@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "code": exc.error_code
        }
    )