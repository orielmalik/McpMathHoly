from Models.models import ActionRequest
from Patterns.Factory.StrategyFactory import StrategyFactory
from Patterns.Strategy.MathContext import Context
from abc import ABC, abstractmethod


class OperationCommand(ABC):
    @abstractmethod
    def invoke(self, req: ActionRequest):
        pass


class MathCommand(OperationCommand):
    def invoke(self, req: ActionRequest):
        return Context(StrategyFactory.create(req.type)).run(req.message)
