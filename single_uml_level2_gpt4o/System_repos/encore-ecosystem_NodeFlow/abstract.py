# abstract.py

from abc import ABC, abstractmethod

__all__ = ['Node', 'Adapter']

class Node(ABC):
    """To serve as an abstract base class for defining node structures in various data structures or algorithms."""
    pass

class Adapter(ABC):
    """The Adapter class serves as an abstract base class for implementing adapters that transform one type of variable to another, with capabilities to check for information loss during the transformation and to inspect the input and output variable types."""

    @abstractmethod
    def compute(self, variable):
        """This method is intended to perform a computation or transformation on the given Variable object, but it is designed to be overridden by subclasses with specific implementations."""
        pass

    def get_type_of_source_variable(self):
        """Retrieve the type annotation of the 'variable' parameter from the signature of the 'compute' method."""
        return self.compute.__annotations__.get('variable', None)

    def get_type_of_target_variable(self):
        """Determine the return type annotation of the `compute` method in the class instance."""
        return self.compute.__annotations__.get('return', None)

    def is_loses_information(self):
        """Determine whether the operation or transformation represented by the method results in a loss of information when applied to the data."""
        return False