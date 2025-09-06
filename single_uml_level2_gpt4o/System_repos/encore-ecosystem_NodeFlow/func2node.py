# func2node.py

from nodeflow.node.function import Function
from nodeflow.node.abstract import Node

class ConvertedFunction(Function):
    def compute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method")

def func2node(func):
    class FuncNode(ConvertedFunction):
        def compute(self, *args, **kwargs):
            return func(*args, **kwargs)
    
    return FuncNode()

__all__ = ["func2node"]