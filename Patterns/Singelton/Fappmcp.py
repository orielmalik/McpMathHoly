# Patterns/Singelton/FastMCPSingleton.py
from fastmcp import FastMCP
from Utils.consts import mcptitle


class FastMCPSingleton:
    _instance: FastMCP | None = None

    @classmethod
    def get_instance(cls) -> FastMCP:
        if cls._instance is None:
            cls._instance = FastMCP(name=mcptitle)
        return cls._instance