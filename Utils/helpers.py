import os
import requests

from Patterns.Singelton.Fappmcp import Fappmcp
from Utils import consts
from Patterns.Singelton import LoggerSingelton

from functools import wraps
from pathlib import Path
from dotenv import load_dotenv
import os


def find_and_load_env(key_name, filename=consts.filename):
    current = Path(__file__).resolve()

    for parent in current.parents:
        candidate = parent / filename
        if candidate.exists():
            load_dotenv(candidate)
            kk = os.getenv(key_name)
            return kk.strip() if kk else None

    return None


def call_apifreellm(api_key, builder):
    response = requests.post(
        consts.apf_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json=builder
    )
    return response.status_code, response.json()


def build_tools_prompt():
    tools = Fappmcp.list_tools()
    lines = []
    for name in tools:
        lines.append(f"- {name}")

    return "\n".join(lines)
