from pathlib import Path

class PathVariable:
    def __init__(self, value):
        if not isinstance(value, Path):
            raise TypeError("value must be a pathlib.Path instance")
        self.value = value.resolve()

    def __truediv__(self, other):
        if not isinstance(other, (str, Path)):
            raise TypeError("other must be a string or pathlib.Path instance")
        return self.value / other