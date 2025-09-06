# utils.py

from collections.abc import Mapping
from typing import Iterator

class Frozen:
    __slots__ = ['mapping']

    def __init__(self, mapping):
        self.mapping = mapping

    def __contains__(self, key):
        return key in self.mapping

    def __getitem__(self, key):
        return self.mapping[key]

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mapping!r})"

class FrozenDict(Frozen):
    pass

K = None
V = None