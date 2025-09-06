# nodeflow/node/function.py

from collections import OrderedDict
from typing import Type

from nodeflow.node.variable import Variable

class Function:
    def compute(self, *args, **kwargs) -> Variable:
        raise NotImplementedError("Subclasses should implement this method")

    def get_parameters(self) -> OrderedDict[str, Type[Variable]]:
        from inspect import signature
        sig = signature(self.compute)
        return OrderedDict((name, param.annotation) for name, param in sig.parameters.items())

    def get_return_type(self) -> Type[Variable]:
        from inspect import signature
        sig = signature(self.compute)
        return sig.return_annotation