import json
from pathlib import Path
from typing import Dict, Any
import json
from typing import List
from Models.models import ActionRequest
from dotenv import load_dotenv
import os

ALLOWED_TOOLS = {"math", "physics", "cs"}


def enforce_llm_output(raw: Any) -> Dict:
    if isinstance(raw, dict) and "result" in raw:
        raw = raw["result"]

    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return {
                "tool_name": None,
                "args": {},
                "final_answer": raw,
                "status": "fallback_text"
            }
    if not isinstance(raw, dict):
        return {
            "tool_name": None,
            "args": {},
            "final_answer": str(raw),
            "status": "invalid_type_fallback"
        }

    tool = raw.get("tool_name")
    args = raw.get("args") or {}
    action = raw.get("action")
    operation = raw.get("operation")
    final = raw.get("final_answer")

    if tool is None and action:
        raw["tool_name"] = None  # router stage
        raw["args"] = args
        return raw

    # 6️⃣ enforce allowed tools
    if tool is not None and tool not in ALLOWED_TOOLS:
        return {
            "tool_name": None,
            "args": {},
            "final_answer": f"INVALID TOOL BLOCKED: {tool}",
            "status": "blocked_tool"
        }
    # 7️⃣ ensure structure completeness
    return {
        "tool_name": tool,
        "args": args,
        "final_answer": final,
        "status": "ok"
    }


def finalize_response(action: str, args: dict, result):
    return {
        "action": action,
        "args": args,
        "result": result
    }


def get_project_root():
    current = Path(__file__).resolve()

    for parent in [current] + list(current.parents):
        if (parent / ".git").exists() or (parent / "pyproject.toml").exists():
            return parent

    return current.parents[-1]


def find_and_load_env(key_name: str, filename: str = "k.env"):
    root = get_project_root()
    env_path = root / filename

    if not env_path.exists():
        raise FileNotFoundError(f"{filename} not found in project root: {root}")

    load_dotenv(env_path)

    value = os.getenv(key_name)
    if not value:
        raise ValueError(f"{key_name} not found in {filename}")

    return value.strip()


def build_router_prompt(domain: str | None = None) -> str:
    base = """
You are a deterministic MCP routing engine.

Your ONLY job is to:
- understand the user request
- select the correct tool
- extract structured arguments

You MUST NOT:
- compute results
- solve math
- produce final answers
- explain anything

OUTPUT MUST BE VALID JSON ONLY:

{
  "tool_name": "math | physics | cs | null",
  "operation": string,
  "args": object
}

RULES:
- If no tool is needed → tool_name = null
- NEVER hallucinate tools
- NEVER return text outside JSON
"""

    context = ""

    if domain == "math":
        context = "\nDomain focus: mathematical reasoning, algebra, calculus."

    elif domain == "physics":
        context = "\nDomain focus: physical modeling, formulas, mechanics."

    elif domain == "cs":
        context = "\nDomain focus: algorithms, data structures, computation."

    return base + context


def normalize_router_output(parsed: object) -> object:
    if isinstance(parsed, dict):
        if "action" in parsed:
            return parsed

        if "tool_name" in parsed:
            return parsed

        if "tool" in parsed and "operation" in parsed:
            return parsed

        if "text" in parsed:
            return {
                "tool": None,
                "operation": None,
                "message": parsed["text"]
            }

    raise ValueError(f"Unknown LLM format: {parsed}")

def load_actions_from_json(path: str):
    with open(path, "r") as f:
        return json.load(f)


def action_to_string(action: ActionRequest) -> str:
    msg = action.message

    if isinstance(msg, list):
        msg = " ".join(map(str, msg))

    elif isinstance(msg, dict):
        msg = json.dumps(msg)

    else:
        msg = str(msg)

    return f"{action.type}: {msg}"


def build_user_prompt(action):
    msg = ""
    typ = ""

    if hasattr(action, "message"):
        msg = action.message
        typ = getattr(action, "type", "")
    elif isinstance(action, dict):
        msg = action.get("message", "")
        typ = action.get("type", "")
    else:
        msg = action
        typ = ""

    if isinstance(msg, (list, dict)):
        try:
            msg = json.dumps(msg, ensure_ascii=False)
        except Exception:
            msg = str(msg)
    elif msg is None:
        msg = ""
    else:
        msg = str(msg)

    prefix = f"{typ}: " if typ else ""
    content = f"{prefix}{msg}".strip()

    return content if content else "Empty message content"


def action_to_prompt(action: ActionRequest) -> str:
    msg = action.message

    if isinstance(msg, list):
        msg = " ".join(map(str, msg))

    return f"{action.type}: {msg}"

def normalize_router_output(parsed: object) -> object:
    if isinstance(parsed, dict):
        if "action" in parsed:
            return parsed

        if "tool_name" in parsed:
            return parsed

        if "tool" in parsed and "operation" in parsed:
            return parsed

        if "text" in parsed:
            return {
                "tool": None,
                "operation": None,
                "message": parsed["text"]
            }

    raise ValueError(f"Unknown LLM format: {parsed}")