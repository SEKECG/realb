# result.py

from nodeflow.node.variable import Variable

class Result(Variable):
    def __init__(self, value):
        if not isinstance(value, bool):
            raise ValueError("Result value must be a boolean")
        super().__init__(value)