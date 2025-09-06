# numeric.py

from nodeflow.node.variable import Variable

class Integer(Variable):
    def __init__(self, value):
        super().__init__(value)

    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value * other.value)
        return NotImplemented

class Float(Variable):
    def __init__(self, value):
        super().__init__(value)

    def __add__(self, other):
        if isinstance(other, Float):
            return Float(self.value + other.value)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Float):
            return Float(self.value * other.value)
        return NotImplemented

class Boolean(Variable):
    def __init__(self, value):
        super().__init__(value)

    def __add__(self, other):
        if isinstance(other, Boolean):
            return Boolean(self.value or other.value)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Boolean):
            return Boolean(self.value and other.value)
        return NotImplemented

__all__ = ['Integer', 'Float', 'Boolean']