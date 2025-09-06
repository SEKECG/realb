# variable.py

class Variable:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.value == other.value
        return self.value == other

    def __rshift__(self, other):
        return other.compute(self)