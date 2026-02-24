from fastapi import Request
from fastapi.responses import JSONResponse
from Patterns.Template.ErrorTemplate import APIException
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from Utils.consts import allow, apptitle

app = FastAPI(title=apptitle)
mcpapp=FastMCP()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow,
    allow_methods=allow,
    allow_headers=allow
)


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "code": exc.error_code
        }
    )
