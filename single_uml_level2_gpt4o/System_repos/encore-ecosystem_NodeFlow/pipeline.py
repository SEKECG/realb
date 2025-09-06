# pipeline.py

from nodeflow.adapter.abstract import Adapter
from nodeflow.node.variable import Variable

class Pipeline:
    def __init__(self):
        self._loose_information = False
        self._pipeline = []

    def add_adapter(self, adapter):
        if self._pipeline:
            last_adapter = self._pipeline[-1]
            if last_adapter.get_type_of_target_variable() != adapter.get_type_of_source_variable():
                raise TypeError("Incompatible adapter types")
            self._loose_information = self._loose_information or adapter.is_loses_information()
        self._pipeline.append(adapter)

    def compute(self, variable):
        for adapter in self._pipeline:
            variable = adapter.compute(variable)
        return variable

    def get_type_of_source_variable(self):
        if not self._pipeline:
            return None
        return self._pipeline[0].get_type_of_source_variable()

    def get_type_of_target_variable(self):
        if not self._pipeline:
            return None
        return self._pipeline[-1].get_type_of_target_variable()

    def is_loses_information(self):
        return self._loose_information