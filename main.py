from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List

from Patterns.Singelton import LoggerSingelton
from Utils.consts import allow
from Patterns.Decorator.decorators import auto_error_logger
from Patterns.Template.ErrorTemplate import AppErrors

# ייבוא ה-FastMCP שלך
from Impl.mcpserver import mcp_server

app = FastAPI(title="MCP Math Tools Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow,
    allow_methods=allow,
    allow_headers=allow
)


class ActionRequest(BaseModel):
    type: str
    message: List[Dict[str, Any]] | Dict[str, Any] | str | None = None
    timestamp: str | None = None


@app.post("/action")
@auto_error_logger
async def execute(req: ActionRequest):
    """
    נקודת הכניסה היחידה – כל פעולה (tool call) עוברת דרך כאן
    ומעבירה ישירות ל-FastMCP
    """
    try:
        result = mcp_server.invoke_action({
            "type": req.type,
            "message": req.message,
            "timestamp": req.timestamp
        })
        return {
            "success": True,
            "type": req.type,
            "result": result
        }

    except ValueError as ve:
        # שגיאות מהסוג "action type לא מוכר" או ולידציה
        raise AppErrors.bad_request(str(ve))

    except Exception as e:
        LoggerSingelton.printer("ERROR", f"Action failed: {str(e)}")
        raise AppErrors.internal()


# אם אתה רוצה גם endpoint לבדיקת חיים / מה זמין
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "mcp_server": mcp_server.name,
        "tools_available": list(mcp_server.tools.keys())   # רשימת שמות ה-tools
    }


if __name__ == "__main__":
    import uvicorn
    LoggerSingelton.printer("INFO", "Starting MCP server...")
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)