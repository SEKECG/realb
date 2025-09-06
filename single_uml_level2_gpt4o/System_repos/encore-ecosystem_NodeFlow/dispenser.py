# dispenser.py

from nodeflow.node.variable import Variable
from nodeflow.node.function import Function
from nodeflow.converter.converter import Converter

class Dispenser:
    def __init__(self, **kwargs):
        self.variables_table = kwargs

    def __rshift__(self, other):
        if isinstance(other, Function):
            params = other.get_parameters()
            converted_params = {}
            for name, var_type in params.items():
                if name in self.variables_table:
                    variable = self.variables_table[name]
                    if isinstance(variable, var_type):
                        converted_params[name] = variable
                    else:
                        converter = Converter()
                        converted_variable = converter.convert(variable, var_type)
                        if converted_variable is not None:
                            converted_params[name] = converted_variable
                        else:
                            raise TypeError(f"Cannot convert {type(variable)} to {var_type}")
                else:
                    raise KeyError(f"Variable {name} not found in dispenser")
            return other.compute(**converted_params)
        else:
            raise TypeError("Right operand must be an instance of Function")