from typing import List, Union

from Models.models import ActionRequest
from Patterns.Factory.StrategyFactory import StrategyFactory
from Patterns.Strategy.MathContext import Context
from abc import ABC, abstractmethod


class OperationCommand(ABC):
    @abstractmethod
    def invoke(self, req: ActionRequest):
        pass


def normalize_message(message: Union[str, List[str], None]) -> List[str]:
    if message is None:
        return []
    if isinstance(message, list):
        return message
    return [message]


class MathCommand(OperationCommand):
    def invoke(self, req: ActionRequest):
        return Context(StrategyFactory.create(req.type.removeprefix("math_"))).run(normalize_message(req.message))
