import pyproj
import xarray as xr
from xarray import Index

class CRSIndex(Index):
    def __init__(self, crs):
        self.crs = pyproj.CRS.from_user_input(crs)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.crs})"

    def _repr_inline_(self, max_width):
        crs_str = str(self.crs)
        if len(crs_str) > max_width:
            return crs_str[:max_width - 3] + "..."
        return crs_str

    @property
    def crs(self):
        return self._crs

    @crs.setter
    def crs(self, value):
        self._crs = pyproj.CRS.from_user_input(value)

    def equals(self, other):
        if not isinstance(other, CRSIndex):
            return False
        return self.crs == other.crs

    @classmethod
    def from_variables(cls, variables, options):
        if len(variables) != 1:
            raise ValueError("CRSIndex can only be created from a single scalar variable.")
        crs = options.get("crs", variables[0].attrs.get("crs"))
        if crs is None:
            raise ValueError("CRS must be provided either in options or variable attributes.")
        return cls(crs)

def _format_crs(crs, max_width):
    crs_str = str(crs)
    if len(crs_str) > max_width:
        return crs_str[:max_width - 3] + "..."
    return crs_str