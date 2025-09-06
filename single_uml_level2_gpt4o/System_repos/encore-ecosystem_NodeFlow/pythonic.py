# pythonic.py

from nodeflow.node.variable import Variable
from nodeflow.builtin.variables.numeric import Boolean, Integer, Float
from nodeflow.adapter.abstract import Adapter

class Boolean2bool(Adapter):
    def compute(self, variable):
        return variable.value

class Float2float(Adapter):
    def compute(self, variable):
        return variable.value

class Integer2int(Adapter):
    def compute(self, variable):
        return variable.value

class PythonicAdapter(Adapter):
    def is_loses_information(self):
        return False

class bool2Boolean(PythonicAdapter):
    def compute(self, variable):
        return Boolean(variable)

class float2Float(PythonicAdapter):
    def compute(self, variable):
        return Float(variable)

class int2Integer(PythonicAdapter):
    def compute(self, variable):
        return Integer(variable)