from typing import List

from Models.models import ActionRequest
from Patterns.Command.Commands import OperationCommand, MathCommand
from Patterns.Singelton import LoggerSingelton


class CommandFactory:
    @staticmethod
    def invoke(action_type: str, req: ActionRequest) -> OperationCommand:
        if action_type.startswith("math_"):
            return MathCommand().invoke(req)
        else:
            return None
